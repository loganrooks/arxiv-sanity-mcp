"""Metadata mapper: RawPaperMetadata -> Paper ORM instance.

Converts parsed OAI-PMH metadata (from any format parser) into
canonical Paper model instances ready for database insertion.
"""

from __future__ import annotations

from datetime import UTC, datetime

from dateutil import parser as dateutil_parser

from arxiv_mcp.db.models import Paper, ProcessingTier
from arxiv_mcp.ingestion.parsers import RawPaperMetadata


def _parse_datetime(date_str: str | None) -> datetime | None:
    """Parse a date string to a timezone-aware datetime.

    Tries datetime.fromisoformat first (fast path), falls back to
    dateutil.parser for arXiv's various date formats (e.g.,
    'Mon, 2 Jan 2023 12:00:00 GMT').

    Returns None for None or empty input.
    """
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str)
    except (ValueError, TypeError):
        try:
            dt = dateutil_parser.parse(date_str)
        except (ValueError, TypeError):
            return None

    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt


def map_to_paper(
    raw: RawPaperMetadata,
    source: str = "oai_pmh",
) -> Paper:
    """Map parsed metadata to a Paper ORM instance.

    Args:
        raw: Parsed metadata from any format parser.
        source: Data source identifier (default "oai_pmh").

    Returns:
        Paper ORM instance ready for DB insertion.
    """
    # Split categories into list
    category_list = raw.categories.split() if raw.categories else []
    primary_category = raw.primary_category or (category_list[0] if category_list else None)

    # Parse dates
    submitted_date = _parse_datetime(raw.submission_date)
    updated_date = _parse_datetime(raw.update_date)

    # Parse OAI datestamp to date
    oai_datestamp = None
    if raw.oai_datestamp:
        oai_dt = _parse_datetime(raw.oai_datestamp)
        if oai_dt:
            oai_datestamp = oai_dt.date()

    # Convert version history to JSONB-compatible list of dicts
    version_history = [
        {
            "version": v.version,
            "date": v.date,
            "size": v.size,
            "source_type": v.source_type,
        }
        for v in raw.versions
    ]

    # Determine latest version number
    latest_version = len(raw.versions) if raw.versions else None

    return Paper(
        arxiv_id=raw.arxiv_id,
        title=raw.title,
        authors_text=raw.authors,
        abstract=raw.abstract,
        submitter=raw.submitter,
        comments=raw.comments,
        journal_ref=raw.journal_ref,
        report_no=raw.report_no,
        categories=raw.categories or "",
        primary_category=primary_category,
        category_list=category_list if category_list else None,
        msc_class=raw.msc_class,
        acm_class=raw.acm_class,
        doi=raw.doi,
        submitted_date=submitted_date,
        updated_date=updated_date,
        oai_datestamp=oai_datestamp,
        license_uri=raw.license,
        latest_version=latest_version,
        version_history=version_history,
        processing_tier=ProcessingTier.FTS_INDEXED,
        source=source,
        fetched_at=datetime.now(UTC),
    )
