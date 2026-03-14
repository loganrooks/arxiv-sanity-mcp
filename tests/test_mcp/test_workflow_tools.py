"""Unit tests for workflow, interest, and enrichment MCP tools.

Tests call tool functions directly with mock context (not through MCP transport).
Covers: triage_paper, add_to_collection, create_watch, add_signal, enrich_paper.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock


from arxiv_mcp.enrichment.models import EnrichmentResult, EnrichmentStatus
from arxiv_mcp.models.interest import SignalInfo
from arxiv_mcp.models.workflow import (
    CollectionSummary,
    SavedQuerySummary,
    TriageStateResponse,
    WatchSummary,
)


# ---- triage_paper tests ----


class TestTriagePaper:
    """triage_paper delegates to TriageService.mark_triage with source='mcp'."""

    async def test_triage_paper_valid_state(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.workflow import triage_paper

        now = datetime.now(timezone.utc)
        mock_app_context.triage.mark_triage = AsyncMock(
            return_value=TriageStateResponse(
                paper_id="2301.00001", state="shortlisted", updated_at=now
            )
        )

        result = await triage_paper(
            arxiv_id="2301.00001", state="shortlisted", ctx=mock_ctx
        )

        mock_app_context.triage.mark_triage.assert_awaited_once_with(
            paper_id="2301.00001", new_state="shortlisted", source="mcp", reason=None
        )
        assert isinstance(result, dict)
        assert result["arxiv_id"] == "2301.00001"
        assert result["state"] == "shortlisted"
        assert result["updated"] is True

    async def test_triage_paper_with_reason(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.workflow import triage_paper

        now = datetime.now(timezone.utc)
        mock_app_context.triage.mark_triage = AsyncMock(
            return_value=TriageStateResponse(
                paper_id="2301.00001", state="dismissed", updated_at=now
            )
        )

        _result = await triage_paper(
            arxiv_id="2301.00001",
            state="dismissed",
            reason="Not relevant to my research",
            ctx=mock_ctx,
        )

        call_kwargs = mock_app_context.triage.mark_triage.call_args.kwargs
        assert call_kwargs["reason"] == "Not relevant to my research"
        assert call_kwargs["source"] == "mcp"

    async def test_triage_paper_invalid_state_returns_error(
        self, mock_ctx, mock_app_context
    ):
        from arxiv_mcp.mcp.tools.workflow import triage_paper

        mock_app_context.triage.mark_triage = AsyncMock(
            side_effect=ValueError("Invalid triage state: 'bogus'")
        )

        result = await triage_paper(
            arxiv_id="2301.00001", state="bogus", ctx=mock_ctx
        )

        assert isinstance(result, dict)
        assert "error" in result
        assert "bogus" in result["error"]


# ---- add_to_collection tests ----


class TestAddToCollection:
    """add_to_collection delegates to CollectionService with auto-create."""

    async def test_add_to_existing_collection(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.workflow import add_to_collection

        mock_app_context.collections.add_papers = AsyncMock(return_value=1)

        result = await add_to_collection(
            arxiv_id="2301.00001",
            collection_name="My Reading List",
            ctx=mock_ctx,
        )

        mock_app_context.collections.add_papers.assert_awaited_once_with(
            "my-reading-list", ["2301.00001"], source="mcp"
        )
        assert isinstance(result, dict)
        assert result["arxiv_id"] == "2301.00001"
        assert result["collection"] == "my-reading-list"
        assert result["added"] is True

    async def test_add_to_new_collection_creates_first(
        self, mock_ctx, mock_app_context
    ):
        """When collection doesn't exist, create it then add papers."""
        from arxiv_mcp.mcp.tools.workflow import add_to_collection

        now = datetime.now(timezone.utc)
        # First add_papers call fails (collection doesn't exist)
        # Second add_papers call succeeds (after create)
        mock_app_context.collections.add_papers = AsyncMock(
            side_effect=[
                ValueError("Collection not found: 'new-collection'"),
                1,
            ]
        )
        mock_app_context.collections.create_collection = AsyncMock(
            return_value=CollectionSummary(
                slug="new-collection",
                name="New Collection",
                paper_count=0,
                is_archived=False,
                created_at=now,
                updated_at=now,
            )
        )

        result = await add_to_collection(
            arxiv_id="2301.00001",
            collection_name="New Collection",
            ctx=mock_ctx,
        )

        mock_app_context.collections.create_collection.assert_awaited_once_with(
            "New Collection"
        )
        assert mock_app_context.collections.add_papers.await_count == 2
        assert result["added"] is True


# ---- create_watch tests ----


class TestCreateWatch:
    """create_watch creates a saved query then promotes to watch."""

    async def test_create_watch_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.workflow import create_watch

        now = datetime.now(timezone.utc)
        mock_app_context.saved_queries.create_saved_query = AsyncMock(
            return_value=SavedQuerySummary(
                slug="ml-safety",
                name="ML Safety",
                run_count=0,
                last_run_at=None,
                is_watch=False,
                cadence_hint=None,
                created_at=now,
            )
        )
        mock_app_context.watches.promote_to_watch = AsyncMock(
            return_value=WatchSummary(
                slug="ml-safety",
                name="ML Safety",
                cadence_hint="daily",
                checkpoint_date=date.today(),
                last_checked_at=None,
                is_paused=False,
                pending_estimate=None,
            )
        )

        result = await create_watch(
            name="ML Safety",
            query="machine learning safety alignment",
            category="cs.AI",
            cadence="daily",
            ctx=mock_ctx,
        )

        # Verify saved query creation
        sq_call = mock_app_context.saved_queries.create_saved_query.call_args
        assert sq_call.kwargs["name"] == "ML Safety"
        assert sq_call.kwargs["params"]["query_text"] == "machine learning safety alignment"
        assert sq_call.kwargs["params"]["category"] == "cs.AI"

        # Verify watch promotion
        mock_app_context.watches.promote_to_watch.assert_awaited_once_with(
            "ml-safety", cadence="daily"
        )

        assert isinstance(result, dict)
        assert result["slug"] == "ml-safety"


# ---- add_signal tests ----


class TestAddSignal:
    """add_signal delegates to ProfileService.add_signal."""

    async def test_add_signal_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import add_signal

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.add_signal = AsyncMock(
            return_value=SignalInfo(
                signal_type="seed_paper",
                signal_value="2301.00001",
                status="active",
                source="mcp",
                added_at=now,
                reason="Foundational paper",
            )
        )

        result = await add_signal(
            profile_slug="my-profile",
            signal_type="seed_paper",
            signal_value="2301.00001",
            reason="Foundational paper",
            ctx=mock_ctx,
        )

        mock_app_context.profiles.add_signal.assert_awaited_once_with(
            "my-profile", "seed_paper", "2301.00001", source="mcp", reason="Foundational paper"
        )
        assert isinstance(result, dict)
        assert result["signal_type"] == "seed_paper"

    async def test_add_signal_invalid_returns_error(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import add_signal

        mock_app_context.profiles.add_signal = AsyncMock(
            side_effect=ValueError("Invalid signal type: 'bad_type'")
        )

        result = await add_signal(
            profile_slug="my-profile",
            signal_type="bad_type",
            signal_value="test",
            ctx=mock_ctx,
        )

        assert isinstance(result, dict)
        assert "error" in result


# ---- batch_add_signals tests ----


class TestBatchAddSignals:
    """batch_add_signals adds multiple signals in one call with partial-success semantics."""

    async def test_batch_add_all_succeed(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import batch_add_signals

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.add_signal = AsyncMock(
            return_value=SignalInfo(
                signal_type="seed_paper",
                signal_value="2301.00001",
                status="active",
                source="mcp",
                added_at=now,
                reason=None,
            )
        )

        signals = [
            {"signal_type": "seed_paper", "signal_value": "2301.00001", "reason": "Important"},
            {"signal_type": "seed_paper", "signal_value": "2301.00002"},
            {"signal_type": "followed_author", "signal_value": "Jane Doe", "reason": "Key author"},
        ]

        result = await batch_add_signals(
            profile_slug="my-profile",
            signals=signals,
            ctx=mock_ctx,
        )

        assert isinstance(result, dict)
        assert result["profile_slug"] == "my-profile"
        assert result["total"] == 3
        assert result["added"] == 3
        assert result["errors"] == 0
        assert len(result["results"]) == 3
        assert mock_app_context.profiles.add_signal.await_count == 3

    async def test_batch_add_partial_failure(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import batch_add_signals

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.add_signal = AsyncMock(
            side_effect=[
                SignalInfo(
                    signal_type="seed_paper",
                    signal_value="2301.00001",
                    status="active",
                    source="mcp",
                    added_at=now,
                    reason=None,
                ),
                ValueError("Duplicate signal: seed_paper:2301.00002"),
                SignalInfo(
                    signal_type="followed_author",
                    signal_value="Jane Doe",
                    status="active",
                    source="mcp",
                    added_at=now,
                    reason=None,
                ),
            ]
        )

        signals = [
            {"signal_type": "seed_paper", "signal_value": "2301.00001"},
            {"signal_type": "seed_paper", "signal_value": "2301.00002"},
            {"signal_type": "followed_author", "signal_value": "Jane Doe"},
        ]

        result = await batch_add_signals(
            profile_slug="my-profile",
            signals=signals,
            ctx=mock_ctx,
        )

        assert result["total"] == 3
        assert result["added"] == 2
        assert result["errors"] == 1
        assert "error" in result["results"][1]
        assert result["results"][1]["signal_value"] == "2301.00002"

    async def test_batch_add_empty_list(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import batch_add_signals

        result = await batch_add_signals(
            profile_slug="my-profile",
            signals=[],
            ctx=mock_ctx,
        )

        assert result["total"] == 0
        assert result["added"] == 0
        assert result["errors"] == 0
        assert result["results"] == []

    async def test_batch_add_passes_source_mcp(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.interest import batch_add_signals

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.add_signal = AsyncMock(
            return_value=SignalInfo(
                signal_type="seed_paper",
                signal_value="2301.00001",
                status="active",
                source="mcp",
                added_at=now,
                reason=None,
            )
        )

        await batch_add_signals(
            profile_slug="my-profile",
            signals=[{"signal_type": "seed_paper", "signal_value": "2301.00001"}],
            ctx=mock_ctx,
        )

        call_args = mock_app_context.profiles.add_signal.call_args
        assert call_args[1].get("source") is None or "mcp" in str(call_args)
        # Check positional args or kwargs for source="mcp"
        mock_app_context.profiles.add_signal.assert_awaited_once_with(
            "my-profile", "seed_paper", "2301.00001", source="mcp", reason=None
        )


# ---- enrich_paper tests ----


class TestEnrichPaper:
    """enrich_paper delegates to EnrichmentService.enrich_paper."""

    async def test_enrich_paper_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.enrichment import enrich_paper

        mock_app_context.enrichment.enrich_paper = AsyncMock(
            return_value=EnrichmentResult(
                status=EnrichmentStatus.SUCCESS,
                openalex_id="W123456",
                doi="10.1234/test",
                cited_by_count=42,
                fwci=1.5,
            )
        )

        result = await enrich_paper(arxiv_id="2301.00001", ctx=mock_ctx)

        mock_app_context.enrichment.enrich_paper.assert_awaited_once_with(
            "2301.00001", refresh=False
        )
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert result["cited_by_count"] == 42

    async def test_enrich_paper_with_refresh(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.enrichment import enrich_paper

        mock_app_context.enrichment.enrich_paper = AsyncMock(
            return_value=EnrichmentResult(
                status=EnrichmentStatus.SUCCESS,
                openalex_id="W123456",
            )
        )

        await enrich_paper(arxiv_id="2301.00001", refresh=True, ctx=mock_ctx)

        mock_app_context.enrichment.enrich_paper.assert_awaited_once_with(
            "2301.00001", refresh=True
        )

    async def test_enrich_paper_error_returns_dict(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.enrichment import enrich_paper

        mock_app_context.enrichment.enrich_paper = AsyncMock(
            side_effect=ValueError("Paper '9999.99999' not found in database")
        )

        result = await enrich_paper(arxiv_id="9999.99999", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result
