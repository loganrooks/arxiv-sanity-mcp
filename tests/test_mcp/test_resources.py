"""Unit tests for MCP resource templates.

Tests call resource functions directly with mock context (not through MCP transport).
Covers: paper://{arxiv_id}, collection://{slug}, profile://{slug}, watch://{slug}/deltas.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from arxiv_mcp.enrichment.models import EnrichmentResult, EnrichmentStatus
from arxiv_mcp.models.interest import ProfileDetail, SignalInfo
from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.paper import PaperSummary, SearchResult
from arxiv_mcp.models.workflow import CollectionSummary, WatchSummary


# ---- paper resource tests ----


class TestPaperResource:
    """paper://{arxiv_id} returns composite paper view."""

    async def test_paper_resource_returns_composite(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.paper import paper_resource

        now = datetime.now(timezone.utc)

        # Mock Paper ORM query
        mock_paper = MagicMock()
        mock_paper.arxiv_id = "2301.00001"
        mock_paper.title = "Test Paper"
        mock_paper.authors_text = "Author One"
        mock_paper.abstract = "Test abstract"
        mock_paper.categories = "cs.AI cs.LG"
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

        # Mock triage state
        mock_app_context.triage.get_triage_state = AsyncMock(return_value="shortlisted")

        # Mock enrichment
        mock_enrichment = MagicMock()
        mock_enrichment.openalex_id = "W123"
        mock_enrichment.doi = "10.1234/test"
        mock_enrichment.cited_by_count = 42
        mock_enrichment.fwci = 1.5
        mock_enrichment.status = "success"
        mock_enrichment.source_api = "openalex"
        mock_enrichment.enriched_at = now
        mock_app_context.enrichment.get_enrichment_status = AsyncMock(
            return_value=mock_enrichment
        )

        # Mock collections
        mock_app_context.collections.get_paper_collections = AsyncMock(
            return_value=[
                CollectionSummary(
                    slug="ml-papers",
                    name="ML Papers",
                    paper_count=5,
                    is_archived=False,
                    created_at=now,
                    updated_at=now,
                )
            ]
        )

        result = await paper_resource(arxiv_id="2301.00001", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert result["arxiv_id"] == "2301.00001"
        assert result["title"] == "Test Paper"
        assert result["triage_state"] == "shortlisted"
        assert result["enrichment"] is not None
        assert result["enrichment"]["cited_by_count"] == 42
        assert len(result["collections"]) == 1
        assert result["collections"][0]["slug"] == "ml-papers"

    async def test_paper_resource_not_found(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.paper import paper_resource

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        result = await paper_resource(arxiv_id="9999.99999", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result

    async def test_paper_resource_no_enrichment(self, mock_ctx, mock_app_context):
        """Paper with no enrichment returns enrichment=None."""
        from arxiv_mcp.mcp.resources.paper import paper_resource

        now = datetime.now(timezone.utc)

        mock_paper = MagicMock()
        mock_paper.arxiv_id = "2301.00001"
        mock_paper.title = "Test"
        mock_paper.authors_text = "A"
        mock_paper.abstract = "B"
        mock_paper.categories = "cs.AI"
        mock_paper.primary_category = "cs.AI"
        mock_paper.submitted_date = now
        mock_paper.updated_date = now
        mock_paper.announced_date = date.today()
        mock_paper.doi = None
        mock_paper.license_uri = None

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_paper
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        mock_app_context.triage.get_triage_state = AsyncMock(return_value="unseen")
        mock_app_context.enrichment.get_enrichment_status = AsyncMock(return_value=None)
        mock_app_context.collections.get_paper_collections = AsyncMock(return_value=[])

        result = await paper_resource(arxiv_id="2301.00001", ctx=mock_ctx)

        assert result["enrichment"] is None
        assert result["collections"] == []
        assert result["triage_state"] == "unseen"


# ---- collection resource tests ----


class TestCollectionResource:
    """collection://{slug} delegates to CollectionService.show_collection."""

    async def test_collection_resource_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.collection import collection_resource
        from arxiv_mcp.workflow.collections import CollectionPaperView

        now = datetime.now(timezone.utc)
        mock_app_context.collections.show_collection = AsyncMock(
            return_value=PaginatedResponse[CollectionPaperView](
                items=[
                    CollectionPaperView(
                        arxiv_id="2301.00001",
                        title="Test Paper",
                        source="mcp",
                        added_at=now,
                        triage_state="unseen",
                    )
                ],
                page_info=PageInfo(has_next=False, next_cursor=None, total_estimate=1),
            )
        )

        result = await collection_resource(slug="my-collection", ctx=mock_ctx)

        mock_app_context.collections.show_collection.assert_awaited_once_with("my-collection")
        assert isinstance(result, dict)
        assert "items" in result

    async def test_collection_resource_not_found(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.collection import collection_resource

        mock_app_context.collections.show_collection = AsyncMock(
            side_effect=ValueError("Collection not found: 'no-such'")
        )

        result = await collection_resource(slug="no-such", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result


# ---- profile resource tests ----


class TestProfileResource:
    """profile://{slug} delegates to ProfileService.get_profile."""

    async def test_profile_resource_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.profile import profile_resource

        now = datetime.now(timezone.utc)
        mock_app_context.profiles.get_profile = AsyncMock(
            return_value=ProfileDetail(
                slug="my-profile",
                name="My Profile",
                signal_count=2,
                is_archived=False,
                negative_weight=0.3,
                created_at=now,
                updated_at=now,
                signals=[
                    SignalInfo(
                        signal_type="seed_paper",
                        signal_value="2301.00001",
                        status="active",
                        source="mcp",
                        added_at=now,
                    )
                ],
                signal_counts_by_type={"seed_paper": 1},
                signal_counts_by_source={"mcp": 1},
            )
        )

        result = await profile_resource(slug="my-profile", ctx=mock_ctx)

        mock_app_context.profiles.get_profile.assert_awaited_once_with("my-profile")
        assert isinstance(result, dict)
        assert result["slug"] == "my-profile"
        assert len(result["signals"]) == 1

    async def test_profile_resource_not_found(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.profile import profile_resource

        mock_app_context.profiles.get_profile = AsyncMock(
            side_effect=ValueError("Profile 'no-such' not found")
        )

        result = await profile_resource(slug="no-such", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result


# ---- watch deltas resource tests ----


class TestWatchDeltasResource:
    """watch://{slug}/deltas delegates to WatchService.check_watch."""

    async def test_watch_deltas_delegates(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.watch import watch_deltas_resource

        mock_app_context.watches.check_watch = AsyncMock(
            return_value=PaginatedResponse[SearchResult](
                items=[
                    SearchResult(
                        paper=PaperSummary(
                            arxiv_id="2301.00099",
                            title="New Paper",
                            authors_text="Author",
                            abstract_snippet="Abstract",
                            categories="cs.AI",
                            primary_category="cs.AI",
                            category_list=["cs.AI"],
                            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
                            updated_date=datetime(2023, 1, 2, tzinfo=timezone.utc),
                            announced_date=date(2023, 1, 3),
                            oai_datestamp=date(2023, 1, 3),
                            latest_version=1,
                            license_uri="http://creativecommons.org/licenses/by/4.0/",
                        ),
                        score=0.9,
                    )
                ],
                page_info=PageInfo(has_next=False, next_cursor=None, total_estimate=1),
            )
        )

        result = await watch_deltas_resource(slug="ml-safety", ctx=mock_ctx)

        mock_app_context.watches.check_watch.assert_awaited_once_with("ml-safety")
        assert isinstance(result, dict)
        assert "items" in result
        assert len(result["items"]) == 1

    async def test_watch_deltas_not_found(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.resources.watch import watch_deltas_resource

        mock_app_context.watches.check_watch = AsyncMock(
            side_effect=ValueError("Saved query not found: 'no-such'")
        )

        result = await watch_deltas_resource(slug="no-such", ctx=mock_ctx)

        assert isinstance(result, dict)
        assert "error" in result
