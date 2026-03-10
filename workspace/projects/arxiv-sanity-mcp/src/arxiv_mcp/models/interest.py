"""Pydantic v2 schemas for interest profiles and signals.

Provides response schemas for interest profiles, signals, and
profile detail views. All schemas that bridge ORM models use
ConfigDict(from_attributes=True).
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


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
