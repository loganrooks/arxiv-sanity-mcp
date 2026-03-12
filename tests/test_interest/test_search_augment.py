"""Tests for search augmentation: docstring verification for PREMCP-03.

Ensures the _ranked_search pagination limitation is documented.
"""

from __future__ import annotations

from arxiv_mcp.interest.search_augment import ProfileRankingService


class TestPaginationDocumentation:
    """PREMCP-03: Verify pagination limitation is documented."""

    def test_ranked_search_pagination_documented(self):
        """PREMCP-03: Over-fetch pagination limitation must be documented."""
        doc = ProfileRankingService._ranked_search.__doc__
        assert doc is not None, "_ranked_search must have a docstring"
        assert "approximate" in doc.lower(), (
            "_ranked_search docstring must document approximate pagination"
        )
