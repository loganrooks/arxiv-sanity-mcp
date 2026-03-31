---
date: 2026-03-30
status: draft
scope: next spike suite design after Spike 004 critique and pre-spike analyses
depends_on:
  - ../HYPOTHESES-005.md
  - PRE-SPIKE-ANALYSES.md
  - ../SPIKE-DESIGN-PRINCIPLES.md
  - ../METHODOLOGY.md
---

# Spike Round 005 Suite Design

## Suite question

What is the shortest sequence of spikes that can turn the current representational findings into trustworthy, function-relevant guidance without prematurely revising the architecture?

## Why a suite, not a single spike

The pre-spike analyses show three distinct uncertainties that should not be collapsed into one protocol:

1. **Framework robustness**: do current model differences survive alternative profile construction and checked-in seed variation?
2. **Retrieval interaction**: do centroid vs kNN retrieval choices change which models or view-combinations look useful?
3. **Function-in-use**: do the surviving alternative views actually help complete research tasks or surface blind spots researchers would value?

Each uncertainty requires a different evaluator, a different success condition, and a different failure mode. Bundling them would recreate the same "the design names the problem but execution doesn't structurally address it" failure documented in Spike 004.

## Round structure

### Spike 005A

**Name:** Framework Robustness and Seed Dependence  
**Primary hypotheses:** `H4`, plus the seed-robustness prerequisite surfaced in `PRE-SPIKE-ANALYSES.md`  
**Why first:** If rankings change under profile construction changes, every downstream claim must be reported as framework-dependent.

### Spike 005B

**Name:** Retrieval Geometry and Complementarity  
**Primary hypotheses:** `H3`, with `H2` treated as a mechanistic interpretation layer rather than a standalone verdict  
**Why second:** It only becomes meaningful after 005A establishes which differences survive the evaluation frame.

### Spike 005C

**Name:** Task-Based Value of Blind Spots  
**Primary hypotheses:** `H1` and `H5`  
**Why third:** It is the most expensive spike and should only evaluate candidate views that survive the first two gates.

## Commitment levels

### Settled

- The next round should not attempt architecture closure.
- The next round should keep `MiniLM + TF-IDF` as the incumbent baseline throughout.
- The next round should require independent design critique before execution.

### Chosen for now

- The round will be executed as `005A → 005B → 005C`.
- `P1`, `P3`, `P6`, and `P7` are the main discriminating profiles.
- `P2`, `P4`, and `P8` will be used as controls where TF-IDF retains the strongest claim to secondary-view status.

### Hypothesis

- `Qwen3` and `Stella` may belong to the same downstream family for design purposes.
- `SPECTER2` may justify a distinct "scientific-community" evaluation lane.
- `Voyage` may remain useful as an orthogonal comparison even if it remains operationally disfavored.

### Open

- Whether fixed-K seed sensitivity must become part of 005A execution or can remain a bounded limitation.
- Whether 005C should include a human checkpoint if the user is available to provide judgments.

## Gating logic

### Gate after 005A

Proceed to 005B only if one of the following is true:

- at least one challenger remains meaningfully distinct under 3 profile constructions, or
- the result is that all challenger claims are framework-dependent and 005B is reframed as a profile-framework interaction spike.

### Gate after 005B

Proceed to 005C only if one of the following is true:

- at least one challenger-view configuration still shows profile-specific complementarity after retrieval variation, or
- the result is that `MiniLM + TF-IDF` remains dominant and 005C is narrowed to testing whether the apparent blind spots are functionally valuable anyway.

## What this suite is not

- It is not a race to crown a new default model.
- It is not a commitment to deploy new views.
- It is not a proof that representational differences matter to researchers.

It is a structured attempt to stop confusing those three things.
