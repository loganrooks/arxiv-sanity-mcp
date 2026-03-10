"""Profile service for managing interest profiles and signals.

Provides full CRUD for profiles and signal management (add/remove)
for all 4 signal types: seed_paper, saved_query, followed_author,
negative_example. Follows the CollectionService pattern: session_factory
+ settings DI.
"""

from __future__ import annotations

import logging
from collections import Counter
from datetime import datetime, timezone

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import InterestProfile, InterestSignal, Paper, SavedQuery
from arxiv_mcp.interest.signals import validate_signal
from arxiv_mcp.models.interest import ProfileDetail, ProfileSummary, SignalInfo
from arxiv_mcp.workflow.util import slugify

logger = logging.getLogger(__name__)


class ProfileService:
    """Manages interest profiles with signal tracking and provenance.

    All mutations update profile.updated_at. Signal counts are computed
    from loaded signals. Slug collisions raise ValueError.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _get_profile_or_raise(
        self,
        session: AsyncSession,
        slug: str,
        *,
        load_signals: bool = False,
    ) -> InterestProfile:
        """Load profile by slug, optionally eager-loading signals."""
        stmt = select(InterestProfile).where(InterestProfile.slug == slug)
        if load_signals:
            stmt = stmt.options(selectinload(InterestProfile.signals))
        result = await session.execute(stmt)
        profile = result.scalar_one_or_none()
        if profile is None:
            raise ValueError(f"Profile {slug!r} not found")
        return profile

    def _to_summary(self, profile: InterestProfile, signal_count: int = 0) -> ProfileSummary:
        """Convert ORM profile to ProfileSummary."""
        return ProfileSummary(
            slug=profile.slug,
            name=profile.name,
            signal_count=signal_count,
            is_archived=profile.is_archived,
            negative_weight=profile.negative_weight,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
        )

    def _to_detail(self, profile: InterestProfile) -> ProfileDetail:
        """Convert ORM profile with loaded signals to ProfileDetail."""
        signals = [
            SignalInfo.model_validate(s, from_attributes=True)
            for s in profile.signals
        ]
        active_signals = [s for s in profile.signals if s.status == "active"]

        type_counts: dict[str, int] = dict(Counter(s.signal_type for s in active_signals))
        source_counts: dict[str, int] = dict(Counter(s.source for s in active_signals))

        return ProfileDetail(
            slug=profile.slug,
            name=profile.name,
            signal_count=len(profile.signals),
            is_archived=profile.is_archived,
            negative_weight=profile.negative_weight,
            created_at=profile.created_at,
            updated_at=profile.updated_at,
            signals=signals,
            signal_counts_by_type=type_counts,
            signal_counts_by_source=source_counts,
        )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create_profile(
        self,
        name: str,
        negative_weight: float | None = None,
        source: str = "manual",
    ) -> ProfileSummary:
        """Create a new named profile. Raises ValueError on slug collision."""
        slug = slugify(name)
        now = datetime.now(timezone.utc)

        if negative_weight is None:
            negative_weight = self.settings.default_negative_weight

        async with self.session_factory() as session:
            # Check for existing slug
            existing = await session.execute(
                select(InterestProfile).where(InterestProfile.slug == slug)
            )
            if existing.scalar_one_or_none() is not None:
                raise ValueError(f"Profile with slug {slug!r} already exists")

            # Check soft limit
            count_result = await session.execute(
                select(func.count()).select_from(InterestProfile)
            )
            count = count_result.scalar() or 0
            if count >= self.settings.soft_limit_profiles:
                logger.warning(
                    "Profile count (%d) exceeds soft limit (%d)",
                    count + 1,
                    self.settings.soft_limit_profiles,
                )

            profile = InterestProfile(
                slug=slug,
                name=name,
                is_archived=False,
                negative_weight=negative_weight,
                weights=None,
                created_at=now,
                updated_at=now,
            )
            session.add(profile)
            await session.commit()
            return self._to_summary(profile, signal_count=0)

    async def list_profiles(
        self, include_archived: bool = False
    ) -> list[ProfileSummary]:
        """List all profiles, optionally including archived ones."""
        async with self.session_factory() as session:
            # Subquery for signal count
            signal_count_subq = (
                select(func.count(InterestSignal.id))
                .where(InterestSignal.profile_id == InterestProfile.id)
                .correlate(InterestProfile)
                .scalar_subquery()
            )

            stmt = select(InterestProfile, signal_count_subq.label("signal_count"))
            if not include_archived:
                stmt = stmt.where(InterestProfile.is_archived == False)  # noqa: E712
            stmt = stmt.order_by(InterestProfile.created_at.desc())

            result = await session.execute(stmt)
            return [
                self._to_summary(row.InterestProfile, signal_count=row.signal_count or 0)
                for row in result.all()
            ]

    async def get_profile(self, slug: str) -> ProfileDetail:
        """Get a profile with all signals and computed counts."""
        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug, load_signals=True)
            return self._to_detail(profile)

    async def rename_profile(self, slug: str, new_name: str) -> ProfileSummary:
        """Rename a profile, regenerating its slug. Raises on slug conflict."""
        new_slug = slugify(new_name)
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)

            # Check new slug doesn't conflict
            if new_slug != slug:
                existing = await session.execute(
                    select(InterestProfile).where(InterestProfile.slug == new_slug)
                )
                if existing.scalar_one_or_none() is not None:
                    raise ValueError(f"Profile with slug {new_slug!r} already exists")

            profile.name = new_name
            profile.slug = new_slug
            profile.updated_at = now
            await session.commit()

            # Get signal count
            count_result = await session.execute(
                select(func.count(InterestSignal.id))
                .where(InterestSignal.profile_id == profile.id)
            )
            signal_count = count_result.scalar() or 0
            return self._to_summary(profile, signal_count=signal_count)

    async def archive_profile(self, slug: str) -> ProfileSummary:
        """Archive a profile (hide from default listing)."""
        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)
            profile.is_archived = True
            profile.updated_at = datetime.now(timezone.utc)
            await session.commit()

            count_result = await session.execute(
                select(func.count(InterestSignal.id))
                .where(InterestSignal.profile_id == profile.id)
            )
            signal_count = count_result.scalar() or 0
            return self._to_summary(profile, signal_count=signal_count)

    async def unarchive_profile(self, slug: str) -> ProfileSummary:
        """Unarchive a profile (show in default listing)."""
        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)
            profile.is_archived = False
            profile.updated_at = datetime.now(timezone.utc)
            await session.commit()

            count_result = await session.execute(
                select(func.count(InterestSignal.id))
                .where(InterestSignal.profile_id == profile.id)
            )
            signal_count = count_result.scalar() or 0
            return self._to_summary(profile, signal_count=signal_count)

    async def delete_profile(self, slug: str) -> None:
        """Delete a profile and all its signals (cascade)."""
        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)
            await session.delete(profile)
            await session.commit()

    # ------------------------------------------------------------------
    # Signal management (core)
    # ------------------------------------------------------------------

    async def add_signal(
        self,
        slug: str,
        signal_type: str,
        signal_value: str,
        source: str = "manual",
        reason: str | None = None,
    ) -> SignalInfo:
        """Add a signal to a profile.

        Validates signal type, normalizes value (for authors),
        checks FK targets for papers/queries, and prevents duplicates.
        """
        # Validate and normalize
        normalized_value = validate_signal(signal_type, signal_value)
        now = datetime.now(timezone.utc)
        status = "pending" if source == "suggestion" else "active"

        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)

            # FK validation for paper-based signals
            if signal_type in ("seed_paper", "negative_example"):
                paper = await session.execute(
                    select(Paper).where(Paper.arxiv_id == normalized_value)
                )
                if paper.scalar_one_or_none() is None:
                    raise ValueError(f"Paper {normalized_value!r} not found")

            # FK validation for saved query signals (warn, don't error)
            if signal_type == "saved_query":
                query = await session.execute(
                    select(SavedQuery).where(SavedQuery.slug == normalized_value)
                )
                if query.scalar_one_or_none() is None:
                    logger.warning(
                        "Saved query %r not found -- adding signal anyway "
                        "(query may have been deleted)",
                        normalized_value,
                    )

            # Check for existing duplicate
            existing = await session.execute(
                select(InterestSignal).where(
                    InterestSignal.profile_id == profile.id,
                    InterestSignal.signal_type == signal_type,
                    InterestSignal.signal_value == normalized_value,
                )
            )
            if existing.scalar_one_or_none() is not None:
                raise ValueError(
                    f"Signal ({signal_type}, {normalized_value!r}) already exists "
                    f"in profile {slug!r}"
                )

            signal = InterestSignal(
                profile_id=profile.id,
                signal_type=signal_type,
                signal_value=normalized_value,
                status=status,
                source=source,
                added_at=now,
                reason=reason,
            )
            session.add(signal)

            # Update profile timestamp
            profile.updated_at = now
            await session.commit()

            return SignalInfo.model_validate(signal, from_attributes=True)

    async def remove_signal(
        self,
        slug: str,
        signal_type: str,
        signal_value: str,
    ) -> None:
        """Remove a signal from a profile. Raises ValueError if not found."""
        # Normalize value for author signals
        normalized_value = validate_signal(signal_type, signal_value)

        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, slug)

            result = await session.execute(
                select(InterestSignal).where(
                    InterestSignal.profile_id == profile.id,
                    InterestSignal.signal_type == signal_type,
                    InterestSignal.signal_value == normalized_value,
                )
            )
            signal = result.scalar_one_or_none()
            if signal is None:
                raise ValueError(
                    f"Signal ({signal_type}, {normalized_value!r}) not found "
                    f"in profile {slug!r}"
                )

            await session.delete(signal)
            profile.updated_at = datetime.now(timezone.utc)
            await session.commit()

    # ------------------------------------------------------------------
    # Convenience wrappers
    # ------------------------------------------------------------------

    async def add_seed_paper(
        self, slug: str, arxiv_id: str, source: str = "manual", reason: str | None = None
    ) -> SignalInfo:
        """Add a seed paper signal to a profile."""
        return await self.add_signal(slug, "seed_paper", arxiv_id, source, reason)

    async def remove_seed_paper(self, slug: str, arxiv_id: str) -> None:
        """Remove a seed paper signal from a profile."""
        await self.remove_signal(slug, "seed_paper", arxiv_id)

    async def add_saved_query(
        self, slug: str, query_slug: str, source: str = "manual", reason: str | None = None
    ) -> SignalInfo:
        """Add a saved query signal to a profile."""
        return await self.add_signal(slug, "saved_query", query_slug, source, reason)

    async def remove_saved_query(self, slug: str, query_slug: str) -> None:
        """Remove a saved query signal from a profile."""
        await self.remove_signal(slug, "saved_query", query_slug)

    async def add_followed_author(
        self, slug: str, author_name: str, source: str = "manual", reason: str | None = None
    ) -> SignalInfo:
        """Add a followed author signal (name is normalized before storage)."""
        return await self.add_signal(slug, "followed_author", author_name, source, reason)

    async def remove_followed_author(self, slug: str, author_name: str) -> None:
        """Remove a followed author signal (name is normalized for lookup)."""
        await self.remove_signal(slug, "followed_author", author_name)

    async def add_negative_example(
        self, slug: str, arxiv_id: str, source: str = "manual", reason: str | None = None
    ) -> SignalInfo:
        """Add a negative example signal to a profile."""
        return await self.add_signal(slug, "negative_example", arxiv_id, source, reason)

    async def remove_negative_example(self, slug: str, arxiv_id: str) -> None:
        """Remove a negative example signal from a profile."""
        await self.remove_signal(slug, "negative_example", arxiv_id)
