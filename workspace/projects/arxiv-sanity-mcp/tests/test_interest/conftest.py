"""Shared test fixtures for interest model tests.

Provides interest-specific sample data factories for profiles and signals.
Shared fixtures (test_engine, test_session, sample_paper_data, TSVECTOR
constants) are imported from the root conftest.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.db.models import Paper, SavedQuery
from tests.conftest import sample_paper_data


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
