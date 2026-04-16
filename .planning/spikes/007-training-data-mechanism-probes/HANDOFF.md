---
type: spike-handoff
status: complete
date: 2026-04-16
author: codex
target: .planning/spikes/007-training-data-mechanism-probes
next_spike: .planning/spikes/008-function-in-use-and-blind-spots
---

# Spike Handoff

## Carry Forward

1. `[chosen for now]` Carry forward `SPECTER2`.
2. `[chosen for now]` Carry forward `Voyage`.

## Deferred

1. `[chosen for now]` Defer `Stella`.
2. `[chosen for now]` Defer `GTE`.
3. `[open]` If `Voyage` proves too operationally unstable during `008` execution prep, `Stella` is the first fallback candidate, but that substitution must be recorded explicitly rather than done silently.

## Drop For Now

1. `[chosen for now]` Keep `Qwen3` dropped.
2. `[derived]` Nothing in 007 created a new reason to reopen it.

## Still Ambiguous

1. `[artifact-reported]` The direct citation/community branch for `SPECTER2` remains blocked.
2. `[artifact-reported]` `Voyage` remains operationally problematic and partly confounded by its 8% embedding-failure history.
3. `[derived]` `Stella` still looks like a plausible practical-extension candidate, but not one with enough mechanism-backed support to outrank the carried pair.

## Downstream Obligations

1. `008` should compare exactly three configurations in the first pass:
   - incumbent `MiniLM + TF-IDF`
   - `SPECTER2`
   - `Voyage`
2. `008` should include at least:
   - one broad conceptual profile (`P2` is the clearest candidate)
   - one specialized technical profile (`P3` or `P8`)
3. `008` should explicitly trace whether challenger-only papers are merely selected or actually contributed to the final task outputs.
4. If `Voyage` is replaced during execution prep, write that branch decision into `TASK-MATRIX.md` before any runs begin.

## Trace-Attunement Note

This spike translated training-data / mechanism questions into profile-sensitive divergence checks plus lexical/category proxy surfaces because the stronger citation/community route was unavailable. That translation was necessary and productive, but it also compresses richer mechanism questions into the traces left by ranking differences on one sample and one review surface.

## Counter-Reading

One counter-reading is that `Stella` should have claimed an `008` slot because it had the strongest 006 complementarity score. I am not choosing that reading because 007 was supposed to narrow on mechanism-backed reasons to keep paying evaluation cost. `Stella` remained interesting but too proxy-heavy; `Voyage` retained the stronger direct qualitative case for a distinct relation type, and `SPECTER2` retained the strongest specialized-domain pattern.
