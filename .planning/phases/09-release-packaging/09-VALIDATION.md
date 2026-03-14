---
phase: 9
slug: release-packaging
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-13
---

# Phase 9 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 8.x (existing) |
| **Config file** | pyproject.toml `[tool.pytest.ini_options]` |
| **Quick run command** | `python -m pytest tests/ -x -q --timeout=30` |
| **Full suite command** | `python -m pytest tests/ --timeout=30` |
| **Estimated runtime** | ~5 seconds (493 tests) |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/ -x -q --timeout=30`
- **After every plan wave:** Run `python -m pytest tests/ --timeout=30`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 10 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 09-01-01 | 01 | 1 | SC-1 (LICENSE) | file check | `test -f LICENSE` | ❌ W0 | ⬜ pending |
| 09-01-02 | 01 | 1 | SC-3 (pyproject.toml) | schema check | `python -c "import tomllib; ..."` | ✅ | ⬜ pending |
| 09-01-03 | 01 | 1 | SC-4 (CHANGELOG) | file check | `test -f CHANGELOG.md` | ❌ W0 | ⬜ pending |
| 09-01-04 | 01 | 1 | SC-6 (lint fix) | ruff | `ruff check src/ tests/` | ✅ | ⬜ pending |
| 09-02-01 | 02 | 1 | SC-2 (README) | content check | `grep -q "Installation" README.md` | ✅ | ⬜ pending |
| 09-02-02 | 02 | 1 | SC-6 (CI config) | file check | `test -f .github/workflows/ci.yml` | ❌ W0 | ⬜ pending |
| 09-03-01 | 03 | 2 | SC-5 (GitHub repo) | gh check | `gh repo view loganrooks/arxiv-sanity-mcp` | ❌ W0 | ⬜ pending |
| 09-03-02 | 03 | 2 | SC-6 (CI passes) | gh check | `gh run list --limit 1` | ❌ W0 | ⬜ pending |
| 09-03-03 | 03 | 2 | SC-7 (v0.1.0 tag) | git check | `git tag -l v0.1.0` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- Existing test infrastructure covers functional requirements
- Phase 9 adds no new library code — only packaging, documentation, and CI
- Validation is primarily file existence checks and external service verification (GitHub, CI)

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| README is comprehensible to new user | SC-2 | Subjective quality | Read README as if unfamiliar with project. Can you install and run? |
| CI pipeline passes on GitHub | SC-6 | Requires push to remote | Push code, check GitHub Actions tab |
| MCP config example works | SC-2 | Requires MCP client | Copy config from README, verify server starts |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
