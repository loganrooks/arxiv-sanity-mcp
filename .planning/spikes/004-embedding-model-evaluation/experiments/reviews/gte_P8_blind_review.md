# Blind Pairwise Qualitative Review

**Profile:** Mathematical foundations of neural networks (P8)
**Depth:** full
**Models:** Model A vs Model B (identities withheld)

## Seed Papers
  - [2504.05695] Architecture independent generalization bounds for overparametrized deep ReLU networks (cs.LG)
  - [2601.08100] Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds (stat.ML)
  - [2507.21429] From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions (stat.ML)
  - [2204.12392] A PAC-Bayes oracle inequality for sparse neural networks (math.ST)
  - [2407.17092] Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications (math.NA)

## Recommendations

### Model A Paper 1: [2601.08100]
**Title:** Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds
**Category:** stat.ML
**Score:** 0.8783

Understanding the generalization behavior of deep neural networks remains a fundamental challenge in modern statistical learning theory. Among existing approaches, PAC-Bayesian norm-based bounds have demonstrated particular promise due to their data-dependent nature and their ability to capture algorithmic and geometric properties of learned models. However, most existing results rely on isotropic Gaussian posteriors, heavy use of spectral-norm concentration for weight perturbations, and largely architecture-agnostic analyses, which together limit both the tightness and practical relevance of the resulting bounds. To address these limitations, in this work, we propose a unified framework for PAC-Bayesian norm-based generalization by reformulating the derivation of generalization bounds as a stochastic optimization problem over anisotropic Gaussian posteriors. The key to our approach is a sensitivity matrix that quantifies the network outputs with respect to structured weight perturbations, enabling the explicit incorporation of heterogeneous parameter sensitivities and architectural structures. By imposing different structural assumptions on this sensitivity matrix, we derive a family of generalization bounds that recover several existing PAC-Bayesian results as special cases, while yielding bounds that are comparable to or tighter than state-of-the-art approaches. Such a unified framework provides a principled and flexible way for geometry-/structure-aware and interpretable generalization analysis in deep learning.

### Model A Paper 2: [2504.05695]
**Title:** Architecture independent generalization bounds for overparametrized deep ReLU networks
**Category:** cs.LG
**Score:** 0.8586

We prove that overparametrized neural networks are able to generalize with a test error that is independent of the level of overparametrization, and independent of the Vapnik-Chervonenkis (VC) dimension. We prove explicit bounds that only depend on the metric geometry of the test and training sets, on the regularity properties of the activation function, and on the operator norms of the weights and norms of biases. For overparametrized deep ReLU networks with a training sample size bounded by the input space dimension, we explicitly construct zero loss minimizers without use of gradient descent, and prove a uniform generalization bound that is independent of the network architecture. We perform computational experiments of our theoretical results with MNIST, and obtain agreement with the true test error within a 22 % margin on average.

### Model A Paper 3: [2507.21429]
**Title:** From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions
**Category:** stat.ML
**Score:** 0.8294

Gradient descent (GD) on deep neural network loss landscapes is non-convex, yet often converges far faster in practice than classical guarantees suggest. Prior work shows that within locally quasi-convex regions (LQCRs), GD converges to stationary points at sublinear rates, leaving the commonly observed near-exponential training dynamics unexplained. We show that, under a mild local Neural Tangent Kernel (NTK) stability assumption, the loss satisfies a PL-type error bound within these regions, yielding a Locally Polyak-Lojasiewicz Region (LPLR) in which the squared gradient norm controls the suboptimality gap. For properly initialized finite-width networks, we show that under local NTK stability this PL-type mechanism holds around initialization and establish linear convergence of GD as long as the iterates remain within the resulting LPLR. Empirically, we observe PL-like scaling and linear-rate loss decay in controlled full-batch training and in a ResNet-style CNN trained with mini-batch SGD on a CIFAR-10 subset, indicating that LPLR signatures can persist under modern architectures and stochastic optimization. Overall, the results connect local geometric structure, local NTK stability, and fast optimization rates in a finite-width setting.

### Model A Paper 4: [2204.12392]
**Title:** A PAC-Bayes oracle inequality for sparse neural networks
**Category:** math.ST
**Score:** 0.8124

We study the Gibbs posterior distribution for sparse deep neural nets in a nonparametric regression setting. The posterior can be accessed via Metropolis-adjusted Langevin algorithms. Using a mixture over uniform priors on sparse sets of network weights, we prove an oracle inequality which shows that the method adapts to the unknown regularity and hierarchical structure of the regression function. The estimator achieves the minimax-optimal rate of convergence (up to a logarithmic factor).

### Model A Paper 5: [2601.01295]
**Title:** Sobolev Approximation of Deep ReLU Networks in Log-Barron Space
**Category:** cs.LG
**Score:** 0.8007

Universal approximation theorems show that neural networks can approximate any continuous function; however, the number of parameters may grow exponentially with the ambient dimension, so these results do not fully explain the practical success of deep models on high-dimensional data. Barron space theory addresses this: if a target function belongs to a Barron space, a two-layer network with $n$ parameters achieves an $O(n^{-1/2})$ approximation error in $L^2$. Yet classical Barron spaces $\mathscr{B}^{s+1}$ still require stronger regularity than Sobolev spaces $H^s$, and existing depth-sensitive results often assume constraints such as $sL \le 1/2$. In this paper, we introduce a log-weighted Barron space $\mathscr{B}^{\log}$, which requires a strictly weaker assumption than $\mathscr{B}^s$ for any $s>0$. For this new function space, we first study embedding properties and carry out a statistical analysis via the Rademacher complexity. Then we prove that functions in $\mathscr{B}^{\log}$ can be approximated by deep ReLU networks with explicit depth dependence. We then define a family $\mathscr{B}^{s,\log}$, establish approximation bounds in the $H^1$ norm, and identify maximal depth scales under which these rates are preserved. Our results clarify how depth reduces regularity requirements for efficient representation, offering a more precise explanation for the performance of deep architectures beyond the classical Barron setting, and for their stable use in high-dimensional problems used today.

### Model A Paper 6: [2601.14026]
**Title:** Universal Approximation Theorem for Input-Connected Multilayer Perceptrons
**Category:** cs.LG
**Score:** 0.7830

We introduce the Input-Connected Multilayer Perceptron (IC-MLP), a feedforward neural network architecture in which each hidden neuron receives, in addition to the outputs of the preceding layer, a direct affine connection from the raw input. We first study this architecture in the univariate setting and give an explicit and systematic description of IC-MLPs with an arbitrary finite number of hidden layers, including iterated formulas for the network functions. In this setting, we prove a universal approximation theorem showing that deep IC-MLPs can approximate any continuous function on a closed interval of the real line if and only if the activation function is nonlinear. We then extend the analysis to vector-valued inputs and establish a corresponding universal approximation theorem for continuous functions on compact subsets of $\mathbb{R}^n$.

### Model A Paper 7: [2601.17987]
**Title:** Systematic Characterization of Minimal Deep Learning Architectures: A Unified Analysis of Convergence, Pruning, and Quantization
**Category:** cs.LG
**Score:** 0.7777

Deep learning networks excel at classification, yet identifying minimal architectures that reliably solve a task remains challenging. We present a computational methodology for systematically exploring and analyzing the relationships among convergence, pruning, and quantization. The workflow first performs a structured design sweep across a large set of architectures, then evaluates convergence behavior, pruning sensitivity, and quantization robustness on representative models. Focusing on well-known image classification of increasing complexity, and across Deep Neural Networks, Convolutional Neural Networks, and Vision Transformers, our initial results show that, despite architectural diversity, performance is largely invariant and learning dynamics consistently exhibit three regimes: unstable, learning, and overfitting. We further characterize the minimal learnable parameters required for stable learning, uncover distinct convergence and pruning phases, and quantify the effect of reduced numeric precision on trainable parameters. Aligning with intuition, the results confirm that deeper architectures are more resilient to pruning than shallower ones, with parameter redundancy as high as 60%, and quantization impacts models with fewer learnable parameters more severely and has a larger effect on harder image datasets. These findings provide actionable guidance for selecting compact, stable models under pruning and low-precision constraints in image classification.

### Model A Paper 8: [2410.14951]
**Title:** Architectural Scaling Surpass Basis Complexity? Efficient KANs with Single-Parameter Design
**Category:** cs.AI
**Score:** 0.7751

The landscape of Kolmogorov-Arnold Networks (KANs) is rapidly expanding, yet lacks a unified theoretical framework and a clear principle for efficient architecture design. This paper addresses these gaps with three core contributions. First, we introduce the Universal KAN (Uni-KAN) framework, a novel abstraction that formally unifies all KAN-style networks through dense and sparse representations. We prove their interchangeability and provide an open-source library for this framework, facilitating future research. Second, we propose the Efficient KAN Expansion (EKE) Hypothesis, a design philosophy positing that allocating parameters to architectural scaling rather than basis function complexity yields superior performance. Third, we present Single-Parameter KANs (SKANs), a family of ultra-lightweight networks that embody the EKE Hypothesis. Our comprehensive experiments provide the first strong empirical validation for the theoretical necessity of basis function smoothness for stable training. Furthermore, SKANs demonstrate state-of-the-art performance, improving F1 scores by up to 6.51\% and reducing test loss by 93.1\%, while achieving up to 6x faster training speeds compared to existing KAN variants. These results establish a robust framework, a guiding hypothesis, and a practical methodology for designing the next generation of efficient and powerful neural networks. The code is accessible at https://anonymous.4open.science/r/SKAN-EBBB/.

### Model A Paper 9: [2601.05732]
**Title:** mHC-lite: You Don't Need 20 Sinkhorn-Knopp Iterations
**Category:** cs.LG
**Score:** 0.7653

Hyper-Connections (HC) generalizes residual connections by introducing dynamic residual matrices that mix information across multiple residual streams, accelerating convergence in deep neural networks. However, unconstrained residual matrices can compromise training stability. To address this, DeepSeek's Manifold-Constrained Hyper-Connections (mHC) approximately projects these matrices onto the Birkhoff polytope via iterative Sinkhorn--Knopp (SK) normalization. We identify two limitations of this approach: (i) finite SK iterations do not guarantee exact doubly stochasticity, leaving an approximation gap that can accumulate through network depth and undermine stability; (ii) efficient SK implementation requires highly specialized CUDA kernels, raising engineering barriers and reducing portability. Motivated by the Birkhoff--von Neumann theorem, we propose mHC-lite, a simple reparameterization that explicitly constructs doubly stochastic matrices as convex combinations of permutation matrices. This approach guarantees exact doubly stochasticity by construction and can be implemented using only native matrix operations. Extensive experiments demonstrate that mHC-lite matches or exceeds mHC in performance while achieving higher training throughput with a naive implementation and eliminating the residual instabilities observed in both HC and mHC. The code is publicly available at https://github.com/FFTYYY/mhc-lite.

### Model A Paper 10: [2405.07098]
**Title:** Interpretable global minima of deep ReLU neural networks on sequentially separable data
**Category:** cs.LG
**Score:** 0.7632

We explicitly construct zero loss neural network classifiers. We write the weight matrices and bias vectors in terms of cumulative parameters, which determine truncation maps acting recursively on input space. The configurations for the training data considered are (i) sufficiently small, well separated clusters corresponding to each class, and (ii) equivalence classes which are sequentially linearly separable. In the best case, for $Q$ classes of data in $\mathbb{R}^M$, global minimizers can be described with $Q(M+2)$ parameters.

### Model A Paper 11: [2601.01465]
**Title:** Leveraging Flatness to Improve Information-Theoretic Generalization Bounds for SGD
**Category:** cs.LG
**Score:** 0.7611

Information-theoretic (IT) generalization bounds have been used to study the generalization of learning algorithms. These bounds are intrinsically data- and algorithm-dependent so that one can exploit the properties of data and algorithm to derive tighter bounds. However, we observe that although the flatness bias is crucial for SGD's generalization, these bounds fail to capture the improved generalization under better flatness and are also numerically loose. This is caused by the inadequate leverage of SGD's flatness bias in existing IT bounds. This paper derives a more flatness-leveraging IT bound for the flatness-favoring SGD. The bound indicates the learned models generalize better if the large-variance directions of the final weight covariance have small local curvatures in the loss landscape. Experiments on deep neural networks show our bound not only correctly reflects the better generalization when flatness is improved, but is also numerically much tighter. This is achieved by a flexible technique called "omniscient trajectory". When applied to Gradient Descent's minimax excess risk on convex-Lipschitz-Bounded problems, it improves representative IT bounds' $\Omega(1)$ rates to $O(1/\sqrt{n})$. It also implies a by-pass of memorization-generalization trade-offs.

### Model A Paper 12: [2312.08410]
**Title:** Universal approximation property of Banach space-valued random feature models including random neural networks
**Category:** cs.LG
**Score:** 0.7594

We introduce a Banach space-valued extension of random feature learning, a data-driven supervised machine learning technique for large-scale kernel approximation. By randomly initializing the feature maps, only the linear readout needs to be trained, which reduces the computational complexity substantially. Viewing random feature models as Banach space-valued random variables, we prove a universal approximation result in the corresponding Bochner space. Moreover, we derive approximation rates and an explicit algorithm to learn an element of the given Banach space by such models. The framework of this paper includes random trigonometric/Fourier regression and in particular random neural networks which are single-hidden-layer feedforward neural networks whose weights and biases are randomly initialized, whence only the linear readout needs to be trained. For the latter, we can then lift the universal approximation property of deterministic neural networks to random neural networks, even within function spaces over non-compact domains, e.g., weighted spaces, $L^p$-spaces, and (weighted) Sobolev spaces, where the latter includes the approximation of the (weak) derivatives. In addition, we analyze when the training costs for approximating a given function grow polynomially in both the input/output dimension and the reciprocal of a pre-specified tolerated approximation error. Furthermore, we demonstrate in a numerical example the empirical advantages of random feature models over their deterministic counterparts.

### Model A Paper 13: [2512.24381]
**Title:** Tubular Riemannian Laplace Approximations for Bayesian Neural Networks
**Category:** cs.LG
**Score:** 0.7554

Laplace approximations are among the simplest and most practical methods for approximate Bayesian inference in neural networks, yet their Euclidean formulation struggles with the highly anisotropic, curved loss surfaces and large symmetry groups that characterize modern deep models. Recent work has proposed Riemannian and geometric Gaussian approximations to adapt to this structure. Building on these ideas, we introduce the Tubular Riemannian Laplace (TRL) approximation. TRL explicitly models the posterior as a probabilistic tube that follows a low-loss valley induced by functional symmetries, using a Fisher/Gauss-Newton metric to separate prior-dominated tangential uncertainty from data-dominated transverse uncertainty. We interpret TRL as a scalable reparametrised Gaussian approximation that utilizes implicit curvature estimates to operate in high-dimensional parameter spaces. Our empirical evaluation on ResNet-18 (CIFAR-10 and CIFAR-100) demonstrates that TRL achieves excellent calibration, matching or exceeding the reliability of Deep Ensembles (in terms of ECE) while requiring only a fraction (1/5) of the training cost. TRL effectively bridges the gap between single-model efficiency and ensemble-grade reliability.

### Model A Paper 14: [2601.01853]
**Title:** Asymptotic Convergence and Stability of Adaptive Gradient Methods in Smooth Non-convex Optimization
**Category:** math.OC
**Score:** 0.7551

Adaptive gradient methods, such as AdaGrad, have become fundamental tools in deep learning. Despite their widespread use, the asymptotic convergence of AdaGrad remains poorly understood in non-convex scenarios. In this work, we present the first rigorous asymptotic convergence analysis of AdaGrad-Norm for smooth non-convex optimization. Using a novel stopping-time partitioning technique, we establish a key stability result: the objective function values remain bounded in expectation, and the iterates are bounded almost surely under a mild coercivity assumption. Building on these stability results, we prove that AdaGrad-Norm achieves both almost sure and mean-square convergence. Furthermore, we extend our analysis to RMSProp and show that, with appropriate hyperparameter choices, it also enjoys stability and asymptotic convergence. The techniques developed herein may be of independent interest for analyzing other adaptive stochastic optimization algorithms.

### Model A Paper 15: [2407.17092]
**Title:** Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications
**Category:** math.NA
**Score:** 0.7517

In this paper, we introduce semi-autonomous neural ordinary differential equations (SA-NODEs), a variation of the vanilla NODEs, employing fewer parameters. We investigate the universal approximation properties of SA-NODEs for dynamical systems from both a theoretical and a numerical perspective. Within the assumption of a finite-time horizon, under general hypotheses we establish an asymptotic approximation result, demonstrating that the error vanishes as the number of parameters goes to infinity. Under additional regularity assumptions, we further specify this convergence rate in relation to the number of parameters, utilizing quantitative approximation results in the Barron space. Based on the previous result, we prove an approximation rate for transport equations by their neural counterparts. Our numerical experiments validate the effectiveness of SA-NODEs in capturing the dynamics of various ODE systems and transport equations. Additionally, we compare SA-NODEs with vanilla NODEs, highlighting the superior performance and reduced complexity of our approach.

### Model A Paper 16: [2506.16065]
**Title:** Floating-Point Neural Networks Are Provably Robust Universal Approximators
**Category:** cs.LG
**Score:** 0.7507

The classical universal approximation (UA) theorem for neural networks establishes mild conditions under which a feedforward neural network can approximate a continuous function $f$ with arbitrary accuracy. A recent result shows that neural networks also enjoy a more general interval universal approximation (IUA) theorem, in the sense that the abstract interpretation semantics of the network using the interval domain can approximate the direct image map of $f$ (i.e., the result of applying $f$ to a set of inputs) with arbitrary accuracy. These theorems, however, rest on the unrealistic assumption that the neural network computes over infinitely precise real numbers, whereas their software implementations in practice compute over finite-precision floating-point numbers. An open question is whether the IUA theorem still holds in the floating-point setting.
  This paper introduces the first IUA theorem for floating-point neural networks that proves their remarkable ability to perfectly capture the direct image map of any rounded target function $f$, showing no limits exist on their expressiveness. Our IUA theorem in the floating-point setting exhibits material differences from the real-valued setting, which reflects the fundamental distinctions between these two computational models. This theorem also implies surprising corollaries, which include (i) the existence of provably robust floating-point neural networks; and (ii) the computational completeness of the class of straight-line programs that use only floating-point additions and multiplications for the class of all floating-point programs that halt.

### Model A Paper 17: [2510.21245]
**Title:** Convergence of Stochastic Gradient Langevin Dynamics in the Lazy Training Regime
**Category:** cs.LG
**Score:** 0.7502

Continuous-time models provide important insights into the training dynamics of optimization algorithms in deep learning. In this work, we establish a non-asymptotic convergence analysis of stochastic gradient Langevin dynamics (SGLD), which is an It\^o stochastic differential equation (SDE) approximation of stochastic gradient descent in continuous time, in the lazy training regime. We show that, under regularity conditions on the Hessian of the loss function, SGLD with multiplicative and state-dependent noise (i) yields a non-degenerate kernel throughout the training process with high probability, and (ii) achieves exponential convergence to the empirical risk minimizer in expectation, and we establish finite-time and finite-width bounds on the optimality gap. We corroborate our theoretical findings with numerical examples in the regression setting.

### Model A Paper 18: [2502.20580]
**Title:** Training Large Neural Networks With Low-Dimensional Error Feedback
**Category:** cs.LG
**Score:** 0.7425

Training deep neural networks typically relies on backpropagating high dimensional error signals a computationally intensive process with little evidence supporting its implementation in the brain. However, since most tasks involve low-dimensional outputs, we propose that low-dimensional error signals may suffice for effective learning. To test this hypothesis, we introduce a novel local learning rule based on Feedback Alignment that leverages indirect, low-dimensional error feedback to train large networks. Our method decouples the backward pass from the forward pass, enabling precise control over error signal dimensionality while maintaining high-dimensional representations. We begin with a detailed theoretical derivation for linear networks, which forms the foundation of our learning framework, and extend our approach to nonlinear, convolutional, and transformer architectures. Remarkably, we demonstrate that even minimal error dimensionality on the order of the task dimensionality can achieve performance matching that of traditional backpropagation. Furthermore, our rule enables efficient training of convolutional networks, which have previously been resistant to Feedback Alignment methods, with minimal error. This breakthrough not only paves the way toward more biologically accurate models of learning but also challenges the conventional reliance on high-dimensional gradient signals in neural network training. Our findings suggest that low-dimensional error signals can be as effective as high-dimensional ones, prompting a reevaluation of gradient-based learning in high-dimensional systems. Ultimately, our work offers a fresh perspective on neural network optimization and contributes to understanding learning mechanisms in both artificial and biological systems.

### Model A Paper 19: [2403.05809]
**Title:** Two-hidden-layer ReLU neural networks and finite elements
**Category:** math.NA
**Score:** 0.7371

We point out that (continuous or discontinuous) piecewise linear functions on a convex polytope mesh can be represented by two-hidden-layer ReLU neural networks in a weak sense. In addition, the numbers of neurons of the two hidden layers required to weakly represent are accurately given based on the numbers of polytopes and hyperplanes involved in this mesh. The results naturally hold for constant and linear finite element functions. Such weak representation establishes a bridge between two-hidden-layer ReLU neural networks and finite element functions, and leads to a perspective for analyzing approximation capability of ReLU neural networks in $L^p$ norm via finite element functions. Moreover, we discuss the strict representation for tensor finite element functions via the recent tensor neural networks.

### Model A Paper 20: [2408.08055]
**Title:** DeNOTS: Stable Deep Neural ODEs for Time Series
**Category:** cs.LG
**Score:** 0.7357

Neural CDEs provide a natural way to process the temporal evolution of irregular time series. The number of function evaluations (NFE) is these systems' natural analog of depth (the number of layers in traditional neural networks). It is usually regulated via solver error tolerance: lower tolerance means higher numerical precision, requiring more integration steps. However, lowering tolerances does not adequately increase the models' expressiveness. We propose a simple yet effective alternative: scaling the integration time horizon to increase NFEs and "deepen`` the model. Increasing the integration interval causes uncontrollable growth in conventional vector fields, so we also propose a way to stabilize the dynamics via Negative Feedback (NF). It ensures provable stability without constraining flexibility. It also implies robustness: we provide theoretical bounds for Neural ODE risk using Gaussian process theory. Experiments on four open datasets demonstrate that our method, DeNOTS, outperforms existing approaches~ -- ~including recent Neural RDEs and state space models,~ -- ~achieving up to $20\%$ improvement in metrics. DeNOTS combines expressiveness, stability, and robustness, enabling reliable modelling in continuous-time domains.

---


### Model B Paper 1: [2601.08100]
**Title:** Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds
**Category:** stat.ML
**Score:** 0.8067

Understanding the generalization behavior of deep neural networks remains a fundamental challenge in modern statistical learning theory. Among existing approaches, PAC-Bayesian norm-based bounds have demonstrated particular promise due to their data-dependent nature and their ability to capture algorithmic and geometric properties of learned models. However, most existing results rely on isotropic Gaussian posteriors, heavy use of spectral-norm concentration for weight perturbations, and largely architecture-agnostic analyses, which together limit both the tightness and practical relevance of the resulting bounds. To address these limitations, in this work, we propose a unified framework for PAC-Bayesian norm-based generalization by reformulating the derivation of generalization bounds as a stochastic optimization problem over anisotropic Gaussian posteriors. The key to our approach is a sensitivity matrix that quantifies the network outputs with respect to structured weight perturbations, enabling the explicit incorporation of heterogeneous parameter sensitivities and architectural structures. By imposing different structural assumptions on this sensitivity matrix, we derive a family of generalization bounds that recover several existing PAC-Bayesian results as special cases, while yielding bounds that are comparable to or tighter than state-of-the-art approaches. Such a unified framework provides a principled and flexible way for geometry-/structure-aware and interpretable generalization analysis in deep learning.

### Model B Paper 2: [2504.05695]
**Title:** Architecture independent generalization bounds for overparametrized deep ReLU networks
**Category:** cs.LG
**Score:** 0.7970

We prove that overparametrized neural networks are able to generalize with a test error that is independent of the level of overparametrization, and independent of the Vapnik-Chervonenkis (VC) dimension. We prove explicit bounds that only depend on the metric geometry of the test and training sets, on the regularity properties of the activation function, and on the operator norms of the weights and norms of biases. For overparametrized deep ReLU networks with a training sample size bounded by the input space dimension, we explicitly construct zero loss minimizers without use of gradient descent, and prove a uniform generalization bound that is independent of the network architecture. We perform computational experiments of our theoretical results with MNIST, and obtain agreement with the true test error within a 22 % margin on average.

### Model B Paper 3: [2507.21429]
**Title:** From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions
**Category:** stat.ML
**Score:** 0.7677

Gradient descent (GD) on deep neural network loss landscapes is non-convex, yet often converges far faster in practice than classical guarantees suggest. Prior work shows that within locally quasi-convex regions (LQCRs), GD converges to stationary points at sublinear rates, leaving the commonly observed near-exponential training dynamics unexplained. We show that, under a mild local Neural Tangent Kernel (NTK) stability assumption, the loss satisfies a PL-type error bound within these regions, yielding a Locally Polyak-Lojasiewicz Region (LPLR) in which the squared gradient norm controls the suboptimality gap. For properly initialized finite-width networks, we show that under local NTK stability this PL-type mechanism holds around initialization and establish linear convergence of GD as long as the iterates remain within the resulting LPLR. Empirically, we observe PL-like scaling and linear-rate loss decay in controlled full-batch training and in a ResNet-style CNN trained with mini-batch SGD on a CIFAR-10 subset, indicating that LPLR signatures can persist under modern architectures and stochastic optimization. Overall, the results connect local geometric structure, local NTK stability, and fast optimization rates in a finite-width setting.

### Model B Paper 4: [2204.12392]
**Title:** A PAC-Bayes oracle inequality for sparse neural networks
**Category:** math.ST
**Score:** 0.7570

We study the Gibbs posterior distribution for sparse deep neural nets in a nonparametric regression setting. The posterior can be accessed via Metropolis-adjusted Langevin algorithms. Using a mixture over uniform priors on sparse sets of network weights, we prove an oracle inequality which shows that the method adapts to the unknown regularity and hierarchical structure of the regression function. The estimator achieves the minimax-optimal rate of convergence (up to a logarithmic factor).

### Model B Paper 5: [2601.01465]
**Title:** Leveraging Flatness to Improve Information-Theoretic Generalization Bounds for SGD
**Category:** cs.LG
**Score:** 0.7310

Information-theoretic (IT) generalization bounds have been used to study the generalization of learning algorithms. These bounds are intrinsically data- and algorithm-dependent so that one can exploit the properties of data and algorithm to derive tighter bounds. However, we observe that although the flatness bias is crucial for SGD's generalization, these bounds fail to capture the improved generalization under better flatness and are also numerically loose. This is caused by the inadequate leverage of SGD's flatness bias in existing IT bounds. This paper derives a more flatness-leveraging IT bound for the flatness-favoring SGD. The bound indicates the learned models generalize better if the large-variance directions of the final weight covariance have small local curvatures in the loss landscape. Experiments on deep neural networks show our bound not only correctly reflects the better generalization when flatness is improved, but is also numerically much tighter. This is achieved by a flexible technique called "omniscient trajectory". When applied to Gradient Descent's minimax excess risk on convex-Lipschitz-Bounded problems, it improves representative IT bounds' $\Omega(1)$ rates to $O(1/\sqrt{n})$. It also implies a by-pass of memorization-generalization trade-offs.

### Model B Paper 6: [2601.01295]
**Title:** Sobolev Approximation of Deep ReLU Networks in Log-Barron Space
**Category:** cs.LG
**Score:** 0.6804

Universal approximation theorems show that neural networks can approximate any continuous function; however, the number of parameters may grow exponentially with the ambient dimension, so these results do not fully explain the practical success of deep models on high-dimensional data. Barron space theory addresses this: if a target function belongs to a Barron space, a two-layer network with $n$ parameters achieves an $O(n^{-1/2})$ approximation error in $L^2$. Yet classical Barron spaces $\mathscr{B}^{s+1}$ still require stronger regularity than Sobolev spaces $H^s$, and existing depth-sensitive results often assume constraints such as $sL \le 1/2$. In this paper, we introduce a log-weighted Barron space $\mathscr{B}^{\log}$, which requires a strictly weaker assumption than $\mathscr{B}^s$ for any $s>0$. For this new function space, we first study embedding properties and carry out a statistical analysis via the Rademacher complexity. Then we prove that functions in $\mathscr{B}^{\log}$ can be approximated by deep ReLU networks with explicit depth dependence. We then define a family $\mathscr{B}^{s,\log}$, establish approximation bounds in the $H^1$ norm, and identify maximal depth scales under which these rates are preserved. Our results clarify how depth reduces regularity requirements for efficient representation, offering a more precise explanation for the performance of deep architectures beyond the classical Barron setting, and for their stable use in high-dimensional problems used today.

### Model B Paper 7: [2407.18384]
**Title:** Mathematical theory of deep learning
**Category:** cs.LG
**Score:** 0.6790

This book provides an introduction to the mathematical analysis of deep learning. It covers fundamental results in approximation theory, optimization theory, and statistical learning theory, which are the three main pillars of deep neural network theory. Serving as a guide for students and researchers in mathematics and related fields, the book aims to equip readers with foundational knowledge on the topic. It prioritizes simplicity over generality, and presents rigorous yet accessible results to help build an understanding of the essential mathematical concepts underpinning deep learning.

### Model B Paper 8: [2510.21245]
**Title:** Convergence of Stochastic Gradient Langevin Dynamics in the Lazy Training Regime
**Category:** cs.LG
**Score:** 0.6763

Continuous-time models provide important insights into the training dynamics of optimization algorithms in deep learning. In this work, we establish a non-asymptotic convergence analysis of stochastic gradient Langevin dynamics (SGLD), which is an It\^o stochastic differential equation (SDE) approximation of stochastic gradient descent in continuous time, in the lazy training regime. We show that, under regularity conditions on the Hessian of the loss function, SGLD with multiplicative and state-dependent noise (i) yields a non-degenerate kernel throughout the training process with high probability, and (ii) achieves exponential convergence to the empirical risk minimizer in expectation, and we establish finite-time and finite-width bounds on the optimality gap. We corroborate our theoretical findings with numerical examples in the regression setting.

### Model B Paper 9: [2601.12604]
**Title:** Beyond Softmax and Entropy: Improving Convergence Guarantees of Policy Gradients by f-SoftArgmax Parameterization with Coupled Regularization
**Category:** cs.LG
**Score:** 0.6657

Policy gradient methods are known to be highly sensitive to the choice of policy parameterization. In particular, the widely used softmax parameterization can induce ill-conditioned optimization landscapes and lead to exponentially slow convergence. Although this can be mitigated by preconditioning, this solution is often computationally expensive. Instead, we propose replacing the softmax with an alternative family of policy parameterizations based on the generalized f-softargmax. We further advocate coupling this parameterization with a regularizer induced by the same f-divergence, which improves the optimization landscape and ensures that the resulting regularized objective satisfies a Polyak-Lojasiewicz inequality. Leveraging this structure, we establish the first explicit non-asymptotic last-iterate convergence guarantees for stochastic policy gradient methods for finite MDPs without any form of preconditioning. We also derive sample-complexity bounds for the unregularized problem and show that f-PG, with Tsallis divergences achieves polynomial sample complexity in contrast to the exponential complexity incurred by the standard softmax parameterization.

### Model B Paper 10: [2601.08547]
**Title:** Convergence of gradient flow for learning convolutional neural networks
**Category:** math.OC
**Score:** 0.6472

Convolutional neural networks are widely used in imaging and image recognition. Learning such networks from training data leads to the minimization of a non-convex function. This makes the analysis of standard optimization methods such as variants of (stochastic) gradient descent challenging. In this article we study the simplified setting of linear convolutional networks. We show that the gradient flow (to be interpreted as an abstraction of gradient descent) applied to the empirical risk defined via certain loss functions including the square loss always converges to a critical point, under a mild condition on the training data.

### Model B Paper 11: [2601.14026]
**Title:** Universal Approximation Theorem for Input-Connected Multilayer Perceptrons
**Category:** cs.LG
**Score:** 0.6391

We introduce the Input-Connected Multilayer Perceptron (IC-MLP), a feedforward neural network architecture in which each hidden neuron receives, in addition to the outputs of the preceding layer, a direct affine connection from the raw input. We first study this architecture in the univariate setting and give an explicit and systematic description of IC-MLPs with an arbitrary finite number of hidden layers, including iterated formulas for the network functions. In this setting, we prove a universal approximation theorem showing that deep IC-MLPs can approximate any continuous function on a closed interval of the real line if and only if the activation function is nonlinear. We then extend the analysis to vector-valued inputs and establish a corresponding universal approximation theorem for continuous functions on compact subsets of $\mathbb{R}^n$.

### Model B Paper 12: [2601.21750]
**Title:** FISMO: Fisher-Structured Momentum-Orthogonalized Optimizer
**Category:** cs.LG
**Score:** 0.6347

Training large-scale neural networks requires solving nonconvex optimization where the choice of optimizer fundamentally determines both convergence behavior and computational efficiency. While adaptive methods like Adam have long dominated practice, the recently proposed Muon optimizer achieves superior performance through orthogonalized momentum updates that enforce isotropic geometry with uniform singular values. However, this strict isotropy discards potentially valuable curvature information encoded in gradient spectra, motivating optimization methods that balance geometric structure with adaptivity. We introduce FISMO (Fisher-Structured Momentum-Orthogonalized) optimizer, which generalizes isotropic updates to incorporate anisotropic curvature information through Fisher information geometry. By reformulating the optimizer update as a trust-region problem constrained by a Kronecker-factored Fisher metric, FISMO achieves structured preconditioning that adapts to local loss landscape geometry while maintaining computational tractability. We establish convergence guarantees for FISMO in stochastic nonconvex settings, proving an $\mathcal{O}(1/\sqrt{T})$ rate for the expected squared gradient norm with explicit characterization of variance reduction through mini-batching. Empirical evaluation on image classification and language modeling benchmarks demonstrates that FISMO achieves superior training efficiency and final performance compared to established baselines.

### Model B Paper 13: [2601.01853]
**Title:** Asymptotic Convergence and Stability of Adaptive Gradient Methods in Smooth Non-convex Optimization
**Category:** math.OC
**Score:** 0.6309

Adaptive gradient methods, such as AdaGrad, have become fundamental tools in deep learning. Despite their widespread use, the asymptotic convergence of AdaGrad remains poorly understood in non-convex scenarios. In this work, we present the first rigorous asymptotic convergence analysis of AdaGrad-Norm for smooth non-convex optimization. Using a novel stopping-time partitioning technique, we establish a key stability result: the objective function values remain bounded in expectation, and the iterates are bounded almost surely under a mild coercivity assumption. Building on these stability results, we prove that AdaGrad-Norm achieves both almost sure and mean-square convergence. Furthermore, we extend our analysis to RMSProp and show that, with appropriate hyperparameter choices, it also enjoys stability and asymptotic convergence. The techniques developed herein may be of independent interest for analyzing other adaptive stochastic optimization algorithms.

### Model B Paper 14: [2210.05607]
**Title:** Divergence Results and Convergence of a Variance Reduced Version of ADAM
**Category:** cs.LG
**Score:** 0.6308

Stochastic optimization algorithms using exponential moving averages of the past gradients, such as ADAM, RMSProp and AdaGrad, have been having great successes in many applications, especially in training deep neural networks. ADAM in particular stands out as efficient and robust. Despite of its outstanding performance, ADAM has been proved to be divergent for some specific problems. We revisit the divergent question and provide divergent examples under stronger conditions such as in expectation or high probability. Under a variance reduction assumption, we show that an ADAM-type algorithm converges, which means that it is the variance of gradients that causes the divergence of original ADAM. To this end, we propose a variance reduced version of ADAM and provide a convergent analysis of the algorithm. Numerical experiments show that the proposed algorithm has as good performance as ADAM. Our work suggests a new direction for fixing the convergence issues.

### Model B Paper 15: [2601.05732]
**Title:** mHC-lite: You Don't Need 20 Sinkhorn-Knopp Iterations
**Category:** cs.LG
**Score:** 0.6296

Hyper-Connections (HC) generalizes residual connections by introducing dynamic residual matrices that mix information across multiple residual streams, accelerating convergence in deep neural networks. However, unconstrained residual matrices can compromise training stability. To address this, DeepSeek's Manifold-Constrained Hyper-Connections (mHC) approximately projects these matrices onto the Birkhoff polytope via iterative Sinkhorn--Knopp (SK) normalization. We identify two limitations of this approach: (i) finite SK iterations do not guarantee exact doubly stochasticity, leaving an approximation gap that can accumulate through network depth and undermine stability; (ii) efficient SK implementation requires highly specialized CUDA kernels, raising engineering barriers and reducing portability. Motivated by the Birkhoff--von Neumann theorem, we propose mHC-lite, a simple reparameterization that explicitly constructs doubly stochastic matrices as convex combinations of permutation matrices. This approach guarantees exact doubly stochasticity by construction and can be implemented using only native matrix operations. Extensive experiments demonstrate that mHC-lite matches or exceeds mHC in performance while achieving higher training throughput with a naive implementation and eliminating the residual instabilities observed in both HC and mHC. The code is publicly available at https://github.com/FFTYYY/mhc-lite.

### Model B Paper 16: [2502.20580]
**Title:** Training Large Neural Networks With Low-Dimensional Error Feedback
**Category:** cs.LG
**Score:** 0.6272

Training deep neural networks typically relies on backpropagating high dimensional error signals a computationally intensive process with little evidence supporting its implementation in the brain. However, since most tasks involve low-dimensional outputs, we propose that low-dimensional error signals may suffice for effective learning. To test this hypothesis, we introduce a novel local learning rule based on Feedback Alignment that leverages indirect, low-dimensional error feedback to train large networks. Our method decouples the backward pass from the forward pass, enabling precise control over error signal dimensionality while maintaining high-dimensional representations. We begin with a detailed theoretical derivation for linear networks, which forms the foundation of our learning framework, and extend our approach to nonlinear, convolutional, and transformer architectures. Remarkably, we demonstrate that even minimal error dimensionality on the order of the task dimensionality can achieve performance matching that of traditional backpropagation. Furthermore, our rule enables efficient training of convolutional networks, which have previously been resistant to Feedback Alignment methods, with minimal error. This breakthrough not only paves the way toward more biologically accurate models of learning but also challenges the conventional reliance on high-dimensional gradient signals in neural network training. Our findings suggest that low-dimensional error signals can be as effective as high-dimensional ones, prompting a reevaluation of gradient-based learning in high-dimensional systems. Ultimately, our work offers a fresh perspective on neural network optimization and contributes to understanding learning mechanisms in both artificial and biological systems.

### Model B Paper 17: [2512.24381]
**Title:** Tubular Riemannian Laplace Approximations for Bayesian Neural Networks
**Category:** cs.LG
**Score:** 0.6249

Laplace approximations are among the simplest and most practical methods for approximate Bayesian inference in neural networks, yet their Euclidean formulation struggles with the highly anisotropic, curved loss surfaces and large symmetry groups that characterize modern deep models. Recent work has proposed Riemannian and geometric Gaussian approximations to adapt to this structure. Building on these ideas, we introduce the Tubular Riemannian Laplace (TRL) approximation. TRL explicitly models the posterior as a probabilistic tube that follows a low-loss valley induced by functional symmetries, using a Fisher/Gauss-Newton metric to separate prior-dominated tangential uncertainty from data-dominated transverse uncertainty. We interpret TRL as a scalable reparametrised Gaussian approximation that utilizes implicit curvature estimates to operate in high-dimensional parameter spaces. Our empirical evaluation on ResNet-18 (CIFAR-10 and CIFAR-100) demonstrates that TRL achieves excellent calibration, matching or exceeding the reliability of Deep Ensembles (in terms of ECE) while requiring only a fraction (1/5) of the training cost. TRL effectively bridges the gap between single-model efficiency and ensemble-grade reliability.

### Model B Paper 18: [2509.18766]
**Title:** Diagonal Linear Networks and the Lasso Regularization Path
**Category:** cs.LG
**Score:** 0.6247

Diagonal linear networks are neural networks with linear activation and diagonal weight matrices. Their theoretical interest is that their implicit regularization can be rigorously analyzed: from a small initialization, the training of diagonal linear networks converges to the linear predictor with minimal 1-norm among minimizers of the training loss. In this paper, we deepen this analysis showing that the full training trajectory of diagonal linear networks is closely related to the lasso regularization path. In this connection, the training time plays the role of an inverse regularization parameter. Both rigorous results and simulations are provided to illustrate this conclusion. Under a monotonicity assumption on the lasso regularization path, the connection is exact while in the general case, we show an approximate connection.

### Model B Paper 19: [2405.03251]
**Title:** Exploring the Frontiers of Softmax: Provable Optimization, Applications in Diffusion Model, and Beyond
**Category:** cs.LG
**Score:** 0.6244

The softmax activation function plays a crucial role in the success of large language models (LLMs), particularly in the self-attention mechanism of the widely adopted Transformer architecture. However, the underlying learning dynamics that contribute to the effectiveness of softmax remain largely unexplored. As a step towards better understanding, this paper provides a theoretical study of the optimization and generalization properties of two-layer softmax neural networks, providing theoretical insights into their superior performance as other activation functions, such as ReLU and exponential. Leveraging the Neural Tangent Kernel (NTK) framework, our analysis reveals that the normalization effect of the softmax function leads to a good perturbation property of the induced NTK matrix, resulting in a good convex region of the loss landscape. Consequently, softmax neural networks can learn the target function in the over-parametrization regime. To demonstrate the broad applicability of our theoretical findings, we apply them to the task of learning score estimation functions in diffusion models, a promising approach for generative modeling. Our analysis shows that gradient-based algorithms can learn the score function with a provable accuracy. Our work provides a deeper understanding of the effectiveness of softmax neural networks and their potential in various domains, paving the way for further advancements in natural language processing and beyond.

### Model B Paper 20: [2312.08410]
**Title:** Universal approximation property of Banach space-valued random feature models including random neural networks
**Category:** cs.LG
**Score:** 0.6212

We introduce a Banach space-valued extension of random feature learning, a data-driven supervised machine learning technique for large-scale kernel approximation. By randomly initializing the feature maps, only the linear readout needs to be trained, which reduces the computational complexity substantially. Viewing random feature models as Banach space-valued random variables, we prove a universal approximation result in the corresponding Bochner space. Moreover, we derive approximation rates and an explicit algorithm to learn an element of the given Banach space by such models. The framework of this paper includes random trigonometric/Fourier regression and in particular random neural networks which are single-hidden-layer feedforward neural networks whose weights and biases are randomly initialized, whence only the linear readout needs to be trained. For the latter, we can then lift the universal approximation property of deterministic neural networks to random neural networks, even within function spaces over non-compact domains, e.g., weighted spaces, $L^p$-spaces, and (weighted) Sobolev spaces, where the latter includes the approximation of the (weak) derivatives. In addition, we analyze when the training costs for approximating a given function grow polynomially in both the input/output dimension and the reciprocal of a pre-specified tolerated approximation error. Furthermore, we demonstrate in a numerical example the empirical advantages of random feature models over their deterministic counterparts.

---

## Review Instructions

You are reviewing recommendations from two models for the interest profile "Mathematical foundations of neural networks".
You do NOT know which model is which. Assess each set independently.

For EACH model's recommendation set:

1. **Per-paper relevance** (if full depth): For each paper, is it relevant to the seeds?
   - Relevant via similar topic/method
   - Relevant via adjacent community
   - Productive provocation (challenges assumptions, opens new directions)
   - Noise (no meaningful connection)

2. **Set-level assessment**:
   - Does this set map a research landscape or just list similar papers?
   - What aspects of the interest does it cover? What's missing?
   - Set coherence vs diversity balance

3. **Comparative assessment**:
   - Which set would better serve a researcher with this interest? Why?
   - What does each set find that the other misses?
   - Character of each set's errors (noise vs adjacent vs vocabulary match)

4. **Emergent observations**:
   - Anything surprising or noteworthy about the recommendations?
   - What kind of researcher would prefer each set?

5. **Absent researcher note**:
   - What would you need to know about the researcher's actual situation to assess properly?
   - What are you assuming about their needs?

6. **Metric divergence flags**:
   - Does your qualitative impression contradict any quantitative expectations?
