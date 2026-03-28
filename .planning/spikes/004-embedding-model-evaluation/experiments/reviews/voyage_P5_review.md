# Single-Strategy Characterization Review

**Model:** voyage
**Profile:** Graph neural networks (P5)
**Depth:** full
**Overlap with MiniLM:** 17/20 shared, 3 unique to voyage

## Seed Papers
  - [2503.06614] Using Subgraph GNNs for Node Classification:an Overlooked Potential Approach (cs.LG)
  - [2411.12732] Benchmarking Positional Encodings for GNNs and Graph Transformers (cs.LG)
  - [2506.22727] Convergent Privacy Framework for Multi-layer GNNs through Contractive Message Passing (cs.CR)
  - [2510.15583] Attn-JGNN: Attention Enhanced Join-Graph Neural Networks (cs.LG)
  - [2512.24901] Spectral Graph Neural Networks for Cognitive Task Classification in fMRI Connectomes (cs.LG)

## voyage Top-20 Recommendations

(Papers 1-20 as listed in template above)

---

## Assessment

**Limitation note:** Voyage-4 had 160/2000 papers fail to embed (8% failure rate due to API rate limiting). The effective retrieval pool is approximately 1840 papers. GNN papers are well-represented in ML venues, so the failure rate is unlikely to introduce systematic bias for this profile.

### 1. Per-Paper Assessment

**Paper 1 [2503.06614] SubGND** -- Direct (seed paper). Subgraph GNNs for node classification.

**Paper 2 [2205.07266] Representation Bottleneck** -- Direct. Discovers and addresses GNN representation bottlenecks via graph rewiring. Directly relevant to understanding GNN limitations, complementing the seeds' focus on architectural improvements.

**Paper 3 [2411.12732] Benchmarking PE** -- Direct (seed paper). Positional encodings benchmark for GNNs.

**Paper 4 [2512.24901] SpectralBrainGNN** -- Direct (seed paper). Spectral GNNs for fMRI classification.

**Paper 5 [2601.04807] Parallelizing Explainability** -- Adjacent. Graph partitioning for scalable GNN explainability. Addresses a practical concern (explainability at scale) rather than a core GNN methodology issue.

**Paper 6 [2506.13911] HEGNN** -- Direct. Hierarchical ego GNNs with expressiveness analysis via logic characterization. Extends the subgraph GNN approach from seed [2503.06614] to hierarchical individualization. Strong theoretical contribution.

**Paper 7 [2601.02451] mHC-GNN** -- Direct. Manifold-constrained hyper-connections for deep GNNs. Directly addresses over-smoothing and WL-expressiveness bounds, two central GNN challenges.

**Paper 8 [2510.15583] Attn-JGNN** -- Direct (seed paper). Attention-enhanced join-graph neural networks.

**Paper 9 [2505.22362] DHGNN** -- Direct. Directed homophily-aware GNN. Addresses heterophilic and directed graph settings, extending the standard GNN framework.

**Paper 10 [2410.01308] WL Tests Revisited** -- Direct. Theoretical analysis of WL test limitations for GNN expressivity. A foundational paper directly relevant to the expressiveness questions raised by the seed papers.

**Paper 11 [2601.01123] HISTOGRAPH** -- Direct. Historical activation pooling for GNNs. Addresses the underutilization of intermediate layer features, complementing the deep GNN work in mHC-GNN.

**Paper 12 [2601.17774] CondenseGraph** -- Adjacent. Communication-efficient distributed GNN training via graph condensation. More about training infrastructure than GNN architecture, but relevant to scaling GNNs.

**Paper 13 [2508.02600] ARGNN** -- DIVERGENT. Direct. Adaptive Riemannian GNNs with learned metric tensor fields. A theoretically grounded approach to geometric heterogeneity in graphs, allowing each node to determine its local geometry. This is a genuinely interesting divergent signal -- it represents a geometric deep learning perspective on GNNs that goes beyond the standard message-passing paradigm. The Ricci flow regularization and convergence guarantees add theoretical depth. A GNN researcher should be aware of this direction. Discoverable via geometric deep learning literature, but the Riemannian geometry framing may not surface in standard GNN searches.

**Paper 14 [2506.22727] CARIBOU** -- Direct (seed paper). Privacy framework for multi-layer GNNs.

**Paper 15 [2601.17130] MI Risk in GNNs** -- Direct. Membership inference risk analysis for GNNs. Extends the privacy theme from seed [2506.22727] to membership inference attacks.

**Paper 16 [2601.21281] EGAM** -- Adjacent. Graph attention model for routing problems. More about neural combinatorial optimization than GNN methodology, but uses GNN architecture.

**Paper 17 [2601.14536] engGNN** -- Adjacent. Dual-graph GNN for omics-based disease classification. An application paper that uses GNN methodology for bioinformatics. The dual-graph (external + data-driven) approach is methodologically interesting.

**Paper 18 [2601.06381] Hierarchical Pooling for Cancer** -- DIVERGENT. Adjacent. GNNs with hierarchical pooling for RNA-seq cancer classification. Another GNN application in biomedicine. The hierarchical pooling and explainability via saliency methods are relevant to GNN methodology, but the paper's primary contribution is in the application domain. Discoverable via GNN applications in bioinformatics.

**Paper 19 [2601.04517] Diffusion Geometry Approximation** -- DIVERGENT. Direct/Provocative. Bridges distance and spectral positional encodings via anchor-based diffusion geometry. Directly connects to seed [2411.12732] on positional encodings for GNNs. This is a theoretically rich paper that unifies two PE families. A strong divergent signal -- the mathematical connections between PE approaches should interest anyone working on GNN expressiveness. Discoverable via the positional encoding literature, though the information-theory venue (cs.IT) may make it less visible.

**Paper 20 [2601.19745] GraphDLG** -- Direct. Deep leakage from gradients in federated graph learning. Extends the privacy theme from seed [2506.22727] to federated settings.

### 2. Set-Level Assessment

**Landscape coverage:** The set provides solid coverage of the GNN research landscape:
- Expressiveness theory: WL tests, hierarchical ego GNNs, logical characterization
- Architecture innovations: subgraph GNNs, hyper-connections, directed/heterophilic handling, Riemannian geometry
- Positional encodings: benchmarking, diffusion geometry bridge
- Over-smoothing: deep GNN methods (mHC-GNN, HISTOGRAPH)
- Privacy and security: differential privacy, membership inference, federated learning
- Applications: neuroscience, bioinformatics, combinatorial optimization, distributed training
- Scalability: parallel explainability, graph condensation for distributed training

**What is conspicuously absent:**
- Graph transformers (despite being mentioned in seed [2411.12732], no dedicated graph transformer papers appear)
- Dynamic/temporal graphs
- Heterogeneous graph neural networks (despite the heterophily papers)
- Graph generation and generative models
- Link prediction methodology (present only in passing)

**Divergent paper character:** The 3 divergent papers represent two distinct signals: (a) geometric/theoretical deepening of GNN methodology (ARGNN, diffusion geometry), and (b) biomedical application (hierarchical pooling for cancer). The former is higher-quality divergence; the latter is more of a domain-specific application.

### 3. Emergent Observations

**Signal character:** Voyage's divergent papers lean toward theoretical/geometric extensions of GNN methodology. ARGNN (Riemannian geometry) and the diffusion geometry bridge both bring mathematical sophistication that extends the seeds' interests. This suggests Voyage may have a slight tendency to surface theoretically-oriented papers in the GNN space.

**Divergence quality:** Largely coherent and valuable. ARGNN and the PE bridge paper are high-quality contributions that a GNN researcher would benefit from knowing. The cancer classification paper is more peripheral.

**Productive provocations:** Paper 19 (diffusion geometry bridge) is the most productive provocation -- it suggests that the commonly opposed "distance-based" and "spectral" PE approaches are in fact approximations of the same underlying geometric structure. This could reshape how researchers think about positional encoding design.

### 4. Absent Researcher Note

To properly assess this recommendation set, I would need to know:
- Whether the researcher is focused on GNN theory (expressiveness, WL hierarchy) or applications (neuroscience, bioinformatics)
- Their interest in privacy/security aspects of GNNs vs. pure methodology
- Whether they work on graph transformers (a conspicuous gap in this set)
- Whether they are interested in geometric deep learning (the ARGNN paper would be central vs. peripheral depending on this)

### 5. Metric Divergence Flags

The 17/20 overlap (J@20 = ~0.74) indicates high agreement with moderate divergence. The qualitative review is consistent: the 3 divergent papers are relevant but represent slightly different emphases (geometric theory, PE theory, biomedical application) rather than noise. No qualitative-quantitative contradiction. The set is well-characterized as a "GNN methodology and theory" recommendation set with light application coverage.
