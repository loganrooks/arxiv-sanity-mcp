---
phase: 05-mcp-validation-iteration
plan: 01
subsystem: scripts
tags: [click, json, import, triage, interest-profile, asyncio, idempotent]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: ArxivAPIClient.fetch_paper, map_to_paper, Paper ORM, pg_insert upsert
  - phase: 02-workflow-state
    provides: TriageService.mark_triage for setting paper triage states
  - phase: 03-interest-modeling-ranking
    provides: ProfileService.create_profile, add_signal for tension vocabulary
provides:
  - Idempotent import script for arxiv-scan pipeline data (150 + 7 papers)
  - CLI command `arxiv-mcp import scan --data-dir`
  - Pure data-loading functions testable without DB
  - Tension vocabulary as 10 followed_author signals
affects: [05-02-PLAN, 05-03-PLAN]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Service composition pattern: import script orchestrates existing services (ArxivAPIClient, TriageService, ProfileService) rather than hand-rolling DB operations"
    - "Pure/impure separation: data-loading functions are pure and testable; orchestration is async and composes services"
    - "Rich progress bar for long-running CLI operations"

key-files:
  created:
    - src/arxiv_mcp/scripts/__init__.py
    - src/arxiv_mcp/scripts/import_arxiv_scan.py
    - tests/test_mcp/test_import.py
  modified:
    - src/arxiv_mcp/cli.py

key-decisions:
  - "Used followed_author signal type for tension vocabulary (tensions map to topical interest areas)"
  - "Paper-index-data.json value scores for triage mapping, NOT normalized_holistic from final-selection.json"
  - "Excluded-audit papers default to 'seen' triage state (not in paper-index-data)"
  - "ON CONFLICT DO NOTHING for paper upsert idempotency"
  - "Profile creation raises ValueError on re-run (caught and logged, not error)"

patterns-established:
  - "Import scripts compose existing services via DI (engine, session_factory, service instances)"
  - "Pure data-loading functions separated from async orchestration for testability"

requirements-completed: [MCPV-01]

# Metrics
duration: 5min
completed: 2026-03-12
---

# Phase 05 Plan 01: Import Script Summary

**Idempotent arxiv-scan import script composing existing services: 150+7 papers, value-score triage mapping, 10-tension interest profile via CLI command**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-12T06:24:41Z
- **Completed:** 2026-03-12T06:29:41Z
- **Tasks:** 1 (TDD: RED + GREEN)
- **Files modified:** 4

## Accomplishments
- Pure data-loading functions for all three pipeline JSON files (final-selection, excluded-audit, paper-index-data)
- Score-to-triage mapping: shortlisted >= 7, seen < 7 (tested exhaustively for values 1-10)
- 10 tension vocabulary signals from evaluation-guidelines.md with philosopher references
- Async import orchestration composing ArxivAPIClient, TriageService, ProfileService
- CLI command `arxiv-mcp import scan --data-dir` registered with Rich progress bars
- 24 unit tests covering all pure functions

## Task Commits

Each task was committed atomically:

1. **Task 1 RED: Import test scaffolding** - `835e008` (test)
2. **Task 1 GREEN: Import script implementation** - `049180d` (feat)

_TDD task: tests written first, then implementation to make them pass._

## Files Created/Modified
- `src/arxiv_mcp/scripts/__init__.py` - Package init for one-time operational scripts
- `src/arxiv_mcp/scripts/import_arxiv_scan.py` - Import script with pure data-loading functions, async orchestration, and Click CLI command
- `tests/test_mcp/test_import.py` - 24 unit tests for data parsing, score mapping, tension signals, and overlap checking
- `src/arxiv_mcp/cli.py` - Added import subgroup registration (lazy import pattern)

## Decisions Made
- Used `followed_author` signal type for tension vocabulary categories (tensions map to topical interest areas that function like followed topics in the interest model)
- Paper-index-data.json `value` scores drive triage mapping (not `normalized_holistic` from final-selection.json), as specified in plan
- Excluded-audit papers (7 false negatives) default to "seen" triage state since they lack paper-index entries
- ON CONFLICT DO NOTHING for paper upsert ensures idempotency on re-runs
- Profile creation uses try/except ValueError for idempotent re-runs (profile slug collision caught gracefully)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
- Pre-existing DB fixture issues in integration tests (`test_enrichment/test_models.py`, `test_search/test_pagination.py`, etc.) cause UniqueViolationError on table re-creation. Not caused by Phase 05 changes. Logged to `deferred-items.md`.

## User Setup Required

None - no external service configuration required. Import script uses existing database and arXiv API settings.

## Next Phase Readiness
- Import script ready to run: `arxiv-mcp import scan` (requires PostgreSQL with schema and arXiv API access)
- Database will have 157 papers with triage states and interest profile after import
- Ready for Plan 02 (MCP prompt implementation + validation session)

## Self-Check: PASSED

All files exist. All commits verified.

---
*Phase: 05-mcp-validation-iteration*
*Completed: 2026-03-12*
