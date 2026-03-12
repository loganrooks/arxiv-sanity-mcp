---
phase: 6
slug: content-normalization
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-12
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio 0.24+ |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest tests/test_content/ -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_content/ -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

Each task's automated verify command references ONLY test files created by that same task or earlier tasks in the same plan. Tests are created TDD-style within each task, not in a separate Wave 0.

| Requirement | Plan | Wave | Test File | Created By | Automated Command | Status |
|-------------|------|------|-----------|------------|-------------------|--------|
| CONT-02 | 06-01 | 1 | tests/test_content/test_models.py | 06-01 Task 1 | `python -m pytest tests/test_content/test_models.py -x` | pending |
| CONT-06 | 06-01 | 1 | tests/test_content/test_rights.py | 06-01 Task 1 | `python -m pytest tests/test_content/test_rights.py -x` | pending |
| CONT-05 | 06-02 | 2 | tests/test_content/test_adapter.py | 06-02 Task 1 | `python -m pytest tests/test_content/test_adapter.py -x` | pending |
| CONT-04 | 06-02 | 2 | tests/test_content/test_html_fetcher.py | 06-02 Task 1 | `python -m pytest tests/test_content/test_html_fetcher.py -x` | pending |
| CONT-01, CONT-03, CONT-04 | 06-02 | 2 | tests/test_content/test_service.py | 06-02 Task 2 | `python -m pytest tests/test_content/test_service.py -x` | pending |
| MCP-03, CONT-06 | 06-03 | 3 | tests/test_mcp/test_content_tool.py | 06-03 Task 1 | `python -m pytest tests/test_mcp/test_content_tool.py -x` | pending |
| MCP-03 | 06-03 | 3 | tests/test_mcp/test_tool_names.py | 06-03 Task 2 (update) | `python -m pytest tests/test_mcp/test_tool_names.py -x` | pending |
| MCP-03 | 06-03 | 3 | tests/test_mcp/test_resources.py | 06-03 Task 2 (update) | `python -m pytest tests/test_mcp/test_resources.py -x` | pending |

*Status: pending / green / red / flaky*

---

## Test File Creation Schedule

Tests are created TDD-style within each task (not in a separate Wave 0). Each plan creates its own test files as part of the task that needs them.

| Wave | Plan | Test Files Created |
|------|------|--------------------|
| 1 | 06-01 | test_models.py, test_rights.py, conftest.py, __init__.py |
| 2 | 06-02 | test_adapter.py, test_html_fetcher.py, test_service.py |
| 3 | 06-03 | test_content_tool.py (new), test_tool_names.py (update), test_resources.py (update) |

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Marker PDF quality on GTX 1080 Ti | CONT-05 | GPU-specific, VRAM varies | Run Marker on 3 sample PDFs, inspect markdown output quality |
| arXiv HTML fetch on live endpoint | CONT-04 | Network-dependent, rate-limited | Fetch HTML for known paper, verify structure preserved |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify referencing only self-created or prior test files
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Test files created TDD-style within each task
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
