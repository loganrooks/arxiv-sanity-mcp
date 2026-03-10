---
phase: 03-interest-modeling-ranking
plan: 01
subsystem: database
tags: [sqlalchemy, pydantic, alembic, interest-profiles, signals, provenance]

# Dependency graph
requires:
  - phase: 01-metadata-substrate
    provides: Paper ORM model with arxiv_id PK for seed paper/negative example FK targets
  - phase: 02-workflow-state
    provides: SavedQuery ORM model for saved query signal references; slugify utility; service DI pattern
provides:
  - InterestProfile and InterestSignal ORM models with constraints and indexes
  - Pydantic schemas (ProfileSummary, ProfileDetail, SignalInfo) for API responses
  - ProfileService with full CRUD and signal management for all 4 signal types
  - Signal validation and author name normalization utilities
  - Alembic migration 003 for interest_profiles and interest_signals tables
affects: [03-02-ranking-pipeline, 03-03-suggestions-cli, 04-mcp-surface]

# Tech tracking
tech-stack:
  added: []
  patterns: [interest-signal-type-discriminator, warn-not-error-for-deleted-fk-targets, counter-based-signal-aggregation]

key-files:
  created:
    - src/arxiv_mcp/interest/__init__.py
    - src/arxiv_mcp/interest/signals.py
    - src/arxiv_mcp/interest/profiles.py
    - src/arxiv_mcp/models/interest.py
    - alembic/versions/003_interest_tables.py
    - tests/test_interest/__init__.py
    - tests/test_interest/conftest.py
    - tests/test_interest/test_profiles.py
  modified:
    - src/arxiv_mcp/db/models.py
    - src/arxiv_mcp/config.py

key-decisions:
  - "Single InterestSignal table with signal_type discriminator (not per-type tables) for uniform querying and simpler schema"
  - "Saved query signals use warn-not-error for non-existent queries (resilient to deleted queries per 03-CONTEXT.md)"
  - "Author name normalization via lowercase + whitespace collapse (exact match, not fuzzy) for deterministic deduplication"
  - "Application-level duplicate check before DB constraint to provide descriptive error messages"

patterns-established:
  - "Interest signal type discriminator: single table with CHECK constraint for 4 signal types"
  - "Counter-based signal aggregation: Python Counter on loaded signals for type/source counts"
  - "Provenance on all signals: source (manual/suggestion/agent), status (active/pending/dismissed), added_at, reason"

requirements-completed: [INTR-01, INTR-02, INTR-03, INTR-04, INTR-05]

# Metrics
duration: 7min
completed: 2026-03-10
---

# Phase 3 Plan 01: Interest Profile Data Model Summary

**InterestProfile/InterestSignal ORM models with ProfileService CRUD, signal management for 4 types (seed_paper, saved_query, followed_author, negative_example), and 42 passing integration tests**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-10T00:53:31Z
- **Completed:** 2026-03-10T01:00:46Z
- **Tasks:** 2
- **Files modified:** 11

## Accomplishments
- InterestProfile and InterestSignal ORM models with CHECK constraints, unique constraints, cascade delete, and indexes
- ProfileService with full CRUD lifecycle (create, list, get, rename, archive/unarchive, delete)
- Signal management for all 4 types with FK validation, author normalization, duplicate detection, and provenance tracking
- 42 integration tests covering ORM round-trips, constraint enforcement, service CRUD, all signal types, and soft limit warnings

## Task Commits

Each task was committed atomically:

1. **Task 1: ORM models, Pydantic schemas, migration, and test infrastructure** - `c80c870` (feat)
2. **Task 2: ProfileService with CRUD and signal management** - `43ed728` (feat)

## Files Created/Modified
- `src/arxiv_mcp/db/models.py` - Added InterestProfile and InterestSignal ORM models with constraints
- `src/arxiv_mcp/models/interest.py` - Pydantic schemas: SignalInfo, ProfileSummary, ProfileDetail, request schemas
- `src/arxiv_mcp/interest/__init__.py` - Interest module package
- `src/arxiv_mcp/interest/signals.py` - Signal validation, author normalization, signal type constants
- `src/arxiv_mcp/interest/profiles.py` - ProfileService with CRUD, signal management, convenience wrappers
- `src/arxiv_mcp/config.py` - Added soft_limit_profiles and default_negative_weight settings
- `alembic/versions/003_interest_tables.py` - Migration for interest_profiles and interest_signals tables
- `tests/test_interest/__init__.py` - Test package
- `tests/test_interest/conftest.py` - Test fixtures, factories, session setup
- `tests/test_interest/test_profiles.py` - 42 integration tests across 10 test classes

## Decisions Made
- Single InterestSignal table with signal_type discriminator column (not per-type tables) -- enables uniform querying and simpler schema, same pattern as TriageLog
- Saved query signals use warn-not-error when the referenced SavedQuery doesn't exist -- per resilience decision in 03-CONTEXT.md, signals survive deleted queries
- Author name normalization uses lowercase + whitespace collapse (exact match, not fuzzy) -- deterministic and sufficient for Phase 3; OpenAlex author disambiguation can enhance this in Phase 4
- Application-level duplicate check runs before hitting DB unique constraint -- provides descriptive error messages with profile slug and signal details
- signal_counts_by_type and signal_counts_by_source computed from active signals only using Python Counter on loaded signals

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- InterestProfile and InterestSignal tables provide the data foundation for Plan 02 (ranking pipeline)
- ProfileService provides the API that Plan 03 (CLI) will consume
- All 4 signal types are functional and tested, ready for ranking signal extraction
- Provenance fields (source, status, reason) ready for suggestion system in Plan 03

## Self-Check: PASSED

All 10 created/modified files verified present. Both task commits (c80c870, 43ed728) verified in git log.

---
*Phase: 03-interest-modeling-ranking*
*Completed: 2026-03-10*
