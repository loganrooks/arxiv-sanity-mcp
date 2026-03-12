"""Pydantic schemas for content normalization.

Defines VariantType enum, ContentStatus enum, AccessDecision model,
and ContentConversionResult model. These types are used by the content
service, rights checker, and conversion adapters.
"""

from __future__ import annotations

import enum

from pydantic import BaseModel


class VariantType(str, enum.Enum):
    """Content variant types for paper content.

    Each variant type represents a different source or format of paper content:
    - ABSTRACT: The paper abstract from arXiv metadata (always available)
    - HTML: ar5iv HTML rendering of the paper
    - SOURCE_DERIVED: Markdown extracted from LaTeX source
    - PDF_MARKDOWN: Markdown converted from PDF via Marker/Docling
    """

    ABSTRACT = "abstract"
    HTML = "html"
    SOURCE_DERIVED = "source_derived"
    PDF_MARKDOWN = "pdf_markdown"


class ContentStatus(str, enum.Enum):
    """Status of a content variant.

    - AVAILABLE: Content has been fetched/converted and is ready
    - PENDING: Content fetch/conversion is in progress or queued
    - FAILED: Content fetch/conversion failed (see error details)
    - NOT_AVAILABLE: Content is not available for this paper/variant
    """

    AVAILABLE = "available"
    PENDING = "pending"
    FAILED = "failed"
    NOT_AVAILABLE = "not_available"


class AccessDecision(BaseModel):
    """Result of a license/rights access check.

    Used by RightsChecker to communicate whether content access is
    allowed, with optional reason (for denial) or warning (for
    conditional access).
    """

    allowed: bool
    reason: str | None = None
    warning: str | None = None


class ContentConversionResult(BaseModel):
    """Result of converting paper content to normalized format.

    Captures the converted content along with full provenance:
    which backend performed the conversion, its version, the
    extraction method used, and any quality warnings generated.
    """

    content: str
    backend: str
    backend_version: str
    extraction_method: str
    quality_warnings: list[str] = []
