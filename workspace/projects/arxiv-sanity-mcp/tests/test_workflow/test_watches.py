"""Integration tests for WatchService.

Tests watch promotion, delta tracking, checkpoint auto-advance,
check-all, pause/resume, reset, dashboard, and demote operations.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Paper
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.workflow.queries import SavedQueryService
from arxiv_mcp.workflow.watches import WatchService

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
async def search_service(session_factory):
    """Create a SearchService."""
    settings = get_settings()
    return SearchService(session_factory=session_factory, settings=settings)


@pytest.fixture
async def query_service(session_factory, search_service):
    """Create a SavedQueryService."""
    settings = get_settings()
    return SavedQueryService(
        session_factory=session_factory,
        settings=settings,
        search_service=search_service,
    )


@pytest.fixture
async def watch_service(session_factory, search_service):
    """Create a WatchService."""
    settings = get_settings()
    return WatchService(
        session_factory=session_factory,
        settings=settings,
        search_service=search_service,
    )


@pytest.fixture
async def papers_with_dates(session_factory):
    """Insert papers with different announced_dates for delta testing."""
    async with session_factory() as session:
        dates = [
            date(2023, 1, 1),
            date(2023, 1, 5),
            date(2023, 1, 10),
            date(2023, 1, 15),
            date(2023, 1, 20),
        ]
        for i, d in enumerate(dates, 1):
            data = sample_paper_data(
                arxiv_id=f"2301.0000{i}",
                title=f"Transformer Paper {i}",
                authors_text=f"Author {i}",
                abstract=f"Studying transformer architectures for paper {i}.",
                announced_date=d,
                submitted_date=datetime(2023, 1, i, 12, 0, 0, tzinfo=timezone.utc),
            )
            session.add(Paper(**data))
        await session.commit()


# --- Promote ---


@pytest.mark.asyncio
async def test_promote_to_watch(query_service, watch_service):
    """promote_to_watch sets is_watch=True, cadence_hint, checkpoint_date."""
    await query_service.create_saved_query(
        "Daily Transformers", params={"query_text": "transformer"}
    )
    result = await watch_service.promote_to_watch("daily-transformers", cadence="daily")
    assert result.is_paused is False
    assert result.cadence_hint == "daily"
    assert result.checkpoint_date is not None


@pytest.mark.asyncio
async def test_promote_already_watch_raises(query_service, watch_service):
    """promote_to_watch on existing watch raises ValueError."""
    await query_service.create_saved_query(
        "Already Watch", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("already-watch")
    with pytest.raises(ValueError, match="already a watch"):
        await watch_service.promote_to_watch("already-watch")


# --- Check ---


@pytest.mark.asyncio
async def test_check_watch_returns_delta(
    query_service, watch_service, papers_with_dates
):
    """check_watch returns only papers newer than checkpoint_date."""
    await query_service.create_saved_query(
        "Transformer Watch",
        params={"query_text": "transformer", "time_basis": "announced"},
    )
    # Set checkpoint to Jan 10 -- should get papers after Jan 10
    await watch_service.promote_to_watch("transformer-watch", cadence="daily")
    await watch_service.reset_checkpoint("transformer-watch", date(2023, 1, 10))

    result = await watch_service.check_watch("transformer-watch")
    # Papers with announced_date > 2023-01-10: papers 4 (Jan 15) and 5 (Jan 20)
    announced_dates = [item.paper.announced_date for item in result.items]
    for d in announced_dates:
        assert d > date(2023, 1, 10)


@pytest.mark.asyncio
async def test_check_watch_advances_checkpoint(
    query_service, watch_service, papers_with_dates
):
    """check_watch auto-advances checkpoint_date after check."""
    await query_service.create_saved_query(
        "Advance Watch",
        params={"query_text": "transformer"},
    )
    await watch_service.promote_to_watch("advance-watch")
    old_checkpoint = (await watch_service.get_watch_dashboard()).watches[0].checkpoint_date

    await watch_service.check_watch("advance-watch")

    dashboard = await watch_service.get_watch_dashboard()
    watch = next(w for w in dashboard.watches if w.slug == "advance-watch")
    # Checkpoint should be advanced to today
    assert watch.checkpoint_date >= old_checkpoint


@pytest.mark.asyncio
async def test_check_paused_watch_raises(query_service, watch_service):
    """check_watch on paused watch raises ValueError."""
    await query_service.create_saved_query(
        "Paused Watch", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("paused-watch")
    await watch_service.pause_watch("paused-watch")

    with pytest.raises(ValueError, match="paused"):
        await watch_service.check_watch("paused-watch")


# --- Check all ---


@pytest.mark.asyncio
async def test_check_all_watches(
    query_service, watch_service, papers_with_dates
):
    """check_all_watches runs all active (non-paused) watches."""
    # Create two watches
    await query_service.create_saved_query(
        "Watch A", params={"query_text": "transformer"}
    )
    await query_service.create_saved_query(
        "Watch B", params={"query_text": "transformer"}
    )
    await watch_service.promote_to_watch("watch-a")
    await watch_service.promote_to_watch("watch-b")
    # Pause one
    await watch_service.pause_watch("watch-b")

    results = await watch_service.check_all_watches()
    # Only watch-a should have been checked (watch-b is paused)
    slugs = [r["slug"] for r in results]
    assert "watch-a" in slugs
    assert "watch-b" not in slugs


# --- Pause / Resume ---


@pytest.mark.asyncio
async def test_pause_watch(query_service, watch_service):
    """pause_watch sets is_paused=True."""
    await query_service.create_saved_query(
        "To Pause", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("to-pause")
    result = await watch_service.pause_watch("to-pause")
    assert result.is_paused is True


@pytest.mark.asyncio
async def test_resume_watch(query_service, watch_service):
    """resume_watch sets is_paused=False."""
    await query_service.create_saved_query(
        "To Resume", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("to-resume")
    await watch_service.pause_watch("to-resume")
    result = await watch_service.resume_watch("to-resume")
    assert result.is_paused is False


# --- Reset checkpoint ---


@pytest.mark.asyncio
async def test_reset_checkpoint(query_service, watch_service):
    """reset_checkpoint updates checkpoint_date."""
    await query_service.create_saved_query(
        "Reset Watch", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("reset-watch")
    new_date = date(2023, 6, 1)
    result = await watch_service.reset_checkpoint("reset-watch", new_date)
    assert result.checkpoint_date == new_date


# --- Dashboard ---


@pytest.mark.asyncio
async def test_get_watch_dashboard(query_service, watch_service):
    """get_watch_dashboard returns list of all watches with status info."""
    await query_service.create_saved_query(
        "Dashboard A", params={"query_text": "a"}
    )
    await query_service.create_saved_query(
        "Dashboard B", params={"query_text": "b"}
    )
    await watch_service.promote_to_watch("dashboard-a")
    await watch_service.promote_to_watch("dashboard-b")
    await watch_service.pause_watch("dashboard-b")

    dashboard = await watch_service.get_watch_dashboard()
    assert dashboard.total_active == 1
    assert dashboard.total_paused == 1
    assert len(dashboard.watches) == 2


# --- Demote ---


@pytest.mark.asyncio
async def test_demote_watch(query_service, watch_service):
    """demote_watch clears watch fields, saved query remains."""
    await query_service.create_saved_query(
        "To Demote", params={"query_text": "test"}
    )
    await watch_service.promote_to_watch("to-demote")
    result = await watch_service.demote_watch("to-demote")
    assert result.is_watch is False

    # Saved query should still exist
    from arxiv_mcp.workflow.queries import SavedQueryService

    detail = await query_service.get_saved_query("to-demote")
    assert detail.slug == "to-demote"
