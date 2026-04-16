---
status: complete
date: 2026-04-16
source_checkpoint: ./experiments/checkpoints/phase2_mechanism_probes.json
qualitative_review: ./QUALITATIVE-REVIEW.md
---

# Spike 007 Findings

## Question

For the four families carried from `006`, can the remaining differences be supported by mechanism probes rather than left as ad hoc narratives?

## Main Findings

1. `[artifact-reported]` The direct citation/community probe is blocked.
   - Graph/citation coverage is far below the `70%` gate, so the strongest direct test for the `SPECTER2` story could not run.

2. `[artifact-reported]` Even with that blocked branch, three families show strong target-profile concentration in the probe wave.
   - `SPECTER2`: `jaccard_gap_vs_non_targets = 0.2015`, `truly_unique_lift = 3.6667`
   - `Stella`: `0.1912`, `3.1667`
   - `Voyage`: `0.2230`, `3.5000`
   - `GTE`: weaker at `0.0863`, `1.1667`

3. `[derived]` The surviving mechanism stories are not equally credible.
   - `SPECTER2` has the clearest specialized-domain pattern but only partial direct mechanism support because the citation/community probe is blocked.
   - `Voyage` has the strongest broad-profile qualitative support, especially on `P2`.
   - `Stella` remains interesting, but the specific deployment/practicality story is still too proxy-dependent.
   - `GTE` remains coherent but conservative.

4. `[chosen for now]` The best `008` shortlist is:
   - `SPECTER2`
   - `Voyage`

## Per-Family Read

### `SPECTER2`

- `[artifact-reported]` Divergence concentrates on `P3` and `P8`.
- `[source-traceable]` The Spike 004 blind `P3` review remains the strongest qualitative support case; see [specter2_P3_blind_review.md](../004-embedding-model-evaluation/experiments/reviews/specter2_P3_blind_review.md).
- `[derived]` The story that survives is narrow: `SPECTER2` looks strongest on specialized technical domains, not as a universal alternative similarity notion.
- `[chosen for now]` Status: `carry forward`

### `Stella`

- `[artifact-reported]` Divergence concentrates on `P6` and `P7`, and 006 still gives it the strongest complementarity score among the shortlist.
- `[source-traceable]` But Spike 004 also called Stella the thinnest evidence case, and 006 marked it explicitly ambiguous; see [DECISION.md](../004-embedding-model-evaluation/DECISION.md) and [HANDOFF.md](../006-model-retrieval-interactions/HANDOFF.md).
- `[derived]` The family remains live as an unresolved practical-extension candidate, but the mechanism story is not strong enough to justify an `008` slot ahead of stronger-backed families.
- `[chosen for now]` Status: `defer`

### `GTE`

- `[artifact-reported]` `GTE` shows only moderate concentration and the weakest 006 complementarity score of the four remaining families.
- `[source-traceable]` Spike 004 already described it as the most conservative challenger; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[derived]` The mechanism story still reads as "coherent conservative widening" rather than a distinct relation type that urgently needs function-in-use testing.
- `[chosen for now]` Status: `defer`

### `Voyage`

- `[artifact-reported]` `Voyage` shows the strongest broad-profile concentration and the highest structural distinctness proxy in the shortlist (`0.5007`).
- `[source-traceable]` The Spike 004 blind `P2` review remains the strongest qualitative evidence in the whole model-comparison program; see [voyage_P2_blind_review.md](../004-embedding-model-evaluation/experiments/reviews/voyage_P2_blind_review.md).
- `[derived]` The bounded surviving story is: `Voyage` matters most on broad conceptual profiles where frontier / failure-mode papers are valuable.
- `[chosen for now]` Status: `carry forward`

## Shortlist For 008

### Carry Forward

1. `SPECTER2`
2. `Voyage`

### Deferred

1. `Stella`
2. `GTE`

### Already Dropped

1. `Qwen3`

## Bounded Conclusion

- `[chosen for now]` `H2` is moderately strengthened.
- `[chosen for now]` The strengthened claim is not that every challenger maps to a clean signal axis. It is that some remaining family-level differences do show patterned, profile-sensitive behavior that is strong enough to justify one more functional test.
- `[chosen for now]` The next practical question is now sharp: do `SPECTER2` and `Voyage` actually help researchers more than the incumbent when their blind-spot papers enter real tasks?
