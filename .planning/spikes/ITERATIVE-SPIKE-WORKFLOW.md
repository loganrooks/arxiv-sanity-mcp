# Iterative Spike Workflow

**Status:** Active repo-local execution contract for the `005`-`008` inter-milestone suite  
**Last updated:** 2026-04-16

## Purpose

This document defines the durable execution contract for the active spike program.

It exists to prevent the current suite from depending on:

- terminal-only critique,
- ad hoc file placement,
- or executor-specific interpretations of what each spike must produce before the next one can begin.

This is a **repo-local workflow layer**, not an upstream GSDR contract.

## Applies To

- [005-evaluation-framework-robustness](./005-evaluation-framework-robustness/DESIGN.md)
- [006-model-retrieval-interactions](./006-model-retrieval-interactions/DESIGN.md)
- [007-training-data-mechanism-probes](./007-training-data-mechanism-probes/DESIGN.md)
- [008-function-in-use-and-blind-spots](./008-function-in-use-and-blind-spots/DESIGN.md)

Historical spikes `001`-`004` remain valid as records, but this workflow is the canonical execution contract for the active next-round suite.

## Lifecycle

The default lifecycle for a suite spike is:

1. `DESIGN.md`
2. execution prep
3. raw experiment outputs under `experiments/`
4. `QUALITATIVE-REVIEW.md` when required
5. `POSTERIOR.md`
6. `HANDOFF.md` or closeout artifact
7. `FINDINGS.md`
8. `DECISION.md` if and only if the spike reaches a real decision rather than a deferral

The suite should prefer explicit deferral over premature closure.

## Artifact Layout

### Spike root

Durable spike-level artifacts live at the root of the spike directory, for example:

- `.planning/spikes/005-evaluation-framework-robustness/DESIGN.md`
- `.planning/spikes/005-evaluation-framework-robustness/QUALITATIVE-REVIEW.md`
- `.planning/spikes/005-evaluation-framework-robustness/POSTERIOR.md`
- `.planning/spikes/005-evaluation-framework-robustness/HANDOFF.md`

### `experiments/`

Use `experiments/` for:

- raw generated outputs,
- intermediate data,
- scripts,
- notebooks,
- review inputs,
- and other execution byproducts that support the durable synthesis artifacts.

### `reviews/`

Use `reviews/` for durable external or independent critique artifacts.

Examples:

- suite-level review: `.planning/spikes/reviews/YYYY-MM-DD-<name>.md`
- spike-specific review: `.planning/spikes/<spike>/reviews/YYYY-MM-DD-<name>.md`

## Required Durable Artifacts

### Always present at spike root

- `DESIGN.md`
- `FINDINGS.md`
- `DECISION.md`

`DECISION.md` may conclude with deferral or `[chosen for now]` rather than settlement.

### Required for active suite spikes

#### `POSTERIOR.md`

Required for `005`-`008`.

Purpose:

- carry prior to posterior movement explicitly,
- name the evidence that shifted the credence,
- and state the reversal conditions.

Minimum sections:

- question and linked hypothesis
- prior credence
- evidence summary
- posterior credence
- reversal conditions
- bounded conclusion

#### `HANDOFF.md`

Required for `005`-`007`.

Purpose:

- make the downstream obligations and branch conditions explicit,
- name what is carried forward, dropped, deferred, or still ambiguous.

Minimum sections:

- status of candidate configurations
- required downstream frame or shortlist
- blocked / ambiguous items
- downstream obligations
- trace-attunement note
- counter-reading

#### `QUALITATIVE-REVIEW.md`

Required whenever a spike design names qualitative review as a mandatory gate.

For the current suite, this means `005`-`008`.

Minimum sections:

- reviewed cases
- observed agreement and disagreement with the metrics
- bounded interpretation
- what the review cannot settle

#### `TASK-MATRIX.md`

Required for `008`.

Purpose:

- pre-register the task set and execution budgets before configuration runs begin.

Minimum sections:

- compared configurations
- selected profiles
- task instances
- prompt frame
- tool / turn / context budgets
- stopping condition
- output schema

#### `HUMAN-ADJUDICATION.md`

Required for `008`.

This file is required even if the spike ends as `pilot only / incomplete`.

Minimum sections:

- sampled outputs
- rubric
- adjudication outcomes
- disagreements with agent-side reading
- effect on posterior update or closeout status
- trace-attunement note
- counter-reading

## Required Sections For Higher-Level Reflexive Discipline

To keep the earlier deliberation work operative without turning every artifact into philosophy prose:

- `trace-attunement note` is required in:
  - `HANDOFF.md`
  - `HUMAN-ADJUDICATION.md`
  - suite-level review artifacts under `.planning/spikes/reviews/`

- `counter-reading` is required in:
  - `HANDOFF.md`
  - `HUMAN-ADJUDICATION.md`
  - suite-level review artifacts under `.planning/spikes/reviews/`

These fields are **not** required in raw experiment notes or data files.

## Current Spike Obligations

### Spike 005

Required outputs:

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `FINDINGS.md`
- `DECISION.md`

### Spike 006

Required outputs:

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `FINDINGS.md`
- `DECISION.md`

### Spike 007

Required outputs:

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `FINDINGS.md`
- `DECISION.md`

### Spike 008

Required outputs:

- `TASK-MATRIX.md`
- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HUMAN-ADJUDICATION.md`
- `FINDINGS.md`
- `DECISION.md`

## Template Source

Use the templates under [templates](./templates):

- [POSTERIOR.template.md](./templates/POSTERIOR.template.md)
- [HANDOFF.template.md](./templates/HANDOFF.template.md)
- [QUALITATIVE-REVIEW.template.md](./templates/QUALITATIVE-REVIEW.template.md)
- [TASK-MATRIX.template.md](./templates/TASK-MATRIX.template.md)
- [HUMAN-ADJUDICATION.template.md](./templates/HUMAN-ADJUDICATION.template.md)

## Non-Goals

- This workflow does not settle product questions by itself.
- This workflow does not replace `DESIGN.md`.
- This workflow does not require every spike to end in a new architecture commitment.
