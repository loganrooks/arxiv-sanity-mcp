---
question: "How does retrieval method interact with each model family's embedding geometry, and does that interaction change which models remain meaningfully distinct?"
type: comparative
status: drafted
round: 1
depends_on:
  - 005 (evaluation framework robustness)
  - H3 from HYPOTHESES-005.md
linked_references:
  - ../HYPOTHESES-005.md
  - ../SPIKE-DESIGN-PRINCIPLES.md
  - ../METHODOLOGY.md
  - ../004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md
---

# Spike 006: Model-Retrieval Interactions

## Question

When each model is evaluated under both centroid retrieval and kNN-per-seed retrieval, which comparative differences persist, which collapse, and which emerge only under one retrieval method?

## Why This Spike Now

The pre-spike matrix shows that challenger structure is not trivial, but Spike 004 still tested only centroid retrieval for the new models. That leaves a large ambiguity: some of the apparent model differences may really be model-by-retrieval interactions.

This spike stays cheap because it uses existing embeddings and does not yet require new evaluator infrastructure.

## Hypotheses Addressed

- **Primary:** `H3`
- **Secondary:** shortlist support for `H2` and `H5`

## Chosen For Now

1. The core comparison is **centroid vs kNN-per-seed**.
   `MMR` is deferred unless centroid/kNN results are too ambiguous to interpret.

2. Run on the **full model set** from Spike 004.
   The point here is to discover whether the apparent clusters from the pre-spike matrix survive retrieval variation.

3. Run on the **frameworks that survive Spike 005**.
   If 005 shows one alternative profile family materially changes rankings, 006 should compare at least:
   - the existing MiniLM-derived frame
   - one alternative frame that changed the picture

## Experimental Shape

### Phase 1: Implement kNN for every model family

- Add kNN-per-seed retrieval for `SPECTER2`, `Stella`, `Qwen3`, `GTE`, and `Voyage`.
- Preserve identical candidate-pool and exclusion rules across models.

### Phase 2: Run the cross-product

- Model x retrieval method x profile family
- Report subset-aware distributions, not single-seed outcomes
- Report complementarity against the incumbent `MiniLM + TF-IDF` arrangement, not only pairwise model similarity

### Phase 3: Interaction synthesis

- Identify models whose apparent strengths depend on retrieval method
- Identify models whose comparative behavior is retrieval-stable
- Use the interaction results to build a shortlist for the later, more expensive spikes

## Success Criteria

1. Every Spike 004 challenger has both centroid and kNN outputs.
2. The spike produces an explicit interaction table: model, retrieval method, profile family, and whether the comparative story changed.
3. The spike produces an explicit complementarity table against `MiniLM + TF-IDF`.
4. The output names a provisional shortlist of model families for Spikes 007 and 008.
5. Any shortlist is marked `[chosen for now]`, not settled.

## Guardrails

- Do not upgrade kNN merely because it increases diversity; diversity is not yet user value.
- Do not use one profile or one seed choice as the decisive case.
- If 005 shows strong framework dependence, interpret 006 within each framework family rather than averaging the issue away.
