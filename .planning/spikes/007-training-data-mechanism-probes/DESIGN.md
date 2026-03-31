---
question: "For the model families that remain live after framework and retrieval checks, are their differences predictable from training-data and community-structure hypotheses rather than from ad hoc narratives?"
type: mechanistic + comparative
status: drafted
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

## Chosen For Now

1. This spike runs on **shortlisted model families only**.
   The shortlist is created by 005 and 006. If those spikes fail to produce a meaningful shortlist, 007 should pause rather than expand back to the entire model set by default.

2. Mechanism probes focus on **independently testable steps**, not on full narrative packages:
   - citation/community overlap probes
   - vocabulary-overlap and adjacent-field false-positive probes
   - profile-specialization sensitivity probes

3. This spike is allowed to conclude that a narrative remains unvalidated.
   That is a legitimate result.

## Experimental Shape

### Phase 1: Candidate and profile selection

- Pick the surviving model families from 005/006
- Choose the most discriminating profiles from the pre-spike analysis as probe sites, with `P3`, `P5`, `P7`, and `P8` as the leading candidates

### Phase 2: Mechanism-specific probes

- Test citation/community claims where citation data exists
- Test vocabulary-overlap claims by checking adjacent-field false positives
- Test whether divergence concentrates in the profiles the mechanism predicts

### Phase 3: Mechanism synthesis

- For each candidate mechanism, separate:
  - supported steps
  - unsupported steps
  - contradictory evidence

## Success Criteria

1. Every retained mechanism claim is decomposed into concrete sub-tests.
2. The output distinguishes supported mechanistic evidence from narrative residue.
3. The spike narrows the candidate set or explicitly reports that mechanism probes failed to discriminate among them.

## Guardrails

- Do not infer mechanism from recommendation outputs alone.
- If citation coverage is too weak for a probe, mark the probe blocked rather than replacing it with a looser story.
- Do not let this spike become a hidden architecture recommendation; its job is explanation-strengthening or explanation-weakening.
