"""Enrichment tool: enrich_paper.

Wraps EnrichmentService.enrich_paper as an MCP tool with user-intent-oriented
name and dict return type.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.tool()
async def enrich_paper(
    arxiv_id: str,
    refresh: bool = False,
    ctx: Context = None,
) -> dict:
    """Trigger OpenAlex enrichment for a paper to get topics, citations, and related works.

    Set refresh=True to re-enrich even if data exists within the cooldown window.
    """
    app = _get_app(ctx)

    try:
        result = await app.enrichment.enrich_paper(arxiv_id, refresh=refresh)
    except (ValueError, Exception) as e:
        return {"error": str(e)}

    return result.model_dump(mode="json")
