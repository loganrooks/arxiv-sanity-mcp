---
phase: 06-content-normalization
verified: 2026-03-13T02:55:00Z
status: passed
score: 7/7 must-haves verified
re_verification: true
gaps: []
human_verification:
  - test: "arxiv-mcp content get <arxiv_id> --variant abstract"
    expected: "Prints abstract text with Rich formatting; exit code 0"
    why_human: "CLI rendering and terminal output require manual inspection"
  - test: "arxiv-mcp content status <arxiv_id> after running 'get'"
    expected: "Shows a Rich table listing the cached variant types and backends"
    why_human: "Rich table output requires visual inspection"
---

# Phase 6: Content Normalization Verification Report

**Phase Goal:** Users can access paper content at multiple fidelity levels (abstract through full-text markdown) with source-aware acquisition, rights-gated serving, and full provenance. Content tools exposed via MCP.
**Verified:** 2026-03-13T02:55:00Z
**Status:** passed
**Re-verification:** Yes — after gap closure (06-04: beautifulsoup4 dependency fix)

---

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | ContentVariant ORM model exists with composite PK (arxiv_id, variant_type) and all provenance columns | VERIFIED | `src/arxiv_mcp/db/models.py` lines 418-460: `class ContentVariant(Base)` with `PrimaryKeyConstraint("arxiv_id", "variant_type")`, CHECK constraint, all 12 provenance columns confirmed present |
| 2 | RightsChecker correctly classifies all 6 arXiv license URIs; deployment-mode-aware access decisions | VERIFIED | `src/arxiv_mcp/content/rights.py`: PERMISSIVE_LICENSES set (3 URIs), PERSONAL_USE_LICENSES set (3 URIs), `check_access(license_uri, deployment_mode)` returns `AccessDecision(allowed, reason, warning)` per mode |
| 3 | ContentService implements source-aware priority chain (abstract → HTML → PDF markdown) with caching and tier promotion | VERIFIED | `src/arxiv_mcp/content/service.py`: `get_or_create_variant` with full priority chain, `_acquire_html`, `_acquire_pdf_markdown`, `_store_variant` with `pg_insert ON CONFLICT`, processing tier promotion to `CONTENT_PARSED` |
| 4 | MCP tool `get_content_variant` is registered as the 11th tool with rights enforcement | VERIFIED | `src/arxiv_mcp/mcp/tools/content.py`: `@mcp.tool()` decorator present, rights check before non-abstract variants, `VALID_VARIANTS` set; `src/arxiv_mcp/mcp/server.py` line 84 imports content tool module; `tests/test_mcp/test_tool_names.py` asserts `len(tools) == 11` and `get_content_variant` in expected set |
| 5 | Paper resource includes `content_variants` field listing available variant types | VERIFIED | `src/arxiv_mcp/mcp/resources/paper.py` line 58: `content_variants = await app.content.list_variants(arxiv_id)`, included in return dict at line 75 |
| 6 | Content CLI subgroup with `get` and `status` commands is registered | VERIFIED | `src/arxiv_mcp/content/cli.py`: `content_group` with `content_get` and `content_status` commands; `src/arxiv_mcp/cli.py` lines 67-73 register `content_group` with lazy import pattern |
| 7 | Full test suite passes — all 471 tests green (295 existing + 176 new Phase 6 tests) | VERIFIED | Gap closed by 06-04: `beautifulsoup4>=4.12` added to pyproject.toml, `uv sync` installed bs4. Full suite: 471 passed, 0 failed (confirmed 2026-03-13T02:55:00Z) |

**Score:** 7/7 truths verified

---

## Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/content/models.py` | VariantType, ContentStatus, AccessDecision, ContentConversionResult | VERIFIED | 72 lines; all 4 models/enums present with correct fields |
| `src/arxiv_mcp/content/rights.py` | RightsChecker with 6-license classification | VERIFIED | 119 lines; PERMISSIVE_LICENSES and PERSONAL_USE_LICENSES sets, `check_access` method complete |
| `src/arxiv_mcp/db/models.py` | ContentVariant ORM model with composite PK | VERIFIED | Lines 415-461; composite PK, FK, CHECK, Index all present |
| `src/arxiv_mcp/config.py` | Settings extended with deployment_mode, content_rate_limit, content_max_pdf_pages | VERIFIED | Lines 69-71; all three settings present with correct defaults |
| `alembic/versions/008_content_variants_table.py` | Migration creating content_variants table | VERIFIED | 72 lines; creates table with all columns, composite PK, FK, CHECK constraint, index; downgrade drops table |
| `src/arxiv_mcp/content/adapters.py` | ContentAdapter protocol, MarkerAdapter, MockContentAdapter | VERIFIED | 194 lines; protocol defined, MarkerAdapter with asyncio.to_thread, MockContentAdapter with call tracking |
| `src/arxiv_mcp/content/html_fetcher.py` | fetch_arxiv_html with HEAD check and sanitization | VERIFIED (code only) | 87 lines; HEAD-first check, 404 handling, BeautifulSoup extraction, nav/header/footer stripping — but `bs4` import fails at runtime |
| `src/arxiv_mcp/content/service.py` | ContentService with priority chain, caching, tier promotion | VERIFIED | 358 lines; full implementation including `_variant_to_dict` static method |
| `src/arxiv_mcp/mcp/tools/content.py` | get_content_variant MCP tool | VERIFIED | 94 lines; validates variant, rights check for non-abstract, delegates to content service, propagates warnings |
| `src/arxiv_mcp/content/cli.py` | content CLI subgroup (get + status) | VERIFIED | 159 lines; `content_get` with `--variant`, `--full`, `-q` flags; `content_status` with Rich table |
| `tests/test_content/test_service.py` | Integration tests for ContentService (min 80 lines) | VERIFIED | 405 lines; 12 test functions covering all scenarios |
| `tests/test_mcp/test_content_tool.py` | Tests for get_content_variant (min 40 lines) | VERIFIED | 190 lines; 6 test functions covering abstract, best, invalid, not-found, rights-warning, rights-blocked |

---

## Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `content/rights.py` | `content/models.py` | imports AccessDecision | WIRED | Line 11: `from arxiv_mcp.content.models import AccessDecision` |
| `content/service.py` | `content/adapters.py` | `self.adapter` | WIRED | Line 24 import; `self.adapter = adapter` in `__init__`; called at line 228 `await self.adapter.convert(...)` |
| `content/service.py` | `content/html_fetcher.py` | `fetch_arxiv_html` call | WIRED | Line 25 import; called at line 180 in `_acquire_html` |
| `content/service.py` | `db/models.py` | ContentVariant reads/writes + tier promotion | WIRED | Line 27 import; `ContentVariant` used in `get_variant` select, `_store_variant` upsert; `ProcessingTier.CONTENT_PARSED` used at line 301 |
| `mcp/tools/content.py` | `content/service.py` | `app.content.get_or_create_variant` | WIRED | Line 81: `result = await app.content.get_or_create_variant(arxiv_id, variant)` |
| `mcp/tools/content.py` | `content/rights.py` | `RightsChecker` at serving time | WIRED | Line 13 import; line 19 `_rights_checker = RightsChecker()`; line 66 `_rights_checker.check_access(license_uri, app.settings.deployment_mode)` |
| `mcp/server.py` | `content/service.py` | ContentService in AppContext | WIRED | Line 18 import; line 43 `content: ContentService` in dataclass; line 61 `content = ContentService(sf, settings)` in lifespan; line 75 `content=content` in yield |
| `mcp/resources/paper.py` | `content/service.py` | `app.content.list_variants` | WIRED | Line 58: `content_variants = await app.content.list_variants(arxiv_id)` |

---

## Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|---------|
| CONT-01 | 06-01-PLAN | Abstract as default content variant (no rights issues) | SATISFIED | `service.py` `_get_abstract` returns `Paper.abstract` directly; `get_content_variant` tool skips rights check for `variant="abstract"` |
| CONT-02 | 06-01-PLAN | Explicit content variant modeling: abstract, HTML, source-derived, PDF-derived markdown | SATISFIED | `VariantType` enum in `models.py` with 4 values; `ContentVariant` ORM with CHECK constraint enforcing all 4 types; migration 008 matches |
| CONT-03 | 06-01-PLAN | Provenance recording: source, extraction method, conversion path, license basis | SATISFIED | `ContentVariant` has `source_url`, `backend`, `backend_version`, `extraction_method`, `license_uri`, `content_hash`; `_store_variant` copies `license_uri` from `Paper` at storage time |
| CONT-04 | 06-02-PLAN | Source-aware acquisition priority: abstract → arXiv HTML → source → PDF | SATISFIED | `get_or_create_variant` in `service.py` implements: abstract direct, then HTML (`_acquire_html`), then PDF markdown (`_acquire_pdf_markdown`); "best" falls through on HTML 404 |
| CONT-05 | 06-02-PLAN | Multiple parsing backends behind common interface | SATISFIED | `ContentAdapter` Protocol in `adapters.py`; `MarkerAdapter` and `MockContentAdapter` both implement it; service accepts any adapter via DI |
| CONT-06 | 06-03-PLAN | Content serving respects per-paper license restrictions | SATISFIED | `get_content_variant` in `mcp/tools/content.py` checks `RightsChecker.check_access(paper.license_uri, deployment_mode)` before serving non-abstract content; blocks in hosted mode, warns in local mode |
| MCP-03 | 06-03-PLAN | MCP server exposes `get_content_variant` tool | SATISFIED | Tool registered via `@mcp.tool()` and wired into server; tool count test asserts 11 tools including `get_content_variant`; all MCP tests pass after bs4 fix |

---

## Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `pyproject.toml` | — | ~~Missing dependency `beautifulsoup4`~~ | Resolved | Fixed by 06-04: `beautifulsoup4>=4.12` added to pyproject.toml |
| `src/arxiv_mcp/content/__init__.py` | 10 | Eager top-level import of `fetch_arxiv_html` from `html_fetcher` | Warning | Propagates import failure to any code doing `from arxiv_mcp.content import ...`; already occurs via `service.py` direct import, so fixing `__init__.py` alone would not fix the issue |

---

## Human Verification Required

### 1. CLI Content Get Command

**Test:** With a paper in the DB, run `arxiv-mcp content get <arxiv_id> --variant abstract`
**Expected:** Rich-formatted output showing variant type, license, hash, and abstract text preview (first 500 chars); exit code 0
**Why human:** CLI rendering and terminal output require visual inspection; cannot verify Rich formatting programmatically

### 2. CLI Content Status Command

**Test:** After running `content get`, run `arxiv-mcp content status <arxiv_id>`
**Expected:** Rich table showing the cached variant (variant_type, backend, converted_at); no error
**Why human:** Rich table output requires visual inspection of terminal formatting

---

## Gaps Summary

All gaps resolved. Phase 6 achieves its goal — all required artifacts exist, are substantive implementations, are correctly wired, and the full test suite passes (471 tests, 0 failures).

**Previous gap (resolved by 06-04):** `beautifulsoup4` was missing from `pyproject.toml`. Fixed by adding `beautifulsoup4>=4.12` and running `uv sync`. Also fixed test fixture isolation (TRUNCATE CASCADE).

---

_Verified: 2026-03-13T02:55:00Z (re-verification after gap closure)_
_Verifier: Claude (gsd-verifier + manual orchestrator update)_
