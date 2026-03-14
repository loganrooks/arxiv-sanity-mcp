"""Unit tests for create_profile and suggest_signals MCP tools.

Tests call tool functions directly with mock context (not through MCP transport).
Covers: create_profile (happy path, negative_weight, error), suggest_signals
(happy path, auto_add, error), SuggestionCandidate serialization via dataclasses.asdict,
and AppContext spec including profile_ranking and suggestions attributes.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone
from unittest.mock import AsyncMock


from arxiv_mcp.interest.suggestions import SuggestionCandidate
from arxiv_mcp.mcp.server import AppContext
from arxiv_mcp.models.interest import ProfileSummary, SignalInfo


# ---- AppContext spec ----


class TestAppContextSpec:
    """AppContext dataclass includes profile_ranking and suggestions fields."""

    def test_appcontext_has_profile_ranking_field(self):
        fields = {f.name for f in dataclasses.fields(AppContext)}
        assert "profile_ranking" in fields

    def test_appcontext_has_suggestions_field(self):
        fields = {f.name for f in dataclasses.fields(AppContext)}
        assert "suggestions" in fields


# ---- create_profile tests ----


class TestCreateProfile:
    """create_profile delegates to ProfileService.create_profile."""

    async def test_create_profile_happy_path(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import create_profile

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.create_profile = AsyncMock(
            return_value=ProfileSummary(
                slug="my-research",
                name="My Research",
                signal_count=0,
                is_archived=False,
                negative_weight=0.3,
                created_at=now,
                updated_at=now,
            )
        )

        result = await create_profile(name="My Research", ctx=mock_ctx)

        mock_app_context.profiles.create_profile.assert_awaited_once_with(
            "My Research", negative_weight=None
        )
        assert isinstance(result, dict)
        assert result["slug"] == "my-research"
        assert result["name"] == "My Research"
        assert result["signal_count"] == 0
        assert "created_at" in result

    async def test_create_profile_with_negative_weight(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import create_profile

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.create_profile = AsyncMock(
            return_value=ProfileSummary(
                slug="custom-weight",
                name="Custom Weight",
                signal_count=0,
                is_archived=False,
                negative_weight=0.5,
                created_at=now,
                updated_at=now,
            )
        )

        result = await create_profile(
            name="Custom Weight", negative_weight=0.5, ctx=mock_ctx
        )

        mock_app_context.profiles.create_profile.assert_awaited_once_with(
            "Custom Weight", negative_weight=0.5
        )
        assert result["negative_weight"] == 0.5

    async def test_create_profile_error_returns_error_dict(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import create_profile

        mock_app_context.profiles.create_profile = AsyncMock(
            side_effect=ValueError("Profile with slug 'duplicate' already exists")
        )

        result = await create_profile(name="Duplicate", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result
        assert "duplicate" in result["error"]


# ---- suggest_signals tests ----


class TestSuggestSignals:
    """suggest_signals delegates to SuggestionService."""

    async def test_suggest_signals_happy_path(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import suggest_signals

        mock_app_context.suggestions.generate_suggestions = AsyncMock(
            return_value=[
                SuggestionCandidate(
                    signal_type="seed_paper",
                    signal_value="2301.00001",
                    reason="Triaged as shortlisted",
                    score=2.0,
                ),
                SuggestionCandidate(
                    signal_type="followed_author",
                    signal_value="jane doe",
                    reason="Appears in 5 shortlisted papers",
                    score=5.0,
                ),
            ]
        )

        result = await suggest_signals(profile_slug="my-profile", ctx=mock_ctx)

        mock_app_context.suggestions.generate_suggestions.assert_awaited_once_with(
            "my-profile"
        )
        assert isinstance(result, dict)
        assert len(result["candidates"]) == 2
        assert result["added_count"] == 0
        # Verify candidate dict shape (serialized via dataclasses.asdict)
        candidate = result["candidates"][0]
        assert candidate["signal_type"] == "seed_paper"
        assert candidate["signal_value"] == "2301.00001"
        assert candidate["reason"] == "Triaged as shortlisted"
        assert candidate["score"] == 2.0

    async def test_suggest_signals_auto_add(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import suggest_signals

        candidates = [
            SuggestionCandidate(
                signal_type="seed_paper",
                signal_value="2301.00001",
                reason="Triaged as shortlisted",
                score=2.0,
            ),
        ]
        now = datetime.now(timezone.utc)

        mock_app_context.suggestions.generate_suggestions = AsyncMock(
            return_value=candidates
        )
        mock_app_context.suggestions.add_suggestions_to_profile = AsyncMock(
            return_value=[
                SignalInfo(
                    signal_type="seed_paper",
                    signal_value="2301.00001",
                    status="pending",
                    source="suggestion",
                    added_at=now,
                    reason="Triaged as shortlisted",
                ),
            ]
        )

        result = await suggest_signals(
            profile_slug="my-profile", auto_add=True, ctx=mock_ctx
        )

        mock_app_context.suggestions.add_suggestions_to_profile.assert_awaited_once_with(
            "my-profile", candidates
        )
        assert result["added_count"] == 1

    async def test_suggest_signals_error_returns_error_dict(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import suggest_signals

        mock_app_context.suggestions.generate_suggestions = AsyncMock(
            side_effect=ValueError("Profile 'nonexistent' not found")
        )

        result = await suggest_signals(profile_slug="nonexistent", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result
        assert "nonexistent" in result["error"]

    async def test_suggestion_candidate_serialized_via_asdict(self, mock_ctx, mock_app_context):
        """SuggestionCandidate is a dataclass -- serialized via dataclasses.asdict, not model_dump."""
        from arxiv_mcp.mcp.tools.interest import suggest_signals

        candidate = SuggestionCandidate(
            signal_type="saved_query",
            signal_value="ml-safety",
            reason="Run 5 times",
            score=5.0,
        )
        mock_app_context.suggestions.generate_suggestions = AsyncMock(
            return_value=[candidate]
        )

        result = await suggest_signals(profile_slug="my-profile", ctx=mock_ctx)

        # dataclasses.asdict produces a plain dict with all fields
        expected = dataclasses.asdict(candidate)
        assert result["candidates"][0] == expected
