---
type: posterior-update
status: complete
date: 2026-04-16
reviewer: codex
target: .planning/spikes/006-model-retrieval-interactions
hypothesis: H3
---

# Posterior Update

## Question

Did centroid vs `kNN-per-seed` materially change the comparative picture enough to strengthen `H3`?

## Prior Credence

- `[chosen for now]` `P(H3) = 0.75`

## Evidence Summary

- `[artifact-reported]` All 10 challenger-family combinations were classified `method-sensitive`.
- `[artifact-reported]` Centroid vs `kNN-per-seed` overlap is low-to-moderate for every challenger (`mean J@20 ~= 0.43-0.51`).
- `[artifact-reported]` `kNN-per-seed` improves the union benchmark against `MiniLM + TF-IDF` almost everywhere, but qualitative review finds recurrent fragmentation and adjacency drift.
- `[derived]` Retrieval choice is therefore not a small implementation detail. It materially changes what each model appears to be doing.

## Posterior Credence

- `[chosen for now]` `P(H3) = 0.89`

## What Caused The Shift

1. `[derived]` The strongest driver is universality: every challenger changed meaningfully under retrieval-method variation across both carried frames.
2. `[derived]` The second driver is asymmetry of interpretation: `kNN` regularly increases breadth but does not regularly improve coherence. That is exactly a model-by-retrieval interaction, not mere random variance.
3. `[derived]` The posterior does not move all the way to certainty because the present evidence still comes from one `kNN` operator and one sample-bounded evaluation environment.

## Reversal Conditions

1. `[artifact-reported]` If later runs with a different retrieval operator such as MMR show that the same families are stable across methods, this posterior should move back down.
2. `[derived]` If 007 finds that the most load-bearing differences are mechanistically model-specific rather than method-specific, some of this shift should be redistributed from H3 to H2.
3. `[derived]` If 008 later shows that the broader `kNN` lists do not improve task outputs at all, `H3` remains true as an interaction claim, but its product significance decreases.

## Bounded Conclusion

- `[chosen for now]` `H3` is strongly strengthened.
- `[chosen for now]` The strengthened claim is: retrieval method materially changes challenger behavior and therefore changes how model differences should be interpreted.
- `[chosen for now]` The claim is **not**: `kNN-per-seed` is better than centroid overall.
