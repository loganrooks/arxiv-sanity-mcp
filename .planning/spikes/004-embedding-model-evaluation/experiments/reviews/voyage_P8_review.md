# Single-Strategy Characterization Review

**Model:** voyage
**Profile:** Mathematical foundations of neural networks (P8)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to voyage

## Seed Papers
  - [2504.05695] Architecture independent generalization bounds for overparametrized deep ReLU networks (cs.LG)
  - [2601.08100] Towards A Unified PAC-Bayesian Framework for Norm-based Generalization Bounds (stat.ML)
  - [2507.21429] From Sublinear to Linear: Fast Convergence in Deep Networks via Locally Polyak-Lojasiewicz Regions (stat.ML)
  - [2204.12392] A PAC-Bayes oracle inequality for sparse neural networks (math.ST)
  - [2407.17092] Universal Approximation of Dynamical Systems by Semi-Autonomous Neural ODEs and Applications (math.NA)

## voyage Top-20 Recommendations

(Papers 1-20 as listed in template above)

---

## Assessment

**Limitation note:** Voyage-4 had 160/2000 papers fail to embed (8% failure rate due to API rate limiting). The effective retrieval pool is approximately 1840 papers. Mathematical foundations papers may be underrepresented in a general ML corpus, and the embedding failure could affect niche mathematical papers disproportionately. However, the 14/20 overlap suggests the impact is moderate.

### 1. Per-Paper Assessment

**Paper 1 [2601.08100] PAC-Bayesian Framework** -- Direct (seed paper). Unified PAC-Bayesian framework for generalization bounds.

**Paper 2 [2504.05695] Architecture-Independent Bounds** -- Direct (seed paper). Overparameterized ReLU network generalization bounds.

**Paper 3 [2507.21429] LPLR Convergence** -- Direct (seed paper). Fast convergence via locally Polyak-Lojasiewicz regions.

**Paper 4 [2204.12392] PAC-Bayes Sparse** -- Direct (seed paper). PAC-Bayes oracle inequality for sparse networks.

**Paper 5 [2601.01295] Sobolev Approximation** -- Direct. Log-Barron space approximation theory for deep ReLU networks. Extends Barron space theory to deeper architectures with Sobolev norm guarantees. Directly connected to seed [2504.05695]'s approximation theory concerns.

**Paper 6 [2601.01465] IT Generalization Bounds** -- Direct. Information-theoretic generalization bounds that leverage flatness bias of SGD. Connects to PAC-Bayesian seeds but from the information-theoretic angle. The "omniscient trajectory" technique is novel.

**Paper 7 [2509.18766] Diagonal Linear Networks** -- Direct. Theoretical analysis connecting diagonal linear network training trajectories to the lasso regularization path. Pure mathematical analysis of implicit regularization.

**Paper 8 [2512.24381] TRL Approximation** -- Adjacent. Tubular Riemannian Laplace approximation for Bayesian neural networks. More about Bayesian inference methodology than mathematical foundations per se, but the Riemannian geometry and Fisher metric analysis are theoretically grounded.

**Paper 9 [2407.18384] Math Theory of DL Book** -- Direct. Textbook covering approximation, optimization, and statistical learning theory for deep learning. A comprehensive reference that spans all three pillars of the seed papers' concerns.

**Paper 10 [2407.17092] SA-NODEs** -- Direct (seed paper). Universal approximation of dynamical systems by semi-autonomous neural ODEs.

**Paper 11 [2502.20580] Low-Dimensional Error Feedback** -- Adjacent. Training via low-dimensional error signals as alternative to backpropagation. More about biological plausibility and training methodology than mathematical foundations, though the theoretical derivation for linear networks connects.

**Paper 12 [2312.08410] Banach-Valued Random Features** -- Direct. Universal approximation for Banach space-valued random feature models including random neural networks. Strong theoretical contribution extending approximation theory to Banach spaces and weighted Sobolev spaces.

**Paper 13 [2601.08547] Gradient Flow for CNNs** -- Direct. Convergence analysis of gradient flow for learning linear convolutional networks. Directly addresses the optimization theory pillar of neural network foundations.

**Paper 14 [2410.14951] SKANs** -- DIVERGENT. Adjacent. Efficient Kolmogorov-Arnold Networks with single-parameter design. The paper introduces a unified framework for KANs and proposes the EKE Hypothesis (architectural scaling over basis complexity). The mathematical analysis of basis function smoothness for stable training is relevant to the foundations, but the primary contribution is architectural rather than theoretical. Partially connected.

**Paper 15 [2410.17764] Multi-Tangent Forward Gradients** -- DIVERGENT. Adjacent. Analysis of forward gradients with multiple tangents for approximate backpropagation. The theoretical analysis of approximation quality improvement is rigorous, but the paper is more about optimization methodology than mathematical foundations of neural networks specifically. The orthogonal projection approach is mathematically interesting.

**Paper 16 [2510.21245] SGLD Convergence** -- Direct. Non-asymptotic convergence of stochastic gradient Langevin dynamics in the lazy training regime. NTK analysis with finite-width bounds. Directly addresses the optimization theory of neural networks.

**Paper 17 [2601.03162] PGD Convergence** -- DIVERGENT. Direct. Preconditioned gradient descent for mitigating spectral bias and grokking. Studies the NTK-to-feature-rich regime transition. Directly addresses foundational questions about neural network learning dynamics. The connection between preconditioned optimization, spectral bias, and grokking is a genuine theoretical contribution.

**Paper 18 [2405.03251] Softmax Optimization** -- Direct. Provable optimization and generalization for two-layer softmax networks via NTK framework. Extends theoretical analysis to the softmax activation, which is central to modern architectures.

**Paper 19 [2405.07098] Interpretable Global Minima** -- DIVERGENT. Direct. Explicit construction of zero-loss ReLU classifiers via cumulative parameters. Directly connected to seed [2504.05695]'s concern with constructing zero-loss minimizers for overparameterized networks. The constructive approach (writing explicit weight matrices) is distinctive.

**Paper 20 [2311.16086] MAST** -- DIVERGENT. Adjacent. Model-agnostic sparsified training via sparsification-aware optimization formulation. The theoretical contribution (novel objective formulation connecting dropout and sparse training to convergence rates) is relevant, but the primary thrust is practical training methodology. The convergence rate improvements and relaxed assumptions connect to optimization theory foundations.

### 2. Set-Level Assessment

**Landscape coverage:** This set provides strong coverage of the mathematical foundations of neural networks across three pillars:

**Approximation theory:** Barron space extensions (Sobolev/log-Barron), Banach space random features, universal approximation for NODEs, constructive zero-loss minimizers, CNN convergence, architecture-independent generalization bounds

**Optimization theory:** Gradient flow convergence, SGLD convergence in lazy regime, PGD for spectral bias/grokking, Polyak-Lojasiewicz regions, diagonal linear network regularization paths, softmax NTK analysis

**Statistical learning theory:** PAC-Bayesian framework, PAC-Bayes oracle inequalities, information-theoretic generalization bounds, Rademacher complexity analysis

**What this set does well:** Comprehensive coverage of the three-pillar structure of neural network theory. Both classical results (approximation bounds, PAC-Bayes) and modern topics (NTK regime, lazy training, grokking) are represented. The textbook entry (Paper 9) is a useful anchor.

**What is conspicuously absent:**
- Mean field theory and infinite-width limits (beyond NTK)
- Neural tangent kernel theory per se (it appears as a tool but no NTK-focused papers)
- Implicit bias and regularization theory (only diagonal linear networks)
- Loss landscape geometry (saddle points, mode connectivity)
- Double descent and benign overfitting
- Theoretical computer science perspectives (circuit complexity of neural networks)

**Divergent paper character:** The 6 divergent papers split into:
- 3 directly relevant theoretical papers: PGD convergence/grokking, interpretable global minima construction, multi-tangent forward gradients
- 2 methodological papers with theoretical components: SKANs (KAN architecture), MAST (sparsified training)
- 1 primarily about training alternative: multi-tangent forward gradients

The theoretical papers (PGD convergence, interpretable minima) are high quality. The architectural/methodological papers are relevant but less central to "mathematical foundations."

### 3. Emergent Observations

**Signal character:** With 6/20 unique papers (30% divergence), Voyage shows meaningful differentiation. The strongest divergent signals are PGD convergence for grokking (Paper 17) and interpretable global minima (Paper 19), both of which address genuine foundational questions. The weaker signals are the more applied papers (SKANs, MAST) that have theoretical components but are primarily about architecture design or training methodology.

**Divergence quality:** Mixed but leaning positive. 3/6 divergent papers are directly valuable for the mathematical foundations profile. 2/6 are adjacent with relevant theoretical components. 1/6 (multi-tangent forward gradients) is more tangential.

**Productive provocations:** Paper 17 (PGD convergence) is the strongest provocation -- it provides evidence that grokking represents a transition from the NTK to the feature-rich regime, connecting optimization dynamics to learning phase transitions. Paper 19 (interpretable global minima) provokes by showing that for certain data configurations, global minimizers of deep ReLU networks can be written down explicitly with only Q(M+2) parameters, suggesting that the apparent complexity of neural network loss landscapes may be less daunting than commonly assumed.

### 4. Absent Researcher Note

To properly assess this recommendation set, I would need to know:
- Whether the researcher is primarily working in approximation theory, optimization theory, or statistical learning theory (the set covers all three but the emphasis may matter)
- Their mathematical background (some papers require measure theory and functional analysis)
- Whether they care about connections to practice (NTK regime, grokking) or pure theory
- Whether they work on specific architecture families (ReLU networks, convolutional, transformers)
- Their interest in emerging theoretical topics (KANs, neural ODEs, Bayesian neural networks)

### 5. Metric Divergence Flags

The 14/20 overlap (J@20 = ~0.58) indicates moderate divergence. The qualitative review is consistent: the 14 shared papers form a strong core of mathematical foundations work, and the 6 divergent papers are of mixed but generally positive quality. The 3 directly relevant divergent papers (PGD convergence, interpretable minima, MAST to a lesser degree) suggest that Voyage finds some theoretically interesting papers that MiniLM misses. The 2-3 more peripheral papers (SKANs, forward gradients) slightly dilute the mathematical foundations focus.

No significant qualitative-quantitative contradiction. The profile is intrinsically harder to serve well because "mathematical foundations" spans multiple mathematical subdisciplines, and different embedding models may weight different mathematical vocabulary differently. The moderate divergence is expected for this kind of broad theoretical profile.
