# Single-Strategy Characterization Review

**Model:** gte
**Profile:** Quantum computing / quantum ML (P3)
**Depth:** full
**Overlap with MiniLM:** 15/20 shared, 5 unique to gte

## Seed Papers
  - [2601.18710] Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia (cs.ET)
  - [2506.22555] Spectral Bias in Variational Quantum Machine Learning (quant-ph)
  - [2601.11937] Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection (quant-ph)
  - [2209.07714] Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations (quant-ph)
  - [2507.16036] Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks (quant-ph)

## gte Top-20 Recommendations

### Paper 1: [2506.22555]
**Title:** Spectral Bias in Variational Quantum Machine Learning
**Category:** quant-ph
**Score:** 0.8548
**In MiniLM top-20:** True

In this work, we investigate the phenomenon of spectral bias in quantum machine learning, where, in classical settings, models tend to fit low-frequency components of a target function earlier during training than high-frequency ones, demonstrating a frequency-dependent rate of convergence. We study this effect specifically in parameterised quantum circuits (PQCs). Leveraging the established formulation of PQCs as Fourier series, we prove that spectral bias in this setting arises from the ``redundancy'' of the Fourier coefficients, which denotes the number of terms in the analytical form of the model contributing to the same frequency component. The choice of data encoding scheme dictates the degree of redundancy for a Fourier coefficient. We find that the magnitude of the Fourier coefficients' gradients during training strongly correlates with the coefficients' redundancy. We then further demonstrate this empirically with three different encoding schemes. Additionally, we demonstrate that PQCs with greater redundancy exhibit increased robustness to random perturbations in their parameters at the corresponding frequencies. We investigate how design choices affect the ability of PQCs to learn Fourier sums, focusing on parameter initialization scale and entanglement structure, finding large initializations and low-entanglement schemes tend to slow convergence.

### Paper 2: [2601.18710]
**Title:** Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia
**Category:** cs.ET
**Score:** 0.8529
**In MiniLM top-20:** True

This paper presents a feasibility study demonstrating that quantum machine learning (QML) algorithms achieve competitive performance on real-world medical imaging despite operating under severe constraints. We evaluate Equilibrium Propagation (EP), an energy-based learning method that does not use backpropagation (incompatible with quantum systems due to state-collapsing measurements) and Variational Quantum Circuits (VQCs) for automated detection of Acute Myeloid Leukemia (AML) from blood cell microscopy images using binary classification (2 classes: AML vs. Healthy).
  Key Result: Using limited subsets (50-250 samples per class) of the AML-Cytomorphology dataset (18,365 expert-annotated images), quantum methods achieve performance only 12-15% below classical CNNs despite reduced image resolution (64x64 pixels), engineered features (20D), and classical simulation via Qiskit. EP reaches 86.4% accuracy (only 12% below CNN) without backpropagation, while the 4-qubit VQC attains 83.0% accuracy with consistent data efficiency: VQC maintains stable 83% performance with only 50 samples per class, whereas CNN requires 250 samples (5x more data) to reach 98%. These results establish reproducible baselines for QML in healthcare, validating NISQ-era feasibility.

### Paper 3: [2601.11937]
**Title:** Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection
**Category:** quant-ph
**Score:** 0.8299
**In MiniLM top-20:** True

High-Energy Physics (HEP) experiments, such as those at the Large Hadron Collider (LHC), generate massive datasets that challenge classical computational limits. Quantum Machine Learning (QML) offers a potential advantage in processing high-dimensional data; however, finding the optimal architecture for current Noisy Intermediate-Scale Quantum (NISQ) devices remains an open challenge. This study investigates the performance of Variational Quantum Classifiers (VQC) in detecting Higgs Boson signals using the ATLAS Higgs Boson Machine Learning Challenge 2014 experiment dataset. We implemented a dimensionality reduction pipeline using Principal Component Analysis (PCA) to map 30 physical features into 4-qubit and 8-qubit latent spaces. We benchmarked three configurations: (A) a shallow 4-qubit circuit, (B) a deep 4-qubit circuit with increased entanglement layers, and (C) an expanded 8-qubit circuit. Experimental results demonstrate that increasing circuit depth significantly improves performance, yielding the highest accuracy of 56.2% (Configuration B), compared to a baseline of 51.9%. Conversely, simply scaling to 8 qubits resulted in a performance degradation to 50.6% due to optimization challenges associated with Barren Plateaus in the larger Hilbert space. These findings suggest that for near-term quantum hardware, prioritizing circuit depth and entanglement capability is more critical than increasing qubit count for effective anomaly detection in HEP data.

### Paper 4: [2209.07714]
**Title:** Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations
**Category:** quant-ph
**Score:** 0.8051
**In MiniLM top-20:** True

Classical-quantum hybrid algorithms have recently garnered significant attention, which are characterized by combining quantum and classical computing protocols to obtain readout from quantum circuits of interest. Recent progress due to Lubasch et al in a 2019 paper provides readout for solutions to the Schrodinger and Inviscid Burgers equations, by making use of a new variational quantum algorithm (VQA) which determines the ground state of a cost function expressed with a superposition of expectation values and variational parameters. In the following, we analyze additional computational prospects in which the VQA can reliably produce solutions to other PDEs that are comparable to solutions that have been previously realized classically, which are characterized with noiseless quantum simulations. To determine the range of nonlinearities that the algorithm can process for other IVPs, we study several PDEs, first beginning with the Navier-Stokes equations and progressing to other equations underlying physical phenomena ranging from electromagnetism, gravitation, and wave propagation, from simulations of the Einstein, Boussniesq-type, Lin-Tsien, Camassa-Holm, Drinfeld-Sokolov-Wilson (DSW), and Hunter-Saxton equations. To formulate optimization routines that the VQA undergoes for numerical approximations of solutions that are obtained as readout from quantum circuits, cost functions corresponding to each PDE are provided in the supplementary section after which simulations results from hundreds of ZGR-QFT ansatzae are generated.

### Paper 5: [2502.04271]
**Title:** Variational decision diagrams for quantum-inspired machine learning applications
**Category:** quant-ph
**Score:** 0.7894
**In MiniLM top-20:** True

Decision diagrams (DDs) have emerged as an efficient tool for simulating quantum circuits due to their capacity to exploit data redundancies in quantum states and quantum operations, enabling the efficient computation of probability amplitudes. However, their application in quantum machine learning (QML) has remained unexplored. This paper introduces variational decision diagrams (VDDs), a novel graph structure that combines the structural benefits of DDs with the adaptability of variational methods for efficiently representing quantum states. We investigate the trainability of VDDs by applying them to the ground state estimation problem for transverse-field Ising and Heisenberg Hamiltonians. Analysis of gradient variance suggests that training VDDs is possible, as no signs of vanishing gradients--also known as barren plateaus--are observed. This work provides new insights into the use of decision diagrams in QML as an alternative to design and train variational ans\"atze.

### Paper 6: [2507.16036]
**Title:** Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks
**Category:** quant-ph
**Score:** 0.7878
**In MiniLM top-20:** True

Quantum computers face inherent scaling challenges, a fact that necessitates investigation of distributed quantum computing systems, whereby scaling is achieved through interconnection of smaller quantum processing units. However, connecting large numbers of QPUs will eventually result in connectivity constraints at the network level, where the difficulty of entanglement sharing increases with network path lengths. This increases the complexity of the quantum circuit partitioning problem, since the cost of generating entanglement between end nodes varies with network topologies and existing links. We address this challenge using a simple modification to existing partitioning schemes designed for all-to-all connected networks, that efficiently accounts for both of these factors. We investigate the performance in terms of entanglement requirements and optimisation time of various quantum circuits over different network topologies, achieving lower entanglement costs in the majority of cases than state-of-the-art methods. We provide techniques for scaling to large-scale quantum networks employing both network and problem coarsening. We show that coarsened methods can achieve improved solution quality in most cases with significantly lower run-times than direct partitioning methods.

### Paper 7 [DIVERGENT]: [2601.01877]
**Title:** Random-Matrix-Induced Simplicity Bias in Over-parameterized Variational Quantum Circuits
**Category:** quant-ph
**Score:** 0.7839
**In MiniLM top-20:** False

Over-parameterization is commonly used to increase the expressivity of variational quantum circuits (VQCs), yet deeper and more highly parameterized circuits often exhibit poor trainability and limited generalization. In this work, we provide a theoretical explanation for this phenomenon from a function-class perspective. We show that sufficiently expressive, unstructured variational ansatze enter a Haar-like universality class in which both observable expectation values and parameter gradients concentrate exponentially with system size. As a consequence, the hypothesis class induced by such circuits collapses with high probability to a narrow family of near-constant functions, a phenomenon we term simplicity bias, with barren plateaus arising as a consequence rather than the root cause. Using tools from random matrix theory and concentration of measure, we rigorously characterize this universality class and establish uniform hypothesis-class collapse over finite datasets. We further show that this collapse is not unavoidable: tensor-structured VQCs, including tensor-network-based and tensor-hypernetwork parameterizations, lie outside the Haar-like universality class. By restricting the accessible unitary ensemble through bounded tensor rank or bond dimension, these architectures prevent concentration of measure, preserve output variability for local observables, and retain non-degenerate gradient signals even in over-parameterized regimes. Together, our results unify barren plateaus, expressivity limits, and generalization collapse under a single structural mechanism rooted in random-matrix universality, highlighting the central role of architectural inductive bias in variational quantum algorithms.

### Paper 8: [2504.11109]
**Title:** Agent-Q: Fine-Tuning Large Language Models for Quantum Circuit Generation and Optimization
**Category:** quant-ph
**Score:** 0.7758
**In MiniLM top-20:** True

Large language models (LLMs) have achieved remarkable outcomes in complex problems, including math, coding, and analyzing large amounts of scientific reports. Yet, few works have explored the potential of LLMs in quantum computing. The most challenging problem is to leverage LLMs to automatically generate quantum circuits at a large scale. Fundamentally, the existing pre-trained LLMs lack the knowledge of quantum circuits. In this paper, we address this challenge by fine-tuning LLMs and injecting the domain-specific knowledge of quantum computing. We describe Agent-Q, an LLM fine-tuning system to generate and optimize quantum circuits. In particular, Agent-Q implements the mechanisms to generate training data sets and constructs an end-to-end pipeline to fine-tune pre-trained LLMs to generate parameterized quantum circuits for various optimization problems. Agent-Q provides 14,000 quantum circuits covering a large spectrum of the quantum optimization landscape: 12 optimization problem instances and their optimized QAOA, VQE, and adaptive VQE circuits. Based thereon, Agent-Q fine-tunes LLMs and constructs syntactically correct parametrized quantum circuits in OpenQASM 3.0. We have evaluated the quality of the LLM-generated circuits and parameters by comparing them to the optimized expectation values and distributions. Experimental results show superior performance of Agent-Q, compared to several state-of-the-art LLMs and better parameters than random. Agent-Q can be integrated into an agentic workflow, and the generated parametrized circuits with initial parameters can be used as a starting point for further optimization, e.g., as templates in quantum machine learning and as benchmarks for compilers and hardware.

### Paper 9: [2601.05250]
**Title:** QNeRF: Neural Radiance Fields on a Simulated Gate-Based Quantum Computer
**Category:** cs.CV
**Score:** 0.7715
**In MiniLM top-20:** True

Recently, Quantum Visual Fields (QVFs) have shown promising improvements in model compactness and convergence speed for learning the provided 2D or 3D signals. Meanwhile, novel-view synthesis has seen major advances with Neural Radiance Fields (NeRFs), where models learn a compact representation from 2D images to render 3D scenes, albeit at the cost of larger models and intensive training. In this work, we extend the approach of QVFs by introducing QNeRF, the first hybrid quantum-classical model designed for novel-view synthesis from 2D images. QNeRF leverages parameterised quantum circuits to encode spatial and view-dependent information via quantum superposition and entanglement, resulting in more compact models compared to the classical counterpart. We present two architectural variants. Full QNeRF maximally exploits all quantum amplitudes to enhance representational capabilities. In contrast, Dual-Branch QNeRF introduces a task-informed inductive bias by branching spatial and view-dependent quantum state preparations, drastically reducing the complexity of this operation and ensuring scalability and potential hardware compatibility. Our experiments demonstrate that -- when trained on images of moderate resolution -- QNeRF matches or outperforms classical NeRF baselines while using less than half the number of parameters. These results suggest that quantum machine learning can serve as a competitive alternative for continuous signal representation in mid-level tasks in computer vision, such as 3D representation learning from 2D observations.

### Paper 10: [2507.01726]
**Title:** Generative flow-based warm start of the variational quantum eigensolver
**Category:** quant-ph
**Score:** 0.7698
**In MiniLM top-20:** True

Hybrid quantum-classical algorithms like the variational quantum eigensolver (VQE) show promise for quantum simulations on near-term quantum devices, but are often limited by complex objective functions and expensive optimization procedures. Here, we propose Flow-VQE, a generative framework leveraging conditional normalizing flows with parameterized quantum circuits to efficiently generate high-quality variational parameters. By embedding a generative model into the VQE optimization loop through preference-based training, Flow-VQE enables quantum gradient-free optimization and offers a systematic approach for parameter transfer, accelerating convergence across related problems through warm-started optimization. We compare Flow-VQE to a number of standard benchmarks through numerical simulations on molecular systems, including hydrogen chains, water, ammonia, and benzene. We find that Flow-VQE outperforms baseline optimization algorithms, achieving computational accuracy with fewer circuit evaluations (improvements range from modest to more than two orders of magnitude) and, when used to warm-start the optimization of new systems, accelerates subsequent fine-tuning by up to 50-fold compared with Hartree--Fock initialization. Therefore, we believe Flow-VQE can become a pragmatic and versatile paradigm for leveraging generative modeling to reduce the costs of variational quantum algorithms.

### Paper 11 [DIVERGENT]: [2601.19635]
**Title:** DynQ: A Dynamic Topology-Agnostic Quantum Virtual Machine via Quality-Weighted Community Detection
**Category:** quant-ph
**Score:** 0.7630
**In MiniLM top-20:** False

Quantum cloud platforms remain fundamentally non-virtualised: despite rapid hardware scaling, each user program still monopolises an entire quantum processor, preventing resource sharing, economic scalability, and quality-of-service differentiation. Existing Quantum Virtual Machine (QVM) designs attempt spatial multiplexing through topology-specific or template-based partitioning, but these approaches are brittle under hardware heterogeneity, calibration drift, and transient defects, which dominate real quantum devices. We present DynQ, the first dynamic, topology-agnostic Quantum Virtual Machine that virtualises quantum hardware using quality-weighted community detection. Instead of imposing fixed geometric regions, DynQ models a quantum processor as a weighted graph derived from live calibration data and automatically discovers execution regions that maximise internal gate quality while minimising inter-region coupling. This operationalises the classical virtualisation principle of high cohesion and low coupling in a quantum-native setting, producing execution regions that are connectivity-efficient, noise-aware, and resilient to crosstalk and defects. We evaluate DynQ across five IBM Quantum backends using calibration-derived noise simulation and on two production devices, comparing against state-of-the-art QVM and standard compilation baselines. On hardware with pronounced spatial quality variation, DynQ achieves up to 19.1 percent higher fidelity and 45.1 percent lower output error. When transient hardware defects cause baseline executions to fail completely, DynQ adapts dynamically and achieves over 86 percent fidelity. By transforming calibrated device graphs into adaptive virtual hardware abstractions, DynQ decouples quantum programs from fragile physical layouts and enables reliable, high-utilisation quantum cloud services.

### Paper 12: [2601.14226]
**Title:** Deep Learning Approaches to Quantum Error Mitigation
**Category:** quant-ph
**Score:** 0.7627
**In MiniLM top-20:** True

We present a systematic investigation of deep learning methods applied to quantum error mitigation of noisy output probability distributions from measured quantum circuits. We compare different architectures, from fully connected neural networks to transformers, and we test different design/training modalities, identifying sequence-to-sequence, attention-based models as the most effective on our datasets. These models consistently produce mitigated distributions that are closer to the ideal outputs when tested on both simulated and real device data obtained from IBM superconducting quantum processing units (QPU) up to five qubits. Across several different circuit depths, our approach outperforms other baseline error mitigation techniques. We perform a series of ablation studies to examine: how different input features (circuit, device properties, noisy output statistics) affect performance; cross-dataset generalization across circuit families; and transfer learning to a different IBM QPU. We observe that generalization performance across similar devices with the same architecture works effectively, without needing to fully retrain models.

### Paper 13: [2601.18811]
**Title:** Variational Quantum Circuit-Based Reinforcement Learning for Dynamic Portfolio Optimization
**Category:** cs.LG
**Score:** 0.7522
**In MiniLM top-20:** True

This paper presents a Quantum Reinforcement Learning (QRL) solution to the dynamic portfolio optimization problem based on Variational Quantum Circuits. The implemented QRL approaches are quantum analogues of the classical neural-network-based Deep Deterministic Policy Gradient and Deep Q-Network algorithms. Through an empirical evaluation on real-world financial data, we show that our quantum agents achieve risk-adjusted performance comparable to, and in some cases exceeding, that of classical Deep RL models with several orders of magnitude more parameters. However, while quantum circuit execution is inherently fast at the hardware level, practical deployment on cloud-based quantum systems introduces substantial latency, making end-to-end runtime currently dominated by infrastructural overhead and limiting practical applicability. Taken together, our results suggest that QRL is theoretically competitive with state-of-the-art classical reinforcement learning and may become practically advantageous as deployment overheads diminish. This positions QRL as a promising paradigm for dynamic decision-making in complex, high-dimensional, and non-stationary environments such as financial markets. The complete codebase is released as open source at: https://github.com/VincentGurgul/qrl-dpo-public

### Paper 14: [2510.09824]
**Title:** Quantum Circuit for Quantum Fourier Transform for Arbitrary Qubit Connectivity Graphs
**Category:** quant-ph
**Score:** 0.7502
**In MiniLM top-20:** True

In the paper, we consider quantum circuits for the Quantum Fourier Transform (QFT) algorithm. The QFT algorithm is a very popular technique used in many quantum algorithms. We present a generic method for constructing quantum circuits for this algorithm implementing on quantum devices with restrictions. Many quantum devices (for example, based on superconductors) have restrictions on applying two-qubit gates. These restrictions are presented by a qubit connectivity graph. Typically, researchers consider only the linear nearest neighbor (LNN) architecture of the qubit connection, but current devices have more complex graphs. We present a method for arbitrary connected graphs that minimizes the number of CNOT gates in the circuit for implementing on such architecture.
  We compare quantum circuits built by our algorithm with existing quantum circuits optimized for specific graphs that are Linear-nearest-neighbor (LNN) architecture, ``sun'' (a cycle with tails, presented by the 16-qubit IBMQ device) and ``two joint suns'' (two joint cycles with tails, presented by the 27-qubit IBMQ device). Our generic method gives similar results with existing optimized circuits for ``sun'' and ``two joint suns'' architectures, and a circuit with slightly more CNOT gates for the LNN architecture. At the same time, our method allows us to construct a circuit for arbitrary connected graphs.

### Paper 15 [DIVERGENT]: [2601.02818]
**Title:** Quantum-enhanced long short-term memory with attention for spatial permeability prediction in oilfield reservoirs
**Category:** cs.AI
**Score:** 0.7489
**In MiniLM top-20:** False

Spatial prediction of reservoir parameters, especially permeability, is crucial for oil and gas exploration and development. However, the wide range and high variability of permeability prevent existing methods from providing reliable predictions. For the first time in subsurface spatial prediction, this study presents a quantum-enhanced long short-term memory with attention (QLSTMA) model that incorporates variational quantum circuits (VQCs) into the recurrent cell. Using quantum entanglement and superposition principles, the QLSTMA significantly improves the ability to predict complex geological parameters such as permeability. Two quantization structures, QLSTMA with Shared Gates (QLSTMA-SG) and with Independent Gates (QLSTMA-IG), are designed to investigate and evaluate the effects of quantum structure configurations and the number of qubits on model performance. Experimental results demonstrate that the 8-qubit QLSTMA-IG model significantly outperforms the traditional long short-term memory with attention (LSTMA), reducing Mean Absolute Error (MAE) by 19% and Root Mean Squared Error (RMSE) by 20%, with particularly strong performance in regions featuring complex well-logging data. These findings validate the potential of quantum-classical hybrid neural networks for reservoir prediction, indicating that increasing the number of qubits yields further accuracy gains despite the reliance on classical simulations. This study establishes a foundational framework for the eventual deployment of such models on real quantum hardware and their extension to broader applications in petroleum engineering and geoscience.

### Paper 16: [2501.15828]
**Title:** Hybrid Quantum Neural Networks with Amplitude Encoding: Advancing Recovery Rate Predictions
**Category:** q-fin.CP
**Score:** 0.7462
**In MiniLM top-20:** True

Recovery rate prediction plays a pivotal role in bond investment strategies by enhancing risk assessment, optimizing portfolio allocation, improving pricing accuracy, and supporting effective credit risk management. However, accurate forecasting remains challenging due to complex nonlinear dependencies, high-dimensional feature spaces, and limited sample sizes-conditions under which classical machine learning models are prone to overfitting. We propose a hybrid Quantum Machine Learning (QML) model with Amplitude Encoding, leveraging the unitarity constraint of Parametrized Quantum Circuits (PQC) and the exponential data compression capability of qubits. We evaluate the model on a global recovery rate dataset comprising 1,725 observations and 256 features from 1996 to 2023. Our hybrid method significantly outperforms both classical neural networks and QML models using Angle Encoding, achieving a lower Root Mean Squared Error (RMSE) of 0.228, compared to 0.246 and 0.242, respectively. It also performs competitively with ensemble tree methods such as XGBoost. While practical implementation challenges remain for Noisy Intermediate-Scale Quantum (NISQ) hardware, our quantum simulation and preliminary results on noisy simulators demonstrate the promise of hybrid quantum-classical architectures in enhancing the accuracy and robustness of recovery rate forecasting. These findings illustrate the potential of quantum machine learning in shaping the future of credit risk prediction.

### Paper 17 [DIVERGENT]: [2512.24173]
**Title:** Variational Quantum Brushes
**Category:** quant-ph
**Score:** 0.7459
**In MiniLM top-20:** False

Quantum brushes are computational arts software introduced by Ferreira et al (2025) that leverage quantum behavior to generate novel artistic effects. In this outreach paper, we introduce the mathematical framework and describe the implementation of two quantum brushes based on variational quantum algorithms, Steerable and Chemical. While Steerable uses quantum geometric control theory to merge two works of art, Chemical mimics variational eigensolvers for estimating molecular ground energies to evolve colors on an underlying canvas. The implementation of both brushes is available open-source at https://github.com/moth-quantum/QuantumBrush and is fully compatible with the original quantum brushes.

### Paper 18: [2601.09374]
**Title:** Network-Based Quantum Computing: an efficient design framework for many-small-node distributed fault-tolerant quantum computing
**Category:** quant-ph
**Score:** 0.7420
**In MiniLM top-20:** True

In fault-tolerant quantum computing, a large number of physical qubits are required to construct a single logical qubit, and a single quantum node may be able to hold only a small number of logical qubits. In such a case, the idea of distributed fault-tolerant quantum computing (DFTQC) is important to demonstrate large-scale quantum computation using small-scale nodes. However, the design of distributed systems on small-scale nodes, where each node can store only one or a few logical qubits for computation, has not been explored well yet. In this paper, we propose network-based quantum computation (NBQC) to efficiently realize distributed fault-tolerant quantum computation using many small-scale nodes. A key idea of NBQC is to let computational data continuously move throughout the network while maintaining the connectivity to other nodes. We numerically show that, for practical benchmark tasks, our method achieves shorter execution times than circuit-based strategies and more node-efficient constructions than measurement-based quantum computing. Also, if we are allowed to specialize the network to the structure of quantum programs, such as peak access frequencies, the number of nodes can be significantly reduced. Thus, our methods provide a foundation in designing DFTQC architecture exploiting the redundancy of many small fault-tolerant nodes.

### Paper 19: [2505.16714]
**Title:** Experimental robustness benchmarking of quantum neural networks on a superconducting quantum processor
**Category:** quant-ph
**Score:** 0.7382
**In MiniLM top-20:** True

Quantum machine learning (QML) models, like their classical counterparts, are vulnerable to adversarial attacks, hindering their secure deployment. Here, we report the first systematic experimental robustness benchmark for 20-qubit quantum neural network (QNN) classifiers executed on a superconducting processor. Our benchmarking framework features an efficient adversarial attack algorithm designed for QNNs, enabling quantitative characterization of adversarial robustness and robustness bounds. From our analysis, we verify that adversarial training reduces sensitivity to targeted perturbations by regularizing input gradients, significantly enhancing QNN's robustness. Additionally, our analysis reveals that QNNs exhibit superior adversarial robustness compared to classical neural networks, an advantage attributed to inherent quantum noise. Furthermore, the empirical upper bound extracted from our attack experiments shows a minimal deviation ($3 \times 10^{-3}$) from the theoretical lower bound, providing strong experimental confirmation of the attack's effectiveness and the tightness of fidelity-based robustness bounds. This work establishes a critical experimental framework for assessing and improving quantum adversarial robustness, paving the way for secure and reliable QML applications.

### Paper 20 [DIVERGENT]: [2601.00656]
**Title:** Quantum Simulation of Protein Fragment Electronic Structure Using Moment-based Adaptive Variational Quantum Algorithms
**Category:** q-bio.QM
**Score:** 0.7362
**In MiniLM top-20:** False

Background: Understanding electronic interactions in protein active sites is fundamental to drug discovery and enzyme engineering, but remains computationally challenging due to exponential scaling of quantum mechanical calculations.
  Results: We present a quantum-classical hybrid framework for simulating protein fragment electronic structure using variational quantum algorithms. We construct fermionic Hamiltonians from experimentally determined protein structures, map them to qubits via Jordan-Wigner transformation, and optimize ground state energies using the Variational Quantum Eigensolver implemented in pure Python. For a 4-orbital serine protease fragment, we achieve chemical accuracy (< 1.6 mHartree) with 95.3% correlation energy recovery. Systematic analysis reveals three-phase convergence behaviour with exponential decay ({\alpha} = 0.95), power law optimization ({\gamma} = 1.21), and asymptotic approach. Application to SARS-CoV-2 protease inhibition demonstrates predictive accuracy (MAE=0.25 kcal/mol), while cytochrome P450 metabolism predictions achieve 85% site accuracy.
  Conclusions: This work establishes a pathway for quantum-enhanced biomolecular simulations on near-term quantum hardware, bridging quantum algorithm development with practical biological applications.

---

## Review Instructions

You are reviewing the top-20 recommendations from gte for the profile "Quantum computing / quantum ML".
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
