# W1 Characterization Review: S1d (TF-IDF centroid) x P3 (Quantum ML)

**Strategy:** S1d -- TF-IDF (50K features, sublinear TF, English stopwords), cosine similarity centroid
**Profile:** P3 -- Quantum computing / quantum ML (Narrow breadth, 10 seeds)
**Score range:** 0.331 -- 0.275 (spread: 0.056)
**Held-out recovery:** 1/5 (Optimizing Compilation for Distributed Quantum Computing)
**Profile papers in top-20:** 2

## Part 1: Per-Paper Assessment

**#1 Inductive Graph Representation Learning with Quantum GNNs (2503.24111) -- 0.331**
Quantum GNNs for graph-structured data. Directly on-topic: quantum computing applied to ML for graph data. Uses variational quantum circuits, same infrastructure as the seeds. MiniLM #6, SPECTER2 did not include. Strong recommendation.

**#2 Mathematical Model for Universal Digital Quantum Computer (2503.13388) -- 0.330**
Theoretical framework for quantum circuits. Not quantum ML per se, but the abstract contains heavy quantum circuit terminology (gates, circuits, algorithms) that overlaps with the seeds' vocabulary. TF-IDF hits because of shared terms like "quantum circuits," "quantum gates," "parameterized." Marginal relevance -- too theoretical for a quantum ML researcher.

**#3 Optimizing Compilation for Distributed Quantum Computing (2508.15267) -- 0.319, HELD-OUT**
Quantum circuit compilation for distributed systems. HELD-OUT paper recovered. This is about circuit compilation and distribution, matching the seed about "Cutting Quantum Circuits Beyond Qubits" (circuit distribution/partitioning) and "Entanglement-Efficient Distribution" (quantum networks). TF-IDF finds it through shared vocabulary: "quantum circuit," "distributed," "compilation." Not the most central quantum ML paper, but matches the infrastructure portion of the profile.

**#4 Quantum Circuit Pre-Synthesis: Learning Local Edits to Reduce T-count (2601.19738) -- 0.315**
ML for quantum circuit optimization. UNIQUE to TF-IDF. This is the reverse direction: using ML to optimize quantum circuits (rather than quantum computing for ML). But the vocabulary overlap is genuine -- "quantum circuit," "learning," "optimization." A quantum ML researcher might find this interesting as it applies their techniques to their own infrastructure.

**#5 Noise Resilience for the VQE (2601.16758) -- 0.311**
Variational quantum algorithms with convergence guarantees. Same as SPECTER2 #2. Relevant through the variational algorithm lens.

**#6 Agent-Q: LLMs for Quantum Circuit Generation (2504.11109) -- 0.310, profile paper**
LLMs generating quantum circuits. On-topic. MiniLM #12.

**#7 Shallow-circuit Supervised Learning on Quantum Processor (2601.03235) -- 0.309**
Practical quantum ML on hardware. On-topic. MiniLM #4.

**#8 The Role of Quantum in Hybrid Quantum-Classical NNs (2601.04732) -- 0.309**
Critical assessment of quantum ML. On-topic. MiniLM #19. TF-IDF ranks it higher (#8 vs #19) -- the critical/assessment vocabulary ("role," "realistic assessment," "hybrid quantum-classical") gives it strong keyword match.

**#9 Noise-Aware QAS (2601.10965) -- 0.299**
Quantum architecture search under noise. On-topic. MiniLM #5.

**#10 Taming Barren Plateaus (2511.13408) -- 0.298**
Barren plateaus in PQCs. On-topic. MiniLM #2.

**#11 Investigation of Hardware Architecture Effects (2601.05286) -- 0.296**
Quantum hardware benchmarking. Same as SPECTER2 #15. Relevant for hardware-aware research.

**#12 Quantum AI for Cybersecurity (2601.02237) -- 0.292**
Quantum ML applied to cybersecurity. UNIQUE to TF-IDF. The quantum ML component (hybrid quantum-classical model for attack path analysis) is genuine, but the application domain is cybersecurity. A quantum ML researcher might be interested in the quantum architecture but not the cybersecurity application. Moderate relevance.

**#13 Continual QAS with Tensor-Train Encoding (2601.06392) -- 0.290**
Continual learning for quantum circuits. On-topic. MiniLM #13.

**#14 Quantum Approaches to Minimum Edge Multiway Cut (2601.00720) -- 0.290**
Quantum optimization for graph problems. Same as SPECTER2 #19. Not quantum ML.

**#15 RL for Quantum Technology (2601.18953) -- 0.289**
Survey of RL applied to quantum technology. UNIQUE to TF-IDF. This is a significant find -- it bridges RL and quantum computing, which maps to one of the seeds (variational RL for portfolio optimization). A quantum ML researcher interested in RL-based training would want this survey.

**#16 Deep Learning for Quantum Error Mitigation (2601.14226) -- 0.282**
Using deep learning to mitigate quantum errors. UNIQUE to TF-IDF. Cross-direction: classical ML improving quantum computing. Relevant for anyone deploying quantum ML on noisy hardware who needs practical error mitigation.

**#17 Quantum Circuit Complexity and Unsupervised ML of Topological Order (2508.04486) -- 0.280**
Quantum circuit complexity meets unsupervised ML. UNIQUE to TF-IDF. Interesting theoretical intersection of quantum information and ML. Niche but relevant for theoretically inclined quantum ML researchers.

**#18 Quantum Data Centres: Why Entanglement Changes Everything (2506.02920) -- 0.277**
Quantum networking and distributed computing infrastructure. Not quantum ML. Matched through "quantum" + "distributed" + "computing" vocabulary shared with circuit distribution seeds.

**#19 C2|Q>: Framework for Bridging Classical and Quantum Software (2510.02854) -- 0.276**
Quantum software engineering framework. UNIQUE to TF-IDF. Not quantum ML but relevant as tooling for anyone building quantum applications. A quantum ML researcher needs software tools, and this is one. Marginal but practical utility.

**#20 Efficient Quantum Circuits for the Hilbert Transform (2601.10876) -- 0.275**
Quantum signal processing. Same as SPECTER2 #13. Not quantum ML.

## Part 2: Set-Level Assessment

**Overall character:** TF-IDF's set for P3 is more scattered than MiniLM's. Approximately 10-12 papers are genuinely on-topic for quantum ML, compared to MiniLM's 16-17. The remaining papers fall into two categories: (1) quantum computing infrastructure that shares vocabulary (circuit compilation, hardware benchmarking, quantum networking), and (2) cross-direction papers where classical ML is applied to quantum problems rather than the reverse. The second category is actually interesting and unique to TF-IDF.

**Strengths:**
- Only strategy to recover a held-out paper for this profile
- Surfaces the cross-direction "ML for quantum" literature (#4, #16) that both embedding models miss
- Finds the RL-for-quantum survey (#15) that bridges two seeds
- Ranks the critical assessment paper (#8) higher than MiniLM does, suggesting TF-IDF is less biased toward the enthusiasm of the field

**Gaps:**
- Weaker on core quantum ML theory than MiniLM (barren plateaus at #10 instead of #2, trainability not in top-20 at all)
- Includes more off-topic quantum infrastructure papers (networking, software engineering)
- Missing some of MiniLM's best finds (quantum GNN architecture search, adversarially robust quantum CV, QuFeX)

**False positive pattern:** Quantum computing infrastructure papers that share the vocabulary "quantum circuit" and "quantum computing" with the ML papers but are about different problems (compilation, networking, software engineering). TF-IDF cannot distinguish "quantum circuits for ML" from "quantum circuits for anything."

**Failure mode:** For a narrow profile with distinctive vocabulary, TF-IDF's keyword matching is precise enough to find the right field (quantum computing) but not precise enough to find the right subfield (quantum ML specifically). The key terms ("quantum," "circuit," "variational," "learning") appear across the entire quantum computing literature, diluting TF-IDF's specificity.

## Part 4: Emergent Observations

1. **TF-IDF's score spread reveals its discriminative capacity.** The 0.056 spread for P3 is the widest of any strategy on any profile. TF-IDF makes the sharpest distinctions between top-1 and top-20, which means its ranking carries the most information. But this advantage is partially wasted because some of the top-ranked papers are off-topic (the mathematical model paper at #2 has a high TF-IDF score because it uses the exact same terms, not because it is relevant).

2. **The held-out recovery pattern extends.** TF-IDF again recovers a held-out paper (1/5), continuing its advantage over both embedding models (0/5 each). The recovered paper (circuit compilation) is not the most central quantum ML paper, but it IS one of the seeds' concerns (circuit distribution). TF-IDF finds it because the vocabulary match is precise: "quantum circuit" + "distributed" + "compilation" matches the seed about circuit cutting and distribution.

3. **Cross-direction papers are TF-IDF's unique contribution.** Papers #4 (ML for circuit optimization), #16 (DL for error mitigation), and #15 (RL for quantum technology) all represent the "classical ML applied to quantum problems" direction, which is the reverse of the profile's primary interest. This is actually valuable discovery -- a researcher working on "quantum for ML" should know what "ML for quantum" is doing, as the techniques are often transferable. Neither embedding model surfaces these papers, probably because their citation graphs and semantic neighborhoods are separated.

4. **Narrow profiles expose TF-IDF's subfield discrimination weakness.** For P1 (medium), TF-IDF excelled because "reinforcement learning for robotics" has sufficiently distinctive vocabulary. For P3 (narrow), the subfield vocabulary ("quantum circuit," "variational," "quantum computing") is shared across multiple quantum computing subfields, and TF-IDF cannot reliably distinguish between them.

## Part 5: Metric Divergence

TF-IDF's LOO-MRR of 0.104 is the lowest, and for P3 specifically, this seems partly justified -- MiniLM does produce a more focused and relevant recommendation set. However, TF-IDF's held-out recovery advantage and its unique cross-direction discoveries suggest that the MRR gap is larger than the actual quality gap. TF-IDF is finding a different (broader, less focused) slice of the relevant literature, not a worse one.

The critical question for P3 is whether a researcher wants: (a) a focused set of papers about quantum ML specifically (MiniLM's strength), or (b) a broader set that includes quantum computing infrastructure and cross-direction papers (TF-IDF's character). Both are legitimate information needs; they represent different stages of research (deep dive vs literature survey).
