"""Enrichment adapters for external paper metadata sources.

Exports the core enrichment types for use by other modules.
"""

from arxiv_mcp.enrichment.models import (
    EnrichmentResult,
    EnrichmentStatus,
    ExternalIds,
    TopicInfo,
)
from arxiv_mcp.enrichment.openalex import EnrichmentAdapter, OpenAlexAdapter
from arxiv_mcp.enrichment.service import EnrichmentService

__all__ = [
    "EnrichmentAdapter",
    "EnrichmentResult",
    "EnrichmentService",
    "EnrichmentStatus",
    "ExternalIds",
    "OpenAlexAdapter",
    "TopicInfo",
]
