# Single-Strategy Characterization Review

**Model:** gte
**Profile:** RL for robotics (P1)
**Depth:** full
**Overlap with MiniLM:** 16/20 shared, 4 unique to gte

## Seed Papers
  - [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning (cs.AI)
  - [2601.20668] GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control (cs.RO)
  - [2601.20846] End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting (cs.RO)
  - [2505.06357] DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition (cs.RO)
  - [2505.22094] ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning (cs.RO)

## gte Top-20 Recommendations

### Paper 1: [2601.15761]
**Title:** Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning
**Category:** cs.AI
**Score:** 0.8663
**In MiniLM top-20:** True

Deploying reinforcement learning in the real world remains challenging due to sample inefficiency, sparse rewards, and noisy visual observations. Prior work leverages demonstrations and human feedback to improve learning efficiency and robustness. However, offline-to-online methods need large datasets and can be unstable, while VLA-assisted RL relies on large-scale pretraining and fine-tuning. As a result, a low-cost real-world RL method with minimal data requirements has yet to emerge. We introduce \textbf{SigEnt-SAC}, an off-policy actor-critic method that learns from scratch using a single expert trajectory. Our key design is a sigmoid-bounded entropy term that prevents negative-entropy-driven optimization toward out-of-distribution actions and reduces Q-function oscillations. We benchmark SigEnt-SAC on D4RL tasks against representative baselines. Experiments show that SigEnt-SAC substantially alleviates Q-function oscillations and reaches a 100\% success rate faster than prior methods. Finally, we validate SigEnt-SAC on four real-world robotic tasks across multiple embodiments, where agents learn from raw images and sparse rewards; results demonstrate that SigEnt-SAC can learn successful policies with only a small number of real-world interactions, suggesting a low-cost and practical pathway for real-world RL deployment.

### Paper 2: [2505.22094]
**Title:** ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
**Category:** cs.RO
**Score:** 0.8621
**In MiniLM top-20:** True

We propose ReinFlow, a simple yet effective online reinforcement learning (RL) framework that fine-tunes a family of flow matching policies for continuous robotic control. Derived from rigorous RL theory, ReinFlow injects learnable noise into a flow policy's deterministic path, converting the flow into a discrete-time Markov Process for exact and straightforward likelihood computation. This conversion facilitates exploration and ensures training stability, enabling ReinFlow to fine-tune diverse flow model variants, including Rectified Flow [35] and Shortcut Models [19], particularly at very few or even one denoising step. We benchmark ReinFlow in representative locomotion and manipulation tasks, including long-horizon planning with visual input and sparse reward. The episode reward of Rectified Flow policies obtained an average net growth of 135.36% after fine-tuning in challenging legged locomotion tasks while saving denoising steps and 82.63% of wall time compared to state-of-the-art diffusion RL fine-tuning method DPPO [43]. The success rate of the Shortcut Model policies in state and visual manipulation tasks achieved an average net increase of 40.34% after fine-tuning with ReinFlow at four or even one denoising step, whose performance is comparable to fine-tuned DDIM policies while saving computation time for an average of 23.20%. Project webpage: https://reinflow.github.io/

### Paper 3: [2601.20668]
**Title:** GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control
**Category:** cs.RO
**Score:** 0.8578
**In MiniLM top-20:** True

Training reinforcement learning (RL) policies for legged robots remains challenging due to high-dimensional continuous actions, hardware constraints, and limited exploration. Existing methods for locomotion and whole-body control work well for position-based control with environment-specific heuristics (e.g., reward shaping, curriculum design, and manual initialization), but are less effective for torque-based control, where sufficiently exploring the action space and obtaining informative gradient signals for training is significantly more difficult. We introduce Growing Policy Optimization (GPO), a training framework that applies a time-varying action transformation to restrict the effective action space in the early stage, thereby encouraging more effective data collection and policy learning, and then progressively expands it to enhance exploration and achieve higher expected return. We prove that this transformation preserves the PPO update rule and introduces only bounded, vanishing gradient distortion, thereby ensuring stable training. We evaluate GPO on both quadruped and hexapod robots, including zero-shot deployment of simulation-trained policies on hardware. Policies trained with GPO consistently achieve better performance. These results suggest that GPO provides a general, environment-agnostic optimization framework for learning legged locomotion.

### Paper 4: [2505.06357]
**Title:** DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition
**Category:** cs.RO
**Score:** 0.8469
**In MiniLM top-20:** True

Preference-based Reinforcement Learning (PbRL) enables policy learning through simple queries comparing trajectories from a single policy. While human responses to these queries make it possible to learn policies aligned with human preferences, PbRL suffers from low query efficiency, as policy bias limits trajectory diversity and reduces the number of discriminable queries available for learning preferences. This paper identifies preference discriminability, which quantifies how easily a human can judge which trajectory is closer to their ideal behavior, as a key metric for improving query efficiency. To address this, we move beyond comparisons within a single policy and instead generate queries by comparing trajectories from multiple policies, as training them from scratch promotes diversity without policy bias. We propose Discriminability-Aware Policy-to-Policy Preference-Based Efficient Reinforcement Learning (DAPPER), which integrates preference discriminability with trajectory diversification achieved by multiple policies. DAPPER trains new policies from scratch after each reward update and employs a discriminator that learns to estimate preference discriminability, enabling the prioritized sampling of more discriminable queries. During training, it jointly maximizes the preference reward and preference discriminability score, encouraging the discovery of highly rewarding and easily distinguishable policies. Experiments in simulated and real-world legged robot environments demonstrate that DAPPER outperforms previous methods in query efficiency, particularly under challenging preference discriminability conditions. A supplementary video that facilitates understanding of the proposed framework and its experimental results is available at: https://youtu.be/lRwX8FNN8n4

### Paper 5: [2601.20846]
**Title:** End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting
**Category:** cs.RO
**Score:** 0.8286
**In MiniLM top-20:** True

Whereas reinforcement learning has been applied with success to a range of robotic control problems in complex, uncertain environments, reliance on extensive data - typically sourced from simulation environments - limits real-world deployment due to the domain gap between simulated and physical systems, coupled with limited real-world sample availability. We propose a novel method for sim-to-real transfer of reinforcement learning policies, based on a reinterpretation of neural style transfer from image processing to synthesise novel training data from unpaired unlabelled real world datasets. We employ a variational autoencoder to jointly learn self-supervised feature representations for style transfer and generate weakly paired source-target trajectories to improve physical realism of synthesised trajectories. We demonstrate the application of our approach based on the case study of robot cutting of unknown materials. Compared to baseline methods, including our previous work, CycleGAN, and conditional variational autoencoder-based time series translation, our approach achieves improved task completion time and behavioural stability with minimal real-world data. Our framework demonstrates robustness to geometric and material variation, and highlights the feasibility of policy adaptation in challenging contact-rich tasks where real-world reward information is unavailable.

### Paper 6: [2512.24698]
**Title:** Dynamic Policy Learning for Legged Robot with Simplified Model Pretraining and Model Homotopy Transfer
**Category:** cs.RO
**Score:** 0.7962
**In MiniLM top-20:** True

Generating dynamic motions for legged robots remains a challenging problem. While reinforcement learning has achieved notable success in various legged locomotion tasks, producing highly dynamic behaviors often requires extensive reward tuning or high-quality demonstrations. Leveraging reduced-order models can help mitigate these challenges. However, the model discrepancy poses a significant challenge when transferring policies to full-body dynamics environments. In this work, we introduce a continuation-based learning framework that combines simplified model pretraining and model homotopy transfer to efficiently generate and refine complex dynamic behaviors. First, we pretrain the policy using a single rigid body model to capture core motion patterns in a simplified environment. Next, we employ a continuation strategy to progressively transfer the policy to the full-body environment, minimizing performance loss. To define the continuation path, we introduce a model homotopy from the single rigid body model to the full-body model by gradually redistributing mass and inertia between the trunk and legs. The proposed method not only achieves faster convergence but also demonstrates superior stability during the transfer process compared to baseline methods. Our framework is validated on a range of dynamic tasks, including flips and wall-assisted maneuvers, and is successfully deployed on a real quadrupedal robot.

### Paper 7: [2509.04069]
**Title:** Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep Reinforcement Learning
**Category:** cs.RO
**Score:** 0.7947
**In MiniLM top-20:** True

This paper proposes an exploration-efficient Deep Reinforcement Learning with Reference policy (DRLR) framework for learning robotics tasks that incorporates demonstrations. The DRLR framework is developed based on an algorithm called Imitation Bootstrapped Reinforcement Learning (IBRL). We propose to improve IBRL by modifying the action selection module. The proposed action selection module provides a calibrated Q-value, which mitigates the bootstrapping error that otherwise leads to inefficient exploration. Furthermore, to prevent the RL policy from converging to a sub-optimal policy, SAC is used as the RL policy instead of TD3. The effectiveness of our method in mitigating bootstrapping error and preventing overfitting is empirically validated by learning two robotics tasks: bucket loading and open drawer, which require extensive interactions with the environment. Simulation results also demonstrate the robustness of the DRLR framework across tasks with both low and high state-action dimensions, and varying demonstration qualities. To evaluate the developed framework on a real-world industrial robotics task, the bucket loading task is deployed on a real wheel loader. The sim2real results validate the successful deployment of the DRLR framework.

### Paper 8: [2601.00675]
**Title:** RoboReward: General-Purpose Vision-Language Reward Models for Robotics
**Category:** cs.RO
**Score:** 0.7945
**In MiniLM top-20:** True

A well-designed reward is critical for effective reinforcement learning-based policy improvement. In real-world robotics, obtaining such rewards typically requires either labor-intensive human labeling or brittle, handcrafted objectives. Vision-language models (VLMs) have shown promise as automatic reward models, yet their effectiveness on real robot tasks is poorly understood. In this work, we aim to close this gap by introducing (1) RoboReward, a robotics reward dataset and benchmark built on large-scale real-robot corpora from Open X-Embodiment (OXE) and RoboArena, and (2) vision-language reward models trained on this dataset (RoboReward 4B/8B). Because OXE is success-heavy and lacks failure examples, we propose a negative examples data augmentation pipeline that generates calibrated negative and near-misses via counterfactual relabeling of successful episodes and temporal clipping to create partial-progress outcomes from the same videos. Using this framework, we build a large training and evaluation dataset spanning diverse tasks and embodiments to test whether state-of-the-art VLMs can reliably provide rewards for robot learning. Our evaluation of open and proprietary VLMs finds that no model excels across tasks, highlighting substantial room for improvement. We then train general-purpose 4B- and 8B-parameter models that outperform much larger VLMs in assigning rewards for short-horizon robotic tasks. Finally, we deploy the 8B model in real-robot reinforcement learning and find that it improves policy learning over Gemini Robotics-ER 1.5 while narrowing the gap to RL training with human-provided rewards. We release the full dataset, trained reward models, and evaluation suite on our website to advance the development of general-purpose reward models in robotics: https://crfm.stanford.edu/helm/robo-reward-bench (project website).

### Paper 9: [2601.14234]
**Title:** Q-learning with Adjoint Matching
**Category:** cs.LG
**Score:** 0.7930
**In MiniLM top-20:** True

We propose Q-learning with Adjoint Matching (QAM), a novel TD-based reinforcement learning (RL) algorithm that tackles a long-standing challenge in continuous-action RL: efficient optimization of an expressive diffusion or flow-matching policy with respect to a parameterized Q-function. Effective optimization requires exploiting the first-order information of the critic, but it is challenging to do so for flow or diffusion policies because direct gradient-based optimization via backpropagation through their multi-step denoising process is numerically unstable. Existing methods work around this either by only using the value and discarding the gradient information, or by relying on approximations that sacrifice policy expressivity or bias the learned policy. QAM sidesteps both of these challenges by leveraging adjoint matching, a recently proposed technique in generative modeling, which transforms the critic's action gradient to form a step-wise objective function that is free from unstable backpropagation, while providing an unbiased, expressive policy at the optimum. Combined with temporal-difference backup for critic learning, QAM consistently outperforms prior approaches on hard, sparse reward tasks in both offline and offline-to-online RL.

### Paper 10: [2505.18763]
**Title:** GenPO: Generative Diffusion Models Meet On-Policy Reinforcement Learning
**Category:** cs.LG
**Score:** 0.7924
**In MiniLM top-20:** True

Recent advances in reinforcement learning (RL) have demonstrated the powerful exploration capabilities and multimodality of generative diffusion-based policies. While substantial progress has been made in offline RL and off-policy RL settings, integrating diffusion policies into on-policy frameworks like PPO remains underexplored. This gap is particularly significant given the widespread use of large-scale parallel GPU-accelerated simulators, such as IsaacLab, which are optimized for on-policy RL algorithms and enable rapid training of complex robotic tasks. A key challenge lies in computing state-action log-likelihoods under diffusion policies, which is straightforward for Gaussian policies but intractable for flow-based models due to irreversible forward-reverse processes and discretization errors (e.g., Euler-Maruyama approximations). To bridge this gap, we propose GenPO, a generative policy optimization framework that leverages exact diffusion inversion to construct invertible action mappings. GenPO introduces a novel doubled dummy action mechanism that enables invertibility via alternating updates, resolving log-likelihood computation barriers. Furthermore, we also use the action log-likelihood for unbiased entropy and KL divergence estimation, enabling KL-adaptive learning rates and entropy regularization in on-policy updates. Extensive experiments on eight IsaacLab benchmarks, including legged locomotion (Ant, Humanoid, Anymal-D, Unitree H1, Go2), dexterous manipulation (Shadow Hand), aerial control (Quadcopter), and robotic arm tasks (Franka), demonstrate GenPO's superiority over existing RL baselines. Notably, GenPO is the first method to successfully integrate diffusion policies into on-policy RL, unlocking their potential for large-scale parallelized training and real-world robotic deployment.

### Paper 11: [2504.16680]
**Title:** Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots
**Category:** cs.RO
**Score:** 0.7850
**In MiniLM top-20:** True

Reinforcement Learning (RL) has achieved impressive results in robotics, yet high-performing pipelines remain highly task-specific, with little reuse of prior data. Offline Model-based RL (MBRL) offers greater data efficiency by training policies entirely from existing datasets, but suffers from compounding errors and distribution shift in long-horizon rollouts. Although existing methods have shown success in controlled simulation benchmarks, robustly applying them to the noisy, biased, and partially observed datasets typical of real-world robotics remains challenging. We present a principled pipeline for making offline MBRL effective on physical robots. Our RWM-U extends autoregressive world models with epistemic uncertainty estimation, enabling temporally consistent multi-step rollouts with uncertainty effectively propagated over long horizons. We combine RWM-U with MOPO-PPO, which adapts uncertainty-penalized policy optimization to the stable, on-policy PPO framework for real-world control. We evaluate our approach on diverse manipulation and locomotion tasks in simulation and on real quadruped and humanoid, training policies entirely from offline datasets. The resulting policies consistently outperform model-free and uncertainty-unaware model-based baselines, and fusing real-world data in model learning further yields robust policies that surpass online model-free baselines trained solely in simulation.

### Paper 12: [2601.12169]
**Title:** Learning Legged MPC with Smooth Neural Surrogates
**Category:** cs.RO
**Score:** 0.7847
**In MiniLM top-20:** True

Deep learning and model predictive control (MPC) can play complementary roles in legged robotics. However, integrating learned models with online planning remains challenging. When dynamics are learned with neural networks, three key difficulties arise: (1) stiff transitions from contact events may be inherited from the data; (2) additional non-physical local nonsmoothness can occur; and (3) training datasets can induce non-Gaussian model errors due to rapid state changes. We address (1) and (2) by introducing the smooth neural surrogate, a neural network with tunable smoothness designed to provide informative predictions and derivatives for trajectory optimization through contact. To address (3), we train these models using a heavy-tailed likelihood that better matches the empirical error distributions observed in legged-robot dynamics. Together, these design choices substantially improve the reliability, scalability, and generalizability of learned legged MPC. Across zero-shot locomotion tasks of increasing difficulty, smooth neural surrogates with robust learning yield consistent reductions in cumulative cost on simple, well-conditioned behaviors (typically 10-50%), while providing substantially larger gains in regimes where standard neural dynamics often fail outright. In these regimes, smoothing enables reliable execution (from 0/5 to 5/5 success) and produces about 2-50x lower cumulative cost, reflecting orders-of-magnitude absolute improvements in robustness rather than incremental performance gains.

### Paper 13: [2601.06748]
**Title:** On-the-Fly VLA Adaptation via Test-Time Reinforcement Learning
**Category:** cs.RO
**Score:** 0.7843
**In MiniLM top-20:** True

Vision-Language-Action models have recently emerged as a powerful paradigm for general-purpose robot learning, enabling agents to map visual observations and natural-language instructions into executable robotic actions. Though popular, they are primarily trained via supervised fine-tuning or training-time reinforcement learning, requiring explicit fine-tuning phases, human interventions, or controlled data collection. Consequently, existing methods remain unsuitable for challenging simulated- or physical-world deployments, where robots must respond autonomously and flexibly to evolving environments. To address this limitation, we introduce a Test-Time Reinforcement Learning for VLAs (TT-VLA), a framework that enables on-the-fly policy adaptation during inference. TT-VLA formulates a dense reward mechanism that leverages step-by-step task-progress signals to refine action policies during test time while preserving the SFT/RL-trained priors, making it an effective supplement to current VLA models. Empirical results show that our approach enhances overall adaptability, stability, and task success in dynamic, previously unseen scenarios under simulated and real-world settings. We believe TT-VLA offers a principled step toward self-improving, deployment-ready VLAs.

### Paper 14: [2509.18631]
**Title:** Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training
**Category:** cs.RO
**Score:** 0.7826
**In MiniLM top-20:** True

Behavior cloning has shown promise for robot manipulation, but real-world demonstrations are costly to acquire at scale. While simulated data offers a scalable alternative, particularly with advances in automated demonstration generation, transferring policies to the real world is hampered by various simulation and real domain gaps. In this work, we propose a unified sim-and-real co-training framework for learning generalizable manipulation policies that primarily leverages simulation and only requires a few real-world demonstrations. Central to our approach is learning a domain-invariant, task-relevant feature space. Our key insight is that aligning the joint distributions of observations and their corresponding actions across domains provides a richer signal than aligning observations (marginals) alone. We achieve this by embedding an Optimal Transport (OT)-inspired loss within the co-training framework, and extend this to an Unbalanced OT framework to handle the imbalance between abundant simulation data and limited real-world examples. We validate our method on challenging manipulation tasks, showing it can leverage abundant simulation data to achieve up to a 30% improvement in the real-world success rate and even generalize to scenarios seen only in simulation. Project webpage: https://ot-sim2real.github.io/.

### Paper 15: [2506.00070]
**Title:** Robot-R1: Reinforcement Learning for Enhanced Embodied Reasoning in Robotics
**Category:** cs.RO
**Score:** 0.7818
**In MiniLM top-20:** True

Large Vision-Language Models (LVLMs) have recently shown great promise in advancing robotics by combining embodied reasoning with robot control. A common approach involves training on embodied reasoning tasks related to robot control using Supervised Fine-Tuning (SFT). However, SFT datasets are often heuristically constructed and not explicitly optimized for improving robot control. Furthermore, SFT often leads to issues such as catastrophic forgetting and reduced generalization performance. To address these limitations, we introduce Robot-R1, a novel framework that leverages reinforcement learning to enhance embodied reasoning specifically for robot control. Robot-R1 learns to predict the next keypoint state required for task completion, conditioned on the current scene image and environment metadata derived from expert demonstrations. Inspired by the DeepSeek-R1 learning approach, Robot-R1 samples reasoning-based responses and reinforces those that lead to more accurate predictions. To rigorously evaluate Robot-R1, we also introduce a new benchmark that demands the diverse embodied reasoning capabilities for the task. Our experiments show that models trained with Robot-R1 outperform SFT methods on embodied reasoning tasks. Despite having only 7B parameters, Robot-R1 even surpasses GPT-4o on reasoning tasks related to low-level action control, such as spatial and movement reasoning.

### Paper 16: [2509.25756]
**Title:** SAC Flow: Sample-Efficient Reinforcement Learning of Flow-Based Policies via Velocity-Reparameterized Sequential Modeling
**Category:** cs.RO
**Score:** 0.7809
**In MiniLM top-20:** True

Training expressive flow-based policies with off-policy reinforcement learning is notoriously unstable due to gradient pathologies in the multi-step action sampling process. We trace this instability to a fundamental connection: the flow rollout is algebraically equivalent to a residual recurrent computation, making it susceptible to the same vanishing and exploding gradients as RNNs. To address this, we reparameterize the velocity network using principles from modern sequential models, introducing two stable architectures: Flow-G, which incorporates a gated velocity, and Flow-T, which utilizes a decoded velocity. We then develop a practical SAC-based algorithm, enabled by a noise-augmented rollout, that facilitates direct end-to-end training of these policies. Our approach supports both from-scratch and offline-to-online learning and achieves state-of-the-art performance on continuous control and robotic manipulation benchmarks, eliminating the need for common workarounds like policy distillation or surrogate objectives.

### Paper 17 [DIVERGENT]: [2601.01803]
**Title:** Moments Matter:Stabilizing Policy Optimization using Return Distributions
**Category:** cs.LG
**Score:** 0.7807
**In MiniLM top-20:** False

Deep Reinforcement Learning (RL) agents often learn policies that achieve the same episodic return yet behave very differently, due to a combination of environmental (random transitions, initial conditions, reward noise) and algorithmic (minibatch selection, exploration noise) factors. In continuous control tasks, even small parameter shifts can produce unstable gaits, complicating both algorithm comparison and real-world transfer. Previous work has shown that such instability arises when policy updates traverse noisy neighborhoods and that the spread of post-update return distribution $R(\theta)$, obtained by repeatedly sampling minibatches, updating $\theta$, and measuring final returns, is a useful indicator of this noise. Although explicitly constraining the policy to maintain a narrow $R(\theta)$ can improve stability, directly estimating $R(\theta)$ is computationally expensive in high-dimensional settings. We propose an alternative that takes advantage of environmental stochasticity to mitigate update-induced variability. Specifically, we model state-action return distribution through a distributional critic and then bias the advantage function of PPO using higher-order moments (skewness and kurtosis) of this distribution. By penalizing extreme tail behaviors, our method discourages policies from entering parameter regimes prone to instability. We hypothesize that in environments where post-update critic values align poorly with post-update returns, standard PPO struggles to produce a narrow $R(\theta)$. In such cases, our moment-based correction narrows $R(\theta)$, improving stability by up to 75% in Walker2D, while preserving comparable evaluation returns.

### Paper 18 [DIVERGENT]: [2601.18107]
**Title:** Beyond Static Datasets: Robust Offline Policy Optimization via Vetted Synthetic Transitions
**Category:** cs.LG
**Score:** 0.7782
**In MiniLM top-20:** False

Offline Reinforcement Learning (ORL) holds immense promise for safety-critical domains like industrial robotics, where real-time environmental interaction is often prohibitive. A primary obstacle in ORL remains the distributional shift between the static dataset and the learned policy, which typically mandates high degrees of conservatism that can restrain potential policy improvements. We present MoReBRAC, a model-based framework that addresses this limitation through Uncertainty-Aware latent synthesis. Instead of relying solely on the fixed data, MoReBRAC utilizes a dual-recurrent world model to synthesize high-fidelity transitions that augment the training manifold. To ensure the reliability of this synthetic data, we implement a hierarchical uncertainty pipeline integrating Variational Autoencoder (VAE) manifold detection, model sensitivity analysis, and Monte Carlo (MC) dropout. This multi-layered filtering process guarantees that only transitions residing within high-confidence regions of the learned dynamics are utilized. Our results on D4RL Gym-MuJoCo benchmarks reveal significant performance gains, particularly in ``random'' and ``suboptimal'' data regimes. We further provide insights into the role of the VAE as a geometric anchor and discuss the distributional trade-offs encountered when learning from near-optimal datasets.

### Paper 19 [DIVERGENT]: [2512.24125]
**Title:** Unified Embodied VLM Reasoning with Robotic Action via Autoregressive Discretized Pre-training
**Category:** cs.RO
**Score:** 0.7781
**In MiniLM top-20:** False

General-purpose robotic systems operating in open-world environments must achieve both broad generalization and high-precision action execution, a combination that remains challenging for existing Vision-Language-Action (VLA) models. While large Vision-Language Models (VLMs) improve semantic generalization, insufficient embodied reasoning leads to brittle behavior, and conversely, strong reasoning alone is inadequate without precise control. To provide a decoupled and quantitative assessment of this bottleneck, we introduce Embodied Reasoning Intelligence Quotient (ERIQ), a large-scale embodied reasoning benchmark in robotic manipulation, comprising 6K+ question-answer pairs across four reasoning dimensions. By decoupling reasoning from execution, ERIQ enables systematic evaluation and reveals a strong positive correlation between embodied reasoning capability and end-to-end VLA generalization. To bridge the gap from reasoning to precise execution, we propose FACT, a flow-matching-based action tokenizer that converts continuous control into discrete sequences while preserving high-fidelity trajectory reconstruction. The resulting GenieReasoner jointly optimizes reasoning and action in a unified space, outperforming both continuous-action and prior discrete-action baselines in real-world tasks. Together, ERIQ and FACT provide a principled framework for diagnosing and overcoming the reasoning-precision trade-off, advancing robust, general-purpose robotic manipulation. Project page: https://geniereasoner.github.io/GenieReasoner/

### Paper 20 [DIVERGENT]: [2601.19810]
**Title:** Unsupervised Learning of Efficient Exploration: Pre-training Adaptive Policies via Self-Imposed Goals
**Category:** cs.LG
**Score:** 0.7715
**In MiniLM top-20:** False

Unsupervised pre-training can equip reinforcement learning agents with prior knowledge and accelerate learning in downstream tasks. A promising direction, grounded in human development, investigates agents that learn by setting and pursuing their own goals. The core challenge lies in how to effectively generate, select, and learn from such goals. Our focus is on broad distributions of downstream tasks where solving every task zero-shot is infeasible. Such settings naturally arise when the target tasks lie outside of the pre-training distribution or when their identities are unknown to the agent. In this work, we (i) optimize for efficient multi-episode exploration and adaptation within a meta-learning framework, and (ii) guide the training curriculum with evolving estimates of the agent's post-adaptation performance. We present ULEE, an unsupervised meta-learning method that combines an in-context learner with an adversarial goal-generation strategy that maintains training at the frontier of the agent's capabilities. On XLand-MiniGrid benchmarks, ULEE pre-training yields improved exploration and adaptation abilities that generalize to novel objectives, environment dynamics, and map structures. The resulting policy attains improved zero-shot and few-shot performance, and provides a strong initialization for longer fine-tuning processes. It outperforms learning from scratch, DIAYN pre-training, and alternative curricula.

---

## Review Instructions

You are reviewing the top-20 recommendations from gte for the profile "RL for robotics".
Papers marked [DIVERGENT] are in gte's top-20 but NOT in MiniLM's.

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

## Review

### Per-Paper Assessment

**Paper 1 [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy (seed)** -- Direct. This is a seed paper. Off-policy RL for real-world robotics with minimal data. Core to the profile.

**Paper 2 [2505.22094] ReinFlow (seed)** -- Direct. Seed paper. Flow matching policies fine-tuned with online RL for robotic control. Central to the profile intersection of generative policies and RL for robotics.

**Paper 3 [2601.20668] GPO (seed)** -- Direct. Seed paper. Policy optimization for legged robot locomotion. Prototypical RL-for-robotics work.

**Paper 4 [2505.06357] DAPPER (seed)** -- Direct. Seed paper. Preference-based RL for robot skill acquisition, including real-world legged robots.

**Paper 5 [2601.20846] Sim-to-real RL (seed)** -- Direct. Seed paper. Neural style transfer for sim-to-real policy transfer applied to robotic cutting.

**Paper 6 [2512.24698] Dynamic Policy Learning for Legged Robots** -- Direct. Legged robot dynamic motions via simplified model pretraining and policy transfer. Tightly aligned with seeds on legged locomotion RL. Would be easily discoverable via keyword search.

**Paper 7 [2509.04069] Solving Robotics Tasks with Prior Demonstration** -- Direct. RL with demonstrations for robotics, including real wheel-loader deployment. Strong methodological overlap with seeds on sample-efficient RL for real robots.

**Paper 8 [2601.00675] RoboReward** -- Direct. Vision-language reward models for real-robot RL. Addresses the reward specification problem that underlies all seed papers. Easily discoverable but a valuable inclusion.

**Paper 9 [2601.14234] Q-learning with Adjoint Matching** -- Adjacent. Continuous-action RL algorithm using diffusion/flow policies. Not robotics-specific but directly applicable to robotic control. Shares the diffusion-policy RL intersection with seeds 2 and 5.

**Paper 10 [2505.18763] GenPO** -- Adjacent. Integrates diffusion policies into on-policy RL for robotic tasks in IsaacLab. Strong alignment with the generative-policy-for-robotics thread. cs.LG rather than cs.RO, but validated on robotics benchmarks.

**Paper 11 [2504.16680] Uncertainty-Aware Robotic World Model** -- Direct. Offline model-based RL for real quadruped and humanoid robots. Directly addresses the data-efficiency challenge from seeds.

**Paper 12 [2601.12169] Learning Legged MPC with Smooth Neural Surrogates** -- Direct. Learned dynamics for legged robot MPC. Bridges model-based and learning-based approaches for legged locomotion. Tightly aligned with seed 3 (GPO).

**Paper 13 [2601.06748] On-the-Fly VLA Adaptation via Test-Time RL** -- Adjacent. VLA model adapted via RL at test time. More about foundation models for robotics than pure RL, but the RL-at-deployment framing connects to the real-world RL thread.

**Paper 14 [2509.18631] Generalizable Domain Adaptation for Sim-and-Real** -- Direct. Sim-to-real transfer via optimal transport, directly related to seed 5. Real-robot manipulation validation.

**Paper 15 [2506.00070] Robot-R1** -- Adjacent. Uses RL to enhance embodied reasoning in vision-language models for robot control. RL is the training mechanism rather than the core contribution, but the robotics application is central.

**Paper 16 [2509.25756] SAC Flow** -- Direct. Flow-based RL policies for robotic manipulation. Directly combines RL algorithms with generative policies for robot tasks, same thread as seeds 2 and the flow-matching papers.

**Paper 17 [DIVERGENT] [2601.01803] Moments Matter: Stabilizing Policy Optimization** -- Adjacent. Pure RL methodology (distributional critic for PPO stability) in continuous control tasks. No explicit robotics application but directly relevant to the stability issues in robotic RL. This is a genuinely different signal: GTE picks up on the methodological RL foundations that underpin the applied robotics work. A robotics RL researcher would benefit from this if they face training instability. Moderately discoverable via RL venues but not via robotics-specific searches.

**Paper 18 [DIVERGENT] [2601.18107] Beyond Static Datasets: Robust Offline Policy Optimization** -- Adjacent. Model-based offline RL with uncertainty-aware synthetic data augmentation. Validated on D4RL MuJoCo, mentions industrial robotics motivation. Connects to seed themes of data efficiency and sim-to-real. Genuinely different signal: GTE identifies the offline RL methodology space that feeds into real-robot deployment. Discoverable at RL conferences but not through robotics channels.

**Paper 19 [DIVERGENT] [2512.24125] Unified Embodied VLM Reasoning with Robotic Action** -- Adjacent. VLA model with flow-matching action tokenizer for robotic manipulation. More VLM-centric than RL-centric, but the robotics application and the flow-matching action representation connect to multiple seeds. Somewhat surprising inclusion given the weak RL thread, but the robotic manipulation grounding is real.

**Paper 20 [DIVERGENT] [2601.19810] Unsupervised Learning of Efficient Exploration (ULEE)** -- Provocative. Meta-learning for unsupervised exploration and adaptation. No robotics application (XLand-MiniGrid benchmarks). This is the most distant from the seed profile. The connection is via the exploration/adaptation thread in RL, which is foundational to robot learning. A robotics researcher would likely not encounter this unless following meta-RL closely. Genuinely different signal but borderline noise for a robotics-focused researcher.

### Set-Level Assessment

This set competently maps the RL-for-robotics landscape with strong coverage of: policy optimization methods (PPO variants, SAC, off-policy), generative policies (flow matching, diffusion), sim-to-real transfer, and real-world deployment. The 16 shared papers form a coherent core that any researcher in this area would expect to see.

**Coverage:** Methods are well-represented (on-policy, off-policy, model-based, model-free, flow-based). Applications span legged locomotion, manipulation, and real-world deployment. Foundations of RL algorithms are present via the divergent papers. What is notably absent: multi-agent robotics RL, safe RL for robotics (constraint satisfaction), hierarchical RL for long-horizon tasks, and any explicit coverage of reward design or curriculum learning beyond RoboReward.

**Character of divergent papers:** The 4 unique GTE papers split into two categories: (1) pure RL methodology papers without robotics application (Papers 17, 18, 20) that capture the algorithmic foundations, and (2) a VLM-robotics paper (Paper 19) that captures the emergent intersection of foundation models and robotic action. This suggests GTE has a slightly wider methodological aperture than MiniLM, pulling in foundational RL work that is relevant but not explicitly robotics-labeled.

### Emergent Observations

GTE captures a broader methodological envelope than MiniLM for this profile. The divergent papers reveal sensitivity to: (a) RL training stability methodology (distributional critics, moment-based regularization), (b) offline RL data augmentation strategies, and (c) the VLM-to-action pipeline. This is a coherent signal, not noise. Three of the four divergent papers are plausibly valuable to a robotics RL researcher, with Paper 20 (ULEE) being the weakest link.

The divergence signal is coherent and mildly valuable. It extends the profile into the RL methodology substrate without losing topical coherence. No single divergent paper is a "productive provocation" that would fundamentally reframe the research question, but Papers 17 and 18 offer practical methodological insights.

### Absent Researcher Note

To assess this set properly, I would need to know: (1) whether the researcher is primarily an RL methodologist who applies to robots, or a roboticist who uses RL as a tool -- this determines whether the methodological divergent papers are welcome or distracting; (2) the specific robot platform (legged, manipulator, mobile) -- the set skews heavily toward legged locomotion; (3) whether the researcher is interested in sim-only or requires real-world deployment -- this affects the relevance of Papers 18 and 20.

### Metric Divergence Flags

The 16/20 overlap with MiniLM (80%) suggests high agreement. Qualitatively, this matches: the shared papers form a strong, coherent core, and the 4 divergent papers are adjacent rather than alien. No qualitative-quantitative contradiction. The divergent papers are all plausible recommendations, none are outright noise. If anything, the quantitative overlap slightly understates the qualitative similarity, since the divergent papers are methodologically adjacent rather than topically distant.
