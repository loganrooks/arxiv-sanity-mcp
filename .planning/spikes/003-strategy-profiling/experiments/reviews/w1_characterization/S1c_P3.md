# W1 Characterization Review: S1c (SPECTER2 adapter) x P3 (Quantum ML)

**Strategy:** S1c -- SPECTER2 with proximity adapter, cosine similarity centroid
**Profile:** P3 -- Quantum computing / quantum ML (Narrow breadth, 10 seeds)
**Score range:** 0.957 -- 0.951 (spread: 0.006)
**Held-out recovery:** 0/5
**Profile papers in top-20:** 1

## Part 1: Per-Paper Assessment

**#1 Continual QAS with Tensor-Train Encoding (2601.06392) -- 0.957**
Continual learning for quantum architecture search. On-topic: variational quantum circuits + continual learning. MiniLM also includes this at #13.

**#2 Noise Resilience and Robust Convergence for the VQE (2601.16758) -- 0.956**
Variational quantum eigensolver with convergence guarantees. This is more quantum chemistry/physics than quantum ML, but variational quantum algorithms are common ground. Relevant for the algorithmic techniques, though the application domain (eigenvalue problems) diverges from the ML focus of the seeds.

**#3 FAQNAS: FLOPs-aware Hybrid Quantum NAS (2511.10062) -- 0.956**
Quantum neural architecture search. On-topic. MiniLM also includes this at #10.

**#4 Q-CHOP: Quantum Constrained Hamiltonian Optimization (2403.05653) -- 0.956**
Quantum optimization with constraints. NOT quantum ML -- this is quantum optimization for combinatorial problems. SPECTER2 surfaces it because it shares the variational quantum algorithm infrastructure with quantum ML papers and is well-connected in the citation graph. A quantum ML researcher might find the optimization techniques transferable, but this is a different research community.

**#5 Quantum LEGO Learning (2601.21780) -- 0.956**
Modular hybrid quantum-classical learning. On-topic. MiniLM #1.

**#6 Quantum Error Mitigation with Attention Graph Transformers (2512.23817) -- 0.955**
Error mitigation for quantum computing using classical ML. Interesting cross-direction: using ML to improve quantum computing, rather than quantum computing for ML. UNIQUE to SPECTER2. A quantum ML researcher might find this relevant if they deal with noisy hardware, which they almost certainly do. Good cross-community recommendation.

**#7 Taming Barren Plateaus (2511.13408) -- 0.955**
Barren plateaus in PQCs. On-topic. MiniLM #2.

**#8 Mathematical Model for Universal Digital Quantum Computer (2503.13388) -- 0.955**
Theoretical framework for quantum computation. This is pure theory -- mathematical foundations of quantum circuits. NOT quantum ML. SPECTER2 surfaces it because of citation-graph proximity to quantum circuit papers, but a quantum ML practitioner would find this too foundational/abstract. Weak recommendation.

**#9 hdlib 2.0: Vector-Symbolic Architectures (2601.02509) -- 0.954**
Classical vector-symbolic architecture library. NOT quantum at all. This is a classical ML library that happens to share some mathematical vocabulary with quantum computing (vectors, symbolic architectures, superposition-like operations). Clear false positive. This is the most egregious misfire in any review so far.

**#10 Spectral Bias in Variational Quantum ML (2506.22555) -- 0.954, profile paper**
Spectral bias in quantum learning. Directly on-topic. MiniLM #16.

**#11 Quantum Computing Strategic Recommendations (2601.08578) -- 0.954**
Industry whitepaper. Same as MiniLM #11. Moderate utility.

**#12 Information-Minimal Geometry for Qubit-Efficient Optimization (2511.08362) -- 0.954**
Qubit-efficient optimization using geometric methods. More quantum optimization than quantum ML, but the qubit-efficiency concern is shared. Tangentially relevant.

**#13 Efficient Quantum Circuits for the Hilbert Transform (2601.10876) -- 0.954**
Quantum signal processing circuits. NOT quantum ML -- this is quantum circuit design for signal processing. The connection is through quantum circuits generally, not ML specifically. A quantum ML researcher would not find this directly useful unless they needed Hilbert transform as a subroutine.

**#14 Gradient Descent Reliably Finds Depth-and-Gate-Optimal Circuits (2601.03123) -- 0.952**
Quantum circuit synthesis optimization. This is quantum compilation/synthesis, not ML. However, it addresses a problem (finding optimal circuits) that quantum ML researchers face when deploying their models. Moderate relevance through the tooling lens.

**#15 Investigation of Hardware Architecture Effects on Quantum Algorithm Performance (2601.05286) -- 0.952**
Benchmarking quantum algorithms across hardware platforms. Relevant for anyone deploying quantum ML on real hardware -- they need to know how hardware affects performance. Good practical recommendation.

**#16 Shallow-circuit Supervised Learning on Quantum Processor (2601.03235) -- 0.952**
Practical quantum ML. On-topic. MiniLM #4.

**#17 GNN-Based Predictor for Optimal Quantum Hardware Selection (2507.19093) -- 0.951**
Using classical GNNs to select quantum hardware. Cross-community: ML for quantum infrastructure. A quantum ML researcher might use this as a tool. Moderate relevance.

**#18 One-Shot Structured Pruning of QNNs (2512.24019) -- 0.951**
QNN pruning for NISQ. On-topic. MiniLM #18.

**#19 Quantum Approaches to Minimum Edge Multiway Cut (2601.00720) -- 0.951**
Quantum optimization for graph problems. NOT quantum ML. SPECTER2 surfaces combinatorial optimization papers that share the quantum computing infrastructure.

**#20 Noise-Aware QAS (2601.10965) -- 0.951**
Quantum architecture search under noise. On-topic. MiniLM #5.

## Part 2: Set-Level Assessment

**Overall character:** SPECTER2's set for P3 is noticeably broader than MiniLM's. Where MiniLM produced ~16-17 on-topic papers, SPECTER2 produces ~10-12. The additional papers are from adjacent quantum computing subfields: quantum optimization (#4, #12, #19), quantum circuit theory (#8, #13, #14), and one outright false positive (#9 hdlib). SPECTER2 interprets "quantum ML" more broadly as "quantum computing with ML connections."

**Strengths:**
- Surfaces quantum error mitigation (#6) and hardware benchmarking (#15) -- practically useful papers for deploying quantum ML on real hardware
- Includes papers about quantum infrastructure tooling (#14, #17) that a researcher building systems would use
- The broader scope might be valuable for researchers who need to understand the quantum computing ecosystem beyond just ML

**Gaps:**
- Weaker on the core quantum ML theory (barren plateaus, trainability, spectral bias) -- these papers appear but ranked lower
- Misses several MiniLM-unique papers that are directly about quantum ML applications (Quantum GNNs #6, QuFeX #17, trainability-oriented regression #8)
- The hdlib false positive (#9) is concerning -- a completely non-quantum paper ranked in the top-10

**False positive pattern:** Papers from adjacent quantum computing subfields (optimization, circuit theory, signal processing) that share citation-graph proximity but not research focus. Plus one complete misfire (#9) that seems to be a generic similarity artifact.

**Failure mode:** SPECTER2's citation-graph-informed proximity treats the entire quantum computing field as a connected community, which it is -- but a "quantum ML" researcher does not need papers about quantum optimization or quantum signal processing just because those papers share infrastructure and citation patterns.

## Part 4: Emergent Observations

1. **Score compression is even more extreme for narrow profiles.** The 0.006 spread (0.957-0.951) means the entire top-20 exists in a range that is essentially measurement noise. SPECTER2 cannot meaningfully distinguish between any of these papers. The ranking is arbitrary. Combined with the observation from P1, this appears to be a systematic property of SPECTER2's proximity adapter: it assigns very high similarity to a large number of papers and cannot make fine-grained distinctions.

2. **The hdlib false positive is diagnostic.** Paper #9 (hdlib 2.0 - Vector-Symbolic Architectures) is a classical computing library that has zero quantum content. Its presence at #9 (score 0.954, essentially identical to the top-1 score of 0.957) reveals that SPECTER2's similarity surface has noise spikes -- isolated papers that achieve high similarity for unknown reasons (possibly citation connections to a quantum ML paper, or shared mathematical vocabulary in the SPECTER2 embedding). This is worse than any MiniLM false positive, which at least involved papers in adjacent topics.

3. **SPECTER2 spreads across the quantum computing field.** For a narrow profile, this is a liability. The citation graph connects quantum ML to quantum chemistry (VQE), quantum optimization (QAOA, combinatorial), and quantum hardware (benchmarking, compilation) because researchers in these areas co-cite and co-author. But a researcher interested specifically in "quantum ML" does not want their recommendations dominated by quantum optimization papers. SPECTER2's "proximity" signal is too coarse for narrow interests.

4. **MiniLM outperforms SPECTER2 qualitatively for narrow profiles.** For P1 (medium), the strategies were roughly comparable. For P3 (narrow), MiniLM clearly produces a more useful recommendation set. The narrow vocabulary of quantum ML gives MiniLM's semantic matching a natural advantage: it can distinguish "quantum ML" from "quantum optimization" based on abstract text, while SPECTER2's citation graph treats them as one community.

## Part 5: Metric Divergence

For this profile, the quantitative metrics (MiniLM MRR 0.398 >> SPECTER2 MRR 0.184) align with the qualitative impression. SPECTER2 genuinely produces a weaker recommendation set for narrow interests. The score compression alone disqualifies SPECTER2 from fine-grained recommendation: it cannot tell its #1 from its #1000.

The false positive rate (at least 5-6 out of 20 are off-topic or tangential) is materially worse than MiniLM's (2-3 out of 20). For narrow profiles, SPECTER2's citation-graph breadth becomes a liability rather than an asset.

However, the held-out recovery is still 0/5 for both strategies, preserving the pattern that centroid-based approaches struggle to recover held-out papers regardless of the embedding model.
