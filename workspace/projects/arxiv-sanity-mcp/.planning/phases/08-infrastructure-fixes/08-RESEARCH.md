# Phase 8: Infrastructure Fixes (GAP CLOSURE) - Research

**Researched:** 2026-03-13
**Domain:** Database migration, test fixture architecture, Python import patterns, docstring accuracy
**Confidence:** HIGH

## Summary

Phase 8 addresses four pre-existing infrastructure issues identified during the v1 audit. Each issue is concrete, locally scoped, and independently verifiable. No new libraries, patterns, or architectural decisions are needed -- this is pure remediation of known tech debt.

The most impactful issue is the enrichment schema mismatch: the live database sits at Alembic migration 004 (single-column PK on `paper_enrichments`) while the ORM model and service code expect the composite PK `(arxiv_id, source_api)` introduced by migration 006. This blocks `enrich_paper` against the live database. The remaining three issues are lower severity: duplicated test fixture definitions across conftest files, a stale docstring reference in `create_watch`, and eager import propagation from `content/__init__.py`.

**Primary recommendation:** Run pending Alembic migrations (005-008) against the live database, consolidate duplicated test fixtures into root `conftest.py` with import rewiring in workflow/interest tests, fix the `create_watch` docstring to reference `watch://{slug}/deltas`, and strip all re-exports from `content/__init__.py`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Migration execution (SC-1):** Fully automated `alembic upgrade head` for migrations 005-008. Pre-flight URL logging. Automated `alembic current` verification. No human checkpoint. Downgrade path as documented escape hatch.
- **Test fixture consolidation (SC-2):** Deduplicate only -- import TSVECTOR SQL, sample_paper_data, test_engine, test_session from root conftest. Do NOT standardize cleanup strategy (TRUNCATE vs drop_all/create_all). Use root conftest's richer factory defaults as canonical. Domain-specific factories stay in module conftest files. Run full test suite after each conftest modification.
- **Docstring fix (SC-3):** Minimum fix: change "Run get_delta" to reference `watch://{slug}/deltas`. Do NOT expand docstring. Add docstring assertion regression test following Phase 04.1 pattern. Assert on "watch://" + "/deltas" substring.
- **Import cleanup (SC-4 -- expanded scope):** Remove ALL re-exports from `content/__init__.py`, not just `fetch_arxiv_html`. Before removing, verify no code imports from package level. Update consumers if found, then remove. Regression test: verify `from arxiv_mcp.content.models import VariantType` does not load httpx/bs4/marker.

### Claude's Discretion
- Exact sample_paper_data default values for consolidated factory (use root conftest's richer version)
- Whether to remove `__all__` entirely or leave it empty in content/__init__.py
- Test fixture function naming consistency (test_engine vs domain-prefixed names)
- Alembic downgrade documentation format in plan
- Docstring assertion test exact matching strategy

### Deferred Ideas (OUT OF SCOPE)
- Standardize all test cleanup to TRUNCATE CASCADE
- Expand create_watch docstring with full parameter/return documentation
- Add __getattr__ lazy loading to content/__init__.py
- Alembic-managed test database (run migrations in tests instead of create_all)
</user_constraints>

## Standard Stack

### Core

No new libraries needed. All fixes use existing project dependencies.

| Library | Version | Purpose | Already Installed |
|---------|---------|---------|-------------------|
| alembic | >=1.14 | Database migration runner | Yes |
| sqlalchemy[asyncio] | >=2.0 | ORM model definition, PrimaryKeyConstraint | Yes |
| asyncpg | >=0.30 | Async PostgreSQL driver | Yes |
| pytest-asyncio | >=0.24 | Async test fixture support | Yes (dev) |

### Supporting

No additional libraries.

### Alternatives Considered

None -- all fixes use existing infrastructure.

## Architecture Patterns

### Recommended Project Structure (Post-Consolidation)

```
tests/
  conftest.py                 # CENTRAL: engine, session, paper factory, tsvector SQL
  test_workflow/
    conftest.py               # IMPORTS from tests.conftest; KEEPS workflow-specific factories
  test_interest/
    conftest.py               # IMPORTS from tests.conftest; KEEPS interest-specific factories
  test_search/
    conftest.py               # ALREADY correct pattern (imports from root)
  test_enrichment/
    conftest.py               # ALREADY correct pattern (imports from root)
  test_content/
    conftest.py               # ALREADY correct pattern (imports from root)
  test_mcp/
    conftest.py               # Mock-based (no DB fixtures -- unaffected)
```

### Pattern 1: Alembic Migration Execution

**What:** Run pending migrations 005-008 against the live database to align schema with code expectations.
**When to use:** When ORM model diverges from live DB schema.
**Current state (verified by direct inspection):**

```
Live DB (arxiv_mcp):      migration 004 (single-column PK on paper_enrichments)
Test DB (arxiv_mcp_test): no alembic_version table (tests use create_all/drop_all)
ORM model:                composite PK (arxiv_id, source_api) via PrimaryKeyConstraint
.env DATABASE_URL:        postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp
```

**Key finding:** The enrichment service upserts with `on_conflict_do_update(index_elements=["arxiv_id", "source_api"])`. This fails against the live DB because `source_api` is not part of the PK constraint. All four migrations must be applied in sequence:
- 005: Drop signal_type CHECK constraint (extensible signal types)
- 006: Enrichment composite PK `(arxiv_id, source_api)`
- 007: Add `seen` triage state to CHECK constraint
- 008: Create `content_variants` table

**Data safety analysis (HIGH confidence):**
- All existing `paper_enrichments` rows have `source_api = 'openalex'` (server_default)
- `arxiv_id` was previously unique PK, so no duplicate `(arxiv_id, source_api)` pairs can exist
- Migration 005 only drops a CHECK constraint -- no data risk
- Migration 007 only modifies a CHECK constraint -- no data risk
- Migration 008 creates a new table -- no data risk

**Command sequence:**
```bash
# Pre-flight: verify target database
python -c "from arxiv_mcp.config import get_settings; print(get_settings().database_url)"

# Run all pending migrations
alembic upgrade head
# Expected: 004 -> 005 -> 006 -> 007 -> 008

# Verify final state
alembic current
# Expected: 008 (head)
```

**Alembic env.py (verified):** Reads `database_url` from `get_settings()`, which reads from `.env`. The `.env` file points to `localhost:5432/arxiv_mcp`. Pre-flight URL logging prevents wrong-DB execution.

### Pattern 2: Centralized Test Fixture Architecture

**What:** Consolidate duplicated fixture definitions into the root `tests/conftest.py`.
**When to use:** When identical code appears in multiple conftest files.

**Duplication inventory (verified by direct code reading):**

| Item | Root | Workflow | Interest | Search | Enrichment | Content |
|------|------|----------|----------|--------|------------|---------|
| TSVECTOR_FUNCTION_SQL | defined | DUPLICATE | DUPLICATE | imports root | imports root | imports root |
| TSVECTOR_DROP_TRIGGER_SQL | defined | DUPLICATE | DUPLICATE | imports root | imports root | imports root |
| TSVECTOR_CREATE_TRIGGER_SQL | defined | DUPLICATE | DUPLICATE | imports root | imports root | imports root |
| sample_paper_data() | defined | DUPLICATE | DUPLICATE | imports root | imports root | imports root |
| test_engine fixture | defined | DUPLICATE | DUPLICATE | own (search_engine) | uses root | uses root |
| test_session fixture | defined | DUPLICATE | DUPLICATE | own (search_session) | own (enrichment_session_factory) | own (content_session_factory) |

**Default divergence analysis (critical for consolidation):**

The duplicated `sample_paper_data()` factories have different defaults:

| Field | Root conftest | Workflow conftest | Interest conftest |
|-------|---------------|-------------------|-------------------|
| authors_text | "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit" | "Ashish Vaswani, Noam Shazeer" | "Ashish Vaswani, Noam Shazeer" |
| abstract | 5-sentence paragraph (~300 chars) | Single sentence (~60 chars) | Single sentence (~60 chars) |
| categories | "cs.CL cs.AI cs.LG" | "cs.CL cs.AI" | "cs.CL cs.AI" |
| category_list | ["cs.CL", "cs.AI", "cs.LG"] | ["cs.CL", "cs.AI"] | ["cs.CL", "cs.AI"] |
| doi | "10.48550/arXiv.2301.00001" | None | None |
| comments | "15 pages, 5 figures" | "15 pages" | "15 pages" |
| version_history | [v1, v2 dicts] | None | None |

**Import impact analysis (verified by grep):**

Workflow test files that import `sample_paper_data` from `.conftest`:
- `test_search_augment.py` -- also imports TSVECTOR constants
- `test_queries.py` -- also imports `sample_saved_query_data`
- `test_export.py` -- also imports TSVECTOR constants
- `test_watches.py` -- also imports TSVECTOR constants

Interest test files that import `sample_paper_data` from `.conftest`:
- `test_suggestions.py` -- also imports `sample_profile_data`, `sample_saved_query_data`, `sample_signal_data`

**Critical finding:** No workflow or interest test asserts on the default values of `authors_text`, `abstract`, `doi`, `categories`, `comments`, or `version_history`. All uses of `sample_paper_data()` in these test files pass explicit overrides for the fields they care about (arxiv_id, title, authors_text, abstract). The default divergence is therefore safe to unify -- using the root conftest's richer defaults will not break any assertions.

**Consolidation approach:**
1. Remove duplicated constants and `sample_paper_data` from workflow/interest conftest
2. Add imports from `tests.conftest` (matching the enrichment/content pattern)
3. Remove duplicated `test_engine` and `test_session` fixtures from workflow/interest conftest
4. Keep domain-specific factories in their module conftest:
   - workflow: `sample_collection_data`, `sample_triage_data`, `sample_saved_query_data`, `sample_papers` fixture
   - interest: `sample_profile_data`, `sample_signal_data`, `sample_saved_query_data`, `session_factory`, `sample_papers`, `sample_saved_query` fixtures
5. Update relative imports in test files: `from .conftest import sample_paper_data` -> `from tests.conftest import sample_paper_data`

**Note on `sample_saved_query_data`:** Both workflow and interest conftest define identical `sample_saved_query_data` factories. Per the locked decision, domain-specific factories stay in their module conftest files. Since these are independently used and identical, keeping both is acceptable (they're domain-specific in context even if identical in content).

### Pattern 3: Import Cleanup in `content/__init__.py`

**What:** Remove ALL re-exports from `content/__init__.py` to prevent eager import propagation.
**When to use:** When a package `__init__.py` eagerly imports modules with heavy external dependencies.

**Current state (verified by runtime test):**

```python
# content/__init__.py -- current (eager)
from arxiv_mcp.content.adapters import ContentAdapter, MarkerAdapter, MockContentAdapter
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
from arxiv_mcp.content.models import AccessDecision, ContentConversionResult, ContentStatus, VariantType
from arxiv_mcp.content.rights import RightsChecker
from arxiv_mcp.content.service import ContentService
```

**Runtime verification results:** Importing `from arxiv_mcp.content.models import VariantType` triggers loading of:
- `arxiv_mcp.content` (the `__init__.py`)
- `arxiv_mcp.content.adapters` (pulls marker dependency chain)
- `arxiv_mcp.content.html_fetcher` (pulls httpx + bs4)
- `arxiv_mcp.content.service` (pulls everything transitively)
- httpx (30+ submodules)
- bs4 (12+ submodules)

**Consumer analysis (verified by grep):**
- `from arxiv_mcp.content import ...` -- **zero matches** in `src/`
- `from arxiv_mcp.content import ...` -- **zero matches** in `tests/`
- All consumers already use direct submodule imports (e.g., `from arxiv_mcp.content.service import ContentService`)

**Fix:** Remove all import statements and `__all__` from `content/__init__.py`. Keep only the module docstring. This is safe because no code uses package-level imports.

**Regression test design:** After the fix, verify that `from arxiv_mcp.content.models import VariantType` does NOT cause httpx or bs4 to appear in `sys.modules`.

### Pattern 4: Docstring Fix with Regression Test

**What:** Update `create_watch` tool docstring to reference the `watch://{slug}/deltas` resource instead of the non-existent `get_delta` tool.

**Current state (verified, line 73 of workflow.py):**
```python
    """Create a monitored search that tracks new papers matching your query.

    Run get_delta to see papers added since your last check.
    """
```

**Correct reference:** The actual mechanism for getting deltas is the `watch://{slug}/deltas` MCP resource (defined in `src/arxiv_mcp/mcp/resources/watch.py`). The daily_digest prompt already uses this reference correctly.

**Fix:**
```python
    """Create a monitored search that tracks new papers matching your query.

    Read the watch://{slug}/deltas resource to see papers added since your last check.
    """
```

**Existing docstring assertion pattern (Phase 04.1, verified):**
```python
# tests/test_interest/test_search_augment.py
class TestPaginationDocumentation:
    def test_ranked_search_pagination_documented(self):
        doc = ProfileRankingService._ranked_search.__doc__
        assert doc is not None, "_ranked_search must have a docstring"
        assert "approximate" in doc.lower(), (...)
```

**No existing docstring test for `create_watch`** -- confirmed by grep across all test files. This is a Wave 0 gap that needs to be created.

**Regression test design:** Assert `create_watch.__doc__` contains "watch://" and "/deltas" substrings. Do NOT assert on "get_delta" absence (too brittle if other tools legitimately reference it).

### Anti-Patterns to Avoid

- **Do NOT standardize cleanup strategy** during fixture consolidation (TRUNCATE vs drop_all/create_all mixing is explicitly out of scope per locked decision)
- **Do NOT expand the create_watch docstring** beyond fixing the resource reference (separate scope)
- **Do NOT add `__getattr__` lazy loading** to content/__init__.py (unnecessary since no consumers exist)
- **Do NOT run alembic migrations in tests** (keep create_all for test DB -- simpler, faster)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| DB schema migration | Manual SQL against live DB | `alembic upgrade head` | Alembic tracks state, handles rollback, is already configured |
| Test fixture deduplication | Copy-paste factories | Import from root conftest.py | Already working pattern in enrichment/content tests |
| Lazy imports | Custom import hooks | Remove from `__init__.py` | No consumers exist, removal is sufficient |
| Docstring regression | Manual code review | Assertion test on `__doc__` | Phase 04.1 pattern already established |

## Common Pitfalls

### Pitfall 1: Running Migrations Against Wrong Database
**What goes wrong:** `alembic upgrade head` runs against the database URL in settings/.env. If `.env` has been modified or an environment variable overrides `DATABASE_URL`, migrations could hit the wrong target.
**Why it happens:** Alembic's `env.py` reads from `get_settings()` which loads `.env` and environment variables.
**How to avoid:** Pre-flight: print and log the resolved `database_url` before running. Verify it points to `localhost:5432/arxiv_mcp`. The `.env` file (verified) correctly sets `DATABASE_URL=postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp`.
**Warning signs:** Migration says "0 rows affected" when you expect data, or connects to unexpected host.

### Pitfall 2: Test Fixture Import Rewiring
**What goes wrong:** After removing `sample_paper_data` from workflow/interest conftest, test files that import it via `from .conftest import sample_paper_data` will break with ImportError.
**Why it happens:** The consolidation removes the local definition but does not update consumers.
**How to avoid:** When removing a function from a module conftest, simultaneously update all test files that import it to use `from tests.conftest import sample_paper_data` instead. Do not attempt to re-export from the module conftest (that recreates the duplication problem).
**Warning signs:** ImportError mentioning `cannot import name 'sample_paper_data' from '.conftest'`.

### Pitfall 3: TSVECTOR Constants Still Needed in Workflow/Interest Conftest
**What goes wrong:** Several workflow test files import TSVECTOR constants from `.conftest` to set up their own session_factory fixtures (e.g., `test_search_augment.py` lines 34-38). If TSVECTOR constants are removed from the module conftest without updating these inline session_factory fixtures, tests break.
**Why it happens:** Some workflow/interest tests define their own `session_factory` fixture that uses TSVECTOR constants directly, even though there's a `test_session` fixture that already handles this.
**How to avoid:** After removing TSVECTOR constants from module conftest, update inline session_factory fixtures in test files to import from `tests.conftest` instead. OR: let these test files import TSVECTOR from `tests.conftest` directly.
**Warning signs:** NameError for TSVECTOR_FUNCTION_SQL in test files.

### Pitfall 4: Default Value Dependency in Tests
**What goes wrong:** Consolidating `sample_paper_data()` factories with different defaults may break tests that implicitly depend on the simplified defaults (e.g., workflow's `doi: None` vs root's `doi: "10.48550/arXiv.2301.00001"`).
**Why it happens:** Each conftest evolved independently with slightly different defaults.
**How to avoid:** Verified by grep: no workflow or interest test asserts on default values of `doi`, `abstract`, `authors_text`, `categories`, `comments`, or `version_history`. All callers pass explicit overrides. This pitfall is therefore LOW risk for this specific codebase but should still be verified by running the full test suite after consolidation.
**Warning signs:** Assertion failures on field values that the test didn't explicitly set.

### Pitfall 5: Migration 006 on DB With Existing Enrichment Data
**What goes wrong:** Migration 006 changes PK from `(arxiv_id)` to `(arxiv_id, source_api)`. If duplicate `(arxiv_id, source_api)` pairs existed, the migration would fail.
**Why it happens:** Theoretical concern about data integrity during PK change.
**How to avoid:** All existing enrichment rows have `source_api = 'openalex'` (server_default). Since `arxiv_id` was previously unique, no duplicate composite keys can exist. This is safe.
**Warning signs:** Migration fails with "duplicate key violates unique constraint" -- would indicate unexpected data.

## Code Examples

### Running Pending Migrations (SC-1)

```bash
# Pre-flight: verify target database
python -c "from arxiv_mcp.config import get_settings; print(f'Target: {get_settings().database_url}')"
# Expected: postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp

# Verify current state
alembic current
# Expected: 004 (head at 008)

# Run all pending
alembic upgrade head
# Expected: 004 -> 005 -> 006 -> 007 -> 008

# Verify final state
alembic current
# Expected: 008 (head)
```

### Verifying Schema After Migration

```sql
-- Verify composite PK on paper_enrichments
\d paper_enrichments
-- PK should be: "paper_enrichments_pkey" PRIMARY KEY, btree (arxiv_id, source_api)

-- Verify content_variants table exists
\d content_variants
-- Should show table with composite PK (arxiv_id, variant_type)
```

### Test Fixture Consolidation Pattern (SC-2)

**Before (workflow conftest -- duplicated):**
```python
# tests/test_workflow/conftest.py -- BEFORE
TSVECTOR_FUNCTION_SQL = """..."""  # DUPLICATE
TSVECTOR_DROP_TRIGGER_SQL = "..."  # DUPLICATE
TSVECTOR_CREATE_TRIGGER_SQL = """..."""  # DUPLICATE

def sample_paper_data(**overrides) -> dict:  # DUPLICATE
    defaults = {...}  # simplified defaults
    ...

@pytest.fixture
async def test_engine():  # DUPLICATE
    ...

@pytest.fixture
async def test_session(test_engine):  # DUPLICATE
    ...
```

**After (workflow conftest -- imports from root):**
```python
# tests/test_workflow/conftest.py -- AFTER
from tests.conftest import sample_paper_data  # shared factory, no longer local

# Domain-specific factories STAY here:
def sample_collection_data(**overrides) -> dict: ...
def sample_triage_data(**overrides) -> dict: ...
def sample_saved_query_data(**overrides) -> dict: ...

# Domain-specific fixture STAYS here:
@pytest.fixture
async def sample_papers(test_session): ...
```

**Consumer file update pattern:**
```python
# tests/test_workflow/test_search_augment.py -- BEFORE
from .conftest import sample_paper_data

# tests/test_workflow/test_search_augment.py -- AFTER
from tests.conftest import sample_paper_data
```

### Import Cleanup Pattern (SC-4)

**Before:**
```python
# content/__init__.py -- BEFORE (causes httpx/bs4 eager loading)
from arxiv_mcp.content.adapters import ContentAdapter, MarkerAdapter, MockContentAdapter
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
from arxiv_mcp.content.models import AccessDecision, ContentConversionResult, ContentStatus, VariantType
from arxiv_mcp.content.rights import RightsChecker
from arxiv_mcp.content.service import ContentService

__all__ = [...]
```

**After:**
```python
# content/__init__.py -- AFTER (no eager imports)
"""Content normalization package for arxiv-mcp.

Provides content variant types, conversion result schemas, license
rights checking, adapters for PDF-to-markdown conversion, HTML fetching,
and the data layer for storing normalized paper content in multiple
formats (abstract, HTML, source-derived markdown, PDF-derived markdown).
"""
```

### Docstring Fix Pattern (SC-3)

**Before (line 73):**
```python
    """Create a monitored search that tracks new papers matching your query.

    Run get_delta to see papers added since your last check.
    """
```

**After:**
```python
    """Create a monitored search that tracks new papers matching your query.

    Read the watch://{slug}/deltas resource to see papers added since your last check.
    """
```

### Regression Test for Docstring (SC-3)

```python
# Following Phase 04.1 pattern from test_interest/test_search_augment.py
class TestCreateWatchDocstring:
    def test_create_watch_references_watch_resource(self):
        from arxiv_mcp.mcp.tools.workflow import create_watch
        doc = create_watch.__doc__
        assert doc is not None, "create_watch must have a docstring"
        assert "watch://" in doc, "create_watch docstring must reference watch:// resource"
        assert "/deltas" in doc, "create_watch docstring must reference /deltas"
```

### Regression Test for Import Isolation (SC-4)

```python
import sys

class TestContentImportIsolation:
    def test_content_models_does_not_load_httpx_or_bs4(self):
        """Importing content.models should not trigger heavy dependency loading."""
        # Track modules loaded before import
        before = set(sys.modules.keys())
        from arxiv_mcp.content.models import VariantType  # noqa: F401
        after = set(sys.modules.keys())
        new_modules = after - before
        assert not any("httpx" in m for m in new_modules), (
            f"Importing content.models loaded httpx: {[m for m in new_modules if 'httpx' in m]}"
        )
        assert not any("bs4" in m for m in new_modules), (
            f"Importing content.models loaded bs4: {[m for m in new_modules if 'bs4' in m]}"
        )
```

**Note:** This test must run early (before other tests import httpx/bs4) or use subprocess isolation. The planner should determine the best approach -- either `subprocess.run` with a fresh Python interpreter or careful test ordering.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single PK (arxiv_id) for enrichments | Composite PK (arxiv_id, source_api) | Phase quick-1 (code), migration 006 (schema) | Blocks enrichment on live DB until migration runs |
| Duplicated conftest per test module | Central conftest with module-specific imports | Phase 6 (enrichment/content adopted it) | DRY, consistent test setup, no UniqueViolation risk |
| Eager `__init__.py` imports | Direct submodule imports only | Python 3.7+ best practice | Reduced import overhead, no hidden dependency chains |

## Open Questions

1. **Import isolation test execution order**
   - What we know: If httpx/bs4 are already in `sys.modules` from earlier test imports, the regression test will pass vacuously (new_modules will be empty because they were already loaded).
   - What's unclear: Whether pytest test ordering guarantees this test runs before content integration tests that load httpx.
   - Recommendation: Use `subprocess.run(["python", "-c", "import sys; ..."])` for a clean interpreter, or place the test in an early-running module. The planner should decide the exact approach.

2. **Duplicate sample_saved_query_data across workflow and interest conftest**
   - What we know: Both workflow and interest conftest define identical `sample_saved_query_data` factories.
   - What's unclear: Whether to consolidate this into root conftest too.
   - Recommendation: Per locked decision, domain-specific factories stay in module conftest. Since both modules use `sample_saved_query_data` in their domain context, keeping both copies is acceptable. This is not part of SC-2's scope.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.x + pytest-asyncio 0.24+ (asyncio_mode = "auto") |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `python -m pytest -x -q` |
| Full suite command | `python -m pytest -x -q` |

### Phase Requirements -> Test Map

This is a gap closure phase with no formal requirement IDs. Tests map to success criteria:

| Criterion | Behavior | Test Type | Automated Command | File Exists? |
|-----------|----------|-----------|-------------------|-------------|
| SC-1 | Enrichment upsert works with composite PK against live DB | integration (manual) | `alembic current` (verify 008) | N/A (live DB) |
| SC-2 | Test fixtures don't conflict; full suite passes after consolidation | integration | `python -m pytest -x -q` (full suite) | Yes (existing 490 tests) |
| SC-3 | create_watch docstring references watch resource | unit | `python -m pytest tests/test_mcp/test_workflow_tools.py -x -q` | No -- Wave 0 gap |
| SC-4 | content.models importable without httpx/bs4 | unit | `python -m pytest tests/test_content/test_import_isolation.py -x -q` | No -- Wave 0 gap |

### Sampling Rate

- **Per task commit:** `python -m pytest -x -q`
- **Per wave merge:** `python -m pytest -x -q`
- **Phase gate:** Full suite green (490+ tests) before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] Docstring assertion test for `create_watch` -- covers SC-3 (place in `tests/test_mcp/test_workflow_tools.py`)
- [ ] Import isolation test for `content.models` -- covers SC-4 (place in `tests/test_content/` or `tests/`)

No framework install needed -- pytest infrastructure already fully configured.

## Sources

### Primary (HIGH confidence)

- **Direct code reading:** All 8 conftest files, `content/__init__.py`, `workflow.py` docstring, 8 Alembic migration files, `alembic/env.py`, `.env` file, `config.py`
- **Runtime verification:** `python -c "import sys; from arxiv_mcp.content.models import VariantType; ..."` confirmed httpx/bs4 loading via `content/__init__.py`
- **Grep verification:** `from arxiv_mcp.content import` returns zero matches in both `src/` and `tests/` -- no package-level consumers
- **Grep verification:** No workflow or interest test asserts on default values that differ between conftest copies
- **Test collection:** `python -m pytest --co -q` confirms 490 tests collected

### Secondary (MEDIUM confidence)

None needed -- all findings from direct codebase inspection.

### Tertiary (LOW confidence)

None.

## Metadata

**Confidence breakdown:**
- Enrichment schema mismatch (SC-1): HIGH -- verified by reading all migration files, ORM model, and .env configuration
- Test fixture duplication (SC-2): HIGH -- verified by reading all 8 conftest files and all consumer imports; default divergence analyzed field-by-field; no assertion dependencies found
- Docstring error (SC-3): HIGH -- verified by reading workflow.py line 73 and resources/watch.py
- Import propagation (SC-4): HIGH -- verified by runtime `sys.modules` test and grep confirming zero package-level consumers

**Research date:** 2026-03-13
**Valid until:** No expiry (codebase-specific findings, not library version dependent)
