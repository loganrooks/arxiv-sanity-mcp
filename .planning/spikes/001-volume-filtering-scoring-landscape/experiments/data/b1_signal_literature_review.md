# B1: Signal Literature Review — Findings

**Date:** 2026-03-19
**Method:** Reviewed 6 production systems + 2 comprehensive surveys (covering 117 systems, 2019-2024)

## Key Findings

### Signal Adoption Rates (2021-2024, from survey of 63 systems)

1. **Citations** — 78.72% of relational systems
2. **Title + abstract text** — 68.75% each
3. **Dense embeddings** — 50.79% (growing, replacing TF-IDF)
4. **Author information** — 37.5-51%
5. **User interactions** — 34.04%
6. **TF-IDF** — ~6% (declining)

### Production System Approaches

| System | Primary Approach | Key Signals |
|--------|-----------------|-------------|
| arxiv-sanity-lite | TF-IDF + per-user SVM | TF-IDF bigrams, user tags, weighted field search (title 20x, author 10x) |
| Semantic Scholar | SPECTER2 embeddings + LightGBM reranker | Citation-graph-trained embeddings, user library, "not relevant" feedback |
| Google Scholar | Citation-dominant ranking | Citation count (highest weight), title match, author name |
| ResearchRabbit | Pure graph-based | Co-citation, bibliographic coupling, co-authorship (no content analysis) |
| Connected Papers | Co-citation + bibliographic coupling | Jaccard on co-citing/reference sets, publication year proximity |
| Elicit | SPLADE + LLM reranking | Sparse learned embeddings, deliberately ignores citation count |

### Importance Hierarchy (from literature + production evidence)

1. **Content similarity** — universal baseline, works for cold start
2. **Citation structure** — most powerful enrichment, unavailable for new papers
3. **User personalization** — strongest for individual relevance
4. **Author/venue metadata** — supplementary, risk of prestige bias
5. **Temporal signals** — necessary for freshness, secondary to relevance

### Availability Assessment for Our Architecture

**Already available (Tier 1):** TF-IDF, embeddings, FTS5/tsvector, recency, user signals (seed papers, followed authors, saved queries, triage state)

**Available via OpenAlex (Tier 2):** Citation count, FWCI, citation percentile, author h-index, topics, referenced works, related works, publication type

**Not feasible now (Tier 3):** Co-citation analysis (expensive), co-readership (needs multi-user data), social media mentions (API costs), full graph centrality

### Highest-Value Additions (impact/effort ratio)

1. **Dense embedding similarity** — already benchmarked, SPECTER2 is SOTA for scientific docs
2. **Citation count** — already in enrichment schema, most validated metadata signal
3. **FWCI** — already in enrichment schema, better than raw citation for cross-field
4. **Bibliographic coupling** — computable from OpenAlex referenced_works, works for new papers
5. **Author h-index** — available via OpenAlex, supplementary signal

### SPECTER2 vs MiniLM

SPECTER2 (allenai/specter2) is trained on citation graph structure via contrastive learning — encodes citation network position into embeddings even for papers with zero citations. This is a fundamentally different approach from MiniLM which uses general sentence similarity. SPECTER2 is 768-dim (vs MiniLM 384-dim), doubling compute and storage costs but providing domain-specific quality.

### Sources

- Survey: "Recent Advances and Trends in Research Paper Recommender Systems" (arXiv:2508.08828, 2025) — 63 systems
- Survey: "Scientific paper recommendation systems: a literature review" (PMC9533296, 2022) — 54 systems
- Production: arxiv-sanity-lite (GitHub), Semantic Scholar FAQ, Connected Papers about page, ResearchRabbit AI docs, Elicit blog, Google Scholar ranking (Beel & Gipp 2009)
