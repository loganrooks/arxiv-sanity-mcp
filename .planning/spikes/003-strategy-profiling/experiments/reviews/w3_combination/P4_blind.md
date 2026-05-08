# W3 Blind Pairwise Comparison: P4 (AI Safety / Alignment)

**Profile breadth**: Broad
**Overlap**: 14 consensus / 6 A-only / 6 B-only (70% overlap)

## Seed Papers

The profile is defined by five papers covering:
1. Trigger-token defense strategy for LLM safety
2. Multi-LLM adversarial scaling experiments (jailbreak between models)
3. Self-guided adaptive safety alignment for reasoning models
4. Survey of jailbreak attacks and defenses for LLMs and VLMs
5. Jailbreaking text-to-image models for politically harmful content

The profile name says "AI safety / alignment" (broad), but the seeds are actually quite narrow: they are all about **jailbreak attacks and defenses** for large language models and multimodal models. There is no representation of alignment theory, RLHF methodology, interpretability, governance, or value specification. The effective interest is "LLM jailbreak security" -- a specific sub-community within AI safety.

---

## Part 1: Per-Paper Assessment

### Strategy A

1. **Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning** (CONSENSUS, 0.855) -- On-topic. Defense method using proactive safety reasoning against jailbreaks. Directly in the seed community.

2. **Jailbreaking Attacks vs. Content Safety Filters** (CONSENSUS, 0.847) -- On-topic. Systematic evaluation of jailbreak attacks against content safety filters. Meta-analysis paper very relevant to the seeds.

3. **Exploring the Secondary Risks of Large Language Models** (CONSENSUS, 0.834) -- Relevant. Non-adversarial safety failures. Slightly broader than the jailbreak focus of the seeds, but this is the kind of broadening that is genuinely useful.

4. **SafeThinker: Reasoning about Risk to Deepen Safety Beyond Shallow Alignment** (CONSENSUS, 0.817) -- On-topic. Defense framework addressing vulnerability to disguised attacks. Directly in the seed community.

5. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks via RL** (CONSENSUS, 0.816) -- On-topic. New jailbreak attack method. Directly in the seed community.

6. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** (CONSENSUS, 0.811) -- On-topic. Interpretability-informed analysis of jailbreak mechanisms. Directly in the seed community with an interesting mechanistic angle.

7. **AprielGuard** (A-ONLY, 0.807) -- On-topic. Unified safeguard model handling both safety risks and adversarial threats. Directly in the seed community.

8. **RECAP: Resource-Efficient Method for Adversarial Prompting** (CONSENSUS, 0.801) -- On-topic. Automated jailbreaking method (red-teaming). Same community.

9. **Jailbreak-Zero: Path to Pareto Optimal Red Teaming** (CONSENSUS, 0.799) -- On-topic. Red teaming methodology shifting from example-based to policy-based frameworks. Same community.

10. **MiJaBench: Revealing Minority Biases via Hate Speech Jailbreaking** (CONSENSUS, 0.789) -- On-topic. Jailbreak evaluation revealing bias disparities. Same community with a fairness dimension.

11. **JPU: Bridging Jailbreak Defense and Unlearning** (CONSENSUS, 0.788) -- On-topic. Machine unlearning as jailbreak defense. Same community.

12. **Emoji-Based Jailbreaking of LLMs** (CONSENSUS, 0.785) -- On-topic. Specific jailbreak technique. Same community.

13. **Jailbreaking Commercial Black-Box LLMs with Explicitly Harmful Prompts** (A-ONLY, 0.783) -- On-topic. Black-box jailbreak attacks on reasoning models. Same community.

14. **Beyond Visual Safety: Jailbreaking MLLMs for Harmful Image Generation** (CONSENSUS, 0.781) -- On-topic. Multimodal jailbreaking. Connects to seed 5 (text-to-image models).

15. **TrojanPraise: Jailbreak LLMs via Benign Fine-Tuning** (A-ONLY, 0.779) -- On-topic. Fine-tuning-based jailbreak attack. Same community.

16. **Latent Fusion Jailbreak: Blending Harmful and Harmless Representations** (A-ONLY, 0.777) -- On-topic. White-box jailbreak operating in continuous latent space. Same community.

17. **Jailbreaking Safeguarded Text-to-Image Models via LLMs** (CONSENSUS, 0.773) -- On-topic. Jailbreaking T2I models. Directly connects to seed 5.

18. **Learning to Detect Unseen Jailbreak Attacks in LVLMs** (A-ONLY, 0.773) -- On-topic. Jailbreak detection for vision-language models. Same community.

19. **From Adversarial Poetry to Adversarial Tales** (A-ONLY, 0.768) -- On-topic. Creative jailbreak technique using narrative structures. Same community with a cultural-interpretive angle.

20. **RAJ-PGA: Reasoning-Activated Jailbreak and Principle-Guided Alignment** (CONSENSUS, 0.766) -- On-topic. Jailbreak specific to reasoning models plus alignment framework. Same community.

### Strategy B

1. **Jailbreaking Attacks vs. Content Safety Filters** (CONSENSUS, 0.033) -- On-topic. (Same assessment as A-2.)

2. **Jailbreaking Safeguarded Text-to-Image Models via LLMs** (CONSENSUS, 0.029) -- On-topic. (Same assessment as A-17.)

3. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks via RL** (CONSENSUS, 0.029) -- On-topic. (Same assessment as A-5.)

4. **Exploring the Secondary Risks of LLMs** (CONSENSUS, 0.028) -- Relevant. (Same assessment as A-3.)

5. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** (CONSENSUS, 0.028) -- On-topic. (Same assessment as A-6.)

6. **Jailbreak-Zero: Path to Pareto Optimal Red Teaming** (CONSENSUS, 0.028) -- On-topic. (Same assessment as A-9.)

7. **Beyond Visual Safety: Jailbreaking MLLMs for Harmful Image Generation** (CONSENSUS, 0.027) -- On-topic. (Same assessment as A-14.)

8. **RAJ-PGA: Reasoning-Activated Jailbreak and Principle-Guided Alignment** (CONSENSUS, 0.027) -- On-topic. (Same assessment as A-20.)

9. **Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning** (CONSENSUS, 0.027) -- On-topic. (Same assessment as A-1.)

10. **Be Your Own Red Teamer: Safety Alignment via Self-Play and Reflective Experience Replay** (B-ONLY, 0.027) -- On-topic. Self-play-based safety alignment replacing static red teaming. Directly in the seed community with an interesting self-improvement angle.

11. **MacPrompt: Maraconic-guided Jailbreak against Text-to-Image Models** (B-ONLY, 0.027) -- On-topic. Cross-lingual jailbreak for T2I models. Directly connects to seed 5. This is a good find.

12. **Attributing and Exploiting Safety Vectors through Global Optimization** (B-ONLY, 0.027) -- On-topic. Mechanistic analysis of safety in LLMs via global optimization of attention heads. Interesting interpretability-meets-safety paper. Connects to seed community with a deeper mechanistic angle.

13. **SafeThinker: Reasoning about Risk to Deepen Safety** (CONSENSUS, 0.025) -- On-topic. (Same assessment as A-4.)

14. **Emoji-Based Jailbreaking of LLMs** (CONSENSUS, 0.025) -- On-topic. (Same assessment as A-12.)

15. **JPU: Bridging Jailbreak Defense and Unlearning** (CONSENSUS, 0.025) -- On-topic. (Same assessment as A-11.)

16. **RECAP: Resource-Efficient Method for Adversarial Prompting** (CONSENSUS, 0.025) -- On-topic. (Same assessment as A-8.)

17. **Understanding and Preserving Safety in Fine-Tuned LLMs** (B-ONLY, 0.024) -- On-topic. Fine-tuning degrading safety alignment. Relevant to the broader safety concern, connects to seed community (how safety mechanisms break).

18. **STAR-S: Improving Safety Alignment through Self-Taught Reasoning on Safety Rules** (B-ONLY, 0.024) -- On-topic. Self-taught safety reasoning for jailbreak defense. Directly in the seed community. Connects to seed 3 (self-guided defense).

19. **ALERT: Zero-shot LLM Jailbreak Detection via Internal Discrepancy** (B-ONLY, 0.023) -- On-topic. Zero-shot jailbreak detection. Addresses a practical gap (detection without jailbreak templates). Directly in the seed community.

20. **MiJaBench: Revealing Minority Biases via Hate Speech Jailbreaking** (CONSENSUS, 0.023) -- On-topic. (Same assessment as A-10.)

---

## Part 2: Set-Level Assessment

### Strategy A

**Overall character**: Strategy A delivers an extremely focused set. All 20 papers are directly about LLM/multimodal jailbreak attacks or defenses. There are no false positives in any meaningful sense. The ranking is clean: highest-scored papers are the most directly relevant.

**Strengths**: (1) Zero noise. Every paper is in the target community. (2) Good balance of attack papers (5, 12, 13, 15, 16, 19), defense papers (1, 4, 7, 11), evaluation/analysis papers (2, 3, 6, 9, 10), and detection papers (18). (3) Covers the modality breadth of the seeds: LLMs, VLMs, and T2I models.

**Gaps**: (1) No papers on alignment theory, RLHF, or value specification -- but this reflects the seeds, not a retrieval failure. (2) No papers on safety governance or policy. (3) The set is so narrowly focused on jailbreaking that a researcher interested in the broader "AI safety" question would find it one-dimensional.

**False positive pattern**: None. This is a clean retrieval set.

### Strategy B

**Overall character**: Strategy B is also extremely focused, with all 20 papers directly about jailbreak attacks, defenses, or closely related safety mechanisms. The B-only papers are all strong, on-topic additions.

**Strengths**: (1) Also near-zero noise. (2) The B-only papers add genuinely useful diversity: self-play red teaming (10), cross-lingual T2I jailbreaking (11), mechanistic safety analysis (12), fine-tuning safety degradation (17), self-taught safety reasoning (18), and zero-shot detection (19). (3) These exclusive finds are individually as good as or better than A's exclusives.

**Gaps**: (1) Same fundamental gap as A: narrowly focused on jailbreaking, not broader safety/alignment. (2) The ranking is slightly less intuitive -- SafeThinker drops to rank 13 despite being a strong paper.

**False positive pattern**: None. This is also a clean retrieval set.

---

## Part 3: Comparative Assessment

**What A found that B missed**: AprielGuard (unified safeguard model), black-box jailbreaking of reasoning models, TrojanPraise (fine-tuning-based jailbreak), Latent Fusion Jailbreak (latent-space attack), detection of unseen jailbreak attacks in VLMs, and Adversarial Tales (narrative-based jailbreak). These are a mix of attack techniques and defense systems.

**What B found that A missed**: Self-play red teaming, MacPrompt (cross-lingual T2I jailbreak), safety vector attribution via global optimization, safety degradation through fine-tuning, self-taught safety reasoning (STAR-S), and zero-shot jailbreak detection (ALERT). These trend slightly more toward defense and analysis methods.

**Where they agree**: 14 of 20 papers overlap. This is the highest consensus rate across the three profiles. The agreement indicates that for a well-defined, narrow topic, both strategies converge on the same core literature. The consensus papers cover all the major sub-themes: attacks, defenses, evaluation, multimodal safety.

**Character of errors**: Neither strategy makes real errors here. The exclusive papers in both sets are genuinely relevant. The difference is more about which specific attack/defense papers get surfaced rather than a difference in retrieval quality. A's exclusives lean slightly more toward novel attack techniques; B's exclusives lean slightly more toward defense mechanisms and detection.

**If a researcher could only use one**: This is essentially a coin flip. Both sets are excellent. B's exclusives are arguably marginally more diverse in their sub-topic coverage (self-play, mechanistic analysis, zero-shot detection), but the difference is small. A's ranking is slightly more intuitive (top-ranked papers are the most broadly relevant). I would give a very slight edge to B for the diversity of its exclusive finds, but the margin is negligible.

---

## Part 4: Emergent Observations

1. **The profile is mislabeled**: The profile says "AI safety / alignment (Broad)" but the seeds are narrowly about LLM jailbreaking. Both strategies correctly follow the seeds rather than the label. A truly "broad" AI safety profile should include alignment theory, interpretability for safety, governance, and RLHF -- none of which appear. This is a data-generation issue, not a retrieval issue.

2. **High consensus rate is expected for narrow, well-defined topics**: With 70% overlap and zero false positives in either set, the two strategies are largely interchangeable for this profile. This suggests that for well-defined sub-communities with clear vocabulary, the choice of retrieval strategy matters less.

3. **Neither strategy escapes the jailbreak bubble**: A researcher who defined their interest with these five seed papers might actually want to see adjacent work (e.g., on RLHF methodology, or on interpretability tools that could explain jailbreak vulnerabilities). Neither strategy provides this kind of serendipitous broadening.

4. **The quality ceiling is high**: Both strategies achieve what could be described as near-perfect precision for the narrow interest. The challenge for this profile is not precision but recall and diversity.

---

## Part 5: Metric Divergence

The quantitative metrics said Strategy B (the fusion) performed worse than Strategy A (standalone). Qualitatively, **this verdict is questionable for P4**.

**Where metrics may mislead**: Both sets are near-perfect in precision. The MRR difference likely comes from rank ordering (e.g., Strategy A puts "Enhancing Model Defense" at rank 1, while B puts it at rank 9). But both rankings produce a top-20 that a jailbreak researcher would find equally valuable. The rank-ordering differences do not correspond to meaningful quality differences when every paper in both sets is relevant.

**What the metric misses**: Strategy B's exclusive papers (self-play red teaming, zero-shot detection, mechanistic safety analysis, safety through fine-tuning) are at least as interesting as A's exclusives (AprielGuard, Latent Fusion Jailbreak, Adversarial Tales). The qualitative impression is that B provides slightly more diverse coverage of the defense and detection sub-space. MRR does not capture this diversity advantage.

**Net assessment**: For P4, the quantitative verdict of B < A is not well-supported qualitatively. The two strategies are effectively equivalent, with B having a slight qualitative edge in sub-topic diversity that is invisible to MRR. The "losing" strategy does not feel worse; it may feel marginally better.
