"""SQLAlchemy ORM models for arxiv-mcp.

Paper model, workflow models, and supporting types are defined here.
The Base declarative class is imported by alembic/env.py for autogenerate.

All ORM models share a single Base to keep relationship references
in one module. Use string-based forward references in relationship().
"""

from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class ProcessingTier(enum.IntEnum):
    """Multi-tier processing levels for papers.

    Papers start at METADATA_ONLY (tier 0) after OAI-PMH ingestion.
    Higher tiers are reached via lazy enrichment and promotion.
    """

    METADATA_ONLY = 0
    FTS_INDEXED = 1
    ENRICHED = 2
    EMBEDDED = 3
    CONTENT_PARSED = 4


class Paper(Base):
    """Canonical paper model for arXiv metadata.

    Stores all metadata fields from OAI-PMH arXivRaw format, four
    distinct time semantics, external identifiers, provenance tracking,
    and a tsvector search column populated by a PostgreSQL trigger.
    """

    __tablename__ = "papers"

    # --- Identity ---
    arxiv_id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # --- Core metadata ---
    title: Mapped[str | None] = mapped_column(Text)
    authors_text: Mapped[str | None] = mapped_column(Text)
    abstract: Mapped[str | None] = mapped_column(Text)
    submitter: Mapped[str | None] = mapped_column(String(256))
    comments: Mapped[str | None] = mapped_column(Text)
    journal_ref: Mapped[str | None] = mapped_column(Text)
    report_no: Mapped[str | None] = mapped_column(String(256))

    # --- Classification ---
    categories: Mapped[str] = mapped_column(Text)  # Space-separated, all categories
    primary_category: Mapped[str | None] = mapped_column(String(20))
    category_list: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    msc_class: Mapped[str | None] = mapped_column(String(256))
    acm_class: Mapped[str | None] = mapped_column(String(256))

    # --- External identifiers ---
    doi: Mapped[str | None] = mapped_column(String(256))
    openalex_id: Mapped[str | None] = mapped_column(String(32))
    semantic_scholar_id: Mapped[str | None] = mapped_column(String(64))

    # --- Time semantics (INGS-03) ---
    submitted_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    announced_date: Mapped[date | None] = mapped_column(Date)
    oai_datestamp: Mapped[date | None] = mapped_column(Date)

    # --- Rights (INGS-04) ---
    license_uri: Mapped[str | None] = mapped_column(String(256))

    # --- Version info ---
    latest_version: Mapped[int | None] = mapped_column(Integer)
    version_history: Mapped[dict | None] = mapped_column(JSONB)

    # --- Processing tier ---
    processing_tier: Mapped[int] = mapped_column(Integer, default=0)
    promotion_reason: Mapped[str | None] = mapped_column(String(64))

    # --- Provenance (PAPR-04) ---
    source: Mapped[str] = mapped_column(String(32), default="oai_pmh")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_metadata_update: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # --- Full-text search vector (populated by trigger) ---
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR)

    __table_args__ = (
        Index("idx_papers_search_vector", "search_vector", postgresql_using="gin"),
        Index("idx_papers_primary_category", "primary_category"),
        Index("idx_papers_submitted_date", "submitted_date"),
        Index("idx_papers_announced_date", "announced_date"),
        Index("idx_papers_updated_date", "updated_date"),
        Index("idx_papers_oai_datestamp", "oai_datestamp"),
        Index("idx_papers_categories_gin", "category_list", postgresql_using="gin"),
        Index("idx_papers_processing_tier", "processing_tier"),
    )

    def __repr__(self) -> str:
        return f"<Paper(arxiv_id={self.arxiv_id!r}, title={self.title!r:.50})>"


# --- Workflow models (Phase 2) ---


class Collection(Base):
    """Named paper collection for organizing research workflow.

    Flat collections (no hierarchy). Papers belong via CollectionPaper
    association object. Slugs are auto-generated from names.
    """

    __tablename__ = "collections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    paper_associations: Mapped[list[CollectionPaper]] = relationship(
        "CollectionPaper", back_populates="collection", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Collection(slug={self.slug!r}, name={self.name!r})>"


class CollectionPaper(Base):
    """Association object for collection-paper membership with provenance.

    Stores extra columns (source, added_at) beyond a simple many-to-many.
    Source tracks how the paper was added: manual, saved_query, or agent.
    """

    __tablename__ = "collection_papers"

    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True
    )
    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"), primary_key=True
    )
    source: Mapped[str] = mapped_column(String(32), default="manual")
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    collection: Mapped[Collection] = relationship(
        "Collection", back_populates="paper_associations"
    )
    paper: Mapped[Paper] = relationship("Paper")

    __table_args__ = (
        Index("idx_collection_papers_paper_id", "paper_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<CollectionPaper(collection_id={self.collection_id}, "
            f"paper_id={self.paper_id!r}, source={self.source!r})>"
        )


class TriageState(Base):
    """Per-paper triage state (global, not per-collection).

    Only non-default states are stored. Absence of a row means 'unseen'.
    Valid states: shortlisted, dismissed, read, cite-later, archived.
    """

    __tablename__ = "triage_states"

    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"), primary_key=True
    )
    state: Mapped[str] = mapped_column(String(20), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "state IN ('shortlisted', 'dismissed', 'read', 'cite-later', 'archived')",
            name="ck_triage_state_valid",
        ),
        Index("idx_triage_states_state", "state"),
    )

    def __repr__(self) -> str:
        return f"<TriageState(paper_id={self.paper_id!r}, state={self.state!r})>"


class TriageLog(Base):
    """Audit trail for triage state transitions.

    Logs every state change with timestamp, source, and optional reason.
    old_state includes 'unseen' for first triage from no-row state.
    """

    __tablename__ = "triage_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"), nullable=False
    )
    old_state: Mapped[str] = mapped_column(String(20), nullable=False)
    new_state: Mapped[str] = mapped_column(String(20), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    source: Mapped[str] = mapped_column(String(32), default="manual")
    reason: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("idx_triage_log_paper_timestamp", "paper_id", "timestamp"),
    )

    def __repr__(self) -> str:
        return (
            f"<TriageLog(paper_id={self.paper_id!r}, "
            f"{self.old_state!r} -> {self.new_state!r})>"
        )


class SavedQuery(Base):
    """Named, reusable search query with optional watch functionality.

    Watch = saved query + checkpoint metadata (extends, not separate entity).
    Watch columns are nullable -- not all queries are watches.
    """

    __tablename__ = "saved_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Usage tracking
    run_count: Mapped[int] = mapped_column(Integer, default=0)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Watch fields (nullable -- not all queries are watches)
    is_watch: Mapped[bool] = mapped_column(Boolean, default=False)
    cadence_hint: Mapped[str | None] = mapped_column(String(20))
    checkpoint_date: Mapped[date | None] = mapped_column(Date)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_paused: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __repr__(self) -> str:
        watch = " (watch)" if self.is_watch else ""
        return f"<SavedQuery(slug={self.slug!r}{watch})>"


# --- Interest models (Phase 3) ---


class InterestProfile(Base):
    """Named interest profile containing typed signals.

    Profiles represent research threads (e.g., "attention-mechanisms",
    "philosophy-of-ai"). Each profile contains a set of typed signals
    that express the user's interests. Slugs are auto-generated from names.
    """

    __tablename__ = "interest_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    negative_weight: Mapped[float] = mapped_column(Float, default=0.3)
    weights: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    signals: Mapped[list[InterestSignal]] = relationship(
        "InterestSignal", back_populates="profile", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<InterestProfile(slug={self.slug!r}, name={self.name!r})>"


class InterestSignal(Base):
    """Typed signal within an interest profile.

    Each signal has a type (seed_paper, saved_query, followed_author,
    negative_example), a value, provenance tracking (source, added_at,
    reason), and a status (active, pending, dismissed).

    Unique constraint on (profile_id, signal_type, signal_value) prevents
    duplicate signals within a profile.
    """

    __tablename__ = "interest_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("interest_profiles.id", ondelete="CASCADE"), nullable=False
    )
    signal_type: Mapped[str] = mapped_column(String(32), nullable=False)
    signal_value: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    source: Mapped[str] = mapped_column(String(32), default="manual")
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    profile: Mapped[InterestProfile] = relationship(
        "InterestProfile", back_populates="signals"
    )

    __table_args__ = (
        CheckConstraint(
            "signal_type IN ('seed_paper', 'saved_query', 'followed_author', 'negative_example')",
            name="ck_signal_type_valid",
        ),
        CheckConstraint(
            "status IN ('active', 'pending', 'dismissed')",
            name="ck_signal_status_valid",
        ),
        UniqueConstraint(
            "profile_id", "signal_type", "signal_value",
            name="uq_interest_signals_profile_type_value",
        ),
        Index("idx_interest_signals_profile_type", "profile_id", "signal_type"),
    )

    def __repr__(self) -> str:
        return (
            f"<InterestSignal(profile_id={self.profile_id}, "
            f"type={self.signal_type!r}, value={self.signal_value!r})>"
        )
