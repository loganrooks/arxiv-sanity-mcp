# Phase 5: MCP Validation & Iteration - Research

**Researched:** 2026-03-12
**Domain:** MCP validation workflows, prompt design, import scripting, evidence-based iteration
**Confidence:** HIGH

## Summary

Phase 5 is qualitatively different from Phases 1-4 and 04.1. Those phases built features; this phase validates them with real data and real workflows. The primary activities are: (1) importing the arxiv-scan dataset (154 papers, 1,211 triage decisions, tension vocabulary, citation data) into the MCP substrate, (2) running real literature review workflows through the MCP server, (3) designing and implementing MCP prompts based on observed usage patterns, (4) resolving doc 06 open questions with evidence, and (5) iterating the MCP surface based on what works and what does not.

The existing infrastructure is well-suited for this work. The MCP server (FastMCP 1.26.0) already supports `@mcp.prompt()` decorators with async functions, context injection, and typed arguments -- the same patterns used for tools and resources. The arxiv-scan pipeline data at `/scratch/arxiv-scan/pipeline/` contains 154 analyzed papers in JSON format with arXiv IDs, triage scores, tension engagement labels, and citation data. The existing `ArxivAPIClient.fetch_paper()` method fetches individual papers by ID with rate limiting, and `map_to_paper()` converts raw metadata to Paper ORM instances. The import script can compose these existing services without new infrastructure.

**Primary recommendation:** Structure the phase as three plans: (1) import script + data bootstrap, (2) MCP prompt implementation + validation session execution, (3) evidence-based iteration + doc 06 resolution. The import script is a prerequisite for everything else.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

1. **Phase 5 is qualitatively different from prior phases** -- primary activity is using the MCP, not building new code. Evidence from real usage drives design decisions.

2. **First validation dataset: arxiv-scan import** -- Use the arxiv-scan pipeline data at `/scratch/arxiv-scan/pipeline/` to bootstrap MCP usage. Import strategy:
   - Ingest 154 papers via arXiv API (metadata substrate)
   - Set triage states from paper-index value scores (shortlisted >= 7, seen <= 6)
   - Create interest profile from tension vocabulary
   - Enrich top papers via OpenAlex
   - Run ranking against imported papers to compare MCP ranking vs arxiv-scan human ranking
   - Test whether find_related_papers with known seeds surfaces the 4 false negatives

3. **Doc 06 open questions to resolve** -- 5 questions need evidence-based answers from validation:
   - How much workflow state belongs in v1? (validate agents use all tools)
   - Should interest profiles exist before collections, or vice versa? (observe ordering)
   - Should result sets be explicit persisted objects or ephemeral? (detect need for persistence)
   - Which operations benefit from resources vs tools? (observe agent reading patterns)
   - Which prompts are genuinely reusable? (design through practice)

4. **Prompt design candidates** -- Three prompts to design through practice:
   - `literature-review-session` (guided multi-step workflow)
   - `daily-digest` (automated monitoring)
   - `triage-shortlist` (batch evaluation)

5. **MCP surface iteration expectations** -- Specific iteration points identified in CONTEXT.md section 5.

6. **What NOT to build** -- No content normalization, no semantic search, no evaluation lenses, no new ranking scorers, no premature optimization.

7. **Success criteria interpretation** -- Precise definitions for all 4 success criteria provided in CONTEXT.md section 7.

### Claude's Discretion

- Import script structure (one-time CLI command vs standalone script)
- Prompt implementation ordering (which prompts first)
- Specific iteration changes to MCP surface based on validation evidence
- How to record validation observations (log format, structured notes, etc.)

### Deferred Ideas (OUT OF SCOPE)

- Content normalization (Phase 6)
- Semantic search (v2)
- Evaluation lenses / feedback loop design
- New ranking scorers or signal types (unless validation specifically reveals need)
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| MCP-05 | MCP server exposes reusable prompts: daily-digest, literature-map-from-seeds, triage-shortlist | FastMCP `@mcp.prompt()` decorator supports async functions, typed arguments, context injection. Prompt functions return `list[Message]` with `UserMessage`/`AssistantMessage`. See Architecture Patterns section for implementation pattern. |
| MCPV-01 | At least one real literature review session completed through MCP (search -> triage -> collect -> expand -> enrich) | Import script provides 154 real papers. Session can be run via `mcp dev` or Claude Code MCP client connection. Existing tools cover full workflow: search_papers, triage_paper, add_to_collection, find_related_papers, enrich_paper. |
| MCPV-02 | Doc 06 open questions resolved with evidence from MCP usage | 5 questions identified in CONTEXT.md section 3. Each needs a written answer citing specific observations. Validation session provides the evidence; structured observation log enables traceability. |
| MCPV-03 | MCP tool set iterated at least once based on real agent workflow feedback | CONTEXT.md section 5 identifies likely iteration points. Changes must be motivated by observations, not speculation. Iteration targets: create_watch two-step flow, add_signal batch, find_related_papers provenance, possible new tools (run_saved_query, bulk triage via MCP). |
</phase_requirements>

## Standard Stack

### Core (already installed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| mcp[cli] | 1.26.0 | FastMCP server framework | Already used for tools/resources; prompt support via same framework |
| sqlalchemy[asyncio] | >=2.0 | Async ORM for PostgreSQL | Already used throughout codebase |
| httpx | >=0.28 | Async HTTP client for arXiv API calls | Already used for API ingestion |
| click | >=8.1 | CLI framework | Already used; import script should be a CLI command |
| pytest-asyncio | >=0.24 | Async test runner | Already configured with asyncio_mode="auto" |

### Supporting (validation-specific)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| structlog | >=24.4 | Structured logging for validation observations | Already installed; use for recording validation session events |
| rich | >=13.9 | CLI output formatting | Already installed; use for import progress display |

### No New Dependencies Required

Phase 5 needs no new libraries. Everything required is already in pyproject.toml.

## Architecture Patterns

### Recommended Structure for New Code

```
src/arxiv_mcp/
├── mcp/
│   ├── prompts/              # NEW: prompt module directory
│   │   ├── __init__.py
│   │   ├── literature_review.py   # literature-review-session prompt
│   │   ├── daily_digest.py        # daily-digest prompt
│   │   └── triage_shortlist.py    # triage-shortlist prompt
│   └── server.py             # Add prompt module imports (side-effect registration)
├── scripts/                  # NEW: one-time operational scripts
│   └── import_arxiv_scan.py  # Import script for arxiv-scan data
tests/
├── test_mcp/
│   ├── test_prompts.py       # NEW: prompt unit tests
│   └── test_import.py        # NEW: import script tests (optional)
```

### Pattern 1: MCP Prompt Registration (FastMCP @mcp.prompt())

**What:** Register reusable prompts that generate message sequences for agent workflows.
**When to use:** For structured, multi-step workflows that agents should be able to invoke.
**Confidence:** HIGH -- verified from installed FastMCP source code at `.venv/lib/python3.13/site-packages/mcp/server/fastmcp/`.

```python
# Source: FastMCP 1.26.0 server.py lines 650-703, prompts/base.py
from mcp.server.fastmcp import Context
from mcp.server.fastmcp.prompts.base import UserMessage, AssistantMessage
from arxiv_mcp.mcp.server import AppContext, mcp

def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context

@mcp.prompt()
async def literature_review_session(
    seed_query: str,
    category: str | None = None,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> list[UserMessage | AssistantMessage]:
    """Guided literature review: search, triage, collect, expand, enrich.

    Start with a search query and optionally a category filter and interest
    profile. The prompt guides you through discovering papers, triaging them,
    building collections, expanding via related papers, and enriching metadata.
    """
    app = _get_app(ctx)

    # Build context-aware instruction based on current state
    instructions = f"You are conducting a literature review on: {seed_query}\n\n"
    instructions += "## Available Tools\n"
    instructions += "- search_papers: Find papers by query\n"
    instructions += "- triage_paper: Mark papers as shortlisted/dismissed/seen\n"
    # ... etc

    return [
        UserMessage(instructions),
    ]
```

**Key API details from source code:**
- `@mcp.prompt()` accepts optional `name`, `title`, `description`, `icons` parameters
- Function name becomes prompt name if `name` not specified
- Function arguments become prompt arguments (auto-extracted via func_metadata)
- Return type: `str | Message | dict | Sequence[str | Message | dict]`
- Async functions supported (coroutine result is awaited)
- Context injection works identically to tools (`ctx: Context = None`)
- Prompts are registered via side-effect import, same as tools/resources

### Pattern 2: Import Script as CLI Command

**What:** One-time import script that bootstraps the database with arxiv-scan data.
**When to use:** Before validation sessions. Rerunnable (idempotent via upsert).

```python
# Import script pattern -- compose existing services
import json
from pathlib import Path
from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.ingestion.arxiv_api import ArxivAPIClient
from arxiv_mcp.ingestion.mapper import map_to_paper

async def import_arxiv_scan(data_dir: Path, settings):
    """Import arxiv-scan pipeline data into MCP substrate."""
    sf = session_factory(create_engine(settings.database_url))
    client = ArxivAPIClient(settings)

    # 1. Load final-selection.json for paper IDs + scores
    with open(data_dir / "triage" / "final-selection.json") as f:
        selection = json.load(f)

    # 2. Fetch each paper via arXiv API, map, and upsert
    for paper_data in selection["papers"]:
        raw = await client.fetch_paper(paper_data["arxiv_id"])
        if raw:
            paper = map_to_paper(raw, source="arxiv_api")
            # Upsert into DB...

    # 3. Set triage states based on normalized_holistic scores
    # shortlisted >= 7, seen <= 6

    # 4. Create interest profile from tension vocabulary
    # 5. Enrich top papers via OpenAlex
```

### Pattern 3: Validation Observation Recording

**What:** Structured recording of validation session observations for evidence-based doc 06 answers.
**When to use:** During the validation session, to capture what works and what does not.

```python
# Observation log format (Markdown, not code)
# Record in: .planning/phases/05-mcp-validation-iteration/validation-log.md
#
# ## Observation: [timestamp]
# **Action:** [what was attempted]
# **Tool/Resource used:** [which MCP primitive]
# **Result:** [what happened]
# **Friction:** [what was awkward or missing]
# **Doc 06 relevance:** [which open question this informs]
```

### Anti-Patterns to Avoid

- **Speculative iteration:** Do not change the MCP surface based on guesses about what might be needed. Change it based on observed friction during real usage.
- **Building mock validation:** Do not create synthetic test scenarios and call them "validation." The point is real papers, real searches, real triage decisions.
- **Prompt-first design:** Do not design elaborate prompts before running the validation session. Design prompts from observed workflow patterns.
- **Over-engineering the import script:** The import script runs once. It does not need to be production-grade. It needs to be correct.
- **Conflating unit tests with validation:** Unit tests verify code correctness. Validation verifies that the MCP surface supports real workflows. Both matter; they are different things.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Paper ingestion from arXiv | Custom HTTP fetcher | `ArxivAPIClient.fetch_paper()` | Already handles rate limiting, XML parsing, ID extraction |
| Metadata-to-ORM mapping | Manual Paper() construction | `map_to_paper(raw, source="arxiv_api")` | Handles date parsing, version history, category splitting |
| Triage state setting | Direct DB INSERT | `TriageService.mark_triage()` | Handles state validation, triage log, upsert |
| Profile creation + signals | Direct DB operations | `ProfileService.create_profile()` + `add_signal()` | Handles slug generation, duplicate detection, provenance |
| Prompt registration | Manual MCP protocol implementation | `@mcp.prompt()` decorator | Handles argument extraction, rendering, context injection |
| Watch creation from query | Manual SavedQuery + flag setting | `create_watch` tool (compose create_saved_query + promote_to_watch) | Already handles two-step flow |

**Key insight:** Phase 5 should compose existing services, not build new ones. The import script is the only new "feature" code, and even it should be composed from existing service methods.

## Common Pitfalls

### Pitfall 1: arXiv API Rate Limiting During Bulk Import
**What goes wrong:** Importing 154 papers sequentially with the default 3-second rate limit takes ~8 minutes. If the script crashes mid-import, you restart from scratch.
**Why it happens:** ArxivAPIClient has a 3-second rate limit between requests (settings.harvest_rate_limit).
**How to avoid:**
1. The arXiv API supports batch fetch via `id_list` with comma-separated IDs (up to ~50 per request). Use `ArxivAPIClient.search()` or direct `id_list` requests to fetch in batches.
2. Make import idempotent: use ON CONFLICT upsert so re-runs skip existing papers.
3. Add progress reporting (Rich progress bar) so the user knows where import stands.
**Warning signs:** Import takes more than 2-3 minutes for 154 papers.

### Pitfall 2: Triage Score Mapping Ambiguity
**What goes wrong:** The arxiv-scan `normalized_holistic` scores range from 1-10 (z-score rescaled), but triage states are categorical (shortlisted/seen/dismissed). The threshold matters.
**Why it happens:** CONTEXT.md specifies "shortlisted >= 7, seen <= 6" but doesn't address granularity within "seen" (a 2 is very different from a 6).
**How to avoid:** Use the CONTEXT.md thresholds exactly. Papers with normalized_holistic >= 7 get "shortlisted", all others get "seen". Don't over-think the mapping -- this is validation data, not production triage.
**Warning signs:** Large numbers of papers in a single triage state (e.g., all 154 shortlisted or all seen).

### Pitfall 3: Prompt Context Token Budget
**What goes wrong:** Prompts that include too much context (full paper abstracts, collection listings, profile signals) can exhaust the agent's context window or produce overwhelming output.
**Why it happens:** MCP prompts are system-level messages injected into the conversation. Each prompt message consumes context tokens.
**How to avoid:** Keep prompt messages concise. Provide workflow guidance and tool references, not paper content. Let the agent use tools to fetch content as needed. The `literature-review-session` prompt should be ~500 tokens max, not 5,000.
**Warning signs:** Prompt render output exceeds 1,000 tokens.

### Pitfall 4: Conflating "Validation Session" with "Automated Test"
**What goes wrong:** Writing a pytest that calls MCP tools in sequence and declaring it "validation." This tests code correctness, not workflow usability.
**Why it happens:** Developer instinct to automate everything.
**How to avoid:** The validation session is an interactive MCP session with real agent interaction. The import script and prompt tests are automated. The validation itself is manual (agent + human working through a real research task). Record observations in a structured log.
**Warning signs:** No human-in-the-loop during validation; no subjective observations about workflow friction.

### Pitfall 5: Forgetting to Register Prompt Modules in server.py
**What goes wrong:** Prompts are defined but never appear in `mcp.list_prompts()`.
**Why it happens:** Tools and resources register via side-effect imports at the bottom of `server.py`. Prompts need the same treatment.
**How to avoid:** Add prompt module imports to server.py, mirroring the existing pattern:
```python
# Register prompt modules (side-effect imports)
from arxiv_mcp.mcp.prompts import literature_review, daily_digest, triage_shortlist  # noqa: F401, E402
```
**Warning signs:** `mcp dev` shows 0 prompts despite defined `@mcp.prompt()` functions.

### Pitfall 6: False Negative Test Depends on Corpus Coverage
**What goes wrong:** Testing whether `find_related_papers` surfaces the 4 false negatives (2501.11733, 2501.11425, 2510.23595, 2506.24119) fails because some of those papers are not in the database.
**Why it happens:** The import script ingests 154 papers from final-selection.json. The 4 false negatives may or may not be in that set. Need to also import the false negative papers.
**How to avoid:** Check which false negatives are already in the 154. Import any that are missing. The excluded-paper-audit.json at `/scratch/arxiv-scan/pipeline/excluded-paper-audit.json` has their arXiv IDs.
**Warning signs:** `find_related_papers` returns empty for known seeds because the seed or the false negatives are not in the corpus.

## Code Examples

### MCP Prompt Function (verified from FastMCP source)

```python
# Source: FastMCP 1.26.0 installed at .venv/lib/python3.13/site-packages/mcp/server/fastmcp/
# Decorator: server.py lines 650-703
# Base classes: prompts/base.py lines 22-50 (Message, UserMessage, AssistantMessage)
# Manager: prompts/manager.py (PromptManager.add_prompt, render_prompt)

from mcp.server.fastmcp import Context
from mcp.server.fastmcp.prompts.base import UserMessage, AssistantMessage

@mcp.prompt()
async def triage_shortlist(
    collection_slug: str,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> list[UserMessage]:
    """Batch-evaluate papers in a collection for triage decisions.

    Reviews each paper against the interest profile and recommends
    triage states with reasoning. Human confirms or overrides.
    """
    app = _get_app(ctx)

    # Fetch collection contents for context
    try:
        collection = await app.collections.show_collection(collection_slug)
        paper_count = len(collection.papers) if hasattr(collection, 'papers') else 0
    except ValueError:
        return [UserMessage(f"Collection '{collection_slug}' not found.")]

    profile_context = ""
    if profile_slug:
        try:
            profile = await app.profiles.get_profile(profile_slug)
            profile_context = f"\n\nInterest profile '{profile_slug}' has {profile.signal_count} signals."
        except ValueError:
            profile_context = f"\n\nWarning: Profile '{profile_slug}' not found. Proceeding without profile."

    instructions = f"""## Triage Shortlist: {collection_slug}

You have {paper_count} papers in collection '{collection_slug}' to evaluate.{profile_context}

### Workflow
For each paper in the collection:
1. Read the paper resource: paper://{{arxiv_id}}
2. Assess relevance against the research interest
3. Recommend a triage state (shortlisted, dismissed, seen, read, cite-later)
4. Provide brief reasoning

### Tools to Use
- get_paper: Read paper metadata and abstract
- triage_paper: Set the triage state after assessment
- enrich_paper: Get citation/topic data if needed for assessment

### Output Format
For each paper, provide:
- arXiv ID
- Title
- Recommended state
- 1-2 sentence reasoning

Start by listing all papers in the collection, then evaluate each one."""

    return [UserMessage(instructions)]
```

### Import Script Structure (composing existing services)

```python
# Source: existing patterns from ingestion/cli.py, workflow/triage.py, interest/profiles.py
import asyncio
import json
from pathlib import Path

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.ingestion.arxiv_api import ArxivAPIClient
from arxiv_mcp.ingestion.mapper import map_to_paper

async def _ingest_papers(sf, client, paper_ids: list[str]) -> dict:
    """Fetch papers from arXiv API and upsert into DB."""
    from sqlalchemy.dialects.postgresql import insert as pg_insert
    from arxiv_mcp.db.models import Paper

    ingested, skipped, errors = 0, 0, 0
    for arxiv_id in paper_ids:
        try:
            raw = await client.fetch_paper(arxiv_id)
            if raw is None:
                errors += 1
                continue
            paper = map_to_paper(raw, source="arxiv_api")
            async with sf() as session:
                # Upsert: skip if already exists
                stmt = pg_insert(Paper).values(
                    # ... paper fields
                ).on_conflict_do_nothing(index_elements=["arxiv_id"])
                await session.execute(stmt)
                await session.commit()
            ingested += 1
        except Exception as e:
            errors += 1
    return {"ingested": ingested, "skipped": skipped, "errors": errors}
```

### Prompt Test Pattern

```python
# Source: existing test pattern from tests/test_mcp/test_discovery_tools.py
import pytest
from unittest.mock import AsyncMock, MagicMock

class TestPromptRegistration:
    """Prompts are registered with correct names and arguments."""

    def test_prompt_names(self):
        from arxiv_mcp.mcp.server import mcp
        prompt_names = {p.name for p in mcp._prompt_manager.list_prompts()}
        expected = {"literature_review_session", "daily_digest", "triage_shortlist"}
        assert expected.issubset(prompt_names)

    def test_prompt_arguments(self):
        from arxiv_mcp.mcp.server import mcp
        prompt = mcp._prompt_manager.get_prompt("triage_shortlist")
        arg_names = {a.name for a in prompt.arguments}
        assert "collection_slug" in arg_names

class TestPromptRendering:
    """Prompts render to valid message sequences."""

    async def test_triage_shortlist_renders(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.prompts.triage_shortlist import triage_shortlist

        mock_app_context.collections.show_collection = AsyncMock(return_value=MagicMock(papers=[]))

        result = await triage_shortlist(collection_slug="test-coll", ctx=mock_ctx)
        assert isinstance(result, list)
        assert len(result) > 0
        assert result[0].role == "user"
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| MCP prompts as static strings | MCP prompts as async functions with context injection | FastMCP 1.x (2024-2025) | Prompts can fetch live state (collection contents, profile signals) before rendering |
| Validation via unit tests only | Validation via real agent workflow sessions | N/A (process change) | Phase 5 requires interactive validation, not just automated tests |

**Not deprecated:**
- `@mcp.prompt()` decorator API is current in mcp 1.26.0
- `@mcp.tool()` and `@mcp.resource()` patterns unchanged
- Side-effect import registration pattern unchanged

## Open Questions

1. **Batch fetch via arXiv API**
   - What we know: ArxivAPIClient.search() supports `id_list` parameter for multiple IDs. The arXiv API documentation states up to 2000 results per query and supports comma-separated ID lists.
   - What's unclear: Whether batch fetch with 154 IDs works in a single request or needs to be chunked. The API might have per-request ID limits.
   - Recommendation: Chunk into batches of 20-50 IDs per request. ArxivAPIClient already handles rate limiting.

2. **MCP Inspector / mcp dev for validation sessions**
   - What we know: `mcp dev` runs a development inspector that can call tools and resources interactively. The project uses `mcp[cli]` which includes the dev command.
   - What's unclear: Whether `mcp dev` supports prompt invocation in the inspector UI, or whether an agent client (Claude Code MCP connection) is needed for prompt-driven validation.
   - Recommendation: Plan for both. Use `mcp dev` for quick tool-level validation, then use Claude Code MCP client for prompt-driven agent workflow validation.

3. **Validation session: human-in-the-loop or fully autonomous agent?**
   - What we know: CONTEXT.md success criteria say "useful agent workflows" and "without human intervention beyond confirmation." The `triage-shortlist` prompt explicitly includes "human confirms or overrides."
   - What's unclear: Whether the "real literature review session" (MCPV-01) should be a fully autonomous agent run or an interactive human-guided session.
   - Recommendation: Interactive session with human observation. The agent does the work; the human watches, records observations, and provides confirmations. This produces richer evidence for doc 06 answers.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | `pyproject.toml` [tool.pytest.ini_options] |
| Quick run command | `pytest tests/test_mcp/ -x -q` |
| Full suite command | `pytest tests/ -x -q` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| MCP-05 | Prompts registered with correct names + arguments | unit | `pytest tests/test_mcp/test_prompts.py -x` | No -- Wave 0 |
| MCP-05 | Prompts render valid message sequences | unit | `pytest tests/test_mcp/test_prompts.py -x` | No -- Wave 0 |
| MCP-05 | Prompts accept context injection | unit | `pytest tests/test_mcp/test_prompts.py -x` | No -- Wave 0 |
| MCPV-01 | Import script ingests papers correctly | integration | `pytest tests/test_mcp/test_import.py -x` | No -- Wave 0 (optional) |
| MCPV-01 | Imported papers have correct triage states | integration | `pytest tests/test_mcp/test_import.py -x` | No -- Wave 0 (optional) |
| MCPV-01 | Full workflow session completed | manual | Human-observed agent session | N/A |
| MCPV-02 | Doc 06 answers documented with evidence | manual | Review of validation-log.md | N/A |
| MCPV-03 | MCP surface iterated based on evidence | unit | `pytest tests/test_mcp/ -x` | Existing tests updated |

### Sampling Rate

- **Per task commit:** `pytest tests/test_mcp/ -x -q`
- **Per wave merge:** `pytest tests/ -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_mcp/test_prompts.py` -- covers MCP-05 (prompt registration, rendering, context injection)
- [ ] `tests/test_mcp/test_import.py` -- covers MCPV-01 import correctness (optional -- import is one-time)
- [ ] No new framework install needed; existing pytest + pytest-asyncio infrastructure covers all requirements

## Sources

### Primary (HIGH confidence)

- FastMCP 1.26.0 source code at `.venv/lib/python3.13/site-packages/mcp/server/fastmcp/` -- prompt decorator API, Message/UserMessage/AssistantMessage classes, PromptManager
- Existing codebase at `src/arxiv_mcp/mcp/` -- tool/resource registration patterns, AppContext structure, `_get_app()` helper
- arxiv-scan pipeline data at `/scratch/arxiv-scan/pipeline/` -- 154 papers in final-selection.json, 4 false negatives in excluded-paper-audit.json, tension vocabulary in evaluation-guidelines.md

### Secondary (MEDIUM confidence)

- Existing ingestion patterns: `ArxivAPIClient.fetch_paper()`, `map_to_paper()`, CLI harvest commands
- Existing test patterns: mock AppContext, mock Context, direct function call testing (not MCP transport)

### Tertiary (LOW confidence)

- arXiv API batch ID list limits (not verified; chunking recommended as safety measure)
- `mcp dev` prompt invocation support (needs testing at runtime)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies, verified from installed packages
- Architecture patterns: HIGH -- prompt API verified from FastMCP source, patterns from existing codebase
- Pitfalls: HIGH -- derived from codebase analysis (rate limiting, registration patterns, data format inspection)
- Import script approach: HIGH -- data files inspected, service APIs verified from source
- Validation methodology: MEDIUM -- validation is inherently subjective; recording approach is a recommendation

**Research date:** 2026-03-12
**Valid until:** 2026-04-12 (stable -- no fast-moving dependencies)
