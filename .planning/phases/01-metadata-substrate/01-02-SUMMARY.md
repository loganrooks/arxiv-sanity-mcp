---
phase: 01-metadata-substrate
plan: 02
subsystem: ingestion
tags: [oaipmh-scythe, lxml, httpx, xml-parsing, oai-pmh, arxiv-api, click-cli, structlog, python-dateutil]

# Dependency graph
requires:
  - "Paper SQLAlchemy model with 25+ columns and 8 indexes"
  - "Async engine/session factory"
  - "Settings with category TOML loading"
  - "Click CLI skeleton"
provides:
  - "XML parsers for arXivRaw, arXiv, and oai_dc OAI-PMH formats"
  - "RawPaperMetadata and PaperVersion dataclasses"
  - "Metadata mapper: RawPaperMetadata to Paper ORM instances"
  - "OAIPMHHarvester with bulk and incremental modes"
  - "Batch upsert with ON CONFLICT deduplication"
  - "JSON checkpoint for incremental harvesting"
  - "ArxivAPIClient with fetch_paper() and search()"
  - "Atom XML parser for arXiv API responses"
  - "CLI commands: harvest bulk, harvest incremental, harvest fetch"
affects: [01-03-search, 02-workflow-state, 03-enrichment-adapters]

# Tech tracking
tech-stack:
  added: [python-dateutil]
  patterns: [oai-pmh-arXivRaw-parsing, atom-xml-parsing, mock-based-integration-tests, on-conflict-upsert, json-checkpoint-file]

key-files:
  created:
    - src/arxiv_mcp/ingestion/parsers.py
    - src/arxiv_mcp/ingestion/mapper.py
    - src/arxiv_mcp/ingestion/oai_pmh.py
    - src/arxiv_mcp/ingestion/arxiv_api.py
    - src/arxiv_mcp/ingestion/cli.py
    - tests/test_ingestion/__init__.py
    - tests/test_ingestion/conftest.py
    - tests/test_ingestion/test_parsers.py
    - tests/test_ingestion/test_oai_pmh.py
    - tests/test_ingestion/test_arxiv_api.py
    - tests/fixtures/arxiv_raw_sample.xml
    - tests/fixtures/arxiv_format_sample.xml
    - tests/fixtures/oai_dc_sample.xml
  modified:
    - src/arxiv_mcp/cli.py
    - pyproject.toml

key-decisions:
  - "Used arXivRaw as primary harvest format for version history, arXiv format for structured authors, oai_dc as fallback"
  - "Category filtering applied post-parse: ingest broadly, filter to configured subset before DB insertion"
  - "JSON checkpoint file (data/harvest_checkpoint.json) for incremental harvest state, avoiding extra DB table in Phase 1"
  - "ON CONFLICT DO UPDATE preserves processing_tier, promotion_reason, source, fetched_at on upsert"
  - "Rate limiting built into ArxivAPIClient with configurable delay (default 3s)"
  - "parse_atom_entry() in arxiv_api.py rather than parsers.py since Atom format is API-specific"

patterns-established:
  - "TDD RED->GREEN->REFACTOR with separate commits for tests and implementation"
  - "Mock-based integration tests: mock oaipmh-scythe Scythe class with synthetic XML records"
  - "Mock httpx responses with sample Atom XML for API client tests"
  - "XML fixture files in tests/fixtures/ loaded via conftest helpers"
  - "Dataclass pipeline: XML -> RawPaperMetadata -> Paper ORM (two-stage transform)"

requirements-completed: [INGS-01, INGS-02, INGS-05]

# Metrics
duration: 8min
completed: 2026-03-09
---

# Phase 1 Plan 02: Ingestion Pipeline Summary

**OAI-PMH harvester with arXivRaw/arXiv/oai_dc XML parsers, arXiv API client, metadata mapper, and CLI commands for bulk/incremental/single-paper harvest**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-09T14:36:21Z
- **Completed:** 2026-03-09T14:44:58Z
- **Tasks:** 3
- **Files modified:** 15 created, 2 modified

## Accomplishments
- Three XML parsers covering all arXiv OAI-PMH metadata formats (arXivRaw with version history, arXiv with structured authors, oai_dc fallback)
- Metadata mapper converting any parsed format to canonical Paper ORM instances with correct date parsing, category splitting, and version history serialization
- OAI-PMH harvester with bulk and incremental modes, category filtering, batch upsert with ON CONFLICT dedup, and JSON checkpoint management
- arXiv search API client with single-paper fetch and fielded search, built-in rate limiting, and Atom XML parsing
- CLI commands (`harvest bulk`, `harvest incremental`, `harvest fetch`) with Rich progress display
- 20 passing tests with mocked external services (no real arXiv calls)

## Task Commits

Each task was committed atomically:

1. **Task 1: XML parsers and metadata mapper** - `8d9b280` (test/RED), `5735536` (feat/GREEN)
2. **Task 2: OAI-PMH harvester** - `5477609` (test/RED), `3ef8460` (feat/GREEN)
3. **Task 3: arXiv API client and CLI** - `cf5e730` (test/RED), `05ecdc4` (feat/GREEN)

## Files Created/Modified
- `src/arxiv_mcp/ingestion/parsers.py` - XML parsers for arXivRaw, arXiv, oai_dc formats with RawPaperMetadata/PaperVersion dataclasses
- `src/arxiv_mcp/ingestion/mapper.py` - Maps RawPaperMetadata to Paper ORM with date parsing, category splitting, version serialization
- `src/arxiv_mcp/ingestion/oai_pmh.py` - OAIPMHHarvester with bulk/incremental harvest, batch upsert, checkpoint management
- `src/arxiv_mcp/ingestion/arxiv_api.py` - ArxivAPIClient with fetch_paper/search, rate limiting, Atom XML parsing
- `src/arxiv_mcp/ingestion/cli.py` - Click CLI subgroup: harvest bulk/incremental/fetch commands
- `src/arxiv_mcp/cli.py` - Updated to register harvest subgroup
- `tests/fixtures/*.xml` - Sample XML fixtures for all three OAI-PMH formats
- `tests/test_ingestion/conftest.py` - Test fixtures loading XML files
- `tests/test_ingestion/test_parsers.py` - 8 parser/mapper tests
- `tests/test_ingestion/test_oai_pmh.py` - 7 harvester tests
- `tests/test_ingestion/test_arxiv_api.py` - 5 API client tests
- `pyproject.toml` - Added python-dateutil dependency

## Decisions Made
- **arXivRaw as primary format:** Used arXivRaw for bulk harvest (provides version history essential for time semantics), with arXiv format and oai_dc as secondary options.
- **Post-parse category filtering:** Parse all records, then filter to configured categories before DB insertion. This is simpler and naturally captures cross-listings.
- **JSON checkpoint file:** Used `data/harvest_checkpoint.json` for incremental harvest state rather than a separate database table. Simpler for Phase 1; can migrate to DB later if needed.
- **Upsert preservation:** ON CONFLICT DO UPDATE updates all metadata fields but preserves processing_tier, promotion_reason, source, and fetched_at to maintain provenance.
- **Atom parser placement:** parse_atom_entry() lives in arxiv_api.py rather than parsers.py since the Atom format is API-specific, not an OAI-PMH format.
- **python-dateutil added:** Required for parsing arXiv's varied date formats (e.g., "Mon, 2 Jan 2023 12:00:00 GMT") that datetime.fromisoformat cannot handle.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Added python-dateutil dependency**
- **Found during:** Task 1 (mapper implementation)
- **Issue:** arXiv date strings use RFC 2822 format ("Mon, 2 Jan 2023 12:00:00 GMT") which datetime.fromisoformat cannot parse. dateutil.parser handles all formats.
- **Fix:** Added python-dateutil to pyproject.toml dependencies.
- **Files modified:** pyproject.toml, uv.lock
- **Verification:** All date parsing tests pass
- **Committed in:** 5735536 (Task 1 GREEN commit)

---

**Total deviations:** 1 auto-fixed (1 blocking)
**Impact on plan:** Essential dependency for correct date parsing. No scope creep.

## Issues Encountered
- test_search directory contains tests from a previous Plan 01 execution that reference not-yet-implemented Plan 03 modules. These tests are excluded from the current test runs (they will pass once Plan 03 is complete).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Ingestion pipeline complete, ready for Plan 03 (search/browse)
- Papers can be harvested via CLI and inserted into database
- Parser/mapper infrastructure reusable for future enrichment adapters
- All 44 tests passing (24 from Plan 01 + 20 from Plan 02)

## Self-Check: PASSED

All 12 created files verified present. All 6 commit hashes verified in git log.

---
*Phase: 01-metadata-substrate*
*Completed: 2026-03-09*
