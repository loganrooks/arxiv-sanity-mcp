---
date: 2026-03-30
status: complete
scope: pre-spike analyses run on existing Spike 004 assets to sharpen next-round design
artifacts:
  - artifacts/pairwise-tau-matrix.json
  - artifacts/seed-sensitivity.json
  - artifacts/tfidf-complementarity.json
sources:
  - ../004-embedding-model-evaluation/experiments/checkpoints/phase2_metrics.json
  - ../004-embedding-model-evaluation/experiments/checkpoints/phase2_classification.json
  - ../004-embedding-model-evaluation/experiments/data/*.npy
  - ../003-strategy-profiling/experiments/data/interest_profiles.json
---

# Pre-Spike Analyses for the Next Spike Round

These analyses were run on the checked-in Spike 004 sample embeddings and the existing interest-profile assets. Their purpose is not to settle architecture. Their purpose is to sharpen the next suite so it tests the highest-leverage uncertainties first.

## Methodological scope

- **Artifact-reported**: all three analyses use repo-local assets only.
- **Artifact-reported**: pairwise model comparison uses the 2000-paper sample embeddings already produced in Spike 004.
- **Artifact-reported**: complementarity analysis uses the same sample and the same TF-IDF construction used in Spike 004 Phase 2.
- **Artifact-reported but limited**: seed-sensitivity uses the seed variants explicitly available in `interest_profiles.json`.
- **Open**: the repo-local seed assets do not encode the full "five fixed-5-seed variants" language mentioned in the March 30 checkpoint. The formal sensitivity characterization below is therefore bounded by the assets we can actually trace in-repo.

## Analysis 1: Model-to-model pairwise tau matrix

### Artifact-reported results

Lowest mean pairwise taus across profiles and checked-in 5-seed variants:

- `TF-IDF ↔ Voyage`: `0.3698`
- `TF-IDF ↔ SPECTER2`: `0.3774`
- `TF-IDF ↔ GTE`: `0.4182`
- `TF-IDF ↔ Qwen3`: `0.4338`
- `TF-IDF ↔ Stella`: `0.4377`
- `SPECTER2 ↔ Voyage`: `0.4518`
- `GTE ↔ Voyage`: `0.4815`
- `MiniLM ↔ TF-IDF`: `0.4661`
- `MiniLM ↔ Voyage`: `0.4834`
- `Qwen3 ↔ Voyage`: `0.5063`

Highest mean pairwise taus:

- `Qwen3 ↔ Stella`: `0.6866`
- `MiniLM ↔ Stella`: `0.6420`
- `GTE ↔ Stella`: `0.6335`
- `MiniLM ↔ GTE`: `0.6319`

### Interpretation

- **Derived**: Voyage is not merely "another challenger to MiniLM." It is also the most orthogonal model relative to the other challengers.
- **Derived**: TF-IDF remains one of the most orthogonal signals in the full matrix, especially relative to `Voyage` and `SPECTER2`.
- **Derived**: Qwen3, Stella, GTE, and MiniLM occupy a more tightly related neighborhood than Voyage does.
- **Derived**: SPECTER2 remains a structurally distinct comparison target. It is not interchangeable with the "general semantic" cluster, and it is also not especially close to Voyage.
- **Chosen for now**: the next suite should reason about at least three comparison families, not a single challenger family:
  - `MiniLM / Stella / GTE / Qwen3` as a more correlated semantic family
  - `SPECTER2` as a distinct scientific-community-style family
  - `Voyage` as a distinct broad-semantic/API family
  - `TF-IDF` as the lexical baseline whose structural distinctness still has to be beaten, not assumed away

## Analysis 2: Seed sensitivity characterization

### What was actually measured

Two variant sets were available in-repo:

1. **Checked-in 5-seed variants**
   - `seed_papers_first5`
   - `subset_5`
   - `subset_10_first5`
   - `subset_15_first5`

2. **Explicit seed-count variants**
   - `subset_5`
   - `subset_10`
   - `subset_15`

The first set isolates multiple checked-in 5-seed choices. The second mixes seed membership and seed count. Both are informative; neither should be mistaken for a complete fixed-K robustness study.

### Artifact-reported results

Across the checked-in 5-seed variants:

- `J@20` remains much more volatile than tau on most profile/model pairs.
- The largest `J@20` ranges were:
  - `Voyage / P1`: `0.3048`
  - `Qwen3 / P6`: `0.2667`
  - `Stella / P1`: `0.2576`
  - `SPECTER2 / P3`: `0.2207`
- The largest tau ranges were:
  - `SPECTER2 / P3`: `0.0864`
  - `GTE / P3`: `0.0837`
  - `Qwen3 / P5`: `0.0659`
  - `Voyage / P3`: `0.0656`

Strongest instability profiles by model:

- `P3 (Quantum)` is the strongest tau-instability profile for `SPECTER2`, `GTE`, and `Voyage`.
- `P1 (RL for robotics)` is the strongest `J@20` instability profile for `Stella`, `GTE`, and `Voyage`.
- `P6 (Diffusion)` is the strongest `J@20` instability profile for `Qwen3`.

### Interpretation

- **Derived**: seed sensitivity is profile-specific, not uniform across the evaluation set.
- **Derived**: `J@20` remains the less stable instrument, but tau is not invariant under the checked-in variant set either.
- **Open**: because the repo-local variants are not a pure fixed-K family, we still do not have a definitive answer to "how stable are findings under fixed-size seed replacement alone?"
- **Chosen for now**: the next suite should treat seed variation as a design variable in its own right rather than a post-hoc caveat.

## Analysis 3: `MiniLM + challenger` vs `MiniLM + TF-IDF`

### Artifact-reported aggregate result

At `K=20`, none of the challengers clearly beats `MiniLM + TF-IDF` on aggregate union size:

- `Qwen3`: mean union delta vs TF-IDF `0.0`
- `Stella`: `-0.375`
- `SPECTER2`: `-1.0`
- `Voyage`: `-1.25`
- `GTE`: `-1.5`

At `K=100`, all challengers are worse on mean union size than `MiniLM + TF-IDF`.

### Artifact-reported profile-level wins and losses

Profiles where challengers beat `MiniLM + TF-IDF` on `K=20` union size:

- `P1`: `Qwen3 (+3)`, `GTE (+1)`
- `P3`: `SPECTER2 (+4)`, `Stella (+3)`, `Voyage (+2)`, `Qwen3 (+1)`
- `P6`: `Qwen3 (+2)`, `Stella (+1)`
- `P7`: `Stella (+2)`, `Qwen3 (+1)`

Profiles where `MiniLM + TF-IDF` beats **all** challengers:

- `P2`
- `P4`
- `P8`

Mixed / tie profiles:

- `P5`: `SPECTER2` and `Voyage` tie TF-IDF on union size; others lose

### Category-match data

Challenger unions often have **higher seed-category match rates** than `MiniLM + TF-IDF`.

Examples:

- `SPECTER2` mean `K=20` union seed-category match rate: `0.8066`
- `Voyage`: `0.8160`
- `Stella`: `0.8127`
- `MiniLM + TF-IDF` baseline: `0.7618`

### Interpretation

- **Derived**: the question "better second view than TF-IDF?" still does not collapse to a global yes for any challenger.
- **Interpretive**: the right frame is profile-conditional and value-conditional, not global replacement.
- **Chosen for now**: the next suite should test challenger complementarity only on the profiles where challengers materially win or tie:
  - `P1`, `P3`, `P5`, `P6`, `P7`
- **Chosen for now**: `P2`, `P4`, and `P8` should serve as controls where TF-IDF remains the incumbent complement to beat.

## What these analyses change

### Settled for this design round

- The next suite should not ask only "how far is model X from MiniLM?"
- The next suite should preserve `MiniLM + TF-IDF` as the practical incumbent baseline.
- The next suite should explicitly separate:
  - framework robustness,
  - retrieval-method interaction,
  - function-in-use value.

### Chosen for now

- The next suite should be three spikes, not one omnibus spike:
  1. framework robustness first,
  2. retrieval/complementarity second,
  3. task-based value last.
- `P1`, `P3`, `P6`, and `P7` are the main discriminating profiles.
- `P2`, `P4`, and `P8` remain the most important control profiles for challenger claims.

### Open

- Whether the checked-in 5-seed variants are sufficient or whether a dedicated fixed-K seed generator should be built before any claims are made.
- Whether `Voyage` should remain in the execution-critical path or only as a cached comparison/control.
- Whether `Qwen3` and `Stella` are meaningfully distinct enough to both deserve full downstream task-based evaluation.

## Design consequence

The suite should not begin with agent tasks. It should begin by stress-testing the evaluation frame itself, because the pre-spike analyses show that both model relations and complementarity claims are still profile- and seed-sensitive.
