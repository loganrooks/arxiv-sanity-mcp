# Single-Strategy Characterization Review

**Model:** voyage
**Profile:** Federated learning + privacy (P7)
**Depth:** full
**Overlap with MiniLM:** 13/20 shared, 7 unique to voyage

## Seed Papers
  - [2601.00785] FedHypeVAE: Federated Learning with Hypernetwork Generated Conditional VAEs for Differentially Private Embedding Sharing (cs.LG)
  - [2509.14024] Differentially private federated learning for localized control of infectious disease dynamics (cs.LG)
  - [2509.14603] Towards Privacy-Preserving and Heterogeneity-aware Split Federated Learning via Probabilistic Masking (cs.LG)
  - [2601.01737] Local Layer-wise Differential Privacy in Federated Learning (cs.CR)
  - [2601.06466] SecureDyn-FL: A Robust Privacy-Preserving Federated Learning Framework for Intrusion Detection in IoT Networks (cs.CR)

## voyage Top-20 Recommendations

(Papers 1-20 as listed in template above)

---

## Assessment

**Limitation note:** Voyage-4 had 160/2000 papers fail to embed (8% failure rate due to API rate limiting). The effective retrieval pool is approximately 1840 papers. Federated learning is well-represented in the corpus, so the failure rate is unlikely to introduce systematic bias, but individual relevant FL papers may be absent due to embedding failure.

### 1. Per-Paper Assessment

**Paper 1 [2601.01737] LaDP** -- Direct (seed paper). Layer-wise adaptive differential privacy for FL.

**Paper 2 [2509.14603] PM-SFL** -- Direct (seed paper). Privacy-preserving split federated learning via probabilistic masking.

**Paper 3 [2509.14024] DP-FL for Epidemics** -- Direct (seed paper). Differentially private FL for infectious disease forecasting.

**Paper 4 [2601.06466] SecureDyn-FL** -- Direct (seed paper). Privacy-preserving FL framework for IoT intrusion detection.

**Paper 5 [2412.07454] Tazza** -- Direct. Secure FL via neural network parameter shuffling. Addresses both gradient inversion and model poisoning attacks. Core to the profile.

**Paper 6 [2507.14629] VMask** -- Direct. Label privacy protection in vertical FL via layer masking. Extends the privacy framework to the vertical FL setting.

**Paper 7 [2601.17713] FedCCA** -- Adjacent. Client-centric adaptation for FL on IoT devices with data heterogeneity. More about heterogeneity handling than privacy, but relevant to the FL ecosystem.

**Paper 8 [2601.06710] Privacy-Preserving Cloud Review** -- Adjacent. Survey of privacy-preserving data processing in cloud computing. Broader than FL specifically, covering HE, DP, and federated analytics.

**Paper 9 [2510.23463] DP as a Perk** -- Direct. DP via channel noise in over-the-air FL. Theoretical contribution showing DP can be gained naturally from wireless channel noise without artificial noise injection.

**Paper 10 [2601.17183] FedProx for Heart Disease** -- DIVERGENT. Adjacent. Simulation study of FedProx for heart disease prediction. A narrow, domain-specific application paper with a small dataset (303 patients). The contribution is incremental -- applying existing FedProx to a single medical dataset. This is the weakest paper in the set. A researcher working on FL privacy methods would find this unremarkable.

**Paper 11 [2503.15550] Zero-Knowledge FL** -- Direct. ZK-proofs integrated into FL for trustworthy client selection. Combines FL with zero-knowledge proofs, a distinctive and advanced privacy mechanism.

**Paper 12 [2412.04416] FedDUAL** -- Direct. Dual-strategy FL with adaptive loss and dynamic aggregation for data heterogeneity. Addresses a core FL challenge (non-IID data) with novel aggregation.

**Paper 13 [2601.01053] Byzantine-Robust + Post-Quantum FL** -- DIVERGENT. Direct. Byzantine-robust FL with post-quantum secure aggregation for IoT. Combines two active FL security research threads (Byzantine robustness + quantum-safe cryptography). Novel combination, directly relevant to the security dimension of the profile.

**Paper 14 [2410.05637] FedPP** -- DIVERGENT. Adjacent. Federated neural nonparametric point processes. A specialized FL application for temporal event modeling. The FL methodology (divergence-based aggregation of SGCP kernel hyperparameters) is novel but the application domain (point processes) is far from the privacy-focused seeds. This divergent signal is coherent but niche.

**Paper 15 [2601.19745] GraphDLG** -- Direct. Deep leakage from gradients in federated graph learning. Directly addresses the gradient privacy attack problem in FL, which is central to understanding why privacy-preserving mechanisms are needed.

**Paper 16 [2510.07132] DPMM-CFL** -- DIVERGENT. Adjacent. Bayesian nonparametric clustering for federated learning. Addresses cluster number inference in clustered FL, which is about FL methodology rather than privacy. Relevant to the broader FL landscape but peripheral to the privacy focus.

**Paper 17 [2601.19090] DP Synthetic Distillation** -- Direct. Privacy-preserving model transcription via differentially private synthetic data generation. Directly addresses DP for model transfer, core to the profile.

**Paper 18 [2512.24286] Data Heterogeneity-Aware CSRA** -- DIVERGENT. Adjacent. Client selection and resource allocation for FL in wireless networks with data heterogeneity. More about wireless FL optimization than privacy. The generalization error analysis connects to model quality, but privacy is not the central concern.

**Paper 19 [2405.09037] SSFL** -- DIVERGENT. Adjacent. Sparse subnetwork discovery for efficient FL communication. Communication efficiency rather than privacy, though communication reduction has privacy implications (fewer bits transmitted). A useful but not directly privacy-focused contribution.

**Paper 20 [2601.14687] ECA** -- DIVERGENT. Adjacent/Provocative. Fine-grained poisoning attacks on ranking-based FL. Reveals that even FRL, which was thought to be robust against poisoning, is vulnerable to precise accuracy control attacks. Provocative security finding.

### 2. Set-Level Assessment

**Landscape coverage:**
- Privacy mechanisms: differential privacy (layer-wise, channel-noise-based, synthetic distillation), secure aggregation (post-quantum, shuffling-based), zero-knowledge proofs, vertical FL label privacy
- Security threats: gradient leakage (GraphDLG), Byzantine attacks, poisoning (ECA), data reconstruction
- FL methodology: heterogeneity handling (FedCCA, FedDUAL, DPMM-CFL, CSRA), split FL, communication efficiency (SSFL)
- Applications: healthcare (heart disease, epidemic forecasting), IoT intrusion detection, wireless networks
- Broader context: cloud privacy survey, model transcription

**Coverage strengths:**
- Good breadth across privacy mechanisms (DP, HE, ZKP, secure aggregation)
- Both attack and defense perspectives represented
- Multiple FL paradigms (horizontal, vertical, split)
- Real-world applications included

**What is conspicuously absent:**
- Differential privacy composition theorems and tighter privacy accounting (theoretical foundations)
- Personalization under privacy constraints (a growing subfield)
- Federated unlearning / right-to-be-forgotten
- Privacy in federated foundation model training
- MPC-based FL protocols

**Divergent paper character:** The 7 divergent papers split into:
- 2 directly relevant to security (Byzantine-robust + post-quantum FL, ECA poisoning attack)
- 2 FL methodology without strong privacy focus (DPMM-CFL clustering, CSRA resource allocation)
- 1 narrow application (FedProx heart disease)
- 1 communication efficiency (SSFL)
- 1 specialized FL application (FedPP point processes)

The divergent signal is mixed: 2/7 are high-quality security contributions, 2/7 are FL methodology tangential to privacy, and 3/7 are peripheral or narrow.

### 3. Emergent Observations

**Signal character:** With 7/20 unique papers (35% divergence), Voyage shows significant differentiation from MiniLM on this profile. The divergence is mixed: some papers represent genuinely useful expansions of the FL security landscape (Byzantine-robust post-quantum FL, ECA attack), while others drift toward general FL methodology without a strong privacy focus.

**Divergence quality:** Partially coherent. The security-oriented divergent papers (Byzantine-robust, ECA) are valuable. The FL methodology papers (DPMM-CFL, CSRA) are relevant to FL but not specifically to the privacy theme. The heart disease application paper is weak. Overall, maybe 3/7 divergent papers add genuine value to the privacy-focused profile.

**Productive provocations:** ECA (Paper 20) is the strongest provocation -- demonstrating that ranking-based FL, assumed to be robust against poisoning, is vulnerable to fine-grained control attacks. This challenges assumptions about FL security. The Byzantine-robust post-quantum paper (Paper 13) is also forward-looking, addressing the intersection of quantum computing threats with FL security.

### 4. Absent Researcher Note

To properly assess this recommendation set, I would need to know:
- Whether the researcher is focused on privacy specifically (DP, MPC) or FL security broadly (including Byzantine robustness, poisoning)
- Whether they work on theoretical privacy guarantees or practical system design
- Whether IoT/wireless settings are relevant (several papers address this deployment context)
- Whether they are interested in FL methodology generally or specifically in privacy-preserving FL
- The 7-paper divergence from MiniLM suggests Voyage retrieves more broadly within FL, potentially diluting the privacy focus

### 5. Metric Divergence Flags

The 13/20 overlap (J@20 = ~0.52) indicates moderate-to-significant divergence. The qualitative review partially supports this: while the core FL + privacy papers are well-represented (13 shared papers are mostly strong), the 7 divergent papers are of mixed quality for the privacy-specific profile. About 3/7 divergent papers are strong privacy/security contributions, while 4/7 are general FL methodology or narrow applications that dilute the privacy focus.

This suggests Voyage may have a slightly broader retrieval radius on this profile, pulling in FL papers that are methodologically relevant but not specifically about privacy. Whether this is a strength or weakness depends on the researcher's scope.
