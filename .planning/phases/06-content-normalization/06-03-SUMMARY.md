---
phase: 06-content-normalization
plan: 03
subsystem: mcp
tags: [mcp-tool, rights-enforcement, content-variants, cli, paper-resource]

# Dependency graph
requires:
  - phase: 06-content-normalization
    provides: ContentService with get_or_create_variant and list_variants, RightsChecker with check_access, ContentConversionResult
  - phase: 04.1-mcp-v1
    provides: AppContext dataclass, _get_app helper pattern, tool registration via side-effect imports, paper resource composition
provides:
  - get_content_variant MCP tool with serving-time rights enforcement (CONT-06)
  - AppContext extended with ContentService field
  - Paper resource content_variants listing
  - Content CLI subgroup (get + status commands)
  - Tool count at 11 (was 10, +1 for get_content_variant)
affects: [phase-07, mcp-surface, content-batch-processing]

# Tech tracking
tech-stack:
  added: []
  patterns: [rights-enforcement-at-serving-time, content-tool-pattern, content-cli-pattern]

key-files:
  created:
    - src/arxiv_mcp/mcp/tools/content.py
    - src/arxiv_mcp/content/cli.py
    - tests/test_mcp/test_content_tool.py
  modified:
    - src/arxiv_mcp/mcp/server.py
    - src/arxiv_mcp/mcp/resources/paper.py
    - src/arxiv_mcp/cli.py
    - tests/test_mcp/conftest.py
    - tests/test_mcp/test_tool_names.py
    - tests/test_mcp/test_resources.py

key-decisions:
  - "get_content_variant validates variant parameter before rights check (fail fast on invalid input)"
  - "Abstract variant skips rights check entirely (always available, no license restriction needed)"
  - "Rights enforcement uses Paper.license_uri from DB lookup, not from ContentService result (single source of truth)"
  - "Content CLI follows enrichment CLI pattern: _make_services helper, asyncio.run wrapper, Rich+JSON output"
  - "Paper resource returns content_variants as lightweight metadata list (no full content)"

patterns-established:
  - "Content tool pattern: validate input -> check rights -> delegate to service -> propagate warnings"
  - "Serving-time rights enforcement: RightsChecker at MCP tool layer, not service layer (ADR-0003)"

requirements-completed: [MCP-03, CONT-06]

# Metrics
duration: 18min
completed: 2026-03-13
---

# Phase 06 Plan 03: MCP Tool, Resource, and CLI Integration Summary

**get_content_variant MCP tool with serving-time rights enforcement, paper resource content_variants listing, and content CLI subgroup for Phase 6 completion**

## Performance

- **Duration:** 18 min
- **Started:** 2026-03-13T00:32:31Z
- **Completed:** 2026-03-13T00:50:31Z
- **Tasks:** 2 (Task 1: TDD red/green, Task 2: integration)
- **Files modified:** 9

## Accomplishments
- get_content_variant MCP tool registered as 11th tool with abstract/html/pdf_markdown/best variant support
- Serving-time rights enforcement via RightsChecker: local mode allows with warning, hosted mode blocks restrictive licenses
- AppContext extended with ContentService for lifespan-managed DI
- Paper resource now includes content_variants field listing available variant types without full content
- Content CLI subgroup with "get" (--variant, --full, -q) and "status" (table display) commands
- 471 tests passing (was 465), no regressions

## Task Commits

Each task was committed atomically (Task 1 as TDD: test then implementation):

1. **Task 1: get_content_variant MCP tool, AppContext extension, and server wiring** (TDD)
   - `9ecbad3` (test: failing tests for get_content_variant MCP tool)
   - `f462588` (feat: implement get_content_variant with rights enforcement)
2. **Task 2: Paper resource extension, tool count update, content CLI, and full integration**
   - `457ca19` (feat: paper resource extension, tool count update, content CLI)

## Files Created/Modified
- `src/arxiv_mcp/mcp/tools/content.py` - get_content_variant MCP tool with rights enforcement
- `src/arxiv_mcp/content/cli.py` - Content CLI subgroup (get + status commands)
- `tests/test_mcp/test_content_tool.py` - 6 tests for content tool (abstract, best, invalid, not found, warning, blocked)
- `src/arxiv_mcp/mcp/server.py` - ContentService import, AppContext.content field, lifespan wiring, tool import
- `src/arxiv_mcp/mcp/resources/paper.py` - content_variants field in paper resource response
- `src/arxiv_mcp/cli.py` - content_group registration with lazy import pattern
- `tests/test_mcp/conftest.py` - content mock added to mock_app_context
- `tests/test_mcp/test_tool_names.py` - Tool count 10->11, get_content_variant in expected set
- `tests/test_mcp/test_resources.py` - Paper resource test verifies content_variants field

## Decisions Made
- get_content_variant validates variant parameter before rights check (fail fast on invalid input)
- Abstract variant skips rights check entirely -- abstracts are always available per arXiv terms
- Rights enforcement uses Paper.license_uri from DB lookup at tool layer, not at service layer -- keeps serving-time enforcement visible at the MCP surface (ADR-0003)
- Content CLI follows enrichment CLI pattern exactly: _make_services helper, asyncio.run wrapper, Rich+JSON output
- Paper resource returns content_variants as lightweight metadata list (variant_type + converted_at + backend, no full content)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Phase 6 complete: all CONT-01 through CONT-06 + MCP-03 requirements addressed
- 11 MCP tools + 4 resources + 3 prompts operational
- Content normalization pipeline: rights checking -> variant acquisition (abstract/HTML/PDF) -> DB caching -> MCP serving
- 471 tests passing across all phases, no regressions
- Ready for Phase 7 or v2 planning

## Self-Check: PASSED

All 9 files verified present. All 3 commits (9ecbad3, f462588, 457ca19) verified in git log.
