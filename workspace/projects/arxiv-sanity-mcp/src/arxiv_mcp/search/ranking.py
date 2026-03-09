"""Result shaping and ranking configuration for search results.

Converts raw SQLAlchemy Row objects to SearchResult Pydantic models
with truncated abstracts and optional relevance scores.
"""

from __future__ import annotations

from typing import Any

from arxiv_mcp.models.paper import PaperSummary, SearchResult


# Weight configuration matching the tsvector trigger:
# title = A (highest weight), authors = B, abstract = C
TSVECTOR_WEIGHTS = {
    "title": "A",
    "authors": "B",
    "abstract": "C",
}

# Default abstract snippet length
ABSTRACT_SNIPPET_MAX = 300


def shape_search_results(
    rows: list[Any],
    abstract_max: int = ABSTRACT_SNIPPET_MAX,
) -> list[SearchResult]:
    """Convert SQLAlchemy Row objects to SearchResult Pydantic models.

    Each row is expected to be a tuple of (Paper, rank) where rank may be None
    for non-text-search queries.

    Args:
        rows: List of (Paper, rank) tuples from query execution.
        abstract_max: Maximum abstract snippet length.

    Returns:
        List of SearchResult models.
    """
    results = []
    for row in rows:
        paper = row[0]  # Paper ORM object
        rank = row[1]   # rank score or None

        summary = PaperSummary.from_orm_paper(paper, abstract_max=abstract_max)
        score = float(rank) if rank is not None else None
        results.append(SearchResult(paper=summary, score=score))

    return results
