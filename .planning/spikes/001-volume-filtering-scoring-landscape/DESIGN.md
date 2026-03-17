---
question: "What does the arXiv paper landscape look like for our configured categories, what signals predict paper importance, and how do different filtering/promotion strategies trade off volume against coverage?"
type: exploratory
status: in_progress
round: 1
linked_deliberation: deployment-portability.md
linked_questions:
  - "docs/10-open-questions.md Q16: Processing promotion strategy"
  - "docs/10-open-questions.md Q17: Retrospective demotion"
---

# Spike 001: Volume, Filtering, and Scoring Landscape

## Question

What does the arXiv paper landscape look like for our configured categories? What signals — both raw and computed — predict paper importance? How do different filtering and promotion strategies trade off volume against coverage?

## Why This Matters

We need empirical understanding before making architectural decisions about:
- Backend choice (SQLite vs PostgreSQL — depends on expected corpus size)
- Promotion pipeline design (depends on which scoring signals exist and work)
- Filtering strategy (depends on the volume-quality tradeoff shape)
- User-facing tier recommendations (depends on all of the above)
- **Capability envelope** (what compute/storage operations are feasible at what scale on what hardware)

We currently have partial empirical data (volume and FTS5 search). This spike continues exploring the landscape before we commit to any particular approach.

## Background

### What the architecture currently says
- **ADR-0002:** "Ingest metadata eagerly, enrich lazily, embed selectively"
- **Ingestion filtering:** Category-only (categories.toml: 15 categories across cs, stat, math, eess)
- **Promotion:** Demand-driven only — entirely manual
- **Processing tiers:** METADATA_ONLY(0) → FTS_INDEXED(1) → ENRICHED(2) → EMBEDDED(3) → CONTENT_PARSED(4)

### What we don't know
- ~~The actual volume dynamics of our pipeline at realistic scale~~ → **Measured (A1)**
- What the corpus looks like structurally (clusters, distributions, outliers)
- Which features — raw or computed — correlate with paper importance
- Whether "importance" is even one thing or multiple dimensions
- What the coverage-regret tradeoff looks like at different filtering levels
- How different promotion strategies compare in resource requirements
- **Whether TF-IDF recommendation features fit in RAM at our expected corpus sizes**
- **Whether SQLite can serve reads during concurrent writes (harvest daemon + MCP coexistence)**
- **Whether lightweight embeddings are feasible without pgvector at personal scale**

### Key discovery during deliberation (2026-03-14)
The NLP intelligence layer (TF-IDF, SVM, embeddings) runs in Python, not the database. The database is storage. This means the "SQLite vs PostgreSQL" question is narrower than assumed — it's about storage and indexing, not about the scoring/recommendation capabilities. This discovery expanded the spike scope: we now need to measure the capability envelope of these Python-side operations to understand what's feasible at different hardware levels.

## Design Principles

1. **Explore before operationalize.** Don't define "important paper = >50 citations" upfront. Let the data reveal what importance looks like.
2. **Compute signals, don't just read them.** Metadata fields are inputs. Interesting signals are often derived (author network centrality, category entropy, temporal patterns).
3. **Visualize before quantify.** Maps and distributions reveal structure that summary statistics hide.
4. **Leave room for emergence.** The most interesting findings will be things we didn't think to look for.
5. **Measure the envelope, not just the product.** Before designing a feature, measure whether its prerequisites are feasible on target hardware. Don't build a TF-IDF recommendation system and then discover the matrix doesn't fit in RAM on a laptop.

## Progress

| Experiment | Status | Key Finding | Script |
|-----------|--------|-------------|--------|
| A1: Volume Mapping | **Complete** | Big4 = 12K/month, All CS = 18K/month, 81% overlap | `a1_volume_mapping.py` |
| A1b: FTS5 Search Benchmark | **Complete** | <40ms p50 at 215K papers, linear scaling | `a1_fts5_benchmark.py` |
| A1c.1: TF-IDF Matrix Benchmark | **Complete** | 157 MB at 215K; cosine search 516ms (bottleneck is compute, not RAM) | `a1c_tfidf_benchmark.py` |
| A1c.2: Concurrent SQLite R+W | **Complete** | WAL mode: zero degradation at 100 writes/s. Non-issue. | `a1c_concurrent_sqlite.py` |
| A1c.3: Lightweight Embeddings | **Complete** | 16ms search at 215K (no pgvector needed). GPU 20x faster for compute. | `a1c_embedding_benchmark.py` |
| A2: Corpus Visualization | Pending | — | — |
| A2b: Interactive Explorer | Pending | — | — |
| A3: Distribution Analysis | Pending | — | — |
| B1: Signal Literature Review | Pending | — | — |
| B2: Computed Signal Exploration | Pending | — | — |
| B3: Importance Analysis | Pending | — | — |
| C1: Coverage-Regret Analysis | Pending | — | — |
| C2: Promotion Pipeline Sim | Pending | — | — |
| C3: Backend Implications | Pending | — | — |

## Scope Evolution

The original DESIGN.md covered three phases (A: landscape, B: signals, C: tradeoffs). During the deployment-portability deliberation (2026-03-14), we discovered that the NLP layer is independent of the database — TF-IDF, SVM, and embeddings all run in Python. This expanded the spike scope in two ways:

1. **New experiments (A1b, A1c):** We need to measure the capability envelope of key operations (FTS5 search, TF-IDF matrices, concurrent access, embeddings) at our measured scale points to understand what's feasible on different hardware. These determine whether proposed deployment tiers are realistic.

2. **New success criteria:** The spike now also needs to answer "what can this hardware actually do?" — not just "what does the data look like?" These capability measurements feed directly into the deployment-portability deliberation's tier recommendations.

This is a natural extension of an exploratory spike (the reference says exploratory spikes "can refine during spike as understanding grows"). The capability experiments share the A1 dataset and scale methodology, and their findings are prerequisites for Phase C (tradeoff mapping).

## Phases

This spike has three phases. Each phase's design may be refined based on previous phase findings.

### Phase A: Landscape Exploration

**Objective:** Understand what our slice of arXiv looks like — volume, structure, distributions, clusters — and what compute/storage operations are feasible at those volumes.

---

**A1: Volume Mapping** — COMPLETE

- Harvested 1 calendar month of real data (January 2026) at three category configs
- 19,252 unique papers in `experiments/data/spike_001_harvest.db`
- See FINDINGS.md for full results

---

**A1b: FTS5 Search Performance Benchmark** — COMPLETE

- Measured SQLite FTS5 search latency at 7 scale points (5K–500K)
- Used duplicated paper data (preserves text distribution, vocabulary limited to 19K unique)
- See FINDINGS.md for full results

---

**A1c: Capability Envelope Benchmarks** — IN PROGRESS

These experiments measure whether key computational operations are feasible at our measured corpus sizes. Each tests a specific capability that a deployment tier might depend on.

**A1c.1: TF-IDF Matrix Benchmark** — COMPLETE

*Question:* What are the memory footprint and rebuild time of a TF-IDF matrix at our scale points? At what corpus size does it stop fitting comfortably in RAM?

*Why it matters:* arxiv-sanity-lite's core recommendation loop is TF-IDF + SVM. If TF-IDF matrices fit in RAM at 50K–215K papers, content-based recommendation is feasible on a laptop without a database. If they don't, the recommendation architecture needs a different approach (approximate, segmented, or database-side).

*Results:* Memory is trivial (157 MB at 215K). Cosine search is the bottleneck (516ms at 215K, crosses 100ms around 50-75K). See FINDINGS.md for full data.

**A1c.2: Concurrent SQLite Read+Write** — COMPLETE

*Question:* What happens to search latency when another process is writing papers simultaneously?

*Why it matters:* In normal operation, the harvest daemon writes new papers while the MCP server handles search queries. SQLite uses file-level locking. WAL mode allows concurrent reads during writes, but contention is possible. If search latency degrades significantly during writes, the MCP server and harvester can't coexist on the same SQLite database — which undermines Tier 1's "single-file simplicity" value proposition.

*Results:* WAL mode completely eliminates the problem. Search p50 stays 1.3-1.6ms at 0-100 writes/s. Zero lock errors. DELETE mode with unbatched writes is catastrophic (p95=3.7s at 100/s). See FINDINGS.md for full data.

**A1c.3: Lightweight Embedding Benchmark** — COMPLETE

*Question:* What are the compute time, memory, and brute-force search characteristics of lightweight sentence embeddings at our scale points?

*Why it matters:* Semantic search is a v2 feature. The deliberation's tier model assumes pgvector is needed for semantic search. But at personal scale (<50K papers), brute-force cosine similarity over pre-computed embeddings might be fast enough — which would mean semantic search works on SQLite too. This fundamentally changes the tier differentiation story.

*Results:* Brute-force embedding search is 16ms at 215K papers — 30x faster than TF-IDF cosine. pgvector is unnecessary at personal scale. GPU provides 20x embedding speedup (1.7ms vs 35ms per paper). Memory is 315 MB float32 at 215K. See FINDINGS.md for full data.

---

**A2: Corpus Visualization and Structure** — PENDING

- Using the harvested sample, explore the corpus structure:
  - Topic modeling (LDA or BERTopic) on abstracts — what clusters emerge naturally?
  - Dimensionality reduction (UMAP or t-SNE) of TF-IDF vectors — visualize the paper space
  - Category co-occurrence heatmap — how do categories overlap?
  - Temporal patterns — submission rate by day/week/month, seasonal effects
  - Author network — who publishes together, prolific author distribution
- Output: visualizations, cluster descriptions, structural observations
- **This is the most open-ended part.** We're looking at the data to see what patterns exist before deciding what to measure.

**A2b: Interactive Explorer Prototype** — PENDING

- Build a Streamlit (or Plotly Dash) app for interactive exploration of the harvested corpus
- Not a polished product — a spike instrument for understanding the data
- Output: working interactive app in experiments/explorer/

**A3: Distribution Analysis** — PENDING

- For the harvested sample, compute distributions of key features
- Output: distribution plots, summary statistics, outlier identification

### Phase B: Signal Research and Discovery

**Objective:** Identify and evaluate candidate signals that could predict paper importance or relevance. Start with research, then compute and test.

**B1:** Literature review of paper recommendation features
**B2:** Computed signal exploration on retrospective sample with OpenAlex citations
**B3:** Explore what "importance" means empirically

### Phase C: Tradeoff Mapping

**Objective:** Map the tradeoffs between filtering strategies, promotion strategies, and resource requirements.

**C1:** Coverage-regret analysis with candidate filtering strategies
**C2:** Promotion pipeline simulation (resource projections)
**C3:** Backend implications synthesis

## Success Criteria

Exploratory spike — success is learning, not confirming.

**The spike succeeds if we can provide grounded answers to:**
1. What are the realistic paper volumes at each category configuration?
2. What does the arXiv landscape look like structurally for our categories?
3. Which 3-5 signals are most worth computing for paper scoring?
4. What shape is the coverage-regret tradeoff? Is there an elbow?
5. What promotion strategy best fits our architectural values (ADR-0002)?
6. What are the approximate resource requirements for 1 year of operation?
7. **What is the capability envelope for TF-IDF, embeddings, and concurrent access at our scale points?**
8. **At what corpus sizes do different NLP features become infeasible on a laptop (8-16 GB RAM)?**

## Practical Constraints

- arXiv OAI-PMH: 3s between requests (our harvester rate limit)
- OpenAlex: 10 req/s with email configured
- Storage: /scratch (87GB free) for experiment data, /data (1.4TB) for large datasets
- GPU: GTX 1080 Ti available for BERTopic / UMAP / embedding computation
- RAM: 32 GB — relevant constraint for TF-IDF and embedding matrix benchmarks
- Python environment: system Python 3 with scikit-learn 1.8.0, scipy 1.16.3, numpy 2.2.6
- All experiment code lives in this spike workspace

## Experiment Code Location

`.planning/spikes/001-volume-filtering-scoring-landscape/experiments/`

## Output

- **FINDINGS.md:** Data, visualizations, analysis organized by phase
- **DECISION.md:** Answers to the success criteria questions + recommendations (written when spike concludes)
- **Artifacts:** Scripts, datasets in experiments/
- **Feeds into:** Spike 002 (backend benchmarking), deployment-portability deliberation, potentially new spikes
