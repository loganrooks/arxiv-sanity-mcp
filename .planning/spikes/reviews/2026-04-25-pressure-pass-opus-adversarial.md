---
type: opus-adversarial-review
phase: paired
status: complete
date: 2026-04-25
reviewer: Claude Opus 4.7 (fresh session)
target: 2026-04-25-handoff-pressure-pass.md (Findings 1 and 2 only)
---

# Opus Adversarial Pass — Findings 1 and 2

## Adversarial argument against Finding 1

Finding 1 claims: *"Mechanism-support > complementarity is a load-bearing stance choice that is not labeled as one. It is the single decision excluding Stella from 008. Not pre-registered in NEXT-ROUND-SUITE.md, not argued from evidence in 007. Reclassifying it as a contested choice changes the program substantively."*

Three parts of this claim are independently contestable: (a) "not pre-registered in NEXT-ROUND-SUITE.md," (b) "not argued from evidence in 007," and (c) "the single decision excluding Stella." I will argue (a) and (b) are wrong on the textual evidence, and that (c) is overstated. What survives is a thinner, more interesting finding the pressure pass does not quite locate.

### (a) The "not pre-registered" claim is straightforwardly false on the text

The pressure pass writes Finding 1 in the synthesis as "Not pre-registered in NEXT-ROUND-SUITE.md." This is wrong. The suite contract at `NEXT-ROUND-SUITE.md:62-69` reads:

> "If more than two challengers remain live, `007` must rank them and select the top two for `008` using this order:
>   1. strongest evidence of complementarity against the incumbent from `006`
>   2. strongest surviving mechanism support from `007`
>   3. if still tied, greater structural distinctness from the incumbent"

This is a pre-registered tiebreaker. So the operative criterion *is* enumerated, in order, in the suite contract — the program did exactly the kind of pre-registration the pressure pass says it didn't do. That fact alone makes the strong "not pre-registered" framing of Finding 1 indefensible as written.

What the suite contract pre-registers, however, is the *opposite* ordering from the one 007 applied: **complementarity is criterion #1, mechanism support is #2.** And by 006's own scoring (`007/FINDINGS.md:46`: "006 still gives [Stella] the strongest complementarity score among the shortlist"), Stella was the top-ranked challenger on criterion #1. 007's narrowing therefore reverses the suite's tiebreaker order. This is a real finding, but it is the *opposite* finding from "the choice was unflagged" — it is "the choice was flagged in the suite contract and then countermanded at 007 without re-pre-registration of the new ordering." The pressure pass missed this because it relied on the chain-coherence intuition without auditing the suite contract for the very rule the chain was supposed to follow.

This sharpens the methodological concern but undermines the rhetorical framing. "Load-bearing stance choice that is not labeled as one" is the wrong description. The accurate description is "load-bearing tiebreaker reversal that the chain does not register as a reversal."

### (b) The "not argued from evidence" claim is uncharitable on the text

The pressure pass writes "Not pre-registered in NEXT-ROUND-SUITE.md, not argued from evidence in 007. Reclassifying it as a contested choice changes the program substantively." Two of those clauses are doing different work, and both are stronger than the artifacts support.

007/HANDOFF.md's Counter-Reading reads:

> "One counter-reading is that `Stella` should have claimed an `008` slot because it had the strongest 006 complementarity score. I am not choosing that reading because 007 was supposed to narrow on mechanism-backed reasons to keep paying evaluation cost. `Stella` remained interesting but too proxy-heavy; `Voyage` retained the stronger direct qualitative case for a distinct relation type, and `SPECTER2` retained the strongest specialized-domain pattern."

This sentence does three things in twelve lines: (i) it names the alternative criterion (complementarity), (ii) it gives a reason for declining it (007's purpose, with cost as the operative constraint), and (iii) it provides per-family evidential differentiation ("too proxy-heavy" for Stella, "stronger direct qualitative case" for Voyage, "strongest specialized-domain pattern" for SPECTER2). The pressure pass treats this Counter-Reading as evidence the choice was *unflagged*. That is structurally backwards. The Counter-Reading exists precisely to flag the contested choice; if naming the alternative criterion, justifying its rejection, and citing per-family evidential differences does not count as flagging, then "flagging" reduces to "would have used the words 'load-bearing stance choice'," which is a vocabulary objection, not a methodological one.

This is the *Counter-Reading-is-the-flag* frame from the prompt, and on the textual evidence it is largely correct. The pressure pass's own characterization at 007/Q4 — "The Counter-Reading does honest work, but the carried claim sits in a frame where the 'mechanism > complementarity' weighting is asserted, not argued" — concedes the Counter-Reading does honest work, then walks the concession back. The walk-back relies on a specific high standard for "argued from evidence" that the pressure pass does not justify.

What would "argued from evidence" look like? Presumably a quantitative comparison of "complementarity score's predictive validity for function-in-use" versus "mechanism support's predictive validity for function-in-use" — the only thing that could decide the criterion choice on evidence rather than on epistemic posture. But neither metric has been validated against function-in-use yet (that is what 008 is for). At Round 1, the criterion choice cannot be decided by evidence, only by methodological commitment. That makes the "not argued from evidence" critique self-undermining: it sets a standard the program could not yet meet.

### (c) Methodology-level support for mechanism-as-gate is non-trivial

The *implicit-norm* frame asks: does the program's standing methodology already commit to mechanism-backed reasoning as the canonical narrowing posture?

`METHODOLOGY.md:68-75` (the "Mechanistic decomposition" lens) reads:

> "**Diagnoses:** End-to-end testing that confirms something works without explaining why. When it breaks, you don't know what to fix. When it succeeds, you don't know what's load-bearing. 'Signal axis' characterizations are mechanistic stories with untested mechanism steps. **Recommends:** For hypotheses with proposed mechanisms... design tests for individual steps, not just the endpoint."

This is the program's standing reason for preferring mechanism-backed evidence over end-to-end correlational evidence. Complementarity scores from 006 are exactly the kind of "end-to-end" pattern (model A's output diverges from incumbent's output) that the methodology specifically warns against trusting in isolation. Treating mechanism support as a tiebreak criterion when complementarity alone is correlational is *inside* the methodology, not outside it. The pressure pass's implication that mechanism-as-gate appears *de novo* at 007 ignores that the methodology already gives reasons to weight mechanism evidence more highly than end-to-end pattern evidence when the two diverge.

Note this only partially defends 007. The methodology supports treating mechanism evidence as *important*, not as *trumping* complementarity in a tiebreaker. So the implicit-norm frame supports the *direction* of 007's choice while leaving the *override* of the suite contract's #1 criterion still unlicensed. That is a real but smaller residue than Finding 1 claims.

### (d) Cost-rationality is real and the pressure pass underweights it

007/HANDOFF.md's Counter-Reading explicitly invokes cost: "I am not choosing that reading because 007 was supposed to narrow on mechanism-backed reasons **to keep paying evaluation cost**." The suite contract pre-registers an "at most two challengers" cap (`NEXT-ROUND-SUITE.md:62-63`, `008/DESIGN.md:47-50`). Given the cap, the question 007 faced was not whether to narrow but on what criterion. The pressure pass treats the criterion choice as if narrowing itself were optional. It isn't, given the cap.

If the cap is taken as binding, the practically forced choice was between (i) following the suite's #1 tiebreaker (complementarity → Stella in) and (ii) following the suite's #2 tiebreaker plus the methodology's preference for mechanism evidence (→ Stella out). Both are defensible. Neither is "unflagged stance" in the rhetorically loaded sense the pressure pass uses. The frame "contested choice between two pre-registered criteria, with the chosen criterion under-justified relative to the suite's stated #1" is more accurate.

### (e) "The single decision excluding Stella" is too strong

007/HANDOFF.md's Counter-Reading also says: "Stella remained interesting but too proxy-heavy." This is a separate substantive judgment about Stella's *evidence quality*, not just about the criterion choice. 007/FINDINGS.md is harder still:

> "Stella: ...006 still gives it the strongest complementarity score among the shortlist. But Spike 004 also called Stella the thinnest evidence case, and 006 marked it explicitly ambiguous... The family remains live as an unresolved practical-extension candidate, but the mechanism story is not strong enough to justify an 008 slot ahead of stronger-backed families."

Two things follow. First, Stella's exclusion has at least three named bases — proxy-heaviness (evidence-quality concern, not stance-choice), 004's "thinnest evidence case" judgment carried forward, and 006's explicit "ambiguous" tag. The mechanism-vs-complementarity criterion choice is not the only thing excluding Stella. Second, even if you flip the criterion to complementarity-first, you have to overcome Stella's accumulated evidence-quality problems. The claim that reclassifying the criterion would force Stella into 008 ("**Forces:** `008` should run with three challengers") is not supported. It would re-open the question, not settle it the other way.

### What survives of Finding 1

Pulling these threads together: **the framing of Finding 1 does not survive, but a sharper finding survives inside it.** What survives is:

> "007's narrowing reverses the suite contract's pre-registered tiebreaker order (complementarity #1, mechanism #2) by treating mechanism support as the operative gate. The reversal is acknowledged in 007's Counter-Reading but is not registered as a reversal of the suite-level rule that would normally govern the situation. Whether the reversal is licensed by the program's standing methodology (which prefers mechanism evidence over correlational evidence) or whether the suite contract should govern is the actual contested question."

This is narrower, more locatable, and more actionable than "load-bearing stance choice not labeled as one." It also shifts the remedy: the right response is not "split or widen 008 to three challengers" — it is "reconcile the suite contract's tiebreaker order with the methodology's mechanism-preference and update one or the other." That is closer to the *amend* / *augment* cells than the *split-or-widen* cell the pressure pass actuates.

## Adversarial argument against Finding 2

Finding 2 claims: *"Configuration-vs-family slippage runs through the whole chain. 005 evaluates families; 006 honestly defers configuration-level questions; 007 narrows on family; 008 evaluates 'configurations' but uses family names. The configuration question is never directly answered yet 008 is asking for that answer."*

This finding is more textually grounded than Finding 1 — slippage between "configurations" and "family" in 008/DESIGN.md is a real lexical fact. But three claims inside the finding are stronger than the artifacts support: (i) the slippage runs "through the whole chain"; (ii) 008 is "asking for" a configuration-level answer; and (iii) the slippage is substantive rather than registral. I take these in turn.

### (i) The "whole chain" claim conflates honest deferral with slippage

The pressure pass at 006/Q1 itself classifies "Model-specific kNN configuration re-entering 008" as *cost-deferred* and adds: "This is a textbook cost-deferred exclusion that the handoff itself names." Then in Finding 2 it cites 006 as part of the "slippage" — even though the same pass just classified 006's treatment as the *non*-slippage case ("006 honestly defers configuration-level questions"). Finding 2's grammar elides this: "005 evaluates families; 006 honestly defers configuration-level questions; 007 narrows on family; 008 evaluates 'configurations' but uses family names." That sentence wants to indict the chain, but its second clause is exoneration, not indictment. If 006's treatment is honest, then "the slippage runs through the whole chain" is rhetorically convenient but textually wrong: 006 is the counter-example.

This is the *deferred-not-elided* frame from the prompt and on the textual evidence it lands. 006/HANDOFF.md's Counter-Reading is explicit:

> "kNN's near-universal union gains mean the spike should have carried method-specific configurations rather than model families. I am not choosing that reading here because it would explode the downstream space too early. The stronger practical move is to carry the families, remember the method-sensitivity, and force 007 to decide whether any of these families still have mechanism-backed reasons to survive before 008 revisits concrete configuration choices."

That is principled bracketing with an explicit hand-off back to 008 ("before 008 revisits concrete configuration choices"). Treating that as evidence of the slippage is the move the prompt warns about: the deferral is the methodology's auxiliary-aware discipline working as intended. Finding 2 would be more honest scoped as "the slippage exists at 008 and was handed to 008 by 007 without resolution," not as a chain-wide failure.

### (ii) The "wrong question" charge is overreach

The pressure pass writes: "If the configuration-vs-family distinction is reclassified from 'deferred' to 'the actual primary failure mode,' `008`'s narrowing premise — *that families are the right unit* — collapses... **`008` is asking the wrong question.**" That phrase ("asking the wrong question") is the core of the *wrong-question* frame from the prompt, and on examination it is not what 008 is doing.

008/DESIGN.md's question (`008/DESIGN.md:21-23`) reads:

> "For the configurations that remain live after Spikes 005-007, which ones actually help research tasks, and do the papers outside the current two-view arrangement contribute to task outputs or merely to measured difference?"

This question is not "is family-level analysis sufficient?" It is "do these configurations help research tasks?" The unit is whatever was carried forward from 005-007 — which by 006's deferral is family-level for now, with configuration-level as a possible later return. 008's correct response to family-level inputs is to test family-level outputs and (if the result is positive) flag that configuration-level testing is the next obvious move. That is not the wrong question. That is the right question for the unit it was given.

The pressure pass's charge therefore has to slide from "008 is testing the wrong unit" (defensible) to "008 is asking the wrong question" (overreach). Testing units and asking questions are different things. The unit is contestable; the question is not. Finding 2 would be sounder if it read "008's unit of analysis inherits an unresolved family-vs-configuration question that should be made explicit in the design's preamble."

### (iii) "Configurations" in 008/DESIGN.md may be vocabulary, not slippage

The *register-not-substance* frame asks whether "configuration" and "family" are different registers of the same object in this program's vocabulary. Look at 008/DESIGN.md's actual usage:

- `008/DESIGN.md:47-50`: "Run at most three configurations in one pass: the incumbent control, plus up to two shortlisted challengers... The current 007 handoff selects SPECTER2 and Voyage for the first pass."

The sentence binds "configurations" to "what 007 carried forward." Within 008/DESIGN.md, a "configuration" *is operationally defined* as "a model family slot whose internal retrieval geometry, profile family, prompt frame, tool budget, turn budget, context budget, and stopping condition are standardized in Phase 1" (`008/DESIGN.md:67-75`). That is a configuration in the strong sense — model family + retrieval geometry + profile + tool/turn/context budgets all held fixed. The fact that the model-family slot is named by family label (`SPECTER2`, `Voyage`) rather than by configuration ID does not entail that the entity tested is a family rather than a configuration; the entity tested is the configuration that pairs the family label with the standardized everything-else.

This is the *substitutability* frame. If, within a family, the configuration choice is locally consequential but globally substitutable for function-in-use, then the family-as-configuration shorthand is empirically warranted. We don't yet know whether substitutability holds — but neither does the pressure pass, and the pressure pass's stronger conclusion ("the slippage is material") is no better evidenced than the program's working assumption that it isn't. The pressure pass's "Slippage" verdict at 008/Q3 is asserted without showing that any plausible reasonable SPECTER2 configuration would behave very differently at the function-in-use layer. That is exactly the load-bearing claim the pressure pass needs to support and doesn't.

Note also: 008's standardization of *everything else* (`008/DESIGN.md:67-75`) is the configuration-level move. The model family is the only varying piece across "configurations" by design. That is a configuration-level test where the differentiating axis happens to be the family. Calling that "family masquerading as configuration" gets the rhetorical force exactly backwards — it is configuration-level testing of family as the contrastive variable. Whether that test is sufficient depends on substitutability within family, which 008's results would themselves bear on (positively if SPECTER2 wins; ambiguously if it doesn't).

### What survives of Finding 2

What survives, and what does not, is sharper than Finding 1:

**Survives:** 008/DESIGN.md uses "configuration" and family-name interchangeably without defining their relation. A footnote or preamble paragraph stating "by 'configuration' we mean: model family slot + standardized retrieval geometry, profile selection, and tool/turn/context budget; the model family is the only contrastive variable" would resolve the lexical issue without any structural redesign. This is a clarification finding, not a "the chain has been doing the wrong thing" finding.

**Does not survive:** The chain-wide indictment ("runs through the whole chain"). 006 is a counter-example, not an example. The "wrong question" framing. 008 is asking the right question for its inherited unit. The implication that the criterion choice forces 008's redesign rather than its preamble.

## Pressure-pass overstep audit

Numbered list of specific sentences in the pressure pass that overstep, with the overstep named:

1. **Synthesis Finding 1, line 260: "Not pre-registered in NEXT-ROUND-SUITE.md, not argued from evidence in 007."** *Overstep: factually wrong on the first clause.* The suite contract at `NEXT-ROUND-SUITE.md:65-69` pre-registers a tiebreaker that names complementarity #1 and mechanism #2. The pressure pass's claim is the opposite of what the document says. The accurate finding is that 007 *reversed* the pre-registered order — a different and weaker indictment.

2. **007/Q1, line 132: "The judgment that *mechanism-support trumps complementarity* is the load-bearing stance choice in the entire chain."** *Overstep: persuasive framing standing in for argument.* "Load-bearing" is asserted; the load it bears is asserted ("excludes Stella from 008 on its own"); but the demonstration that it is *the single* exclusionary mechanism is contradicted by 007/FINDINGS.md's separate "proxy-heavy" and "thinnest evidence case" judgments about Stella, which the same pressure pass cites approvingly elsewhere.

3. **007/Q1, line 132: "It excludes Stella from `008` on its own."** *Overstep: ignores other named bases for exclusion.* 007/FINDINGS.md flags Stella's "proxy-heavy" mechanism story, 004's "thinnest evidence case" verdict carried forward, and 006's "ambiguous" tag. The criterion choice is one of several factors. Saying "on its own" elides the others.

4. **006/Q6, line 122: "HIGHEST-IMPACT FINDING IN THE PASS:"** *Overstep: persuasive framing in lieu of argument.* All-caps emphasis is doing rhetorical work the analysis under it does not earn. The claim ("`008` is asking the wrong question") is not derived from textual evidence; it is asserted.

5. **006/Q6, line 122: "But the latter two are family designators, not specific configurations."** *Overstep: assumes the slippage's substantive consequences without showing them.* Whether SPECTER2 and Voyage are "family designators" or "canonical-family-configuration designators" depends on the program's working vocabulary, not on the words alone. 008/DESIGN.md's standardization of everything-else (Phase 1) makes the model-family-name a contrastive label *within* a configuration. The pass treats this as obviously slippage; the artifacts allow at least two readings.

6. **007/Q4, line 154: "The 'mechanism > complementarity' weighting is asserted, not argued."** *Overstep: holds the artifact to a standard the program could not yet meet.* At Round 1, the relative predictive validity of mechanism evidence vs complementarity for function-in-use cannot be argued from evidence — that is what 008 is for. Treating the criterion choice as failable for "not argued from evidence" sets an unmeetable bar for any pre-functional-test methodological commitment.

7. **007/Q6, line 168: "**CRITICAL:**"** *Overstep: persuasive labeling.* Like the all-caps elsewhere, "CRITICAL" performs urgency the underlying argument does not establish. The Stella-into-008 conclusion presupposes that flipping the criterion is sufficient to override 004/006's evidence-quality concerns, which is not shown.

8. **007/Q6, line 168: "Forces: `008` should run with three challengers (SPECTER2, Voyage, Stella) plus the control — exceeding the suite rule."** *Overstep: prescription not entailed by the diagnostic.* Even if the criterion is contested, "forces three challengers" treats the cost cap as suspendable on framing grounds. The pass nowhere argues the cap should bend; it just declares the consequence.

9. **Cross-artifact synthesis, Finding 2, line 262: "The configuration question is never directly answered yet `008` is being asked to answer it."** *Overstep: misdescribes 008's question.* 008's question is whether shortlisted configurations help research tasks, not whether configuration-level analysis is the right unit. The pass collapses "the program has not answered question X" into "spike asking question Y is failing." Those are different.

10. **Confidence calibration, line 311: "If so, the load-bearing stance label is mine, not theirs — but the *unflagged* nature of the choice still warrants the methodological remedy."** *Overstep: the calibration walks back the framing without retiring the remedy.* If the choice was always implicitly flagged by the methodology's mechanism-preference (as the calibration concedes is possible), then "unflagged" is the wrong word and the methodological remedy proposed (decision-tag templates) does not follow from a vocabulary objection. The calibration concedes the framing while preserving its consequences. The two should move together.

11. **006/Q4, line 110: "operational closure with no pre-registered concrete reason."** *Overstep: treats absence of a *new* pre-registered reason as absence of pre-registration.* Qwen3 had been classified `[chosen for now] Drop For Now` at 005/HANDOFF.md (line 21) and `[chosen for now] Drop Qwen3 for now` at 006/HANDOFF.md (line 21). The chain's operational closure was the cumulative result of two pre-registered decisions, not a fresh closure with no pre-registration. The pass's framing implies absence of evidence where there is documented prior decision-making.

12. **NEXT-ROUND-SUITE Q4, line 196: "Asymmetry: narrowing is the default; non-narrowing requires explicit declaration. Biases toward closure."** *Overstep: pathologizes asymmetry that is methodologically required.* Some asymmetries between default and exception are non-pathological (e.g., "deferring requires reasons" is the design principle of decision-by-evidence). Calling this "bias toward closure" treats normative structure as evidential bias.

13. **Cross-artifact synthesis, line 260: "**Highest impact.**"** *Overstep: ranking-by-rhetoric.* "Highest impact" is asserted as a label. The pressure pass does not perform a comparative impact analysis among findings; it labels Finding 1 highest and Finding 2 second-highest by fiat. Given that Finding 1 contains a factual error (the pre-registration claim) and Finding 2's chain-wide claim is contradicted by Finding 2's own internal exoneration of 006, the impact ranking is at minimum unstable.

## Net effect

After this pass: **Finding 1 does not survive in its claimed form; a narrower finding survives inside it.** What survives is "007 reversed the suite contract's pre-registered tiebreaker order without registering the reversal." That is real, methodologically actionable, and substantially different from "load-bearing stance choice not labeled as one." The remedy implied by the surviving finding is reconciliation between suite contract and standing methodology, not splitting/widening 008. **Finding 2 partly survives.** The lexical complaint — "configuration" and family-name used interchangeably in 008/DESIGN.md without defining their relation — is real and warrants a one-paragraph preamble fix. The chain-wide claim does not survive (006 is the program's counter-example to it, by the pressure pass's own assessment). The "wrong question" charge does not survive (008's question, read carefully, is correctly posed for its inherited unit). The remedy implied by what survives is a vocabulary clarification in 008's preamble, not a structural redesign. The overstep audit found systematic rhetorical inflation — all-caps emphasis labels, "load-bearing" / "highest-impact" / "CRITICAL" used as argument-substitutes, prescriptive consequences ("Forces:") that overrun their diagnostic grounds, and one factual error about pre-registration that is foundational to Finding 1. The pressure pass's confidence calibration acknowledges Findings 1 and 2 are framing claims but does not retire the rhetorically loaded vocabulary or scale the remedies down to match the calibrated confidence. (One adjacent observation noted only in passing per the prompt's "no new findings" rule: the surviving Finding 1 residue suggests a worth-checking question about *which* document — suite contract, methodology, or both — should be amended to reconcile the tiebreaker reversal. That is for the next deliberation, not this review.)

## Steelman residue

I want to be honest about which adversarial frames did less work than they look like they did on first writing.

The *register-not-substance* frame for Finding 2 looks strong rhetorically but is weaker than it appears. It asks the reader to grant that "configuration" and family-name are the same object in different registers — but 008/DESIGN.md does not actually establish that vocabulary anywhere. I had to do the establishing work in my argument, citing Phase 1 standardization. A program that has to be defended by external reconstruction has not done its own vocabulary work, and the pressure pass's complaint that the relation is undefined is correct as far as it goes. What I attacked was the *consequence* the pressure pass drew from the lexical fact, not the lexical fact itself. The lexical fact survives as a clarification finding; my defense narrows the remedy without rescuing the artifact.

The *cost-rationality* frame for Finding 1 is real — the cap is binding, the choice was on criterion not on whether to narrow — but it does not fully defend the criterion choice. Cost-rationality can defend "narrowing was forced," not "the criterion the narrowing used was the right one." The pressure pass is wrong to treat the criterion as freely chosen, but the charge that the criterion override of the suite's #1 tiebreaker is unflagged is partly right after I correct the framing. I took the pressure pass's "not pre-registered" claim apart on the document, but I had to substitute a more accurate finding ("tiebreaker reversed without re-pre-registration") rather than retire the concern.

The *Counter-Reading-is-the-flag* frame is the strongest of the four. It does most of the load-bearing work in my Finding 1 attack. But its strength depends on what counts as "flagging." If "flagging" requires using methodology-internal vocabulary like "this is a stance choice" with explicit alternative argumentation, 007's Counter-Reading does *not* meet that bar — it states the alternative and gives reasons against it but does not adopt the metacognitive frame of "I am making a contested methodological commitment." The pressure pass's standard is high but not unreasonable. So this frame partially defeats Finding 1, not fully.

The *deferred-not-elided* frame for Finding 2 is correct on the text and I am confident in it. 006 is the counter-example to the chain-wide claim and the pressure pass's own classification of 006's treatment as honest deferral concedes this. I do not think this frame is weaker than it looks.

The *wrong-question* frame is correct on the text. 008's design-question phrasing is unambiguous; "asking the wrong question" requires misreading the design's actual question.

The *implicit-norm* frame for Finding 1 is real but limited. The methodology supports treating mechanism evidence as important, not as trumping the suite contract's #1 tiebreaker. So this frame defends *direction* but not *magnitude* of 007's choice.

Net of the steelman residue: my attack on Finding 2 is stronger than my attack on Finding 1. Finding 1 has a real methodological residue ("tiebreaker reversal") that I think survives, even though the pressure pass's framing of that residue does not. Finding 2 reduces to a clarification finding. Honest summary: the pressure pass identified two real issues, mis-described both, and the right response is to keep the underlying concerns and discard the rhetorical scaffolding that attached them to "load-bearing-but-unflagged" and "asking the wrong question."
