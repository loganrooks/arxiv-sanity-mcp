---
phase: 4
slug: enrichment-adapters
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-09
---

# Phase 4 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.0+ with pytest-asyncio |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `pytest tests/test_enrichment/ -x -q` |
| **Full suite command** | `pytest tests/ -x --timeout=30` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_enrichment/ -x -q`
- **After every plan wave:** Run `pytest tests/ -x --timeout=30`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| TBD | 01 | 1 | ENRC-01 | integration | `pytest tests/test_enrichment/test_service.py::test_enrich_single_paper -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-01 | unit | `pytest tests/test_enrichment/test_models.py::test_parse_topics -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-01 | unit | `pytest tests/test_enrichment/test_models.py::test_parse_fwci -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-02 | integration | `pytest tests/test_enrichment/test_service.py::test_cooldown_enforcement -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-02 | integration | `pytest tests/test_enrichment/test_service.py::test_refresh_bypasses_cooldown -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-02 | integration | `pytest tests/test_enrichment/test_service.py::test_enrich_collection -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-03 | unit | `pytest tests/test_enrichment/test_adapter.py::test_resolve_via_doi -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-03 | integration | `pytest tests/test_enrichment/test_service.py::test_paper_ids_updated -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-03 | unit | `pytest tests/test_enrichment/test_adapter.py::test_batch_resolution -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-04 | integration | `pytest tests/test_enrichment/test_service.py::test_provenance_tracking -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-04 | integration | `pytest tests/test_enrichment/test_service.py::test_failed_enrichment -x` | Wave 0 | pending |
| TBD | 01 | 1 | ENRC-04 | integration | `pytest tests/test_enrichment/test_service.py::test_not_found_recorded -x` | Wave 0 | pending |

*Status: pending -- task IDs will be assigned during planning*

---

## Wave 0 Requirements

- [ ] `tests/test_enrichment/__init__.py` -- package init
- [ ] `tests/test_enrichment/conftest.py` -- session factory, sample data, respx fixtures
- [ ] `tests/test_enrichment/fixtures/` -- directory for JSON fixture files
- [ ] `tests/test_enrichment/fixtures/openalex_work_attention.json` -- recorded response
- [ ] `tests/test_enrichment/fixtures/openalex_work_not_found.json` -- empty results
- [ ] `tests/test_enrichment/fixtures/openalex_batch_response.json` -- multi-work batch
- [ ] `tests/test_enrichment/test_adapter.py` -- OpenAlexAdapter unit tests
- [ ] `tests/test_enrichment/test_service.py` -- EnrichmentService integration tests
- [ ] `tests/test_enrichment/test_models.py` -- Pydantic schema validation tests
- [ ] Dev dependency: `respx>=0.22` in pyproject.toml

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Live OpenAlex API responds correctly | ENRC-01 | Requires network and API key | `pytest tests/test_enrichment/ -m live --live-api` with OPENALEX_API_KEY set |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
