"""Test fixtures for content module tests.

Provides async session factory and sample data factories for content
variant and rights testing. Follows the enrichment conftest pattern.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from tests.conftest import (
    TSVECTOR_CREATE_TRIGGER_SQL,
    TSVECTOR_DROP_TRIGGER_SQL,
    TSVECTOR_FUNCTION_SQL,
    sample_paper_data,
)
from arxiv_mcp.db.models import Base


@pytest.fixture
async def content_session_factory(test_engine):
    """Create tables, yield async_sessionmaker, then drop tables.

    Same pattern as the enrichment conftest: yields the factory
    instead of a single session, allowing tests to create their
    own session scopes for content operations.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_FUNCTION_SQL))
        await conn.execute(text(TSVECTOR_DROP_TRIGGER_SQL))
        await conn.execute(text(TSVECTOR_CREATE_TRIGGER_SQL))
        # Truncate to ensure clean state (avoids stale data from prior fixtures
        # while preserving table structure for asyncpg prepared statement cache)
        await conn.execute(text("TRUNCATE TABLE content_variants CASCADE"))
        await conn.execute(text("TRUNCATE TABLE papers CASCADE"))

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


def sample_content_variant_data(**overrides) -> dict:
    """Factory function returning a dict with default ContentVariant column values.

    Pass keyword arguments to override any field.
    """
    defaults = {
        "arxiv_id": "2301.00001",
        "variant_type": "abstract",
        "content": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks.",
        "content_hash": "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2",
        "source_url": None,
        "backend": None,
        "backend_version": None,
        "extraction_method": "metadata_copy",
        "license_uri": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "quality_warnings": None,
        "fetched_at": None,
        "converted_at": datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


def sample_paper_with_license(
    license_uri: str = "http://creativecommons.org/licenses/by/4.0/",
    arxiv_id: str = "2301.00001",
    **overrides,
) -> dict:
    """Factory returning Paper sample data with a specific license_uri.

    Useful for rights testing where the license matters.
    """
    return sample_paper_data(
        arxiv_id=arxiv_id,
        license_uri=license_uri,
        **overrides,
    )
