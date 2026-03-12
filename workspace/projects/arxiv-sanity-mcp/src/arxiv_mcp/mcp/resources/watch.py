"""Watch deltas resource: watch://{slug}/deltas.

Provides papers new since the last checkpoint for a watch.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.resource("watch://{slug}/deltas")
async def watch_deltas_resource(slug: str, ctx: Context) -> dict:
    """Papers new since the last checkpoint for this watch."""
    app = _get_app(ctx)

    try:
        result = await app.watches.check_watch(slug)
    except ValueError as e:
        return {"error": str(e)}

    return result.model_dump(mode="json")
