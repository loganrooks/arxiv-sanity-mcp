---
type: posterior-update
status: complete
date: 2026-04-16
reviewer: codex
target: .planning/spikes/005-evaluation-framework-robustness
hypothesis: H4
---

# Posterior Update

## Question

Did changing the profile-construction family materially alter the comparative picture enough to strengthen `H4`?

## Prior Credence

- `[chosen for now]` `P(H4) = 0.80`
- `[chosen for now]` `P(framework-dependent portion of H2) = 0.60`

## Evidence Summary

- `[artifact-reported]` Five family-induced classification changes occurred across the three profile-construction families.
- `[artifact-reported]` `Qwen3` shifted from `candidate complementary second view` under the saved MiniLM family to `blocked / unclear` under both alternative families.
- `[artifact-reported]` No challenger gained a new positive classification under an alternative family.
- `[derived]` The effect of framework variation is real but directional: it weakens fragile positive stories more than it creates new ones.

## Posterior Credence

- `[chosen for now]` `P(H4) = 0.87`
- `[chosen for now]` `P(framework-dependent portion of H2) = 0.64`

## What Caused The Shift

### H4

- `[derived]` The Qwen3 reversal is the main update driver. A candidate-complementarity claim that disappears under both alternative families is exactly the kind of framework dependence this spike was designed to expose.
- `[derived]` The smaller negative shifts for SPECTER2, GTE, and Voyage add support, but they are not individually strong enough to move the posterior much on their own.
- `[derived]` Stella's stability prevents the posterior from moving further upward; not everything in the comparison frame is family-fragile.

### Framework-dependent portion of H2

- `[derived]` Some model-specific interpretive stories now need weaker language because part of their apparent value depends on the evaluation frame.
- `[derived]` The movement is modest because the spike did not erase the broader structural differences between models; it only narrowed how confidently some of those differences can be read.

## Reversal Conditions

1. `[artifact-reported]` Re-running 005 with a less sample-bounded alternative family could shrink the observed changes if the current category / challenger constructions are themselves unstable heuristics.
2. `[derived]` If 006 shows that retrieval geometry restores the weakened Qwen3 picture across both carried frames, part of the present H4 update would need to be returned to H3 instead.
3. `[derived]` If 008 later shows that a family-sensitive challenger still produces better task outcomes, the practical importance of this H4 update would decrease even if the framework-dependence claim remains true.

## Bounded Conclusion

- `[chosen for now]` H4 is strengthened: the evaluation frame materially affects at least one load-bearing comparative claim.
- `[chosen for now]` The update is **not** "everything was a MiniLM artifact."
- `[chosen for now]` The present posterior supports carrying one alternative family into 006, not abandoning the incumbent frame.
