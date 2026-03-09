---
phase: 02-workflow-state
plan: 03
subsystem: workflow
tags: [sqlalchemy, asyncpg, pydantic, click, rich, async-service, tdd, delta-tracking, json-export, search-augmentation]

# Dependency graph
requires:
  - phase: 02-workflow-state
    plan: 01
    provides: "SavedQuery ORM model with JSONB params, watch columns; Pydantic schemas; slugify utility"
  - phase: 02-workflow-state
    plan: 02
    provides: "CollectionService (11 methods) and TriageService (6 methods) for CRUD and batch operations"
  - phase: 01-metadata-substrate
    provides: "SearchService, Paper ORM model, query builders, CLI patterns, config module"
provides:
  - "SavedQueryService with 6 async methods for query lifecycle (CRUD + run)"
  - "WatchService with 8 async methods for delta tracking (promote, check, check-all, pause/resume, reset, dashboard, demote)"
  - "WorkflowSearchService wrapping SearchService with triage state + collection context enrichment"
  - "ExportService with 6 methods (export, import, stats, reset, paper detail)"
  - "WorkflowSearchResult Pydantic model with triage_state and collection_slugs"
  - "CLI subgroups: collection (10 commands), triage (6 commands), query (8 commands), watch (6 commands), paper (1 command), workflow (4 commands)"
  - "Config extended with workflow soft limits and defaults"
  - "40 new integration tests (13 query + 11 watch + 6 search_augment + 10 export)"
affects: [03-enrichment, 04-mcp-surface]

# Tech tracking
tech-stack:
  added: []
  patterns: [checkpoint-plus-one-delta, search-result-post-process-enrichment, last-write-wins-import, cross-entity-insight-queries, lazy-workflow-service-import]

key-files:
  created:
    - src/arxiv_mcp/workflow/queries.py
    - src/arxiv_mcp/workflow/watches.py
    - src/arxiv_mcp/workflow/search_augment.py
    - src/arxiv_mcp/workflow/export.py
    - src/arxiv_mcp/workflow/cli.py
    - tests/test_workflow/test_queries.py
    - tests/test_workflow/test_watches.py
    - tests/test_workflow/test_search_augment.py
    - tests/test_workflow/test_export.py
  modified:
    - src/arxiv_mcp/models/paper.py
    - src/arxiv_mcp/search/cli.py
    - src/arxiv_mcp/cli.py
    - src/arxiv_mcp/config.py

key-decisions:
  - "Checkpoint+1 delta: check_watch uses checkpoint_date + 1 day as date_from (seen through checkpoint, want newer)"
  - "Post-process enrichment: WorkflowSearchService wraps SearchService with 2-query batch (no N+1, no Phase 1 modification)"
  - "Last-write-wins for triage import: most recent updated_at takes precedence on conflict"
  - "Lazy workflow CLI import: main CLI uses try/except for workflow module (forward-compatible)"

patterns-established:
  - "Checkpoint+1 delta: checkpoint_date + timedelta(days=1) as date_from for strictly-newer results"
  - "Search result post-process enrichment: batch triage/collection queries after base search"
  - "Triage color coding in CLI: green=shortlisted, red=dismissed, blue=read, cyan=cite-later, dim=unseen/archived"
  - "Last-write-wins import: timestamp comparison for triage state conflict resolution"
  - "Cross-entity insight queries: SQL aggregation for orphaned shortlisted, stale watches, untriaged-in-collections"

requirements-completed: [WKFL-04, WKFL-05, WKFL-06, WKFL-07, WKFL-08]

# Metrics
duration: 11min
completed: 2026-03-09
---

# Phase 2 Plan 03: Saved Queries, Watches, Export, CLI Summary

**SavedQueryService (6 methods), WatchService (8 methods) with checkpoint delta tracking, WorkflowSearchService enrichment, ExportService (6 methods), and 35 CLI commands across 6 subgroups; 40 new tests, 164 total passing**

## Performance

- **Duration:** 11 min
- **Started:** 2026-03-09T23:45:02Z
- **Completed:** 2026-03-09T23:56:06Z
- **Tasks:** 4
- **Files modified:** 13 (9 created, 4 modified)

## Accomplishments
- SavedQueryService with full CRUD, JSONB param deserialization, run_count tracking, and graceful handling of stale filter references
- WatchService with delta tracking via checkpoint+1 date filtering, auto-advance, check-all, pause/resume, dashboard with pending estimate
- WorkflowSearchService wrapping Phase 1 SearchService with 2-query post-process enrichment (triage state + collection context per paper)
- ExportService with JSON export/import (skip + last-write-wins conflict resolution), cross-entity stats with insights, nuclear reset, paper detail view
- Complete CLI surface: 35 commands across 6 subgroups (collection, triage, query, watch, paper, workflow)
- Search CLI auto-upgraded to show triage state column with color coding
- Config extended with soft limits (collections: 100, queries: 50, watches: 20) and defaults

## Task Commits

Each task was committed atomically (TDD: test then feat):

1. **Task 1: SavedQueryService and WatchService** - `dcb65dc` (test/RED), `06a2106` (feat/GREEN)
2. **Task 2: WorkflowSearchService augmentation** - `d220abf` (test/RED), `f5b8610` (feat/GREEN)
3. **Task 3: ExportService, stats, paper detail, config** - `8f199fa` (feat)
4. **Task 4: CLI commands** - `0b3edbd` (feat)

## Files Created/Modified
- `src/arxiv_mcp/workflow/queries.py` - SavedQueryService: CRUD + run with JSONB param deserialization
- `src/arxiv_mcp/workflow/watches.py` - WatchService: delta tracking, checkpoint auto-advance, dashboard
- `src/arxiv_mcp/workflow/search_augment.py` - WorkflowSearchService: post-process triage + collection enrichment
- `src/arxiv_mcp/workflow/export.py` - ExportService: JSON export/import, stats with insights, reset, paper detail
- `src/arxiv_mcp/workflow/cli.py` - 35 Click commands across 6 subgroups
- `src/arxiv_mcp/models/paper.py` - Added WorkflowSearchResult model
- `src/arxiv_mcp/search/cli.py` - Auto-upgrade to WorkflowSearchService, triage column with colors
- `src/arxiv_mcp/cli.py` - Registered 6 workflow subgroups
- `src/arxiv_mcp/config.py` - Added workflow soft limits and defaults
- `tests/test_workflow/test_queries.py` - 13 integration tests for saved query lifecycle
- `tests/test_workflow/test_watches.py` - 11 integration tests for watch lifecycle
- `tests/test_workflow/test_search_augment.py` - 6 integration tests for search enrichment
- `tests/test_workflow/test_export.py` - 10 integration tests for export/import/stats/reset

## Decisions Made
- **Checkpoint+1 delta:** check_watch uses checkpoint_date + 1 day as date_from since build_search_query uses >= for date_from. Checkpoint represents "seen through this date," so +1 day gives strictly newer papers.
- **Post-process enrichment:** WorkflowSearchService wraps SearchService output with 2 batch queries (triage states + collection memberships) instead of modifying Phase 1's query builders. Follows "compose by wrapping, not by editing" pattern from research.
- **Last-write-wins triage import:** When importing triage states that already exist, the record with the most recent updated_at wins. This is the safest conflict resolution for state data.
- **Lazy workflow CLI import:** Main cli.py uses try/except to import workflow subgroups, maintaining backward compatibility if workflow modules are not yet available.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Watch delta returned checkpoint-date papers (off-by-one)**
- **Found during:** Task 1 (WatchService GREEN phase)
- **Issue:** check_watch set date_from=checkpoint_date, but build_search_query uses >= for date_from, causing papers ON the checkpoint date (already seen) to be returned
- **Fix:** Changed to checkpoint_date + timedelta(days=1) for strictly-newer delta
- **Files modified:** src/arxiv_mcp/workflow/watches.py
- **Verification:** test_check_watch_returns_delta passes with correct >-comparison
- **Committed in:** 06a2106 (Task 1 feat commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Critical correctness fix for delta semantics. No scope creep.

## Issues Encountered
None.

## User Setup Required
None - all services operate on existing schema from Plan 02-01 migration.

## Next Phase Readiness
- Phase 2 (Workflow State) is complete: all 3 plans delivered
- All services importable: SavedQueryService, WatchService, WorkflowSearchService, ExportService, CollectionService, TriageService
- Full test suite at 164 tests (all passing): 64 Phase 1 + 100 Phase 2
- CLI provides complete workflow surface for terminal usage
- Triage logs, saved query usage data, and collection membership source tracking are ready for Phase 3 interest modeling
- Export/import enables workflow state portability
- WorkflowSearchService pattern (post-process enrichment) extensible for Phase 3 ranking signals

## Self-Check: PASSED

All 13 files verified present. All 6 commit hashes verified in git log. Test files exceed minimum line counts.

---
*Phase: 02-workflow-state*
*Completed: 2026-03-09*
