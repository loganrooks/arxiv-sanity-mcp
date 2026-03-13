---
phase: 7
slug: mcp-surface-parity
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-12
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.0.2 + pytest-asyncio (auto mode) |
| **Config file** | `pyproject.toml` `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest tests/test_mcp/ -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_mcp/ -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | SC-5 | unit | `python -m pytest tests/test_mcp/test_import.py -x` | Extend existing | ⬜ pending |
| 07-01-02 | 01 | 1 | SC-1 | unit | `python -m pytest tests/test_mcp/test_discovery_tools.py::TestSearchPapersProfileRanked -x` | ❌ W0 | ⬜ pending |
| 07-01-03 | 01 | 1 | SC-2 | unit | `python -m pytest tests/test_mcp/test_discovery_tools.py::TestSearchPapersWorkflowEnriched -x` | ❌ W0 | ⬜ pending |
| 07-01-04 | 01 | 1 | SC-3 | unit | `python -m pytest tests/test_mcp/test_interest_tools.py::TestCreateProfile -x` | ❌ W0 | ⬜ pending |
| 07-01-05 | 01 | 1 | SC-4 | unit | `python -m pytest tests/test_mcp/test_interest_tools.py::TestSuggestSignals -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_mcp/test_interest_tools.py` — stubs for SC-3, SC-4 (create_profile, suggest_signals)
- [ ] `tests/test_mcp/test_discovery_tools.py` — new test classes for SC-1, SC-2 (profile-ranked search, workflow-enriched results)
- [ ] `tests/test_mcp/conftest.py` — add `profile_ranking` and `suggestions` to `mock_app_context`

*Existing infrastructure covers framework, fixtures, and import checks.*

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
