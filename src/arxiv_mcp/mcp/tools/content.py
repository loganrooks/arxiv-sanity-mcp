"""Content tool: get_content_variant.

Wraps ContentService.get_or_create_variant as an MCP tool with serving-time
rights enforcement (CONT-06). Checks license_uri via RightsChecker before
returning non-abstract content. Deployment-mode-aware: local mode allows
with warning, hosted mode blocks restrictive licenses.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context

from arxiv_mcp.content.rights import RightsChecker
from arxiv_mcp.db.models import Paper
from arxiv_mcp.mcp.server import AppContext, mcp

VALID_VARIANTS = {"abstract", "html", "pdf_markdown", "best"}

_rights_checker = RightsChecker()


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.tool()
async def get_content_variant(
    arxiv_id: str,
    variant: str = "best",
    ctx: Context = None,
) -> dict:
    """Get paper content at the requested fidelity level.

    Retrieves paper content as abstract, HTML, or PDF-derived markdown.
    Use variant='best' (default) to get the highest-quality available format,
    which tries HTML first then falls back to PDF markdown.

    Valid variants: 'abstract', 'html', 'pdf_markdown', 'best'

    Returns content with provenance metadata (source, backend, license).
    For non-abstract variants, respects per-paper license restrictions.
    """
    app = _get_app(ctx)

    # 1. Validate variant parameter
    if variant not in VALID_VARIANTS:
        return {
            "error": (
                f"Invalid variant '{variant}'. "
                f"Valid variants: {', '.join(sorted(VALID_VARIANTS))}"
            )
        }

    # 2. For non-abstract variants, check rights before proceeding
    rights_warning = None
    if variant != "abstract":
        # Get Paper.license_uri from DB
        async with app.session_factory() as session:
            paper = await session.get(Paper, arxiv_id)

        if paper is None:
            return {"error": f"Paper '{arxiv_id}' not found"}

        license_uri = paper.license_uri
        decision = _rights_checker.check_access(
            license_uri, app.settings.deployment_mode
        )

        if not decision.allowed:
            return {
                "error": decision.reason,
                "license_uri": license_uri,
            }

        if decision.warning:
            rights_warning = decision.warning

    # 3. Delegate to ContentService
    try:
        result = await app.content.get_or_create_variant(arxiv_id, variant)
    except Exception as e:
        return {"error": str(e)}

    # 4. If service returned an error, pass it through
    if "error" in result:
        return result

    # 5. Add rights warning if present
    if rights_warning:
        result["rights_warning"] = rights_warning

    return result
