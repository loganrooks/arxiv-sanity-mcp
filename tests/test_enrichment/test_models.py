"""Unit tests for enrichment Pydantic schemas and ORM model.

Tests EnrichmentResult, TopicInfo, ExternalIds, EnrichmentStatus parsing
and validation, plus PaperEnrichment ORM model creation and constraints.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from tests.conftest import sample_paper_data
from arxiv_mcp.db.models import Paper, PaperEnrichment
from arxiv_mcp.enrichment.models import (
    EnrichmentResult,
    EnrichmentStatus,
    ExternalIds,
    TopicInfo,
)


class TestEnrichmentStatus:
    """Tests for EnrichmentStatus enum."""

    def test_success_status(self):
        assert EnrichmentStatus.SUCCESS == "success"

    def test_not_found_status(self):
        assert EnrichmentStatus.NOT_FOUND == "not_found"

    def test_partial_status(self):
        assert EnrichmentStatus.PARTIAL == "partial"

    def test_error_status(self):
        assert EnrichmentStatus.ERROR == "error"

    def test_invalid_status_raises(self):
        with pytest.raises(ValueError):
            EnrichmentStatus("invalid")


class TestTopicInfo:
    """Tests for TopicInfo Pydantic model."""

    def test_parse_full_topic(self, openalex_work_fixture):
        """TopicInfo parses 4-level hierarchy (domain, field, subfield, topic with score)."""
        topic_data = openalex_work_fixture["topics"][0]
        topic = TopicInfo.model_validate(topic_data)

        assert topic.id == "T10032"  # Short form, stripped URL prefix
        assert topic.display_name == "Natural Language Processing Techniques"
        assert topic.score == 0.999
        assert topic.subfield["display_name"] == "Artificial Intelligence"
        assert topic.field["display_name"] == "Computer Science"
        assert topic.domain["display_name"] == "Physical Sciences"

    def test_parse_topic_extracts_short_id(self):
        """TopicInfo stores short-form ID (not full URL)."""
        topic = TopicInfo(
            id="https://openalex.org/T10032",
            display_name="NLP",
            score=0.9,
            subfield={"id": "S1", "display_name": "AI"},
            field={"id": "F1", "display_name": "CS"},
            domain={"id": "D1", "display_name": "Physical Sciences"},
        )
        assert topic.id == "T10032"


class TestExternalIds:
    """Tests for ExternalIds Pydantic model."""

    def test_stores_short_openalex_id(self):
        """ExternalIds stores short-form OpenAlex ID (W-prefixed, not full URL)."""
        ids = ExternalIds(
            openalex_id="https://openalex.org/W2741809807",
            doi="https://doi.org/10.48550/arxiv.1706.03762",
        )
        assert ids.openalex_id == "W2741809807"

    def test_stores_doi_without_prefix(self):
        """ExternalIds stores DOI without https://doi.org/ prefix."""
        ids = ExternalIds(
            openalex_id="W2741809807",
            doi="https://doi.org/10.48550/arxiv.1706.03762",
        )
        assert ids.doi == "10.48550/arxiv.1706.03762"

    def test_none_values_allowed(self):
        """ExternalIds allows None for both fields."""
        ids = ExternalIds(openalex_id=None, doi=None)
        assert ids.openalex_id is None
        assert ids.doi is None


class TestEnrichmentResult:
    """Tests for EnrichmentResult Pydantic model."""

    def test_parse_full_openalex_work(self, openalex_work_fixture):
        """EnrichmentResult parses a full OpenAlex Work response with all fields."""
        result = EnrichmentResult.from_openalex_work(openalex_work_fixture)

        assert result.openalex_id == "W2741809807"
        assert result.doi == "10.48550/arxiv.1706.03762"
        assert result.cited_by_count == 6497
        assert result.fwci == pytest.approx(115.7593)
        assert result.openalex_type == "preprint"
        assert result.status == EnrichmentStatus.SUCCESS
        assert result.error_detail is None

        # Topics
        assert result.topics is not None
        assert len(result.topics) == 3
        assert result.topics[0].display_name == "Natural Language Processing Techniques"
        assert result.topics[0].score == 0.999

        # Related works
        assert result.related_works is not None
        assert len(result.related_works) == 10
        assert "https://openalex.org/W2965373594" in result.related_works

        # Counts by year
        assert result.counts_by_year is not None
        assert len(result.counts_by_year) == 6

        # Raw response stored
        assert result.raw_response is not None
        assert result.raw_response["id"] == "https://openalex.org/W2741809807"

        # API version is a date string
        assert result.api_version is not None

    def test_handles_missing_fwci(self, openalex_batch_fixture):
        """EnrichmentResult handles missing/null FWCI gracefully (fwci=None)."""
        # Second work in batch has fwci=null
        work = openalex_batch_fixture["results"][1]
        result = EnrichmentResult.from_openalex_work(work)

        assert result.fwci is None
        assert result.cited_by_count == 42

    def test_handles_partial_response(self, openalex_batch_fixture):
        """EnrichmentResult handles partial response (no topics, no related_works) with status='partial'."""
        # Second work: has cited_by_count but no fwci, no topics
        work = openalex_batch_fixture["results"][1]
        result = EnrichmentResult.from_openalex_work(work)

        assert result.status == EnrichmentStatus.PARTIAL
        assert result.cited_by_count == 42
        assert result.fwci is None

    def test_from_openalex_work_sets_api_version(self, openalex_work_fixture):
        """from_openalex_work sets api_version to current date string."""
        result = EnrichmentResult.from_openalex_work(openalex_work_fixture)
        # api_version should be a date string like "2026-03-09"
        assert len(result.api_version) == 10
        assert "-" in result.api_version


class TestPaperEnrichmentORM:
    """Tests for PaperEnrichment ORM model."""

    @pytest.mark.asyncio
    async def test_create_and_query(self, enrichment_session_factory):
        """PaperEnrichment ORM model can be created and queried with all columns."""
        now = datetime.now(tz=timezone.utc)

        async with enrichment_session_factory() as session:
            # Insert a paper first (FK requirement)
            paper = Paper(**sample_paper_data())
            session.add(paper)
            await session.flush()

            enrichment = PaperEnrichment(
                arxiv_id="2301.00001",
                openalex_id="W2741809807",
                doi="10.48550/arXiv.2301.00001",
                cited_by_count=100,
                fwci=1.5,
                topics=[{"id": "T10032", "display_name": "NLP", "score": 0.9}],
                related_works=["https://openalex.org/W123"],
                counts_by_year=[{"year": 2026, "cited_by_count": 50}],
                openalex_type="preprint",
                openalex_raw={"id": "https://openalex.org/W2741809807"},
                source_api="openalex",
                api_version="2026-03-09",
                enriched_at=now,
                last_attempted_at=now,
                status="success",
                error_detail=None,
            )
            session.add(enrichment)
            await session.commit()

            # Query it back
            result = await session.execute(
                select(PaperEnrichment).where(PaperEnrichment.arxiv_id == "2301.00001")
            )
            row = result.scalar_one()
            assert row.openalex_id == "W2741809807"
            assert row.cited_by_count == 100
            assert row.fwci == 1.5
            assert row.topics[0]["display_name"] == "NLP"
            assert row.status == "success"
            assert row.source_api == "openalex"

    @pytest.mark.asyncio
    async def test_unique_constraint_prevents_duplicates(self, enrichment_session_factory):
        """PaperEnrichment unique constraint on arxiv_id prevents duplicate records."""
        now = datetime.now(tz=timezone.utc)

        async with enrichment_session_factory() as session:
            paper = Paper(**sample_paper_data())
            session.add(paper)
            await session.flush()

            enrichment1 = PaperEnrichment(
                arxiv_id="2301.00001",
                openalex_id="W111",
                last_attempted_at=now,
                status="success",
            )
            session.add(enrichment1)
            await session.commit()

        # Try inserting a duplicate in a new session
        async with enrichment_session_factory() as session:
            enrichment2 = PaperEnrichment(
                arxiv_id="2301.00001",
                openalex_id="W222",
                last_attempted_at=now,
                status="success",
            )
            session.add(enrichment2)
            with pytest.raises(IntegrityError):
                await session.commit()
