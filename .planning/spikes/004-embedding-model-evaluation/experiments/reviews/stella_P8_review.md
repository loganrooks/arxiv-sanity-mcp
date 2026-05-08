# Single-Strategy Characterization Review

**Model:** stella
**Profile:** Mathematical foundations of neural networks (P8)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to stella

## Seed Papers
  - [2504.05695] Architecture independent generalization bounds for overparametrized deep ReLU networks (cs.LG)
  - [2601.08100] Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds (stat.ML)
  - [2507.21429] From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions (stat.ML)
  - [2204.12392] A PAC-Bayes oracle inequality for sparse neural networks (math.ST)
  - [2407.17092] Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications (math.NA)

## stella Top-20 Recommendations

### Paper 1: [2504.05695]
**Title:** Architecture independent generalization bounds for overparametrized deep ReLU networks
**Category:** cs.LG
**Score:** 0.9145
**In MiniLM top-20:** True

We prove that overparametrized neural networks are able to generalize with a test error that is independent of the level of overparametrization, and independent of the Vapnik-Chervonenkis (VC) dimension. We prove explicit bounds that only depend on the metric geometry of the test and training sets, on the regularity properties of the activation function, and on the operator norms of the weights and norms of biases. For overparametrized deep ReLU networks with a training sample size bounded by the input space dimension, we explicitly construct zero loss minimizers without use of gradient descent, and prove a uniform generalization bound that is independent of the network architecture. We perform computational experiments of our theoretical results with MNIST, and obtain agreement with the true test error within a 22 % margin on average.

### Paper 2: [2601.08100]
**Title:** Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds
**Category:** stat.ML
**Score:** 0.9112
**In MiniLM top-20:** True

Understanding the generalization behavior of deep neural networks remains a fundamental challenge in modern statistical learning theory. Among existing approaches, PAC-Bayesian norm-based bounds have demonstrated particular promise due to their data-dependent nature and their ability to capture algorithmic and geometric properties of learned models. However, most existing results rely on isotropic Gaussian posteriors, heavy use of spectral-norm concentration for weight perturbations, and largely architecture-agnostic analyses, which together limit both the tightness and practical relevance of the resulting bounds. To address these limitations, in this work, we propose a unified framework for PAC-Bayesian norm-based generalization by reformulating the derivation of generalization bounds as a stochastic optimization problem over anisotropic Gaussian posteriors. The key to our approach is a sensitivity matrix that quantifies the network outputs with respect to structured weight perturbations, enabling the explicit incorporation of heterogeneous parameter sensitivities and architectural structures. By imposing different structural assumptions on this sensitivity matrix, we derive a family of generalization bounds that recover several existing PAC-Bayesian results as special cases, while yielding bounds that are comparable to or tighter than state-of-the-art approaches. Such a unified framework provides a principled and flexible way for geometry-/structure-aware and interpretable generalization analysis in deep learning.

### Paper 3: [2204.12392]
**Title:** A PAC-Bayes oracle inequality for sparse neural networks
**Category:** math.ST
**Score:** 0.8968
**In MiniLM top-20:** True

We study the Gibbs posterior distribution for sparse deep neural nets in a nonparametric regression setting. The posterior can be accessed via Metropolis-adjusted Langevin algorithms. Using a mixture over uniform priors on sparse sets of network weights, we prove an oracle inequality which shows that the method adapts to the unknown regularity and hierarchical structure of the regression function. The estimator achieves the minimax-optimal rate of convergence (up to a logarithmic factor).

### Paper 4: [2507.21429]
**Title:** From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions
**Category:** stat.ML
**Score:** 0.8932
**In MiniLM top-20:** True

Gradient descent (GD) on deep neural network loss landscapes is non-convex, yet often converges far faster in practice than classical guarantees suggest. Prior work shows that within locally quasi-convex regions (LQCRs), GD converges to stationary points at sublinear rates, leaving the commonly observed near-exponential training dynamics unexplained. We show that, under a mild local Neural Tangent Kernel (NTK) stability assumption, the loss satisfies a PL-type error bound within these regions, yielding a Locally Polyak-Lojasiewicz Region (LPLR) in which the squared gradient norm controls the suboptimality gap. For properly initialized finite-width networks, we show that under local NTK stability this PL-type mechanism holds around initialization and establish linear convergence of GD as long as the iterates remain within the resulting LPLR. Empirically, we observe PL-like scaling and linear-rate loss decay in controlled full-batch training and in a ResNet-style CNN trained with mini-batch SGD on a CIFAR-10 subset, indicating that LPLR signatures can persist under modern architectures and stochastic optimization. Overall, the results connect local geometric structure, local NTK stability, and fast optimization rates in a finite-width setting.

### Paper 5: [2601.01295]
**Title:** Sobolev Approximation of Deep ReLU Networks in Log-Barron Space
**Category:** cs.LG
**Score:** 0.8727
**In MiniLM top-20:** True

Universal approximation theorems show that neural networks can approximate any continuous function; however, the number of parameters may grow exponentially with the ambient dimension, so these results do not fully explain the practical success of deep models on high-dimensional data. Barron space theory addresses this: if a target function belongs to a Barron space, a two-layer network with $n$ parameters achieves an $O(n^{-1/2})$ approximation error in $L^2$. Yet classical Barron spaces $\mathscr{B}^{s+1}$ still require stronger regularity than Sobolev spaces $H^s$, and existing depth-sensitive results often assume constraints such as $sL \le 1/2$. In this paper, we introduce a log-weighted Barron space $\mathscr{B}^{\log}$, which requires a strictly weaker assumption than $\mathscr{B}^s$ for any $s>0$. For this new function space, we first study embedding properties and carry out a statistical analysis via the Rademacher complexity. Then we prove that functions in $\mathscr{B}^{\log}$ can be approximated by deep ReLU networks with explicit depth dependence. We then define a family $\mathscr{B}^{s,\log}$, establish approximation bounds in the $H^1$ norm, and identify maximal depth scales under which these rates are preserved. Our results clarify how depth reduces regularity requirements for efficient representation, offering a more precise explanation for the performance of deep architectures beyond the classical Barron setting, and for their stable use in high-dimensional problems used today.

### Paper 6: [2312.08410]
**Title:** Universal approximation property of Banach space-valued random feature models including random neural networks
**Category:** cs.LG
**Score:** 0.8532
**In MiniLM top-20:** True

We introduce a Banach space-valued extension of random feature learning, a data-driven supervised machine learning technique for large-scale kernel approximation. By randomly initializing the feature maps, only the linear readout needs to be trained, which reduces the computational complexity substantially. Viewing random feature models as Banach space-valued random variables, we prove a universal approximation result in the corresponding Bochner space. Moreover, we derive approximation rates and an explicit algorithm to learn an element of the given Banach space by such models. The framework of this paper includes random trigonometric/Fourier regression and in particular random neural networks which are single-hidden-layer feedforward neural networks whose weights and biases are randomly initialized, whence only the linear readout needs to be trained. For the latter, we can then lift the universal approximation property of deterministic neural networks to random neural networks, even within function spaces over non-compact domains, e.g., weighted spaces, $L^p$-spaces, and (weighted) Sobolev spaces, where the latter includes the approximation of the (weak) derivatives. In addition, we analyze when the training costs for approximating a given function grow polynomially in both the input/output dimension and the reciprocal of a pre-specified tolerated approximation error. Furthermore, we demonstrate in a numerical example the empirical advantages of random feature models over their deterministic counterparts.

### Paper 7: [2510.21245]
**Title:** Convergence of Stochastic Gradient Langevin Dynamics in the Lazy Training Regime
**Category:** cs.LG
**Score:** 0.8501
**In MiniLM top-20:** True

Continuous-time models provide important insights into the training dynamics of optimization algorithms in deep learning. In this work, we establish a non-asymptotic convergence analysis of stochastic gradient Langevin dynamics (SGLD), which is an It\^o stochastic differential equation (SDE) approximation of stochastic gradient descent in continuous time, in the lazy training regime. We show that, under regularity conditions on the Hessian of the loss function, SGLD with multiplicative and state-dependent noise (i) yields a non-degenerate kernel throughout the training process with high probability, and (ii) achieves exponential convergence to the empirical risk minimizer in expectation, and we establish finite-time and finite-width bounds on the optimality gap. We corroborate our theoretical findings with numerical examples in the regression setting.

### Paper 8: [2601.14026]
**Title:** Universal Approximation Theorem for Input-Connected Multilayer Perceptrons
**Category:** cs.LG
**Score:** 0.8493
**In MiniLM top-20:** True

We introduce the Input-Connected Multilayer Perceptron (IC-MLP), a feedforward neural network architecture in which each hidden neuron receives, in addition to the outputs of the preceding layer, a direct affine connection from the raw input. We first study this architecture in the univariate setting and give an explicit and systematic description of IC-MLPs with an arbitrary finite number of hidden layers, including iterated formulas for the network functions. In this setting, we prove a universal approximation theorem showing that deep IC-MLPs can approximate any continuous function on a closed interval of the real line if and only if the activation function is nonlinear. We then extend the analysis to vector-valued inputs and establish a corresponding universal approximation theorem for continuous functions on compact subsets of $\mathbb{R}^n$.

### Paper 9: [2601.08547]
**Title:** Convergence of gradient flow for learning convolutional neural networks
**Category:** math.OC
**Score:** 0.8456
**In MiniLM top-20:** True

Convolutional neural networks are widely used in imaging and image recognition. Learning such networks from training data leads to the minimization of a non-convex function. This makes the analysis of standard optimization methods such as variants of (stochastic) gradient descent challenging. In this article we study the simplified setting of linear convolutional networks. We show that the gradient flow (to be interpreted as an abstraction of gradient descent) applied to the empirical risk defined via certain loss functions including the square loss always converges to a critical point, under a mild condition on the training data.

### Paper 10 [DIVERGENT]: [2405.07098]
**Title:** Interpretable global minima of deep ReLU neural networks on sequentially separable data
**Category:** cs.LG
**Score:** 0.8388
**In MiniLM top-20:** False

We explicitly construct zero loss neural network classifiers. We write the weight matrices and bias vectors in terms of cumulative parameters, which determine truncation maps acting recursively on input space. The configurations for the training data considered are (i) sufficiently small, well separated clusters corresponding to each class, and (ii) equivalence classes which are sequentially linearly separable. In the best case, for $Q$ classes of data in $\mathbb{R}^M$, global minimizers can be described with $Q(M+2)$ parameters.

### Paper 11: [2601.01465]
**Title:** Leveraging Flatness to Improve Information-Theoretic Generalization Bounds for SGD
**Category:** cs.LG
**Score:** 0.8313
**In MiniLM top-20:** True

Information-theoretic (IT) generalization bounds have been used to study the generalization of learning algorithms. These bounds are intrinsically data- and algorithm-dependent so that one can exploit the properties of data and algorithm to derive tighter bounds. However, we observe that although the flatness bias is crucial for SGD's generalization, these bounds fail to capture the improved generalization under better flatness and are also numerically loose. This is caused by the inadequate leverage of SGD's flatness bias in existing IT bounds. This paper derives a more flatness-leveraging IT bound for the flatness-favoring SGD. The bound indicates the learned models generalize better if the large-variance directions of the final weight covariance have small local curvatures in the loss landscape. Experiments on deep neural networks show our bound not only correctly reflects the better generalization when flatness is improved, but is also numerically much tighter. This is achieved by a flexible technique called "omniscient trajectory". When applied to Gradient Descent's minimax excess risk on convex-Lipschitz-Bounded problems, it improves representative IT bounds' $\Omega(1)$ rates to $O(1/\sqrt{n})$. It also implies a by-pass of memorization-generalization trade-offs.

### Paper 12: [2512.24381]
**Title:** Tubular Riemannian Laplace Approximations for Bayesian Neural Networks
**Category:** cs.LG
**Score:** 0.8310
**In MiniLM top-20:** True

Laplace approximations are among the simplest and most practical methods for approximate Bayesian inference in neural networks, yet their Euclidean formulation struggles with the highly anisotropic, curved loss surfaces and large symmetry groups that characterize modern deep models. Recent work has proposed Riemannian and geometric Gaussian approximations to adapt to this structure. Building on these ideas, we introduce the Tubular Riemannian Laplace (TRL) approximation. TRL explicitly models the posterior as a probabilistic tube that follows a low-loss valley induced by functional symmetries, using a Fisher/Gauss-Newton metric to separate prior-dominated tangential uncertainty from data-dominated transverse uncertainty. We interpret TRL as a scalable reparametrised Gaussian approximation that utilizes implicit curvature estimates to operate in high-dimensional parameter spaces. Our empirical evaluation on ResNet-18 (CIFAR-10 and CIFAR-100) demonstrates that TRL achieves excellent calibration, matching or exceeding the reliability of Deep Ensembles (in terms of ECE) while requiring only a fraction (1/5) of the training cost. TRL effectively bridges the gap between single-model efficiency and ensemble-grade reliability.

### Paper 13: [2601.01853]
**Title:** Asymptotic Convergence and Stability of Adaptive Gradient Methods in Smooth Non-convex Optimization
**Category:** math.OC
**Score:** 0.8238
**In MiniLM top-20:** True

Adaptive gradient methods, such as AdaGrad, have become fundamental tools in deep learning. Despite their widespread use, the asymptotic convergence of AdaGrad remains poorly understood in non-convex scenarios. In this work, we present the first rigorous asymptotic convergence analysis of AdaGrad-Norm for smooth non-convex optimization. Using a novel stopping-time partitioning technique, we establish a key stability result: the objective function values remain bounded in expectation, and the iterates are bounded almost surely under a mild coercivity assumption. Building on these stability results, we prove that AdaGrad-Norm achieves both almost sure and mean-square convergence. Furthermore, we extend our analysis to RMSProp and show that, with appropriate hyperparameter choices, it also enjoys stability and asymptotic convergence. The techniques developed herein may be of independent interest for analyzing other adaptive stochastic optimization algorithms.

### Paper 14 [DIVERGENT]: [2308.14555]
**Title:** Kernel Limit for a Class of Recurrent Neural Networks Trained on Ergodic Data Sequences
**Category:** cs.LG
**Score:** 0.8160
**In MiniLM top-20:** False

Mathematical methods are developed to characterize the asymptotics of recurrent neural networks (RNN) as the number of hidden units, data samples in the sequence, hidden state updates, and training steps simultaneously grow to infinity. In the case of an RNN with a simplified weight matrix, we prove the convergence of the RNN to the solution of an infinite-dimensional ODE coupled with the fixed point of a random algebraic equation. The analysis requires addressing several challenges which are unique to RNNs. In typical mean-field applications (e.g., feedforward neural networks), discrete updates are of magnitude $\mathcal{O}(1/N)$ and the number of updates is $\mathcal{O}(N)$. Therefore, the system can be represented as an Euler approximation of an appropriate ODE/PDE, which it will converge to as $N \rightarrow \infty$. However, the RNN hidden layer updates are $\mathcal{O}(1)$. Therefore, RNNs cannot be represented as a discretization of an ODE/PDE and standard mean-field techniques cannot be applied. Instead, we develop a fixed point analysis for the evolution of the RNN memory states, with convergence estimates in terms of the number of update steps and the number of hidden units. The RNN hidden layer is studied as a function in a Sobolev space, whose evolution is governed by the data sequence (a Markov chain), the parameter updates, and its dependence on the RNN hidden layer at the previous time step. Due to the strong correlation between updates, a Poisson equation must be used to bound the fluctuations of the RNN around its limit equation. These mathematical methods give rise to the neural tangent kernel (NTK) limits for RNNs trained on data sequences as the number of data samples and size of the neural network grow to infinity.

### Paper 15 [DIVERGENT]: [2407.17092]
**Title:** Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications
**Category:** math.NA
**Score:** 0.8147
**In MiniLM top-20:** False

In this paper, we introduce semi-autonomous neural ordinary differential equations (SA-NODEs), a variation of the vanilla NODEs, employing fewer parameters. We investigate the universal approximation properties of SA-NODEs for dynamical systems from both a theoretical and a numerical perspective. Within the assumption of a finite-time horizon, under general hypotheses we establish an asymptotic approximation result, demonstrating that the error vanishes as the number of parameters goes to infinity. Under additional regularity assumptions, we further specify this convergence rate in relation to the number of parameters, utilizing quantitative approximation results in the Barron space. Based on the previous result, we prove an approximation rate for transport equations by their neural counterparts. Our numerical experiments validate the effectiveness of SA-NODEs in capturing the dynamics of various ODE systems and transport equations. Additionally, we compare SA-NODEs with vanilla NODEs, highlighting the superior performance and reduced complexity of our approach.

### Paper 16: [2509.18766]
**Title:** Diagonal Linear Networks and the Lasso Regularization Path
**Category:** cs.LG
**Score:** 0.8129
**In MiniLM top-20:** True

Diagonal linear networks are neural networks with linear activation and diagonal weight matrices. Their theoretical interest is that their implicit regularization can be rigorously analyzed: from a small initialization, the training of diagonal linear networks converges to the linear predictor with minimal 1-norm among minimizers of the training loss. In this paper, we deepen this analysis showing that the full training trajectory of diagonal linear networks is closely related to the lasso regularization path. In this connection, the training time plays the role of an inverse regularization parameter. Both rigorous results and simulations are provided to illustrate this conclusion. Under a monotonicity assumption on the lasso regularization path, the connection is exact while in the general case, we show an approximate connection.

### Paper 17 [DIVERGENT]: [2103.03191]
**Title:** Generalization Bounds for Sparse Random Feature Expansions
**Category:** stat.ML
**Score:** 0.8129
**In MiniLM top-20:** False

Random feature methods have been successful in various machine learning tasks, are easy to compute, and come with theoretical accuracy bounds. They serve as an alternative approach to standard neural networks since they can represent similar function spaces without a costly training phase. However, for accuracy, random feature methods require more measurements than trainable parameters, limiting their use for data-scarce applications or problems in scientific machine learning. This paper introduces the sparse random feature expansion to obtain parsimonious random feature models. Specifically, we leverage ideas from compressive sensing to generate random feature expansions with theoretical guarantees even in the data-scarce setting. In particular, we provide generalization bounds for functions in a certain class (that is dense in a reproducing kernel Hilbert space) depending on the number of samples and the distribution of features. The generalization bounds improve with additional structural conditions, such as coordinate sparsity, compact clusters of the spectrum, or rapid spectral decay. In particular, by introducing sparse features, i.e. features with random sparse weights, we provide improved bounds for low order functions. We show that the sparse random feature expansions outperforms shallow networks in several scientific machine learning tasks.

### Paper 18: [2210.05607]
**Title:** Divergence Results and Convergence of a Variance Reduced Version of ADAM
**Category:** cs.LG
**Score:** 0.8123
**In MiniLM top-20:** True

Stochastic optimization algorithms using exponential moving averages of the past gradients, such as ADAM, RMSProp and AdaGrad, have been having great successes in many applications, especially in training deep neural networks. ADAM in particular stands out as efficient and robust. Despite of its outstanding performance, ADAM has been proved to be divergent for some specific problems. We revisit the divergent question and provide divergent examples under stronger conditions such as in expectation or high probability. Under a variance reduction assumption, we show that an ADAM-type algorithm converges, which means that it is the variance of gradients that causes the divergence of original ADAM. To this end, we propose a variance reduced version of ADAM and provide a convergent analysis of the algorithm. Numerical experiments show that the proposed algorithm has as good performance as ADAM. Our work suggests a new direction for fixing the convergence issues.

### Paper 19 [DIVERGENT]: [2502.10578]
**Title:** Implicit vs. explicit regularization for high-dimensional gradient descent
**Category:** math.ST
**Score:** 0.8116
**In MiniLM top-20:** False

In this paper we investigate the generalization error of gradient descent (GD) applied to an $\ell_2$-regularized OLS objective function in the linear model. Based on our analysis we develop new methodology for computationally tractable and statistically efficient linear prediction in a high-dimensional and massive data scenario (large-$n$, large-$p$). Our results are based on the surprising observation that the generalization error of optimally tuned regularized gradient descent approaches that of an optimal benchmark procedure $monotonically$ in the iteration number $t$. On the other hand standard GD for OLS (without explicit regularization) can achieve the benchmark only in degenerate cases. This shows that (optimal) explicit regularization can be nearly statistically efficient (for large $t$) whereas implicit regularization by (optimal) early stopping can not.
  To complete our methodology, we provide a fully data driven and computationally tractable choice of the $\ell_2$ regularization parameter $\lambda$ that is computationally cheaper than cross-validation. On this way, we follow and extend ideas of Dicker (2014) to the non-gaussian case, which requires new results on high-dimensional sample covariance matrices that might be of independent interest.

### Paper 20 [DIVERGENT]: [2601.20047]
**Title:** Minimax Rates for Hyperbolic Hierarchical Learning
**Category:** stat.ML
**Score:** 0.8077
**In MiniLM top-20:** False

We prove an exponential separation in sample complexity between Euclidean and hyperbolic representations for learning on hierarchical data under standard Lipschitz regularization. For depth-$R$ hierarchies with branching factor $m$, we first establish a geometric obstruction for Euclidean space: any bounded-radius embedding forces volumetric collapse, mapping exponentially many tree-distant points to nearby locations. This necessitates Lipschitz constants scaling as $\exp(\Omega(R))$ to realize even simple hierarchical targets, yielding exponential sample complexity under capacity control. We then show this obstruction vanishes in hyperbolic space: constant-distortion hyperbolic embeddings admit $O(1)$-Lipschitz realizability, enabling learning with $n = O(mR \log m)$ samples. A matching $\Omega(mR \log m)$ lower bound via Fano's inequality establishes that hyperbolic representations achieve the information-theoretic optimum. We also show a geometry-independent bottleneck: any rank-$k$ prediction space captures only $O(k)$ canonical hierarchical contrasts.

---

## Review Instructions

You are reviewing the top-20 recommendations from stella for the profile "Mathematical foundations of neural networks".
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
