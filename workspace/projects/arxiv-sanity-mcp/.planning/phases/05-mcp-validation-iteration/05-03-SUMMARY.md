---
phase: 05-mcp-validation-iteration
plan: 03
subsystem: mcp
tags: [validation, mcp-tools, evidence-based, batch-signals, doc-06, literature-review]

# Dependency graph
requires:
  - phase: 05-mcp-validation-iteration
    provides: "Import script (plan 01), 3 MCP prompts (plan 02), 9 tools + 4 resources"
provides:
  - "Evidence-based validation of full MCP surface (10 tools, 4 resources, 3 prompts)"
  - "Structured validation log with 13 observations across 7 workflow phases"
  - "Doc 06 open questions resolved with cited evidence"
  - "batch_add_signals tool for multi-signal profile updates"
affects: [phase-06-content-normalization, v2-planning]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "batch_add_signals: partial-success semantics (continue on individual errors, report summary)"
    - "Evidence-based MCP surface iteration: change only what validation observations demand"

key-files:
  created:
    - .planning/phases/05-mcp-validation-iteration/validation-log.md
    - .planning/phases/05-mcp-validation-iteration/doc-06-answers.md
  modified:
    - src/arxiv_mcp/mcp/tools/interest.py
    - src/arxiv_mcp/config.py
    - src/arxiv_mcp/ingestion/arxiv_api.py
    - src/arxiv_mcp/models/paper.py
    - tests/test_mcp/test_tool_names.py
    - tests/test_mcp/test_workflow_tools.py
    - docs/06-mcp-surface-options.md

key-decisions:
  - "batch_add_signals uses partial-success semantics: continues on individual errors, returns per-signal results"
  - "Result sets remain ephemeral in v1 (agents compensate via context window; persistence deferred to v2)"
  - "Option D (hybrid tools+resources+prompts) validated as correct MCP surface shape"
  - "All 5 doc 06 questions resolved with evidence from real MCP usage, not speculation"
  - "Profile vs collection ordering is irrelevant (independent concepts at different workflow stages)"

patterns-established:
  - "Evidence-based iteration: MCP surface changes must cite specific observations from validation-log.md"
  - "Batch tool pattern: accept list, process each, return summary with counts + per-item results"

requirements-completed: [MCPV-01, MCPV-02, MCPV-03]

# Metrics
duration: 27min
completed: 2026-03-12
---

# Phase 05 Plan 03: MCP Validation Session Summary

**Real literature review workflow validated against 126 imported papers; doc 06 resolved with evidence; batch_add_signals tool added based on observed friction**

## Performance

- **Duration:** 27 min
- **Started:** 2026-03-12T06:33:15Z
- **Completed:** 2026-03-12T07:00:59Z
- **Tasks:** 2 (+ 1 auto-approved checkpoint)
- **Files modified:** 9

## Accomplishments
- Executed complete literature review workflow through MCP tools: search (5 queries), triage (15 papers), collect (5 papers), expand (3 seeds, 15 unique related), profile (13 signals, profile-ranked search)
- Structured validation log with 13 observations across 7 workflow phases, documenting friction points and doc 06 relevance
- All 5 doc 06 open questions answered with specific observation citations from the validation session
- batch_add_signals MCP tool implemented with partial-success semantics (4 new tests, 84 MCP tests total)
- Updated docs/06-mcp-surface-options.md with resolved question markers and section 11 (validated surface)
- 403 total tests passing across full suite

## Task Commits

Each task was committed atomically:

1. **Task 1: Run import + execute validation session** - `60c461a` (feat)
2. **Task 2: Resolve doc 06 + iterate MCP surface** - `3711c6a` (feat)

## Files Created/Modified
- `.planning/phases/05-mcp-validation-iteration/validation-log.md` - 185-line structured observation log from MCP validation session
- `.planning/phases/05-mcp-validation-iteration/doc-06-answers.md` - Evidence-based answers to all 5 doc 06 open questions
- `src/arxiv_mcp/mcp/tools/interest.py` - Added batch_add_signals tool with partial-success semantics
- `src/arxiv_mcp/config.py` - Fixed arXiv API URL to HTTPS (was HTTP, 301 redirect broke imports)
- `src/arxiv_mcp/ingestion/arxiv_api.py` - Added follow_redirects=True to httpx client
- `src/arxiv_mcp/models/paper.py` - Made PaperSummary.oai_datestamp optional (None for API-fetched papers)
- `tests/test_mcp/test_tool_names.py` - Updated tool count 9->10, added batch_add_signals to expected set
- `tests/test_mcp/test_workflow_tools.py` - 4 new tests for batch_add_signals
- `docs/06-mcp-surface-options.md` - Section 10 resolved markers, section 11 validated surface table

## Decisions Made
- **batch_add_signals partial-success:** Continues processing on individual signal errors, returns per-signal results with overall counts. This is consistent with the existing error pattern (tools return `{"error": ...}` dicts) and avoids all-or-nothing batch semantics.
- **Result sets ephemeral for v1:** Observation C.1 showed agents compensate by keeping results in context. Persistence adds schema complexity (new table, new resource, new lifecycle) without clear v1 benefit.
- **Option D validated:** The hybrid tool+resource+prompt design is the correct MCP surface shape. No reclassification needed between tools and resources.
- **Profile/collection ordering irrelevant:** They serve different purposes (ranking vs organization) at different workflow stages. No sequencing constraint needed.
- **Enrichment blocked documented but not fixed:** Pre-existing schema mismatch (composite PK) prevents enrichment. Out of scope per deviation rules (not caused by Phase 5 changes).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed arXiv API URL to HTTPS**
- **Found during:** Task 1 (import script execution)
- **Issue:** config.py had `http://export.arxiv.org/api/query` but arXiv now redirects to HTTPS. httpx without follow_redirects=True raised 301 error, causing all 157 paper fetches to fail.
- **Fix:** Changed default URL to https://, added follow_redirects=True to AsyncClient
- **Files modified:** src/arxiv_mcp/config.py, src/arxiv_mcp/ingestion/arxiv_api.py
- **Verification:** Import successfully fetched 126/157 papers (31 failed with 429 rate limiting)
- **Committed in:** 60c461a

**2. [Rule 1 - Bug] Made PaperSummary.oai_datestamp optional**
- **Found during:** Task 1 (search phase of validation)
- **Issue:** Papers fetched via arXiv search API don't have oai_datestamp (it comes from OAI-PMH). PaperSummary required it as `date`, causing ValidationError when searching imported papers.
- **Fix:** Changed `oai_datestamp: date` to `oai_datestamp: date | None = None`
- **Files modified:** src/arxiv_mcp/models/paper.py
- **Verification:** Search queries return results successfully, 403 tests pass
- **Committed in:** 60c461a

---

**Total deviations:** 2 auto-fixed (2 bug fixes)
**Impact on plan:** Both fixes necessary for validation to proceed. No scope creep.

## Issues Encountered
- **arXiv API 429 rate limiting:** 31 of 157 papers failed to fetch due to rate limiting (3-second delay insufficient for sustained bulk import). Result: 126 papers imported, which is sufficient for validation (80% of corpus).
- **False-negative papers not imported:** All 4 false-negative papers (2501.11733, 2501.11425, 2510.23595, 2506.24119) were among the 429-failed papers. The false-negative surfacing test was inconclusive (data limitation, not tool limitation).
- **Enrichment schema mismatch:** EnrichmentService expects composite PK (arxiv_id, source_api) but DB has only arxiv_id PK. Pre-existing issue from Quick Task 1. Documented in validation-log.md as Observation 5.1. Out of scope for this plan.
- **Triage FK violations during import:** Papers that failed to fetch still attempted triage state setting, causing FK violations. Idempotent import design means this resolves on re-run (once papers exist).

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 5 validation complete: all 3 plans executed, requirements MCPV-01/02/03 satisfied
- MCP surface validated: 10 tools, 4 resources, 3 prompts
- Known issues for future work:
  - Enrichment schema migration needed (composite PK)
  - total_estimate=None for search/collection results
  - Seed provenance in find_related_papers
  - Error message improvement for triage_paper
- Phase 6 (content normalization) can proceed independently

## Self-Check: PASSED

All files exist. All commits verified.

---
*Phase: 05-mcp-validation-iteration*
*Completed: 2026-03-12*
