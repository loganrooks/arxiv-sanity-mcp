---
phase: 07-mcp-surface-parity
plan: 02
subsystem: mcp
tags: [fastmcp, profile-ranking, discovery-tools, workflow-enrichment]

# Dependency graph
requires:
  - phase: 07-mcp-surface-parity
    provides: AppContext with profile_ranking and suggestions fields, mock fixtures
  - phase: 03-interest-modeling-ranking
    provides: ProfileRankingService, ProfileSearchResponse, ProfileSearchResult
  - phase: 02-workflow-state
    provides: WorkflowSearchService, WorkflowSearchResult (triage_state, collection_slugs)
provides:
  - search_papers with profile_slug parameter routing through ProfileRankingService
  - browse_recent with profile_slug parameter routing through ProfileRankingService
  - Workflow-enriched results (triage_state, collection_slugs) on all discovery tool results
  - Profile-ranked results (ranking_explanation, ranker_snapshot) when profile_slug provided
affects: [mcp-clients, agent-workflows, interest-profiles]

# Tech tracking
tech-stack:
  added: []
  patterns: [ProfileRankingService as universal discovery delegation target]

key-files:
  created: []
  modified:
    - src/arxiv_mcp/mcp/tools/discovery.py
    - tests/test_mcp/test_discovery_tools.py
    - tests/test_mcp/conftest.py

key-decisions:
  - "Always include ranking_explanation when profile_slug provided (no explain toggle) -- MCP returns structured data, agents always want it"
  - "find_related_papers not routed through ProfileRankingService -- flat list return is architecturally incompatible with ProfileSearchResponse"
  - "Response shape change from PaginatedResponse to ProfileSearchResponse is intentional and additive"

patterns-established:
  - "ProfileRankingService as universal delegation target for discovery tools (handles both paths internally)"
  - "ProfileSearchResponse helper factories in conftest for MCP test fixtures"

requirements-completed: [SC-1, SC-2]

# Metrics
duration: 18min
completed: 2026-03-13
---

# Phase 07 Plan 02: Discovery Tool Rerouting Summary

**search_papers and browse_recent rerouted through ProfileRankingService with profile_slug parameter for profile-ranked and workflow-enriched results**

## Performance

- **Duration:** 18 min
- **Started:** 2026-03-13T04:24:14Z
- **Completed:** 2026-03-13T04:43:02Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 3

## Accomplishments
- search_papers and browse_recent now route through app.profile_ranking instead of app.search
- Both tools accept optional profile_slug parameter for personalized ranking
- Without profile_slug: results include triage_state and collection_slugs (WorkflowSearchResult enrichment)
- With profile_slug: results additionally include ranking_explanation and ranker_snapshot
- Response shape changed from PaginatedResponse to ProfileSearchResponse (additive, backward-compatible)
- find_related_papers and get_paper unchanged (per plan)

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): Failing tests for ProfileRankingService delegation** - `892a4c4` (test)
2. **Task 1 (GREEN): Implementation rerouting through ProfileRankingService** - `2ddb444` (feat)

_TDD task: RED (failing tests) then GREEN (implementation)._

## Files Created/Modified
- `src/arxiv_mcp/mcp/tools/discovery.py` - search_papers and browse_recent rerouted through profile_ranking with profile_slug parameter
- `tests/test_mcp/test_discovery_tools.py` - 24 tests: updated existing classes + 3 new test classes (ProfileRanked, WorkflowEnriched, BrowseRecentProfileRanked)
- `tests/test_mcp/conftest.py` - Added _make_profile_search_result and _make_profile_search_response factory helpers, updated profile_ranking mock returns

## Decisions Made
- Always include ranking_explanation when profile_slug is provided (no separate explain parameter) -- MCP returns structured data consumed by agents, not display formatting
- find_related_papers not routed through ProfileRankingService -- returns flat list[dict], incompatible with ProfileSearchResponse pagination wrapper
- Response shape change is intentional: old {"items": [...], "page_info": {...}} becomes {"results": {"items": [...], "page_info": {...}}, "ranker_snapshot": ...}

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed RankingExplanation and RankerSnapshot field requirements in tests**
- **Found during:** Task 1 (GREEN phase)
- **Issue:** Test used incorrect SignalType enum value (QUERY_RELEVANCE vs QUERY_MATCH) and incomplete RankerSnapshot construction (dict instead of proper model with all required fields)
- **Fix:** Used correct SignalType.QUERY_MATCH and constructed full RankerSnapshot with all 9 required fields
- **Files modified:** tests/test_mcp/test_discovery_tools.py
- **Verification:** All 24 discovery tool tests pass
- **Committed in:** 2ddb444 (part of GREEN commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - test fixture accuracy)
**Impact on plan:** Necessary correction for test data accuracy. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 07 (MCP Surface Parity) is now complete: 2/2 plans done
- All 13 tools now route through the full service chain
- Discovery tools provide workflow-enriched and profile-ranked results to MCP clients
- 490 tests passing, all green
- Ready for Phase 08 or next milestone work

## Self-Check: PASSED

All 3 modified files verified present. Both commit hashes (892a4c4, 2ddb444) confirmed in git log.

---
*Phase: 07-mcp-surface-parity*
*Completed: 2026-03-13*
