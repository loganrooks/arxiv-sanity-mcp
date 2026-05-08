# W1 Characterization Review: S1a (MiniLM centroid) x P4 (AI Safety)

**Strategy:** S1a -- MiniLM all-MiniLM-L6-v2 centroid, dot-product ranking
**Profile:** P4 -- AI safety / alignment (Broad breadth, 10 seeds)
**Score range:** 0.711 -- 0.658 (spread: 0.053)
**Held-out recovery:** 2/5 (Unraveling LLM Jailbreaks, RAJ-PGA)
**Profile papers in top-20:** 3

## Seeds Summary

The 10 seeds are overwhelmingly about LLM jailbreaking and safety alignment: jailbreak attacks (GCG variants, multi-modal, prompt injection), defenses (proactive reasoning, self-guided alignment, trigger tokens), and evaluation (safety arms race benchmarking, politically controversial content). The "broad" designation is debatable for the seed set -- it is actually quite narrow within AI safety, focusing heavily on jailbreaking rather than broader alignment concerns (value alignment, RLHF theory, interpretability, AI governance, existential risk). This will constrain all three strategies.

## Part 1: Per-Paper Assessment

**#1 Jailbreaking LLMs through Iterative Tool-Disguised Attacks via RL (2601.05466) -- 0.711**
RL-based jailbreak attack method. Directly on-topic: this is a jailbreak attack paper. A researcher studying LLM safety/jailbreaking would absolutely want this.

**#2 Exploring the Secondary Risks of LLMs (2506.12382) -- 0.707**
Beyond jailbreaking -- examining downstream safety risks. Slightly broader than the seed focus. This is a valuable recommendation because it contextualizes jailbreaking within a broader safety landscape. Good discovery for expanding perspective.

**#3 SafeThinker: Reasoning about Risk for Deep Safety (2601.16506) -- 0.698**
Defense against disguised attacks via risk reasoning. On-topic: a defense paper that addresses the attack-defense dynamic the seeds explore. Strong recommendation.

**#4 JPU: Bridging Jailbreak Defense and Unlearning (2601.03005) -- 0.694, profile paper**
Jailbreak defense via machine unlearning. On-topic. Connects two safety subfields (jailbreaking and unlearning) that are usually separate.

**#5 Unraveling LLM Jailbreaks Through Safety Knowledge Neurons (2509.01631) -- 0.692, HELD-OUT**
Mechanistic interpretability of jailbreak vulnerability. HELD-OUT paper recovered. Excellent find: this connects jailbreaking to interpretability, which is a broader safety concern the seeds do not directly address.

**#6 AprielGuard (2512.20293) -- 0.687**
LLM safety moderation system. On-topic: a practical defense/moderation tool. A researcher would want to know about production-grade defenses.

**#7 Jailbreaking Commercial Black-Box LLMs with Explicit Harmful Prompts (2508.10390) -- 0.687**
Black-box jailbreak attacks including reasoning models. On-topic. Advances the attack methodology the profile is tracking.

**#8 TrojanPraise: Jailbreak LLMs via Benign Fine-Tuning (2601.12460) -- 0.686**
Fine-tuning-based jailbreak. On-topic. A different attack vector (training-time vs inference-time) that broadens understanding.

**#9 RECAP: Resource-Efficient Adversarial Prompting (2601.15331) -- 0.684**
Efficient adversarial prompt generation. On-topic. Methodological contribution to jailbreak attack efficiency.

**#10 RAJ-PGA: Reasoning-Activated Jailbreak and Alignment for Large Reasoning Models (2508.12897) -- 0.673, HELD-OUT**
Safety of reasoning models (LRMs). HELD-OUT paper recovered. Important extension of jailbreaking to reasoning models -- a critical emerging area.

**#11 Jailbreak-Zero: Pareto Optimal Red Teaming (2601.03265) -- 0.673**
Red teaming methodology. On-topic. Shifts from finding specific jailbreaks to systematic safety evaluation.

**#12 Multi-turn Jailbreaking Attack in Multi-Modal LLMs (2601.05339) -- 0.669**
Multi-modal, multi-turn jailbreaking. On-topic. Extends the attack surface to multi-modal models.

**#13 Jailbreaking LLMs Without Gradients or Priors (2601.03420) -- 0.669**
Gradient-free jailbreak attacks. On-topic. A methodological variant.

**#14 TROJail: Trajectory-Level Optimization for Multi-Turn Jailbreaks (2512.07761) -- 0.668**
Multi-turn jailbreak with process rewards. On-topic. RL-based attack optimization.

**#15 Beyond Prompts: Space-Time Decoupling Control-Plane Jailbreaks (2503.24191) -- 0.664**
Structural jailbreaks via output formatting. On-topic. Novel attack vector through structured output APIs.

**#16 Jailbreaking Safeguarded Text-to-Image Models via LLMs (2503.01839) -- 0.661**
Jailbreaking T2I safety filters. On-topic but extends to a different modality (image generation).

**#17 Defenses Against Prompt Attacks Learn Surface Heuristics (2601.07185) -- 0.660**
Analysis of why defenses fail. On-topic and potentially high-value: a meta-analysis of defense strategies revealing fundamental limitations.

**#18 ALERT: Zero-shot Jailbreak Detection (2601.03600) -- 0.659**
Jailbreak detection method. On-topic. Practical defense contribution.

**#19 MiJaBench: Minority Biases via Hate Speech Jailbreaking (2601.04389) -- 0.659**
Jailbreaking as a tool to evaluate bias. Broadens the scope: uses jailbreaking methodology to study a different problem (bias evaluation). Interesting cross-application.

**#20 Sockpuppetting: Jailbreaking via Output Prefix Injection (2601.13359) -- 0.658**
Prefix injection jailbreak for open-weight models. On-topic. Attack methodology.

## Part 2: Set-Level Assessment

**Overall character:** An extraordinarily focused and high-quality set. Arguably 19-20 out of 20 papers are directly relevant to the research interest. This is the highest on-topic rate of any review. The set is dominated by jailbreaking attack and defense papers, with a few papers that broaden into related safety concerns (secondary risks, bias evaluation, interpretability).

**Strengths:**
- Near-perfect topical relevance
- Good balance of attack papers (#1, #7, #8, #9, #12, #13, #14, #15, #20) and defense papers (#3, #4, #6, #17, #18)
- Recovers 2/5 held-out papers -- the best held-out recovery for any embedding strategy across all profiles
- Includes papers that broaden beyond pure jailbreaking (#2 secondary risks, #5 safety neurons, #19 bias)
- Strong diversity within the topic: different attack vectors (RL-based, tool-disguised, fine-tuning, multi-turn, multi-modal, prefix injection)

**Gaps:**
- Almost exclusively about jailbreaking specifically. The "AI safety" framing of the profile could include: RLHF theory, constitutional AI, AI governance, interpretability, value alignment, scalable oversight, AI existential risk. None of these appear.
- No papers about the broader alignment research program
- The set reinforces the narrow reading of the seeds rather than expanding toward the broader topic label

**False positive pattern:** Essentially none. Every paper is on-topic.

**Failure mode:** Over-convergence. The set is so focused on jailbreaking that it functions as a "jailbreaking paper feed" rather than an "AI safety research feed." This is a direct consequence of the seeds being almost entirely jailbreaking papers. MiniLM faithfully reproduces the seeds' focus rather than interpreting "AI safety" more broadly.

## Part 4: Emergent Observations

1. **Broad profiles with narrow seeds produce narrow recommendations.** Despite being labeled "broad," this profile's seeds are narrow (all jailbreaking). MiniLM recommends more jailbreaking papers. This is the correct behavior for a centroid approach (find papers like the seeds) but not necessarily what a user labeled "AI safety - broad" actually wants. The mismatch between the profile label and the seed selection is a research design issue, not a strategy failure, but it reveals how sensitive centroid approaches are to seed selection.

2. **The highest top-20 score (0.711) correlates with the narrowest effective topic.** P4 has the highest MiniLM top score despite being labeled "broad." This is because the seeds cluster tightly in a jailbreaking sub-neighborhood of the embedding space, producing a centroid that is very close to many papers. The "breadth" of a profile should be measured by centroid spread, not by label.

3. **MiniLM excels when the topic is a hot research area with many papers.** Jailbreaking is one of the most active LLM research areas in 2025-2026, producing hundreds of papers per month. MiniLM can be extremely selective when there is a large pool to choose from. For niche topics (quantum ML), it has less to work with.

4. **The two held-out recoveries are both mechanistically interesting.** Safety Knowledge Neurons (#5) connects jailbreaking to interpretability; RAJ-PGA (#10) extends to reasoning models. These are the held-out papers that represent extensions of the core topic rather than repetitions of it. MiniLM finds them because they still share substantial vocabulary with jailbreaking papers.

## Part 5: Metric Divergence

For P4, MiniLM's quantitative advantage over SPECTER2 appears to be genuine and substantial. The recommendation set is tight, relevant, and well-ranked (the top-scored papers are the most relevant). The 2/5 held-out recovery is the best of any embedding strategy.

However, the set's extreme focus on jailbreaking raises a different concern: is this set useful for an "AI safety" researcher, or only for a "jailbreaking" researcher? The quantitative metrics cannot distinguish between a set that is precisely relevant to a narrow reading of the profile and a set that is broadly useful for the intended research interest. For a genuinely broad AI safety research interest, SPECTER2 or TF-IDF might provide more useful diversity.
