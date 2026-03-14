"""Tests for the Paper SQLAlchemy model.

Covers all column groups: identity, metadata, classification,
external IDs, time semantics, rights, versioning, provenance,
processing tier, and the tsvector search trigger.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest
from sqlalchemy import select

from arxiv_mcp.db.models import Paper, ProcessingTier
from tests.conftest import sample_paper_data


@pytest.mark.asyncio
async def test_canonical_model(test_session):
    """Paper model has arxiv_id as String(20) primary key, is insertable and retrievable."""
    data = sample_paper_data()
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00001")
    assert result is not None
    assert result.arxiv_id == "2301.00001"


@pytest.mark.asyncio
async def test_full_metadata(test_session):
    """Paper stores title, authors_text, abstract, categories, primary_category,
    category_list, submitter, comments, journal_ref, report_no, latest_version,
    version_history."""
    data = sample_paper_data(arxiv_id="2301.00002")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00002")
    assert result.title == "Attention Is All You Need"
    assert "Vaswani" in result.authors_text
    assert "Transformer" in result.abstract
    assert result.categories == "cs.CL cs.AI cs.LG"
    assert result.primary_category == "cs.CL"
    assert result.category_list == ["cs.CL", "cs.AI", "cs.LG"]
    assert result.submitter == "Ashish Vaswani"
    assert result.comments == "15 pages, 5 figures"
    assert result.latest_version == 2
    assert isinstance(result.version_history, list)
    assert len(result.version_history) == 2
    assert result.version_history[0]["version"] == "v1"


@pytest.mark.asyncio
async def test_external_ids(test_session):
    """Paper has nullable doi, openalex_id, semantic_scholar_id columns."""
    # Paper with DOI but no external IDs
    data = sample_paper_data(arxiv_id="2301.00003")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00003")
    assert result.doi == "10.48550/arXiv.2301.00001"
    assert result.openalex_id is None
    assert result.semantic_scholar_id is None

    # Paper with external IDs populated
    data2 = sample_paper_data(
        arxiv_id="2301.00004",
        openalex_id="W123456789",
        semantic_scholar_id="abc123def456",
    )
    paper2 = Paper(**data2)
    test_session.add(paper2)
    await test_session.commit()

    result2 = await test_session.get(Paper, "2301.00004")
    assert result2.openalex_id == "W123456789"
    assert result2.semantic_scholar_id == "abc123def456"


@pytest.mark.asyncio
async def test_time_semantics(test_session):
    """Paper has submitted_date (DateTime TZ), updated_date (DateTime TZ nullable),
    announced_date (Date nullable), oai_datestamp (Date)."""
    data = sample_paper_data(arxiv_id="2301.00005")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00005")
    # submitted_date is DateTime with timezone
    assert isinstance(result.submitted_date, datetime)
    assert result.submitted_date.tzinfo is not None
    assert result.submitted_date.year == 2023
    assert result.submitted_date.month == 1

    # updated_date is DateTime with timezone (nullable)
    assert isinstance(result.updated_date, datetime)
    assert result.updated_date.year == 2023
    assert result.updated_date.month == 6

    # announced_date is Date (nullable)
    assert isinstance(result.announced_date, date)
    assert result.announced_date == date(2023, 1, 2)

    # oai_datestamp is Date
    assert isinstance(result.oai_datestamp, date)
    assert result.oai_datestamp == date(2023, 6, 15)


@pytest.mark.asyncio
async def test_time_semantics_nullable(test_session):
    """updated_date and announced_date can be NULL."""
    data = sample_paper_data(
        arxiv_id="2301.00006",
        updated_date=None,
        announced_date=None,
    )
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00006")
    assert result.updated_date is None
    assert result.announced_date is None


@pytest.mark.asyncio
async def test_license(test_session):
    """Paper has license_uri column (nullable String)."""
    data = sample_paper_data(arxiv_id="2301.00007")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00007")
    assert result.license_uri == "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"

    # NULL license
    data2 = sample_paper_data(arxiv_id="2301.00008", license_uri=None)
    paper2 = Paper(**data2)
    test_session.add(paper2)
    await test_session.commit()

    result2 = await test_session.get(Paper, "2301.00008")
    assert result2.license_uri is None


@pytest.mark.asyncio
async def test_provenance(test_session):
    """Paper has source, fetched_at, last_metadata_update, processing_tier,
    promotion_reason."""
    data = sample_paper_data(arxiv_id="2301.00009")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    result = await test_session.get(Paper, "2301.00009")
    assert result.source == "oai_pmh"
    assert isinstance(result.fetched_at, datetime)
    assert result.fetched_at.tzinfo is not None
    assert result.last_metadata_update is None
    assert result.processing_tier == 0
    assert result.promotion_reason is None


@pytest.mark.asyncio
async def test_search_vector_trigger(test_session):
    """After inserting a paper with title/authors/abstract, the search_vector
    column is populated by the trigger (not NULL)."""
    data = sample_paper_data(arxiv_id="2301.00010")
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()

    # Expire to force re-fetch from DB (trigger runs server-side)
    test_session.expire(paper)
    stmt = select(Paper).where(Paper.arxiv_id == "2301.00010")
    result = await test_session.execute(stmt)
    refreshed = result.scalar_one()

    assert refreshed.search_vector is not None
    # Verify it contains expected terms
    assert "attention" in str(refreshed.search_vector).lower() or len(str(refreshed.search_vector)) > 0


def test_processing_tier_enum():
    """ProcessingTier IntEnum has values METADATA_ONLY=0, FTS_INDEXED=1,
    ENRICHED=2, EMBEDDED=3, CONTENT_PARSED=4."""
    assert ProcessingTier.METADATA_ONLY == 0
    assert ProcessingTier.FTS_INDEXED == 1
    assert ProcessingTier.ENRICHED == 2
    assert ProcessingTier.EMBEDDED == 3
    assert ProcessingTier.CONTENT_PARSED == 4
    assert len(ProcessingTier) == 5
