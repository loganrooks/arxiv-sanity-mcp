---
phase: 02-workflow-state
plan: 01
subsystem: database
tags: [sqlalchemy, asyncpg, alembic, pydantic, postgresql, check-constraint, jsonb, association-object]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: "Paper ORM model with arxiv_id PK, Base declarative class, Alembic migration 001"
provides:
  - "Collection, CollectionPaper, TriageState, TriageLog, SavedQuery ORM models"
  - "12 Pydantic schemas for workflow API responses"
  - "Alembic migration 002 creating 5 workflow tables"
  - "slugify utility function for name-to-slug conversion"
  - "Workflow test infrastructure with conftest fixtures and sample data factories"
affects: [02-02-collection-service, 02-03-triage-service, 02-04-saved-query-service]

# Tech tracking
tech-stack:
  added: []
  patterns: [association-object-pattern, absence-means-unseen-triage, jsonb-saved-query-params, check-constraint-enum, watch-columns-on-saved-query]

key-files:
  created:
    - src/arxiv_mcp/models/workflow.py
    - src/arxiv_mcp/workflow/__init__.py
    - src/arxiv_mcp/workflow/util.py
    - alembic/versions/002_workflow_tables.py
    - tests/test_workflow/__init__.py
    - tests/test_workflow/conftest.py
    - tests/test_workflow/test_models.py
  modified:
    - src/arxiv_mcp/db/models.py

key-decisions:
  - "All 5 workflow ORM models in single db/models.py file (shared Base, string-based forward references)"
  - "TriageState uses VARCHAR + CHECK constraint (not native ENUM) for migration simplicity"
  - "SavedQuery params stored as JSONB for schema-free evolution"
  - "Watch columns on SavedQuery table (not separate table) per CONTEXT.md decision"
  - "Absence-means-unseen pattern: no row in triage_states = unseen state"

patterns-established:
  - "Association object pattern: CollectionPaper with source/added_at provenance columns"
  - "CHECK constraint for enum-like validation: ck_triage_state_valid"
  - "Watch as extension of SavedQuery: is_watch, cadence_hint, checkpoint_date, last_checked_at, is_paused"
  - "slugify utility: re.sub-based slug generation without external dependency"
  - "Workflow test conftest: sample_collection_data, sample_triage_data, sample_saved_query_data factories"

requirements-completed: [WKFL-01, WKFL-02, WKFL-03, WKFL-04, WKFL-06]

# Metrics
duration: 4min
completed: 2026-03-09
---

# Phase 2 Plan 01: Workflow Schema Foundation Summary

**5 workflow ORM models with CHECK constraints, JSONB params, and association object pattern; 12 Pydantic schemas; Alembic migration 002; 19 passing tests**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-09T23:29:16Z
- **Completed:** 2026-03-09T23:33:34Z
- **Tasks:** 2
- **Files modified:** 8 (7 created, 1 modified)

## Accomplishments
- 5 ORM models (Collection, CollectionPaper, TriageState, TriageLog, SavedQuery) with correct FK relationships to Paper.arxiv_id
- 12 Pydantic schemas for workflow API responses with from_attributes ORM bridge
- Alembic migration 002 creating all 5 tables with CHECK constraints, indexes, and FK cascades
- Test infrastructure with conftest fixtures, sample data factories, and 19 passing tests
- slugify utility function for name-to-slug conversion

## Task Commits

Each task was committed atomically:

1. **Task 1: ORM models and Pydantic schemas** - `7a4e65f` (test/RED), `483d352` (feat/GREEN)
2. **Task 2: Alembic migration 002** - `bf5c848` (feat)

## Files Created/Modified
- `src/arxiv_mcp/db/models.py` - Added Collection, CollectionPaper, TriageState, TriageLog, SavedQuery ORM models
- `src/arxiv_mcp/models/workflow.py` - 12 Pydantic schemas (CollectionSummary, CollectionDetail, TriageStateResponse, etc.)
- `src/arxiv_mcp/workflow/__init__.py` - Package init
- `src/arxiv_mcp/workflow/util.py` - slugify function
- `alembic/versions/002_workflow_tables.py` - Migration creating 5 workflow tables
- `tests/test_workflow/__init__.py` - Test package init
- `tests/test_workflow/conftest.py` - Fixtures with sample data factories and 5-paper FK targets
- `tests/test_workflow/test_models.py` - 19 tests covering all ORM models, Pydantic schemas, and slugify

## Decisions Made
- **All models in db/models.py:** Kept all ORM models in a single file per Phase 1 pattern to share Base and avoid circular imports. String-based forward references in relationship() calls.
- **CHECK constraint over native ENUM:** Used VARCHAR(20) + CHECK constraint for triage state validation. Native ENUM ALTER TYPE ADD VALUE is non-transactional, making rollback difficult.
- **JSONB for saved query params:** Stored search parameters as JSONB column so the parameter schema can evolve across phases without migrations.
- **Watch columns on SavedQuery:** Per CONTEXT.md locked decision "Watch = saved query + checkpoint metadata (extends, not separate entity)."
- **Absence-means-unseen:** No triage_state row means "unseen." Avoids materializing millions of default rows.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - migration 002 applies cleanly on top of existing schema.

## Next Phase Readiness
- All 5 ORM models ready for service layer implementation (Plans 02, 03)
- Pydantic schemas ready for API/CLI response shaping
- Test infrastructure with sample data factories ready for service-level tests
- All 83 tests passing (19 new + 64 existing) as regression suite

## Self-Check: PASSED

All 8 files verified present. All 3 commit hashes verified in git log.

---
*Phase: 02-workflow-state*
*Completed: 2026-03-09*
