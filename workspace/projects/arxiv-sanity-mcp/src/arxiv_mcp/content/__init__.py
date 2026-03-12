"""Content normalization package for arxiv-mcp.

Provides content variant types, conversion result schemas, license
rights checking, and the data layer for storing normalized paper
content in multiple formats (abstract, HTML, source-derived markdown,
PDF-derived markdown).
"""

from arxiv_mcp.content.models import (
    AccessDecision,
    ContentConversionResult,
    ContentStatus,
    VariantType,
)
from arxiv_mcp.content.rights import RightsChecker

__all__ = [
    "AccessDecision",
    "ContentConversionResult",
    "ContentStatus",
    "RightsChecker",
    "VariantType",
]
