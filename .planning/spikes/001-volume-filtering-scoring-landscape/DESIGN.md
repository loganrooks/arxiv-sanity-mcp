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
| A2: Corpus Visualization | **Pending** | Protocol expanded 2026-03-19. Validates pre-filtering assumption. | — |
| A2b: Interactive Explorer | Deferred | UMAP HTML from A2 sufficient for now | — |
| A3: Distribution Analysis | **Pending** | Protocol expanded 2026-03-19 | — |
| B1: Signal Literature Review | **Pending** | Protocol expanded 2026-03-19. Research task, no data needed. | — |
| B2: Computed Signal Exploration | **Pending** | Requires B1, A2, A3. OpenAlex enrichment needed (~500 papers). | — |
| B3: Importance Analysis | **Pending** | Requires B2. Factor analysis on signal matrix. | — |
| C1: Coverage-Regret Analysis | **Pending** | Requires B2, B3. Simulated filtering strategies. | — |
| C2: Promotion Pipeline Sim | **Pending** | Requires C1, A1. Resource projections. | — |
| C3: Backend Implications | **Deprioritized** | Answered by A1c + Spike 002. Synthesis in deliberation. | — |

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

*Question:* What does the paper space look like structurally? Do arXiv categories map to topical clusters?

*Why it matters:* The deployment deliberation assumes category-based pre-filtering is viable (e.g., "filter to cs.AI before computing TF-IDF similarity"). This assumption requires that categories correspond to topical clusters. If papers within a category are topically diffuse, category pre-filtering may exclude relevant papers. A2 also reveals whether our 15 configured categories carve the space meaningfully or arbitrarily.

*Protocol:*
1. **Topic modeling (BERTopic):** Run BERTopic on the 19K paper abstracts using the Spike 002 MiniLM embeddings (already computed, 384-dim). Extract topic labels, sizes, and representative documents.
2. **UMAP visualization:** Reduce the 384-dim embeddings to 2D via UMAP. Color by primary_category. Save as interactive HTML (plotly) and static PNG.
3. **Category–topic alignment:** For each BERTopic topic, compute the distribution of primary_category values. Are topics dominated by one category (alignment) or spread across many (misalignment)?
4. **Category co-occurrence heatmap:** For multi-category papers, compute pairwise co-occurrence counts. Visualize as heatmap.
5. **Temporal patterns:** Submission rate by day-of-week and week-of-month for January 2026. Identify any cyclical patterns (conference deadlines, holidays).
6. **Author frequency distribution:** How many papers does the median/90th/99th percentile author publish in one month?

*Output:* Visualizations (saved as PNG + HTML), structural observations in FINDINGS.md.

*Deployment relevance:* If categories align well with topics → category pre-filtering is valid. If they don't → pre-filtering mitigation in deliberation is questionable.

**A2b: Interactive Explorer Prototype** — DEFERRED

- Originally planned as a Streamlit app. Deferred — the UMAP interactive HTML from A2 provides sufficient exploration capability. Can revisit if A2 findings create demand for deeper exploration.

**A3: Distribution Analysis** — PENDING

*Question:* What are the statistical properties of key corpus features? What distributions do they follow?

*Why it matters:* Distribution shapes affect ranking normalization, enrichment scheduling, and promotion pipeline design. Power-law distributions (common in bibliometrics) need different handling than normal distributions. Outlier identification reveals papers that break assumptions.

*Protocol:*
1. **Category distribution:** Paper counts by primary_category. Bar chart + Gini coefficient.
2. **Abstract length distribution:** Histogram + summary stats (mean, median, std, min, max).
3. **Title length distribution:** Same.
4. **Author count per paper:** Distribution — how many authors is typical?
5. **Category count per paper:** How many papers have multiple categories? Distribution of category_count.
6. **Temporal distribution within the month:** Papers per day. Is the rate uniform or bursty?
7. **Vocabulary analysis:** Unique terms in abstracts, term frequency distribution (Zipf's law fit). How many terms cover 80% of content?

*Output:* Distribution plots (matplotlib, saved as PNG), summary statistics table in FINDINGS.md.

*Dependencies:* None — uses existing harvest data.

### Phase B: Signal Research and Discovery

**Objective:** Identify and evaluate candidate signals that could predict paper importance or relevance. Start with research, then compute and test.

**B1: Signal Literature Review** — PENDING

*Question:* What signals do existing academic paper recommender systems use? What does the research literature say about predicting paper importance?

*Why it matters:* Our current system uses a 5-signal composite ranker (seed_paper, followed_author, saved_query, category, negative_author) — all based on user-declared interest. We have no computed signals (citation velocity, author h-index, topic novelty, etc.). B1 establishes what the field considers effective before we start computing our own.

*Protocol:*
1. **Review existing systems:** arxiv-sanity (original + lite), Semantic Scholar recommendations, Google Scholar ranking, ResearchRabbit, Connected Papers, Elicit. For each: what signals do they use? What's their ranking approach?
2. **Review literature:** Search for "academic paper recommendation" surveys (2020+). Key areas:
   - Content-based filtering (TF-IDF, embeddings, topic models)
   - Collaborative filtering (citation graphs, co-readership)
   - Metadata signals (citation count, recency, venue, author metrics)
   - Hybrid approaches
3. **Compile candidate signal list:** For each signal, note: what data is needed, can we compute it from our sources (arXiv metadata + OpenAlex enrichment), approximate compute cost.
4. **Classify signals by availability:**
   - Available now: already in our schema
   - Available via OpenAlex: requires enrichment API call
   - Requires new data source: not currently accessible
   - Requires user interaction data: needs usage history we don't have yet

*Output:* Signal catalog with source, availability, and literature evidence. Written to FINDINGS.md.

*Dependencies:* None — research task, no data computation needed.

**B2: Computed Signal Exploration** — PENDING

*Question:* Which candidate signals from B1 actually correlate with paper importance in our corpus?

*Why it matters:* Literature tells us what signals exist in theory. B2 tests which ones are informative in practice for our specific corpus (15 arXiv categories, January 2026). A signal might be well-established in the literature but useless for our categories or time window.

*Protocol:*
1. **Enrich a sample:** Select ~500 papers from the 19K corpus (stratified by category). Fetch OpenAlex enrichment for each: citation count, cited_by_count, FWCI, topics, related works, author h-indices.
2. **Compute candidate signals:** For each enriched paper, compute:
   - Citation velocity (citations per month since publication — may be near-zero for January 2026 papers)
   - Author h-index (max h-index among authors, from OpenAlex)
   - Category entropy (how many categories vs. papers in those categories)
   - Topic novelty (cosine distance from category centroid in embedding space)
   - Reference overlap (Jaccard of references against user's library — simulated)
   - Abstract readability (sentence length, technical term density)
3. **Correlation analysis:** Compute pairwise correlations between signals. Compute correlation between each signal and available importance proxies (cited_by_count, FWCI if available).
4. **Feature importance:** Train a simple classifier (random forest) to predict "highly cited" (top 20% by citation count) from computed signals. Extract feature importances.
5. **Caveat:** January 2026 papers have had <2 months to accumulate citations. Citation-based importance proxies will be weak. Focus on signal structure and correlations rather than absolute predictive power.

*Output:* Correlation matrix, feature importance ranking, signal evaluation table in FINDINGS.md.

*Dependencies:* B1 (signal catalog), A2 (embeddings for topic novelty), A3 (distributions for normalization).

**B3: Importance Analysis** — PENDING

*Question:* Is "paper importance" one thing or multiple dimensions? Does it decompose into distinct factors?

*Why it matters:* Our ranking system produces a single score. If importance is multidimensional (e.g., methodological significance vs. topical relevance vs. citation impact vs. novelty), a single score loses information. The interest profile model might need multiple axes rather than one composite.

*Protocol:*
1. Using the enriched sample from B2, collect all computed signals into a feature matrix.
2. **PCA/Factor analysis:** How many principal components explain >80% of variance? Do the components have interpretable meanings (e.g., "impact" vs. "novelty" vs. "breadth")?
3. **Cluster analysis on papers:** K-means or HDBSCAN on the signal feature matrix. Do distinct paper "types" emerge (landmark papers, survey papers, incremental papers, methodological papers)?
4. **Qualitative validation:** For each cluster or factor, inspect 5 representative papers. Does the grouping make intuitive sense?

*Output:* Factor analysis results, paper type taxonomy (if clusters emerge), recommendation for single-score vs. multi-axis ranking. Written to FINDINGS.md.

*Dependencies:* B2 (computed signal matrix).

### Phase C: Tradeoff Mapping

**Objective:** Map the tradeoffs between filtering strategies, promotion strategies, and resource requirements.

**C1: Coverage-Regret Analysis** — PENDING

*Question:* What's the tradeoff shape for filtering strategies? Is there an elbow?

*Why it matters:* We currently ingest ALL papers in configured categories. This means 12K-18K papers/month. Most of these are irrelevant to any particular user. Filtering reduces volume but risks missing important papers. C1 maps this tradeoff to find whether a "sweet spot" exists.

*Protocol:*
1. **Define importance proxy:** Using B2's findings, select the best available importance proxy (likely: cited_by_count from OpenAlex, or composite of top signals from B2).
2. **Simulate filtering strategies:**
   - Category-only (current): all papers in configured categories
   - Keyword filter: papers matching user-defined keywords in title/abstract
   - Citation threshold: papers by authors with h-index > X
   - Embedding similarity: papers within cosine distance Y of user's seed papers
   - Combined: keyword OR citation OR similarity (union)
3. **For each strategy at various thresholds, measure:**
   - Coverage: fraction of "important" papers retained (important = top 20% by proxy)
   - Volume: total papers retained
   - Regret: important papers missed
4. **Plot coverage-volume curves.** Look for elbows where increasing filtering aggressiveness causes disproportionate coverage loss.
5. **Sensitivity analysis:** How robust are results to the importance proxy choice?

*Output:* Coverage-volume tradeoff curves, elbow identification, filtering strategy ranking. Written to FINDINGS.md.

*Dependencies:* B2 (importance proxy), B3 (multi-dimensional importance consideration).

**C2: Promotion Pipeline Simulation** — PENDING

*Question:* What are the resource costs of different promotion strategies over 1 year of operation?

*Why it matters:* ADR-0002 says "enrich lazily, embed selectively." C2 tests what "lazy" and "selective" mean concretely. How many OpenAlex API calls per month? How much GPU time for embedding? How much storage growth? These numbers determine whether the operational story is sustainable.

*Protocol:*
1. **Define promotion strategies:**
   - S1: Embed only triaged papers (conservative — user-driven)
   - S2: Embed top 10% by filtering score (moderate — semi-automatic)
   - S3: Embed all ingested papers (aggressive — full coverage)
   - S4: Enrich via OpenAlex, then embed enriched subset (two-stage)
2. **For each strategy, project 12 months of operation at our measured ingestion rates:**
   - OpenAlex API calls/month (rate limited at 10/s with email)
   - GPU hours/month for embedding computation (using A1c.3 per-paper times)
   - CPU hours/month if no GPU
   - Storage growth: database size + embedding file size
   - Total wall time for daily incremental processing
3. **Cost table:** resource usage × 12 months, with and without GPU.

*Output:* Resource projection table per strategy per tier. Written to FINDINGS.md.

*Dependencies:* C1 (filtering thresholds inform promotion volumes), A1 (ingestion rates).

**C3: Backend Implications Synthesis** — DEPRIORITIZED

*Status:* Largely answered by Spike 001 A1c + Spike 002. Backend performance at scale is thoroughly measured. No additional experiments needed.

*Remaining work:* Integrate C1/C2 findings with Spike 002 findings to produce final backend recommendation. This synthesis happens in the deliberation, not in an experiment.

---

## Round 2: Gap Closure (added 2026-03-19)

Round 1 of B/C completed the protocol as specified but failed to propagate findings between experiments. B1 identified SVM, keyword, and hybrid filtering as the most validated approaches in the literature — but C1 didn't test any of them. QV3 showed MiniLM/SPECTER2 disagree strongly — but C1's embedding filter used only MiniLM. B3 found importance is multi-dimensional — but C1 used a single proxy.

See signal: `sig-2026-03-19-gaps-not-proactively-identified`

### C1-R: Extended Filtering Strategies

C1 Round 1 tested basic strategies. Round 2 tests the approaches B1 identified as most validated:

**C1-R1: Keyword-based filtering**

Protocol:
1. Define 5 seed keyword sets simulating different user interests (e.g., "reinforcement learning + robotics", "language model + reasoning", "diffusion + generation")
2. For each seed, filter the 460 enriched papers by keyword match in title+abstract
3. Measure coverage of "important" papers (same proxy as C1 Round 1)
4. Compare volume reduction vs coverage loss against C1 baselines

**C1-R2: Author-based filtering**

Protocol:
1. From enrichment data, extract author publication counts (via OpenAlex authorship)
2. Filter to papers with at least one "prolific" author (>= 5 papers in corpus)
3. Simulate "followed_author" filtering: select 10 most prolific authors as "followed", keep their papers
4. Measure coverage and volume

**C1-R3: SVM classifier filtering (arxiv-sanity-lite approach)**

Protocol:
1. Simulate a user library: randomly select 20 papers as "positive" (user's saved papers)
2. Compute TF-IDF on all 460 enriched papers
3. Train LinearSVC (C=0.01, balanced weights) on positive vs rest
4. Score all papers by SVM decision function
5. Keep top 50%, top 20%, top 10% — measure coverage at each threshold
6. Repeat with 5 different random libraries to assess stability

**C1-R4: Hybrid union filtering**

Protocol:
1. Combine: keyword match OR SVM top-50% OR embedding top-50%
2. Measure coverage of union (should be higher than any individual strategy)
3. Measure volume of union
4. Compare efficiency (coverage/volume ratio) against individual strategies

**C1-R5: SPECTER2 embedding filter**

Protocol:
1. Recompute the embedding top-50% filter using SPECTER2 embeddings instead of MiniLM
2. Compare coverage and volume against MiniLM embedding filter from C1 Round 1
3. Assess whether SPECTER2's domain-specific similarity produces better filtering

### C1-R6: Importance proxy sensitivity

Round 1's importance proxy (citation count) is near-zero for January 2026 papers. This undermines all coverage measurements.

Protocol:
1. Use reference_count as alternative proxy (available for more papers, not time-dependent)
2. Use OpenAlex FWCI as second alternative (field-normalized)
3. Re-run top 3 filtering strategies against each proxy
4. Report: how stable are coverage numbers across different importance definitions?

### Category Resource Model Refinement

Already completed (category_resource_model.py). Produced per-category and per-preset resource estimates for interactive installer.

Additional refinement needed:
1. **Primary vs listed distinction**: installer should filter by "listed in" not "primary category" — the category model showed cs.AI has 5,438 listed vs 1,318 primary papers
2. **Overlap estimation**: for multi-category selections, use the pairwise overlap data to estimate unique paper count

### Round 2 Completion Checklist

- [ ] C1-R1: Keyword-based filtering tested
- [ ] C1-R2: Author-based filtering tested
- [ ] C1-R3: SVM classifier filtering tested
- [ ] C1-R4: Hybrid union filtering tested
- [ ] C1-R5: SPECTER2 embedding filter tested
- [ ] C1-R6: Importance proxy sensitivity analyzed
- [ ] Category resource model committed
- [ ] FINDINGS.md updated with all Round 2 results

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
