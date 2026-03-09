"""Pydantic v2 schemas for workflow entities.

Provides response schemas for collections, triage states, saved queries,
watches, batch operations, stats, and export/import. All schemas that
bridge ORM models use ConfigDict(from_attributes=True).
"""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# --- Collection schemas ---


class CollectionSummary(BaseModel):
    """Summary view of a collection for listings."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    paper_count: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime


class CollectionMemberInfo(BaseModel):
    """Membership info for a paper in a collection."""

    model_config = ConfigDict(from_attributes=True)

    arxiv_id: str
    source: str
    added_at: datetime


class CollectionDetail(CollectionSummary):
    """Detailed view of a collection, extending summary with paper list."""

    papers: list[CollectionMemberInfo] = []


# --- Triage schemas ---


class TriageStateResponse(BaseModel):
    """Response schema for a paper's triage state."""

    model_config = ConfigDict(from_attributes=True)

    paper_id: str
    state: str
    updated_at: datetime


class TriageLogEntry(BaseModel):
    """A single entry in the triage audit trail."""

    model_config = ConfigDict(from_attributes=True)

    paper_id: str
    old_state: str
    new_state: str
    timestamp: datetime
    source: str
    reason: str | None = None


# --- Saved query schemas ---


class SavedQuerySummary(BaseModel):
    """Summary view of a saved query for listings."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    run_count: int
    last_run_at: datetime | None = None
    is_watch: bool
    cadence_hint: str | None = None
    created_at: datetime


class SavedQueryResponse(SavedQuerySummary):
    """Detailed view of a saved query, extending summary with params."""

    params: dict
    updated_at: datetime


# --- Watch schemas ---


class WatchSummary(BaseModel):
    """Summary view of a watch for the watch dashboard."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    cadence_hint: str | None = None
    checkpoint_date: date | None = None
    last_checked_at: datetime | None = None
    is_paused: bool
    pending_estimate: int | None = None


class WatchDashboard(BaseModel):
    """Aggregated view of all watches."""

    watches: list[WatchSummary]
    total_active: int
    total_paused: int


# --- Batch triage schemas ---


class BatchTriageResult(BaseModel):
    """Result of a batch triage operation."""

    affected_count: int
    skipped_count: int
    errors: list[str] = []


class BatchTriagePreview(BaseModel):
    """Preview of a query-based batch triage operation (dry-run)."""

    matching_count: int
    sample_ids: list[str]
    query_description: str


# --- Stats and export schemas ---


class WorkflowStats(BaseModel):
    """Overview of all workflow state."""

    collection_count: int
    triage_counts: dict[str, int]
    saved_query_count: int
    watch_count: int
    insights: list[str] = []


class ExportData(BaseModel):
    """Full workflow state export envelope."""

    version: str
    exported_at: datetime
    collections: list[dict] = []
    triage_states: list[dict] = []
    triage_log: list[dict] = []
    saved_queries: list[dict] = []
