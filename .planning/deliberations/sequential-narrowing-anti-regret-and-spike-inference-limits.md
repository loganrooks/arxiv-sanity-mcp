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
**Status:** Open
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
