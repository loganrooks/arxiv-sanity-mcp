# Next Spike Suite

**Status:** drafted on 2026-03-30 after [PRE-SPIKE-ANALYSES.md](./004-embedding-model-evaluation/PRE-SPIKE-ANALYSES.md)

## Inputs From The Pre-Spike Analyses

1. **Pairwise structure is real, not just MiniLM hub-and-spoke.**
   The exhaustive pairwise matrix shows non-trivial structure across challengers: Stella and Qwen3 are the closest pair (`tau=0.681`), while SPECTER2 and Voyage are the farthest (`tau=0.444`). This means the next round should not assume "all challengers merely differ from MiniLM in the same way."

2. **Seed choice still destabilizes top-K narratives.**
   Across all 3,003 five-of-fifteen subsets per profile, `J@20`, `J@100`, and "additional papers" counts vary widely. The next round cannot treat per-profile top-K overlap or unique-paper counts as stable enough for architectural claims without explicit subset-aware reporting.

3. **`MiniLM + TF-IDF` still outcovers `MiniLM + SPECTER2` on current profiles.**
   Under the current MiniLM-derived profile frame, `MiniLM + TF-IDF` has the larger mean union at `K=20`, `K=50`, and `K=100`. This does not settle the second-view question, but it means the next round should not privilege SPECTER2 as the presumptive successor to TF-IDF.

## Chosen For Now

The next suite is a **four-spike sequence**:

1. **Spike 005: Evaluation Framework Robustness**
   Test whether the current findings survive alternative profile construction methods.

2. **Spike 006: Retrieval Geometry Interactions**
   Test whether centroid-vs-kNN interaction changes the comparative picture for each model family.

3. **Spike 007: Mechanism Probes For Shortlisted Model Families**
   Test whether the remaining differences are predictable from training-data and community-structure hypotheses.

4. **Spike 008: Function-In-Use And Blind-Spot Value**
   Test whether the remaining candidate configurations help actual research tasks and whether their "blind-spot" papers contribute to outputs.

## Why This Order

- **005 comes first** because profile-construction bias is the deepest threat identified in [OPEN-QUESTIONS.md](./004-embedding-model-evaluation/OPEN-QUESTIONS.md). If rankings invert under alternative profiles, every later spike must be read as framework-dependent.
- **006 comes second** because it is still cheap, uses existing embeddings, and may explain some of the observed model differences without yet invoking stronger causal stories.
- **007 comes third** because mechanism claims should only be tested after the framework and retrieval surfaces are more stable.
- **008 comes last** because task-based evaluation is the most expensive and should operate on a narrowed, better-justified candidate set.

## Shortlisting Rule

**Chosen for now:** Spikes 005 and 006 run on the full current comparison set. Spikes 007 and 008 run on a **shortlisted set of model families**, not every challenger, unless 005/006 show that collapsing to representatives would erase meaningful differences.

This is justified by the pre-spike matrix:
- `Stella` and `Qwen3` are very close to each other.
- `MiniLM` and `GTE` are also comparatively close.
- `SPECTER2` and `Voyage` remain the most structurally distinct challengers.

The shortlist itself remains **Open** until 005 and 006 complete.

## Open

- Whether the challenger-derived profile family in 005 should be `SPECTER2`-based, `GTE`-based, or both.
- Whether 006 should evaluate one or two profile-construction families after 005.
- Whether 008 can include even a small amount of human judgment rather than AI-only agent evaluation.
- Whether H2 remains a standalone spike after 005/006 or collapses into a narrower mechanistic appendix for the shortlisted candidates.

## Required Gate

Before any of Spikes 005-008 execute:
- an independent design critic must review the suite and each spike `DESIGN.md` against [SPIKE-DESIGN-PRINCIPLES.md](./SPIKE-DESIGN-PRINCIPLES.md) and [METHODOLOGY.md](./METHODOLOGY.md)
- any critique that identifies a Pattern A risk must be resolved structurally, not merely acknowledged in caveats
