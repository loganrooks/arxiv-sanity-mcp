---
phase: 3
slug: interest-modeling-ranking
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-09
---

# Phase 3 — Validation Strategy

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
| 03-01-01 | 01 | 1 | INTR-01 | integration | `uv run pytest tests/test_interest/test_profiles.py::TestProfileCRUD -x` | ❌ W0 | ⬜ pending |
| 03-01-02 | 01 | 1 | INTR-02 | integration | `uv run pytest tests/test_interest/test_profiles.py::TestSeedPaperSignals -x` | ❌ W0 | ⬜ pending |
| 03-01-03 | 01 | 1 | INTR-03 | integration | `uv run pytest tests/test_interest/test_profiles.py::TestSavedQuerySignals -x` | ❌ W0 | ⬜ pending |
| 03-01-04 | 01 | 1 | INTR-04 | integration | `uv run pytest tests/test_interest/test_profiles.py::TestFollowedAuthorSignals -x` | ❌ W0 | ⬜ pending |
| 03-01-05 | 01 | 1 | INTR-05 | integration | `uv run pytest tests/test_interest/test_profiles.py::TestNegativeExampleSignals -x` | ❌ W0 | ⬜ pending |
| 03-01-06 | 01 | 1 | INTR-06 | integration | `uv run pytest tests/test_interest/test_suggestions.py -x` | ❌ W0 | ⬜ pending |
| 03-02-01 | 02 | 2 | RANK-01 | integration | `uv run pytest tests/test_interest/test_ranking.py::TestRankingExplanations -x` | ❌ W0 | ⬜ pending |
| 03-02-02 | 02 | 2 | RANK-02 | unit | `uv run pytest tests/test_interest/test_ranking.py::TestSignalScorers -x` | ❌ W0 | ⬜ pending |
| 03-02-03 | 02 | 2 | RANK-03 | integration | `uv run pytest tests/test_interest/test_ranking.py::TestRankerSnapshot -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_interest/__init__.py` — package init
- [ ] `tests/test_interest/conftest.py` — shared fixtures (test DB with interest tables, sample profiles/signals, pre-loaded seed papers)
- [ ] `tests/test_interest/test_profiles.py` — stubs for INTR-01 through INTR-05 (profile CRUD and all signal types)
- [ ] `tests/test_interest/test_suggestions.py` — stubs for INTR-06 (suggestion generation, confirm, dismiss, provenance inspection)
- [ ] `tests/test_interest/test_ranking.py` — stubs for RANK-01 through RANK-03 (signal scorers, composite ranking, explanations, snapshot)
- [ ] Interest table creation in test conftest (extending Phase 2's test_session pattern with InterestProfile + InterestSignal)
- [ ] Sample profile/signal test data factory functions (`sample_profile_data()`, `sample_signal_data()`)
- [ ] Pre-loaded seed paper fixtures with known categories for deterministic category overlap tests

---

## Manual-Only Verifications

*All phase behaviors have automated verification.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
