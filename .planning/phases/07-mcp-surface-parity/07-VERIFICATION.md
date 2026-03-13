---
phase: 07-mcp-surface-parity
verified: 2026-03-13T05:30:00Z
status: passed
score: 5/5 must-haves verified
gaps: []
human_verification: []
---

# Phase 7: MCP Surface Parity Verification Report

**Phase Goal:** MCP tools expose the same capabilities available in the CLI — profile-ranked search, workflow-enriched search results, profile creation, and signal suggestions — so agents using MCP have full parity with CLI users.
**Verified:** 2026-03-13T05:30:00Z
**Status:** passed
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths

Phase 7 success criteria (SC-1 through SC-5) are drawn from ROADMAP.md Phase 7 success criteria. These are internal roadmap labels, not REQUIREMENTS.md IDs. See Requirements Coverage section for full accounting.

| #  | Truth | Status | Evidence |
|----|-------|--------|----------|
| 1  | An MCP client can search papers with profile_slug and receive profile-ranked results with RankingExplanation on each result | VERIFIED | `search_papers` accepts `profile_slug`, routes to `app.profile_ranking.search_papers()`, returns `ProfileSearchResponse` with `ranking_explanation` per item; 3 test classes confirm |
| 2  | MCP search_papers and browse_recent return WorkflowSearchResult-enriched results (triage_state, collection_slugs) even without profile_slug | VERIFIED | Both tools route through `ProfileRankingService` which wraps `WorkflowSearchService`; `triage_state` and `collection_slugs` present on all items; `TestSearchPapersWorkflowEnriched` confirms |
| 3  | An MCP client can create an interest profile via create_profile tool and receive a ProfileSummary dict | VERIFIED | `create_profile` tool in `interest.py` wraps `app.profiles.create_profile()`, returns `result.model_dump(mode="json")`; `TestCreateProfile` (3 tests) confirms happy path, negative_weight forwarding, error handling |
| 4  | An MCP client can generate signal suggestions via suggest_signals tool with optional auto_add | VERIFIED | `suggest_signals` tool wraps `app.suggestions.generate_suggestions()` and `app.suggestions.add_suggestions_to_profile()`; `TestSuggestSignals` (4 tests) confirms both paths |
| 5  | AppContext includes ProfileRankingService and SuggestionService fields and all 13 tools register | VERIFIED | `AppContext` dataclass has `profile_ranking: ProfileRankingService` and `suggestions: SuggestionService` fields; `app_lifespan()` creates and yields both; `mcp._tool_manager._tools` shows 13 tools registered |

**Score:** 5/5 truths verified

---

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/mcp/server.py` | AppContext with profile_ranking + suggestions fields; app_lifespan service chain | VERIFIED | Lines 47-48 declare both fields; lines 69-71 initialize `workflow_search`, `profile_ranking`, `suggestions`; both yielded in AppContext |
| `src/arxiv_mcp/mcp/tools/interest.py` | create_profile and suggest_signals tool functions | VERIFIED | Lines 90-141 contain both `@mcp.tool()` functions; substantive implementations with error handling |
| `src/arxiv_mcp/mcp/tools/discovery.py` | search_papers and browse_recent with profile_slug, routed through ProfileRankingService | VERIFIED | Lines 34 and 58-72 (search_papers), lines 82 and 102-111 (browse_recent); both accept `profile_slug`, both call `app.profile_ranking.*` |
| `tests/test_mcp/conftest.py` | mock_app_context with profile_ranking and suggestions mocks | VERIFIED | Lines 117-126 add `ctx.profile_ranking` (with `search_papers` and `browse_recent` mocks returning `ProfileSearchResponse`) and `ctx.suggestions`; factory helpers `_make_profile_search_result` and `_make_profile_search_response` added |
| `tests/test_mcp/test_interest_tools.py` | Tests for create_profile and suggest_signals | VERIFIED | 9 tests: `TestAppContextSpec` (2), `TestCreateProfile` (3), `TestSuggestSignals` (4); all pass |
| `tests/test_mcp/test_discovery_tools.py` | Tests for profile-ranked search, workflow-enriched results, backward compatibility | VERIFIED | 24 tests across 6 classes; `TestSearchPapersProfileRanked`, `TestSearchPapersWorkflowEnriched`, `TestBrowseRecentProfileRanked` are new; all pass |

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `mcp/tools/interest.py` | `AppContext.profiles` | `app.profiles.create_profile()` | WIRED | Line 103: `result = await app.profiles.create_profile(name, negative_weight=negative_weight)` |
| `mcp/tools/interest.py` | `AppContext.suggestions` | `app.suggestions.generate_suggestions()` | WIRED | Line 127: `candidates = await app.suggestions.generate_suggestions(profile_slug)` |
| `mcp/tools/interest.py` | `AppContext.suggestions` | `app.suggestions.add_suggestions_to_profile()` | WIRED | Line 133: `added = await app.suggestions.add_suggestions_to_profile(profile_slug, candidates)` |
| `mcp/tools/discovery.py` | `AppContext.profile_ranking` | `app.profile_ranking.search_papers()` | WIRED | Line 59: `result = await app.profile_ranking.search_papers(profile_slug=profile_slug, ...)` |
| `mcp/tools/discovery.py` | `AppContext.profile_ranking` | `app.profile_ranking.browse_recent()` | WIRED | Line 102: `result = await app.profile_ranking.browse_recent(profile_slug=profile_slug, ...)` |
| `mcp/server.py` | `ProfileRankingService` | import + initialization in app_lifespan | WIRED | Line 22 imports; line 47 declares field; line 70 initializes with `WorkflowSearchService` as intermediate |
| `mcp/server.py` | `SuggestionService` | import + initialization in app_lifespan | WIRED | Line 23 imports; line 48 declares field; line 71 initializes with `profiles` service |

---

### Requirements Coverage

Phase 7 plans use `SC-N` identifiers referencing ROADMAP.md success criteria, not REQUIREMENTS.md requirement IDs. REQUIREMENTS.md contains no Phase 7 rows in the traceability table, and no v1 requirements are labeled SC-1 through SC-5. This is an intentional documentation pattern: Phase 7 is a gap-closure phase that does not introduce new v1 requirements — it fulfills the gap-closure mandate described in the ROADMAP.

The functional content of SC-1 through SC-5 maps onto existing requirements as follows:

| SC ID | Source Plan(s) | Content | Related REQUIREMENTS.md IDs | Status |
|-------|---------------|---------|----------------------------|--------|
| SC-1 | 07-02 | MCP search_papers with profile_slug returns profile-ranked results with RankingExplanation | MCP-01 (search_papers tool), RANK-01 (ranking explanations) | SATISFIED — implementation verified |
| SC-2 | 07-02 | MCP search_papers and browse_recent return triage_state and collection_slugs | MCP-01 (browse_recent tool), WKFL-03 (triage state) | SATISFIED — implementation verified |
| SC-3 | 07-01 | MCP create_profile tool | MCP-02 (workflow/interest tools), INTR-01 (create profile) | SATISFIED — implementation verified |
| SC-4 | 07-01 | MCP suggest_signals tool | MCP-02 (workflow/interest tools), INTR-06 (inspect signals) | SATISFIED — implementation verified |
| SC-5 | 07-01 | AppContext has ProfileRankingService and SuggestionService; all tools tested | MCP-02 (interest tools), MCP-07 (tool count discipline) | SATISFIED — 13 tools, both services in AppContext |

No REQUIREMENTS.md IDs are orphaned: all v1 requirements mapped to Phase 7 by plan frontmatter belong to gap-closure success criteria accounted for above.

---

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| — | — | — | — | No anti-patterns found |

Scan covered: `src/arxiv_mcp/mcp/server.py`, `src/arxiv_mcp/mcp/tools/interest.py`, `src/arxiv_mcp/mcp/tools/discovery.py`, `tests/test_mcp/conftest.py`, `tests/test_mcp/test_interest_tools.py`, `tests/test_mcp/test_discovery_tools.py`. No TODOs, FIXMEs, placeholder returns, empty handlers, or stub implementations found.

---

### Human Verification Required

None. All phase behaviors have automated verification. The VALIDATION.md notes "All phase behaviors have automated verification." The test suite (490 tests) covers all five success criteria programmatically.

---

### Commit Verification

All four commit hashes documented in SUMMARY.md files are confirmed present in git history:
- `900b822` — test(07-01): add failing tests for create_profile and suggest_signals tools
- `7f07942` — feat(07-01): expand AppContext and add create_profile + suggest_signals tools
- `892a4c4` — test(07-02): add failing tests for discovery tool ProfileRankingService delegation
- `2ddb444` — feat(07-02): reroute discovery tools through ProfileRankingService

---

### Test Suite Results

| Scope | Count | Result |
|-------|-------|--------|
| `tests/test_mcp/` (MCP suite) | 109 tests | 109 passed |
| `tests/test_mcp/test_interest_tools.py` | 9 tests | 9 passed |
| `tests/test_mcp/test_discovery_tools.py` | 33 tests | 33 passed |
| Full suite `tests/` | 490 tests | 490 passed |

No regressions introduced. SUMMARY.md reported 490 tests — confirmed.

---

### Tool Registration Verification

MCP server registers 13 tools (confirmed via `mcp._tool_manager._tools`):

`add_signal`, `add_to_collection`, `batch_add_signals`, `browse_recent`, `create_profile`, `create_watch`, `enrich_paper`, `find_related_papers`, `get_content_variant`, `get_paper`, `search_papers`, `suggest_signals`, `triage_paper`

New tools from Phase 7: `create_profile`, `suggest_signals` (SC-3, SC-4).
Enhanced tools from Phase 7: `search_papers`, `browse_recent` (SC-1, SC-2).

---

### Gap Summary

No gaps. All five success criteria from ROADMAP.md Phase 7 are fully achieved:

- SC-1 (profile-ranked search): `search_papers` accepts `profile_slug`, returns `ProfileSearchResponse` with `ranking_explanation` per item.
- SC-2 (workflow-enriched results): Both discovery tools route through `ProfileRankingService` → `WorkflowSearchService`; `triage_state` and `collection_slugs` appear on all results.
- SC-3 (create_profile tool): Thin wrapper around `ProfileService.create_profile()`; returns `ProfileSummary` dict; handles errors.
- SC-4 (suggest_signals tool): Wraps `SuggestionService`; supports `auto_add`; serializes `SuggestionCandidate` via `dataclasses.asdict()`.
- SC-5 (AppContext + tests): Both services are declared, initialized, and wired in server lifespan; 490 tests green.

The phase goal — full CLI/MCP parity for profile-ranked search, workflow-enriched results, profile creation, and signal suggestions — is achieved.

---

_Verified: 2026-03-13T05:30:00Z_
_Verifier: Claude (gsd-verifier)_
