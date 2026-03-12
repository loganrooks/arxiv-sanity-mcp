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

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| TBD | 01 | 1 | CONT-01 | unit | `python -m pytest tests/test_content/test_service.py::test_get_abstract_variant -x` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | CONT-02 | unit | `python -m pytest tests/test_content/test_models.py -x` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | CONT-03 | unit | `python -m pytest tests/test_content/test_service.py::test_provenance_fields -x` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | CONT-04 | unit | `python -m pytest tests/test_content/test_service.py::test_acquisition_priority -x` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | CONT-05 | unit | `python -m pytest tests/test_content/test_adapter.py -x` | ❌ W0 | ⬜ pending |
| TBD | 01 | 1 | CONT-06 | unit | `python -m pytest tests/test_content/test_rights.py -x` | ❌ W0 | ⬜ pending |
| TBD | 02 | 2 | MCP-03 | unit | `python -m pytest tests/test_mcp/test_content_tool.py -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_content/__init__.py` — package init
- [ ] `tests/test_content/conftest.py` — shared fixtures (content_session_factory, mock adapter)
- [ ] `tests/test_content/test_models.py` — ContentConversionResult, ContentStatus Pydantic model tests
- [ ] `tests/test_content/test_adapter.py` — MarkerAdapter protocol compliance, MockAdapter
- [ ] `tests/test_content/test_rights.py` — RightsChecker with all license types, both deployment modes
- [ ] `tests/test_content/test_service.py` — ContentService orchestration, priority chain, DB storage, tier promotion
- [ ] `tests/test_mcp/test_content_tool.py` — get_content_variant MCP tool with mock services
- [ ] Update `tests/test_mcp/test_tool_names.py` — expect 11 tools, include "get_content_variant"

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Marker PDF quality on GTX 1080 Ti | CONT-05 | GPU-specific, VRAM varies | Run Marker on 3 sample PDFs, inspect markdown output quality |
| arXiv HTML fetch on live endpoint | CONT-04 | Network-dependent, rate-limited | Fetch HTML for known paper, verify structure preserved |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
