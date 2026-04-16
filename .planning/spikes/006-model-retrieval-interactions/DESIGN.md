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

## Prior Credence And Update Target

- `[chosen for now]` Prior `P(H3) = 0.75`

This spike should shift that prior upward if centroid vs `kNN-per-seed` materially changes the comparative classification of multiple live model families or changes which candidates deserve to move forward. It should shift the prior downward if the comparative picture remains stable across retrieval methods once 005's framework variation is accounted for.

## Chosen For Now

1. The core comparison is **centroid vs kNN-per-seed**.
   `MMR` is deferred unless centroid/kNN results are too ambiguous to interpret.

   `kNN-per-seed` means the Spike 003 operator, not a fresh variant:
   - retrieve each seed's top `k_per_seed = max(5, ceil(K / n_seeds) + 2)` neighbors,
   - union the candidate sets,
   - rank by best cosine score to any seed,
   - break ties by mean score across nominating seeds, then by number of seed nominations.

2. Run on the **full model set** from Spike 004.
   The point here is to discover whether the apparent clusters from the pre-spike matrix survive retrieval variation.

3. Run on the **frameworks named in the 005 handoff**.
   - `MiniLM`-derived remains the default carried-forward frame.
   - If 005 shows that one alternative profile family materially changed a comparative classification or the second-view story, 006 must include that alternative frame too.
   - If 005 shows no material inversion, 006 may stay on the incumbent frame only and must say so explicitly.

4. 006 must not end in a vague "shortlist." It must classify each model family as:
   - `carry forward`
   - `drop for now`
   - `ambiguous / needs later functional test`

## Experimental Shape

### Phase 1: Implement kNN for every model family

- Add kNN-per-seed retrieval for `SPECTER2`, `Stella`, `Qwen3`, `GTE`, and `Voyage`.
- Preserve identical candidate-pool and exclusion rules across models.

### Phase 2: Run the cross-product

- Model x retrieval method x profile family
- Report subset-aware distributions, not single-seed outcomes
- Report complementarity against the incumbent `MiniLM + TF-IDF` arrangement, not only pairwise model similarity

### Phase 3: Mandatory qualitative review

- Review the profiles where centroid and `kNN-per-seed` change a model's comparative classification or complementarity story.
- Specifically inspect cases where `kNN-per-seed` appears to help because it adds papers, to distinguish genuinely useful different papers from fragmentation already seen in Spike 003.
- If a model looks promising under only one retrieval method, the qualitative review must say whether that looks like a viable niche or a retrieval artifact.

### Phase 4: Interaction synthesis and 007/008 handoff

- Identify models whose apparent strengths depend on retrieval method
- Identify models whose comparative behavior is retrieval-stable
- Use the interaction results to build a shortlist for the later, more expensive spikes
- The shortlist must be capped at **four model families or concrete configurations**.
- Entry requires at least one of:
  - retrieval-stable distinctness,
  - retrieval-stable complementarity against `MiniLM + TF-IDF`,
  - or a high-consequence centroid/kNN disagreement that later spikes are needed to resolve.
- A family should be marked `drop for now` if its apparent value appears only under one retrieval method and the qualitative review reads the difference as noise or fragmentation.

## Success Criteria

1. Every Spike 004 challenger has both centroid and kNN outputs.
2. The spike produces an explicit interaction table: model, retrieval method, profile family, and whether the comparative story changed.
3. The spike produces an explicit complementarity table against `MiniLM + TF-IDF`.
4. The spike includes a mandatory qualitative review over every material centroid/kNN story change.
5. The output assigns each model family to `carry forward`, `drop for now`, or `ambiguous / needs later functional test`.
6. The output names a provisional shortlist of at most four model families or concrete configurations for Spikes 007 and 008.
7. Any shortlist is marked `[chosen for now]`, not settled.

## Guardrails

- Do not upgrade kNN merely because it increases diversity; diversity is not yet user value.
- Do not use one profile or one seed choice as the decisive case.
- If 005 shows strong framework dependence, interpret 006 within each framework family rather than averaging the issue away.
