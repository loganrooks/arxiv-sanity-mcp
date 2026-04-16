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

The next-round suite is **not ready to execute yet**.

The current blocking condition is structural, not empirical:

- the independent design review found blocker-level issues
- those need to be resolved in the suite and per-spike designs before execution begins

Primary review artifact:

- [SPIKE-DESIGN-REVIEW-SPEC.md](./SPIKE-DESIGN-REVIEW-SPEC.md)

Primary review findings currently in force:

1. qualitative review must be structurally required
2. prior credences / probability-shift framing must be added
3. inter-spike handoff contracts must be made explicit
4. `008` needs a clearer task-harness and human-evaluation position

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
- [HYPOTHESES-005.md](./HYPOTHESES-005.md)
- [PRE-SPIKE-ANALYSES.md](./004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md)
- [comparative-characterization-and-nonadditive-evaluation-praxis.md](../deliberations/comparative-characterization-and-nonadditive-evaluation-praxis.md)
- [local-gap-propagation-and-signal-interpretation.md](../deliberations/local-gap-propagation-and-signal-interpretation.md)

## Immediate Next Steps

1. Patch the `005`-`008` suite to resolve the blocker review findings.
2. Decide and document the iterative spike-workflow contract for shared code reuse, review outputs, and execution gating.
3. Execute `005` only after the suite becomes structurally ready.
4. Use the resulting findings, together with deliberations, to define the next milestone.
