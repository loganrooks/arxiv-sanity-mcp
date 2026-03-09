"""Watch service for delta tracking on saved queries.

Extends saved queries with checkpoint-based date filtering to answer
"what's new since I last checked." Provides promote, check, check-all,
pause/resume, reset, dashboard, and demote operations.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Paper, SavedQuery
from arxiv_mcp.models.pagination import PaginatedResponse
from arxiv_mcp.models.paper import SearchResult
from arxiv_mcp.models.workflow import (
    SavedQuerySummary,
    WatchDashboard,
    WatchSummary,
)
from arxiv_mcp.search.service import SearchService

logger = logging.getLogger(__name__)


class WatchService:
    """Manages watch lifecycle: delta tracking, checkpoint auto-advance.

    A watch is a saved query with checkpoint_date for delta filtering.
    check_watch overrides date_from with checkpoint_date to return only
    papers newer than the last check.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        search_service: SearchService,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.search_service = search_service

    # ------------------------------------------------------------------
    # Promote / Demote
    # ------------------------------------------------------------------

    async def promote_to_watch(
        self, slug: str, cadence: str = "daily"
    ) -> WatchSummary:
        """Promote a saved query to a watch.

        Sets is_watch=True, cadence_hint, checkpoint_date=today.
        Raises ValueError if already a watch.
        """
        today = date.today()

        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)

            if sq.is_watch:
                raise ValueError(
                    f"Saved query '{slug}' is already a watch"
                )

            sq.is_watch = True
            sq.cadence_hint = cadence
            sq.checkpoint_date = today
            sq.is_paused = False
            sq.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(sq)

            return self._to_watch_summary(sq)

    async def demote_watch(self, slug: str) -> SavedQuerySummary:
        """Demote a watch back to a regular saved query.

        Clears is_watch, cadence_hint, checkpoint_date, last_checked_at, is_paused.
        """
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)

            if not sq.is_watch:
                raise ValueError(f"Saved query '{slug}' is not a watch")

            sq.is_watch = False
            sq.cadence_hint = None
            sq.checkpoint_date = None
            sq.last_checked_at = None
            sq.is_paused = False
            sq.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(sq)

            return SavedQuerySummary(
                slug=sq.slug,
                name=sq.name,
                run_count=sq.run_count,
                last_run_at=sq.last_run_at,
                is_watch=sq.is_watch,
                cadence_hint=sq.cadence_hint,
                created_at=sq.created_at,
            )

    # ------------------------------------------------------------------
    # Check (delta)
    # ------------------------------------------------------------------

    async def check_watch(
        self,
        slug: str,
        cursor_token: str | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[SearchResult]:
        """Check a watch for new papers since checkpoint_date.

        Overrides date_from in the query params with checkpoint_date.
        Auto-advances checkpoint_date to today after check.
        Raises ValueError if watch is paused.
        """
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)

            if not sq.is_watch:
                raise ValueError(f"Saved query '{slug}' is not a watch")
            if sq.is_paused:
                raise ValueError(
                    f"Watch '{slug}' is paused. Resume it before checking."
                )

            params = dict(sq.params)
            checkpoint = sq.checkpoint_date

        # Deserialize params, override date_from with checkpoint + 1 day
        # (checkpoint represents the last date we've seen through)
        search_kwargs = self._deserialize_params(params)
        if checkpoint is not None:
            search_kwargs["date_from"] = checkpoint + timedelta(days=1)

        if cursor_token is not None:
            search_kwargs["cursor_token"] = cursor_token
        if page_size is not None:
            search_kwargs["page_size"] = page_size

        result = await self.search_service.search_papers(**search_kwargs)

        # Auto-advance checkpoint and update tracking
        today = date.today()
        now = datetime.now(timezone.utc)
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            sq.checkpoint_date = today
            sq.last_checked_at = now
            sq.run_count += 1
            sq.last_run_at = now
            sq.updated_at = now
            await session.commit()

        return result

    async def check_all_watches(self) -> list[dict]:
        """Check all active (non-paused) watches and return combined summary.

        Returns list of {slug, delta_count, cadence_hint,
        checkpoint_advanced_from, checkpoint_advanced_to}.
        """
        async with self.session_factory() as session:
            stmt = (
                select(SavedQuery)
                .where(SavedQuery.is_watch.is_(True))
                .where(SavedQuery.is_paused.is_(False))
            )
            result = await session.execute(stmt)
            watches = result.scalars().all()
            watch_slugs = [(w.slug, w.checkpoint_date, w.cadence_hint) for w in watches]

        results = []
        for slug, old_checkpoint, cadence in watch_slugs:
            try:
                delta = await self.check_watch(slug)
                results.append({
                    "slug": slug,
                    "delta_count": len(delta.items),
                    "cadence_hint": cadence,
                    "checkpoint_advanced_from": str(old_checkpoint) if old_checkpoint else None,
                    "checkpoint_advanced_to": str(date.today()),
                })
            except Exception as e:
                logger.warning(f"Error checking watch '{slug}': {e}")
                results.append({
                    "slug": slug,
                    "delta_count": 0,
                    "cadence_hint": cadence,
                    "error": str(e),
                })

        return results

    # ------------------------------------------------------------------
    # Pause / Resume
    # ------------------------------------------------------------------

    async def pause_watch(self, slug: str) -> WatchSummary:
        """Pause a watch (skipped by check-all)."""
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            if not sq.is_watch:
                raise ValueError(f"Saved query '{slug}' is not a watch")

            sq.is_paused = True
            sq.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(sq)

            return self._to_watch_summary(sq)

    async def resume_watch(self, slug: str) -> WatchSummary:
        """Resume a paused watch."""
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            if not sq.is_watch:
                raise ValueError(f"Saved query '{slug}' is not a watch")

            sq.is_paused = False
            sq.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(sq)

            return self._to_watch_summary(sq)

    # ------------------------------------------------------------------
    # Checkpoint
    # ------------------------------------------------------------------

    async def reset_checkpoint(
        self, slug: str, new_date: date
    ) -> WatchSummary:
        """Reset checkpoint date ("pretend I haven't checked since date X")."""
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            if not sq.is_watch:
                raise ValueError(f"Saved query '{slug}' is not a watch")

            sq.checkpoint_date = new_date
            sq.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(sq)

            return self._to_watch_summary(sq)

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    async def get_watch_dashboard(self) -> WatchDashboard:
        """Return dashboard with all watches and counts.

        pending_estimate uses a lightweight COUNT query for papers
        since checkpoint_date.
        """
        async with self.session_factory() as session:
            stmt = (
                select(SavedQuery)
                .where(SavedQuery.is_watch.is_(True))
                .order_by(SavedQuery.created_at.desc())
            )
            result = await session.execute(stmt)
            watches = result.scalars().all()

            summaries = []
            active_count = 0
            paused_count = 0

            for w in watches:
                # Lightweight pending estimate: count papers since checkpoint
                pending = None
                if w.checkpoint_date is not None and not w.is_paused:
                    time_basis = w.params.get("time_basis", "announced")
                    date_col = self._get_date_column(time_basis)
                    count_stmt = (
                        select(func.count(Paper.arxiv_id))
                        .where(date_col > w.checkpoint_date)
                    )
                    # Apply category filter if present in params
                    category = w.params.get("category")
                    if category:
                        count_stmt = count_stmt.where(
                            Paper.category_list.any(category)
                        )
                    count_result = await session.execute(count_stmt)
                    pending = count_result.scalar() or 0

                if w.is_paused:
                    paused_count += 1
                else:
                    active_count += 1

                summaries.append(
                    WatchSummary(
                        slug=w.slug,
                        name=w.name,
                        cadence_hint=w.cadence_hint,
                        checkpoint_date=w.checkpoint_date,
                        last_checked_at=w.last_checked_at,
                        is_paused=w.is_paused,
                        pending_estimate=pending,
                    )
                )

        return WatchDashboard(
            watches=summaries,
            total_active=active_count,
            total_paused=paused_count,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _deserialize_params(self, params: dict) -> dict:
        """Deserialize JSONB params into SearchService keyword arguments."""
        from datetime import date as date_type

        search_kwargs: dict = {}

        for key in ("query_text", "title", "author", "category"):
            if key in params and params[key] is not None:
                search_kwargs[key] = params[key]

        for key in ("date_from", "date_to"):
            if key in params and params[key] is not None:
                val = params[key]
                if isinstance(val, str):
                    search_kwargs[key] = date_type.fromisoformat(val)
                elif isinstance(val, date_type):
                    search_kwargs[key] = val

        if "time_basis" in params and params["time_basis"] is not None:
            search_kwargs["time_basis"] = params["time_basis"]

        return search_kwargs

    def _get_date_column(self, time_basis: str):
        """Return the Paper date column for the given time basis."""
        mapping = {
            "submitted": Paper.submitted_date,
            "updated": Paper.updated_date,
            "announced": Paper.announced_date,
        }
        return mapping.get(time_basis, Paper.announced_date)

    def _to_watch_summary(self, sq: SavedQuery) -> WatchSummary:
        """Convert a SavedQuery ORM object to WatchSummary."""
        return WatchSummary(
            slug=sq.slug,
            name=sq.name,
            cadence_hint=sq.cadence_hint,
            checkpoint_date=sq.checkpoint_date,
            last_checked_at=sq.last_checked_at,
            is_paused=sq.is_paused,
            pending_estimate=None,
        )

    async def _get_or_raise(
        self, session: AsyncSession, slug: str
    ) -> SavedQuery:
        """Fetch a SavedQuery by slug or raise ValueError."""
        result = await session.execute(
            select(SavedQuery).where(SavedQuery.slug == slug)
        )
        sq = result.scalar_one_or_none()
        if sq is None:
            raise ValueError(f"Saved query not found: '{slug}'")
        return sq
