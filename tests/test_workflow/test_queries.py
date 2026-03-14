"""Integration tests for SavedQueryService.

Tests CRUD operations, run with param deserialization,
run_count tracking, and graceful handling of stale references.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Paper
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.workflow.queries import SavedQueryService

from tests.conftest import sample_paper_data


@pytest.fixture
async def session_factory(test_engine):
    """Create async session factory bound to the test engine."""
    from arxiv_mcp.db.models import Base
    from sqlalchemy import text

    from tests.conftest import (
        TSVECTOR_CREATE_TRIGGER_SQL,
        TSVECTOR_DROP_TRIGGER_SQL,
        TSVECTOR_FUNCTION_SQL,
    )

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_FUNCTION_SQL))
        await conn.execute(text(TSVECTOR_DROP_TRIGGER_SQL))
        await conn.execute(text(TSVECTOR_CREATE_TRIGGER_SQL))

    sf = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    yield sf

    async with test_engine.begin() as conn:
        await conn.execute(
            text("DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers")
        )
        await conn.execute(
            text("DROP FUNCTION IF EXISTS papers_search_vector_update()")
        )
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def search_service(session_factory):
    """Create a SearchService for testing query runs."""
    settings = get_settings()
    return SearchService(session_factory=session_factory, settings=settings)


@pytest.fixture
async def query_service(session_factory, search_service):
    """Create a SavedQueryService for testing."""
    settings = get_settings()
    return SavedQueryService(
        session_factory=session_factory,
        settings=settings,
        search_service=search_service,
    )


@pytest.fixture
async def papers_in_db(session_factory):
    """Insert papers with search-relevant content for query runs."""
    async with session_factory() as session:
        for i in range(1, 6):
            announced = date(2023, 1, i + 1)
            data = sample_paper_data(
                arxiv_id=f"2301.0000{i}",
                title=f"Transformer Architecture Paper {i}",
                authors_text=f"Author {i}",
                abstract=f"This paper studies transformer models and attention mechanisms version {i}.",
                announced_date=announced,
                submitted_date=datetime(2023, 1, i, 12, 0, 0, tzinfo=timezone.utc),
            )
            session.add(Paper(**data))
        await session.commit()


# --- Create ---


@pytest.mark.asyncio
async def test_create_saved_query(query_service):
    """create_saved_query creates a query with auto-generated slug."""
    result = await query_service.create_saved_query(
        "Daily Transformers",
        params={"query_text": "transformer", "category": "cs.CL"},
    )
    assert result.slug == "daily-transformers"
    assert result.name == "Daily Transformers"
    assert result.run_count == 0
    assert result.is_watch is False


@pytest.mark.asyncio
async def test_create_duplicate_slug_raises(query_service):
    """create_saved_query with duplicate slug raises ValueError."""
    await query_service.create_saved_query(
        "Daily Transformers",
        params={"query_text": "transformer"},
    )
    with pytest.raises(ValueError, match="already exists"):
        await query_service.create_saved_query(
            "Daily Transformers",
            params={"query_text": "attention"},
        )


# --- List ---


@pytest.mark.asyncio
async def test_list_saved_queries(query_service):
    """list_saved_queries returns all queries with run_count."""
    await query_service.create_saved_query(
        "Query A", params={"query_text": "a"}
    )
    await query_service.create_saved_query(
        "Query B", params={"query_text": "b"}
    )

    queries = await query_service.list_saved_queries()
    assert len(queries) == 2
    slugs = {q.slug for q in queries}
    assert "query-a" in slugs
    assert "query-b" in slugs


# --- Get ---


@pytest.mark.asyncio
async def test_get_saved_query(query_service):
    """get_saved_query returns full detail with params."""
    await query_service.create_saved_query(
        "My Query",
        params={"query_text": "attention", "category": "cs.AI"},
    )
    detail = await query_service.get_saved_query("my-query")
    assert detail.slug == "my-query"
    assert detail.params["query_text"] == "attention"
    assert detail.params["category"] == "cs.AI"


@pytest.mark.asyncio
async def test_get_nonexistent_query_raises(query_service):
    """get_saved_query raises ValueError for nonexistent slug."""
    with pytest.raises(ValueError, match="not found"):
        await query_service.get_saved_query("does-not-exist")


# --- Edit ---


@pytest.mark.asyncio
async def test_edit_saved_query_name(query_service):
    """edit_saved_query updates name and slug."""
    await query_service.create_saved_query(
        "Old Name", params={"query_text": "test"}
    )
    result = await query_service.edit_saved_query("old-name", name="New Name")
    assert result.slug == "new-name"
    assert result.name == "New Name"


@pytest.mark.asyncio
async def test_edit_saved_query_params(query_service):
    """edit_saved_query updates params."""
    await query_service.create_saved_query(
        "My Query", params={"query_text": "old"}
    )
    result = await query_service.edit_saved_query(
        "my-query", params={"query_text": "new", "category": "cs.CL"}
    )
    assert result.params["query_text"] == "new"
    assert result.params["category"] == "cs.CL"


@pytest.mark.asyncio
async def test_edit_saved_query_updates_timestamp(query_service):
    """edit_saved_query updates updated_at."""
    created = await query_service.create_saved_query(
        "Timestamp Query", params={"query_text": "test"}
    )
    edited = await query_service.edit_saved_query(
        "timestamp-query", name="Timestamp Query Updated"
    )
    assert edited.updated_at >= created.created_at


# --- Delete ---


@pytest.mark.asyncio
async def test_delete_saved_query(query_service):
    """delete_saved_query removes the query."""
    await query_service.create_saved_query(
        "To Delete", params={"query_text": "delete me"}
    )
    await query_service.delete_saved_query("to-delete")

    with pytest.raises(ValueError, match="not found"):
        await query_service.get_saved_query("to-delete")


# --- Run ---


@pytest.mark.asyncio
async def test_run_saved_query(query_service, papers_in_db):
    """run_saved_query executes search with stored params."""
    await query_service.create_saved_query(
        "Transformer Search",
        params={"query_text": "transformer"},
    )
    result = await query_service.run_saved_query("transformer-search")
    assert len(result.items) > 0
    # All results should be SearchResult objects
    assert result.items[0].paper.arxiv_id is not None


@pytest.mark.asyncio
async def test_run_saved_query_increments_count(query_service, papers_in_db):
    """run_saved_query increments run_count and sets last_run_at."""
    await query_service.create_saved_query(
        "Counter Query",
        params={"query_text": "transformer"},
    )
    await query_service.run_saved_query("counter-query")
    await query_service.run_saved_query("counter-query")

    detail = await query_service.get_saved_query("counter-query")
    assert detail.run_count == 2
    assert detail.last_run_at is not None


@pytest.mark.asyncio
async def test_run_saved_query_with_date_filter(query_service, papers_in_db):
    """run_saved_query with date_from param filters results."""
    await query_service.create_saved_query(
        "Date Filter Query",
        params={
            "query_text": "transformer",
            "date_from": "2023-01-04",
            "time_basis": "announced",
        },
    )
    result = await query_service.run_saved_query("date-filter-query")
    # Should only get papers announced on or after 2023-01-04
    for item in result.items:
        assert item.paper.announced_date >= date(2023, 1, 4)


@pytest.mark.asyncio
async def test_run_saved_query_category_filter(query_service, papers_in_db):
    """run_saved_query with category param filters correctly."""
    await query_service.create_saved_query(
        "Category Query",
        params={"category": "cs.CL"},
    )
    result = await query_service.run_saved_query("category-query")
    # Our sample papers all have cs.CL
    assert len(result.items) > 0
