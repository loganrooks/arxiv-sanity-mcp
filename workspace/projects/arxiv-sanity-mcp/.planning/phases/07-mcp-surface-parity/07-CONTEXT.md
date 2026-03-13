# Phase 07 Context: MCP Surface Parity (GAP CLOSURE)

**Date:** 2026-03-12
**Source:** Auto-generated from codebase analysis, ROADMAP.md success criteria, and Phase 04.1/05 patterns
**Phase Character:** Gap closure — wiring existing services into MCP, not building new business logic

---

## Phase Boundary

Phase 7 closes the gap between CLI capabilities and MCP tool surface. After Phase 04.1 shipped the initial MCP server (9 tools → 11 after Phase 5), the CLI still offers profile-ranked search, workflow-enriched results, profile creation, and signal suggestions that MCP clients cannot access. Phase 7 wires these existing services into MCP tools so agents have full parity with CLI users.

This is a **wiring phase**, not a feature phase. All business logic already exists in `ProfileRankingService`, `SuggestionService`, `ProfileService`, and `WorkflowSearchService`. Phase 7 exposes them through MCP protocol without modification.

---

## What Already Exists

### Services Ready to Wire

| Service | Location | Already in AppContext? | Phase 7 Action |
|---------|----------|----------------------|----------------|
| `ProfileRankingService` | `src/arxiv_mcp/interest/search_augment.py` | **No** | Add to AppContext, use from discovery tools |
| `SuggestionService` | `src/arxiv_mcp/interest/suggestions.py` | **No** | Add to AppContext, expose as tool |
| `ProfileService` | `src/arxiv_mcp/interest/profiles.py` | **Yes** | Already available; expose `create_profile` as tool |
| `WorkflowSearchService` | Composed inside `SearchService` | **Yes** (via search) | Already returns `WorkflowSearchResult`; ensure MCP surfaces it |

### Models Ready for MCP Transport

| Model | Module | Serialization |
|-------|--------|---------------|
| `ProfileSearchResult` | `models/paper.py` | Extends `SearchResult` with `RankingExplanation` |
| `ProfileSearchResponse` | `interest/search_augment.py` | Wraps `PaginatedResponse[ProfileSearchResult]` + `RankerSnapshot` |
| `WorkflowSearchResult` | `models/paper.py` | Extends `SearchResult` with `triage_state`, `collection_slugs` |
| `RankerSnapshot` | `models/interest.py` | Profile config at query time (weights, signal counts) |
| `SuggestionCandidate` | `interest/suggestions.py` | Dataclass with `signal_type`, `signal_value`, `reason`, `score` |
| `ProfileSummary` | `models/interest.py` | Returned by `create_profile` |

### Established MCP Patterns (from Phase 04.1)

All existing tools follow these conventions — Phase 7 must match:

1. **Return type:** `dict` (via `.model_dump(mode="json")`) — MCP transport requires JSON-serializable dicts, not Pydantic models
2. **Context extraction:** `_get_app(ctx)` helper per tool module
3. **Tool registration:** `@mcp.tool()` decorator, functions in `src/arxiv_mcp/mcp/tools/`
4. **Error handling:** Return `{"error": "message"}` dict, not exceptions
5. **Import side-effects:** Tool modules register via import at bottom of `server.py`

---

## Implementation Decisions

### 1. AppContext Expansion

Add `ProfileRankingService` and `SuggestionService` to the `AppContext` dataclass and initialize in `app_lifespan()`.

- `ProfileRankingService` requires `session_factory` and the existing `SearchService` (it wraps `WorkflowSearchService` internally via over-fetch + re-rank)
- `SuggestionService` requires `session_factory`, `Settings`, and `ProfileService`
- Keep existing field naming convention: `profiles`, `search`, `triage` → use `profile_ranking` and `suggestions`

### 2. Discovery Tool Enhancement (search_papers + browse_recent)

**Add `profile_slug: str | None = None` parameter** to both `search_papers` and `browse_recent`.

Behavior:
- **If `profile_slug` is None:** Current behavior unchanged — call `app.search.search_papers(...)`, return bare results
- **If `profile_slug` provided:** Call `app.profile_ranking.search_papers(profile_slug=..., ...)` instead, return `ProfileSearchResponse` with ranked results + `RankerSnapshot`

The CLI implementation in `src/arxiv_mcp/search/cli.py` (lines 210-268) shows the exact pattern. The MCP version should match.

**WorkflowSearchResult enrichment:** Currently `search_papers` and `browse_recent` return `SearchResult`. The existing `WorkflowSearchService` already produces `WorkflowSearchResult` (with `triage_state` + `collection_slugs`). Verify the service composition chain surfaces these fields through MCP — if `SearchService` delegates to `WorkflowSearchService`, the enriched fields should already be present in the model dump. If not, the tools need to call the workflow-enriched path.

### 3. New Tool: create_profile

**Location:** `src/arxiv_mcp/mcp/tools/interest.py` (extend existing file)

Parameters:
- `name: str` (required) — profile display name
- `negative_weight: float | None = None` — weight for negative signals (default from service)

Returns: `dict` — `ProfileSummary.model_dump(mode="json")` (slug, name, signal_count, created_at)

Maps directly to `app.profiles.create_profile(name, negative_weight)`.

### 4. New Tool: suggest_signals

**Location:** `src/arxiv_mcp/mcp/tools/interest.py` (extend existing file)

Parameters:
- `profile_slug: str` (required) — which profile to generate suggestions for
- `auto_add: bool = False` — if True, automatically add suggestions as pending signals

Returns: `dict` with:
- `candidates`: list of `{signal_type, signal_value, reason, score}`
- `added_count`: number added (only if `auto_add=True`)

Maps to `app.suggestions.generate_suggestions(profile_slug)` and optionally `app.suggestions.add_suggestions_to_profile(profile_slug, candidates)`.

Note: `SuggestionCandidate` is a dataclass, not Pydantic — serialize manually via `asdict()` or explicit dict construction.

### 5. Response Format for Profile-Ranked Results

When `profile_slug` is provided to search tools, the response should include:
- `results`: the paginated results (each item has `ranking_explanation` with composite score + signal breakdown)
- `ranker_snapshot`: profile configuration at query time (weights, signal counts, types applied)
- `page_info`: standard pagination cursor

Use `ProfileSearchResponse.model_dump(mode="json")` — it already bundles results + snapshot.

### Claude's Discretion

- Whether to add an `explain: bool = False` parameter to discovery tools (CLI has `--explain` flag) or always include explanations when profile_slug is present
- Whether `find_related_papers` should also support `profile_slug` (CLI doesn't, but it's a natural extension)
- Test file organization: extend existing test files vs. create new ones
- Whether `SuggestionCandidate` should be converted to Pydantic for consistent `.model_dump()` — or keep manual dict conversion

---

## Specific Ideas

### CLI Parity Reference

The CLI implementations serve as the authoritative reference for what MCP should match:

- **Profile-ranked search:** `src/arxiv_mcp/search/cli.py` lines 210-268
- **Profile creation:** `src/arxiv_mcp/interest/cli.py` lines 68-83
- **Signal suggestions:** `src/arxiv_mcp/interest/cli.py` lines 493-553

### Tool Count Target

Phase 04.1 shipped 9 tools, Phase 5 added 2 (content + batch_signals) for 11 total. Phase 7 adds 2 new tools (`create_profile`, `suggest_signals`) and enhances 2 existing tools (`search_papers`, `browse_recent`). Final count: **13 tools** — still within the MCP-07 guideline range.

### Integration Test Pattern

Phase 04.1 and 05 established the test pattern in `tests/mcp/test_tools_*.py`. Each tool has:
- A test for the happy path
- A test for error/edge cases (missing profile, empty results)
- Tests use the test database fixture with seeded data

---

## What NOT to Build in Phase 7

- **No new business logic** — MCP wraps existing services only (same rule as Phase 04.1)
- **No semantic search** — remains v2 scope
- **No prompt additions** — existing 3 prompts sufficient unless validation reveals need
- **No bulk profile operations** — single profile creation is sufficient for parity
- **No suggestion confirmation/dismissal workflow** — `auto_add` covers the primary use case; full lifecycle is future work
- **No changes to resource URIs** — existing `profile://{slug}` resource already exposes profile details

---

## Deferred Ideas

- **Suggestion confirmation UI flow** — confirm/dismiss individual suggestions (SuggestionService has the methods but MCP doesn't need the full lifecycle yet)
- **Profile description field** — mentioned in Phase 04.1 context as future enhancement
- **Profile snapshots** — version history of profile configurations
- **Bulk triage via MCP** — listed as Phase 5+ candidate, not yet needed
- **Cross-source relatedness in MCP** — OpenAlex related_works exposure as discovery tool

---

*Phase: 07-mcp-surface-parity*
*Context generated: 2026-03-12 via automated codebase analysis*
