---
phase: 5
slug: mcp-validation-iteration
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-12
---

# Phase 5 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x + pytest-asyncio 0.24+ |
| **Config file** | `pyproject.toml` [tool.pytest.ini_options] |
| **Quick run command** | `pytest tests/test_mcp/ -x -q` |
| **Full suite command** | `pytest tests/ -x -q` |
| **Estimated runtime** | ~15 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/test_mcp/ -x -q`
- **After every plan wave:** Run `pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 15 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | MCPV-01 | integration | `pytest tests/test_mcp/test_import.py -x` | ❌ W0 | ⬜ pending |
| 05-01-02 | 01 | 1 | MCPV-01 | integration | `pytest tests/test_mcp/test_import.py -x` | ❌ W0 | ⬜ pending |
| 05-02-01 | 02 | 2 | MCP-05 | unit | `pytest tests/test_mcp/test_prompts.py -x` | ❌ W0 | ⬜ pending |
| 05-02-02 | 02 | 2 | MCP-05 | unit | `pytest tests/test_mcp/test_prompts.py -x` | ❌ W0 | ⬜ pending |
| 05-02-03 | 02 | 2 | MCP-05 | unit | `pytest tests/test_mcp/test_prompts.py -x` | ❌ W0 | ⬜ pending |
| 05-02-04 | 02 | 2 | MCPV-01 | manual | Human-observed agent session | N/A | ⬜ pending |
| 05-03-01 | 03 | 3 | MCPV-02 | manual | Review validation-log.md | N/A | ⬜ pending |
| 05-03-02 | 03 | 3 | MCPV-03 | unit | `pytest tests/test_mcp/ -x` | Existing | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_mcp/test_prompts.py` — stubs for MCP-05 (prompt registration, rendering, context injection)
- [ ] `tests/test_mcp/test_import.py` — stubs for MCPV-01 (import script correctness, triage state mapping)
- [ ] No new framework install needed; existing pytest + pytest-asyncio covers all requirements

*Existing infrastructure covers framework needs.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Full literature review workflow through MCP | MCPV-01 | Requires interactive agent session with real papers | 1. Start MCP server with imported arxiv-scan data. 2. Connect Claude Code as MCP client. 3. Execute search → triage → collect → expand → enrich workflow. 4. Record observations in validation-log.md. |
| Doc 06 open questions answered with evidence | MCPV-02 | Answers come from human observation during validation | 1. During validation session, note tool usage patterns. 2. Record which tools/resources agents use vs ignore. 3. Write evidence-based answers for each of 5 open questions. |
| MCP surface iteration based on observed friction | MCPV-03 | Iteration targets emerge from real usage, not pre-planned | 1. Collect friction points from validation-log.md. 2. Identify top iteration priority. 3. Implement change. 4. Verify change improves workflow. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 15s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
