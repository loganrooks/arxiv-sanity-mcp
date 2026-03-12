"""Integration tests for TriageService.

Tests single triage, batch triage (ID-based and query-based with dry-run),
triage state listing, and audit log. All tests run against PostgreSQL.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Paper, TriageState, TriageLog
from arxiv_mcp.workflow.triage import TriageService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def session_factory(test_engine):
    """Provide async_sessionmaker for service DI."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture
async def svc(session_factory):
    """TriageService instance with settings."""
    settings = get_settings()
    return TriageService(session_factory, settings)


# ---------------------------------------------------------------------------
# Single triage tests
# ---------------------------------------------------------------------------


class TestMarkTriage:
    async def test_mark_triage_creates_state_and_log(self, svc, sample_papers):
        result = await svc.mark_triage("2301.00001", "shortlisted")
        assert result.paper_id == "2301.00001"
        assert result.state == "shortlisted"
        # Check audit log
        log = await svc.get_triage_log("2301.00001")
        assert len(log) == 1
        assert log[0].old_state == "unseen"
        assert log[0].new_state == "shortlisted"

    async def test_mark_triage_updates_existing(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted")
        result = await svc.mark_triage("2301.00001", "read")
        assert result.state == "read"
        log = await svc.get_triage_log("2301.00001")
        assert len(log) == 2
        assert log[1].old_state == "shortlisted"
        assert log[1].new_state == "read"

    async def test_mark_triage_with_reason(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted", reason="interesting method")
        log = await svc.get_triage_log("2301.00001")
        assert log[0].reason == "interesting method"

    async def test_mark_triage_with_source(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted", source="agent")
        log = await svc.get_triage_log("2301.00001")
        assert log[0].source == "agent"

    async def test_mark_triage_to_unseen_deletes_row(self, svc, session_factory, sample_papers):
        """Marking as 'unseen' deletes the TriageState row (absence-means-unseen)."""
        await svc.mark_triage("2301.00001", "shortlisted")
        result = await svc.mark_triage("2301.00001", "unseen")
        assert result.state == "unseen"

        # Verify no row in triage_states
        async with session_factory() as session:
            db_result = await session.execute(
                select(TriageState).where(TriageState.paper_id == "2301.00001")
            )
            assert db_result.scalar_one_or_none() is None

        # But the log should still record the transition
        log = await svc.get_triage_log("2301.00001")
        assert len(log) == 2
        assert log[1].new_state == "unseen"

    async def test_mark_triage_invalid_state_raises(self, svc, sample_papers):
        with pytest.raises(ValueError, match="Invalid"):
            await svc.mark_triage("2301.00001", "invalid-state")


# ---------------------------------------------------------------------------
# Get triage state tests
# ---------------------------------------------------------------------------


class TestGetTriageState:
    async def test_untriaged_returns_unseen(self, svc, sample_papers):
        state = await svc.get_triage_state("2301.00001")
        assert state == "unseen"

    async def test_triaged_returns_current_state(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted")
        state = await svc.get_triage_state("2301.00001")
        assert state == "shortlisted"


# ---------------------------------------------------------------------------
# List by state tests
# ---------------------------------------------------------------------------


class TestListByState:
    async def test_list_by_state_shortlisted(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted")
        await svc.mark_triage("2301.00002", "shortlisted")
        await svc.mark_triage("2301.00003", "dismissed")
        result = await svc.list_by_state("shortlisted")
        ids = {item.paper_id for item in result.items}
        assert ids == {"2301.00001", "2301.00002"}

    async def test_list_by_state_unseen(self, svc, sample_papers):
        """Unseen = papers with no triage_states row."""
        await svc.mark_triage("2301.00001", "shortlisted")
        await svc.mark_triage("2301.00002", "dismissed")
        result = await svc.list_by_state("unseen")
        ids = {item.paper_id for item in result.items}
        assert ids == {"2301.00003", "2301.00004", "2301.00005"}


# ---------------------------------------------------------------------------
# Batch triage (ID-based) tests
# ---------------------------------------------------------------------------


class TestBatchTriage:
    async def test_batch_triage_marks_all(self, svc, sample_papers):
        result = await svc.batch_triage(
            ["2301.00001", "2301.00002", "2301.00003"], "read"
        )
        assert result.affected_count == 3

    async def test_batch_triage_skips_already_in_target(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "read")
        result = await svc.batch_triage(
            ["2301.00001", "2301.00002"], "read"
        )
        assert result.affected_count == 1
        assert result.skipped_count == 1

    async def test_batch_triage_nonexistent_paper_in_errors(self, svc, sample_papers):
        result = await svc.batch_triage(
            ["2301.00001", "9999.99999"], "shortlisted"
        )
        assert result.affected_count == 1
        assert "9999.99999" in result.errors


# ---------------------------------------------------------------------------
# Batch triage (query-based) tests
# ---------------------------------------------------------------------------


class TestBatchTriageByQuery:
    async def test_dry_run_returns_preview(self, svc, sample_papers):
        """Dry-run should return preview without changing any state."""
        result = await svc.batch_triage_by_query(
            query_params={"category": "cs.CL"},
            new_state="shortlisted",
            dry_run=True,
        )
        # Should be a BatchTriagePreview, not BatchTriageResult
        assert hasattr(result, "matching_count")
        assert hasattr(result, "sample_ids")
        assert result.matching_count > 0

        # Verify no state was actually changed
        state = await svc.get_triage_state("2301.00001")
        assert state == "unseen"

    async def test_confirmed_execution_applies_state(self, svc, sample_papers):
        """With dry_run=False, state should actually change."""
        result = await svc.batch_triage_by_query(
            query_params={"category": "cs.CL"},
            new_state="shortlisted",
            dry_run=False,
        )
        assert hasattr(result, "affected_count")
        assert result.affected_count > 0

        # Verify state was actually changed
        state = await svc.get_triage_state("2301.00001")
        assert state == "shortlisted"

    async def test_query_based_skips_already_in_target(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted")
        result = await svc.batch_triage_by_query(
            query_params={"category": "cs.CL"},
            new_state="shortlisted",
            dry_run=False,
        )
        assert result.skipped_count >= 1


# ---------------------------------------------------------------------------
# Audit log tests
# ---------------------------------------------------------------------------


class TestSeenTriageState:
    """PREMCP-02: Tests for 'seen' triage state."""

    async def test_mark_seen_creates_row(self, svc, session_factory, sample_papers):
        """mark_triage(arxiv_id, 'seen') creates a TriageState row (not absence)."""
        result = await svc.mark_triage("2301.00001", "seen")
        assert result.state == "seen"

        # Verify row exists in DB
        async with session_factory() as session:
            db_result = await session.execute(
                select(TriageState).where(TriageState.paper_id == "2301.00001")
            )
            ts = db_result.scalar_one_or_none()
            assert ts is not None
            assert ts.state == "seen"

    async def test_mark_seen_then_get_returns_seen(self, svc, sample_papers):
        """mark_triage followed by get_triage_state returns 'seen'."""
        await svc.mark_triage("2301.00001", "seen")
        state = await svc.get_triage_state("2301.00001")
        assert state == "seen"

    async def test_seen_distinct_from_unseen(self, svc, sample_papers):
        """'seen' is distinct from 'unseen' (absence of row)."""
        # Before marking: unseen
        state_before = await svc.get_triage_state("2301.00001")
        assert state_before == "unseen"

        # After marking as seen: seen
        await svc.mark_triage("2301.00001", "seen")
        state_after = await svc.get_triage_state("2301.00001")
        assert state_after == "seen"
        assert state_after != "unseen"

    async def test_seen_in_valid_states(self, svc):
        """'seen' is in TriageService.VALID_STATES."""
        assert "seen" in TriageService.VALID_STATES

    async def test_seen_to_shortlisted_transition(self, svc, sample_papers):
        """Transitioning from 'seen' to 'shortlisted' works and logs transition."""
        await svc.mark_triage("2301.00001", "seen")
        result = await svc.mark_triage("2301.00001", "shortlisted")
        assert result.state == "shortlisted"

        # Check audit log
        log = await svc.get_triage_log("2301.00001")
        assert len(log) == 2
        assert log[0].old_state == "unseen"
        assert log[0].new_state == "seen"
        assert log[1].old_state == "seen"
        assert log[1].new_state == "shortlisted"

    async def test_unseen_to_seen_creates_row(self, svc, session_factory, sample_papers):
        """Transitioning from 'unseen' (no row) to 'seen' creates a row."""
        # Verify no row exists
        async with session_factory() as session:
            db_result = await session.execute(
                select(TriageState).where(TriageState.paper_id == "2301.00001")
            )
            assert db_result.scalar_one_or_none() is None

        # Mark as seen
        result = await svc.mark_triage("2301.00001", "seen")
        assert result.state == "seen"

        # Verify row now exists
        async with session_factory() as session:
            db_result = await session.execute(
                select(TriageState).where(TriageState.paper_id == "2301.00001")
            )
            ts = db_result.scalar_one_or_none()
            assert ts is not None
            assert ts.state == "seen"


class TestGetTriageLog:
    async def test_log_returns_chronological(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted")
        await svc.mark_triage("2301.00001", "read")
        await svc.mark_triage("2301.00001", "cite-later")
        log = await svc.get_triage_log("2301.00001")
        assert len(log) == 3
        assert log[0].new_state == "shortlisted"
        assert log[1].new_state == "read"
        assert log[2].new_state == "cite-later"

    async def test_log_entries_have_all_fields(self, svc, sample_papers):
        await svc.mark_triage("2301.00001", "shortlisted", source="agent", reason="good paper")
        log = await svc.get_triage_log("2301.00001")
        entry = log[0]
        assert entry.paper_id == "2301.00001"
        assert entry.old_state == "unseen"
        assert entry.new_state == "shortlisted"
        assert entry.timestamp is not None
        assert entry.source == "agent"
        assert entry.reason == "good paper"
