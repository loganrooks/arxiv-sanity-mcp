"""Triage service for per-paper lifecycle state management.

Provides mark, get, list_by_state, batch (ID-based), batch_by_query
(with dry-run support), and audit log operations. Implements the
absence-means-unseen pattern: no row in triage_states = "unseen".
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Paper, TriageLog, TriageState
from arxiv_mcp.db.queries import build_search_query
from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.workflow import (
    BatchTriagePreview,
    BatchTriageResult,
    TriageLogEntry,
    TriageStateResponse,
)


class TriageService:
    """Manages per-paper triage states with audit trail.

    States: unseen, shortlisted, dismissed, read, cite-later, archived.
    Absence of a triage_states row means "unseen" (no materialization).
    All transitions are logged to triage_log with source and optional reason.
    """

    VALID_STATES = {"unseen", "seen", "shortlisted", "dismissed", "read", "cite-later", "archived"}

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    # ------------------------------------------------------------------
    # Single paper triage
    # ------------------------------------------------------------------

    async def mark_triage(
        self,
        paper_id: str,
        new_state: str,
        source: str = "manual",
        reason: str | None = None,
    ) -> TriageStateResponse:
        """Mark a paper with a triage state.

        - "unseen": deletes the TriageState row (restoring absence-means-unseen).
        - Other valid states: upsert the TriageState row.
        - Always logs the transition to triage_log.

        Raises ValueError for invalid states.
        """
        if new_state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid triage state: '{new_state}'. "
                f"Valid states: {sorted(self.VALID_STATES)}"
            )

        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            # Get current state
            old_state = await self._get_current_state(session, paper_id)

            # Log the transition
            log_entry = TriageLog(
                paper_id=paper_id,
                old_state=old_state,
                new_state=new_state,
                timestamp=now,
                source=source,
                reason=reason,
            )
            session.add(log_entry)

            if new_state == "unseen":
                # Delete the row to restore absence-means-unseen
                await session.execute(
                    delete(TriageState).where(TriageState.paper_id == paper_id)
                )
            else:
                # Upsert: check if row exists
                existing = await session.execute(
                    select(TriageState).where(TriageState.paper_id == paper_id)
                )
                ts = existing.scalar_one_or_none()
                if ts is not None:
                    ts.state = new_state
                    ts.updated_at = now
                else:
                    session.add(
                        TriageState(
                            paper_id=paper_id,
                            state=new_state,
                            updated_at=now,
                        )
                    )

            await session.commit()

            return TriageStateResponse(
                paper_id=paper_id,
                state=new_state,
                updated_at=now,
            )

    async def get_triage_state(self, paper_id: str) -> str:
        """Get the current triage state for a paper.

        Returns "unseen" if no TriageState row exists.
        """
        async with self.session_factory() as session:
            return await self._get_current_state(session, paper_id)

    # ------------------------------------------------------------------
    # List by state
    # ------------------------------------------------------------------

    async def list_by_state(
        self,
        state: str,
        page_size: int = 20,
        cursor_token: str | None = None,
    ) -> PaginatedResponse[TriageStateResponse]:
        """List papers by triage state.

        "unseen": papers with no triage_states row (LEFT JOIN, IS NULL).
        Other states: simple WHERE clause on triage_states.
        """
        page_size = min(max(1, page_size), self.settings.max_page_size)
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            if state == "unseen":
                stmt = (
                    select(Paper.arxiv_id)
                    .outerjoin(TriageState, TriageState.paper_id == Paper.arxiv_id)
                    .where(TriageState.state.is_(None))
                    .order_by(Paper.arxiv_id)
                    .limit(page_size + 1)
                )
                result = await session.execute(stmt)
                rows = result.all()

                has_next = len(rows) > page_size
                items = [
                    TriageStateResponse(
                        paper_id=row[0],
                        state="unseen",
                        updated_at=now,
                    )
                    for row in rows[:page_size]
                ]
            else:
                stmt = (
                    select(TriageState)
                    .where(TriageState.state == state)
                    .order_by(TriageState.paper_id)
                    .limit(page_size + 1)
                )
                result = await session.execute(stmt)
                rows = result.scalars().all()

                has_next = len(rows) > page_size
                items = [
                    TriageStateResponse(
                        paper_id=ts.paper_id,
                        state=ts.state,
                        updated_at=ts.updated_at,
                    )
                    for ts in rows[:page_size]
                ]

        page_info = PageInfo(has_next=has_next, next_cursor=None)
        return PaginatedResponse[TriageStateResponse](items=items, page_info=page_info)

    # ------------------------------------------------------------------
    # Batch triage (ID-based)
    # ------------------------------------------------------------------

    async def batch_triage(
        self,
        paper_ids: list[str],
        new_state: str,
        source: str = "manual",
        reason: str | None = None,
    ) -> BatchTriageResult:
        """Batch triage papers by explicit ID list.

        Validates paper existence. Tracks affected (state changed),
        skipped (already in target state), and errors (paper not found).
        All operations in a single transaction.
        """
        if new_state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid triage state: '{new_state}'. "
                f"Valid states: {sorted(self.VALID_STATES)}"
            )

        affected = 0
        skipped = 0
        errors: list[str] = []
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            # Validate paper existence
            existing_result = await session.execute(
                select(Paper.arxiv_id).where(Paper.arxiv_id.in_(paper_ids))
            )
            existing_ids = {r[0] for r in existing_result.all()}

            for pid in paper_ids:
                if pid not in existing_ids:
                    errors.append(pid)
                    continue

                current = await self._get_current_state(session, pid)
                if current == new_state:
                    skipped += 1
                    continue

                # Log transition
                session.add(
                    TriageLog(
                        paper_id=pid,
                        old_state=current,
                        new_state=new_state,
                        timestamp=now,
                        source=source,
                        reason=reason,
                    )
                )

                if new_state == "unseen":
                    await session.execute(
                        delete(TriageState).where(TriageState.paper_id == pid)
                    )
                else:
                    existing_ts = await session.execute(
                        select(TriageState).where(TriageState.paper_id == pid)
                    )
                    ts = existing_ts.scalar_one_or_none()
                    if ts is not None:
                        ts.state = new_state
                        ts.updated_at = now
                    else:
                        session.add(
                            TriageState(
                                paper_id=pid,
                                state=new_state,
                                updated_at=now,
                            )
                        )

                affected += 1

            await session.commit()

        return BatchTriageResult(
            affected_count=affected,
            skipped_count=skipped,
            errors=errors,
        )

    # ------------------------------------------------------------------
    # Batch triage (query-based)
    # ------------------------------------------------------------------

    async def batch_triage_by_query(
        self,
        query_params: dict,
        new_state: str,
        dry_run: bool = True,
        source: str = "batch",
        reason: str | None = None,
    ) -> BatchTriageResult | BatchTriagePreview:
        """Batch triage papers matching a query.

        Uses Phase 1's build_search_query to resolve matching paper IDs.

        dry_run=True (default): Returns BatchTriagePreview with count and
        sample IDs without modifying any state.

        dry_run=False: Applies triage to all matching papers and returns
        BatchTriageResult. Processes in chunks of 500.
        """
        if new_state not in self.VALID_STATES:
            raise ValueError(
                f"Invalid triage state: '{new_state}'. "
                f"Valid states: {sorted(self.VALID_STATES)}"
            )

        # Build the search query to find matching papers
        # Remove pagination to get all matching IDs
        search_stmt = build_search_query(
            query_text=query_params.get("query_text"),
            title=query_params.get("title"),
            author=query_params.get("author"),
            category=query_params.get("category"),
            date_from=query_params.get("date_from"),
            date_to=query_params.get("date_to"),
            time_basis=query_params.get("time_basis", "announced"),
            cursor=None,
            page_size=10000,  # Large enough to get all results
        )

        # Extract just the paper IDs from the search query
        async with self.session_factory() as session:
            result = await session.execute(search_stmt)
            rows = result.all()

        matching_ids = [row[0].arxiv_id for row in rows]

        if dry_run:
            # Build human-readable query description
            desc_parts = []
            for key, value in query_params.items():
                if value is not None:
                    desc_parts.append(f"{key}={value}")
            query_description = ", ".join(desc_parts) if desc_parts else "all papers"

            return BatchTriagePreview(
                matching_count=len(matching_ids),
                sample_ids=matching_ids[:10],
                query_description=query_description,
            )

        # Execute: process in chunks of 500
        chunk_size = 500
        total_result = BatchTriageResult(
            affected_count=0, skipped_count=0, errors=[]
        )

        for i in range(0, len(matching_ids), chunk_size):
            chunk = matching_ids[i : i + chunk_size]
            chunk_result = await self.batch_triage(
                chunk, new_state, source=source, reason=reason
            )
            total_result.affected_count += chunk_result.affected_count
            total_result.skipped_count += chunk_result.skipped_count
            total_result.errors.extend(chunk_result.errors)

        return total_result

    # ------------------------------------------------------------------
    # Audit log
    # ------------------------------------------------------------------

    async def get_triage_log(
        self, paper_id: str, limit: int = 50
    ) -> list[TriageLogEntry]:
        """Get the triage audit trail for a paper, chronological order."""
        async with self.session_factory() as session:
            stmt = (
                select(TriageLog)
                .where(TriageLog.paper_id == paper_id)
                .order_by(TriageLog.timestamp.asc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            rows = result.scalars().all()

        return [
            TriageLogEntry(
                paper_id=log.paper_id,
                old_state=log.old_state,
                new_state=log.new_state,
                timestamp=log.timestamp,
                source=log.source,
                reason=log.reason,
            )
            for log in rows
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _get_current_state(
        self, session: AsyncSession, paper_id: str
    ) -> str:
        """Get current triage state from the DB. Returns 'unseen' if no row."""
        result = await session.execute(
            select(TriageState.state).where(TriageState.paper_id == paper_id)
        )
        row = result.scalar_one_or_none()
        return row if row is not None else "unseen"
