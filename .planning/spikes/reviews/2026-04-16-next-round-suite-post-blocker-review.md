---
type: design-review
status: complete
date: 2026-04-16
reviewer: Codex (GPT-5)
target:
  - .planning/spikes/NEXT-ROUND-SUITE.md
  - .planning/spikes/HYPOTHESES-005.md
  - .planning/spikes/005-evaluation-framework-robustness/DESIGN.md
  - .planning/spikes/006-model-retrieval-interactions/DESIGN.md
  - .planning/spikes/007-training-data-mechanism-probes/DESIGN.md
  - .planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md
scope:
  - suite-level
  - post-blocker follow-up
  - execution-readiness check
verdict: revise-before-execution
linked_artifacts:
  - .planning/spikes/SPIKE-DESIGN-REVIEW-SPEC.md
  - .planning/spikes/SPIKE-DESIGN-PRINCIPLES.md
  - .planning/spikes/METHODOLOGY.md
  - docs/02-product-principles.md
  - docs/08-evaluation-and-experiments.md
  - docs/10-open-questions.md
---

# Next-Round Suite Post-Blocker Review

## Verdict

`revise-before-execution`

The earlier blocker themes appear structurally resolved:

- priors and probability-shift framing are now present
- qualitative review is mandatory in `005`-`008`
- handoff terms are more operationalized
- `008` no longer treats AI-only evaluation as enough to close `H1` / `H5`

What remains is narrower but still material. The suite is closer to execution-ready, but it still lacks a durable artifact contract for the new gates and a sufficiently concrete output-evaluation contract for `008`.

## Findings

### 1. Major: The suite now requires many gating outputs, but still has no durable artifact contract for them

**Why it matters**

The patched suite now requires:

- prior/posterior updates
- mandatory qualitative reviews
- `005 -> 006` handoff notes
- `006 -> 007/008` shortlist outputs
- `007` narrowing or failure-to-discriminate memo
- `008` task matrix and human-adjudication evidence

But none of those outputs yet has a required artifact path or canonical filename. That leaves execution, later reflection, and cross-review comparison vulnerable to ad hoc file placement and terminal-only loss.

This is now the main structural gap in the suite.

**File references**

- `.planning/spikes/NEXT-ROUND-SUITE.md`
- `.planning/spikes/005-evaluation-framework-robustness/DESIGN.md`
- `.planning/spikes/006-model-retrieval-interactions/DESIGN.md`
- `.planning/spikes/007-training-data-mechanism-probes/DESIGN.md`
- `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md`

**Minimal corrective direction**

Add a small program-level artifact contract before execution. At minimum, name required outputs and paths for:

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `TASK-MATRIX.md`
- `HUMAN-ADJUDICATION.md`

This can live in a short iterative-spike workflow note rather than in every spike doc separately.

### 2. Major: Spike 008 still lacks an operational rubric for “better research output” and a concrete human-adjudication sample plan

**Why it matters**

`008` now defines:

- task types
- control vs challenger structure
- `selected` vs `contributed`
- a pilot-only fallback if no human review is available

That is a real improvement. But the design still does not say:

- how final task outputs are judged as better / worse
- which outputs the human reviewer sees
- how many outputs are sampled
- what the human rubric is
- how evaluator disagreement changes the posterior update or suite conclusion

So the spike is better bounded, but still partly executor-defined at the exact point where it makes function-in-use claims.

**File references**

- `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md`
- `.planning/spikes/NEXT-ROUND-SUITE.md`
- `docs/08-evaluation-and-experiments.md`

**Minimal corrective direction**

Pre-register:

- an output-quality rubric
- a human-review sampling rule
- and a disagreement rule explaining how human vs agent disagreement affects `H1` / `H5` updates

### 3. Notable: Spike 005’s “category-derived” family is metadata-only at the representation level, but still seed-anchored at the interest-definition level

**Why it matters**

The new 005 design gives a much more concrete procedure for the category-derived profile family. That resolves the earlier underdefinition problem. But the procedure still derives the profile seed set using the existing profile label plus seed titles/abstracts.

That is acceptable if the claim is kept narrow. It means 005 tests embedding-model independence of the evaluation frame, not full independence from prior interest-definition choices.

Without that qualification, later synthesis could accidentally overstate what 005 established.

**File references**

- `.planning/spikes/005-evaluation-framework-robustness/DESIGN.md`

**Minimal corrective direction**

Add one explicit sentence in 005 or in the later findings template stating that the category-derived family is metadata-based but still seed-anchored.

### 4. Notable: The suite now has a narrowing contract, but the branch where 007 still leaves more than two live candidates for 008 remains implicit

**Why it matters**

`006` can carry forward up to four live model families or configurations. `007` must narrow further or say that it failed to discriminate. `008` then runs only the incumbent plus up to two challengers in one pass.

What is still not explicit is the middle case where `007` narrows the set, but not far enough to fit the `008` comparison budget.

This is not a fatal gap, but it is a real branch condition that should be named before execution.

**File references**

- `.planning/spikes/006-model-retrieval-interactions/DESIGN.md`
- `.planning/spikes/007-training-data-mechanism-probes/DESIGN.md`
- `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md`
- `.planning/spikes/NEXT-ROUND-SUITE.md`

**Minimal corrective direction**

Add one branch rule:

- either `007` must narrow to at most two challengers,
- or the suite must permit multiple `008` passes with an explicit tie-break or bracket rule.

## Open Assumptions

- This review treats the current target as **full-suite execution readiness**, not merely readiness to start `005`.
- This review treats the earlier blocker set as resolved unless execution later shows otherwise.

## Brief Strengths

- The earlier blocker findings were not merely caveated; they were mostly fixed structurally.
- `005`-`007` now have materially stronger evidence contracts than before the patch.
- `008` is much better bounded and no longer lets AI-only evaluation masquerade as a completed functional answer.
