---
type: cross-vendor-review
phase: 1
status: complete
date: 2026-04-25
reviewer: GPT (codex CLI, gpt-5.5, reasoning_effort=xhigh)
target: 2026-04-25-handoff-pressure-pass.md (Findings 1 and 2 only)
---

# Cross-Vendor Review — Phase 1: Independent Reading

## Phase 1 — Independent reading

### Question A — Mechanism-support as gate criterion

**A1 (where, if anywhere, is the weighting justified):**

My independent reading: mechanism support is explicitly justified as a relevant discriminator, but I do not see an explicit upstream justification for weighting mechanism support over 006 complementarity as the 007-to-008 narrowing criterion. The clearest formal suite rule points the other way.

Evidence:

- `METHODOLOGY.md` makes mechanism testing important: "design tests for individual steps, not just the endpoint" and says mechanisms matter because otherwise "you don't know what's load-bearing."
- `NEXT-ROUND-SUITE.md` justifies the sequence: "007 comes third because mechanism claims should only be tested after the framework and retrieval surfaces are more stable" and "008 comes last because task-based evaluation is the most expensive and should operate on a narrowed, better-justified candidate set."
- But the explicit `007 -> 008` ranking rule says that if more than two challengers remain live, 007 must select the top two using: "1. strongest evidence of complementarity against the incumbent from `006`; 2. strongest surviving mechanism support from `007`; 3. if still tied, greater structural distinctness from the incumbent."
- `006/HANDOFF.md` does authorize a family-level mechanism pass: "007 should probe mechanism claims at the family level first" and "must narrow the live challenger set to at most two for `008`." It does not say mechanism support outranks complementarity.
- `006/DECISION.md` also leaves the unit/criterion issue unsettled: "It does not decide whether a later task-based evaluation should compare family-level or method-specific configurations."

So the artifacts justify mechanism support as a gate, and justify narrowing before 008, but they do not explicitly justify reversing the suite contract's complementarity-first ranking. Confidence: high.

**A2 (contested choice or implicit best practice):**

I would treat the weighting as a contested choice, not as an implicit best practice. The methodology's epistemic posture supports asking for mechanisms, but it also warns against single-criterion closure. `SPIKE-DESIGN-PRINCIPLES.md` says "Never use a single metric as a sole decision criterion," and it frames spikes as trade-off maps: "The purpose is to map the trade-off space... not a verdict about which is best."

The contested-choice reading is strengthened by the fact that the suite contract explicitly ranked complementarity before mechanism support. A careful uninitiated reader would not naturally infer that 007 was supposed to override that order unless the artifact said why. `007/HANDOFF.md` does give a reason locally: "007 was supposed to narrow on mechanism-backed reasons to keep paying evaluation cost." But read against `NEXT-ROUND-SUITE.md`, that is a local stance choice, not an obvious pre-authorized best practice.

Confidence: high.

**A3 (consequences for 008):**

It matters, but it does not invalidate 008 outright. If the weighting is contested, then the identity of the two challengers is partly hostage to that contested choice. `008/DESIGN.md` explicitly inherits the 007 branch: "The current 007 handoff selects `SPECTER2` and `Voyage` for the first pass, with `Stella` retained only as an explicit fallback if `Voyage` proves impractical during execution prep."

That structure is still epistemically warranted as a bounded first pass because the suite required 008 to be scarce-budget and narrowed: "Run at most three configurations in one pass" and "Do not reopen the full model set unless 005-007 fail to reduce uncertainty." It is also guarded by provisional language: architectural recommendation remains "at most `[chosen for now]` unless human judgment materially supports it."

But the warranted claim should be narrow: 008 can test whether the inherited `SPECTER2`/`Voyage` shortlist helps in task use, not whether those were uniquely the right challengers to test. If a reader thinks Stella should have been selected on complementarity grounds, then 008's first-pass scope remains defensible as a constrained experimental branch, while any negative or positive conclusion must carry the selection-criterion caveat. Confidence: medium-high.

### Question B — Family vs configuration

**B1 (consistency of unit definition):**

The unit of analysis is not consistently defined across the chain. It shifts among strategy/configuration, model family, profile-construction family, and method-specific configuration.

Evidence:

- `METHODOLOGY.md` frames the desired functional question as configuration-level: ask "which configuration helps accomplish a research task?"
- `HYPOTHESES-005.md` defines H3 as a model-by-retrieval experiment: "for each model x profile x retrieval method" and calls it "a 5 model x 8 profile x 2 method = 80 configuration experiment."
- `NEXT-ROUND-SUITE.md` initially says "Spikes 007 and 008 run on a shortlisted set of model families," but its 006 handoff contract allows "at most four model families or concrete configurations."
- `005/FINDINGS.md` uses "family" mainly for profile construction, reporting "15 challenger-family comparisons (`5 models x 3 profile families`)."
- `006/FINDINGS.md` asks how retrieval method interacts with "each model family's embedding geometry," while showing material method sensitivity: centroid vs `kNN-per-seed` overlap is only "`0.43-0.51` on average."
- `006/HANDOFF.md` explicitly keeps family as the next unit: "007 should probe mechanism claims at the family level first" and "should not let 006's method-sensitivity reopen the full configuration space."
- `006/DECISION.md` then says it does not decide "whether a later task-based evaluation should compare family-level or method-specific configurations."
- `007/FINDINGS.md` returns to family-level language: "some remaining family-level differences do show patterned, profile-sensitive behavior."
- `008/DESIGN.md` asks about "shortlisted configurations" and names the comparison as incumbent `MiniLM + TF-IDF`, `SPECTER2`, and `Voyage`. That mixes one explicit model-plus-retrieval configuration with two family names.

Confidence: high.

**B2 (008's commitment):**

`008/DESIGN.md` commits to task-level functional evaluation of compared options, but it is ambiguous about whether the answer is a family-level or configuration-level claim.

The strongest configuration-level language is: "The unit of interest is whether a configuration helps an agent produce a better research output for a stated task." The design also asks: "For the configurations that remain live after Spikes 005-007, which ones actually help research tasks..."

But the concrete list does not fully specify configurations. `MiniLM + TF-IDF` is a configuration. `SPECTER2` and `Voyage` are named as families/models without a retrieval method, fusion arrangement, or inherited concrete setup stated in the design section. It may be intended that previous spike defaults fill this in, but that would be extrapolation; the design text itself does not make the unit explicit enough.

Confidence: high.

**B3 (resolved / deferred / elided):**

My classification is: substantively addressed and explicitly deferred in 006, then partially elided in 007/008.

`006` names the problem directly. The handoff says a counter-reading would carry "method-specific configurations rather than model families," and declines that reading because "it would explode the downstream space too early." The decision then states that 006 does not decide "whether a later task-based evaluation should compare family-level or method-specific configurations."

That is an explicit deferral, not a resolution. `007` proceeds family-first for mechanism narrowing, which is consistent with the deferral as a temporary discipline. But `008` then uses "configurations" while listing `SPECTER2` and `Voyage` without method-specific definition. So the chain does not resolve the distinction before 008; it carries the family-level simplification forward while using configuration-level language.

If forced into the provided categories for the chain as a whole, I would choose (b) addressed and explicitly deferred, with the important qualification that the deferral is not visibly preserved as a caveat in `008/DESIGN.md`. Confidence: high.

### Anything else you noticed

The same pattern appears in both questions: the artifacts are often careful locally, but a local "chosen for now" move can become load-bearing downstream without being re-labeled at the handoff boundary. That is not a failure of the spike suite as a whole, but it is exactly where an uninitiated reader needs the trace to be more explicit.

## Phase 2 — Comparison

**C1 — Finding 1 framing:**

Match, with qualification. The pressure pass's core framing — "Mechanism-support > complementarity is a load-bearing stance choice that is not labeled as a stance" — matches my Phase 1 reading. I independently found that the artifacts justify mechanism support as relevant, but do not explicitly justify ranking mechanism support above 006 complementarity for the 007-to-008 narrowing move. My reading actually makes the finding slightly stronger in one respect: `NEXT-ROUND-SUITE.md` appeared to give an explicit `007 -> 008` ranking rule that put "strongest evidence of complementarity against the incumbent from `006`" before "strongest surviving mechanism support from `007`."

The qualification is that I would not say mechanism-support excludes Stella entirely "on its own." It is the decisive selection criterion inside a scarce-budget rule, and it is load-bearing because the suite only allowed two challengers. The pressure pass is right about the stance choice, but its strongest remedial language should keep the cost-cap auxiliary visible. Confidence: high.

**C2 — Finding 2 framing:**

Match, with a small qualification. The pressure pass's Finding 2 — "The configuration-vs-family slippage runs through the whole chain" — matches my Phase 1 reading. I independently found that the chain moves among model families, profile families, retrieval-method configurations, and named "configurations" in `008` that are not actually specified at equal granularity.

The qualification is that the slippage is not equally hidden everywhere. `006` explicitly names and defers the issue; the problem is that the deferral is then not visibly preserved as a caveat in `007`/`008`. So I would frame this as: the distinction is surfaced, deferred, and then partially elided downstream, rather than simply missed from the start. Confidence: high.

**C3 — Overstep:**

The pressure pass oversteps in a few places by turning a strong methodological caveat into a more categorical invalidation.

First: "It excludes Stella from `008` on its own." That is too strong. The mechanism-over-complementarity stance is decisive, but not solitary. Stella is excluded under a combined bundle: the suite's two-challenger cap, the inherited 006/007 evidence, and the local decision to prefer mechanism-backed support over complementarity. A more precise claim would be that the stance is the decisive rule that determines which candidate loses the scarce slot.

Second: "It is not argued from evidence in 007." This overstates by treating an insufficient argument as no argument. `007` does give a local rationale: it says it is narrowing on "mechanism-backed reasons to keep paying evaluation cost." My Phase 1 objection is that this rationale is not explicitly justified against the upstream complementarity-first rule. So the better claim is: the stance is locally asserted and partially rationalized, but not justified against the competing criterion that the suite contract had already named.

Third: "If `mechanism-support > complementarity` is reclassified from a stance to a contested choice, Stella's exclusion is barely justified." I would not go as far as "barely justified." My Phase 1 conclusion was that `008` remains epistemically warranted as a bounded first pass, but its result must carry the selection-criterion caveat. "Barely justified" understates the legitimacy of budgeted experimental narrowing.

Fourth: "If the live question is configuration-level, `008` is asking the wrong question." The evidence supports "underspecified question" or "mixed-level question" more cleanly than "wrong question." `008` can still ask a valid functional task question if the concrete retrieval/profile/operator settings for `SPECTER2` and `Voyage` are supplied before execution. The overstep is the jump from unresolved unit-of-analysis ambiguity to categorical wrong-question diagnosis. Confidence: medium-high.

**C4 — Understate:**

Finding 1 is understated in one specific way. The pass says: "It is not pre-registered in `NEXT-ROUND-SUITE.md`, not argued from evidence in 007." My Phase 1 reading was stronger: this is not only an unregistered stance, but a stance that appears to reverse the only explicit ranking order I found in the suite contract, where complementarity from `006` came before surviving mechanism support from `007`. If that reading of the suite rule is correct, the issue is not just missing stance labeling; it is a local override of a prior decision rule without an explicit override note. Confidence: high.

Finding 2 is also slightly understated. The pass says: "`008/DESIGN.md` says compare three configurations: `MiniLM + TF-IDF`, `SPECTER2`, `Voyage`. But the latter two are family designators, not specific configurations." That is right, but the stronger version is that `008` creates an asymmetric comparison surface: the incumbent is specified as model-plus-retrieval, while the challengers are named only as families. That means the ambiguity is not just terminological; it could affect reproducibility, fairness of comparison, and interpretation of any `008` result. Confidence: high.

## Bottom line

Findings 1 and 2 both survive, with qualifications. Finding 1 survives as a load-bearing, insufficiently labeled stance choice; if my Phase 1 reading of the suite contract is right, it is even stronger than the pressure pass says because it overrides a complementarity-first rule. But the pressure pass should soften claims that Stella is excluded "on its own" or "barely justified." Finding 2 survives as stated at the synthesis level: the family/configuration unit remains unresolved going into `008`. The strongest defensible remedy is to make the exact configurations and the inherited stance choice explicit before treating `008` as a clean test of challenger value.

<!-- END CROSS-VENDOR REVIEW — both phases complete -->
