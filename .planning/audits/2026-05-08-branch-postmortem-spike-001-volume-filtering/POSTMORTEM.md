# Branch Post-mortem: `spike/001-volume-filtering`

**Audit date:** 2026-05-08
**Branch:** `spike/001-volume-filtering`
**Branch base (local main):** `4501420 docs(spike-001): add interactive explorer prototype to design` (2026-03-15)
**Branch tip:** `1eab859 docs(gsd-2-uplift): drop residual directory shell + scrub live governance refs` (2026-05-08)
**Volume:** 223 commits, 447 files, +187,549 / -658 lines, ~7.5 weeks of activity

---

## Summary

This branch was born 2026-03-15 to execute spike-001 (volume filtering / scoring landscape) and never closed. Over 7.5 weeks it absorbed seven additional workstreams: spikes 002-008, the v0.1→v0.2 milestone pivot, ADR-0005 and the rest of the ADR/governance corpus, the foundation audit, the full v0.2 paired/governance audit cycle, and the gsd-2-uplift methodology initiative (now extracted to its own repo). The branch is the de-facto working trunk; **local main has not advanced since 2026-03-15** while the branch grew. The user's branch-hygiene rule ("branches older than ~2 weeks are a smell") was breached by ~5.5 weeks. The branch is now structurally clean (gsd-2-uplift extraction commit `753f67a` removed that workstream's content from tree on 2026-05-08), so a merge decision is genuinely on the table.

There is also a separate-but-related issue: **`origin/main` is structurally broken** — see "Open Questions" §1.

---

## Workstream Inventory

Workstreams clustered by commit-message scope, content domain, and file paths. Commit-counts approximate (some commits span multiple workstreams).

| # | Workstream | Date range | Commits | Volume (lines) | Status | Disposition |
|---|---|---|---|---|---|---|
| 1 | **Foundation docs + ADRs (initial)** | 2026-03-17 | ~3 | ~2,000 docs/, ~600 .planning/ | Pending — never landed on main | **Land** — referenced by project CLAUDE.md as authority |
| 2 | **Spike-001: volume filtering** | 2026-03-15 → 2026-03-19 | ~18 | ~12,326 | Complete (DECISION + FINDINGS shipped) | **Land** — original branch purpose |
| 3 | **Spike-002: backend comparison** | 2026-03-18 → 2026-03-19 | ~5 | ~10,647 | Complete | **Land** — coherent unit |
| 4 | **Spike-003: strategy profiling** | 2026-03-19 → 2026-03-26 | ~24 | ~38,856 | Complete (closed with qualifications, deliberation logged) | **Land** |
| 5 | **Spike-004: embedding model eval** | 2026-03-26 → 2026-03-30 | ~9 | ~50,347 | Complete | **Land** |
| 6 | **Spikes 005-008 (next-round suite)** | 2026-04-16 → 2026-04-25 | ~12 | ~55,000 | Complete (007 override + 008 superseded per `bfe73a1`) | **Land** — 008 is intentionally superseded; document why |
| 7 | **v0.1 freeze + v0.2 pivot (planning + roadmap)** | 2026-04-16 → 2026-04-25 | ~10 | ~717 in `.planning/` roots | Pending — never landed | **Land** — STATE/ROADMAP/REQUIREMENTS/PROJECT all reflect post-v0.1 reality |
| 8 | **v0.2 paired audits + ADR-0005 + governance corpus** | 2026-04-25 → 2026-04-27 | ~30 | ~10,000 audits + governance | Pending — never landed | **Land** — establishes the ADR-0005 multi-lens decision and governance read-order map; project CLAUDE.md cites these |
| 9 | **gsd-2-uplift initiative** | 2026-04-27 → 2026-05-01 | ~38 | ~0 (content extracted) | **Extracted** to `~/workspace/projects/gsd-2-uplift/` (`753f67a`) | **Decide:** keep history or filter-branch out — see Risk #2 |
| 10 | **gsd-2-uplift housekeeping (post-extraction)** | 2026-05-08 | 4 | ~129 (extraction log + pointer-stubs) | Pending | **Land with #9 decision** |
| 11 | **WIP/handoff checkpoints (interleaved)** | 2026-03-17 → 2026-04-28 | 10 (`wip:`) + 9 (`docs(handoff)`) | ~1,500 | Mostly transient context-handoff notes | **Land but consider squash** — handoffs proper live in `.planning/handoffs/`; some `wip:` checkpoints are orphan pause-points |

### Workstream Detail

**(2) Spike-001 — `001-volume-filtering-scoring-landscape/`**
Original branch purpose. Phase A1 (volume mapping, capability envelope), B/C (filtering strategies, ground truth, fair cross-model evaluation, null hypothesis testing). DESIGN/FINDINGS/DECISION/API-EMBEDDING-COST-ANALYSIS all shipped. 47 files, ~1,096-line round-3 results JSON. Headline finding visible in commits: "models are complementary, not competing" (`19fdffc`).

**(6) Spikes 005-008 — next-round suite**
Designed 2026-03-30 (`4c2b4eb wip: spike program paused — ready to design next round`), executed 2026-04-16, methodology-audited 2026-04-25 (`bfe73a1`: 007 override + 008 supersession). 005 and 006 carry the heaviest data weight (~52,000 lines combined, almost entirely JSON checkpoints). 008 is intentionally superseded — verify the supersession is documented before merge so it isn't read later as "abandoned spike."

**(8) v0.2 paired audits + ADR-0005**
Two parallel audit cycles in late April: (a) v0.2 plan paired audit (cross-vendor + same-vendor adversarial + xhigh independent + comparison + synthesis), (b) governance-doc paired audit. Both sit in `.planning/audits/2026-04-25-…/` and `.planning/audits/2026-04-26-…/`. ADR-0005 (`docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`) is the durable output. 619 lines total in governance synthesis alone.

**(9) gsd-2-uplift — extracted**
*Verified:* the working tree contains **no** `.planning/gsd-2-uplift/` directory; only `.planning/extraction/EXTRACTION-LOG.md` (129 lines) and a single tangential research-notes file remain. Per `753f67a` body: ~110 files MOVEd to new repo, 17 pointer-stubs created at moved-from paths, DUPLICATE artifacts updated with bidirectional cross-refs. Commits #1-#42 of this workstream still exist in branch history but their content is not in HEAD's tree. The 42 commits added then removed roughly 30,000+ lines (the diff stats *understate* what was moved through this branch because extraction netted those out).

---

## Risk Items

1. **`origin/main` structural breakage (highest risk).** `origin/main` (last commit `692a607`, 2026-04-20) has the entire project nested under `workspace/projects/arxiv-sanity-mcp/…`. Local main has the correct flat layout. Pushing this branch as-is to `origin` will produce a catastrophic-looking diff. **Resolve `origin/main` divergence before any merge to origin.** This is unrelated to branch contents but blocks publication.

2. **gsd-2-uplift commits are orphans in branch history.** 42 commits (`b8db2a0` through `1eab859` and ancestors) modify content that no longer exists in HEAD's tree. The diffs they introduce are net-zero after `753f67a` extraction. They are not load-bearing for current state but inflate commit count and make any rebase/squash review noisy. Three options: (a) keep as-is — honest history, +42 commits noise; (b) `git filter-branch` / `git replace` to drop them — cleaner but rewrites history; (c) interactive-rebase squash the entire gsd-2-uplift arc into a single "doc(gsd-2-uplift): full uplift initiative arc, extracted to dedicated repo" commit. Recommend (c) for a PR review-ability trade-off; (a) for "git as ledger" purism.

3. **Spike-008 is intentionally superseded** but not abandoned. Commit `bfe73a1 docs(spikes): close methodology audit cycle (007 override + 008 supersession)`. Anyone reviewing the merge will see only 3 files / 439 lines for 008 and may assume incomplete work. Verify supersession rationale is in 008's directory README or the spike `ROADMAP.md` before merge.

4. **Mid-flight WIP checkpoints.** 10 `wip:` commits exist as pause-point markers (e.g., `02615f6 wip: spike-001 paused at Phase A1 complete, A2+ pending`). They were superseded by completion commits. Not load-bearing; squash candidates.

5. **No conflicts expected.** Local main has not advanced since 2026-03-15 (branch base). The branch's only base-vs-tip divergence is additive — `git diff main..HEAD --shortstat` shows 658 deletions across 447 files, all attributable to (a) governance edits to STATE/PROJECT/REQUIREMENTS/ROADMAP files that already exist on main and (b) gsd-2-uplift extraction-time pointer-stub rewrites. **No merge conflicts on rebase to local main are expected.** (Origin/main is a separate problem — see #1.)

6. **CLAUDE.md authority gap.** Project CLAUDE.md (added on this branch in `ee1716d` 2026-04-29 with subsequent edits) cites ADRs 0001-0005, the foundation audit, ECOSYSTEM-COMMENTARY, LONG-ARC, VISION, METHODOLOGY etc. — **none of which are on local main**. If this branch is split and only spike artifacts land first, CLAUDE.md without its referenced docs is half-broken. Foundation/governance docs and CLAUDE.md should land in the same merge unit.

7. **No source-code deletions.** No `src/`, `tests/`, `alembic/`, `pyproject.toml`, or other production-code paths are touched. The branch is entirely `.planning/` + `docs/` + root governance files. Safe to merge from a "won't break v0.1 software" perspective.

---

## Volume / Cleanliness Audit

Total: **+187,549 / -658 lines** across 447 files.

| Category | Lines | % |
|---|---|---|
| **JSON / CSV / JSONL data files** | 114,359 | **61%** |
| Markdown (docs, audits, deliberations, FINDINGS, etc.) | 43,500 | 23% |
| Python (spike experiments, harnesses) | 29,657 | 16% |
| Other (.gitignore etc.) | 33 | 0% |

### Where the data volume lives

The 5 largest files alone account for ~70,000 lines (37% of total branch volume), all spike experiment artifacts:

- `005-evaluation-framework-robustness/experiments/checkpoints/phase1_quantitative.json` — 27,801 lines
- `006-model-retrieval-interactions/experiments/checkpoints/phase1_quantitative.json` — 19,223 lines
- `004-embedding-model-evaluation/experiments/checkpoints/pre_spike_analyses.json` — 11,668 lines
- `003-strategy-profiling/experiments/data/w3_4_pipeline_profiles.json` — 5,364 lines
- `004-embedding-model-evaluation/experiments/checkpoints/phase2_metrics.json` — 4,987 lines

### Cleanliness findings

- **No venv / cache / node_modules / `.env` pollution.** `.gitignore` is properly configured and respected.
- **No source-code generated artifacts.** All committed Python files are spike harnesses (intentional research code), not generated.
- **Spike experiment-result JSONs:** these are reproducibility artifacts and arguably *should* be in version control for a research project that values "traces over erasure" (per project memory feedback on methodology). However, the 27k-line single-file checkpoints are a smell. Consider for v0.3+: split checkpoints by phase, store under `.planning/spikes/<id>/experiments/data/` with consistent naming, or move very large reproducibility artifacts to `/data/` with a manifest pointer in-repo. **No action required for this merge** — but worth a follow-up todo.
- **No accidentally committed secrets** detected by name (no `.env`, no `credentials*`, no `*.pem`, no `*.key`).

---

## PR Strategy Recommendation

**Recommended: hybrid — single PR with optional pre-PR squash of the gsd-2-uplift arc.**

### Why not split

The user's pattern is bundled PRs for coherent areas. The temptation here is to split by workstream (5+ PRs), but:

- Workstream #1 (foundation docs/ADRs), #7 (v0.1 freeze + v0.2 pivot), #8 (v0.2 audits + ADR-0005 + governance), and #11 (handoffs) are mutually entangled — STATE.md/PROJECT.md/ROADMAP.md edits in #7 cite ADRs from #8, governance docs from #8 cite foundation audit from #1, CLAUDE.md from #8 cites ADRs from #1 and #8. Splitting these creates broken-reference half-merges.
- Spikes 001-008 (#2-#6) are sequenced and cite each other. Spike-002 references spike-001's volume model; spike-003 builds on spike-002's backend choice; spikes 005-008 are the "next-round suite" derived from 001-004's findings. Splitting per-spike creates multiple PRs that all want to land in order with no parallelism gain.
- All workstreams touch only `.planning/` and `docs/`. There's no "high-risk infrastructure change" that needs to be isolated for code review.
- This is a solo research repo with no external review queue. Splitting buys nothing operational — there's no second reviewer's bandwidth being economized.

### Why not single bundle as-is

The 42 gsd-2-uplift commits are the structural noise. They make the PR look unreviewable (~223 commits) when the substantive content is more like 180 commits' worth of work + an extracted initiative trail. Reviewers (including future-Logan) will spend cognitive energy parsing "why are there 38 docs(gsd-2-uplift) commits whose content isn't in the diff?"

### Recommended sequence

1. **Resolve `origin/main` divergence first** (Risk #1). Whatever that requires — force-push local main, file a fix-up commit on origin/main, or rebase origin/main into local main. **Without this, no merge to origin is safe.**
2. **Optional pre-PR cleanup** (Risk #2): interactive-rebase the 42 gsd-2-uplift commits into one "docs(gsd-2-uplift): full initiative arc — extracted to dedicated repo" squash commit. Preserves the ledger of "this happened" without the per-step noise. Skip if you prefer history-as-written.
3. **Squash the 10 `wip:` commits** into their successor completion commits (Risk #4). Each `wip:` is a pause-point that was superseded.
4. **Single PR `spike/001-volume-filtering` → `main`.** Title: `docs(.planning): seven spikes (001-008), v0.1→v0.2 pivot, ADR-0001..0005, governance corpus, foundation audit, extracted gsd-2-uplift trail`. Body: link to this post-mortem.
5. **Tag the merge commit.** Recommend `v0.2-planning-complete` or similar — captures "all design work for v0.2 is on main, implementation begins with Phase 12 plan-1."
6. **Delete branch immediately on merge.** Don't keep "spike/001-volume-filtering" around.

### Trade-off being accepted

The hybrid approach optimizes for: (a) preserving causal-narrative integrity of how v0.2 was decided; (b) fitting the user's bundled-PR preference; (c) treating this as a one-time "branch-debt-payoff" merge rather than a sustainable workflow.

It does **not** optimize for: per-workstream review independence (impossible given entanglement), bisect-friendly history (gsd-2-uplift squash sacrifices commit-level bisect into that arc — but the arc's content was extracted anyway, so bisecting it is unlikely to help).

The deeper trade-off the user is paying: **branch hygiene was already breached weeks ago.** No PR strategy recovers the ability to have caught this earlier. The recommendation here is the cheapest exit. The forward-looking discipline question — "how do we not accumulate another 7-week branch?" — is separate, and probably belongs in a deliberation, not this post-mortem.

---

## Open Questions for Logan

1. **`origin/main` — what happened?** `origin/main` last advanced 2026-04-20 with `692a607 chore(pyproject): rename PyPI distribution to arxiv-sanity-mcp (#1)`, but the entire tree is nested under `workspace/projects/arxiv-sanity-mcp/`. This looks like a misclone or a malformed PR-merge that put the whole filesystem path inside the repo. Was this a known issue? Is there a backup of the "real" pre-flatpath origin/main somewhere? **Cannot publish this branch to origin without first resolving this.**

2. **gsd-2-uplift commit-arc disposition.** Three options listed in Risk #2: keep all 42, squash to one, or filter-branch them out entirely. Your call — I lean toward squash-to-one for review hygiene, but you may value the per-step ledger.

3. **`v0.1.0` tag was on origin's old layout.** `v0.1.0 → 31abb5a` is an ancestor of origin/main but **not** of local main (`git merge-base --is-ancestor v0.1.0 main` returns NO). When origin/main is fixed, will the v0.1.0 tag need to be re-anchored, or does it need to stay where it is for PyPI release tooling? Cannot determine from git alone.

4. **Squash `wip:` commits or keep?** Risk #4 — minor. They're pause-point markers superseded by completion commits. Squash recommended but not load-bearing.

5. **Spike-008 supersession — visible enough?** Commit `bfe73a1` documents that 008 was intentionally superseded, but the spike's directory has only 3 files. A reader of the merged history may not connect the two. Worth a one-line README in `008-function-in-use-and-blind-spots/` if not already present? Not checked.

6. **Foundation audit closure.** `.planning/foundation-audit/` exists on this branch with FINDINGS.md and METHODOLOGY.md. The closeout matrix from `ee06cc1` references "pending validations" — are any of these blocking the merge, or are they all post-merge follow-ups?

7. **Future branch policy for this repo.** Out of scope for this post-mortem, but flagged: this branch breached your global CLAUDE.md branch-hygiene rule by ~5.5 weeks. The pattern (spike branch absorbs unrelated planning work) will recur unless the rule is operationalized — e.g., add a session-start hook that checks branch age or a `branch-audit` invocation as a recurring loop. Worth a deliberation.

---

## Cited Evidence

Commit hashes and key paths used in this audit:

- Branch base: `4501420` (2026-03-15) — local main tip
- gsd-2-uplift extraction: `753f67a` (2026-05-08), log at `.planning/extraction/EXTRACTION-LOG.md`
- Spike-001 pause-point: `02615f6` (2026-03-17, .continue-here.md)
- Spike-001 completion (round 3): `c6c08d3` `2b48b35` `4450d6a` (2026-03-19)
- Spike-002 completion: `07fec3e` (2026-03-18)
- Spike-003 closure with qualifications: `9c5c5f9` `465c628` (2026-03-20, 2026-03-26)
- Spike-004 completion: `982295e` (2026-03-27); methodological correction `b7c1cff` (2026-03-29)
- v0.1 freeze: `665c972` (2026-04-16, "mark v0.1 complete and freeze milestone")
- ADR-0005 commit: `3f8e46f` (2026-04-25)
- v0.2 paired audit synthesis: `ca7e568`, `931bca1` (2026-04-26)
- Governance read-order map: `c31e21a` (2026-04-26)
- Doctrine load-points: `f1e2699` (2026-04-27)
- 007 override + 008 supersession: `bfe73a1` (2026-04-25)

`origin/main` HEAD: `692a607` (2026-04-20, broken nested layout)
`v0.1.0` tag → `31abb5a` (2026-03-13, ancestor of origin/main only, not local main)

---

*Generated 2026-05-08 as a working artifact for merge decision-making. Not a polished report — provenance is the audit-trail above.*
