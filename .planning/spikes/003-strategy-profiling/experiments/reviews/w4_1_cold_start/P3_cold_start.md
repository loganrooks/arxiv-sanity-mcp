# W4.1 Cold-Start Review: P3 (Quantum Computing / Quantum ML / Narrow)

## Profile Context

P3 targets quantum computing and quantum ML -- a narrow domain with distinctive vocabulary. "Narrow" means the profile has a tight conceptual scope: quantum circuits, QML architectures, fault tolerance, and noise-aware methods. This should make cold-start easier for lexical methods (distinctive terms) but potentially harder for semantic methods (fewer semantically similar non-quantum papers).

---

## 1-Seed Condition

**Seed paper:** "Polynomial-Time Classical Simulation of Noisy Quantum Circuits with Naturally Fault-Tolerant Gates"

This seed is extremely specific: classical simulation of noisy quantum circuits, Clifford circuits, percolation theory, Pauli path analysis, fault tolerance. The profile label is "Quantum ML" but this seed paper is pure quantum complexity theory / fault tolerance -- it has zero ML content. This mismatch between profile intent and seed content is itself a cold-start challenge.

### Part 1: Per-Paper Assessment

#### MiniLM (1 seed)

1. **Noisy Quantum Learning Theory** -- Relevant to the seed. Noisy quantum computation + learning theory. Directly addresses noise + quantum + learning. "Yes" would signal interest in the intersection of noise and quantum learning; excellent cold-start probe.

2. **Quantum Circuit Pre-Synthesis: Learning Local Edits to Reduce T-count** -- Relevant. Fault-tolerant quantum circuits + ML for circuit optimization. Bridges the seed's fault-tolerance focus with ML applications.

3. **Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation** -- Directly relevant. Fault-tolerant QC with stabilizer codes. Matches the seed's core area.

4. **Taming Barren Plateaus in Parameterized Quantum Circuits** -- Relevant. QML trainability (barren plateaus). This starts moving toward the quantum ML side of the profile. Good probe: "yes" confirms interest in QML architectures.

5. **Qimax: Efficient quantum simulation via GPU-accelerated stabilizer formalism** -- Directly relevant. Simulation of Clifford circuits using extended stabilizer formalism. Nearly identical topic to the seed.

6. **Improved Lower Bounds for QAC0** -- Relevant. Quantum circuit complexity. Matches the seed's theoretical complexity focus.

7. **Network-Based Quantum Computing: distributed fault-tolerant QC** -- Relevant. Fault-tolerant distributed QC. Same fault-tolerance theme.

8. **Robustness of quantum algorithms: Worst-case fidelity bounds** -- Relevant. Noise robustness for quantum algorithms. Closely related to the seed's noise analysis.

9. **Fault-Tolerant QEC: Implementing Hamming-Based Codes** -- Relevant. Quantum error correction implementation. Matches fault-tolerance theme.

10. **Assessing Superposition-Targeted Coverage Criteria for QNNs** -- Moderately relevant. QNN testing methodology. Moves toward QML but focused on testing/coverage.

11. **Adaptive Fidelity Estimation for Quantum Programs** -- Relevant. Noise-aware quantum program testing. Matches noise theme.

12. **Optimizing Fault-tolerant Cat State Preparation** -- Relevant. Fault-tolerant state preparation.

13. **Wigner's Friend as a Circuit** -- Moderately relevant. Quantum foundations experiment on hardware. Same general quantum computing domain but different sub-area (foundations vs. complexity).

14. **QAC0 Contains TC0 (with Many Copies)** -- Relevant. Quantum circuit complexity classes. Direct match to seed's complexity theory focus.

15. **Towards Simple and Useful One-Time Programs in the Quantum Random Oracle Model** -- Weakly relevant. Quantum cryptography. Same "quantum" domain but different sub-field. Would help probe whether user is interested in quantum crypto.

16. **Assessing fault-tolerant quantum advantage for k-SAT** -- Relevant. Fault-tolerant quantum advantage assessment. Matches seed themes.

17. **Optimizing compilation of error correction codes for 2xN quantum dot arrays** -- Relevant. QEC compilation for specific hardware. Fault-tolerance focus.

18. **A Rigorous Proof of the Grover-Rudolph State Preparation Algorithm** -- Moderately relevant. Quantum algorithms with amplitude encoding. Not about noise or fault tolerance, but same quantum computing domain.

19. **Testing classical properties from quantum data** -- Relevant. Quantum-classical boundary in learning. Connects to the seed's classical simulation angle.

20. **Constant-Depth Unitary Preparation of Dicke States** -- Relevant. Constant-depth quantum circuits. Matches circuit depth/complexity themes.

**MiniLM 1-seed verdict:** 17/20 clearly relevant, 3 moderately relevant, 0 misses. However, there is a critical observation: the recommendations are overwhelmingly about quantum computing fundamentals (fault tolerance, circuit complexity, error correction) and almost entirely miss the "quantum ML" part of the profile. This is not MiniLM's fault -- the seed paper is about classical simulation of noisy quantum circuits, not quantum ML. MiniLM faithfully found papers similar to the seed, but the seed does not represent the full profile. This is a textbook cold-start alignment problem: the seed anchors recommendations to a sub-area of the user's actual interest.

**For cold-start profile building:** The set would help a user who is broadly interested in quantum computing to identify which sub-areas they care about. But it would not help them discover quantum ML papers unless they explicitly add QML seeds.

#### TF-IDF (1 seed)

1. **Quantum Circuit Pre-Synthesis: Learning Local Edits to Reduce T-count** -- Relevant. FT circuits + ML.
2. **Reducing T Gates with Unitary Synthesis** -- Relevant. T-gate reduction for fault tolerance.
3. **Quantum Circuit for QFT for Arbitrary Qubit Connectivity** -- Moderately relevant. Quantum circuit design. Same domain but different focus.
4. **CktGen: Automated Analog Circuit Design with Generative AI** -- NOT relevant. Classical analog circuit design. TF-IDF matched on "circuit" without understanding "quantum circuit" vs. "analog circuit." This is a significant cold-start failure.
5. **Digital Circuits as Moore Machines** -- NOT relevant. Classical digital circuit theory. Another "circuit" term match failure. A researcher in quantum computing would find this baffling.
6. **Agent-Q: Fine-Tuning LLMs for Quantum Circuit Generation** -- Moderately relevant. LLMs for quantum circuits. Quantum-adjacent but more about LLM applications.
7. **Improved Lower Bounds for QAC0** -- Relevant. Quantum circuit complexity.
8. **Gradient descent reliably finds depth- and gate-optimal circuits** -- Relevant. Quantum circuit synthesis optimization.
9. **A mathematical model for a universal digital quantum computer** -- Relevant. Quantum computation formalism.
10. **Cutting Quantum Circuits Beyond Qubits** -- Relevant. Quantum circuit cutting for distributed execution.
11. **GTAC: A Generative Transformer for Approximate Circuits** -- NOT relevant. Classical approximate circuit design. Third "circuit" term match failure.
12. **Graph Neural Network-Based Predictor for Optimal Quantum Hardware Selection** -- Moderately relevant. ML for quantum hardware selection.
13. **Function Recovery Attacks in Gate-Hiding Garbled Circuits using SAT Solving** -- NOT relevant. Classical cryptography / garbled circuits. Fourth "circuit" failure. Completely wrong domain.
14. **RL for Adaptive Composition of Quantum Circuit Optimisation Passes** -- Relevant. RL for quantum circuit optimization.
15. **Impact of Circuit Depth vs Qubit Count on Variational Quantum Classifiers** -- Relevant. QML with variational circuits.
16. **Modular composition & polynomial GCD in the border of small, shallow circuits** -- NOT relevant. Algebraic complexity theory about polynomial computation. Fifth "circuit" failure -- this is about algebraic circuits (a complexity theory concept), not quantum or electrical circuits.
17. **ALIGN: A System for Automating Analog Layout** -- NOT relevant. Analog IC layout automation. Sixth "circuit" failure.
18. **When quantum resources backfire: Non-gaussianity in noisy bosonic circuits** -- Relevant. Noise in quantum (bosonic) circuits. Directly related to seed's noise analysis.
19. **Non-Abelian qLDPC** -- Relevant. Fault-tolerant QC with qLDPC codes.
20. **Stabilizer Code-Generic Universal Fault-Tolerant Quantum Computation** -- Relevant.

**TF-IDF 1-seed verdict:** 12/20 relevant, 2 moderately relevant, 6 clear misses. The misses are all caused by the same failure mode: TF-IDF matched on the word "circuit" without distinguishing quantum circuits from classical analog/digital/algebraic circuits. This is a devastating failure for a narrow domain. Six out of twenty recommendations are about classical circuits -- a quantum computing researcher would lose confidence in the system immediately.

### Part 2: Set-Level Cold-Start Assessment (1 seed)

**MiniLM:** The set gives a quantum computing researcher a useful feed to work with. Nearly everything is genuinely about quantum computing. The coverage is heavily weighted toward fault tolerance and circuit complexity (matching the seed) rather than quantum ML (the broader profile goal). A researcher would think "this tool gets my area" even if it does not yet know they also care about QML. The set is narrow but appropriate for cold start -- it correctly identifies the neighborhood of the seed.

**TF-IDF:** The set is contaminated with 6 classical circuit papers. A quantum computing researcher seeing analog layout automation and garbled circuits in their feed would immediately distrust the system. The 12 relevant papers are good, but the 6 misses are bad enough to undermine the entire experience. This is not "usable" -- the user would have to wade through noise to find the signal.

### Part 3: Strategy Comparison at Cold Start (1 seed)

MiniLM decisively outperforms TF-IDF at 1 seed for this narrow profile. The difference is stark: 17/20 vs. 12/20 relevant, with TF-IDF's failures being embarrassingly wrong (analog circuits, garbled circuits, algebraic circuits). MiniLM's semantic understanding distinguishes "quantum circuit" from other uses of "circuit" -- a disambiguation that TF-IDF cannot perform.

**TF-IDF produces garbage at 1 seed for P3.** Not all of it, but 30% is from the wrong domain entirely. That is enough to destroy user trust at cold start.

**MiniLM works at 1 seed for P3.** The recommendations are coherent and useful, even if they do not yet cover the QML side of the profile.

---

## 3-Seed Condition

**Seed papers:**
1. "Polynomial-Time Classical Simulation of Noisy Quantum Circuits" (same as 1-seed) -- quantum complexity/fault tolerance
2. "Hybrid Quantum Neural Networks with Amplitude Encoding: Advancing Recovery Rate Predictions" -- QML for finance with hybrid circuits
3. "Variational decision diagrams for quantum-inspired ML applications" -- decision diagrams for QML, barren plateaus, variational methods

Adding seeds 2-3 introduces the quantum ML dimension. Seed 2 is an applied QML paper (finance), seed 3 is QML methodology (variational methods, barren plateaus). The 3-seed set now covers both the quantum computing fundamentals (seed 1) and quantum ML (seeds 2-3) aspects of the profile.

### Part 1: Per-Paper Assessment

#### MiniLM (3 seeds)

1. **Shallow-circuit Supervised Learning on a Quantum Processor** -- Directly relevant. QML on real hardware with shallow circuits. Bridges seeds 1 and 2-3.
2. **Quantum LEGO Learning: Modular Design for Hybrid AI** -- Relevant to seeds 2-3. Hybrid quantum-classical models with VQCs.
3. **Differentiable Architecture Search for Adversarially Robust Quantum CV** -- Relevant. QNN robustness and architecture search. Bridges noise (seed 1) and QML (seeds 2-3).
4. **Trainability-Oriented Hybrid Quantum Regression** -- Relevant to seeds 2-3. Hybrid QML with barren plateau mitigation.
5. **Detecting underdetermination in parameterized quantum circuits** -- Relevant. Reliability of parameterized QC / QML models.
6. **Assessing Superposition-Targeted Coverage Criteria for QNNs** -- Relevant. QNN testing.
7. **Taming Barren Plateaus** -- Relevant to seed 3. Barren plateaus in PQCs.
8. **Noisy Quantum Learning Theory** -- Relevant. Bridges seed 1 (noise) and seeds 2-3 (learning).
9. **Continual Quantum Architecture Search** -- Relevant to seeds 2-3. QML architecture search.
10. **Quantum-Enhanced Neural Contextual Bandit Algorithms** -- Relevant. QML for decision-making.
11. **Superpositional Gradient Descent** -- Weakly relevant. Quantum-inspired classical optimization. Not actually quantum computing, just quantum-inspired. The distinction matters for domain experts.
12. **The Role of Quantum in Hybrid Quantum-Classical NNs: A Realistic Assessment** -- Relevant. Critical assessment of hybrid QML. Good for refining whether user wants applied or theoretical QML.
13. **Spectral Bias in Variational QML** -- Directly relevant to seed 3. Variational QML analysis.
14. **Inductive Graph Representation Learning with QGNNs** -- Relevant. Quantum graph neural networks.
15. **Adaptive Fidelity Estimation for Quantum Programs** -- Relevant to seed 1. Noise-aware quantum programs.
16. **Experimental robustness benchmarking of QNNs on superconducting hardware** -- Relevant. QNN robustness on real hardware.
17. **Quantum Computing -- Strategic Recommendations for Industry** -- Weakly relevant. Industry whitepaper / survey. Not a research paper. A researcher would find this mildly interesting at best.
18. **HiQ-Lip: Hierarchical Quantum-Classical Method for Lipschitz Estimation** -- Relevant. Quantum methods for neural network analysis.
19. **Noise-Aware Quantum Architecture Search** -- Relevant. Noise-aware QAS. Bridges seed 1 and seeds 2-3.
20. **Enhancing Expressivity of QNNs Based on SWAP test** -- Relevant. QNN expressivity.

**MiniLM 3-seed verdict:** 17/20 clearly relevant, 2 weakly relevant, 0 clear misses. The critical improvement over 1-seed: the QML dimension is now well-represented. Papers about barren plateaus, variational methods, hybrid architectures, QNN robustness, and architecture search all appear. The fault-tolerance papers are reduced but not eliminated. The set now covers both halves of the profile. The two weakly relevant papers (quantum-inspired gradient descent, industry whitepaper) are minor issues.

#### TF-IDF (3 seeds)

1. **A mathematical model for a universal digital quantum computer** -- Moderately relevant. Quantum computation formalism.
2. **Quantum AI for Cybersecurity: hybrid Quantum-Classical models** -- Moderately relevant. Applied hybrid QML but for cybersecurity.
3. **The Role of Quantum in Hybrid Quantum-Classical NNs** -- Relevant. Hybrid QML assessment.
4. **Agent-Q: Fine-Tuning LLMs for Quantum Circuit Generation** -- Moderately relevant. LLMs for quantum circuits.
5. **Shallow-circuit Supervised Learning on a Quantum Processor** -- Relevant. QML on real hardware.
6. **RL for Quantum Technology** -- Relevant. RL applied to quantum technology. Interesting cross-domain.
7. **Quantum Circuit for QFT for Arbitrary Qubit Connectivity** -- Moderately relevant. Quantum circuit design.
8. **Quantum circuit complexity and unsupervised ML of topological order** -- Relevant. Quantum circuits + unsupervised ML. Bridges both themes.
9. **Noise Resilience for VQE** -- Relevant. Variational algorithms + noise resilience.
10. **Quantum Data Centres: Why Entanglement Changes Everything** -- Weakly relevant. Quantum internet / networking. Not about QML or circuit complexity.
11. **1Q: First-Generation Wireless Systems Integrating Classical and Quantum Communication** -- NOT relevant. Quantum communication / wireless networking. No connection to QML or quantum circuits.
12. **Quantum Approaches to Minimum Edge Multiway Cut** -- Weakly relevant. Quantum optimization applied to graph problems. Tangential.
13. **Inductive Graph Representation Learning with QGNNs** -- Relevant. Quantum graph neural networks.
14. **Differentiable Architecture Search for Adversarially Robust Quantum CV** -- Relevant.
15. **C2|Q>: Framework for Bridging Classical and Quantum Software Dev** -- Weakly relevant. Quantum software engineering, not QML research.
16. **QAISim: Toolkit for Modeling AI in Quantum Cloud Computing** -- Weakly relevant. Cloud quantum computing simulation toolkit.
17. **Noise-Aware Quantum Architecture Search** -- Relevant.
18. **Superpositional Gradient Descent** -- Weakly relevant. Quantum-inspired, not actually quantum.
19. **Quantum LEGO Learning** -- Relevant.
20. **Noisy Quantum Learning Theory** -- Relevant.

**TF-IDF 3-seed verdict:** 10/20 clearly relevant, 7 weakly/moderately relevant, 3 clear misses or irrelevant. The misses are better than 1-seed (no analog circuits this time) but the set is still diluted. Quantum communication (#11), quantum data centres (#10), and quantum cloud computing (#16) are from adjacent quantum sub-fields that do not match the user's QML/circuit-complexity interest. The classical "circuit" confusion is mostly gone because the additional seeds diluted the problematic term.

### Part 2: Set-Level Cold-Start Assessment (3 seeds)

**MiniLM:** A substantial improvement over 1-seed. The QML dimension is now well-covered, with papers about variational circuits, barren plateaus, QNN robustness, architecture search, and hybrid models. The fault-tolerance thread from seed 1 is maintained through noise-aware papers. A quantum ML researcher would find this feed useful and well-targeted. The 3-seed MiniLM experience is significantly better than the 1-seed experience for this profile.

**TF-IDF:** Better than 1-seed (no classical circuit contamination) but still noisy. The presence of quantum networking, quantum communication, and software engineering papers creates clutter. A researcher would need to skip about half the papers to find the useful ones. The 3-seed TF-IDF experience is improved but not yet good.

### Part 3: Strategy Comparison at Cold Start (3 seeds)

MiniLM clearly outperforms at 3 seeds (17/20 vs. 10/20 clearly relevant). The gap has actually widened compared to 1-seed. TF-IDF's improvement from 1-to-3 seeds is mostly about eliminating the "classical circuit" contamination, but it replaces that noise with quantum-adjacent-but-wrong-subfield papers. MiniLM's improvement is more substantive: it gains QML coverage while retaining fault-tolerance relevance.

At 3 seeds, the difference is meaningful. MiniLM provides a coherent, useful feed. TF-IDF provides a noisy one that requires significant manual curation.

### Part 4: Emergent Observations

**Narrow domains are where TF-IDF fails most dramatically at cold start.** The word "circuit" appears in quantum computing, analog electronics, digital logic, algebraic complexity, and cryptography. TF-IDF cannot disambiguate. MiniLM understands that "noisy quantum circuit with Clifford gates" lives in a completely different semantic space than "analog circuit layout." This is the strongest argument for MiniLM at cold start.

**The seed-profile mismatch is real and matters.** The 1-seed condition used a quantum complexity theory paper for a "quantum ML" profile. MiniLM correctly found quantum complexity papers. The user would need to explicitly add QML seeds to steer the profile. This is not a strategy failure -- it is a cold-start UI challenge.

**At 3 seeds, MiniLM achieves genuine profile coverage for a narrow domain.** With one seed from each sub-area (complexity, applied QML, QML methodology), the recommendations span the full profile. The minimum viable seed set for a narrow domain appears to be one seed per major sub-area.

### Part 5: Metric Divergence

The quantitative claim that "MiniLM works from 1 seed" is PARTIALLY validated for P3. MiniLM produces relevant papers at 1 seed, but they cover only one facet of the profile (fault tolerance, not QML). Whether this "works" depends on what "works" means:
- If "works" means "produces non-garbage recommendations": yes, validated.
- If "works" means "captures the user's full interest": no, not validated. One seed captures one sub-area.

For P3, 3 seeds is the minimum for a genuinely useful experience. But this is because the profile has two distinct sub-areas (quantum complexity and QML), and 1 seed can only anchor one of them.

TF-IDF genuinely does not work at 1 seed for P3. The classical circuit contamination (30% of recommendations) is disqualifying.
