---
type: qualitative-review
status: complete
date: 2026-04-16
reviewer: codex
target: .planning/spikes/007-training-data-mechanism-probes
source_review_input: ./experiments/review_inputs/phase2_probe_cases.json
---

# Qualitative Review

## Reviewed Cases

This review uses the bounded 007 probe surface in [phase2_probe_cases.json](./experiments/review_inputs/phase2_probe_cases.json) together with the most relevant 004 review artifacts and the 006 handoff. The question is not whether every family still looks interesting. The question is whether the surviving families now have mechanism-backed reasons to consume one of the scarce `008` slots.

### `SPECTER2`

- `[artifact-reported]` The quantitative probe shows the clearest specialization pattern after `Voyage`: target profiles `P3` and `P8` have mean `J@20 = 0.4589` versus `0.6604` on non-target profiles, with `7.0` truly unique papers on target profiles versus `3.33` elsewhere.
- `[source-traceable]` The strongest prior qualitative support remains the blind `P3` review from Spike 004, where the divergent set was preferred on the specialized quantum profile; see [specter2_P3_blind_review.md](../004-embedding-model-evaluation/experiments/reviews/specter2_P3_blind_review.md).
- `[artifact-reported]` The new `P8` probe surface shows lower seed-token overlap than MiniLM's unique papers (`0.0784` vs `0.1898`) while staying mostly inside seed categories (`0.8333` category-match rate).
- `[artifact-reported]` The contradiction case is `P2`: the broad LLM-reasoning surface is less category-coherent (`0.3333` vs MiniLM `0.5`) and the unique titles read more like broad CoT-adjacent widening than a clean specialized-science signal.
- `[derived]` The mechanism story survives, but only in a bounded form: `SPECTER2` looks strongest on narrow technical / specialized domains. The direct citation/community step remains blocked, so the mechanism should be treated as partially supported rather than settled.

### `Stella`

- `[artifact-reported]` The quantitative probe shows strong target concentration: `P6` and `P7` have mean `J@20 = 0.4304` versus `0.6216` on non-target profiles, with `6.5` truly unique papers on target profiles versus `3.33` elsewhere.
- `[source-traceable]` Spike 004 already described `Stella` as the thinnest evidence case among the live local challengers and said the deployment-realism story "only emerged clearly on 2 profiles"; see [DECISION.md](../004-embedding-model-evaluation/DECISION.md).
- `[source-traceable]` Spike 004's broader findings also record that `Stella`'s divergence is highest and most interesting on `P6` and `P7`, but mixed on quality; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[artifact-reported]` The `P6` probe surface does show a practical/application-heavy mix, but the `P7` surface is more scattered and the contradiction case `P2` reads as broad reasoning-adjacent widening rather than a practical/deployment mechanism.
- `[source-traceable]` Spike 006 also left `Stella` explicitly ambiguous because it produced the strongest `kNN` lifts together with some of the strongest qualitative instability; see [HANDOFF.md](../006-model-retrieval-interactions/HANDOFF.md) and [QUALITATIVE-REVIEW.md](../006-model-retrieval-interactions/QUALITATIVE-REVIEW.md).
- `[derived]` `Stella` still carries a real open question, but the specific mechanism story remains too proxy-dependent and too profile-local to count as a strong mechanistic justification for an `008` slot.

### `GTE`

- `[artifact-reported]` `GTE` is the weakest divergence-concentration case that still survives the probe wave: target profiles `P2` and `P8` show mean `J@20 = 0.5738` versus `0.6601` on non-target profiles, with a `1.17` lift in truly unique papers.
- `[source-traceable]` Spike 004 already characterized `GTE` as the most conservative challenger: coherent, mildly valuable, and methodologically broader, but less distinct than `SPECTER2` or `Voyage`; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[artifact-reported]` The best support case is `P8`, where the unique titles remain clearly foundational and mathematically oriented. The contradiction case is `P2`, where the unique papers widen into multimodal and benchmark-style reasoning papers with no category match to the seed categories.
- `[derived]` The methodological-envelope story still looks coherent, but it reads as a modest conservative extension rather than a sharply distinct relation type. That weakens its claim on scarce downstream evaluation capacity.

### `Voyage`

- `[artifact-reported]` `Voyage` shows the strongest overall divergence concentration in the probe wave: target profiles `P2` and `P7` have mean `J@20 = 0.4074` versus `0.6304` on non-target profiles, with `7.0` truly unique papers versus `3.5` elsewhere.
- `[source-traceable]` The decisive prior qualitative evidence remains the blind `P2` review from Spike 004, which explicitly says the divergence is not noise and that the unique papers surface reasoning failure modes and alternative mechanisms; see [voyage_P2_blind_review.md](../004-embedding-model-evaluation/experiments/reviews/voyage_P2_blind_review.md).
- `[artifact-reported]` The contradiction case is `P1`, where `Voyage` is near-redundant with the incumbent and adds almost no meaningful distinctness.
- `[source-traceable]` Spike 004 already framed `Voyage` as highly profile-dependent and operationally problematic, not as universally better; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[derived]` The mechanism story survives in a bounded but meaningful form: `Voyage` appears most defensible on broad conceptual profiles where the incumbent misses frontier / failure-mode papers, not on narrow profiles where it mostly converges.

## Agreement With Metrics

1. `[derived]` The metrics are right that `SPECTER2`, `Stella`, and `Voyage` each show real target-profile concentration, while `GTE` is materially weaker.
2. `[derived]` The metrics are also right that `Voyage` and `SPECTER2` remain the most structurally distinctive families worth explaining, not merely the most different lists.
3. `[derived]` The review supports treating the blocked citation/community branch as a real limit on how far the `SPECTER2` mechanism story can be taken.

## Disagreement With Metrics

1. `[derived]` `Stella`'s strong concentration signal is not enough, by itself, to validate the specific deployment-oriented mechanism claim. The mechanism remains too proxy-heavy.
2. `[derived]` `GTE`'s weaker concentration signal should not be read as incoherence or noise. The review surface supports "coherent but conservative," not "failed."

## Bounded Interpretation

- `[derived]` Spike 007 strengthens `H2`, but unevenly. The training-data / representation story looks most defensible for `SPECTER2` and `Voyage`, only partially defensible for `Stella`, and modest for `GTE`.
- `[chosen for now]` The best use of the scarce `008` comparison budget is therefore to carry forward the two families with the clearest surviving mechanism-backed reasons to matter in use: `SPECTER2` and `Voyage`.
- `[chosen for now]` `Stella` should be treated as a deferred unresolved candidate rather than a promoted one. `GTE` should be treated as a coherent conservative challenger that no longer justifies one of the top two slots.

## What This Review Cannot Settle

1. `[artifact-reported]` The direct citation/community probe is blocked by missing graph metadata, so the strongest version of the `SPECTER2` story remains untested.
2. `[artifact-reported]` Much of the historical qualitative surface still comes from Spike 004 AI reviews rather than human adjudication.
3. `[derived]` This review cannot say whether the surviving mechanism-backed differences actually improve research outputs. That remains the purpose of `008`.
