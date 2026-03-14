"""Search orchestration: search_papers, browse_recent, find_related_papers.

High-level service that coordinates query building, execution, result
shaping, and pagination for the three main search operations.
"""

from __future__ import annotations

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Paper
from arxiv_mcp.db.queries import build_browse_query, build_related_query, build_search_query
from arxiv_mcp.models.pagination import Cursor, PaginatedResponse
from arxiv_mcp.models.paper import SearchResult
from arxiv_mcp.search.pagination import build_page_info
from arxiv_mcp.search.ranking import shape_search_results


class SearchService:
    """Orchestrates search, browse, and related-paper discovery.

    Each method clamps page_size, decodes cursor if provided, calls
    the appropriate query builder, executes the query, shapes results,
    and builds pagination metadata.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    def _clamp_page_size(self, page_size: int | None) -> int:
        """Clamp page_size to valid range."""
        if page_size is None:
            return self.settings.default_page_size
        return min(max(1, page_size), self.settings.max_page_size)

    async def search_papers(
        self,
        query_text: str | None = None,
        title: str | None = None,
        author: str | None = None,
        category: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        time_basis: str = "announced",
        cursor_token: str | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[SearchResult]:
        """Fielded search with AND/OR composition (SRCH-01, SRCH-02).

        Supports full-text search, individual field filters, and combinations.
        Results are ordered by relevance (when text search is active) or
        date descending (when only filters are used).
        """
        page_size = self._clamp_page_size(page_size)
        cursor = Cursor.decode(cursor_token) if cursor_token else None
        has_text_search = query_text is not None

        stmt = build_search_query(
            query_text=query_text,
            title=title,
            author=author,
            category=category,
            date_from=date_from,
            date_to=date_to,
            time_basis=time_basis,
            cursor=cursor,
            page_size=page_size,
        )

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.all()

        # Shape results
        shaped = shape_search_results(rows)

        # Build pagination
        if has_text_search:
            sort_extractor = lambda item: item.score  # noqa: E731
        else:
            date_attr = {
                "submitted": "submitted_date",
                "updated": "updated_date",
                "announced": "announced_date",
            }.get(time_basis, "announced_date")
            sort_extractor = lambda item: str(getattr(item.paper, date_attr))  # noqa: E731

        items, page_info = build_page_info(
            shaped,
            page_size,
            sort_value_extractor=sort_extractor,
            id_extractor=lambda item: item.paper.arxiv_id,
        )

        return PaginatedResponse[SearchResult](items=items, page_info=page_info)

    async def browse_recent(
        self,
        category: str | None = None,
        time_basis: str = "announced",
        days: int = 7,
        cursor_token: str | None = None,
        page_size: int | None = None,
    ) -> PaginatedResponse[SearchResult]:
        """Browse recently announced papers (SRCH-03, SRCH-04).

        Returns papers within the specified day window, optionally
        filtered by category, ordered by the selected time basis.
        """
        page_size = self._clamp_page_size(page_size)
        cursor = Cursor.decode(cursor_token) if cursor_token else None

        stmt = build_browse_query(
            category=category,
            time_basis=time_basis,
            days=days,
            cursor=cursor,
            page_size=page_size,
        )

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.all()

        shaped = shape_search_results(rows)

        date_attr = {
            "submitted": "submitted_date",
            "updated": "updated_date",
            "announced": "announced_date",
        }.get(time_basis, "announced_date")

        items, page_info = build_page_info(
            shaped,
            page_size,
            sort_value_extractor=lambda item: str(getattr(item.paper, date_attr)),
            id_extractor=lambda item: item.paper.arxiv_id,
        )

        return PaginatedResponse[SearchResult](items=items, page_info=page_info)

    async def find_related_papers(
        self,
        seed_arxiv_id: str,
        page_size: int | None = None,
    ) -> list[SearchResult]:
        """Find related papers from seed via lexical similarity (SRCH-05).

        Uses the seed paper's title and abstract to find lexically
        similar papers via tsvector ranking.
        """
        page_size = self._clamp_page_size(page_size)

        async with self.session_factory() as session:
            # Fetch the seed paper
            seed_result = await session.execute(
                select(Paper).where(Paper.arxiv_id == seed_arxiv_id)
            )
            seed_paper = seed_result.scalar_one_or_none()
            if seed_paper is None:
                raise ValueError(f"Seed paper not found: {seed_arxiv_id}")

            stmt = build_related_query(seed_paper=seed_paper, page_size=page_size)
            result = await session.execute(stmt)
            rows = result.all()

        return shape_search_results(rows)
