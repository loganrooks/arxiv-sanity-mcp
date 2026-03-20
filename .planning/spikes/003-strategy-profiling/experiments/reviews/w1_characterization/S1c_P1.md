# W1 Characterization Review: S1c (SPECTER2 adapter) x P1 (RL for Robotics)

**Strategy:** S1c -- SPECTER2 with proximity adapter, cosine similarity centroid
**Profile:** P1 -- RL for Robotics (Medium breadth, 10 seeds)
**Score range:** 0.971 -- 0.964 (spread: 0.007)
**Held-out recovery:** 0/5
**Profile papers in top-20:** 2

## Part 1: Per-Paper Assessment

**#1 Real-world RL from Suboptimal Interventions (2512.24288) -- 0.971**
Online RL for real-world robotic manipulation. Squarely on-topic. One of the strongest single recommendations across any strategy. Directly addresses the core research interest -- learning policies on physical robots with RL.

**#2 SOP: Scalable Online Post-Training for VLA Models (2601.03044) -- 0.971**
Post-training VLA models with online RL. Interesting that SPECTER2 ranks this #2 when MiniLM ranks it nowhere near the top-20. This is a systems-level paper about scaling RL-based fine-tuning of foundation models for robotics. High-value cross-community paper: it bridges the VLA and RL-for-robotics communities.

**#3 Flattening Hierarchies with Policy Bootstrapping (2505.14975) -- 0.969**
Offline goal-conditioned RL. This is pure RL methodology paper positioned in the "self-supervised pre-training" frame. MiniLM did not surface this. SPECTER2 finds it, probably because of citation-graph connections to the RL-for-robotics literature. A researcher would find this useful for its bootstrapping technique, even though its robotics connection is secondary.

**#4 Abstracting Robot Manipulation Skills via MoE Diffusion Policies (2601.21251) -- 0.969**
Multi-task diffusion policies for manipulation. Not RL -- this is imitation learning with diffusion models. But the multi-task manipulation framing is directly relevant to the research interest. Same false-positive category as MiniLM: policy learning conflated with RL.

**#5 Reflection-Based Task Adaptation for Self-Improving VLA (2510.12710) -- 0.968**
VLA model adaptation via RL. Genuinely at the RL+VLA frontier. This is unique to SPECTER2's list and represents its tendency to find cross-community connections. A researcher in RL for robotics would benefit from knowing about this work.

**#6 ReinFlow (2505.22094) -- 0.968, profile paper**
Flow matching + RL for robotic control. Same paper MiniLM ranked #1. On-topic.

**#7 GenPO (2505.18763) -- 0.967, profile paper**
Diffusion models + on-policy RL. Also a profile seed paper in the full set. On-topic.

**#8 Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training (2509.18631) -- 0.967**
Behavior cloning with domain adaptation. Not RL. Same false positive as in MiniLM. SPECTER2 also conflates policy learning approaches.

**#9 Cosmos Policy (2601.16163) -- 0.967**
Video foundation models for robot policy learning. Not RL. SPECTER2 ranks this #9; MiniLM ranks it #20. Both include it, but SPECTER2 gives it higher priority, probably because it is well-cited/connected in the graph to the broader robotics policy learning community.

**#10 Bootstrap Off-policy with World Model (2511.00423) -- 0.966**
Model-based RL with off-policy data. Genuine RL paper, same as MiniLM #6. Both strategies agree this belongs.

**#11 Masked Generative Policy for Robotic Control (2512.09101) -- 0.966**
Discrete token imitation learning. Not RL. False positive.

**#12 Scalable Exploration via Value-Guided Flow (2601.19707) -- 0.966**
RL exploration methods. On-topic. MiniLM had this at #2; SPECTER2 at #12. Interesting rank disagreement.

**#13 Learning Diffusion Policy from Primitive Skills (2601.01948) -- 0.966**
Diffusion policies for manipulation. Not RL. MiniLM had this at #3; SPECTER2 agrees on inclusion but ranks lower.

**#14 Beyond Static Datasets: Robust Offline Policy Optimization (2601.18107) -- 0.965**
Offline RL for industrial robotics with synthetic data. Genuinely on-topic and UNIQUE to SPECTER2's list. This paper explicitly addresses RL in safety-critical industrial settings -- exactly the kind of applied RL-for-robotics paper the profile seeks. Good discovery.

**#15 Action Tokenizer Matters in In-Context Imitation Learning (2503.01206) -- 0.965**
In-context imitation learning action representation. Not RL. False positive.

**#16 Coupled Distributional Random Expert Distillation (2505.02228) -- 0.965**
World model + imitation learning. Mentions robotics and autonomous driving. Tangentially relevant through the "learning from demonstrations" lens. Weak recommendation.

**#17 Lipschitz-Regularized Critics for Policy Robustness (2404.13879) -- 0.965**
Robust RL with Lipschitz critics under dynamics uncertainty. Pure RL theory paper, but directly applicable to sim-to-real transfer robustness. UNIQUE to SPECTER2. This is a high-value discovery -- a robotics researcher might miss this cs.LG paper, but the technique is directly applicable to their sim-to-real challenges.

**#18 Learning from Demonstrations via Capability-Aware Goal Sampling (2601.08731) -- 0.964**
Imitation learning with goal-conditioned behavior. Not RL (or only loosely RL through the goal-conditioned framing). Weak.

**#19 One Step Is Enough: Dispersive MeanFlow Policy Optimization (2601.20701) -- 0.964**
Fast flow matching for robotic control. Not RL. Same paper as MiniLM #12.

**#20 PALM: Progress-Aware Policy Learning via Affordance Reasoning (2601.07060) -- 0.964**
VLA model for long-horizon manipulation. Not RL proper, though uses affordance reasoning. Weak RL connection.

## Part 2: Set-Level Assessment

**Overall character:** Remarkably similar to MiniLM's set in composition -- roughly 8-10 genuine RL papers, 10-12 imitation learning / VLA / policy learning papers. The same fundamental confusion between "RL for robotics" and "policy learning for robotics" persists. However, the specific papers are partially different (9/20 overlap with MiniLM), and SPECTER2's unique papers tend to be slightly more methodologically interesting.

**Strengths:**
- Surfaces some high-value cross-community papers that MiniLM misses (#2 SOP, #3 Policy Bootstrapping, #5 VLA adaptation, #14 Robust Offline RL, #17 Lipschitz critics)
- The unique papers tend to be more architecturally diverse -- not just "diffusion/flow for manipulation" variations

**Gaps:**
- Same gaps as MiniLM: no reward design, no safe RL, no multi-robot RL
- Also 0/5 held-out papers recovered
- Heavy VLA/foundation model presence (arguably heavier than MiniLM)

**False positive pattern:** Identical to MiniLM -- imitation learning and behavior cloning papers conflated with RL. The rate is roughly the same.

**Failure mode:** The extreme score compression (0.007 spread!) means SPECTER2 is making essentially no discriminative judgments within this set. Every paper in the top-20 has a score within 0.7% of every other paper. This is much worse than MiniLM's 5.3% spread. SPECTER2's proximity adapter embeddings may be poorly normalized or may not separate well at the fine-grained level within a topic.

## Part 4: Emergent Observations

1. **Score compression is the headline finding:** SPECTER2 adapter's score range of 0.007 is an order of magnitude tighter than MiniLM's 0.053 and TF-IDF's 0.037. This is not just a normalization artifact -- it means the top-20 is essentially an arbitrary cut from a large pool of equally-scored papers. The ranking within the top-20 is meaningless. This has profound implications for any user-facing presentation: SPECTER2 cannot meaningfully distinguish between its #1 and its #100 recommendation.

2. **Different papers, same failure:** Despite sharing only 9/20 papers with MiniLM, SPECTER2 exhibits the same conceptual confusion between RL and other policy learning paradigms. This suggests the confusion is not a property of either embedding model specifically -- it is a property of the problem. The papers genuinely do share semantic and citation-graph proximity because they address the same tasks, use similar evaluation setups, and cite each other.

3. **The citation graph effect:** SPECTER2's unique papers (#2, #3, #5, #14, #17) tend to be papers that are well-connected in the citation graph to the RL-for-robotics community even if their primary contribution is in a different subfield. This is the "would cite" or "would be cited by" signal -- SPECTER2 captures proximity in academic discourse, not just semantic similarity. Paper #17 (Lipschitz critics) is the clearest example: it is a pure theory paper that SPECTER2 surfaces because it is relevant to the community's problems, even though its abstract does not mention "robot."

4. **VLA saturation:** Both MiniLM and SPECTER2 are saturated with VLA-related papers (foundation models applied to robotics). This reflects the current state of the field -- VLA is the dominant research direction in robotics ML as of early 2026. A recommendation system would need temporal awareness or explicit diversity mechanisms to avoid overwhelming users with the hot-topic-of-the-moment.

## Part 5: Metric Divergence

SPECTER2's LOO-MRR of 0.184 (half of MiniLM's 0.398) suggested it was substantially worse at retrieval. The qualitative impression is more nuanced: SPECTER2 finds papers that are roughly as useful as MiniLM's, but its ranking within the result set is meaningless due to extreme score compression. Its MRR is lower not because its papers are worse, but because the LOO evaluation rewards precise ranking, and SPECTER2 cannot rank precisely.

The 0/5 held-out recovery is the same for both strategies, which is more damning for the evaluation framework (the held-out papers may simply not be in the top-20 of any centroid approach) than for either strategy individually.

The qualitative impression does NOT support a 2x quality advantage for MiniLM. The strategies produce similarly useful (and similarly flawed) recommendation sets. MiniLM's quantitative advantage may be largely an artifact of better score calibration rather than better retrieval.
