# W1 Cross-Strategy Characterization Summary

## Overview

9 qualitative reviews conducted: 3 strategies (S1a MiniLM, S1c SPECTER2 adapter, S1d TF-IDF) x 3 profiles (P1 RL for Robotics / Medium, P3 Quantum ML / Narrow, P4 AI Safety / Broad).

Each review assessed 20 recommended papers for relevance, discovery value, and failure patterns. This summary synthesizes the findings into cross-strategy insights.

## Aggregate Statistics

| Metric | S1a MiniLM | S1c SPECTER2 | S1d TF-IDF |
|--------|-----------|--------------|------------|
| Avg score spread | 0.053 | 0.009 | 0.072 |
| Total held-out recovered (across 3 profiles) | 2/15 | 0/15 | 5/15 |
| Total profile papers in top-20 | 8 | 3 | 11 |
| Avg on-topic rate (estimated) | ~80% | ~70% | ~80% |
| Unique papers (not in other strategies' top-20) | 24/60 | 25/60 | 28/60 |

## Per-Profile Strategy Winner

### P1: RL for Robotics (Medium breadth)

**Most useful set: TF-IDF (S1d)**

TF-IDF produces the most useful set because it:
- Recovers the only held-out paper any strategy found (quadrupedal locomotion)
- Finds papers in RL sub-areas (safe RL, control-theoretic RL, failure recovery) that both embedding models miss entirely
- Has fewer false positives from the imitation learning / behavior cloning / VLA paradigm that floods both embedding models
- Surfaces 12-14 genuinely RL-focused papers vs 8-10 for the embeddings

MiniLM and SPECTER2 are roughly comparable for P1. Both suffer from conflating RL with other policy learning paradigms. SPECTER2 adds cross-community papers (Lipschitz critics, policy bootstrapping) that MiniLM misses, but these are marginal gains.

**Key insight:** For a medium-breadth topic where the interest (RL) overlaps heavily with adjacent topics (imitation learning, behavior cloning) in vocabulary, TF-IDF's literal keyword matching paradoxically outperforms semantic embeddings because it can distinguish papers that explicitly mention "reinforcement learning" from those that do not.

### P3: Quantum ML (Narrow breadth)

**Most useful set: MiniLM (S1a)**

MiniLM dominates for this narrow profile:
- 16-17 on-topic papers vs 10-12 for SPECTER2 and TF-IDF
- The quantum ML vocabulary is distinctive enough that MiniLM's semantic matching achieves high precision
- Includes both theoretical (barren plateaus, spectral bias) and practical (hardware deployment, pruning) papers
- Only 2-3 false positives vs 5-6 for TF-IDF and SPECTER2

SPECTER2 is the weakest here: its citation-graph breadth brings in quantum computing infrastructure papers (optimization, circuit theory, signal processing) that dilute the quantum ML focus. Worse, it has a clear false positive (hdlib, a classical computing library). TF-IDF is intermediate: it finds the right field but not always the right subfield.

**Key insight:** For narrow topics with distinctive vocabulary, MiniLM's semantic matching is precise and effective. The narrower the interest, the more MiniLM's dominance grows, because there are fewer adjacent topics to confuse with.

### P4: AI Safety/Jailbreaking (Broad label, narrow seeds)

**Most useful set: Depends on the user's actual need.**

This profile reveals a three-way split:
- **TF-IDF** for highest recall: 3/5 held-out, 5 profile papers, zero false positives
- **MiniLM** for balanced attack-defense coverage: 2/5 held-out, includes defense analysis and interpretability
- **SPECTER2** for community infrastructure: evaluation benchmarks, production defenses, emerging attack surfaces

If the user wants "find me all the jailbreaking papers I might have missed," TF-IDF is the answer. If they want "help me understand the jailbreaking landscape," MiniLM provides the most balanced picture. If they want "show me what the safety research community is building," SPECTER2 surfaces the infrastructure.

**Key insight:** For hot, active topics with massive publication volume, the strategies' qualitative differences become strategic rather than quality differences. All three produce excellent on-topic results; they differ in *which slice* of the literature they emphasize.

## Cross-Profile Analysis: Does the answer change by breadth?

**Yes, dramatically.**

| Profile breadth | Best strategy | Why |
|----------------|---------------|-----|
| Narrow (P3) | MiniLM | Distinctive vocabulary enables precise semantic matching |
| Medium (P1) | TF-IDF | Distinguishes RL from adjacent paradigms via keyword presence |
| Broad/Hot (P4) | All competitive | Large paper pool means all strategies find relevant papers |

The key variable is not breadth per se but **vocabulary distinctiveness relative to adjacent topics.**

- P3 (quantum ML) has highly distinctive vocabulary ("variational quantum circuit," "parameterized quantum circuit," "qubit"). Adjacent topics (quantum optimization, quantum chemistry) use different terms. MiniLM excels.
- P1 (RL for robotics) has vocabulary that overlaps heavily with adjacent topics (imitation learning, behavior cloning). "Policy," "robot," "manipulation," "sim-to-real" appear in both RL and non-RL robot learning papers. TF-IDF's literal matching on "reinforcement learning" outperforms semantic similarity, which blurs the RL/IL boundary.
- P4 (AI safety/jailbreaking) has very distinctive vocabulary ("jailbreak," "adversarial prompt," "safety alignment") AND a massive paper pool. All strategies can find relevant papers easily.

**This is the most actionable finding:** The optimal strategy depends on the interest's vocabulary overlap with adjacent topics, not on the strategy's intrinsic quality.

## Cross-Strategy Comparison Matrix

### Character

| Dimension | S1a MiniLM | S1c SPECTER2 | S1d TF-IDF |
|-----------|-----------|--------------|------------|
| **Feels like...** | A well-read colleague who knows the semantic neighborhood but sometimes conflates related-sounding work | A department librarian who knows who cites whom but cannot rank within a community | A keyword search with intelligent ranking -- literal but precise |
| **Best at finding...** | Papers semantically similar to your seeds, especially for narrow/distinctive topics | Cross-community papers, field infrastructure (benchmarks, production tools), well-connected work from major labs | Papers using exact same terminology as your seeds, papers you would find by keyword search but ranked by relevance |
| **Blind to...** | Papers that describe the same concept with different vocabulary; papers from adjacent paradigms that should not be included but share terms | Papers outside the citation community; papers at the edges of the field; fine-grained relevance distinctions | Papers that use different terminology for the same concepts; papers whose relevance is conceptual rather than terminological |
| **Typical false positive** | Adjacent-paradigm papers (imitation learning in an RL search) | Papers from adjacent subfields within the same community (quantum optimization in a quantum ML search); occasional wild misfires (hdlib) | Papers that mention the keywords without being primarily about the topic (VLA papers mentioning "RL") |
| **Score interpretation** | Moderate spread (~0.05); ranking is somewhat meaningful | Near-zero spread (~0.01); ranking is meaningless noise | Wide spread (~0.07); ranking carries genuine information |

### Quantitative Summary

| Metric | S1a MiniLM | S1c SPECTER2 | S1d TF-IDF |
|--------|-----------|--------------|------------|
| LOO-MRR (quantitative) | 0.398 | 0.184 | 0.104 |
| Held-out recovery (qualitative) | 2/15 (13%) | 0/15 (0%) | 5/15 (33%) |
| Profile paper recovery | 8/15 (53%) | 3/15 (20%) | 11/15 (73%) |
| Estimated false positive rate | ~20% | ~30% | ~20% |

## The Critical Question: Does SPECTER2's qualitative character justify keeping it despite lower MRR?

**Answer: Yes, but not as a primary strategy. SPECTER2 provides a unique signal that the other two cannot.**

### The case for SPECTER2:

1. **Cross-community discovery.** SPECTER2 uniquely surfaces papers that are relevant because they are connected in the academic discourse (cited by the same community, published by overlapping author groups) rather than because they use similar words or concepts. The Lipschitz critics paper (P1, pure RL theory applicable to sim-to-real) and the Constitutional Classifiers++ paper (P4, production defense from Anthropic) are examples that neither MiniLM nor TF-IDF would find.

2. **Field infrastructure papers.** Benchmarks, evaluation frameworks, and production tools tend to have different vocabulary from the research papers they support. SPECTER2 catches them through citation-graph proximity.

3. **Emerging attack surface extensions.** For P4, SPECTER2 uniquely finds papers extending safety concerns to new deployment contexts (MCP, RAG, agentic systems). These papers share the safety community but not the exact jailbreaking vocabulary.

### The case against SPECTER2 as primary:

1. **Score compression makes ranking useless.** Average spread of 0.009 means SPECTER2 cannot distinguish between its #1 and its #1000 recommendation. Any user-facing presentation would need a different ranking signal.

2. **0/15 held-out recovery.** SPECTER2 fails to recover any independently-identified relevant papers across all three profiles. This is a significant reliability concern.

3. **Noise in the proximity signal.** The hdlib false positive (P3, a classical computing library ranked in the top-10 of a quantum ML profile) reveals that SPECTER2's similarity surface has unexplained noise. Trust in individual recommendations is lower.

4. **Worse for narrow interests.** When the research interest is specific enough to exclude adjacent fields, SPECTER2's breadth becomes a liability.

### Recommendation:

SPECTER2 should be a **secondary/supplementary signal**, not a primary retrieval strategy. Its value is in providing diversity and cross-community discovery that MiniLM and TF-IDF miss. Possible implementation patterns:
- Use MiniLM or TF-IDF as primary retrieval, then boost papers that SPECTER2 also ranks highly
- Dedicate a "discovery" section of recommendations to SPECTER2-unique papers
- Use SPECTER2 agreement as a confidence signal: papers ranked highly by both MiniLM and SPECTER2 are more likely to be relevant across multiple dimensions

## The MRR Bias Question

**Is MiniLM's 2x MRR advantage real when you look at the actual papers?**

**No.** The MRR advantage is partly real and partly an artifact of evaluation framework bias.

### What is real:
- MiniLM produces more focused, on-topic recommendation sets for narrow profiles (P3)
- MiniLM recovers more held-out papers than SPECTER2 (2/15 vs 0/15)
- MiniLM's score spread enables meaningful ranking; SPECTER2's does not

### What is artifact:
- The LOO-MRR evaluation uses embedding-defined clusters that inherently favor embedding-based strategies. TF-IDF scores 0.104 despite being qualitatively competitive with MiniLM
- MiniLM's 2x advantage over SPECTER2 in MRR does not translate to a 2x quality advantage in the actual recommendation sets. For P1 (medium), the sets are roughly comparable; for P4 (broad), SPECTER2 surfaces different but equally valuable papers
- TF-IDF's 4x MRR deficit relative to MiniLM is the most egregious bias: TF-IDF outperforms both embedding strategies on held-out recovery (the most objective quality measure available) while scoring lowest on MRR

### Corrected ranking:
The strategies are better described as **complementary** than as ranked. Each captures a different quality dimension:
- MiniLM: semantic precision, especially for narrow/distinctive topics
- SPECTER2: community connectivity, cross-field discovery
- TF-IDF: keyword precision, held-out recovery, methodological diversity

A system using any single strategy is leaving value on the table. The combination of at least two strategies (MiniLM + TF-IDF, or all three) would substantially outperform any individual strategy.

## Emergent Quality Dimensions

Beyond the 7 quantitative instruments (LOO-MRR, coherence, diversity, novelty, seed-relevance, coverage, redundancy), the qualitative reviews surfaced these additional quality dimensions:

1. **Methodological precision:** Does the strategy distinguish between the target methodology and adjacent methodologies? (RL vs imitation learning, quantum ML vs quantum optimization)

2. **Score informativeness:** Does the strategy's score carry ranking information, or is it essentially flat? (TF-IDF > MiniLM >> SPECTER2)

3. **Discovery breadth:** Does the strategy surface papers the researcher would not find through simple keyword search or citation following? (SPECTER2 > MiniLM > TF-IDF)

4. **Community representation:** Does the strategy capture the field's infrastructure (benchmarks, tools, production systems), not just individual contributions? (SPECTER2 > MiniLM > TF-IDF)

5. **Paradigm sensitivity:** Does the strategy over-represent the current dominant paradigm (VLA, diffusion policies, etc.) at the expense of less fashionable but valuable work? (All strategies are susceptible; TF-IDF least so)

6. **Held-out recall:** Does the strategy recover papers that were independently identified as relevant? (TF-IDF > MiniLM > SPECTER2)

7. **Seed sensitivity:** How much does the recommendation set depend on the specific seeds chosen vs the broader topic? (All strategies are highly seed-dependent; this is a structural limitation of centroid approaches)

## Implications for Strategy Configuration

1. **Default single-strategy recommendation: MiniLM (S1a).** It is the most reliably good strategy across profile types, with the fewest catastrophic failure modes.

2. **When to prefer TF-IDF:** Medium-breadth topics where the interest overlaps with adjacent paradigms; when held-out recall matters; when the user wants keyword-precise recommendations.

3. **When SPECTER2 adds value:** As a supplementary signal for cross-community discovery; for identifying field infrastructure and emerging research directions; when the user explicitly requests "show me what I would miss."

4. **Optimal combination: MiniLM + TF-IDF as dual primary, SPECTER2 as discovery boost.** This gives semantic precision + keyword precision + community connectivity. The overlap between MiniLM and TF-IDF is moderate (7-8 out of 20 shared), meaning the combination covers substantially more ground than either alone.
