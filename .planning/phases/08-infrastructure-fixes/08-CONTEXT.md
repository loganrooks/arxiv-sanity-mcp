# Phase 8: Infrastructure Fixes (GAP CLOSURE) - Context

**Gathered:** 2026-03-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Fix 4 pre-existing infrastructure issues identified during v1 audit: enrichment schema mismatch blocking live enrichment, test fixture duplication/conflicts, stale docstring reference, and eager import propagation. Pure remediation — no new features, no new architecture.

</domain>

<decisions>
## Implementation Decisions

### Migration execution (SC-1)
- Fully automated: `alembic upgrade head` applies migrations 005-008 in sequence
- Pre-flight: log target database URL before running to prevent wrong-DB execution
- Automated verification: `alembic current` must report migration 008
- No human checkpoint — research confirmed existing data is safe (all rows have source_api='openalex' server_default, arxiv_id was previously unique, no duplicate composite keys possible)
- Downgrade path exists (`alembic downgrade`) as documented escape hatch

### Test fixture consolidation (SC-2)
- Deduplicate only — import TSVECTOR SQL, sample_paper_data, test_engine, test_session from root conftest into workflow and interest conftest files
- Do NOT standardize cleanup strategy (TRUNCATE vs drop_all/create_all) — that's a separate concern from SC-2's duplication problem
- Use root conftest's richer factory defaults as canonical; tests that depend on simplified defaults get explicit overrides
- Domain-specific factories (sample_collection_data, sample_profile_data, etc.) stay in their module conftest files — follows the established pattern from search/enrichment/content
- Run full test suite after each conftest modification to catch value-dependent assertion failures

### Docstring fix (SC-3)
- Minimum fix: change "Run get_delta" to reference `watch://{slug}/deltas` resource
- Do NOT expand docstring with parameter/return documentation — that's separate scope
- Add docstring assertion regression test following the Phase 04.1 pattern
- Assert on "watch://" + "/deltas" substring — specific enough to catch regression, not so brittle it breaks on formatting

### Import cleanup (SC-4 — expanded scope)
- Remove ALL re-exports from `content/__init__.py`, not just `fetch_arxiv_html`
- Rationale: the spirit of SC-4 is "no eager import propagation." All re-exports in `__init__.py` share the same pathology — eagerly importing adapters (pulls Marker lib), html_fetcher (pulls httpx/bs4), and service (pulls everything transitively)
- **CONSTRAINT:** Before removing re-exports, planner MUST verify no code imports from `arxiv_mcp.content` package level (grep for `from arxiv_mcp.content import`). If consumers found: update their imports to use submodule paths (e.g., `from arxiv_mcp.content.service import ContentService`), then remove re-exports
- Empty or removed `__all__` is acceptable — this package is not used with wildcard imports
- Regression test: verify `from arxiv_mcp.content.models import VariantType` does not load httpx/bs4/marker

### Claude's Discretion
- Exact sample_paper_data default values for consolidated factory (use root conftest's richer version)
- Whether to remove `__all__` entirely or leave it empty in content/__init__.py
- Test fixture function naming consistency (test_engine vs domain-prefixed names)
- Alembic downgrade documentation format in plan
- Docstring assertion test exact matching strategy

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/conftest.py`: Root conftest with TSVECTOR SQL, sample_paper_data, test_engine, test_session — the consolidation target
- `tests/test_search/conftest.py`: Exemplar of correct pattern — imports from root conftest, adds domain-specific data
- `tests/test_enrichment/conftest.py`: Exemplar of correct pattern — imports from root, adds enrichment fixtures
- `tests/test_content/conftest.py`: Exemplar of correct pattern — imports from root, adds content fixtures with TRUNCATE cleanup
- Phase 04.1 docstring assertion test pattern in `test_workflow_tools.py`

### Established Patterns
- Central conftest with module-specific imports (search/enrichment/content already follow this)
- Function-scoped async engine fixtures (Phase 01 decision: avoids asyncpg event loop conflicts)
- Docstring regression tests using substring assertions (Phase 04.1)
- `content/service.py` already imports `fetch_arxiv_html` directly from submodule (line 25) — no dependency on package-level re-export

### Integration Points
- `tests/test_workflow/conftest.py`: Remove TSVECTOR SQL (3 constants), sample_paper_data, test_engine, test_session; add imports from root
- `tests/test_interest/conftest.py`: Same removal/import pattern as workflow
- `src/arxiv_mcp/content/__init__.py`: Remove all import statements and __all__; verify no consumers first
- `src/arxiv_mcp/mcp/tools/workflow.py`: Single docstring edit at create_watch function
- Live database `arxiv_mcp`: Target for alembic upgrade head (migrations 005-008)

</code_context>

<specifics>
## Specific Ideas

### Dialectical consistency note
For imports: chose "spirit over letter" (broader than SC-4 literal). For fixtures: chose "letter over spirit" (minimum SC-2). The principle is coherent: fix the identified problem thoroughly within its problem class, but don't fix adjacent problems. Import re-exports all share the same pathology; fixture cleanup strategy is a different concern from duplication.

### Failure modes to guard against
1. **Import removal breaks consumers** (MEDIUM risk) — grep for package-level imports before removing re-exports. If found, update consumers first.
2. **Factory deduplication breaks value-dependent tests** (MEDIUM risk) — run full suite after each conftest change. Tests with simplified defaults may need explicit overrides.
3. **Migration hits wrong DB** (LOW risk) — pre-flight URL logging.
4. **Docstring test too brittle** (LOW risk) — use substring matching, not exact text.

### Analysis method
Context generated via 6-layer epistemic analysis: assumptions, grey area identification (material/formal/efficient/final), prioritization by reversibility, dialectical consistency check, failure mode analysis, and iterative convergence.

</specifics>

<deferred>
## Deferred Ideas

- Standardize all test cleanup to TRUNCATE CASCADE (Phase 06-04 pattern) — a preventive measure against parallel execution bugs, but separate scope from SC-2
- Expand create_watch docstring with full parameter/return documentation — separate from SC-3 resource reference fix
- Add __getattr__ lazy loading to content/__init__.py as backwards-compatible alternative — unnecessary if no package-level consumers exist
- Alembic-managed test database (run migrations in tests instead of create_all) — would catch migration issues in tests but adds complexity

</deferred>

---

*Phase: 08-infrastructure-fixes*
*Context gathered: 2026-03-13 via 6-layer epistemic analysis*
