---
phase: 2
slug: workflow-state
status: draft
nyquist_compliant: false
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

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 0 | WKFL-01..08 | unit | `uv run pytest tests/test_workflow/ -x` | Wave 0 | pending |
| 02-02-01 | 02 | 1 | WKFL-01 | integration | `uv run pytest tests/test_workflow/test_collections.py::TestCollectionCRUD -x` | Wave 0 | pending |
| 02-02-02 | 02 | 1 | WKFL-02 | integration | `uv run pytest tests/test_workflow/test_collections.py::TestCollectionMembership -x` | Wave 0 | pending |
| 02-03-01 | 03 | 1 | WKFL-03 | integration | `uv run pytest tests/test_workflow/test_triage.py::TestTriageState -x` | Wave 0 | pending |
| 02-03-02 | 03 | 1 | WKFL-08 | integration | `uv run pytest tests/test_workflow/test_triage.py::TestBatchTriage -x` | Wave 0 | pending |
| 02-04-01 | 04 | 2 | WKFL-04 | integration | `uv run pytest tests/test_workflow/test_queries.py::TestSavedQueryCRUD -x` | Wave 0 | pending |
| 02-04-02 | 04 | 2 | WKFL-05 | integration | `uv run pytest tests/test_workflow/test_queries.py::TestSavedQueryRun -x` | Wave 0 | pending |
| 02-05-01 | 05 | 2 | WKFL-06 | integration | `uv run pytest tests/test_workflow/test_watches.py::TestWatchCreate -x` | Wave 0 | pending |
| 02-05-02 | 05 | 2 | WKFL-07 | integration | `uv run pytest tests/test_workflow/test_watches.py::TestWatchDelta -x` | Wave 0 | pending |

*Status: pending / green / red / flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_workflow/__init__.py` — package init
- [ ] `tests/test_workflow/conftest.py` — shared fixtures (test DB with workflow tables, sample collections/triage data)
- [ ] `tests/test_workflow/test_collections.py` — stubs for WKFL-01, WKFL-02
- [ ] `tests/test_workflow/test_triage.py` — stubs for WKFL-03, WKFL-08
- [ ] `tests/test_workflow/test_queries.py` — stubs for WKFL-04, WKFL-05
- [ ] `tests/test_workflow/test_watches.py` — stubs for WKFL-06, WKFL-07
- [ ] Workflow table creation in test conftest (extending Phase 1's test_session pattern)
- [ ] Sample collection/triage/saved query test data factory functions

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Watch cadence hint display | WKFL-06 | Cadence is advisory only, no runtime scheduler | Verify `cadence_hint` persists and displays in `watch list` output |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
