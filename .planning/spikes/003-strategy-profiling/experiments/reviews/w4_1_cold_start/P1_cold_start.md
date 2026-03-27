# W4.1 Cold-Start Review: P1 (RL for Robotics / Medium Breadth)

## Profile Context

P1 targets reinforcement learning for robotics -- a medium-breadth topic that spans offline/online RL, sim-to-real transfer, model-based methods, locomotion, manipulation, and embodied reasoning. This breadth means the seed signal has to cover a fairly large conceptual territory.

---

## 1-Seed Condition

**Seed paper:** "Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots"

This seed is highly specific: offline model-based RL with uncertainty-aware world models, evaluated on physical robots (quadruped, humanoid). Key concepts: MBRL, world models, epistemic uncertainty, PPO, sim-to-real, manipulation/locomotion.

### Part 1: Per-Paper Assessment

#### MiniLM (1 seed)

1. **Learning on the Fly: Rapid Policy Adaptation via Differentiable Simulation** -- Directly relevant. Sim-to-real policy adaptation for quadrotor control. Would help refine: "yes" narrows toward sim-to-real transfer; "no" signals user cares more about offline methods specifically. Good cold-start probe.

2. **Efficiently Learning Robust Torque-based Locomotion Through Reinforcement with Model-Based Supervision** -- Highly relevant. Model-based + RL for bipedal locomotion with sim-to-real transfer. Saying "yes" confirms interest in locomotion + model-based methods. Strong signal paper.

3. **Bayes Adaptive Monte Carlo Tree Search for Offline Model-based RL** -- Directly relevant. Same core topic (offline MBRL) with uncertainty handling via BAMDPs. "Yes" confirms the theoretical RL side; "no" signals user prefers the robotics application side.

4. **GPO: Growing Policy Optimization for Legged Robot Locomotion** -- Relevant. RL for legged robots (quadruped + hexapod) with zero-shot sim-to-real. "Yes" confirms locomotion focus; good profile-building question.

5. **Bootstrap Off-policy with World Model** -- Relevant. World model + planning + policy improvement. Less robotics-specific but hits the MBRL core. "Yes" confirms interest in world model methods broadly.

6. **A Simple Unified Uncertainty-Guided Framework for Offline-to-Online RL** -- Relevant. Uncertainty-guided offline-to-online RL. Closely matches the seed's uncertainty theme. Good refinement paper: does the user care about the offline-to-online transition specifically?

7. **ReinFlow: Fine-tuning Flow Matching Policy with Online RL** -- Relevant. Flow matching policies for robotic locomotion and manipulation with RL fine-tuning. Slightly different method family but same application area.

8. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning** -- Relevant. Real-world robot RL with sparse rewards and visual observations. "Yes" confirms interest in practical real-robot deployment.

9. **Controllable Flow Matching for Online RL** -- Moderately relevant. MBRL with flow matching for trajectory synthesis on MuJoCo benchmarks. Less robotics-specific, more RL methodology.

10. **Failure-Aware RL: Reliable Offline-to-Online RL with Self-Recovery** -- Highly relevant. Safety during real-world RL training for manipulation. Directly addresses a practical concern for the seed's real-robot theme.

11. **Beyond Static Datasets: Robust Offline Policy Optimization** -- Relevant. Offline RL with synthetic data augmentation for robotics. Matches the seed's offline MBRL focus.

12. **Real-world RL from Suboptimal Interventions** -- Relevant. Real-world RL for manipulation with human-in-the-loop. Good probe for whether user cares about human-robot interaction during training.

13. **Learning Legged MPC with Smooth Neural Surrogates** -- Relevant. MPC + learned models for legged robotics. Different control paradigm (MPC vs. pure RL) but same application domain.

14. **Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep RL** -- Relevant. RL with demonstrations for robotics tasks. Good but slightly generic.

15. **Lipschitz-Regularized Critics Lead to Policy Robustness** -- Moderately relevant. Robust RL against dynamics uncertainty. Theoretical but addresses a real concern from the seed. Would help probe: does user care about robustness theory?

16. **One Step Is Enough: Dispersive MeanFlow Policy Optimization** -- Relevant. Real-time robotic control with single-step generative policies. Addresses deployment constraints.

17. **Long-Horizon Model-Based Offline RL Without Conservatism** -- Relevant. Directly addresses offline MBRL with Bayesian approaches. Matches seed closely.

18. **Walk the PLANC: Physics-Guided RL for Agile Humanoid Locomotion** -- Relevant. RL for humanoid on constrained footholds. Matches seed's humanoid evaluation.

19. **SAC Flow: Sample-Efficient RL of Flow-Based Policies** -- Moderately relevant. RL methodology paper with robotic manipulation applications.

20. **Scalable Exploration for High-Dimensional Continuous Control** -- Moderately relevant. Exploration in high-dimensional RL, applied to biological/robotic systems.

**MiniLM 1-seed verdict:** 18/20 papers are clearly relevant to RL for robotics. The remaining 2 are still in the broader RL space and would serve as useful refinement probes. No garbage. This is a strong 1-seed performance.

#### TF-IDF (1 seed)

1. **Bayes Adaptive MCTS for Offline Model-based RL** -- Directly relevant (also in MiniLM). Offline MBRL with uncertainty.

2. **Scaling Offline Model-Based RL via Jointly-Optimized World-Action Model Pretraining** -- Directly relevant. Scaling offline MBRL -- exactly the seed's core topic.

3. **Learning on the Fly: Rapid Policy Adaptation** -- Relevant (also in MiniLM). Sim-to-real adaptation.

4. **A Simple Unified Uncertainty-Guided Framework for Offline-to-Online RL** -- Relevant (also in MiniLM). Uncertainty-guided RL.

5. **Failure-Aware RL** -- Relevant (also in MiniLM). Safety in real-world RL.

6. **Long-Horizon Model-Based Offline RL Without Conservatism** -- Relevant (also in MiniLM). Offline MBRL.

7. **Uncertainty Quantification for Deep Learning** -- Tangentially relevant. General UQ framework -- not robotics-specific. The word "uncertainty" appears in the seed and this paper was likely matched on that term. This would still help refine the profile: "no" signals user wants robotics applications, not general UQ theory.

8. **Real-world RL from Suboptimal Interventions** -- Relevant (also in MiniLM).

9. **DynaWeb: Model-Based RL of Web Agents** -- NOT relevant. Model-based RL for web browsing agents, not robotics. This is a TF-IDF failure: matched on "model-based RL" and "world model" terms without understanding the domain. A robotics researcher would find this confusing in their feed.

10. **Learning Quadrotor Control from Visual Features Using Differentiable Simulation** -- Relevant. Robotics + differentiable simulation + RL.

11. **PolaRiS: Scalable Real-to-Sim Evaluations for Generalist Robot Policies** -- Relevant. Real-to-sim benchmarking for robot policies.

12. **Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training** -- Relevant. Sim-to-real transfer for robot manipulation.

13. **Disentangling perception and reasoning for cloth manipulation** -- Moderately relevant. RL for cloth manipulation. Specific application but still robotics + RL.

14. **Towards Fast Safe Online RL via Policy Finetuning** -- Relevant. Safe online RL finetuning from offline.

15. **GenPO: Generative Diffusion Models Meet On-Policy RL** -- Moderately relevant. Diffusion-based RL policies. Less robotics-specific.

16. **STO-RL: Offline RL under Sparse Rewards via LLM-Guided Subgoal Temporal Order** -- Moderately relevant. Offline RL with LLM guidance. Novel but tangential to the seed's focus.

17. **Lipschitz-Regularized Critics** -- Moderately relevant (also in MiniLM). Robustness theory.

18. **Beyond Static Datasets** -- Relevant (also in MiniLM). Offline RL for robotics.

19. **AnyTask: Automated Task and Data Generation for Sim-to-Real** -- Relevant. Sim-to-real with automated data generation.

20. **End-to-end example-based sim-to-real RL policy transfer** -- Relevant. Sim-to-real for robotic cutting.

**TF-IDF 1-seed verdict:** 17/20 papers are relevant. DynaWeb (#9) is a clear miss -- web agents have nothing to do with robotics. Uncertainty Quantification (#7) is domain-generic. The rest are solid. TF-IDF performs well on this seed because the technical vocabulary of the seed (offline, model-based, RL, robotics, uncertainty, world model) is distinctive enough for lexical matching.

### Part 2: Set-Level Cold-Start Assessment (1 seed)

**MiniLM:** The recommendation set gives a new user a genuinely useful map of the RL-for-robotics landscape. It covers offline RL, online RL, sim-to-real, locomotion, manipulation, world models, flow matching, and safety. A researcher would look at this and think "yes, this tool understands the space I work in." The set is not too narrow (it goes beyond just offline MBRL) but not too broad (everything involves RL + physical robots or control). This is a usable set from a single seed.

**TF-IDF:** Also a usable set, with one notable failure (DynaWeb). The coverage is slightly more skewed toward offline MBRL methods and sim-to-real, which matches the seed's emphasis well. The inclusion of generic papers (UQ for deep learning, web agents) shows that TF-IDF is less able to filter by domain when terms overlap.

### Part 3: Strategy Comparison at Cold Start (1 seed)

MiniLM produces a more consistently relevant set (18/20 vs 17/20 clearly relevant). Neither strategy produces "garbage" -- even the weakest recommendations are in the right general area. The key difference: MiniLM better understands the robotics context and avoids domain confusion (no web agents). TF-IDF occasionally matches on shared terminology without domain awareness.

At 1 seed, the difference is real but not dramatic. Both strategies provide a usable starting point.

---

## 3-Seed Condition

**Seed papers:**
1. "Uncertainty-Aware Robotic World Model Makes Offline MBRL Work on Real Robots" (same as 1-seed)
2. "Robot-R1: RL for Enhanced Embodied Reasoning in Robotics" -- VLM-based embodied reasoning + RL
3. "VIKI-R: Coordinating Embodied Multi-Agent Cooperation via RL" -- Multi-agent embodied cooperation with VLMs

Adding seeds 2 and 3 dramatically shifts the profile signal. The new seeds introduce VLMs, VLAs, embodied reasoning, and multi-agent systems. This is no longer just "offline MBRL for physical robots" -- it is "RL + foundation models for embodied intelligence."

### Part 1: Per-Paper Assessment

#### MiniLM (3 seeds)

1. **Vlaser: VLA Model with Synergistic Embodied Reasoning** -- Directly relevant to seeds 2-3. VLA + embodied reasoning. Good.
2. **Unified Embodied VLM Reasoning with Robotic Action** -- Directly relevant. VLA models for open-world robotics. Good.
3. **RoboReward: Vision-Language Reward Models for Robotics** -- Relevant. VLM-based reward for RL in robotics. Bridges seeds 1 and 2-3.
4. **RoboRefer: Spatial Referring with Reasoning in VLMs for Robotics** -- Relevant to seed 2-3. Spatial reasoning for robots.
5. **Off-Policy Actor-Critic with Sigmoid-Bounded Entropy** -- Relevant to seed 1. Real-world robot RL.
6. **Causal World Modeling for Robot Control** -- Relevant. Video world models for robot learning. Bridges world models (seed 1) and embodied AI (seeds 2-3).
7. **On-the-Fly VLA Adaptation via Test-Time RL** -- Relevant. VLA + RL adaptation. Bridges both seed groups.
8. **CLARE: Continual Learning for VLA Models** -- Relevant to seeds 2-3. Continual learning for robot VLAs.
9. **Learning Diffusion Policy from Primitive Skills** -- Relevant. Diffusion policies for manipulation.
10. **RoboTracer: Spatial Trace with Reasoning in VLMs** -- Relevant to seeds 2-3.
11. **OSVI-WM: One-Shot Visual Imitation via World Models** -- Relevant. Bridges world models and imitation learning.
12. **Genie Centurion: Accelerating Real-World Robot Training** -- Relevant. VLA training efficiency.
13. **Generalizable Geometric Prior for Humanoid Manipulation** -- Relevant. Humanoid manipulation with learning.
14. **pi_0: Vision-Language-Action Flow Model** -- Highly relevant. Foundational VLA model paper.
15. **Boosting Deep RL with Semantic Knowledge for Manipulators** -- Relevant. RL + semantic knowledge for robotics.
16. **Value Vision-Language-Action Planning & Search** -- Relevant. VLA with test-time search.
17. **ConceptACT: Episode-Level Concepts for Robotic Imitation** -- Relevant. Sample-efficient imitation learning.
18. **Rethinking Video Generation Model for Embodied World** -- Relevant. Video generation for robot data.
19. **ReWorld: Multi-Dimensional Reward for Embodied World Models** -- Relevant. World models for robot learning.
20. **IVRA: Improving Visual-Token Relations for Robot Action** -- Relevant. VLA improvement method.

**MiniLM 3-seed verdict:** 20/20 relevant. However, there is a notable observation: the recommendation set has completely pivoted from the 1-seed set. The 1-seed set was dominated by offline RL, model-based methods, and sim-to-real. The 3-seed set is dominated by VLAs, VLMs, and embodied reasoning. Only 1 paper (Off-Policy Actor-Critic, #5) represents the offline/online RL methodology track from the original seed. The 2 new seeds (both about VLMs/embodied reasoning) have overwhelmed the original seed's signal. This is a profile-distortion problem: the user who started with offline MBRL now gets a feed that barely acknowledges that interest.

#### TF-IDF (3 seeds)

1. **Vlaser** -- Same as MiniLM. Relevant.
2. **pi_0** -- Relevant. VLA model.
3. **OmniEVA: Embodied Versatile Planner** -- Relevant to seeds 2-3. Embodied planning.
4. **Unified Embodied VLM Reasoning** -- Same as MiniLM. Relevant.
5. **AnyTask: Automated Task and Data Generation for Sim-to-Real** -- Relevant. Sim-to-real data generation.
6. **Explore with Long-term Memory: LLM-based RL for Embodied Exploration** -- Relevant to seeds 2-3. Embodied exploration with LLMs.
7. **InteLiPlan: Interactive LLM-Based Planner for Domestic Robots** -- Moderately relevant. LLM-based robot planning. A bit generic.
8. **Rethinking Video Generation for Embodied World** -- Same as MiniLM. Relevant.
9. **Bayes Adaptive MCTS for Offline Model-based RL** -- Relevant to seed 1. This is a good sign -- TF-IDF retains some signal from the original seed.
10. **ReWorld: Multi-Dimensional Reward for Embodied World Models** -- Same as MiniLM. Relevant.
11. **SimWorld-Robotics: Synthesizing Urban Environments for Robot Navigation** -- Moderately relevant. Simulation for robotics but focused on urban navigation.
12. **RoboReward** -- Same as MiniLM. Relevant.
13. **VLM4VLA: Revisiting VLMs in VLA Models** -- Relevant to seeds 2-3.
14. **EduSim-LLM: Educational Platform with LLMs and Robot Simulation** -- Weakly relevant. Educational robotics platform. Not research-level for this profile.
15. **UserLM-R1: Modeling Human Reasoning in User Language Models** -- NOT relevant. User simulator for agent training. No robotics connection. TF-IDF failure: matched on "R1" and "reinforcement learning" terms.
16. **DeepSeek-R1 Thoughtology** -- NOT relevant. LLM reasoning analysis. No robotics connection. Another term-matching failure on "R1" and "reasoning."
17. **Alpamayo-R1: Reasoning and Action for Autonomous Driving** -- Weakly relevant. Autonomous driving, not robotics manipulation/locomotion. Tangential.
18. **Proprioception Enhances VLM for Robot Task Captions** -- Relevant. VLMs + robot proprioception.
19. **Scaling Offline Model-Based RL** -- Relevant to seed 1.
20. **H2R: Human-to-Robot Data Augmentation for Pre-training** -- Relevant. Robot learning from video.

**TF-IDF 3-seed verdict:** 15/20 clearly relevant, 3 weakly relevant, 2 clear misses. The misses (UserLM-R1, DeepSeek-R1) are particularly telling -- they show TF-IDF matching on "R1" as a token from the seed paper titles, which is completely spurious. On the positive side, TF-IDF retains better coverage of the original seed's focus area (Bayes MCTS, Scaling Offline MBRL) than MiniLM does.

### Part 2: Set-Level Cold-Start Assessment (3 seeds)

**MiniLM:** The set is high-quality (20/20 relevant) but has over-rotated toward the VLA/embodied-reasoning theme introduced by seeds 2-3. A researcher who started with offline MBRL and then added two VLA papers would likely find this set useful but might wonder why their original interest has been almost entirely abandoned. The set gives a coherent view of "VLMs/VLAs for robotics" but loses the "RL methodology for robot control" thread.

**TF-IDF:** Lower precision (15/20) but better balance across the seed themes. It retains some offline MBRL papers alongside the VLA papers. The 2 clear misses are embarrassing (DeepSeek-R1 reasoning? UserLM?) and would undermine user confidence. A researcher seeing these would think "this tool doesn't really understand what I want."

### Part 3: Strategy Comparison at Cold Start (3 seeds)

MiniLM wins on precision (20/20 vs 15/20) but loses on balance. TF-IDF is more susceptible to spurious term matches ("R1") but better at preserving representation of all seed themes. Neither strategy handles the 1-to-3 seed transition gracefully: MiniLM over-indexes on the majority signal (2/3 seeds are VLA-focused), while TF-IDF picks up token noise.

### Part 4: Emergent Observations

**Seed specificity matters more than strategy at 1 seed.** The single seed paper happens to use very distinctive technical vocabulary (offline MBRL, world models, uncertainty, real robots), which works well for both strategies. A more generic seed (e.g., "RL for robots" without the specific method) might produce worse results.

**The 1-to-3 transition reveals a fundamental cold-start problem.** When 2 of 3 seeds share a different sub-theme (VLAs) than the original seed (offline MBRL), the aggregate profile shifts dramatically. Both strategies lose track of the original interest. This suggests the system should weight seeds by recency or let users mark which seed best represents their core interest.

**MiniLM's semantic similarity creates coherent but narrow recommendation sets.** At 3 seeds, MiniLM effectively builds a "nearest semantic neighborhood" that is self-consistent but may not represent the full breadth of the user's evolving interests.

### Part 5: Metric Divergence

The quantitative claim that "MiniLM works from 1 seed" is validated. The 1-seed recommendations are genuinely useful -- a researcher could start working with this feed immediately. However, "works" needs qualification: it works because this specific seed has distinctive enough vocabulary/semantics to anchor the recommendations. Whether MiniLM would work as well from a vague or interdisciplinary seed is an open question.

The 3-seed MiniLM set is higher precision but arguably less useful for profile-building because it has collapsed around the majority theme. For cold-start profile bootstrapping, the 1-seed set may actually be more valuable because it covers more of the space the user might want to explore.
