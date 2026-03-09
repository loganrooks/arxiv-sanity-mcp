---
phase: 02-workflow-state
plan: 02
subsystem: workflow
tags: [sqlalchemy, asyncpg, pydantic, postgresql, async-service, tdd, batch-triage, dry-run, audit-trail]

# Dependency graph
requires:
  - phase: 02-workflow-state
    plan: 01
    provides: "Collection, CollectionPaper, TriageState, TriageLog ORM models; Pydantic schemas; slugify utility"
provides:
  - "CollectionService with 11 async methods for full collection lifecycle"
  - "TriageService with 6 async methods for triage lifecycle (mark, get, list, batch, batch_by_query, log)"
  - "CollectionPaperView Pydantic model for collection paper display with triage state"
  - "23 integration tests for collection CRUD, membership, merge, archive, reverse lookup"
  - "18 integration tests for triage mark, list, batch (ID + query), log"
affects: [02-03-saved-query-service, 03-enrichment, 04-mcp-surface]

# Tech tracking
tech-stack:
  added: []
  patterns: [service-layer-with-session-factory-di, subquery-paper-count, left-join-triage-display, absence-means-unseen-queries, query-based-batch-triage-with-dry-run, chunk-processing-for-large-batches]

key-files:
  created:
    - src/arxiv_mcp/workflow/collections.py
    - src/arxiv_mcp/workflow/triage.py
    - tests/test_workflow/test_collections.py
    - tests/test_workflow/test_triage.py

key-decisions:
  - "CollectionPaperView as Pydantic BaseModel (not plain class) for PaginatedResponse generic compatibility"
  - "Query-based batch triage uses build_search_query with large page_size (10000) instead of removing pagination"
  - "Batch triage processes chunks of 500 papers per transaction for memory safety"

patterns-established:
  - "Service layer pattern: session_factory + settings DI (consistent with SearchService)"
  - "Subquery paper count: outerjoin with grouped count subquery avoids N+1"
  - "LEFT JOIN triage display: case(TriageState.state IS NULL -> 'unseen') for collection paper listings"
  - "Absence-means-unseen queries: LEFT JOIN + IS NULL for listing unseen papers"
  - "Dry-run pattern: same query resolution, preview vs execute based on boolean flag"

requirements-completed: [WKFL-01, WKFL-02, WKFL-03, WKFL-08]

# Metrics
duration: 6min
completed: 2026-03-09
---

# Phase 2 Plan 02: Collection & Triage Services Summary

**CollectionService (11 methods) and TriageService (6 methods) with full CRUD, batch operations, query-based dry-run triage, and audit trail; 41 integration tests passing**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-09T23:36:36Z
- **Completed:** 2026-03-09T23:42:25Z
- **Tasks:** 2
- **Files modified:** 4 (4 created)

## Accomplishments
- CollectionService with CRUD, membership (add/remove/bulk), merge, archive/unarchive, reverse lookup, and show with triage state display
- TriageService with mark, get_state, list_by_state (including unseen via LEFT JOIN), batch triage (ID-based), query-based batch triage with dry-run preview, and audit log
- 41 integration tests (23 collection + 18 triage) all passing against PostgreSQL
- Both services follow SearchService pattern: async_sessionmaker + Settings dependency injection

## Task Commits

Each task was committed atomically (TDD: test then feat):

1. **Task 1: CollectionService** - `9bad2f8` (test/RED), `f2d1179` (feat/GREEN)
2. **Task 2: TriageService** - `eda7491` (test/RED), `ed41e0d` (feat/GREEN)

## Files Created/Modified
- `src/arxiv_mcp/workflow/collections.py` - CollectionService with 11 async methods for collection lifecycle
- `src/arxiv_mcp/workflow/triage.py` - TriageService with 6 async methods for triage lifecycle
- `tests/test_workflow/test_collections.py` - 23 integration tests for collection operations
- `tests/test_workflow/test_triage.py` - 18 integration tests for triage operations

## Decisions Made
- **CollectionPaperView as Pydantic BaseModel:** Plain class failed with PaginatedResponse[T] generic because Pydantic needs BaseModel for schema generation. Used BaseModel instead.
- **Large page_size for query-based batch:** Used build_search_query with page_size=10000 rather than removing pagination entirely. Practical ceiling for batch operations.
- **Chunk processing at 500:** Query-based batch triage processes matching papers in chunks of 500 to avoid oversized transactions (per research pitfall 3).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] CollectionPaperView needed Pydantic BaseModel**
- **Found during:** Task 1 (CollectionService GREEN phase)
- **Issue:** CollectionPaperView was a plain Python class, but PaginatedResponse[CollectionPaperView] requires a Pydantic model for schema generation
- **Fix:** Changed CollectionPaperView from plain class to Pydantic BaseModel with typed fields
- **Files modified:** src/arxiv_mcp/workflow/collections.py
- **Verification:** All 23 collection tests pass
- **Committed in:** f2d1179 (Task 1 feat commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor type system fix. No scope creep.

## Issues Encountered
None.

## User Setup Required
None - services operate on existing schema from Plan 02-01 migration.

## Next Phase Readiness
- CollectionService and TriageService ready for CLI integration (Plan 02-03 or Phase 4 MCP surface)
- Both services importable: `from arxiv_mcp.workflow.collections import CollectionService` and `from arxiv_mcp.workflow.triage import TriageService`
- Full test suite at 124 tests (all passing): 83 existing + 23 collection + 18 triage
- Triage audit trail data ready for Phase 3 interest modeling signals

## Self-Check: PASSED

All 4 files verified present. All 4 commit hashes verified in git log. Test files exceed 100-line minimum (272 and 238 lines).

---
*Phase: 02-workflow-state*
*Completed: 2026-03-09*
