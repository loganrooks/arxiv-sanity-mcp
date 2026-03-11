---
phase: foundation-fixes
plan: 1
subsystem: database, interest-modeling, enrichment, documentation
tags: [alembic, sqlalchemy, composite-pk, check-constraint, openalex, ranking]

# Dependency graph
requires:
  - phase: 03-interest-modeling-ranking
    provides: InterestSignal ORM model, ranking pipeline, apply_negative_demotion
  - phase: 04-enrichment-adapters
    provides: PaperEnrichment ORM model, EnrichmentService, OpenAlexAdapter
provides:
  - "Extensible signal types (no DB migration needed for new types)"
  - "Multi-source enrichment support via composite PK (arxiv_id, source_api)"
  - "ADR-0001-compliant negative demotion (direct ID only, no category inference)"
  - "OpenAlex polite pool config (openalex_email setting)"
  - "Epistemic discipline guidelines for CONTEXT.md authoring"
affects: [05-content-normalization, 06-mcp-surface, enrichment-adapters]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Application-level type validation instead of DB CHECK constraints for extensible enums"
    - "Composite PK for multi-source enrichment records"
    - "User-Agent and mailto params for OpenAlex polite pool"

key-files:
  created:
    - alembic/versions/005_drop_signal_type_check.py
    - alembic/versions/006_enrichment_composite_pk.py
  modified:
    - src/arxiv_mcp/db/models.py
    - src/arxiv_mcp/enrichment/service.py
    - src/arxiv_mcp/enrichment/openalex.py
    - src/arxiv_mcp/interest/ranking.py
    - src/arxiv_mcp/config.py
    - tests/test_enrichment/test_service.py
    - tests/test_interest/test_profiles.py
    - tests/test_interest/test_ranking.py
    - docs/10-open-questions.md
    - .planning/REQUIREMENTS.md
    - AGENTS.md

key-decisions:
  - "Application-level validation for signal types instead of DB CHECK constraint"
  - "Composite PK (arxiv_id, source_api) for multi-source enrichment"
  - "Direct ID matching only for negative demotion per ADR-0001"
  - "openalex_email as Settings field with empty string default"

patterns-established:
  - "Extensible enum pattern: validate at application level, not DB level"
  - "CONTEXT.md epistemic discipline: separate grounded from inferred decisions"

requirements-completed: []

# Metrics
duration: 7min
completed: 2026-03-11
---

# Quick Task 1: Foundation Fixes Summary

**Extensible signal types via removed CHECK constraint, composite enrichment PK for multi-source support, ADR-0001-compliant direct-ID-only negative demotion, and epistemic discipline documentation**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-11T01:08:47Z
- **Completed:** 2026-03-11T01:16:38Z
- **Tasks:** 3
- **Files modified:** 14

## Accomplishments
- Signal types can now be extended without DB migrations (CHECK constraint removed, validated at application level)
- Multiple enrichment sources can store data for the same paper via composite PK (arxiv_id, source_api)
- Negative demotion no longer penalizes innocent papers sharing categories with negative examples (ADR-0001 compliance)
- OpenAlex polite pool access configurable via openalex_email setting
- Open Questions Q1, Q4, Q16 annotated as provisionally resolved
- Five requirements annotated with [chosen for now] provenance markers
- AGENTS.md gains epistemic discipline section for CONTEXT.md authoring

## Task Commits

Each task was committed atomically:

1. **Task 1: Schema migrations** - `9b5d86b` (feat)
2. **Task 2: Remove category demotion, add openalex_email** - `70f0f0f` (fix)
3. **Task 3: Documentation annotations** - `7570d4c` (docs)

## Files Created/Modified
- `alembic/versions/005_drop_signal_type_check.py` - Migration to drop ck_signal_type_valid CHECK constraint
- `alembic/versions/006_enrichment_composite_pk.py` - Migration to change PK to (arxiv_id, source_api)
- `src/arxiv_mcp/db/models.py` - ORM: removed signal_type CHECK, added PrimaryKeyConstraint for enrichment
- `src/arxiv_mcp/enrichment/service.py` - Composite PK lookups, upserts with both conflict columns
- `src/arxiv_mcp/enrichment/openalex.py` - User-Agent and mailto from openalex_email setting
- `src/arxiv_mcp/interest/ranking.py` - Direct ID matching only in apply_negative_demotion
- `src/arxiv_mcp/config.py` - Added openalex_email setting
- `tests/test_enrichment/test_service.py` - Updated all session.get calls for composite PK
- `tests/test_interest/test_profiles.py` - Updated signal_type CHECK test to verify extensibility
- `tests/test_interest/test_ranking.py` - Added category-overlap-does-not-demote regression test
- `docs/10-open-questions.md` - Q1, Q4, Q16 annotated as provisionally resolved
- `.planning/REQUIREMENTS.md` - CONT-05, INTR-04, INTR-05, MCP-05, MCP-07 annotated with provenance
- `AGENTS.md` - Added epistemic discipline section

## Decisions Made
- **Application-level validation for signal types**: Removed DB CHECK constraint in favor of VALID_SIGNAL_TYPES set in signals.py. New signal types can be added without migrations. Downgrade migration restores the original constraint if needed.
- **Composite PK approach**: Used PrimaryKeyConstraint in ORM rather than mapped_column(primary_key=True) on both columns. This keeps the FK relationship on arxiv_id clean while allowing source_api to default to "openalex".
- **get_enrichment_status backward compatibility**: Added optional source_api parameter defaulting to "openalex" so existing callers (CLI, etc.) continue to work without changes.
- **Direct ID matching only**: Removed category-based inference from negative demotion. This is a behavioral change that aligns with ADR-0001's exploration-first principle -- sharing categories with a disliked paper should not penalize a paper the user has never seen.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed test_check_constraint_rejects_invalid_signal_type**
- **Found during:** Task 1
- **Issue:** Test expected IntegrityError for invalid signal_type, but CHECK constraint was removed
- **Fix:** Changed test to verify novel signal types are now accepted by DB (test_novel_signal_type_accepted_by_db)
- **Files modified:** tests/test_interest/test_profiles.py
- **Committed in:** 9b5d86b (Task 1 commit)

**2. [Rule 1 - Bug] Fixed test_get_enrichment_status with composite PK**
- **Found during:** Task 1
- **Issue:** get_enrichment_status defaulted to source_api="openalex" but MockAdapter uses "mock_openalex"
- **Fix:** Updated test to pass source_api="mock_openalex" explicitly
- **Files modified:** tests/test_enrichment/test_service.py
- **Committed in:** 9b5d86b (Task 1 commit)

---

**Total deviations:** 2 auto-fixed (2 bugs from plan-specified changes)
**Impact on plan:** Both fixes were direct consequences of the planned changes. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required. The openalex_email setting is optional and defaults to empty string.

## Next Phase Readiness
- Foundation issues from epistemic audit are resolved
- Schema supports future enrichment sources without additional migrations
- Signal type extensibility enables future interest modeling without DB changes
- Epistemic discipline guidelines ready for use in Phase 5+ CONTEXT.md files

## Self-Check: PASSED

All 14 files verified present. All 3 task commits verified in git log. Full test suite: 307 passed.

---
*Phase: foundation-fixes (quick task)*
*Completed: 2026-03-11*
