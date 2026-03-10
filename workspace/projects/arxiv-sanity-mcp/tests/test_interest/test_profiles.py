"""Integration tests for interest profiles, signals, and Pydantic schemas.

Tests cover:
- ORM model round-trips (InterestProfile, InterestSignal)
- Constraint enforcement (unique, CHECK, cascade)
- Signal validation and author normalization
- Pydantic schema conversion (from_attributes)
"""

from __future__ import annotations

from datetime import datetime, timezone

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from arxiv_mcp.db.models import InterestProfile, InterestSignal
from arxiv_mcp.interest.signals import normalize_author, validate_signal
from arxiv_mcp.models.interest import ProfileDetail, ProfileSummary, SignalInfo
from tests.test_interest.conftest import sample_profile_data, sample_signal_data


# ---------------------------------------------------------------------------
# ORM round-trip tests
# ---------------------------------------------------------------------------


class TestProfileORM:
    """InterestProfile ORM round-trip and constraint tests."""

    @pytest.mark.asyncio
    async def test_create_and_read_profile(self, test_session):
        """Create a profile and verify all fields round-trip through DB."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.commit()

        result = await test_session.execute(
            select(InterestProfile).where(InterestProfile.slug == "my-ml-profile")
        )
        loaded = result.scalar_one()
        assert loaded.name == "My ML Profile"
        assert loaded.slug == "my-ml-profile"
        assert loaded.is_archived is False
        assert loaded.negative_weight == 0.3
        assert loaded.weights is None
        assert loaded.created_at is not None
        assert loaded.updated_at is not None
        assert loaded.id is not None

    @pytest.mark.asyncio
    async def test_cascade_delete_removes_signals(self, test_session, sample_papers):
        """Deleting a profile cascades to its signals."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_value="2301.00001"),
        )
        test_session.add(signal)
        await test_session.commit()

        # Delete profile
        await test_session.delete(profile)
        await test_session.commit()

        # Signals should be gone
        result = await test_session.execute(select(InterestSignal))
        assert result.scalars().all() == []

    @pytest.mark.asyncio
    async def test_unique_slug_constraint(self, test_session):
        """Two profiles with the same slug should fail."""
        profile1 = InterestProfile(**sample_profile_data())
        profile2 = InterestProfile(**sample_profile_data(name="Different Name"))
        test_session.add(profile1)
        await test_session.commit()

        test_session.add(profile2)
        with pytest.raises(IntegrityError):
            await test_session.commit()
        await test_session.rollback()


class TestSignalORM:
    """InterestSignal ORM round-trip and constraint tests."""

    @pytest.mark.asyncio
    async def test_all_signal_types_roundtrip(self, test_session, sample_papers, sample_saved_query):
        """All 4 signal types store and retrieve correctly."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal_configs = [
            {"signal_type": "seed_paper", "signal_value": "2301.00001"},
            {"signal_type": "saved_query", "signal_value": "daily-transformers"},
            {"signal_type": "followed_author", "signal_value": "john doe"},
            {"signal_type": "negative_example", "signal_value": "2301.00002"},
        ]

        for cfg in signal_configs:
            signal = InterestSignal(
                profile_id=profile.id,
                **sample_signal_data(**cfg),
            )
            test_session.add(signal)
        await test_session.commit()

        result = await test_session.execute(
            select(InterestSignal).where(InterestSignal.profile_id == profile.id)
        )
        signals = result.scalars().all()
        assert len(signals) == 4
        types = {s.signal_type for s in signals}
        assert types == {"seed_paper", "saved_query", "followed_author", "negative_example"}

    @pytest.mark.asyncio
    async def test_unique_constraint_profile_type_value(self, test_session, sample_papers):
        """Duplicate (profile_id, signal_type, signal_value) should fail."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal1 = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_value="2301.00001"),
        )
        test_session.add(signal1)
        await test_session.commit()

        signal2 = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_value="2301.00001"),
        )
        test_session.add(signal2)
        with pytest.raises(IntegrityError):
            await test_session.commit()
        await test_session.rollback()

    @pytest.mark.asyncio
    async def test_check_constraint_rejects_invalid_signal_type(self, test_session):
        """Invalid signal_type should be rejected by CHECK constraint."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_type="invalid_type"),
        )
        test_session.add(signal)
        with pytest.raises(IntegrityError):
            await test_session.commit()
        await test_session.rollback()

    @pytest.mark.asyncio
    async def test_check_constraint_rejects_invalid_status(self, test_session):
        """Invalid status should be rejected by CHECK constraint."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(status="bogus"),
        )
        test_session.add(signal)
        with pytest.raises(IntegrityError):
            await test_session.commit()
        await test_session.rollback()

    @pytest.mark.asyncio
    async def test_cascade_from_profile_delete(self, test_session, sample_papers):
        """Signals are deleted when parent profile is deleted."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_value="2301.00001"),
        )
        test_session.add(signal)
        await test_session.commit()

        await test_session.delete(profile)
        await test_session.commit()

        result = await test_session.execute(select(InterestSignal))
        assert result.scalars().all() == []


# ---------------------------------------------------------------------------
# Signal validation tests
# ---------------------------------------------------------------------------


class TestSignalValidation:
    """Test signal validation and author normalization functions."""

    def test_normalize_author_whitespace_and_case(self):
        """normalize_author collapses whitespace and lowercases."""
        assert normalize_author("  John  DOE ") == "john doe"

    def test_normalize_author_empty(self):
        """normalize_author returns empty string for empty input."""
        assert normalize_author("") == ""

    def test_normalize_author_already_clean(self):
        """normalize_author leaves already-clean names unchanged."""
        assert normalize_author("jane smith") == "jane smith"

    def test_validate_signal_seed_paper(self):
        """validate_signal passes through seed_paper values unchanged."""
        result = validate_signal("seed_paper", "2301.00001")
        assert result == "2301.00001"

    def test_validate_signal_followed_author_normalizes(self):
        """validate_signal normalizes author names."""
        result = validate_signal("followed_author", "  John  DOE ")
        assert result == "john doe"

    def test_validate_signal_saved_query(self):
        """validate_signal passes through saved_query values."""
        result = validate_signal("saved_query", "daily-transformers")
        assert result == "daily-transformers"

    def test_validate_signal_negative_example(self):
        """validate_signal passes through negative_example values."""
        result = validate_signal("negative_example", "2301.00002")
        assert result == "2301.00002"

    def test_validate_signal_invalid_type_raises(self):
        """validate_signal raises ValueError on invalid signal type."""
        with pytest.raises(ValueError, match="Invalid signal type"):
            validate_signal("invalid_type", "some_value")


# ---------------------------------------------------------------------------
# Pydantic schema tests
# ---------------------------------------------------------------------------


class TestPydanticSchemas:
    """Test Pydantic schema construction and from_attributes conversion."""

    @pytest.mark.asyncio
    async def test_profile_summary_from_attributes(self, test_session):
        """ProfileSummary can be built from ORM model attributes."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.commit()

        # Construct ProfileSummary manually (signal_count not on ORM model)
        summary = ProfileSummary(
            slug=profile.slug,
            name=profile.name,
            signal_count=0,
            is_archived=profile.is_archived,
            negative_weight=profile.negative_weight,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )
        assert summary.slug == "my-ml-profile"
        assert summary.name == "My ML Profile"
        assert summary.signal_count == 0
        assert summary.is_archived is False
        assert summary.negative_weight == 0.3

    @pytest.mark.asyncio
    async def test_signal_info_from_attributes(self, test_session, sample_papers):
        """SignalInfo can be built from ORM model attributes."""
        profile = InterestProfile(**sample_profile_data())
        test_session.add(profile)
        await test_session.flush()

        signal = InterestSignal(
            profile_id=profile.id,
            **sample_signal_data(signal_value="2301.00001", reason="Important paper"),
        )
        test_session.add(signal)
        await test_session.commit()

        info = SignalInfo.model_validate(signal, from_attributes=True)
        assert info.signal_type == "seed_paper"
        assert info.signal_value == "2301.00001"
        assert info.status == "active"
        assert info.source == "manual"
        assert info.reason == "Important paper"
        assert info.added_at is not None

    def test_profile_detail_construction(self):
        """ProfileDetail can be constructed with signals and counts."""
        now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        detail = ProfileDetail(
            slug="my-profile",
            name="My Profile",
            signal_count=3,
            is_archived=False,
            negative_weight=0.3,
            created_at=now,
            updated_at=now,
            signals=[
                SignalInfo(
                    signal_type="seed_paper",
                    signal_value="2301.00001",
                    status="active",
                    source="manual",
                    added_at=now,
                    reason=None,
                ),
                SignalInfo(
                    signal_type="followed_author",
                    signal_value="john doe",
                    status="active",
                    source="manual",
                    added_at=now,
                    reason=None,
                ),
                SignalInfo(
                    signal_type="seed_paper",
                    signal_value="2301.00002",
                    status="active",
                    source="suggestion",
                    added_at=now,
                    reason="From shortlist",
                ),
            ],
            signal_counts_by_type={"seed_paper": 2, "followed_author": 1},
            signal_counts_by_source={"manual": 2, "suggestion": 1},
        )
        assert detail.signal_count == 3
        assert len(detail.signals) == 3
        assert detail.signal_counts_by_type["seed_paper"] == 2
        assert detail.signal_counts_by_source["suggestion"] == 1
