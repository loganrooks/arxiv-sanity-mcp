# P3: Quantum Computing / Quantum ML (Narrow breadth) -- Strategy Comparison Review

## Seeds

1. **Polynomial-Time Classical Simulation of Noisy Quantum Circuits** (2411.02535) -- Classical simulation of noisy quantum circuits with fault-tolerant gates
2. **Hybrid Quantum Neural Networks with Amplitude Encoding** (2501.15828) -- Hybrid QNN for recovery rate predictions
3. **Random-Matrix-Induced Simplicity Bias in VQCs** (2601.01877) -- Theoretical analysis of over-parameterized variational quantum circuits
4. **Impact of Circuit Depth vs Qubit Count on VQCs** (2601.11937) -- Variational quantum classifiers for Higgs boson detection
5. **Variational Quantum Circuit-Based RL** (2601.18811) -- VQC for dynamic portfolio optimization

The seeds define a narrow, specialized interest: variational quantum circuits and quantum ML, with applications spanning classification, RL, and financial optimization. The presence of a classical simulation paper (seed 1) and a portfolio optimization paper (seed 5) creates some internal heterogeneity, but the core is VQC-based quantum machine learning.

---

## Part 1: Per-Strategy Paper Assessment

### Centroid (20 papers)

1. **Shallow-circuit Supervised Learning on a Quantum Processor** (2601.03235) -- Directly relevant: supervised learning on quantum hardware. Core quantum ML.
2. **RL for Adaptive Composition of Quantum Circuit Optimisation** (2601.21629) -- Directly relevant: using RL to optimize quantum circuits. Bridges RL seed with circuit optimization.
3. **Variational decision diagrams for quantum-inspired ML** (2502.04271) -- Relevant: quantum-inspired ML using variational methods. Slight shift to "quantum-inspired" rather than quantum-native.
4. **Enhancing Expressivity of QNNs via SWAP test** (2506.16938) -- Directly relevant: improving quantum neural network architectures.
5. **Superpositional Gradient Descent** (2511.01918) -- Relevant: quantum principles for model training. Quantum-inspired optimization.
6. **Probabilistic Computers for Neural Quantum States** (2512.24558) -- Relevant: probabilistic computing for quantum state representation. Adjacent to quantum ML.
7. **Role of Quantum in Hybrid Quantum-Classical NNs** (2601.04732) -- Directly relevant: realistic assessment of hybrid QNNs. Meta-level analysis of the field.
8. **Taming Barren Plateaus in Parameterized Quantum Circuits** (2511.13408) -- Directly relevant: fundamental training challenge for VQCs. Core topic.
9. **QuFeX: Quantum feature extraction module** (2501.13165) -- Directly relevant: quantum feature extraction for deep NNs.
10. **Spectral Bias in Variational Quantum ML** (2506.22555) -- Directly relevant: analyzing learning bias in VQC-based ML.
11. **Experimental robustness benchmarking of QNNs** (2505.16714) -- Directly relevant: benchmarking QNNs on real hardware. Practical angle.
12. **Entanglement-Efficient Distribution of Quantum Circuits** (2507.16036) -- Relevant but shifted: distributed quantum computing, not ML. Circuit-level concern that relates to scaling.
13. **RL for Quantum Technology** (2601.18953) -- Relevant: RL applied to quantum systems broadly. Matches seed 5's RL angle.
14. **Quantum-Inspired Episode Selection for Monte Carlo RL** (2601.17570) -- Partially relevant: quantum-inspired RL, but the quantum part is QUBO optimization, not quantum hardware or circuits.
15. **Assessing Superposition-Targeted Coverage Criteria for QNNs** (2411.02450) -- Relevant: testing/coverage for QNNs. Software engineering perspective on QNNs.
16. **Robustness of quantum algorithms** (2509.08481) -- Relevant: fidelity bounds for quantum algorithms. Circuit reliability.
17. **Extended parameter shift rules for parameterized quantum circuits** (2508.08802) -- Directly relevant: gradient computation for PQCs. Core VQC training methodology.
18. **Quantum Approximate Optimization Algorithm for Test Case Optimization** (2312.15547) -- Weakly relevant: QAOA application to software testing. Uses quantum optimization but domain is software engineering.
19. **Interpolation-based coordinate descent for PQCs** (2503.04620) -- Directly relevant: parameter optimization for parameterized quantum circuits.
20. **Learning to Decode in Parallel: Neural Network for Quantum Error Correction** (2601.09921) -- Relevant: neural networks for quantum error correction. Connects ML and quantum, but from the error-correction side rather than ML-application side.

**Centroid assessment:** Very strong set for this narrow topic. Papers 1-11 are solidly in quantum ML / VQC territory. Papers 12-20 fan out into related areas (distributed quantum computing, quantum error correction, QAOA applications) but remain within the quantum computing orbit. The centroid works well for narrow interests because there is less averaging-induced drift -- all seeds point in roughly the same direction.

### kNN Per Seed (20 papers)

1. **Role of Quantum in Hybrid Quantum-Classical NNs** (2601.04732) -- Directly relevant (also in centroid).
2. **RL for Adaptive Composition of Quantum Circuit Optimisation** (2601.21629) -- Directly relevant (also in centroid).
3. **RL for Quantum Technology** (2601.18953) -- Relevant (also in centroid).
4. **Quantum-Inspired Episode Selection for RL** (2601.17570) -- Partially relevant (also in centroid).
5. **QuFeX: Quantum feature extraction** (2501.13165) -- Directly relevant (also in centroid).
6. **Quantum-Driven Evolutionary Framework for Portfolio Optimization** (2601.11029) -- **kNN-unique.** Relevant to seed 5 (portfolio optimization with quantum methods). Financial optimization angle, not QML per se.
7. **End-to-End Portfolio Optimization with Quantum Annealing** (2504.08843) -- **kNN-unique.** Relevant to seed 5. Quantum annealing for finance. Again finance-focused, not QML.
8. **Enhancing Expressivity of QNNs via SWAP test** (2506.16938) -- Directly relevant (also in centroid).
9. **Probabilistic Computers for Neural Quantum States** (2512.24558) -- Relevant (also in centroid).
10. **Superpositional Gradient Descent** (2511.01918) -- Relevant (also in centroid).
11. **Quantum-Enhanced Neural Contextual Bandit Algorithms** (2601.02870) -- **kNN-unique.** Relevant: QNNs for bandit/RL. Bridges quantum ML and decision-making.
12. **Assessing Superposition-Targeted Coverage Criteria** (2411.02450) -- Relevant (also in centroid).
13. **Network-Based Quantum Computing** (2601.09374) -- **kNN-unique.** Relevant to seed 1 (noisy circuits / fault tolerance). Distributed fault-tolerant computing.
14. **Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation** (2601.10964) -- **kNN-unique.** Relevant to seed 1. Pure fault-tolerant quantum computing. Not ML at all.
15. **Taming Barren Plateaus** (2511.13408) -- Directly relevant (also in centroid).
16. **Extended parameter shift rules** (2508.08802) -- Directly relevant (also in centroid).
17. **Entanglement-Efficient Distribution of Quantum Circuits** (2507.16036) -- Relevant (also in centroid).
18. **Taxonomy of Real Faults in Hybrid Quantum-Classical Architectures** (2502.08739) -- **kNN-unique.** Relevant: fault taxonomy for hybrid quantum systems. Software engineering perspective.
19. **Spectral Bias in Variational Quantum ML** (2506.22555) -- Directly relevant (also in centroid).
20. **Quantum Computing for Power Electronics** (2507.02577) -- **kNN-unique.** Weakly relevant: quantum computing applied to power electronics. Application domain far from ML or the seeds' concerns.

**kNN assessment:** For this narrow profile, kNN has much higher overlap with centroid (13 shared papers out of 20) compared to P1 (5 shared). This makes sense: when all seeds point in similar directions, per-seed neighborhoods overlap substantially. The 7 kNN-unique papers split into: 2 finance/portfolio papers (from seed 5), 2 fault-tolerant computing papers (from seed 1), and 3 miscellaneous. The finance papers are relevant to seed 5 but not to the overall QML interest. The fault-tolerance papers are relevant to seed 1 but not QML. The kNN-vs-centroid divergence is smaller but follows the same pattern: seed-specific papers that do not serve the overall interest.

### MMR (20 papers)

1. **Shallow-circuit Supervised Learning** (2601.03235) -- Same as centroid #1. Directly relevant.
2. **Variational decision diagrams** (2502.04271) -- Same as centroid #3. Relevant.
3. **Taming Barren Plateaus** (2511.13408) -- Same as centroid #8. Directly relevant.
4. **RL for Quantum Circuit Optimisation** (2601.21629) -- Same as centroid #2. Directly relevant.
5. **Role of Quantum in Hybrid NNs** (2601.04732) -- Same as centroid #7. Directly relevant.
6. **Entanglement-Efficient Distribution** (2507.16036) -- Same as centroid #12. Relevant.
7. **Robustness of quantum algorithms** (2509.08481) -- Same as centroid #16. Relevant.
8. **Superpositional Gradient Descent** (2511.01918) -- Same as centroid #5. Relevant.
9. **Extended parameter shift rules** (2508.08802) -- Same as centroid #17. Directly relevant.
10. **Probabilistic Computers for Neural Quantum States** (2512.24558) -- Same as centroid #6. Relevant.
11. **Experimental robustness benchmarking of QNNs** (2505.16714) -- Same as centroid #11. Directly relevant.
12. **Projection Coefficients Estimation in CV Quantum Circuits** (2504.16246) -- **MMR-unique.** Marginally relevant: continuous-variable quantum circuits, but focused on numerical analysis of projection coefficients, not ML.
13. **Enhancing Expressivity of QNNs** (2506.16938) -- Same as centroid #4. Directly relevant.
14. **Agent-Q: LLMs for Quantum Circuit Generation** (2504.11109) -- **MMR-unique.** Interesting: using LLMs to generate and optimize quantum circuits. Novel intersection of LLMs and quantum computing.
15. **GNN-Based Predictor for Optimal Quantum Hardware Selection** (2507.19093) -- **MMR-unique.** Relevant: ML for quantum hardware selection. ML supporting quantum, not quantum ML per se, but useful.
16. **Bias-Aware BP Decoding of Quantum Codes** (2601.07240) -- **MMR-unique.** Marginally relevant: quantum error correction decoding. Related to seed 1 (noisy circuits) but not ML-focused.
17. **Spectral Bias in Variational Quantum ML** (2506.22555) -- Same as centroid #10. Directly relevant.
18. **Continual Quantum Architecture Search** (2601.06392) -- **MMR-unique.** Relevant: automated search for quantum circuit architectures. Connects architecture search and quantum ML.
19. **QAOA for Test Case Optimization** (2312.15547) -- Same as centroid #18. Weakly relevant.
20. **Adversarial quantum channel discrimination** (2506.03060) -- **MMR-unique.** Weakly relevant: quantum information theory, not ML. Adversarial framing is interesting but domain is quantum channels.

**MMR assessment:** MMR retains 14 of centroid's 20, swapping 6. Of the 6 MMR-unique papers: Agent-Q (LLMs for quantum circuits) and Continual QAS (quantum architecture search) are genuinely interesting additions that bring different perspectives. GNN for hardware selection is useful but peripheral. The other three (projection coefficients, BP decoding, adversarial channels) are quantum computing papers without ML relevance. The centroid papers that were dropped include two core QML papers (QuFeX, Assessing Coverage) and two methodology papers (interpolation-based coordinate descent, neural decoder for QEC). Net swap quality is mixed: MMR trades two solid QML papers for two novel-angle papers and four peripherals.

---

## Part 2: Strategy Comparison

### Centroid vs kNN

For this narrow profile, the difference is smaller (13/20 overlap vs 5/20 for P1). The 7 kNN-unique papers are clearly seed-specific: finance papers from seed 5, fault-tolerance papers from seed 1. These are thematically coherent with their source seeds but dilute the QML focus that the centroid maintains. The centroid does a better job of representing the *intersection* of the seeds' interests (variational quantum circuits for ML), while kNN preserves the *union* (including finance applications and pure fault-tolerance theory).

### Centroid vs MMR

MMR's 6 swaps introduce two genuinely interesting papers (Agent-Q, Continual QAS) that represent novel approaches (LLMs for quantum circuits, automated architecture search) not present in the centroid. These are legitimate diversity gains -- they are not just noise. However, the cost includes losing QuFeX and Assessing Coverage, both core QML papers. The net is roughly neutral in relevance but MMR adds topical breadth.

### kNN Unique Papers

Of the 7 kNN-unique papers: Quantum-Enhanced Contextual Bandits is genuinely interesting for the QML interest. The two portfolio optimization papers are relevant only to seed 5. The two fault-tolerance papers are relevant only to seed 1. The fault taxonomy paper is marginally useful. The power electronics paper is noise. Only 1 out of 7 is a genuine find.

---

## Part 3: Set-Level Assessment

### Centroid
- **Coherence:** High. Almost all papers relate to variational quantum circuits, quantum ML, or quantum computing infrastructure. The set reads as a focused literature review.
- **Diversity:** Moderate. Covers QNN expressivity, training challenges (barren plateaus), hardware benchmarking, quantum-inspired methods, circuit optimization. Missing: quantum finance applications, LLM-quantum intersection, quantum architecture search.
- **Researcher satisfaction:** High. A quantum ML researcher would find this a strong starting set. The weakest papers (QAOA for test cases, coordinate descent for PQCs) are still within the quantum computing space.

### kNN Per Seed
- **Coherence:** Moderate. Higher than P1's kNN set because the seeds are more similar to each other. But the finance papers and pure fault-tolerance papers break the QML focus.
- **Diversity:** Higher than centroid but in an unhelpful way. Adding portfolio optimization and fault-tolerant computing does not serve a QML researcher.
- **Researcher satisfaction:** Moderate. A QML researcher would recognize most papers as relevant but find the finance and fault-tolerance papers distracting.

### MMR
- **Coherence:** Comparable to centroid. Slightly more scattered due to adversarial channel discrimination and BP decoding additions.
- **Diversity:** Slightly better than centroid. Agent-Q and Continual QAS add genuinely novel perspectives.
- **Researcher satisfaction:** Comparable to centroid, possibly slightly better due to the two novel-angle papers.

---

## Part 4: Emergent Observations

1. **Narrow profiles compress the strategy differences.** With all seeds pointing in similar directions, the centroid, kNN, and MMR sets converge (13/20 overlap for kNN, 14/20 for MMR). The retrieval strategy matters less when the interest is well-defined and homogeneous. This is consistent with the quantitative finding that kNN performs worst on narrow profiles.

2. **kNN's seed-specific pulls are more visible on narrow profiles.** The portfolio optimization papers (from seed 5) and fault-tolerance papers (from seed 1) are clearly "one seed talking." Because the profile is narrow, these tangential papers stand out more sharply against the coherent quantum ML core.

3. **MMR's best finds here (Agent-Q, Continual QAS) represent genuine topical diversity.** Unlike P1 where MMR's swaps were roughly neutral, here two of the swaps introduce papers that approach quantum circuits from a different angle (using LLMs, using architecture search). This is more valuable on a narrow profile where the centroid set risks being too homogeneous.

4. **The centroid handles narrow profiles well.** With less internal heterogeneity among seeds, the averaging effect of the centroid does not dilute signals. The centroid produces a focused, coherent set. The main risk is that it may be too focused -- missing novel angles that MMR catches.

---

## Part 5: Metric Divergence

- **Does kNN FEEL catastrophic for P3?** Less catastrophic than for P1, because the overlap is higher (13/20). The 7 kNN-unique papers are mostly off-topic (finance, fault-tolerance, power electronics), which drags quality down. But the shared core of 13 papers means the set is still majority-good. "Diluted" is a better descriptor than "catastrophic."

- **Does MMR FEEL meaningfully better for P3?** Slightly more so than for P1. Agent-Q and Continual QAS are genuinely novel papers that a QML researcher might appreciate. The diversity gain is small but qualitatively meaningful -- these papers represent different methodological approaches (LLMs for circuits, automated search) rather than just different application domains.
