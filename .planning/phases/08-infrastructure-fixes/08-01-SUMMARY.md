---
phase: 08-infrastructure-fixes
plan: 01
subsystem: testing, api
tags: [pytest, conftest, fixtures, docstring, import-isolation, content-package]

# Dependency graph
requires:
  - phase: 06-content-normalization
    provides: content package with models, adapters, html_fetcher, rights, service
  - phase: 04.1-mcp-v1
    provides: MCP tools including create_watch with docstring
provides:
  - Deduplicated conftest hierarchy (single source of truth for shared fixtures)
  - Corrected create_watch docstring referencing watch:// resource
  - Empty content/__init__.py preventing eager loading of heavy dependencies
  - Regression tests for docstring accuracy and import isolation
affects: [08-02, content-normalization, mcp-tools]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Import shared test fixtures from root conftest, keep domain-specific factories in module conftest"
    - "Subprocess-based import isolation testing for verifying lazy loading"
    - "Docstring assertion tests to prevent stale tool references"

key-files:
  created:
    - tests/test_mcp/test_docstrings.py
    - tests/test_content/test_import_isolation.py
  modified:
    - tests/test_workflow/conftest.py
    - tests/test_interest/conftest.py
    - tests/test_workflow/test_search_augment.py
    - tests/test_workflow/test_queries.py
    - tests/test_workflow/test_export.py
    - tests/test_workflow/test_watches.py
    - tests/test_interest/test_suggestions.py
    - src/arxiv_mcp/mcp/tools/workflow.py
    - src/arxiv_mcp/content/__init__.py

key-decisions:
  - "Shared fixtures (test_engine, test_session, TSVECTOR SQL, sample_paper_data) live only in root conftest; module conftest files import them"
  - "Domain-specific factories (sample_collection_data, sample_profile_data, etc.) stay in module conftest files"
  - "content/__init__.py stripped to docstring only (zero re-exports) per locked SC-4 decision"
  - "Subprocess-based import isolation test chosen over sys.modules check to avoid false passes from pre-loaded modules"

patterns-established:
  - "Conftest hierarchy: root conftest owns shared fixtures, module conftest imports shared + owns domain-specific"
  - "Docstring regression tests: assert tool docstrings reference correct MCP resources"
  - "Subprocess import isolation: verify lazy loading in clean interpreter"

requirements-completed: [SC-2, SC-3, SC-4]

# Metrics
duration: 51min
completed: 2026-03-13
---

# Phase 08 Plan 01: Test Fixture Consolidation and Code Fixes Summary

**Deduplicated test fixtures across conftest hierarchy, fixed create_watch docstring to reference watch:// resource, removed content package re-exports for lazy loading, added 3 regression tests (493 total passing)**

## Performance

- **Duration:** 51 min
- **Started:** 2026-03-13T20:37:37Z
- **Completed:** 2026-03-13T21:29:21Z
- **Tasks:** 2
- **Files modified:** 11

## Accomplishments
- Eliminated ~200 lines of duplicated test fixture code (TSVECTOR SQL, sample_paper_data, test_engine, test_session) from workflow and interest conftest files
- Rewired 5 consumer test files to import shared fixtures from tests.conftest while keeping domain-specific factories in module conftest
- Fixed create_watch docstring from referencing non-existent get_delta tool to referencing watch://{slug}/deltas resource
- Stripped content/__init__.py to docstring-only (zero imports, zero __all__) preventing httpx/bs4 eager loading
- Added 3 regression tests: 1 docstring assertion + 2 subprocess-based import isolation tests
- Full test suite: 493 tests passing

## Task Commits

Each task was committed atomically:

1. **Task 1: Consolidate conftest files and rewire all consumer imports** - `b21e126` (refactor)
2. **Task 2: Fix docstring, remove all content re-exports, add regression tests** - `e535b96` (fix)

## Files Created/Modified
- `tests/test_workflow/conftest.py` - Removed duplicated TSVECTOR SQL, sample_paper_data, test_engine, test_session; imports from root conftest
- `tests/test_interest/conftest.py` - Same deduplication; imports from root conftest
- `tests/test_workflow/test_search_augment.py` - Rewired imports from .conftest to tests.conftest
- `tests/test_workflow/test_queries.py` - Split import: sample_paper_data from tests.conftest, sample_saved_query_data from .conftest
- `tests/test_workflow/test_export.py` - Rewired imports from .conftest to tests.conftest
- `tests/test_workflow/test_watches.py` - Rewired imports from .conftest to tests.conftest
- `tests/test_interest/test_suggestions.py` - Split import: sample_paper_data from tests.conftest, domain factories from .conftest
- `src/arxiv_mcp/mcp/tools/workflow.py` - create_watch docstring references watch://{slug}/deltas resource
- `src/arxiv_mcp/content/__init__.py` - Docstring only, all re-exports removed
- `tests/test_mcp/test_docstrings.py` - New: regression test for create_watch docstring accuracy
- `tests/test_content/test_import_isolation.py` - New: subprocess-based import isolation tests for content.models and content.rights

## Decisions Made
- Shared fixtures (test_engine, test_session, TSVECTOR SQL, sample_paper_data) centralized in root conftest.py only; module conftest files import them via `from tests.conftest import`
- Domain-specific factories (sample_collection_data, sample_triage_data, sample_profile_data, sample_signal_data, sample_saved_query_data) kept in their module conftest files
- test_engine and test_session fixtures auto-discovered by pytest (not re-imported as functions) since they are @pytest.fixture-decorated
- Subprocess-based import isolation testing chosen because sys.modules checks in the test runner would pass vacuously if httpx/bs4 were already loaded by earlier tests

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

- Test suite with `-x` flag initially appeared to fail on `tests/test_content/test_service.py` but this is a pre-existing DB fixture ordering issue (content_session_factory TRUNCATE runs before tables exist). Verified by running the same test against pre-change code. Running the full suite without `-x` results in 493 tests passing.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Conftest hierarchy clean and deduplicated, ready for 08-02 (live DB migration)
- All 493 tests green, test infrastructure stable
- Pre-existing test_content/test_service fixture ordering issue exists but is unrelated to this plan's scope

---
*Phase: 08-infrastructure-fixes*
*Completed: 2026-03-13*
