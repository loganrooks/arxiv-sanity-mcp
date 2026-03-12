"""Interest tool: add_signal.

Wraps ProfileService.add_signal as an MCP tool with user-intent-oriented
name and dict return type.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.tool()
async def add_signal(
    profile_slug: str,
    signal_type: str,
    signal_value: str,
    reason: str | None = None,
    ctx: Context = None,
) -> dict:
    """Add a signal to an interest profile.

    Signal types: seed_paper (arXiv ID), saved_query (query slug),
    followed_author (author name), negative_example (arXiv ID).
    """
    app = _get_app(ctx)

    try:
        result = await app.profiles.add_signal(
            profile_slug, signal_type, signal_value, source="mcp", reason=reason
        )
    except ValueError as e:
        return {"error": str(e)}

    return result.model_dump(mode="json")
