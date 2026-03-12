"""Interest tools: add_signal, batch_add_signals.

Wraps ProfileService.add_signal as MCP tools with user-intent-oriented
names and dict return types.
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


@mcp.tool()
async def batch_add_signals(
    profile_slug: str,
    signals: list[dict],
    ctx: Context = None,
) -> dict:
    """Add multiple signals to an interest profile in one call.

    Each signal dict must have: signal_type, signal_value.
    Optional per-signal: reason.

    Returns a summary with counts and per-signal results.
    Continues on individual signal errors (partial success is OK).
    """
    app = _get_app(ctx)

    results = []
    added = 0
    errors = 0

    for sig in signals:
        signal_type = sig.get("signal_type", "")
        signal_value = sig.get("signal_value", "")
        reason = sig.get("reason")

        try:
            result = await app.profiles.add_signal(
                profile_slug, signal_type, signal_value, source="mcp", reason=reason
            )
            results.append(result.model_dump(mode="json"))
            added += 1
        except ValueError as e:
            results.append({"error": str(e), "signal_type": signal_type, "signal_value": signal_value})
            errors += 1

    return {
        "profile_slug": profile_slug,
        "total": len(signals),
        "added": added,
        "errors": errors,
        "results": results,
    }
