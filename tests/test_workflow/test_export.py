"""Integration tests for ExportService.

Tests export/import with conflict resolution, stats with insights,
nuclear reset, and paper detail view.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    Paper,
    SavedQuery,
    TriageLog,
    TriageState,
)
from arxiv_mcp.workflow.export import ExportService

from .conftest import sample_paper_data


@pytest.fixture
async def session_factory(test_engine):
    """Create async session factory bound to the test engine."""
    from sqlalchemy import text

    from arxiv_mcp.db.models import Base

    from .conftest import (
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
async def export_service(session_factory):
    """Create an ExportService."""
    settings = get_settings()
    return ExportService(session_factory=session_factory, settings=settings)


@pytest.fixture
async def populated_workflow(session_factory):
    """Populate workflow state for export/stats testing."""
    now = datetime.now(timezone.utc)

    async with session_factory() as session:
        # Create papers
        for i in range(1, 4):
            data = sample_paper_data(
                arxiv_id=f"2301.0000{i}",
                title=f"Test Paper {i}",
                authors_text=f"Author {i}",
                abstract=f"Abstract for paper {i}.",
                announced_date=date(2023, 1, i + 1),
                submitted_date=datetime(
                    2023, 1, i, 12, 0, 0, tzinfo=timezone.utc
                ),
            )
            session.add(Paper(**data))

        # Create a collection with paper 1
        coll = Collection(
            slug="reading-list",
            name="Reading List",
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

        # Triage paper 1 as shortlisted
        session.add(
            TriageState(
                paper_id="2301.00001",
                state="shortlisted",
                updated_at=now,
            )
        )

        # Add a triage log entry
        session.add(
            TriageLog(
                paper_id="2301.00001",
                old_state="unseen",
                new_state="shortlisted",
                timestamp=now,
                source="manual",
                reason="Interesting method",
            )
        )

        # Create a saved query
        session.add(
            SavedQuery(
                slug="daily-transformers",
                name="Daily Transformers",
                params={"query_text": "transformer"},
                run_count=3,
                last_run_at=now,
                is_watch=True,
                cadence_hint="daily",
                checkpoint_date=date(2023, 1, 1),
                last_checked_at=None,  # Not checked yet -> stale
                is_paused=False,
                created_at=now,
                updated_at=now,
            )
        )

        await session.commit()


# --- Export ---


@pytest.mark.asyncio
async def test_export_all(export_service, populated_workflow):
    """export_all returns ExportData with all entity types populated."""
    data = await export_service.export_all()
    assert data.version == "1.0"
    assert data.exported_at is not None
    assert len(data.collections) == 1
    assert len(data.triage_states) == 1
    assert len(data.triage_log) == 1
    assert len(data.saved_queries) == 1


@pytest.mark.asyncio
async def test_export_filtered(export_service, populated_workflow):
    """export_all with entity_types filter exports only specified types."""
    data = await export_service.export_all(entity_types=["collections"])
    assert len(data.collections) == 1
    assert len(data.triage_states) == 0
    assert len(data.triage_log) == 0
    assert len(data.saved_queries) == 0


@pytest.mark.asyncio
async def test_export_to_file(export_service, populated_workflow, tmp_path):
    """export_to_file creates a valid JSON file."""
    file_path = str(tmp_path / "export.json")
    await export_service.export_to_file(file_path)

    content = json.loads(Path(file_path).read_text())
    assert content["version"] == "1.0"
    assert len(content["collections"]) == 1
    assert len(content["saved_queries"]) == 1


# --- Import ---


@pytest.mark.asyncio
async def test_import_skip_strategy(export_service, populated_workflow, tmp_path):
    """import_from_file with skip strategy skips existing slugs."""
    file_path = str(tmp_path / "export.json")
    await export_service.export_to_file(file_path)

    # Import again (should skip existing)
    result = await export_service.import_from_file(file_path, conflict_strategy="skip")
    assert result["skipped_count"] > 0
    assert len(result["warnings"]) > 0


@pytest.mark.asyncio
async def test_import_triage_last_write_wins(
    export_service, session_factory, populated_workflow, tmp_path
):
    """import_from_file triage uses 'last write wins' for conflicts."""
    file_path = str(tmp_path / "export.json")
    await export_service.export_to_file(file_path)

    # Modify existing triage to be older
    older_time = datetime(2020, 1, 1, tzinfo=timezone.utc)
    async with session_factory() as session:
        result = await session.execute(
            select(TriageState).where(TriageState.paper_id == "2301.00001")
        )
        ts = result.scalar_one()
        ts.updated_at = older_time
        await session.commit()

    # Import: the exported state should win (newer timestamp)
    result = await export_service.import_from_file(file_path)
    assert result["imported_count"] > 0


# --- Stats ---


@pytest.mark.asyncio
async def test_get_stats(export_service, populated_workflow):
    """get_stats returns correct counts and at least one insight."""
    stats = await export_service.get_stats()
    assert stats.collection_count >= 1
    assert "shortlisted" in stats.triage_counts
    assert stats.watch_count >= 1
    assert len(stats.insights) >= 1


# --- Nuclear reset ---


@pytest.mark.asyncio
async def test_nuclear_reset(export_service, session_factory, populated_workflow):
    """nuclear_reset clears all workflow tables but preserves papers."""
    await export_service.nuclear_reset()

    async with session_factory() as session:
        # Papers should still exist
        papers = await session.execute(select(Paper))
        assert len(papers.all()) == 3

        # Workflow tables should be empty
        colls = await session.execute(select(Collection))
        assert len(colls.all()) == 0

        triages = await session.execute(select(TriageState))
        assert len(triages.all()) == 0

        queries = await session.execute(select(SavedQuery))
        assert len(queries.all()) == 0


# --- Paper detail ---


@pytest.mark.asyncio
async def test_get_paper_detail(export_service, populated_workflow):
    """get_paper_detail returns paper with triage state and collection list."""
    detail = await export_service.get_paper_detail("2301.00001")

    assert detail["paper"]["arxiv_id"] == "2301.00001"
    assert detail["triage_state"] == "shortlisted"
    assert len(detail["collections"]) == 1
    assert detail["collections"][0]["slug"] == "reading-list"


@pytest.mark.asyncio
async def test_get_paper_detail_unseen(export_service, populated_workflow):
    """get_paper_detail with untriaged paper returns 'unseen'."""
    detail = await export_service.get_paper_detail("2301.00002")
    assert detail["triage_state"] == "unseen"
    assert detail["collections"] == []


@pytest.mark.asyncio
async def test_get_paper_detail_not_found(export_service, populated_workflow):
    """get_paper_detail raises ValueError for nonexistent paper."""
    with pytest.raises(ValueError, match="not found"):
        await export_service.get_paper_detail("9999.99999")
