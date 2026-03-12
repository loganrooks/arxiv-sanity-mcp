"""Triage shortlist prompt.

Guides an agent through batch evaluation of papers in a collection,
recommending triage states with reasoning for human confirmation.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.fastmcp.prompts.base import UserMessage

from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.prompt()
async def triage_shortlist(
    collection_slug: str,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> list[UserMessage]:
    """Batch-evaluate papers in a collection for triage decisions.

    Reviews each paper against the research interest and recommends
    triage states with reasoning. Human confirms or overrides.
    """
    app = _get_app(ctx)

    # Fetch live collection state for paper count
    try:
        collection = await app.collections.show_collection(collection_slug)
        paper_count = collection.page_info.total_estimate or len(collection.items)
    except ValueError:
        return [UserMessage(f"Collection '{collection_slug}' not found. Create it first with `add_to_collection`.")]

    profile_line = ""
    if profile_slug:
        profile_line = (
            f"\nAssess each paper against interest profile '{profile_slug}'."
        )

    instructions = f"""## Triage Shortlist: {collection_slug}

You have {paper_count} papers in collection '{collection_slug}' to evaluate.{profile_line}

### Workflow
For each paper in the collection:
1. Read the paper resource: `paper://{{arxiv_id}}`
2. Assess relevance to the research interest
3. Recommend a triage state (shortlisted, dismissed, seen, read, cite-later)
4. Provide 1-2 sentence reasoning

Human confirms or overrides each recommendation.

### Available Tools
- `get_paper` -- Read paper metadata and abstract
- `triage_paper` -- Set the triage state after assessment
- `enrich_paper` -- Get citation/topic data if needed for assessment

### Output Format
For each paper:
- arXiv ID and title
- Recommended triage state
- 1-2 sentence reasoning

Start by listing all papers in the collection, then evaluate each one."""

    return [UserMessage(instructions)]
