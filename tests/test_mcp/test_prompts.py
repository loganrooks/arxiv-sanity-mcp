"""Unit tests for MCP prompts: literature_review_session, daily_digest, triage_shortlist.

Tests cover: prompt registration (names, arguments), rendering (valid UserMessage
sequences, conciseness), and error handling (triage_shortlist with missing collection).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest


# ---- Registration tests ----


class TestPromptRegistration:
    """All 3 prompts are registered with correct names on the MCP server."""

    def test_three_prompts_registered(self):
        from arxiv_mcp.mcp.server import mcp

        prompt_names = {p.name for p in mcp._prompt_manager.list_prompts()}
        expected = {"literature_review_session", "daily_digest", "triage_shortlist"}
        assert expected.issubset(prompt_names), (
            f"Missing prompts: {expected - prompt_names}"
        )

    def test_literature_review_session_arguments(self):
        from arxiv_mcp.mcp.server import mcp

        prompt = mcp._prompt_manager.get_prompt("literature_review_session")
        assert prompt is not None
        args = {a.name: a for a in prompt.arguments}
        # seed_query is required
        assert "seed_query" in args
        assert args["seed_query"].required is True
        # category and profile_slug are optional
        assert "category" in args
        assert args["category"].required is False
        assert "profile_slug" in args
        assert args["profile_slug"].required is False

    def test_daily_digest_arguments(self):
        from arxiv_mcp.mcp.server import mcp

        prompt = mcp._prompt_manager.get_prompt("daily_digest")
        assert prompt is not None
        args = {a.name: a for a in prompt.arguments}
        # No required arguments
        for arg in prompt.arguments:
            assert arg.required is False, (
                f"daily_digest arg '{arg.name}' should be optional"
            )
        # profile_slug is optional
        assert "profile_slug" in args

    def test_triage_shortlist_arguments(self):
        from arxiv_mcp.mcp.server import mcp

        prompt = mcp._prompt_manager.get_prompt("triage_shortlist")
        assert prompt is not None
        args = {a.name: a for a in prompt.arguments}
        # collection_slug is required
        assert "collection_slug" in args
        assert args["collection_slug"].required is True
        # profile_slug is optional
        assert "profile_slug" in args
        assert args["profile_slug"].required is False


# ---- Rendering tests ----


class TestLiteratureReviewRendering:
    """literature_review_session renders concise workflow guidance."""

    async def test_renders_non_empty_user_messages(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.literature_review import literature_review_session

        result = await literature_review_session(
            seed_query="attention mechanisms",
            ctx=mock_ctx,
        )
        assert isinstance(result, list)
        assert len(result) > 0
        for msg in result:
            assert msg.role == "user"

    async def test_includes_seed_query_in_output(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.literature_review import literature_review_session

        result = await literature_review_session(
            seed_query="transformer architectures",
            ctx=mock_ctx,
        )
        content = result[0].content.text
        assert "transformer architectures" in content

    async def test_includes_category_when_provided(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.literature_review import literature_review_session

        result = await literature_review_session(
            seed_query="attention",
            category="cs.AI",
            ctx=mock_ctx,
        )
        content = result[0].content.text
        assert "cs.AI" in content

    async def test_includes_profile_context_when_provided(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.literature_review import literature_review_session

        result = await literature_review_session(
            seed_query="attention",
            profile_slug="my-profile",
            ctx=mock_ctx,
        )
        content = result[0].content.text
        assert "my-profile" in content

    async def test_conciseness_under_4000_chars(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.literature_review import literature_review_session

        result = await literature_review_session(
            seed_query="long query with many terms",
            category="cs.AI",
            profile_slug="test-profile",
            ctx=mock_ctx,
        )
        total_chars = sum(len(msg.content.text) for msg in result)
        assert total_chars < 4000, (
            f"Prompt too long: {total_chars} chars (limit 4000)"
        )


class TestDailyDigestRendering:
    """daily_digest renders concise monitoring workflow guidance."""

    async def test_renders_non_empty_user_messages(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.daily_digest import daily_digest

        result = await daily_digest(ctx=mock_ctx)
        assert isinstance(result, list)
        assert len(result) > 0
        for msg in result:
            assert msg.role == "user"

    async def test_mentions_watch_resources(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.daily_digest import daily_digest

        result = await daily_digest(ctx=mock_ctx)
        content = result[0].content.text
        assert "watch://" in content

    async def test_includes_profile_when_provided(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.daily_digest import daily_digest

        result = await daily_digest(profile_slug="my-interests", ctx=mock_ctx)
        content = result[0].content.text
        assert "my-interests" in content

    async def test_conciseness_under_4000_chars(self, mock_ctx):
        from arxiv_mcp.mcp.prompts.daily_digest import daily_digest

        result = await daily_digest(profile_slug="test", ctx=mock_ctx)
        total_chars = sum(len(msg.content.text) for msg in result)
        assert total_chars < 4000, (
            f"Prompt too long: {total_chars} chars (limit 4000)"
        )


class TestTriageShortlistRendering:
    """triage_shortlist renders batch evaluation guidance with live collection state."""

    async def test_renders_non_empty_user_messages(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        # Mock show_collection to return a collection with a paper count
        mock_collection = MagicMock()
        mock_collection.total = 5
        mock_app_context.collections.show_collection = AsyncMock(
            return_value=mock_collection
        )

        result = await triage_shortlist(
            collection_slug="test-coll",
            ctx=mock_ctx,
        )
        assert isinstance(result, list)
        assert len(result) > 0
        for msg in result:
            assert msg.role == "user"

    async def test_includes_paper_count_from_collection(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        mock_collection = MagicMock()
        mock_collection.total = 12
        mock_app_context.collections.show_collection = AsyncMock(
            return_value=mock_collection
        )

        result = await triage_shortlist(
            collection_slug="my-papers",
            ctx=mock_ctx,
        )
        content = result[0].content.text
        assert "12" in content

    async def test_includes_profile_context_when_provided(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        mock_collection = MagicMock()
        mock_collection.total = 3
        mock_app_context.collections.show_collection = AsyncMock(
            return_value=mock_collection
        )

        result = await triage_shortlist(
            collection_slug="test-coll",
            profile_slug="my-profile",
            ctx=mock_ctx,
        )
        content = result[0].content.text
        assert "my-profile" in content

    async def test_error_on_missing_collection(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        mock_app_context.collections.show_collection = AsyncMock(
            side_effect=ValueError("Collection not found: nonexistent")
        )

        result = await triage_shortlist(
            collection_slug="nonexistent",
            ctx=mock_ctx,
        )
        assert isinstance(result, list)
        assert len(result) > 0
        content = result[0].content.text
        assert "not found" in content.lower()

    async def test_conciseness_under_4000_chars(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        mock_collection = MagicMock()
        mock_collection.total = 20
        mock_app_context.collections.show_collection = AsyncMock(
            return_value=mock_collection
        )

        result = await triage_shortlist(
            collection_slug="big-coll",
            profile_slug="test",
            ctx=mock_ctx,
        )
        total_chars = sum(len(msg.content.text) for msg in result)
        assert total_chars < 4000, (
            f"Prompt too long: {total_chars} chars (limit 4000)"
        )
