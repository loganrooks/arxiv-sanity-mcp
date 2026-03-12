"""Collection resource: collection://{slug}.

Provides collection contents with paper metadata and triage states.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.resource("collection://{slug}")
async def collection_resource(slug: str, ctx: Context) -> dict:
    """Collection contents with paper metadata and triage states."""
    app = _get_app(ctx)

    try:
        result = await app.collections.show_collection(slug)
    except ValueError as e:
        return {"error": str(e)}

    return result.model_dump(mode="json")
