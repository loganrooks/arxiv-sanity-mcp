"""Tests for workflow ORM models and Pydantic schemas.

Tests cover: Collection, CollectionPaper, TriageState, TriageLog,
SavedQuery ORM models; Pydantic schemas for API serialization; and
the slugify utility function.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from arxiv_mcp.db.models import (
    Collection,
    CollectionPaper,
    SavedQuery,
    TriageLog,
    TriageState,
)
from arxiv_mcp.models.workflow import (
    CollectionDetail,
    SavedQueryResponse,
    TriageStateResponse,
    WatchSummary,
)
from arxiv_mcp.workflow.util import slugify

from .conftest import (
    sample_collection_data,
    sample_saved_query_data,
    sample_triage_data,
)


# --- Slugify tests ---


class TestSlugify:
    """Tests for the slugify utility function."""

    def test_slugify_basic(self):
        assert slugify("My Reading List") == "my-reading-list"

    def test_slugify_strips_symbols(self):
        assert slugify("  Spaces & Symbols!  ") == "spaces-symbols"

    def test_slugify_consecutive_separators(self):
        assert slugify("hello---world") == "hello-world"

    def test_slugify_numbers(self):
        assert slugify("Paper 42 Notes") == "paper-42-notes"

    def test_slugify_empty_after_strip(self):
        assert slugify("!!!") == ""


# --- Collection ORM tests ---


class TestCollectionModel:
    """Tests for the Collection ORM model."""

    @pytest.mark.asyncio
    async def test_create_collection(self, test_session, sample_papers):
        """Collection creates row with slug, name, is_archived=False, created_at, updated_at."""
        data = sample_collection_data()
        collection = Collection(**data)
        test_session.add(collection)
        await test_session.commit()

        result = await test_session.execute(
            select(Collection).where(Collection.slug == "my-reading-list")
        )
        fetched = result.scalar_one()

        assert fetched.slug == "my-reading-list"
        assert fetched.name == "My Reading List"
        assert fetched.is_archived is False
        assert fetched.created_at is not None
        assert fetched.updated_at is not None

    @pytest.mark.asyncio
    async def test_collection_slug_unique(self, test_session, sample_papers):
        """Collection slug must be unique."""
        data1 = sample_collection_data()
        data2 = sample_collection_data(name="Duplicate Slug")
        test_session.add(Collection(**data1))
        await test_session.commit()

        test_session.add(Collection(**data2))
        with pytest.raises(IntegrityError):
            await test_session.commit()


# --- CollectionPaper association tests ---


class TestCollectionPaperModel:
    """Tests for the CollectionPaper association object."""

    @pytest.mark.asyncio
    async def test_collection_paper_association(self, test_session, sample_papers):
        """CollectionPaper stores collection_id, paper_id, source, added_at."""
        collection = Collection(**sample_collection_data())
        test_session.add(collection)
        await test_session.commit()

        assoc = CollectionPaper(
            collection_id=collection.id,
            paper_id="2301.00001",
            source="manual",
            added_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        )
        test_session.add(assoc)
        await test_session.commit()

        result = await test_session.execute(
            select(CollectionPaper).where(
                CollectionPaper.collection_id == collection.id,
                CollectionPaper.paper_id == "2301.00001",
            )
        )
        fetched = result.scalar_one()

        assert fetched.collection_id == collection.id
        assert fetched.paper_id == "2301.00001"
        assert fetched.source == "manual"
        assert fetched.added_at is not None

    @pytest.mark.asyncio
    async def test_collection_paper_sources(self, test_session, sample_papers):
        """CollectionPaper accepts different source values."""
        collection = Collection(**sample_collection_data())
        test_session.add(collection)
        await test_session.commit()

        for source, paper_id in [
            ("manual", "2301.00001"),
            ("saved_query", "2301.00002"),
            ("agent", "2301.00003"),
        ]:
            assoc = CollectionPaper(
                collection_id=collection.id,
                paper_id=paper_id,
                source=source,
                added_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            )
            test_session.add(assoc)

        await test_session.commit()

        result = await test_session.execute(
            select(CollectionPaper).where(
                CollectionPaper.collection_id == collection.id
            )
        )
        assocs = result.scalars().all()
        sources = {a.source for a in assocs}
        assert sources == {"manual", "saved_query", "agent"}


# --- TriageState ORM tests ---


class TestTriageStateModel:
    """Tests for the TriageState ORM model."""

    @pytest.mark.asyncio
    async def test_triage_state_valid_values(self, test_session, sample_papers):
        """TriageState stores paper_id and state with valid values."""
        valid_states = ["shortlisted", "dismissed", "read", "cite-later", "archived"]
        for i, state in enumerate(valid_states, 1):
            ts = TriageState(
                paper_id=f"2301.0000{i}",
                state=state,
                updated_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            )
            test_session.add(ts)

        await test_session.commit()

        result = await test_session.execute(select(TriageState))
        states = result.scalars().all()
        assert len(states) == 5
        assert {s.state for s in states} == set(valid_states)

    @pytest.mark.asyncio
    async def test_triage_state_rejects_invalid(self, test_session, sample_papers):
        """TriageState rejects invalid state values via CHECK constraint."""
        ts = TriageState(
            paper_id="2301.00001",
            state="invalid_state",
            updated_at=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        )
        test_session.add(ts)
        with pytest.raises(IntegrityError):
            await test_session.commit()


# --- TriageLog ORM tests ---


class TestTriageLogModel:
    """Tests for the TriageLog ORM model."""

    @pytest.mark.asyncio
    async def test_triage_log_entry(self, test_session, sample_papers):
        """TriageLog stores paper_id, old_state, new_state, timestamp, source, reason."""
        log = TriageLog(
            paper_id="2301.00001",
            old_state="unseen",
            new_state="shortlisted",
            timestamp=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            source="manual",
            reason="Interesting method section",
        )
        test_session.add(log)
        await test_session.commit()

        result = await test_session.execute(
            select(TriageLog).where(TriageLog.paper_id == "2301.00001")
        )
        fetched = result.scalar_one()

        assert fetched.paper_id == "2301.00001"
        assert fetched.old_state == "unseen"
        assert fetched.new_state == "shortlisted"
        assert fetched.timestamp is not None
        assert fetched.source == "manual"
        assert fetched.reason == "Interesting method section"

    @pytest.mark.asyncio
    async def test_triage_log_optional_reason(self, test_session, sample_papers):
        """TriageLog accepts None for reason field."""
        log = TriageLog(
            paper_id="2301.00001",
            old_state="unseen",
            new_state="dismissed",
            timestamp=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
            source="batch",
            reason=None,
        )
        test_session.add(log)
        await test_session.commit()

        result = await test_session.execute(
            select(TriageLog).where(TriageLog.paper_id == "2301.00001")
        )
        fetched = result.scalar_one()
        assert fetched.reason is None


# --- SavedQuery ORM tests ---


class TestSavedQueryModel:
    """Tests for the SavedQuery ORM model."""

    @pytest.mark.asyncio
    async def test_saved_query_all_fields(self, test_session):
        """SavedQuery stores all fields including watch extension columns."""
        data = sample_saved_query_data(
            is_watch=True,
            cadence_hint="daily",
            checkpoint_date=date(2026, 3, 1),
            last_checked_at=datetime(2026, 3, 8, 10, 0, 0, tzinfo=timezone.utc),
        )
        sq = SavedQuery(**data)
        test_session.add(sq)
        await test_session.commit()

        result = await test_session.execute(
            select(SavedQuery).where(SavedQuery.slug == "daily-transformers")
        )
        fetched = result.scalar_one()

        assert fetched.slug == "daily-transformers"
        assert fetched.name == "Daily Transformers"
        assert fetched.params == {"query_text": "transformer", "category": "cs.CL"}
        assert fetched.run_count == 0
        assert fetched.last_run_at is None
        assert fetched.is_watch is True
        assert fetched.cadence_hint == "daily"
        assert fetched.checkpoint_date == date(2026, 3, 1)
        assert fetched.last_checked_at is not None
        assert fetched.is_paused is False
        assert fetched.created_at is not None
        assert fetched.updated_at is not None

    @pytest.mark.asyncio
    async def test_saved_query_slug_unique(self, test_session):
        """SavedQuery slug must be unique."""
        data1 = sample_saved_query_data()
        data2 = sample_saved_query_data(name="Duplicate")
        test_session.add(SavedQuery(**data1))
        await test_session.commit()

        test_session.add(SavedQuery(**data2))
        with pytest.raises(IntegrityError):
            await test_session.commit()


# --- Pydantic schema tests ---


class TestPydanticSchemas:
    """Tests for workflow Pydantic response schemas."""

    def test_collection_detail_serialization(self):
        """CollectionDetail serializes with paper_count."""
        detail = CollectionDetail(
            slug="my-list",
            name="My List",
            paper_count=5,
            is_archived=False,
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        assert detail.slug == "my-list"
        assert detail.paper_count == 5
        assert detail.is_archived is False

    def test_triage_state_response(self):
        """TriageStateResponse includes paper_id, state, updated_at."""
        resp = TriageStateResponse(
            paper_id="2301.00001",
            state="shortlisted",
            updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        assert resp.paper_id == "2301.00001"
        assert resp.state == "shortlisted"
        assert resp.updated_at is not None

    def test_saved_query_response(self):
        """SavedQueryResponse includes slug, name, params, run_count, is_watch, cadence_hint."""
        resp = SavedQueryResponse(
            slug="daily-transformers",
            name="Daily Transformers",
            params={"query_text": "transformer"},
            run_count=5,
            last_run_at=datetime(2026, 3, 8, tzinfo=timezone.utc),
            is_watch=True,
            cadence_hint="daily",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )
        assert resp.slug == "daily-transformers"
        assert resp.run_count == 5
        assert resp.is_watch is True
        assert resp.cadence_hint == "daily"

    def test_watch_summary(self):
        """WatchSummary includes slug, last_checked_at, is_paused, checkpoint_date."""
        ws = WatchSummary(
            slug="daily-transformers",
            name="Daily Transformers",
            cadence_hint="daily",
            checkpoint_date=date(2026, 3, 1),
            last_checked_at=datetime(2026, 3, 8, tzinfo=timezone.utc),
            is_paused=False,
            pending_estimate=12,
        )
        assert ws.slug == "daily-transformers"
        assert ws.checkpoint_date == date(2026, 3, 1)
        assert ws.is_paused is False
        assert ws.pending_estimate == 12
