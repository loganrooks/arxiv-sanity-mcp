---
phase: 06-content-normalization
plan: 01
subsystem: database
tags: [sqlalchemy, pydantic, alembic, content-variants, rights, license]

# Dependency graph
requires:
  - phase: 04-enrichment-adapters
    provides: PaperEnrichment ORM pattern (composite PK, provenance columns)
provides:
  - ContentVariant ORM model with composite PK and provenance columns
  - VariantType, ContentStatus, AccessDecision, ContentConversionResult Pydantic models
  - RightsChecker with deployment-mode-aware license classification
  - Migration 008 (content_variants table)
  - Settings extension (deployment_mode, content_rate_limit, content_max_pdf_pages)
  - Test infrastructure (content_session_factory, sample data factories)
affects: [06-02-PLAN, 06-03-PLAN, content-service, mcp-content-tool]

# Tech tracking
tech-stack:
  added: []
  patterns: [rights-checker-pattern, deployment-mode-setting]

key-files:
  created:
    - src/arxiv_mcp/content/__init__.py
    - src/arxiv_mcp/content/models.py
    - src/arxiv_mcp/content/rights.py
    - alembic/versions/008_content_variants_table.py
    - tests/test_content/__init__.py
    - tests/test_content/test_models.py
    - tests/test_content/test_rights.py
    - tests/test_content/conftest.py
  modified:
    - src/arxiv_mcp/db/models.py
    - src/arxiv_mcp/config.py

key-decisions:
  - "RightsChecker uses set-based license classification (PERMISSIVE vs PERSONAL_USE) with unknown/None treated as restrictive"
  - "Local mode always allows access with informational warning; hosted mode blocks non-permissive licenses"
  - "ContentVariant follows PaperEnrichment pattern: composite PK, FK to papers, CHECK constraint on variant_type"
  - "quality_warnings stored as JSONB in ORM (list serialization) and list[str] in Pydantic (default_factory)"

patterns-established:
  - "RightsChecker pattern: stateless classifier with deployment_mode parameter for access decisions"
  - "Content test conftest: content_session_factory + sample_content_variant_data + sample_paper_with_license helpers"

requirements-completed: [CONT-01, CONT-02, CONT-03, CONT-06]

# Metrics
duration: 7min
completed: 2026-03-12
---

# Phase 06 Plan 01: Content Data Foundation Summary

**ContentVariant ORM model, Pydantic schemas, RightsChecker with 6-license classification, migration 008, and test infrastructure for content normalization**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-12T23:24:57Z
- **Completed:** 2026-03-12T23:31:40Z
- **Tasks:** 2
- **Files modified:** 10

## Accomplishments
- Complete content data layer: ContentVariant ORM, 4 Pydantic models, 2 enums
- RightsChecker correctly classifying all 6 arXiv license URIs in both local and hosted deployment modes
- Migration 008 for content_variants table with composite PK, FK, CHECK constraint, and index
- Settings extended with deployment_mode, content_rate_limit, content_max_pdf_pages
- Test infrastructure ready for Plan 02 adapters (conftest with session factory and sample data helpers)

## Task Commits

Each task was committed atomically:

1. **Task 1: Content Pydantic models, RightsChecker, and ORM model with tests** (TDD)
   - `74e12aa` (test: failing tests for content models and rights)
   - `8e024cf` (feat: implement content models, rights checker, and ORM model)
2. **Task 2: Migration 008, Settings extension, and test conftest** - `38f829f` (feat)

## Files Created/Modified
- `src/arxiv_mcp/content/__init__.py` - Content package with public exports
- `src/arxiv_mcp/content/models.py` - VariantType, ContentStatus, AccessDecision, ContentConversionResult
- `src/arxiv_mcp/content/rights.py` - RightsChecker with permissive/personal-use license classification
- `src/arxiv_mcp/db/models.py` - ContentVariant ORM model added (composite PK, provenance columns)
- `src/arxiv_mcp/config.py` - deployment_mode, content_rate_limit, content_max_pdf_pages settings
- `alembic/versions/008_content_variants_table.py` - Migration creating content_variants table
- `tests/test_content/__init__.py` - Test package marker
- `tests/test_content/test_models.py` - 21 tests for enums, Pydantic models, ORM model structure
- `tests/test_content/test_rights.py` - 14 tests for all license URIs x deployment modes
- `tests/test_content/conftest.py` - content_session_factory, sample_content_variant_data, sample_paper_with_license

## Decisions Made
- RightsChecker uses set-based license classification (PERMISSIVE vs PERSONAL_USE sets) with unknown/None treated as restrictive -- simple, extensible, consistent with ADR-0003
- Local mode always allows access with informational warning; hosted mode blocks non-permissive -- per ADR-0003 rights enforcement
- ContentVariant follows PaperEnrichment pattern: composite PK (arxiv_id, variant_type), FK to papers with CASCADE, CHECK constraint -- proven pattern from Phase 4
- quality_warnings as JSONB in ORM and list[str] in Pydantic -- natural serialization boundary

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- ContentVariant ORM model and Pydantic schemas ready for Plan 02 (abstract adapter and HTML fetcher)
- RightsChecker ready for Plan 02 service integration (called before content access)
- Test conftest with content_session_factory ready for Plan 02 integration tests
- Migration 008 ready for application against live DB when needed
- Settings extension supports deployment_mode switching and PDF page limits

## Self-Check: PASSED

All 10 files verified present. All 3 commits (74e12aa, 8e024cf, 38f829f) verified in git log.

---
*Phase: 06-content-normalization*
*Completed: 2026-03-12*
