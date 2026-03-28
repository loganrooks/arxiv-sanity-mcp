# Single-Strategy Characterization Review

**Model:** qwen3
**Profile:** RL for robotics (P1)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to qwen3

## Seed Papers
  - [2601.15761] Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning (cs.AI)
  - [2601.20668] GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control (cs.RO)
  - [2601.20846] End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting (cs.RO)
  - [2505.06357] DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition (cs.RO)
  - [2505.22094] ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning (cs.RO)

## qwen3 Top-20 Recommendations

### Paper 1: [2601.20668]
**Title:** GPO: Growing Policy Optimization for Legged Robot Locomotion and Whole-Body Control
**Category:** cs.RO
**Score:** 0.7950
**In MiniLM top-20:** True

Training reinforcement learning (RL) policies for legged robots remains challenging due to high-dimensional continuous actions, hardware constraints, and limited exploration. Existing methods for locomotion and whole-body control work well for position-based control with environment-specific heuristics (e.g., reward shaping, curriculum design, and manual initialization), but are less effective for torque-based control, where sufficiently exploring the action space and obtaining informative gradient signals for training is significantly more difficult. We introduce Growing Policy Optimization (GPO), a training framework that applies a time-varying action transformation to restrict the effective action space in the early stage, thereby encouraging more effective data collection and policy learning, and then progressively expands it to enhance exploration and achieve higher expected return. We prove that this transformation preserves the PPO update rule and introduces only bounded, vanishing gradient distortion, thereby ensuring stable training. We evaluate GPO on both quadruped and hexapod robots, including zero-shot deployment of simulation-trained policies on hardware. Policies trained with GPO consistently achieve better performance. These results suggest that GPO provides a general, environment-agnostic optimization framework for learning legged locomotion.

### Paper 2: [2601.20846]
**Title:** End-to-end example-based sim-to-real RL policy transfer based on neural stylisation with application to robotic cutting
**Category:** cs.RO
**Score:** 0.7892
**In MiniLM top-20:** True

Whereas reinforcement learning has been applied with success to a range of robotic control problems in complex, uncertain environments, reliance on extensive data - typically sourced from simulation environments - limits real-world deployment due to the domain gap between simulated and physical systems, coupled with limited real-world sample availability. We propose a novel method for sim-to-real transfer of reinforcement learning policies, based on a reinterpretation of neural style transfer from image processing to synthesise novel training data from unpaired unlabelled real world datasets. We employ a variational autoencoder to jointly learn self-supervised feature representations for style transfer and generate weakly paired source-target trajectories to improve physical realism of synthesised trajectories. We demonstrate the application of our approach based on the case study of robot cutting of unknown materials. Compared to baseline methods, including our previous work, CycleGAN, and conditional variational autoencoder-based time series translation, our approach achieves improved task completion time and behavioural stability with minimal real-world data. Our framework demonstrates robustness to geometric and material variation, and highlights the feasibility of policy adaptation in challenging contact-rich tasks where real-world reward information is unavailable.

### Paper 3: [2505.22094]
**Title:** ReinFlow: Fine-tuning Flow Matching Policy with Online Reinforcement Learning
**Category:** cs.RO
**Score:** 0.7863
**In MiniLM top-20:** True

We propose ReinFlow, a simple yet effective online reinforcement learning (RL) framework that fine-tunes a family of flow matching policies for continuous robotic control. Derived from rigorous RL theory, ReinFlow injects learnable noise into a flow policy's deterministic path, converting the flow into a discrete-time Markov Process for exact and straightforward likelihood computation. This conversion facilitates exploration and ensures training stability, enabling ReinFlow to fine-tune diverse flow model variants, including Rectified Flow [35] and Shortcut Models [19], particularly at very few or even one denoising step. We benchmark ReinFlow in representative locomotion and manipulation tasks, including long-horizon planning with visual input and sparse reward. The episode reward of Rectified Flow policies obtained an average net growth of 135.36% after fine-tuning in challenging legged locomotion tasks while saving denoising steps and 82.63% of wall time compared to state-of-the-art diffusion RL fine-tuning method DPPO [43]. The success rate of the Shortcut Model policies in state and visual manipulation tasks achieved an average net increase of 40.34% after fine-tuning with ReinFlow at four or even one denoising step, whose performance is comparable to fine-tuned DDIM policies while saving computation time for an average of 23.20%. Project webpage: https://reinflow.github.io/

### Paper 4: [2505.06357]
**Title:** DAPPER: Discriminability-Aware Policy-to-Policy Preference-Based Reinforcement Learning for Query-Efficient Robot Skill Acquisition
**Category:** cs.RO
**Score:** 0.7850
**In MiniLM top-20:** True

Preference-based Reinforcement Learning (PbRL) enables policy learning through simple queries comparing trajectories from a single policy. While human responses to these queries make it possible to learn policies aligned with human preferences, PbRL suffers from low query efficiency, as policy bias limits trajectory diversity and reduces the number of discriminable queries available for learning preferences. This paper identifies preference discriminability, which quantifies how easily a human can judge which trajectory is closer to their ideal behavior, as a key metric for improving query efficiency. To address this, we move beyond comparisons within a single policy and instead generate queries by comparing trajectories from multiple policies, as training them from scratch promotes diversity without policy bias. We propose Discriminability-Aware Policy-to-Policy Preference-Based Efficient Reinforcement Learning (DAPPER), which integrates preference discriminability with trajectory diversification achieved by multiple policies. DAPPER trains new policies from scratch after each reward update and employs a discriminator that learns to estimate preference discriminability, enabling the prioritized sampling of more discriminable queries. During training, it jointly maximizes the preference reward and preference discriminability score, encouraging the discovery of highly rewarding and easily distinguishable policies. Experiments in simulated and real-world legged robot environments demonstrate that DAPPER outperforms previous methods in query efficiency, particularly under challenging preference discriminability conditions. A supplementary video that facilitates understanding of the proposed framework and its experimental results is available at: https://youtu.be/lRwX8FNN8n4

### Paper 5: [2601.15761]
**Title:** Off-Policy Actor-Critic with Sigmoid-Bounded Entropy for Real-World Robot Learning
**Category:** cs.AI
**Score:** 0.7842
**In MiniLM top-20:** True

Deploying reinforcement learning in the real world remains challenging due to sample inefficiency, sparse rewards, and noisy visual observations. Prior work leverages demonstrations and human feedback to improve learning efficiency and robustness. However, offline-to-online methods need large datasets and can be unstable, while VLA-assisted RL relies on large-scale pretraining and fine-tuning. As a result, a low-cost real-world RL method with minimal data requirements has yet to emerge. We introduce \textbf{SigEnt-SAC}, an off-policy actor-critic method that learns from scratch using a single expert trajectory. Our key design is a sigmoid-bounded entropy term that prevents negative-entropy-driven optimization toward out-of-distribution actions and reduces Q-function oscillations. We benchmark SigEnt-SAC on D4RL tasks against representative baselines. Experiments show that SigEnt-SAC substantially alleviates Q-function oscillations and reaches a 100\% success rate faster than prior methods. Finally, we validate SigEnt-SAC on four real-world robotic tasks across multiple embodiments, where agents learn from raw images and sparse rewards; results demonstrate that SigEnt-SAC can learn successful policies with only a small number of real-world interactions, suggesting a low-cost and practical pathway for real-world RL deployment.

### Paper 6: [2509.18631]
**Title:** Generalizable Domain Adaptation for Sim-and-Real Policy Co-Training
**Category:** cs.RO
**Score:** 0.7399
**In MiniLM top-20:** True

Behavior cloning has shown promise for robot manipulation, but real-world demonstrations are costly to acquire at scale. While simulated data offers a scalable alternative, particularly with advances in automated demonstration generation, transferring policies to the real world is hampered by various simulation and real domain gaps. In this work, we propose a unified sim-and-real co-training framework for learning generalizable manipulation policies that primarily leverages simulation and only requires a few real-world demonstrations. Central to our approach is learning a domain-invariant, task-relevant feature space. Our key insight is that aligning the joint distributions of observations and their corresponding actions across domains provides a richer signal than aligning observations (marginals) alone. We achieve this by embedding an Optimal Transport (OT)-inspired loss within the co-training framework, and extend this to an Unbalanced OT framework to handle the imbalance between abundant simulation data and limited real-world examples. We validate our method on challenging manipulation tasks, showing it can leverage abundant simulation data to achieve up to a 30% improvement in the real-world success rate and even generalize to scenarios seen only in simulation. Project webpage: https://ot-sim2real.github.io/.

### Paper 7: [2504.16680]
**Title:** Uncertainty-Aware Robotic World Model Makes Offline Model-Based Reinforcement Learning Work on Real Robots
**Category:** cs.RO
**Score:** 0.7289
**In MiniLM top-20:** True

Reinforcement Learning (RL) has achieved impressive results in robotics, yet high-performing pipelines remain highly task-specific, with little reuse of prior data. Offline Model-based RL (MBRL) offers greater data efficiency by training policies entirely from existing datasets, but suffers from compounding errors and distribution shift in long-horizon rollouts. Although existing methods have shown success in controlled simulation benchmarks, robustly applying them to the noisy, biased, and partially observed datasets typical of real-world robotics remains challenging. We present a principled pipeline for making offline MBRL effective on physical robots. Our RWM-U extends autoregressive world models with epistemic uncertainty estimation, enabling temporally consistent multi-step rollouts with uncertainty effectively propagated over long horizons. We combine RWM-U with MOPO-PPO, which adapts uncertainty-penalized policy optimization to the stable, on-policy PPO framework for real-world control. We evaluate our approach on diverse manipulation and locomotion tasks in simulation and on real quadruped and humanoid, training policies entirely from offline datasets. The resulting policies consistently outperform model-free and uncertainty-unaware model-based baselines, and fusing real-world data in model learning further yields robust policies that surpass online model-free baselines trained solely in simulation.

### Paper 8: [2505.18763]
**Title:** GenPO: Generative Diffusion Models Meet On-Policy Reinforcement Learning
**Category:** cs.LG
**Score:** 0.7284
**In MiniLM top-20:** True

Recent advances in reinforcement learning (RL) have demonstrated the powerful exploration capabilities and multimodality of generative diffusion-based policies. While substantial progress has been made in offline RL and off-policy RL settings, integrating diffusion policies into on-policy frameworks like PPO remains underexplored. This gap is particularly significant given the widespread use of large-scale parallel GPU-accelerated simulators, such as IsaacLab, which are optimized for on-policy RL algorithms and enable rapid training of complex robotic tasks. A key challenge lies in computing state-action log-likelihoods under diffusion policies, which is straightforward for Gaussian policies but intractable for flow-based models due to irreversible forward-reverse processes and discretization errors (e.g., Euler-Maruyama approximations). To bridge this gap, we propose GenPO, a generative policy optimization framework that leverages exact diffusion inversion to construct invertible action mappings. GenPO introduces a novel doubled dummy action mechanism that enables invertibility via alternating updates, resolving log-likelihood computation barriers. Furthermore, we also use the action log-likelihood for unbiased entropy and KL divergence estimation, enabling KL-adaptive learning rates and entropy regularization in on-policy updates. Extensive experiments on eight IsaacLab benchmarks, including legged locomotion (Ant, Humanoid, Anymal-D, Unitree H1, Go2), dexterous manipulation (Shadow Hand), aerial control (Quadcopter), and robotic arm tasks (Franka), demonstrate GenPO's superiority over existing RL baselines. Notably, GenPO is the first method to successfully integrate diffusion policies into on-policy RL, unlocking their potential for large-scale parallelized training and real-world robotic deployment.

### Paper 9: [2509.04069]
**Title:** Solving Robotics Tasks with Prior Demonstration via Exploration-Efficient Deep Reinforcement Learning
**Category:** cs.RO
**Score:** 0.7219
**In MiniLM top-20:** True

This paper proposes an exploration-efficient Deep Reinforcement Learning with Reference policy (DRLR) framework for learning robotics tasks that incorporates demonstrations. The DRLR framework is developed based on an algorithm called Imitation Bootstrapped Reinforcement Learning (IBRL). We propose to improve IBRL by modifying the action selection module. The proposed action selection module provides a calibrated Q-value, which mitigates the bootstrapping error that otherwise leads to inefficient exploration. Furthermore, to prevent the RL policy from converging to a sub-optimal policy, SAC is used as the RL policy instead of TD3. The effectiveness of our method in mitigating bootstrapping error and preventing overfitting is empirically validated by learning two robotics tasks: bucket loading and open drawer, which require extensive interactions with the environment. Simulation results also demonstrate the robustness of the DRLR framework across tasks with both low and high state-action dimensions, and varying demonstration qualities. To evaluate the developed framework on a real-world industrial robotics task, the bucket loading task is deployed on a real wheel loader. The sim2real results validate the successful deployment of the DRLR framework.

### Paper 10: [2601.00675]
**Title:** RoboReward: General-Purpose Vision-Language Reward Models for Robotics
**Category:** cs.RO
**Score:** 0.7106
**In MiniLM top-20:** True

A well-designed reward is critical for effective reinforcement learning-based policy improvement. In real-world robotics, obtaining such rewards typically requires either labor-intensive human labeling or brittle, handcrafted objectives. Vision-language models (VLMs) have shown promise as automatic reward models, yet their effectiveness on real robot tasks is poorly understood. In this work, we aim to close this gap by introducing (1) RoboReward, a robotics reward dataset and benchmark built on large-scale real-robot corpora from Open X-Embodiment (OXE) and RoboArena, and (2) vision-language reward models trained on this dataset (RoboReward 4B/8B). Because OXE is success-heavy and lacks failure examples, we propose a negative examples data augmentation pipeline that generates calibrated negative and near-misses via counterfactual relabeling of successful episodes and temporal clipping to create partial-progress outcomes from the same videos. Using this framework, we build a large training and evaluation dataset spanning diverse tasks and embodiments to test whether state-of-the-art VLMs can reliably provide rewards for robot learning. Our evaluation of open and proprietary VLMs finds that no model excels across tasks, highlighting substantial room for improvement. We then train general-purpose 4B- and 8B-parameter models that outperform much larger VLMs in assigning rewards for short-horizon robotic tasks. Finally, we deploy the 8B model in real-robot reinforcement learning and find that it improves policy learning over Gemini Robotics-ER 1.5 while narrowing the gap to RL training with human-provided rewards. We release the full dataset, trained reward models, and evaluation suite on our website to advance the development of general-purpose reward models in robotics: https://crfm.stanford.edu/helm/robo-reward-bench (project website).

### Paper 11: [2509.25756]
**Title:** SAC Flow: Sample-Efficient Reinforcement Learning of Flow-Based Policies via Velocity-Reparameterized Sequential Modeling
**Category:** cs.RO
**Score:** 0.7025
**In MiniLM top-20:** True

Training expressive flow-based policies with off-policy reinforcement learning is notoriously unstable due to gradient pathologies in the multi-step action sampling process. We trace this instability to a fundamental connection: the flow rollout is algebraically equivalent to a residual recurrent computation, making it susceptible to the same vanishing and exploding gradients as RNNs. To address this, we reparameterize the velocity network using principles from modern sequential models, introducing two stable architectures: Flow-G, which incorporates a gated velocity, and Flow-T, which utilizes a decoded velocity. We then develop a practical SAC-based algorithm, enabled by a noise-augmented rollout, that facilitates direct end-to-end training of these policies. Our approach supports both from-scratch and offline-to-online learning and achieves state-of-the-art performance on continuous control and robotic manipulation benchmarks, eliminating the need for common workarounds like policy distillation or surrogate objectives.

### Paper 12: [2601.07821]
**Title:** Failure-Aware RL: Reliable Offline-to-Online Reinforcement Learning with Self-Recovery for Real-World Manipulation
**Category:** cs.RO
**Score:** 0.7014
**In MiniLM top-20:** True

Post-training algorithms based on deep reinforcement learning can push the limits of robotic models for specific objectives, such as generalizability, accuracy, and robustness. However, Intervention-requiring Failures (IR Failures) (e.g., a robot spilling water or breaking fragile glass) during real-world exploration happen inevitably, hindering the practical deployment of such a paradigm. To tackle this, we introduce Failure-Aware Offline-to-Online Reinforcement Learning (FARL), a new paradigm minimizing failures during real-world reinforcement learning. We create FailureBench, a benchmark that incorporates common failure scenarios requiring human intervention, and propose an algorithm that integrates a world-model-based safety critic and a recovery policy trained offline to prevent failures during online exploration. Extensive simulation and real-world experiments demonstrate the effectiveness of FARL in significantly reducing IR Failures while improving performance and generalization during online reinforcement learning post-training. FARL reduces IR Failures by 73.1% while elevating performance by 11.3% on average during real-world RL post-training. Videos and code are available at https://failure-aware-rl.github.io.

### Paper 13 [DIVERGENT]: [2601.18107]
**Title:** Beyond Static Datasets: Robust Offline Policy Optimization via Vetted Synthetic Transitions
**Category:** cs.LG
**Score:** 0.6924
**In MiniLM top-20:** False

Offline Reinforcement Learning (ORL) holds immense promise for safety-critical domains like industrial robotics, where real-time environmental interaction is often prohibitive. A primary obstacle in ORL remains the distributional shift between the static dataset and the learned policy, which typically mandates high degrees of conservatism that can restrain potential policy improvements. We present MoReBRAC, a model-based framework that addresses this limitation through Uncertainty-Aware latent synthesis. Instead of relying solely on the fixed data, MoReBRAC utilizes a dual-recurrent world model to synthesize high-fidelity transitions that augment the training manifold. To ensure the reliability of this synthetic data, we implement a hierarchical uncertainty pipeline integrating Variational Autoencoder (VAE) manifold detection, model sensitivity analysis, and Monte Carlo (MC) dropout. This multi-layered filtering process guarantees that only transitions residing within high-confidence regions of the learned dynamics are utilized. Our results on D4RL Gym-MuJoCo benchmarks reveal significant performance gains, particularly in ``random'' and ``suboptimal'' data regimes. We further provide insights into the role of the VAE as a geometric anchor and discuss the distributional trade-offs encountered when learning from near-optimal datasets.

### Paper 14: [2512.17853]
**Title:** AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning
**Category:** cs.RO
**Score:** 0.6879
**In MiniLM top-20:** True

Generalist robot learning remains constrained by data: large-scale, diverse, and high-quality interaction data are expensive to collect in the real world. While simulation has become a promising way for scaling up data collection, the related tasks, including simulation task design, task-aware scene generation, expert demonstration synthesis, and sim-to-real transfer, still demand substantial human effort. We present AnyTask, an automated framework that pairs massively parallel GPU simulation with foundation models to design diverse manipulation tasks and synthesize robot data. We introduce three AnyTask agents for generating expert demonstrations aiming to solve as many tasks as possible: 1) ViPR, a novel task and motion planning agent with VLM-in-the-loop Parallel Refinement; 2) ViPR-Eureka, a reinforcement learning agent with generated dense rewards and LLM-guided contact sampling; 3) ViPR-RL, a hybrid planning and learning approach that jointly produces high-quality demonstrations with only sparse rewards. We train behavior cloning policies on generated data, validate them in simulation, and deploy them directly on real robot hardware. The policies generalize to novel object poses, achieving 44% average success across a suite of real-world pick-and-place, drawer opening, contact-rich pushing, and long-horizon manipulation tasks. Our project website is at https://anytask.rai-inst.com .

### Paper 15 [DIVERGENT]: [2601.11143]
**Title:** Learning Quadrupedal Locomotion for a Heavy Hydraulic Robot Using an Actuator Model
**Category:** cs.RO
**Score:** 0.6863
**In MiniLM top-20:** False

The simulation-to-reality (sim-to-real) transfer of large-scale hydraulic robots presents a significant challenge in robotics because of the inherent slow control response and complex fluid dynamics. The complex dynamics result from the multiple interconnected cylinder structure and the difference in fluid rates of the cylinders. These characteristics complicate detailed simulation for all joints, making it unsuitable for reinforcement learning (RL) applications. In this work, we propose an analytical actuator model driven by hydraulic dynamics to represent the complicated actuators. The model predicts joint torques for all 12 actuators in under 1 microsecond, allowing rapid processing in RL environments. We compare our model with neural network-based actuator models and demonstrate the advantages of our model in data-limited scenarios. The locomotion policy trained in RL with our model is deployed on a hydraulic quadruped robot, which is over 300 kg. This work is the first demonstration of a successful transfer of stable and robust command-tracking locomotion with RL on a heavy hydraulic quadruped robot, demonstrating advanced sim-to-real transferability.

### Paper 16 [DIVERGENT]: [2601.01803]
**Title:** Moments Matter:Stabilizing Policy Optimization using Return Distributions
**Category:** cs.LG
**Score:** 0.6856
**In MiniLM top-20:** False

Deep Reinforcement Learning (RL) agents often learn policies that achieve the same episodic return yet behave very differently, due to a combination of environmental (random transitions, initial conditions, reward noise) and algorithmic (minibatch selection, exploration noise) factors. In continuous control tasks, even small parameter shifts can produce unstable gaits, complicating both algorithm comparison and real-world transfer. Previous work has shown that such instability arises when policy updates traverse noisy neighborhoods and that the spread of post-update return distribution $R(\theta)$, obtained by repeatedly sampling minibatches, updating $\theta$, and measuring final returns, is a useful indicator of this noise. Although explicitly constraining the policy to maintain a narrow $R(\theta)$ can improve stability, directly estimating $R(\theta)$ is computationally expensive in high-dimensional settings. We propose an alternative that takes advantage of environmental stochasticity to mitigate update-induced variability. Specifically, we model state-action return distribution through a distributional critic and then bias the advantage function of PPO using higher-order moments (skewness and kurtosis) of this distribution. By penalizing extreme tail behaviors, our method discourages policies from entering parameter regimes prone to instability. We hypothesize that in environments where post-update critic values align poorly with post-update returns, standard PPO struggles to produce a narrow $R(\theta)$. In such cases, our moment-based correction narrows $R(\theta)$, improving stability by up to 75% in Walker2D, while preserving comparable evaluation returns.

### Paper 17 [DIVERGENT]: [2601.12730]
**Title:** Distribution-Centric Policy Optimization Dominates Exploration-Exploitation Trade-off
**Category:** cs.LG
**Score:** 0.6856
**In MiniLM top-20:** False

The exploration-exploitation (EE) trade-off is a central challenge in reinforcement learning (RL) for large language models (LLMs). With Group Relative Policy Optimization (GRPO), training tends to be exploitation driven: entropy decreases monotonically, samples convergence, and exploration fades. Most existing fixes are \textbf{sample-centric}: they seek or bonus rare samples, assuming exploration comes from novel trajectories and tokens. These heuristics depend on the "luck" of informative samples, lack principled control of the policy, and often yield limited or inconsistent gains. In this work, we are the first to introduce a \textbf{distribution-centric} perspective for RL, in which exploration is always guided by a "better" target distribution, and reveal that a policy's ability to resist entropy collapse is governed by the distribution itself rather than individual samples. Building on this insight, we propose Distribution-Centric Policy Optimization (DCPO), which reformulates entropy regulation as distribution-level regularization. DCPO achieves controllable entropy fully on-policy without sampling from external distributions, enabling efficient exploration while maintaining training stability. Across multiple models and seven benchmarks, DCPO improves over GRPO by about 20\% on average. Overall, DCPO replaces sample-level heuristics with distribution-level principles, offering a theoretically grounded and flexible framework for controllable exploration and a stronger EE trade-off. The code is available in https://github.com/597358816/DCPO.

### Paper 18: [2601.06748]
**Title:** On-the-Fly VLA Adaptation via Test-Time Reinforcement Learning
**Category:** cs.RO
**Score:** 0.6845
**In MiniLM top-20:** True

Vision-Language-Action models have recently emerged as a powerful paradigm for general-purpose robot learning, enabling agents to map visual observations and natural-language instructions into executable robotic actions. Though popular, they are primarily trained via supervised fine-tuning or training-time reinforcement learning, requiring explicit fine-tuning phases, human interventions, or controlled data collection. Consequently, existing methods remain unsuitable for challenging simulated- or physical-world deployments, where robots must respond autonomously and flexibly to evolving environments. To address this limitation, we introduce a Test-Time Reinforcement Learning for VLAs (TT-VLA), a framework that enables on-the-fly policy adaptation during inference. TT-VLA formulates a dense reward mechanism that leverages step-by-step task-progress signals to refine action policies during test time while preserving the SFT/RL-trained priors, making it an effective supplement to current VLA models. Empirical results show that our approach enhances overall adaptability, stability, and task success in dynamic, previously unseen scenarios under simulated and real-world settings. We believe TT-VLA offers a principled step toward self-improving, deployment-ready VLAs.

### Paper 19 [DIVERGENT]: [2512.24740]
**Title:** Control of Microrobots with Reinforcement Learning under On-Device Compute Constraints
**Category:** cs.RO
**Score:** 0.6830
**In MiniLM top-20:** False

An important function of autonomous microrobots is the ability to perform robust movement over terrain. This paper explores an edge ML approach to microrobot locomotion, allowing for on-device, lower latency control under compute, memory, and power constraints. This paper explores the locomotion of a sub-centimeter quadrupedal microrobot via reinforcement learning (RL) and deploys the resulting controller on an ultra-small system-on-chip (SoC), SC$\mu$M-3C, featuring an ARM Cortex-M0 microcontroller running at 5 MHz. We train a compact FP32 multilayer perceptron (MLP) policy with two hidden layers ($[128, 64]$) in a massively parallel GPU simulation and enhance robustness by utilizing domain randomization over simulation parameters. We then study integer (Int8) quantization (per-tensor and per-feature) to allow for higher inference update rates on our resource-limited hardware, and we connect hardware power budgets to achievable update frequency via a cycles-per-update model for inference on our Cortex-M0. We propose a resource-aware gait scheduling viewpoint: given a device power budget, we can select the gait mode (trot/intermediate/gallop) that maximizes expected RL reward at a corresponding feasible update frequency. Finally, we deploy our MLP policy on a real-world large-scale robot on uneven terrain, qualitatively noting that domain-randomized training can improve out-of-distribution stability. We do not claim real-world large-robot empirical zero-shot transfer in this work.

### Paper 20 [DIVERGENT]: [2601.07118]
**Title:** Reward-Preserving Attacks For Robust Reinforcement Learning
**Category:** cs.LG
**Score:** 0.6726
**In MiniLM top-20:** False

Adversarial training in reinforcement learning (RL) is challenging because perturbations cascade through trajectories and compound over time, making fixed-strength attacks either overly destructive or too conservative. We propose reward-preserving attacks, which adapt adversarial strength so that an $\alpha$ fraction of the nominal-to-worst-case return gap remains achievable at each state. In deep RL, perturbation magnitudes $\eta$ are selected dynamically, using a learned critic $Q((s,a),\eta)$ that estimates the expected return of $\alpha$-reward-preserving rollouts. For intermediate values of $\alpha$, this adaptive training yields policies that are robust across a wide range of perturbation magnitudes while preserving nominal performance, outperforming fixed-radius and uniformly sampled-radius adversarial training.

---

## Review Instructions

You are reviewing the top-20 recommendations from qwen3 for the profile "RL for robotics".
Papers marked [DIVERGENT] are in qwen3's top-20 but NOT in MiniLM's.

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
