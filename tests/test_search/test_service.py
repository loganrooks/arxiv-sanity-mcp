"""Integration tests for the SearchService.

Tests are written against a real PostgreSQL test database populated
with 15 sample papers covering varied categories, authors, and dates.
"""

from __future__ import annotations

from datetime import date

import pytest

from arxiv_mcp.config import get_settings
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.models import PaginatedResponse, SearchResult


@pytest.fixture
def service(search_session_factory):
    """Create a SearchService wired to the test session factory."""
    settings = get_settings()
    return SearchService(session_factory=search_session_factory, settings=settings)


# --- Fielded search tests ---


class TestFieldedSearch:
    """Test search_papers with individual field filters."""

    async def test_fielded_search_by_title(self, service: SearchService):
        """Search with title='attention' returns papers with 'attention' in title."""
        result = await service.search_papers(title="attention")
        assert isinstance(result, PaginatedResponse)
        assert len(result.items) > 0
        for item in result.items:
            assert isinstance(item, SearchResult)
            assert "attention" in item.paper.title.lower()

    async def test_fielded_search_by_author(self, service: SearchService):
        """Search with author='Vaswani' returns papers by that author."""
        result = await service.search_papers(author="Vaswani")
        assert len(result.items) > 0
        for item in result.items:
            assert "Vaswani" in item.paper.authors_text

    async def test_fielded_search_by_abstract(self, service: SearchService):
        """Search with query_text='transformer architecture' matches relevant papers."""
        result = await service.search_papers(query_text="transformer architecture")
        assert len(result.items) > 0
        # Results should be ranked by relevance (score present)
        for item in result.items:
            assert item.score is not None
            assert item.score > 0

    async def test_fielded_search_by_category(self, service: SearchService):
        """Search with category='cs.CV' returns only papers in that category."""
        result = await service.search_papers(category="cs.CV")
        assert len(result.items) > 0
        for item in result.items:
            assert "cs.CV" in item.paper.category_list

    async def test_fielded_search_by_date_range(self, service: SearchService):
        """Search with date range returns papers in that range."""
        result = await service.search_papers(
            date_from=date(2023, 1, 5),
            date_to=date(2023, 1, 10),
            time_basis="announced",
        )
        assert len(result.items) > 0
        for item in result.items:
            assert item.paper.announced_date is not None
            assert date(2023, 1, 5) <= item.paper.announced_date <= date(2023, 1, 10)


class TestBooleanSearch:
    """Test AND/OR composition via websearch_to_tsquery natural syntax."""

    async def test_boolean_and(self, service: SearchService):
        """Query 'machine AND learning' returns papers containing both terms."""
        result = await service.search_papers(query_text="machine AND learning")
        assert len(result.items) > 0
        for item in result.items:
            assert item.score is not None
            assert item.score > 0

    async def test_boolean_or(self, service: SearchService):
        """Query 'transformer OR attention' returns papers containing either term."""
        result = await service.search_papers(query_text="transformer OR attention")
        assert len(result.items) > 0
        # Should find more papers than a strict AND query
        assert len(result.items) >= 3  # Several papers mention transformer or attention


class TestCombinedFilters:
    """Test combining multiple filters."""

    async def test_combined_filters(self, service: SearchService):
        """Search with title + category + date returns intersection."""
        result = await service.search_papers(
            title="attention",
            category="cs.CL",
            date_from=date(2023, 1, 1),
            date_to=date(2023, 1, 16),
            time_basis="announced",
        )
        assert len(result.items) > 0
        for item in result.items:
            assert "attention" in item.paper.title.lower()
            assert "cs.CL" in item.paper.category_list


# --- Pagination tests ---


class TestPagination:
    """Test cursor-based pagination behavior."""

    async def test_cursor_pagination_forward(self, service: SearchService):
        """First page returns page_size items; next page has no overlap."""
        page1 = await service.search_papers(category="cs.CL", page_size=3)
        assert len(page1.items) == 3
        assert page1.page_info.has_next is True
        assert page1.page_info.next_cursor is not None

        page2 = await service.search_papers(
            category="cs.CL",
            page_size=3,
            cursor_token=page1.page_info.next_cursor,
        )
        assert len(page2.items) > 0

        # No overlap between pages
        page1_ids = {item.paper.arxiv_id for item in page1.items}
        page2_ids = {item.paper.arxiv_id for item in page2.items}
        assert page1_ids.isdisjoint(page2_ids)

    async def test_cursor_pagination_empty(self, service: SearchService):
        """Search with no results returns empty items and has_next=false."""
        result = await service.search_papers(query_text="xyznonexistentterm12345")
        assert len(result.items) == 0
        assert result.page_info.has_next is False

    async def test_page_size_capped(self, service: SearchService):
        """Requesting page_size > max_page_size returns max_page_size items."""
        settings = get_settings()
        result = await service.search_papers(
            category="cs.CL",
            page_size=5000,  # Way above max_page_size
        )
        assert len(result.items) <= settings.max_page_size


# --- Result shape tests ---


class TestResultShape:
    """Test that results are properly shaped."""

    async def test_search_result_shape(self, service: SearchService):
        """Each result has PaperSummary with truncated abstract and optional score."""
        result = await service.search_papers(query_text="transformer")
        assert len(result.items) > 0
        for item in result.items:
            assert isinstance(item, SearchResult)
            assert item.paper.arxiv_id
            assert item.paper.title
            # abstract_snippet should be truncated (max 300 chars + ellipsis)
            if item.paper.abstract_snippet:
                assert len(item.paper.abstract_snippet) <= 304  # 300 + "..."


# --- Browse recent tests ---


class TestBrowseRecent:
    """Test browse_recent functionality."""

    async def test_browse_recent_all(self, service: SearchService):
        """Browse recent with large window returns papers ordered by date desc."""
        result = await service.browse_recent(days=30)
        assert len(result.items) > 0
        # Verify ordering: announced_date should be descending
        dates = [
            item.paper.announced_date
            for item in result.items
            if item.paper.announced_date is not None
        ]
        assert dates == sorted(dates, reverse=True)

    async def test_browse_recent_by_category(self, service: SearchService):
        """Browse recent with category filter returns only papers in that category."""
        result = await service.browse_recent(category="stat.ML", days=30)
        assert len(result.items) > 0
        for item in result.items:
            assert "stat.ML" in item.paper.category_list

    async def test_browse_recent_time_basis(self, service: SearchService):
        """Browse with submitted time_basis uses submitted_date for ordering."""
        result = await service.browse_recent(time_basis="submitted", days=30)
        assert len(result.items) > 0


# --- Find related papers tests ---


class TestFindRelated:
    """Test find_related_papers functionality."""

    async def test_find_related_papers(self, service: SearchService):
        """Find related to an attention paper returns relevant papers."""
        result = await service.find_related_papers(seed_arxiv_id="2301.00001")
        assert len(result) > 0
        # Seed paper should NOT be in results
        result_ids = {r.paper.arxiv_id for r in result}
        assert "2301.00001" not in result_ids
        # Results should have scores
        for item in result:
            assert item.score is not None
            assert item.score > 0

    async def test_find_related_excludes_seed(self, service: SearchService):
        """Related papers exclude the seed paper itself."""
        result = await service.find_related_papers(seed_arxiv_id="2301.00001")
        for item in result:
            assert item.paper.arxiv_id != "2301.00001"
