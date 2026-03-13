---
phase: 06-content-normalization
plan: 02
subsystem: content
tags: [httpx, beautifulsoup, lxml, marker, content-adapters, html-fetcher, content-service, priority-chain]

# Dependency graph
requires:
  - phase: 06-content-normalization
    provides: ContentVariant ORM model, ContentConversionResult Pydantic model, RightsChecker, Settings extension, content_session_factory
  - phase: 04-enrichment-adapters
    provides: RateLimiter, EnrichmentService DI pattern, MockAdapter pattern, pg_insert ON CONFLICT upsert
provides:
  - ContentAdapter protocol for pluggable PDF conversion backends
  - MarkerAdapter wrapping Marker PdfConverter with asyncio.to_thread
  - MockContentAdapter with call tracking for testing
  - fetch_arxiv_html function with HEAD-first availability check and sanitization
  - ContentService with get_or_create_variant implementing source-aware priority chain
  - Variant caching via content_variants DB lookup
  - Processing tier promotion to CONTENT_PARSED
affects: [06-03-PLAN, mcp-content-tool, content-batch-processing]

# Tech tracking
tech-stack:
  added: [respx]
  patterns: [content-adapter-protocol, html-fetcher-pattern, content-service-priority-chain, temp-file-pdf-lifecycle]

key-files:
  created:
    - src/arxiv_mcp/content/adapters.py
    - src/arxiv_mcp/content/html_fetcher.py
    - src/arxiv_mcp/content/service.py
    - tests/test_content/test_adapter.py
    - tests/test_content/test_html_fetcher.py
    - tests/test_content/test_service.py
  modified:
    - src/arxiv_mcp/content/__init__.py

key-decisions:
  - "ContentAdapter protocol mirrors EnrichmentAdapter: adapter_name property + async convert method"
  - "MarkerAdapter initializes PdfConverter once in __init__ (not per-call) and uses asyncio.to_thread"
  - "HTML fetcher uses HEAD-first check to avoid wasting bandwidth on 404 papers"
  - "ContentService reuses enrichment RateLimiter (1/content_rate_limit requests per second)"
  - "PDF temp file uses NamedTemporaryFile with delete=True (auto-cleanup after conversion)"
  - "Variant storage uses pg_insert ON CONFLICT upsert (same pattern as enrichment)"

patterns-established:
  - "Content adapter protocol: adapter_name + async convert(pdf_path, arxiv_id) -> ContentConversionResult"
  - "HTML fetcher: HEAD availability check + GET + BeautifulSoup sanitization"
  - "ContentService priority chain: cache check -> acquire -> store -> promote"
  - "MockContentAdapter: call tracking + configurable results (mirrors MockAdapter from enrichment)"

requirements-completed: [CONT-04, CONT-05]

# Metrics
duration: 54min
completed: 2026-03-13
---

# Phase 06 Plan 02: Content Adapters and Service Summary

**ContentAdapter protocol with MarkerAdapter, HTML fetcher with sanitization, and ContentService implementing source-aware priority chain (abstract -> HTML -> PDF markdown) with DB caching and tier promotion**

## Performance

- **Duration:** 54 min
- **Started:** 2026-03-12T23:35:00Z
- **Completed:** 2026-03-13T00:29:00Z
- **Tasks:** 2 (both TDD: red/green)
- **Files modified:** 7

## Accomplishments
- ContentAdapter protocol defined with MarkerAdapter (GPU/CPU) and MockContentAdapter (testing)
- HTML fetcher with HEAD-first availability check, article content extraction, nav/header/footer stripping
- ContentService.get_or_create_variant implementing full priority chain: abstract -> HTML -> PDF markdown
- Cached variants returned from DB without re-fetching (cache-first pattern)
- Processing tier promoted to CONTENT_PARSED on first non-abstract variant storage
- Full provenance tracking: source_url, backend, backend_version, extraction_method, license_uri, content_hash
- 27 new tests (16 adapter/fetcher + 11 service), 465 total suite passing

## Task Commits

Each task was committed atomically (TDD: test then implementation):

1. **Task 1: ContentAdapter protocol, MarkerAdapter, HTML fetcher, MockContentAdapter** (TDD)
   - `8a44918` (test: failing tests for content adapters and HTML fetcher)
   - `52314d1` (feat: implement ContentAdapter protocol, MarkerAdapter, HTML fetcher)
2. **Task 2: ContentService orchestration with priority chain, DB storage, tier promotion** (TDD)
   - `f92f31a` (test: failing tests for ContentService orchestration)
   - `01e06ba` (feat: implement ContentService with priority chain and DB storage)

## Files Created/Modified
- `src/arxiv_mcp/content/adapters.py` - ContentAdapter protocol, MarkerAdapter, MockContentAdapter
- `src/arxiv_mcp/content/html_fetcher.py` - fetch_arxiv_html with HEAD check, sanitization, rate limiting
- `src/arxiv_mcp/content/service.py` - ContentService with priority chain, caching, tier promotion
- `src/arxiv_mcp/content/__init__.py` - Updated exports (ContentAdapter, MarkerAdapter, MockContentAdapter, ContentService, fetch_arxiv_html)
- `tests/test_content/test_adapter.py` - 8 tests for adapter protocol, call tracking, results
- `tests/test_content/test_html_fetcher.py` - 8 tests for HTML fetching, 404, stripping, timeout
- `tests/test_content/test_service.py` - 11 tests for service orchestration, caching, promotion, provenance

## Decisions Made
- ContentAdapter protocol mirrors EnrichmentAdapter: adapter_name property + async convert method -- consistent project pattern
- MarkerAdapter initializes PdfConverter once in __init__ (not per-call) -- avoids repeated GPU model loading
- HTML fetcher uses HEAD-first check before GET -- avoids wasting bandwidth on papers without HTML (most pre-Dec 2023)
- ContentService reuses enrichment RateLimiter (1/content_rate_limit rps) -- consistent rate limiting across arXiv fetches
- PDF temp file uses NamedTemporaryFile with delete=True -- automatic cleanup, no orphaned files
- Variant storage uses pg_insert ON CONFLICT upsert -- same proven pattern as enrichment service

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Missing _variant_to_dict helper method**
- **Found during:** Task 2 (ContentService tests)
- **Issue:** get_variant called self._variant_to_dict which was not defined, causing AttributeError on cache hit path
- **Fix:** Added _variant_to_dict static method converting ContentVariant ORM to response dict
- **Files modified:** src/arxiv_mcp/content/service.py
- **Committed in:** 01e06ba (part of Task 2 GREEN commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Trivial omission caught by tests. No scope creep.

## Issues Encountered

- Test duration longer than expected (~14 min per DB test run) due to asyncpg/PostgreSQL connection overhead in test DB. Not a code issue -- test infrastructure overhead with content_session_factory creating/dropping all tables per test class. Acceptable for correctness.

## User Setup Required

None - no external service configuration required. Marker is optional (falls back gracefully if not installed).

## Next Phase Readiness
- ContentService ready for Plan 03 (MCP tool integration: get_content_variant tool)
- ContentAdapter protocol ready for future Docling/GROBID adapter additions
- All provenance fields populated per CONT-03 requirement
- Processing tier promotion working for MCP resource enrichment display
- 465 tests passing, no regressions

## Self-Check: PASSED

All 7 files verified present. All 4 commits (8a44918, 52314d1, f92f31a, 01e06ba) verified in git log.

---
*Phase: 06-content-normalization*
*Completed: 2026-03-13*
