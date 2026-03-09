---
phase: 2
slug: workflow-state
status: draft
nyquist_compliant: true
wave_0_complete: false
created: 2026-03-09
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio 0.24+ |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` (existing) |
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

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------|-------------------|--------|
| 02-01-T1 | 01 | 1 | WKFL-01..04,06 | unit | `uv run pytest tests/test_workflow/test_models.py -x` | pending |
| 02-01-T2 | 01 | 1 | WKFL-01..04,06 | integration | `uv run alembic upgrade head && uv run alembic downgrade -1 && uv run alembic upgrade head` | pending |
| 02-02-T1 | 02 | 2 | WKFL-01,02 | integration | `uv run pytest tests/test_workflow/test_collections.py -x` | pending |
| 02-02-T2 | 02 | 2 | WKFL-03,08 | integration | `uv run pytest tests/test_workflow/test_triage.py -x` | pending |
| 02-03-T1 | 03 | 3 | WKFL-04,05,06,07 | integration | `uv run pytest tests/test_workflow/test_queries.py tests/test_workflow/test_watches.py -x` | pending |
| 02-03-T2 | 03 | 3 | WKFL-08 | integration | `uv run pytest tests/test_workflow/test_search_augment.py -x` | pending |
| 02-03-T3 | 03 | 3 | WKFL-05,08 | integration | `uv run pytest tests/test_workflow/test_export.py -x` | pending |
| 02-03-T4 | 03 | 3 | WKFL-01..08 | smoke | `uv run arxiv-mcp collection --help && uv run arxiv-mcp triage --help && uv run arxiv-mcp query --help` | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_workflow/__init__.py` — package init
- [ ] `tests/test_workflow/conftest.py` — shared fixtures (test DB with workflow tables, sample collections/triage data)
- [ ] `tests/test_workflow/test_models.py` — tests for ORM models and Pydantic schemas (Plan 01)
- [ ] `tests/test_workflow/test_collections.py` — tests for WKFL-01, WKFL-02 (Plan 02)
- [ ] `tests/test_workflow/test_triage.py` — tests for WKFL-03, WKFL-08 (Plan 02)
- [ ] `tests/test_workflow/test_queries.py` — tests for WKFL-04, WKFL-05 (Plan 03)
- [ ] `tests/test_workflow/test_watches.py` — tests for WKFL-06, WKFL-07 (Plan 03)
- [ ] `tests/test_workflow/test_search_augment.py` — tests for triage in search output (Plan 03)
- [ ] `tests/test_workflow/test_export.py` — tests for export/import/stats (Plan 03)
- [ ] Workflow table creation in test conftest (extending Phase 1's test_session pattern)
- [ ] Sample collection/triage/saved query test data factory functions

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Watch cadence hint display | WKFL-06 | Cadence is advisory only, no runtime scheduler | Verify `cadence_hint` persists and displays in `watch dashboard` output |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 30s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
