# Reconcile-first plan — arxiv-sanity-mcp (2026-05-29)

**Status: EXECUTED 2026-05-29. R1–R5 + R6 (branch cleanup) committed on `reconcile/state-drift-2026-05-29` → PR #3; `spike/001` deleted; `pull-1` parked (revisit before next publish/tag). Follow-up triage of PR #3 reviewer findings applied F1 (ADR paths), F2 (`.mcp.json` un-ignored), F3 (this status). This file is a historical record of the executed reconcile, NOT a pending approval gate.**
Re-entry option chosen: **Reconcile-first (light)** (PROMPT §3, late-orchestration = MIXED ⇒ Clean-resume not standalone-eligible).
Companion: ground-truth in `arxiv-sanity-mcp-state-2026-05-29.md` (drift IDs D1–D7 referenced below).

## Recommendation + exit criteria (§3.2)

**Recommendation:** execute units R1–R4 (the recommended, low-risk doc reconcile) as atomic commits; resolve R5–R6 per your decisions; then clean-resume Phase 12 plan-1 authoring. Justification: the repo is healthy (v0.1 build planning-paced, suite GREEN at 493). The only thing blocking a safe resume is that a cold-start agent would orient on stale STATE (D1/D3) and a pointer-stub/pre-merge handoff trail (D2), and that two doctrine load-points are dead (D5). Fixing those four is cheap and removes the false-premise risk. The spike/001 late-orchestration is already landed + postmortem'd; nothing to rebuild.

**Cost of doing nothing:** the next session (human or agent) re-incurs the same ~30-min recalibration, and risks acting on STATE's false "last activity 2026-03-14 / resume from handoff" — the exact navigation trap the KB flags (`sig-2026-04-16-inter-milestone-exploration-gap`).

**Exit criteria (conjunction — reconcile is DONE only when ALL hold):**
1. STATE.md reflects HEAD: `last_updated` current, names the spike/001 merge (`dd1a34b`) + PyPI rename (`9186c8a`), and distinguishes "last *feature* impl 2026-03-14" from "last activity 2026-05-08". [D1,D3]
2. A 2026-05-29 *real* handoff is the newest in `.planning/handoffs/`, reflecting post-merge reality + pointing at the recalibration anchor. [D2]
3. CLAUDE.md doctrine-load-point + read-order paths resolve (`.planning/VISION.md`, `.planning/LONG-ARC.md`). [D5]
4. `uv.lock` consistent with `pyproject.toml` (or explicitly dispositioned). [D6]
5. Untracked WIP (`skills-lock.json`, `CONSUMER-REQUIREMENTS.md`) + `.gitignore` mod dispositioned (committed / relocated / ignored). [D6,WIP]
6. `pull-1` / `spike/001` branches dispositioned (deleted-with-recorded-SHAs, or parked with a revisit trigger). [D7]
7. Suite still GREEN (`uv run pytest` → 480 passed) after edits.
8. THEN: Phase 12 plan-1 authoring is unblocked.

---

## Unit R1 — Reconcile STATE.md to true position  [D1, D3 · recommended]
- **Objective:** make STATE.md a faithful derived cache of HEAD.
- **Output path:** `.planning/STATE.md` (edit).
- **Edits:** `last_updated` → `2026-05-29`; `last_activity` → note the 2026-05-08 spike/001 branch-debt payoff merge (`dd1a34b`, 224 commits / 11 workstreams, **planning+governance only, 0 feature code**), gsd-2-uplift extraction, PyPI rename (`9186c8a`), and 2026-05-29 recalibration; fix line 32 to read "Last *feature* implementation: 2026-03-14 (Phase 10 P03); subsequent activity 2026-05-08 was planning/governance + the PyPI rename, not feature code"; update Session Continuity to point at the recalibration anchor + the new R2 handoff; clarify "Phases 12-17 authored" = ROADMAP/milestone prose (no phase dirs/PLANs yet).
- **Do NOT modify:** v0.1 historical metrics, Decisions log, frontmatter `progress` block (31/31 is correct for v0.1), milestone/status fields.
- **Verification:** re-read STATE; `grep -ni 'spike/001\|9186c8a\|2026-05-29' STATE.md` ≥1; no claim contradicts `git log -5`.

## Unit R2 — Add a real cold-start handoff  [D2 · recommended]
- **Objective:** kill the cold-start navigation trap (newest handoffs are pointer-stubs → gsd-2-uplift; newest real one predates the merge).
- **Output path:** `.planning/handoffs/2026-05-29-recalibration-handoff.md` (new file).
- **Content:** true position (post spike/001 merge; v0.2 planning; Phase 12 plan-1 NOT started); pointer to recalibration anchor + RECONCILE-PLAN; open dispositions (R5/R6); explicit "read STATE.md + this file, NOT the 2026-04-28 pointer-stubs."
- **Do NOT modify:** existing handoffs / pointer-stubs (leave as historical).
- **Verification:** file is newest by date in `.planning/handoffs/`; references HEAD `9186c8a`.

## Unit R3 — Fix CLAUDE.md doctrine-path defect  [D5 · recommended · DOCTRINE FILE]
- **Objective:** make dead doctrine load-points resolve. CLAUDE.md is auto-loaded startup context → treat as a careful, review-worthy edit (PROMPT §2.4); change is **path-only, no behavioral/posture change**.
- **Output path:** `CLAUDE.md` (edit, repo root).
- **Edits:** `` `LONG-ARC.md` `` → `` `.planning/LONG-ARC.md` `` (lines 30,31,32,35,59); `` `VISION.md` `` → `` `.planning/VISION.md` `` (lines 31,59). **Verify-at-exec:** `PROJECT.md` on line 59 — prefix to `.planning/PROJECT.md` IFF that is where it lives (`ls .planning/PROJECT.md`).
- **Do NOT modify:** ADR refs (`docs/adrs/…` resolve), `.planning/`-prefixed refs already correct (line 9 STATE.md, line 35 METHODOLOGY.md), prose/semantics. (Out of scope, optional later: stale "Roadmap Phases" §69-71 lists only 1-6.)
- **Verification:** every doc path in CLAUDE.md read-order/load-points resolves via `ls`; `git diff CLAUDE.md` shows only path prefixes.

## Unit R4 — Land uv.lock + .gitignore  [D6 · recommended]
- **Objective:** commit the corrected `uv.lock` (now pyproject-consistent: pkg `arxiv-sanity-mcp`, `pytest-asyncio 0.26.0 < 1`) + the benign `.gitignore` GSD-baseline block.
- **Rationale:** committed lock violated pyproject `pytest-asyncio>=0.24,<1` and was named `arxiv-mcp` (stale post-rename). CI installs via `pip … "pytest-asyncio>=0.24,<1"` (never reads uv.lock), so CI stayed green and the lock drift was invisible. The in-tree lock (re-resolved by this session's `uv run`) is the correct state.
- **Output paths:** `uv.lock`, `.gitignore` (both already modified in working tree; commit only).
- **Do NOT modify:** `pyproject.toml` (already correct).
- **Verification:** `uv run pytest --co -q` → 493, exit 0 (already confirmed); `git diff --cached` shows only lock + ignores.

## Unit R5 — Untracked WIP disposition  [needs your decision]
- `skills-lock.json` — 16-skill lockfile (source+hash). Q2 below.
- `.planning/audits/2026-05-08-long-horizon-doctrine-load-points/CONSUMER-REQUIREMENTS.md` — finished gsd-2-uplift-migration input spec. Q3 below. **Relocating to gsd-2-uplift crosses a project boundary → human-gated (PROMPT §3.4); I will not move it without explicit approval.**

## Unit R6 — Branch cleanup  [D7 · destructive · human-gated]
- `pull-1` (`1fc96fc`) — broken-nested divergent misclone, no unique flat code. `spike/001-volume-filtering` (`986855c` = `dd1a34b^2`, fully in main history; origin gone).
- **Destructive** (`git branch -D`) → human-gated (PROMPT §3.4 + contract §3). I will record both tip SHAs first (reflog-recoverable ~90d; `986855c` permanently safe via the merge). Q4 below. **Default recommendation: park with revisit trigger (before next publish/tag), not delete this session.**

---

## Commit / sequencing
- Per your global trunk-based-for-solo doctrine: atomic commit per unit (R1, R2 can share; R3; R4) — Q1 decides direct-to-main vs a short `reconcile/state-drift-2026-05-29` branch.
- One unit → commit → next. No push/tag/publish (all outward-facing → separate gate, PROMPT §3.4). Tests re-run after R3/R4.
- Method note: deliberately NOT a workflow fan-out (contract bans auto-acceptEdits fan-out on a tracked tree); bounded inline edits with gates.
