# Autonomous-loop spec — arxiv-sanity-mcp v0.2

**Status: DRAFT for Logan's review (2026-05-29/30). Merge-autonomy DECIDED 2026-05-30 — the loop auto-merges (§2a), no human merge stop. The rest runs only after the §7 rollout preconditions.**
Companion: [HARNESS.md](./HARNESS.md). Grounds: `.planning/ROADMAP.md` (Phase 12–17), `docs/adrs/ADR-0005`, the operating contract, and the field lessons in §6.

This is the contract for a **bounded, checkpointed** autonomous run — *not* "iterate through all phases blindly." It encodes which phases an agent may drive to done, where it must **halt and surface to a human**, and how the per-plan loop terminates without looping forever or rubber-stamping "done."

## 1. Phase taxonomy — what may be driven autonomously

| Phase | Nature | Disposition |
|---|---|---|
| **12** Lens Abstraction Primitives | Refactor; gate = *all v0.1 tests pass unmodified* | **Auto-eligible, but first run SUPERVISED** (it's the load-bearing core; the "don't rewrite the v0.1 ranking core" STOP-rule lives here) |
| **13** MCP Surface Lens-Awareness | Implementation (dep: 12) | **Auto-eligible** |
| **14** Citation Graph Data Integration | 14-01 = **OpenAlex coverage spike + pre-registered decision matrix**; 14-02/03 = schema + backfill | 14-02/03 **auto-eligible**; **14-01 outcome = HARD HALT** |
| **15** Citation/Community Lens | Implementation + 15-3 extensibility *walkthrough* checkpoint | **Auto-eligible**, halt at 15-3 checkpoint for sign-off |
| **16** Lens-Disagreement/Intersection | Implementation + 16-1 *no-fusion-as-default* checkpoint | **Auto-eligible**, halt at 16-1 checkpoint |
| **17** Longitudinal Pilot Harness | 17-01 build harness; 17-02 **run 4+ week human pilot with Logan** | 17-01 **auto-eligible**; **17-02 = HARD HALT (cannot be auto-run)** |

**Critical path:** `(12 ∥ 14-data) → 15; 12 → 13; (13 ∧ 15) → 16 → 17`.

### The two hard gates (non-negotiable)
- **Phase 14-01 decision matrix.** Thresholds K (median cited-by edges/paper) and X (missingness on AI/CS post-2023) are fixed in `14-01-PLAN.md` *before* the spike runs. Outcomes: **A** sufficient → proceed; **B** intermediate → proceed + flag Semantic-Scholar-likely-in-v0.3; **C** insufficient → **re-deliberate** (pull Semantic Scholar into v0.2 / defer citation lens to v0.3 / ship thin direct-citation lens). The agent **runs the spike + populates the matrix + STOPS**. It must NOT pick the outcome — the matrix exists *precisely* to stop post-hoc sunk-cost rationalization, and a Stop-hook contract pressuring "Phase 14 done" would induce exactly that goal-gaming (see §6, the field report's "I had to bend on what counted as the same dataset").
- **Phase 17-02 pilot.** A 4+ week single-user (Logan) data-collection with weekly/mid/end reviews. The agent builds 17-01 and **stops at kickoff**. Auto-"completing" 17-02 = fabricating pilot data = hard integrity line.

## 2. The per-plan loop

For each eligible plan `NN-PP`:

```
1. ENTER   read PLAN.md + doctrine load-points (CLAUDE.md routes by trigger)
2. LIVE    run the suite first (test-live-before-audit, §6); record the real baseline
3. WORKTREE  isolate parallel plans in a git worktree (never the shared tree)
4. EXECUTE   implement against the plan's deliverables; commit per unit (small blast radius)
5. VERIFY    gate = mechanical deliverables hold (tests pass unmodified, registrations present,
             0 regressions). Judgment items → produce evidence, do NOT self-certify.
6. PR        open a PR (per plan/phase). Self-review with pr-reviewer; let CR/Codex review.
7. TRIAGE    pr-review-triage loop until termination (§3); record verdicts.
8. MERGE     gate = contract verified + suite green (run it, don't trust CI) + 0 unresolved
             agent-reviewer comments + retry ceiling not hit + NOT a gated-phase PR → AUTO-MERGE
             (squash, --delete-branch; §2a). Else → halt_for_human with evidence. Decision/
             checkpoint halts (§1) still stop the loop — they are not merge gates.
```

Between plans the agent updates STATE/handoff (durable state to files, not chat), then advances per the critical path — **pausing at every HARD HALT and checkpoint** (merge itself is no longer a pause — see §2a).

## 2a. PR mechanics & merge autonomy

**Merge is automatic, not human-gated** (Logan's decision, 2026-05-30: "I don't want us stopping for human merge"). When a plan PR satisfies all of:
1. completion-contract deliverables verified (mechanical),
2. the suite was run *this round* and is green — test-live. GitHub enforces **no** required status checks on this repo, so "green" means *locally-run `pytest` exit 0 + whatever CI exists*, never "CI is probably fine,"
3. **0 unresolved comments from the agent PR-reviewers** (CodeRabbit / Codex / Claude-review) — each such thread either code-fixed or carrying a resolving verdict block. This is the operative merge condition: the loop gates on the *automated reviewers*, since they are the only commenters in an unattended run. (A *human* comment left mid-run is also an unresolved thread that `required_conversation_resolution` will block on — desirable: it naturally pauses auto-merge until the loop addresses the human note. The loop never resolves a human thread by fiat; it answers it or `halt_for_human`.)
4. retry ceiling (§3) not exceeded,
5. the PR is **not** a gated-phase artifact (§1 hard halts / checkpoints / Phase-12-first-run),

then the loop **merges it itself**: `gh pr merge <n> --squash --delete-branch`, updates main locally, and advances. No stop for a human. If any condition fails and can't be made to pass within the retry ceiling → `halt_for_human` with evidence (never a silent skip, never a forced merge).

**Branch-protection mechanics (live on this repo — encode, don't rediscover):**
- `required_linear_history` ⇒ **squash-only** (a merge commit is rejected; proven on PR #3). Always `--squash`.
- `required_conversation_resolution` ⇒ **every thread resolved before merge.** A *resolved* thread satisfies this — resolution can be a code fix **or** a verdict-disposition (DEFERRED / REJECTED_*). Resolve-then-merge in one pass: push fixes → post verdict blocks → `resolveReviewThread` each thread → re-confirm 0 unresolved → merge. (PR #3 hit this live: a late push re-opened review and added threads; the merge blocked until they were resolved.)
- `enforce_admins:false`, `required_approving_review_count:0`, no required status checks ⇒ GitHub will not itself block a green-thread merge — which is *precisely why* the suite-green gate (cond. 2) is the loop's responsibility, not CI's.

**PR granularity & stacking:**
- **One PR per plan** (`NN-PP`) — small blast radius, one contract, one triage loop.
- **Dependencies stack:** Phase 13 depends on 12. Prefer (a) merge 12's PR first, then branch 13 off updated main (linear, simplest); fall back to (b) basing 13's branch on 12's branch (stacked PR) only when they must develop in parallel — keep 12 merged before 13's merge so no history-rewrite is needed. Parallel *independent* plans use worktree isolation (§2 step 3).

**What auto-merge does NOT cover** (these were never merge gates — lifting the merge stop doesn't touch them): the §1 hard halts (14-01 outcome, 17-02 pilot), the 15-3 / 16-1 checkpoints, **Phase 12's first supervised run** (execution oversight of the don't-rewrite-the-core trap — a human-eyes-on-execution gate, not a merge approval), and every §5 standing gate other than merge-to-main (tag / version bump / publish / release / v0.3 / cross-repo / mutating `~/.gsd`·`~/.claude`·`~/.codex`).

## 3. PR-triage termination rule (the "until just nitpicks" problem)

Each push re-triggers the bot reviewers, so the triage sub-loop needs a defined stop (demonstrated live on PR #3: it took 2 rounds to converge):

- **Fix:** any `P0/P1` (CR Critical/Major; Codex P0/P1) **and** any correctness/resolution finding of an *already-seen class* (e.g. dead doc-ref) — repo-scoped, not file-scoped.
- **Disposition without code change:** `P2`-and-below cosmetic / wrong-locus → resolve with a `DEFERRED`/`REJECTED_*` verdict block (a *resolved* thread satisfies `required_conversation_resolution`; resolution ≠ code fix).
- **Retry ceiling:** **max 2 review rounds per finding-category.** After that, remaining same-category items are resolve-acknowledged, not chased. (The field report's #1 operational fix — avoids the Stop-hook re-fire spiral.)
- **Stop condition:** a review round yields only `P2`-or-lower of already-categorized classes → triage loop terminates → proceed to the §2a merge gate (auto, no human stop).

Every disposition is a `review-verdict` block (pr-review-journal); the verdict buckets are the honest-failure taxonomy.

## 4. Completion contract (per plan) — template

Modeled on the `/goal` Stop-hook contract, with **gated outcomes as halts, never success conditions**:

```jsonc
{
  "unit": "12-01",
  "deliverables": [            // VERIFIABLE — the Stop hook checks these mechanically
    {"id": "tests-green", "check": "uv run pytest -> exit 0, 0 failures", "required": true},
    {"id": "v0.1-unmodified", "check": "no edits to existing v0.1 test files", "required": true},
    {"id": "lens-protocol", "check": "Lens protocol + scorer registry exist; semantic lens registered"}
  ],
  "honest_failure_buckets": ["done", "blocked_external", "halt_for_human", "deferred_with_seam"],
  "hard_constraints": [
    "do NOT rewrite the v0.1 ranking core (ADR-0001 coexistence: generalize, don't replace)",
    "fusion is never the default",
    "merge only via squash on green+resolved+contract-verified (auto, per §2a) — never a merge commit, never on red"
  ],
  "halt_conditions": [         // STOP + surface; NOT failure, NOT success
    "phase-14-01 decision-matrix outcome (any of A/B/C)",
    "phase-15-3 / 16-1 checkpoint",
    "phase-17-02 pilot kickoff",
    "any irreversible/outward-facing action EXCEPT auto-merge (tag, publish, release, v0.3, cross-repo)"
  ],
  "retry_ceiling": 2
}
```

The contract must be **concrete enough to verify** (so "done" can't be faked) **and loose enough to accept honest failure** (so it doesn't loop forever or force goal-gaming). "halt_for_human" and "deferred_with_seam" are **first-class outcomes**.

## 5. Standing human gates (always, even mid-run)

`git tag` / version bump / publish / GitHub release · starting v0.3 / a new milestone · enabling full-access or mutating `~/.gsd`/`~/.claude`/`~/.codex` · crossing a project boundary (gsd-2-uplift etc.) · any destructive git (now also blocked by the deny hook) · Phase 14-01 outcome · Phase 17-02 pilot · Phase 12 first-run execution (supervised).

**Merge-to-main is NO LONGER a standing gate** (Logan, 2026-05-30) — the loop auto-merges plan PRs under the §2a conditions. The gates above are decision / data-integrity / outward-facing actions, none of which is "merge a passing in-repo plan PR." Removing the merge stop does not widen any of them.

## 6. Field lessons applied (from a 9-hour /goal run + this session)

Held as **directional field experience, n=1, different domain** — adopted where it converges with our doctrine, flagged where it's a trap for us.

- **Iterative > exhaustive auditing.** Three short audits each reading the prior's failures beat one long audit (29→64→79→100% there; 2-round triage convergence here). → the per-plan loop and triage rounds are iterative by design.
- **Test-live-before-audit.** A cheap check (HTTP 200 / a filename I hand-listed) misses ~30%; the real test is run-it-and-parse / extract-and-resolve. → step 2 of the loop; and the doc-ref bug this session was the same failure (verify by extraction, not proxy).
- **Honest-failure taxonomy is first-class.** `fix | ack_stale | abandon` (theirs) ≈ our verdict buckets and the 14-01 A/B/C. An adapter that fails for license reasons is `ack_stale`, never a stubbed "success." → §3, §4.
- **Subagents that say "no."** A refusal-with-evidence saved a downstream timeout. → DEFERRED-with-seam is a real outcome.
- **Ledger as source of truth, "no trust-me-bro."** Live state on disk, not chat. → `.planning/` artifacts + the pr-review-journal JSON + §9-bis harness-facts.
- **TRAP — over-strict contract → goal-gaming.** Their hook lacked an `external_blocker` bucket; it bounced 4× and the author *bent the definition of "same dataset"* to satisfy it. For us that failure aimed at **Phase 14's matrix** (rationalizing Outcome A) or **17's pilot** (faking data) is severe. → gated outcomes are HALTS, never success conditions (§1, §4).
- **Retry ceiling.** Cap retries per finding-category to stop the re-fire spiral. → §3.
- **Worktree isolation.** Their parallel run interleaved 4 stray commits. → step 3.
- **Smaller goals.** One 4000-char goal chaining 5 passes < two scoped goals with a checkpoint. → per-plan contracts, not a milestone-sized one.
- **Mechanism, not the Codex `/goal`.** Reproduce the Stop-hook completion contract natively (Claude Code `Stop` hook + `/loop`), not the Codex `/goal` loop (permission layer unenforceable from Claude Code; no `/goal` installed here anyway).

## 7. Recommended rollout

1. **Harness** (done: deny hook live + tested; Stop-contract built, not enabled). **Precondition before the unattended loop:** refine the deny hook to *command-position* matching. With auto-merge (§2a) + autonomous triage, commit messages / PR bodies / verdict blocks routinely contain literal banned strings (they *describe* resets, removals, force-pushes); the current substring matcher would false-positive-block the loop's own commits constantly. Attended single actions are fine today; the self-merging loop is not until this lands.
2. **Phase 12 plan-1 SUPERVISED** — proves plan→execute→verify→PR→triage→contract→**auto-merge** end-to-end on the load-bearing refactor, with eyes on the don't-rewrite-the-core trap. (Supervised = human watches *execution*; the merge still goes through the §2a auto path so the merge mechanics are validated too.)
3. **Enable the bounded autonomous loop** for 13 → 15 → 16 + 14-data/17-01, with 14-01 and 17-02 as hard halts, per-plan contracts, retry ceilings, worktree isolation, and §2a auto-merge — only after (1) the hook fix lands and (2) validates the loop.
