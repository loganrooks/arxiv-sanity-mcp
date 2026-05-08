---
type: qualitative-review
status: complete
date: 2026-04-16
reviewer: codex
target: .planning/spikes/005-evaluation-framework-robustness
---

# Qualitative Review

## Reviewed Cases

### 1. `category_lexical / SPECTER2`

- `[artifact-reported]` The changed cases center on `P3`, `P4`, and `P8`.
- `[artifact-reported]` `P4` remains coherent and safety-focused under the category family (`ReasAlign`, prompt-injection defense, persona jailbreaking).
- `[artifact-reported]` `P3` and `P8` also introduce more obvious adjacency drift than the saved MiniLM family, including option-pricing and oilfield-reservoir items on `P3`.
- `[derived]` The move from `blocked / unclear` to `distinct but not currently complementary` looks qualitatively supported. The category family makes SPECTER2 look broader and less clean, not newly valuable.

### 2. `category_lexical / Qwen3`

- `[artifact-reported]` The changed cases center on `P1`, `P5`, and `P6`.
- `[artifact-reported]` Some current-family uniques are clearly on-topic (`timed constraints for robotics motion planning`, `multiple diffusion models`, `QwenStyle`), but the set remains mixed and does not remove the previously documented vocabulary-noise risk from Spike 004.
- `[source-traceable]` Spike 004 already recorded Qwen3's structural vocabulary-match false-positive problem, especially on `P1`; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[derived]` The shift from `candidate complementary second view` to `blocked / unclear` is qualitatively supported. The alternative family weakens an already fragile positive story rather than exposing a hidden robust one.

### 3. `category_lexical / Voyage`

- `[artifact-reported]` The changed cases center on `P1`, `P3`, and `P5`.
- `[artifact-reported]` `P1` and `P5` current-family uniques are on-topic and not obviously noisy. `P3`, however, again widens into adjacency items like option pricing.
- `[source-traceable]` Spike 004's strongest Voyage value story was the blind `P2` result, not these profiles; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[derived]` The move to `distinct but not currently complementary` is only partially supported qualitatively. The quantitative downgrade is real, but the review does not justify a strong negative read on Voyage in general.

### 4. `specter2_refined / Qwen3`

- `[artifact-reported]` The changed cases center on `P1`, `P4`, and `P5`.
- `[artifact-reported]` `P4` remains on-topic but narrower; `P5` adds no strong new positive evidence; `P1` still includes a mixed robotics / embodied-control edge rather than a clean complementarity case.
- `[derived]` The move from `candidate complementary second view` to `blocked / unclear` is qualitatively supported. The challenger-derived family does not rescue Qwen3's positive baseline story.

### 5. `specter2_refined / GTE`

- `[artifact-reported]` The changed cases center on `P1`, `P5`, and `P8`.
- `[artifact-reported]` The current-family uniques remain broadly on-topic: explainable activity recognition via GNNs, graph models on connectomes, Bayesian neural network approximation, robotics-VLM transfer.
- `[source-traceable]` Spike 004 described GTE as the most conservative challenger with coherent but modest methodological-envelope divergence; see [FINDINGS.md](../004-embedding-model-evaluation/FINDINGS.md).
- `[derived]` The move to `distinct but not currently complementary` is weaker qualitatively than it is quantitatively. The review supports "not promoted" more than it supports a decisive negative classification.

## Agreement With Metrics

1. `[derived]` Both Qwen3 demotions are supported. Family variation exposes how dependent the candidate-complementary read was on the saved MiniLM frame.
2. `[derived]` The SPECTER2 category-family downgrade is also supported, though as a bounded negative: more mixed and adjacency-prone, not noisy failure.
3. `[derived]` No reviewed case looks like a missed positive winner created by an alternative family.

## Disagreement With Metrics

1. `[derived]` Voyage's category-family downgrade is harsher quantitatively than the title-level review supports.
2. `[derived]` GTE's challenger-family downgrade is also harsher quantitatively than the review supports; the changed papers still look coherent and on-topic.

## Bounded Interpretation

- `[derived]` The strongest qualitative evidence from the changed-case set is **not** "MiniLM was wrong." It is that one apparently live candidate (`Qwen3`) loses credibility once the profile family changes.
- `[derived]` The weaker changes for SPECTER2, Voyage, and GTE support a more cautious claim: alternative profile families can move the comparative reading, but not every moved reading deserves to be treated as decisive.
- `[chosen for now]` The qualitative gate therefore supports carrying framework dependence forward into 006 while treating the non-Qwen3 negative shifts as softening signals, not hard eliminations.

## What This Review Cannot Settle

1. `[artifact-reported]` The review only covers the five family-induced classification changes, not every recommendation delta in the spike.
2. `[artifact-reported]` The alternative families are still sample-bounded and seed-anchored.
3. `[derived]` This review cannot say whether any of these shifted cases would help researchers more in actual tasks; that remains for 008.
