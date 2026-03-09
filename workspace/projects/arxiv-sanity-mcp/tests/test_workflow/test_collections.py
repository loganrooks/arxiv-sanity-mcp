"""Integration tests for CollectionService.

Tests CRUD, membership (add/remove/bulk), merge, archive/unarchive,
reverse lookup, and show_collection with triage state display.
All tests run against PostgreSQL via async session_factory fixtures.
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.db.models import Collection, CollectionPaper, Paper, TriageState
from arxiv_mcp.config import get_settings
from arxiv_mcp.workflow.collections import CollectionService


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def session_factory(test_engine):
    """Provide async_sessionmaker for service DI (mirrors SearchService pattern)."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@pytest.fixture
async def svc(session_factory):
    """CollectionService instance with settings."""
    settings = get_settings()
    return CollectionService(session_factory, settings)


@pytest.fixture
async def populated_collection(svc, sample_papers):
    """Create a collection with 3 papers already added."""
    coll = await svc.create_collection("My Reading List")
    ids = [p.arxiv_id for p in sample_papers[:3]]
    await svc.add_papers(coll.slug, ids)
    return coll


# ---------------------------------------------------------------------------
# CRUD tests
# ---------------------------------------------------------------------------


class TestCreateCollection:
    async def test_create_collection_basic(self, svc, sample_papers):
        result = await svc.create_collection("My Reading List")
        assert result.slug == "my-reading-list"
        assert result.name == "My Reading List"
        assert result.paper_count == 0
        assert result.is_archived is False

    async def test_create_collection_duplicate_slug_raises(self, svc, sample_papers):
        await svc.create_collection("My Reading List")
        with pytest.raises(ValueError, match="slug"):
            await svc.create_collection("My Reading List")


class TestListCollections:
    async def test_list_collections_with_paper_count(self, svc, sample_papers):
        coll = await svc.create_collection("Test Collection")
        await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id])
        result = await svc.list_collections()
        assert len(result) == 1
        assert result[0].paper_count == 1

    async def test_list_collections_excludes_archived(self, svc, sample_papers):
        await svc.create_collection("Active")
        coll2 = await svc.create_collection("Archived")
        await svc.archive_collection(coll2.slug)
        result = await svc.list_collections()
        assert len(result) == 1
        assert result[0].name == "Active"

    async def test_list_collections_includes_archived(self, svc, sample_papers):
        await svc.create_collection("Active")
        coll2 = await svc.create_collection("Archived")
        await svc.archive_collection(coll2.slug)
        result = await svc.list_collections(include_archived=True)
        assert len(result) == 2


class TestDeleteCollection:
    async def test_delete_collection_removes_memberships(self, svc, sample_papers):
        coll = await svc.create_collection("To Delete")
        await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id])
        await svc.delete_collection(coll.slug)
        result = await svc.list_collections()
        assert len(result) == 0


class TestRenameCollection:
    async def test_rename_collection_updates_slug(self, svc, sample_papers):
        coll = await svc.create_collection("Old Name")
        result = await svc.rename_collection(coll.slug, "New Name")
        assert result.slug == "new-name"
        assert result.name == "New Name"
        assert result.updated_at > coll.updated_at

    async def test_rename_to_existing_slug_raises(self, svc, sample_papers):
        await svc.create_collection("First")
        coll2 = await svc.create_collection("Second")
        with pytest.raises(ValueError, match="slug"):
            await svc.rename_collection(coll2.slug, "First")


# ---------------------------------------------------------------------------
# Membership tests
# ---------------------------------------------------------------------------


class TestAddPapers:
    async def test_add_papers_with_source(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        added = await svc.add_papers(
            coll.slug, [sample_papers[0].arxiv_id, sample_papers[1].arxiv_id], source="agent"
        )
        assert added == 2

    async def test_add_papers_idempotent(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id])
        added = await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id])
        assert added == 0


class TestRemovePapers:
    async def test_remove_papers(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id, sample_papers[1].arxiv_id])
        removed = await svc.remove_papers(coll.slug, [sample_papers[0].arxiv_id])
        assert removed == 1


# ---------------------------------------------------------------------------
# Show collection with triage state
# ---------------------------------------------------------------------------


class TestShowCollection:
    async def test_show_collection_returns_papers(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        await svc.add_papers(coll.slug, [sample_papers[0].arxiv_id])
        result = await svc.show_collection(coll.slug)
        assert len(result.items) == 1

    async def test_show_collection_includes_triage_state(self, svc, session_factory, sample_papers):
        """Papers with triage state should show that state; others show 'unseen'."""
        coll = await svc.create_collection("Test")
        await svc.add_papers(
            coll.slug, [sample_papers[0].arxiv_id, sample_papers[1].arxiv_id]
        )
        # Set triage state on one paper
        async with session_factory() as session:
            ts = TriageState(
                paper_id=sample_papers[0].arxiv_id,
                state="shortlisted",
                updated_at=datetime.now(timezone.utc),
            )
            session.add(ts)
            await session.commit()
        result = await svc.show_collection(coll.slug)
        states = {item.arxiv_id: item.triage_state for item in result.items}
        assert states[sample_papers[0].arxiv_id] == "shortlisted"
        assert states[sample_papers[1].arxiv_id] == "unseen"

    async def test_show_collection_sort_by_added(self, populated_collection, svc):
        result = await svc.show_collection(populated_collection.slug, sort_by="added")
        assert len(result.items) == 3

    async def test_show_collection_sort_by_paper_date(self, populated_collection, svc):
        result = await svc.show_collection(populated_collection.slug, sort_by="paper_date")
        assert len(result.items) == 3

    async def test_show_collection_sort_by_title(self, populated_collection, svc):
        result = await svc.show_collection(populated_collection.slug, sort_by="title")
        assert len(result.items) == 3


# ---------------------------------------------------------------------------
# Merge tests
# ---------------------------------------------------------------------------


class TestMergeCollections:
    async def test_merge_moves_papers_deletes_source(self, svc, sample_papers):
        source = await svc.create_collection("Source")
        target = await svc.create_collection("Target")
        await svc.add_papers(source.slug, [sample_papers[0].arxiv_id])
        await svc.add_papers(target.slug, [sample_papers[1].arxiv_id])
        merged = await svc.merge_collections(source.slug, target.slug)
        assert merged.paper_count == 2
        # Source should be deleted
        result = await svc.list_collections()
        slugs = [c.slug for c in result]
        assert "source" in slugs or "target" in slugs
        assert "source" not in slugs

    async def test_merge_skips_duplicates(self, svc, sample_papers):
        source = await svc.create_collection("Source")
        target = await svc.create_collection("Target")
        # Same paper in both
        await svc.add_papers(source.slug, [sample_papers[0].arxiv_id])
        await svc.add_papers(target.slug, [sample_papers[0].arxiv_id])
        merged = await svc.merge_collections(source.slug, target.slug)
        assert merged.paper_count == 1


# ---------------------------------------------------------------------------
# Archive tests
# ---------------------------------------------------------------------------


class TestArchiveCollection:
    async def test_archive_sets_flag(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        result = await svc.archive_collection(coll.slug)
        assert result.is_archived is True

    async def test_unarchive_clears_flag(self, svc, sample_papers):
        coll = await svc.create_collection("Test")
        await svc.archive_collection(coll.slug)
        result = await svc.unarchive_collection(coll.slug)
        assert result.is_archived is False


# ---------------------------------------------------------------------------
# Reverse lookup tests
# ---------------------------------------------------------------------------


class TestGetPaperCollections:
    async def test_reverse_lookup_returns_collections(self, svc, sample_papers):
        coll1 = await svc.create_collection("List A")
        coll2 = await svc.create_collection("List B")
        await svc.add_papers(coll1.slug, [sample_papers[0].arxiv_id])
        await svc.add_papers(coll2.slug, [sample_papers[0].arxiv_id])
        result = await svc.get_paper_collections(sample_papers[0].arxiv_id)
        slugs = {c.slug for c in result}
        assert slugs == {"list-a", "list-b"}


# ---------------------------------------------------------------------------
# Bulk operations tests
# ---------------------------------------------------------------------------


class TestBulkOperations:
    async def test_bulk_add_papers(self, svc, sample_papers):
        coll = await svc.create_collection("Bulk Test")
        ids = [p.arxiv_id for p in sample_papers]
        added = await svc.add_papers(coll.slug, ids)
        assert added == 5

    async def test_bulk_remove_papers(self, svc, sample_papers):
        coll = await svc.create_collection("Bulk Test")
        ids = [p.arxiv_id for p in sample_papers]
        await svc.add_papers(coll.slug, ids)
        removed = await svc.remove_papers(coll.slug, ids[:3])
        assert removed == 3
