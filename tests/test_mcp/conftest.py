"""Shared MCP test fixtures: mock AppContext, mock services, mock Context."""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from arxiv_mcp.mcp.server import AppContext
from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.paper import PaperSummary, SearchResult


def _make_paper_summary(arxiv_id: str = "2301.00001", title: str = "Test Paper") -> PaperSummary:
    """Create a sample PaperSummary for test fixtures."""
    return PaperSummary(
        arxiv_id=arxiv_id,
        title=title,
        authors_text="Author One, Author Two",
        abstract_snippet="This is a test abstract for the paper.",
        categories="cs.AI cs.LG",
        primary_category="cs.AI",
        category_list=["cs.AI", "cs.LG"],
        submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 2, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 3),
        oai_datestamp=date(2023, 1, 3),
        latest_version=1,
        license_uri="http://creativecommons.org/licenses/by/4.0/",
    )


def _make_search_result(arxiv_id: str = "2301.00001", score: float = 0.9) -> SearchResult:
    """Create a sample SearchResult for test fixtures."""
    return SearchResult(paper=_make_paper_summary(arxiv_id=arxiv_id), score=score)


@pytest.fixture
def mock_app_context():
    """Mock AppContext with AsyncMock service instances."""
    ctx = MagicMock(spec=AppContext)

    # Mock search service
    ctx.search = AsyncMock()
    ctx.search.search_papers = AsyncMock(
        return_value=PaginatedResponse[SearchResult](
            items=[_make_search_result("2301.00001", 0.95)],
            page_info=PageInfo(has_next=False, next_cursor=None, total_estimate=1),
        )
    )
    ctx.search.browse_recent = AsyncMock(
        return_value=PaginatedResponse[SearchResult](
            items=[_make_search_result("2301.00002", 0.8)],
            page_info=PageInfo(has_next=False, next_cursor=None, total_estimate=1),
        )
    )
    ctx.search.find_related_papers = AsyncMock(
        return_value=[_make_search_result("2301.00003", 0.7)]
    )

    # Mock session factory for get_paper
    ctx.session_factory = MagicMock()

    # Other mock services (not used in discovery tools, but present on AppContext)
    ctx.collections = AsyncMock()
    ctx.triage = AsyncMock()
    ctx.saved_queries = AsyncMock()
    ctx.watches = AsyncMock()
    ctx.profiles = AsyncMock()
    ctx.enrichment = AsyncMock()
    ctx.settings = MagicMock()
    ctx.engine = MagicMock()

    return ctx


@pytest.fixture
def mock_ctx(mock_app_context):
    """Mock MCP Context whose request_context.lifespan_context returns mock_app_context."""
    ctx = MagicMock()
    ctx.request_context.lifespan_context = mock_app_context
    return ctx
