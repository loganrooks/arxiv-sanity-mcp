# Single-Strategy Characterization Review

**Model:** specter2
**Profile:** Mathematical foundations of neural networks (P8)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to specter2

## Seed Papers
  - [2504.05695] Architecture independent generalization bounds for overparametrized deep ReLU networks (cs.LG)
  - [2601.08100] Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds (stat.ML)
  - [2507.21429] From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions (stat.ML)
  - [2204.12392] A PAC-Bayes oracle inequality for sparse neural networks (math.ST)
  - [2407.17092] Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications (math.NA)

## specter2 Top-20 Recommendations

### Paper 1: [2601.08100]
**Title:** Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds
**Category:** stat.ML
**Score:** 0.9659
**In MiniLM top-20:** True

Understanding the generalization behavior of deep neural networks remains a fundamental challenge in modern statistical learning theory. Among existing approaches, PAC-Bayesian norm-based bounds have demonstrated particular promise due to their data-dependent nature and their ability to capture algorithmic and geometric properties of learned models. However, most existing results rely on isotropic Gaussian posteriors, heavy use of spectral-norm concentration for weight perturbations, and largely architecture-agnostic analyses, which together limit both the tightness and practical relevance of the resulting bounds. To address these limitations, in this work, we propose a unified framework for PAC-Bayesian norm-based generalization by reformulating the derivation of generalization bounds as a stochastic optimization problem over anisotropic Gaussian posteriors. The key to our approach is a sensitivity matrix that quantifies the network outputs with respect to structured weight perturbations, enabling the explicit incorporation of heterogeneous parameter sensitivities and architectural structures. By imposing different structural assumptions on this sensitivity matrix, we derive a family of generalization bounds that recover several existing PAC-Bayesian results as special cases, while yielding bounds that are comparable to or tighter than state-of-the-art approaches. Such a unified framework provides a principled and flexible way for geometry-/structure-aware and interpretable generalization analysis in deep learning.

### Paper 2: [2507.21429]
**Title:** From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions
**Category:** stat.ML
**Score:** 0.9632
**In MiniLM top-20:** True

Gradient descent (GD) on deep neural network loss landscapes is non-convex, yet often converges far faster in practice than classical guarantees suggest. Prior work shows that within locally quasi-convex regions (LQCRs), GD converges to stationary points at sublinear rates, leaving the commonly observed near-exponential training dynamics unexplained. We show that, under a mild local Neural Tangent Kernel (NTK) stability assumption, the loss satisfies a PL-type error bound within these regions, yielding a Locally Polyak-Lojasiewicz Region (LPLR) in which the squared gradient norm controls the suboptimality gap. For properly initialized finite-width networks, we show that under local NTK stability this PL-type mechanism holds around initialization and establish linear convergence of GD as long as the iterates remain within the resulting LPLR. Empirically, we observe PL-like scaling and linear-rate loss decay in controlled full-batch training and in a ResNet-style CNN trained with mini-batch SGD on a CIFAR-10 subset, indicating that LPLR signatures can persist under modern architectures and stochastic optimization. Overall, the results connect local geometric structure, local NTK stability, and fast optimization rates in a finite-width setting.

### Paper 3: [2504.05695]
**Title:** Architecture independent generalization bounds for overparametrized deep ReLU networks
**Category:** cs.LG
**Score:** 0.9624
**In MiniLM top-20:** True

We prove that overparametrized neural networks are able to generalize with a test error that is independent of the level of overparametrization, and independent of the Vapnik-Chervonenkis (VC) dimension. We prove explicit bounds that only depend on the metric geometry of the test and training sets, on the regularity properties of the activation function, and on the operator norms of the weights and norms of biases. For overparametrized deep ReLU networks with a training sample size bounded by the input space dimension, we explicitly construct zero loss minimizers without use of gradient descent, and prove a uniform generalization bound that is independent of the network architecture. We perform computational experiments of our theoretical results with MNIST, and obtain agreement with the true test error within a 22 % margin on average.

### Paper 4: [2407.18384]
**Title:** Mathematical theory of deep learning
**Category:** cs.LG
**Score:** 0.9607
**In MiniLM top-20:** True

This book provides an introduction to the mathematical analysis of deep learning. It covers fundamental results in approximation theory, optimization theory, and statistical learning theory, which are the three main pillars of deep neural network theory. Serving as a guide for students and researchers in mathematics and related fields, the book aims to equip readers with foundational knowledge on the topic. It prioritizes simplicity over generality, and presents rigorous yet accessible results to help build an understanding of the essential mathematical concepts underpinning deep learning.

### Paper 5: [2601.01295]
**Title:** Sobolev Approximation of Deep ReLU Networks in Log-Barron Space
**Category:** cs.LG
**Score:** 0.9575
**In MiniLM top-20:** True

Universal approximation theorems show that neural networks can approximate any continuous function; however, the number of parameters may grow exponentially with the ambient dimension, so these results do not fully explain the practical success of deep models on high-dimensional data. Barron space theory addresses this: if a target function belongs to a Barron space, a two-layer network with $n$ parameters achieves an $O(n^{-1/2})$ approximation error in $L^2$. Yet classical Barron spaces $\mathscr{B}^{s+1}$ still require stronger regularity than Sobolev spaces $H^s$, and existing depth-sensitive results often assume constraints such as $sL \le 1/2$. In this paper, we introduce a log-weighted Barron space $\mathscr{B}^{\log}$, which requires a strictly weaker assumption than $\mathscr{B}^s$ for any $s>0$. For this new function space, we first study embedding properties and carry out a statistical analysis via the Rademacher complexity. Then we prove that functions in $\mathscr{B}^{\log}$ can be approximated by deep ReLU networks with explicit depth dependence. We then define a family $\mathscr{B}^{s,\log}$, establish approximation bounds in the $H^1$ norm, and identify maximal depth scales under which these rates are preserved. Our results clarify how depth reduces regularity requirements for efficient representation, offering a more precise explanation for the performance of deep architectures beyond the classical Barron setting, and for their stable use in high-dimensional problems used today.

### Paper 6: [2512.24381]
**Title:** Tubular Riemannian Laplace Approximations for Bayesian Neural Networks
**Category:** cs.LG
**Score:** 0.9559
**In MiniLM top-20:** True

Laplace approximations are among the simplest and most practical methods for approximate Bayesian inference in neural networks, yet their Euclidean formulation struggles with the highly anisotropic, curved loss surfaces and large symmetry groups that characterize modern deep models. Recent work has proposed Riemannian and geometric Gaussian approximations to adapt to this structure. Building on these ideas, we introduce the Tubular Riemannian Laplace (TRL) approximation. TRL explicitly models the posterior as a probabilistic tube that follows a low-loss valley induced by functional symmetries, using a Fisher/Gauss-Newton metric to separate prior-dominated tangential uncertainty from data-dominated transverse uncertainty. We interpret TRL as a scalable reparametrised Gaussian approximation that utilizes implicit curvature estimates to operate in high-dimensional parameter spaces. Our empirical evaluation on ResNet-18 (CIFAR-10 and CIFAR-100) demonstrates that TRL achieves excellent calibration, matching or exceeding the reliability of Deep Ensembles (in terms of ECE) while requiring only a fraction (1/5) of the training cost. TRL effectively bridges the gap between single-model efficiency and ensemble-grade reliability.

### Paper 7: [2204.12392]
**Title:** A PAC-Bayes oracle inequality for sparse neural networks
**Category:** math.ST
**Score:** 0.9537
**In MiniLM top-20:** True

We study the Gibbs posterior distribution for sparse deep neural nets in a nonparametric regression setting. The posterior can be accessed via Metropolis-adjusted Langevin algorithms. Using a mixture over uniform priors on sparse sets of network weights, we prove an oracle inequality which shows that the method adapts to the unknown regularity and hierarchical structure of the regression function. The estimator achieves the minimax-optimal rate of convergence (up to a logarithmic factor).

### Paper 8: [2510.21245]
**Title:** Convergence of Stochastic Gradient Langevin Dynamics in the Lazy Training Regime
**Category:** cs.LG
**Score:** 0.9487
**In MiniLM top-20:** True

Continuous-time models provide important insights into the training dynamics of optimization algorithms in deep learning. In this work, we establish a non-asymptotic convergence analysis of stochastic gradient Langevin dynamics (SGLD), which is an It\^o stochastic differential equation (SDE) approximation of stochastic gradient descent in continuous time, in the lazy training regime. We show that, under regularity conditions on the Hessian of the loss function, SGLD with multiplicative and state-dependent noise (i) yields a non-degenerate kernel throughout the training process with high probability, and (ii) achieves exponential convergence to the empirical risk minimizer in expectation, and we establish finite-time and finite-width bounds on the optimality gap. We corroborate our theoretical findings with numerical examples in the regression setting.

### Paper 9: [2601.08547]
**Title:** Convergence of gradient flow for learning convolutional neural networks
**Category:** math.OC
**Score:** 0.9484
**In MiniLM top-20:** True

Convolutional neural networks are widely used in imaging and image recognition. Learning such networks from training data leads to the minimization of a non-convex function. This makes the analysis of standard optimization methods such as variants of (stochastic) gradient descent challenging. In this article we study the simplified setting of linear convolutional networks. We show that the gradient flow (to be interpreted as an abstraction of gradient descent) applied to the empirical risk defined via certain loss functions including the square loss always converges to a critical point, under a mild condition on the training data.

### Paper 10 [DIVERGENT]: [2410.14951]
**Title:** Architectural Scaling Surpass Basis Complexity? Efficient KANs with Single-Parameter Design
**Category:** cs.AI
**Score:** 0.9470
**In MiniLM top-20:** False

The landscape of Kolmogorov-Arnold Networks (KANs) is rapidly expanding, yet lacks a unified theoretical framework and a clear principle for efficient architecture design. This paper addresses these gaps with three core contributions. First, we introduce the Universal KAN (Uni-KAN) framework, a novel abstraction that formally unifies all KAN-style networks through dense and sparse representations. We prove their interchangeability and provide an open-source library for this framework, facilitating future research. Second, we propose the Efficient KAN Expansion (EKE) Hypothesis, a design philosophy positing that allocating parameters to architectural scaling rather than basis function complexity yields superior performance. Third, we present Single-Parameter KANs (SKANs), a family of ultra-lightweight networks that embody the EKE Hypothesis. Our comprehensive experiments provide the first strong empirical validation for the theoretical necessity of basis function smoothness for stable training. Furthermore, SKANs demonstrate state-of-the-art performance, improving F1 scores by up to 6.51\% and reducing test loss by 93.1\%, while achieving up to 6x faster training speeds compared to existing KAN variants. These results establish a robust framework, a guiding hypothesis, and a practical methodology for designing the next generation of efficient and powerful neural networks. The code is accessible at https://anonymous.4open.science/r/SKAN-EBBB/.

### Paper 11: [2601.21750]
**Title:** FISMO: Fisher-Structured Momentum-Orthogonalized Optimizer
**Category:** cs.LG
**Score:** 0.9462
**In MiniLM top-20:** True

Training large-scale neural networks requires solving nonconvex optimization where the choice of optimizer fundamentally determines both convergence behavior and computational efficiency. While adaptive methods like Adam have long dominated practice, the recently proposed Muon optimizer achieves superior performance through orthogonalized momentum updates that enforce isotropic geometry with uniform singular values. However, this strict isotropy discards potentially valuable curvature information encoded in gradient spectra, motivating optimization methods that balance geometric structure with adaptivity. We introduce FISMO (Fisher-Structured Momentum-Orthogonalized) optimizer, which generalizes isotropic updates to incorporate anisotropic curvature information through Fisher information geometry. By reformulating the optimizer update as a trust-region problem constrained by a Kronecker-factored Fisher metric, FISMO achieves structured preconditioning that adapts to local loss landscape geometry while maintaining computational tractability. We establish convergence guarantees for FISMO in stochastic nonconvex settings, proving an $\mathcal{O}(1/\sqrt{T})$ rate for the expected squared gradient norm with explicit characterization of variance reduction through mini-batching. Empirical evaluation on image classification and language modeling benchmarks demonstrates that FISMO achieves superior training efficiency and final performance compared to established baselines.

### Paper 12: [2601.05732]
**Title:** mHC-lite: You Don't Need 20 Sinkhorn-Knopp Iterations
**Category:** cs.LG
**Score:** 0.9448
**In MiniLM top-20:** True

Hyper-Connections (HC) generalizes residual connections by introducing dynamic residual matrices that mix information across multiple residual streams, accelerating convergence in deep neural networks. However, unconstrained residual matrices can compromise training stability. To address this, DeepSeek's Manifold-Constrained Hyper-Connections (mHC) approximately projects these matrices onto the Birkhoff polytope via iterative Sinkhorn--Knopp (SK) normalization. We identify two limitations of this approach: (i) finite SK iterations do not guarantee exact doubly stochasticity, leaving an approximation gap that can accumulate through network depth and undermine stability; (ii) efficient SK implementation requires highly specialized CUDA kernels, raising engineering barriers and reducing portability. Motivated by the Birkhoff--von Neumann theorem, we propose mHC-lite, a simple reparameterization that explicitly constructs doubly stochastic matrices as convex combinations of permutation matrices. This approach guarantees exact doubly stochasticity by construction and can be implemented using only native matrix operations. Extensive experiments demonstrate that mHC-lite matches or exceeds mHC in performance while achieving higher training throughput with a naive implementation and eliminating the residual instabilities observed in both HC and mHC. The code is publicly available at https://github.com/FFTYYY/mhc-lite.

### Paper 13 [DIVERGENT]: [2601.06597]
**Title:** Implicit bias as a Gauge correction: Theory and Inverse Design
**Category:** cs.LG
**Score:** 0.9446
**In MiniLM top-20:** False

A central problem in machine learning theory is to characterize how learning dynamics select particular solutions among the many compatible with the training objective, a phenomenon, called implicit bias, which remains only partially characterized. In the present work, we identify a general mechanism, in terms of an explicit geometric correction of the learning dynamics, for the emergence of implicit biases, arising from the interaction between continuous symmetries in the model's parametrization and stochasticity in the optimization process. Our viewpoint is constructive in two complementary directions: given model symmetries, one can derive the implicit bias they induce; conversely, one can inverse-design a wide class of different implicit biases by computing specific redundant parameterizations. More precisely, we show that, when the dynamics is expressed in the quotient space obtained by factoring out the symmetry group of the parameterization, the resulting stochastic differential equation gains a closed form geometric correction in the stationary distribution of the optimizer dynamics favoring orbits with small local volume. We compute the resulting symmetry induced bias for a range of architectures, showing how several well known results fit into a single unified framework. The approach also provides a practical methodology for deriving implicit biases in new settings, and it yields concrete, testable predictions that we confirm by numerical simulations on toy models trained on synthetic data, leaving more complex scenarios for future work. Finally, we test the implicit bias inverse-design procedure in notable cases, including biases toward sparsity in linear features or in spectral properties of the model parameters.

### Paper 14: [2601.01853]
**Title:** Asymptotic Convergence and Stability of Adaptive Gradient Methods in Smooth Non-convex Optimization
**Category:** math.OC
**Score:** 0.9431
**In MiniLM top-20:** True

Adaptive gradient methods, such as AdaGrad, have become fundamental tools in deep learning. Despite their widespread use, the asymptotic convergence of AdaGrad remains poorly understood in non-convex scenarios. In this work, we present the first rigorous asymptotic convergence analysis of AdaGrad-Norm for smooth non-convex optimization. Using a novel stopping-time partitioning technique, we establish a key stability result: the objective function values remain bounded in expectation, and the iterates are bounded almost surely under a mild coercivity assumption. Building on these stability results, we prove that AdaGrad-Norm achieves both almost sure and mean-square convergence. Furthermore, we extend our analysis to RMSProp and show that, with appropriate hyperparameter choices, it also enjoys stability and asymptotic convergence. The techniques developed herein may be of independent interest for analyzing other adaptive stochastic optimization algorithms.

### Paper 15 [DIVERGENT]: [2311.16086]
**Title:** MAST: Model-Agnostic Sparsified Training
**Category:** cs.LG
**Score:** 0.9424
**In MiniLM top-20:** False

We introduce a novel optimization problem formulation that departs from the conventional way of minimizing machine learning model loss as a black-box function. Unlike traditional formulations, the proposed approach explicitly incorporates an initially pre-trained model and random sketch operators, allowing for sparsification of both the model and gradient during training. We establish the insightful properties of the proposed objective function and highlight its connections to the standard formulation. Furthermore, we present several variants of the Stochastic Gradient Descent (SGD) method adapted to the new problem formulation, including SGD with general sampling, a distributed version, and SGD with variance reduction techniques. We achieve tighter convergence rates and relax assumptions, bridging the gap between theoretical principles and practical applications, covering several important techniques such as Dropout and Sparse training. This work presents promising opportunities to enhance the theoretical understanding of model training through a sparsification-aware optimization approach.

### Paper 16 [DIVERGENT]: [2512.05534]
**Title:** A Unified Theory of Sparse Dictionary Learning in Mechanistic Interpretability: Piecewise Biconvexity and Spurious Minima
**Category:** cs.LG
**Score:** 0.9420
**In MiniLM top-20:** False

As AI models achieve remarkable capabilities across diverse domains, understanding what representations they learn and how they encode concepts has become increasingly important for both scientific progress and trustworthy deployment. Recent works in mechanistic interpretability have widely reported that neural networks represent meaningful concepts as linear directions in their representation spaces and often encode diverse concepts in superposition. Various sparse dictionary learning (SDL) methods, including sparse autoencoders, transcoders, and crosscoders, are utilized to address this by training auxiliary models with sparsity constraints to disentangle these superposed concepts into monosemantic features. These methods are the backbone of modern mechanistic interpretability, yet in practice they consistently produce polysemantic features, feature absorption, and dead neurons, with very limited theoretical understanding of why these phenomena occur. Existing theoretical work is limited to tied-weight sparse autoencoders, leaving the broader family of SDL methods without formal grounding. We develop the first unified theoretical framework that casts all major SDL variants as a single piecewise biconvex optimization problem, and characterize its global solution set, non-identifiability, and spurious optima. This analysis yields principled explanations for feature absorption and dead neurons. To expose these pathologies under full ground-truth access, we introduce the Linear Representation Bench. Guided by our theory, we propose feature anchoring, a novel technique that restores SDL identifiability, substantially improving feature recovery across synthetic benchmarks and real neural representations.

### Paper 17: [2601.14026]
**Title:** Universal Approximation Theorem for Input-Connected Multilayer Perceptrons
**Category:** cs.LG
**Score:** 0.9390
**In MiniLM top-20:** True

We introduce the Input-Connected Multilayer Perceptron (IC-MLP), a feedforward neural network architecture in which each hidden neuron receives, in addition to the outputs of the preceding layer, a direct affine connection from the raw input. We first study this architecture in the univariate setting and give an explicit and systematic description of IC-MLPs with an arbitrary finite number of hidden layers, including iterated formulas for the network functions. In this setting, we prove a universal approximation theorem showing that deep IC-MLPs can approximate any continuous function on a closed interval of the real line if and only if the activation function is nonlinear. We then extend the analysis to vector-valued inputs and establish a corresponding universal approximation theorem for continuous functions on compact subsets of $\mathbb{R}^n$.

### Paper 18 [DIVERGENT]: [2601.20961]
**Title:** A Theory of Universal Agnostic Learning
**Category:** cs.LG
**Score:** 0.9389
**In MiniLM top-20:** False

We provide a complete theory of optimal universal rates for binary classification in the agnostic setting. This extends the realizable-case theory of Bousquet, Hanneke, Moran, van Handel, and Yehudayoff (2021) by removing the realizability assumption on the distribution. We identify a fundamental tetrachotomy of optimal rates: for every concept class, the optimal universal rate of convergence of the excess error rate is one of $e^{-n}$, $e^{-o(n)}$, $o(n^{-1/2})$, or arbitrarily slow. We further identify simple combinatorial structures which determine which of these categories any given concept class falls into.

### Paper 19: [2312.08410]
**Title:** Universal approximation property of Banach space-valued random feature models including random neural networks
**Category:** cs.LG
**Score:** 0.9382
**In MiniLM top-20:** True

We introduce a Banach space-valued extension of random feature learning, a data-driven supervised machine learning technique for large-scale kernel approximation. By randomly initializing the feature maps, only the linear readout needs to be trained, which reduces the computational complexity substantially. Viewing random feature models as Banach space-valued random variables, we prove a universal approximation result in the corresponding Bochner space. Moreover, we derive approximation rates and an explicit algorithm to learn an element of the given Banach space by such models. The framework of this paper includes random trigonometric/Fourier regression and in particular random neural networks which are single-hidden-layer feedforward neural networks whose weights and biases are randomly initialized, whence only the linear readout needs to be trained. For the latter, we can then lift the universal approximation property of deterministic neural networks to random neural networks, even within function spaces over non-compact domains, e.g., weighted spaces, $L^p$-spaces, and (weighted) Sobolev spaces, where the latter includes the approximation of the (weak) derivatives. In addition, we analyze when the training costs for approximating a given function grow polynomially in both the input/output dimension and the reciprocal of a pre-specified tolerated approximation error. Furthermore, we demonstrate in a numerical example the empirical advantages of random feature models over their deterministic counterparts.

### Paper 20 [DIVERGENT]: [2311.08745]
**Title:** Using Stochastic Gradient Descent to Smooth Nonconvex Functions: Analysis of Implicit Graduated Optimization
**Category:** cs.LG
**Score:** 0.9380
**In MiniLM top-20:** False

The graduated optimization approach is a method for finding global optimal solutions for nonconvex functions by using a function smoothing operation with stochastic noise. This paper makes three contributions regarding graduated optimization. First, we extend the definition of function smoothing that is traditionally achieved through convolution with Gaussian noise and characterize for the first time function smoothing with heavy-tailed noise. Second, we show that light- or heavy-tailed stochastic noise in stochastic gradient descent (SGD) has the effect of smoothing the objective function, the degree of which is determined by the learning rate, batch size, and the moment of the stochastic noise. Using this finding, we propose and analyze a new graduated optimization algorithm that varies the degree of smoothing by varying the learning rate and batch size. Third, we relax the $\sigma$-nice property, a standard but restrictive condition in the analysis of graduated optimization. Our refinement enables convergence guarantees for a broader class of non-convex functions, thereby bridging the gap between theoretical assumptions and practical optimization landscapes.

---

## Review Instructions

You are reviewing the top-20 recommendations from specter2 for the profile "Mathematical foundations of neural networks".
Papers marked [DIVERGENT] are in specter2's top-20 but NOT in MiniLM's.

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
