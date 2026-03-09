"""Pydantic v2 schemas for paper data.

Provides validation models for paper summaries (search results),
detailed paper views, version history, and search result wrappers.
All schemas support from_attributes for direct ORM model conversion.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class PaperVersion(BaseModel):
    """A single version entry in a paper's version history."""

    version: str  # "v1", "v2", etc.
    date: datetime
    size: str | None = None
    source_type: str | None = None


class PaperSummary(BaseModel):
    """Rich paper summary for search results and browse listings.

    Contains all fields needed for a useful result display: identity,
    core metadata, all four time semantics, version info, and license.
    """

    model_config = ConfigDict(from_attributes=True)

    # Identity
    arxiv_id: str
    title: str
    authors_text: str
    abstract_snippet: str  # Truncated abstract (max ~300 chars)

    # Classification
    categories: str
    primary_category: str
    category_list: list[str]

    # Time semantics
    submitted_date: datetime
    updated_date: datetime | None = None
    announced_date: date | None = None
    oai_datestamp: date

    # Version and rights
    latest_version: int | None = None
    license_uri: str | None = None

    # Max snippet length
    _ABSTRACT_MAX: ClassVar[int] = 300

    @classmethod
    def from_orm_paper(cls, paper, abstract_max: int = 300) -> PaperSummary:
        """Create a PaperSummary from an ORM Paper object.

        Truncates abstract to abstract_snippet with ellipsis if needed.
        """
        abstract = getattr(paper, "abstract", "") or ""
        if len(abstract) > abstract_max:
            snippet = abstract[:abstract_max] + "..."
        else:
            snippet = abstract

        return cls(
            arxiv_id=paper.arxiv_id,
            title=paper.title,
            authors_text=paper.authors_text,
            abstract_snippet=snippet,
            categories=paper.categories,
            primary_category=paper.primary_category,
            category_list=paper.category_list or [],
            submitted_date=paper.submitted_date,
            updated_date=paper.updated_date,
            announced_date=paper.announced_date,
            oai_datestamp=paper.oai_datestamp,
            latest_version=paper.latest_version,
            license_uri=paper.license_uri,
        )


class PaperDetail(PaperSummary):
    """Full paper detail extending PaperSummary.

    Includes the complete abstract, version history, external identifiers,
    provenance fields, and processing tier information.
    """

    # Full content
    abstract: str | None = None
    version_history: list[PaperVersion] | None = None

    # External identifiers
    doi: str | None = None
    comments: str | None = None
    journal_ref: str | None = None
    report_no: str | None = None

    # Provenance
    source: str | None = None
    fetched_at: datetime | None = None
    processing_tier: int | None = None
    promotion_reason: str | None = None

    # External IDs (populated in Phase 4)
    openalex_id: str | None = None
    semantic_scholar_id: str | None = None


class SearchResult(BaseModel):
    """A search result wrapping a PaperSummary with an optional relevance score."""

    paper: PaperSummary
    score: float | None = None


class WorkflowSearchResult(BaseModel):
    """Search result enriched with workflow context (triage state, collections).

    Wraps the same PaperSummary and score as SearchResult, plus:
    - triage_state: always present, defaults to "unseen" (absence-means-unseen)
    - collection_slugs: list of collection slugs this paper belongs to
    """

    paper: PaperSummary
    score: float | None = None
    triage_state: str = "unseen"
    collection_slugs: list[str] = []
