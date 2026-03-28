# Single-Strategy Characterization Review

**Model:** voyage
**Profile:** Quantum computing / quantum ML (P3)
**Depth:** full
**Overlap with MiniLM:** 14/20 shared, 6 unique to voyage

## Seed Papers
  - [2601.18710] Analyzing Images of Blood Cells with Quantum Machine Learning Methods: Equilibrium Propagation and Variational Quantum Circuits to Detect Acute Myeloid Leukemia (cs.ET)
  - [2506.22555] Spectral Bias in Variational Quantum Machine Learning (quant-ph)
  - [2601.11937] Impact of Circuit Depth versus Qubit Count on Variational Quantum Classifiers for Higgs Boson Signal Detection (quant-ph)
  - [2209.07714] Variational quantum algorithm for measurement extraction from the Navier-Stokes, Einstein, Maxwell, B-type, Lin-Tsien, Camassa-Holm, DSW, H-S, KdV-B, non-homogeneous KdV, generalized KdV, KdV, translational KdV, sKdV, B-L and Airy equations (quant-ph)
  - [2507.16036] Entanglement-Efficient Distribution of Quantum Circuits over Large-Scale Quantum Networks (quant-ph)

## voyage Top-20 Recommendations

(Papers 1-20 as listed in template above)

---

## Assessment

**Limitation note:** Voyage-4 had 160/2000 papers fail to embed (8% failure rate due to API rate limiting). The effective retrieval pool is approximately 1840 papers. Given that quantum computing/quantum ML papers are a minority topic in a general CS/ML corpus, the 8% failure rate could disproportionately affect this niche profile if quantum papers happened to cluster among the failed embeddings.

### 1. Per-Paper Assessment

**Paper 1 [2601.11937] VQC for Higgs Boson** -- Direct (seed paper). Variational quantum classifiers for particle physics.

**Paper 2 [2506.22555] Spectral Bias in VQM** -- Direct (seed paper). Spectral bias in parametrized quantum circuits.

**Paper 3 [2507.16036] Entanglement-Efficient Distribution** -- Direct (seed paper). Quantum circuit distribution over large-scale networks.

**Paper 4 [2209.07714] Variational quantum PDE solver** -- Direct (seed paper). VQA for solving PDEs.

**Paper 5 [2601.01877] Simplicity Bias in VQCs** -- DIVERGENT. Direct. This paper addresses a fundamental question about why overparameterized variational quantum circuits exhibit poor trainability and generalization -- directly extending the spectral bias and barren plateau concerns from seed [2506.22555]. The random matrix theory approach is a genuine theoretical contribution to understanding VQC limitations. This is a high-quality divergent signal. A quantum ML researcher would want to read this. Discoverable via the barren plateaus literature, but the random matrix framing may not surface via standard keyword search.

**Paper 6 [2508.15267] Optimizing DQC Compilation** -- DIVERGENT. Adjacent. Compilation for distributed quantum computing with heterogeneous QPUs. Connects to seed [2507.16036] on distributed quantum computing but shifts from circuit partitioning theory to practical compilation. A useful complement for researchers working on DQC, though less directly about quantum ML. Discoverable via DQC compilation literature.

**Paper 7 [2507.01726] Flow-VQE** -- Direct. Generative flow models for warm-starting VQE optimization. Directly extends the variational quantum algorithm theme from seeds [2209.07714] and [2506.22555].

**Paper 8 [2601.14226] DL for Quantum Error Mitigation** -- Adjacent. Deep learning applied to quantum error mitigation. Not quantum ML per se (it is classical ML applied to quantum computing problems), but relevant to the practical deployment of quantum circuits.

**Paper 9 [2501.15828] Hybrid QNN for Recovery Rates** -- Adjacent. Quantum ML applied to financial prediction. Extends the application-oriented QML theme from seed [2601.18710] to a different domain (finance vs. medical imaging).

**Paper 10 [2601.02818] QLSTMA for Reservoir Prediction** -- DIVERGENT. Adjacent. Quantum-enhanced LSTM for oilfield permeability prediction. Another domain application of quantum-classical hybrid neural networks. Thematically consistent with the application-oriented seeds but specific to petroleum engineering. Marginally discoverable -- a QML researcher would need to specifically look in geoscience applications.

**Paper 11 [2601.01777] Quantum Computing for Unit Commitment** -- Adjacent. Survey of quantum computing for power system optimization. More quantum optimization than quantum ML, but the variational algorithm coverage overlaps with the profile.

**Paper 12 [2601.02064] Cutting Quantum Circuits Beyond Qubits** -- DIVERGENT. Adjacent. Circuit cutting extended to mixed-dimensional qudit registers. Connects to distributed quantum computing (seed [2507.16036]) but at a lower level -- hardware fragmentation rather than network-level distribution. A specialized contribution. Not directly about ML.

**Paper 13 [2601.14024] Hybrid Quantum-Classical Benders** -- Adjacent. Quantum annealing for MILP optimization via Benders decomposition. Quantum optimization rather than quantum ML, but shares the hybrid quantum-classical methodology.

**Paper 14 [2601.00656] Quantum Protein Simulation** -- DIVERGENT. Adjacent. VQE for protein fragment electronic structure. A quantum chemistry application using the same variational quantum algorithms as the seeds. The connection is methodological (VQE/VQA) rather than thematic (biology vs. the seeds' physics/engineering applications). Discoverable via quantum chemistry literature.

**Paper 15 [2504.11109] Agent-Q** -- Adjacent. LLM fine-tuning for quantum circuit generation. An unusual intersection of LLMs and quantum computing. The quantum circuit generation connects to the profile, but the LLM methodology is orthogonal.

**Paper 16 [2601.06332] Bipartitioning for DQC** -- DIVERGENT. Adjacent. Graph partitioning for distributed measurement-based quantum computing. Directly extends seed [2507.16036]'s distributed quantum computing theme. Technical and specialized.

**Paper 17 [2601.18198] Quantum Message Passing GNN** -- Adjacent. Quantum-enhanced GNNs for wireless communications. Intersects quantum computing with GNNs and wireless systems. The PQC methodology connects to the profile.

**Paper 18 [2601.05250] QNeRF** -- Adjacent. Quantum-classical hybrid model for novel-view synthesis. An application of parameterized quantum circuits to computer vision. Novel application domain but methodologically connected.

**Paper 19 [2601.09374] Network-Based Quantum Computing** -- Adjacent. Distributed fault-tolerant quantum computing architecture. Extends the distributed QC theme from seed [2507.16036].

**Paper 20 [2601.18811] QRL for Portfolio Optimization** -- Adjacent. Variational quantum circuits for RL-based portfolio optimization. Bridges quantum computing, RL, and finance.

### 2. Set-Level Assessment

**Landscape coverage:** This set maps a broad quantum computing landscape rather than narrowly focusing on quantum ML:
- Variational quantum algorithms: VQC, VQE, VQA for various tasks (multiple papers)
- Distributed quantum computing: circuit partitioning, compilation, network architecture (3 papers)
- Quantum ML applications: medical imaging (seed), finance, petroleum engineering, wireless, CV
- Theoretical foundations: barren plateaus, spectral bias, overparameterization
- Quantum error mitigation and hardware-oriented work

**Coverage character:** The set is notably broad -- it covers quantum computing more generally, with quantum ML as one thread among several. This reflects the seeds themselves, which span QML (variational classifiers, spectral bias) and quantum computing infrastructure (distributed circuits, PDE solvers).

**What is conspicuously absent:**
- Quantum kernel methods (a major QML subfield)
- Quantum advantage/separability results for ML tasks
- Quantum data encoding strategies beyond amplitude/angle encoding
- Quantum generative models (QGANs, quantum Boltzmann machines)
- Critical assessments of QML utility (the "is QML useful?" debate)

**Divergent paper character:** The 6 divergent papers divide into two clusters: (a) distributed quantum computing papers (compilation, circuit cutting, bipartitioning) that extend seed [2507.16036], and (b) domain applications of hybrid quantum-classical models (oilfield prediction, protein simulation, VQC theory). The DQC cluster is coherent but represents Voyage pulling in more quantum computing infrastructure than MiniLM. The application cluster represents broader domain coverage.

### 3. Emergent Observations

**Signal character:** Voyage appears to retrieve more broadly within quantum computing than MiniLM, pulling in distributed QC infrastructure and diverse domain applications. With 6 unique papers (30% divergence), Voyage shows meaningful differentiation on this profile.

**Divergence quality:** Coherent and mostly valuable. The simplicity bias paper (Paper 5) is a genuinely important theoretical contribution that a QML researcher should know. The DQC papers are relevant to a researcher working on distributed quantum circuits. The domain application papers are more peripheral but represent real use-cases.

**Productive provocations:** Paper 5 (simplicity bias in VQCs) is the strongest provocation -- it offers a unified theoretical explanation for barren plateaus and expressivity collapse that challenges the assumption that more parameters always help. This has direct implications for the design of variational quantum ML models.

### 4. Absent Researcher Note

To properly assess this recommendation set, I would need to know:
- Whether the researcher is primarily a QML researcher or a quantum computing systems researcher (the set spans both)
- Their interest level in domain applications (medical, financial, petroleum) vs. methodology
- Whether they work on NISQ-era hardware or are interested in fault-tolerant quantum computing
- Their familiarity with classical ML -- several papers bridge quantum and classical methods

### 5. Metric Divergence Flags

The 14/20 overlap (J@20 = ~0.58) indicates moderate divergence, and the qualitative review is consistent with this. The 6 divergent papers are spread across related but non-identical subfields (DQC infrastructure, domain applications, VQC theory), suggesting that Voyage has a slightly wider retrieval radius in the quantum computing space. This profile is inherently broad (the seeds span QML and distributed QC), so moderate divergence is expected and not concerning. No contradictions between qualitative and quantitative assessments.
