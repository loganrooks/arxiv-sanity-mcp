"""EnrichmentService: orchestrates enrichment resolution, storage, and cooldown.

Provides single-paper and batch enrichment workflows, cooldown enforcement,
processing tier promotion, and aggregate statistics. Wires the EnrichmentAdapter
(from openalex.py) into PaperEnrichment DB storage with upsert semantics.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import structlog
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    Paper,
    PaperEnrichment,
    ProcessingTier,
)
from arxiv_mcp.enrichment.models import EnrichmentResult, EnrichmentStatus
from arxiv_mcp.enrichment.openalex import OpenAlexAdapter

logger = structlog.get_logger(__name__)


class EnrichmentService:
    """Orchestrates enrichment workflows: enrich, store, promote.

    Constructor follows the same DI pattern as CollectionService:
    session_factory + settings + optional adapter injection (for testing).
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        adapter=None,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.adapter = adapter or OpenAlexAdapter(settings)

    # ------------------------------------------------------------------
    # Single-paper enrichment
    # ------------------------------------------------------------------

    async def enrich_paper(
        self, arxiv_id: str, refresh: bool = False
    ) -> EnrichmentResult:
        """Enrich a single paper via the configured adapter.

        Steps:
        1. Verify paper exists in DB (raise ValueError if not).
        2. Check cooldown (skip if within window, unless refresh=True).
        3. Call adapter.enrich([arxiv_id]).
        4. Upsert PaperEnrichment record.
        5. On success/partial: update Paper.openalex_id, Paper.doi (if null),
           and promote processing_tier to ENRICHED.
        6. Return the EnrichmentResult.
        """
        async with self.session_factory() as session:
            # 1. Verify paper exists
            paper = await session.get(Paper, arxiv_id)
            if paper is None:
                raise ValueError(f"Paper '{arxiv_id}' not found in database")

            # 2. Check cooldown
            if not refresh:
                existing = await session.get(PaperEnrichment, arxiv_id)
                if existing is not None:
                    cooldown_threshold = datetime.now(timezone.utc) - timedelta(
                        days=self.settings.enrichment_cooldown_days
                    )
                    if existing.last_attempted_at and existing.last_attempted_at >= cooldown_threshold:
                        logger.info(
                            "enrichment_skipped_cooldown",
                            arxiv_id=arxiv_id,
                            last_attempted=existing.last_attempted_at.isoformat(),
                        )
                        return EnrichmentResult(
                            status=existing.status,
                            openalex_id=existing.openalex_id,
                            doi=existing.doi,
                            cited_by_count=existing.cited_by_count,
                            fwci=existing.fwci,
                            api_version=existing.api_version or "",
                        )

            # 3. Call adapter
            results = await self.adapter.enrich([arxiv_id])
            result = results[0]

            # 4. Upsert PaperEnrichment
            now = datetime.now(timezone.utc)
            await self._upsert_enrichment(session, arxiv_id, result, now)

            # 5. Update Paper columns on success/partial
            if result.status in (EnrichmentStatus.SUCCESS, EnrichmentStatus.PARTIAL):
                await self._promote_paper(session, paper, result)

            await session.commit()
            return result

    # ------------------------------------------------------------------
    # Collection-scoped batch enrichment
    # ------------------------------------------------------------------

    async def enrich_collection(
        self,
        slug: str,
        refresh: bool = False,
        dry_run: bool = False,
    ) -> dict:
        """Enrich all unenriched papers in a collection.

        Returns summary dict with keys: total, enriched, not_found,
        errors, skipped_cooldown, to_enrich (dry_run only).
        """
        async with self.session_factory() as session:
            # Get all paper IDs in collection
            stmt = (
                select(CollectionPaper.paper_id)
                .join(Collection, CollectionPaper.collection_id == Collection.id)
                .where(Collection.slug == slug)
            )
            rows = await session.execute(stmt)
            all_ids = [r[0] for r in rows.all()]

            # Filter out papers within cooldown
            eligible, skipped = await self._filter_cooldown(session, all_ids, refresh)

            if dry_run:
                return {
                    "total": len(all_ids),
                    "to_enrich": len(eligible),
                    "skipped_cooldown": len(skipped),
                }

        # Enrich eligible papers
        return await self._batch_enrich(eligible, skipped)

    # ------------------------------------------------------------------
    # Search-scoped batch enrichment
    # ------------------------------------------------------------------

    async def enrich_search(
        self,
        query: str,
        limit: int = 20,
        refresh: bool = False,
        dry_run: bool = False,
    ) -> dict:
        """Run search and enrich resulting papers.

        Uses SearchService to find papers, then enriches up to `limit`.
        """
        from arxiv_mcp.search.service import SearchService

        search_svc = SearchService(self.session_factory, self.settings)
        search_results = await search_svc.search_papers(
            query_text=query, page_size=min(limit, self.settings.max_page_size)
        )

        arxiv_ids = [r.paper.arxiv_id for r in search_results.items][:limit]

        if not arxiv_ids:
            return {"total": 0, "enriched": 0, "not_found": 0, "errors": 0, "skipped_cooldown": 0}

        async with self.session_factory() as session:
            eligible, skipped = await self._filter_cooldown(session, arxiv_ids, refresh)

        if dry_run:
            return {
                "total": len(arxiv_ids),
                "to_enrich": len(eligible),
                "skipped_cooldown": len(skipped),
            }

        return await self._batch_enrich(eligible, skipped)

    # ------------------------------------------------------------------
    # Status / stats
    # ------------------------------------------------------------------

    async def get_enrichment_status(self, arxiv_id: str) -> PaperEnrichment | None:
        """Get enrichment record for a paper, or None if not enriched."""
        async with self.session_factory() as session:
            return await session.get(PaperEnrichment, arxiv_id)

    async def get_enrichment_stats(self) -> dict:
        """Get aggregate enrichment statistics.

        Returns dict with keys: total, success, not_found, partial,
        error, last_enrichment.
        """
        async with self.session_factory() as session:
            # Total count
            total_stmt = select(func.count()).select_from(PaperEnrichment)
            total = (await session.execute(total_stmt)).scalar() or 0

            # Count by status
            status_stmt = select(
                PaperEnrichment.status,
                func.count().label("cnt"),
            ).group_by(PaperEnrichment.status)
            status_rows = (await session.execute(status_stmt)).all()
            status_counts = {row[0]: row[1] for row in status_rows}

            # Last enrichment
            last_stmt = select(func.max(PaperEnrichment.enriched_at))
            last_enrichment = (await session.execute(last_stmt)).scalar()

            return {
                "total": total,
                "success": status_counts.get("success", 0),
                "not_found": status_counts.get("not_found", 0),
                "partial": status_counts.get("partial", 0),
                "error": status_counts.get("error", 0),
                "last_enrichment": last_enrichment,
            }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _upsert_enrichment(
        self,
        session: AsyncSession,
        arxiv_id: str,
        result: EnrichmentResult,
        now: datetime,
    ) -> None:
        """Upsert a PaperEnrichment record using INSERT ON CONFLICT UPDATE."""
        # Serialize topics to JSON-safe format
        topics_data = None
        if result.topics:
            topics_data = [t.model_dump() for t in result.topics]

        values = {
            "arxiv_id": arxiv_id,
            "openalex_id": result.openalex_id,
            "doi": result.doi,
            "cited_by_count": result.cited_by_count,
            "fwci": result.fwci,
            "topics": topics_data,
            "related_works": result.related_works,
            "counts_by_year": result.counts_by_year,
            "openalex_type": result.openalex_type,
            "openalex_raw": result.raw_response,
            "source_api": self.adapter.adapter_name,
            "api_version": result.api_version,
            "last_attempted_at": now,
            "status": result.status.value,
            "error_detail": result.error_detail,
        }

        # Set enriched_at only on success/partial
        if result.status in (EnrichmentStatus.SUCCESS, EnrichmentStatus.PARTIAL):
            values["enriched_at"] = now
        else:
            values["enriched_at"] = None

        stmt = pg_insert(PaperEnrichment).values(**values)

        # On conflict: update all columns except arxiv_id
        update_cols = {k: v for k, v in values.items() if k != "arxiv_id"}

        # For error status, preserve existing enrichment data columns
        # but update status, error_detail, and last_attempted_at
        if result.status == EnrichmentStatus.ERROR:
            update_cols = {
                "status": values["status"],
                "error_detail": values["error_detail"],
                "last_attempted_at": values["last_attempted_at"],
                "enriched_at": values["enriched_at"],
            }

        stmt = stmt.on_conflict_do_update(
            index_elements=["arxiv_id"],
            set_=update_cols,
        )

        await session.execute(stmt)

    async def _promote_paper(
        self,
        session: AsyncSession,
        paper: Paper,
        result: EnrichmentResult,
    ) -> None:
        """Update Paper columns after successful enrichment."""
        if result.openalex_id:
            paper.openalex_id = result.openalex_id

        # Only set DOI if currently null
        if paper.doi is None and result.doi is not None:
            paper.doi = result.doi

        paper.processing_tier = ProcessingTier.ENRICHED
        paper.promotion_reason = "openalex_enrichment"

    async def _filter_cooldown(
        self,
        session: AsyncSession,
        arxiv_ids: list[str],
        refresh: bool,
    ) -> tuple[list[str], list[str]]:
        """Split arxiv_ids into eligible (past cooldown) and skipped (within cooldown).

        Returns (eligible, skipped) tuple.
        """
        if refresh:
            return arxiv_ids, []

        cooldown_threshold = datetime.now(timezone.utc) - timedelta(
            days=self.settings.enrichment_cooldown_days
        )

        stmt = select(PaperEnrichment.arxiv_id).where(
            PaperEnrichment.arxiv_id.in_(arxiv_ids),
            PaperEnrichment.last_attempted_at >= cooldown_threshold,
        )
        rows = await session.execute(stmt)
        within_cooldown = {r[0] for r in rows.all()}

        eligible = [aid for aid in arxiv_ids if aid not in within_cooldown]
        skipped = [aid for aid in arxiv_ids if aid in within_cooldown]

        return eligible, skipped

    async def _batch_enrich(
        self, eligible: list[str], skipped: list[str]
    ) -> dict:
        """Enrich a batch of papers and return summary stats."""
        enriched = 0
        not_found = 0
        errors = 0

        if eligible:
            results = await self.adapter.enrich(eligible)

            for arxiv_id, result in zip(eligible, results):
                async with self.session_factory() as session:
                    now = datetime.now(timezone.utc)
                    await self._upsert_enrichment(session, arxiv_id, result, now)

                    if result.status in (
                        EnrichmentStatus.SUCCESS,
                        EnrichmentStatus.PARTIAL,
                    ):
                        paper = await session.get(Paper, arxiv_id)
                        if paper:
                            await self._promote_paper(session, paper, result)
                        enriched += 1
                    elif result.status == EnrichmentStatus.NOT_FOUND:
                        not_found += 1
                    else:
                        errors += 1

                    await session.commit()

        return {
            "total": len(eligible) + len(skipped),
            "enriched": enriched,
            "not_found": not_found,
            "errors": errors,
            "skipped_cooldown": len(skipped),
        }
