# W5.4 Final Validation: P3 -- Quantum Computing / Quantum ML (Narrow Breadth)

## Profile Summary

**Seed papers** define a researcher working at the intersection of quantum computing and machine learning, with specific interests in: classical simulation of noisy quantum circuits, hybrid quantum neural networks for finance, variational quantum circuit trainability (over-parameterization, simplicity bias), variational quantum classifiers for HEP, and variational quantum circuit-based reinforcement learning for portfolio optimization. The profile is narrow and technical, sitting squarely within the quantum ML subfield with applications in finance and physics. Categories center on quant-ph with secondary cs.LG.

---

## Part 1: Per-View Paper Assessment

### View 1: Similar Ideas (MiniLM)

1. **[2601.21780] Quantum LEGO Learning** -- Highly relevant. Modular hybrid quantum-classical learning with VQCs. Same research area (hybrid QNN design), same concerns (trainability, modularity). Strong "Similar Ideas" match.

2. **[2601.11942] Trainability-Oriented Hybrid Quantum Regression** -- Highly relevant. Directly addresses trainability of QNNs via geometric preconditioning. Same core concern as seed [2601.01877] (VQC trainability). Excellent match.

3. **[2601.18058] DiffAS for Adversarially Robust Quantum Computer Vision** -- Relevant. Quantum architecture search for adversarial robustness. Shares concerns about VQC design and noise sensitivity. Good placement.

4. **[2601.06392] CL-QAS -- Continual Quantum Architecture Search** -- Relevant. Quantum architecture search with continual learning. Same method family (VQC design/optimization). Appropriate.

5. **[2511.01918] Superpositional Gradient Descent** -- Moderately relevant. Quantum-inspired optimization for classical model training. Tangentially connected -- uses quantum principles but applies them to classical LLM training. The "quantum" connection is metaphorical rather than literal.

6. **[2601.03235] Shallow-circuit Supervised Learning on a Quantum Processor** -- Highly relevant. Practical QML on real quantum hardware. Same community, same concerns (practical quantum advantage in ML). Excellent match.

7. **[2411.02450] Assessing Coverage Criteria for Quantum Neural Networks** -- Relevant. Testing and reliability of QNNs. Adjacent concern (testing rather than training), same artifacts (QNNs). Good.

8. **[2601.02870] Quantum-Enhanced Neural Contextual Bandits** -- Relevant. Quantum circuits for contextual bandits (decision-making). Connects through quantum + ML, with the RL angle linking to seed [2601.18811]. Good.

9. **[2506.22555] Spectral Bias in Variational Quantum ML** -- Highly relevant. Directly studies VQC learning dynamics (spectral bias). Same core concern as seeds about VQC behavior and trainability. Excellent match.

10. **[2505.16714] Robustness Benchmarking of QNNs on Superconducting Processor** -- Relevant. Adversarial robustness of QML on real hardware. Same concerns (practical QML, hardware noise). Good.

11. **[2601.10965] Noise-Aware Quantum Architecture Search** -- Relevant. QAS accounting for hardware noise. Same concern (noise-aware VQC design). Directly connected to seed themes.

12. **[2511.10062] FAQNAS -- FLOPs-aware Hybrid QNN Architecture Search** -- Relevant. Practical QNN design with resource awareness. Same method family (quantum architecture search). Good.

13. **[2511.13408] Taming Barren Plateaus in PQCs** -- Highly relevant. Directly addresses barren plateaus -- a central concern for VQC trainability, directly connected to seed [2601.01877]. Excellent match.

14. **[2503.16342] HiQ-Lip -- Quantum-Classical Lipschitz Estimation** -- Moderately relevant. Uses quantum computing for neural network analysis. Cross-domain application of quantum methods. Reasonable but stretches the profile's core interests.

15. **[2601.14226] Deep Learning for Quantum Error Mitigation** -- Relevant. ML applied to quantum computing (error mitigation). Adjacent direction (ML for quantum rather than quantum for ML) but same community.

16. **[2601.04732] Role of Quantum in Hybrid QNNs: A Realistic Assessment** -- Highly relevant. Critical assessment of whether quantum components add value in hybrid models. Directly addresses core open questions in the field. Excellent pick.

17. **[2504.11109] Agent-Q -- LLMs for Quantum Circuit Generation** -- Moderately relevant. LLMs applied to quantum circuits. Adjacent method (LLMs, not VQCs) for quantum computing tasks. Tangentially connected.

18. **[2601.21629] RL for Quantum Circuit Optimization Passes** -- Relevant. RL applied to optimize quantum circuits. Connects to seed [2601.18811] (RL + quantum). Good cross-connection.

19. **[2504.03315] Detecting Underdetermination in PQCs** -- Relevant. Reliability analysis of parameterized quantum circuits. Same artifacts (PQCs), complementary concern (reliability). Good.

20. **[2601.08578] Quantum Computing -- Strategic Recommendations** -- Weakly relevant. Industry whitepaper on quantum computing prospects. Not a research paper in the usual sense. Outlier.

**Summary**: MiniLM performs well for P3. The top 14-15 papers are tightly relevant, sharing the same research questions about VQC design, trainability, quantum architecture search, and practical QML. The narrow profile helps MiniLM focus on genuinely similar ideas. The one clear miss is the industry whitepaper at #20. The view accurately captures "Similar Ideas" -- papers asking the same technical questions about the same artifacts.

---

### View 2: Same Vocabulary (TF-IDF)

1. **[2503.13388] Mathematical Model for Universal Digital Quantum Computer** -- Weakly relevant. Formal quantum computing theory (algebraic probability). Shares "quantum circuit" vocabulary but is theoretical computer science, not QML. Pure vocabulary match.

2. **[2510.09824] QFT Circuit for Arbitrary Qubit Connectivity** -- Weakly relevant. Quantum circuit design for QFT algorithm. Shares "quantum circuit" terms but is quantum algorithms, not ML. Vocabulary-only match.

3. **[2601.02237] Quantum AI for Cybersecurity** -- Moderately relevant. Hybrid quantum-classical models for attack analysis. Shares the "hybrid quantum-classical" vocabulary and uses QML, but the application (cybersecurity) and method style differ from the seed profile's focus.

4. **[2601.04732] Role of Quantum in Hybrid QNNs** -- (Also in MiniLM.) Highly relevant.

5. **[2601.16758] Noise Resilience for Variational Quantum Eigensolver** -- Relevant. VQA convergence guarantees under noise. Same method family (variational quantum algorithms), different application (eigensolvers vs classifiers). Good vocabulary and topical match.

6. **[2504.11109] Agent-Q** -- (Also in MiniLM.) Moderately relevant.

7. **[2503.24111] Quantum Graph Neural Networks** -- Moderately relevant. QGNNs for graph learning. Same community (quantum ML), different architecture (graph-based). Reasonable.

8. **[2508.04486] Quantum Circuit Complexity and Unsupervised ML** -- Moderately relevant. Circuit complexity for understanding topological order. Connects quantum circuits and ML but in a condensed matter context. Shared vocabulary ("quantum circuit," "machine learning") creates a match across quite different research goals.

9. **[2601.18953] Reinforcement Learning for Quantum Technology** -- Relevant. RL applied to quantum technology challenges. Directly connects RL + quantum, a seed paper theme [2601.18811]. Good.

10. **[2601.03235] Shallow-circuit Supervised Learning** -- (Also in MiniLM.) Highly relevant.

11. **[2601.00720] Quantum Approaches to Minimum Edge Multiway Cut** -- Weakly relevant. Quantum algorithms for combinatorial optimization. Shares "quantum" vocabulary but is optimization/graph theory, not ML.

12. **[2601.18058] DiffAS for Robust Quantum CV** -- (Also in MiniLM.) Relevant.

13. **[2506.02920] Quantum Data Centres** -- Not relevant. Quantum networking and entanglement distribution. Shares "quantum" vocabulary only. This is quantum communication, not quantum ML. Clear TF-IDF failure.

14. **[2601.21780] Quantum LEGO Learning** -- (Also in MiniLM.) Highly relevant.

15. **[2510.02854] C2|Q> -- Framework Bridging Classical and Quantum Software** -- Weakly relevant. Quantum software engineering tools. Shares "quantum" vocabulary but is about development environments, not ML algorithms.

16. **[2512.17918] QAISim -- Quantum Cloud Computing Simulation Toolkit** -- Weakly relevant. Cloud simulation toolkit for quantum AI. Infrastructure-level, not algorithmic research. Vocabulary match only.

17. **[2507.19093] GNN-Based Predictor for Quantum Hardware Selection** -- Moderately relevant. ML for quantum hardware selection. Adjacent concern (meta-level tool for quantum computing). Connects ML + quantum but differently from the profile's focus.

18. **[2509.14731] 1Q -- Classical and Quantum Communication Systems** -- Not relevant. Quantum communication for wireless systems. Shares "quantum" term only. Clearly irrelevant to a QML researcher.

19. **[2601.10965] Noise-Aware QAS** -- (Also in MiniLM.) Relevant.

20. **[2511.01918] Superpositional Gradient Descent** -- (Also in MiniLM.) Moderately relevant.

**Summary**: TF-IDF performs notably worse for P3 than for P1. The narrow quantum ML profile means that "quantum" is such a dominant term that TF-IDF matches on it broadly, pulling in quantum communication, quantum networking, quantum software engineering, and quantum algorithms papers that are irrelevant to a QML researcher. At least 5-6 papers (QFT circuits, minimum edge cut, quantum data centres, 1Q wireless, C2|Q> framework, QAISim) are clearly not relevant. The "Same Vocabulary" label is technically accurate -- they do share quantum vocabulary -- but the quality of recommendations is poor. For a narrow profile, shared vocabulary is an especially weak signal.

---

### View 3: Adjacent Communities (SPECTER2)

1. **[2601.06392] CL-QAS** -- (Also in MiniLM.) Relevant.

2. **[2601.21780] Quantum LEGO Learning** -- (Also in MiniLM, TF-IDF.) Highly relevant.

3. **[2511.01918] Superpositional Gradient Descent** -- (Also in MiniLM, TF-IDF.) Moderately relevant.

4. **[2506.22555] Spectral Bias in VQ ML** -- (Also in MiniLM.) Highly relevant.

5. **[2601.02870] Quantum Contextual Bandits** -- (Also in MiniLM.) Relevant.

6. **[2601.16758] VQE Noise Resilience** -- (Also in TF-IDF.) Relevant.

7. **[2511.10062] FAQNAS** -- (Also in MiniLM.) Relevant.

8. **[2405.10360] Adversarial Robustness Guarantees for Quantum Classifiers** -- Relevant. Formal robustness guarantees for quantum classifiers. Same artifacts (quantum classifiers), complementary angle (formal guarantees vs empirical benchmarks). Reasonable adjacent-community pick.

9. **[2511.13408] Taming Barren Plateaus** -- (Also in MiniLM.) Highly relevant.

10. **[2601.11942] Trainability-Oriented Hybrid Quantum Regression** -- (Also in MiniLM.) Highly relevant.

11. **[2512.23817] Quantum Error Mitigation with Attention Graph Transformers** -- Relevant. Hybrid quantum-classical framework with learned error mitigation for PDE solving. Adjacent application (PDE solving, not classification), same method family (quantum circuits + classical ML for error handling).

12. **[2601.03802] Quantum vs Classical ML for Financial Prediction** -- Relevant. Benchmarking QML vs classical for finance. Directly connects to seed paper [2501.15828] which uses QNNs for financial prediction. Good placement.

13. **[2601.02509] hdlib 2.0 -- Vector-Symbolic Architectures** -- Not relevant. Classical vector-symbolic architecture library. No quantum component. SPECTER2 has picked up a paper that happens to be in the citation neighborhood of ML architecture papers but has nothing to do with quantum computing.

14. **[2601.01589] Quantum Walks and Underdamped Langevin Dynamics** -- Moderately relevant. Quantum walks related to classical sampling algorithms. Tangential -- studies quantum-classical connections but from a theoretical dynamics perspective, not ML.

15. **[2512.10929] Noisy Quantum Learning Theory** -- Relevant. Theoretical framework for learning from noisy quantum experiments. Same concerns (noise, quantum circuits, learnability). Good.

16. **[2601.13708] GANs for Resource State Generation** -- Moderately relevant. GANs for quantum state generation. Connects ML + quantum but in the opposite direction (ML for quantum resource generation, not quantum for ML).

17. **[2501.10077] Double Descent in Quantum Kernel Methods** -- Relevant. Statistical learning theory applied to quantum kernels. Same community (QML theory), complementary angle. Good.

18. **[2511.14296] Empirical Quantum Advantage in Constrained Optimization** -- Moderately relevant. QAOA for constrained optimization. Same field (quantum algorithms) but different subarea (optimization, not ML). Tangentially connected.

19. **[2402.08606] Polynomial Separations in Trainable QML** -- Highly relevant. Formal results on expressivity-trainability tradeoffs in QNNs. Directly addresses the core theoretical question of seed [2601.01877]. Excellent pick.

20. **[2506.20355] Encodings and Ansatze in Quantum CNNs** -- Relevant. Practical PQC design choices for quantum CNNs. Same artifacts and concerns (PQC design, encoding strategies). Good.

**Summary**: SPECTER2 performs better for P3 than for P1, surfacing more genuinely distinct papers. The unique picks include some valuable finds (polynomial separations in QML, quantum vs classical benchmarking for finance, adversarial robustness guarantees for quantum classifiers, noisy quantum learning theory). However, it also includes one clear miss (hdlib -- vector-symbolic architectures with no quantum component) and some tangential picks (quantum walks, GANs for resource states). The citation-graph approach brings in papers from the broader quantum computing theory community that share citation patterns with the QML subfield. The "Adjacent Communities" label works better here than for P1, since SPECTER2 does surface QML theory and quantum algorithms papers that are genuinely adjacent.

The score compression problem persists (range 0.9475-0.9644, spread 0.0170) but is less extreme than P1, suggesting SPECTER2 has slightly more discriminative power in the quantum ML space.

---

## Part 2: View Characterization

### Similar Ideas (MiniLM)

- **Label accuracy**: Accurate. MiniLM identifies papers sharing the same technical ideas about VQC trainability, quantum architecture search, and hybrid QNN design.
- **Distinctiveness**: High. MiniLM's unique picks (barren plateaus, coverage criteria for QNNs, RL for circuit optimization, QNN robustness benchmarking) are tightly focused on the profile's specific research questions.
- **What it finds that others don't**: MiniLM uniquely surfaces practical QML papers about circuit testing, error mitigation, and QNN reliability -- the "how to make VQCs work" cluster that is the profile's core concern.

### Same Vocabulary (TF-IDF)

- **Label accuracy**: Technically accurate but problematic. For a narrow profile, "Same Vocabulary" means "uses the word quantum," which matches quantum communication, quantum networking, quantum software tools, and other irrelevant subfields.
- **Distinctiveness**: High by count (12 unique papers) but low by quality. Many unique papers are irrelevant (quantum data centres, 1Q wireless, minimum edge cut, C2|Q> framework).
- **What it finds that others don't**: TF-IDF uniquely surfaces RL for quantum technology, quantum circuit complexity, and quantum graph neural networks, which are genuine finds. But at least half its unique papers are noise.

### Adjacent Communities (SPECTER2)

- **Label accuracy**: Better than for P1. SPECTER2 does surface papers from adjacent areas (QML theory, quantum algorithms, formal learning theory) that are genuinely adjacent to the seeds' core QML focus.
- **Distinctiveness**: Moderate. 11 unique papers, with several valuable finds (polynomial separations, double descent in quantum kernels, quantum vs classical financial ML benchmarking).
- **What it finds that others don't**: SPECTER2's best unique contributions are the theoretical/formal papers (polynomial separations, noisy quantum learning theory, adversarial robustness guarantees) that share citation patterns with the profile's papers but approach the same problems from a more theoretical angle.

---

## Part 3: Multi-View Assessment

### Coverage
44 unique papers from 60 slots. For the narrow quantum ML profile, the three views do cover different aspects: MiniLM covers practical VQC engineering, TF-IDF covers the broad "quantum" landscape (including much noise), and SPECTER2 covers QML theory. There are likely relevant papers in areas like quantum kernel methods, quantum optimization theory, and quantum error correction for ML that none of the views surface, but the coverage is reasonable.

### Distinctiveness
More distinct than P1. MiniLM-SPECTER2 overlap is lower, and the unique papers from each view serve different purposes. TF-IDF is too noisy to be useful as a standalone view -- its signal-to-noise ratio is poor for narrow profiles.

### Label Accuracy
- **"Similar Ideas" (MiniLM)**: Accurate and helpful.
- **"Same Vocabulary" (TF-IDF)**: Misleading for narrow profiles. When a profile's vocabulary is dominated by a single broad term ("quantum"), the view matches on that term indiscriminately.
- **"Adjacent Communities" (SPECTER2)**: More accurate here than for P1. The view does surface adjacent theoretical and algorithmic communities.

### Overlap Papers
Papers in all three views (Superpositional Gradient Descent [2511.01918], Quantum LEGO Learning [2601.21780]) are relevant but not the most relevant. The all-three overlap is not a reliable indicator of top quality -- it just means these papers are generic enough to match all three retrieval strategies.

### Would a Researcher Actually Switch Views?
For P3, a researcher would benefit from switching between MiniLM (for practical QML engineering) and SPECTER2 (for QML theory). TF-IDF would be actively harmful -- a researcher would see quantum networking and quantum communication papers and lose trust in the system. Two views (MiniLM + SPECTER2) would serve this profile well. Three views with TF-IDF included would degrade the user experience.

### Information Overload
60 papers is excessive, especially when TF-IDF contributes mostly noise. A narrow profile would be better served by 10 papers from MiniLM and 10 from SPECTER2, with TF-IDF either removed or presented as a secondary "broad search" option.

---

## Part 4: Emergent Observations

- The three-view architecture reveals that narrow profiles expose TF-IDF's fundamental weakness: when a field's vocabulary is dominated by a small set of terms ("quantum circuit," "variational," "qubit"), TF-IDF cannot distinguish within the field and instead matches broadly across all quantum computing subfields.
- SPECTER2 provides genuine cross-pollination value for P3 that it does not provide for P1. This suggests SPECTER2's utility is profile-dependent -- it works better when the citation graph distinguishes nearby subfields (QML theory vs QML practice) than when the entire field shares one citation cluster.
- The quality of the "Adjacent Communities" view depends on whether the adjacent communities are actually interesting to the researcher. For P3, theoretical QML is adjacent and interesting. For P1, the adjacent communities (VLA models, diffusion policies without RL) are less directly useful.
- The narrow profile also makes MiniLM's precision more valuable -- when the research question is specific, semantic precision is exactly what you want.

---

## Part 5: Metric Divergence

The quantitative story would show 44 unique papers across views, suggesting good coverage. The qualitative reality is that perhaps 30 of those 44 are genuinely relevant (TF-IDF contributes mostly noise for this profile). The "unique papers per view" metric (7, 12, 11) suggests TF-IDF and SPECTER2 are both contributing substantially, but qualitatively TF-IDF's contributions are mostly irrelevant while SPECTER2's are mostly valuable. Paper count alone is a poor proxy for view quality.

SPECTER2's score compression (std = 0.0042) is slightly better than P1 but still means the ranking within the view is unreliable. The top-ranked SPECTER2 paper is not meaningfully "more similar" than the 20th-ranked one.
