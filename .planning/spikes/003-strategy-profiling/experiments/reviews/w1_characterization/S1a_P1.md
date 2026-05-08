# W1 Characterization Review: S1a (MiniLM centroid) x P1 (RL for Robotics)

**Strategy:** S1a -- MiniLM all-MiniLM-L6-v2 centroid, dot-product ranking
**Profile:** P1 -- RL for Robotics (Medium breadth, 10 seeds)
**Score range:** 0.660 -- 0.607 (spread: 0.053)
**Held-out recovery:** 0/5
**Profile papers in top-20:** 2

## Seeds Summary

The 10 seeds cover a tight RL-for-robotics core: policy optimization (GPO, SAC Flow, ReinFlow), sim-to-real transfer, model-based RL for real robots, multi-agent cooperation (VIKI-R), and niche applications (gastrointestinal navigation, robotic cutting). Most are cs.RO primary, with some cs.AI and cs.LG cross-listings. The interest is methodologically focused on RL applied to physical robots rather than pure RL theory.

## Part 1: Per-Paper Assessment

**#1 ReinFlow (2505.22094) -- score 0.660, profile paper**
Also a seed paper in the full set (subset_15). Flow matching + RL for robotic control. Extremely on-topic -- this is what the profile is about. A researcher interested in RL for robotics would absolutely want this paper. It would be easy to find via keyword search ("reinforcement learning" + "flow matching" + "robot").

**#2 Scalable Exploration for High-Dimensional Continuous Control via Value-Guided Flow (2601.19707) -- 0.638**
Exploration methods for high-dimensional RL, with robotics applications mentioned. Relevant but slightly more on the RL theory side than the robotics application side. A researcher might find this through RL venue proceedings but not necessarily through robotics channels. Decent recommendation.

**#3 Learning Diffusion Policy from Primitive Skills for Robot Manipulation (2601.01948) -- 0.638**
Diffusion policies for robotic manipulation. Clearly relevant to the research interest, though the approach is imitation learning rather than RL proper. A researcher in RL for robotics would want to know about this as a competing paradigm. Good discovery recommendation.

**#4 Efficiently Learning Robust Torque-based Locomotion Through RL with Model-Based Supervision (2601.16109) -- 0.634**
RL for bipedal locomotion with model-based supervision. Squarely on-topic: RL + robot + locomotion. Practically useful for anyone working on legged robots. Easy to find via keyword search.

**#5 Learning Diverse Skills for Behavior Models with MoE (2601.12397) -- 0.632**
Mixture-of-experts for imitation learning in robotic manipulation. Related but again leans toward imitation learning rather than RL. The connection is through the robotics application domain and the "skill learning" framing that overlaps with RL skill discovery literature.

**#6 Bootstrap Off-policy with World Model (2511.00423) -- 0.626**
Model-based RL with off-policy data. More general RL theory paper that happens to include robotics benchmarks. Would be useful for the methodological toolkit, but the robotics connection is incidental to the contribution. A pure robotics researcher might miss this; an RL-theory-aware researcher would find it via venue.

**#7 AnyTask (2512.17853) -- 0.624, profile paper**
Sim-to-real policy learning framework. Directly relevant: it addresses one of the core challenges in RL for robotics (data generation for sim-to-real transfer). Strong recommendation.

**#8 Learning on the Fly: Rapid Policy Adaptation via Differentiable Simulation (2508.21065) -- 0.623**
Sim-to-real transfer through differentiable simulation. Relevant for the same reason as AnyTask -- addresses the sim-to-real gap that RL robotics researchers face. Slightly more niche in its specific approach (differentiable physics) but clearly valuable.

**#9 Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training (2509.18631) -- 0.623**
Behavior cloning with sim-real co-training. Again, the sim-to-real theme. Relevant but is behavior cloning, not RL. The strategy seems to be pulling in many "robot policy learning" papers regardless of whether the learning paradigm is RL or imitation.

**#10 Real-world RL from Suboptimal Interventions (2512.24288) -- 0.621**
Online RL for real-world robotic manipulation with human interventions. Directly on-topic: this is literally "RL for robotics" applied to real hardware. Strong recommendation that a researcher would want to read.

**#11 On-the-Fly VLA Adaptation via Test-Time RL (2601.06748) -- 0.620**
VLA models fine-tuned with RL at test time. Interesting intersection: large foundation models meet RL for adaptation. Relevant and potentially high-discovery-value -- this is the frontier where RL meets VLAs, which a pure RL-for-robotics researcher might not track.

**#12 One Step Is Enough: Dispersive MeanFlow Policy Optimization (2601.20701) -- 0.620**
Fast action generation for robotic control via flow matching. Relevant for deployment considerations in robot RL. Would be useful for anyone deploying learned policies on real hardware.

**#13 Masked Generative Policy for Robotic Control (2512.09101) -- 0.617**
Discrete-token action generation for imitation learning. Again imitation learning, not RL. The robotics connection is strong but the RL connection is weak. This is becoming a pattern.

**#14 Value Vision-Language-Action Planning & Search (2601.00969) -- 0.616**
VLA model with value-based search for robotic manipulation. Bridges RL (value estimation) and foundation models. Relevant through the value function component; a researcher interested in RL for robotics should know about this.

**#15 PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies (2512.16881) -- 0.615**
Evaluation infrastructure for robot policies. Relevant as tooling/infrastructure, not as a technique paper. A researcher would use this, not cite it as related work. Moderate discovery value.

**#16 Towards Space-Based Environmentally-Adaptive Grasping (2601.21394) -- 0.615**
Robotic grasping with RL in unstructured environments. On-topic but very application-specific. The RL component seems to be a means to an end rather than the contribution.

**#17 Causal World Modeling for Robot Control (2601.21998) -- 0.612**
Video world models for robot learning. Not RL-specific but related through the world modeling connection that model-based RL researchers would recognize. Interesting cross-pollination recommendation.

**#18 Breaking Task Impasses: Adaptive Neuro-Symbolic Learning for Open-World Robotics (2601.16985) -- 0.611**
Neuro-symbolic planning + RL for open-world robot adaptation. Relevant intersection -- combines planning and RL for robots. Moderate discovery value; the neuro-symbolic angle is distinctive.

**#19 MetaWorld: Skill Transfer in Hierarchical World Model (2601.17507) -- 0.608**
Hierarchical world model for humanoid robot control. Related through the robot control lens but the connection to RL is tangential. The main contribution is in hierarchical skill composition.

**#20 Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control (2601.16163) -- 0.607**
Video foundation models adapted for robot policy learning. Related through the policy learning connection but is fundamentally a generative model approach, not RL. A researcher interested in RL for robotics would want to know about this as an alternative paradigm.

## Part 2: Set-Level Assessment

**Overall character:** This set reads as "robot policy learning broadly construed" rather than "RL for robotics specifically." Approximately 8-10 of the 20 papers are genuinely about RL applied to robots. The remaining 10-12 are about imitation learning, behavior cloning, VLA models, or other policy learning approaches that happen to target robotic manipulation or locomotion. The semantic centroid has collapsed the distinction between RL and other policy learning paradigms because they share vocabulary: "policy," "robot," "manipulation," "control," "sim-to-real."

**Strengths:**
- Very high topical coherence within the "robot policy learning" super-topic
- Good coverage of the sim-to-real transfer problem, which is genuinely central to RL for robotics
- Several high-discovery-value papers at the RL-VLA frontier (#11, #14) that a researcher focused on classical RL might miss

**Gaps:**
- No papers on RL reward design for robotics, which is a major subfield
- No papers on safe RL for robots (constraint satisfaction, safety guarantees)
- No papers on multi-robot RL systems beyond the seeds
- Missing the classical control + RL intersection (e.g., Lyapunov-based RL) -- though TF-IDF catches these

**False positive pattern:** Imitation learning and behavior cloning papers that share vocabulary with RL robotics but use fundamentally different training paradigms. Papers #3, #5, #9, #12, #13, #15, #20 are all in this category to varying degrees.

**Failure mode:** MiniLM centroid averages the embedding space, creating a "semantic center of mass" that drifts toward the most common vocabulary rather than the distinctive vocabulary. "Reinforcement learning" is distinctive; "robot," "policy," "manipulation" are shared with imitation learning. The centroid gravitates toward the shared terms.

## Part 4: Emergent Observations

1. **The vocabulary trap:** MiniLM appears to encode relatedness primarily through vocabulary overlap at the abstract-semantic level. The distinction between "RL for robotics" and "imitation learning for robotics" is conceptual (different training paradigms) but not strongly reflected in the embedding space, because the papers discuss similar problems, tasks, and evaluation methods. This is a fundamental limitation of general-purpose sentence embeddings for domain-specific recommendation: they capture surface similarity, not methodological similarity.

2. **Score compression:** The top-20 scores span only 0.053 (0.660 to 0.607). This is a very narrow band, suggesting that many papers beyond the top-20 have nearly identical scores. The strategy is not making fine-grained relevance distinctions -- it is finding a cluster of ~100+ papers that all "look like RL for robotics" and then the ranking within that cluster is essentially noise.

3. **Held-out paper failure:** Zero held-out papers recovered. This is notable because the held-out papers include things like "Hybrid Motion Planning with Deep RL for Mobile Robot Navigation" and "Reinforcement learning with timed constraints for robotics motion planning" -- papers that should be easy to find. This suggests the centroid is slightly mispositioned relative to the broader profile, possibly because the seeds over-represent certain sub-topics (flow matching, locomotion) relative to others (mobile robot navigation, constraint satisfaction).

4. **The VLA/foundation model magnet:** Multiple papers (#11, #14, #17, #20) are about applying large foundation models to robot control. This is probably the hottest topic in robotics right now, so these papers are numerous in the corpus. The centroid picks them up because they overlap in vocabulary, but they represent a different research program from classical RL for robotics. Whether this is a false positive or a valuable discovery depends on the researcher's openness to adjacent paradigms.

## Part 5: Metric Divergence

The 0/5 held-out recovery is concerning given MiniLM's high LOO-MRR (0.398). This suggests the MRR was measured on clusters that are well-aligned with MiniLM's similarity structure (because they were defined by MiniLM embeddings), but real research interests may cross cluster boundaries in ways that the MRR evaluation does not capture. The profile papers that MiniLM does find are the ones closest to the centroid in embedding space, which is circular -- it finds the papers that are most similar to the centroid by the same metric used to define the centroid.

The qualitative impression is that MiniLM produces a competent but shallow set: topically coherent, but unable to distinguish between RL and other policy learning paradigms. A researcher would find useful papers here, but would also spend time filtering out imitation learning papers they do not need.
