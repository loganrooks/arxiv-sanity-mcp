---
status: complete
date: 2026-04-16
target: .planning/spikes/006-model-retrieval-interactions
---

# Spike 006 Decision

## Decision

### Chosen For Now

1. Treat retrieval geometry as a live interpretive variable for every challenger family.
2. Do not treat `kNN-per-seed` as a default replacement for centroid.
3. Drop `Qwen3` from the live challenger set for now.
4. Carry `SPECTER2`, `Stella`, `GTE`, and `Voyage` into 007.

## Why

- `[artifact-reported]` Every challenger changed materially under centroid vs `kNN-per-seed`.
- `[derived]` The qualitative review shows that many of those changes come from seed-local breadth and fragmentation, not from a clean improvement in recommendation quality.
- `[artifact-reported]` Qwen3 was already weakened by 005 and 006 did not restore it.
- `[derived]` The remaining four families still each carry a distinct enough open question to justify mechanism probes in 007.

## What This Does Not Decide

1. It does not decide that centroid is globally better than `kNN-per-seed`.
2. It does not decide that `Stella`, `SPECTER2`, `GTE`, or `Voyage` should become product views.
3. It does not decide whether a later task-based evaluation should compare family-level or method-specific configurations.

## Resulting Posture For 007

- `[chosen for now]` 007 should investigate mechanism claims for the four carried families.
- `[chosen for now]` 007 should use 006's method sensitivity as a qualifier, not as permission to reopen the full configuration matrix.
