"""Export/import service for workflow state.

Provides JSON export/import of all workflow state (collections,
triage states, triage log, saved queries), stats with cross-entity
insights, nuclear reset, and paper detail view.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    Paper,
    SavedQuery,
    TriageLog,
    TriageState,
)
from arxiv_mcp.models.paper import PaperDetail, PaperSummary
from arxiv_mcp.models.workflow import ExportData, WorkflowStats

logger = logging.getLogger(__name__)


class ExportService:
    """Manages workflow state export/import, stats, reset, and paper detail.

    Export serializes all workflow state to ExportData Pydantic model.
    Import deserializes with conflict resolution (skip or last-write-wins).
    Stats provides cross-entity insights via SQL aggregation.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    async def export_all(
        self, entity_types: list[str] | None = None
    ) -> ExportData:
        """Export all workflow state as ExportData.

        If entity_types is provided, only exports those types
        (e.g., ["collections", "triage_states"]).
        """
        now = datetime.now(timezone.utc)
        include_all = entity_types is None

        data = ExportData(version="1.0", exported_at=now)

        async with self.session_factory() as session:
            # Collections (with paper memberships)
            if include_all or "collections" in entity_types:
                collections_result = await session.execute(
                    select(Collection).order_by(Collection.created_at)
                )
                collections = collections_result.scalars().all()
                for coll in collections:
                    # Get membership
                    members_result = await session.execute(
                        select(CollectionPaper).where(
                            CollectionPaper.collection_id == coll.id
                        )
                    )
                    members = members_result.scalars().all()
                    data.collections.append({
                        "slug": coll.slug,
                        "name": coll.name,
                        "is_archived": coll.is_archived,
                        "created_at": coll.created_at.isoformat(),
                        "updated_at": coll.updated_at.isoformat(),
                        "papers": [
                            {
                                "paper_id": m.paper_id,
                                "source": m.source,
                                "added_at": m.added_at.isoformat(),
                            }
                            for m in members
                        ],
                    })

            # Triage states
            if include_all or "triage_states" in entity_types:
                triage_result = await session.execute(
                    select(TriageState).order_by(TriageState.paper_id)
                )
                for ts in triage_result.scalars().all():
                    data.triage_states.append({
                        "paper_id": ts.paper_id,
                        "state": ts.state,
                        "updated_at": ts.updated_at.isoformat(),
                    })

            # Triage log
            if include_all or "triage_log" in entity_types:
                log_result = await session.execute(
                    select(TriageLog).order_by(TriageLog.timestamp)
                )
                for entry in log_result.scalars().all():
                    data.triage_log.append({
                        "paper_id": entry.paper_id,
                        "old_state": entry.old_state,
                        "new_state": entry.new_state,
                        "timestamp": entry.timestamp.isoformat(),
                        "source": entry.source,
                        "reason": entry.reason,
                    })

            # Saved queries
            if include_all or "saved_queries" in entity_types:
                sq_result = await session.execute(
                    select(SavedQuery).order_by(SavedQuery.created_at)
                )
                for sq in sq_result.scalars().all():
                    data.saved_queries.append({
                        "slug": sq.slug,
                        "name": sq.name,
                        "params": sq.params,
                        "run_count": sq.run_count,
                        "last_run_at": sq.last_run_at.isoformat() if sq.last_run_at else None,
                        "is_watch": sq.is_watch,
                        "cadence_hint": sq.cadence_hint,
                        "checkpoint_date": sq.checkpoint_date.isoformat() if sq.checkpoint_date else None,
                        "last_checked_at": sq.last_checked_at.isoformat() if sq.last_checked_at else None,
                        "is_paused": sq.is_paused,
                        "created_at": sq.created_at.isoformat(),
                        "updated_at": sq.updated_at.isoformat(),
                    })

        return data

    async def export_to_file(
        self,
        path: str,
        entity_types: list[str] | None = None,
    ) -> None:
        """Export workflow state to a JSON file."""
        data = await self.export_all(entity_types=entity_types)
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(data.model_dump_json(indent=2))

    # ------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------

    async def import_from_file(
        self, path: str, conflict_strategy: str = "skip"
    ) -> dict:
        """Import workflow state from a JSON file.

        conflict_strategy:
        - "skip" (default): skip existing slugs for collections/saved_queries;
          for triage_states use "last write wins" (most recent updated_at).
        - "overwrite": always overwrite existing data.

        Returns summary: {imported_count, skipped_count, warnings: []}.
        """
        file_path = Path(path)
        raw = json.loads(file_path.read_text())
        data = ExportData(**raw)

        imported = 0
        skipped = 0
        warnings: list[str] = []

        async with self.session_factory() as session:
            # Import collections
            for coll_data in data.collections:
                existing = await session.execute(
                    select(Collection).where(
                        Collection.slug == coll_data["slug"]
                    )
                )
                if existing.scalar_one_or_none() is not None:
                    if conflict_strategy == "skip":
                        skipped += 1
                        warnings.append(
                            f"Skipped collection '{coll_data['slug']}' (already exists)"
                        )
                        continue

                coll = Collection(
                    slug=coll_data["slug"],
                    name=coll_data["name"],
                    is_archived=coll_data.get("is_archived", False),
                    created_at=datetime.fromisoformat(coll_data["created_at"]),
                    updated_at=datetime.fromisoformat(coll_data["updated_at"]),
                )
                session.add(coll)
                await session.flush()

                # Add paper memberships (skip if paper doesn't exist)
                for paper_data in coll_data.get("papers", []):
                    paper_exists = await session.execute(
                        select(Paper.arxiv_id).where(
                            Paper.arxiv_id == paper_data["paper_id"]
                        )
                    )
                    if paper_exists.scalar_one_or_none() is not None:
                        session.add(
                            CollectionPaper(
                                collection_id=coll.id,
                                paper_id=paper_data["paper_id"],
                                source=paper_data.get("source", "import"),
                                added_at=datetime.fromisoformat(
                                    paper_data["added_at"]
                                ),
                            )
                        )
                    else:
                        warnings.append(
                            f"Skipped paper '{paper_data['paper_id']}' "
                            f"in collection '{coll_data['slug']}' (paper not found)"
                        )

                imported += 1

            # Import triage states (last write wins for conflicts)
            for ts_data in data.triage_states:
                existing = await session.execute(
                    select(TriageState).where(
                        TriageState.paper_id == ts_data["paper_id"]
                    )
                )
                existing_ts = existing.scalar_one_or_none()
                import_updated = datetime.fromisoformat(ts_data["updated_at"])

                if existing_ts is not None:
                    # Last write wins
                    if import_updated > existing_ts.updated_at:
                        existing_ts.state = ts_data["state"]
                        existing_ts.updated_at = import_updated
                        imported += 1
                    else:
                        skipped += 1
                else:
                    # Check paper exists
                    paper_exists = await session.execute(
                        select(Paper.arxiv_id).where(
                            Paper.arxiv_id == ts_data["paper_id"]
                        )
                    )
                    if paper_exists.scalar_one_or_none() is not None:
                        session.add(
                            TriageState(
                                paper_id=ts_data["paper_id"],
                                state=ts_data["state"],
                                updated_at=import_updated,
                            )
                        )
                        imported += 1
                    else:
                        skipped += 1
                        warnings.append(
                            f"Skipped triage for '{ts_data['paper_id']}' (paper not found)"
                        )

            # Import triage log
            for log_data in data.triage_log:
                # Check paper exists
                paper_exists = await session.execute(
                    select(Paper.arxiv_id).where(
                        Paper.arxiv_id == log_data["paper_id"]
                    )
                )
                if paper_exists.scalar_one_or_none() is not None:
                    session.add(
                        TriageLog(
                            paper_id=log_data["paper_id"],
                            old_state=log_data["old_state"],
                            new_state=log_data["new_state"],
                            timestamp=datetime.fromisoformat(log_data["timestamp"]),
                            source=log_data.get("source", "import"),
                            reason=log_data.get("reason"),
                        )
                    )
                    imported += 1

            # Import saved queries
            for sq_data in data.saved_queries:
                existing = await session.execute(
                    select(SavedQuery).where(
                        SavedQuery.slug == sq_data["slug"]
                    )
                )
                if existing.scalar_one_or_none() is not None:
                    if conflict_strategy == "skip":
                        skipped += 1
                        warnings.append(
                            f"Skipped saved query '{sq_data['slug']}' (already exists)"
                        )
                        continue

                from datetime import date

                sq = SavedQuery(
                    slug=sq_data["slug"],
                    name=sq_data["name"],
                    params=sq_data["params"],
                    run_count=sq_data.get("run_count", 0),
                    last_run_at=(
                        datetime.fromisoformat(sq_data["last_run_at"])
                        if sq_data.get("last_run_at")
                        else None
                    ),
                    is_watch=sq_data.get("is_watch", False),
                    cadence_hint=sq_data.get("cadence_hint"),
                    checkpoint_date=(
                        date.fromisoformat(sq_data["checkpoint_date"])
                        if sq_data.get("checkpoint_date")
                        else None
                    ),
                    last_checked_at=(
                        datetime.fromisoformat(sq_data["last_checked_at"])
                        if sq_data.get("last_checked_at")
                        else None
                    ),
                    is_paused=sq_data.get("is_paused", False),
                    created_at=datetime.fromisoformat(sq_data["created_at"]),
                    updated_at=datetime.fromisoformat(sq_data["updated_at"]),
                )
                session.add(sq)
                imported += 1

            await session.commit()

        return {
            "imported_count": imported,
            "skipped_count": skipped,
            "warnings": warnings,
        }

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    async def get_stats(self) -> WorkflowStats:
        """Return workflow stats with counts and cross-entity insights.

        Uses SQL aggregation queries (no N+1).
        """
        insights: list[str] = []

        async with self.session_factory() as session:
            # Collection count
            coll_count_result = await session.execute(
                select(func.count(Collection.id)).where(
                    Collection.is_archived.is_(False)
                )
            )
            collection_count = coll_count_result.scalar() or 0

            # Triage counts by state
            triage_counts_result = await session.execute(
                select(TriageState.state, func.count(TriageState.paper_id))
                .group_by(TriageState.state)
            )
            triage_counts = {
                row[0]: row[1] for row in triage_counts_result.all()
            }

            # Count unseen (papers without triage row)
            unseen_result = await session.execute(
                select(func.count(Paper.arxiv_id))
                .outerjoin(TriageState, TriageState.paper_id == Paper.arxiv_id)
                .where(TriageState.state.is_(None))
            )
            triage_counts["unseen"] = unseen_result.scalar() or 0

            # Saved query count
            sq_count_result = await session.execute(
                select(func.count(SavedQuery.id)).where(
                    SavedQuery.is_watch.is_(False)
                )
            )
            saved_query_count = sq_count_result.scalar() or 0

            # Watch count
            watch_count_result = await session.execute(
                select(func.count(SavedQuery.id)).where(
                    SavedQuery.is_watch.is_(True)
                )
            )
            watch_count = watch_count_result.scalar() or 0

            # --- Insights ---

            # Shortlisted papers not in any collection
            shortlisted_not_in_coll = await session.execute(
                select(func.count(TriageState.paper_id))
                .outerjoin(
                    CollectionPaper,
                    CollectionPaper.paper_id == TriageState.paper_id,
                )
                .where(TriageState.state == "shortlisted")
                .where(CollectionPaper.paper_id.is_(None))
            )
            orphaned = shortlisted_not_in_coll.scalar() or 0
            if orphaned > 0:
                insights.append(
                    f"{orphaned} shortlisted paper{'s' if orphaned != 1 else ''} "
                    f"not in any collection"
                )

            # Stale watches (not checked in 7+ days)
            from datetime import timedelta

            cutoff = datetime.now(timezone.utc) - timedelta(days=7)
            stale_watches_result = await session.execute(
                select(func.count(SavedQuery.id))
                .where(SavedQuery.is_watch.is_(True))
                .where(SavedQuery.is_paused.is_(False))
                .where(
                    (SavedQuery.last_checked_at < cutoff)
                    | (SavedQuery.last_checked_at.is_(None))
                )
            )
            stale = stale_watches_result.scalar() or 0
            if stale > 0:
                insights.append(
                    f"{stale} watch{'es' if stale != 1 else ''} "
                    f"haven't been checked in 7+ days"
                )

            # Papers in collections with no triage state
            in_coll_no_triage = await session.execute(
                select(
                    func.count(func.distinct(CollectionPaper.paper_id))
                )
                .outerjoin(
                    TriageState,
                    TriageState.paper_id == CollectionPaper.paper_id,
                )
                .where(TriageState.state.is_(None))
            )
            untriaged_in_coll = in_coll_no_triage.scalar() or 0
            if untriaged_in_coll > 0:
                insights.append(
                    f"{untriaged_in_coll} paper{'s' if untriaged_in_coll != 1 else ''} "
                    f"in collections with no triage state set"
                )

        return WorkflowStats(
            collection_count=collection_count,
            triage_counts=triage_counts,
            saved_query_count=saved_query_count,
            watch_count=watch_count,
            insights=insights,
        )

    # ------------------------------------------------------------------
    # Nuclear reset
    # ------------------------------------------------------------------

    async def nuclear_reset(self) -> None:
        """TRUNCATE all workflow tables (preserves papers).

        Deletes in FK order: triage_log, triage_states,
        collection_papers, saved_queries, collections.
        """
        async with self.session_factory() as session:
            await session.execute(delete(TriageLog))
            await session.execute(delete(TriageState))
            await session.execute(delete(CollectionPaper))
            await session.execute(delete(SavedQuery))
            await session.execute(delete(Collection))
            await session.commit()

    # ------------------------------------------------------------------
    # Paper detail
    # ------------------------------------------------------------------

    async def get_paper_detail(self, arxiv_id: str) -> dict:
        """Fetch paper with triage state and collection memberships.

        Returns dict combining PaperDetail + triage_state + collections list.
        Powers the `paper show` CLI command.
        """
        async with self.session_factory() as session:
            # Fetch paper
            paper_result = await session.execute(
                select(Paper).where(Paper.arxiv_id == arxiv_id)
            )
            paper = paper_result.scalar_one_or_none()
            if paper is None:
                raise ValueError(f"Paper not found: '{arxiv_id}'")

            # Get triage state
            triage_result = await session.execute(
                select(TriageState.state).where(
                    TriageState.paper_id == arxiv_id
                )
            )
            triage_state = triage_result.scalar_one_or_none() or "unseen"

            # Get collection memberships
            coll_result = await session.execute(
                select(Collection.slug, Collection.name)
                .join(
                    CollectionPaper,
                    CollectionPaper.collection_id == Collection.id,
                )
                .where(CollectionPaper.paper_id == arxiv_id)
            )
            collections = [
                {"slug": row.slug, "name": row.name}
                for row in coll_result.all()
            ]

            # Build PaperDetail
            summary = PaperSummary.from_orm_paper(paper)
            detail_data = summary.model_dump()
            detail_data.update({
                "abstract": paper.abstract,
                "doi": paper.doi,
                "comments": paper.comments,
                "journal_ref": paper.journal_ref,
                "report_no": paper.report_no,
                "source": paper.source,
                "fetched_at": paper.fetched_at,
                "processing_tier": paper.processing_tier,
                "promotion_reason": paper.promotion_reason,
                "openalex_id": paper.openalex_id,
                "semantic_scholar_id": paper.semantic_scholar_id,
            })

            return {
                "paper": detail_data,
                "triage_state": triage_state,
                "collections": collections,
            }
