"""Shared test fixtures for interest model tests.

Provides async database engine, session with interest tables,
and sample data factories for interest profiles and signals.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Base, Paper, SavedQuery

# SQL statements for the tsvector trigger -- reused from Phase 1 conftest.
TSVECTOR_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION papers_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('simple', COALESCE(NEW.authors_text, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.abstract, '')), 'C');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql
"""

TSVECTOR_DROP_TRIGGER_SQL = (
    "DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers"
)

TSVECTOR_CREATE_TRIGGER_SQL = """
CREATE TRIGGER papers_search_vector_trigger
  BEFORE INSERT OR UPDATE ON papers
  FOR EACH ROW EXECUTE FUNCTION papers_search_vector_update()
"""


def sample_paper_data(**overrides) -> dict:
    """Factory for paper data dicts. Pass overrides for specific fields."""
    defaults = {
        "arxiv_id": "2301.00001",
        "title": "Attention Is All You Need",
        "authors_text": "Ashish Vaswani, Noam Shazeer",
        "abstract": "We propose a new simple network architecture, the Transformer.",
        "submitter": "Ashish Vaswani",
        "comments": "15 pages",
        "journal_ref": None,
        "report_no": None,
        "categories": "cs.CL cs.AI",
        "primary_category": "cs.CL",
        "category_list": ["cs.CL", "cs.AI"],
        "msc_class": None,
        "acm_class": None,
        "doi": None,
        "openalex_id": None,
        "semantic_scholar_id": None,
        "submitted_date": datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "updated_date": datetime(2023, 6, 15, 8, 30, 0, tzinfo=timezone.utc),
        "announced_date": date(2023, 1, 2),
        "oai_datestamp": date(2023, 6, 15),
        "license_uri": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "latest_version": 2,
        "version_history": None,
        "processing_tier": 0,
        "promotion_reason": None,
        "source": "oai_pmh",
        "fetched_at": datetime(2023, 7, 1, 0, 0, 0, tzinfo=timezone.utc),
        "last_metadata_update": None,
    }
    defaults.update(overrides)
    return defaults


def sample_profile_data(**overrides) -> dict:
    """Factory for interest profile data dicts."""
    defaults = {
        "slug": "my-ml-profile",
        "name": "My ML Profile",
        "is_archived": False,
        "negative_weight": 0.3,
        "weights": None,
        "created_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


def sample_signal_data(**overrides) -> dict:
    """Factory for interest signal data dicts."""
    defaults = {
        "signal_type": "seed_paper",
        "signal_value": "2301.00001",
        "status": "active",
        "source": "manual",
        "added_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "reason": None,
    }
    defaults.update(overrides)
    return defaults


def sample_saved_query_data(**overrides) -> dict:
    """Factory for saved query data dicts."""
    defaults = {
        "slug": "daily-transformers",
        "name": "Daily Transformers",
        "params": {"query_text": "transformer", "category": "cs.CL"},
        "run_count": 0,
        "last_run_at": None,
        "is_watch": False,
        "cadence_hint": None,
        "checkpoint_date": None,
        "last_checked_at": None,
        "is_paused": False,
        "created_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


@pytest.fixture
async def test_engine():
    """Create async engine for the test database.

    Function-scoped to avoid event loop issues with asyncpg.
    """
    settings = get_settings()
    engine = create_async_engine(
        settings.test_database_url,
        echo=False,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_session(test_engine):
    """Create all tables (including interest), yield a session, then drop all.

    Also creates the tsvector trigger function and trigger
    since create_all does not run Alembic migrations.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_FUNCTION_SQL))
        await conn.execute(text(TSVECTOR_DROP_TRIGGER_SQL))
        await conn.execute(text(TSVECTOR_CREATE_TRIGGER_SQL))

    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.execute(text("DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers"))
        await conn.execute(text("DROP FUNCTION IF EXISTS papers_search_vector_update()"))
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session_factory(test_engine, test_session):
    """Provide an async_sessionmaker for service tests.

    Depends on test_session to ensure tables exist, but returns
    a fresh session_factory for the service to use.
    """
    factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return factory


@pytest.fixture
async def sample_papers(test_session):
    """Insert 5 sample papers for FK targets and return them."""
    papers = []
    for i in range(1, 6):
        data = sample_paper_data(
            arxiv_id=f"2301.0000{i}",
            title=f"Test Paper {i}",
            authors_text=f"Author {i}",
            abstract=f"Abstract for paper {i}.",
        )
        paper = Paper(**data)
        test_session.add(paper)
        papers.append(paper)
    await test_session.commit()
    return papers


@pytest.fixture
async def sample_saved_query(test_session):
    """Insert a sample saved query for FK targets and return it."""
    data = sample_saved_query_data()
    query = SavedQuery(**data)
    test_session.add(query)
    await test_session.commit()
    return query
