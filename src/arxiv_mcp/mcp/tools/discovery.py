"""Discovery tools: search_papers, browse_recent, find_related_papers, get_paper.

Wraps SearchService methods as MCP tools with user-intent-oriented names
and dict return types suitable for MCP transport.
"""

from __future__ import annotations

from datetime import date

from mcp.server.fastmcp import Context
from sqlalchemy import select

from arxiv_mcp.db.models import Paper
from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.tool()
async def search_papers(
    query: str | None = None,
    title: str | None = None,
    author: str | None = None,
    category: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    time_basis: str = "announced",
    page_size: int = 20,
    cursor: str | None = None,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> dict:
    """Search for arXiv papers by text, title, author, or category.

    Returns paginated results with paper metadata and relevance scores.
    Use cursor from previous results to get the next page.

    Optionally provide profile_slug to get profile-ranked results with
    ranking explanations on each result.

    Response shape: {"results": {"items": [...], "page_info": {...}}, "ranker_snapshot": ...}

    Without profile_slug: items include triage_state and collection_slugs;
    ranking_explanation is null; ranker_snapshot is null.

    With profile_slug: items additionally include ranking_explanation
    and the response includes a ranker_snapshot capturing ranker config.
    """
    app = _get_app(ctx)

    # Parse date strings to date objects if provided
    parsed_date_from = date.fromisoformat(date_from) if date_from else None
    parsed_date_to = date.fromisoformat(date_to) if date_to else None

    result = await app.profile_ranking.search_papers(
        profile_slug=profile_slug,
        query_text=query,
        title=title,
        author=author,
        category=category,
        date_from=parsed_date_from,
        date_to=parsed_date_to,
        time_basis=time_basis,
        page_size=page_size,
        cursor_token=cursor,
    )

    return result.model_dump(mode="json")


@mcp.tool()
async def browse_recent(
    category: str | None = None,
    time_basis: str = "announced",
    days: int = 7,
    page_size: int = 20,
    cursor: str | None = None,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> dict:
    """Browse recently announced arXiv papers, optionally filtered by category.

    Use time_basis to select ordering: announced, submitted, or updated.
    Note: Many papers may not have announced_date populated. If results are
    empty with the default time_basis='announced', try time_basis='submitted'.

    Optionally provide profile_slug to get profile-ranked results with
    ranking explanations on each result.

    Response shape: {"results": {"items": [...], "page_info": {...}}, "ranker_snapshot": ...}

    Without profile_slug: items include triage_state and collection_slugs;
    ranking_explanation is null; ranker_snapshot is null.

    With profile_slug: items additionally include ranking_explanation
    and the response includes a ranker_snapshot capturing ranker config.
    """
    app = _get_app(ctx)

    result = await app.profile_ranking.browse_recent(
        profile_slug=profile_slug,
        category=category,
        time_basis=time_basis,
        days=days,
        page_size=page_size,
        cursor_token=cursor,
    )

    return result.model_dump(mode="json")


@mcp.tool()
async def find_related_papers(
    seed_arxiv_ids: list[str] | str,
    page_size: int = 20,
    ctx: Context = None,
) -> list[dict]:
    """Find papers related to one or more seed papers via lexical similarity.

    Accepts a single arXiv ID or a list of IDs. When multiple seeds are given,
    results are merged and deduplicated, keeping the highest score for each paper.
    """
    app = _get_app(ctx)

    # Normalize to list
    if isinstance(seed_arxiv_ids, str):
        ids = [seed_arxiv_ids]
    else:
        ids = list(seed_arxiv_ids)

    seed_set = set(ids)

    # Collect results from each seed
    best_by_id: dict[str, object] = {}  # arxiv_id -> SearchResult with highest score
    for seed_id in ids:
        related = await app.search.find_related_papers(
            seed_arxiv_id=seed_id,
            page_size=page_size,
        )
        for item in related:
            aid = item.paper.arxiv_id
            # Exclude seed IDs from results
            if aid in seed_set:
                continue
            existing = best_by_id.get(aid)
            if existing is None or (item.score or 0) > (existing.score or 0):
                best_by_id[aid] = item

    merged = list(best_by_id.values())
    return [r.model_dump(mode="json") for r in merged]


@mcp.tool()
async def get_paper(
    arxiv_id: str,
    ctx: Context = None,
) -> dict:
    """Get metadata for a single paper by its arXiv ID."""
    app = _get_app(ctx)

    async with app.session_factory() as session:
        result = await session.execute(
            select(Paper).where(Paper.arxiv_id == arxiv_id)
        )
        paper = result.scalar_one_or_none()

    if paper is None:
        return {"error": f"Paper not found: {arxiv_id}"}

    return {
        "arxiv_id": paper.arxiv_id,
        "title": paper.title,
        "authors_text": paper.authors_text,
        "abstract": paper.abstract,
        "categories": paper.categories,
        "primary_category": paper.primary_category,
        "submitted_date": str(paper.submitted_date) if paper.submitted_date else None,
        "updated_date": str(paper.updated_date) if paper.updated_date else None,
        "announced_date": str(paper.announced_date) if paper.announced_date else None,
        "doi": paper.doi,
        "license_uri": paper.license_uri,
    }
