"""Unit tests for the 4 discovery tools: search_papers, browse_recent,
find_related_papers, get_paper.

Tests call tool functions directly with mock context (not through MCP transport).
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.paper import PaperSummary, SearchResult


# ---- Tool name tests ----

class TestToolNames:
    """Tool names describe user intent, not implementation details."""

    def test_tool_names_are_user_intent_oriented(self):
        from arxiv_mcp.mcp.tools import discovery

        expected_names = {"search_papers", "browse_recent", "find_related_papers", "get_paper"}
        actual_names = {
            discovery.search_papers.__name__,
            discovery.browse_recent.__name__,
            discovery.find_related_papers.__name__,
            discovery.get_paper.__name__,
        }
        assert actual_names == expected_names


# ---- search_papers tests ----

class TestSearchPapers:
    """search_papers tool calls SearchService.search_papers with mapped params."""

    async def test_search_papers_delegates_to_service(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import search_papers

        result = await search_papers(
            query="attention mechanisms",
            category="cs.AI",
            page_size=10,
            ctx=mock_ctx,
        )

        mock_app_context.search.search_papers.assert_awaited_once()
        call_kwargs = mock_app_context.search.search_papers.call_args.kwargs
        # query maps to query_text
        assert call_kwargs["query_text"] == "attention mechanisms"
        assert call_kwargs["category"] == "cs.AI"
        assert call_kwargs["page_size"] == 10

    async def test_search_papers_maps_cursor_to_cursor_token(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import search_papers

        await search_papers(cursor="abc123", ctx=mock_ctx)

        call_kwargs = mock_app_context.search.search_papers.call_args.kwargs
        assert call_kwargs["cursor_token"] == "abc123"

    async def test_search_papers_returns_dict(self, mock_ctx):
        from arxiv_mcp.mcp.tools.discovery import search_papers

        result = await search_papers(query="test", ctx=mock_ctx)
        assert isinstance(result, dict)
        assert "items" in result
        assert "page_info" in result

    async def test_search_papers_parses_date_strings(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import search_papers

        await search_papers(
            date_from="2023-01-01",
            date_to="2023-06-30",
            ctx=mock_ctx,
        )

        call_kwargs = mock_app_context.search.search_papers.call_args.kwargs
        assert call_kwargs["date_from"] == date(2023, 1, 1)
        assert call_kwargs["date_to"] == date(2023, 6, 30)


# ---- browse_recent tests ----

class TestBrowseRecent:
    """browse_recent tool calls SearchService.browse_recent with mapped params."""

    async def test_browse_recent_delegates_to_service(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import browse_recent

        result = await browse_recent(
            category="cs.AI",
            days=14,
            page_size=10,
            ctx=mock_ctx,
        )

        mock_app_context.search.browse_recent.assert_awaited_once()
        call_kwargs = mock_app_context.search.browse_recent.call_args.kwargs
        assert call_kwargs["category"] == "cs.AI"
        assert call_kwargs["days"] == 14
        assert call_kwargs["page_size"] == 10

    async def test_browse_recent_maps_cursor(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import browse_recent

        await browse_recent(cursor="xyz789", ctx=mock_ctx)

        call_kwargs = mock_app_context.search.browse_recent.call_args.kwargs
        assert call_kwargs["cursor_token"] == "xyz789"

    async def test_browse_recent_returns_dict(self, mock_ctx):
        from arxiv_mcp.mcp.tools.discovery import browse_recent

        result = await browse_recent(ctx=mock_ctx)
        assert isinstance(result, dict)
        assert "items" in result


# ---- find_related_papers tests ----

class TestFindRelatedPapers:
    """find_related_papers supports single and multiple seed IDs with dedup."""

    async def test_find_related_single_seed(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import find_related_papers

        result = await find_related_papers(seed_arxiv_ids="2301.00001", ctx=mock_ctx)

        mock_app_context.search.find_related_papers.assert_awaited_once_with(
            seed_arxiv_id="2301.00001",
            page_size=20,
        )
        assert isinstance(result, list)

    async def test_find_related_multiple_seeds(self, mock_ctx, mock_app_context):
        """Multiple seeds: service called once per seed, results deduplicated."""
        from arxiv_mcp.mcp.tools.discovery import find_related_papers
        from tests.test_mcp.conftest import _make_search_result

        # Two seeds return overlapping results
        mock_app_context.search.find_related_papers.side_effect = [
            [
                _make_search_result("2301.00003", 0.7),
                _make_search_result("2301.00004", 0.5),
            ],
            [
                _make_search_result("2301.00003", 0.9),  # higher score for duplicate
                _make_search_result("2301.00005", 0.6),
            ],
        ]

        result = await find_related_papers(
            seed_arxiv_ids=["2301.00001", "2301.00002"],
            ctx=mock_ctx,
        )

        # Two service calls
        assert mock_app_context.search.find_related_papers.await_count == 2

        # Deduplicated: 3 unique papers (seed IDs excluded)
        arxiv_ids = [r["paper"]["arxiv_id"] for r in result]
        assert len(arxiv_ids) == len(set(arxiv_ids)), "Results should be deduplicated"

        # Duplicate kept highest score
        for r in result:
            if r["paper"]["arxiv_id"] == "2301.00003":
                assert r["score"] == 0.9, "Should keep highest score for duplicates"

    async def test_find_related_excludes_seed_ids(self, mock_ctx, mock_app_context):
        """Seed IDs should not appear in results."""
        from arxiv_mcp.mcp.tools.discovery import find_related_papers
        from tests.test_mcp.conftest import _make_search_result

        mock_app_context.search.find_related_papers.return_value = [
            _make_search_result("2301.00001", 0.9),  # same as seed
            _make_search_result("2301.00003", 0.7),
        ]

        result = await find_related_papers(seed_arxiv_ids="2301.00001", ctx=mock_ctx)

        result_ids = [r["paper"]["arxiv_id"] for r in result]
        assert "2301.00001" not in result_ids, "Seed ID should be excluded from results"

    async def test_find_related_returns_list_of_dicts(self, mock_ctx):
        from arxiv_mcp.mcp.tools.discovery import find_related_papers

        result = await find_related_papers(seed_arxiv_ids="2301.00001", ctx=mock_ctx)
        assert isinstance(result, list)
        if result:
            assert isinstance(result[0], dict)


# ---- get_paper tests ----

class TestGetPaper:
    """get_paper fetches paper by arxiv_id from DB and returns dict."""

    async def test_get_paper_returns_paper_dict(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import get_paper

        # Mock the session factory context manager chain
        mock_paper = MagicMock()
        mock_paper.arxiv_id = "2301.00001"
        mock_paper.title = "Test Paper"
        mock_paper.authors_text = "Author One"
        mock_paper.abstract = "Test abstract"
        mock_paper.categories = "cs.AI"
        mock_paper.primary_category = "cs.AI"
        mock_paper.submitted_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
        mock_paper.updated_date = datetime(2023, 1, 2, tzinfo=timezone.utc)
        mock_paper.announced_date = date(2023, 1, 3)
        mock_paper.doi = "10.1234/test"
        mock_paper.license_uri = "http://creativecommons.org/licenses/by/4.0/"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_paper
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        result = await get_paper(arxiv_id="2301.00001", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert result["arxiv_id"] == "2301.00001"
        assert result["title"] == "Test Paper"
        assert result["doi"] == "10.1234/test"

    async def test_get_paper_not_found_returns_error(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.discovery import get_paper

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        result = await get_paper(arxiv_id="9999.99999", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result
        assert "9999.99999" in result["error"]
