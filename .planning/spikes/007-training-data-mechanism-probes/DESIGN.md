---
question: "For the model families that remain live after framework and retrieval checks, are their differences predictable from training-data and community-structure hypotheses rather than from ad hoc narratives?"
type: mechanistic + comparative
status: complete
round: 1
depends_on:
  - 005 (evaluation framework robustness)
  - 006 (model-retrieval interactions)
  - H2 from HYPOTHESES-005.md
linked_references:
  - ../HYPOTHESES-005.md
  - ../SPIKE-DESIGN-PRINCIPLES.md
  - ../METHODOLOGY.md
---

# Spike 007: Training-Data Mechanism Probes

## Question

For the candidate model families that survive Spikes 005 and 006, can we support or weaken the proposed mechanism stories about what they encode, using tests tied to citation structure, vocabulary overlap, and profile specialization?

## Why This Spike Now

Spike 004 produced AI narratives about "signal axes," but the pre-spike analyses and post-spike critique both reject treating those narratives as validated model properties. Before paying the cost of task-based evaluation, this spike tests whether the remaining differences have any mechanistic support at all.

## Hypotheses Addressed

- **Primary:** `H2`
- **Secondary:** candidate selection for `H1` and `H5`

## Prior Credence And Update Target

- `[chosen for now]` Prior `P(H2) = 0.60`

This spike should shift that prior upward only if the shortlisted model families show the mechanism-patterns predicted for them across multiple sub-tests. It should shift the prior downward if the mechanism stories collapse into narrative residue, contradict one another, or depend on missing citation/community data.

## Chosen For Now

1. This spike runs on **shortlisted model families only**.
   The shortlist is created by 005 and 006. If those spikes fail to produce a meaningful shortlist, 007 should pause rather than expand back to the entire model set by default.

2. Mechanism probes focus on **independently testable steps**, not on full narrative packages:
   - citation/community overlap probes
   - vocabulary-overlap and adjacent-field false-positive probes
   - profile-specialization sensitivity probes

3. This spike is allowed to conclude that a narrative remains unvalidated.
   That is a legitimate result.

4. This spike requires an explicit data-readiness gate before any citation/community claim is tested.
   `[chosen for now]` A citation/community probe is runnable only if at least `70%` of the selected probe papers have the required citation/community metadata. If not, that sub-probe is `blocked`, not replaced by a looser story.

## Experimental Shape

### Phase 1: Candidate and probe selection

- Pick the surviving model families from 005/006
- Choose the most discriminating profiles from the pre-spike analysis as probe sites, with `P3`, `P5`, `P7`, and `P8` as the leading candidates
- Register the exact mechanism claims that each shortlisted family is carrying into this spike

### Phase 2: Data-readiness gate

- Verify citation/community metadata coverage for the candidate probe sets.
- Verify that each shortlisted family has at least one concrete mechanism claim that 007 can actually test.
- If 006 still leaves more than four live families or no concrete mechanism claims, stop and write a narrowing memo instead of executing the probe wave.

### Phase 3: Mechanism-specific probes

- Test citation/community claims where citation data exists
- Test vocabulary-overlap claims by checking adjacent-field false positives
- Test whether divergence concentrates in the profiles the mechanism predicts

### Phase 4: Mandatory qualitative review

- Review representative supporting and contradictory cases for each mechanism claim.
- Inspect whether the probe outputs correspond to recognizable paper-level relations or whether they only look coherent at the metric level.
- If a mechanism claim appears supported quantitatively but the reviewed cases look ad hoc, carry that disagreement forward explicitly.

### Phase 5: Mechanism synthesis and 008 handoff

- For each candidate mechanism, separate:
  - supported steps
  - unsupported steps
  - contradictory evidence
- Produce an 008 handoff that names:
  - which candidate configurations remain live,
  - which mechanism stories are strengthened enough to motivate function-in-use testing,
  - and which candidates remain live only as unresolved functional comparisons rather than mechanism-backed ones.
- If more than two challengers remain live, rank them and select the top two for `008` using this order:
  1. strongest evidence of complementarity against the incumbent from `006`
  2. strongest surviving mechanism support from this spike
  3. if still tied, greater structural distinctness from the incumbent
- Record any excluded live candidate in `HANDOFF.md` as deferred, not dropped.

## Success Criteria

1. Every retained mechanism claim is decomposed into concrete sub-tests.
2. Citation/community probes are either run against adequate metadata coverage or explicitly marked `blocked`.
3. The spike includes a mandatory qualitative review over representative supporting and contradictory cases.
4. The output distinguishes supported mechanistic evidence from narrative residue.
5. The spike narrows the challenger set for `008` to at most two or explicitly reports that mechanism probes failed to discriminate among them.

## Required Durable Outputs

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `FINDINGS.md`
- `DECISION.md`

Execution should follow [ITERATIVE-SPIKE-WORKFLOW.md](../ITERATIVE-SPIKE-WORKFLOW.md).

## Guardrails

- Do not infer mechanism from recommendation outputs alone.
- If citation coverage is too weak for a probe, mark the probe blocked rather than replacing it with a looser story.
- Do not let this spike become a hidden architecture recommendation; its job is explanation-strengthening or explanation-weakening.
