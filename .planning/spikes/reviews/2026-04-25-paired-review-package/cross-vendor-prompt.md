---
type: review-prompt
audience: cross-vendor reviewer (GPT-class, Gemini-class, Grok, or other non-Anthropic AI)
phase: independent first reading + post-pressure-pass comparison
output_target: .planning/spikes/reviews/2026-04-25-pressure-pass-cross-vendor-review.md
---

# Cross-Vendor Review Prompt — Spike Suite Reading Conventions

## Your role

You are an independent second reader for a research project's spike methodology audit. Another reader (a Claude Opus model) has already produced a "pressure pass" on the project's spike handoffs. We want to know whether your independent reading of the underlying artifacts arrives at the same framing on two specific questions, *before* you see the pressure pass. This is a deliberate independence protocol — please respect it.

You will work in two phases:

1. **Phase 1: independent reading.** Read the underlying spike artifacts and answer two questions about reading conventions, without consulting the pressure pass.
2. **Phase 2: comparison.** Read the pressure pass, compare its framing to yours, and react.

Both phase outputs go in your response, clearly labeled.

## Project context (minimal — for vocabulary only)

- The project is an MCP-native research discovery substrate. Spikes are bounded experiments testing whether design choices (retrieval methods, embedding models, profile constructions) survive perturbation.
- Spikes 005 / 006 / 007 are complete. They form a sequential narrowing chain: 005 tests evaluation framework robustness, 006 tests model-retrieval interactions, 007 probes mechanism narratives. Each handoff selects survivors and defers or drops candidates.
- Spike 008 is designed but unrun. Its design says it will compare the incumbent (`MiniLM + TF-IDF`) plus two challengers (`SPECTER2` and `Voyage`), with `Stella` retained only as an operational fallback.
- The methodology values fallibilist, auxiliary-aware, post-verificationist reasoning. Bounded language and challenge-seeking design are explicit norms.

## Phase 1 — Independent reading

### Required reading order (artifacts only, in this order)

Do not read the pressure pass yet. Do not read the deliberation document. Read these and only these:

1. `.planning/spikes/METHODOLOGY.md` — working vocabulary
2. `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md` — explicit norms
3. `.planning/spikes/NEXT-ROUND-SUITE.md` — suite contract
4. `.planning/spikes/HYPOTHESES-005.md` — hypothesis priors carried into the suite
5. `.planning/spikes/005-evaluation-framework-robustness/HANDOFF.md`
6. `.planning/spikes/006-model-retrieval-interactions/HANDOFF.md`
7. `.planning/spikes/007-training-data-mechanism-probes/HANDOFF.md`
8. `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md`

You may also skim `FINDINGS.md`, `POSTERIOR.md`, `DECISION.md`, or `QUALITATIVE-REVIEW.md` from any of the 005/006/007 directories if needed for context. **Do not read** `.planning/deliberations/` or `.planning/spikes/reviews/` yet.

### Questions to answer in Phase 1

Answer each question with: (a) your independent reading, (b) specific textual evidence from the artifacts, (c) confidence level (low / medium / high).

**Question A — Mechanism-support as gate criterion.**

`007/HANDOFF.md` selects `SPECTER2` and `Voyage` as the carried challengers and defers `Stella`. The Counter-Reading section explicitly says: "Stella should have claimed an 008 slot because it had the strongest 006 complementarity score. I am not choosing that reading because 007 was supposed to narrow on mechanism-backed reasons to keep paying evaluation cost."

So `007` chose to weight *mechanism-backed support* over *complementarity score* as the narrowing criterion.

- A1. Is this weighting (mechanism-support over complementarity) explicitly justified anywhere in the chain — in `005`, `006`, `NEXT-ROUND-SUITE.md`, `METHODOLOGY.md`, or `SPIKE-DESIGN-PRINCIPLES.md`? If so, where?
- A2. Reading the artifacts as a careful but uninitiated reader: would you treat this weighting as a *contested choice* (one of multiple defensible criteria, picked at this step), or as an *implicit best practice* (the obvious narrowing criterion that the methodology's epistemic posture would have endorsed in advance)?
- A3. Does it matter for the validity of `008`'s narrowing? Specifically: if a reader judged the weighting to be a contested choice, would `008`'s "two challengers and `Stella` as fallback" structure still be epistemically warranted, or would it be partly hostage to that contested choice?

**Question B — Family vs configuration as unit of analysis.**

`005` evaluates model families across alternative profile families. `006` evaluates centroid vs `kNN-per-seed` per model family, and its Counter-Reading flags that `kNN`'s near-universal union gains might warrant carrying *method-specific configurations* rather than model families. `007` narrows on family. `008/DESIGN.md` says the spike compares "configurations" but names them as `MiniLM + TF-IDF`, `SPECTER2`, `Voyage` — which mixes a configuration (model + retrieval) with two family names.

- B1. Is the unit of analysis (family vs specific configuration) consistently defined across the chain? Where is it defined explicitly, and where (if anywhere) does it shift?
- B2. Does `008/DESIGN.md` carry a substantive commitment about whether the answer to its question — "which configurations actually help research tasks" — is a family-level claim or a configuration-level claim? Or is the design ambiguous on this?
- B3. Reading the chain as a careful but uninitiated reader: is the family-vs-configuration distinction (a) substantively addressed and resolved, (b) substantively addressed and explicitly deferred, or (c) elided / unaddressed?

### Phase 1 output format

```
## Phase 1 — Independent reading

### Question A — Mechanism-support as gate criterion

**A1 (where, if anywhere, is the weighting justified):**
[your reading + textual evidence + confidence]

**A2 (contested choice or implicit best practice):**
[your reading + reasoning + confidence]

**A3 (consequences for 008):**
[your reading + reasoning + confidence]

### Question B — Family vs configuration

**B1 (consistency of unit definition):**
[your reading + textual evidence + confidence]

**B2 (008's commitment):**
[your reading + reasoning + confidence]

**B3 (resolved / deferred / elided):**
[your reading + reasoning + confidence]

### Anything else you noticed

[optional: framing claims you would have raised that are not in Findings 1 or 2]
```

**Stop here. Do not yet read the pressure pass.**

## Phase 2 — Comparison

After completing Phase 1, read:

- `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md` — the pressure pass, especially Findings 1 and 2 in the Cross-artifact synthesis section.

Then answer:

- C1. Does the pressure pass's framing of Finding 1 (mechanism-support > complementarity is a load-bearing stance choice that is not labeled as one) match, qualify, or contradict your Phase 1 reading? If it qualifies or contradicts, name the specific point of difference.
- C2. Same for Finding 2 (configuration-vs-family slippage runs through the whole chain).
- C3. Does the pressure pass overstep on any specific claim — language that draws more than the textual evidence supports? Quote the sentence(s) and explain.
- C4. Does the pressure pass *understate* anything — is there a stronger version of either finding that the textual evidence supports and the pass did not name?

### Phase 2 output format

```
## Phase 2 — Comparison

**C1 — Finding 1 framing:**
[match / qualify / contradict — with specifics]

**C2 — Finding 2 framing:**
[match / qualify / contradict — with specifics]

**C3 — Overstep:**
[any sentences that overstep, with quotes]

**C4 — Understate:**
[any stronger versions the evidence supports]

## Bottom line

[one paragraph: net effect of your reading on Findings 1 and 2 — survive as stated, survive with qualification, retract]
```

## Norms for this review

- **Disagreement is welcome.** This package exists because we suspect single-reader framing claims may be unreliable. If you read the artifacts and Findings 1 or 2 are wrong, say so directly.
- **Independence is the point.** Do not read the pressure pass before completing Phase 1. Do not consult the deliberation document at all unless your final response benefits from a single targeted check.
- **Quote the artifacts.** Specific textual evidence is more useful than general impressions.
- **Calibrated confidence.** It is fine to say "low confidence — the artifacts do not address this clearly enough for me to judge."
- **No silent extrapolation.** If you are extrapolating beyond what the artifacts say, name it as extrapolation.
