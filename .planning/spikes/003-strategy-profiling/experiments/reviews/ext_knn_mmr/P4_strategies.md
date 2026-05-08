# P4: AI Safety / Alignment (Broad breadth) -- Strategy Comparison Review

## Seeds

1. **One Trigger Token Is Enough** (2505.07167) -- Defense strategy balancing safety and usability via trigger tokens
2. **Scaling Patterns in Adversarial Alignment** (2511.13788) -- Multi-LLM jailbreak experiments at scale
3. **Self-Guided Defense** (2511.21214) -- Adaptive safety alignment for reasoning models via synthesized guidelines
4. **Jailbreaking LLMs & VLMs** (2601.03594) -- Survey/unified defense for jailbreaking mechanisms
5. **PC^2: Politically Controversial Content** (2601.05150) -- Jailbreaking text-to-image models for political content

The seeds define a broad interest centered on LLM/VLM safety, specifically the jailbreak attack/defense cycle. Seed 5 extends this to text-to-image models. Despite "AI safety / alignment" label, the seeds are overwhelmingly focused on jailbreak attacks and defenses rather than alignment theory, value alignment, or existential risk. The breadth comes from spanning LLMs, VLMs, multimodal models, and text-to-image models, plus both attack and defense perspectives.

---

## Part 1: Per-Strategy Paper Assessment

### Centroid (20 papers)

1. **Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning** (2501.19180) -- Directly relevant: proactive safety reasoning to prevent jailbreaks.
2. **Latent Fusion Jailbreak** (2508.10029) -- Directly relevant: novel jailbreak technique via latent representation blending.
3. **When Models Outthink Their Safety** (2510.21285) -- Directly relevant: self-jailbreak in reasoning models. Interesting threat model.
4. **Jailbreaking Safeguarded T2I Models via LLMs** (2503.01839) -- Directly relevant: jailbreaking text-to-image models. Matches seed 5.
5. **TRYLOCK: Defense-in-Depth Against Jailbreaks** (2601.03300) -- Directly relevant: layered defense via preference and representation engineering.
6. **Jailbreaking Attacks vs Content Safety Filters** (2512.24044) -- Directly relevant: arms race between attacks and filters. Survey-like.
7. **From static to adaptive: immune memory-based jailbreak detection** (2512.03356) -- Directly relevant: adaptive detection inspired by immune systems.
8. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** (2509.01631) -- Directly relevant: mechanistic analysis of jailbreaks via neuron-level understanding.
9. **E^2AT: Multimodal Jailbreak Defense** (2503.04833) -- Directly relevant: defense for multimodal LLMs via joint optimization.
10. **Multi-turn Jailbreaking Attack in MLLMs** (2601.05339) -- Directly relevant: multi-turn attacks on multimodal LLMs.
11. **Constitutional Classifiers++** (2601.04603) -- Directly relevant: production-grade jailbreak defense. Practical systems work.
12. **Merging Triggers, Breaking Backdoors** (2601.04448) -- Directly relevant: defensive poisoning against backdoors in instruction-tuned LLMs.
13. **Simulated Ensemble Attack** (2508.01741) -- Directly relevant: transferring jailbreaks across fine-tuned VLMs.
14. **Learning to Detect Unseen Jailbreak Attacks in LVLMs** (2508.09201) -- Directly relevant: generalization of jailbreak detection to unseen attacks.
15. **JPU: Bridging Jailbreak Defense and Unlearning** (2601.03005) -- Directly relevant: connecting jailbreak defense with machine unlearning.
16. **LLM-VA: Resolving Jailbreak-Overrefusal Trade-off** (2601.19487) -- Directly relevant: the safety-utility balance via vector alignment.
17. **Jailbreaking LLMs Without Gradients or Priors** (2601.03420) -- Directly relevant: gradient-free, transferable jailbreak attacks.
18. **Knowledge-Driven Multi-Turn Jailbreaking** (2601.05445) -- Directly relevant: knowledge-guided multi-turn attacks.
19. **ALERT: Zero-shot Jailbreak Detection** (2601.03600) -- Directly relevant: detection via internal discrepancy amplification.
20. **Jailbreaking Commercial Black-Box LLMs** (2508.10390) -- Directly relevant: attacking commercial LLMs with explicit prompts.

**Centroid assessment:** Remarkably strong. All 20 papers are directly relevant to the jailbreak attack/defense topic. The set covers: attack methods (latent fusion, multi-turn, gradient-free, ensemble transfer, self-jailbreak), defense methods (proactive reasoning, layered defense, adaptive detection, constitutional classifiers, unlearning), and analysis (safety neurons, arms race survey, safety-utility trade-off). Both LLM and VLM/multimodal targets are represented. This is the centroid at its best -- a tightly coherent interest with well-represented topic in the corpus.

### kNN Per Seed (20 papers)

1. **Effective and Efficient Jailbreaks with Cross-Behavior Attacks** (2503.08990) -- Directly relevant: black-box jailbreak via cross-behavior attacks.
2. **LLMStinger: Jailbreaking LLMs using RL fine-tuned LLMs** (2411.08862) -- Directly relevant: RL-based automated jailbreaking.
3. **Jailbreaking LLMs Without Gradients or Priors** (2601.03420) -- Directly relevant (also in centroid).
4. **TrojanPraise: Jailbreak LLMs via Benign Fine-Tuning** (2601.12460) -- Directly relevant: backdoor attacks via fine-tuning APIs.
5. **Jailbreaking Commercial Black-Box LLMs** (2508.10390) -- Directly relevant (also in centroid).
6. **STAR-S: Improving Safety Alignment through Self-Taught Reasoning** (2601.03537) -- Directly relevant: safety alignment via reasoning on safety rules.
7. **TRYLOCK** (2601.03300) -- Directly relevant (also in centroid).
8. **Merging Triggers, Breaking Backdoors** (2601.04448) -- Directly relevant (also in centroid).
9. **Attributing and Exploiting Safety Vectors** (2601.15801) -- Directly relevant: mechanistic understanding and exploitation of safety representations.
10. **Jailbreaking Safeguarded T2I Models** (2503.01839) -- Directly relevant (also in centroid).
11. **SafeRBench: Reasoning Safety of LLMs** (2511.15169) -- Directly relevant: benchmark for reasoning safety. Novel evaluation angle.
12. **Guardrails for trust, safety, and ethical deployment** (2601.14298) -- Relevant: broader guardrails perspective. More survey/policy than technical.
13. **Safe-FedLLM: Safety of Federated LLMs** (2601.07177) -- Relevant: safety in federated learning for LLMs. Novel setting (federated) for safety.
14. **LLM-VA: Resolving Jailbreak-Overrefusal Trade-off** (2601.19487) -- Directly relevant (also in centroid).
15. **SafeThinker: Reasoning about Risk** (2601.16506) -- Directly relevant: deep safety alignment via risk reasoning.
16. **Safe Language Generation in the Limit** (2601.08648) -- Interesting: formal/theoretical perspective on safe language generation. More theoretical than practical.
17. **MacPrompt: Macaronic-guided Jailbreak for T2I** (2601.07141) -- Directly relevant: novel jailbreak technique for text-to-image models using macaronic text.
18. **CSSBench: Safety of Lightweight LLMs against Chinese Adversarial Patterns** (2601.00588) -- Relevant: safety benchmarking for specific language/model contexts.
19. **ReasAlign: Reasoning Enhanced Safety Alignment** (2601.10173) -- Directly relevant: reasoning-enhanced defense against prompt injection.
20. **Latent Fusion Jailbreak** (2508.10029) -- Directly relevant (also in centroid).

**kNN assessment:** Also a very strong set. All 20 papers are relevant to LLM/VLM safety and jailbreaking. The overlap with centroid is only 7, yet the 13 kNN-unique papers are almost all high-quality and on-topic. This is a notable finding: kNN does NOT degrade catastrophically for this broad profile. The kNN-unique papers include: several novel attack methods (LLMStinger via RL, TrojanPraise via fine-tuning, MacPrompt for T2I), several defense methods (STAR-S, SafeThinker, ReasAlign, safety vectors), a benchmark (SafeRBench), and broader perspectives (Safe-FedLLM, Guardrails, Safe Language Generation). The kNN set is more attack-heavy in its unique papers, while the centroid set is more balanced between attack and defense.

### MMR (20 papers)

1. **Enhancing Model Defense with Proactive Safety Reasoning** (2501.19180) -- Same as centroid #1.
2. **Latent Fusion Jailbreak** (2508.10029) -- Same as centroid #2.
3. **Jailbreaking Safeguarded T2I Models** (2503.01839) -- Same as centroid #4.
4. **Guardrails for trust, safety, and ethical deployment** (2601.14298) -- **Shared with kNN only.** Broader guardrails perspective.
5. **From static to adaptive: immune memory-based detection** (2512.03356) -- Same as centroid #7.
6. **Jailbreaking Attacks vs Content Safety Filters** (2512.24044) -- Same as centroid #6.
7. **Merging Triggers, Breaking Backdoors** (2601.04448) -- Same as centroid #12.
8. **TRYLOCK** (2601.03300) -- Same as centroid #5.
9. **Unraveling Jailbreaks Through Safety Knowledge Neurons** (2509.01631) -- Same as centroid #8.
10. **When Models Outthink Their Safety** (2510.21285) -- Same as centroid #3.
11. **E^2AT: Multimodal Jailbreak Defense** (2503.04833) -- Same as centroid #9.
12. **False Alarms, Real Damage: Adversarial Attacks on CTI Systems** (2507.06252) -- **MMR-unique.** Relevant but shifted: adversarial attacks on cyber threat intelligence systems using LLMs. Related to LLM safety but in a cybersecurity application context.
13. **ARREST: Adversarial Resilient Regulation** (2601.04394) -- **MMR-unique.** Relevant: safety and truth regulation in LLMs inspired by cognitive self-correction.
14. **CSSBench** (2601.00588) -- **Shared with kNN.** Safety benchmarking for Chinese adversarial patterns.
15. **ReasAlign** (2601.10173) -- **Shared with kNN.** Reasoning-enhanced safety alignment.
16. **Multi-turn Jailbreaking Attack** (2601.05339) -- Same as centroid #10.
17. **Jailbreak-as-a-Service++** (2505.21184) -- **MMR-unique.** Relevant: distributed jailbreak campaigns using LLM crowdsourcing. Novel threat model at system level.
18. **Simulated Ensemble Attack** (2508.01741) -- Same as centroid #13.
19. **Overlooked Safety Vulnerability: Malicious Optimization Algorithm Request** (2601.00213) -- **MMR-unique.** Relevant: novel jailbreak vector via optimization algorithm requests.
20. **GuardEval: Multi-Perspective Safety Benchmark** (2601.03273) -- **MMR-unique.** Relevant: comprehensive benchmark for evaluating safety, fairness, and robustness in LLM moderators.

**MMR assessment:** Retains 12 of centroid's 20 papers. The 5 MMR-unique papers are all relevant: Jailbreak-as-a-Service++ (system-level threat), False Alarms on CTI (applied adversarial), ARREST (cognitive-inspired regulation), Overlooked Safety Vulnerability (novel attack vector), and GuardEval (comprehensive benchmark). These are genuinely diverse additions -- they bring different perspectives (system-level threats, benchmarking, applied security) compared to the centroid's more focused jailbreak-attack/defense papers. The centroid papers that MMR drops include: Constitutional Classifiers++ (production defense), Learning to Detect Unseen Attacks (generalization of detection), JPU (defense + unlearning), ALERT (zero-shot detection), and Knowledge-Driven Multi-Turn Jailbreaking. These are all strong papers. The trade-off is real: MMR sacrifices some of the best technical attack/defense papers for broader perspective papers.

---

## Part 2: Strategy Comparison

### Centroid vs kNN

This is the most interesting profile for the centroid-vs-kNN comparison because both sets are high quality. Unlike P1 (where kNN was incoherent) and P3 (where kNN pulled in tangential topics), P4's kNN set is almost entirely on-topic. The 13 kNN-unique papers are overwhelmingly about LLM safety and jailbreaking, just different papers than the centroid selected.

Why does kNN work well here? Two possible explanations:

1. **High topic density:** The safety/jailbreaking topic is densely populated in the corpus. There are many relevant papers, so even seed-specific neighborhoods produce relevant results. The problem is not finding relevant papers -- it is ranking them.

2. **Seed homogeneity despite "broad" label:** Despite being labeled "broad," all 5 seeds are about jailbreak attacks and defenses on language/vision models. The breadth is in model types (LLM, VLM, T2I) and perspectives (attack vs defense), not in fundamentally different topics. So per-seed neighborhoods still overlap heavily with the centroid's neighborhood.

The kNN set does tilt toward the attack side (LLMStinger, TrojanPraise, MacPrompt, Cross-Behavior Attacks are all attack papers), while the centroid is more balanced. This reflects the seeds' emphasis -- more seeds describe attacks than defenses.

### Centroid vs MMR

MMR's 5 unique additions are qualitatively interesting:
- **Jailbreak-as-a-Service++** brings a system-level threat model (distributed jailbreaking campaigns) that no centroid paper covers.
- **GuardEval** brings a comprehensive evaluation perspective.
- **Overlooked Safety Vulnerability** highlights a specific attack vector.
- **ARREST** brings a cognitive-science-inspired approach.
- **False Alarms on CTI** extends the safety concern to a specific application domain.

The centroid papers that MMR drops (Constitutional Classifiers++, Learning to Detect Unseen Attacks, JPU, ALERT, Knowledge-Driven Multi-Turn Jailbreaking) are all strong technical papers focused on specific attack/defense mechanisms. MMR trades depth (specific techniques) for breadth (system-level threats, benchmarks, applied domains). Whether this trade is positive depends on the researcher's goal.

### kNN Unique Papers

Of the 10 kNN-unique papers, this is a remarkably good set:
- **Genuinely relevant and missed by centroid:** LLMStinger (RL-based jailbreaking -- novel technique), TrojanPraise (fine-tuning API backdoor -- novel threat model), SafeRBench (reasoning safety benchmark), STAR-S (self-taught safety reasoning), SafeThinker (deep safety alignment), Attributing Safety Vectors (mechanistic analysis), MacPrompt (macaronic jailbreak for T2I). That is 7 out of 10.
- **Relevant but peripheral:** Safe-FedLLM (federated safety), Safe Language Generation (theoretical), Guardrails (policy-level). These are relevant but broader than the seeds' technical focus.

This is the strongest kNN-unique showing across all three profiles. The quantitative metrics may penalize kNN here because the centroid set is also strong, and MRR measures whether the TOP results are right -- but the kNN set has a different ordering and different papers that are nonetheless relevant.

---

## Part 3: Set-Level Assessment

### Centroid
- **Coherence:** Very high. Every paper is about LLM/VLM safety with a focus on jailbreaking. The set reads as a thorough literature review of the jailbreak attack/defense landscape.
- **Diversity:** High within the topic. Covers: attack methods (multi-turn, gradient-free, ensemble, self-jailbreak), defense methods (proactive reasoning, layered defense, detection, unlearning, constitutional classifiers), analysis (mechanistic neurons, arms race), modalities (LLM, VLM, T2I). Balanced between attack and defense.
- **Researcher satisfaction:** Very high. A safety researcher would find this an excellent starting set. Possibly too focused on jailbreaking -- misses broader alignment, governance, or deployment safety topics.

### kNN Per Seed
- **Coherence:** High. Almost all papers are about LLM safety/jailbreaking. No off-topic drift.
- **Diversity:** High but attack-tilted. More attack papers than the centroid set. Adds novel attack vectors (RL-based, fine-tuning API, macaronic) and reasoning-safety perspectives (SafeRBench, SafeThinker, STAR-S).
- **Researcher satisfaction:** High. Different from the centroid set but not worse. A researcher would find different but equally valuable papers. The attack tilt might be a positive or negative depending on their focus.

### MMR
- **Coherence:** High but slightly more scattered than centroid. The CTI paper and guardrails paper broaden the scope.
- **Diversity:** Highest of the three. Adds system-level threats (Jailbreak-as-a-Service), evaluation perspectives (GuardEval), applied domains (CTI), and cognitive-inspired approaches (ARREST).
- **Researcher satisfaction:** High. A researcher interested in the broader safety landscape (not just technical attacks/defenses) would prefer this set. A researcher focused on specific techniques would prefer the centroid.

---

## Part 4: Emergent Observations

1. **P4 is the profile where kNN comes closest to matching centroid quality.** The quantitative catastrophe (-58% MRR average) does not manifest here. This is because the topic is densely populated and the seeds are semantically coherent despite the "broad" label. kNN's failure mode (fragmentation) does not occur when all seed neighborhoods point to the same topic.

2. **P4 challenges the narrative that kNN is universally bad.** The 10 kNN-unique papers include 7 genuinely relevant papers that the centroid misses. These are not tangential -- they are core jailbreak/safety papers with novel techniques (RL-based jailbreaking, fine-tuning backdoors, macaronic jailbreaks) and novel evaluation perspectives (reasoning safety benchmark, deep alignment). A researcher would benefit from seeing both lists.

3. **MMR's diversity gain is most visible on P4.** Jailbreak-as-a-Service++ and GuardEval represent genuinely different perspectives (system-level threats, comprehensive evaluation) that the centroid's focus on individual attack/defense mechanisms does not capture. For a broad interest like "AI safety," this broader perspective is valuable.

4. **The "broad" label may be misleading for P4.** Despite being labeled broad, the seeds are tightly clustered around jailbreaking. True breadth (alignment theory, value specification, existential risk, deployment governance) is not represented in the seeds. This means the strategies' performance on P4 reflects a densely-populated narrow topic that has been labeled broad, not a genuinely heterogeneous interest.

---

## Part 5: Metric Divergence

- **Does kNN FEEL catastrophic for P4?** No. The kNN set is high-quality and coherent. If this profile represents the -58% MRR that the aggregate reports, then the metric is misleading for this particular profile. The ordering of papers may differ from the centroid, and the specific top-K papers may not match the ground truth rankings, but the set as a whole is good. The MRR drop likely reflects different paper selection rather than worse paper selection.

- **Does MMR FEEL meaningfully better for P4?** Yes, more so than for P1 or P3. The system-level perspective (Jailbreak-as-a-Service++), comprehensive benchmark (GuardEval), and cognitive-inspired approach (ARREST) are qualitatively different from the centroid's technical focus. A safety researcher with broad interests would appreciate these additions. However, the cost (losing Constitutional Classifiers++ and other strong technical papers) is real.
