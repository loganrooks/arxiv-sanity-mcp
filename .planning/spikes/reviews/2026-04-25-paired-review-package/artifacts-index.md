---
type: review-package-index
purpose: Paths to all artifacts the paired reviewers need, with reading-phase notes
---

# Artifacts Index

Paths are relative to project root: `~/workspace/projects/arxiv-sanity-mcp/`.

## For the cross-vendor reviewer

### Phase 1 — independent reading (read these only, in this order)

| # | Path | Why |
|---|---|---|
| 1 | `.planning/spikes/METHODOLOGY.md` | Working vocabulary; epistemic posture |
| 2 | `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md` | Explicit norms (winner-crowning, binary verdicts, etc.) |
| 3 | `.planning/spikes/NEXT-ROUND-SUITE.md` | Suite contract; narrowing rules; handoff contract |
| 4 | `.planning/spikes/HYPOTHESES-005.md` | Hypothesis priors carried through 005-008 |
| 5 | `.planning/spikes/005-evaluation-framework-robustness/HANDOFF.md` | First narrowing step |
| 6 | `.planning/spikes/006-model-retrieval-interactions/HANDOFF.md` | Retrieval-method narrowing |
| 7 | `.planning/spikes/007-training-data-mechanism-probes/HANDOFF.md` | Mechanism-backed narrowing; **Counter-Reading is load-bearing** |
| 8 | `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md` | The unrun spike whose narrowing premise is being tested |

### Phase 1 — optional skim if needed for context

- `.planning/spikes/005-evaluation-framework-robustness/{FINDINGS,POSTERIOR,DECISION,QUALITATIVE-REVIEW}.md`
- `.planning/spikes/006-model-retrieval-interactions/{FINDINGS,POSTERIOR,DECISION,QUALITATIVE-REVIEW}.md`
- `.planning/spikes/007-training-data-mechanism-probes/{FINDINGS,POSTERIOR,DECISION,QUALITATIVE-REVIEW}.md`

### Phase 1 — must NOT read

- `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` (read only in Phase 2)
- `.planning/deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md`
- `.planning/deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md`

### Phase 2 — read after Phase 1 output is written

- `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` — focus on Findings 1 and 2 in the *Cross-artifact synthesis* section.

## For the Opus adversarial reviewer

### Read

| # | Path | Why |
|---|---|---|
| 1 | `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` | Primary attack target |
| 2 | `.planning/spikes/005-evaluation-framework-robustness/HANDOFF.md` | Ground attack in textual evidence |
| 3 | `.planning/spikes/006-model-retrieval-interactions/HANDOFF.md` | Ground attack in textual evidence |
| 4 | `.planning/spikes/007-training-data-mechanism-probes/HANDOFF.md` | Ground attack in textual evidence; especially Counter-Reading |
| 5 | `.planning/spikes/NEXT-ROUND-SUITE.md` | Suite contract; check whether mechanism-support gate is pre-registered |
| 6 | `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md` | Verify configuration-vs-family read |
| 7 | `.planning/spikes/METHODOLOGY.md` | Check whether implicit-norm reads have textual support |
| 8 | `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md` | Same |

### May skim if needed

- `FINDINGS.md` / `POSTERIOR.md` / `DECISION.md` / `QUALITATIVE-REVIEW.md` from any 005/006/007 directory.

### May read for context

- `.planning/deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md` (the parent deliberation, with its addendum)
- `.planning/deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md` (the prior review of the deliberation)

The adversarial reviewer is allowed to see everything because its role is to attack the argument structure, not to perform an independent reading.

## Output paths (where reviewers should write their responses)

| Reviewer | Output file |
|---|---|
| Cross-vendor primary | `.planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md` |
| Opus adversarial | `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md` |

After both outputs land, the next step (handled outside this package) is a "Status after second-reader pass" addition to the original pressure pass at `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md`, recording which of Findings 1 and 2 survived, were qualified, or were retracted.
