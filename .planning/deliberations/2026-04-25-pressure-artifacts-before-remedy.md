---
type: deliberation
status: workflow articulated; pattern reusable
date: 2026-04-25
level: workflow / methodology
form: short workflow articulation with worked example
follow_through: followed through; produced a substantive artifact
related:
  - ../spikes/reviews/2026-04-25-handoff-pressure-pass.md
  - sequential-narrowing-anti-regret-and-spike-inference-limits.md
---

# Pressure the Artifacts Before Remedy

## What prompted this deliberation

After the deliberation `sequential-narrowing-anti-regret-and-spike-inference-limits.md` and its independent review, I had proposed adopting one of the review's recommendations — the `[evidence-weakened] / [cost-deferred] / [both]` decision tag — and applying it forward to the next handoff to "see if it survives contact." The user pushed:

> "So wait, pressure the artifacts, the reviews, the findings, before deciding how to proceed?"

The prompt named the inversion. I was about to *adopt a remedy* and then test it forward. The user's reframe: *pressure-test the existing artifacts first*; let what surfaces decide what discipline to adopt.

## What the deliberation surfaced

### The asymmetry the prompt corrected

Forward-pressure-testing (adopt a remedy, see how it lands) and backward-pressure-testing (read the existing artifacts critically, see what surfaces) sound symmetric but aren't.

- Forward-pressure-testing has the new remedy as a *premise*. It tests "does this remedy hold?" but not "is this the right remedy?" The remedy is granted standing.
- Backward-pressure-testing has the existing artifacts as the only premises. It surfaces *what failure modes are actually present*. Then the remedy can be selected to match what's present.

The first answers a closed question (does the remedy work?). The second answers an open question (what should the remedy be?). For methodology audit work, the open question should come first.

### The pattern, generalized

When proposing a remedy in response to a perceived methodological problem:

1. **Identify what artifacts the remedy would govern.** (E.g., `005`/`006`/`007` `HANDOFF.md`s, `NEXT-ROUND-SUITE.md`, `008/DESIGN.md`.)
2. **Read those artifacts critically before adopting the remedy.** Not as a rewrite — as a read-and-annotate pass that produces a separate artifact.
3. **Surface what's actually there.** Concrete failure modes, framing claims, register issues, internal contradictions, classification difficulties.
4. **Select the remedy from what surfaces**, not from the option space the original deliberation drew.
5. **Preserve the source artifacts.** Pressure passes don't overwrite their subjects.

### Why this matters

The deliberation that prompted the audit had constructed a four-option space (A/B/C/D). Adopting a remedy from that space without first pressuring the artifacts would have repeated the deliberation's own mistake — choosing a patch from a constructed option space without anchoring in concrete failure modes. The user named this directly in the prompt's framing.

The corollary: **constructed option spaces are themselves subject to pressure-testing.** Pressure passes can surface that the deliberation's option space was wrong, before any of its options is adopted.

## What was decided

**Workflow pattern:** Before adopting a remedy in response to a perceived methodological problem:

1. Run a pressure pass on the artifacts the remedy would govern.
2. Use what surfaces to select / shape / retract the remedy.
3. Pressure passes are read-and-annotate passes producing separate artifacts; they do not overwrite their subjects.
4. The pressure pass is itself subject to pressure-testing if it produces framing claims (see paired review of pressure pass — `2026-04-25-pass-fail-vs-nuance-of-differences.md`).

**Format conventions for pressure passes:**

- Date-prefixed naming: `YYYY-MM-DD-<subject>-pressure-pass.md`.
- Per-artifact diagnostic questions, structured.
- Cross-artifact synthesis with explicit findings.
- Confidence calibration per finding.
- A reflexive section: what does this pass not legitimately tell us?

## Status of follow-through

**Followed through in this session.** The pattern produced:

1. A pressure pass artifact (`2026-04-25-handoff-pressure-pass.md`) with seven findings.
2. A paired review of the pressure pass that caught two factual errors and identified rhetorical inflation.
3. A layered "After the paired review" section appended to the pressure pass that recorded what survived, qualified, or retracted.
4. Substantive findings (the suite-contract tiebreaker reversal at `007`; the asymmetric comparison surface in `008/DESIGN.md`) that the original deliberation would not have surfaced.
5. The eventual multi-lens redirection (which would not have been visible without the pressure pass uncovering the chain's drift from ADR-0001).

The workflow paid for itself many times over relative to the alternative of forward-testing the original deliberation's remedy.

## Open questions

- **When should pressure passes happen automatically?** Probably whenever a methodology-audit remedy is being proposed for committed adoption. The pattern's cost (1-3 hours per pass) is small relative to the cost of adopting the wrong remedy.
- **What about pressure-passing the pressure pass?** This is what the paired review effectively did. The pattern recurses: pressure-test the artifacts; pressure-test the pressure-test if it produces framing claims; stop when the next pressure-test would only surface vocabulary issues. Diminishing returns set in fairly fast (after 2-3 levels in this session).
- **Can the pressure pass be done cross-vendor?** Yes, and arguably should be when the artifacts have been written by one vendor's models. Cross-vendor pressure-testing avoids same-vendor blind spots in reading.

## Workflow-level lesson

**Pressure-test what's there before adopting what's proposed.** The artifacts the remedy would govern are the only authoritative source of what failure modes exist. Read them critically; let what surfaces shape the remedy. Don't adopt-and-then-validate; surface-and-then-select.

## Form notes

Short because the workflow is recipe-shaped. The worked example (this session's pressure pass + paired review chain) demonstrates the pattern; the recipe is generalizable.
