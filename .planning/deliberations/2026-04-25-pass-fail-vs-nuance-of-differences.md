---
type: deliberation
status: principle articulated; pattern recurring
date: 2026-04-25
level: workflow / writing posture
form: short principle articulation with worked examples and honest follow-through
follow_through: PARTIAL — pattern recurred in subsequent prose
related:
  - 2026-04-25-mediation-vs-position-taking.md
  - ../spikes/reviews/2026-04-25-handoff-pressure-pass.md
---

# Pass/Fail vs Nuance-of-Differences

## What prompted this deliberation

After the paired AI review of the pressure pass landed (cross-vendor + Opus adversarial), I framed the synthesis in survive/qualify/retract terms — "Finding 1 survives with qualification; Finding 2 partially retracts; what's the net effect on remedies?" The user pushed:

> "I mean we should stop thinking about things in terms of a 'pass/fail' verdict, and think about what the nuances of their differences perhaps demand of us? And yes we should record the dispatch, did they not write their own outputs?"

Two redirections in one prompt: first, stop reducing the paired-review outputs to verdicts; second, stop summarizing the reviews' content (they wrote their own outputs).

## What the deliberation surfaced

### The flaw in pass/fail framing

When two readers produce overlapping-but-not-identical readings of the same artifact, summarizing them as "this finding survives / that one retracts" does several harmful things:

- **Collapses information into verdict.** The two readers' *differences* carry information — about reading distance, about which kinds of failures each catches, about the multiple defensible framings of the same underlying concern. Verdicts erase this.
- **Smuggles in synthesis as judgment.** Choosing which parts "survive" requires the synthesizer to weight the reviewers — but who is the synthesizer to do so? A single-author synthesizer-of-reviewers is exactly the closure point the paired review was meant to escape.
- **Replicates the closure-pressure pattern at one level up.** The paired review caught closure pressure in the pressure pass. If its outputs are then collapsed back to verdicts, the pressure escapes the audit and lands again.

The right move: hold the divergences as data; let differences indicate what they demand.

### What the differences actually demanded

The two reviews, working independently, produced:

- **One convergent fact** (`NEXT-ROUND-SUITE.md:65-69`'s pre-registered tiebreaker rule) that indicted a specific clause in the pressure pass — much narrower than a finding-level verdict.
- **Multiple defensible readings of the same residue** — Finding 1 carries (a) a methodological-vocabulary reading (when is something "labeled"?), (b) a document-discipline reading (when an explicit rule is overridden, how should the override be registered?), and (c) a cost-rationality reading (the cap forced criterion choice). Each implies different remedy-cells in the dimensional response space. *Holding the plurality* — not picking — is the methodology's stance.
- **Reading-distance signal.** Cross-vendor caught substance more readily; same-vendor caught register more readily. Different review pairs catch different categories of failure. This is itself a finding worth recording.
- **A retraction the chain itself contained.** Finding 2's chain-wide claim was contradicted by the pressure pass's own analysis of 006. The contradiction was internal; no review needed to demonstrate it; the pressure pass demonstrated it against itself.

### Why this is its own deliberation

The pattern (verdict-shaped synthesis under multi-source input) recurred in this session's prose more than once. It's not just a one-off correction; it's a writing posture that needs explicit pattern-watch.

## What was decided

**Principle:** When multiple sources produce overlapping-but-not-identical readings of the same artifact, do not synthesize into a verdict. Hold the plurality, treat the differences as data, and ask what they demand.

**Workflow consequence:** When integrating multi-source output, the integration step should:

- Surface the convergent facts (high-confidence indictments).
- Enumerate the multiple defensible readings without picking among them.
- Report the divergence axes as findings in their own right.
- Identify any internal contradictions in the source artifacts that the multi-source reading exposes.

**Writing-register consequence:** Avoid "X survives" / "Y retracts" / "Z is overstated" register. Use "X's narrowest version is concrete and specific; X's broader claim faces specific counter-evidence; X's remedy implications scale with which version you take." Calibrated language as default, not closing-section exception.

## Status of follow-through

**Partial.** The layered "After the paired review" section in the pressure pass embodies this principle (convergent fact, multiple defensible readings, divergence analysis, self-application). But:

- Subsequent operationalization-recommendation prose slipped back into verdict-shaped framing ("Finding 1 carries a binding reading") that needed re-prompting from the user to walk back.
- The walk-back required an explicit assumption audit (see `2026-04-25-load-bearing-assumptions-audit.md`) before the verdict-shape was fully retired.
- The pattern is recurring rather than fixed. Pattern-watch is needed at every subsequent integration step.

## Open questions

- **When is synthesis appropriate vs cover for non-commitment?** Synthesis is appropriate when honestly producing a fused view that's more than the sum of parts; it's cover when used to defer position-taking. Hard to distinguish in practice except by asking *whose work* the synthesis is doing. If it's doing *my* work (helping me commit), it's honest. If it's doing the *reader's* work (forcing them to pick the position I won't), it's cover.
- **How to integrate multi-source output without verdict-shaping when a decision is required?** Sometimes a decision must be made (e.g., "should we fix `008`'s comparison surface or not?"). Then the decision-act is a position-taking move (see `2026-04-25-mediation-vs-position-taking.md`), and verdict-shaping the *prior multi-source reading* is a different category. Don't confuse the two.

## Workflow-level lesson

**Verdict-shape the decisions; nuance-shape the readings.** When taking a position, name it. When integrating multi-source readings, hold the plurality. Don't let one register colonize the other.

## Form notes

This document is short because the principle is simple. Its value comes from the worked examples (paired-review integration; assumption audit walk-back) and the honest follow-through admission. The pattern's value increases each time it's referenced from a new piece of work, so brevity helps re-reading.
