# W1 Characterization Review: S1c (SPECTER2 adapter) x P4 (AI Safety)

**Strategy:** S1c -- SPECTER2 with proximity adapter, cosine similarity centroid
**Profile:** P4 -- AI safety / alignment (Broad breadth, 10 seeds)
**Score range:** 0.982 -- 0.966 (spread: 0.015)
**Held-out recovery:** 0/5
**Profile papers in top-20:** 0

## Part 1: Per-Paper Assessment

**#1 Exploring the Secondary Risks of LLMs (2506.12382) -- 0.982**
Broader LLM safety risks beyond jailbreaking. MiniLM #2. Good recommendation that contextualizes jailbreaking within larger safety concerns.

**#2 Effective and Efficient Jailbreaks of Black-Box LLMs (2503.08990) -- 0.976**
Black-box jailbreak attack methodology. On-topic. UNIQUE to SPECTER2 in the top-20 (not in MiniLM's top-20).

**#3 Jailbreak-Zero: Pareto Optimal Red Teaming (2601.03265) -- 0.976**
Red teaming methodology. On-topic. MiniLM #11.

**#4 SPECTRE: Conditional System Prompt Poisoning (2505.16888) -- 0.975**
Supply-chain attack via system prompt poisoning. On-topic and UNIQUE to SPECTER2. This extends beyond direct jailbreaking to supply-chain security -- a broader safety concern. Good discovery for expanding the attack surface understanding.

**#5 RECAP: Resource-Efficient Adversarial Prompting (2601.15331) -- 0.974**
Efficient adversarial prompts. On-topic. MiniLM #9.

**#6 Jailbreaking LLMs through Iterative Tool-Disguised Attacks (2601.05466) -- 0.973**
RL-based jailbreak. On-topic. MiniLM #1. SPECTER2 ranks it #6 vs MiniLM's #1 -- significant rank disagreement on a clearly on-topic paper.

**#7 ICON: Intent-Context Coupling for Multi-Turn Jailbreak (2601.20903) -- 0.973**
Multi-turn jailbreak attack. UNIQUE to SPECTER2. On-topic -- extends the multi-turn attack methodology.

**#8 SafeThinker: Reasoning about Risk (2601.16506) -- 0.971**
Deep safety alignment via risk reasoning. On-topic. MiniLM #3.

**#9 Sockpuppetting: Jailbreaking via Output Prefix Injection (2601.13359) -- 0.971**
Prefix injection jailbreak. On-topic. MiniLM #20.

**#10 RedBench: Universal Dataset for Red Teaming (2601.03699) -- 0.970**
Red teaming benchmark dataset. UNIQUE to SPECTER2. Valuable infrastructure paper: standardized evaluation for safety research. A researcher would use this for their evaluations.

**#11 RoguePrompt: Dual-Layer Ciphering for Self-Reconstruction (2511.18790) -- 0.970**
Cipher-based jailbreak method. UNIQUE to SPECTER2. Novel attack vector using encoding/ciphering to bypass safety.

**#12 Constitutional Classifiers++: Efficient Production-Grade Defenses (2601.04603) -- 0.970**
Production-grade jailbreak defense (Anthropic). UNIQUE to SPECTER2. This is a significant paper from a major lab about deploying safety at scale. Important for any safety researcher to know about.

**#13 TROJail: Trajectory-Level Multi-Turn Jailbreaks (2512.07761) -- 0.969**
Multi-turn jailbreak optimization. On-topic. MiniLM #14.

**#14 Emoji-Based Jailbreaking of LLMs (2601.00936) -- 0.969**
Emoji-based jailbreak attacks. On-topic. Novel attack modality.

**#15 Knowledge-Driven Multi-Turn Jailbreaking (2601.05445) -- 0.969**
Knowledge-guided multi-turn attacks. UNIQUE to SPECTER2. Extends multi-turn methodology with knowledge-driven context building.

**#16 How Real is Your Jailbreak? Fine-grained Jailbreak Evaluation (2601.03288) -- 0.968**
Jailbreak evaluation methodology. UNIQUE to SPECTER2. Meta-methodological contribution about how to assess jailbreak success. Important for the field's evaluation standards.

**#17 MacPrompt: Maraconic-guided Jailbreak against T2I Models (2601.07141) -- 0.967**
T2I model jailbreaking. On-topic but different modality. MiniLM did not include this.

**#18 Attributing and Exploiting Safety Vectors in LLMs (2601.15801) -- 0.967**
Mechanistic analysis of safety in LLMs. UNIQUE to SPECTER2. Interpretability-focused safety research -- finding the components that implement safety behavior. Connects jailbreaking to mechanistic understanding.

**#19 MCP-Guard: Defense Framework for Model Context Protocol (2508.10991) -- 0.967**
Safety framework for MCP-based agentic systems. UNIQUE to SPECTER2. Extends safety concerns to the agentic AI deployment context. Relevant and timely -- most safety research focuses on chat interfaces, but this addresses tool-using agents.

**#20 Overcoming the Retrieval Barrier: Indirect Prompt Injection (2601.07072) -- 0.966**
Indirect prompt injection in RAG systems. UNIQUE to SPECTER2. Extends jailbreaking to retrieval-augmented systems. Another extension of the attack surface to deployment contexts.

## Part 2: Set-Level Assessment

**Overall character:** Like MiniLM, SPECTER2 produces a near-perfect on-topic set (19-20 out of 20 relevant). But the specific papers differ in an important way: SPECTER2 includes more infrastructure and methodology papers (benchmarks, evaluation frameworks, production defenses) and more attack-surface-extension papers (supply-chain poisoning, indirect prompt injection, MCP security, agentic AI safety). Where MiniLM stays tightly focused on the attack-defense dynamic within jailbreaking, SPECTER2 reaches toward the broader safety ecosystem.

**Strengths:**
- Every paper is relevant to LLM safety/jailbreaking
- Better coverage of the safety infrastructure (RedBench #10, Constitutional Classifiers++ #12, evaluation methodology #16)
- Surfaces emerging attack surfaces (supply-chain #4, MCP/agentic #19, retrieval systems #20) that MiniLM misses
- More methodologically diverse attack papers (cipher-based, emoji-based, knowledge-driven)
- Constitutional Classifiers++ (#12) is an important industry paper -- SPECTER2's citation-graph signal likely catches well-cited papers from major labs

**Gaps:**
- 0/5 held-out papers recovered (vs MiniLM's 2/5) -- a significant disadvantage
- 0 profile papers in top-20 -- none of the broader profile papers appear
- Missing the interpretability-jailbreaking connection that MiniLM finds (#5 Safety Knowledge Neurons)
- Replaces MiniLM's fine-grained ranking with essentially flat scores (0.015 spread)

**False positive pattern:** Virtually none. The jailbreaking/safety topic is tight enough and SPECTER2's citation graph connects papers within this community very well.

**Failure mode:** Score compression remains (0.015 spread) but is less extreme than P1 or P3. For a very active research area with many papers, SPECTER2 has slightly more dynamic range. But the 0/5 held-out recovery is worse than MiniLM's 2/5.

## Part 4: Emergent Observations

1. **SPECTER2 finds the "field infrastructure" papers that MiniLM misses.** RedBench (benchmark dataset), Constitutional Classifiers++ (production defense), "How Real is Your Jailbreak?" (evaluation methodology) -- these are the papers that define how the field works, not individual contributions. SPECTER2's citation-graph proximity captures these because they are heavily cited within the community. This is a genuinely different quality dimension from MiniLM's "semantic similarity to the seeds" -- it is more like "centrality within the research community."

2. **Attack surface extension is SPECTER2's unique discovery type.** Supply-chain poisoning, MCP security, indirect prompt injection, retrieval-system attacks -- these extend the jailbreaking concern to new deployment contexts. SPECTER2 finds these because the citation graph connects researchers who work on different attack surfaces but share the safety community. MiniLM misses them because the abstract vocabulary is slightly different (e.g., "prompt injection" vs "jailbreak" vs "adversarial attack").

3. **The 0/5 held-out recovery is damning.** Despite producing an excellent recommendation set qualitatively, SPECTER2 fails to recover ANY held-out papers. This suggests that SPECTER2's citation-graph proximity creates a bubble effect: it finds papers that are well-connected within the existing community graph but may miss papers that are slightly outside the core (newer papers, cross-community papers). The held-out papers, being manually selected to represent the broader profile, may be at the edges of the citation graph.

4. **Profile label vs seed content matters more for broad profiles.** The "AI safety / alignment (Broad)" label suggests the researcher wants to know about alignment theory, scalable oversight, interpretability for safety, governance, etc. But the seeds are all jailbreaking papers. Both MiniLM and SPECTER2 faithfully follow the seeds, not the label. For a broad interest, the user would need to provide broadly-representative seeds, or the system would need to interpret the label rather than just the seeds.

## Part 5: Metric Divergence

The qualitative impression is closer than the metrics suggest. SPECTER2's set is not 2x worse than MiniLM's (as the MRR ratio implies). It is *differently focused*: more on community infrastructure and attack surface extension, less on the specific attack-defense papers that are closest to the seeds. For a researcher who already knows the core jailbreaking literature and wants to understand emerging threats and evaluation standards, SPECTER2's set might actually be more useful than MiniLM's.

However, the 0/5 vs 2/5 held-out recovery is a real quality difference, not a measurement artifact. SPECTER2's citation-graph proximity seems to create a tighter community boundary than MiniLM's semantic similarity, which is counterintuitive -- one would expect citation graphs to be broader than semantic similarity. This may be because SPECTER2's extreme score compression means the community-boundary papers that should appear in the top-20 are lost in a sea of equally-scored papers.

The 0 profile papers in SPECTER2's top-20 (vs 3 in MiniLM's) further supports MiniLM's advantage for this profile. MiniLM finds more of the papers that were independently identified as relevant to the profile.
