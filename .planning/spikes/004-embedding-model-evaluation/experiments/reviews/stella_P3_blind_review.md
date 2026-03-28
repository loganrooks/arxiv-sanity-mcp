# Blind Pairwise Qualitative Review

**Profile:** Quantum computing / quantum ML (P3)
**Depth:** full
**Models:** Model B vs Model A (identities withheld)

## Seed Papers
  - [2601.18710] Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia (cs.ET)
  - [2506.22555] Spectral Bias in Variational Quantum Machine Learning (quant-ph)
  - [2601.11937] Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection (quant-ph)
  - [2209.07714] Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations (quant-ph)
  - [2507.16036] Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks (quant-ph)

## Recommendations

### Model B Paper 1: [2601.11937]
**Title:** Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection
**Category:** quant-ph
**Score:** 0.8967

High-Energy Physics (HEP) experiments, such as those at the Large Hadron Collider (LHC), generate massive datasets that challenge classical computational limits. Quantum Machine Learning (QML) offers a potential advantage in processing high-dimensional data; however, finding the optimal architecture for current Noisy Intermediate-Scale Quantum (NISQ) devices remains an open challenge. This study investigates the performance of Variational Quantum Classifiers (VQC) in detecting Higgs Boson signals using the ATLAS Higgs Boson Machine Learning Challenge 2014 experiment dataset. We implemented a dimensionality reduction pipeline using Principal Component Analysis (PCA) to map 30 physical features into 4-qubit and 8-qubit latent spaces. We benchmarked three configurations: (A) a shallow 4-qubit circuit, (B) a deep 4-qubit circuit with increased entanglement layers, and (C) an expanded 8-qubit circuit. Experimental results demonstrate that increasing circuit depth significantly improves performance, yielding the highest accuracy of 56.2% (Configuration B), compared to a baseline of 51.9%. Conversely, simply scaling to 8 qubits resulted in a performance degradation to 50.6% due to optimization challenges associated with Barren Plateaus in the larger Hilbert space. These findings suggest that for near-term quantum hardware, prioritizing circuit depth and entanglement capability is more critical than increasing qubit count for effective anomaly detection in HEP data.

### Model B Paper 2: [2506.22555]
**Title:** Spectral Bias in Variational Quantum Machine Learning
**Category:** quant-ph
**Score:** 0.8834

In this work, we investigate the phenomenon of spectral bias in quantum machine learning, where, in classical settings, models tend to fit low-frequency components of a target function earlier during training than high-frequency ones, demonstrating a frequency-dependent rate of convergence. We study this effect specifically in parameterised quantum circuits (PQCs). Leveraging the established formulation of PQCs as Fourier series, we prove that spectral bias in this setting arises from the ``redundancy'' of the Fourier coefficients, which denotes the number of terms in the analytical form of the model contributing to the same frequency component. The choice of data encoding scheme dictates the degree of redundancy for a Fourier coefficient. We find that the magnitude of the Fourier coefficients' gradients during training strongly correlates with the coefficients' redundancy. We then further demonstrate this empirically with three different encoding schemes. Additionally, we demonstrate that PQCs with greater redundancy exhibit increased robustness to random perturbations in their parameters at the corresponding frequencies. We investigate how design choices affect the ability of PQCs to learn Fourier sums, focusing on parameter initialization scale and entanglement structure, finding large initializations and low-entanglement schemes tend to slow convergence.

### Model B Paper 3: [2601.18710]
**Title:** Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia
**Category:** cs.ET
**Score:** 0.8654

This paper presents a feasibility study demonstrating that quantum machine learning (QML) algorithms achieve competitive performance on real-world medical imaging despite operating under severe constraints. We evaluate Equilibrium Propagation (EP), an energy-based learning method that does not use backpropagation (incompatible with quantum systems due to state-collapsing measurements) and Variational Quantum Circuits (VQCs) for automated detection of Acute Myeloid Leukemia (AML) from blood cell microscopy images using binary classification (2 classes: AML vs. Healthy).
  Key Result: Using limited subsets (50-250 samples per class) of the AML-Cytomorphology dataset (18,365 expert-annotated images), quantum methods achieve performance only 12-15% below classical CNNs despite reduced image resolution (64x64 pixels), engineered features (20D), and classical simulation via Qiskit. EP reaches 86.4% accuracy (only 12% below CNN) without backpropagation, while the 4-qubit VQC attains 83.0% accuracy with consistent data efficiency: VQC maintains stable 83% performance with only 50 samples per class, whereas CNN requires 250 samples (5x more data) to reach 98%. These results establish reproducible baselines for QML in healthcare, validating NISQ-era feasibility.

### Model B Paper 4: [2502.04271]
**Title:** Variational decision diagrams for quantum-inspired machine learning applications
**Category:** quant-ph
**Score:** 0.8535

Decision diagrams (DDs) have emerged as an efficient tool for simulating quantum circuits due to their capacity to exploit data redundancies in quantum states and quantum operations, enabling the efficient computation of probability amplitudes. However, their application in quantum machine learning (QML) has remained unexplored. This paper introduces variational decision diagrams (VDDs), a novel graph structure that combines the structural benefits of DDs with the adaptability of variational methods for efficiently representing quantum states. We investigate the trainability of VDDs by applying them to the ground state estimation problem for transverse-field Ising and Heisenberg Hamiltonians. Analysis of gradient variance suggests that training VDDs is possible, as no signs of vanishing gradients--also known as barren plateaus--are observed. This work provides new insights into the use of decision diagrams in QML as an alternative to design and train variational ans\"atze.

### Model B Paper 5: [2209.07714]
**Title:** Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations
**Category:** quant-ph
**Score:** 0.8527

Classical-quantum hybrid algorithms have recently garnered significant attention, which are characterized by combining quantum and classical computing protocols to obtain readout from quantum circuits of interest. Recent progress due to Lubasch et al in a 2019 paper provides readout for solutions to the Schrodinger and Inviscid Burgers equations, by making use of a new variational quantum algorithm (VQA) which determines the ground state of a cost function expressed with a superposition of expectation values and variational parameters. In the following, we analyze additional computational prospects in which the VQA can reliably produce solutions to other PDEs that are comparable to solutions that have been previously realized classically, which are characterized with noiseless quantum simulations. To determine the range of nonlinearities that the algorithm can process for other IVPs, we study several PDEs, first beginning with the Navier-Stokes equations and progressing to other equations underlying physical phenomena ranging from electromagnetism, gravitation, and wave propagation, from simulations of the Einstein, Boussniesq-type, Lin-Tsien, Camassa-Holm, Drinfeld-Sokolov-Wilson (DSW), and Hunter-Saxton equations. To formulate optimization routines that the VQA undergoes for numerical approximations of solutions that are obtained as readout from quantum circuits, cost functions corresponding to each PDE are provided in the supplementary section after which simulations results from hundreds of ZGR-QFT ansatzae are generated.

### Model B Paper 6: [2601.14226]
**Title:** Deep Learning Approaches to Quantum Error Mitigation
**Category:** quant-ph
**Score:** 0.8315

We present a systematic investigation of deep learning methods applied to quantum error mitigation of noisy output probability distributions from measured quantum circuits. We compare different architectures, from fully connected neural networks to transformers, and we test different design/training modalities, identifying sequence-to-sequence, attention-based models as the most effective on our datasets. These models consistently produce mitigated distributions that are closer to the ideal outputs when tested on both simulated and real device data obtained from IBM superconducting quantum processing units (QPU) up to five qubits. Across several different circuit depths, our approach outperforms other baseline error mitigation techniques. We perform a series of ablation studies to examine: how different input features (circuit, device properties, noisy output statistics) affect performance; cross-dataset generalization across circuit families; and transfer learning to a different IBM QPU. We observe that generalization performance across similar devices with the same architecture works effectively, without needing to fully retrain models.

### Model B Paper 7: [2601.01877]
**Title:** Random-Matrix-Induced Simplicity Bias in Over-parameterized Variational Quantum Circuits
**Category:** quant-ph
**Score:** 0.8256

Over-parameterization is commonly used to increase the expressivity of variational quantum circuits (VQCs), yet deeper and more highly parameterized circuits often exhibit poor trainability and limited generalization. In this work, we provide a theoretical explanation for this phenomenon from a function-class perspective. We show that sufficiently expressive, unstructured variational ansatze enter a Haar-like universality class in which both observable expectation values and parameter gradients concentrate exponentially with system size. As a consequence, the hypothesis class induced by such circuits collapses with high probability to a narrow family of near-constant functions, a phenomenon we term simplicity bias, with barren plateaus arising as a consequence rather than the root cause. Using tools from random matrix theory and concentration of measure, we rigorously characterize this universality class and establish uniform hypothesis-class collapse over finite datasets. We further show that this collapse is not unavoidable: tensor-structured VQCs, including tensor-network-based and tensor-hypernetwork parameterizations, lie outside the Haar-like universality class. By restricting the accessible unitary ensemble through bounded tensor rank or bond dimension, these architectures prevent concentration of measure, preserve output variability for local observables, and retain non-degenerate gradient signals even in over-parameterized regimes. Together, our results unify barren plateaus, expressivity limits, and generalization collapse under a single structural mechanism rooted in random-matrix universality, highlighting the central role of architectural inductive bias in variational quantum algorithms.

### Model B Paper 8: [2601.03802]
**Title:** Quantum vs. Classical Machine Learning: A Benchmark Study for Financial Prediction
**Category:** cs.LG
**Score:** 0.8222

In this paper, we present a reproducible benchmarking framework that systematically compares QML models with architecture-matched classical counterparts across three financial tasks: (i) directional return prediction on U.S. and Turkish equities, (ii) live-trading simulation with Quantum LSTMs versus classical LSTMs on the S\&P 500, and (iii) realized volatility forecasting using Quantum Support Vector Regression. By standardizing data splits, features, and evaluation metrics, our study provides a fair assessment of when current-generation QML models can match or exceed classical methods. Our results reveal that quantum approaches show performance gains when data structure and circuit design are well aligned. In directional classification, hybrid quantum neural networks surpass the parameter-matched ANN by \textbf{+3.8 AUC} and \textbf{+3.4 accuracy points} on \texttt{AAPL} stock and by \textbf{+4.9 AUC} and \textbf{+3.6 accuracy points} on Turkish stock \texttt{KCHOL}. In live trading, the QLSTM achieves higher risk-adjusted returns in \textbf{two of four} S\&P~500 regimes. For volatility forecasting, an angle-encoded QSVR attains the \textbf{lowest QLIKE} on \texttt{KCHOL} and remains within $\sim$0.02-0.04 QLIKE of the best classical kernels on \texttt{S\&P~500} and \texttt{AAPL}. Our benchmarking framework clearly identifies the scenarios where current QML architectures offer tangible improvements and where established classical methods continue to dominate.

### Model B Paper 9: [2509.12341]
**Title:** Exact Coset Sampling for Quantum Lattice Algorithms
**Category:** quant-ph
**Score:** 0.8196

We revisit the post-processing phase of Chen's Karst-wave quantum lattice algorithm (Chen, 2024) in the Learning with Errors (LWE) parameter regime. Conditioned on a transcript $E$, the post-Step 7 coordinate state on $(\mathbb{Z}_M)^n$ is supported on an affine grid line $\{\, j\Delta + v^{\ast}(E) + M_2 k \bmod M : j \in \mathbb{Z},\ k \in \mathcal{K} \,\}$, with $\Delta = 2D^2 b$, $M = 2M_2 = 2D^2 Q$, and $Q$ odd. The amplitudes include a quadratic Karst-wave chirp $\exp(-2\pi i j^2 / Q)$ and an unknown run-dependent offset $v^{\ast}(E)$. We show that Chen's Steps 8-9 can be replaced by a single exact post-processing routine: measure the deterministic residue $\tau := X_1 \bmod D^2$, obtain the run-local class $v_{1,Q} := v_1^{\ast}(E) \bmod Q$ as explicit side information in our access model, apply a $v_{1,Q}$-dependent diagonal quadratic phase on $X_1$ to cancel the chirp, and then apply $\mathrm{QFT}_{\mathbb{Z}_M}^{\otimes n}$ to the coordinate registers. The routine never needs the full offset $v^{\ast}(E)$. Under Additional Conditions AC1-AC5 on the front end, a measured Fourier outcome $u \in \mathbb{Z}_M^n$ satisfies the resonance $\langle b, u \rangle \equiv 0 \pmod Q$ with probability $1 - o(1)$. Moreover, conditioned on resonance, the reduced outcome $u \bmod Q$ is exactly uniform on the dual hyperplane $H = \{\, v \in \mathbb{Z}_Q^n : \langle b, v \rangle \equiv 0 \pmod Q \,\}$.

### Model B Paper 10: [2411.02535]
**Title:** Polynomial-Time Classical Simulation of Noisy Quantum Circuits with Naturally Fault-Tolerant Gates
**Category:** quant-ph
**Score:** 0.8168

We construct a polynomial-time classical algorithm that samples from the output distribution of noisy geometrically local Clifford circuits with any product-state input and single-qubit measurements in any basis. Our results apply to circuits with nearest-neighbor gates on an $O(1)$-D architecture with depolarizing noise after each gate. Importantly, we assume that the circuit does not contain qubit resets or mid-circuit measurements. This class of circuits includes Clifford-magic circuits and Conjugated-Clifford circuits, which are important candidates for demonstrating quantum advantage using non-universal gates. Additionally, our results can be extended to the case of IQP circuits augmented with CNOT gates, which is another class of non-universal circuits that are relevant to current experiments. Importantly, these results do not require randomness assumptions over the circuit families considered (such as anticoncentration properties) and instead hold for every circuit in each class as long as the depth is above a constant threshold. This allows us to rule out the possibility of fault-tolerance in these circuit models. As a key technical step, we prove that interspersed noise causes a decay of long-range entanglement at depths beyond a critical threshold. To prove our results, we merge techniques from percolation theory and Pauli path analysis.

### Model B Paper 11: [2507.01726]
**Title:** Generative flow-based warm start of the variational quantum eigensolver
**Category:** quant-ph
**Score:** 0.8104

Hybrid quantum-classical algorithms like the variational quantum eigensolver (VQE) show promise for quantum simulations on near-term quantum devices, but are often limited by complex objective functions and expensive optimization procedures. Here, we propose Flow-VQE, a generative framework leveraging conditional normalizing flows with parameterized quantum circuits to efficiently generate high-quality variational parameters. By embedding a generative model into the VQE optimization loop through preference-based training, Flow-VQE enables quantum gradient-free optimization and offers a systematic approach for parameter transfer, accelerating convergence across related problems through warm-started optimization. We compare Flow-VQE to a number of standard benchmarks through numerical simulations on molecular systems, including hydrogen chains, water, ammonia, and benzene. We find that Flow-VQE outperforms baseline optimization algorithms, achieving computational accuracy with fewer circuit evaluations (improvements range from modest to more than two orders of magnitude) and, when used to warm-start the optimization of new systems, accelerates subsequent fine-tuning by up to 50-fold compared with Hartree--Fock initialization. Therefore, we believe Flow-VQE can become a pragmatic and versatile paradigm for leveraging generative modeling to reduce the costs of variational quantum algorithms.

### Model B Paper 12: [2507.16036]
**Title:** Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks
**Category:** quant-ph
**Score:** 0.8085

Quantum computers face inherent scaling challenges, a fact that necessitates investigation of distributed quantum computing systems, whereby scaling is achieved through interconnection of smaller quantum processing units. However, connecting large numbers of QPUs will eventually result in connectivity constraints at the network level, where the difficulty of entanglement sharing increases with network path lengths. This increases the complexity of the quantum circuit partitioning problem, since the cost of generating entanglement between end nodes varies with network topologies and existing links. We address this challenge using a simple modification to existing partitioning schemes designed for all-to-all connected networks, that efficiently accounts for both of these factors. We investigate the performance in terms of entanglement requirements and optimisation time of various quantum circuits over different network topologies, achieving lower entanglement costs in the majority of cases than state-of-the-art methods. We provide techniques for scaling to large-scale quantum networks employing both network and problem coarsening. We show that coarsened methods can achieve improved solution quality in most cases with significantly lower run-times than direct partitioning methods.

### Model B Paper 13: [2601.18811]
**Title:** Variational Quantum Circuit-Based Reinforcement Learning for Dynamic Portfolio Optimization
**Category:** cs.LG
**Score:** 0.8064

This paper presents a Quantum Reinforcement Learning (QRL) solution to the dynamic portfolio optimization problem based on Variational Quantum Circuits. The implemented QRL approaches are quantum analogues of the classical neural-network-based Deep Deterministic Policy Gradient and Deep Q-Network algorithms. Through an empirical evaluation on real-world financial data, we show that our quantum agents achieve risk-adjusted performance comparable to, and in some cases exceeding, that of classical Deep RL models with several orders of magnitude more parameters. However, while quantum circuit execution is inherently fast at the hardware level, practical deployment on cloud-based quantum systems introduces substantial latency, making end-to-end runtime currently dominated by infrastructural overhead and limiting practical applicability. Taken together, our results suggest that QRL is theoretically competitive with state-of-the-art classical reinforcement learning and may become practically advantageous as deployment overheads diminish. This positions QRL as a promising paradigm for dynamic decision-making in complex, high-dimensional, and non-stationary environments such as financial markets. The complete codebase is released as open source at: https://github.com/VincentGurgul/qrl-dpo-public

### Model B Paper 14: [2601.05250]
**Title:** QNeRF: Neural Radiance Fields on a Simulated Gate-Based Quantum Computer
**Category:** cs.CV
**Score:** 0.8054

Recently, Quantum Visual Fields (QVFs) have shown promising improvements in model compactness and convergence speed for learning the provided 2D or 3D signals. Meanwhile, novel-view synthesis has seen major advances with Neural Radiance Fields (NeRFs), where models learn a compact representation from 2D images to render 3D scenes, albeit at the cost of larger models and intensive training. In this work, we extend the approach of QVFs by introducing QNeRF, the first hybrid quantum-classical model designed for novel-view synthesis from 2D images. QNeRF leverages parameterised quantum circuits to encode spatial and view-dependent information via quantum superposition and entanglement, resulting in more compact models compared to the classical counterpart. We present two architectural variants. Full QNeRF maximally exploits all quantum amplitudes to enhance representational capabilities. In contrast, Dual-Branch QNeRF introduces a task-informed inductive bias by branching spatial and view-dependent quantum state preparations, drastically reducing the complexity of this operation and ensuring scalability and potential hardware compatibility. Our experiments demonstrate that -- when trained on images of moderate resolution -- QNeRF matches or outperforms classical NeRF baselines while using less than half the number of parameters. These results suggest that quantum machine learning can serve as a competitive alternative for continuous signal representation in mid-level tasks in computer vision, such as 3D representation learning from 2D observations.

### Model B Paper 15: [2601.02064]
**Title:** Cutting Quantum Circuits Beyond Qubits
**Category:** quant-ph
**Score:** 0.8046

We extend quantum circuit cutting to heterogeneous registers comprising mixed-dimensional qudits. By decomposing non-local interactions into tensor products of local generalised Gell-Mann matrices, we enable the simulation and execution of high-dimensional circuits on disconnected hardware fragments. We validate this framework on qubit--qutrit ($2$--$3$) interfaces, achieving exact state reconstruction with a Total Variation Distance of 0 within single-precision floating-point tolerance. Furthermore, we demonstrate the memory advantage in an 8-particle, dimension-8 system, reducing memory usage from 128 MB to 64 KB per circuit.

### Model B Paper 16: [2601.06332]
**Title:** Bipartitioning of Graph States for Distributed Measurement-Based Quantum Computing
**Category:** quant-ph
**Score:** 0.7975

Measurement-Based Quantum Computing (MBQC) is inherently well-suited for Distributed Quantum Computing (DQC): once a resource state is prepared and distributed across a network of quantum nodes, computation proceeds through local measurements coordinated by classical communication. However, since non-local gates acting on different Quantum Processing Units (QPUs) are a bottleneck, it is crucial to optimize the qubit assignment to minimize inter-node entanglement of the shared resource. For graph state resources shared across two QPUs, this task reduces to finding bipartitions with minimal cut rank. We introduce a simulated annealing-based algorithm that efficiently updates the cut rank when two vertices swap sides across a bipartition, such that computing the new cut rank from scratch, which would be much more expensive, is not necessary. We show that the approach is highly effective for determining qubit assignments in distributed MBQC by testing it on grid graphs and the measurement-based Quantum Approximate Optimization Algorithm (QAOA).

### Model B Paper 17: [2510.09824]
**Title:** Quantum Circuit for Quantum Fourier Transform for Arbitrary Qubit Connectivity Graphs
**Category:** quant-ph
**Score:** 0.7964

In the paper, we consider quantum circuits for the Quantum Fourier Transform (QFT) algorithm. The QFT algorithm is a very popular technique used in many quantum algorithms. We present a generic method for constructing quantum circuits for this algorithm implementing on quantum devices with restrictions. Many quantum devices (for example, based on superconductors) have restrictions on applying two-qubit gates. These restrictions are presented by a qubit connectivity graph. Typically, researchers consider only the linear nearest neighbor (LNN) architecture of the qubit connection, but current devices have more complex graphs. We present a method for arbitrary connected graphs that minimizes the number of CNOT gates in the circuit for implementing on such architecture.
  We compare quantum circuits built by our algorithm with existing quantum circuits optimized for specific graphs that are Linear-nearest-neighbor (LNN) architecture, ``sun'' (a cycle with tails, presented by the 16-qubit IBMQ device) and ``two joint suns'' (two joint cycles with tails, presented by the 27-qubit IBMQ device). Our generic method gives similar results with existing optimized circuits for ``sun'' and ``two joint suns'' architectures, and a circuit with slightly more CNOT gates for the LNN architecture. At the same time, our method allows us to construct a circuit for arbitrary connected graphs.

### Model B Paper 18: [2505.16714]
**Title:** Experimental robustness benchmarking of quantum neural networks on a superconducting quantum processor
**Category:** quant-ph
**Score:** 0.7959

Quantum machine learning (QML) models, like their classical counterparts, are vulnerable to adversarial attacks, hindering their secure deployment. Here, we report the first systematic experimental robustness benchmark for 20-qubit quantum neural network (QNN) classifiers executed on a superconducting processor. Our benchmarking framework features an efficient adversarial attack algorithm designed for QNNs, enabling quantitative characterization of adversarial robustness and robustness bounds. From our analysis, we verify that adversarial training reduces sensitivity to targeted perturbations by regularizing input gradients, significantly enhancing QNN's robustness. Additionally, our analysis reveals that QNNs exhibit superior adversarial robustness compared to classical neural networks, an advantage attributed to inherent quantum noise. Furthermore, the empirical upper bound extracted from our attack experiments shows a minimal deviation ($3 \times 10^{-3}$) from the theoretical lower bound, providing strong experimental confirmation of the attack's effectiveness and the tightness of fidelity-based robustness bounds. This work establishes a critical experimental framework for assessing and improving quantum adversarial robustness, paving the way for secure and reliable QML applications.

### Model B Paper 19: [2601.16004]
**Title:** Wigner's Friend as a Circuit: Inter-Branch Communication Witness Benchmarks on Superconducting Quantum Hardware
**Category:** quant-ph
**Score:** 0.7902

We implement and benchmark on IBM Quantum hardware the circuit family proposed by Violaris for estimating operational inter-branch communication witnesses, defined as correlations in classical measurement records produced by compiled Wigner's-friend-style circuits. We realize a five-qubit instance of the protocol as an inter-register message-transfer pattern within a single circuit, rather than physical signaling, and evaluate its behavior under realistic device noise and compilation constraints. The circuit encodes branch-conditioned evolution of an observer subsystem whose dynamics depend on a control qubit, followed by a controlled transfer operation that probes correlations between conditional measurement contexts.
  Executing on the ibm_fez backend with 20000 shots, we observe population-based visibility of 0.877, coherence witnesses of 0.840 and -0.811 along orthogonal axes, and a phase-sensitive magnitude of approximately 1.17. While the visibility metric is insensitive to some classes of dephasing, the coherence witnesses provide complementary sensitivity to off-diagonal noise.
  This work does not test or discriminate among interpretations of quantum mechanics. Instead, it provides a reproducible operational constraint pipeline for evaluating detectability of non-ideal channels relative to calibrated device noise.

### Model B Paper 20: [2601.19635]
**Title:** DynQ: A Dynamic Topology-Agnostic Quantum Virtual Machine via Quality-Weighted Community Detection
**Category:** quant-ph
**Score:** 0.7884

Quantum cloud platforms remain fundamentally non-virtualised: despite rapid hardware scaling, each user program still monopolises an entire quantum processor, preventing resource sharing, economic scalability, and quality-of-service differentiation. Existing Quantum Virtual Machine (QVM) designs attempt spatial multiplexing through topology-specific or template-based partitioning, but these approaches are brittle under hardware heterogeneity, calibration drift, and transient defects, which dominate real quantum devices. We present DynQ, the first dynamic, topology-agnostic Quantum Virtual Machine that virtualises quantum hardware using quality-weighted community detection. Instead of imposing fixed geometric regions, DynQ models a quantum processor as a weighted graph derived from live calibration data and automatically discovers execution regions that maximise internal gate quality while minimising inter-region coupling. This operationalises the classical virtualisation principle of high cohesion and low coupling in a quantum-native setting, producing execution regions that are connectivity-efficient, noise-aware, and resilient to crosstalk and defects. We evaluate DynQ across five IBM Quantum backends using calibration-derived noise simulation and on two production devices, comparing against state-of-the-art QVM and standard compilation baselines. On hardware with pronounced spatial quality variation, DynQ achieves up to 19.1 percent higher fidelity and 45.1 percent lower output error. When transient hardware defects cause baseline executions to fail completely, DynQ adapts dynamically and achieves over 86 percent fidelity. By transforming calibrated device graphs into adaptive virtual hardware abstractions, DynQ decouples quantum programs from fragile physical layouts and enables reliable, high-utilisation quantum cloud services.

---


### Model A Paper 1: [2601.11937]
**Title:** Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection
**Category:** quant-ph
**Score:** 0.8031

High-Energy Physics (HEP) experiments, such as those at the Large Hadron Collider (LHC), generate massive datasets that challenge classical computational limits. Quantum Machine Learning (QML) offers a potential advantage in processing high-dimensional data; however, finding the optimal architecture for current Noisy Intermediate-Scale Quantum (NISQ) devices remains an open challenge. This study investigates the performance of Variational Quantum Classifiers (VQC) in detecting Higgs Boson signals using the ATLAS Higgs Boson Machine Learning Challenge 2014 experiment dataset. We implemented a dimensionality reduction pipeline using Principal Component Analysis (PCA) to map 30 physical features into 4-qubit and 8-qubit latent spaces. We benchmarked three configurations: (A) a shallow 4-qubit circuit, (B) a deep 4-qubit circuit with increased entanglement layers, and (C) an expanded 8-qubit circuit. Experimental results demonstrate that increasing circuit depth significantly improves performance, yielding the highest accuracy of 56.2% (Configuration B), compared to a baseline of 51.9%. Conversely, simply scaling to 8 qubits resulted in a performance degradation to 50.6% due to optimization challenges associated with Barren Plateaus in the larger Hilbert space. These findings suggest that for near-term quantum hardware, prioritizing circuit depth and entanglement capability is more critical than increasing qubit count for effective anomaly detection in HEP data.

### Model A Paper 2: [2601.18710]
**Title:** Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia
**Category:** cs.ET
**Score:** 0.7975

This paper presents a feasibility study demonstrating that quantum machine learning (QML) algorithms achieve competitive performance on real-world medical imaging despite operating under severe constraints. We evaluate Equilibrium Propagation (EP), an energy-based learning method that does not use backpropagation (incompatible with quantum systems due to state-collapsing measurements) and Variational Quantum Circuits (VQCs) for automated detection of Acute Myeloid Leukemia (AML) from blood cell microscopy images using binary classification (2 classes: AML vs. Healthy).
  Key Result: Using limited subsets (50-250 samples per class) of the AML-Cytomorphology dataset (18,365 expert-annotated images), quantum methods achieve performance only 12-15% below classical CNNs despite reduced image resolution (64x64 pixels), engineered features (20D), and classical simulation via Qiskit. EP reaches 86.4% accuracy (only 12% below CNN) without backpropagation, while the 4-qubit VQC attains 83.0% accuracy with consistent data efficiency: VQC maintains stable 83% performance with only 50 samples per class, whereas CNN requires 250 samples (5x more data) to reach 98%. These results establish reproducible baselines for QML in healthcare, validating NISQ-era feasibility.

### Model A Paper 3: [2506.22555]
**Title:** Spectral Bias in Variational Quantum Machine Learning
**Category:** quant-ph
**Score:** 0.7954

In this work, we investigate the phenomenon of spectral bias in quantum machine learning, where, in classical settings, models tend to fit low-frequency components of a target function earlier during training than high-frequency ones, demonstrating a frequency-dependent rate of convergence. We study this effect specifically in parameterised quantum circuits (PQCs). Leveraging the established formulation of PQCs as Fourier series, we prove that spectral bias in this setting arises from the ``redundancy'' of the Fourier coefficients, which denotes the number of terms in the analytical form of the model contributing to the same frequency component. The choice of data encoding scheme dictates the degree of redundancy for a Fourier coefficient. We find that the magnitude of the Fourier coefficients' gradients during training strongly correlates with the coefficients' redundancy. We then further demonstrate this empirically with three different encoding schemes. Additionally, we demonstrate that PQCs with greater redundancy exhibit increased robustness to random perturbations in their parameters at the corresponding frequencies. We investigate how design choices affect the ability of PQCs to learn Fourier sums, focusing on parameter initialization scale and entanglement structure, finding large initializations and low-entanglement schemes tend to slow convergence.

### Model A Paper 4: [2507.16036]
**Title:** Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks
**Category:** quant-ph
**Score:** 0.7579

Quantum computers face inherent scaling challenges, a fact that necessitates investigation of distributed quantum computing systems, whereby scaling is achieved through interconnection of smaller quantum processing units. However, connecting large numbers of QPUs will eventually result in connectivity constraints at the network level, where the difficulty of entanglement sharing increases with network path lengths. This increases the complexity of the quantum circuit partitioning problem, since the cost of generating entanglement between end nodes varies with network topologies and existing links. We address this challenge using a simple modification to existing partitioning schemes designed for all-to-all connected networks, that efficiently accounts for both of these factors. We investigate the performance in terms of entanglement requirements and optimisation time of various quantum circuits over different network topologies, achieving lower entanglement costs in the majority of cases than state-of-the-art methods. We provide techniques for scaling to large-scale quantum networks employing both network and problem coarsening. We show that coarsened methods can achieve improved solution quality in most cases with significantly lower run-times than direct partitioning methods.

### Model A Paper 5: [2502.04271]
**Title:** Variational decision diagrams for quantum-inspired machine learning applications
**Category:** quant-ph
**Score:** 0.7302

Decision diagrams (DDs) have emerged as an efficient tool for simulating quantum circuits due to their capacity to exploit data redundancies in quantum states and quantum operations, enabling the efficient computation of probability amplitudes. However, their application in quantum machine learning (QML) has remained unexplored. This paper introduces variational decision diagrams (VDDs), a novel graph structure that combines the structural benefits of DDs with the adaptability of variational methods for efficiently representing quantum states. We investigate the trainability of VDDs by applying them to the ground state estimation problem for transverse-field Ising and Heisenberg Hamiltonians. Analysis of gradient variance suggests that training VDDs is possible, as no signs of vanishing gradients--also known as barren plateaus--are observed. This work provides new insights into the use of decision diagrams in QML as an alternative to design and train variational ans\"atze.

### Model A Paper 6: [2501.15828]
**Title:** Hybrid Quantum Neural Networks with Amplitude Encoding: Advancing Recovery Rate Predictions
**Category:** q-fin.CP
**Score:** 0.7274

Recovery rate prediction plays a pivotal role in bond investment strategies by enhancing risk assessment, optimizing portfolio allocation, improving pricing accuracy, and supporting effective credit risk management. However, accurate forecasting remains challenging due to complex nonlinear dependencies, high-dimensional feature spaces, and limited sample sizes-conditions under which classical machine learning models are prone to overfitting. We propose a hybrid Quantum Machine Learning (QML) model with Amplitude Encoding, leveraging the unitarity constraint of Parametrized Quantum Circuits (PQC) and the exponential data compression capability of qubits. We evaluate the model on a global recovery rate dataset comprising 1,725 observations and 256 features from 1996 to 2023. Our hybrid method significantly outperforms both classical neural networks and QML models using Angle Encoding, achieving a lower Root Mean Squared Error (RMSE) of 0.228, compared to 0.246 and 0.242, respectively. It also performs competitively with ensemble tree methods such as XGBoost. While practical implementation challenges remain for Noisy Intermediate-Scale Quantum (NISQ) hardware, our quantum simulation and preliminary results on noisy simulators demonstrate the promise of hybrid quantum-classical architectures in enhancing the accuracy and robustness of recovery rate forecasting. These findings illustrate the potential of quantum machine learning in shaping the future of credit risk prediction.

### Model A Paper 7: [2507.01726]
**Title:** Generative flow-based warm start of the variational quantum eigensolver
**Category:** quant-ph
**Score:** 0.7108

Hybrid quantum-classical algorithms like the variational quantum eigensolver (VQE) show promise for quantum simulations on near-term quantum devices, but are often limited by complex objective functions and expensive optimization procedures. Here, we propose Flow-VQE, a generative framework leveraging conditional normalizing flows with parameterized quantum circuits to efficiently generate high-quality variational parameters. By embedding a generative model into the VQE optimization loop through preference-based training, Flow-VQE enables quantum gradient-free optimization and offers a systematic approach for parameter transfer, accelerating convergence across related problems through warm-started optimization. We compare Flow-VQE to a number of standard benchmarks through numerical simulations on molecular systems, including hydrogen chains, water, ammonia, and benzene. We find that Flow-VQE outperforms baseline optimization algorithms, achieving computational accuracy with fewer circuit evaluations (improvements range from modest to more than two orders of magnitude) and, when used to warm-start the optimization of new systems, accelerates subsequent fine-tuning by up to 50-fold compared with Hartree--Fock initialization. Therefore, we believe Flow-VQE can become a pragmatic and versatile paradigm for leveraging generative modeling to reduce the costs of variational quantum algorithms.

### Model A Paper 8: [2209.07714]
**Title:** Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations
**Category:** quant-ph
**Score:** 0.7080

Classical-quantum hybrid algorithms have recently garnered significant attention, which are characterized by combining quantum and classical computing protocols to obtain readout from quantum circuits of interest. Recent progress due to Lubasch et al in a 2019 paper provides readout for solutions to the Schrodinger and Inviscid Burgers equations, by making use of a new variational quantum algorithm (VQA) which determines the ground state of a cost function expressed with a superposition of expectation values and variational parameters. In the following, we analyze additional computational prospects in which the VQA can reliably produce solutions to other PDEs that are comparable to solutions that have been previously realized classically, which are characterized with noiseless quantum simulations. To determine the range of nonlinearities that the algorithm can process for other IVPs, we study several PDEs, first beginning with the Navier-Stokes equations and progressing to other equations underlying physical phenomena ranging from electromagnetism, gravitation, and wave propagation, from simulations of the Einstein, Boussniesq-type, Lin-Tsien, Camassa-Holm, Drinfeld-Sokolov-Wilson (DSW), and Hunter-Saxton equations. To formulate optimization routines that the VQA undergoes for numerical approximations of solutions that are obtained as readout from quantum circuits, cost functions corresponding to each PDE are provided in the supplementary section after which simulations results from hundreds of ZGR-QFT ansatzae are generated.

### Model A Paper 9: [2505.16714]
**Title:** Experimental robustness benchmarking of quantum neural networks on a superconducting quantum processor
**Category:** quant-ph
**Score:** 0.6895

Quantum machine learning (QML) models, like their classical counterparts, are vulnerable to adversarial attacks, hindering their secure deployment. Here, we report the first systematic experimental robustness benchmark for 20-qubit quantum neural network (QNN) classifiers executed on a superconducting processor. Our benchmarking framework features an efficient adversarial attack algorithm designed for QNNs, enabling quantitative characterization of adversarial robustness and robustness bounds. From our analysis, we verify that adversarial training reduces sensitivity to targeted perturbations by regularizing input gradients, significantly enhancing QNN's robustness. Additionally, our analysis reveals that QNNs exhibit superior adversarial robustness compared to classical neural networks, an advantage attributed to inherent quantum noise. Furthermore, the empirical upper bound extracted from our attack experiments shows a minimal deviation ($3 \times 10^{-3}$) from the theoretical lower bound, providing strong experimental confirmation of the attack's effectiveness and the tightness of fidelity-based robustness bounds. This work establishes a critical experimental framework for assessing and improving quantum adversarial robustness, paving the way for secure and reliable QML applications.

### Model A Paper 10: [2504.11109]
**Title:** Agent-Q: Fine-Tuning Large Language Models for Quantum Circuit Generation and Optimization
**Category:** quant-ph
**Score:** 0.6846

Large language models (LLMs) have achieved remarkable outcomes in complex problems, including math, coding, and analyzing large amounts of scientific reports. Yet, few works have explored the potential of LLMs in quantum computing. The most challenging problem is to leverage LLMs to automatically generate quantum circuits at a large scale. Fundamentally, the existing pre-trained LLMs lack the knowledge of quantum circuits. In this paper, we address this challenge by fine-tuning LLMs and injecting the domain-specific knowledge of quantum computing. We describe Agent-Q, an LLM fine-tuning system to generate and optimize quantum circuits. In particular, Agent-Q implements the mechanisms to generate training data sets and constructs an end-to-end pipeline to fine-tune pre-trained LLMs to generate parameterized quantum circuits for various optimization problems. Agent-Q provides 14,000 quantum circuits covering a large spectrum of the quantum optimization landscape: 12 optimization problem instances and their optimized QAOA, VQE, and adaptive VQE circuits. Based thereon, Agent-Q fine-tunes LLMs and constructs syntactically correct parametrized quantum circuits in OpenQASM 3.0. We have evaluated the quality of the LLM-generated circuits and parameters by comparing them to the optimized expectation values and distributions. Experimental results show superior performance of Agent-Q, compared to several state-of-the-art LLMs and better parameters than random. Agent-Q can be integrated into an agentic workflow, and the generated parametrized circuits with initial parameters can be used as a starting point for further optimization, e.g., as templates in quantum machine learning and as benchmarks for compilers and hardware.

### Model A Paper 11: [2601.14226]
**Title:** Deep Learning Approaches to Quantum Error Mitigation
**Category:** quant-ph
**Score:** 0.6778

We present a systematic investigation of deep learning methods applied to quantum error mitigation of noisy output probability distributions from measured quantum circuits. We compare different architectures, from fully connected neural networks to transformers, and we test different design/training modalities, identifying sequence-to-sequence, attention-based models as the most effective on our datasets. These models consistently produce mitigated distributions that are closer to the ideal outputs when tested on both simulated and real device data obtained from IBM superconducting quantum processing units (QPU) up to five qubits. Across several different circuit depths, our approach outperforms other baseline error mitigation techniques. We perform a series of ablation studies to examine: how different input features (circuit, device properties, noisy output statistics) affect performance; cross-dataset generalization across circuit families; and transfer learning to a different IBM QPU. We observe that generalization performance across similar devices with the same architecture works effectively, without needing to fully retrain models.

### Model A Paper 12: [2601.18811]
**Title:** Variational Quantum Circuit-Based Reinforcement Learning for Dynamic Portfolio Optimization
**Category:** cs.LG
**Score:** 0.6697

This paper presents a Quantum Reinforcement Learning (QRL) solution to the dynamic portfolio optimization problem based on Variational Quantum Circuits. The implemented QRL approaches are quantum analogues of the classical neural-network-based Deep Deterministic Policy Gradient and Deep Q-Network algorithms. Through an empirical evaluation on real-world financial data, we show that our quantum agents achieve risk-adjusted performance comparable to, and in some cases exceeding, that of classical Deep RL models with several orders of magnitude more parameters. However, while quantum circuit execution is inherently fast at the hardware level, practical deployment on cloud-based quantum systems introduces substantial latency, making end-to-end runtime currently dominated by infrastructural overhead and limiting practical applicability. Taken together, our results suggest that QRL is theoretically competitive with state-of-the-art classical reinforcement learning and may become practically advantageous as deployment overheads diminish. This positions QRL as a promising paradigm for dynamic decision-making in complex, high-dimensional, and non-stationary environments such as financial markets. The complete codebase is released as open source at: https://github.com/VincentGurgul/qrl-dpo-public

### Model A Paper 13: [2601.14024]
**Title:** Performance enhancing of hybrid quantum-classical Benders approach for MILP optimization
**Category:** quant-ph
**Score:** 0.6596

Mixed-integer linear programming problems are extensively used in industry for a wide range of optimization tasks. However, as they get larger, they present computational challenges for classical solvers within practical time limits. Quantum annealers can, in principle, accelerate the solution of problems formulated as quadratic unconstrained binary optimization instances, but their limited scale currently prevents achieving practical speedups. Quantum-classical algorithms have been proposed to take advantage of both paradigms and to allow current quantum computers to be used in larger problems. In this work, a hardware-agnostic Benders' decomposition algorithm and a series of enhancements with the goal of taking the most advantage of quantum computing are presented. The decomposition consists of a master problem with integer variables, which is reformulated as a quadratic unconstrained binary optimization problem and solved with a quantum annealer, and a linear subproblem solved by a classical computer. The enhancements consist, among others, of different embedding processes that substantially reduce the pre-processing time of the embedding computation without compromising solution quality, a conservative handling of cut constraints, and a stopping criterion that accounts for the limited size of current quantum computers and their heuristic nature. The proposed algorithm is benchmarked against classical approaches using a D-Wave quantum annealer for a scalable family of transmission network expansion planning problems.

### Model A Paper 14: [2601.18198]
**Title:** Scalable Quantum Message Passing Graph Neural Networks for Next-Generation Wireless Communications: Architectures, Use Cases, and Future Directions
**Category:** cs.IT
**Score:** 0.6551

Graph Neural Networks (GNNs) are eminently suitable for wireless resource management, thanks to their scalability, but they still face computational challenges in large-scale, dense networks in classical computers. The integration of quantum computing with GNNs offers a promising pathway for enhancing computational efficiency because they reduce the model complexity. This is achieved by leveraging the quantum advantages of parameterized quantum circuits (PQCs), while retaining the expressive power of GNNs. However, existing pure quantum message passing models remain constrained by the limited number of qubits, hence limiting the scalability of their application to the wireless systems. As a remedy, we conceive a Scalable Quantum Message Passing Graph Neural Network (SQM-GNN) relying on a quantum message passing architecture. To address the aforementioned scalability issue, we decompose the graph into subgraphs and apply a shared PQC to each local subgraph. Importantly, the model incorporates both node and edge features, facilitating the full representation of the underlying wireless graph structure. We demonstrate the efficiency of SQM GNN on a device-to-device (D2D) power control task, where it outperforms both classical GNNs and heuristic baselines. These results highlight SQM-GNN as a promising direction for future wireless network optimization.

### Model A Paper 15: [2312.15547]
**Title:** Quantum Approximate Optimization Algorithm for Test Case Optimization
**Category:** cs.SE
**Score:** 0.6545

Test case optimization (TCO) reduces software testing cost while preserving its effectiveness, but solving TCO problems for large-scale and complex systems requires substantial computational resources. Quantum approximate optimization algorithms (QAOAs) are promising combinatorial optimization algorithms that rely on quantum computational resources, with the potential efficiency advantages over classical approaches. Several proof-of-concept applications of QAOAs for solving combinatorial problems, such as portfolio optimization, energy systems, and job scheduling, have been proposed. Given the lack of investigation into QAOA's application to TCO problems, and motivated by the computational challenges of TCO problems and the potential of QAOAs, we present IGDec-QAOA to formulate a TCO problem as a QAOA problem and solve it on both ideal and noisy quantum computer simulators, as well as on a real quantum computer. To solve bigger TCO problems that require many qubits, which are unavailable currently, we integrate a problem decomposition strategy with the QAOA. We performed an empirical evaluation with five TCO problems and four publicly available industrial datasets from ABB, Google, and Orona to compare various configurations of IGDec-QAOA, assess its decomposition strategy of handling large datasets, and compare its performance with classical algorithms (i.e., GA and Random Search). Based on the evaluation results achieved on an ideal simulator, we recommend the best configuration of our approach for TCO problems. We also demonstrate that it can reach the same effectiveness as GA and outperform GA in two out of five test case optimization problems. In addition, we observe that, on a noisy simulator, IGDec-QAOA achieved similar performance to that from an ideal simulator. Finally, we demonstrate the feasibility of IGDec-QAOA on a real quantum computer in the presence of noise.

### Model A Paper 16: [2601.05250]
**Title:** QNeRF: Neural Radiance Fields on a Simulated Gate-Based Quantum Computer
**Category:** cs.CV
**Score:** 0.6475

Recently, Quantum Visual Fields (QVFs) have shown promising improvements in model compactness and convergence speed for learning the provided 2D or 3D signals. Meanwhile, novel-view synthesis has seen major advances with Neural Radiance Fields (NeRFs), where models learn a compact representation from 2D images to render 3D scenes, albeit at the cost of larger models and intensive training. In this work, we extend the approach of QVFs by introducing QNeRF, the first hybrid quantum-classical model designed for novel-view synthesis from 2D images. QNeRF leverages parameterised quantum circuits to encode spatial and view-dependent information via quantum superposition and entanglement, resulting in more compact models compared to the classical counterpart. We present two architectural variants. Full QNeRF maximally exploits all quantum amplitudes to enhance representational capabilities. In contrast, Dual-Branch QNeRF introduces a task-informed inductive bias by branching spatial and view-dependent quantum state preparations, drastically reducing the complexity of this operation and ensuring scalability and potential hardware compatibility. Our experiments demonstrate that -- when trained on images of moderate resolution -- QNeRF matches or outperforms classical NeRF baselines while using less than half the number of parameters. These results suggest that quantum machine learning can serve as a competitive alternative for continuous signal representation in mid-level tasks in computer vision, such as 3D representation learning from 2D observations.

### Model A Paper 17: [2510.09824]
**Title:** Quantum Circuit for Quantum Fourier Transform for Arbitrary Qubit Connectivity Graphs
**Category:** quant-ph
**Score:** 0.6435

In the paper, we consider quantum circuits for the Quantum Fourier Transform (QFT) algorithm. The QFT algorithm is a very popular technique used in many quantum algorithms. We present a generic method for constructing quantum circuits for this algorithm implementing on quantum devices with restrictions. Many quantum devices (for example, based on superconductors) have restrictions on applying two-qubit gates. These restrictions are presented by a qubit connectivity graph. Typically, researchers consider only the linear nearest neighbor (LNN) architecture of the qubit connection, but current devices have more complex graphs. We present a method for arbitrary connected graphs that minimizes the number of CNOT gates in the circuit for implementing on such architecture.
  We compare quantum circuits built by our algorithm with existing quantum circuits optimized for specific graphs that are Linear-nearest-neighbor (LNN) architecture, ``sun'' (a cycle with tails, presented by the 16-qubit IBMQ device) and ``two joint suns'' (two joint cycles with tails, presented by the 27-qubit IBMQ device). Our generic method gives similar results with existing optimized circuits for ``sun'' and ``two joint suns'' architectures, and a circuit with slightly more CNOT gates for the LNN architecture. At the same time, our method allows us to construct a circuit for arbitrary connected graphs.

### Model A Paper 18: [2601.09374]
**Title:** Network-Based Quantum Computing: an efficient design framework for many-small-node distributed fault-tolerant quantum computing
**Category:** quant-ph
**Score:** 0.6341

In fault-tolerant quantum computing, a large number of physical qubits are required to construct a single logical qubit, and a single quantum node may be able to hold only a small number of logical qubits. In such a case, the idea of distributed fault-tolerant quantum computing (DFTQC) is important to demonstrate large-scale quantum computation using small-scale nodes. However, the design of distributed systems on small-scale nodes, where each node can store only one or a few logical qubits for computation, has not been explored well yet. In this paper, we propose network-based quantum computation (NBQC) to efficiently realize distributed fault-tolerant quantum computation using many small-scale nodes. A key idea of NBQC is to let computational data continuously move throughout the network while maintaining the connectivity to other nodes. We numerically show that, for practical benchmark tasks, our method achieves shorter execution times than circuit-based strategies and more node-efficient constructions than measurement-based quantum computing. Also, if we are allowed to specialize the network to the structure of quantum programs, such as peak access frequencies, the number of nodes can be significantly reduced. Thus, our methods provide a foundation in designing DFTQC architecture exploiting the redundancy of many small fault-tolerant nodes.

### Model A Paper 19: [2601.01777]
**Title:** A Survey on Applications of Quantum Computing for Unit Commitment
**Category:** quant-ph
**Score:** 0.6329

Unit Commitment (UC) is a core optimization problem in power system operation and electricity market scheduling. It determines the optimal on/off status and dispatch of generating units while satisfying system, operational, and market constraints. Traditionally, UC has been solved using mixed-integer programming, dynamic programming, or metaheuristic methods, all of which face scalability challenges as systems grow in size and uncertainty. Recent advances in quantum computing, spanning quantum annealing, variational algorithms, and hybrid quantum classical optimization, have opened new opportunities to accelerate UC solution processes by exploiting quantum parallelism and entanglement. This paper presents a comprehensive survey of existing research on the applications of quantum computing for solving the UC problem. The reviewed works are categorized based on the employed quantum paradigms, including annealing-based, variational hybrid, quantum machine learning, and quantum-inspired methods. Key modeling strategies, hardware implementations, and computational trade-offs are discussed, highlighting the current progress, limitations, and potential future directions for large-scale quantum-enabled UC.

### Model A Paper 20: [2507.02577]
**Title:** Quantum Computing in the Computational Landscape of Power Electronics: Vision and Reality
**Category:** quant-ph
**Score:** 0.6320

Quantum computing is rapidly emerging as a promising technology for solving complex optimization problems that arise in various engineering fields. Therefore, it holds significant promise to transform the computational foundations of power electronics. Motivated by this potential, this paper adopts a visionary perspective to examine how quantum computing could influence the evolution of power electronics in areas such as converter design, control, modulation, simulation workflows, and beyond. Within this framework, the current status, limitations, and anticipated progress of quantum algorithms and hardware are discussed, together with their potential to enable efficient solutions to large-scale, multiobjective, mixed-integer optimization problems. To place these developments in context, the paper begins with a concise tutorial on fundamental concepts in quantum computing, serving as both an introduction to the field and a bridge to its potential applications in power electronics. As a first step in this direction, the use of quantum computing for solving offline mixed-integer optimization problems commonly encountered in power electronics is examined. To this end, a simplified power electronics design problem is reformulated as a quadratic unconstrained binary optimization (QUBO) problem and executed on quantum hardware, despite current limitations such as low qubit counts and hardware noise. This demonstration marks a pioneering step towards leveraging quantum computing in power electronics and motivates the value of early adoption and exploration. Building on these insights, the paper outlines a forward-looking vision in which quantum computing becomes an integral part of the computational landscape of power electronics, guiding its transition from classical to quantum-enabled design and operation.

---

## Review Instructions

You are reviewing recommendations from two models for the interest profile "Quantum computing / quantum ML".
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
