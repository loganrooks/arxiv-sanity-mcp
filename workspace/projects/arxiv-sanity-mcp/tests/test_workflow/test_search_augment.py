"""Integration tests for WorkflowSearchService.

Tests that search and browse results include triage state
and collection context per paper (WorkflowSearchResult).
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    Paper,
    TriageState,
)
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.workflow.search_augment import WorkflowSearchService

from tests.conftest import sample_paper_data


@pytest.fixture
async def session_factory(test_engine):
    """Create async session factory bound to the test engine."""
    from sqlalchemy import text

    from arxiv_mcp.db.models import Base

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
async def workflow_search_service(session_factory):
    """Create a WorkflowSearchService for testing."""
    settings = get_settings()
    search_service = SearchService(
        session_factory=session_factory, settings=settings
    )
    return WorkflowSearchService(
        session_factory=session_factory,
        settings=settings,
        search_service=search_service,
    )


@pytest.fixture
async def papers_with_triage(session_factory):
    """Insert papers with various triage states and collection memberships."""
    now = datetime.now(timezone.utc)

    async with session_factory() as session:
        # Create 4 papers
        for i in range(1, 5):
            data = sample_paper_data(
                arxiv_id=f"2301.0000{i}",
                title=f"Transformer Architecture Paper {i}",
                authors_text=f"Author {i}",
                abstract=f"This paper studies transformer models and attention mechanisms version {i}.",
                announced_date=date(2023, 1, i + 1),
                submitted_date=datetime(
                    2023, 1, i, 12, 0, 0, tzinfo=timezone.utc
                ),
            )
            session.add(Paper(**data))

        # Triage paper 1 as shortlisted
        session.add(
            TriageState(
                paper_id="2301.00001",
                state="shortlisted",
                updated_at=now,
            )
        )

        # Triage paper 2 as dismissed
        session.add(
            TriageState(
                paper_id="2301.00002",
                state="dismissed",
                updated_at=now,
            )
        )

        # Paper 3: no triage row (should show as "unseen")
        # Paper 4: no triage row (should show as "unseen")

        # Create a collection and add papers 1 and 3
        coll = Collection(
            slug="my-reading-list",
            name="My Reading List",
            is_archived=False,
            created_at=now,
            updated_at=now,
        )
        session.add(coll)
        await session.flush()

        session.add(
            CollectionPaper(
                collection_id=coll.id,
                paper_id="2301.00001",
                source="manual",
                added_at=now,
            )
        )
        session.add(
            CollectionPaper(
                collection_id=coll.id,
                paper_id="2301.00003",
                source="manual",
                added_at=now,
            )
        )

        await session.commit()


# --- Search augmentation ---


@pytest.mark.asyncio
async def test_search_returns_triage_state(
    workflow_search_service, papers_with_triage
):
    """WorkflowSearchService.search_papers returns results with triage_state."""
    result = await workflow_search_service.search_papers(
        query_text="transformer"
    )
    assert len(result.items) > 0

    # Every item should have a triage_state field
    for item in result.items:
        assert hasattr(item, "triage_state")
        assert item.triage_state in (
            "unseen",
            "shortlisted",
            "dismissed",
            "read",
            "cite-later",
            "archived",
        )


@pytest.mark.asyncio
async def test_browse_returns_triage_state(
    workflow_search_service, papers_with_triage
):
    """WorkflowSearchService.browse_recent returns results with triage_state."""
    result = await workflow_search_service.browse_recent(days=365)
    assert len(result.items) > 0

    for item in result.items:
        assert hasattr(item, "triage_state")


@pytest.mark.asyncio
async def test_unseen_papers_show_unseen(
    workflow_search_service, papers_with_triage
):
    """Papers with no triage row show triage_state='unseen'."""
    result = await workflow_search_service.search_papers(
        query_text="transformer"
    )
    # Find papers 3 and 4 (no triage row)
    unseen_papers = [
        item
        for item in result.items
        if item.paper.arxiv_id in ("2301.00003", "2301.00004")
    ]
    for item in unseen_papers:
        assert item.triage_state == "unseen"


@pytest.mark.asyncio
async def test_triaged_papers_show_correct_state(
    workflow_search_service, papers_with_triage
):
    """Papers with triage state show correct state."""
    result = await workflow_search_service.search_papers(
        query_text="transformer"
    )

    # Paper 1 should be shortlisted
    paper1 = next(
        (item for item in result.items if item.paper.arxiv_id == "2301.00001"),
        None,
    )
    assert paper1 is not None
    assert paper1.triage_state == "shortlisted"

    # Paper 2 should be dismissed
    paper2 = next(
        (item for item in result.items if item.paper.arxiv_id == "2301.00002"),
        None,
    )
    assert paper2 is not None
    assert paper2.triage_state == "dismissed"


@pytest.mark.asyncio
async def test_results_include_collection_slugs(
    workflow_search_service, papers_with_triage
):
    """WorkflowSearchResult includes collection_slugs list per paper."""
    result = await workflow_search_service.search_papers(
        query_text="transformer"
    )

    # Paper 1 is in my-reading-list
    paper1 = next(
        (item for item in result.items if item.paper.arxiv_id == "2301.00001"),
        None,
    )
    assert paper1 is not None
    assert "my-reading-list" in paper1.collection_slugs


@pytest.mark.asyncio
async def test_papers_not_in_collections_show_empty(
    workflow_search_service, papers_with_triage
):
    """Papers in no collections show empty collection_slugs list."""
    result = await workflow_search_service.search_papers(
        query_text="transformer"
    )

    # Paper 2 and 4 are not in any collection
    paper2 = next(
        (item for item in result.items if item.paper.arxiv_id == "2301.00002"),
        None,
    )
    assert paper2 is not None
    assert paper2.collection_slugs == []

    paper4 = next(
        (item for item in result.items if item.paper.arxiv_id == "2301.00004"),
        None,
    )
    assert paper4 is not None
    assert paper4.collection_slugs == []
