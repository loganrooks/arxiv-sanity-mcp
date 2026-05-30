# Autonomous-loop spec — arxiv-sanity-mcp v0.2

**Status: DRAFT for Logan's review (2026-05-29/30). Nothing here runs until approved.**
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
8. GATE      STOP for human merge (merge is always human-gated). Halt at any decision/checkpoint.
```

Between plans the agent updates STATE/handoff (durable state to files, not chat), then advances per the critical path — **pausing at every HARD HALT and checkpoint.**

## 3. PR-triage termination rule (the "until just nitpicks" problem)

Each push re-triggers the bot reviewers, so the triage sub-loop needs a defined stop (demonstrated live on PR #3: it took 2 rounds to converge):

- **Fix:** any `P0/P1` (CR Critical/Major; Codex P0/P1) **and** any correctness/resolution finding of an *already-seen class* (e.g. dead doc-ref) — repo-scoped, not file-scoped.
- **Disposition without code change:** `P2`-and-below cosmetic / wrong-locus → resolve with a `DEFERRED`/`REJECTED_*` verdict block (a *resolved* thread satisfies `required_conversation_resolution`; resolution ≠ code fix).
- **Retry ceiling:** **max 2 review rounds per finding-category.** After that, remaining same-category items are resolve-acknowledged, not chased. (The field report's #1 operational fix — avoids the Stop-hook re-fire spiral.)
- **Stop condition:** a review round yields only `P2`-or-lower of already-categorized classes → STOP, hand to human for the merge gate.

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
    "no merge without human approval"
  ],
  "halt_conditions": [         // STOP + surface; NOT failure, NOT success
    "phase-14-01 decision-matrix outcome (any of A/B/C)",
    "phase-15-3 / 16-1 checkpoint",
    "phase-17-02 pilot kickoff",
    "any irreversible/outward-facing action (merge, tag, publish, v0.3, cross-repo)"
  ],
  "retry_ceiling": 2
}
```

The contract must be **concrete enough to verify** (so "done" can't be faked) **and loose enough to accept honest failure** (so it doesn't loop forever or force goal-gaming). "halt_for_human" and "deferred_with_seam" are **first-class outcomes**.

## 5. Standing human gates (always, even mid-run)

Merge to main · `git tag` / version bump / publish / GitHub release · starting v0.3 / a new milestone · enabling full-access or mutating `~/.gsd`/`~/.claude`/`~/.codex` · crossing a project boundary (gsd-2-uplift etc.) · any destructive git (now also blocked by the deny hook) · Phase 14-01 outcome · Phase 17-02 pilot.

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

1. **Harness** (done: deny hook live + tested; Stop-contract built, not enabled).
2. **Phase 12 plan-1 SUPERVISED** — proves plan→execute→verify→PR→triage→contract end-to-end on the load-bearing refactor, with eyes on the don't-rewrite-the-core trap.
3. **Enable the bounded autonomous loop** for 13 → 15 → 16 + 14-data/17-01, with 14-01 and 17-02 as hard halts, per-plan contracts, retry ceilings, worktree isolation — only after (2) validates the loop.
