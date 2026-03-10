---
phase: 04-enrichment-adapters
plan: 02
subsystem: enrichment
tags: [openalex, enrichment, cli, click, rich, sqlalchemy, upsert, cooldown, batch, pydantic]

# Dependency graph
requires:
  - phase: 04-enrichment-adapters
    provides: EnrichmentAdapter protocol, OpenAlexAdapter, PaperEnrichment ORM, EnrichmentResult schemas
  - phase: 01-metadata-substrate
    provides: Paper ORM model with arxiv_id PK, doi, openalex_id, processing_tier columns
  - phase: 02-workflow-state
    provides: Collection/CollectionPaper ORM models, CollectionService, SearchService
provides:
  - EnrichmentService with enrich_paper, enrich_collection, enrich_search, status, and stats
  - Cooldown enforcement (7-day default, --refresh bypass)
  - Paper promotion to ENRICHED tier with DOI preservation
  - PaperEnrichment upsert with pg_insert ON CONFLICT
  - EnrichmentInfo Pydantic display model extending PaperDetail
  - CLI subgroup (enrich paper/collection/search/status/refresh)
  - Rich formatted output with FWCI interpretation and recency warning
  - Quiet mode (-q) for machine-readable JSON output
  - Dry-run mode for batch operations
affects: [mcp-surface, ranking-integration, content-normalization]

# Tech tracking
tech-stack:
  added: []
  patterns: [pg_insert ON CONFLICT upsert for enrichment records, cooldown filter with timedelta, batch enrich with per-paper session scope, CLI lazy import pattern for enrichment group]

key-files:
  created:
    - src/arxiv_mcp/enrichment/service.py
    - src/arxiv_mcp/enrichment/cli.py
    - tests/test_enrichment/test_service.py
    - tests/test_enrichment/test_cli.py
  modified:
    - src/arxiv_mcp/enrichment/__init__.py
    - src/arxiv_mcp/models/paper.py
    - src/arxiv_mcp/cli.py

key-decisions:
  - "pg_insert ON CONFLICT for enrichment upsert: full column overwrite on success/partial, status-only update on error (preserves existing data)"
  - "DOI preservation: Paper.doi only set if currently null (never overwrite user-provided or arXiv-harvested DOI)"
  - "Cooldown filter as separate SQL query before batch enrichment (simple, avoids complex JOIN)"
  - "Per-paper session scope in batch enrichment (commit after each paper for partial failure resilience)"
  - "Mock adapter pattern for service tests (implements protocol, no real HTTP, predetermined results by arxiv_id)"

patterns-established:
  - "EnrichmentService DI pattern: session_factory + settings + optional adapter injection (mirrors CollectionService)"
  - "Enrichment upsert: pg_insert ON CONFLICT with conditional update columns based on result status"
  - "Cooldown enforcement: timedelta comparison on last_attempted_at column"
  - "CLI enrich subgroup: lazy import EnrichmentService inside command functions"
  - "Mock adapter for enrichment testing: class with adapter_name + enrich() returning predetermined results"

requirements-completed: [ENRC-01, ENRC-02, ENRC-03, ENRC-04]

# Metrics
duration: 8min
completed: 2026-03-10
---

# Phase 4 Plan 2: EnrichmentService, CLI Subgroup & Paper Show Integration Summary

**EnrichmentService with cooldown-enforced upsert, batch operations (collection/search), and full CLI subgroup with Rich formatted output and FWCI interpretation**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-10T02:59:24Z
- **Completed:** 2026-03-10T03:07:50Z
- **Tasks:** 2
- **Files modified:** 7

## Accomplishments
- EnrichmentService orchestrates full enrich workflow: verify paper, check cooldown, call adapter, upsert record, promote Paper
- Cooldown enforcement (7-day default, --refresh bypass) prevents unnecessary API calls
- Paper.openalex_id, Paper.doi (if null), and processing_tier updated on successful enrichment
- Not-found and error statuses recorded without losing existing enrichment data
- Collection-scoped and search-scoped batch enrichment with progress summary and dry-run mode
- CLI subgroup with 5 commands (paper, collection, search, status, refresh) and Rich formatted display
- 25 new tests (17 integration + 8 CLI) all passing; 306 total tests with zero regressions

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1: EnrichmentService with storage, cooldown, batch operations, and integration tests**
   - `8771e24` (test) - Failing tests for EnrichmentService (17 integration tests)
   - `e9831fc` (feat) - Implement EnrichmentService with storage, cooldown, and batch operations
2. **Task 2: Enrichment CLI subgroup and paper show integration**
   - `8a0991b` (feat) - Add enrichment CLI subgroup and paper show integration (8 CLI tests)

## Files Created/Modified
- `src/arxiv_mcp/enrichment/service.py` - EnrichmentService with enrich_paper, enrich_collection, enrich_search, status, stats
- `src/arxiv_mcp/enrichment/cli.py` - Click subgroup with paper/collection/search/status/refresh commands
- `src/arxiv_mcp/enrichment/__init__.py` - Updated exports with EnrichmentService, OpenAlexAdapter, etc.
- `src/arxiv_mcp/models/paper.py` - Added EnrichmentInfo display model, enrichment field on PaperDetail
- `src/arxiv_mcp/cli.py` - Registered enrich_group with lazy import pattern
- `tests/test_enrichment/test_service.py` - 17 integration tests with MockAdapter
- `tests/test_enrichment/test_cli.py` - 8 CLI tests with mocked EnrichmentService

## Decisions Made
- Used pg_insert ON CONFLICT for PaperEnrichment upsert: on success/partial, all columns overwritten; on error, only status/error_detail/last_attempted_at updated (preserves existing enrichment data)
- Paper.doi only set if currently null -- never overwrites existing DOI from arXiv harvest or user entry
- Cooldown filter implemented as separate SQL query (SELECT PaperEnrichment WHERE last_attempted_at >= threshold) before batch enrichment, keeping batch logic simple
- Per-paper session scope in _batch_enrich (each paper commits independently) for partial failure resilience
- MockAdapter class implementing EnrichmentAdapter protocol for testing -- returns predetermined EnrichmentResults by arxiv_id, tracks enrich() calls for assertion

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required. OpenAlex API key configuration is optional (handled via `.env` file when ready for live usage).

## Next Phase Readiness
- Phase 4 (enrichment adapters) is fully complete
- EnrichmentService + CLI ready for MCP tool integration in Phase 5
- EnrichmentInfo model ready for paper show display enrichment
- Batch enrichment ready for scheduled/automated workflows
- 306 total tests passing with full coverage of enrichment features

## Self-Check: PASSED

All 7 created/modified files verified present. All 3 task commits verified in git log.

---
*Phase: 04-enrichment-adapters*
*Completed: 2026-03-10*
