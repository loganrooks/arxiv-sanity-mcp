# PR: `spike/001-volume-filtering` → `main` — branch-debt payoff

**Disposition:** single bundled PR. History preserved as-written; no squash, no filter-branch, no graft. Companion artifact: [`POSTMORTEM.md`](./POSTMORTEM.md) (audit-grade, ~180 lines).

**Scope:** `.planning/` and `docs/` and root governance files only. **No source code, tests, migrations, or build artifacts touched.** Safe to merge from a "won't break v0.1 software" perspective.

**Volume:** 223 commits, 447 files, +187,549 / −658 lines. 61% of additions are JSON spike-experiment checkpoints (reproducibility artifacts, not generated noise). Zero secrets, zero `.env`, zero venv pollution.

---

## Summary

This branch was born 2026-03-15 to execute spike-001 (volume filtering / scoring landscape) and never closed. Over 7.5 weeks it absorbed seven additional workstreams: spikes 002-008, the v0.1→v0.2 milestone pivot, ADR-0005 + the rest of the ADR/governance corpus, the foundation audit, the full v0.2 paired/governance audit cycle, and the gsd-2-uplift methodology initiative (now extracted to its own repo).

Local `main` has not advanced since 2026-03-15 while this branch grew. **The branch is the de-facto working trunk.** The branch-hygiene rule ("branches older than ~2 weeks are a smell") was breached by ~5.5 weeks. The post-mortem (`POSTMORTEM.md`) is candid about how that happened and what discipline would have caught it earlier; that discipline question is post-merge work.

The branch is now structurally clean — gsd-2-uplift extraction commit `753f67a` removed that workstream's content from tree on 2026-05-08 — so a merge decision is genuinely on the table. No conflicts expected against local `main`.

---

## What's in this PR

Eleven workstreams entangled by cross-references. Splitting would create broken-reference half-merges; full table and rationale in `POSTMORTEM.md` §Workstream Inventory.

| # | Workstream | Date range | Status |
|---|---|---|---|
| 1 | Foundation docs + ADRs (initial set: 0001-0004) | 2026-03-17 | Complete |
| 2 | Spike-001: volume filtering / scoring landscape | 2026-03-15 → 03-19 | Complete (DECISION + FINDINGS shipped) |
| 3 | Spike-002: backend comparison | 2026-03-18 → 03-19 | Complete |
| 4 | Spike-003: strategy profiling | 2026-03-19 → 03-26 | Complete (closed with qualifications, deliberation logged) |
| 5 | Spike-004: embedding model evaluation | 2026-03-26 → 03-30 | Complete |
| 6 | Spikes 005-008 (next-round suite) | 2026-04-16 → 04-25 | Complete (007 override + 008 supersession per `bfe73a1`) |
| 7 | v0.1 freeze + v0.2 pivot (planning + roadmap) | 2026-04-16 → 04-25 | Complete |
| 8 | v0.2 paired audits + ADR-0005 + governance corpus | 2026-04-25 → 04-27 | Complete |
| 9 | gsd-2-uplift initiative — **extracted to dedicated repo** | 2026-04-27 → 05-01 | See §"About the 45 gsd-2-uplift commits" below |
| 10 | gsd-2-uplift housekeeping (post-extraction) | 2026-05-08 | Complete |
| 11 | WIP / handoff checkpoints (interleaved) | throughout | Honest pause-points |

### Headline artifacts (durable outputs)

- **ADR-0001..ADR-0005** under `docs/adrs/` — including the v0.2 multi-lens commitment in ADR-0005.
- **Project CLAUDE.md** at repo root — accepted decisions, doctrine load-points, governance read-order map. (Note: cites ADRs 0001-0005, foundation audit, ECOSYSTEM-COMMENTARY, LONG-ARC, VISION, METHODOLOGY — all of which are also on this branch and land together. See "Why one PR" below.)
- **AGENTS.md** at repo root — agent behavior rules, anti-patterns, deliberation boundaries.
- **`.planning/STATE.md`, `PROJECT.md`, `ROADMAP.md`, `REQUIREMENTS.md`, `LONG-ARC.md`, `VISION.md`** — all reflecting post-v0.1 / pre-Phase-12 reality.
- **`.planning/spikes/001..008/`** — full spike program with DESIGN, FINDINGS, DECISION, supersession notes, methodology audits.
- **`.planning/foundation-audit/`** — FINDINGS.md + METHODOLOGY.md.
- **`.planning/audits/`** — including the v0.2 paired-audit cycle (cross-vendor + same-vendor adversarial + xhigh independent + comparison + synthesis) and this post-mortem.
- **`.planning/deliberations/`** — chronological deliberation log including the v0.2 pivot decisions.

---

## About the 45 gsd-2-uplift commits (the shift)

This is the load-bearing thing this PR description has to explain clearly, because future readers will ask "why are there 45 commits about a thing that isn't in the tree?"

### What gsd-2-uplift is

A meta-initiative — not arxiv-sanity-mcp work — about whether the GSD (Get Shit Done) v1 project-management methodology can be uplifted to handle complex experimental-AI work. arxiv-sanity-mcp is a **test case** for that question. The initiative ran 2026-04-27 → 2026-05-01 and accumulated weight inside `.planning/gsd-2-uplift/` (~25 deliberations, ~15 audit folders, an 842-line trajectory plan, ~5.6 MB subtree).

### Why it was extracted

On 2026-05-01 the initiative reproduced a closure-pressure-into-elaboration pattern at a meta-level (6 commits / ~250K codex tokens producing audit-of-audit infrastructure to verify a plan revision for mapping work that hadn't started). The disposition: **extract gsd-2-uplift to its own repo + clean arxiv-sanity-mcp**. The corrected framing landed 2026-05-08: *connection-by-question, not co-location* — gsd-2-uplift exists to ask whether gsd-2 can handle this kind of work; arxiv-sanity-mcp is the test case; the substrate-evidence channel is preserved post-extraction via cross-repo references, not via co-location.

### How the extraction was done

**Content-only migration** — *not* `git subtree split`. A new repo was bootstrapped at `~/workspace/projects/gsd-2-uplift/` from a snapshot. The new repo has 2 commits total (`bb0650e` initial population + `d1a2833` paired-hash record). **The 45 commits of history exist only on this branch.** That's a deliberate trade-off: history-preservation across repos was rejected as costlier than the documentary alternative.

The documentary alternative is `.planning/extraction/EXTRACTION-LOG.md`, which records:
- Cross-repo commit identity pair: `4457c30 (arxiv-sanity-mcp pre) ↔ bb0650e (gsd-2-uplift initial)`
- Per-artifact disposition table (~110 files MOVEd; 17 pointer-stubs created at moved-from paths)
- DUPLICATE artifacts updated with bidirectional cross-references
- Cleanup edits to CLAUDE.md / STATE.md / PROJECT.md / LONG-ARC.md / `deliberations/INDEX.md`

### Why we kept the 45 commits in branch history (option b3)

Three options were considered for these commits during merge-prep:
- **(a) Keep as-is** — chosen. Honest record that this work happened on this branch.
- **(b) Squash to one** — would have required interactive rebase across 60 commits with 45 fixups, conflicting on shared files (CLAUDE.md, STATE.md, INDEX.md) since uplift commits and non-uplift commits both edit them. Estimated 1-2 hours of conflict resolution with non-trivial subtle-error risk.
- **(c) `git filter-branch` to drop** — ironically *more* historically dishonest than (a) since the work absolutely did happen here.

The 45 commits, listed in chronological order with a one-line per:

```
5129569 add INITIATIVE.md staging artifact
52c09e0 integrate Stage 1 audit findings (Option α)
cfee8d6 update INITIATIVE.md per dispatch-readiness decisions B1-B6
edefdaf add orchestration package per decision B6
52ee43c add cross-vendor pre-pilot audit of orchestration package
6d1063b apply within-artifact revisions per cross-vendor audit
3681ada focused cross-vendor re-audit + addendum fixes; package clean to proceed to pilot
e9d99dd W1 slice 1 pilot output + side-investigation evidence
26cae76 apply slice prompt revisions + synthesis input update + STATE.md per framing-widening Part II §6
d191095 W1 slices 2-5 outputs (parallel cross-vendor dispatch at GPT-5.5 high)
41cf12b capture gsd-2 audit wave 1
5c513fc capture gsd-2 audit wave 2
d627a02 synthesize gsd-2 audit findings
54bb73b W2 audits + slice (vi) addenda + disposition log + predecessor handoff
5313e6c W3 first-wave syntheses (same-vendor + cross-vendor paired)
73e5615 SYNTHESIS-COMPARISON.md draft-complete + drafting decisions DC0-DC4
4c7ad01 v1-GSD mental-model premise-bleed audit spec (draft-for-disposition)
b229940 audit-spec arc — AUDIT-SPEC.md v2 + DECISION-SPACE.md §1.17 + deliberation log
ac609c9 coordination updates reflecting comparison-draft + audit-spec arcs
b8db2a0 v1-GSD premise-bleed audit-arc — Step-1 + Step-2-independent + differential + disposition
fae9650 SYNTHESIS-COMPARISON.md §7 audit addendum + frontmatter status update
a79e761 coordination updates reflecting audit-arc completion + disposition trail
f1e0a68 trajectory plan (in-repo) + Phase A plan-self-audit + revise-before-execute disposition
092da0b coordination updates reflecting Phase A completion
ee1716d Phase B standing-context artifact + CLAUDE.md load-point + audit
24aad62 coordination updates reflecting Phase B completion
767ad6f Phase B verification + G-1 addendum
004a1a7 G-3 follow-up — broaden doctrine-load-point trigger to cover STATE.md uplift-status edits
4422bab trajectory plan Phase C step 2 — INCUBATION-CHECKPOINT.md surfacing draft
e1da6ae Phase C steps 3-5 + audit-disposition (Option 4 hybrid)
98505f1 Phase C VERIFICATION.md — goal-delivered, green-light C→D
50f7261 Phase C step 6 — INCUBATION-CHECKPOINT.md §7.10 Phase D entry pre-mini-spec amendment
5a377fb Phase D entry Steps 0-5 + paired audit + Revise-before-dispatch revisions
c0465a4 Phase D dispatch mid-arc — Step 6 + methodology + Option 4 + Option 5 + structural review
43e652b Phase D mid-arc methodology-mismatch finding + (V'.a) trajectory-replan disposition
c1b098c EXTERNAL-VISION-CONTEXT.md + 12-property substrate-vision articulation
ffc0fb0 trajectory plan (V'.a) Step 2 — mapping-shape Phase D + self-review revisions
f6af0f1 (V'.a) Step 3 audit-spec-drafting brief for cross-vendor codex (B-strong)
da64b2c (V'.a) Step 3 Claude-parallel-skeleton authored blind to codex output (P2 timing)
f15dc5d (V'.a) Step 3 audit-spec — codex AUDIT-SPEC.md + DIFFERENTIAL-SPEC.md vs Claude-parallel-skeleton
fbfab8b extraction-planning handoff (small + temp; pre-context-clear)
4457c30 commit dispatch logs for 2026-05-01 trajectory-replan-audit spec drafting
753f67a extract initiative to dedicated repo + cleanup planning tree   ← extraction commit
45956cc rewrite MOVEd-content references in DUPLICATE artifacts
1eab859 drop residual directory shell + scrub live governance refs
```

The net diff of all 45 commits combined with the extraction is small: pointer-stubs at moved-from paths + `EXTRACTION-LOG.md` + DUPLICATE-artifact cross-references + cleanup edits to CLAUDE.md / STATE.md / PROJECT.md / LONG-ARC.md / `deliberations/INDEX.md`. The intermediate diffs added then removed roughly 30,000+ lines that exist now only in commit history, not in HEAD's tree.

---

## Why one PR, not several

Workstreams 1, 7, 8, 11 are mutually entangled — STATE.md / PROJECT.md / ROADMAP.md edits in #7 cite ADRs from #8; governance docs from #8 cite the foundation audit from #1; CLAUDE.md edits depend on ADRs from both #1 and #8. Splitting these creates broken-reference half-merges that are worse than no split.

Spikes 001-008 (#2-#6) are sequenced and cross-citing — spike-002 references spike-001's volume model; spike-003 builds on spike-002's backend choice; spikes 005-008 are the "next-round suite" derived from 001-004's findings. Splitting per-spike creates multiple PRs that all want to land in order with no parallelism gain.

All workstreams touch only `.planning/` and `docs/`. There's no high-risk infrastructure change that needs to be isolated for code review. This is a solo research repo with no external review queue — splitting buys nothing operational.

---

## Cleanliness audit

Total: **+187,549 / −658 lines** across 447 files.

| Category | Lines | % |
|---|---|---|
| JSON / CSV / JSONL data files (spike experiment artifacts) | 114,359 | **61%** |
| Markdown (docs, audits, deliberations, FINDINGS, etc.) | 43,500 | 23% |
| Python (spike experiments, harnesses) | 29,657 | 16% |
| Other | 33 | 0% |

Top 5 files = ~70k lines (37% of total), all spike experiment-result JSONs:
- `005-evaluation-framework-robustness/experiments/checkpoints/phase1_quantitative.json` — 27,801 lines
- `006-model-retrieval-interactions/experiments/checkpoints/phase1_quantitative.json` — 19,223 lines
- `004-embedding-model-evaluation/experiments/checkpoints/pre_spike_analyses.json` — 11,668 lines
- `003-strategy-profiling/experiments/data/w3_4_pipeline_profiles.json` — 5,364 lines
- `004-embedding-model-evaluation/experiments/checkpoints/phase2_metrics.json` — 4,987 lines

These are reproducibility artifacts and arguably *should* be in version control for a research project that values traces over erasure. The 27k-line single-file checkpoints are a smell worth follow-up (split-by-phase, or move to `/data/` with a manifest pointer) — but no action required for this merge.

No `.env`, no credentials, no venv, no `node_modules`, no generated artifacts.

---

## Known issues, not blocking this merge

Three items surfaced in `POSTMORTEM.md` §Open Questions that are *not* gating this merge but should be addressed downstream:

1. **`origin/main` is structurally broken.** Last advanced 2026-04-20 with `692a607` (PyPI rename) which somehow nested the entire tree under `workspace/projects/arxiv-sanity-mcp/`. Local `main` has the correct flat layout. **Cannot push to origin without resolving this** — this is a separate publishing problem, not a merge-to-local-main blocker. The `v0.1.0` tag is anchored on the broken origin/main lineage and will need re-anchoring when origin/main is fixed.
2. **Spike-008 supersession visibility.** `bfe73a1` documents the supersession; the directory has only 3 files. A one-line README in `008-function-in-use-and-blind-spots/` may help future readers connect the two. Not checked.
3. **Foundation-audit pending validations.** Q1 / Q4 / Q16 have closure rationales recorded; Logan-validation pending. Tracker in `STATE.md` §Pending Validations.

---

## Test plan

This is a `.planning/` + `docs/` PR. No code changes. Verification:

- [x] No `src/` / `tests/` / `alembic/` / `pyproject.toml` files modified (verified via `git diff main..HEAD --stat | grep -E "^(src|tests|alembic|pyproject)"`)
- [x] No accidentally-committed secrets, credentials, `.env`, or large binaries
- [x] `.gitignore` properly configured and respected (no venv / cache / node_modules pollution)
- [x] Working tree matches HEAD's tree-hash `efb5fc2cb8de44ff966da5cfe5108790581062e8`
- [x] Safety tag `backup/spike-001-pre-squash` exists at `1eab8591` for rollback
- [ ] Local `main` fast-forward / merge succeeds with no conflicts (to be confirmed at merge time)
- [ ] Post-merge `git log main --oneline` shows the 223 commits in expected chronological order

---

## Companion artifact

[`POSTMORTEM.md`](./POSTMORTEM.md) — full audit of the branch: workstream inventory, risk items, volume/cleanliness audit, PR-strategy rationale, open questions for Logan, cited evidence (commit hashes and key paths). ~180 lines, 10-15 minute read.

---

*Generated 2026-05-08 by Claude in coordination with Logan. Single-author repo, no external reviewer; this PR description doubles as the merge-commit explanation and the historical record of "why does this branch look the way it does." The commit-history-as-ledger is preserved per option (b3) — no squashes, no grafts, no rewrites.*
