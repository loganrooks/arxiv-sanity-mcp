"""Test fixtures for enrichment module tests.

Provides JSON fixture loading, async session factory, and sample data
for enrichment adapter and model tests.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.conftest import (
    TSVECTOR_CREATE_TRIGGER_SQL,
    TSVECTOR_DROP_TRIGGER_SQL,
    TSVECTOR_FUNCTION_SQL,
)
from arxiv_mcp.db.models import Base

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def openalex_work_fixture() -> dict:
    """Load the 'Attention Is All You Need' OpenAlex Work response."""
    return json.loads((FIXTURES_DIR / "openalex_work_attention.json").read_text())


@pytest.fixture
def openalex_not_found_fixture() -> dict:
    """Load the empty results (not found) OpenAlex response."""
    return json.loads((FIXTURES_DIR / "openalex_work_not_found.json").read_text())


@pytest.fixture
def openalex_batch_fixture() -> dict:
    """Load the batch (multi-work) OpenAlex response."""
    return json.loads((FIXTURES_DIR / "openalex_batch_response.json").read_text())


@pytest.fixture
async def enrichment_session_factory(test_engine):
    """Create tables, yield async_sessionmaker, then drop tables.

    Same pattern as the root conftest test_session fixture but yields
    the factory instead of a single session, allowing tests to create
    their own session scopes.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_FUNCTION_SQL))
        await conn.execute(text(TSVECTOR_DROP_TRIGGER_SQL))
        await conn.execute(text(TSVECTOR_CREATE_TRIGGER_SQL))

    factory = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    yield factory

    async with test_engine.begin() as conn:
        await conn.execute(text("DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers"))
        await conn.execute(text("DROP FUNCTION IF EXISTS papers_search_vector_update()"))
        await conn.run_sync(Base.metadata.drop_all)
