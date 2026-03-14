"""Shared test fixtures for workflow model tests.

Provides workflow-specific sample data factories for collections,
triage states, and saved queries. Shared fixtures (test_engine,
test_session, sample_paper_data, TSVECTOR constants) are imported
from the root conftest.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from arxiv_mcp.db.models import Paper
from tests.conftest import (
    sample_paper_data,
)


def sample_collection_data(**overrides) -> dict:
    """Factory for collection data dicts."""
    defaults = {
        "slug": "my-reading-list",
        "name": "My Reading List",
        "is_archived": False,
        "created_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        "updated_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


def sample_triage_data(**overrides) -> dict:
    """Factory for triage state data dicts."""
    defaults = {
        "paper_id": "2301.00001",
        "state": "shortlisted",
        "updated_at": datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
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
