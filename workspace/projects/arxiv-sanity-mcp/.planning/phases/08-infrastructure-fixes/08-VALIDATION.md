---
phase: 8
slug: infrastructure-fixes
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-13
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 9.x + pytest-asyncio 0.24+ |
| **Config file** | pyproject.toml [tool.pytest.ini_options] |
| **Quick run command** | `python -m pytest -x -q` |
| **Full suite command** | `python -m pytest -x -q` |
| **Estimated runtime** | ~14m30s |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest -x -q`
- **After every plan wave:** Run `python -m pytest -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 870 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | SC-1 | integration | `python -m pytest tests/test_enrichment/ -x -q` | Yes | ⬜ pending |
| 08-01-02 | 01 | 1 | SC-2 | integration | `python -m pytest -x -q` | Yes | ⬜ pending |
| 08-02-01 | 02 | 1 | SC-3 | unit | `python -m pytest tests/test_mcp/test_workflow_tools.py -x -q` | Partial | ⬜ pending |
| 08-02-02 | 02 | 1 | SC-4 | unit | `python -m pytest tests/test_content/ -x -q` | No (W0) | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Docstring assertion test for create_watch (may already exist from Phase 04.1 pattern)
- [ ] Import isolation test: verify `from arxiv_mcp.content.models import VariantType` does not load httpx/bs4

*Existing infrastructure covers most phase requirements. Two targeted test additions needed.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Enrichment works against live DB | SC-1 | Requires running migrations on live DB | Run `alembic upgrade head` then `enrich_paper` against real paper |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 870s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
