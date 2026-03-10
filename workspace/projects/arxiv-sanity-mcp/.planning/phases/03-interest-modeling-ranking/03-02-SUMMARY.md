---
phase: 03-interest-modeling-ranking
plan: 02
subsystem: ranking
tags: [ranking-pipeline, signal-scorers, pydantic, composable-ranking, inspectable-results]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: PaperSummary model with category_list and authors_text for scorer inputs
  - phase: 02-workflow-state
    provides: WorkflowSearchService wrapping SearchService for profile ranking to compose with
  - phase: 03-interest-modeling-ranking
    plan: 01
    provides: InterestProfile/InterestSignal ORM models and ProfileService for profile context loading
provides:
  - RankingPipeline with 5 signal scorers (query_match, category_overlap, recency, seed_relation, profile_match)
  - ProfileRankingService wrapping WorkflowSearchService with profile-based re-ranking
  - SignalType, SignalScore, RankingExplanation, RankerSnapshot Pydantic models
  - ProfileSearchResult extending WorkflowSearchResult with ranking_explanation field
  - ProfileSearchResponse wrapping PaginatedResponse + RankerSnapshot
  - ProfileContext dataclass for batch-loaded profile data
affects: [03-03-suggestions-cli, 04-enrichment-adapters, 06-mcp-integration]

# Tech tracking
tech-stack:
  added: []
  patterns: [composable-scorer-pipeline, over-fetch-re-rank, negative-soft-demotion, pydantic-ranking-types-in-models]

key-files:
  created:
    - src/arxiv_mcp/interest/ranking.py
    - src/arxiv_mcp/interest/search_augment.py
  modified:
    - src/arxiv_mcp/models/interest.py
    - src/arxiv_mcp/models/paper.py
    - tests/test_interest/test_ranking.py

key-decisions:
  - "Ranking types (SignalType, SignalScore, RankingExplanation, RankerSnapshot) as Pydantic BaseModels in models/interest.py to avoid circular imports with models/paper.py"
  - "ProfileContext as dataclass in ranking.py (internal to ranking, references PaperSummary)"
  - "ProfileSearchResponse defined in interest/search_augment.py to avoid circular import chain"
  - "Over-fetch multiplier of 3x for re-ranking compensation (page_size * 3 from base service)"
  - "Negative demotion uses multiplicative factor (1 - weight) on weighted_scores, never removes results"
  - "Test injection via _test_profile_context parameter for ProfileRankingService unit tests without DB"

patterns-established:
  - "Composable scorer pipeline: pure module-level scorer functions + pipeline class for dispatch/weights"
  - "Over-fetch re-rank: request N*3 from base service, re-rank, trim to N for accurate profile-ranked pagination"
  - "Negative soft demotion: multiply all weighted_scores by (1-weight) instead of filtering results"
  - "Test injection pattern: _test_* constructor parameter bypasses DB loading for unit tests"

requirements-completed: [RANK-01, RANK-02, RANK-03]

# Metrics
duration: 8min
completed: 2026-03-10
---

# Phase 3 Plan 02: Ranking Pipeline Summary

**Composable 5-signal ranking pipeline with ProfileRankingService wrapping WorkflowSearchService, inspectable RankingExplanation per result, and negative soft demotion**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-10T01:03:29Z
- **Completed:** 2026-03-10T01:11:53Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- RankingPipeline with 5 composable signal scorers (query_match, category_overlap, recency, seed_relation, profile_match) producing normalized scores in [0,1]
- ProfileRankingService wrapping WorkflowSearchService with over-fetch re-ranking strategy and batch profile context loading
- Every ranked result includes RankingExplanation with composite_score, signal_breakdown, and ranker_version for full inspectability
- 30 tests covering all scorers, edge cases (zero division, self-match exclusion, empty profiles), pipeline integration, and service composition

## Task Commits

Each task was committed atomically:

1. **Task 1: Signal scorers, RankingPipeline, and Pydantic types**
   - RED: `54541b2` (test) - Failing tests for all 5 scorers, pipeline, snapshot, and ProfileSearchResult
   - GREEN: `d79c2cf` (feat) - Implementation passing all 24 tests

2. **Task 2: ProfileRankingService wrapping WorkflowSearchService**
   - RED: `b54b605` (test) - Failing tests for ProfileRankingService with mock WorkflowSearchService
   - GREEN: `526ac5f` (feat) - Implementation passing all 6 integration tests

## Files Created/Modified
- `src/arxiv_mcp/interest/ranking.py` - 5 pure scorer functions, RankingPipeline, ProfileContext, DEFAULT_WEIGHTS
- `src/arxiv_mcp/interest/search_augment.py` - ProfileRankingService, ProfileSearchResponse, over-fetch re-ranking
- `src/arxiv_mcp/models/interest.py` - Added SignalType, SignalScore, RankingExplanation, RankerSnapshot Pydantic models
- `src/arxiv_mcp/models/paper.py` - Added ProfileSearchResult with ranking_explanation field
- `tests/test_interest/test_ranking.py` - 30 tests across 9 test classes

## Decisions Made
- Ranking types (SignalType, SignalScore, RankingExplanation, RankerSnapshot) defined as Pydantic BaseModels in models/interest.py rather than dataclasses in ranking.py -- avoids circular import between ranking.py (imports PaperSummary from paper.py) and paper.py (ProfileSearchResult needs RankingExplanation)
- ProfileContext kept as dataclass in ranking.py since it's internal to the ranking module and only consumed by scorers
- ProfileSearchResponse defined in interest/search_augment.py (not models/interest.py) to avoid the circular import chain between models/interest.py and models/paper.py
- Over-fetch multiplier set to 3x -- requests 3x the page_size from the base service before re-ranking, then trims results to the original page_size
- Negative demotion uses multiplicative factor (1.0 - negative_weight) applied to all weighted_scores, rather than filtering or zeroing results -- preserves soft demotion semantics per AGENTS.md exploration-first principle
- Test injection via `_test_profile_context` constructor parameter lets unit tests bypass DB loading while still exercising the full ranking path

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Moved ranking types to models/interest.py to break circular import**
- **Found during:** Task 1 (implementing ProfileSearchResult in paper.py)
- **Issue:** ranking.py imports PaperSummary from paper.py; paper.py needs RankingExplanation from ranking.py -- circular import
- **Fix:** Moved SignalType, SignalScore, RankingExplanation, RankerSnapshot from ranking.py to models/interest.py as Pydantic BaseModels; ranking.py re-exports them
- **Files modified:** src/arxiv_mcp/models/interest.py, src/arxiv_mcp/interest/ranking.py, src/arxiv_mcp/models/paper.py
- **Verification:** All 236 tests pass
- **Committed in:** d79c2cf (Task 1 commit)

**2. [Rule 3 - Blocking] Moved ProfileSearchResponse to search_augment.py**
- **Found during:** Task 1 (trying to define in models/interest.py)
- **Issue:** ProfileSearchResponse references PaginatedResponse[ProfileSearchResult], creating another circular import from models/interest.py to models/paper.py
- **Fix:** Defined ProfileSearchResponse in interest/search_augment.py alongside ProfileRankingService where it's produced
- **Files modified:** src/arxiv_mcp/models/interest.py, src/arxiv_mcp/interest/search_augment.py
- **Verification:** All tests pass, no circular imports
- **Committed in:** 526ac5f (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (both Rule 3 - blocking circular imports)
**Impact on plan:** Both fixes were necessary for correct module structure. Same types and APIs as planned, just different module locations. No scope creep.

## Issues Encountered
None beyond the circular import restructuring documented above.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- RankingPipeline ready for Plan 03 (CLI integration with --profile and --explain flags)
- ProfileRankingService provides the ranked search API that Plan 03 CLI commands will call
- RankerSnapshot enables --explain flag to show full ranker inputs for any result set
- Pipeline is composable -- Phase 4 enrichment signals (citations, FWCI) can plug in as new SignalType entries without restructuring
- All 236 tests green (30 new ranking tests + 42 existing interest tests + 164 other)

## Self-Check: PASSED

All 5 created/modified files verified present. All 4 task commits (54541b2, d79c2cf, b54b605, 526ac5f) verified in git log.

---
*Phase: 03-interest-modeling-ranking*
*Completed: 2026-03-10*
