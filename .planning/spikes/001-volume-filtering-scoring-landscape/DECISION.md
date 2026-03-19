# Spike 001 Decision: Volume, Filtering, and Scoring Landscape

**Date:** 2026-03-19
**Status:** Complete (with qualified limitations)

## Success Criteria Answers

### 1. What are the realistic paper volumes at each category configuration?

**Answer:** 19,252 papers/month at 15 configured categories (January 2026). Big4 (cs.LG, cs.CV, cs.CL, cs.AI) = ~12K/month. All CS = ~18K/month with 81% overlap. Per-category resource model built for interactive installer.

**Confidence:** High. Based on real OAI-PMH harvest data.

### 2. What does the arXiv landscape look like structurally for our categories?

**Answer:** Topic purity 0.40 — categories moderately align with topical clusters but not tightly. Only 1/48 BERTopic topics has high purity (>0.7). 60.6% of papers have multiple categories. 130 unique categories, Gini 0.83 (cs.LG/CV/CL dominate with 41% of papers). Zipf's law holds for vocabulary (4% of terms cover 80% of content).

**Confidence:** High for structure. The implication — that category-based pre-filtering will miss cross-domain papers — is supported by data but not validated against user preferences.

**Limitation:** Structure derived from one month (January 2026). Seasonal variation not captured.

### 3. Which 3-5 signals are most worth computing for paper scoring?

**Answer (from B1 literature + B2 computation):**
1. **Dense embedding similarity** (MiniLM and/or SPECTER2) — content-based discovery. Most adopted signal in recent systems (50.79%).
2. **FWCI** (field-weighted citation impact, from OpenAlex) — strongest non-tautological correlation with citations (r=0.75). Already in our enrichment schema.
3. **Citation count** (from OpenAlex) — most validated metadata signal across all surveyed systems. Near-zero for new papers — useful for established literature, not for triage of fresh papers.
4. **Bibliographic coupling** (reference overlap, from OpenAlex) — works for new papers with zero citations. Connected Papers' approach. Computable from existing data.
5. **User interaction signals** (seed papers, followed authors, triage behavior) — already in our schema. Strongest for personalization per B1 literature.

**Confidence:** Moderate. B1 literature evidence is strong. B2 computation was limited (460 papers, near-zero citations). The ranking of signals by importance depends on whether the user is triaging new papers (citation signals weak) or exploring established literature (citation signals strong).

**Limitation:** Content signals (topic novelty, abstract length, category entropy) showed near-zero correlation with citations — but this may reflect the weak importance proxy, not genuine signal weakness.

### 4. What shape is the coverage-regret tradeoff? Is there an elbow?

**Answer:** No sharp elbow. The tradeoff is smooth — increasing filter aggressiveness causes roughly proportional coverage loss. This means users need a configurable aggressiveness slider, not a fixed threshold.

Parameterized quality curves (C1-R8) show coherence degrades from 0.65 (top-20) to 0.18 (all 19K). The 200-500 paper range is where the tradeoff starts to bite for the "RL for Robotics" interest tested.

**Confidence:** Low-to-moderate. The coverage metric was measured against a near-zero citation proxy (unreliable). The quality metrics (coherence, diversity, novelty) are better measures but are mathematical properties of embedding space, not validated against user preferences. The null hypothesis tests showed that apparent model degradation was a simulation artifact.

**Limitation:** All coverage measurements should be interpreted as showing strategy *structure*, not absolute quality. Proper evaluation requires human relevance judgments.

### 5. What promotion strategy best fits our architectural values (ADR-0002)?

**Answer:** ADR-0002 says "enrich lazily, embed selectively." The data supports a two-layer architecture:

- **Ingestion layer** (wide net): User selects categories at install. All papers in those categories ingested. Category resource model provides volume estimates.
- **Promotion layer** (learned, per-project): From ingested papers, multiple strategies surface relevant papers. Strategies are selectable and combinable — not a single pipeline.

The "selective" in "embed selectively" can mean per-project: embed papers the user interacts with, or embed based on filtering score. Either approach is resource-feasible (C2).

**Confidence:** Moderate. The architectural recommendation is grounded in data, but the specific implementation (how strategies combine, how per-project profiles learn) is a design question for v0.2, not tested in this spike.

### 6. What are the approximate resource requirements for 1 year of operation?

**Answer (at 19K papers/month):**

| Strategy | GPU/day | CPU/day | Storage/year |
|----------|---------|---------|-------------|
| Triage-only embedding | 0.1s | 1.1s | 1.3 GB |
| Top 10% by filter | 0.1s | 2.2s | 1.3 GB |
| Embed all (MiniLM) | 1.1s | 22.5s | 1.6 GB |
| Embed all (SPECTER2) | 13s | — | 2.2 GB |
| Full OpenAlex enrich | — | 62s | — |

Per-category resource model provides estimates for any category selection:
- ML Researcher (4 categories): 10K/mo, 0.6s GPU/day, 723 MB/year
- Broad CS (10 categories): 14K/mo, 0.8s GPU/day, 1 GB/year

**Confidence:** High for compute costs (measured). Storage estimates assume current schema; actual may differ. All strategies are trivially feasible on any modern hardware.

### 7. What is the capability envelope for TF-IDF, embeddings, and concurrent access at our scale points?

**Answer:** See Spike 001 FINDINGS.md A1c section. All operations are feasible to 215K papers. FTS5 search <100ms to 500K. Embedding brute-force search 16ms at 215K. Concurrent R+W: zero degradation with WAL mode. mmap loading validated (0.2ms open, 47ms first query for 472MB).

**Confidence:** High. Direct measurements on real hardware.

### 8. At what corpus sizes do different NLP features become infeasible on a laptop (8-16 GB RAM)?

**Answer:** None of the tested features become infeasible at our measured scale (215K papers):
- TF-IDF matrix: 157 MB at 215K (trivial)
- Embeddings (MiniLM 384-dim): 315 MB at 215K
- Embeddings (SPECTER2 768-dim): 630 MB at 215K
- Combined: ~950 MB (fits in 8 GB with room)

Projected infeasibility point: ~2M papers for combined MiniLM+SPECTER2 embeddings (~6 GB). For a personal research tool, this is years of accumulation.

**Confidence:** Moderate. Extrapolated from 215K measurements. Real corpora may have different characteristics.

## Key Findings Beyond Success Criteria

### Recommendation strategies capture different dimensions of relatedness

12 strategies compared. No single strategy dominates. Different strategies excel at different definitions of "related":

| Definition | Best strategy | What it captures |
|---|---|---|
| Same authors | Co-author network (R@100=82%) | Social/collaborative proximity |
| Same niche | Rare category co-occurrence (50%) | Metadata structure |
| Same broad topic | BERTopic (47%) | Topical clustering |
| Similar content/language | MiniLM embedding (17%) | Semantic similarity |
| Same research conversation | SPECTER2 embedding (16%) | Citation-structure proximity |

**Implication:** The recommendation system should offer multiple strategies as selectable profiles, each tagged with what kind of relatedness it captures. This maps to ADR-0001 (exploration-first, multiple strategies coexist) and the existing InterestProfile architecture.

### Embedding models are complementary, not competing

Qualitative review (3 seeds, 15 papers each) showed:
- MiniLM finds papers using similar language (topical precision)
- SPECTER2 finds papers from adjacent research communities using different vocabulary (discovery potential)
- Consensus papers (both agree) are more category-similar to seed (0.40 vs 0.32)
- Best papers for each seed are distributed across consensus, MiniLM-only, and SPECTER2-only sets

**Implication:** System should use both models and expose the distinction to users.

### "Quality" is not one dimension

Three distinct values emerged from qualitative analysis:
1. **Topical precision** — does the paper study the same specific problem?
2. **Methodological kinship** — does the paper use the same formal tools?
3. **Discovery potential** — would this paper surprise the researcher and open new directions?

A single "relevance score" collapses these dimensions and loses information.

## Critical Limitations

1. **SPECTER2 loaded improperly throughout all experiments.** Used `SentenceTransformer('allenai/specter2_base')` which falls back to mean pooling without the proximity adapter. Proper adapter changes ~35% of top-20 recommendations (Spearman 0.78). All SPECTER2 comparisons must be re-evaluated with proper loading. **Spike 003 required.**

2. **No human relevance judgments.** All evaluations use mathematical proxies (category overlap, cluster membership, embedding similarity) or AI-agent qualitative review. None uses domain expert judgment. The AI review is informative but not authoritative.

3. **Near-zero citation proxy.** January 2026 papers have <2 months to accumulate citations. All coverage/importance measurements are unreliable as absolute values. Signal structure (correlations) is more informative than absolute predictions.

4. **One month of data.** All findings are based on January 2026. Seasonal variation, conference deadline effects, and longer-term trends not captured.

5. **Evaluation frameworks can favor specific approaches by construction.** This was caught multiple times during this spike (see signals). The fair cross-model evaluation addressed it for embedding comparison, but other comparisons (e.g., R@K on category groups) may still have hidden biases favoring metadata-based strategies.

## Open Questions for Spike 003

1. Does proper SPECTER2 (with proximity adapter) change the embedding comparison?
2. What do cross-encoder reranking and LLM-based relevance scoring add?
3. Systematic cross-profiling of all strategies across multiple evaluation frameworks
4. Per-strategy quality profiles with explicit valuation framework
5. Does the multi-strategy architecture actually help a real user find papers?

## Recommendation for v0.2

Design the recommendation system as a **multi-strategy, per-project architecture**:

```
Per Project:
├── Ingestion: user-selected categories (wide net)
├── Strategies (selectable, combinable):
│   ├── Content similarity (MiniLM) → "papers about similar topics"
│   ├── Research context (SPECTER2) → "papers from related conversations"
│   ├── Keyword match (FTS/TF-IDF) → "papers using these terms"
│   ├── Personal taste (SVM on library) → "papers like ones you've saved"
│   ├── Citation network (bibcoupling) → "papers sharing your references"
│   └── Author network → "papers by researchers you follow"
├── Each recommendation tagged with WHY it was found
├── Consensus badge when 2+ strategies agree
└── User-configurable aggressiveness slider (top-100 focused → top-2000 broad)
```

This is grounded in:
- B1: hybrid systems dominate in production (55.56%)
- Qualitative review: best papers distributed across strategy-exclusive sets
- B3: importance is multi-dimensional → multi-axis display
- ADR-0001: exploration-first, multiple strategies coexist
- C2: all strategies are resource-feasible
