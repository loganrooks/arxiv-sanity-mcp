"""Literature review session prompt.

Guides an agent through a multi-step discovery workflow: search, triage,
collect, expand via related papers, and enrich top papers.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.fastmcp.prompts.base import UserMessage

from arxiv_mcp.mcp.server import mcp


@mcp.prompt()
async def literature_review_session(
    seed_query: str,
    category: str | None = None,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> list[UserMessage]:
    """Guided literature review: search, triage, collect, expand, enrich.

    Start with a search query and optionally a category filter and interest
    profile. The prompt guides you through discovering papers, triaging them,
    building collections, expanding via related papers, and enriching metadata.
    """
    # Build category and profile context lines
    category_line = ""
    if category:
        category_line = f"\nFilter by category: {category}"

    profile_line = ""
    if profile_slug:
        profile_line = (
            f"\nUse interest profile '{profile_slug}' for ranked results."
        )

    instructions = f"""## Literature Review: {seed_query}
{category_line}{profile_line}

### Workflow Steps

1. **Search** -- Use `search_papers` with query "{seed_query}"{f' and category "{category}"' if category else ''}. Scan titles and abstracts.
2. **Triage** -- For each relevant paper, use `triage_paper` to mark as shortlisted, dismissed, or seen.
3. **Collect** -- Use `add_to_collection` to group shortlisted papers into a named collection.
4. **Expand** -- Use `find_related_papers` with your best shortlisted paper IDs as seeds. Triage new discoveries.
5. **Enrich** -- Use `enrich_paper` on top papers to get citation counts and topic data.
6. **Iterate** -- Repeat steps 1-5 with refined queries until diminishing returns.

### Available Tools
- `search_papers` -- Full-text and metadata search
- `browse_recent` -- Recent papers by category
- `find_related_papers` -- Lexical similarity from seed papers
- `get_paper` -- Single paper metadata
- `triage_paper` -- Set triage state (shortlisted/dismissed/seen)
- `add_to_collection` -- Group papers into collections
- `enrich_paper` -- Fetch citation and topic data

### Tips
- Start broad, then narrow with category or date filters.
- Use `find_related_papers` with multiple seeds for better coverage.
- Enrich only papers you plan to read or cite."""

    return [UserMessage(instructions)]
