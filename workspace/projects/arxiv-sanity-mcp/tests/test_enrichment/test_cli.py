"""Tests for enrichment CLI commands.

Uses Click's CliRunner with monkeypatched EnrichmentService
to test CLI commands without real DB or HTTP calls.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from click.testing import CliRunner

from arxiv_mcp.enrichment.cli import enrich_group
from arxiv_mcp.enrichment.models import (
    EnrichmentResult,
    EnrichmentStatus,
    TopicInfo,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def runner():
    """Click CLI test runner."""
    return CliRunner()


def _mock_success_result(arxiv_id="2301.00001"):
    """Build a mock success EnrichmentResult."""
    return EnrichmentResult(
        openalex_id=f"W{arxiv_id.replace('.', '')}",
        doi=f"10.48550/arXiv.{arxiv_id}",
        cited_by_count=42,
        fwci=1.5,
        topics=[
            TopicInfo(
                id="T1234",
                display_name="Machine Learning",
                score=0.95,
                subfield={"id": "SF1", "display_name": "AI"},
                field={"id": "F1", "display_name": "CS"},
                domain={"id": "D1", "display_name": "Sciences"},
            )
        ],
        related_works=["https://openalex.org/W111", "https://openalex.org/W222"],
        counts_by_year=[{"year": 2023, "cited_by_count": 10}],
        openalex_type="article",
        raw_response={"id": "W230100001"},
        status=EnrichmentStatus.SUCCESS,
        api_version="2026-03-10",
    )


def _mock_enrichment_orm(arxiv_id="2301.00001"):
    """Build a mock PaperEnrichment ORM-like object."""
    mock = MagicMock()
    mock.arxiv_id = arxiv_id
    mock.openalex_id = "W230100001"
    mock.doi = "10.48550/arXiv.2301.00001"
    mock.cited_by_count = 42
    mock.fwci = 1.5
    mock.status = "success"
    mock.source_api = "openalex"
    mock.api_version = "2026-03-10"
    mock.enriched_at = datetime(2026, 3, 10, 0, 0, 0, tzinfo=timezone.utc)
    mock.last_attempted_at = datetime(2026, 3, 10, 0, 0, 0, tzinfo=timezone.utc)
    mock.error_detail = None
    mock.topics = [{"id": "T1234", "display_name": "Machine Learning"}]
    mock.related_works = ["https://openalex.org/W111"]
    return mock


# ---------------------------------------------------------------------------
# Patch helper
# ---------------------------------------------------------------------------


def _make_mock_svc(mock_svc):
    """Create patch contexts that inject mock_svc into CLI commands.

    The CLI commands use lazy import: `from arxiv_mcp.enrichment.service import EnrichmentService`
    inside each function. We patch the class in the source module so when it's imported,
    the mock is returned.
    """
    mock_sf = MagicMock()
    mock_settings = MagicMock()

    return (
        patch("arxiv_mcp.enrichment.cli._make_services", return_value=(mock_sf, mock_settings)),
        patch("arxiv_mcp.enrichment.service.EnrichmentService", return_value=mock_svc),
    )


# ===========================================================================
# Tests
# ===========================================================================


def test_enrich_paper_displays_result(runner):
    """enrich paper <arxiv_id> displays enrichment result."""
    mock_svc = MagicMock()
    mock_svc.enrich_paper = AsyncMock(return_value=_mock_success_result())

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls, patch(
        "arxiv_mcp.enrichment.cli._get_paper_submitted_date",
        new_callable=AsyncMock,
        return_value=datetime(2023, 1, 1, tzinfo=timezone.utc),
    ):
        result = runner.invoke(enrich_group, ["paper", "2301.00001"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert "Enrichment" in result.output
    assert "42" in result.output  # citations
    assert "Machine Learning" in result.output


def test_enrich_paper_refresh(runner):
    """enrich paper <arxiv_id> --refresh passes refresh=True to service."""
    mock_svc = MagicMock()
    mock_svc.enrich_paper = AsyncMock(return_value=_mock_success_result())

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls, patch(
        "arxiv_mcp.enrichment.cli._get_paper_submitted_date",
        new_callable=AsyncMock,
        return_value=None,
    ):
        result = runner.invoke(enrich_group, ["paper", "2301.00001", "--refresh"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    mock_svc.enrich_paper.assert_called_once_with("2301.00001", refresh=True)


def test_enrich_paper_quiet_json(runner):
    """enrich paper <arxiv_id> -q outputs JSON."""
    mock_svc = MagicMock()
    mock_svc.enrich_paper = AsyncMock(return_value=_mock_success_result())

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls:
        result = runner.invoke(enrich_group, ["paper", "2301.00001", "-q"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    data = json.loads(result.output)
    assert data["status"] == "success"
    assert data["cited_by_count"] == 42


def test_enrich_collection_dry_run(runner):
    """enrich collection <slug> --dry-run shows preview."""
    mock_svc = MagicMock()
    mock_svc.enrich_collection = AsyncMock(return_value={
        "total": 5,
        "to_enrich": 3,
        "skipped_cooldown": 2,
    })

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls:
        result = runner.invoke(enrich_group, ["collection", "my-coll", "--dry-run"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert "Dry-run" in result.output
    assert "5" in result.output
    assert "3" in result.output
    mock_svc.enrich_collection.assert_called_once_with("my-coll", refresh=False, dry_run=True)


def test_enrich_status_aggregate(runner):
    """enrich status (no arxiv_id) shows aggregate stats."""
    mock_svc = MagicMock()
    mock_svc.get_enrichment_stats = AsyncMock(return_value={
        "total": 100,
        "success": 80,
        "not_found": 15,
        "partial": 3,
        "error": 2,
        "last_enrichment": datetime(2026, 3, 10, tzinfo=timezone.utc),
    })

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls:
        result = runner.invoke(enrich_group, ["status"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert "100" in result.output
    assert "80" in result.output


def test_enrich_status_per_paper(runner):
    """enrich status <arxiv_id> shows paper-specific enrichment."""
    mock_svc = MagicMock()
    mock_svc.get_enrichment_status = AsyncMock(return_value=_mock_enrichment_orm())

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls:
        result = runner.invoke(enrich_group, ["status", "2301.00001"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    assert "2301.00001" in result.output
    assert "W230100001" in result.output
    assert "success" in result.output


def test_enrich_refresh_command(runner):
    """enrich refresh <arxiv_id> calls enrich_paper with refresh=True."""
    mock_svc = MagicMock()
    mock_svc.enrich_paper = AsyncMock(return_value=_mock_success_result())

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls, patch(
        "arxiv_mcp.enrichment.cli._get_paper_submitted_date",
        new_callable=AsyncMock,
        return_value=None,
    ):
        result = runner.invoke(enrich_group, ["refresh", "2301.00001"])

    assert result.exit_code == 0, f"CLI failed: {result.output}"
    mock_svc.enrich_paper.assert_called_once_with("2301.00001", refresh=True)


def test_enrich_paper_nonexistent_error(runner):
    """Error for non-existent paper shows helpful message."""
    mock_svc = MagicMock()
    mock_svc.enrich_paper = AsyncMock(
        side_effect=ValueError("Paper '9999.99999' not found in database")
    )

    patch_make, patch_cls = _make_mock_svc(mock_svc)

    with patch_make, patch_cls:
        result = runner.invoke(enrich_group, ["paper", "9999.99999"])

    assert result.exit_code == 1
    assert "not found" in result.output
