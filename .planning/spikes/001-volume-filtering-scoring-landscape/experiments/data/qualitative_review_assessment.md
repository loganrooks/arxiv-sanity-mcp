# Qualitative Review: MiniLM vs SPECTER2 Recommendation Quality

**Date:** 2026-03-19
**Method:** AI agent reviewed titles + abstracts for 3 seed papers × 3 recommendation sets (consensus, MiniLM-only, SPECTER2-only)
**Limitation:** AI reviewer, not domain expert. Assessment based on abstract analysis, not full paper reading.

## Key Findings

### The models capture genuinely different dimensions of relatedness

| Dimension | MiniLM | SPECTER2 |
|---|---|---|
| **What it captures** | Semantic/lexical similarity — papers using similar language | Citation-structural proximity — papers in the same research conversation |
| **Strength** | Topical precision (especially in fields with distinctive vocabulary) | Cross-community discovery (papers using different vocabulary for same problem) |
| **Weakness** | Vocabulary squatters — papers sharing words but not research questions | Community neighbors — papers from same community but different problems |
| **False positive type** | Easy to spot (wrong topic, similar words) | Harder to spot (right community, wrong problem) |

### Both models contribute unique value

For each seed, the best papers were distributed across all three sets:

**Seed 1 (Quantum generative models):**
- Best MiniLM-only: "Arbitrary Polynomial Separations in Trainable QML" — same theoretical question, same vocabulary
- Best SPECTER2-only: "Random-Matrix-Induced Simplicity Bias in VQCs" — explains a mechanism the seed likely discusses, different framing
- Neither alone would find both

**Seed 2 (Axiomatic AGI):**
- Best MiniLM-only: "The Relativity of AGI" — methodologically identical (axiomatizing AGI), same vocabulary
- Best SPECTER2-only: "Minary Primitive of Computational Autopoiesis" — same problem, completely different vocabulary (autopoiesis vs self-organizing networks)
- SPECTER2's unique contribution is precisely the cross-pollination value: papers a researcher would never find by keyword search

**Seed 3 (Neural network approximation):**
- MiniLM dominated: "Linear Regions," "Functional Dimension," "IC-MLP Universal Approximation" — all precisely on-topic
- SPECTER2 added peripheral awareness: KANs, RBF networks — alternative approaches to the same mathematical question
- In narrow technical fields, MiniLM's vocabulary matching is highly reliable

### "Quality" is not one thing

At least three distinct notions emerged:
1. **Topical precision** — does the paper study the same specific problem?
2. **Methodological kinship** — does the paper use the same formal tools?
3. **Discovery potential** — would this paper surprise the researcher and open new directions?

MiniLM optimizes for (1). SPECTER2 optimizes for (3). Both contribute to (2).

### Recommendation for the system

A system that surfaces:
- **Consensus papers** as high-confidence recommendations (both models agree)
- **Model-exclusive papers** as "explore these" recommendations (one model's unique contribution)
- Labels indicating WHY each paper was recommended (topical similarity vs research community proximity)

would serve researchers better than choosing a single model.

## Per-Paper Ratings

### Seed 1: Quantum generative models
| Set | Paper | Rating |
|-----|-------|--------|
| Consensus | Exponential capacity scaling of QGANs | Highly relevant |
| Consensus | Detecting underdetermination in PQCs | Relevant |
| Consensus | Adversarial Robustness in QML | Tangentially relevant |
| MiniLM-only | Arbitrary Polynomial Separations | **Highly relevant** |
| MiniLM-only | Sample-Efficient Optimization | Tangentially relevant |
| SPECTER2-only | VQC Simplicity Bias | **Highly relevant** |
| SPECTER2-only | Brain quantum effects | Not relevant |

### Seed 2: Axiomatic AGI
| Set | Paper | Rating |
|-----|-------|--------|
| Consensus | Cognition spaces | Highly relevant |
| Consensus | Systems Explaining Systems | Highly relevant |
| MiniLM-only | Relativity of AGI | **Highly relevant** |
| MiniLM-only | Information Physics of Intelligence | **Highly relevant** |
| SPECTER2-only | Geometric Theory of Cognition | **Highly relevant** |
| SPECTER2-only | Minary Primitive | **Highly relevant** |

### Seed 3: Neural network approximation
| Set | Paper | Rating |
|-----|-------|--------|
| Consensus | Two-hidden-layer ReLU + finite elements | **Highly relevant** |
| MiniLM-only | Counting Linear Regions | **Highly relevant** |
| MiniLM-only | Functional Dimension of ReLU NNs | **Highly relevant** |
| SPECTER2-only | Sparse RBF Networks | Relevant |
| SPECTER2-only | KANs (Architectural Scaling) | Relevant |
