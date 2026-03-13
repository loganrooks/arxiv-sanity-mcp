---
phase: 06-content-normalization
plan: 04
subsystem: database, testing
tags: [beautifulsoup4, bs4, dependency, pyproject, test-isolation]

# Dependency graph
requires:
  - phase: 06-content-normalization
    provides: "html_fetcher.py imports bs4 (beautifulsoup4)"
provides:
  - "beautifulsoup4 declared as project dependency in pyproject.toml"
  - "Content test isolation fix (TRUNCATE instead of stale create_all)"
  - "All 471 tests passing including 176 Phase 6 tests"
affects: [content-normalization, mcp-server]

# Tech tracking
tech-stack:
  added: [beautifulsoup4>=4.12, soupsieve]
  patterns: [TRUNCATE CASCADE for test fixture isolation]

key-files:
  created: []
  modified:
    - pyproject.toml
    - tests/test_content/conftest.py
    - uv.lock

key-decisions:
  - "TRUNCATE CASCADE instead of drop+create for content test fixture cleanup (preserves asyncpg prepared statement cache)"

patterns-established:
  - "Test fixture isolation via TRUNCATE CASCADE: preserves table structure and connection pool compatibility while clearing stale data"

requirements-completed: [CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06, MCP-03]

# Metrics
duration: 51min
completed: 2026-03-13
---

# Phase 06 Plan 04: Missing Dependency Gap Closure Summary

**beautifulsoup4 declared in pyproject.toml, content test isolation fixed, all 471 tests green**

## Performance

- **Duration:** 51 min (mostly test execution time -- content service integration tests make real HTTP calls to arXiv, ~14 min per full suite run)
- **Started:** 2026-03-13T01:34:40Z
- **Completed:** 2026-03-13T02:26:35Z
- **Tasks:** 1
- **Files modified:** 3

## Accomplishments
- beautifulsoup4>=4.12 added to pyproject.toml dependencies (was imported but never declared)
- Fixed content test fixture isolation that caused UniqueViolation and UndefinedTableError in full suite runs
- All 471 tests pass with zero failures (460 non-content + 11 content service)
- MCP server importable without ModuleNotFoundError

## Task Commits

Each task was committed atomically:

1. **Task 1: Add beautifulsoup4 dependency and verify full test suite** - `c5cd2ef` (fix)

**Plan metadata:** pending (docs: complete plan)

## Files Created/Modified
- `pyproject.toml` - Added beautifulsoup4>=4.12 to [project].dependencies
- `tests/test_content/conftest.py` - TRUNCATE CASCADE in content_session_factory setup for clean test state
- `uv.lock` - Lock file updated with beautifulsoup4 4.14.3 and soupsieve 2.8.3

## Decisions Made
- Used TRUNCATE CASCADE instead of DROP+CREATE for content test fixture cleanup. Drop+create caused asyncpg prepared statement cache invalidation when multiple test modules share the same test_engine connection pool. TRUNCATE preserves table structure and prepared statement compatibility while clearing stale data from prior test fixtures.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed content test fixture isolation**
- **Found during:** Task 1 (full test suite verification)
- **Issue:** content_session_factory used bare create_all without cleaning prior data, causing UniqueViolation when other test modules left papers with arxiv_id '2301.00001' in shared test DB. Initial fix (drop+create) broke asyncpg prepared statement cache, causing UndefinedTableError.
- **Fix:** Changed to TRUNCATE CASCADE in fixture setup to clear data while preserving table structure and connection pool state.
- **Files modified:** tests/test_content/conftest.py
- **Verification:** Full suite (471 tests) passes. Content tests pass both in isolation and within full suite.
- **Committed in:** c5cd2ef (part of task commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Fix necessary for full test suite to pass. No scope creep.

## Issues Encountered
- Content service integration tests make real HTTP calls to arXiv in some cases (respx mock scope), causing ~14 minutes per full suite run. This is a pre-existing condition, not introduced by this change. Noted but not fixed (out of scope).

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Phase 06 (Content Normalization) fully complete with all gaps closed
- All 471 tests passing, MCP server importable, 11 tools operational
- Project ready for v2 planning or maintenance

## Self-Check: PASSED

- FOUND: pyproject.toml
- FOUND: tests/test_content/conftest.py
- FOUND: uv.lock
- FOUND: 06-04-SUMMARY.md
- FOUND: c5cd2ef (task commit)

---
*Phase: 06-content-normalization*
*Completed: 2026-03-13*
