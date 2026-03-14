---
phase: 10
slug: agent-integration-test
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-14
---

# Phase 10 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio 0.24+ |
| **Config file** | `pyproject.toml` [tool.pytest.ini_options] |
| **Quick run command** | `pytest tests/test_mcp/ -x -q` |
| **Full suite command** | `pytest tests/ -x -q` |
| **Estimated runtime** | ~30 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_mcp/ -x -q`
- **After every plan wave:** Run `pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 10-01-01 | 01 | 1 | SC-1 | manual + smoke | `claude mcp list` | N/A | ⬜ pending |
| 10-01-02 | 01 | 1 | SC-1 | manual | Verify tool listing | N/A | ⬜ pending |
| 10-02-01 | 02 | 2 | SC-2 | manual | Human-observed session | N/A | ⬜ pending |
| 10-02-02 | 02 | 2 | SC-2 | manual | Human-observed session | N/A | ⬜ pending |
| 10-03-01 | 03 | 2 | SC-3 | manual | Review 10-FRICTION.md | N/A | ⬜ pending |
| 10-03-02 | 03 | 2 | SC-4 | manual | Follow README steps | N/A | ⬜ pending |
| 10-03-03 | 03 | 3 | SC-5 | manual + unit | `pytest tests/test_mcp/ -x -q` | Existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. This phase tests integration, not unit behavior. Any new tests created for `fix(10):` commits will use the existing test patterns in `tests/test_mcp/`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| MCP server connects to Claude Code | SC-1 | Requires live MCP client | Configure in `.claude.json`, run `claude mcp list`, verify server appears |
| Agent completes research workflow | SC-2 | Requires agent interaction | Pose research questions to Claude Code with MCP active, observe tool selection |
| Friction points documented | SC-3 | Subjective assessment | Review 10-FRICTION.md for completeness and categorization |
| Setup guide validated | SC-4 | Requires human following instructions | Follow README from scratch, note missing/wrong steps |
| Critical fixes resolved or tracked | SC-5 | Depends on friction findings | Verify each critical item has a commit or v0.2.0 tracking entry |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
