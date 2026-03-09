"""SQLAlchemy ORM models for arxiv-mcp.

Paper model and supporting types are defined here. The Base
declarative class is imported by alembic/env.py for autogenerate.
"""

from __future__ import annotations

import enum
from datetime import date, datetime

from sqlalchemy import ARRAY, Date, DateTime, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
