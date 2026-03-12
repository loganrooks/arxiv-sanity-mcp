"""Daily digest prompt.

Guides an agent through an automated monitoring workflow: check watches
for new papers, triage them, and produce a summary organized by watch.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context
from mcp.server.fastmcp.prompts.base import UserMessage

from arxiv_mcp.mcp.server import mcp


@mcp.prompt()
async def daily_digest(
    profile_slug: str | None = None,
    ctx: Context = None,
) -> list[UserMessage]:
    """Automated daily monitoring: check watches, triage new papers, summarize.

    Reviews all active watches for new papers, performs quick triage on each,
    and produces a summary organized by watch/collection.
    """
    profile_line = ""
    if profile_slug:
        profile_line = (
            f"\nAssess each paper against interest profile '{profile_slug}'."
        )

    instructions = f"""## Daily Digest
{profile_line}

### Workflow Steps

1. **Check watches** -- Read each watch resource at `watch://{{slug}}/deltas` to find new papers since last check.
2. **Quick triage** -- For each new paper, use `get_paper` to read metadata. Assess relevance quickly.
3. **Auto-shortlist** -- Use `triage_paper` to shortlist high-confidence matches. Flag borderline papers as seen for human review.
4. **Summarize** -- Report findings organized by watch/collection: how many new papers, how many shortlisted, any notable discoveries.

### Available Tools
- `get_paper` -- Read paper metadata and abstract
- `triage_paper` -- Set triage state (shortlisted/seen)
- `search_papers` -- Follow up on interesting finds
- `enrich_paper` -- Get citation data for standout papers

### Resources
- `watch://{{slug}}/deltas` -- New papers for each watch

### Output Format
For each watch with new papers:
- Watch name and query
- Count of new papers
- Papers shortlisted (with 1-line reason each)
- Papers flagged for human review (with 1-line reason each)"""

    return [UserMessage(instructions)]
