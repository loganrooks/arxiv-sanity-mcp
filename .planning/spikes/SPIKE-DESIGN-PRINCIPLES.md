# Spike Design Principles

Distilled from the Spike 003 epistemic revision, the Spike 004 post-execution critique, and the deliberation constellation on framework reflexivity. These are practical guidelines for designing and executing spike experiments, not a comprehensive methodology. They address specific failure modes observed in practice.

**Source:** Spike 003 review session (2026-03-20/21), Spike 004 execution + critique (2026-03-27/30), signals `sig-2026-03-20-jaccard-screening-methodology`, `sig-2026-03-20-spike-experimental-design-rigor`, `sig-2026-03-20-premature-spike-decisions`. Codex review (2026-03-23). Philosophies-of-science discussion (2026-03-29/30).

**Companion documents:** `METHODOLOGY.md` (interpretive lenses for design critique and findings interpretation) complements these practical rules.

---

## Purpose and framing

1. **Spikes characterize; they don't crown winners.** The purpose is to map the trade-off space so users can make informed decisions for their own situation (hardware, use case, domain, values). The output is a characterization of each strategy's behavior, costs, and conditions — not a verdict about which is best. Different users with different constraints will make different choices from the same characterization.

2. **State the question clearly.** What specifically will the spike answer? What will it NOT address? Scope creep during execution is the enemy of honest findings.

3. **Check what earlier spikes assumed.** If this spike depends on earlier findings, check whether those findings have been qualified by later work. Cross-spike qualification notes exist for a reason.

4. **Get independent design critique before execution.** The same agent that writes DESIGN.md should not be the sole judge of whether it's ready. An independent critic should review the design for: untested auxiliary assumptions, paradigmatic framing that advantages an incumbent, evaluator monoculture, mechanism steps that are asserted but untested, non-epistemic values doing implicit work. (See `METHODOLOGY.md` for the critical lenses.) Pattern A — self-awareness outruns executable protocol — is not prevented by self-critique alone.

## Sample and measurement design

3. **Justify sample size relative to selectivity.** If you're selecting top-K from N papers, what is K/N? Selectivity above 5% risks inflating agreement between methods. The Spike 003 Voyage screening used 20% selectivity (top-20 from 100 papers) — too coarse to distinguish models.

4. **Validate the sample from multiple perspectives.** Don't validate only from the baseline/incumbent's perspective. A sample that preserves MiniLM's neighborhoods might not preserve Voyage's. Check that challenger models also produce non-degenerate results on the sample.

5. **Use multiple metrics that constitute different aspects of the phenomenon.** Jaccard constitutes difference as binary overlap. Rank correlation constitutes it as ordering agreement. Qualitative review constitutes it as situated relevance. Their disagreements are the most informative data. Never use a single metric as a sole decision criterion.

6. **Document each metric's limitations before using it.** What does it detect? What can't it detect? Is it biased toward any particular approach? This documentation should exist in the DESIGN.md, not be discovered during synthesis.

7. **Characterize seed sensitivity before reporting findings.** Compute key metrics across all available seed subsets and report the distribution, not a point estimate. Spike 004 discovered post-hoc that per-profile J@20 varies by up to 0.360 depending on seed choice — a finding that would have reframed the entire synthesis if known upfront. Any metric that is not stable across seed variants should be flagged as seed-sensitive and used with appropriate caution.

8. **Compare all models to each other, not just to one baseline.** Hub-and-spoke comparison (everything vs MiniLM) structurally privileges the baseline. A full pairwise comparison matrix reveals whether challengers cluster (similar signal) or scatter (genuinely different axes). Spike 004's "signal axis" characterizations were based on hub-and-spoke only — we never checked whether SPECTER2 and GTE diverge from each other or just from MiniLM.

## Qualitative review

9. **Qualitative review is mandatory, not optional.** It is a blocking gate before any verdict. Spike 003 demonstrated repeatedly that qualitative review contradicts quantitative conclusions — SPECTER2 redundancy, fusion profile-dependence, kNN niche utility, TF-IDF undervaluation. Skipping it doesn't reduce confidence; it produces wrong conclusions.

10. **Invite the reviewer to notice value beyond standard relevance.** Productive provocations, landscape-mapping, set-level coherence, connections to adjacent fields — these may be where a model's distinctive value lies, and a review template that asks only "is this paper relevant?" will miss them.

11. **Note what the review can't assess.** The reviewer is an AI model, not a researcher. Ask the reviewer to note: "What would I need to know about the researcher's actual situation to assess this properly?" This preserves the trace of the absent researcher.

## Decision structure

12. **Distinguish decided, deferred, and provisional.** Not every finding warrants a decision. "Decision deferred pending further evidence" is a legitimate and valuable spike outcome. Provisional defaults (pragmatic starting points for implementation) are different from settled decisions.

13. **Don't let the template pressure closure.** A DECISION.md has a "Decision" section. Having the section doesn't mean you have to fill it with a decision. If the evidence warrants deferral, defer.

14. **Use the three-level confidence framework.** For each finding:
    - **Measurement:** Did we accurately measure what the instrument detects? (Usually yes for well-executed experiments)
    - **Interpretation:** Does the measurement mean what we say it means? (Depends on evaluation framework, biases, entanglements)
    - **Extrapolation:** Does the finding hold beyond the testing conditions? (Depends on domain, scale, temporal scope, who's asking)

13. **Report probability shifts, not binary verdicts.** "CONFIRMED" and "FALSIFIED" throw away information about how much the evidence moved our confidence and why. Instead: state a prior, describe the evidence, state the posterior, explain the shift. This prevents the overclaiming-then-overqualifying whiplash that characterized Spike 004.

14. **Present findings as trade-off maps, not recommendations.** Different users with different hardware, domains, and values will choose different configurations. Separate epistemic findings ("Model X produces different rankings from Model Y, characterized by Z") from value-laden recommendations ("If you value local-first, choose X; if you value breadth, choose Y"). The spike's job is to characterize the options honestly, not to choose for the user.

## Synthesis discipline

15. **The synthesis must use what the design prescribed, not just what's most legible.** Spike 004 computed 7 metrics but the synthesis led with J@20 — the metric the design explicitly demoted. The most legible number colonizes the narrative unless the synthesizer deliberately structures the findings around the design's stated metric priorities. Write the synthesis from the stable metrics outward, not from the most dramatic number inward.

16. **Get independent findings critique after execution.** The same agent that executed the spike has sunk-cost investment in the narrative. An independent critic should check: Are the claims warranted by the evidence? Are interpretive leaps flagged? Are implicit values stated? Do the findings actually answer the design's stated questions, or a different question?

## Extension experiments

17. **Extensions get the same design rigor as core experiments.** When gap-fill or extension experiments are added during execution, they should go through the same design thinking as the core DESIGN.md — sample justification, metric selection, qualitative review requirement. Otherwise they inherit the spike's authority without inheriting its methodology.

## Evaluation framework awareness

18. **Name your evaluation framework's entanglements.** If the ground truth (clusters, profiles, held-out papers) was constructed using one of the models being evaluated, the evaluation systematically advantages that model. This is not a flaw to fix — it's a condition to name and account for in interpretation.

19. **Supplement entangled metrics with independent ones.** Category-based recall, metadata ground truth, held-out recovery counts — these don't depend on any embedding model's representation and provide a cross-check on entangled metrics.

20. **Vary auxiliary assumptions to test finding robustness.** A finding entangled with its evaluation framework can't be trusted until you vary the framework. Change the profile construction method, change the seed set, change the retrieval method, change the evaluator type. Findings that survive multiple auxiliary variations are framework-independent. Findings that change are framework-dependent and must be reported as such.

## Responsiveness

21. **The DESIGN.md is a plan, not a contract.** If during execution something doesn't fit — a metric seems wrong, an anomaly suggests the assumptions are off, the qualitative review reveals something the design didn't anticipate — pause and ask whether the methodology needs revision. Document the deviation rather than hiding it.

22. **An experiment that discovers it needs to become exploratory mid-execution should be allowed to.** Confirmatory mode (testing predictions) and exploratory mode (following anomalies) serve different purposes. The transition between them should be documented, not suppressed.

## Meta-methodology (lighter touch)

23. **State the methodology's commitments explicitly.** What does it assume about relevance, quality, comparison? These commitments are posited with reasons and held as revisable. They inform how findings should be interpreted, not how experiments should be run.

24. **The meta-methodology section is diagnostic, not additional protocol.** It helps interpret findings; it doesn't add execution steps. Don't over-engineer the philosophical apparatus at the expense of actually running the experiment.

25. **Leave a trace of what exceeded the design.** After the spike, note what happened that the DESIGN.md couldn't hold. This feeds back into these principles and into the deliberation constellation.

26. **These principles are themselves an object of inquiry.** Each spike round should ask: which principles were followed? Which were violated? Which were missing? The answers update this document. The principles improve through the same iterative process they govern.

---

*26 principles across 10 sections. Principles 1-4 and 13-16 are new from Spike 004 critique (2026-03-30). See `METHODOLOGY.md` for the interpretive frameworks that complement these practical rules. Both documents should be read by the independent design critic (principle 4) before spike execution.*
