---
phase: 1
slug: metadata-substrate
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-08
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio 0.24+ |
| **Config file** | none — Wave 0 installs |
| **Quick run command** | `uv run pytest tests/ -x --timeout=30` |
| **Full suite command** | `uv run pytest tests/ -v --cov=src/arxiv_mcp` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `uv run pytest tests/ -x --timeout=30`
- **After every plan wave:** Run `uv run pytest tests/ -v --cov=src/arxiv_mcp`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 01-01-01 | 01 | 0 | — | setup | `uv run pytest tests/ -x` | Wave 0 | ⬜ pending |
| 01-02-01 | 02 | 1 | PAPR-01 | unit | `uv run pytest tests/test_models/test_paper.py::test_canonical_model -x` | Wave 0 | ⬜ pending |
| 01-02-02 | 02 | 1 | PAPR-02 | unit | `uv run pytest tests/test_models/test_paper.py::test_full_metadata -x` | Wave 0 | ⬜ pending |
| 01-02-03 | 02 | 1 | PAPR-03 | unit | `uv run pytest tests/test_models/test_paper.py::test_external_ids -x` | Wave 0 | ⬜ pending |
| 01-02-04 | 02 | 1 | PAPR-04 | unit | `uv run pytest tests/test_models/test_paper.py::test_provenance -x` | Wave 0 | ⬜ pending |
| 01-02-05 | 02 | 1 | INGS-03 | unit | `uv run pytest tests/test_models/test_paper.py::test_time_semantics -x` | Wave 0 | ⬜ pending |
| 01-02-06 | 02 | 1 | INGS-04 | unit | `uv run pytest tests/test_models/test_paper.py::test_license -x` | Wave 0 | ⬜ pending |
| 01-03-01 | 03 | 2 | INGS-01 | integration | `uv run pytest tests/test_ingestion/test_oai_pmh.py -x` | Wave 0 | ⬜ pending |
| 01-03-02 | 03 | 2 | INGS-02 | integration | `uv run pytest tests/test_ingestion/test_arxiv_api.py -x` | Wave 0 | ⬜ pending |
| 01-03-03 | 03 | 2 | INGS-05 | integration | `uv run pytest tests/test_ingestion/test_oai_pmh.py::test_incremental -x` | Wave 0 | ⬜ pending |
| 01-04-01 | 04 | 3 | SRCH-01 | integration | `uv run pytest tests/test_search/test_service.py::test_fielded_search -x` | Wave 0 | ⬜ pending |
| 01-04-02 | 04 | 3 | SRCH-02 | integration | `uv run pytest tests/test_search/test_service.py::test_boolean_queries -x` | Wave 0 | ⬜ pending |
| 01-04-03 | 04 | 3 | SRCH-03 | integration | `uv run pytest tests/test_search/test_service.py::test_browse_recent -x` | Wave 0 | ⬜ pending |
| 01-04-04 | 04 | 3 | SRCH-04 | integration | `uv run pytest tests/test_search/test_service.py::test_time_basis -x` | Wave 0 | ⬜ pending |
| 01-04-05 | 04 | 3 | SRCH-05 | integration | `uv run pytest tests/test_search/test_service.py::test_find_related -x` | Wave 0 | ⬜ pending |
| 01-04-06 | 04 | 3 | SRCH-06 | unit+integration | `uv run pytest tests/test_search/test_pagination.py -x` | Wave 0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `pyproject.toml` — project initialization with uv
- [ ] `tests/conftest.py` — shared fixtures (test database, sample paper data, mock OAI-PMH responses)
- [ ] `pyproject.toml [tool.pytest]` — pytest configuration
- [ ] Test database setup (separate PostgreSQL database for tests)
- [ ] Mock XML responses for OAI-PMH tests (sample arXivRaw, arXiv format records)
- [ ] `tests/test_models/test_paper.py` — stubs for PAPR-01..04, INGS-03..04
- [ ] `tests/test_ingestion/test_oai_pmh.py` — stubs for INGS-01, INGS-05
- [ ] `tests/test_ingestion/test_arxiv_api.py` — stubs for INGS-02
- [ ] `tests/test_search/test_service.py` — stubs for SRCH-01..05
- [ ] `tests/test_search/test_pagination.py` — stubs for SRCH-06

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| OAI-PMH rate limiting compliance | INGS-01 | Requires real arXiv API calls | Trigger harvest, verify 3-second delay between requests in logs |
| Announcement date accuracy | INGS-03 | Requires comparison with actual arXiv announcements | Compare derived dates against arXiv new submissions page for sample papers |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
