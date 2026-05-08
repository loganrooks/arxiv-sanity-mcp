# Single-Strategy Characterization Review

**Model:** qwen3
**Profile:** Graph neural networks (P5)
**Depth:** full
**Overlap with MiniLM:** 18/20 shared, 2 unique to qwen3

## Seed Papers
  - [2503.06614] Using Subgraph GNNs for Node Classification:an Overlooked Potential Approach (cs.LG)
  - [2411.12732] Benchmarking Positional Encodings for GNNs and Graph Transformers (cs.LG)
  - [2506.22727] Convergent Privacy Framework for Multi-layer GNNs through Contractive Message Passing (cs.CR)
  - [2510.15583] Attn-JGNN: Attention Enhanced Join-Graph Neural Networks (cs.LG)
  - [2512.24901] Spectral Graph Neural Networks for Cognitive Task Classification in fMRI Connectomes (cs.LG)

## qwen3 Top-20 Recommendations

### Paper 1: [2503.06614]
**Title:** Using Subgraph GNNs for Node Classification:an Overlooked Potential Approach
**Category:** cs.LG
**Score:** 0.7735
**In MiniLM top-20:** True

Previous studies have demonstrated the strong performance of Graph Neural Networks (GNNs) in node classification. However, most existing GNNs adopt a node-centric perspective and rely on global message passing, leading to high computational and memory costs that hinder scalability. To mitigate these challenges, subgraph-based methods have been introduced, leveraging local subgraphs as approximations of full computational trees. While this approach improves efficiency, it often suffers from performance degradation due to the loss of global contextual information, limiting its effectiveness compared to global GNNs. To address this trade-off between scalability and classification accuracy, we reformulate the node classification task as a subgraph classification problem and propose SubGND (Subgraph GNN for NoDe). This framework introduces a differentiated zero-padding strategy and an Ego-Alter subgraph representation method to resolve label conflicts while incorporating an Adaptive Feature Scaling Mechanism to dynamically adjust feature contributions based on dataset-specific dependencies. Experimental results on six benchmark datasets demonstrate that SubGND achieves performance comparable to or surpassing global message-passing GNNs, particularly in heterophilic settings, highlighting its effectiveness and scalability as a promising solution for node classification.

### Paper 2: [2411.12732]
**Title:** Benchmarking Positional Encodings for GNNs and Graph Transformers
**Category:** cs.LG
**Score:** 0.7605
**In MiniLM top-20:** True

Positional Encodings (PEs) are essential for injecting structural information into Graph Neural Networks (GNNs), particularly Graph Transformers, yet their empirical impact remains insufficiently understood. We introduce a unified benchmarking framework that decouples PEs from architectural choices, enabling a fair comparison across 8 GNN and Transformer models, 9 PEs, and 10 synthetic and real-world datasets. Across more than 500 model-PE-dataset configurations, we find that commonly used expressiveness proxies, including Weisfeiler-Lehman distinguishability, do not reliably predict downstream performance. In particular, highly expressive PEs frequently fail to improve, and can even degrade performance on real-world tasks. At the same time, we identify several simple and previously overlooked model-PE combinations that match or outperform recent state-of-the-art methods. Our results demonstrate the strong task-dependence of PEs and underscore the need for empirical validation beyond theoretical expressiveness. To support reproducible research, we release an open-source benchmarking framework for evaluating PEs for graph learning tasks.

### Paper 3: [2506.22727]
**Title:** Convergent Privacy Framework for Multi-layer GNNs through Contractive Message Passing
**Category:** cs.CR
**Score:** 0.7560
**In MiniLM top-20:** True

Differential privacy (DP) has been integrated into graph neural networks (GNNs) to protect sensitive structural information, e.g., edges, nodes, and associated features across various applications. A prominent approach is to perturb the message-passing process, which forms the core of most GNN architectures. However, existing methods typically incur a privacy cost that grows linearly with the number of layers (e.g., GAP published in Usenix Security'23), ultimately requiring excessive noise to maintain a reasonable privacy level. This limitation becomes particularly problematic when multi-layer GNNs, which have shown better performance than one-layer GNN, are used to process graph data with sensitive information. In this paper, we theoretically establish that the privacy budget converges with respect to the number of layers by applying privacy amplification techniques to the message-passing process, exploiting the contractive properties inherent to standard GNN operations. Motivated by this analysis, we propose a simple yet effective Contractive Graph Layer (CGL) that ensures the contractiveness required for theoretical guarantees while preserving model utility. Our framework, CARIBOU, supports both training and inference, equipped with a contractive aggregation module, a privacy allocation module, and a privacy auditing module. Experimental evaluations demonstrate that CARIBOU significantly improves the privacy-utility trade-off and achieves superior performance in privacy auditing tasks.

### Paper 4: [2601.02451]
**Title:** mHC-GNN: Manifold-Constrained Hyper-Connections for Graph Neural Networks
**Category:** cs.LG
**Score:** 0.7527
**In MiniLM top-20:** True

Graph Neural Networks (GNNs) suffer from over-smoothing in deep architectures and expressiveness bounded by the 1-Weisfeiler-Leman (1-WL) test. We adapt Manifold-Constrained Hyper-Connections (\mhc)~\citep{xie2025mhc}, recently proposed for Transformers, to graph neural networks. Our method, mHC-GNN, expands node representations across $n$ parallel streams and constrains stream-mixing matrices to the Birkhoff polytope via Sinkhorn-Knopp normalization. We prove that mHC-GNN exhibits exponentially slower over-smoothing (rate $(1-\gamma)^{L/n}$ vs.\ $(1-\gamma)^L$) and can distinguish graphs beyond 1-WL. Experiments on 10 datasets with 4 GNN architectures show consistent improvements. Depth experiments from 2 to 128 layers reveal that standard GNNs collapse to near-random performance beyond 16 layers, while mHC-GNN maintains over 74\% accuracy even at 128 layers, with improvements exceeding 50 percentage points at extreme depths. Ablations confirm that the manifold constraint is essential: removing it causes up to 82\% performance degradation. Code is available at \href{https://github.com/smlab-niser/mhc-gnn}{https://github.com/smlab-niser/mhc-gnn}

### Paper 5: [2510.15583]
**Title:** Attn-JGNN: Attention Enhanced Join-Graph Neural Networks
**Category:** cs.LG
**Score:** 0.7155
**In MiniLM top-20:** True

We propose an Attention Enhanced Join-Graph Neural Networks(Attn-JGNN) model for solving #SAT problems, which significantly improves the solving accuracy. Inspired by the Iterative Join Graph Propagation (IJGP) algorithm, Attn-JGNN uses tree decomposition to encode the CNF formula into a join-graph, then performs iterative message passing on the join-graph, and finally approximates the model number by learning partition functions. In order to further improve the accuracy of the solution, we apply the attention mechanism in and between clusters of the join-graphs, which makes Attn-JGNN pay more attention to the key variables and clusters in probabilistic inference, and reduces the redundant calculation. Finally, our experiments show that our Attn-JGNN model achieves better results than other neural network methods.

### Paper 6: [2506.13911]
**Title:** Logical Expressiveness of Graph Neural Networks with Hierarchical Node Individualization
**Category:** cs.LG
**Score:** 0.7138
**In MiniLM top-20:** True

We propose and study Hierarchical Ego Graph Neural Networks (HEGNNs), an expressive extension of graph neural networks (GNNs) with hierarchical node individualization, inspired by the Individualization-Refinement paradigm for isomorphism testing. HEGNNs generalize subgraph-GNNs and form a hierarchy of increasingly expressive models that, in the limit, distinguish graphs up to isomorphism. We show that, over graphs of bounded degree, the separating power of HEGNN node classifiers equals that of graded hybrid logic. This characterization enables us to relate the separating power of HEGNNs to that of higher-order GNNs, GNNs enriched with local homomorphism count features, and color refinement algorithms based on Individualization-Refinement. Our experimental results confirm the practical feasibility of HEGNNs and show benefits in comparison with traditional GNN architectures, both with and without local homomorphism count features.

### Paper 7: [2512.24901]
**Title:** Spectral Graph Neural Networks for Cognitive Task Classification in fMRI Connectomes
**Category:** cs.LG
**Score:** 0.7008
**In MiniLM top-20:** True

Cognitive task classification using machine learning plays a central role in decoding brain states from neuroimaging data. By integrating machine learning with brain network analysis, complex connectivity patterns can be extracted from functional magnetic resonance imaging connectomes. This process transforms raw blood-oxygen-level-dependent (BOLD) signals into interpretable representations of cognitive processes. Graph neural networks (GNNs) further advance this paradigm by modeling brain regions as nodes and functional connections as edges, capturing topological dependencies and multi-scale interactions that are often missed by conventional approaches. Our proposed SpectralBrainGNN model, a spectral convolution framework based on graph Fourier transforms (GFT) computed via normalized Laplacian eigendecomposition. Experiments on the Human Connectome Project-Task (HCPTask) dataset demonstrate the effectiveness of the proposed approach, achieving a classification accuracy of 96.25\%. The implementation is publicly available at https://github.com/gnnplayground/SpectralBrainGNN to support reproducibility and future research.

### Paper 8: [2601.17774]
**Title:** CondenseGraph: Communication-Efficient Distributed GNN Training via On-the-Fly Graph Condensation
**Category:** cs.DC
**Score:** 0.6784
**In MiniLM top-20:** True

Distributed Graph Neural Network (GNN) training suffers from substantial communication overhead due to the inherent neighborhood dependency in graph-structured data. This neighbor explosion problem requires workers to frequently exchange boundary node features across partitions, creating a communication bottleneck that severely limits training scalability. Existing approaches rely on static graph partitioning strategies that cannot adapt to dynamic network conditions. In this paper, we propose CondenseGraph, a novel communication-efficient framework for distributed GNN training. Our key innovation is an on-the-fly graph condensation mechanism that dynamically compresses boundary node features into compact super nodes before transmission. To compensate for the information loss introduced by compression, we develop a gradient-based error feedback mechanism that maintains convergence guarantees while reducing communication volume by 40-60%. Extensive experiments on four benchmark datasets demonstrate that CondenseGraph achieves comparable accuracy to full-precision baselines while significantly reducing communication costs and training time.

### Paper 9: [2601.17130]
**Title:** How does Graph Structure Modulate Membership-Inference Risk for Graph Neural Networks?
**Category:** cs.LG
**Score:** 0.6783
**In MiniLM top-20:** True

Graph neural networks (GNNs) have become the standard tool for encoding data and their complex relationships into continuous representations, improving prediction accuracy in several machine learning tasks like node classification and link prediction. However, their use in sensitive applications has raised concerns about the potential leakage of training data. Research on privacy leakage in GNNs has largely been shaped by findings from non-graph domains, such as images and tabular data. We emphasize the need of graph specific analysis and investigate the impact of graph structure on node level membership inference. We formalize MI over node-neighbourhood tuples and investigate two important dimensions: (i) training graph construction and (ii) inference-time edge access. Empirically, snowball's coverage bias often harms generalisation relative to random sampling, while enabling inter-train-test edges at inference improves test accuracy, shrinks the train-test gap, and yields the lowest membership advantage across most of the models and datasets. We further show that the generalisation gap empirically measured as the performance difference between the train and test nodes is an incomplete proxy for MI risk: access to edges dominates-MI can rise or fall independent of gap changes. Finally, we examine the auditability of differentially private GNNs, adapting the definition of statistical exchangeability of train-test data points for graph based models. We show that for node level tasks the inductive splits (random or snowball sampled) break exchangeability, limiting the applicability of standard bounds for membership advantage of differential private models.

### Paper 10: [2601.19745]
**Title:** GraphDLG: Exploring Deep Leakage from Gradients in Federated Graph Learning
**Category:** cs.LG
**Score:** 0.6781
**In MiniLM top-20:** True

Federated graph learning (FGL) has recently emerged as a promising privacy-preserving paradigm that enables distributed graph learning across multiple data owners. A critical privacy concern in federated learning is whether an adversary can recover raw data from shared gradients, a vulnerability known as deep leakage from gradients (DLG). However, most prior studies on the DLG problem focused on image or text data, and it remains an open question whether graphs can be effectively recovered, particularly when the graph structure and node features are uniquely entangled in GNNs. In this work, we first theoretically analyze the components in FGL and derive a crucial insight: once the graph structure is recovered, node features can be obtained through a closed-form recursive rule. Building on this analysis, we propose GraphDLG, a novel approach to recover raw training graphs from shared gradients in FGL, which can utilize randomly generated graphs or client-side training graphs as auxiliaries to enhance recovery. Extensive experiments demonstrate that GraphDLG outperforms existing solutions by successfully decoupling the graph structure and node features, achieving improvements of over 5.46% (by MSE) for node feature reconstruction and over 25.04% (by AUC) for graph structure reconstruction.

### Paper 11: [2205.07266]
**Title:** Discovering the Representation Bottleneck of Graph Neural Networks
**Category:** cs.LG
**Score:** 0.6726
**In MiniLM top-20:** True

Graph neural networks (GNNs) rely mainly on the message-passing paradigm to propagate node features and build interactions, and different graph learning problems require different ranges of node interactions. In this work, we explore the capacity of GNNs to capture node interactions under contexts of different complexities. We discover that GNNs usually fail to capture the most informative kinds of interaction styles for diverse graph learning tasks, and thus name this phenomenon GNNs' representation bottleneck. As a response, we demonstrate that the inductive bias introduced by existing graph construction mechanisms can result in this representation bottleneck, \emph{i.e.}, preventing GNNs from learning interactions of the most appropriate complexity. To address that limitation, we propose a novel graph rewiring approach based on interaction patterns learned by GNNs to dynamically adjust each node's receptive fields. Extensive experiments on both real-world and synthetic datasets prove the effectiveness of our algorithm in alleviating the representation bottleneck and its superiority in enhancing the performance of GNNs over state-of-the-art graph rewiring baselines.

### Paper 12: [2410.01308]
**Title:** WL Tests Are Far from All We Need: Revisiting WL-Test Hardness and GNN Expressive Power from a Distributed Computation Perspective
**Category:** cs.LG
**Score:** 0.6596
**In MiniLM top-20:** True

The expressive power of graph neural networks (GNNs) is often studied through their relationship to the Weisfeiler-Lehman (WL) tests. Despite its influence, this perspective leaves two gaps: (i) it is unclear whether WL tests are sufficiently primitive for understanding GNN expressivity, and (ii) WL-induced equivalence does not align well with characterizing the function classes that GNNs can approximate or compute. We attempt to address both gaps. First, we strengthen hardness results for the vanilla WL test, showing that in many settings it is not primitive enough to be implemented by constant-depth GNNs. Second, we propose an alternative framework for studying GNN expressivity based on an extended CONGEST model with an explicit preprocessing phase. Within this framework, we identify implicit shortcuts introduced in prior analyses and establish further results for WL tests in settings where graphs are augmented with virtual nodes and virtual edges.

### Paper 13: [2601.01123]
**Title:** Learning from Historical Activations in Graph Neural Networks
**Category:** cs.LG
**Score:** 0.6566
**In MiniLM top-20:** True

Graph Neural Networks (GNNs) have demonstrated remarkable success in various domains such as social networks, molecular chemistry, and more. A crucial component of GNNs is the pooling procedure, in which the node features calculated by the model are combined to form an informative final descriptor to be used for the downstream task. However, previous graph pooling schemes rely on the last GNN layer features as an input to the pooling or classifier layers, potentially under-utilizing important activations of previous layers produced during the forward pass of the model, which we regard as historical graph activations. This gap is particularly pronounced in cases where a node's representation can shift significantly over the course of many graph neural layers, and worsened by graph-specific challenges such as over-smoothing in deep architectures. To bridge this gap, we introduce HISTOGRAPH, a novel two-stage attention-based final aggregation layer that first applies a unified layer-wise attention over intermediate activations, followed by node-wise attention. By modeling the evolution of node representations across layers, our HISTOGRAPH leverages both the activation history of nodes and the graph structure to refine features used for final prediction. Empirical results on multiple graph classification benchmarks demonstrate that HISTOGRAPH offers strong performance that consistently improves traditional techniques, with particularly strong robustness in deep GNNs.

### Paper 14: [2601.17469]
**Title:** Identifying and Correcting Label Noise for Robust GNNs via Influence Contradiction
**Category:** cs.LG
**Score:** 0.6504
**In MiniLM top-20:** True

Graph Neural Networks (GNNs) have shown remarkable capabilities in learning from graph-structured data with various applications such as social analysis and bioinformatics. However, the presence of label noise in real scenarios poses a significant challenge in learning robust GNNs, and their effectiveness can be severely impacted when dealing with noisy labels on graphs, often stemming from annotation errors or inconsistencies. To address this, in this paper we propose a novel approach called ICGNN that harnesses the structure information of the graph to effectively alleviate the challenges posed by noisy labels. Specifically, we first design a novel noise indicator that measures the influence contradiction score (ICS) based on the graph diffusion matrix to quantify the credibility of nodes with clean labels, such that nodes with higher ICS values are more likely to be detected as having noisy labels. Then we leverage the Gaussian mixture model to precisely detect whether the label of a node is noisy or not. Additionally, we develop a soft strategy to combine the predictions from neighboring nodes on the graph to correct the detected noisy labels. At last, pseudo-labeling for abundant unlabeled nodes is incorporated to provide auxiliary supervision signals and guide the model optimization. Experiments on benchmark datasets show the superiority of our proposed approach.

### Paper 15: [2601.04807]
**Title:** Parallelizing Node-Level Explainability in Graph Neural Networks
**Category:** cs.LG
**Score:** 0.6471
**In MiniLM top-20:** True

Graph Neural Networks (GNNs) have demonstrated remarkable performance in a wide range of tasks, such as node classification, link prediction, and graph classification, by exploiting the structural information in graph-structured data. However, in node classification, computing node-level explainability becomes extremely time-consuming as the size of the graph increases, while batching strategies often degrade explanation quality. This paper introduces a novel approach to parallelizing node-level explainability in GNNs through graph partitioning. By decomposing the graph into disjoint subgraphs, we enable parallel computation of explainability for node neighbors, significantly improving the scalability and efficiency without affecting the correctness of the results, provided sufficient memory is available. For scenarios where memory is limited, we further propose a dropout-based reconstruction mechanism that offers a controllable trade-off between memory usage and explanation fidelity. Experimental results on real-world datasets demonstrate substantial speedups, enabling scalable and transparent explainability for large-scale GNN models.

### Paper 16: [2505.22362]
**Title:** Directed Homophily-Aware Graph Neural Network
**Category:** cs.LG
**Score:** 0.6436
**In MiniLM top-20:** True

Graph Neural Networks (GNNs) have achieved significant success in various learning tasks on graph-structured data. Nevertheless, most GNNs struggle to generalize to heterophilic neighborhoods. Additionally, many GNNs ignore the directional nature of real-world graphs, resulting in suboptimal performance on directed graphs with asymmetric structures. In this work, we propose Directed Homophily-aware Graph Neural Network (DHGNN), a novel framework that addresses these limitations by incorporating homophily-aware and direction-sensitive components. DHGNN employs a resettable gating mechanism to adaptively modulate message contributions based on homophily levels and informativeness, and a structure-aware noise-tolerant fusion module to effectively integrate node representations from the original and reverse directions. Extensive experiments on both homophilic and heterophilic directed graph datasets demonstrate that DHGNN outperforms state-of-the-art methods in node classification and link prediction. In particular, DHGNN improves over the best baseline by up to 15.07\% in link prediction. Our analysis further shows that the gating mechanism captures directional homophily gaps and fluctuating homophily across layers, providing deeper insights into message-passing behavior on complex graph structures.

### Paper 17: [2601.21281]
**Title:** EGAM: Extended Graph Attention Model for Solving Routing Problems
**Category:** cs.LG
**Score:** 0.6345
**In MiniLM top-20:** True

Neural combinatorial optimization (NCO) solvers, implemented with graph neural networks (GNNs), have introduced new approaches for solving routing problems. Trained with reinforcement learning (RL), the state-of-the-art graph attention model (GAM) achieves near-optimal solutions without requiring expert knowledge or labeled data. In this work, we generalize the existing graph attention mechanism and propose the extended graph attention model (EGAM). Our model utilizes multi-head dot-product attention to update both node and edge embeddings, addressing the limitations of the conventional GAM, which considers only node features. We employ an autoregressive encoder-decoder architecture and train it with policy gradient algorithms that incorporate a specially designed baseline. Experiments show that EGAM matches or outperforms existing methods across various routing problems. Notably, the proposed model demonstrates exceptional performance on highly constrained problems, highlighting its efficiency in handling complex graph structures.

### Paper 18: [2503.01805]
**Title:** Depth-Width tradeoffs in Algorithmic Reasoning of Graph Tasks with Transformers
**Category:** cs.LG
**Score:** 0.6200
**In MiniLM top-20:** True

Transformers have revolutionized the field of machine learning. In particular, they can be used to solve complex algorithmic problems, including graph-based tasks. In such algorithmic tasks a key question is what is the minimal size of a transformer that can implement the task. Recent work has begun to explore this problem for graph-based tasks, showing that for sub-linear embedding dimension (i.e., model width) logarithmic depth suffices. However, an open question, which we address here, is what happens if width is allowed to grow linearly, while depth is kept fixed. Here we analyze this setting, and provide the surprising result that with linear width, constant depth suffices for solving a host of graph-based problems. This suggests that a moderate increase in width can allow much shallower models, which are advantageous in terms of inference and train time. For other problems, we show that quadratic width is required. Our results demonstrate the complex and intriguing landscape of transformer implementations of graph-based algorithms. We empirically investigate these trade-offs between the relative powers of depth and width and find tasks where wider models have the same accuracy as deep models, while having much faster train and inference time due to parallelizable hardware.

### Paper 19 [DIVERGENT]: [2508.02600]
**Title:** Adaptive Riemannian Graph Neural Networks
**Category:** cs.LG
**Score:** 0.6192
**In MiniLM top-20:** False

Graph data often exhibits complex geometric heterogeneity, where structures with varying local curvature, such as tree-like hierarchies and dense communities, coexist within a single network. Existing geometric GNNs, which embed graphs into single fixed-curvature manifolds or discrete product spaces, struggle to capture this diversity. We introduce Adaptive Riemannian Graph Neural Networks (ARGNN), a novel framework that learns a continuous and anisotropic Riemannian metric tensor field over the graph. It allows each node to determine its optimal local geometry, enabling the model to fluidly adapt to the graph's structural landscape. Our core innovation is an efficient parameterization of the node-wise metric tensor, specializing to a learnable diagonal form that captures directional geometric information while maintaining computational tractability. To ensure geometric regularity and stable training, we integrate a Ricci flow-inspired regularization that smooths the learned manifold. Theoretically, we establish the rigorous geometric evolution convergence guarantee for ARGNN and provide a continuous generalization that unifies prior fixed or mixed-curvature GNNs. Empirically, our method demonstrates superior performance on both homophilic and heterophilic benchmark datasets with the ability to capture diverse structures adaptively. Moreover, the learned geometries both offer interpretable insights into the underlying graph structure and empirically corroborate our theoretical analysis.

### Paper 20 [DIVERGENT]: [2601.05391]
**Title:** DynaSTy: A Framework for SpatioTemporal Node Attribute Prediction in Dynamic Graphs
**Category:** cs.LG
**Score:** 0.6058
**In MiniLM top-20:** False

Accurate multistep forecasting of node-level attributes on dynamic graphs is critical for applications ranging from financial trust networks to biological networks. Existing spatiotemporal graph neural networks typically assume a static adjacency matrix. In this work, we propose an end-to-end dynamic edge-biased spatiotemporal model that ingests a multi-dimensional timeseries of node attributes and a timeseries of adjacency matrices, to predict multiple future steps of node attributes. At each time step, our transformer-based model injects the given adjacency as an adaptable attention bias, allowing the model to focus on relevant neighbors as the graph evolves. We further deploy a masked node-time pretraining objective that primes the encoder to reconstruct missing features, and train with scheduled sampling and a horizon-weighted loss to mitigate compounding error over long horizons. Unlike prior work, our model accommodates dynamic graphs that vary across input samples, enabling forecasting in multi-system settings such as brain networks across different subjects, financial systems in different contexts, or evolving social systems. Empirical results demonstrate that our method consistently outperforms strong baselines on Root Mean Squared Error (RMSE) and Mean Absolute Error (MAE).

---

## Review Instructions

You are reviewing the top-20 recommendations from qwen3 for the profile "Graph neural networks".
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
