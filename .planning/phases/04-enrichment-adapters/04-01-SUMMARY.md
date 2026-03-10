---
phase: 04-enrichment-adapters
plan: 01
subsystem: enrichment
tags: [openalex, httpx, respx, enrichment, doi, rate-limiting, pydantic, sqlalchemy, jsonb]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: Paper ORM model with arxiv_id PK, doi, openalex_id columns, ProcessingTier enum
provides:
  - PaperEnrichment ORM model with FK to Paper and enrichment data columns
  - EnrichmentResult, TopicInfo, ExternalIds, EnrichmentStatus Pydantic schemas
  - OpenAlexAdapter with DOI-based resolution, rate limiting, and retry logic
  - EnrichmentAdapter protocol for future adapter implementations
  - Alembic migration 004 for paper_enrichments table
  - Settings with 5 enrichment configuration fields
  - respx-based test infrastructure with JSON fixtures
affects: [04-02-enrichment-adapters, mcp-surface, ranking-integration]

# Tech tracking
tech-stack:
  added: [respx>=0.22]
  patterns: [respx mock router fixture, EnrichmentAdapter protocol, DOI-based resolution, rate limiter with monotonic clock]

key-files:
  created:
    - src/arxiv_mcp/enrichment/__init__.py
    - src/arxiv_mcp/enrichment/models.py
    - src/arxiv_mcp/enrichment/openalex.py
    - alembic/versions/004_enrichment_table.py
    - tests/test_enrichment/__init__.py
    - tests/test_enrichment/conftest.py
    - tests/test_enrichment/test_models.py
    - tests/test_enrichment/test_adapter.py
    - tests/test_enrichment/fixtures/openalex_work_attention.json
    - tests/test_enrichment/fixtures/openalex_work_not_found.json
    - tests/test_enrichment/fixtures/openalex_batch_response.json
  modified:
    - src/arxiv_mcp/db/models.py
    - src/arxiv_mcp/config.py
    - pyproject.toml

key-decisions:
  - "respx fixture pattern: context manager yield with base_url scoping (not decorator)"
  - "TopicInfo and ExternalIds strip URL prefixes via field_validator (short-form storage)"
  - "EnrichmentResult.from_openalex_work determines status via field completeness heuristic"
  - "RateLimiter uses time.monotonic + asyncio.sleep (simple, sufficient for 5 req/s)"

patterns-established:
  - "respx mock fixture: context manager with base_url for scoped HTTP mocking"
  - "Enrichment adapter protocol: 2 methods + 1 property (resolve_ids, enrich, adapter_name)"
  - "DOI-based arXiv resolution: singleton for 1 paper (FREE), batch filter for N papers (10 credits)"
  - "URL prefix stripping: validators that normalize OpenAlex URLs to short-form IDs"

requirements-completed: [ENRC-01, ENRC-03, ENRC-04]

# Metrics
duration: 8min
completed: 2026-03-10
---

# Phase 4 Plan 1: Enrichment Data Model & OpenAlex Adapter Summary

**PaperEnrichment ORM model with JSONB columns, OpenAlexAdapter with DOI-based singleton/batch resolution, rate limiting, and respx test infrastructure**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-10T02:47:24Z
- **Completed:** 2026-03-10T02:55:54Z
- **Tasks:** 2
- **Files modified:** 14

## Accomplishments
- PaperEnrichment ORM model with 16 columns, FK to Paper, CHECK constraint on status, and 2 indexes
- EnrichmentResult.from_openalex_work() parses full OpenAlex Work JSON with topic hierarchy, citations, FWCI, related works
- OpenAlexAdapter with singleton (FREE) and batch (10 credits) DOI-based resolution endpoints
- Rate limiter, exponential backoff with jitter on 429, graceful timeout/error handling
- 30 tests passing with respx-mocked HTTP and 3 JSON fixture files

## Task Commits

Each task was committed atomically (TDD: RED then GREEN):

1. **Task 1: Enrichment data model, Pydantic schemas, and migration**
   - `9a40e4e` (test) - Failing tests for enrichment models and schemas
   - `bc2f539` (feat) - Implement enrichment data model, schemas, and migration
2. **Task 2: OpenAlexAdapter with DOI-based resolution, rate limiting, and HTTP tests**
   - `aa15fa0` (test) - Failing tests for OpenAlexAdapter
   - `c51f9aa` (feat) - Implement OpenAlexAdapter with DOI resolution and rate limiting

## Files Created/Modified
- `src/arxiv_mcp/enrichment/__init__.py` - Package init
- `src/arxiv_mcp/enrichment/models.py` - EnrichmentResult, TopicInfo, ExternalIds, EnrichmentStatus Pydantic schemas
- `src/arxiv_mcp/enrichment/openalex.py` - OpenAlexAdapter with EnrichmentAdapter protocol, RateLimiter
- `src/arxiv_mcp/db/models.py` - Added PaperEnrichment ORM model
- `src/arxiv_mcp/config.py` - Extended Settings with 5 enrichment fields
- `alembic/versions/004_enrichment_table.py` - Migration for paper_enrichments table
- `pyproject.toml` - Added respx>=0.22 to dev dependencies
- `tests/test_enrichment/conftest.py` - Session factory fixture, JSON fixture loaders
- `tests/test_enrichment/test_models.py` - 16 unit tests for Pydantic schemas and ORM model
- `tests/test_enrichment/test_adapter.py` - 14 unit tests for OpenAlexAdapter with respx mocks
- `tests/test_enrichment/fixtures/` - 3 JSON fixture files (attention, not_found, batch)

## Decisions Made
- Used `respx.mock(base_url=...)` context manager as fixture instead of decorator pattern (decorator creates separate router scope that conflicts with class-based test methods)
- TopicInfo and ExternalIds use `field_validator` to strip OpenAlex URL prefixes to short-form IDs (consistent with Paper.doi storing bare DOI)
- EnrichmentResult status determination: SUCCESS if cited_by_count + (fwci OR topics), PARTIAL otherwise -- matches real-world OpenAlex response patterns
- RateLimiter implementation uses time.monotonic + asyncio.sleep -- simple and sufficient for the 5 req/s target
- Related works stored as full OpenAlex URLs (as returned by API), consistent with research recommendation

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed respx mock pattern from decorator to fixture**
- **Found during:** Task 2 (adapter tests)
- **Issue:** `@respx.mock(base_url=...)` decorator creates isolated router; `respx.get()` inside test body registers on global router, causing AllMockedAssertionError
- **Fix:** Changed to `mock_openalex` fixture using context manager pattern: `with respx.mock(base_url=...) as router: yield router`
- **Files modified:** tests/test_enrichment/test_adapter.py
- **Verification:** All 14 adapter tests pass

**2. [Rule 1 - Bug] Fixed httpx URL attribute from raw_query to query**
- **Found during:** Task 2 (adapter tests)
- **Issue:** httpx URL object has `.query` (bytes), not `.raw_query` attribute
- **Fix:** Changed `request.url.raw_query` to `request.url.query` in parameter assertion tests
- **Files modified:** tests/test_enrichment/test_adapter.py
- **Verification:** API key and select parameter tests pass

---

**Total deviations:** 2 auto-fixed (2 bugs)
**Impact on plan:** Both were test implementation details, not architectural changes. No scope creep.

## Issues Encountered
None beyond the auto-fixed items above.

## User Setup Required
None - no external service configuration required. OpenAlex API key configuration is optional (handled via `.env` file when ready for live usage).

## Next Phase Readiness
- EnrichmentAdapter protocol and OpenAlexAdapter ready for EnrichmentService (04-02)
- PaperEnrichment ORM model ready for DB storage operations
- JSON fixtures and respx infrastructure ready for service-level integration tests
- Settings enrichment fields ready for CLI command injection

## Self-Check: PASSED

All 13 created files verified present. All 4 task commits verified in git log.

---
*Phase: 04-enrichment-adapters*
*Completed: 2026-03-10*
