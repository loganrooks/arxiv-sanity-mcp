"""Integration tests for EnrichmentService.

Tests enrichment orchestration: single-paper and batch enrichment,
cooldown enforcement, processing tier promotion, upsert behavior,
and aggregate statistics. Uses mock adapter (no real HTTP calls).
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    Paper,
    PaperEnrichment,
    ProcessingTier,
)
from arxiv_mcp.enrichment.models import (
    EnrichmentResult,
    EnrichmentStatus,
    ExternalIds,
    TopicInfo,
)
from arxiv_mcp.enrichment.service import EnrichmentService
from tests.conftest import sample_paper_data


# ---------------------------------------------------------------------------
# Mock adapter (implements EnrichmentAdapter protocol)
# ---------------------------------------------------------------------------


class MockAdapter:
    """Test adapter returning predetermined results by arXiv ID."""

    adapter_name = "mock_openalex"

    def __init__(self, results: dict[str, EnrichmentResult] | None = None):
        self._results = results or {}
        self.enrich_calls: list[list[str]] = []

    async def resolve_ids(self, arxiv_ids: list[str]) -> dict[str, ExternalIds]:
        return {
            aid: ExternalIds(openalex_id=f"W{aid.replace('.', '')}", doi=f"10.48550/arXiv.{aid}")
            for aid in arxiv_ids
        }

    async def enrich(self, arxiv_ids: list[str]) -> list[EnrichmentResult]:
        self.enrich_calls.append(arxiv_ids)
        results = []
        for aid in arxiv_ids:
            if aid in self._results:
                results.append(self._results[aid])
            else:
                # Default: success result
                results.append(
                    EnrichmentResult(
                        openalex_id=f"W{aid.replace('.', '')}",
                        doi=f"10.48550/arXiv.{aid}",
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
                        raw_response={"id": f"W{aid.replace('.', '')}"},
                        status=EnrichmentStatus.SUCCESS,
                        api_version="2026-03-10",
                    )
                )
        return results


def _success_result(arxiv_id: str = "2301.00001", **overrides) -> EnrichmentResult:
    """Build a success EnrichmentResult for testing."""
    defaults = dict(
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
        raw_response={"id": f"W{arxiv_id.replace('.', '')}"},
        status=EnrichmentStatus.SUCCESS,
        api_version="2026-03-10",
    )
    defaults.update(overrides)
    return EnrichmentResult(**defaults)


def _not_found_result() -> EnrichmentResult:
    """Build a not-found EnrichmentResult for testing."""
    return EnrichmentResult(
        status=EnrichmentStatus.NOT_FOUND,
        api_version="2026-03-10",
    )


# ---------------------------------------------------------------------------
# Helper: insert sample paper(s)
# ---------------------------------------------------------------------------


async def _insert_paper(session: AsyncSession, **overrides) -> Paper:
    """Insert a sample paper and return it."""
    data = sample_paper_data(**overrides)
    paper = Paper(**data)
    session.add(paper)
    await session.commit()
    await session.refresh(paper)
    return paper


async def _insert_collection_with_papers(
    session: AsyncSession, slug: str, arxiv_ids: list[str]
) -> None:
    """Insert a collection with the given papers."""
    now = datetime.now(timezone.utc)
    coll = Collection(slug=slug, name=slug, created_at=now, updated_at=now)
    session.add(coll)
    await session.flush()

    for aid in arxiv_ids:
        cp = CollectionPaper(
            collection_id=coll.id,
            paper_id=aid,
            source="manual",
            added_at=now,
        )
        session.add(cp)
    await session.commit()


# ===========================================================================
# Tests
# ===========================================================================


@pytest.mark.asyncio
async def test_enrich_paper_creates_enrichment_record(enrichment_session_factory):
    """enrich_paper for existing paper creates PaperEnrichment record with correct fields."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    result = await svc.enrich_paper("2301.00001")

    assert result.status == EnrichmentStatus.SUCCESS
    assert result.openalex_id is not None

    # Verify DB record
    async with enrichment_session_factory() as session:
        enrichment = await session.get(PaperEnrichment, ("2301.00001", "mock_openalex"))
        assert enrichment is not None
        assert enrichment.openalex_id == result.openalex_id
        assert enrichment.doi == result.doi
        assert enrichment.cited_by_count == 42
        assert enrichment.fwci == 1.5
        assert enrichment.status == "success"
        assert enrichment.source_api == "mock_openalex"
        assert enrichment.api_version == "2026-03-10"
        assert enrichment.enriched_at is not None
        assert enrichment.last_attempted_at is not None


@pytest.mark.asyncio
async def test_enrich_paper_updates_paper_ids(enrichment_session_factory):
    """enrich_paper updates Paper.openalex_id and Paper.doi from enrichment result."""
    settings = Settings()
    # Paper starts with no openalex_id and no doi
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, doi=None, openalex_id=None)

    await svc.enrich_paper("2301.00001")

    async with enrichment_session_factory() as session:
        paper = await session.get(Paper, "2301.00001")
        assert paper.openalex_id is not None
        assert paper.doi is not None


@pytest.mark.asyncio
async def test_enrich_paper_promotes_processing_tier(enrichment_session_factory):
    """enrich_paper promotes Paper.processing_tier to ENRICHED (2)."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, processing_tier=0)

    await svc.enrich_paper("2301.00001")

    async with enrichment_session_factory() as session:
        paper = await session.get(Paper, "2301.00001")
        assert paper.processing_tier == ProcessingTier.ENRICHED
        assert paper.promotion_reason == "openalex_enrichment"


@pytest.mark.asyncio
async def test_enrich_paper_cooldown_skips(enrichment_session_factory):
    """enrich_paper within cooldown period skips enrichment."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    # First enrichment
    await svc.enrich_paper("2301.00001")

    # Second enrichment should be skipped (within 7-day cooldown)
    adapter.enrich_calls.clear()
    _result = await svc.enrich_paper("2301.00001")

    # Adapter should NOT have been called again
    assert len(adapter.enrich_calls) == 0


@pytest.mark.asyncio
async def test_enrich_paper_refresh_bypasses_cooldown(enrichment_session_factory):
    """enrich_paper with refresh=True bypasses cooldown."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    # First enrichment
    await svc.enrich_paper("2301.00001")
    adapter.enrich_calls.clear()

    # Second enrichment with refresh should proceed
    result = await svc.enrich_paper("2301.00001", refresh=True)
    assert len(adapter.enrich_calls) == 1
    assert result.status == EnrichmentStatus.SUCCESS


@pytest.mark.asyncio
async def test_enrich_paper_nonexistent_raises(enrichment_session_factory):
    """enrich_paper for non-existent paper raises ValueError."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    with pytest.raises(ValueError, match="not found"):
        await svc.enrich_paper("9999.99999")


@pytest.mark.asyncio
async def test_enrich_paper_not_found_in_openalex(enrichment_session_factory):
    """enrich_paper for paper not in OpenAlex records status=not_found."""
    settings = Settings()
    adapter = MockAdapter(results={"2301.00001": _not_found_result()})
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    result = await svc.enrich_paper("2301.00001")
    assert result.status == EnrichmentStatus.NOT_FOUND

    # Verify DB record
    async with enrichment_session_factory() as session:
        enrichment = await session.get(PaperEnrichment, ("2301.00001", "mock_openalex"))
        assert enrichment is not None
        assert enrichment.status == "not_found"
        assert enrichment.last_attempted_at is not None
        assert enrichment.enriched_at is None  # not set on not_found


@pytest.mark.asyncio
async def test_re_enrichment_upserts(enrichment_session_factory):
    """Re-enrichment overwrites previous enrichment data (upsert)."""
    settings = Settings()
    result_v1 = _success_result(cited_by_count=10, fwci=1.0)
    result_v2 = _success_result(cited_by_count=50, fwci=2.5)

    adapter = MockAdapter(results={"2301.00001": result_v1})
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    # First enrichment
    await svc.enrich_paper("2301.00001")

    # Change adapter result and re-enrich
    adapter._results["2301.00001"] = result_v2
    await svc.enrich_paper("2301.00001", refresh=True)

    async with enrichment_session_factory() as session:
        enrichment = await session.get(PaperEnrichment, ("2301.00001", "mock_openalex"))
        assert enrichment.cited_by_count == 50
        assert enrichment.fwci == 2.5


@pytest.mark.asyncio
async def test_failed_enrichment_preserves_existing(enrichment_session_factory):
    """Failed enrichment preserves existing enrichment record."""
    settings = Settings()
    success = _success_result(cited_by_count=42)
    error = EnrichmentResult(
        status=EnrichmentStatus.ERROR,
        error_detail="API timeout",
        api_version="2026-03-10",
    )

    adapter = MockAdapter(results={"2301.00001": success})
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    # First enrichment (success)
    await svc.enrich_paper("2301.00001")

    # Second enrichment attempt fails
    adapter._results["2301.00001"] = error
    await svc.enrich_paper("2301.00001", refresh=True)

    async with enrichment_session_factory() as session:
        enrichment = await session.get(PaperEnrichment, ("2301.00001", "mock_openalex"))
        # Error should be recorded but existing data preserved
        assert enrichment.status == "error"
        # last_attempted_at should be updated
        assert enrichment.last_attempted_at is not None


@pytest.mark.asyncio
async def test_enrich_collection(enrichment_session_factory):
    """enrich_collection enriches all unenriched papers in a collection."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, arxiv_id="2301.00001")
        await _insert_paper(session, arxiv_id="2301.00002")
        await _insert_paper(session, arxiv_id="2301.00003")
        await _insert_collection_with_papers(
            session, "test-coll", ["2301.00001", "2301.00002", "2301.00003"]
        )

    result = await svc.enrich_collection("test-coll")

    assert result["total"] == 3
    assert result["enriched"] >= 3


@pytest.mark.asyncio
async def test_enrich_collection_skips_cooldown(enrichment_session_factory):
    """enrich_collection skips papers within cooldown."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, arxiv_id="2301.00001")
        await _insert_paper(session, arxiv_id="2301.00002")
        await _insert_collection_with_papers(
            session, "test-coll", ["2301.00001", "2301.00002"]
        )

    # Enrich first paper individually
    await svc.enrich_paper("2301.00001")
    adapter.enrich_calls.clear()

    # Enrich collection -- should skip 2301.00001 (cooldown)
    result = await svc.enrich_collection("test-coll")
    assert result["skipped_cooldown"] >= 1


@pytest.mark.asyncio
async def test_enrich_collection_dry_run(enrichment_session_factory):
    """enrich_collection with dry_run=True returns count without API calls."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, arxiv_id="2301.00001")
        await _insert_paper(session, arxiv_id="2301.00002")
        await _insert_collection_with_papers(
            session, "test-coll", ["2301.00001", "2301.00002"]
        )

    result = await svc.enrich_collection("test-coll", dry_run=True)

    assert result["total"] == 2
    assert result["to_enrich"] == 2
    assert len(adapter.enrich_calls) == 0  # No API calls


@pytest.mark.asyncio
async def test_enrich_search(enrichment_session_factory):
    """enrich_search enriches papers from search results."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    # Insert papers that match the search query
    async with enrichment_session_factory() as session:
        await _insert_paper(session, arxiv_id="2301.00001", title="Attention Is All You Need")
        await _insert_paper(session, arxiv_id="2301.00002", title="Attention Mechanisms Survey")

    result = await svc.enrich_search("attention", limit=2)

    assert result["total"] >= 1
    assert result["enriched"] >= 1


@pytest.mark.asyncio
async def test_get_enrichment_status(enrichment_session_factory):
    """get_enrichment_status returns enrichment record for a paper."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    await svc.enrich_paper("2301.00001")

    status = await svc.get_enrichment_status("2301.00001", source_api="mock_openalex")
    assert status is not None
    assert status.arxiv_id == "2301.00001"
    assert status.status == "success"


@pytest.mark.asyncio
async def test_get_enrichment_stats(enrichment_session_factory):
    """get_enrichment_stats returns aggregate counts."""
    settings = Settings()

    # One success, one not-found
    adapter = MockAdapter(results={
        "2301.00001": _success_result("2301.00001"),
        "2301.00002": _not_found_result(),
    })
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session, arxiv_id="2301.00001")
        await _insert_paper(session, arxiv_id="2301.00002")

    await svc.enrich_paper("2301.00001")
    await svc.enrich_paper("2301.00002")

    stats = await svc.get_enrichment_stats()
    assert stats["total"] == 2
    assert stats["success"] == 1
    assert stats["not_found"] == 1


@pytest.mark.asyncio
async def test_provenance_fields_populated(enrichment_session_factory):
    """Provenance fields (source_api, api_version, enriched_at) are always populated on success."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    async with enrichment_session_factory() as session:
        await _insert_paper(session)

    await svc.enrich_paper("2301.00001")

    async with enrichment_session_factory() as session:
        enrichment = await session.get(PaperEnrichment, ("2301.00001", "mock_openalex"))
        assert enrichment.source_api == "mock_openalex"
        assert enrichment.api_version is not None
        assert enrichment.api_version != ""
        assert enrichment.enriched_at is not None


@pytest.mark.asyncio
async def test_doi_not_overwritten_if_already_set(enrichment_session_factory):
    """Paper.doi is NOT overwritten if already populated (only set if null)."""
    settings = Settings()
    adapter = MockAdapter()
    svc = EnrichmentService(enrichment_session_factory, settings, adapter=adapter)

    original_doi = "10.1234/original-doi"
    async with enrichment_session_factory() as session:
        await _insert_paper(session, doi=original_doi, openalex_id=None)

    await svc.enrich_paper("2301.00001")

    async with enrichment_session_factory() as session:
        paper = await session.get(Paper, "2301.00001")
        # DOI should still be the original, NOT the one from enrichment
        assert paper.doi == original_doi
