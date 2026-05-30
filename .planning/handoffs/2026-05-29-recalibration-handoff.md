---
type: session-handoff
date: 2026-05-29
status: post-recalibration-reconcile
head_at_write: 9186c8a
branch: reconcile/state-drift-2026-05-29
supersedes_for_coldstart: "2026-04-28 W1/W2 handoffs (pointer-stubs → gsd-2-uplift repo)"
---

# 2026-05-29 — Recalibration + light-reconcile handoff

**Read this FIRST on cold start.** Do NOT orient on the `2026-04-28` W1/W2 handoffs (they are pointer-stubs redirecting to the `gsd-2-uplift` repo) or on any pre-2026-05-29 STATE snapshot — both predate the 2026-05-08 spike/001 merge.

## True position
- **v0.1 — complete & frozen.** Shipped 2026-03-13/14 (`v0.1.0` tag `31abb5a`). 11 phase dirs (01–10 + 04.1), 31/31 plans, **13 MCP tools / 4 resources / 3 prompts**. Suite **GREEN: 493 collected, 480 passed / 2 skipped / 11 deselected** (content-integration, same set CI deselects). Re-verified 2026-05-29 via `uv run pytest` against the local `arxiv_mcp_test` DB.
- **v0.2 (multi-lens substrate) — ACTIVE, planning only.** Phases 12–17 are authored as ROADMAP/milestone prose + `docs/adrs/ADR-0005` — **no phase dirs or PLAN files exist yet.**
- **Next active work → author Phase 12 plan-1** (`Lens` protocol + scorer registry + register the existing semantic lens + regression tests). Head of the critical path `(12 ∥ 14) → 15; 12 → 13; (13 ∧ 15) → 16 → 17`; depends on nothing.

## What 2026-05-08 actually was (STATE never captured it)
- The `spike/001-volume-filtering` branch (born 2026-03-15, ~7.5 weeks, 11 workstreams) became a de-facto working trunk and was merged as **`dd1a34b` (224 commits) — planning/governance/audit consolidation, ZERO feature code** (0 files under `src/`/`tests/`/`alembic`). Then the PyPI distribution was renamed `arxiv-mcp → arxiv-sanity-mcp` (`9186c8a`).
- Full forensics: **`.planning/recalibration/arxiv-sanity-mcp-state-2026-05-29.md`**. Reconcile rationale + task specs: **`.planning/recalibration/RECONCILE-PLAN.md`**.

## This session's reconcile — branch `reconcile/state-drift-2026-05-29` (LOCAL, not pushed)
- STATE.md reconciled to true position (last_updated, last_activity, last-feature-vs-activity, Session Continuity).
- This handoff added → closes the cold-start navigation trap.
- CLAUDE.md doctrine load-points + read-order repointed to `.planning/…` (the canonical location of VISION/LONG-ARC/PROJECT).
- `uv.lock` relocked to satisfy `pyproject.toml` (was named `arxiv-mcp` + pinned `pytest-asyncio 1.3.0`, violating `>=0.24,<1`).
- `skills-lock.json` gitignored (machine-local skill pins); `.gitignore` GSD-baseline landed.
- `CONSUMER-REQUIREMENTS.md` (long-horizon doctrine-load-points) committed in-place as historical record.
- **Branch cleanup:** deleted fully-merged `spike/001-volume-filtering` (recovery SHA `986855c9be131ad5a6c105b7b2d559a75496a78f`; permanently reachable via `dd1a34b^2`). Recreate with `git branch spike/001-volume-filtering 986855c` if ever needed.

## Parked / open (with revisit triggers)
- **`pull-1` (tip `1fc96fc`) — PARKED.** Broken-NESTED misclone (whole project under `workspace/projects/…`), divergent from main, no unique flat-layout code. Revisit/delete **before next publish or tag**.
- **Open PR #2 `feat/agentic-ops-onboarding`** (2026-05-14, 3 commits; adds `.github/workflows/claude-review.yml` centralized Claude-review CI). Unmerged, **newest activity in the repo**. **Triage before/with harness setup — NOT a delete candidate.**
- **Harness:** read-only is currently **honor-system** — no `PreToolUse` Edit|Write or Bash deny hook installed. PROMPT §4 offers a deny-hook + Stop-hook setup if wanted.
- **Pending validations Q1/Q4/Q16** (foundation-audit) still await Logan's sign-off (tracked in STATE.md "Pending Validations").

## To resume Phase 12 plan-1 (doctrine load-points)
Per CLAUDE.md: ranking/retrieval/lens code → `.planning/LONG-ARC.md` (anti-patterns) + `docs/adrs/ADR-0001` + `docs/adrs/ADR-0005`; new abstraction/signal type → `.planning/LONG-ARC.md` (protected seams) + `.planning/VISION.md` (anti-vision). **STOP-rules:** don't rewrite the v0.1 ranking core (ADR-0001 lens *coexistence* — generalize, don't replace); fusion is never the default; **all v0.1 tests must pass unmodified.**
