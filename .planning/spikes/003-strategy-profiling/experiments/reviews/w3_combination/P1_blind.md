# W3 Blind Pairwise Comparison: P1 (RL for Robotics)

**Profile breadth**: Medium
**Overlap**: 12 consensus / 8 A-only / 8 B-only (60% overlap)

## Seed Papers

The profile is defined by five papers covering:
1. Offline model-based RL for real robots (uncertainty-aware world models)
2. RL reasoning for embodied robotics (vision-language + RL)
3. Flow-based policy optimization (off-policy actor-critic)
4. Deep RL for magnetic robot navigation in GI tract
5. Growing policy optimization for legged locomotion

The interest is clearly **RL applied to physical robot control** -- not pure RL theory, not pure robotics engineering without learning. The sweet spot is the intersection: algorithms that learn control policies for real or realistic robotic systems. There is a secondary thread of flow/diffusion-based policy representations.

---

## Part 1: Per-Paper Assessment

### Strategy A

1. **ReinFlow: Fine-tuning Flow Matching Policy with Online RL** (CONSENSUS, 0.819) -- Directly on-topic. Flow matching + RL for continuous robotic control. Same method family as seed 3.

2. **Scalable Exploration for High-Dimensional Continuous Control via Value-Guided Flow** (CONSENSUS, 0.800) -- On-topic. RL exploration for high-dimensional robot-like systems. Addresses a core challenge (exploration in large action spaces) relevant to all seeds.

3. **Efficiently Learning Robust Torque-based Locomotion Through Reinforcement** (CONSENSUS, 0.800) -- On-topic. Residual RL for bipedal locomotion. Same community as seed 5.

4. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning** (CONSENSUS, 0.787) -- On-topic. Real-world RL with demonstrations and human feedback. Addresses the practical deployment challenges visible in seeds 1 and 4.

5. **One Step Is Enough: Dispersive MeanFlow Policy Optimization** (CONSENSUS, 0.787) -- On-topic. Flow matching for real-time robotic control. Same method cluster as seed 3 and paper 1.

6. **Bootstrap Off-policy with World Model (BOOM)** (A-ONLY, 0.781) -- Relevant. Model-based RL with planning, evaluated on DeepMind Control Suite and Humanoid-Bench. The connection to robotics is through control benchmarks rather than actual robots, making it slightly less directly relevant than the consensus papers but still within scope.

7. **Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep RL** (CONSENSUS, 0.780) -- On-topic. RL with demonstrations for robotics. Squarely in the intersection.

8. **Learning on the Fly: Rapid Policy Adaptation via Differentiable Simulation** (CONSENSUS, 0.780) -- On-topic. Sim-to-real transfer through differentiable simulation. Addresses the practical deployment gap.

9. **Learning Diffusion Policy from Primitive Skills for Robot Manipulation** (A-ONLY, 0.778) -- On-topic. Diffusion policies for robotic manipulation with skill decomposition. Strong connection to the flow/diffusion policy thread.

10. **Real-world RL from Suboptimal Interventions** (CONSENSUS, 0.768) -- On-topic. Real-world RL for dexterous manipulation. Very practical, directly in the seed interest.

11. **Learning Legged MPC with Smooth Neural Surrogates** (A-ONLY, 0.766) -- On-topic. Learned dynamics models for legged MPC. Directly connects to seed 5 (legged locomotion) and seed 1 (model-based approaches).

12. **Towards Space-Based Environmentally-Adaptive Grasping** (A-ONLY, 0.758) -- Relevant but peripheral. RL-based grasping in space environments. The RL component is present but the emphasis is on the application domain rather than the RL methodology.

13. **Controllable Flow Matching for Online RL** (CONSENSUS, 0.758) -- On-topic. Flow matching as environment dynamics model for MBRL. Same method family.

14. **Learning Diverse Skills for Behavior Models with Mixture of Experts** (A-ONLY, 0.758) -- Partially relevant. Imitation learning (not RL) for robotic manipulation. The connection is through the broader robot policy learning space, but this is behavior cloning, not reinforcement learning. Borderline.

15. **Masked Generative Policy for Robotic Control** (A-ONLY, 0.757) -- Partially relevant. Another imitation learning method for robotic manipulation. Same issue as 14: the robot manipulation component is present, but the RL component is absent. This is visuomotor imitation learning.

16. **Breaking Task Impasses Quickly: Adaptive Neuro-Symbolic Learning for Open-World Robotics** (A-ONLY, 0.753) -- Relevant. Hybrid TAMP + RL for robotics. The RL component is there, but the emphasis is on the neuro-symbolic integration rather than the RL methodology.

17. **PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies** (CONSENSUS, 0.749) -- Relevant. Benchmarking infrastructure for robot policies. Not directly about RL methods but about evaluating the policies they produce. Useful to a researcher in this space.

18. **Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training** (CONSENSUS, 0.748) -- Relevant. Sim-to-real transfer for behavior cloning. Again not RL per se but addresses the sim-to-real gap that is central to seeds 1, 3, and 5.

19. **AnyTask: Automated Task and Data Generation for Sim-to-Real Policy Learning** (CONSENSUS, 0.745) -- Relevant. Simulation infrastructure for robot learning. Same situation as 17 and 18.

20. **Value Vision-Language-Action Planning & Search** (A-ONLY, 0.741) -- Partially relevant. VLA models with MCTS for robotic manipulation. The planning/search component connects loosely to RL, but this is more about augmenting pretrained VLA models than about RL proper.

### Strategy B

1. **Learning on the Fly: Rapid Policy Adaptation via Differentiable Simulation** (CONSENSUS, 0.030) -- On-topic. (Same assessment as A-8.)

2. **Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep RL** (CONSENSUS, 0.029) -- On-topic. (Same assessment as A-7.)

3. **Efficiently Learning Robust Torque-based Locomotion** (CONSENSUS, 0.028) -- On-topic. (Same assessment as A-3.)

4. **GenPO: Generative Diffusion Models Meet On-Policy RL** (B-ONLY, 0.028) -- On-topic. Diffusion policies integrated with on-policy PPO. Evaluated on legged locomotion and manipulation in IsaacLab. Directly connects to both the flow/diffusion policy thread and the robotics applications in the seeds.

5. **AnyTask: Automated Task and Data Generation** (CONSENSUS, 0.027) -- Relevant. (Same assessment as A-19.)

6. **ReinFlow: Fine-tuning Flow Matching Policy with Online RL** (CONSENSUS, 0.027) -- On-topic. (Same assessment as A-1.)

7. **Real-world RL from Suboptimal Interventions** (CONSENSUS, 0.027) -- On-topic. (Same assessment as A-10.)

8. **Learning Quadrotor Control From Visual Features Using Differentiable Simulation** (B-ONLY, 0.027) -- On-topic. RL vs. differentiable simulation for quadrotor control. Directly relevant: RL applied to a specific robotic platform with practical considerations.

9. **Scalable Exploration for High-Dimensional Continuous Control** (CONSENSUS, 0.026) -- On-topic. (Same assessment as A-2.)

10. **One Step Is Enough: Dispersive MeanFlow Policy Optimization** (CONSENSUS, 0.026) -- On-topic. (Same assessment as A-5.)

11. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy** (CONSENSUS, 0.026) -- On-topic. (Same assessment as A-4.)

12. **PolaRiS: Scalable Real-to-Sim Evaluations** (CONSENSUS, 0.025) -- Relevant. (Same assessment as A-17.)

13. **pi_0: A Vision-Language-Action Flow Model for General Robot Control** (B-ONLY, 0.025) -- Partially relevant. This is a major foundation model paper for robot control using flow matching, but it is primarily about pre-training and behavior cloning at scale, not RL. The connection to the seeds is through the flow matching architecture and the robotics application, but the learning paradigm is different.

14. **Controllable Flow Matching for Online RL** (CONSENSUS, 0.025) -- On-topic. (Same assessment as A-13.)

15. **Disentangling perception and reasoning for cloth manipulation** (B-ONLY, 0.024) -- Relevant. RL for cloth manipulation with modular perception. The RL component is there but the emphasis is on efficient representation rather than the RL algorithm.

16. **Cosmos Policy: Fine-Tuning Video Models for Visuomotor Control** (B-ONLY, 0.024) -- Partially relevant. Video model adapted for robot control. Not RL-centric but connects to the broader robot policy learning space. The planning component has RL-adjacent flavor.

17. **Failure-Aware RL: Reliable Offline-to-Online RL with Self-Recovery** (B-ONLY, 0.023) -- On-topic. Offline-to-online RL for real-world manipulation with safety considerations. Directly in the seed interest (practical RL for real robots).

18. **Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training** (CONSENSUS, 0.023) -- Relevant. (Same assessment as A-18.)

19. **Vlaser: Vision-Language-Action Model with Synergistic Embodied Reasoning** (B-ONLY, 0.022) -- Marginally relevant. VLA foundation model with embodied reasoning. The connection to RL is thin -- this is about VLM-based reasoning for robot control, not RL training.

20. **SOP: Scalable Online Post-Training System for VLA Models** (B-ONLY, 0.022) -- Partially relevant. Online post-training of VLA models including RL (RECAP). There is an RL component in the post-training loop, but the primary contribution is the systems infrastructure for scaling VLA training.

---

## Part 2: Set-Level Assessment

### Strategy A

**Overall character**: Strategy A delivers a focused set centered on RL algorithms applied to robotic control, with particular strength in the flow/diffusion policy sub-community. The top half (ranks 1-10) is consistently on-topic with direct connections to the seeds. The bottom half drifts toward imitation learning and broader robot policy methods that share the robotics application but not the RL methodology.

**Strengths**: (1) Strong coverage of the flow/diffusion-based RL policy cluster, which is a clear thread in the seeds. (2) Good representation of model-based RL approaches (BOOM, CtrlFlow). (3) Captures practical concerns: sim-to-real, real-world deployment, locomotion.

**Gaps**: (1) No representation of medical/navigation robotics (seed 4 is about GI tract navigation). (2) Thin on the safety/robustness considerations present in seed 1 (uncertainty-aware models). (3) The bottom quartile drifts into imitation learning territory.

**False positive pattern**: Papers 14, 15, and 20 are imitation learning or VLA papers that share the robotics application domain but not the RL methodology. This is a vocabulary-overlap pattern: "robot manipulation" and "policy" match the seed vocabulary but the learning paradigm is different.

### Strategy B

**Overall character**: Strategy B delivers a broader set that mixes core RL-for-robotics papers with a significant number of VLA/foundation model papers for robot control. The consensus papers appear at slightly different ranks than in A, and the B-only papers trend toward larger-scale, more recent paradigms (pi_0, Cosmos, Vlaser, SOP).

**Strengths**: (1) Surfaces GenPO and quadrotor control (both clearly on-topic) that A missed. (2) Failure-Aware RL is an excellent find -- directly relevant to the practical deployment emphasis in the seeds. (3) Broader view of the robot policy learning ecosystem.

**Gaps**: (1) More dilution from non-RL papers (pi_0, Cosmos, Vlaser, SOP are primarily not RL). (2) The bottom quartile is weaker than A's bottom quartile in terms of direct RL relevance. (3) Same gap as A: no medical/navigation robotics coverage.

**False positive pattern**: Papers 13, 16, 19, and 20 are foundation model / VLA papers. These represent a systematic bias toward the "general robot control" community rather than the "RL for robotics" community. The connection is real but loose.

---

## Part 3: Comparative Assessment

**What A found that B missed**: Learning Legged MPC (neural surrogates for MPC, directly relevant to locomotion seeds), BOOM (model-based RL with planning), SDP (skill-conditioned diffusion policies). These are methodologically closer to the RL core of the seed interest.

**What B found that A missed**: GenPO (diffusion+on-policy RL -- arguably the most directly relevant exclusive find in either set), quadrotor control via differentiable simulation, Failure-Aware RL (practical safety for real-world RL). These are also strong finds, with GenPO being the standout.

**Where they agree**: The 12 consensus papers form a coherent and high-quality core covering flow-matching RL policies, exploration in continuous control, locomotion, real-world RL, sim-to-real transfer, and benchmarking. Agreement indicates these papers are robustly retrievable regardless of strategy.

**Character of errors**: Strategy A's errors trend toward imitation learning papers that share the robotics domain (method-adjacent drift). Strategy B's errors trend toward large-scale foundation models for robots that are not trained with RL (paradigm-adjacent drift). Neither error pattern is catastrophic, but they reveal different retrieval biases.

**If a researcher could only use one**: For a researcher specifically interested in RL algorithms for robotics, Strategy A is slightly better. Its exclusive papers are methodologically closer to the seed interest (legged MPC, model-based RL, skill-conditioned policies). Strategy B's best exclusive find (GenPO) is excellent, but its other exclusives are diluted by VLA/foundation model papers. However, if the researcher's interest has evolved toward the broader "learned robot policies" space (which is where the field is moving), Strategy B's breadth would be more informative.

---

## Part 4: Emergent Observations

1. **The flow/diffusion policy cluster is over-represented**: Both strategies surface many papers about flow matching and diffusion for robot control. This is partly because seed 3 (SAC Flow) anchors this community, but it creates a bias toward one methodological family at the expense of other RL approaches (e.g., hierarchical RL, multi-agent RL for robotics, reward learning).

2. **The medical robotics seed (seed 4) is orphaned**: Neither strategy finds anything related to RL for medical devices or GI tract navigation. This seed appears to be an outlier relative to the other four, and neither strategy handles minority interests in the seed set.

3. **The B-only papers reveal a temporal bias**: pi_0, Cosmos Policy, Vlaser, and SOP represent the current wave of foundation-model-based robot policies. Strategy B appears to be surfacing more recent / trending work at the cost of methodological precision.

4. **Rank ordering within consensus differs meaningfully**: Strategy A puts ReinFlow at rank 1; Strategy B puts Learning on the Fly at rank 1. The reordering suggests different weighting of similarity features. A appears to weight methodological similarity more heavily (flow matching); B appears to weight application similarity more heavily (sim-to-real practical deployment).

---

## Part 5: Metric Divergence

The quantitative metrics said Strategy B (the fusion) performed worse than Strategy A (standalone). Qualitatively, this verdict **mostly holds** for P1, but with an important caveat.

**Where metrics are right**: Strategy A's top-10 is more consistently on-topic. Fewer false positives. The exclusive papers in A (especially legged MPC, BOOM) are methodologically closer to the seed interest.

**Where the story is more nuanced**: Strategy B found GenPO, which is arguably the single most relevant exclusive paper across both sets. It also found Failure-Aware RL, which addresses a practical concern (safety during real-world RL) that none of the A-only papers touch. If MRR penalizes B for having these papers at less optimal ranks while rewarding A for a tighter top-5, the metric correctly captures ranking precision but misses that B's best exclusive finds are individually stronger than A's worst exclusives.

**Net assessment**: The quantitative verdict holds. Strategy B does not "feel" better in practice for P1. Its strengths are real but insufficient to overcome the dilution from VLA/foundation model papers.
