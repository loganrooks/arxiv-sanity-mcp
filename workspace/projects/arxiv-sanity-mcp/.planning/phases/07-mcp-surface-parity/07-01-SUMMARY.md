---
phase: 07-mcp-surface-parity
plan: 01
subsystem: mcp
tags: [fastmcp, interest-profiles, suggestion-engine, dataclass-serialization]

# Dependency graph
requires:
  - phase: 03-interest-modeling-ranking
    provides: ProfileService, SuggestionService, ProfileRankingService
  - phase: 04.1-mcp-v1
    provides: AppContext dataclass, _get_app helper, tool registration pattern
provides:
  - AppContext with profile_ranking (ProfileRankingService) and suggestions (SuggestionService) fields
  - create_profile MCP tool for profile creation
  - suggest_signals MCP tool for suggestion generation with optional auto_add
  - WorkflowSearchService intermediate in app_lifespan service chain
affects: [07-02, mcp-tools, interest-profiles]

# Tech tracking
tech-stack:
  added: []
  patterns: [dataclasses.asdict for non-Pydantic serialization, service chain with intermediate]

key-files:
  created:
    - tests/test_mcp/test_interest_tools.py
  modified:
    - src/arxiv_mcp/mcp/server.py
    - src/arxiv_mcp/mcp/tools/interest.py
    - tests/test_mcp/conftest.py
    - tests/test_mcp/test_tool_names.py

key-decisions:
  - "WorkflowSearchService as intermediate service (not exposed on AppContext) -- only ProfileRankingService needs it"
  - "SuggestionCandidate serialized via dataclasses.asdict (not model_dump) since it is a dataclass not Pydantic"
  - "Tool count updated from 11 to 13 in test assertions"

patterns-established:
  - "dataclasses.asdict for serializing non-Pydantic dataclass types in MCP tools"
  - "Service chain with intermediate: SearchService -> WorkflowSearchService -> ProfileRankingService"

requirements-completed: [SC-3, SC-4, SC-5]

# Metrics
duration: 17min
completed: 2026-03-13
---

# Phase 07 Plan 01: AppContext + Interest Tools Summary

**AppContext expanded with ProfileRankingService and SuggestionService; create_profile and suggest_signals MCP tools added with TDD, 480 tests green**

## Performance

- **Duration:** 17 min
- **Started:** 2026-03-13T04:03:22Z
- **Completed:** 2026-03-13T04:20:20Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 5

## Accomplishments
- AppContext expanded with profile_ranking and suggestions fields, wired through service chain in app_lifespan
- create_profile tool wraps ProfileService.create_profile with error handling
- suggest_signals tool wraps SuggestionService with optional auto_add for bulk signal addition
- Full TDD cycle: 9 new tests covering happy paths, error handling, negative_weight forwarding, auto_add, and asdict serialization

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): Failing tests for create_profile + suggest_signals** - `900b822` (test)
2. **Task 1 (GREEN): Implementation passing all tests** - `7f07942` (feat)

_TDD task: RED (failing tests) then GREEN (implementation)._

## Files Created/Modified
- `tests/test_mcp/test_interest_tools.py` - 9 tests: AppContext spec, create_profile (3), suggest_signals (4)
- `src/arxiv_mcp/mcp/server.py` - AppContext + 2 fields, app_lifespan + 3 service instantiations
- `src/arxiv_mcp/mcp/tools/interest.py` - create_profile and suggest_signals tool functions
- `tests/test_mcp/conftest.py` - profile_ranking and suggestions mocks added to mock_app_context
- `tests/test_mcp/test_tool_names.py` - Tool count 11->13, tool name set expanded

## Decisions Made
- WorkflowSearchService created as intermediate service in app_lifespan (not exposed on AppContext) since only ProfileRankingService wraps it
- SuggestionCandidate serialized via dataclasses.asdict() since it is a dataclass, not a Pydantic model (plan explicitly flagged this)
- Tool count test updated from 11 to 13 as expected consequence of adding 2 new tools

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Updated tool count and tool name set in test_tool_names.py**
- **Found during:** Task 1 (GREEN phase, full regression test)
- **Issue:** test_tool_count_is_eleven asserted exactly 11 tools; adding 2 new tools broke the assertion
- **Fix:** Updated count from 11 to 13, added create_profile and suggest_signals to expected tool name set
- **Files modified:** tests/test_mcp/test_tool_names.py
- **Verification:** All 99 MCP tests pass
- **Committed in:** 7f07942 (part of GREEN commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 - test assertion update)
**Impact on plan:** Necessary correction for test assertions that guard tool registration completeness. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- AppContext now has all services needed for Plan 02 (discovery tools with profile-ranked search)
- profile_ranking and suggestions fields available for any MCP tool/resource to reference
- Total: 13 tools, 4 resources, 3 prompts

## Self-Check: PASSED

All 5 files verified present. Both commit hashes (900b822, 7f07942) confirmed in git log.

---
*Phase: 07-mcp-surface-parity*
*Completed: 2026-03-13*
