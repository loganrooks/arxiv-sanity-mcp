# Spike Design Principles

Distilled from the Spike 003 epistemic revision and the deliberation constellation on framework reflexivity. These are practical guidelines for designing and executing spike experiments, not a comprehensive methodology. They address specific failure modes observed in practice.

**Source:** Spike 003 review session (2026-03-20/21), signals `sig-2026-03-20-jaccard-screening-methodology`, `sig-2026-03-20-spike-experimental-design-rigor`, `sig-2026-03-20-premature-spike-decisions`. Codex review (2026-03-23).

---

## Before designing

1. **State the question clearly.** What specifically will the spike answer? What will it NOT address? Scope creep during execution is the enemy of honest findings.

2. **Check what earlier spikes assumed.** If this spike depends on earlier findings, check whether those findings have been qualified by later work. Cross-spike qualification notes exist for a reason.

## Sample and measurement design

3. **Justify sample size relative to selectivity.** If you're selecting top-K from N papers, what is K/N? Selectivity above 5% risks inflating agreement between methods. The Spike 003 Voyage screening used 20% selectivity (top-20 from 100 papers) — too coarse to distinguish models.

4. **Validate the sample from multiple perspectives.** Don't validate only from the baseline/incumbent's perspective. A sample that preserves MiniLM's neighborhoods might not preserve Voyage's. Check that challenger models also produce non-degenerate results on the sample.

5. **Use multiple metrics that constitute different aspects of the phenomenon.** Jaccard constitutes difference as binary overlap. Rank correlation constitutes it as ordering agreement. Qualitative review constitutes it as situated relevance. Their disagreements are the most informative data. Never use a single metric as a sole decision criterion.

6. **Document each metric's limitations before using it.** What does it detect? What can't it detect? Is it biased toward any particular approach? This documentation should exist in the DESIGN.md, not be discovered during synthesis.

## Qualitative review

7. **Qualitative review is mandatory, not optional.** It is a blocking gate before any verdict. Spike 003 demonstrated repeatedly that qualitative review contradicts quantitative conclusions — SPECTER2 redundancy, fusion profile-dependence, kNN niche utility, TF-IDF undervaluation. Skipping it doesn't reduce confidence; it produces wrong conclusions.

8. **Invite the reviewer to notice value beyond standard relevance.** Productive provocations, landscape-mapping, set-level coherence, connections to adjacent fields — these may be where a model's distinctive value lies, and a review template that asks only "is this paper relevant?" will miss them.

9. **Note what the review can't assess.** The reviewer is an AI model, not a researcher. Ask the reviewer to note: "What would I need to know about the researcher's actual situation to assess this properly?" This preserves the trace of the absent researcher.

## Decision structure

10. **Distinguish decided, deferred, and provisional.** Not every finding warrants a decision. "Decision deferred pending further evidence" is a legitimate and valuable spike outcome. Provisional defaults (pragmatic starting points for implementation) are different from settled decisions.

11. **Don't let the template pressure closure.** A DECISION.md has a "Decision" section. Having the section doesn't mean you have to fill it with a decision. If the evidence warrants deferral, defer.

12. **Use the three-level confidence framework.** For each finding:
    - **Measurement:** Did we accurately measure what the instrument detects? (Usually yes for well-executed experiments)
    - **Interpretation:** Does the measurement mean what we say it means? (Depends on evaluation framework, biases, entanglements)
    - **Extrapolation:** Does the finding hold beyond the testing conditions? (Depends on domain, scale, temporal scope, who's asking)

## Extension experiments

13. **Extensions get the same design rigor as core experiments.** When gap-fill or extension experiments are added during execution, they should go through the same design thinking as the core DESIGN.md — sample justification, metric selection, qualitative review requirement. Otherwise they inherit the spike's authority without inheriting its methodology.

## Evaluation framework awareness

14. **Name your evaluation framework's entanglements.** If the ground truth (clusters, profiles, held-out papers) was constructed using one of the models being evaluated, the evaluation systematically advantages that model. This is not a flaw to fix — it's a condition to name and account for in interpretation.

15. **Supplement entangled metrics with independent ones.** Category-based recall, metadata ground truth, held-out recovery counts — these don't depend on any embedding model's representation and provide a cross-check on entangled metrics.

## Responsiveness

16. **The DESIGN.md is a plan, not a contract.** If during execution something doesn't fit — a metric seems wrong, an anomaly suggests the assumptions are off, the qualitative review reveals something the design didn't anticipate — pause and ask whether the methodology needs revision. Document the deviation rather than hiding it.

17. **An experiment that discovers it needs to become exploratory mid-execution should be allowed to.** Confirmatory mode (testing predictions) and exploratory mode (following anomalies) serve different purposes. The transition between them should be documented, not suppressed.

## Meta-methodology (lighter touch)

18. **State the methodology's commitments explicitly.** What does it assume about relevance, quality, comparison? These commitments are posited with reasons and held as revisable. They inform how findings should be interpreted, not how experiments should be run.

19. **The meta-methodology section is diagnostic, not additional protocol.** It helps interpret findings; it doesn't add execution steps. Don't over-engineer the philosophical apparatus at the expense of actually running the experiment.

20. **Leave a trace of what exceeded the design.** After the spike, note what happened that the DESIGN.md couldn't hold. This feeds back into these principles and into the deliberation constellation.

---

*These principles are themselves revisable. They emerged from one spike program's failures and may not anticipate future failure modes. The last principle (leave a trace of what exceeded the design) is the mechanism by which new principles can emerge.*
