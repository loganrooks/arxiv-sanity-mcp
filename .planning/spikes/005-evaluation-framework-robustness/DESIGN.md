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

## Chosen For Now

1. Compare **three profile-construction families**:
   - existing `MiniLM`-derived profiles
   - `category`-derived profiles
   - one challenger-derived profile family, with `SPECTER2` as the first choice and `GTE` as fallback if `SPECTER2` clustering proves operationally unusable

2. Run the comparison across **all 8 existing profiles** if possible.
   If full reconstruction across all 8 is too brittle, do not silently narrow to an arbitrary subset. Fall back to a declared representative set containing at least `P1`, `P3`, `P5`, `P7`, and `P8`.

3. Keep the evaluation question thin:
   this spike is about **ranking robustness under framework variation**, not about user value and not about architecture closure.

## Experimental Shape

### Phase 1: Build alternative profile families

- Produce category-derived profiles that do not depend on any embedding model.
- Produce one challenger-derived profile family from a non-MiniLM model.
- Record where human judgment was needed in the profile-construction process.

### Phase 2: Re-run the current comparison frame

- Use the same recommendation generation and metric family as Spike 004 where possible.
- Compare all systems under each profile-construction family.
- Preserve subset-aware reporting; do not collapse to one seed choice.

### Phase 3: Robustness synthesis

- Identify findings that are stable across profile-construction families.
- Identify findings that invert or weaken materially when the framework changes.
- Separate "framework-robust" from "framework-dependent" claims explicitly.

## Success Criteria

1. At least three profile-construction families are evaluated or one failed family is explicitly replaced with a justified fallback.
2. The spike produces a table of ranking changes across profile families for every system.
3. The output explicitly states which Spike 004 findings survive framework variation and which do not.
4. No system is promoted or demoted architecturally on the basis of this spike alone.

## Guardrails

- Do not compare only against MiniLM; preserve model-to-model visibility.
- Do not treat agreement across frameworks as proof of researcher value; it only improves trustworthiness.
- If alternative profile construction requires choices that materially shape results, those choices must be reported as `[chosen for now]`, not as settled.
