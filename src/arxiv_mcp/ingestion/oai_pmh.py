"""OAI-PMH harvester for arXiv metadata.

Provides bulk and incremental harvesting via oaipmh-scythe,
with category filtering, batch upsert, and checkpoint management.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

import structlog
from oaipmh_scythe import Scythe
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Paper
from arxiv_mcp.ingestion.mapper import map_to_paper
from arxiv_mcp.ingestion.parsers import parse_arxiv_raw

logger = structlog.get_logger(__name__)

# Default checkpoint file location
DEFAULT_CHECKPOINT_PATH = Path("data/harvest_checkpoint.json")


@dataclass
class HarvestResult:
    """Statistics from a harvest operation."""

    total_fetched: int = 0
    total_inserted: int = 0
    total_updated: int = 0
    total_skipped: int = 0
    checkpoint_date: date | None = None
    duration_seconds: float = 0.0


class OAIPMHHarvester:
    """OAI-PMH harvester using oaipmh-scythe.

    Supports bulk and incremental harvesting with:
    - Automatic resumption token handling (via scythe)
    - Category filtering against configured subset
    - Batch upsert with ON CONFLICT deduplication
    - Datestamp-based checkpoint for incremental harvests
    """

    def __init__(
        self,
        settings: Settings,
        session_factory: async_sessionmaker[AsyncSession] | None = None,
        checkpoint_path: Path | None = None,
    ):
        self.settings = settings
        self.session_factory = session_factory
        self.checkpoint_path = checkpoint_path or DEFAULT_CHECKPOINT_PATH
        self._configured_categories: set[str] | None = None

    @property
    def configured_categories(self) -> set[str]:
        """Load configured categories lazily."""
        if self._configured_categories is None:
            try:
                self._configured_categories = set(self.settings.configured_categories)
            except Exception:
                # If categories file is missing, accept all
                self._configured_categories = set()
        return self._configured_categories

    def _matches_categories(self, paper_categories: str) -> bool:
        """Check if any of the paper's categories match the configured set.

        If no categories are configured, all papers are accepted.
        """
        if not self.configured_categories:
            return True

        paper_cats = paper_categories.split() if paper_categories else []
        return bool(set(paper_cats) & self.configured_categories)

    async def harvest_bulk(
        self,
        archive_set: str | None = None,
        from_date: date | str | None = None,
        metadata_prefix: str = "arXivRaw",
        batch_size: int = 100,
        progress_callback: Callable | None = None,
    ) -> HarvestResult:
        """Bulk harvest via OAI-PMH with resumption token handling.

        Args:
            archive_set: OAI-PMH set to harvest (e.g., 'cs').
            from_date: Start date for harvest (ISO format or date object).
            metadata_prefix: OAI-PMH metadata format (default arXivRaw).
            batch_size: Number of papers per DB flush.
            progress_callback: Optional callback(count) for progress updates.

        Returns:
            HarvestResult with harvest statistics.
        """
        start_time = time.monotonic()
        result = HarvestResult()
        batch: list[Paper] = []
        latest_datestamp: str | None = None

        # Build OAI-PMH parameters
        params: dict = {"metadataPrefix": metadata_prefix}
        if archive_set:
            params["set"] = archive_set
        if from_date:
            if isinstance(from_date, date):
                params["from"] = from_date.isoformat()
            else:
                params["from"] = str(from_date)

        with Scythe(self.settings.arxiv_oai_url) as scythe:
            records = scythe.list_records(**params)

            for record in records:
                result.total_fetched += 1

                try:
                    # Parse the record metadata
                    raw = parse_arxiv_raw(record.metadata)

                    # Category filtering
                    if not self._matches_categories(raw.categories):
                        result.total_skipped += 1
                        continue

                    # Map to Paper
                    paper = map_to_paper(raw)

                    # Track OAI datestamp for checkpoint
                    if hasattr(record.header, "datestamp") and record.header.datestamp:
                        paper.oai_datestamp = date.fromisoformat(record.header.datestamp)
                        if latest_datestamp is None or record.header.datestamp > latest_datestamp:
                            latest_datestamp = record.header.datestamp

                    batch.append(paper)

                    # Flush batch when full
                    if len(batch) >= batch_size:
                        await self._upsert_batch(batch)
                        batch = []

                    if progress_callback:
                        progress_callback(result.total_fetched)

                except Exception as exc:
                    logger.warning(
                        "Failed to parse record",
                        error=str(exc),
                        record_count=result.total_fetched,
                    )
                    result.total_skipped += 1

        # Flush remaining batch
        if batch:
            await self._upsert_batch(batch)

        if latest_datestamp:
            try:
                result.checkpoint_date = date.fromisoformat(latest_datestamp)
            except ValueError:
                pass

        result.duration_seconds = time.monotonic() - start_time

        logger.info(
            "Harvest complete",
            total_fetched=result.total_fetched,
            total_inserted=result.total_inserted,
            total_updated=result.total_updated,
            total_skipped=result.total_skipped,
            duration=f"{result.duration_seconds:.1f}s",
        )

        return result

    async def harvest_incremental(self) -> HarvestResult:
        """Incremental harvest since last checkpoint.

        Reads the checkpoint file for the last harvested datestamp,
        then runs a bulk harvest from that date. Saves a new checkpoint
        after successful completion.

        Returns:
            HarvestResult with harvest statistics.
        """
        from_date: str | None = None

        # Read checkpoint
        if self.checkpoint_path.exists():
            try:
                checkpoint = json.loads(self.checkpoint_path.read_text())
                from_date = checkpoint.get("last_datestamp")
                logger.info("Resuming from checkpoint", from_date=from_date)
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Failed to read checkpoint", error=str(exc))

        # Run harvest
        result = await self.harvest_bulk(from_date=from_date)

        # Save new checkpoint
        if result.checkpoint_date:
            self._save_checkpoint(result.checkpoint_date)

        return result

    def _save_checkpoint(self, datestamp: date) -> None:
        """Save harvest checkpoint to JSON file."""
        checkpoint = {
            "last_datestamp": datestamp.isoformat(),
            "last_run": datetime.now(UTC).isoformat(),
        }
        try:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            self.checkpoint_path.write_text(json.dumps(checkpoint, indent=2))
            logger.info("Checkpoint saved", datestamp=datestamp.isoformat())
        except OSError as exc:
            logger.error("Failed to save checkpoint", error=str(exc))

    async def _upsert_batch(self, papers: list[Paper]) -> None:
        """Batch upsert using ON CONFLICT DO UPDATE.

        Uses PostgreSQL's INSERT ... ON CONFLICT to handle cross-listed
        paper deduplication. Updates metadata fields but preserves
        processing_tier, promotion_reason, source, and fetched_at.

        Args:
            papers: List of Paper instances to upsert.
        """
        if not papers or self.session_factory is None:
            return

        async with self.session_factory() as session:
            for paper in papers:
                values = {
                    "arxiv_id": paper.arxiv_id,
                    "title": paper.title,
                    "authors_text": paper.authors_text,
                    "abstract": paper.abstract,
                    "submitter": paper.submitter,
                    "comments": paper.comments,
                    "journal_ref": paper.journal_ref,
                    "report_no": paper.report_no,
                    "categories": paper.categories,
                    "primary_category": paper.primary_category,
                    "category_list": paper.category_list,
                    "msc_class": paper.msc_class,
                    "acm_class": paper.acm_class,
                    "doi": paper.doi,
                    "submitted_date": paper.submitted_date,
                    "updated_date": paper.updated_date,
                    "announced_date": paper.announced_date,
                    "oai_datestamp": paper.oai_datestamp,
                    "license_uri": paper.license_uri,
                    "latest_version": paper.latest_version,
                    "version_history": paper.version_history,
                    "processing_tier": paper.processing_tier,
                    "source": paper.source,
                    "fetched_at": paper.fetched_at,
                    "last_metadata_update": datetime.now(UTC),
                }

                stmt = pg_insert(Paper).values(**values)
                stmt = stmt.on_conflict_do_update(
                    index_elements=["arxiv_id"],
                    set_={
                        "title": stmt.excluded.title,
                        "authors_text": stmt.excluded.authors_text,
                        "abstract": stmt.excluded.abstract,
                        "submitter": stmt.excluded.submitter,
                        "comments": stmt.excluded.comments,
                        "journal_ref": stmt.excluded.journal_ref,
                        "report_no": stmt.excluded.report_no,
                        "categories": stmt.excluded.categories,
                        "primary_category": stmt.excluded.primary_category,
                        "category_list": stmt.excluded.category_list,
                        "msc_class": stmt.excluded.msc_class,
                        "acm_class": stmt.excluded.acm_class,
                        "doi": stmt.excluded.doi,
                        "submitted_date": stmt.excluded.submitted_date,
                        "updated_date": stmt.excluded.updated_date,
                        "announced_date": stmt.excluded.announced_date,
                        "oai_datestamp": stmt.excluded.oai_datestamp,
                        "license_uri": stmt.excluded.license_uri,
                        "latest_version": stmt.excluded.latest_version,
                        "version_history": stmt.excluded.version_history,
                        "last_metadata_update": stmt.excluded.last_metadata_update,
                        # DO NOT overwrite: processing_tier, promotion_reason, source, fetched_at
                    },
                )
                await session.execute(stmt)

            await session.commit()

        logger.debug("Batch upserted", count=len(papers))
