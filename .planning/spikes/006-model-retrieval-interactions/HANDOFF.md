---
type: spike-handoff
status: complete
date: 2026-04-16
author: codex
target: .planning/spikes/006-model-retrieval-interactions
next_spike: .planning/spikes/007-training-data-mechanism-probes
---

# Spike Handoff

## Carry Forward

1. `[chosen for now]` Carry forward `SPECTER2`.
2. `[chosen for now]` Carry forward `GTE`.
3. `[chosen for now]` Carry forward `Voyage`.
4. `[chosen for now]` Carry forward `Stella` as an explicitly ambiguous family with a possible dense-topic `kNN` niche.

## Drop For Now

1. `[chosen for now]` Drop `Qwen3` for now.
2. `[derived]` 005 weakened Qwen3 on framework-robustness grounds, and 006 did not produce a clean retrieval-based rescue.

## Deferred

1. `[open]` Whether any model-specific `kNN` configuration, rather than the model family as a whole, should later re-enter 008 as a concrete challenger.
2. `[open]` Whether `MMR` would separate "useful breadth" from "fragmented breadth" more cleanly than `kNN-per-seed`.

## Still Ambiguous

1. `[artifact-reported]` `Stella` shows the strongest `kNN` lifts but also some of the strongest qualitative instability.
2. `[artifact-reported]` `Voyage` remains interesting but operationally problematic and high-variance.
3. `[derived]` `SPECTER2` and `GTE` remain live for different reasons, but 006 alone does not rank one clearly above the other.

## Downstream Obligations

1. `007` must run on the shortlist of four families:
   - `SPECTER2`
   - `Stella`
   - `GTE`
   - `Voyage`
2. `007` should treat `Qwen3` as dropped unless a concrete later reason emerges to reopen it.
3. `007` should probe mechanism claims at the family level first, not by exploding into every model x retrieval-method combination.
4. `007` may note `kNN` as a possible niche qualifier, especially for `Stella`, but it should not let 006's method-sensitivity reopen the full configuration space.
5. `007` must narrow the live challenger set to at most two for `008`, following the suite rule.

## Trace-Attunement Note

This spike translated "retrieval geometry" into one concrete operator contrast: centroid vs the Spike 003 `kNN-per-seed` procedure. That translation is productive, but partial. The result should therefore be read as a disciplined test of one retrieval-geometry contrast, not as the final word on retrieval method in general.

## Counter-Reading

One counter-reading is that `kNN`'s near-universal union gains mean the spike should have carried method-specific configurations rather than model families. I am not choosing that reading here because it would explode the downstream space too early. The stronger practical move is to carry the families, remember the method-sensitivity, and force 007 to decide whether any of these families still have mechanism-backed reasons to survive before 008 revisits concrete configuration choices.
