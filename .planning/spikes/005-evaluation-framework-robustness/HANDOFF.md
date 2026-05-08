---
type: spike-handoff
status: complete
date: 2026-04-16
author: codex
target: .planning/spikes/005-evaluation-framework-robustness
next_spike: .planning/spikes/006-model-retrieval-interactions
---

# Spike Handoff

## Carry Forward

1. `[chosen for now]` Carry the saved MiniLM-derived family forward as the incumbent comparison frame.
2. `[chosen for now]` Carry the `category + lexical` family forward into 006 as the required alternative frame.
3. `[artifact-reported]` Keep the full challenger set in 006, consistent with the suite contract.
4. `[derived]` Treat the Qwen3 candidate-second-view story as weakened rather than live by default.

## Drop For Now

1. `[chosen for now]` Drop the assumption that Qwen3 is a presumptive complementary second-view candidate.
2. `[chosen for now]` Drop any expectation that alternative profile construction is likely to produce a new positive challenger without additional retrieval-method evidence.

## Deferred

1. `[open]` Whether the SPECTER2-refined family should be reintroduced later as a tertiary cross-check if 006 produces ambiguous results.
2. `[open]` Whether Voyage's known P2 value story survives a cleaner, non-API-dependent analogue in later spikes.

## Still Ambiguous

1. `[artifact-reported]` Voyage and GTE each show one family-induced downgrade, but the qualitative support for those downgrades is weaker than the quantitative movement.
2. `[derived]` SPECTER2 looks more negative under the category family, but the change reads more like "do not promote" than "remove from consideration."
3. `[artifact-reported]` Stella remains stable but inconclusive.

## Downstream Obligations

1. `006` must run on:
   - the saved MiniLM-derived family
   - the category + lexical family
2. `006` must test whether retrieval geometry changes restore any challenger that 005 weakened, especially Qwen3.
3. `006` must not treat a positive result on the incumbent frame alone as sufficient if the category family still blocks or weakens the same claim.
4. `006` should use the SPECTER2-refined family only as a later adjudication aid if the two carried frames disagree in a way that remains decision-relevant after centroid vs `kNN-per-seed`.

## Trace-Attunement Note

The translation of "framework bias" into this spike is operationalized as "family-induced classification shift across three constructed profile families." That translation is useful, but it compresses a wider plurality of possible interest constructions into three concrete families. In particular, it leaves citation-native and graph-native profile construction outside the present test.

## Counter-Reading

An alternative reading is that some of the observed shifts reflect instability in the new family-construction heuristics rather than deep dependence on MiniLM's worldview. That counter-reading remains live because both alternative families are sample-bounded and seed-anchored. The practical response is not to ignore the present shifts, but to carry only the strongest model-independent alternative family into 006 and avoid inflating 005 into a general anti-MiniLM verdict.
