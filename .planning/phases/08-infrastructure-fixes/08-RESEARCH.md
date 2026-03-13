# Phase 8: Infrastructure Fixes (GAP CLOSURE) - Research

**Researched:** 2026-03-13
**Domain:** Database migration, test fixture architecture, Python import patterns, docstring accuracy
**Confidence:** HIGH

## Summary

Phase 8 addresses four pre-existing infrastructure issues identified during the v1 audit. Each issue is concrete, locally scoped, and independently verifiable. No new libraries, patterns, or architectural decisions are needed -- this is pure remediation of known tech debt.

The most impactful issue is the enrichment schema mismatch: the live database is on Alembic migration 004 (single-column PK on `paper_enrichments`) while the ORM model and service code expect the composite PK `(arxiv_id, source_api)` introduced by migration 006. This blocks `enrich_paper` against the live database. The remaining three issues are lower severity: duplicated test fixture definitions across 4 conftest files, a stale docstring reference, and an eager import in `content/__init__.py`.

**Primary recommendation:** Run pending Alembic migrations (005, 006, 007, 008) against the live database, then consolidate test fixtures into the root conftest.py. The docstring and import fixes are single-line changes.

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

### Pattern 1: Alembic Migration Execution

**What:** Run pending migrations 005-008 against the live database to align schema with code expectations.
**When to use:** When ORM model diverges from live DB schema.
**Current state (verified):**

```
Live DB (arxiv_mcp):  migration 004 (single-column PK)
Test DB (arxiv_mcp_test): no alembic_version table (tests use create_all/drop_all)
ORM model: composite PK (arxiv_id, source_api) via PrimaryKeyConstraint
```

**Key finding:** The code upserts with `on_conflict_do_update(index_elements=["arxiv_id", "source_api"])` which will fail against the live DB because `source_api` is not part of the PK constraint. Migrations 005-008 must all be applied in sequence:
- 005: Drop signal type CHECK constraint
- 006: Enrichment composite PK
- 007: Add seen triage state
- 008: Content variants table

**Command:**
```bash
alembic upgrade head
```

**Verification:** Connect to live DB and confirm PK is `(arxiv_id, source_api)`.

### Pattern 2: Centralized Test Fixture Architecture

**What:** Consolidate duplicated fixture definitions into the root `tests/conftest.py`.
**When to use:** When identical code appears in 4+ conftest files.

**Current state (verified):** The following are duplicated across 3-4 conftest files:
- `TSVECTOR_FUNCTION_SQL` constant (root, workflow, interest -- 3 copies)
- `TSVECTOR_DROP_TRIGGER_SQL` constant (root, workflow, interest -- 3 copies)
- `TSVECTOR_CREATE_TRIGGER_SQL` constant (root, workflow, interest -- 3 copies)
- `sample_paper_data()` factory (root, workflow, interest -- 3 copies with slight data differences)
- `test_engine` fixture (root, workflow, interest, search -- 4 copies)
- `test_session` fixture (root, workflow, interest -- 3 copies with identical structure)

The enrichment and content conftest files already import from `tests.conftest` (the correct pattern). The workflow and interest conftest files duplicated everything instead.

**Target architecture:**
```
tests/
  conftest.py           # Central: engine, session, paper factory, tsvector SQL
  test_workflow/
    conftest.py          # Imports from tests.conftest; adds workflow-specific factories
  test_interest/
    conftest.py          # Imports from tests.conftest; adds interest-specific factories
  test_search/
    conftest.py          # Already imports from tests.conftest for factories
  test_enrichment/
    conftest.py          # Already imports from tests.conftest (correct)
  test_content/
    conftest.py          # Already imports from tests.conftest (correct)
```

**Risk note:** The duplicated `sample_paper_data()` factories have slightly different default values (e.g., workflow's has shorter abstract text, interest's has `doi: None`). This means tests in those modules may depend on those specific defaults. The consolidation must either:
1. Standardize on one set of defaults (preferred), or
2. Keep module-specific overrides where tests depend on them.

### Pattern 3: Lazy Import in `__init__.py`

**What:** Replace eager import of `html_fetcher` with a lazy pattern to avoid pulling in httpx/bs4/lxml when only models or rights are needed.
**When to use:** When a package `__init__.py` imports a module with heavy external dependencies that not all consumers need.

**Current state (verified):**

```python
# content/__init__.py -- current (eager)
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
```

Importing ANY submodule of `arxiv_mcp.content` (even `content.models`) triggers `__init__.py`, which eagerly loads `httpx`, `bs4`, and `lxml`. The only module that actually uses `fetch_arxiv_html` is `content/service.py`, which already imports it directly:

```python
# content/service.py line 25
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
```

**Fix:** Remove `fetch_arxiv_html` from `content/__init__.py`'s eager imports and `__all__`. The only consumer already imports it directly from the submodule.

**Alternative (if backwards compat needed):** Use `__getattr__` for lazy loading:

```python
def __getattr__(name):
    if name == "fetch_arxiv_html":
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
        return fetch_arxiv_html
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

Since nothing imports `fetch_arxiv_html` via the package-level import (confirmed by grep), the simpler removal is sufficient.

### Pattern 4: Docstring Fix

**What:** Update `create_watch` tool docstring to reference the `watch://{slug}/deltas` resource instead of the non-existent `get_delta` tool.

**Current state (verified):**

```python
# src/arxiv_mcp/mcp/tools/workflow.py line 73
    Run get_delta to see papers added since your last check.
```

The actual mechanism for getting deltas is the `watch://{slug}/deltas` MCP resource (defined in `src/arxiv_mcp/mcp/resources/watch.py`). There is no `get_delta` tool. The daily_digest prompt already uses the correct reference:

```python
# src/arxiv_mcp/mcp/prompts/daily_digest.py line 36
# "Read each watch resource at `watch://{{slug}}/deltas`"
```

**Fix:** Change docstring to:
```python
    """Create a monitored search that tracks new papers matching your query.

    Read the watch://{slug}/deltas resource to see papers added since your last check.
    """
```

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| DB schema migration | Manual SQL against live DB | `alembic upgrade head` | Alembic tracks state, handles rollback, is already configured |
| Test fixture deduplication | Copy-paste factories | Import from root conftest.py | Already working pattern in enrichment/content tests |
| Lazy imports | Custom import hooks | Remove from `__init__.py` or use `__getattr__` | Standard Python 3.7+ pattern, no libraries needed |

## Common Pitfalls

### Pitfall 1: Running Migrations Against Wrong Database
**What goes wrong:** `alembic upgrade head` runs against the database in settings, which defaults to the live DB. If someone has `DATABASE_URL` overridden in `.env`, it could hit the wrong target.
**Why it happens:** Alembic reads from `arxiv_mcp.config.get_settings()` which reads `.env`.
**How to avoid:** Verify the target database URL before running migrations. Check `.env` if present.
**Warning signs:** Migration says "0 rows affected" when you expect data to exist, or connects to unexpected host.

### Pitfall 2: Test Fixture Default Divergence
**What goes wrong:** Consolidating `sample_paper_data()` with different defaults may break tests that rely on the specific default values (e.g., `doi: None` vs `doi: "10.48550/..."`, abstract length differences).
**Why it happens:** Each conftest copied and slightly modified the factory during its phase.
**How to avoid:** Run full test suite after consolidation. If tests fail, check which default value they depend on and add explicit overrides in those tests.
**Warning signs:** Tests that worked before consolidation fail on field-value assertions.

### Pitfall 3: Content Test TRUNCATE Order
**What goes wrong:** The content conftest TRUNCATEs `content_variants CASCADE` then `papers CASCADE`. If another fixture module's teardown runs between setup steps, data may be inconsistent.
**Why it happens:** Multiple test modules share the same test database and use create_all/drop_all which can conflict.
**How to avoid:** The TRUNCATE CASCADE pattern (already used in content conftest) is the right approach. If centralizing, use TRUNCATE CASCADE consistently.
**Warning signs:** `UniqueViolationError` during table creation in parallel test execution (the issue this phase fixes).

### Pitfall 4: Migration 006 on DB With Existing Data
**What goes wrong:** Migration 006 changes the PK from `(arxiv_id)` to `(arxiv_id, source_api)`. If there are existing enrichment rows, they all have `source_api = 'openalex'` (server_default). This is safe because the new composite PK accepts any unique `(arxiv_id, source_api)` pair.
**Why it happens:** Developer concern about data migration.
**How to avoid:** Verify there are no duplicate `(arxiv_id, source_api)` pairs before running (there cannot be, since `source_api` has a server_default of `'openalex'` and `arxiv_id` was previously unique).
**Warning signs:** Migration fails with "duplicate key" -- this would indicate unexpected data.

## Code Examples

### Running Pending Migrations

```bash
# Verify current state
alembic current
# Expected: 004 (head at 008)

# Run all pending
alembic upgrade head
# Expected: 004 -> 005 -> 006 -> 007 -> 008

# Verify
alembic current
# Expected: 008 (head)
```

### Verifying Schema After Migration

```sql
-- Verify composite PK
\d paper_enrichments
-- PK should be: "paper_enrichments_pkey" PRIMARY KEY, btree (arxiv_id, source_api)

-- Verify seen triage state works
INSERT INTO triage_states (paper_id, state, updated_at)
  VALUES ('test', 'seen', NOW());
-- Should succeed (was blocked before migration 007)

-- Verify content_variants table exists
\d content_variants
-- Should show table with composite PK (arxiv_id, variant_type)
```

### Centralized Test Engine Fixture

```python
# tests/conftest.py -- after consolidation
@pytest.fixture
async def test_engine():
    """Create async engine for the test database.

    Function-scoped to avoid event loop issues with asyncpg.
    Each test gets a fresh engine bound to its own event loop.
    """
    settings = get_settings()
    engine = create_async_engine(
        settings.test_database_url,
        echo=False,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()
```

### Lazy Import Pattern for `__init__.py`

```python
# content/__init__.py -- after fix
# Remove: from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
# Remove: "fetch_arxiv_html" from __all__

# Consumers that need it already import directly:
# from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Single PK (arxiv_id) for enrichments | Composite PK (arxiv_id, source_api) | Phase quick-1 (code), migration 006 (schema) | Blocks enrichment on live DB |
| Duplicated conftest per test module | Central conftest with module-specific imports | Phase 6 (enrichment/content adopted it) | DRY, consistent test setup |
| Eager `__init__.py` imports | Lazy or direct submodule imports | Python 3.7+ `__getattr__` pattern | Reduced import overhead |

## Open Questions

1. **Should test fixtures use TRUNCATE or drop_all/create_all?**
   - What we know: content conftest uses TRUNCATE CASCADE (Phase 06-04 decision). Other modules use drop_all/create_all.
   - What's unclear: Whether mixing the two patterns across test modules causes the UniqueViolation (tests pass currently but may fail under parallel execution).
   - Recommendation: Standardize on one approach during consolidation. TRUNCATE CASCADE is preferred (Phase 06-04 decision: "preserves asyncpg prepared statement cache").

2. **Should we run `alembic upgrade head` in tests or continue with `Base.metadata.create_all`?**
   - What we know: Tests use `create_all` which creates tables from ORM metadata (always matches code). Alembic tracks incremental migrations. Test DB has no `alembic_version` table.
   - What's unclear: Whether alembic-managed test DB would be better for catching migration issues.
   - Recommendation: Keep `create_all` for tests (simpler, faster, always matches ORM). The migration issue is live-DB-only.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 9.x + pytest-asyncio 0.24+ |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `python -m pytest -x -q` |
| Full suite command | `python -m pytest -x -q` |

### Phase Requirements -> Test Map

This is a gap closure phase with no formal requirement IDs. Tests map to success criteria:

| Criterion | Behavior | Test Type | Automated Command | File Exists? |
|-----------|----------|-----------|-------------------|-------------|
| SC-1 | Enrichment upsert works with composite PK against DB | integration | `python -m pytest tests/test_enrichment/ -x -q` | Yes (existing) |
| SC-2 | Test fixtures don't conflict across modules | integration | `python -m pytest -x -q` (full suite) | Yes (existing) |
| SC-3 | create_watch docstring references watch resource | unit | `python -m pytest tests/test_mcp/test_workflow_tools.py -x -q` | Partial (docstring test may exist per Phase 04.1 pattern) |
| SC-4 | Content models importable without httpx/bs4 | unit | Needs new test | No (Wave 0) |

### Sampling Rate

- **Per task commit:** `python -m pytest -x -q`
- **Per wave merge:** `python -m pytest -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] Docstring assertion test for create_watch (may already exist from Phase 04.1 pattern -- check `test_workflow_tools.py`)
- [ ] Import isolation test: verify `from arxiv_mcp.content.models import VariantType` does not load httpx/bs4

## Sources

### Primary (HIGH confidence)

- **Live database inspection:** `\d paper_enrichments` on `arxiv_mcp` DB -- confirmed single-column PK `(arxiv_id)`
- **Alembic version check:** `SELECT version_num FROM alembic_version` -- confirmed version `004`
- **Source code analysis:** Direct reading of all migration files, ORM models, conftest files, and `__init__.py`
- **Import chain verification:** Python runtime test confirming `content.models` import triggers httpx/bs4 loading
- **Full test suite execution:** 490 tests passing, 14m30s runtime

### Secondary (MEDIUM confidence)

None needed -- all findings from direct codebase inspection.

### Tertiary (LOW confidence)

None.

## Metadata

**Confidence breakdown:**
- Enrichment schema mismatch: HIGH -- verified by live DB inspection + migration version check
- Test fixture duplication: HIGH -- verified by reading all 8 conftest files
- Docstring error: HIGH -- verified by reading workflow.py and resources/watch.py
- Import propagation: HIGH -- verified by runtime import chain test

**Research date:** 2026-03-13
**Valid until:** No expiry (codebase-specific findings, not library version dependent)
