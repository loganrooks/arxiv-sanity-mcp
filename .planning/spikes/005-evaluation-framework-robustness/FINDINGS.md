---
status: complete
date: 2026-04-16
source_checkpoint: ./experiments/checkpoints/phase1_quantitative.json
qualitative_review: ./QUALITATIVE-REVIEW.md
---

# Spike 005 Findings

## Question

How much of the current model-ranking picture is an artifact of MiniLM-derived profile construction rather than a framework-independent difference?

## Main Findings

1. `[artifact-reported]` The quantitative pass produced **five family-induced classification changes** across the 15 challenger-family comparisons (`5 models x 3 profile families`). See [phase1_quantitative.json](./experiments/checkpoints/phase1_quantitative.json).

2. `[artifact-reported]` No challenger became newly `candidate complementary second view` under an alternative profile family. All observed classification changes moved in the opposite direction: from `candidate complementary second view` to `blocked / unclear`, or from `blocked / unclear` to `distinct but not currently complementary`.

3. `[artifact-reported]` `Qwen3` is the strongest framework-sensitive case.
   - Saved MiniLM family: `candidate complementary second view`
   - Category + lexical family: `blocked / unclear`
   - SPECTER2-refined family: `blocked / unclear`

4. `[artifact-reported]` `Stella` is the most stable case in this spike. It remained `blocked / unclear` under all three profile-construction families.

5. `[derived]` The observed framework effect is **asymmetric**. Alternative profile families weaken one positive candidate story (`Qwen3`) and push some challengers toward a more negative reading, but they do not produce a new second-view winner.

## Classification Matrix

| Model | Saved MiniLM family | Category + lexical family | SPECTER2-refined family |
| --- | --- | --- | --- |
| SPECTER2 | blocked / unclear | distinct but not currently complementary | blocked / unclear |
| Stella | blocked / unclear | blocked / unclear | blocked / unclear |
| Qwen3 | candidate complementary second view | blocked / unclear | blocked / unclear |
| GTE | blocked / unclear | blocked / unclear | distinct but not currently complementary |
| Voyage | blocked / unclear | distinct but not currently complementary | blocked / unclear |

## Quantitative Read

### Qwen3

- `[artifact-reported]` Under the saved MiniLM family, Qwen3 beat or matched the `MiniLM + TF-IDF` union benchmark on four profiles and had mean union delta `0.000`.
- `[artifact-reported]` Under the category + lexical family, the same quantity fell to mean union delta `-0.625` with only two profiles beating the benchmark.
- `[artifact-reported]` Under the SPECTER2-refined family, mean union delta was `-0.250`, again with only two profiles beating the benchmark.
- `[derived]` The strongest apparent positive Qwen3 story is not family-robust.

### SPECTER2, GTE, Voyage

- `[artifact-reported]` These three challengers each show one family-induced downgrade toward `distinct but not currently complementary`.
- `[artifact-reported]` None of the three becomes more positive under an alternative family.
- `[derived]` Framework variation can sharpen a negative read for these models, but the effect is weaker and less decisive than the Qwen3 reversal.

### Stella

- `[artifact-reported]` Stella stayed `blocked / unclear` across all three families.
- `[derived]` Stella's comparative ambiguity appears more stable than family-specific in this spike.

## Qualitative Read

The targeted changed-case review is in [QUALITATIVE-REVIEW.md](./QUALITATIVE-REVIEW.md). The short version is:

- `[derived]` The Qwen3 demotions are qualitatively supported. The changed-case papers remain mixed and reinforce the already-known noise sensitivity from Spike 004 rather than overturning it.
- `[derived]` The more negative SPECTER2 category-family read is also supported, but in a narrower sense: the family produces coherent technical papers alongside more obviously adjacency-driven drift, so the classification becomes less optimistic without becoming a failure case.
- `[derived]` The negative shifts for Voyage and GTE are weaker qualitatively than they are quantitatively. They look more like "not promoted" than like decisive evidence against complementarity.

## Bounded Conclusion

- `[derived]` Spike 005 does **not** show that the entire Spike 004 picture was a MiniLM artifact.
- `[derived]` Spike 005 **does** show that at least one apparently live second-view candidate (`Qwen3`) depends materially on how the evaluation frame constructs the underlying profiles.
- `[chosen for now]` The safest reading is: framework dependence is real, but it currently acts more as a **claim-pruning force** than as a **claim-generating force**.

## Qualifications

1. `[artifact-reported]` Both alternative profile families were reconstructed on the existing 2000-paper sample, not the full 19K corpus.
2. `[artifact-reported]` The challenger-derived family is still seed-anchored through lexical bootstrapping and sample-bounded challenger refinement.
3. `[derived]` This spike therefore supports a bounded claim about **framework sensitivity inside the checked-in comparison environment**, not a universal claim about all possible profile-construction methods.
