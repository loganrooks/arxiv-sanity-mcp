"""Content normalization package for arxiv-mcp.

Provides content variant types, conversion result schemas, license
rights checking, adapters for PDF-to-markdown conversion, HTML fetching,
and the data layer for storing normalized paper content in multiple
formats (abstract, HTML, source-derived markdown, PDF-derived markdown).
"""

from arxiv_mcp.content.adapters import ContentAdapter, MarkerAdapter, MockContentAdapter
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
from arxiv_mcp.content.models import (
    AccessDecision,
    ContentConversionResult,
    ContentStatus,
    VariantType,
)
from arxiv_mcp.content.rights import RightsChecker

__all__ = [
    "AccessDecision",
    "ContentAdapter",
    "ContentConversionResult",
    "ContentStatus",
    "MarkerAdapter",
    "MockContentAdapter",
    "RightsChecker",
    "VariantType",
    "fetch_arxiv_html",
]
