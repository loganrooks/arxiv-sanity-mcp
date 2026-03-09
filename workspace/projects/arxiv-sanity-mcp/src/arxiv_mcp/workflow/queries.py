"""Saved query service for creating, running, and managing named searches.

Provides full CRUD, query re-run with param deserialization,
run_count tracking, and graceful handling of stale references.
Follows the SearchService pattern: session_factory + settings DI.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import SavedQuery
from arxiv_mcp.models.pagination import PaginatedResponse
from arxiv_mcp.models.paper import SearchResult
from arxiv_mcp.models.workflow import SavedQueryResponse, SavedQuerySummary
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.workflow.util import slugify

logger = logging.getLogger(__name__)


class SavedQueryService:
    """Manages saved queries with CRUD and re-run operations.

    Params are stored as JSONB. Run deserializes params and delegates
    to SearchService. Stale collection/triage references are handled
    gracefully (skipped with warning).
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
    # CRUD
    # ------------------------------------------------------------------

    async def create_saved_query(
        self, name: str, params: dict
    ) -> SavedQuerySummary:
        """Create a new saved query. Raises ValueError on slug collision."""
        slug = slugify(name)
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            existing = await session.execute(
                select(SavedQuery).where(SavedQuery.slug == slug)
            )
            if existing.scalar_one_or_none() is not None:
                raise ValueError(f"Saved query with slug '{slug}' already exists")

            sq = SavedQuery(
                slug=slug,
                name=name,
                params=params,
                run_count=0,
                last_run_at=None,
                is_watch=False,
                cadence_hint=None,
                checkpoint_date=None,
                last_checked_at=None,
                is_paused=False,
                created_at=now,
                updated_at=now,
            )
            session.add(sq)
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

    async def list_saved_queries(
        self, include_watches: bool = True
    ) -> list[SavedQuerySummary]:
        """List all saved queries. Optionally exclude watches."""
        stmt = select(SavedQuery).order_by(SavedQuery.created_at.desc())
        if not include_watches:
            stmt = stmt.where(SavedQuery.is_watch.is_(False))

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.scalars().all()

        return [
            SavedQuerySummary(
                slug=sq.slug,
                name=sq.name,
                run_count=sq.run_count,
                last_run_at=sq.last_run_at,
                is_watch=sq.is_watch,
                cadence_hint=sq.cadence_hint,
                created_at=sq.created_at,
            )
            for sq in rows
        ]

    async def get_saved_query(self, slug: str) -> SavedQueryResponse:
        """Get full detail of a saved query. Raises ValueError if not found."""
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            return SavedQueryResponse(
                slug=sq.slug,
                name=sq.name,
                run_count=sq.run_count,
                last_run_at=sq.last_run_at,
                is_watch=sq.is_watch,
                cadence_hint=sq.cadence_hint,
                created_at=sq.created_at,
                params=sq.params,
                updated_at=sq.updated_at,
            )

    async def edit_saved_query(
        self,
        slug: str,
        name: str | None = None,
        params: dict | None = None,
    ) -> SavedQueryResponse:
        """Edit a saved query's name, params, or both.

        If name changes, slug is regenerated. Raises ValueError on slug collision.
        """
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)

            if name is not None:
                new_slug = slugify(name)
                if new_slug != sq.slug:
                    # Check for slug collision
                    existing = await session.execute(
                        select(SavedQuery).where(SavedQuery.slug == new_slug)
                    )
                    if existing.scalar_one_or_none() is not None:
                        raise ValueError(
                            f"Saved query with slug '{new_slug}' already exists"
                        )
                    sq.slug = new_slug
                sq.name = name

            if params is not None:
                sq.params = params

            sq.updated_at = now
            await session.commit()
            await session.refresh(sq)

            return SavedQueryResponse(
                slug=sq.slug,
                name=sq.name,
                run_count=sq.run_count,
                last_run_at=sq.last_run_at,
                is_watch=sq.is_watch,
                cadence_hint=sq.cadence_hint,
                created_at=sq.created_at,
                params=sq.params,
                updated_at=sq.updated_at,
            )

    async def delete_saved_query(self, slug: str) -> None:
        """Delete a saved query. Raises ValueError if not found."""
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            await session.delete(sq)
            await session.commit()

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------

    async def run_saved_query(
        self,
        slug: str,
        cursor_token: str | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[SearchResult]:
        """Run a saved query by deserializing stored params and calling SearchService.

        Increments run_count and sets last_run_at on each run.
        Gracefully handles stale references (skips with warning).
        """
        async with self.session_factory() as session:
            sq = await self._get_or_raise(session, slug)
            params = dict(sq.params)

            # Update usage tracking
            sq.run_count += 1
            sq.last_run_at = datetime.now(timezone.utc)
            await session.commit()

        # Deserialize params for SearchService
        search_kwargs = self._deserialize_params(params)

        # Override pagination if provided
        if cursor_token is not None:
            search_kwargs["cursor_token"] = cursor_token
        if page_size is not None:
            search_kwargs["page_size"] = page_size

        return await self.search_service.search_papers(**search_kwargs)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _deserialize_params(self, params: dict) -> dict:
        """Deserialize JSONB params into SearchService keyword arguments.

        Provides defaults for missing keys, ignores unknown keys,
        and converts date strings to date objects.
        """
        search_kwargs: dict = {}

        # Direct pass-through string params
        for key in ("query_text", "title", "author", "category"):
            if key in params and params[key] is not None:
                search_kwargs[key] = params[key]

        # Date params: convert string to date if needed
        for key in ("date_from", "date_to"):
            if key in params and params[key] is not None:
                val = params[key]
                if isinstance(val, str):
                    search_kwargs[key] = date.fromisoformat(val)
                elif isinstance(val, date):
                    search_kwargs[key] = val

        # Time basis
        if "time_basis" in params and params["time_basis"] is not None:
            search_kwargs["time_basis"] = params["time_basis"]

        # Collection filter: log warning if present (not yet supported in search)
        if "collection_filter" in params:
            logger.warning(
                "collection_filter in saved query params is not yet supported "
                "in base SearchService; skipping filter"
            )

        # Triage filter: log warning if present (not yet supported in search)
        if "triage_filter" in params:
            logger.warning(
                "triage_filter in saved query params is not yet supported "
                "in base SearchService; skipping filter"
            )

        return search_kwargs

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
