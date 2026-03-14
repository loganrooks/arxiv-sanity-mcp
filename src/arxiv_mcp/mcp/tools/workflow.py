"""Workflow tools: triage_paper, add_to_collection, create_watch.

Wraps TriageService, CollectionService, SavedQueryService, and WatchService
as MCP tools with user-intent-oriented names and dict return types.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context
from sqlalchemy.exc import IntegrityError

from arxiv_mcp.mcp.server import AppContext, mcp
from arxiv_mcp.workflow.util import slugify


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.tool()
async def triage_paper(
    arxiv_id: str,
    state: str,
    reason: str | None = None,
    ctx: Context = None,
) -> dict:
    """Set the triage state for a paper.

    Valid states: seen, shortlisted, dismissed, read, cite-later, archived, unseen.
    """
    app = _get_app(ctx)

    try:
        await app.triage.mark_triage(
            paper_id=arxiv_id, new_state=state, source="mcp", reason=reason
        )
    except ValueError as e:
        return {"error": str(e)}

    return {"arxiv_id": arxiv_id, "state": state, "updated": True}


@mcp.tool()
async def add_to_collection(
    arxiv_id: str,
    collection_name: str,
    ctx: Context = None,
) -> dict:
    """Add a paper to a collection. Creates the collection if it doesn't exist."""
    app = _get_app(ctx)
    slug = slugify(collection_name)

    try:
        await app.collections.add_papers(slug, [arxiv_id], source="mcp")
    except ValueError:
        # Collection doesn't exist -- create it, then retry
        try:
            await app.collections.create_collection(collection_name)
            await app.collections.add_papers(slug, [arxiv_id], source="mcp")
        except IntegrityError:
            return {"error": f"Paper '{arxiv_id}' not found in database"}
    except IntegrityError:
        return {"error": f"Paper '{arxiv_id}' not found in database"}

    return {"arxiv_id": arxiv_id, "collection": slug, "added": True}


@mcp.tool()
async def create_watch(
    name: str,
    query: str,
    category: str | None = None,
    cadence: str = "daily",
    ctx: Context = None,
) -> dict:
    """Create a monitored search that tracks new papers matching your query.

    Read the watch://{slug}/deltas resource to see papers added since your last check.
    """
    app = _get_app(ctx)

    params: dict = {"query_text": query}
    if category is not None:
        params["category"] = category

    try:
        saved = await app.saved_queries.create_saved_query(name=name, params=params)
    except ValueError as e:
        # Re-phrase internal "Saved query" terminology as user-facing "Watch"
        msg = str(e).replace("Saved query", "Watch")
        return {"error": msg}

    watch = await app.watches.promote_to_watch(saved.slug, cadence=cadence)

    return watch.model_dump(mode="json")
