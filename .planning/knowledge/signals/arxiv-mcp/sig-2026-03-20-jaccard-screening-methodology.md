---
id: sig-2026-03-20-jaccard-screening-methodology
type: signal
project: arxiv-mcp
tags: [spike-003, methodology, evaluation-bias, embedding-screening]
created: 2026-03-20T14:45:00Z
updated: 2026-03-20T14:45:00Z
durability: convention
status: active
---

## Observation

The Voyage AI embedding screening (Spike 003, W5a) used top-K Jaccard overlap as the sole criterion for deciding whether to proceed with full profiling. Voyage was rejected ("not a new signal axis") based on Jaccard 0.717 with MiniLM and 0.772 with SPECTER2, falling in the "partial overlap zone" (0.6-0.8).

This screening methodology has fundamental limitations that the spike's own epistemic principles should have caught:

### Jaccard limitations (as applied)

1. **Binary threshold artifact.** Jaccard over top-K neighbor lists treats papers at rank #19 and #21 as categorically different (in vs out), collapsing near-misses and genuine divergences into the same binary. Two models with nearly identical rankings can produce low Jaccard from boundary noise alone.

2. **All disagreements treated equally.** A paper ranked #1 by Voyage but #21 by MiniLM (barely missed) counts identically to #1 by Voyage but #10,000 by MiniLM (genuinely different signal). The measure cannot distinguish boundary noise from meaningful divergence.

3. **Nature of divergence invisible.** The ~28% of papers Voyage finds differently could be random noise, a specific valuable signal axis, or domain-specific expertise. Jaccard collapses "different how?" into a single number. TF-IDF's value comes from *what kind* of different papers it finds (vocabulary-distinctive), not from the *amount* of difference.

4. **Narrow sample.** Only 10 query seeds from 2 of 8 interest profiles (P1, P3) were tested. Per-seed Jaccard ranged from 0.429 to 0.905 — enormous variance suggesting the aggregate mean is not representative. Profiles where Voyage might shine (broad/cross-domain P4, P7; trending P6) were never tested.

5. **Baseline calibration invalid.** Decision thresholds were calibrated against MiniLM-SPECTER2 overlap (Jaccard 0.732) as the "known different" baseline. The W5.4 qualitative review subsequently found SPECTER2 is actually redundant with MiniLM (45-60% overlap, score compression makes ranking noise). The baseline itself is suspect.

6. **Overlap ≠ redundancy.** This is the deepest problem. A model with 72% overlap could still be essential if the 28% divergence captures a specific kind of paper the other model structurally cannot find. Conversely, a model with 30% overlap could be useless if the different papers are irrelevant. Only qualitative review of the divergent papers can answer this.

### Contradiction with spike's own principles

The DESIGN.md explicitly states:
- "Qualitative review is first-class, not a validation step"
- "Instruments detect, they don't evaluate"
- "No metric value should ever be presented as a bare number — interpretation is required"

Yet the Voyage screening used a single quantitative instrument as the sole evaluation criterion with no qualitative layer. This contradicts the spike's stated methodology.

### Pattern match

This is the same class of error as the MRR bias caught by the W1 qualitative review: a quantitative metric (MRR/Jaccard) giving a verdict (MiniLM best/Voyage redundant) that qualitative assessment might contradict. The W3 review found fusion helps narrow topics despite worse MRR. The W5.4 review found SPECTER2 is redundant despite looking different on Jaccard. Both demonstrate that quantitative overlap/quality measures can mislead in both directions.

## Impact

- Voyage was rejected based on evidence that doesn't meet the spike's own epistemic standards
- Any finding qualified by "Jaccard overlap" (including the SPECTER2 Jaccard 0.178 between MiniLM and SPECTER2 in W1, and the Voyage screening thresholds) should be treated as provisional
- The screening protocol itself needs revision: Jaccard may be a useful initial filter but should never be the sole decision criterion

## Recommendation

1. **Qualify Voyage verdict.** Change from "rejected — not a new signal axis" to "screening inconclusive — Jaccard-based screening insufficient, qualitative evaluation not performed"
2. **Alternative metrics for embedding comparison.** Use rank correlation (Kendall's tau), qualitative review of divergent papers, and semantic clustering of unique papers alongside or instead of top-K Jaccard
3. **Broader sample.** Any embedding screening should test across all interest profiles, not a subset, given the high per-seed variance observed
4. **Apply the spike's own rule.** If "instruments detect, they don't evaluate" is the principle, then no screening instrument alone should produce a stop/go decision. Qualitative review of the divergent papers is the minimum bar before rejecting a model.

## Affected Findings

- W5a Voyage screening verdict (STOP): Should be qualified as "inconclusive pending qualitative review"
- Spike 003 DECISION.md Voyage section: Needs caveat
- The "parallel views with local-only models fully validated" claim in .continue-here.md: Overstated — Voyage was not properly evaluated
- Any prior use of Jaccard as a quality/redundancy measure across the spike program
