"""SQLAlchemy query builders for search, browse, and related-paper queries.

All functions return a Select statement that can be executed by the caller.
Query construction is kept separate from execution for testability and
composability. Uses PostgreSQL full-text search (tsvector/tsquery) with
GIN indexes for efficient filtering.
"""

from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import Select, desc, func, literal, select, tuple_

from arxiv_mcp.db.models import Paper
from arxiv_mcp.models.pagination import Cursor


def _get_date_column(time_basis: str):
    """Return the Paper date column for the given time basis."""
    mapping = {
        "submitted": Paper.submitted_date,
        "updated": Paper.updated_date,
        "announced": Paper.announced_date,
    }
    col = mapping.get(time_basis)
    if col is None:
        raise ValueError(f"Invalid time_basis: {time_basis!r}. Must be one of: {list(mapping)}")
    return col


def build_search_query(
    *,
    query_text: str | None = None,
    title: str | None = None,
    author: str | None = None,
    category: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    time_basis: str = "announced",
    cursor: Cursor | None = None,
    page_size: int = 20,
) -> Select:
    """Build a search query with full-text search and/or field filters.

    When query_text is provided, results are ordered by ts_rank_cd relevance.
    When only filters are provided (no text), results are ordered by date descending.

    Args:
        query_text: Full-text search query (supports AND/OR via websearch_to_tsquery).
        title: Title-only search text.
        author: Author name search text.
        category: arXiv category filter (e.g., "cs.CL").
        date_from: Start date for date range filter.
        date_to: End date for date range filter.
        time_basis: Which date column to use ("submitted", "updated", "announced").
        cursor: Pagination cursor for keyset pagination.
        page_size: Number of results to return (query fetches page_size + 1).

    Returns:
        SQLAlchemy Select statement.
    """
    date_col = _get_date_column(time_basis)
    has_text_search = query_text is not None

    # Build tsquery and rank expression for text search
    tsquery = None
    rank_expr = None
    if has_text_search:
        tsquery = func.websearch_to_tsquery("english", query_text)
        rank_expr = func.ts_rank_cd(Paper.search_vector, tsquery)
        stmt = select(Paper, rank_expr.label("rank")).where(
            Paper.search_vector.op("@@")(tsquery)
        )
    else:
        stmt = select(Paper, literal(None).label("rank"))

    # Title filter: search against title tsvector
    if title is not None:
        title_tsquery = func.plainto_tsquery("english", title)
        title_tsvector = func.to_tsvector("english", Paper.title)
        stmt = stmt.where(title_tsvector.op("@@")(title_tsquery))

    # Author filter: use 'simple' config for names
    if author is not None:
        author_tsquery = func.plainto_tsquery("simple", author)
        author_tsvector = func.to_tsvector("simple", Paper.authors_text)
        stmt = stmt.where(author_tsvector.op("@@")(author_tsquery))

    # Category filter
    if category is not None:
        stmt = stmt.where(Paper.category_list.any(category))

    # Date range filters
    if date_from is not None:
        stmt = stmt.where(date_col >= date_from)
    if date_to is not None:
        stmt = stmt.where(date_col <= date_to)

    # Ordering
    if has_text_search:
        # Relevance descending, then arxiv_id descending as tiebreaker
        stmt = stmt.order_by(desc(rank_expr), desc(Paper.arxiv_id))
    else:
        # Date descending, then arxiv_id descending
        stmt = stmt.order_by(desc(date_col), desc(Paper.arxiv_id))

    # Keyset cursor pagination
    if cursor is not None:
        if has_text_search:
            # For relevance-ordered results: use the rank expression directly
            # (cannot reference SELECT label aliases in WHERE clause)
            stmt = stmt.where(
                tuple_(rank_expr, Paper.arxiv_id)
                < tuple_(literal(float(cursor.sort_value)), literal(cursor.paper_id))
            )
        else:
            # For date-ordered results: (date_col, arxiv_id) < (cursor_date, cursor_id)
            stmt = stmt.where(
                tuple_(date_col, Paper.arxiv_id)
                < tuple_(literal(cursor.sort_value).cast(date_col.type), literal(cursor.paper_id))
            )

    # Fetch one extra to detect has_next
    stmt = stmt.limit(page_size + 1)

    return stmt


def build_browse_query(
    *,
    category: str | None = None,
    time_basis: str = "announced",
    days: int = 7,
    cursor: Cursor | None = None,
    page_size: int = 50,
) -> Select:
    """Build a query for browsing recently announced papers.

    Returns papers within the specified day window, ordered by date descending.

    Args:
        category: arXiv category filter (optional).
        time_basis: Which date column to use for recency.
        days: Number of days to look back from the max date in the database.
        cursor: Pagination cursor.
        page_size: Number of results to return (query fetches page_size + 1).

    Returns:
        SQLAlchemy Select statement.
    """
    date_col = _get_date_column(time_basis)

    stmt = select(Paper, literal(None).label("rank"))

    # Date cutoff: use subquery to find max date, then subtract days
    # This makes tests deterministic (not dependent on current date)
    max_date_subquery = select(func.max(date_col)).scalar_subquery()
    cutoff_expr = max_date_subquery - timedelta(days=days)
    stmt = stmt.where(date_col >= cutoff_expr)

    # Category filter
    if category is not None:
        stmt = stmt.where(Paper.category_list.any(category))

    # Order by date descending, arxiv_id descending
    stmt = stmt.order_by(desc(date_col), desc(Paper.arxiv_id))

    # Keyset cursor pagination
    if cursor is not None:
        stmt = stmt.where(
            tuple_(date_col, Paper.arxiv_id)
            < tuple_(literal(cursor.sort_value).cast(date_col.type), literal(cursor.paper_id))
        )

    stmt = stmt.limit(page_size + 1)

    return stmt


def build_related_query(
    *,
    seed_paper: Paper,
    page_size: int = 20,
) -> Select:
    """Build a query for finding papers related to a seed paper via lexical similarity.

    Uses the seed paper's title (via plainto_tsquery, which ANDs all terms for
    focused matching) combined with an OR-based query from key abstract terms
    (via to_tsquery with '|' operators) for broader recall. The two queries
    are combined with tsquery_or (||) so a paper matching either the title
    terms or abstract terms will be included, with ts_rank_cd providing
    relevance ordering.

    Args:
        seed_paper: The ORM Paper object to find related papers for.
        page_size: Maximum number of related papers to return.

    Returns:
        SQLAlchemy Select statement.
    """
    # Use the title as a focused AND query for high-precision matching
    seed_title = seed_paper.title or ""
    title_tsquery = func.plainto_tsquery("english", seed_title)

    # For the abstract, use an OR-based approach by converting the abstract
    # to a tsvector, extracting lexemes, and building an OR query.
    # This avoids the overly-restrictive AND behavior of plainto_tsquery
    # on long text. We use the database to construct the query:
    # ts_rewrite or strip + individual terms.
    #
    # Simplest robust approach: use websearch_to_tsquery with OR-joined
    # key terms from the abstract (first ~200 chars for relevance).
    seed_abstract = (seed_paper.abstract or "")[:200]

    # Build an OR query from abstract words using websearch_to_tsquery
    # by joining terms with OR
    abstract_words = [w for w in seed_abstract.split() if len(w) > 3][:15]
    if abstract_words:
        or_query_text = " OR ".join(abstract_words)
        abstract_tsquery = func.websearch_to_tsquery("english", or_query_text)
        # Combine title (AND) with abstract (OR) using tsquery OR operator
        combined_tsquery = title_tsquery.op("||")(abstract_tsquery)
    else:
        combined_tsquery = title_tsquery

    rank_expr = func.ts_rank_cd(Paper.search_vector, combined_tsquery)

    stmt = (
        select(Paper, rank_expr.label("rank"))
        .where(Paper.search_vector.op("@@")(combined_tsquery))
        .where(Paper.arxiv_id != seed_paper.arxiv_id)
        .order_by(desc(rank_expr), desc(Paper.arxiv_id))
        .limit(page_size)
    )

    return stmt
