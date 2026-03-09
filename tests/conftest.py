"""Shared test fixtures for arxiv-mcp test suite.

Provides async database engine, session, and sample paper data
for all test modules.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Base, Paper

# SQL for the tsvector trigger function -- mirrors the Alembic migration.
# We create it manually in tests because SQLAlchemy's create_all does not
# run Alembic migrations.
TSVECTOR_TRIGGER_SQL = """
CREATE OR REPLACE FUNCTION papers_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('simple', COALESCE(NEW.authors_text, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.abstract, '')), 'C');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers;

CREATE TRIGGER papers_search_vector_trigger
  BEFORE INSERT OR UPDATE ON papers
  FOR EACH ROW EXECUTE FUNCTION papers_search_vector_update();
"""


def sample_paper_data(**overrides) -> dict:
    """Factory function returning a dict with all required Paper fields.

    Pass keyword arguments to override any field.
    """
    defaults = {
        "arxiv_id": "2301.00001",
        "title": "Attention Is All You Need",
        "authors_text": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit",
        "abstract": (
            "The dominant sequence transduction models are based on complex recurrent "
            "or convolutional neural networks that include an encoder and a decoder. "
            "The best performing models also connect the encoder and decoder through "
            "an attention mechanism. We propose a new simple network architecture, "
            "the Transformer, based solely on attention mechanisms."
        ),
        "submitter": "Ashish Vaswani",
        "comments": "15 pages, 5 figures",
        "journal_ref": None,
        "report_no": None,
        "categories": "cs.CL cs.AI cs.LG",
        "primary_category": "cs.CL",
        "category_list": ["cs.CL", "cs.AI", "cs.LG"],
        "msc_class": None,
        "acm_class": None,
        "doi": "10.48550/arXiv.2301.00001",
        "openalex_id": None,
        "semantic_scholar_id": None,
        "submitted_date": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "updated_date": datetime(2023, 6, 15, 8, 30, 0, tzinfo=timezone.utc),
        "announced_date": date(2023, 1, 2),
        "oai_datestamp": date(2023, 6, 15),
        "license_uri": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "latest_version": 2,
        "version_history": [
            {"version": "v1", "date": "2023-01-01", "size": "45kb"},
            {"version": "v2", "date": "2023-06-15", "size": "48kb"},
        ],
        "processing_tier": 0,
        "promotion_reason": None,
        "source": "oai_pmh",
        "fetched_at": datetime(2023, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "last_metadata_update": None,
    }
    defaults.update(overrides)
    return defaults


@pytest.fixture(scope="session")
def test_engine():
    """Create async engine for the test database."""
    settings = get_settings()
    engine = create_async_engine(
        settings.test_database_url,
        echo=False,
        pool_pre_ping=True,
    )
    return engine


@pytest.fixture
async def test_session(test_engine):
    """Create tables, yield a session, then drop tables.

    Also creates the tsvector trigger function and trigger
    since create_all does not run Alembic migrations.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_TRIGGER_SQL))

    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def sample_paper(test_session):
    """Insert a sample paper and return it."""
    data = sample_paper_data()
    paper = Paper(**data)
    test_session.add(paper)
    await test_session.commit()
    return paper
