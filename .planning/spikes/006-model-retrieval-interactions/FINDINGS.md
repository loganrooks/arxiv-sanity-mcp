---
status: complete
date: 2026-04-16
source_checkpoint: ./experiments/checkpoints/phase1_quantitative.json
qualitative_review: ./QUALITATIVE-REVIEW.md
---

# Spike 006 Findings

## Question

How does retrieval method interact with each model family's embedding geometry, and does that interaction change which models remain meaningfully distinct?

## Main Findings

1. `[artifact-reported]` Retrieval method changes the recommendation sets for every challenger under both carried profile families.
   - Across all 10 challenger-family combinations, centroid vs `kNN-per-seed` top-20 overlap is only `0.43-0.51` on average.

2. `[artifact-reported]` `kNN-per-seed` improves the `MiniLM + challenger` union benchmark relative to centroid for almost every model across almost every profile family.
   - Example: under the saved MiniLM family, every challenger shows `profiles_knn_better_on_union_at_20 = 8`.

3. `[artifact-reported]` The same `kNN` shift usually lowers category recall.
   - This is mild for some challengers and severe in some cases like `Stella` and `Voyage`.

4. `[derived]` The central interaction pattern is:
   - centroid emphasizes intersectional coherence
   - `kNN-per-seed` emphasizes seed-local breadth
   - the tradeoff is real for all challengers, but no challenger turns this tradeoff into a clean overall win

5. `[derived]` Spike 006 therefore strengthens `H3`, but it does not identify a retrieval-method champion.

## Per-Model Read

### `SPECTER2`

- `[artifact-reported]` Mean union delta improves from `-3.625` to `-0.625` on the saved family and from `-3.625` to `-0.875` on the category family when moving from centroid to `kNN`.
- `[derived]` The improvement is real, but qualitative review shows more adjacency drift and less disciplined topical focus.
- `[chosen for now]` Status: `carry forward`

### `Stella`

- `[artifact-reported]` `Stella` shows the strongest raw `kNN` rescue on the saved family (`-4.250` to `0.000`) and a meaningful lift on the category family (`-2.750` to `-0.625`).
- `[derived]` The rescue is not stable. Dense-topic cases look promising, but other cases show obvious drift.
- `[chosen for now]` Status: `ambiguous / needs later functional test`

### `Qwen3`

- `[artifact-reported]` `kNN` improves the union benchmark substantially for Qwen3 on both carried families.
- `[source-traceable]` Spike 005 already weakened Qwen3 on framework-robustness grounds, and Spike 004 documented its vocabulary-sensitive noise.
- `[derived]` 006 does not reverse that earlier weakening. The retrieval change makes Qwen3 more different, not more trustworthy.
- `[chosen for now]` Status: `drop for now`

### `GTE`

- `[artifact-reported]` `GTE` shows consistent `kNN` improvement with comparatively controlled qualitative drift.
- `[derived]` It remains the most conservative challenger: the retrieval choice matters, but the family does not collapse into obvious noise.
- `[chosen for now]` Status: `carry forward`

### `Voyage`

- `[artifact-reported]` `Voyage` also shows strong `kNN` lifts, but the reviewed cases combine genuine exploratory reach with high-variance adjacency drift.
- `[source-traceable]` Spike 004's strongest Voyage story still comes from centroid-era broad-profile divergence on `P2`, not from `kNN`.
- `[derived]` `kNN` keeps Voyage live as an interesting family, but not as a cleaner or safer one.
- `[chosen for now]` Status: `carry forward`

## Shortlist

### `[chosen for now]` Shortlist for 007 / possible 008 carry-forward

1. `SPECTER2`
2. `Stella`
3. `GTE`
4. `Voyage`

### Dropped for now

1. `Qwen3`

## Bounded Conclusion

- `[derived]` Retrieval geometry is a real confound and a real source of behavior change.
- `[derived]` It does not wash away the earlier framework result from 005.
- `[derived]` It also does not produce a simple shortlist by itself; instead it prunes one weakened family (`Qwen3`) and leaves four live challengers that need mechanism-level discrimination in 007.

## Qualifications

1. `[artifact-reported]` The carried frames were limited to the saved MiniLM family and the category + lexical family from 005.
2. `[artifact-reported]` This spike did not run MMR; it tested centroid vs the Spike 003 `kNN-per-seed` operator only.
3. `[derived]` The shortlist is therefore still provisional and should be read as a narrowing result, not a product recommendation.
