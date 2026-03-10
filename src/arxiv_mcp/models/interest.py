"""Pydantic v2 schemas for interest profiles, signals, and ranking.

Provides response schemas for interest profiles, signals,
profile detail views, and ranking types (SignalScore, RankingExplanation,
RankerSnapshot). All schemas that bridge ORM models use
ConfigDict(from_attributes=True).

Ranking types are Pydantic BaseModels (not dataclasses) to support
nested serialization in ProfileSearchResult and ProfileSearchResponse.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


# --- Signal schemas ---


class SignalInfo(BaseModel):
    """Individual signal within a profile, with provenance."""

    model_config = ConfigDict(from_attributes=True)

    signal_type: str
    signal_value: str
    status: str
    source: str
    added_at: datetime
    reason: str | None = None


# --- Profile schemas ---


class ProfileSummary(BaseModel):
    """Summary view of an interest profile for listings."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    signal_count: int
    is_archived: bool
    negative_weight: float
    created_at: datetime
    updated_at: datetime


class ProfileDetail(ProfileSummary):
    """Detailed view of a profile with full signal list and counts."""

    signals: list[SignalInfo] = []
    signal_counts_by_type: dict[str, int] = {}
    signal_counts_by_source: dict[str, int] = {}


# --- Request schemas ---


class ProfileCreateRequest(BaseModel):
    """Request schema for creating a new profile."""

    name: str
    negative_weight: float = 0.3


class ProfileUpdateRequest(BaseModel):
    """Request schema for updating profile settings."""

    name: str | None = None
    negative_weight: float | None = None
    weights: dict | None = None


# --- Ranking types ---


class SignalType(StrEnum):
    """Types of ranking signals that can contribute to composite score."""

    QUERY_MATCH = "query_match"
    SEED_RELATION = "seed_relation"
    CATEGORY_OVERLAP = "category_overlap"
    INTEREST_PROFILE_MATCH = "interest_profile_match"
    RECENCY = "recency"


class SignalScore(BaseModel):
    """A single signal's contribution to the composite ranking score.

    Each signal produces a normalized score in [0.0, 1.0], a weight,
    a weighted_score (which may be reduced by negative demotion),
    and a human-readable explanation.
    """

    signal_type: SignalType
    raw_score: float
    normalized_score: float
    weight: float
    weighted_score: float
    explanation: str


class RankingExplanation(BaseModel):
    """Explains how a paper's composite ranking score was computed.

    Every ranked result includes this to support inspectable ranking
    (ADR-0001 exploration-first architecture).
    """

    composite_score: float
    signal_breakdown: list[SignalScore]
    ranker_version: str


class RankerSnapshot(BaseModel):
    """Captures pipeline configuration at query time for reproducibility.

    Attached to ProfileSearchResponse so consumers can inspect
    exactly what ranker state produced the result set.
    """

    profile_slug: str | None
    ranker_version: str
    weights: dict[str, float]
    signal_types_applied: list[str]
    seed_paper_count: int
    followed_author_count: int
    negative_example_count: int
    saved_query_count: int
    negative_weight: float
    captured_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


    # ProfileSearchResponse is defined in interest/search_augment.py to avoid
    # circular imports (it references both PaginatedResponse and ProfileSearchResult)
