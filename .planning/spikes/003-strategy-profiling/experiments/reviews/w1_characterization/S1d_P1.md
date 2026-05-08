# W1 Characterization Review: S1d (TF-IDF centroid) x P1 (RL for Robotics)

**Strategy:** S1d -- TF-IDF (50K features, sublinear TF, English stopwords), cosine similarity centroid
**Profile:** P1 -- RL for Robotics (Medium breadth, 10 seeds)
**Score range:** 0.290 -- 0.253 (spread: 0.037)
**Held-out recovery:** 1/5 (Learning Quadrupedal Locomotion for a Heavy Hydraulic Robot)
**Profile papers in top-20:** 4

## Part 1: Per-Paper Assessment

**#1 Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control (2601.16163) -- 0.290**
Video foundation models for robot policy. Not RL. However, it explicitly discusses "reinforcement learning" in the abstract as part of its approach. TF-IDF picks this up because of keyword overlap -- the abstract literally contains the key terms. This is a legitimate TF-IDF hit that happens not to be RL-primary.

**#2 On-the-Fly VLA Adaptation via Test-Time RL (2601.06748) -- 0.289**
VLA + test-time RL. Genuinely about applying RL to adapt VLA models for robots. Good recommendation. MiniLM had this at #11.

**#3 Disentangling Perception and Reasoning for Cloth Manipulation (2601.21713) -- 0.287**
RL for cloth manipulation without demonstrations. UNIQUE to TF-IDF's list. Genuinely on-topic: RL applied to a specific robotic manipulation task. The abstract explicitly discusses "reinforcement learning" and "robotic" manipulation. TF-IDF correctly identifies the keyword match.

**#4 Learning Quadrotor Control from Visual Features Using Differentiable Simulation (2410.15979) -- 0.287**
RL for quadrotor control with differentiable simulation. UNIQUE to TF-IDF. Directly on-topic: RL + robot + specific physical platform. Strong recommendation that both embedding models missed. The abstract discusses "reinforcement learning (RL)" and "robotics" explicitly.

**#5 CLF-RL: Control Lyapunov Function Guided RL (2508.09354) -- 0.276**
Structured reward shaping for RL bipedal locomotion using control Lyapunov functions. UNIQUE to TF-IDF and a genuinely excellent find. This paper sits at the classical control + RL intersection that neither embedding model captured. A researcher in RL for robotics would definitely want this -- it addresses reward design, which was a gap in both embedding strategies.

**#6 COVR: Collaborative Optimization of VLMs and RL Agent (2601.06122) -- 0.270**
Visual RL with VLM assistance. Not purely RL for robotics but RL is a primary component. Relevant.

**#7 Efficiently Learning Robust Torque-based Locomotion Through RL (2601.16109) -- 0.269**
RL for bipedal locomotion. On-topic. Same paper as MiniLM #4. Both agree.

**#8 AnyTask (2512.17853) -- 0.266, profile paper**
Sim-to-real policy learning framework. On-topic. Same paper as MiniLM #7.

**#9 Constrained Meta RL with Provable Test-Time Safety (2601.21845) -- 0.264**
Safe meta-RL with formal safety guarantees. UNIQUE to TF-IDF. This is a high-value discovery: it addresses safe RL, which was a complete gap in both embedding strategies. A researcher in RL for robotics deploying on real hardware would absolutely care about test-time safety guarantees. TF-IDF finds it because the abstract contains "reinforcement learning" + "safety" + "robot" terms.

**#10 Learning a Unified Latent Space for Cross-Embodiment Robot Control (2601.15419) -- 0.263**
Cross-embodiment humanoid control. UNIQUE to TF-IDF. Relevant through the robot control lens, though the approach is representation learning more than RL.

**#11 GenPO (2505.18763) -- 0.260, profile paper**
Diffusion + on-policy RL. On-topic.

**#12 Learning on the Fly: Rapid Policy Adaptation (2508.21065) -- 0.259**
Differentiable simulation for sim-to-real. Same as MiniLM #8.

**#13 ReinFlow (2505.22094) -- 0.257, profile paper**
Flow matching + RL. On-topic. Same as MiniLM #1.

**#14 Physics-Driven Data Generation for Contact-Rich Manipulation (2502.20382) -- 0.257**
Data generation pipeline for robot manipulation. UNIQUE to TF-IDF. Not RL but directly relevant as infrastructure for training robot policies.

**#15 RL Goal-Reaching Control with Guaranteed Lyapunov-Like Stabilizer for Mobile Robots (2601.19499) -- 0.256**
RL for mobile robot navigation with stability guarantees. UNIQUE to TF-IDF. Excellent find -- directly on-topic (RL + robot + formal guarantees) and addresses the safe RL gap. The keyword "reinforcement learning" + "robot" + "goal-reaching" + "guarantees" makes this a strong TF-IDF hit.

**#16 Vlaser: VLA Model with Synergistic Embodied Reasoning (2510.11027) -- 0.255**
VLA model. Not RL. The abstract mentions "robot control" extensively. Weak TF-IDF hit based on shared domain vocabulary.

**#17 Failure-Aware RL: Reliable Offline-to-Online RL with Self-Recovery (2601.07821) -- 0.255**
RL with failure recovery for real robot manipulation. UNIQUE to TF-IDF. Directly on-topic and addresses a practical concern (failure recovery during real-world RL) that is highly relevant. Good discovery.

**#18 Learning Quadrupedal Locomotion for a Heavy Hydraulic Robot (2601.11143) -- 0.254, HELD-OUT**
Sim-to-real RL for a specific robot platform. Directly on-topic. This is the one held-out paper TF-IDF recovers that neither embedding model found. The keyword specificity ("quadrupedal locomotion" + "reinforcement learning" + "robot") makes this a natural TF-IDF hit.

**#19 PolaRiS: Scalable Real-to-Sim Evaluations (2512.16881) -- 0.253**
Robot policy evaluation infrastructure. Same as MiniLM #15.

**#20 SOP: Scalable Online Post-Training for VLA Models (2601.03044) -- 0.253**
VLA post-training with RL. Same as SPECTER2 #2.

## Part 2: Set-Level Assessment

**Overall character:** TF-IDF's set reads as "papers that literally talk about reinforcement learning and robots" -- a keyword-faithful interpretation that catches papers the embedding models miss because those papers use the exact terminology. Approximately 12-14 of the 20 papers are genuinely about RL applied to robots, compared to 8-10 for both embedding strategies. The higher on-topic rate is because TF-IDF rewards literal keyword presence rather than semantic neighborhood.

**Strengths:**
- Recovers the only held-out paper any strategy found for P1
- Finds papers at the RL + classical control intersection (#5 CLF-RL, #15 Lyapunov RL) that both embedding models completely missed
- Finds safe RL papers (#9 Constrained Meta RL, #15 Lyapunov) that address a gap in both embedding models
- Higher proportion of genuinely RL-focused papers (fewer imitation learning false positives)
- More topically diverse within the RL-for-robotics space (locomotion, manipulation, navigation, safety, reward design)

**Gaps:**
- Does not find the cross-community / adjacent-field papers that SPECTER2 surfaces (e.g., Lipschitz critics, policy bootstrapping)
- Less likely to surface methodologically novel papers that do not use standard terminology
- Narrower vocabulary focus means it may miss papers that describe RL techniques using different terminology (e.g., "policy optimization" without explicitly saying "reinforcement learning")

**False positive pattern:** Papers that mention "reinforcement learning" and "robot" in the abstract but are not primarily about RL for robotics (e.g., VLA papers that briefly mention RL as one component).

**Failure mode:** TF-IDF is literal -- it finds what the words say, not what the paper is about. This is both its strength (high precision on keyword-relevant papers) and its weakness (cannot infer relevance from conceptual similarity without keyword overlap).

## Part 4: Emergent Observations

1. **TF-IDF's unique advantage: methodological diversity.** The most striking finding is that TF-IDF surfaces papers from RL sub-areas (safe RL, control-theoretic RL, failure recovery) that both embedding models completely miss. These are not obscure papers -- they are directly relevant to the research interest and use the exact same terminology. The embedding models miss them because their semantic neighborhoods are defined by the dominant research direction (VLA + diffusion policies), which drowns out the smaller methodological sub-communities.

2. **The held-out recovery matters.** TF-IDF is the only strategy to recover ANY held-out paper for P1. The held-out paper (#18, quadrupedal locomotion) is recovered because its keywords precisely match the profile. This suggests that TF-IDF is better at finding papers that are "obviously relevant" (keyword match) while embedding models are better at finding papers that are "surprisingly relevant" (semantic proximity without exact keyword match).

3. **TF-IDF as a precision instrument.** Looking at the scores, TF-IDF's spread (0.037) is moderate -- between MiniLM (0.053) and SPECTER2 (0.007). But the scores are much lower in absolute terms (0.29 vs 0.66 vs 0.97), meaning TF-IDF is more conservative in its similarity judgments. A TF-IDF score of 0.29 means approximately 29% of the weighted vocabulary is shared -- a meaningful but not overwhelming overlap. This gives TF-IDF a more graded response that tracks genuine keyword specificity.

4. **The complementarity case.** The combination of TF-IDF + either embedding model would cover significantly more of the relevant literature than either alone. TF-IDF catches the "obvious relevant" papers (keyword match), while embeddings catch the "adjacently relevant" papers (semantic similarity). This is not a novel observation, but the specific character of what each misses makes the case empirically concrete for this profile.

## Part 5: Metric Divergence

TF-IDF's LOO-MRR was 0.104 -- the lowest of the three strategies, less than a quarter of MiniLM's. But qualitatively, TF-IDF's recommendation set is at least as good as MiniLM's and arguably better in some dimensions (methodological diversity, held-out recovery, fewer false positives from adjacent paradigms).

The MRR metric penalizes TF-IDF because:
1. The LOO evaluation uses embedding-defined clusters, which inherently favor embedding-based strategies
2. TF-IDF's recommendations are more dispersed across the topic space (hitting safe RL, control-theoretic RL, etc.) rather than concentrated in the embedding cluster center
3. The "leave one out" protocol tests whether removing one paper from a cluster pushes similar papers to the top -- but TF-IDF's similarity is keyword-based, not cluster-membership-based

The qualitative evidence strongly supports the hypothesis that TF-IDF's low MRR is an artifact of evaluation framework bias, not a genuine quality deficiency. TF-IDF is a competitive strategy that the quantitative metrics systematically underrate.
