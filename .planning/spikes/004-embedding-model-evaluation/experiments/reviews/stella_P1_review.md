# Single-Strategy Characterization Review

**Model:** stella
**Profile:** RL for robotics (P1)
**Depth:** full
**Overlap with MiniLM:** 17/20 shared, 3 unique to stella

## Seed Papers
  - [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning (cs.AI)
  - [2601.20668] GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control (cs.RO)
  - [2601.20846] End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting (cs.RO)
  - [2505.06357] DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition (cs.RO)
  - [2505.22094] ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning (cs.RO)

## stella Top-20 Recommendations

### Paper 1: [2505.22094]
**Title:** ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
**Category:** cs.RO
**Score:** 0.9009
**In MiniLM top-20:** True

We propose ReinFlow, a simple yet effective online reinforcement learning (RL) framework that fine-tunes a family of flow matching policies for continuous robotic control. Derived from rigorous RL theory, ReinFlow injects learnable noise into a flow policy's deterministic path, converting the flow into a discrete-time Markov Process for exact and straightforward likelihood computation. This conversion facilitates exploration and ensures training stability, enabling ReinFlow to fine-tune diverse flow model variants, including Rectified Flow [35] and Shortcut Models [19], particularly at very few or even one denoising step. We benchmark ReinFlow in representative locomotion and manipulation tasks, including long-horizon planning with visual input and sparse reward. The episode reward of Rectified Flow policies obtained an average net growth of 135.36% after fine-tuning in challenging legged locomotion tasks while saving denoising steps and 82.63% of wall time compared to state-of-the-art diffusion RL fine-tuning method DPPO [43]. The success rate of the Shortcut Model policies in state and visual manipulation tasks achieved an average net increase of 40.34% after fine-tuning with ReinFlow at four or even one denoising step, whose performance is comparable to fine-tuned DDIM policies while saving computation time for an average of 23.20%. Project webpage: https://reinflow.github.io/

### Paper 2: [2601.15761]
**Title:** Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning
**Category:** cs.AI
**Score:** 0.8950
**In MiniLM top-20:** True

Deploying reinforcement learning in the real world remains challenging due to sample inefficiency, sparse rewards, and noisy visual observations. Prior work leverages demonstrations and human feedback to improve learning efficiency and robustness. However, offline-to-online methods need large datasets and can be unstable, while VLA-assisted RL relies on large-scale pretraining and fine-tuning. As a result, a low-cost real-world RL method with minimal data requirements has yet to emerge. We introduce \textbf{SigEnt-SAC}, an off-policy actor-critic method that learns from scratch using a single expert trajectory. Our key design is a sigmoid-bounded entropy term that prevents negative-entropy-driven optimization toward out-of-distribution actions and reduces Q-function oscillations. We benchmark SigEnt-SAC on D4RL tasks against representative baselines. Experiments show that SigEnt-SAC substantially alleviates Q-function oscillations and reaches a 100\% success rate faster than prior methods. Finally, we validate SigEnt-SAC on four real-world robotic tasks across multiple embodiments, where agents learn from raw images and sparse rewards; results demonstrate that SigEnt-SAC can learn successful policies with only a small number of real-world interactions, suggesting a low-cost and practical pathway for real-world RL deployment.

### Paper 3: [2601.20668]
**Title:** GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control
**Category:** cs.RO
**Score:** 0.8846
**In MiniLM top-20:** True

Training reinforcement learning (RL) policies for legged robots remains challenging due to high-dimensional continuous actions, hardware constraints, and limited exploration. Existing methods for locomotion and whole-body control work well for position-based control with environment-specific heuristics (e.g., reward shaping, curriculum design, and manual initialization), but are less effective for torque-based control, where sufficiently exploring the action space and obtaining informative gradient signals for training is significantly more difficult. We introduce Growing Policy Optimization (GPO), a training framework that applies a time-varying action transformation to restrict the effective action space in the early stage, thereby encouraging more effective data collection and policy learning, and then progressively expands it to enhance exploration and achieve higher expected return. We prove that this transformation preserves the PPO update rule and introduces only bounded, vanishing gradient distortion, thereby ensuring stable training. We evaluate GPO on both quadruped and hexapod robots, including zero-shot deployment of simulation-trained policies on hardware. Policies trained with GPO consistently achieve better performance. These results suggest that GPO provides a general, environment-agnostic optimization framework for learning legged locomotion.

### Paper 4: [2505.06357]
**Title:** DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition
**Category:** cs.RO
**Score:** 0.8753
**In MiniLM top-20:** True

Preference-based Reinforcement Learning (PbRL) enables policy learning through simple queries comparing trajectories from a single policy. While human responses to these queries make it possible to learn policies aligned with human preferences, PbRL suffers from low query efficiency, as policy bias limits trajectory diversity and reduces the number of discriminable queries available for learning preferences. This paper identifies preference discriminability, which quantifies how easily a human can judge which trajectory is closer to their ideal behavior, as a key metric for improving query efficiency. To address this, we move beyond comparisons within a single policy and instead generate queries by comparing trajectories from multiple policies, as training them from scratch promotes diversity without policy bias. We propose Discriminability-Aware Policy-to-Policy Preference-Based Efficient Reinforcement Learning (DAPPER), which integrates preference discriminability with trajectory diversification achieved by multiple policies. DAPPER trains new policies from scratch after each reward update and employs a discriminator that learns to estimate preference discriminability, enabling the prioritized sampling of more discriminable queries. During training, it jointly maximizes the preference reward and preference discriminability score, encouraging the discovery of highly rewarding and easily distinguishable policies. Experiments in simulated and real-world legged robot environments demonstrate that DAPPER outperforms previous methods in query efficiency, particularly under challenging preference discriminability conditions. A supplementary video that facilitates understanding of the proposed framework and its experimental results is available at: https://youtu.be/lRwX8FNN8n4

### Paper 5: [2601.20846]
**Title:** End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting
**Category:** cs.RO
**Score:** 0.8667
**In MiniLM top-20:** True

Whereas reinforcement learning has been applied with success to a range of robotic control problems in complex, uncertain environments, reliance on extensive data - typically sourced from simulation environments - limits real-world deployment due to the domain gap between simulated and physical systems, coupled with limited real-world sample availability. We propose a novel method for sim-to-real transfer of reinforcement learning policies, based on a reinterpretation of neural style transfer from image processing to synthesise novel training data from unpaired unlabelled real world datasets. We employ a variational autoencoder to jointly learn self-supervised feature representations for style transfer and generate weakly paired source-target trajectories to improve physical realism of synthesised trajectories. We demonstrate the application of our approach based on the case study of robot cutting of unknown materials. Compared to baseline methods, including our previous work, CycleGAN, and conditional variational autoencoder-based time series translation, our approach achieves improved task completion time and behavioural stability with minimal real-world data. Our framework demonstrates robustness to geometric and material variation, and highlights the feasibility of policy adaptation in challenging contact-rich tasks where real-world reward information is unavailable.

### Paper 6: [2509.04069]
**Title:** Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep Reinforcement Learning
**Category:** cs.RO
**Score:** 0.8550
**In MiniLM top-20:** True

This paper proposes an exploration-efficient Deep Reinforcement Learning with Reference policy (DRLR) framework for learning robotics tasks that incorporates demonstrations. The DRLR framework is developed based on an algorithm called Imitation Bootstrapped Reinforcement Learning (IBRL). We propose to improve IBRL by modifying the action selection module. The proposed action selection module provides a calibrated Q-value, which mitigates the bootstrapping error that otherwise leads to inefficient exploration. Furthermore, to prevent the RL policy from converging to a sub-optimal policy, SAC is used as the RL policy instead of TD3. The effectiveness of our method in mitigating bootstrapping error and preventing overfitting is empirically validated by learning two robotics tasks: bucket loading and open drawer, which require extensive interactions with the environment. Simulation results also demonstrate the robustness of the DRLR framework across tasks with both low and high state-action dimensions, and varying demonstration qualities. To evaluate the developed framework on a real-world industrial robotics task, the bucket loading task is deployed on a real wheel loader. The sim2real results validate the successful deployment of the DRLR framework.

### Paper 7: [2509.25756]
**Title:** SAC Flow: Sample-Efficient Reinforcement Learning of Flow-Based Policies via Velocity-Reparameterized Sequential Modeling
**Category:** cs.RO
**Score:** 0.8521
**In MiniLM top-20:** True

Training expressive flow-based policies with off-policy reinforcement learning is notoriously unstable due to gradient pathologies in the multi-step action sampling process. We trace this instability to a fundamental connection: the flow rollout is algebraically equivalent to a residual recurrent computation, making it susceptible to the same vanishing and exploding gradients as RNNs. To address this, we reparameterize the velocity network using principles from modern sequential models, introducing two stable architectures: Flow-G, which incorporates a gated velocity, and Flow-T, which utilizes a decoded velocity. We then develop a practical SAC-based algorithm, enabled by a noise-augmented rollout, that facilitates direct end-to-end training of these policies. Our approach supports both from-scratch and offline-to-online learning and achieves state-of-the-art performance on continuous control and robotic manipulation benchmarks, eliminating the need for common workarounds like policy distillation or surrogate objectives.

### Paper 8: [2504.16680]
**Title:** Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots
**Category:** cs.RO
**Score:** 0.8464
**In MiniLM top-20:** True

Reinforcement Learning (RL) has achieved impressive results in robotics, yet high-performing pipelines remain highly task-specific, with little reuse of prior data. Offline Model-based RL (MBRL) offers greater data efficiency by training policies entirely from existing datasets, but suffers from compounding errors and distribution shift in long-horizon rollouts. Although existing methods have shown success in controlled simulation benchmarks, robustly applying them to the noisy, biased, and partially observed datasets typical of real-world robotics remains challenging. We present a principled pipeline for making offline MBRL effective on physical robots. Our RWM-U extends autoregressive world models with epistemic uncertainty estimation, enabling temporally consistent multi-step rollouts with uncertainty effectively propagated over long horizons. We combine RWM-U with MOPO-PPO, which adapts uncertainty-penalized policy optimization to the stable, on-policy PPO framework for real-world control. We evaluate our approach on diverse manipulation and locomotion tasks in simulation and on real quadruped and humanoid, training policies entirely from offline datasets. The resulting policies consistently outperform model-free and uncertainty-unaware model-based baselines, and fusing real-world data in model learning further yields robust policies that surpass online model-free baselines trained solely in simulation.

### Paper 9: [2509.18631]
**Title:** Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training
**Category:** cs.RO
**Score:** 0.8425
**In MiniLM top-20:** True

Behavior cloning has shown promise for robot manipulation, but real-world demonstrations are costly to acquire at scale. While simulated data offers a scalable alternative, particularly with advances in automated demonstration generation, transferring policies to the real world is hampered by various simulation and real domain gaps. In this work, we propose a unified sim-and-real co-training framework for learning generalizable manipulation policies that primarily leverages simulation and only requires a few real-world demonstrations. Central to our approach is learning a domain-invariant, task-relevant feature space. Our key insight is that aligning the joint distributions of observations and their corresponding actions across domains provides a richer signal than aligning observations (marginals) alone. We achieve this by embedding an Optimal Transport (OT)-inspired loss within the co-training framework, and extend this to an Unbalanced OT framework to handle the imbalance between abundant simulation data and limited real-world examples. We validate our method on challenging manipulation tasks, showing it can leverage abundant simulation data to achieve up to a 30% improvement in the real-world success rate and even generalize to scenarios seen only in simulation. Project webpage: https://ot-sim2real.github.io/.

### Paper 10: [2512.24698]
**Title:** Dynamic Policy Learning for Legged Robot with Simplified Model Pretraining and Model Homotopy Transfer
**Category:** cs.RO
**Score:** 0.8385
**In MiniLM top-20:** True

Generating dynamic motions for legged robots remains a challenging problem. While reinforcement learning has achieved notable success in various legged locomotion tasks, producing highly dynamic behaviors often requires extensive reward tuning or high-quality demonstrations. Leveraging reduced-order models can help mitigate these challenges. However, the model discrepancy poses a significant challenge when transferring policies to full-body dynamics environments. In this work, we introduce a continuation-based learning framework that combines simplified model pretraining and model homotopy transfer to efficiently generate and refine complex dynamic behaviors. First, we pretrain the policy using a single rigid body model to capture core motion patterns in a simplified environment. Next, we employ a continuation strategy to progressively transfer the policy to the full-body environment, minimizing performance loss. To define the continuation path, we introduce a model homotopy from the single rigid body model to the full-body model by gradually redistributing mass and inertia between the trunk and legs. The proposed method not only achieves faster convergence but also demonstrates superior stability during the transfer process compared to baseline methods. Our framework is validated on a range of dynamic tasks, including flips and wall-assisted maneuvers, and is successfully deployed on a real quadrupedal robot.

### Paper 11: [2505.18763]
**Title:** GenPO: Generative Diffusion Models Meet On-Policy Reinforcement Learning
**Category:** cs.LG
**Score:** 0.8344
**In MiniLM top-20:** True

Recent advances in reinforcement learning (RL) have demonstrated the powerful exploration capabilities and multimodality of generative diffusion-based policies. While substantial progress has been made in offline RL and off-policy RL settings, integrating diffusion policies into on-policy frameworks like PPO remains underexplored. This gap is particularly significant given the widespread use of large-scale parallel GPU-accelerated simulators, such as IsaacLab, which are optimized for on-policy RL algorithms and enable rapid training of complex robotic tasks. A key challenge lies in computing state-action log-likelihoods under diffusion policies, which is straightforward for Gaussian policies but intractable for flow-based models due to irreversible forward-reverse processes and discretization errors (e.g., Euler-Maruyama approximations). To bridge this gap, we propose GenPO, a generative policy optimization framework that leverages exact diffusion inversion to construct invertible action mappings. GenPO introduces a novel doubled dummy action mechanism that enables invertibility via alternating updates, resolving log-likelihood computation barriers. Furthermore, we also use the action log-likelihood for unbiased entropy and KL divergence estimation, enabling KL-adaptive learning rates and entropy regularization in on-policy updates. Extensive experiments on eight IsaacLab benchmarks, including legged locomotion (Ant, Humanoid, Anymal-D, Unitree H1, Go2), dexterous manipulation (Shadow Hand), aerial control (Quadcopter), and robotic arm tasks (Franka), demonstrate GenPO's superiority over existing RL baselines. Notably, GenPO is the first method to successfully integrate diffusion policies into on-policy RL, unlocking their potential for large-scale parallelized training and real-world robotic deployment.

### Paper 12 [DIVERGENT]: [2601.18107]
**Title:** Beyond Static Datasets: Robust Offline Policy Optimization via Vetted Synthetic Transitions
**Category:** cs.LG
**Score:** 0.8324
**In MiniLM top-20:** False

Offline Reinforcement Learning (ORL) holds immense promise for safety-critical domains like industrial robotics, where real-time environmental interaction is often prohibitive. A primary obstacle in ORL remains the distributional shift between the static dataset and the learned policy, which typically mandates high degrees of conservatism that can restrain potential policy improvements. We present MoReBRAC, a model-based framework that addresses this limitation through Uncertainty-Aware latent synthesis. Instead of relying solely on the fixed data, MoReBRAC utilizes a dual-recurrent world model to synthesize high-fidelity transitions that augment the training manifold. To ensure the reliability of this synthetic data, we implement a hierarchical uncertainty pipeline integrating Variational Autoencoder (VAE) manifold detection, model sensitivity analysis, and Monte Carlo (MC) dropout. This multi-layered filtering process guarantees that only transitions residing within high-confidence regions of the learned dynamics are utilized. Our results on D4RL Gym-MuJoCo benchmarks reveal significant performance gains, particularly in ``random'' and ``suboptimal'' data regimes. We further provide insights into the role of the VAE as a geometric anchor and discuss the distributional trade-offs encountered when learning from near-optimal datasets.

### Paper 13: [2601.12169]
**Title:** Learning Legged MPC with Smooth Neural Surrogates
**Category:** cs.RO
**Score:** 0.8232
**In MiniLM top-20:** True

Deep learning and model predictive control (MPC) can play complementary roles in legged robotics. However, integrating learned models with online planning remains challenging. When dynamics are learned with neural networks, three key difficulties arise: (1) stiff transitions from contact events may be inherited from the data; (2) additional non-physical local nonsmoothness can occur; and (3) training datasets can induce non-Gaussian model errors due to rapid state changes. We address (1) and (2) by introducing the smooth neural surrogate, a neural network with tunable smoothness designed to provide informative predictions and derivatives for trajectory optimization through contact. To address (3), we train these models using a heavy-tailed likelihood that better matches the empirical error distributions observed in legged-robot dynamics. Together, these design choices substantially improve the reliability, scalability, and generalizability of learned legged MPC. Across zero-shot locomotion tasks of increasing difficulty, smooth neural surrogates with robust learning yield consistent reductions in cumulative cost on simple, well-conditioned behaviors (typically 10-50%), while providing substantially larger gains in regimes where standard neural dynamics often fail outright. In these regimes, smoothing enables reliable execution (from 0/5 to 5/5 success) and produces about 2-50x lower cumulative cost, reflecting orders-of-magnitude absolute improvements in robustness rather than incremental performance gains.

### Paper 14: [2601.00675]
**Title:** RoboReward: General-Purpose Vision-Language Reward Models for Robotics
**Category:** cs.RO
**Score:** 0.8225
**In MiniLM top-20:** True

A well-designed reward is critical for effective reinforcement learning-based policy improvement. In real-world robotics, obtaining such rewards typically requires either labor-intensive human labeling or brittle, handcrafted objectives. Vision-language models (VLMs) have shown promise as automatic reward models, yet their effectiveness on real robot tasks is poorly understood. In this work, we aim to close this gap by introducing (1) RoboReward, a robotics reward dataset and benchmark built on large-scale real-robot corpora from Open X-Embodiment (OXE) and RoboArena, and (2) vision-language reward models trained on this dataset (RoboReward 4B/8B). Because OXE is success-heavy and lacks failure examples, we propose a negative examples data augmentation pipeline that generates calibrated negative and near-misses via counterfactual relabeling of successful episodes and temporal clipping to create partial-progress outcomes from the same videos. Using this framework, we build a large training and evaluation dataset spanning diverse tasks and embodiments to test whether state-of-the-art VLMs can reliably provide rewards for robot learning. Our evaluation of open and proprietary VLMs finds that no model excels across tasks, highlighting substantial room for improvement. We then train general-purpose 4B- and 8B-parameter models that outperform much larger VLMs in assigning rewards for short-horizon robotic tasks. Finally, we deploy the 8B model in real-robot reinforcement learning and find that it improves policy learning over Gemini Robotics-ER 1.5 while narrowing the gap to RL training with human-provided rewards. We release the full dataset, trained reward models, and evaluation suite on our website to advance the development of general-purpose reward models in robotics: https://crfm.stanford.edu/helm/robo-reward-bench (project website).

### Paper 15: [2512.17853]
**Title:** AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning
**Category:** cs.RO
**Score:** 0.8223
**In MiniLM top-20:** True

Generalist robot learning remains constrained by data: large-scale, diverse, and high-quality interaction data are expensive to collect in the real world. While simulation has become a promising way for scaling up data collection, the related tasks, including simulation task design, task-aware scene generation, expert demonstration synthesis, and sim-to-real transfer, still demand substantial human effort. We present AnyTask, an automated framework that pairs massively parallel GPU simulation with foundation models to design diverse manipulation tasks and synthesize robot data. We introduce three AnyTask agents for generating expert demonstrations aiming to solve as many tasks as possible: 1) ViPR, a novel task and motion planning agent with VLM-in-the-loop Parallel Refinement; 2) ViPR-Eureka, a reinforcement learning agent with generated dense rewards and LLM-guided contact sampling; 3) ViPR-RL, a hybrid planning and learning approach that jointly produces high-quality demonstrations with only sparse rewards. We train behavior cloning policies on generated data, validate them in simulation, and deploy them directly on real robot hardware. The policies generalize to novel object poses, achieving 44% average success across a suite of real-world pick-and-place, drawer opening, contact-rich pushing, and long-horizon manipulation tasks. Our project website is at https://anytask.rai-inst.com .

### Paper 16: [2601.14234]
**Title:** Q-learning with Adjoint Matching
**Category:** cs.LG
**Score:** 0.8206
**In MiniLM top-20:** True

We propose Q-learning with Adjoint Matching (QAM), a novel TD-based reinforcement learning (RL) algorithm that tackles a long-standing challenge in continuous-action RL: efficient optimization of an expressive diffusion or flow-matching policy with respect to a parameterized Q-function. Effective optimization requires exploiting the first-order information of the critic, but it is challenging to do so for flow or diffusion policies because direct gradient-based optimization via backpropagation through their multi-step denoising process is numerically unstable. Existing methods work around this either by only using the value and discarding the gradient information, or by relying on approximations that sacrifice policy expressivity or bias the learned policy. QAM sidesteps both of these challenges by leveraging adjoint matching, a recently proposed technique in generative modeling, which transforms the critic's action gradient to form a step-wise objective function that is free from unstable backpropagation, while providing an unbiased, expressive policy at the optimum. Combined with temporal-difference backup for critic learning, QAM consistently outperforms prior approaches on hard, sparse reward tasks in both offline and offline-to-online RL.

### Paper 17: [2506.00070]
**Title:** Robot-R1: Reinforcement Learning for Enhanced Embodied Reasoning in Robotics
**Category:** cs.RO
**Score:** 0.8171
**In MiniLM top-20:** True

Large Vision-Language Models (LVLMs) have recently shown great promise in advancing robotics by combining embodied reasoning with robot control. A common approach involves training on embodied reasoning tasks related to robot control using Supervised Fine-Tuning (SFT). However, SFT datasets are often heuristically constructed and not explicitly optimized for improving robot control. Furthermore, SFT often leads to issues such as catastrophic forgetting and reduced generalization performance. To address these limitations, we introduce Robot-R1, a novel framework that leverages reinforcement learning to enhance embodied reasoning specifically for robot control. Robot-R1 learns to predict the next keypoint state required for task completion, conditioned on the current scene image and environment metadata derived from expert demonstrations. Inspired by the DeepSeek-R1 learning approach, Robot-R1 samples reasoning-based responses and reinforces those that lead to more accurate predictions. To rigorously evaluate Robot-R1, we also introduce a new benchmark that demands the diverse embodied reasoning capabilities for the task. Our experiments show that models trained with Robot-R1 outperform SFT methods on embodied reasoning tasks. Despite having only 7B parameters, Robot-R1 even surpasses GPT-4o on reasoning tasks related to low-level action control, such as spatial and movement reasoning.

### Paper 18: [2501.19128]
**Title:** Shaping Sparse Rewards in Reinforcement Learning: A Semi-supervised Approach
**Category:** cs.LG
**Score:** 0.8080
**In MiniLM top-20:** True

In many real-world scenarios, reward signal for agents are exceedingly sparse, making it challenging to learn an effective reward function for reward shaping. To address this issue, the proposed approach in this paper performs reward shaping not only by utilizing non-zero-reward transitions but also by employing the \emph{Semi-Supervised Learning} (SSL) technique combined with a novel data augmentation to learn trajectory space representations from the majority of transitions, {i.e}., zero-reward transitions, thereby improving the efficacy of reward shaping. Experimental results in Atari and robotic manipulation demonstrate that our method outperforms supervised-based approaches in reward inference, leading to higher agent scores. Notably, in more sparse-reward environments, our method achieves up to twice the peak scores compared to supervised baselines. The proposed double entropy data augmentation enhances performance, showcasing a 15.8\% increase in best score over other augmentation methods

### Paper 19 [DIVERGENT]: [2512.14350]
**Title:** Fine-Tuning of Neural Network Approximate MPC without Retraining via Bayesian Optimization
**Category:** cs.RO
**Score:** 0.8080
**In MiniLM top-20:** False

Approximate model-predictive control (AMPC) aims to imitate an MPC's behavior with a neural network, removing the need to solve an expensive optimization problem at runtime. However, during deployment, the parameters of the underlying MPC must usually be fine-tuned. This often renders AMPC impractical as it requires repeatedly generating a new dataset and retraining the neural network. Recent work addresses this problem by adapting AMPC without retraining using approximated sensitivities of the MPC's optimization problem. Currently, this adaption must be done by hand, which is labor-intensive and can be unintuitive for high-dimensional systems. To solve this issue, we propose using Bayesian optimization to tune the parameters of AMPC policies based on experimental data. By combining model-based control with direct and local learning, our approach achieves superior performance to nominal AMPC on hardware, with minimal experimentation. This allows automatic and data-efficient adaptation of AMPC to new system instances and fine-tuning to cost functions that are difficult to directly implement in MPC. We demonstrate the proposed method in hardware experiments for the swing-up maneuver on an inverted cartpole and yaw control of an under-actuated balancing unicycle robot, a challenging control problem.

### Paper 20 [DIVERGENT]: [2512.24740]
**Title:** Control of Microrobots with Reinforcement Learning under On-Device Compute Constraints
**Category:** cs.RO
**Score:** 0.8062
**In MiniLM top-20:** False

An important function of autonomous microrobots is the ability to perform robust movement over terrain. This paper explores an edge ML approach to microrobot locomotion, allowing for on-device, lower latency control under compute, memory, and power constraints. This paper explores the locomotion of a sub-centimeter quadrupedal microrobot via reinforcement learning (RL) and deploys the resulting controller on an ultra-small system-on-chip (SoC), SC$\mu$M-3C, featuring an ARM Cortex-M0 microcontroller running at 5 MHz. We train a compact FP32 multilayer perceptron (MLP) policy with two hidden layers ($[128, 64]$) in a massively parallel GPU simulation and enhance robustness by utilizing domain randomization over simulation parameters. We then study integer (Int8) quantization (per-tensor and per-feature) to allow for higher inference update rates on our resource-limited hardware, and we connect hardware power budgets to achievable update frequency via a cycles-per-update model for inference on our Cortex-M0. We propose a resource-aware gait scheduling viewpoint: given a device power budget, we can select the gait mode (trot/intermediate/gallop) that maximizes expected RL reward at a corresponding feasible update frequency. Finally, we deploy our MLP policy on a real-world large-scale robot on uneven terrain, qualitatively noting that domain-randomized training can improve out-of-distribution stability. We do not claim real-world large-robot empirical zero-shot transfer in this work.

---

## Review Instructions

You are reviewing the top-20 recommendations from stella for the profile "RL for robotics".
Papers marked [DIVERGENT] are in stella's top-20 but NOT in MiniLM's.

### Full Review (all sections required)

1. **Per-paper assessment**: For each paper:
   - Connection to seeds (direct, adjacent, provocative, noise)
   - For DIVERGENT papers especially: is this a genuinely different signal?
   - Discoverability: would a researcher find this via other means?

2. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - Coverage: methods, applications, critiques, foundations?
   - What's conspicuously absent?
   - How does the character of divergent papers differ from shared papers?

3. **Emergent observations**:
   - What kind of signal does this model capture that MiniLM doesn't?
   - Is the divergence signal (coherent, valuable) or noise (scattered, irrelevant)?
   - Any productive provocations among the recommendations?

4. **Absent researcher note**:
   - What would you need to know about the researcher to assess this properly?

5. **Metric divergence flags**:
   - Does your qualitative impression contradict quantitative expectations?

---

## Assessment

### 1. Per-Paper Assessment

**Paper 1 [2505.22094] ReinFlow** -- Direct (seed paper). Score 0.9009. Flow matching + RL for robotics, core seed topic.

**Paper 2 [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy** -- Direct (seed paper). Score 0.8950. Real-world robot RL with sample efficiency focus.

**Paper 3 [2601.20668] GPO: Growing Policy Optimization** -- Direct (seed paper). Score 0.8846. Legged robot locomotion via RL.

**Paper 4 [2505.06357] DAPPER** -- Direct (seed paper). Score 0.8753. Preference-based RL for robot skill acquisition.

**Paper 5 [2601.20846] End-to-end sim-to-real RL** -- Direct (seed paper). Score 0.8667. Sim-to-real transfer for robotic cutting.

**Paper 6 [2509.04069] Solving Robotics Tasks with Prior Demonstration** -- Direct. Score 0.8550. Demonstration-bootstrapped RL for robotics tasks. Extends the seed themes of sample-efficient robot RL. Would be straightforwardly discoverable via keyword search for "robot reinforcement learning demonstrations."

**Paper 7 [2509.25756] SAC Flow** -- Direct. Score 0.8521. Flow-based policy learning with SAC for robotic manipulation. Strong thematic overlap with ReinFlow (seed 1). Easily discoverable.

**Paper 8 [2504.16680] Uncertainty-Aware Robotic World Model** -- Direct. Score 0.8464. Offline model-based RL for real robot deployment. Connects to the offline/real-world thread in the seeds. Discoverable.

**Paper 9 [2509.18631] Generalizable Domain Adaptation for Sim-and-Real** -- Direct. Score 0.8425. Sim-to-real transfer using optimal transport. Directly extends the sim-to-real seed. Discoverable.

**Paper 10 [2512.24698] Dynamic Policy Learning for Legged Robot** -- Direct. Score 0.8385. Continuation-based RL for dynamic legged locomotion. Extends the GPO seed's legged robot thread. Discoverable.

**Paper 11 [2505.18763] GenPO: Diffusion Models + On-Policy RL** -- Adjacent. Score 0.8344. Bridges diffusion generative models with on-policy RL for robotics. Connects the flow/diffusion policy thread from ReinFlow/SAC Flow to a broader RL algorithmic concern. Somewhat more surprising as a recommendation given its cs.LG venue, but highly relevant.

**Paper 12 [2601.18107] Beyond Static Datasets (DIVERGENT)** -- Adjacent. Score 0.8324. Offline RL with synthetic transition augmentation via world models. This is pure offline RL methodology (D4RL benchmarks), not robotics-specific. The robotics motivation is mentioned but the work is general. Genuinely different signal: Stella captures the offline RL methodology thread that underlies the real-world deployment concern. A researcher focused on robot RL methods would likely encounter this through offline RL channels, not through robotics venues. Moderately discoverable.

**Paper 13 [2601.12169] Learning Legged MPC with Smooth Neural Surrogates** -- Direct. Score 0.8232. Neural network surrogates for model-predictive control on legged robots. Core robotics + learning topic. Discoverable.

**Paper 14 [2601.00675] RoboReward** -- Adjacent. Score 0.8225. Vision-language reward models for robotics RL. Connects the reward design problem to VLMs, extending the RL-for-robotics thread into multi-modal reward specification. Discoverable through robotics venues.

**Paper 15 [2512.17853] AnyTask** -- Direct. Score 0.8223. Automated sim-to-real data generation. Directly serves the sim-to-real pipeline theme. Discoverable.

**Paper 16 [2601.14234] Q-learning with Adjoint Matching** -- Adjacent. Score 0.8206. RL algorithm for diffusion/flow policies. General RL methodology but directly motivated by the flow-policy thread. Would be found through RL algorithmic channels.

**Paper 17 [2506.00070] Robot-R1** -- Adjacent. Score 0.8171. RL for embodied reasoning. Bridges RL with VLM reasoning for robotics. Extends beyond locomotion/manipulation into cognitive robotics. Discoverable.

**Paper 18 [2501.19128] Shaping Sparse Rewards** -- Adjacent. Score 0.8080. Semi-supervised reward shaping. General RL technique applicable to robotics. Would be found through RL methodology searches.

**Paper 19 [2512.14350] Fine-Tuning Neural Network Approximate MPC (DIVERGENT)** -- Adjacent. Score 0.8080. Bayesian optimization for tuning AMPC policies on hardware. This is a control-theoretic paper intersecting with RL through the neural network policy lens. Genuinely different signal: captures the model-predictive control intersection that pure RL keyword searches would miss. A researcher interested in deploying learned controllers would find this valuable. Less discoverable through standard RL channels.

**Paper 20 [2512.24740] Control of Microrobots with RL (DIVERGENT)** -- Adjacent. Score 0.8062. RL for microrobot locomotion on resource-constrained hardware. Genuinely different signal: extends the RL-for-robotics thread to a very different physical scale (sub-centimeter) and computational constraint (Cortex-M0). This is a niche application paper that would be difficult to discover through standard searches unless specifically looking at microrobotics. Interesting for breadth of the field coverage.

### 2. Set-Level Assessment

**Landscape mapping:** This set maps the RL-for-robotics landscape effectively, covering: locomotion (legged robots, microrobots), manipulation (cutting, general pick-and-place), sim-to-real transfer, policy representations (flow-based, diffusion-based, MPC), reward design, and offline RL. It reads more as a well-organized survey of the subfield than a narrow list of similar papers.

**Coverage:** Strong on methods (policy optimization algorithms, flow/diffusion policies, offline RL, MPC). Adequate on applications (legged locomotion, manipulation, sim-to-real). Weak on critiques and foundations -- no papers questioning the fundamental assumptions of RL for robotics, no safety/failure analysis papers, no theoretical convergence or sample complexity results specific to robotics.

**Conspicuously absent:** Multi-robot RL, human-robot interaction, language-conditioned robot RL (beyond Robot-R1), deformable object manipulation, long-horizon planning. The MiniLM-only papers (VLA adaptation, one-shot visual imitation, failure-aware RL) suggest MiniLM captures a vision-and-imitation thread that Stella underweights.

**Divergent paper character:** The three Stella-unique papers (offline RL augmentation, neural MPC tuning, microrobot control) extend the set in the direction of practical deployment concerns: what happens when you actually put learned controllers on hardware with constraints (limited data, compute limits, need for Bayesian tuning). This is a coherent thread of "deployment realism" that MiniLM's divergent papers (VLA adaptation, visual imitation, failure-aware RL) address from a different angle (vision-based, imitation-based).

### 3. Emergent Observations

**Signal character:** Stella appears to capture a slightly more method-centric signal, pulling in RL algorithmic papers (offline RL, MPC neural approximation) that operate at the boundary between pure RL research and robotics applications. MiniLM's divergent papers lean more toward vision-and-imitation-based robotics. The divergence is coherent and interpretable: Stella favors the RL algorithmic substrate, MiniLM favors the perception/imitation layer.

**Divergence quality:** Coherent and modestly valuable. The three divergent papers are all on-topic and represent legitimate research directions. None is noise. However, none is a strong "productive provocation" that would fundamentally reframe the seed interests.

**Productive provocations:** Paper 20 (microrobot control) is the closest to a productive provocation, suggesting that RL-for-robotics extends to dramatically different physical scales with fundamentally different computational constraints. This could prompt a researcher to think about hardware-aware policy design.

### 4. Absent Researcher Note

To properly evaluate this set, I would need to know: (a) whether the researcher is primarily interested in RL algorithms that happen to be applied to robots, or in building real robot systems that happen to use RL; (b) which robot embodiments and tasks matter to them; (c) whether they care about sim-to-real specifically or also real-world-only training; (d) their stance on diffusion/flow policies vs. simpler policy classes. The distinction between the Stella and MiniLM divergent papers would be more or less significant depending on whether the researcher cares more about algorithmic depth or vision-based system integration.

### 5. Metric Divergence Flags

With 17/20 overlap, quantitative metrics would suggest high agreement between Stella and MiniLM. This matches qualitative impression: the two models agree on the core of the RL-for-robotics landscape. The divergence is at the margins (3 papers each) and is interpretable as a difference in emphasis (method-centric vs. vision/imitation-centric). No flag raised: qualitative and quantitative impressions are consistent. The score distributions (Stella 0.80-0.90, MiniLM 0.71-0.87) show Stella compresses the score range less, which may reflect a tighter similarity space but does not qualitatively change the picture.
