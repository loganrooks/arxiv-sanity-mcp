# arxiv-sanity-mcp — RECALIBRATE state anchor

**Status: ground-truth snapshot (read-only), 2026-05-29**
Author: Claude Code (Opus 4.8), executing `PROMPT.md` RECALIBRATE phase.
This file is the recoverability anchor (PROMPT.md §1.1). It records verbatim command output captured at session start. Reconstruction findings, drift map, and the RECALIBRATE-EXIT determination are appended below after the parallel read-only forensics complete.

---

## 0. Pre-flight — does the GSD surface resolve here? (§0.5)

`gsd-sdk --help` — **CLI resolves** at `/home/rookslog/.npm-global/bin/gsd-sdk`:

```
Commands:
  run <prompt>          Run a full milestone from a text prompt
  auto                  Run the full autonomous lifecycle (discover -> execute -> advance)
  init [input]          Bootstrap a new project from a PRD or description
  query <argv...>       Registered query handlers only (longest-prefix argv match; see QUERY-HANDLERS.md)
```

`gsd-*` **skills**: many resolve in the skill registry (gsd-health, gsd-resume-work, gsd-plan-phase, gsd-forensics, gsd-progress, etc.).

**PRE-FLIGHT VERDICT [obs]:** GSD CLI + a full `gsd-*` skill suite are installed. Per operating contract these are *optional accelerants*; git + code + tests + files remain the primary ground-truth path. `gsd-sdk query` is registered-handlers-only (no guaranteed enumerable list).

## 0.5 Read-only reality (§1.0)

`.claude/settings.json` hooks: `SessionStart` → `gsd-check-update.js`; `PostToolUse` → `gsd-context-monitor.js`. **No `PreToolUse` Edit|Write deny hook. No `PreToolUse` Bash deny hook.**

**[obs] READ-ONLY IS HONOR-SYSTEM THIS SESSION.** Plan mode / read-only posture is unenforced; the only enforcement is operator discipline. The single authorized write during RECALIBRATE is this state file (a new, reversible artifact under `.planning/recalibration/`). No tracked-file edits.

---

## 1.1 Git / worktree snapshot (verbatim)

### `git status --short --branch`
```
## main...origin/main
 M .gitignore
?? .planning/audits/2026-05-08-long-horizon-doctrine-load-points/
?? PROMPT.md
?? skills-lock.json
```

### `git stash list`
```
(empty)
```

### HEAD / branches / tracking
```
HEAD: 9186c8a7e1c23d9e972e8c29af2cbe14493c60b7
* main                       9186c8a [origin/main] chore(pyproject): rename PyPI distribution to arxiv-sanity-mcp
  pull-1                     1fc96fc chore(pyproject): rename PyPI distribution to arxiv-sanity-mcp
  spike/001-volume-filtering 986855c [origin/spike/001-volume-filtering: gone] docs(audits): branch post-mortem + PR description for spike/001 → main

ahead/behind origin/main: 0  0
```

### `git log --oneline -25` (head)
```
9186c8a chore(pyproject): rename PyPI distribution to arxiv-sanity-mcp
dd1a34b Merge branch 'spike/001-volume-filtering' — branch-debt payoff (224 commits, 11 workstreams)
986855c docs(audits): branch post-mortem + PR description for spike/001 → main
1eab859 docs(gsd-2-uplift): drop residual directory shell + scrub live governance refs
2dd6f4d docs(handoffs): archive 2026-05-01 extraction-planning handoff post-Phase-H
...
```

### `git rev-list --count dd1a34b^1..dd1a34b^2` → `224` (confirms "224 commits" on spike side)

### Per-item WIP assessment (untracked / modified)
| Path | What it appears to be | Deliberate WIP? |
|---|---|---|
| ` M .gitignore` | Modified gitignore (4 lines added per merge stat history) | Likely deliberate; preserve. Verify diff during REVIEW. |
| `?? .planning/audits/2026-05-08-long-horizon-doctrine-load-points/` (`CONSUMER-REQUIREMENTS.md`) | An audit dir dated 2026-05-08, not yet committed | **Likely deliberate WIP** (matches doctrine-load-point work referenced in CLAUDE.md). Preserve; do not clean. |
| `?? PROMPT.md` | The revival prompt being executed (this session) | External input, not project WIP. Leave as-is. |
| `?? skills-lock.json` | 4.2 KB, perm 0600, dated 2026-05-08 | **Possible deliberate WIP** (skill surface lock). Preserve; assess in REVIEW. |

**Preservation directive:** worktree is sacred (operating contract §2). No `git clean`, `restore`, `checkout --`, `stash`, `reset`. All four items above treated as potentially-deliberate until proven otherwise.

---

## 1.2 Reconstruction — what is actually true

Reconstructed by 5 parallel **read-only Opus** forensic agents (workflow `wf_fad979a6-c80`, 2026-05-29). All claims are `git`/file-anchored; the agents ran no mutating git/file commands. (One side-effect drift — `uv.lock` — is disclosed in §Drift-D6.)

### spike/001-volume-filtering — the 224-commit merge `dd1a34b`
- **[obs]** `git rev-list --count dd1a34b^1..dd1a34b^2` = **224**; `git show dd1a34b --stat` = **449 files, +187,926/-658**. Parents: `4501420` (stale local main, branch base 2026-03-15) + `986855c` (spike tip).
- **[obs] ZERO shipped code touched.** `git diff --numstat dd1a34b^1 dd1a34b -- src/arxiv_mcp tests/ alembic pyproject.toml` = **0 files**. Breakdown: `.planning/` 428, `docs/` 18, root governance 3 (`.gitignore +4`, `AGENTS.md +37/-6`, `CLAUDE.md +71`). **No v0.2 feature delivery whatsoever.**
- **[obs] What it was:** branch-debt payoff. A single branch (born 2026-03-15, ~7.5 weeks, never closed) became the de-facto working trunk while local `main` never advanced. 11 accreted workstreams: foundation ADRs 0001-0004; spikes 001-008; v0.1-freeze/v0.2-pivot planning; v0.2 paired audits + **ADR-0005 (multi-lens)** + governance corpus; the **gsd-2-uplift** meta-initiative (content *extracted out* to `~/workspace/projects/gsd-2-uplift/` @ `753f67a`, ~45 commits net-zero to tree); housekeeping; interleaved WIP/handoff checkpoints. ~61% of +187k lines are JSON spike-experiment checkpoints.
- **[obs] v0.2 relevance** = the *planning substrate only* (ADR-0005 + authored ROADMAP/REQUIREMENTS for Phases 12-17). No Phase 12-17 deliverable.
- **[obs]** PyPI rename `9186c8a` is a *separate post-merge* commit (3 files, 1-line distribution-name string) — not feature work, not inside the merge.

### Branch & untracked disposition
- **[obs] `pull-1` (`1fc96fc`, 2026-04-20):** STALE / STRUCTURALLY-BROKEN / DIVERGENT. `merge-base(main,pull-1)=9186c8a`; `main..pull-1`=209, `pull-1..main`=432; `git diff --stat`=756 files +12,429/-192,500. `git ls-tree pull-1` top-level = `{.gitignore, .planning, workspace}` → carries the **entire project nested under `workspace/projects/arxiv-sanity-mcp/`** (the old broken-origin/main misclone pathology). Holds the v0.1 lineage in broken-nested form; **no unique flat-layout code** (main has the flat v0.1 code). → consolidate/delete candidate **(human-gated; destructive — not actioned).**
- **[obs] `spike/001-volume-filtering` (`986855c`):** == `dd1a34b^2`, already merged; `origin/...: gone`. Local-only leftover; deletable post-confirm (human-gated).
- **[obs] Untracked WIP (preserve):** `2026-05-08-long-horizon-doctrine-load-points/CONSUMER-REQUIREMENTS.md` (305 lines, finished gsd-2-uplift-migration input spec — land as historical record *or* relocate to gsd-2-uplift); `skills-lock.json` (16-skill lockfile, source+hash — landable tooling config). Both NOT git-ignored. `PROMPT.md` + `.planning/recalibration/` = this session's artifacts.

### Test reality — **GREEN** (verified, supersedes any doc/agent guess)
- **[obs]** `uv run pytest --co -q` → **493 collected, exit 0** (exact match to STATE's "~493"; the "~" is unwarranted).
- **[obs]** Full CI-equivalent run `DATABASE_URL=… TEST_DATABASE_URL=… uv run pytest tests/ --timeout=30 --deselect tests/test_content/test_service.py -q` → **`480 passed, 2 skipped, 11 deselected in 63.83s`, exit 0.** Math reconciles: 493 − 11 deselect = 482 = 480 pass + 2 skip. 0 failed / 0 errored.
- **[obs]** Suite needs a live Postgres test DB (`tests/conftest.py:92-145`); `pg_isready localhost:5432` = accepting, dedicated `arxiv_mcp_test` DB exists. Per-test fixtures create/drop their own tables in that test DB (designed; no prod/repo/git mutation). The 11 deselected = `test_content/test_service.py` integration tests, exactly as CI deselects them (STATE.md:189).
- Note: validated against `pytest-asyncio 0.26.0` (pyproject `<1` pin), the re-resolved set — see §Drift-D6.

### Knowledge store (project-local is PRIMARY; global is legacy fallback)
- **[obs]** A global signal `sig-2026-04-09-stale-claude-md-kb-path-misleads-agents` records that the KB **migrated to project-local `.planning/knowledge/`**; `~/.gsd/knowledge/` is now legacy fallback. Read both per protocol; weight the local one.
- **[obs] Most relevant local signal — `sig-2026-04-16-inter-milestone-exploration-gap`** (occurrence_count 2): *"v0.1 milestone was completed but never formally archived, and spike-program work began immediately afterward… too complete to treat as an active implementation milestone, too consequential to treat as unstructured side work."* This **predicts exactly the stall we are recalibrating.**
- **[obs] Recurring guardrails present** (apply as general epistemic discipline): premature closure (occurrence 4 — *walk the DESIGN.md as a checklist*), untested-hypotheses-as-findings (critical), no-CI-verification (*trigger the failure, don't just check the gate exists*), model/effort-profile mismatch, config-version drift, **stale-high-authority-docs-mislead-agents**, performative/lapsed delegation, acting-without-authorization-on-shared-state, late inter-milestone orchestration. Absent from corpus: explicit "hallucinated-done", "weaker-model-third-pass", "PR-to-wrong-repo".
- **[obs]** `sig-2026-03-30-explorer-reasoning-effort-high-at-most` — exploration agents capped at `high` effort. (This session used Opus-tier non-Explore agents for gating evidence, consistent with that + with stored feedback.)

## 1.4 DRIFT MAP — what's actually true vs what the docs claim

| # | Claim (source) | Ground truth | Verdict | Sev |
|---|---|---|---|---|
| D1 | STATE.md:32 "Last implementation activity: 2026-03-14 — Phase 10 P03" is current | `9186c8a` PyPI rename (2026-05-08) + `dd1a34b` 224-commit merge (2026-05-08) are later activity; STATE never mentions either | **DRIFT** (stale-snapshot) | **high** |
| D2 | "Resume by reading the latest handoff" (cold-start norm) | Newest handoffs (2026-04-28 W1/W2) are **pointer-stubs → gsd-2-uplift repo**; newest *real* handoff `2026-04-26` predates the 2026-05-08 merge; the merge is documented **only** in `audits/2026-05-08-branch-postmortem.../POSTMORTEM.md`, unreferenced from STATE/handoffs → cold-start **navigation trap** | **DRIFT** (stale-snapshot) | **high** |
| D3 | STATE.md:8 `last_updated 2026-05-08T00:00:00Z` reflects current position | Midnight stamp predates HEAD (`9186c8a` 14:26) and merge (`dd1a34b` 14:15) by ~14h; omits merge/224-commits/PyPI-rename/postmortem (`grep` exit 1) | **STALE** | med |
| D4 | POSTMORTEM: "origin/main structurally broken @`692a607` nested layout — cannot publish" | `git show -s origin/main` now = `9186c8a` (flat, == local main); broken nesting survives only on local `pull-1`. Resolved at origin since the postmortem | **STALE** | med |
| D5 | CLAUDE.md read-order + doctrine load-points reference root `VISION.md` / `LONG-ARC.md` | Canonical copies are **`.planning/VISION.md`** + **`.planning/LONG-ARC.md`**; root copies never existed (`git log --all` empty). Root-relative doctrine load-points resolve to nothing | **DRIFT** (doc-path defect) | med |
| D6 | Committed `uv.lock` matches `pyproject.toml` | Committed lock names pkg `arxiv-mcp` (stale post-rename) and pins `pytest-asyncio 1.3.0` which **violates** pyproject `>=0.24,<1`. `uv run` (this session) re-resolved → working-tree `uv.lock` corrected (pytest 8.4.2 / pytest-asyncio 0.26.0). **Side-effect drift I introduced, revealing a pre-existing inconsistency** | **DRIFT** (caused + pre-existing) | med |
| D7 | (cleanup) local `pull-1` + `spike/001` branches | `pull-1` = broken-nested divergent misclone; `spike/001` = already-merged leftover (origin gone) | n/a — consolidate/delete candidates (human-gated) | med |
| P1 | STATE: "Phases 12-17 authored" | True **only as ROADMAP/milestone prose + ADR-0005**; `find .planning/phases` shows no dir > 10, no `12-*-PLAN.md`. STATE itself concedes "plan-1 authoring not started" | **PASS** (clarify: charter-prose, not phase-scaffold) | low |
| P2 | STATE/CLAUDE: 31/31 plans; 13 tools / 4 resources / 3 prompts; shipped 2026-03-14; ~493 tests | `*PLAN*`=31, `*SUMMARY*`=31; `@mcp.tool`=13/`@mcp.resource`=4/`@mcp.prompt`=3; v0.1.0 tag `31abb5a` 2026-03-13/14; **493 collected, suite GREEN** | **PASS** (verified) | low |
| P3 | Phase 11 gap | No "Phase 11" in ROADMAP; numbering jumps 10→12 undocumented `[inf]` deliberate v0.1/v0.2 buffer | UNKNOWN→low | low |

## 1.5 Charter-derived goal (from ROADMAP + v0.2-MILESTONE + ADR-0005, not the handoff)

**v0.2 goal (one sentence):** turn ADR-0001's "multiple retrieval/ranking strategies coexist" from design aspiration into a delivered **multi-lens MCP substrate** — generalize the profile/ranking primitive so ≥2 structurally-distinct lenses (existing semantic/lexical stack + a new citation/community lens) coexist, exposing lens-disagreement/intersection as first-class MCP operations, **with the v0.1 ranking core preserved (all v0.1 tests pass unmodified).**

- **Phase 12 = Lens Abstraction Primitives** (refactor single-lens → multi-lens, no behavioral regression). **Plan-1** = `Lens` protocol + scorer registry + register semantic lens + regression tests. Depends on nothing; head of critical path `(12 ∥ 14) → 15; 12 → 13; (13 ∧ 15) → 16 → 17` (15 plans).
- **Charter STOP-rules:** don't rewrite the v0.1 ranking core (ADR-0001 coexistence); fusion is not the default (per-lens dict; explicit `mode="fusion"`); no silent defaults / no implicit profile learning; out-of-scope for v0.2 = third lens, second citation source, behavior-derived signals, multi-user, **pgvector/graph-DB backend** (Stack D foreclosed).
- **No charter↔STATE conflict on next step:** both point to authoring Phase 12 plan-1.

## RECALIBRATE EXIT

**(a) Worktree:** `main @ 9186c8a`, 0/0 vs `origin/main`, stash empty. Tracked-mod: `.gitignore`, `uv.lock` (D6, session-caused). Untracked: `2026-05-08-long-horizon-doctrine-load-points/`, `skills-lock.json` (both deliberate WIP — preserve), `PROMPT.md` + `.planning/recalibration/` (session). HEAD/branches unchanged across the read-only workflow.
**(b) Top drifts:** D1 stale "last impl activity" (high) · D2 cold-start handoff trap (high) · D3 stale STATE snapshot (med) · D5 CLAUDE.md doctrine-path defect (med) · D6 uv.lock↔pyproject inconsistency (med).
**(c) Charter goal:** ship the v0.2 multi-lens substrate; immediate next = author Phase 12 plan-1 (Lens protocol + registry), preserving the v0.1 core.
**(d) Valid resume path:** GSD CLI + full `gsd-*` skill suite resolve here, so native `gsd-progress`/`gsd-resume-work`/`gsd-plan-phase` are available — **but a clean resume is not clean** (stale STATE + cold-start handoff trap + localized late-orchestration). → **Reconcile-first (light), then resume.** Read-only this session is **honor-system** (no Edit/Write/Bash deny hook).

### Late-orchestration determination (gating) — **MIXED**
- **v0.1 build → NO.** Planning kept pace: 31 PLAN + 31 SUMMARY, 10 VERIFICATION (one per phase dir; only Phase 10 lacks one), all committed by the v0.1.0 ship (`31abb5a`, 2026-03-13/14); code (13 tools/4 res/3 prompts) matches docs.
- **spike/001 merge `dd1a34b` → YES (localized).** 224 commits / ~7.5 weeks / 11 workstreams governed **only** by a *retrospective* `POSTMORTEM.md` (committed `986855c` at 14:15:23, ~20s before the merge it documents; commit msg: "Generated as a working artifact for the merge decision"). No forward PLAN/SUMMARY/VERIFICATION; the spike dir has DESIGN/DECISION/FINDINGS (spike-format) but no plan/summary/verification. STATE never caught up.

**Consequence (per PROMPT §RECALIBRATE-EXIT):** because late-orchestration is present (even if localized to already-landed work), **Clean-resume is NOT offered as a standalone first option.** Eligible: **Reconcile-first** (recommended), Consolidate, Triage.

---

## STATUS: RECALIBRATE complete — STOPPED for human direction (PROMPT FIRST-10 §10)
No REVIEW deep-dive, no PROCEED implementation, and no further writes beyond this anchor pending direction.
