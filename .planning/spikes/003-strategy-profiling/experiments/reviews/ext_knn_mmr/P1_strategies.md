# P1: RL for Robotics (Medium breadth) -- Strategy Comparison Review

## Seeds

1. **Uncertainty-Aware Robotic World Model** (2504.16680) -- Offline MBRL for real robots with epistemic uncertainty
2. **Robot-R1** (2506.00070) -- RL-enhanced embodied reasoning for robot control
3. **SAC Flow** (2509.25756) -- Flow-based policies for continuous robotic control
4. **Mobile Magnetic Manipulation** (2601.15545) -- DRL for GI navigation with magnetic capsule
5. **GPO** (2601.20668) -- Growing Policy Optimization for legged locomotion

The seeds define a coherent interest: RL algorithms applied to robotics, with particular emphasis on policy learning, locomotion, and manipulation. The interest is "medium" breadth because it spans multiple robot types (arms, legs, capsules) and multiple RL paradigms (model-based, model-free, flow-based, PPO variants), but stays firmly within RL-for-robotics.

---

## Part 1: Per-Strategy Paper Assessment

### Centroid (20 papers)

1. **RL with timed constraints for motion planning** (2601.00087) -- Directly relevant: MITL specifications for temporal robot planning. Core RL-robotics.
2. **PALM: Progress-Aware Policy Learning** (2601.07060) -- Directly relevant: VLA for long-horizon manipulation, combining RL with affordance reasoning.
3. **Dynamic Policy Learning for Legged Robot** (2512.24698) -- Directly relevant: sim-to-real transfer for legged locomotion. Matches GPO seed closely.
4. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy** (2601.15761) -- Directly relevant: real-world RL from scratch with a single demonstration. Methodological relevance to SAC Flow seed.
5. **CEI: Cross-Embodiment Interface** (2601.09163) -- Relevant: cross-embodiment transfer for manipulation. More policy-transfer than RL-algorithm, but robotics-grounded.
6. **Solving Robotics Tasks with Prior Demonstration** (2509.04069) -- Directly relevant: imitation-bootstrapped RL for sim-to-real robotics tasks.
7. **Efficiently Learning Robust Torque-based Locomotion** (2601.16109) -- Directly relevant: residual RL + model-based locomotion. Strong match to GPO seed.
8. **Hybrid Motion Planning with DRL** (2512.24651) -- Relevant: DRL for mobile robot navigation. Robotics application, though navigation rather than manipulation/locomotion.
9. **E2HiL: Human-in-the-Loop RL** (2601.19969) -- Relevant: sample-efficient real-world RL for manipulation. Human feedback angle is a useful variant.
10. **Geometric Action Control** (2511.08234) -- Relevant but more abstract: novel action space geometry for continuous RL. Methodological, applies to robotics via MuJoCo but not robot-specific.
11. **Offline Policy Learning with Weight Clipping** (2601.12117) -- Weakly relevant: offline policy learning from historical data, but this is operations research / causal inference framing (propensity scores, treatment effects), not robotics.
12. **Learning Diffusion Policy from Primitive Skills** (2601.01948) -- Relevant: diffusion policies for manipulation. Skill decomposition for robot learning.
13. **Deep RL for Bipedal Locomotion: A Survey** (2404.17070) -- Relevant: survey of DRL for bipedal robots. Good overview paper for someone in this area.
14. **DAPPER: Preference-Based RL for Robot Skill Acquisition** (2505.06357) -- Relevant: PbRL for legged robots. Novel query-efficiency angle on robot RL.
15. **Boosting DRL with Semantic Knowledge** (2601.16866) -- Relevant: knowledge graph embeddings + DRL for robotic manipulators. Interesting integration approach.
16. **Failure-Aware RL** (2601.07821) -- Directly relevant: offline-to-online RL with safety for real-world manipulation. Strong practical relevance.
17. **Spark: Strategic Policy-Aware Exploration** (2601.20209) -- Tangentially relevant: RL exploration for LLM agents, not robots. "Embodied planning" mentioned but this is NLP/agent work. Drift.
18. **Tool-Augmented Policy Optimization** (2510.07038) -- Not relevant to robotics: RLHF for LLM tool use. Pure NLP/agent work despite "policy optimization" in title.
19. **Jet-RL: FP8 RL Training** (2601.14243) -- Not relevant to robotics: computational efficiency for LLM RL training. Shares RL vocabulary but wrong domain.
20. **GRL-SNAM: Geometric RL for Navigation** (2601.00116) -- Marginally relevant: robot navigation using geometric RL, but heavily theoretical (Hamiltonians, energy landscapes). The robot connection is present.

**Centroid assessment:** Strong top-10. Papers 1-9 are solidly in the RL-for-robotics intersection. Papers 10-16 are relevant but increasingly peripheral (pure RL methods, surveys). Papers 17-20 show clear drift: Spark, TAPO, and Jet-RL are RL-for-LLMs papers that share vocabulary ("policy", "reinforcement learning") but are not about robotics. The centroid has averaged the "RL" signal too strongly and started pulling in non-robotics RL work at the tail.

### kNN Per Seed (20 papers)

1. **Dynamic Policy Learning for Legged Robot** (2512.24698) -- Directly relevant (also in centroid). Locomotion, sim-to-real.
2. **SUNG: Uncertainty-Guided Offline-to-Online RL** (2306.07541) -- Relevant to seed 1 (offline MBRL). Pure RL methodology, not robot-specific, but close match to the uncertainty-driven offline RL seed.
3. **Unified Embodied VLM Reasoning** (2512.24125) -- Relevant to seed 2 (Robot-R1). VLA for embodied reasoning with robotic action.
4. **Bayes Adaptive MCTS for Offline MBRL** (2410.11234) -- Relevant to seed 1. Model-based offline RL with Bayesian methods. Pure RL, not robotics-grounded.
5. **Long-Horizon Model-Based Offline RL** (2512.04341) -- Relevant to seed 1. Bayesian perspective on offline MBRL. Again pure RL, not robotics.
6. **E-GRPO: High Entropy Steps for Flow Models** (2601.00423) -- Relevant to seed 3 (SAC Flow). RL for flow matching models, but in image generation domain (CV), not robotics.
7. **ReinFlow: Flow Matching Policy with Online RL** (2505.22094) -- Directly relevant to seed 3. Flow policies for robotic control.
8. **Reverse Flow Matching for RL** (2601.08136) -- Relevant to seed 3. Flow/diffusion policies for online RL. Methodological, not robot-specific.
9. **Align While Search: Belief-Guided Agents** (2512.24461) -- Relevant to seed 2 (Robot-R1). Embodied agents with belief refinement. Not RL-focused, more inference-time.
10. **VIKI-R: Multi-Agent Cooperation via RL** (2506.09049) -- Relevant: embodied multi-agent cooperation with RL. Robotics-adjacent.
11. **Benchmarking RL for Large-Scale Flow Control** (2601.15015) -- Weakly relevant: RL for fluid dynamics (AFC), not robots. "Flow control" means airflow/fluid, not robot control.
12. **Sampling Strategy for MPPI on Legged Robots** (2601.01409) -- Relevant to seed 5 (GPO). Model-predictive control for legged locomotion. Not RL per se, but control-for-locomotion.
13. **Failure-Aware RL** (2601.07821) -- Directly relevant (also in centroid).
14. **Solving Robotics Tasks with Prior Demonstration** (2509.04069) -- Directly relevant (also in centroid).
15. **DextER: Language-driven Dexterous Grasp** (2601.16046) -- Relevant: dexterous manipulation with embodied reasoning. Robotics-grounded.
16. **Jet-RL: FP8 RL Training** (2601.14243) -- Not relevant to robotics (also in centroid). LLM training efficiency.
17. **Composite Flow Matching for RL** (2505.23062) -- Relevant to seed 3. Offline-to-online RL with flow matching. Methodological.
18. **Explore with Long-term Memory** (2601.10744) -- Relevant to seed 2. Embodied exploration with multimodal LLMs. Robotics-adjacent.
19. **Smart Exploration with Bounded Uncertainty** (2504.05978) -- Relevant to seed 1. Uncertainty-guided exploration. Pure RL methodology.
20. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy** (2601.15761) -- Directly relevant (also in centroid).

**kNN assessment:** The kNN set shows a clearly different character. It clusters heavily around individual seeds: papers 2-5 are close to seed 1 (offline MBRL), papers 6-8 are close to seed 3 (flow-based policies), papers 9-10 and 15 are close to seed 2 (embodied reasoning). This produces relevant-to-a-seed papers that the centroid misses (e.g., ReinFlow, Composite Flow Matching, Unified Embodied VLM), but also pulls in tangential work (E-GRPO for image generation, benchmarking RL for fluid dynamics). The set is less coherent as a whole -- a researcher reading these 20 papers would notice they jump between sub-topics more than the centroid set.

### MMR (20 papers)

1. **RL with timed constraints** (2601.00087) -- Same as centroid #1. Directly relevant.
2. **Dynamic Policy Learning for Legged Robot** (2512.24698) -- Same as centroid #3. Directly relevant.
3. **Jet-RL: FP8 RL Training** (2601.14243) -- Not relevant (same drift as centroid).
4. **PALM: Progress-Aware Policy Learning** (2601.07060) -- Same as centroid #2. Directly relevant.
5. **E2HiL: Human-in-the-Loop RL** (2601.19969) -- Same as centroid #9. Relevant.
6. **Off-Policy Actor-Critic** (2601.15761) -- Same as centroid #4. Directly relevant.
7. **Efficiently Learning Robust Locomotion** (2601.16109) -- Same as centroid #7. Directly relevant.
8. **CEI: Cross-Embodiment Interface** (2601.09163) -- Same as centroid #5. Relevant.
9. **Geometric Action Control** (2511.08234) -- Same as centroid #10. Methodologically relevant.
10. **RL for Endoscopic Navigation** (2601.02798) -- **MMR-unique.** Directly relevant: RL for robotic endoscopy. Interesting application domain that centroid missed.
11. **Solving Robotics Tasks with Prior Demonstration** (2509.04069) -- Same as centroid #6. Directly relevant.
12. **BAPO: Boundary-Aware Policy Optimization** (2601.11037) -- **MMR-unique.** Not relevant to robotics: agentic search for LLMs with RL. Vocabulary overlap only.
13. **Higher-Order Action Regularization in DRL** (2601.02061) -- **MMR-unique.** Partially relevant: action smoothness for control (MuJoCo + building energy). The continuous control angle connects to robotics, but building energy management is off-topic.
14. **Smart Exploration with Bounded Uncertainty** (2504.05978) -- Methodologically relevant. Uncertainty-guided RL.
15. **Tool-Augmented Policy Optimization** (2510.07038) -- Not relevant (same as centroid).
16. **Failure-Aware RL** (2601.07821) -- Same as centroid #16. Directly relevant.
17. **DAPPER: Preference-Based RL** (2505.06357) -- Same as centroid #14. Relevant.
18. **AION: Aerial Indoor Object-Goal Navigation** (2601.15614) -- **MMR-unique.** Relevant: RL for drone navigation. Adds aerial robotics perspective not present in centroid.
19. **Boosting DRL with Semantic Knowledge** (2601.16866) -- Same as centroid #15. Relevant.
20. **Deep RL for Bipedal Locomotion: A Survey** (2404.17070) -- Same as centroid #13. Relevant.

**MMR assessment:** MMR retains 15 of centroid's 20 papers, swapping 5. Of the 4 MMR-unique papers: one is genuinely good (endoscopic navigation), one is interesting but mixed (aerial navigation), one has partial relevance (action regularization), and one is off-topic (agentic search). The swapped-out centroid papers include two robotics-relevant ones (Hybrid Motion Planning, Diffusion Policy from Skills) and three weaker ones (Offline Policy Learning/operations-research, Spark/LLM-agents, GRL-SNAM/theoretical). So MMR's swap is roughly neutral: it traded some good robotics papers for a mix of one good robotics paper and some tangential work. The diversity gain is real but modest.

---

## Part 2: Strategy Comparison

### Centroid vs kNN

The kNN approach produces a fundamentally different set: only 5 papers overlap (Jaccard ~0.14 on the full sets). The kNN set clearly reflects individual seed neighborhoods:

- **Seed 1 cluster (offline MBRL):** SUNG, Bayes Adaptive MCTS, Long-Horizon Offline RL -- these are all pure RL methodology papers about offline model-based learning. They match seed 1's abstract closely but lack the robotics grounding that the centroid demands. A centroid-based approach averages seed 1's "offline MBRL" signal with seed 5's "legged locomotion" signal and produces papers that sit at the intersection.
- **Seed 3 cluster (flow-based policies):** ReinFlow, Reverse Flow Matching, Composite Flow Matching, E-GRPO -- these are genuinely interesting papers about flow/diffusion policies for RL. The centroid approach does not surface these because the centroid dilutes the "flow policy" signal across all 5 seeds. This is arguably a miss by the centroid.
- **Seed 2 cluster (embodied reasoning):** Unified Embodied VLM, Align While Search, Explore with Long-term Memory -- these match the vision-language-action angle of Robot-R1.

The kNN approach finds papers that are relevant to individual facets of the interest but not to the interest as a whole. For a researcher who wants "RL for robotics broadly," the centroid set is better. For a researcher who wants to deeply explore one sub-area (e.g., flow-based policies for robot control), the kNN approach surfaces papers the centroid misses entirely.

### Centroid vs MMR

MMR retains 75% of the centroid set. The 5 swapped papers are a mixed bag. The best MMR-unique find is **RL for Endoscopic Navigation** (2601.02798) -- a genuine robotics RL paper in an application domain (medical robotics) that the centroid missed. **AION (aerial navigation)** adds another robot type. But **BAPO (agentic search)** is noise. The centroid-unique papers that MMR dropped include some genuine robotics papers (Hybrid Motion Planning, Diffusion Policy from Skills), so the trade is not clearly positive.

Does the MMR set *feel* less redundant? Marginally. The centroid set has clusters of similar papers (e.g., multiple locomotion papers, multiple manipulation papers), and MMR thins these clusters slightly. But the effect is subtle -- you would not notice the difference without side-by-side comparison.

### kNN Unique Papers

Of the 14 kNN-unique papers:
- **Genuinely relevant and missed by centroid:** ReinFlow (flow policies for robots), Sampling Strategy for MPPI (legged locomotion control), DextER (dexterous grasping), VIKI-R (multi-agent embodied cooperation). These are real finds -- 4 out of 14.
- **Relevant to one seed but not the overall interest:** SUNG, Bayes Adaptive MCTS, Long-Horizon Offline RL, Reverse Flow Matching, Composite Flow Matching. These are pure RL methodology papers without robotics grounding. A specialist in one sub-area might value them; a generalist in RL-for-robotics would not.
- **Off-topic or tangential:** E-GRPO (image generation), Benchmarking RL for Flow Control (fluid dynamics), Align While Search (LLM inference), Explore with Long-term Memory (LLM + embodied but not RL-focused). These are noise.

---

## Part 3: Set-Level Assessment

### Centroid
- **Coherence:** High in top-10, degrading in bottom-5. Papers relate to each other through the RL-robotics nexus. The LLM-RL papers at the tail break coherence.
- **Diversity:** Moderate. Covers locomotion (bipedal, quadruped), manipulation (various), navigation, human-in-the-loop. Missing: medical robotics, aerial robotics, flow-based policy methods.
- **Researcher satisfaction:** Good. A researcher in RL for robotics would find the top 15 papers useful and recognize the bottom 5 as drift. Solid starting set for literature review.

### kNN Per Seed
- **Coherence:** Low. The set reads like 3-4 separate reading lists stapled together: offline MBRL papers, flow-policy papers, embodied reasoning papers, and locomotion papers. They do not form a coherent recommendation.
- **Diversity:** Superficially high (many sub-topics), but this is fragmentation, not diversity. The sub-topics are poorly integrated.
- **Researcher satisfaction:** Mixed. A researcher would be confused by the set's lack of coherence but might discover one or two papers (ReinFlow, DextER) they would not have found otherwise.

### MMR
- **Coherence:** Similar to centroid (shares 75% of papers). Slightly improved by adding medical robotics and aerial robotics.
- **Diversity:** Marginally better than centroid. Adds medical and aerial robotics application domains.
- **Researcher satisfaction:** Comparable to centroid. The net swap is roughly neutral.

---

## Part 4: Emergent Observations

1. **kNN has a use case for heterogeneous interests:** If a researcher has seeds that span genuinely distinct sub-fields (e.g., one seed in offline MBRL, one in flow policies, one in locomotion), kNN preserves the neighborhood structure of each seed. The centroid averages these into a mush that favors the intersection. For very heterogeneous profiles, kNN's fragmentation might actually be a feature -- it preserves the distinctness of each research thread. However, the P1 profile is not heterogeneous enough for this to help; all seeds are "RL for robotics" variants.

2. **kNN surfaces the "flow policy" literature that centroid misses entirely.** The centroid approach, by averaging, dilutes the signal from seed 3 (SAC Flow). Three flow-policy papers (ReinFlow, Reverse Flow Matching, Composite Flow Matching) appear only in kNN. These are genuinely relevant to someone interested in the full scope of RL-for-robotics. This is a real blind spot of the centroid approach for interests where one seed represents a methodologically distinct sub-area.

3. **MMR's diversity gain is real but trivial.** Endoscopic navigation and aerial navigation are genuinely different from the centroid's set, but two papers out of 20 is not a meaningful diversity improvement. The cost (losing two relevant robotics papers) may not be worth it.

4. **All three strategies suffer from RL-vocabulary pollution.** Jet-RL (FP8 training for LLM RL), TAPO (tool use for LLM agents), and Spark (LLM agent exploration) appear across strategies. MiniLM embeddings cannot distinguish "RL for robots" from "RL for LLMs" because the vocabulary is shared. This is a fundamental limitation of the embedding space, not the retrieval strategy.

---

## Part 5: Metric Divergence

- **Does kNN FEEL catastrophic?** Not exactly catastrophic, but clearly worse. The set is fragmented and less useful as a coherent recommendation. A researcher asking "what should I read about RL for robotics?" would be poorly served. But a researcher asking "what relates to THIS specific paper?" (pointing at SAC Flow) would find the kNN results useful for that seed. The MRR drop is real, but the word "catastrophic" overstates it -- "incoherent" is more accurate.

- **Does MMR FEEL meaningfully better?** No. The swap of 5 papers is roughly neutral in quality. The one genuinely novel find (endoscopic navigation) does not justify treating MMR as a distinct strategy. It is a minor refinement at best.
