# Spike 001: Findings (In Progress)

**Last updated:** 2026-03-17
**Status:** Phase A1 partially complete, Phase A2-C pending

## Phase A1: Volume Mapping — Complete

### Experiment: January 2026 Harvest

Harvested real arXiv papers via OAI-PMH for three category configurations.

| Config | Categories | Unique Papers (Jan 2026) | % of All CS | Projected Annual |
|--------|-----------|-------------------------|-------------|------------------|
| Big4 | cs.AI, cs.CL, cs.CV, cs.LG | 12,145 | 67.7% | ~146K |
| Configured | All 15 in categories.toml | 14,962 | 83.4% | ~180K |
| All CS | All 37 CS subcategories | 17,928 | 100% | ~215K |

**Key findings:**
1. Big4 captures 81% of what all 15 configured categories would get. The extra 11 categories add only 2,817 papers/month, dominated by robotics (521), optimization (464), and signal processing (429).
2. cs.AI appears in 5,438 papers but is primary category for only 1,318 — the "cs.AI explosion" is largely a cross-listing phenomenon from cs.LG, cs.CL, cs.CV.
3. 65% of papers are cross-listed to 2+ categories. Only 35% have a single category.
4. Daily volume varies from 1 (weekends/holidays) to 1,396 (post-holiday backlog). Weekday average ~550-600 for big4.
5. OAI-PMH datestamps include paper updates, not just new submissions. The unique paper count (via INSERT OR IGNORE) is the reliable metric.

**Data:** 19,252 unique papers stored in `experiments/data/spike_001_harvest.db` (37 MB).

### Experiment: FTS5 Search Performance Benchmark

Measured SQLite FTS5 search latency at 7 scale points using real paper data (duplicated to reach target sizes). 10 query types, 10 runs each with 2 warmup runs.

| Scale | Insert | FTS Build | DB Size | Search p50 | Search p95 |
|-------|--------|-----------|---------|-----------|-----------|
| 5K | 0.1s | 0.3s | 15 MB | 0.9ms | 1.6ms |
| 10K | 0.2s | 0.6s | 28 MB | 1.8ms | 2.9ms |
| 19K | 0.3s | 1.2s | 50 MB | 2.7ms | 4.5ms |
| 50K | 0.5s | 3.6s | 132 MB | 7.2ms | 10.7ms |
| 100K | 1.3s | 6.8s | 259 MB | 13.5ms | 17.8ms |
| 215K | 2.7s | 15.1s | 553 MB | 30ms | 38ms |
| 500K | 5.4s | 36.3s | 1.28 GB | 71ms | 84ms |

**Key findings:**
1. Search latency scales linearly with corpus size. No performance knee or sudden degradation up to 500K papers.
2. At 215K papers (projected annual for configured categories), median search is 30ms, p95 is 38ms — well under the 100ms "feels instant" threshold.
3. At 500K papers (2+ years of broad harvesting), median search is 71ms — still under 100ms.
4. Slowest queries are common two-word terms ("language model": 91ms at 215K) and phrases ("large language model": 73ms at 215K). Specific queries stay fast (<5ms).
5. FTS index build takes 15 seconds at 215K papers — acceptable for initial setup, and daily incremental inserts (300 papers) would be sub-second.
6. DB size is ~2.6 MB per 1K papers (metadata + FTS index).

**Methodology note:** Larger scale points used duplicated papers with modified IDs. This preserves realistic text distributions and term frequencies but means the vocabulary doesn't grow beyond 19K papers' worth. Real 215K unique papers would have more diverse vocabulary, potentially making searches slightly faster (terms are more discriminative) or slightly slower (larger inverted index). This is a known limitation — real-scale testing would require months of harvesting.

## What We Know With Evidence

| Claim | Evidence | Confidence |
|-------|----------|-----------|
| Big4 captures most papers a ML/AI researcher would want | 81% of configured categories' papers | High — measured directly |
| SQLite FTS5 search is fast enough at 215K papers | 30ms p50, 38ms p95 | Medium — measured but with duplicated data caveat |
| Storage is not the constraint for SQLite | 553 MB at 215K papers | High — measured directly |
| Annual paper volume for configured categories is ~180K | Extrapolated from 1 month | Medium — seasonal variation not captured |

## What We Don't Know (Unmeasured)

| Question | Why it matters | Experiment needed |
|----------|---------------|-------------------|
| TF-IDF matrix size vs corpus size | Determines RAM needed for recommendation features | Compute TF-IDF on our 19K papers, measure memory. Extrapolate. |
| TF-IDF rebuild time at scale | Determines feature update latency | Time a full rebuild at 19K, 50K, 100K |
| Embedding computation time (CPU vs GPU) | Determines feasibility of semantic features on different hardware | Embed our 19K papers with all-MiniLM-L6-v2, measure time |
| Brute-force cosine similarity at scale | Determines whether numpy vector search is practical | Benchmark at 19K, 50K, 100K with real embeddings |
| Concurrent read+write on SQLite | Determines whether harvest daemon + MCP server can coexist | Simulate concurrent access patterns |
| PostgreSQL performance at same scales | Needed for fair backend comparison | Run equivalent benchmarks on PostgreSQL |
| FTS5 vs tsvector result quality | Do they return the same papers for the same queries? | Side-by-side comparison on real data |
| MCP server startup time with feature loading | Determines user experience when opening Claude Code | Measure startup with TF-IDF matrix and/or embeddings loaded |
| Quality of TF-IDF recommendations vs current ranker | Is the added complexity worth it? | Comparative evaluation on real triage data |
| Cold start behavior | What happens before user has triaged enough papers? | Test with 0, 5, 10, 20 positive examples |

## Discoveries That Changed Our Thinking

1. **The NLP layer is independent of the database.** TF-IDF, SVM, embeddings — all run in Python/numpy/scikit-learn. The database just stores papers. This means the "SQLite vs PostgreSQL" question is about storage and indexing, not about intelligence.

2. **PostgreSQL's real advantage is narrower than assumed.** It's not search quality or storage. It's: (a) indexed approximate nearest neighbor at >500K vectors (pgvector), (b) concurrent multi-writer access, (c) mature extension ecosystem. For a single-user tool under 500K papers, SQLite + Python handles everything.

3. **The configuration space is multi-dimensional.** What a user can run depends on: hardware (RAM, GPU, disk), category selection (determines corpus size), filter settings (determines what's ingested), and which NLP features are enabled. These interact — designing "tiers" doesn't capture the full picture. A capability/dependency system is more appropriate but risks over-engineering.

4. **Feature lifecycle is an unsolved problem.** Pre-computed features (TF-IDF matrices, embeddings) need to persist across MCP server restarts, update incrementally when new papers arrive, and fit in available RAM. This is an architecture question we haven't addressed.

5. **"Project" as a first-class concept is missing.** Interest profiles provide per-project ranking, but the user wants project-level recommendation feeds, model inheritance, and workspace separation. This isn't in any design doc.
