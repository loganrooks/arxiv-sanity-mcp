---
phase: 03-interest-modeling-ranking
plan: 03
subsystem: interest
tags: [suggestions, cli, click, rich, ranking-display, provenance, tdd]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: Paper ORM model for seed paper FK targets; SearchService for search chain
  - phase: 02-workflow-state
    provides: TriageState, SavedQuery ORM models for suggestion sources; WorkflowSearchService for profile ranking chain
  - phase: 03-interest-modeling-ranking
    plan: 01
    provides: ProfileService CRUD and signal management; InterestProfile/InterestSignal ORM models
  - phase: 03-interest-modeling-ranking
    plan: 02
    provides: RankingPipeline, ProfileRankingService, RankerSnapshot for CLI integration
provides:
  - SuggestionService for generating, confirming, and dismissing profile suggestions from workflow activity
  - Profile CLI subgroup with 19 commands for CRUD, signal management, and suggestion workflow
  - Extended search CLI with --profile and --explain flags for profile-ranked results
  - Ranking explanation inline display with score bar visualization
affects: [04-enrichment-adapters, 06-mcp-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [suggestion-from-workflow-activity, confirm-dismiss-lifecycle, cli-profile-signal-management, profile-ranked-search-display]

key-files:
  created:
    - src/arxiv_mcp/interest/suggestions.py
    - src/arxiv_mcp/interest/cli.py
    - tests/test_interest/test_suggestions.py
  modified:
    - src/arxiv_mcp/search/cli.py
    - src/arxiv_mcp/cli.py

key-decisions:
  - "Suggestion threshold: 3+ shortlisted/cite-later papers by same author to trigger followed_author suggestion"
  - "Suggestion threshold: run_count >= 3 for saved query suggestions"
  - "Existing active, pending, and dismissed signals all excluded from suggestion generation (not just active)"
  - "CLI signal IDs use type:value format for confirm/dismiss commands (e.g., seed_paper:2301.00001)"
  - "Profile-ranked search displays results inline with ranking explanation, not in table format, for richer detail"

patterns-established:
  - "Suggestion from workflow: mine triage states and query run counts for profile signal candidates"
  - "Confirm/dismiss lifecycle: pending -> active (confirmed) or dismissed; dismissed excluded from regeneration"
  - "CLI profile subgroup: 19 commands covering full profile lifecycle, all 4 signal types, and suggestion workflow"
  - "Profile-ranked CLI display: per-result ranking explanation with score bar visualization"

requirements-completed: [INTR-06, RANK-01, RANK-02, RANK-03]

# Metrics
duration: 8min
completed: 2026-03-10
---

# Phase 3 Plan 03: Suggestions & CLI Summary

**SuggestionService generating candidates from triage/query/author workflow activity, 19-command profile CLI with provenance-aware signal display, and profile-ranked search with inline ranking explanations**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-10T01:14:47Z
- **Completed:** 2026-03-10T01:22:47Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- SuggestionService generates seed paper, author, and query suggestions from workflow activity with human-readable reasons and scores
- Full confirm/dismiss lifecycle: pending signals transition to active or dismissed; dismissed signals excluded from future generation
- Profile CLI with 19 commands: create, list, show, delete, rename, archive, unarchive, add-seed, remove-seed, add-query, remove-query, follow, unfollow, add-negative, remove-negative, signals, suggest, confirm, dismiss
- Search and browse commands extended with --profile flag for profile-ranked results and --explain flag for full ranker snapshot display

## Task Commits

Each task was committed atomically:

1. **Task 1: SuggestionService with generation, confirm, and dismiss (TDD)**
   - RED: `78fffbf` (test) - 15 failing tests across 7 test classes
   - GREEN: `d1ac9ec` (feat) - SuggestionService implementation passing all 15 tests

2. **Task 2: Profile CLI subgroup and search CLI integration** - `340db77` (feat)

## Files Created/Modified
- `src/arxiv_mcp/interest/suggestions.py` - SuggestionService with generate, confirm, dismiss, bulk confirm
- `src/arxiv_mcp/interest/cli.py` - 19-command Click subgroup for profile management
- `tests/test_interest/test_suggestions.py` - 15 integration tests across 7 test classes
- `src/arxiv_mcp/search/cli.py` - Extended search query/browse with --profile and --explain flags
- `src/arxiv_mcp/cli.py` - Registered profile_group with lazy import

## Decisions Made
- Suggestion threshold of 3 for both author frequency (3+ shortlisted/cite-later papers) and query run count (>= 3) -- balances signal strength vs. noise
- All signal statuses (active, pending, dismissed) excluded from suggestion generation -- prevents re-suggesting dismissed candidates and duplicating pending/active signals
- CLI signal identifiers use type:value format (e.g., `seed_paper:2301.00001`) for confirm/dismiss -- avoids numeric IDs that change between sessions
- Profile-ranked search results displayed inline (not table) with per-result ranking explanation -- tables cannot accommodate variable-height signal breakdowns
- Score bar visualization using `=` and `-` characters for signal breakdown -- provides quick visual comparison of signal contributions

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 3 is now complete: interest profiles, ranking pipeline, and suggestion/CLI surface all operational
- 87 interest tests (42 profile + 30 ranking + 15 suggestion) provide coverage for all Phase 3 features
- ProfileRankingService and CLI are ready for Phase 4 enrichment signals (new SignalType entries plug into existing pipeline)
- Profile CLI ready for MCP tool wrapping in Phase 6
- All 251 tests green

## Self-Check: PASSED

All 5 created/modified files verified present. All 3 task commits (78fffbf, d1ac9ec, 340db77) verified in git log.

---
*Phase: 03-interest-modeling-ranking*
*Completed: 2026-03-10*
