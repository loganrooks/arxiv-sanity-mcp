# Single-Strategy Characterization Review

**Model:** voyage
**Profile:** RL for robotics (P1)
**Depth:** full
**Overlap with MiniLM:** 18/20 shared, 2 unique to voyage

## Seed Papers
  - [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning (cs.AI)
  - [2601.20668] GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control (cs.RO)
  - [2601.20846] End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting (cs.RO)
  - [2505.06357] DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition (cs.RO)
  - [2505.22094] ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning (cs.RO)

## voyage Top-20 Recommendations

### Paper 1: [2505.22094]
**Title:** ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
**Category:** cs.RO
**Score:** 0.8877
**In MiniLM top-20:** True

### Paper 2: [2601.20668]
**Title:** GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control
**Category:** cs.RO
**Score:** 0.8674
**In MiniLM top-20:** True

### Paper 3: [2601.20846]
**Title:** End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting
**Category:** cs.RO
**Score:** 0.8655
**In MiniLM top-20:** True

### Paper 4: [2601.15761]
**Title:** Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning
**Category:** cs.AI
**Score:** 0.8600
**In MiniLM top-20:** True

### Paper 5: [2505.06357]
**Title:** DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition
**Category:** cs.RO
**Score:** 0.8560
**In MiniLM top-20:** True

### Paper 6: [2509.25756]
**Title:** SAC Flow: Sample-Efficient Reinforcement Learning of Flow-Based Policies via Velocity-Reparameterized Sequential Modeling
**Category:** cs.RO
**Score:** 0.8391
**In MiniLM top-20:** True

### Paper 7: [2505.18763]
**Title:** GenPO: Generative Diffusion Models Meet On-Policy Reinforcement Learning
**Category:** cs.LG
**Score:** 0.8386
**In MiniLM top-20:** True

### Paper 8: [2504.16680]
**Title:** Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots
**Category:** cs.RO
**Score:** 0.8311
**In MiniLM top-20:** True

### Paper 9: [2512.24698]
**Title:** Dynamic Policy Learning for Legged Robot with Simplified Model Pretraining and Model Homotopy Transfer
**Category:** cs.RO
**Score:** 0.8305
**In MiniLM top-20:** True

### Paper 10: [2601.14234]
**Title:** Q-learning with Adjoint Matching
**Category:** cs.LG
**Score:** 0.8035
**In MiniLM top-20:** True

### Paper 11: [2509.04069]
**Title:** Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep Reinforcement Learning
**Category:** cs.RO
**Score:** 0.8033
**In MiniLM top-20:** True

### Paper 12 [DIVERGENT]: [2601.18107]
**Title:** Beyond Static Datasets: Robust Offline Policy Optimization via Vetted Synthetic Transitions
**Category:** cs.LG
**Score:** 0.8000
**In MiniLM top-20:** False

### Paper 13: [2509.18631]
**Title:** Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training
**Category:** cs.RO
**Score:** 0.7977
**In MiniLM top-20:** True

### Paper 14: [2601.06748]
**Title:** On-the-Fly VLA Adaptation via Test-Time Reinforcement Learning
**Category:** cs.RO
**Score:** 0.7922
**In MiniLM top-20:** True

### Paper 15: [2512.17853]
**Title:** AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning
**Category:** cs.RO
**Score:** 0.7859
**In MiniLM top-20:** True

### Paper 16 [DIVERGENT]: [2305.19922]
**Title:** Representation-Driven Reinforcement Learning
**Category:** cs.LG
**Score:** 0.7748
**In MiniLM top-20:** False

### Paper 17: [2506.00070]
**Title:** Robot-R1: Reinforcement Learning for Enhanced Embodied Reasoning in Robotics
**Category:** cs.RO
**Score:** 0.7731
**In MiniLM top-20:** True

### Paper 18: [2505.20425]
**Title:** OSVI-WM: One-Shot Visual Imitation for Unseen Tasks using World-Model-Guided Trajectory Generation
**Category:** cs.RO
**Score:** 0.7682
**In MiniLM top-20:** True

### Paper 19: [2601.12169]
**Title:** Learning Legged MPC with Smooth Neural Surrogates
**Category:** cs.RO
**Score:** 0.7597
**In MiniLM top-20:** True

### Paper 20: [2601.00675]
**Title:** RoboReward: General-Purpose Vision-Language Reward Models for Robotics
**Category:** cs.RO
**Score:** 0.7572
**In MiniLM top-20:** True

---

## Assessment

**Limitation note:** Voyage-4 had 160/2000 papers fail to embed (8% failure rate due to API rate limiting). Zero-embedded papers receive score 0 and never appear in top-K. The effective retrieval pool is approximately 1840 papers, not 2000. This means some potentially relevant papers may be absent not because Voyage ranked them low, but because they were never embedded.

### 1. Per-Paper Assessment

**Paper 1 [2505.22094] ReinFlow** -- Direct (seed paper). Flow matching + RL for robotic control. Self-retrieval confirms embedding integrity.

**Paper 2 [2601.20668] GPO** -- Direct (seed paper). Legged robot RL with progressive action space expansion.

**Paper 3 [2601.20846] Sim-to-real RL** -- Direct (seed paper). Neural style transfer for sim-to-real policy transfer in contact-rich tasks.

**Paper 4 [2601.15761] SigEnt-SAC** -- Direct (seed paper). Off-policy actor-critic for real-world robot learning.

**Paper 5 [2505.06357] DAPPER** -- Direct (seed paper). Preference-based RL for robotic skill acquisition.

**Paper 6 [2509.25756] SAC Flow** -- Direct. Addresses the same flow-based policy + RL intersection as seed paper ReinFlow, but from the off-policy SAC perspective. Directly relevant.

**Paper 7 [2505.18763] GenPO** -- Direct. Diffusion policies for on-policy RL in robotic tasks (legged locomotion, manipulation). Strongly aligned with seeds.

**Paper 8 [2504.16680] Uncertainty-Aware World Model** -- Direct. Offline model-based RL for real robots. Addresses the same real-world deployment concern as seed SigEnt-SAC but from the model-based angle.

**Paper 9 [2512.24698] Dynamic Policy Learning** -- Direct. Legged robot locomotion via simplified-model pretraining and policy transfer. Directly extends GPO's territory.

**Paper 10 [2601.14234] QAM** -- Adjacent. Q-learning with adjoint matching for diffusion/flow policies. More of an algorithmic RL contribution than a robotics application paper, but the flow-policy connection links it firmly to the seed cluster.

**Paper 11 [2509.04069] DRLR** -- Direct. Demonstration-guided RL for robotic manipulation with real-world deployment. Core to the profile.

**Paper 12 [2601.18107] MoReBRAC** -- DIVERGENT. Adjacent. Offline RL with synthetic transition augmentation via world models. Not robotics-specific (evaluated on D4RL MuJoCo benchmarks), but the methods are directly applicable to robotic offline RL. This is a genuinely useful signal -- it surfaces a methodological advance in offline RL that a robotics-focused researcher should know about but might miss because it does not mention robots in the title. Discoverable via D4RL literature, but not trivially from a robotics-first search.

**Paper 13 [2509.18631] Sim-Real Co-Training** -- Direct. Behavior cloning with sim-to-real domain adaptation via optimal transport. Aligned with seed [2601.20846].

**Paper 14 [2601.06748] TT-VLA** -- Adjacent. Test-time RL adaptation for Vision-Language-Action models. Extends the RL-for-robotics theme toward foundation model adaptation. Relevant but more VLA-centric than pure RL.

**Paper 15 [2512.17853] AnyTask** -- Adjacent. Automated task generation for sim-to-real policy learning. More of a data/infrastructure contribution, but directly enables RL-based robotic learning.

**Paper 16 [2305.19922] Representation-Driven RL** -- DIVERGENT. Adjacent/Provocative. A theoretical RL paper about policy representation and exploration-exploitation tradeoffs. Not robotics-specific at all -- no robotic experiments, no sim-to-real. The connection is purely that it addresses RL representation, which is foundational to the methods used in robotics RL. This is a weaker divergent signal: a researcher focused on RL for robotics would only care about this paper if they had theoretical inclinations. Discoverable via general RL theory literature.

**Paper 17 [2506.00070] Robot-R1** -- Adjacent. RL-enhanced embodied reasoning for robot control via LVLMs. Connects RL to foundation models for robotics, a growing subfield.

**Paper 18 [2505.20425] OSVI-WM** -- Adjacent. One-shot visual imitation with world models. Not strictly RL but closely related (world model-guided policy generation). Relevant to the broader research neighborhood.

**Paper 19 [2601.12169] Legged MPC** -- Adjacent. Neural surrogates for model predictive control in legged robots. Not RL per se, but addresses the same legged locomotion control problem from the MPC angle. Interesting complement.

**Paper 20 [2601.00675] RoboReward** -- Adjacent. Vision-language reward models for robotic RL. Addresses the reward specification problem, which is central to RL deployment in robotics.

### 2. Set-Level Assessment

**Landscape coverage:** This set maps the RL-for-robotics landscape reasonably well. It covers:
- Policy optimization methods: flow-based (ReinFlow, SAC Flow, GenPO, QAM), PPO variants (GPO, model-based pipelines), off-policy (SigEnt-SAC, DRLR)
- Real-world deployment: sim-to-real transfer (multiple papers), offline learning, test-time adaptation
- Robotic domains: legged locomotion (multiple papers), manipulation, and industrial tasks
- Learning paradigms: online RL, offline RL, preference-based RL, imitation + RL hybrids
- Reward specification: VLM-based rewards, sparse reward shaping

**Coverage gaps:**
- Multi-agent RL for robotics is absent
- Hierarchical RL / long-horizon task planning is underrepresented
- Safety-aware RL for robotics (constraint satisfaction, safe exploration) is not present despite its importance
- Older foundational work (e.g., domain randomization origins, curriculum learning theory) is absent -- expected given recency bias in the corpus

**Shared vs. divergent character:** The 18 shared papers are overwhelmingly direct hits -- robotics RL papers with experimental validation on real or simulated robots. The 2 divergent papers split: one (MoReBRAC) is a methodological advance in offline RL that a robotics researcher would find useful, while the other (Representation-Driven RL) is more theoretical and less immediately applicable.

### 3. Emergent Observations

**Signal character:** Voyage captures essentially the same signal as MiniLM on this profile, with 18/20 overlap. The divergence is minimal and mixed in quality. MoReBRAC (paper 12) represents Voyage detecting a methodological RL paper relevant to robotics applications, which is a coherent and mildly useful signal. Representation-Driven RL (paper 16) is more of a vocabulary match on "reinforcement learning" + "representation" without strong robotics relevance.

**Divergence quality:** The divergence signal is thin but not noise. With only 2 unique papers, there is insufficient evidence to characterize a distinctive Voyage retrieval signature on this profile.

**Productive provocations:** MoReBRAC could serve as a productive provocation for a researcher focused on online RL -- it demonstrates that offline methods with synthetic augmentation can work in regimes where online interaction is expensive, which is precisely the robotics deployment scenario.

### 4. Absent Researcher Note

To properly assess this recommendation set, I would need to know:
- Whether the researcher works primarily on legged locomotion, manipulation, or both (the set is legged-heavy)
- Their position on the theory-practice spectrum: the theoretical RL papers (QAM, Representation-Driven RL) would be more valuable to someone contributing to RL methods than to someone focused on systems integration
- Whether they are interested in foundation model + RL integration (several papers address VLA/LLM + RL connections)
- Whether they work with real hardware or primarily in simulation (this shapes whether offline and sim-to-real papers are central or peripheral)

### 5. Metric Divergence Flags

**No significant divergence.** With J@20 near 1.0 (18/20 overlap), the quantitative metrics predict very high agreement with MiniLM, and the qualitative review confirms this. The shared papers are almost entirely direct hits for the profile. The 2 divergent papers are both legitimate RL-adjacent papers, not noise, consistent with the quantitative picture of near-identical retrieval behavior on this profile.

The high overlap is consistent with P1 being a well-defined, tightly scoped profile (RL + robotics) where all models converge on the same obvious papers. This profile does not exercise the models' ability to find non-obvious connections.
