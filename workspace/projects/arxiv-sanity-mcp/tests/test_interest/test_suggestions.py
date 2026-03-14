"""Integration tests for SuggestionService.

Tests the suggestion lifecycle: generate candidates from workflow
activity, add as pending signals, confirm, dismiss, and bulk confirm.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import (
    InterestProfile,
    InterestSignal,
    Paper,
    SavedQuery,
    TriageState,
)
from arxiv_mcp.interest.profiles import ProfileService
from arxiv_mcp.interest.suggestions import SuggestionService

from tests.conftest import sample_paper_data
from .conftest import (
    sample_profile_data,
    sample_saved_query_data,
)

pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------
# Helper: create a SuggestionService from test fixtures
# ---------------------------------------------------------------


def _make_services(session_factory):
    settings = get_settings()
    profile_svc = ProfileService(session_factory=session_factory, settings=settings)
    suggestion_svc = SuggestionService(
        session_factory=session_factory,
        settings=settings,
        profile_service=profile_svc,
    )
    return profile_svc, suggestion_svc


# ---------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------


@pytest.fixture
async def profile_with_triage(test_session, session_factory):
    """Create a profile + papers with triage states for suggestion tests.

    Creates:
    - 1 profile ("research-ai")
    - 5 papers by "Alice Author" with triage state "shortlisted"
    - 3 papers by "Bob Builder" with triage state "shortlisted"
    - 2 papers by "Charlie Chaplin" with triage state "cite-later"
    - 1 paper by "Dave Developer" with no triage (should not be suggested)
    - 2 saved queries: one with run_count=5, one with run_count=1
    """
    now = datetime.now(timezone.utc)

    # Create profile
    profile = InterestProfile(**sample_profile_data(
        slug="research-ai", name="Research AI",
    ))
    test_session.add(profile)
    await test_session.flush()

    # Papers by "Alice Author" -- 5 shortlisted (should trigger author suggestion, threshold=3)
    for i in range(1, 6):
        paper = Paper(**sample_paper_data(
            arxiv_id=f"2301.1000{i}",
            title=f"Alice Paper {i}",
            authors_text="Alice Author, Eve Extra",
            categories="cs.AI cs.LG",
            primary_category="cs.AI",
            category_list=["cs.AI", "cs.LG"],
        ))
        test_session.add(paper)
        triage = TriageState(
            paper_id=f"2301.1000{i}", state="shortlisted", updated_at=now,
        )
        test_session.add(triage)

    # Papers by "Bob Builder" -- 3 shortlisted (exactly at threshold)
    for i in range(1, 4):
        paper = Paper(**sample_paper_data(
            arxiv_id=f"2301.2000{i}",
            title=f"Bob Paper {i}",
            authors_text="Bob Builder",
            categories="cs.CV",
            primary_category="cs.CV",
            category_list=["cs.CV"],
        ))
        test_session.add(paper)
        triage = TriageState(
            paper_id=f"2301.2000{i}", state="shortlisted", updated_at=now,
        )
        test_session.add(triage)

    # Papers by "Charlie Chaplin" -- 2 cite-later
    for i in range(1, 3):
        paper = Paper(**sample_paper_data(
            arxiv_id=f"2301.3000{i}",
            title=f"Charlie Paper {i}",
            authors_text="Charlie Chaplin",
            categories="cs.AI",
            primary_category="cs.AI",
            category_list=["cs.AI"],
        ))
        test_session.add(paper)
        triage = TriageState(
            paper_id=f"2301.3000{i}", state="cite-later", updated_at=now,
        )
        test_session.add(triage)

    # Paper by "Dave Developer" -- no triage
    paper = Paper(**sample_paper_data(
        arxiv_id="2301.40001",
        title="Dave Paper 1",
        authors_text="Dave Developer",
        categories="cs.SE",
        primary_category="cs.SE",
        category_list=["cs.SE"],
    ))
    test_session.add(paper)

    # Saved queries: one with high run_count, one with low
    sq_high = SavedQuery(**sample_saved_query_data(
        slug="freq-query", name="Frequent Query", run_count=5,
    ))
    test_session.add(sq_high)

    sq_low = SavedQuery(**sample_saved_query_data(
        slug="rare-query", name="Rare Query", run_count=1,
    ))
    test_session.add(sq_low)

    await test_session.commit()
    return profile


# ---------------------------------------------------------------
# Tests: Seed paper suggestions
# ---------------------------------------------------------------


class TestSuggestSeedPapers:
    """Shortlisted and cite-later papers appear as seed_paper candidates."""

    async def test_shortlisted_papers_as_candidates(
        self, profile_with_triage, session_factory
    ):
        """Papers with triage state shortlisted should appear as seed_paper suggestions."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        seed_candidates = [c for c in candidates if c.signal_type == "seed_paper"]
        seed_values = {c.signal_value for c in seed_candidates}

        # All 5 shortlisted Alice papers + 3 shortlisted Bob papers + 2 cite-later Charlie
        assert "2301.10001" in seed_values
        assert "2301.20001" in seed_values
        assert "2301.30001" in seed_values

    async def test_cite_later_papers_as_candidates(
        self, profile_with_triage, session_factory
    ):
        """Papers triaged as cite-later should also appear as seed_paper suggestions."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        seed_candidates = [c for c in candidates if c.signal_type == "seed_paper"]
        seed_values = {c.signal_value for c in seed_candidates}

        assert "2301.30001" in seed_values
        assert "2301.30002" in seed_values

    async def test_existing_seeds_excluded(
        self, profile_with_triage, session_factory, test_session
    ):
        """Papers already in profile as seed_paper signals should be excluded."""
        # Add one paper as existing seed
        signal = InterestSignal(
            profile_id=profile_with_triage.id,
            signal_type="seed_paper",
            signal_value="2301.10001",
            status="active",
            source="manual",
            added_at=datetime.now(timezone.utc),
        )
        test_session.add(signal)
        await test_session.commit()

        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        seed_values = {c.signal_value for c in candidates if c.signal_type == "seed_paper"}
        assert "2301.10001" not in seed_values

    async def test_seed_reason_includes_triage_state(
        self, profile_with_triage, session_factory
    ):
        """Seed paper suggestions should include reason with triage state."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        shortlisted = [
            c for c in candidates
            if c.signal_type == "seed_paper" and c.signal_value == "2301.10001"
        ]
        assert len(shortlisted) == 1
        assert "shortlisted" in shortlisted[0].reason.lower()


# ---------------------------------------------------------------
# Tests: Author suggestions
# ---------------------------------------------------------------


class TestSuggestAuthors:
    """Authors appearing in 3+ shortlisted/cite-later papers are suggested."""

    async def test_author_with_threshold_papers(
        self, profile_with_triage, session_factory
    ):
        """Author with 3+ shortlisted papers should be suggested as followed_author."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        author_candidates = [c for c in candidates if c.signal_type == "followed_author"]
        author_values = {c.signal_value for c in author_candidates}

        # alice author has 5 shortlisted papers
        assert "alice author" in author_values
        # bob builder has 3 shortlisted papers (at threshold)
        assert "bob builder" in author_values

    async def test_author_below_threshold_excluded(
        self, profile_with_triage, session_factory
    ):
        """Authors with fewer than 3 shortlisted/cite-later papers should not be suggested."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        author_values = {
            c.signal_value for c in candidates if c.signal_type == "followed_author"
        }

        # Charlie Chaplin only has 2 cite-later papers (below threshold)
        assert "charlie chaplin" not in author_values
        # Dave Developer has no triage
        assert "dave developer" not in author_values

    async def test_author_reason_includes_count(
        self, profile_with_triage, session_factory
    ):
        """Author suggestion reason should include the count of papers."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        alice = [
            c for c in candidates
            if c.signal_type == "followed_author" and c.signal_value == "alice author"
        ]
        assert len(alice) == 1
        assert "5" in alice[0].reason  # appears in 5 shortlisted papers


# ---------------------------------------------------------------
# Tests: Saved query suggestions
# ---------------------------------------------------------------


class TestSuggestQueries:
    """Saved queries with run_count >= 3 are suggested."""

    async def test_high_run_count_suggested(
        self, profile_with_triage, session_factory
    ):
        """Saved query with run_count >= 3 should be suggested."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        query_candidates = [c for c in candidates if c.signal_type == "saved_query"]
        query_values = {c.signal_value for c in query_candidates}

        assert "freq-query" in query_values

    async def test_low_run_count_excluded(
        self, profile_with_triage, session_factory
    ):
        """Saved query with run_count < 3 should not be suggested."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        query_values = {
            c.signal_value for c in candidates if c.signal_type == "saved_query"
        }

        assert "rare-query" not in query_values

    async def test_query_reason_includes_run_count(
        self, profile_with_triage, session_factory
    ):
        """Query suggestion reason should mention run count."""
        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("research-ai")

        freq = [
            c for c in candidates
            if c.signal_type == "saved_query" and c.signal_value == "freq-query"
        ]
        assert len(freq) == 1
        assert "5" in freq[0].reason


# ---------------------------------------------------------------
# Tests: Confirm and dismiss lifecycle
# ---------------------------------------------------------------


class TestConfirmDismiss:
    """Confirm changes pending to active; dismiss changes to dismissed."""

    async def test_confirm_suggestion(
        self, profile_with_triage, session_factory
    ):
        """Confirming a suggestion should change status from pending to active."""
        profile_svc, svc = _make_services(session_factory)

        candidates = await svc.generate_suggestions("research-ai")
        assert len(candidates) > 0

        # Add suggestions as pending signals
        await svc.add_suggestions_to_profile("research-ai", candidates[:1])

        # Confirm the first one
        c = candidates[0]
        result = await svc.confirm_suggestion(
            "research-ai", c.signal_type, c.signal_value
        )
        assert result.status == "active"

    async def test_dismiss_suggestion(
        self, profile_with_triage, session_factory
    ):
        """Dismissing a suggestion should change status to dismissed."""
        _, svc = _make_services(session_factory)

        candidates = await svc.generate_suggestions("research-ai")
        await svc.add_suggestions_to_profile("research-ai", candidates[:1])

        c = candidates[0]
        await svc.dismiss_suggestion(
            "research-ai", c.signal_type, c.signal_value
        )

        # Check profile to verify dismissed
        profile_svc = ProfileService(
            session_factory=session_factory, settings=get_settings()
        )
        detail = await profile_svc.get_profile("research-ai")
        dismissed = [
            s for s in detail.signals
            if s.status == "dismissed" and s.signal_value == c.signal_value
        ]
        assert len(dismissed) == 1


# ---------------------------------------------------------------
# Tests: Bulk confirm
# ---------------------------------------------------------------


class TestBulkConfirm:
    """Bulk confirm multiple suggestions at once."""

    async def test_confirm_multiple(
        self, profile_with_triage, session_factory
    ):
        """Bulk confirm should confirm multiple pending suggestions."""
        _, svc = _make_services(session_factory)

        candidates = await svc.generate_suggestions("research-ai")
        # Add 3 suggestions as pending
        await svc.add_suggestions_to_profile("research-ai", candidates[:3])

        items = [(c.signal_type, c.signal_value) for c in candidates[:3]]
        count = await svc.confirm_suggestions_bulk("research-ai", items)
        assert count == 3


# ---------------------------------------------------------------
# Tests: No duplicate suggestions
# ---------------------------------------------------------------


class TestNoDuplicateSuggestions:
    """Dismissed suggestions should not be re-suggested."""

    async def test_dismissed_excluded(
        self, profile_with_triage, session_factory, test_session
    ):
        """After dismissing a suggestion, regenerating should not include it."""
        _, svc = _make_services(session_factory)

        candidates = await svc.generate_suggestions("research-ai")
        # Add first candidate as pending, then dismiss
        await svc.add_suggestions_to_profile("research-ai", candidates[:1])
        c = candidates[0]
        await svc.dismiss_suggestion("research-ai", c.signal_type, c.signal_value)

        # Regenerate -- dismissed should not reappear
        new_candidates = await svc.generate_suggestions("research-ai")
        new_values = {(nc.signal_type, nc.signal_value) for nc in new_candidates}
        assert (c.signal_type, c.signal_value) not in new_values


# ---------------------------------------------------------------
# Tests: Empty workflow
# ---------------------------------------------------------------


class TestEmptyWorkflow:
    """No triage/queries returns empty suggestions."""

    async def test_no_activity_returns_empty(
        self, test_session, session_factory
    ):
        """Profile with no workflow activity should produce no suggestions."""
        # Create an isolated profile with no papers/queries
        profile = InterestProfile(**sample_profile_data(
            slug="empty-profile", name="Empty Profile",
        ))
        test_session.add(profile)
        await test_session.commit()

        _, svc = _make_services(session_factory)
        candidates = await svc.generate_suggestions("empty-profile")
        assert candidates == []
