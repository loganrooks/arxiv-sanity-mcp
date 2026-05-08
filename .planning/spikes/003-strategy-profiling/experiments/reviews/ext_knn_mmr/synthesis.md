# Synthesis: kNN-per-Seed and MMR vs Centroid -- Qualitative Review

## Summary of Quantitative Verdict

The quantitative data says:
- **Centroid top-K:** Best performer. Baseline.
- **kNN per seed:** Catastrophic degradation (-58% MRR, +25% diversity). Rejected.
- **MMR (lambda=0.7):** Marginal change (-2.8% MRR, +6.6% diversity). Not worth the complexity.

Recommendation from quantitative analysis: stick with centroid, use "switch views" (TF-IDF or SPECTER2) for diversity instead of intra-view tricks.

---

## Does the Quantitative Verdict Hold Up?

### kNN: "Catastrophic" is profile-dependent, not universal

The qualitative review reveals that the -58% MRR average hides extreme variation across profiles:

**P1 (RL for Robotics, Medium breadth):** kNN produces a fragmented, incoherent set. 14 unique papers, only 4 genuinely relevant. The set reads like 3-4 separate reading lists stapled together (offline MBRL papers, flow-policy papers, embodied reasoning papers). The centroid is clearly superior. The "catastrophic" label fits.

**P3 (Quantum ML, Narrow breadth):** kNN has 13/20 overlap with centroid. The 7 unique papers are mostly off-topic (finance from seed 5, fault-tolerance from seed 1). The degradation is moderate: "diluted" rather than "catastrophic." The centroid handles narrow profiles well because there is less internal heterogeneity to average over.

**P4 (AI Safety, Broad breadth):** kNN produces a **high-quality, coherent set**. 10 unique papers, 7 of which are genuinely relevant (LLMStinger, TrojanPraise, SafeRBench, STAR-S, SafeThinker, Safety Vectors, MacPrompt). The kNN set is not worse than the centroid -- it is *different*. A researcher would benefit from seeing both. The "catastrophic" label does not fit.

**Why the profile-dependence?** The critical variable is topic density in the corpus, not profile breadth per se:

- When the topic is densely populated (many relevant papers in the corpus, as with AI safety/jailbreaking), per-seed neighborhoods all land in relevant territory. kNN finds different relevant papers, not irrelevant ones.
- When the topic is moderately populated (RL for robotics), per-seed neighborhoods fragment across sub-topics. Some seeds pull in pure-RL papers, others pull in embodied-reasoning papers. The union is incoherent.
- When the topic is narrow (quantum ML), kNN has high overlap with centroid because all seeds point the same direction, but the unique papers are seed-specific tangents.

The MRR metric penalizes kNN because it measures whether the *specific* top papers match ground truth, not whether the *set* is relevant. For P4, kNN's papers are relevant but different from centroid's, so MRR drops even though quality does not.

### MMR: "Marginal" is correct but undersells targeted value

The -2.8% MRR average accurately reflects that MMR does not substantially change results. But the qualitative picture is more nuanced:

**P1:** MMR swaps 5 papers. One genuine find (endoscopic navigation), one partial (aerial navigation), two noise (agentic search, action regularization). Net: neutral. MMR adds nothing a researcher would notice.

**P3:** MMR swaps 6 papers. Two genuinely novel perspectives (Agent-Q: LLMs for quantum circuits; Continual QAS: automated architecture search). These are qualitatively valuable -- they approach the topic from angles the centroid does not represent. Net: slightly positive.

**P4:** MMR swaps 8 papers. System-level perspective (Jailbreak-as-a-Service++), comprehensive benchmark (GuardEval), and cognitive-inspired approach (ARREST) are genuine contributions. But the cost is losing strong technical papers (Constitutional Classifiers++, ALERT, JPU). Net: trade-off between technical depth and topical breadth.

MMR's value is concentrated in specific profiles and specific swaps, not spread uniformly. On average it looks marginal; on particular profiles it introduces papers that represent genuinely different approaches or perspectives.

---

## Key Findings

### 1. kNN's failure mode is fragmentation, not irrelevance

When kNN fails (P1), it does not find irrelevant papers. It finds papers that are each relevant to ONE seed but not to the overall interest. The result is a fragmented set: 4 offline-MBRL papers (from seed 1), 3 flow-policy papers (from seed 3), 3 embodied-reasoning papers (from seed 2), stapled together without coherence. The individual papers are fine; the set is bad.

When kNN succeeds (P4), it is because the seeds are coherent enough that per-seed neighborhoods overlap with each other. The fragmentation disappears because each seed's neighborhood reaches into the same topic.

### 2. kNN surfaces papers the centroid structurally cannot find

The centroid averages seed embeddings, which means it is biased toward the intersection of all seeds. Papers that are strongly relevant to one seed but dissimilar to other seeds get pushed down. Examples:

- **P1:** The flow-policy literature (ReinFlow, Reverse Flow Matching, Composite Flow Matching) is strongly relevant to seed 3 (SAC Flow) but dissimilar to seeds 4-5 (magnetic capsule, locomotion). The centroid averages the flow-policy signal away. kNN finds these papers because it does not average.
- **P4:** LLMStinger (RL-based jailbreaking) is a novel attack method relevant to the interest but using techniques (RL fine-tuning) that make it dissimilar to other seeds' neighborhoods. The centroid misses it.

This is a structural limitation of centroid-based retrieval: it cannot represent multi-modal interests. If a researcher's interest has distinct "arms" (e.g., both flow-based policies AND locomotion), the centroid sits in the middle and misses papers on either arm.

### 3. MMR's best contributions are novel-angle papers, not redundancy reduction

MMR's stated purpose is to reduce redundancy (penalize similarity to already-selected papers). In practice, the qualitative effect is not "less redundancy" but "different angles":

- Agent-Q (LLMs for quantum circuit generation) is not a "less redundant" version of a centroid paper. It is a qualitatively different approach to the quantum circuits topic.
- Jailbreak-as-a-Service++ is not a "less redundant" jailbreak paper. It is a system-level threat model that no centroid paper addresses.

The distinction matters because "redundancy reduction" suggests the centroid set is repetitive (it mostly is not). What MMR actually does is push the selection boundary outward, finding papers that are slightly less similar to the centroid but represent novel perspectives. The mechanism (penalizing similarity to selected papers) incidentally produces this effect, but framing it as "diversity" or "novelty" is more accurate than "redundancy reduction."

### 4. RL-vocabulary pollution is a cross-strategy problem

All three strategies surface papers that share RL vocabulary with robotics seeds but are about RL for LLMs (Jet-RL, TAPO, Spark). This is a MiniLM embedding limitation: it cannot distinguish "policy optimization for robot control" from "policy optimization for language model training" because the token-level overlap is high. This is not a retrieval-strategy problem -- it is an embedding-space problem that motivates the "switch views" recommendation (TF-IDF would not conflate these because the surrounding context differs; SPECTER2 would not because it understands academic paper semantics).

### 5. Profile breadth label can be misleading

P4 is labeled "broad" but its seeds are tightly clustered around jailbreak attacks/defenses. True breadth (alignment theory, value specification, governance, existential risk) is not represented. Meanwhile, P1 is labeled "medium" but its seeds span genuinely different RL sub-methods (offline MBRL, VLA reasoning, flow policies, DRL for medical robots, PPO for locomotion). P1 has more internal heterogeneity than P4 despite a narrower label. The retrieval strategies respond to actual seed heterogeneity, not the label.

---

## Answers to the Three Questions

### 1. Does the quantitative verdict hold up qualitatively?

**Partially.**

- **Centroid best:** Yes, confirmed. Across all three profiles, the centroid produces the most coherent, reliable recommendation set. It is the safe default.
- **kNN rejected:** Overstated. kNN is rejected for P1 (fragmented) and P3 (diluted), but performs comparably to centroid on P4. The aggregate -58% MRR hides this profile-dependent behavior. A blanket rejection throws away P4-like cases where kNN finds genuinely relevant papers the centroid misses.
- **MMR marginal:** Confirmed on average, but undersells specific cases. MMR's best swaps (Agent-Q for P3, Jailbreak-as-a-Service++ for P4) represent genuinely novel perspectives. The average -2.8% MRR masks these targeted gains.

### 2. Is there any scenario where kNN or MMR should be offered as an option?

**kNN: Conditionally yes, with caveats.**

kNN should be considered when:
- The topic is densely populated in the corpus (many relevant papers exist)
- The researcher wants to explore facets of their interest rather than find the "best overall" papers
- The interest has distinct sub-areas that should not be averaged together

kNN should NOT be used as the primary recommendation strategy. Its failure mode (fragmentation) is worse than its success mode (different-but-relevant) is good. But it could be offered as a secondary view: "Papers related to each of your seeds" alongside the centroid's "Papers related to your overall interest." This is effectively a different product: seed-level exploration vs interest-level recommendation.

However, this is complex to implement and explain. The simpler alternative -- "switch to TF-IDF or SPECTER2 for a different perspective" -- achieves a similar goal (different papers surfaced) without the fragmentation risk. The kNN use case is narrow enough that the engineering cost may not be justified.

**MMR: Probably not as a separate strategy.**

MMR's gains are too small and too inconsistent to justify offering as a separate option. The 2 good swaps per profile do not outweigh the 2-3 neutral/negative swaps. A researcher would not meaningfully benefit from choosing "MMR mode" over "centroid mode."

However, a moderate lambda MMR could be applied as a post-processing step within the centroid strategy -- slightly diversifying results without offering it as a separate user-facing option. This is an implementation detail, not a product decision.

### 3. Does the "switch views for diversity" recommendation hold up?

**Yes, strongly confirmed.**

The qualitative review supports this from multiple angles:

1. **Intra-view tricks produce marginal diversity.** MMR's diversity gain is modest and comes at a relevance cost. kNN's "diversity" is actually fragmentation for most profiles. Neither approach produces the kind of meaningful diversity that would help a researcher discover new perspectives.

2. **Cross-view switching addresses the actual problem.** The main diversity failure is RL-vocabulary pollution -- MiniLM conflating "RL for robots" with "RL for LLMs." TF-IDF would not make this error because the contextual words differ. SPECTER2 would not make it because it understands paper semantics. Switching views solves the embedding-space problem that intra-view tricks cannot.

3. **The interesting papers kNN finds could also be found by view-switching.** The flow-policy papers kNN surfaces for P1 would likely appear in a SPECTER2 view because SPECTER2 understands the relationship between SAC Flow and ReinFlow at the paper-semantic level, not just the token level.

4. **View-switching is simpler to explain and implement.** "Show me results from a different perspective" is a clearer user action than "use kNN per seed instead of centroid" or "apply MMR with lambda=0.7." The product surface is cleaner.

---

## Caveats and Open Questions

1. **This review covers only 3 profiles.** The quantitative analysis covers more. The P4 finding (kNN works well on dense topics) needs validation against other profiles. If P7 (Federated Learning, the quantitative exception) shows a similar pattern, there may be a reliable predictor for when kNN adds value.

2. **The review cannot assess ranking quality within sets.** MRR measures the position of the best paper. A set can be qualitatively good (all 20 papers relevant) but still have low MRR if the top-ranked paper is not the same as the ground truth's top paper. The qualitative review assesses set quality, not ranking quality.

3. **Researcher preferences are not uniform.** The review assumes researchers want coherent, interest-level recommendations. Some researchers prefer exploratory, seed-level browsing. The "right" strategy depends on the use case, and the qualitative data supports offering both -- but only if the engineering cost is justified.

4. **The "topic density" predictor for kNN success has not been validated.** The hypothesis (kNN works when the topic is densely populated) emerged from qualitative observation, not systematic testing. It could be tested by correlating kNN-vs-centroid quality with the number of relevant papers per profile in the corpus.
