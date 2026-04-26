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

## Override Annotation — Suite Contract Tiebreaker Reversal (added 2026-04-25)

This handoff narrows the live candidate set for `008` using mechanism-backed reasons as the operative criterion (`SPECTER2` and `Voyage` carried; `Stella` deferred). The 2026-04-25 paired adversarial review of the methodology audit cycle surfaced that this reverses the suite contract's pre-registered tiebreaker rule at [`NEXT-ROUND-SUITE.md:65-69`](../NEXT-ROUND-SUITE.md), which orders the tiebreaker as:

1. strongest evidence of complementarity against the incumbent from 006
2. strongest surviving mechanism support from 007
3. greater structural distinctness from the incumbent

By the suite contract's #1 criterion, `Stella` had the strongest 006 complementarity score among the shortlist (per [`007/FINDINGS.md`](./FINDINGS.md): "006 still gives [Stella] the strongest complementarity score among the shortlist"). 007 selected the carry-forward pair using criterion #2 (mechanism support) ahead of #1, without registering the reversal at the suite-contract layer. The Counter-Reading above states the alternative criterion choice and gives reasons against it, but does not name the choice as an explicit override of the suite-level rule.

This annotation registers that override now: 007's narrowing applied mechanism-support-trumps-complementarity rather than the suite contract's complementarity-first ordering. The reversal was defensible (the program's standing methodology in [`spikes/METHODOLOGY.md`](../METHODOLOGY.md) prefers mechanism evidence over end-to-end correlational evidence) but should have been registered as a reversal at handoff time, not only as a counter-reading.

This annotation is documentation hygiene; it does not change the carried set. With the multi-lens redirection committed in [ADR-0005](../../../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md) and `008` superseded by v0.2 Phase 17 (longitudinal pilot harness), the operational consequence is moot. The annotation exists so future readers can reconcile what 007 did with what the suite contract said it should do.
