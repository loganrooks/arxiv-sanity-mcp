# Spike Program Roadmap

**Status:** Active inter-milestone research program  
**Current role:** Determine the shape of the next implementation milestone  
**Last updated:** 2026-04-16

## Purpose

This spike program is no longer part of the shipped `v0.1` implementation roadmap.

It is the project's **between-milestones research surface**:

- spikes generate findings
- deliberations interpret those findings
- the next milestone will be derived from the resulting conclusions

The spike program is therefore not a hidden extension of `v0.1`. It is the inquiry program that will shape what comes next.

## Current Program State

There are two major research tracks represented in the repo:

1. **Deployment / filtering / backend architecture track**
   - Spikes `001`-`003`
   - Main question: how should the system be deployed, filtered, and architected at scale?
   - Status: historical input set for later milestone shaping

2. **Retrieval / recommendation comparison track**
   - Spike `004` and drafted suite `005`-`008`
   - Main question: do alternative retrieval and recommendation configurations reveal robust, meaningful, and functionally valuable differences beyond the current baseline?
   - Status: active program

## Current Decision Target

The active spike program is trying to reduce uncertainty around:

- what recommendation/retrieval views are actually distinct
- which differences are robust rather than artifacts of the current evaluation frame
- whether any surviving differences matter in use
- and what, if anything, should become committed product or architecture work in the next milestone

## Active Sequence

### Historical inputs

| Item | Role | Status |
|------|------|--------|
| [001-volume-filtering-scoring-landscape](./001-volume-filtering-scoring-landscape/DESIGN.md) | Deployment/filtering/scoring exploratory work | Historical |
| [002-backend-comparison](./002-backend-comparison/DESIGN.md) | Backend/search architecture comparison | Historical |
| [003-strategy-profiling](./003-strategy-profiling/DESIGN.md) | Broad strategy profiling and qualitative revision | Historical |
| [004-embedding-model-evaluation](./004-embedding-model-evaluation/DESIGN.md) | Embedding-model comparison under current frame | Complete |

### Active next-round suite

| Spike | Question | Status |
|------|----------|--------|
| [005-evaluation-framework-robustness](./005-evaluation-framework-robustness/DESIGN.md) | Do current findings survive alternative profile-construction frames? | Drafted, not yet executable |
| [006-model-retrieval-interactions](./006-model-retrieval-interactions/DESIGN.md) | Are observed differences model effects, retrieval-geometry effects, or both? | Drafted, not yet executable |
| [007-training-data-mechanism-probes](./007-training-data-mechanism-probes/DESIGN.md) | Can shortlisted differences be explained mechanistically? | Drafted, downstream of 005/006 |
| [008-function-in-use-and-blind-spots](./008-function-in-use-and-blind-spots/DESIGN.md) | Do surviving differences matter in actual research use? | Drafted, downstream of 005-007 |

Canonical suite wrapper:

- [NEXT-ROUND-SUITE.md](./NEXT-ROUND-SUITE.md)

## Current Gate

The next-round suite is **structurally ready to execute**.

The suite-level blocking issues from the earlier design reviews have been resolved in the current planning artifacts. The current gate is now operational rather than structural:

- execute `005` using the workflow and artifact contract below
- preserve the required handoff / posterior / qualitative review outputs during execution
- avoid collapsing back into terminal-only summaries or ad hoc artifact placement

Primary review artifact:

- [SPIKE-DESIGN-REVIEW-SPEC.md](./SPIKE-DESIGN-REVIEW-SPEC.md)
- [ITERATIVE-SPIKE-WORKFLOW.md](./ITERATIVE-SPIKE-WORKFLOW.md)
- [2026-04-16-next-round-suite-execution-readiness-review.md](./reviews/2026-04-16-next-round-suite-execution-readiness-review.md)

Current execution-readiness conclusion:

1. the artifact contract is now defined at the program level
2. the `007 -> 008` narrowing branch is now explicit
3. `008` has a lightweight but concrete human-adjudication gate

## Working Rules

1. **Spikes produce findings, not roadmap commitments.**
2. **Deliberations and milestone planning decide what gets built next.**
3. **The active suite should be read as shaping the next milestone, not extending `v0.1`.**
4. **Shared experiment code and review outputs should be treated as program-level assets, not ad hoc byproducts.**
5. **A stale spike roadmap is itself a planning risk. This file should track the actual active program, not just preserve historical sequences.**

## Key Supporting Artifacts

- [STRATEGY-SPACE.md](./STRATEGY-SPACE.md)
- [METHODOLOGY.md](./METHODOLOGY.md)
- [SPIKE-DESIGN-PRINCIPLES.md](./SPIKE-DESIGN-PRINCIPLES.md)
- [ITERATIVE-SPIKE-WORKFLOW.md](./ITERATIVE-SPIKE-WORKFLOW.md)
- [HYPOTHESES-005.md](./HYPOTHESES-005.md)
- [PRE-SPIKE-ANALYSES.md](./004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md)
- [comparative-characterization-and-nonadditive-evaluation-praxis.md](../deliberations/comparative-characterization-and-nonadditive-evaluation-praxis.md)
- [local-gap-propagation-and-signal-interpretation.md](../deliberations/local-gap-propagation-and-signal-interpretation.md)

## Immediate Next Steps

1. Treat `005` as complete. Its durable outputs are now available under [005-evaluation-framework-robustness](./005-evaluation-framework-robustness).
2. Treat `006` phase 1 quantitative setup as complete. Its checkpoint and review surface now exist under [006-model-retrieval-interactions/experiments](./006-model-retrieval-interactions/experiments).
3. Complete the mandatory `006` qualitative pass on the bounded interaction-case set from [phase1_interaction_cases.json](./006-model-retrieval-interactions/experiments/review_inputs/phase1_interaction_cases.json).
4. Produce `006`'s durable outputs and use `006/HANDOFF.md` to decide the shortlist carried into `007` and `008`.
5. Continue the suite through `007`-`008` under the same artifact contract.
6. Use the resulting findings, together with deliberations, to define the next milestone.
