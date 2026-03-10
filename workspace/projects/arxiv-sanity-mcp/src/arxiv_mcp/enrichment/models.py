"""Pydantic schemas for enrichment data.

Defines EnrichmentResult, TopicInfo, ExternalIds, and EnrichmentStatus
for parsing and validating OpenAlex API responses.
"""

from __future__ import annotations

import enum
from datetime import date

from pydantic import BaseModel, field_validator


class EnrichmentStatus(str, enum.Enum):
    """Status of an enrichment operation."""

    SUCCESS = "success"
    NOT_FOUND = "not_found"
    PARTIAL = "partial"
    ERROR = "error"


def _strip_openalex_url(value: str | None, prefix: str = "https://openalex.org/") -> str | None:
    """Strip OpenAlex URL prefix to get short-form ID."""
    if value is None:
        return None
    if isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


def _strip_doi_url(value: str | None) -> str | None:
    """Strip doi.org URL prefix to get bare DOI."""
    if value is None:
        return None
    prefix = "https://doi.org/"
    if isinstance(value, str) and value.startswith(prefix):
        return value[len(prefix) :]
    return value


class TopicInfo(BaseModel):
    """OpenAlex topic with 4-level hierarchy (domain > field > subfield > topic)."""

    id: str
    display_name: str
    score: float
    subfield: dict
    field: dict
    domain: dict

    @field_validator("id", mode="before")
    @classmethod
    def strip_openalex_prefix(cls, v: str) -> str:
        result = _strip_openalex_url(v)
        return result if result is not None else v


class ExternalIds(BaseModel):
    """External identifiers for a paper (short forms, no URL prefixes)."""

    openalex_id: str | None = None
    doi: str | None = None

    @field_validator("openalex_id", mode="before")
    @classmethod
    def strip_openalex_prefix(cls, v: str | None) -> str | None:
        return _strip_openalex_url(v)

    @field_validator("doi", mode="before")
    @classmethod
    def strip_doi_prefix(cls, v: str | None) -> str | None:
        return _strip_doi_url(v)


class EnrichmentResult(BaseModel):
    """Parsed enrichment data from an external API response."""

    openalex_id: str | None = None
    doi: str | None = None
    cited_by_count: int | None = None
    fwci: float | None = None
    topics: list[TopicInfo] | None = None
    related_works: list[str] | None = None
    counts_by_year: list[dict] | None = None
    openalex_type: str | None = None
    raw_response: dict | None = None
    status: EnrichmentStatus = EnrichmentStatus.SUCCESS
    error_detail: str | None = None
    api_version: str = ""

    @classmethod
    def from_openalex_work(cls, work: dict) -> EnrichmentResult:
        """Parse raw OpenAlex Work JSON into structured result.

        Extracts primary_topic + topics (up to 3). Stores related_works
        as full URLs. Extracts doi without prefix. Extracts openalex_id
        as short form. Sets api_version to current date. Determines
        status based on field completeness.
        """
        # Extract IDs (short forms)
        openalex_id = _strip_openalex_url(work.get("id"))
        doi = _strip_doi_url(work.get("doi"))

        # Extract citation data
        cited_by_count = work.get("cited_by_count")
        fwci = work.get("fwci")

        # Extract topics (up to 3)
        topics: list[TopicInfo] | None = None
        raw_topics = work.get("topics", [])
        if raw_topics:
            topics = [TopicInfo.model_validate(t) for t in raw_topics[:3]]
        elif work.get("primary_topic"):
            topics = [TopicInfo.model_validate(work["primary_topic"])]

        # Related works (full URLs as returned by API)
        related_works = work.get("related_works")

        # Counts by year
        counts_by_year = work.get("counts_by_year")

        # Work type
        openalex_type = work.get("type")

        # API version as current date
        api_version = date.today().isoformat()

        # Determine status based on field completeness
        # success: cited_by_count present AND (fwci present OR topics present)
        # partial: cited_by_count present but missing fwci AND topics
        # not_found would be set by the caller for empty results
        if cited_by_count is not None and (fwci is not None or topics):
            status = EnrichmentStatus.SUCCESS
        elif cited_by_count is not None:
            status = EnrichmentStatus.PARTIAL
        else:
            status = EnrichmentStatus.PARTIAL

        return cls(
            openalex_id=openalex_id,
            doi=doi,
            cited_by_count=cited_by_count,
            fwci=fwci,
            topics=topics,
            related_works=related_works,
            counts_by_year=counts_by_year,
            openalex_type=openalex_type,
            raw_response=work,
            status=status,
            error_detail=None,
            api_version=api_version,
        )
