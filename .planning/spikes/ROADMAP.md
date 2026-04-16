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
   - Spike `004`, completed `005`, completed `006`, completed `007`, and drafted `008`
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
| [005-evaluation-framework-robustness](./005-evaluation-framework-robustness/DESIGN.md) | Do current findings survive alternative profile-construction frames? | Complete |
| [006-model-retrieval-interactions](./006-model-retrieval-interactions/DESIGN.md) | Are observed differences model effects, retrieval-geometry effects, or both? | Complete |
| [007-training-data-mechanism-probes](./007-training-data-mechanism-probes/DESIGN.md) | Can shortlisted differences be explained mechanistically? | Complete |
| [008-function-in-use-and-blind-spots](./008-function-in-use-and-blind-spots/DESIGN.md) | Do surviving differences matter in actual research use? | Drafted, downstream of completed 005-007 |

Canonical suite wrapper:

- [NEXT-ROUND-SUITE.md](./NEXT-ROUND-SUITE.md)

## Current Gate

The next-round suite is **mid-execution**.

Structural execution blockers were resolved earlier. The current gate is now the first functional pass:

- treat `005` and `006` as completed inquiry steps
- treat `007` as the completed narrowing step
- use `007/HANDOFF.md` to execute `008` on the named three-configuration comparison frame
- avoid reopening deferred families or the full configuration matrix without a new explicit reason

Primary review artifact:

- [SPIKE-DESIGN-REVIEW-SPEC.md](./SPIKE-DESIGN-REVIEW-SPEC.md)
- [ITERATIVE-SPIKE-WORKFLOW.md](./ITERATIVE-SPIKE-WORKFLOW.md)
- [2026-04-16-next-round-suite-execution-readiness-review.md](./reviews/2026-04-16-next-round-suite-execution-readiness-review.md)

Current execution-readiness conclusion:

1. the artifact contract is now defined at the program level
2. the `007 -> 008` narrowing branch is now exercised rather than merely specified
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

1. Treat `007` as complete. Its checkpoint, qualitative review, posterior, and handoff now exist under [007-training-data-mechanism-probes](./007-training-data-mechanism-probes).
2. Use [007/HANDOFF.md](./007-training-data-mechanism-probes/HANDOFF.md) to execute `008` on:
   - incumbent `MiniLM + TF-IDF`
   - `SPECTER2`
   - `Voyage`
3. If `Voyage` must be substituted for execution reasons, record that branch explicitly before task runs begin.
4. Continue the suite through `008` under the same artifact contract.
5. Use the resulting findings, together with deliberations, to define the next milestone.
