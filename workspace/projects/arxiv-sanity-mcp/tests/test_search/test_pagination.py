"""Integration tests for cursor pagination with actual search queries.

These tests verify that keyset cursor pagination works correctly
when applied to real database queries, complementing the unit-level
cursor encode/decode tests in test_models/test_pagination.py.
"""

from __future__ import annotations

import pytest

from arxiv_mcp.config import get_settings
from arxiv_mcp.search.service import SearchService


@pytest.fixture
def service(search_session_factory):
    """Create a SearchService wired to the test session factory."""
    settings = get_settings()
    return SearchService(session_factory=search_session_factory, settings=settings)


class TestCursorPaginationIntegration:
    """Test cursor pagination with actual database queries."""

    async def test_full_pagination_walk(self, service: SearchService):
        """Walk through all pages and collect all results without duplication."""
        all_ids: list[str] = []
        cursor = None
        pages = 0

        while True:
            result = await service.search_papers(
                category="cs.CL",
                page_size=2,
                cursor_token=cursor,
            )
            for item in result.items:
                assert item.paper.arxiv_id not in all_ids, (
                    f"Duplicate: {item.paper.arxiv_id}"
                )
                all_ids.append(item.paper.arxiv_id)

            pages += 1
            if not result.page_info.has_next:
                break
            cursor = result.page_info.next_cursor

        assert pages >= 2  # Should need multiple pages
        assert len(all_ids) > 2  # Should have found multiple papers

    async def test_pagination_with_text_search(self, service: SearchService):
        """Cursor pagination works correctly with text search + relevance ordering."""
        page1 = await service.search_papers(
            query_text="transformer OR attention OR neural",
            page_size=3,
        )
        assert len(page1.items) > 0

        if page1.page_info.has_next:
            page2 = await service.search_papers(
                query_text="transformer OR attention OR neural",
                page_size=3,
                cursor_token=page1.page_info.next_cursor,
            )
            # No overlap
            page1_ids = {item.paper.arxiv_id for item in page1.items}
            page2_ids = {item.paper.arxiv_id for item in page2.items}
            assert page1_ids.isdisjoint(page2_ids)

    async def test_browse_pagination(self, service: SearchService):
        """Cursor pagination works with browse_recent."""
        page1 = await service.browse_recent(days=30, page_size=5)
        assert len(page1.items) > 0

        if page1.page_info.has_next:
            page2 = await service.browse_recent(
                days=30,
                page_size=5,
                cursor_token=page1.page_info.next_cursor,
            )
            page1_ids = {item.paper.arxiv_id for item in page1.items}
            page2_ids = {item.paper.arxiv_id for item in page2.items}
            assert page1_ids.isdisjoint(page2_ids)
