---
phase: 10-agent-integration-test
plan: 03
subsystem: mcp, docs
tags: [mcp, error-handling, readme, friction-report, agent-ux]

# Dependency graph
requires:
  - phase: 10-agent-integration-test
    provides: "10-FRICTION.md with all issues identified from agent session"
provides:
  - "B-01 fix: add_to_collection graceful error for non-existent papers"
  - "F-05 fix: browse_recent description recommends time_basis=submitted"
  - "F-07 fix: create_watch error uses 'Watch' not 'Saved query'"
  - "README: validated MCP setup instructions with venv path and Claude Code command"
  - "Finalized friction report with all 15 items resolved or tracked for v0.2.0"
affects: [v0.2.0-planning]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "IntegrityError catch at MCP tool layer for FK constraint violations"
    - "ValueError catch + string replacement for user-facing error terminology"

key-files:
  created: []
  modified:
    - "src/arxiv_mcp/mcp/tools/workflow.py"
    - "src/arxiv_mcp/mcp/tools/discovery.py"
    - "README.md"
    - ".planning/phases/10-agent-integration-test/10-FRICTION.md"

key-decisions:
  - "IntegrityError catch at MCP tool layer (not service layer) for clean error messages"
  - "F-07 fix via string replacement at tool layer rather than modifying SavedQueryService"
  - "README split into Claude Code and Claude Desktop sections with validated configs"
  - "Absolute venv Python path documented as requirement for MCP config"

patterns-established:
  - "MCP tools catch SQLAlchemy IntegrityError for FK violations and return JSON error"
  - "MCP tools rephrase internal service terminology in error messages"

requirements-completed: [SC-4, SC-5]

# Metrics
duration: 5min
completed: 2026-03-14
---

# Phase 10 Plan 03: Critical Fixes and README Validation Summary

**3 critical MCP ergonomic fixes (B-01 IntegrityError, F-05 browse_recent description, F-07 watch terminology) plus validated README with venv and Claude Code instructions**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-14T05:09:53Z
- **Completed:** 2026-03-14T05:14:26Z
- **Tasks:** 2
- **Files modified:** 4

## Accomplishments
- Fixed add_to_collection raw SQLAlchemy error leak (B-01) -- now returns clean JSON error for non-existent papers
- Fixed browse_recent tool description to recommend time_basis=submitted when announced_date may be null (F-05)
- Fixed create_watch duplicate error to say "Watch" instead of internal "Saved query" (F-07)
- Corrected README: added venv creation, absolute Python path guidance, Claude Code `claude mcp add-json` command
- Finalized friction report with resolution status for all 15 issues (4 fixed, 11 tracked for v0.2.0)

## Task Commits

Each task was committed atomically:

1. **Task 1: Validate README and apply critical fixes**
   - `93feb4c` (fix) -- B-01 + F-07: IntegrityError catch and watch error terminology
   - `18f9097` (fix) -- F-05: browse_recent description update
   - `f68fef8` (fix) -- README setup instructions corrected
2. **Task 2: Finalize friction report with resolution statuses** - `523e251` (docs)

## Files Created/Modified
- `src/arxiv_mcp/mcp/tools/workflow.py` -- Added IntegrityError import and catch in add_to_collection; added ValueError catch with terminology fix in create_watch
- `src/arxiv_mcp/mcp/tools/discovery.py` -- Updated browse_recent docstring to recommend time_basis=submitted
- `README.md` -- Added venv creation steps, absolute Python path requirement, separate Claude Code and Claude Desktop config sections
- `.planning/phases/10-agent-integration-test/10-FRICTION.md` -- Added resolution status for all 15 items plus summary section

## Decisions Made
- IntegrityError catch at MCP tool layer (not service layer) -- keeps service layer clean, tool layer handles user-facing concerns
- F-07 fix via string replacement at tool layer rather than modifying SavedQueryService -- avoids touching shared service code
- README split into Claude Code and Claude Desktop sections -- different setup workflows validated during session
- Absolute venv Python path documented as requirement -- generic `python` fails when MCP server launched from different directory

## Deviations from Plan

None -- plan executed exactly as written.

## Issues Encountered
None

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Phase 10 complete: all 3 plans executed (config, session, fixes)
- 15 friction items tracked: 4 fixed in v0.1, 11 deferred to v0.2.0
- MCP server validated with real agent workflows (13/13 tools, 3/4 resources)
- v0.1 milestone ready for final review

## Self-Check: PASSED

All files exist, all commits verified.

---
*Phase: 10-agent-integration-test*
*Completed: 2026-03-14*
