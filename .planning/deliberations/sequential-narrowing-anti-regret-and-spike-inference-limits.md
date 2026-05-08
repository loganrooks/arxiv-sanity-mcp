# Deliberation: Sequential Narrowing, Anti-Regret, and the Limits of Spike Inference

<!--
Deliberation template grounded in:
- Dewey's inquiry cycle (situation -> problematization -> hypothesis -> test -> warranted assertion)
- Toulmin's argument structure (claim, grounds, warrant, rebuttal)
- Lakatos's progressive vs degenerating programme shifts
- Peirce's fallibilism (no conclusion is permanently settled)

Additional orientation used here:
- Duhem-Quine on auxiliary-assumption dependence
- Mayo on severe testing and what a test can actually tell us
- van Fraassen on empirical adequacy and bounded claims
- Pragmatic anti-regret framing: avoid both premature closure and uncontrolled branch explosion
-->

**Date:** 2026-04-16
**Status:** Open — recommendation deferred pending artifact pressure pass (2026-04-25)
**Trigger:** Conversation during execution of the `005`-`008` spike suite raised a direct critique of the suite's narrowing logic. The question was whether the current sequence is genuinely anti-regret and challenge-seeking, or whether it prematurely closes options based on a few rounds of experiments while claiming more than those experiments can legitimately support.
**Affects:** Active `005`-`008` spike suite, future spike sequencing, spike closeout discipline, handoff design, interpretation discipline
**Related:**
- [METHODOLOGY.md](../spikes/METHODOLOGY.md)
- [SPIKE-DESIGN-PRINCIPLES.md](../spikes/SPIKE-DESIGN-PRINCIPLES.md)
- [NEXT-ROUND-SUITE.md](../spikes/NEXT-ROUND-SUITE.md)
- [HYPOTHESES-005.md](../spikes/HYPOTHESES-005.md)
- [005 HANDOFF.md](../spikes/005-evaluation-framework-robustness/HANDOFF.md)
- [006 HANDOFF.md](../spikes/006-model-retrieval-interactions/HANDOFF.md)
- [007 HANDOFF.md](../spikes/007-training-data-mechanism-probes/HANDOFF.md)
- [2026-04-16-next-round-suite-execution-readiness-review.md](../spikes/reviews/2026-04-16-next-round-suite-execution-readiness-review.md)
- [comparative-characterization-and-nonadditive-evaluation-praxis.md](./comparative-characterization-and-nonadditive-evaluation-praxis.md)
- [2026-04-16-sequential-narrowing-deliberation-review.md](./reviews/2026-04-16-sequential-narrowing-deliberation-review.md) (independent review, lodged 2026-04-25)

## Situation

The active spike suite was designed to improve on earlier spike failures by varying key auxiliaries before making any function-in-use claim:

- `005` varies profile construction.
- `006` varies retrieval method.
- `007` probes mechanism narratives before paying the cost of `008`.
- `008` is the first direct function-in-use test.

This structure is already more self-critical than the earlier spike program. It explicitly rejects winner-picking, binary verdicts, and unqualified extrapolation. But the suite also narrows aggressively:

- `005` constrains the framework families `006` is meant to treat as binding.
- `006` prunes the challenger set to a shortlist.
- `007` narrows that shortlist to at most two challengers for `008`.

That generates a live methodological question. Is this a responsible anti-regret sequence that reduces confounds before spending evaluation cost, or does it risk closing off still-interesting branches for procedural reasons while letting the resulting handoffs look more evidentially final than they are?

The deeper concern is not only about narrowing. It is about what the spikes can actually tell us. Each spike changes one or two parts of the comparison setup, but none of them can by itself license broad claims about "the right model," "the right architecture," or "what the product should expose." The conversation sharpened that we need stronger discipline around:

1. what each spike is allowed to conclude,
2. what would reverse or materially qualify its conclusion,
3. and which dropped or deferred branches are excluded by evidence versus by cost and sequencing.

### Evidence Base

| Source | What it shows | Corroborated? |
|--------|---------------|---------------|
| [METHODOLOGY.md](../spikes/METHODOLOGY.md) | The standing methodology already criticizes paradigm lock-in, auxiliary entanglement, evaluator monoculture, and overreach from representational evidence to functional claims | Yes |
| [SPIKE-DESIGN-PRINCIPLES.md](../spikes/SPIKE-DESIGN-PRINCIPLES.md) | The practical rules explicitly reject winner-crowning, binary verdicts, and unqualified closure | Yes |
| [NEXT-ROUND-SUITE.md](../spikes/NEXT-ROUND-SUITE.md) | The current suite deliberately narrows from full comparison to shortlist to at most two challengers for `008` | Yes |
| [005 HANDOFF.md](../spikes/005-evaluation-framework-robustness/HANDOFF.md) | `005` did not simply report findings; it constrained the frames `006` had to carry and weakened `Qwen3` by default | Yes |
| [006 HANDOFF.md](../spikes/006-model-retrieval-interactions/HANDOFF.md) | `006` converted retrieval findings into a family shortlist and explicitly blocked `007` from reopening the full model x retrieval space | Yes |
| [007 HANDOFF.md](../spikes/007-training-data-mechanism-probes/HANDOFF.md) | `007` narrowed `008` to `SPECTER2` and `Voyage`, but preserved a counter-reading in which `Stella` remained plausible | Yes |
| [2026-04-16-next-round-suite-execution-readiness-review.md](../spikes/reviews/2026-04-16-next-round-suite-execution-readiness-review.md) | The suite was judged structurally ready, but the review still warned that later artifacts could overclaim if they ignore the bounded language in the designs | Yes |
| Conversation on 2026-04-16 | The user explicitly pressed on regret, premature closure, challenge-seeking design, and whether the suite's stance is genuinely post-verificationist / post-falsificationist | Yes |

## Framing

The issue is not whether the suite should narrow at all. Some narrowing is necessary if `008` is to remain tractable. The issue is whether the narrowing logic is epistemically disciplined enough.

**Core question:** How should a sequential spike suite preserve challenge-seeking and anti-regret discipline while still narrowing the active branch set, and what kind of claims is each spike legitimately allowed to support?

**Adjacent questions:**

- When is a branch excluded by evidence, and when is it merely deferred by cost or sequencing?
- How much adversarial or reversal-oriented design is enough before a narrowing decision becomes warranted?
- What should count as a legitimate takeaway from a spike: a ranking, a bounded local claim, a posterior shift, or only a handoff condition?
- How should the suite record what it did not test, could not test, or intentionally postponed?

## Analysis

### Option A: Keep the current suite logic and rely on existing caveats

- **Claim:** The current suite is already sufficiently anti-regret because it varies major auxiliaries before allowing the expensive function-in-use stage.
- **Grounds:** `005` checks framework dependence, `006` checks retrieval dependence, `007` checks mechanism support, and `008` is deliberately delayed until later. The handoff files also record some counter-readings and deferrals.
- **Warrant:** If major confounds are addressed in sequence and the handoffs preserve bounded language, the current narrowing is justified enough.
- **Rebuttal:** This relies too heavily on good interpretive behavior at closeout time. The suite has bounded language, but it does not yet force each spike to say what would reopen a deferred branch or what its conclusion cannot settle.
- **Qualifier:** Better than the earlier spike program, but not quite enough.

### Option B: Hold more branches open longer and widen `008`

- **Claim:** The suite should be more regret-averse by carrying more candidates longer, possibly allowing three or four challengers into `008`.
- **Grounds:** Sequential narrowing can overfit to the particular probes chosen in `005`-`007`. A wider `008` would reduce the risk of dropping a functionally valuable challenger too early.
- **Warrant:** Since function-in-use is the real test, pruning before that stage may remove precisely the branch that matters most there.
- **Rebuttal:** This weakens the whole point of the sequence. `008` is the most expensive stage, and widening it too early would collapse the distinction between "screening" and "functional evaluation." It also risks making `008` itself too noisy and underinterpretable.
- **Qualifier:** Useful as a caution against over-pruning, but too blunt as the default.

### Option C: Keep sequential narrowing, but require an explicit challenge surface

- **Claim:** The suite should keep its current structure, but every spike should explicitly state the challenge surface around its conclusions.
- **Grounds:** The current artifacts already preserve some of this information informally in `Counter-Reading`, `Still Ambiguous`, and `Downstream Obligations`, but not in a systematic way.
- **Warrant:** A named challenge surface would preserve reversibility without forcing the suite to keep every branch live operationally.
- **Rebuttal:** This adds another artifact burden and could become formulaic if written perfunctorily.
- **Qualifier:** The best immediate improvement if kept short and operational.

### Option D: Replace narrowing with a more explicitly exploratory program

- **Claim:** The suite should abandon the current staged narrowing and instead treat the entire round as exploratory characterization without downstream exclusion.
- **Grounds:** The current suite is already philosophically suspicious of winner-picking and overclaiming. A more exploratory program would better match that stance.
- **Warrant:** If the main epistemic risk is premature closure, the safest remedy is to refuse closure until much later.
- **Rebuttal:** This throws away useful structure. It would make the suite less able to allocate effort, less able to state handoff obligations, and more vulnerable to diffuse accumulation of artifacts without any decision pressure.
- **Qualifier:** Too anti-closure to remain practical.

## Tensions

1. **Reversibility vs tractability**
   Preserving every branch reduces regret risk but can make the expensive final test impossible to run cleanly.

2. **Challenge-seeking vs endless reopening**
   A serious research program should design tests that might materially qualify prior findings, but if every result immediately reopens the full space then no sequence can ever narrow responsibly.

3. **Bounded claims vs narrative drift**
   The suite's methodology is already modest in principle, but closeout artifacts can still drift from "this test shifted a posterior under these conditions" toward "this family is the one that matters."

4. **Evidence-based exclusion vs cost-based deferral**
   The current suite sometimes excludes branches because the evidence weakened them, and sometimes because later stages need a smaller set. Those are not the same thing and should not be allowed to blur together.

5. **Post-verificationist intent vs residual eliminativism**
   The suite rejects naive confirmation and naive falsification, but its practical sequencing still uses eliminative gates. The question is how to keep those gates from masquerading as stronger epistemic closure than they deserve.

## Recommendation

**Current leaning:** Option C.

The current suite does not need to be reopened structurally right now. Its narrowing logic is good enough to continue. But future spikes, and the closeout of this suite, should adopt a first-class `challenge surface` discipline.

### Proposed `challenge surface` section

Each spike `FINDINGS.md`, `POSTERIOR.md`, or `HANDOFF.md` should include a short section answering:

1. **What result would materially reverse or qualify this conclusion?**
2. **Which live alternative remains excluded mainly by cost or sequencing, not by strong evidence against it?**
3. **Which branch was actually weakened by evidence, and by what specific evidence?**
4. **What does this spike not legitimately tell us?**
5. **Under what conditions should a dropped or deferred branch be reopened later?**

### Why this helps

- It makes the anti-regret logic explicit instead of merely implied.
- It distinguishes evidence-based narrowing from operational narrowing.
- It fits the suite's existing Bayesian / auxiliary-aware posture without requiring a redesign of the whole program.
- It preserves the trace of excluded possibilities without forcing the active branch set to explode again.

### What this would have clarified in the active suite

- `005 -> 006`: `Qwen3` was weakened by evidence, but the `SPECTER2`-refined frame was mostly deferred by sequencing.
- `006 -> 007`: `Qwen3` was evidence-weakened; `Stella` remained live but unstable; `MMR` and configuration-level reopening were deferred mainly by tractability.
- `007 -> 008`: `Stella` was not shown worthless; it lost the `008` slot because the suite prioritized mechanism-backed narrowing, and that choice should remain explicitly contestable.

## Provisional Conclusion

`[chosen for now]` The current spike suite is neither naively verificationist nor naively falsificationist. It is better described as a bounded, fallibilist, auxiliary-aware sequential program that still contains residual closure pressure. That pressure is not fatal, but it should be made more explicit and more revisable.

`[chosen for now]` The next methodological patch should therefore not be "abolish narrowing" or "widen every later spike." It should be to require every narrowing step to carry its own challenge surface and inference-limit statement, so the suite records not just what it chose, but what remained contestable and why.

> **Status note (2026-04-25):** The two `[chosen for now]` claims above are preserved as a record of what was concluded on 2026-04-16. They have since been re-examined; see the *Review and Status Update* section below. They should not be treated as binding for the next handoff or for `008`.

## Review and Status Update — 2026-04-25

A review of this deliberation was written nine days after it was filed: [2026-04-16-sequential-narrowing-deliberation-review.md](./reviews/2026-04-16-sequential-narrowing-deliberation-review.md).

### What the review found

The framing is mostly right, the conclusion is directionally right but procedurally understrength. Specifically:

- **The Option A-D space is constructed.** A and C differ only in artifact discipline; B and D differ only in degree of closure-aversion. Alternatives that are not represented include parallel rather than sequential narrowing, criterion-triggered reopening, and explicit auxiliary-bundle freeze statements. The space was drawn in a way that makes Option C the only sensible answer.
- **"Challenge surface" is documentation, not mechanism.** A prose section saying a branch *could* be reopened does not create a process that *actually reopens* it. Without a trigger, the section is epistemic insurance paperwork.
- **The philosophy is mobilised as atmospherics.** Mayo, Duhem-Quine, Lakatos, and van Fraassen are named but the actual recommendation does not draw on their machinery (severity arguments, auxiliary-bundle disclosure, progressive-vs-degenerating shifts, empirical adequacy at the bounded scope tested).
- **The deliberation does not apply its own discipline to itself.** It never asks what would reverse its own recommendation.
- **"Anti-regret" does unexamined work.** Decision-theoretic regret presumes enumerable branches and priceable losses that spike work does not have cleanly. "Reversibility budget" or "commitment debt" would be more honest.
- **No concrete failure mode anchors the analysis.** The argument is doctrinal rather than risk-anchored.

The review proposes a richer remedy set: challenge surface (prose) + pre-registered reopening trigger per narrowing step (mechanism) + auxiliary-bundle freeze statement (Duhem-Quine operationalised) + an `[evidence-weakened] / [cost-deferred] / [both]` decision tag on every excluded branch.

### Decision: pressure the artifacts before adopting any remedy

Selecting a remedy now — whether the original Option C, the review's expanded set, or any blend — would repeat the original mistake the review identifies: choosing a patch from a constructed option space without anchoring in concrete failure modes present in the existing handoffs.

State of the suite at time of pressure pass: `005` / `006` / `007` are complete (`DECISION` / `FINDINGS` / `HANDOFF` / `POSTERIOR` / `QUALITATIVE-REVIEW` present in each). `008` exists only as `DESIGN.md` + `TASK-MATRIX.md` and has not been run. `005-next-round-suite/` and `NEXT-ROUND-SUITE.md` exist at the spikes root, so a "next wave" frame is already present in the program independent of `008`. This means the pressure pass is not only a closeout / discipline question — it feeds a real, multi-dimensional design decision.

The next move is therefore neither (a) implement Option C as written, nor (b) implement the review's expanded remedy. It is:

1. **Pressure-test the `005` / `006` / `007` `HANDOFF.md` artifacts** by running diagnostic questions against them as a read-and-annotate pass. The pass produces a separate artifact (per-handoff annotations or a single `HANDOFF-PRESSURE.md`) that records findings without overwriting the handoffs themselves. The handoffs are evidence; pressuring them must not destroy the evidence.

   The pass scope also includes `NEXT-ROUND-SUITE.md` and `008/DESIGN.md`. If pressure-pass findings reshape `008`, they likely reshape the next wave too, and the next wave is partially designed already, so reshaping it cheaply is possible *now*. Reading these artifacts in the same pass keeps cross-wave effects visible rather than serialising them.

   Diagnostic questions, per handoff:
   - Which exclusions are evidence-weakened, which are cost-deferred, which are both? Tag them retrospectively and note where the classification resists clean assignment.
   - What would actually reopen each excluded branch? Write the trigger as if it had to fire. If it cannot be written concretely, the branch is closed in practice regardless of bounded language.
   - Which auxiliary bundle was held fixed? List it. Note whether the list is short and namable or sprawling and implicit.
   - Where does the prose drift from "posterior shift under conditions" toward "family that matters"? Mark the sentences.
   - What does this handoff *not* legitimately tell us?
   - **Redesign signal:** Which excluded branch, if reclassified from `[evidence-weakened]` to `[cost-deferred]` (or to `[both]`) by the pressure pass, would force `008` to be redrawn rather than merely augmented? Which would force `005` / `006` / `007` to be retroactively patched? Which would touch `NEXT-ROUND-SUITE.md`? Which would touch `METHODOLOGY.md` or `SPIKE-DESIGN-PRINCIPLES.md`? Which touch nothing local but warrant an ADR amendment?

   For each finding, the pass annotation should name *which cells in the response space below the finding actuates.* This keeps the response space honest instead of pre-collapsed into binaries.

2. **Use what surfaces** to compose a response from the multi-dimensional space below, rather than from a flat list of pre-named alternatives.

   **Dimensions of response:**

   | Dimension | Range |
   |---|---|
   | **Subject** | `008` itself · the pre-`008` chain (`005` / `006` / `007` retroactively, or a `007.5`) · the post-`008` plan (`NEXT-ROUND-SUITE.md`) · methodology layer (`METHODOLOGY.md`, `SPIKE-DESIGN-PRINCIPLES.md`) · artifact discipline (templates, decision-tag standards, deferred-branch registry) · the deliberations themselves · the interpretation layer (how findings reach product / architecture / ADRs) |
   | **Nature** | augment · narrow · widen · split · reorder · replace · reframe · defer · abandon · retroactively patch |
   | **Trigger** | evidence reversal · auxiliary-bundle gap · interpretive drift · cost reassessment · goal drift · methodological discovery |
   | **Scope of effect** | local to a spike · local to the wave · cross-wave (program) · cross-program (project — touches ADRs) |

   Branches are products of these dimensions, not a flat list. A non-exhaustive sample of live combinations the pass may actuate, beyond the obvious "augment `008` with discipline" and "redraw `008` from scratch":

   - **Retroactively patch `005` / `006` / `007`** with new tags and a `[reopened]` annotation, before `008` is touched. Subject: pre-`008` chain. Nature: retroactively patch. Trigger: evidence reversal.
   - **Insert a `007.5`** — small targeted probe addressing the highest-impact failure mode the pass surfaces (typically: one auxiliary not previously varied), shoring up the narrowing premise before `008` rides on it.
   - **Split `008`** into a confirmatory mechanism-backed test plus a cheap reopening probe on a branch the pass rehabilitates (e.g., `Stella`-under-rerank). Two postures rather than one.
   - **Run `008` plus a counter-`008` in parallel** — one tests the narrowing, one deliberately tests an excluded branch. The program produces two postures rather than one.
   - **Defer `008` indefinitely** with conditions for revisit registered. The narrowing premise is shaky enough that running the expensive test now would burn budget on contestable inputs.
   - **Abandon `008`** — premise unrecoverable; reallocate cost to a different question.
   - **Replace `008` with a different *kind* of test** answering the same question — e.g., function-in-use via longitudinal observation or live triage rather than offline evaluation. Same question, different epistemic regime.
   - **Reframe the question** — pass reveals "which family wins" was always the wrong frame; the right question is about composition or stack discipline, and `008` is replaced with a test of a different question.
   - **Modify only the methodology, not the spikes** — `METHODOLOGY.md` and `SPIKE-DESIGN-PRINCIPLES.md` get new discipline (auxiliary-bundle freeze, decision tags, reopening-trigger requirement); `008` runs as designed because no specific finding contests its premise.
   - **Modify only the artifact discipline** — handoff templates change, registries get added, spikes don't.
   - **Convert `008` from confirmatory to exploratory** — same setup, stance change. No winner-picking output, no narrowing handoff. A change in epistemic posture rather than scope.
   - **Pre-register a reopening protocol** that fires after `008` runs as designed — discipline added, scope unchanged, commitment debt bounded in advance.
   - **Modify only `NEXT-ROUND-SUITE.md`** — `008` is fine on its own terms; what changes is what comes after.
   - **Modify the deliberation itself** — the deliberation's option space was the wrong space; rewrite or supersede, with no direct effect on any spike.
   - **Spawn a parallel exploratory program** — fork, not continue, not abandon.
   - **Cross-program effect** — pass findings warrant an ADR amendment (e.g., touching `ADR-0001` exploration-first, or `ADR-0002` lazy enrichment, in this region of the design space).

   Some compose (retroactive patch of `005`-`007` + `008` augmented + new templates + amended `NEXT-ROUND-SUITE.md`). Some are mutually exclusive (abandon vs. augment). The right response is rarely a single cell.

3. **Then return here** and compose the actual response — incorporate Option C as originally written, adopt the review's expanded set, write a follow-up deliberation grounded in the artifacts, or some combination drawn from the dimensional space above. The choice is made *against evidence from the handoffs* rather than from doctrine.

### Status of original recommendation

The original Provisional Conclusion (Option C with a challenge-surface section) is **deferred, not rejected.** It may still be the right answer, in whole or in part, after the pressure pass. But it should be chosen against evidence from the artifacts rather than from the constructed option space the deliberation originally drew.

### Status of this deliberation

**Open — recommendation deferred pending artifact pressure pass.** The pass is the next concrete move; until it is run, neither this deliberation nor its review should be treated as having settled the question.

### Self-application note

The dimensional reframing above is also a self-application of the review's critique to the addendum's own first draft, which initially compressed the post-pressure response into "run as planned, run with added discipline, or reshape `008`." That was the same constructed-option-space mistake at smaller scale. The dimensional table is the corrected frame; if a future addition to this addendum collapses it again, that collapse should itself be flagged.
