# W1 Characterization Review: S1a (MiniLM centroid) x P3 (Quantum ML)

**Strategy:** S1a -- MiniLM all-MiniLM-L6-v2 centroid, dot-product ranking
**Profile:** P3 -- Quantum computing / quantum ML (Narrow breadth, 10 seeds)
**Score range:** 0.593 -- 0.541 (spread: 0.052)
**Held-out recovery:** 0/5
**Profile papers in top-20:** 2

## Seeds Summary

The 10 seeds span quantum circuit design (Fourier transform, circuit cutting, distribution), quantum ML (variational classifiers, quantum-classical NNs, amplitude encoding), and quantum applications (portfolio optimization, unit commitment, noise simulation). The "narrow" designation is apt: this is specifically quantum computing with ML applications, not general quantum physics or general ML. Several seeds are cross-listed quant-ph + cs.LG.

## Part 1: Per-Paper Assessment

**#1 Quantum LEGO Learning: Modular Design for Hybrid AI (2601.21780) -- 0.593**
Modular hybrid quantum-classical learning with variational quantum circuits. Directly on-topic: variational quantum circuits integrated with neural networks. A researcher in quantum ML would want this -- it proposes a specific architectural principle for the hybrid models they are building.

**#2 Taming Barren Plateaus in Arbitrary PQCs (2511.13408) -- 0.581**
Addressing barren plateaus in parameterized quantum circuits. Extremely relevant to anyone working with variational quantum circuits (which is most of the seeds). This is a methodological contribution that addresses a fundamental training challenge. Strong recommendation.

**#3 Differentiable Architecture Search for Adversarially Robust Quantum CV (2601.18058) -- 0.577**
Quantum neural network architecture search for computer vision robustness. Relevant through the quantum neural network lens, though the application domain (adversarial robustness in CV) is more specific than the profile. Moderate relevance.

**#4 Shallow-circuit Supervised Learning on a Quantum Processor (2601.03235) -- 0.577**
Practical quantum ML on actual quantum hardware. Highly relevant -- this paper demonstrates that quantum ML can work in practice, which is the central question the profile's researchers are investigating.

**#5 Noise-Aware Quantum Architecture Search (2601.10965) -- 0.572**
Automated quantum circuit design under noise constraints. Relevant: noise-aware design is critical for NISQ-era quantum computing, and several seeds deal with noise/circuit optimization. Good topical fit.

**#6 Inductive Graph Representation Learning with Quantum GNNs (2503.24111) -- 0.569**
Quantum graph neural networks for graph-structured data. Relevant as a quantum ML application, though graph-specific rather than the circuit/variational focus of the seeds. Moderate relevance.

**#7 HiQ-Lip: Hierarchical Quantum-Classical Lipschitz Estimation (2503.16342) -- 0.568**
Quantum-classical method for neural network robustness analysis. An interesting cross-community paper: it uses quantum computing as a tool for classical ML verification. Tangentially relevant -- the quantum computing component is a means to an end.

**#8 Trainability-Oriented Hybrid Quantum Regression (2601.11942) -- 0.559**
Addressing trainability issues in quantum neural networks for regression. Directly on-topic: this is the same trainability challenge as #2 (barren plateaus) but focused on regression tasks. Strong recommendation.

**#9 Superpositional Gradient Descent (2511.01918) -- 0.557**
Quantum-inspired optimization for classical LLM training. This is "quantum-inspired" rather than "quantum computing" -- it applies quantum principles to classical optimization. The connection to actual quantum ML is philosophical rather than technical. Borderline false positive.

**#10 FAQNAS: FLOPs-aware Hybrid Quantum NAS (2511.10062) -- 0.555**
Efficiency-aware quantum neural architecture search. Relevant: same NAS-for-quantum theme as #5. A researcher in quantum ML would want to know about efficiency-aware approaches.

**#11 Quantum Computing Strategic Recommendations (2601.08578) -- 0.554**
Industry survey/whitepaper on quantum computing applications. Not a research paper in the traditional sense -- it is a strategic overview. A researcher might read this for context but would not cite it as related work. Moderate utility, low technical value.

**#12 Agent-Q: LLMs for Quantum Circuit Generation (2504.11109) -- 0.553, profile paper**
Using LLMs to generate and optimize quantum circuits. Relevant and novel -- applies the LLM paradigm to quantum circuit design. Good discovery for someone in quantum ML who might not track the LLM-for-science literature.

**#13 Continual Quantum Architecture Search with Tensor-Train Encoding (2601.06392) -- 0.551**
Continual learning for quantum circuits. Relevant: addresses catastrophic forgetting in variational quantum circuits. On-topic.

**#14 Scalable Quantum Message Passing GNNs for Wireless Communications (2601.18198) -- 0.547**
Quantum GNNs applied to wireless network optimization. The quantum computing component is genuine, but the application domain (wireless comms) is far from the profile's interests. A researcher in quantum ML would find the quantum architecture interesting but the application irrelevant. Moderate false positive.

**#15 Assessing Superposition-Targeted Coverage for QNNs (2411.02450) -- 0.546**
Testing/coverage criteria for quantum neural networks. Relevant from a quality assurance perspective for anyone building QNNs. Niche but on-topic.

**#16 Spectral Bias in Variational Quantum ML (2506.22555) -- 0.542, profile paper**
Spectral bias phenomenon in quantum learning. Directly on-topic: this is a fundamental investigation into how variational quantum models learn, which is central to the profile's interest.

**#17 QuFeX: Quantum Feature Extraction Module (2501.13165) -- 0.542**
Quantum feature extraction for hybrid networks. On-topic: proposes a specific quantum module for ML pipelines.

**#18 One-Shot Structured Pruning of QNNs (2512.24019) -- 0.541**
Pruning quantum neural networks for NISQ deployment. On-topic: addresses the practical deployment challenge of QNNs on noisy hardware.

**#19 The Role of Quantum in Hybrid Quantum-Classical NNs (2601.04732) -- 0.541**
Critical assessment of whether quantum components actually help in hybrid models. Extremely relevant and perhaps the most important paper for a researcher in this field -- it asks whether the whole enterprise works. Strong recommendation.

**#20 RL for Adaptive Composition of Quantum Circuit Optimisation (2601.21629) -- 0.541**
Using RL to optimize quantum circuit compilation. Relevant through the quantum circuit optimization lens. Cross-community paper bridging RL and quantum computing.

## Part 2: Set-Level Assessment

**Overall character:** A strong, focused set that centers tightly on variational quantum circuits, quantum neural networks, and hybrid quantum-classical ML. Approximately 16-17 of the 20 papers are genuinely on-topic for the "quantum ML" research interest. This is the highest on-topic rate of any strategy-profile combination reviewed so far. The narrow profile works well with MiniLM because quantum ML has a distinctive vocabulary that separates it clearly from other CS subfields.

**Strengths:**
- Excellent topical coherence -- nearly every paper is about quantum ML or quantum circuit design
- Good coverage of the methodological challenges (barren plateaus, trainability, noise-aware design, pruning for NISQ)
- Includes both theoretical/foundational papers (#2, #16, #19) and practical/applied papers (#4, #12, #18)

**Gaps:**
- No papers on quantum error correction or fault-tolerant quantum computing, despite one seed being about fault-tolerant gates
- Light on quantum applications beyond ML (optimization, simulation) despite seeds in those areas
- No papers on quantum hardware advances or quantum-classical compilation (beyond #20)
- 0/5 held-out papers, same pattern as P1

**False positive pattern:** Quantum-inspired classical methods (#9) and quantum methods applied to irrelevant domains (#14 wireless). These are rare (2-3 out of 20), showing that MiniLM's narrow focus works well for narrow profiles.

**Failure mode:** The centroid gravitates toward the "variational quantum circuits + ML" intersection, which is the densest part of the seed set, at the expense of the quantum computing infrastructure seeds (circuit distribution, Fourier transform, unit commitment). MiniLM captures the "what they're doing" (ML with quantum circuits) but not the "how they're building it" (circuit design, compilation, distribution).

## Part 4: Emergent Observations

1. **Narrow profiles amplify MiniLM's strengths.** For P1 (medium), MiniLM struggled to distinguish RL from imitation learning. For P3 (narrow), MiniLM excels because quantum ML has distinctive vocabulary that does not overlap much with other subfields. The narrower the interest, the better MiniLM's semantic matching works, because there are fewer adjacent topics to confuse with.

2. **The critical assessment paper (#19) is a gem.** "The Role of Quantum in Hybrid Quantum-Classical Neural Networks: A Realistic Assessment" -- this is the kind of paper that challenges the field's assumptions. MiniLM surfaces it at #19, just barely. A researcher would want this near the top. Its low ranking suggests that critical/skeptical papers may have different embedding signatures from the enthusiastic papers that dominate the field.

3. **Score interpretation is cleaner for narrow profiles.** The 0.593-0.541 spread with max score of 0.593 (vs 0.660 for P1) is consistent with quantum ML being a smaller and more distinctive subfield. The centroid does not have a large "neighborhood" in MiniLM space, so the scores are lower but more meaningful.

4. **No held-out recovery continues to be concerning.** The held-out papers for P3 include "Optimizing Compilation for Distributed Quantum Computing" (quant-ph + cs.DC) and "Spectral Bias in Variational Quantum Machine Learning" -- the latter IS in the top-20 as a profile paper but NOT as held-out. The compilation paper should be findable but is likely too infrastructure-focused compared to the ML-heavy centroid.

## Part 5: Metric Divergence

For this narrow profile, MiniLM's LOO-MRR advantage over SPECTER2 (0.398 vs 0.184 overall) likely translates to a genuine quality advantage. The qualitative set is tight and relevant, with few false positives. The narrow vocabulary of quantum ML means that MiniLM's semantic matching is precise rather than merely approximate.

However, the 0/5 held-out recovery still suggests the MRR metric and the profile-based evaluation are measuring different things. MRR within LOO clusters rewards finding papers that are similar to cluster members; profile-based evaluation rewards finding papers that match a researcher's interest. These can diverge when the researcher's interest is broader or different from any single cluster.
