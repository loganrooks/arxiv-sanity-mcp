# W4.1 Cold-Start Review: P4 (AI Safety / Alignment / Broad)

## Profile Context

P4 targets AI safety and alignment -- a broad domain that spans jailbreak attacks/defenses, alignment training, safety evaluation, red teaming, robustness, and the broader societal implications of LLMs. "Broad" means the profile encompasses many sub-areas under the AI safety umbrella.

---

## 1-Seed Condition

**Seed paper:** "Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning"

This seed is about LLM jailbreak defense using "Safety Chain-of-Thought" (SCoT) -- reasoning-based defense against adversarial attacks. Key concepts: jailbreak defense, safety alignment, reasoning capabilities, refusal training, adversarial robustness.

Despite P4 being labeled "broad," this seed is actually quite specific: it is about jailbreak defense for LLMs. The broader AI safety/alignment concerns (RLHF, value alignment, interpretability, fairness, governance) are not represented in this seed.

### Part 1: Per-Paper Assessment

#### MiniLM (1 seed)

1. **Self-Guided Defense: Adaptive Safety Alignment for Reasoning Models** -- Directly relevant. Safety alignment for reasoning models against jailbreaks. Nearly identical topic to seed. Would help refine: does user prefer defense methods or attack analysis?

2. **RAJ-PGA: Reasoning-Activated Jailbreak and Principle-Guided Alignment** -- Directly relevant. Both attack (RAJ) and defense (PGA) for reasoning models. Excellent cold-start probe: covers both sides of the jailbreak arms race.

3. **AprielGuard** -- Relevant. LLM moderation/safeguarding tool. Addresses same safety concerns from a tooling perspective.

4. **Exploring the Secondary Risks of Large Language Models** -- Relevant. Non-adversarial safety failures. Good diversification from the seed's jailbreak focus: helps probe whether user cares about broader safety risks beyond adversarial attacks.

5. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks via RL** -- Directly relevant. RL-based jailbreak attacks. Attack methodology paper.

6. **RECAP: Resource-Efficient Adversarial Prompting** -- Directly relevant. Adversarial prompting for LLMs. Attack methodology.

7. **SafeThinker: Reasoning about Risk to Deepen Safety** -- Directly relevant. Reasoning-based safety alignment. Nearly identical approach to seed (reasoning for safety).

8. **Jailbreaking Commercial Black-Box LLMs with Explicitly Harmful Prompts** -- Directly relevant. Black-box jailbreak attacks.

9. **One Trigger Token Is Enough: Defense Strategy** -- Directly relevant. Jailbreak defense via safety trigger tokens.

10. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** -- Directly relevant. Mechanistic understanding of jailbreaks.

11. **When Models Outthink Their Safety: Self-Jailbreak in Reasoning Models** -- Directly relevant. Self-jailbreak in reasoning models.

12. **Jailbreaking Attacks vs. Content Safety Filters** -- Directly relevant. Benchmarking jailbreak attacks vs. defenses.

13. **Reasoning Hijacking: Subverting LLM Classification** -- Relevant. Adversarial attack on LLM reasoning. Different attack vector but same safety domain.

14. **Defenses Against Prompt Attacks Learn Surface Heuristics** -- Directly relevant. Analysis of defense limitations.

15. **TrojanPraise: Jailbreak LLMs via Benign Fine-Tuning** -- Relevant. Fine-tuning-based jailbreak attack.

16. **TROJail: Trajectory-Level Optimization for Multi-Turn Jailbreaks** -- Directly relevant. Multi-turn jailbreak methodology.

17. **Latent Fusion Jailbreak** -- Directly relevant. Latent-space jailbreak attack.

18. **JPU: Bridging Jailbreak Defense and Unlearning** -- Directly relevant. Defense via machine unlearning.

19. **STAR-S: Improving Safety Alignment through Self-Taught Reasoning** -- Directly relevant. Reasoning-based safety alignment. Very close to seed.

20. **Thought-Transfer: Indirect Targeted Poisoning Attacks on CoT Models** -- Relevant. Poisoning attacks on reasoning models. Safety concern for CoT/reasoning.

**MiniLM 1-seed verdict:** 20/20 relevant. Every single paper is about LLM jailbreaks, safety alignment, or adversarial attacks on language models. This is an exceptional hit rate.

However, there is a critical qualitative concern: **the set is an echo chamber.** Nearly every paper is specifically about jailbreak attacks or defenses. There is almost no representation of:
- Alignment theory (RLHF, constitutional AI, value learning)
- Interpretability / mechanistic safety
- AI governance / policy
- Fairness, bias, or discrimination
- Safety of non-LLM AI systems

For a "broad" AI safety profile, this set is ironically very narrow. It is excellent for a "jailbreak researcher" profile but does not help the user discover the broader AI safety landscape. At cold start, this matters: the user who added a jailbreak defense paper might also care about alignment theory, but these recommendations will not help them discover that.

**For cold-start profile building:** The set is so homogeneous that saying "yes" or "no" to individual papers does not meaningfully differentiate. "Yes" to paper 1 vs. "yes" to paper 7 tells the system almost nothing new -- both are jailbreak defense papers using reasoning. The cold-start refinement value is low because there is no diversity to choose between.

#### TF-IDF (1 seed)

1. **Be Your Own Red Teamer: Safety Alignment via Self-Play** -- Directly relevant. Self-play for safety alignment. Introduces red teaming concept (slight diversification from seed).

2. **Self-Guided Defense** -- Same as MiniLM #1. Directly relevant.

3. **LLMs Can Unlearn Refusal with Only 1,000 Benign Samples** -- Relevant. Safety vulnerability through fine-tuning. Introduces the fine-tuning safety angle.

4. **RAJ-PGA** -- Same as MiniLM #2. Directly relevant.

5. **One Trigger Token Is Enough** -- Same as MiniLM #9. Directly relevant.

6. **Reasoning over Precedents Alongside Statutes: Case-Augmented Deliberative Alignment** -- Relevant. Deliberative alignment for safety. Introduces a different alignment paradigm. Good diversification.

7. **Overlooked Safety Vulnerability: Malicious Optimization Algorithm Request** -- Relevant. Novel attack vector via optimization algorithm requests.

8. **Adversarial Defense in Vision-Language Models: An Overview** -- Moderately relevant. VLM adversarial defense. Extends the safety concern beyond text-only LLMs. Good probe for whether user cares about multimodal safety.

9. **From Adversarial Poetry to Adversarial Tales: An Interpretability Research Agenda** -- Relevant. Culturally-coded jailbreaks + interpretability. Introduces the interpretability angle.

10. **When Models Outthink Their Safety** -- Same as MiniLM #11. Directly relevant.

11. **JPU** -- Same as MiniLM #18. Directly relevant.

12. **STAR-S** -- Same as MiniLM #19. Directly relevant.

13. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** -- Same as MiniLM #10. Directly relevant.

14. **Jailbreaking Safeguarded Text-to-Image Models via LLMs** -- Relevant. Safety of text-to-image models. Extends beyond text-only LLMs.

15. **MacPrompt: Maraconic-guided Jailbreak against Text-to-Image Models** -- Relevant. T2I model jailbreaks. Further multimodal safety coverage.

16. **Health-ORSC-Bench: Benchmark for Over-Refusal and Safety in Health Context** -- Relevant. Safety benchmarking in healthcare domain. Good diversification: introduces domain-specific safety and the over-refusal problem.

17. **SafeThinker** -- Same as MiniLM #7. Directly relevant.

18. **Reasoning While Asking: Transforming Reasoning LLMs from Passive Solvers to Proactive Inquirers** -- Weakly relevant. Reasoning methodology for LLMs. About proactive reasoning, which connects to the seed's "proactive safety reasoning" but is not itself about safety.

19. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks** -- Same as MiniLM #5. Directly relevant.

20. **GAMBIT: A Gamified Jailbreak Framework for Multimodal LLMs** -- Relevant. Multimodal LLM jailbreaks.

**TF-IDF 1-seed verdict:** 18/20 relevant, 1 moderately relevant, 1 weakly relevant, 0 clear misses. TF-IDF performs very well here. Notably, TF-IDF actually provides slightly better diversity than MiniLM: it includes text-to-image safety (#14, #15), healthcare safety benchmarking (#16), VLM adversarial defense (#8), and deliberative alignment (#6). These papers help the user explore beyond the jailbreak-specific niche.

### Part 2: Set-Level Cold-Start Assessment (1 seed)

**MiniLM:** The set is precise (20/20) but monotonous. A safety researcher would look at this and think "yes, this is my area" but would not learn anything new about the breadth of AI safety. Every paper is a variation on "jailbreak attack or defense for LLMs." For profile bootstrapping, this set offers poor leverage -- the user cannot meaningfully differentiate between papers to refine their profile. It is an echo chamber that confirms the seed without exploring the space.

**TF-IDF:** Slightly lower precision (18/20) but better diversity. The inclusion of T2I safety, healthcare safety benchmarks, VLM defense, and deliberative alignment gives the user more dimensions to react to. A researcher could say "yes to jailbreak defense but also yes to healthcare safety evaluation" and the profile would actually learn something. TF-IDF provides better cold-start refinement value despite marginally lower precision.

### Part 3: Strategy Comparison at Cold Start (1 seed)

This is the one profile where **TF-IDF arguably outperforms MiniLM at cold start.** MiniLM's precision is higher, but its diversity is lower, and diversity matters more at cold start when the goal is profile refinement. TF-IDF's broader term matching accidentally produces a more exploratory set that covers T2I safety, multimodal safety, and domain-specific safety applications.

Neither strategy produces garbage. Neither strategy explores the truly broad AI safety landscape (alignment theory, interpretability, governance). Both are anchored to jailbreaks.

The reason TF-IDF does better here: the seed's vocabulary ("safety," "defense," "jailbreak," "alignment," "LLM") is shared with many sub-areas of AI safety. TF-IDF's broader matching picks up T2I safety and healthcare safety because they share these terms. MiniLM's tighter semantic matching produces a more homogeneous set because jailbreak defense papers are semantically very similar to each other.

---

## 3-Seed Condition

**Seed papers:**
1. "Enhancing Model Defense Against Jailbreaks with Proactive Safety Reasoning" (same as 1-seed) -- jailbreak defense via reasoning
2. "One Trigger Token Is Enough: A Defense Strategy" -- jailbreak defense via safety trigger tokens
3. "Latent Fusion Jailbreak: Blending Harmful and Harmless Representations" -- latent-space jailbreak attack

All 3 seeds are about LLM jailbreaks. Two are defense papers, one is an attack paper. Despite having 3 seeds, the signal has not broadened at all -- if anything, it has narrowed further into the jailbreak sub-field. For a "broad" AI safety profile, this seed set is problematically narrow.

### Part 1: Per-Paper Assessment

#### MiniLM (3 seeds)

1. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks** -- Relevant. RL-based jailbreak.
2. **Exploring the Secondary Risks of LLMs** -- Relevant. Non-adversarial safety failures. One of the few papers that goes beyond jailbreaks.
3. **Jailbreaking Attacks vs. Content Safety Filters** -- Relevant. Jailbreak benchmarking.
4. **JPU: Bridging Jailbreak Defense and Unlearning** -- Relevant. Defense via unlearning.
5. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** -- Relevant. Mechanistic jailbreak analysis.
6. **TrojanPraise: Jailbreak LLMs via Benign Fine-Tuning** -- Relevant. Fine-tuning attack.
7. **SafeThinker** -- Relevant. Reasoning-based defense.
8. **Self-Guided Defense** -- Relevant. Reasoning model safety.
9. **AprielGuard** -- Relevant. LLM moderation.
10. **RAJ-PGA** -- Relevant. Reasoning model attack/defense.
11. **Jailbreaking Commercial Black-Box LLMs** -- Relevant. Black-box attacks.
12. **RECAP** -- Relevant. Adversarial prompting.
13. **How Real is Your Jailbreak? Fine-grained Evaluation** -- Relevant. Jailbreak evaluation methodology.
14. **Jailbreaking LLMs Without Gradients or Priors** -- Relevant. Gradient-free attacks.
15. **TROJail: Trajectory-Level Multi-Turn Jailbreaks** -- Relevant. Multi-turn attacks.
16. **Multi-turn Jailbreaking Attack in MLLMs** -- Relevant. Multimodal multi-turn attacks.
17. **Defenses Against Prompt Attacks Learn Surface Heuristics** -- Relevant. Defense limitation analysis.
18. **Beyond Prompts: Space-Time Decoupling Jailbreaks** -- Relevant. Structured output jailbreaks.
19. **Attributing and Exploiting Safety Vectors** -- Relevant. Safety internals analysis.
20. **From static to adaptive: immune memory-based jailbreak detection** -- Relevant. Adaptive jailbreak detection.

**MiniLM 3-seed verdict:** 20/20 relevant. But the echo chamber problem is now extreme. Every single paper is about jailbreaking or jailbreak defense. The 3-seed set is even more homogeneous than the 1-seed set because all 3 seeds reinforce the same signal. There is zero representation of alignment theory, interpretability, fairness, governance, or any other AI safety sub-field.

This is the cold-start problem in its purest form: if the user only has jailbreak papers as seeds, the system will only ever show them jailbreak papers. The user who is broadly interested in AI safety but started with jailbreak papers is trapped in a jailbreak recommendation loop.

#### TF-IDF (3 seeds)

1. **Jailbreaking Attacks vs. Content Safety Filters** -- Relevant.
2. **Self-Guided Defense** -- Relevant.
3. **Jailbreaking Safeguarded Text-to-Image Models via LLMs** -- Relevant. T2I safety.
4. **RAJ-PGA** -- Relevant.
5. **Be Your Own Red Teamer** -- Relevant. Red teaming approach.
6. **Overlooked Safety Vulnerability: Malicious Optimization Algorithm Request** -- Relevant. Novel attack vector.
7. **Attributing and Exploiting Safety Vectors** -- Relevant. Safety internals.
8. **STAR-S** -- Relevant. Reasoning-based alignment.
9. **Safety at One Shot: Patching Fine-Tuned LLMs** -- Relevant. Safety preservation during fine-tuning.
10. **JPU** -- Relevant.
11. **Understanding and Preserving Safety in Fine-Tuned LLMs** -- Relevant. Safety under fine-tuning.
12. **Unraveling LLM Jailbreaks Through Safety Knowledge Neurons** -- Relevant.
13. **MacPrompt: Maraconic-guided Jailbreak against T2I** -- Relevant. T2I safety.
14. **Jailbreaking LLMs through Iterative Tool-Disguised Attacks** -- Relevant.
15. **ALERT: Zero-shot LLM Jailbreak Detection** -- Relevant. Detection methodology.
16. **AsFT: Anchoring Safety During Fine-Tuning** -- Relevant. Safety preservation during fine-tuning.
17. **LLM Jailbreak Detection for (Almost) Free!** -- Relevant. Detection methodology.
18. **When Models Outthink Their Safety** -- Relevant.
19. **GAMBIT: Gamified Jailbreak for MLLMs** -- Relevant. Multimodal jailbreaks.
20. **From static to adaptive: immune memory-based jailbreak detection** -- Relevant.

**TF-IDF 3-seed verdict:** 20/20 relevant. TF-IDF also achieves perfect relevance at 3 seeds. Like MiniLM, it is entirely dominated by jailbreak papers. However, TF-IDF retains slightly more thematic diversity: it includes T2I safety (#3, #13), fine-tuning safety (#9, #11, #16), and detection methods (#15, #17). MiniLM's set is more uniformly about attack/defense methodology.

### Part 2: Set-Level Cold-Start Assessment (3 seeds)

**MiniLM:** 20/20 relevant but catastrophically narrow for a "broad" profile. The user is trapped in a jailbreak echo chamber. Adding 2 more jailbreak seeds did not broaden the recommendations -- it deepened the trench. A safety researcher interested in the full landscape would find this set comprehensive for jailbreaks but would wonder why the tool shows nothing about alignment, interpretability, or governance.

**TF-IDF:** Also 20/20 relevant and also narrow, but with slightly better coverage of adjacent concerns (fine-tuning safety, T2I safety, detection methods). The difference is marginal. Neither strategy escapes the jailbreak gravity well.

### Part 3: Strategy Comparison at Cold Start (3 seeds)

At 3 seeds, both strategies are effectively equivalent for P4: 20/20 relevant, dominated by jailbreaks, no escape from the narrow seed signal. TF-IDF has a slight edge in sub-topic diversity (fine-tuning safety, T2I safety, detection methods), but the difference would not meaningfully change the user experience.

The real finding is that **neither strategy can overcome a homogeneous seed set.** Three jailbreak seeds produce jailbreak recommendations. This is working as designed -- the strategies are finding similar papers -- but it reveals that cold-start quality depends more on seed selection than on strategy choice.

### Part 4: Emergent Observations

**The echo chamber problem is profile-type dependent.** For P1 (medium breadth, heterogeneous seeds), the 3-seed set shows productive diversity. For P4 (broad profile, homogeneous seeds), the 3-seed set is an echo chamber. The problem is not the strategy -- it is the interaction between profile breadth and seed homogeneity.

**Broad profiles are paradoxically hardest at cold start.** P4 is labeled "broad" but the available seeds are from one sub-area. A broad profile needs diverse seeds to cover its breadth, but a cold-start user may not know they need to provide diverse seeds. The system should detect seed homogeneity and actively recommend diversification.

**Jailbreak/safety papers have extremely similar abstracts.** Nearly every paper in this domain uses the same phrases: "jailbreak attacks," "safety alignment," "harmful content," "adversarial prompts," "defense mechanisms." This makes it genuinely hard for any retrieval strategy to differentiate within the field or to find adjacent-but-different safety work.

**MiniLM's high precision is actually a liability at cold start for this profile.** Because jailbreak papers are so semantically clustered, MiniLM finds a very tight neighborhood and stays there. TF-IDF's slightly noisier matching at least occasionally pulls in adjacent work (T2I, healthcare). For cold-start profile building, controlled noise is valuable.

### Part 5: Metric Divergence

The quantitative data says "MiniLM works from 1 seed." For P4, this claim is technically correct (20/20 relevant) but qualitatively misleading. "Works" in the sense of "returns relevant papers": yes. "Works" in the sense of "provides a useful cold-start experience for a broad AI safety researcher": no. The recommendations are relevant but not useful for profile building because they lack diversity.

The user would get a set of 20 papers about jailbreaks, confirm "yes, I care about jailbreaks," and then receive 20 more papers about jailbreaks. The system learns nothing it did not already know from the seed. This is a cold-start failure at the level of information gain, not relevance.

For this profile type, the metrics miss the critical quality dimension: **recommendation diversity matters more than recommendation relevance at cold start.** A set of 15 relevant + 5 adjacent-but-different papers would be more useful for profile building than 20 precisely relevant papers that are all variations on the same theme.
