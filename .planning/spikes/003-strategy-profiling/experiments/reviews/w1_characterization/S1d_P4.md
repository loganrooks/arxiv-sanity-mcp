# W1 Characterization Review: S1d (TF-IDF centroid) x P4 (AI Safety)

**Strategy:** S1d -- TF-IDF (50K features, sublinear TF, English stopwords), cosine similarity centroid
**Profile:** P4 -- AI safety / alignment (Broad breadth, 10 seeds)
**Score range:** 0.423 -- 0.300 (spread: 0.124)
**Held-out recovery:** 3/5 (RAJ-PGA, Unraveling LLM Jailbreaks, Overlooked Safety Vulnerability)
**Profile papers in top-20:** 5

## Part 1: Per-Paper Assessment

**#1 Jailbreaking Safeguarded T2I Models via LLMs (2503.01839) -- 0.423**
Jailbreaking text-to-image safety filters using LLMs. On-topic. MiniLM #16, SPECTER2 did not include. TF-IDF ranks it #1 because of dense keyword overlap: "jailbreak" + "safeguard" + "large language model" + "safety" + "harmful" appear in both the seeds and this abstract. The high TF-IDF score (0.423, much higher than the rest) suggests this paper shares an unusually large vocabulary intersection with the seed centroid.

**#2 Jailbreaking LLMs through Iterative Tool-Disguised Attacks via RL (2601.05466) -- 0.343**
RL-based jailbreak. On-topic. MiniLM #1. TF-IDF agrees on its relevance.

**#3 Be Your Own Red Teamer: Self-Play and Reflective Experience Replay (2601.10589) -- 0.340, profile paper**
Self-play safety alignment. On-topic and UNIQUE to TF-IDF in top-20. Interesting approach: the model red-teams itself. A researcher in safety/alignment would want this for its defense methodology.

**#4 Jailbreak-Zero: Pareto Optimal Red Teaming (2601.03265) -- 0.339**
Red teaming methodology. On-topic. MiniLM #11.

**#5 RAJ-PGA: Reasoning-Activated Jailbreak and Alignment (2508.12897) -- 0.338, HELD-OUT**
Safety of reasoning models. HELD-OUT recovered. MiniLM also recovered this (#10). On-topic.

**#6 Emoji-Based Jailbreaking (2601.00936) -- 0.329**
Emoji jailbreaking. On-topic. Novel attack.

**#7 MacPrompt: Maraconic-guided Jailbreak against T2I (2601.07141) -- 0.327**
T2I jailbreaking. On-topic. SPECTER2 #17.

**#8 Unraveling LLM Jailbreaks Through Safety Knowledge Neurons (2509.01631) -- 0.321, HELD-OUT**
Interpretability of jailbreak vulnerability. HELD-OUT recovered. MiniLM also recovered this (#5). On-topic.

**#9 GCG Attack On A Diffusion LLM (2601.14266) -- 0.315**
Adversarial attacks on diffusion-based language models. UNIQUE to TF-IDF. Extends jailbreaking to a different LLM architecture (diffusion vs autoregressive). Relevant and a natural extension of the GCG attack methodology mentioned in the seeds.

**#10 Effective and Efficient Jailbreaks of Black-Box LLMs (2503.08990) -- 0.313**
Black-box jailbreaking. On-topic. SPECTER2 #2.

**#11 Overlooked Safety Vulnerability in LLMs: Malicious Optimization Algorithm Request (2601.00213) -- 0.309, HELD-OUT**
Safety vulnerability through optimization algorithm requests. HELD-OUT recovered -- the third held-out paper. UNIQUE to TF-IDF. This paper addresses an unusual attack vector: requesting LLMs to generate malicious optimization algorithms. TF-IDF finds it because of keyword overlap ("safety" + "vulnerability" + "jailbreak" + "large language model").

**#12 LLMStinger: Jailbreaking LLMs using RL (2411.08862) -- 0.308**
RL-based jailbreaking. UNIQUE to TF-IDF. On-topic -- another RL-based attack method, complementing #2.

**#13 LLM Jailbreak Detection for (Almost) Free! (2509.14558) -- 0.305**
Efficient jailbreak detection. UNIQUE to TF-IDF. On-topic defense paper. Practical detection method with low computational cost.

**#14 TROJail: Trajectory-Level Multi-Turn Jailbreaks (2512.07761) -- 0.302**
Multi-turn jailbreak optimization. On-topic. MiniLM #14.

**#15 From Static to Adaptive: Immune Memory-Based Jailbreak Detection (2512.03356) -- 0.302**
Adaptive jailbreak detection inspired by immune systems. UNIQUE to TF-IDF. Novel defense methodology. A researcher in AI safety would find the bio-inspired approach interesting.

**#16 SpatialJB: Text Distribution Art as Jailbreak Key (2601.09321) -- 0.302, profile paper**
Visual/spatial jailbreak technique. On-topic. UNIQUE to TF-IDF.

**#17 RECAP: Resource-Efficient Adversarial Prompting (2601.15331) -- 0.300**
Efficient adversarial prompts. On-topic. MiniLM #9.

**#18 Exploring the Secondary Risks of LLMs (2506.12382) -- 0.300**
Broader LLM safety risks. On-topic. MiniLM #2.

**#19 Dynamic Target Attack (2510.02422) -- 0.300**
Improved adversarial suffix optimization. UNIQUE to TF-IDF. On-topic: improves on the GCG attack methodology by optimizing the target response rather than using a fixed affirmative.

**#20 GAMBIT: Gamified Jailbreak for Multimodal LLMs (2601.03416) -- 0.300**
Gamification-based multimodal jailbreak. UNIQUE to TF-IDF. On-topic: extends jailbreaking to multimodal context using game-like interaction.

## Part 2: Set-Level Assessment

**Overall character:** 20/20 papers are on-topic. Every single paper in TF-IDF's recommendation set is directly relevant to jailbreaking / LLM safety. This matches MiniLM's near-perfect precision for this profile. The set is more attack-heavy (14 attacks, 4 defenses, 2 broader safety) compared to MiniLM's more balanced mix.

**Strengths:**
- 3/5 held-out papers recovered -- the highest of any strategy on any profile
- 5 profile papers in top-20 -- the highest recovery of profile-designated papers
- Strong coverage of diverse attack vectors: RL-based, emoji, visual/spatial, tool-disguised, multi-turn, GCG variants, diffusion LLMs
- Every paper is unambiguously on-topic

**Gaps:**
- Heavily attack-focused; underrepresents defenses and safety infrastructure
- Missing the "field infrastructure" papers SPECTER2 finds (benchmarks, evaluation methodology, production defenses like Constitutional Classifiers++)
- No papers about broader safety alignment (same limitation as all strategies)
- Weaker on the "why jailbreaks work" mechanistic understanding papers

**False positive pattern:** None. Zero false positives.

**Failure mode:** Attack saturation. The jailbreaking vocabulary is so distinctive ("jailbreak" + "LLM" + "adversarial" + "safety" + "harmful") that TF-IDF finds a large pool of papers with high keyword overlap, and most of them are attack papers because attacks dominate the publication volume.

## Part 4: Emergent Observations

1. **TF-IDF dominates held-out recovery.** 3/5 for P4, 1/5 for P1 and P3 -- TF-IDF consistently recovers more held-out papers than either embedding strategy. This is the strongest systematic finding across all reviews. The held-out papers were selected independently by the profile design process, so this is a form of external validation. TF-IDF's keyword matching finds papers that are "obviously relevant" based on shared terminology, which is precisely what held-out papers tend to be.

2. **The score spread is diagnostic.** TF-IDF's 0.124 spread for P4 is the widest of any strategy-profile combination across all 9 reviews. The top-1 paper (T2I jailbreaking, score 0.423) is dramatically more keyword-similar to the seeds than the top-20 paper (score 0.300). This means TF-IDF's ranking carries genuine information: papers ranked higher share more specific vocabulary with the seeds. Compare this to SPECTER2's 0.015 spread (8x less) and MiniLM's 0.053 spread (2.4x less). TF-IDF makes the sharpest relevance distinctions.

3. **Attack paper dominance reflects the publication landscape.** The imbalance toward attack papers (14/20 attacks vs 4/20 defenses) is not a strategy failure -- it reflects the actual publication ratio in the jailbreaking literature. Attack papers outnumber defense papers roughly 3:1 in this corpus window (January 2026). A recommendation system built purely on centroid similarity will reproduce this ratio. A user wanting balanced attack-defense coverage would need explicit diversity constraints.

4. **The #1 score outlier reveals TF-IDF's "term density" bias.** The T2I jailbreaking paper at #1 has a score 0.08 higher than #2, a large gap. This paper likely uses an unusually high concentration of the exact terms that appear in the seed centroid ("jailbreak," "safety," "adversarial," "harmful," "prompt," "model"). TF-IDF rewards papers that repeat the centroid's vocabulary, which can favor papers with dense keyword usage over more subtle or original work. This is the inverse of the embedding models' tendency to favor semantically similar but lexically diverse papers.

5. **TF-IDF finds what keyword search would find, but ranked.** A researcher could get many of these papers by searching for "jailbreak LLM safety" in any index. TF-IDF's value-add over simple keyword search is the centroid ranking: it ranks papers by how well they match the profile's vocabulary distribution, not just the presence of keywords. But the fundamental character of the results is "keyword search with intelligent ranking."

## Part 5: Metric Divergence

TF-IDF's LOO-MRR of 0.104 is the lowest, yet for P4 specifically, TF-IDF produces the most useful recommendation set by objective measures: 3/5 held-out recovery, 5 profile papers, 0 false positives. The MRR metric dramatically underrates TF-IDF for this profile.

The explanation is the same as for other profiles: LOO-MRR uses embedding-defined clusters that favor embedding-based strategies. But for P4, the magnitude of the divergence is largest because the topic vocabulary is so distinctive. "Jailbreak" + "LLM" + "safety" is almost a perfect keyword query for this profile, and TF-IDF excels at keyword matching.

This profile provides the strongest evidence that the quantitative metrics are systematically biased against TF-IDF. A strategy that recovers 3/5 held-out papers and 5 profile papers should not be rated 4x worse than strategies that recover 0-2/5.
