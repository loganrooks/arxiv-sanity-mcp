---
question: "How much of the current model-ranking picture is an artifact of MiniLM-derived profile construction rather than a framework-independent difference?"
type: comparative
status: drafted
round: 1
depends_on:
  - 004 (embedding model evaluation)
  - 004 pre-spike analyses
  - H4 from HYPOTHESES-005.md
linked_references:
  - ../HYPOTHESES-005.md
  - ../SPIKE-DESIGN-PRINCIPLES.md
  - ../METHODOLOGY.md
  - ../004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md
---

# Spike 005: Evaluation Framework Robustness

## Question

If the interest profiles are reconstructed using different methods, do the relative rankings and divergences of `MiniLM`, `TF-IDF`, `SPECTER2`, `Stella`, `Qwen3`, `GTE`, and `Voyage` remain materially similar, or do the current findings turn out to be artifacts of MiniLM-derived profile boundaries?

## Why This Spike Now

This is the highest-leverage next experiment because it attacks the strongest unresolved assumption from Spike 004: the current profiles are MiniLM-entangled. The pre-spike analyses strengthened the need for this test in two ways:

- they showed real structure among challengers, which makes framework favoritism more consequential
- they showed `MiniLM + TF-IDF` still outcovers `MiniLM + SPECTER2` under the current profile frame, which means the second-view question remains open but still profile-dependent

## Hypotheses Addressed

- **Primary:** `H4`
- **Secondary:** the framework-dependent part of `H2`

## Prior Credence And Update Target

- `[chosen for now]` Prior `P(H4) = 0.80`
- `[chosen for now]` Prior `P(framework-dependent portion of H2) = 0.60`

This spike should shift those priors upward if alternative profile families materially change the comparative classifications of multiple model families or reverse the current second-view story. It should shift them downward if the main comparative picture remains stable across all three profile-construction families and the qualitative review sees the same kind of divergence rather than only the same metric deltas.

## Chosen For Now

1. Compare **three profile-construction families**:
   - existing `MiniLM`-derived profiles
   - `category`-derived profiles
   - one challenger-derived profile family, with `SPECTER2` as the first choice and `GTE` as fallback if `SPECTER2` clustering proves operationally unusable

2. Run the comparison across **all 8 existing profiles** if possible.
   If full reconstruction across all 8 is too brittle, do not silently narrow to an arbitrary subset. Fall back to a declared representative set containing at least `P1`, `P3`, `P5`, `P7`, and `P8`.

3. Keep the evaluation question thin:
   this spike is about **ranking robustness under framework variation**, not about user value and not about architecture closure.

4. For this spike, each model family must receive one comparative classification per profile family:
   - `near-redundant`
   - `distinct but not currently complementary`
   - `candidate complementary second view`
   - `blocked / unclear`

5. A Spike 004 comparative claim counts as **framework-robust** only if its classification stays unchanged in at least 2 of the 3 profile-construction families and no alternative family reverses it in the mandatory qualitative review. Claims that fail this test must be carried forward as framework-dependent, not averaged into a synthetic middle.

## Experimental Shape

### Phase 1: Build alternative profile families

- Produce category-derived profiles that do not depend on any embedding model.
- For the `category`-derived family, use metadata-only construction:
  - identify the smallest arXiv category set covering at least `80%` of the original seed-category mass,
  - form the candidate pool from papers in that category union,
  - and derive the profile seed set from lexical matching over the existing profile label plus seed titles/abstracts.
- This family is metadata-based at the representation layer, but it is still seed-anchored at the interest-definition layer and should be interpreted that narrowly.
- Produce one challenger-derived profile family from a non-MiniLM model.
- For the challenger-derived family, reuse the existing clustering / profile-construction pipeline with `SPECTER2` embeddings first and `GTE` only if `SPECTER2` proves operationally unusable.
- Record where human judgment was needed in the profile-construction process.

### Phase 2: Re-run the current comparison frame

- Use the same recommendation generation and metric family as Spike 004 where possible.
- Compare all systems under each profile-construction family.
- Preserve subset-aware reporting; do not collapse to one seed choice.

### Phase 3: Mandatory qualitative review

- For every profile family that changes a model's comparative classification, run a qualitative review of the affected recommendation deltas.
- Review the cases where a model becomes newly complementary, newly redundant, or meaningfully less coherent under a different profile family.
- If the qualitative review and the quantitative classification disagree, carry the disagreement forward explicitly rather than forcing a single verdict.

### Phase 4: Robustness synthesis and 006 handoff

- Identify findings that are stable across profile-construction families.
- Identify findings that invert or weaken materially when the framework changes.
- Separate "framework-robust" from "framework-dependent" claims explicitly.
- Produce a handoff note for Spike 006 naming:
  - which profile family remains the incumbent comparison frame,
  - whether an alternative profile family caused a material inversion and must be carried forward into 006,
  - and which model families are now `clearly live`, `clearly weakened`, or `still ambiguous`.

## Success Criteria

1. At least three profile-construction families are evaluated or one failed family is explicitly replaced with a justified fallback.
2. The spike produces a table of ranking changes across profile families for every system.
3. The spike includes a mandatory qualitative review pass over every material classification change.
4. The output explicitly states which Spike 004 findings are `framework-robust`, which are `framework-dependent`, and which remain `blocked / unclear`.
5. The output includes an explicit 006 handoff naming whether one or two profile-construction families must be carried forward.
6. No system is promoted or demoted architecturally on the basis of this spike alone.

## Required Durable Outputs

- `QUALITATIVE-REVIEW.md`
- `POSTERIOR.md`
- `HANDOFF.md`
- `FINDINGS.md`
- `DECISION.md`

Execution should follow [ITERATIVE-SPIKE-WORKFLOW.md](../ITERATIVE-SPIKE-WORKFLOW.md).

## Guardrails

- Do not compare only against MiniLM; preserve model-to-model visibility.
- Do not treat agreement across frameworks as proof of researcher value; it only improves trustworthiness.
- If alternative profile construction requires choices that materially shape results, those choices must be reported as `[chosen for now]`, not as settled.
