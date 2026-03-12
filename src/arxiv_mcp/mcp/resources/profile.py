"""Profile resource: profile://{slug}.

Provides interest profile with all signals, weights, and provenance.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.resource("profile://{slug}")
async def profile_resource(slug: str, ctx: Context) -> dict:
    """Interest profile with all signals, weights, and provenance."""
    app = _get_app(ctx)

    try:
        result = await app.profiles.get_profile(slug)
    except ValueError as e:
        return {"error": str(e)}

    return result.model_dump(mode="json")
