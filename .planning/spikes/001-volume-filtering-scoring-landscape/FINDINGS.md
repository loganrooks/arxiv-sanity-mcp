# Spike 001: Findings (In Progress)

**Last updated:** 2026-03-17
**Status:** Phase A1 complete, A1c.1-2 complete, A1c.3 + A2-C pending

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

## A1c.1: TF-IDF Matrix Benchmark — Complete

Measured TF-IDF matrix construction, memory footprint, and cosine similarity search time at 6 scale points using real arXiv paper abstracts. 5 vocabulary configurations tested. Scikit-learn 1.8.0, float32 dtype, scipy CSR sparse format.

### Memory Footprint (matrix + vocabulary)

| Scale | Default | max_50k | max_20k | Pruned (min2/max0.8) | Pruned+50k |
|-------|---------|---------|---------|----------------------|------------|
| 5K | 5.8 MB | 5.9 MB | 5.3 MB | 4.6 MB | 4.7 MB |
| 10K | 10.4 MB | 10.6 MB | 8.9 MB | 8.7 MB | 8.8 MB |
| 19K | 17.9 MB | 17.6 MB | 14.9 MB | 15.4 MB | 15.5 MB |
| 50K | 40.1 MB | 39.8 MB | 36.5 MB | 40.1 MB | 39.8 MB |
| 100K | 75.4 MB | 74.9 MB | 70.9 MB | 75.4 MB | 74.9 MB |
| 215K | 156.9 MB | 156.2 MB | 150.3 MB | 156.9 MB | 156.2 MB |

### Cosine Similarity Search Time (top-20 via argpartition, median of 5 runs)

| Scale | Default | max_50k | max_20k | Pruned | Pruned+50k |
|-------|---------|---------|---------|--------|------------|
| 5K | 5.4ms | 5.4ms | 5.9ms | 5.2ms | 5.2ms |
| 10K | 11.7ms | 12.1ms | 10.7ms | 11.2ms | 10.4ms |
| 19K | 20.7ms | 21.1ms | 19.3ms | 20.7ms | 20.6ms |
| 50K | 56.9ms | 87.4ms | 51.6ms | 76.2ms | 86.9ms |
| 100K | 173.4ms | 214.6ms | 210.1ms | 207.3ms | 220.1ms |
| 215K | 516.0ms | 495.8ms | 467.9ms | 510.4ms | 463.9ms |

### Fit Time (full fit_transform, median of 3 runs)

| Scale | Default | max_50k | max_20k | Pruned | Pruned+50k |
|-------|---------|---------|---------|--------|------------|
| 5K | 0.6s | 0.7s | 0.7s | 0.6s | 0.6s |
| 10K | 1.2s | 1.5s | 1.3s | 1.3s | 1.3s |
| 19K | 2.2s | 2.7s | 2.5s | 2.2s | 2.5s |
| 50K | 5.6s | 6.6s | 6.5s | 6.1s | 6.3s |
| 100K | 11.4s | 13.2s | 12.8s | 12.1s | 12.8s |
| 215K | 28.5s | 27.2s | 27.0s | 26.1s | 26.9s |

### Other Measurements

- **Query transform time:** <1ms at all scales (negligible)
- **Vocabulary size:** 55,798 terms at 19K unique papers (default config)
- **Sparsity:** >99.5% at all scales (TF-IDF matrices are extremely sparse)
- **NNZ per document:** ~90-97 nonzero entries per paper (average abstract ~200 words, ~95 unique terms after stop words)
- **Partitioned vs full argsort:** No meaningful difference — the cosine similarity computation dominates, not the sort

### Key Findings

1. **Memory is not the bottleneck.** At 215K papers, the full TF-IDF matrix + vocabulary requires only ~157 MB. A laptop with 8 GB RAM can hold this trivially. Even at 500K (extrapolating linearly), it would be ~365 MB. The deliberation's concern about RAM feasibility was unfounded.

2. **Cosine similarity search IS the bottleneck.** Brute-force cosine similarity crosses the 100ms "feels instant" threshold between 50K and 100K papers. At 215K, it's ~500ms — noticeable but usable. At 500K (extrapolating), it would be ~1.2s — too slow for interactive use.

3. **The feasibility breakpoint for brute-force TF-IDF similarity is ~50K-75K papers.** Below this, brute-force cosine similarity is under 100ms. Above, you need either pre-filtering (search within a category or time window), approximate nearest neighbors, or acceptance of perceptible latency.

4. **Vocabulary pruning makes minimal difference.** At scale, all configs converge to similar memory and search times. The vocabulary size is dominated by the number of unique documents, not the pruning parameters. At 19K unique papers: default=56K terms, pruned=26K terms, but the memory difference is only 2.5 MB. The compute time difference is within measurement noise.

5. **Rebuild time is acceptable.** A full TF-IDF rebuild at 215K papers takes ~28 seconds. This is fine for a nightly rebuild or MCP server startup. Daily incremental papers (~600 for configured categories) would mean a rebuild adding 0.06s — negligible.

6. **This is a compute constraint, not a memory constraint.** The architectural implication is that pre-filtering (not ANN, not bigger hardware) is the path to scaling TF-IDF recommendations. An SVM trained on user preferences acts as a pre-filter naturally — you only need similarity against the papers in the user's interest categories.

### What Would Have Surprised Us (Pre-registered Predictions vs Results)

| Prediction | Threshold | Actual | Surprised? |
|-----------|-----------|--------|-----------|
| Matrix at 215K exceeds 2 GB | >2 GB | 157 MB | No — 13x under threshold |
| Cosine search at 215K exceeds 100ms | >100ms | 516ms | **Yes** — 5x over threshold |
| Vocabulary pruning dramatically changes results | Quality degradation | Minimal effect | No |
| Rebuild time at 215K exceeds 60s | >60s | 28.5s | No — 2x under threshold |

### Methodology Note

Same duplication caveat as A1b: scale points above 19K use duplicated papers with modified IDs. This preserves term frequency distributions but means vocabulary is capped at 19K unique papers' worth (~56K terms). Real 215K unique papers would have larger vocabulary (~150K-200K terms estimated), which would increase memory slightly but likely decrease search time (sparser, more discriminative vectors). The cosine search time finding (the main concern) may be slightly pessimistic for real data — duplicated documents create a denser similarity landscape than truly diverse papers would.

## A1c.2: Concurrent SQLite Read+Write — Complete

Measured FTS5 search latency during concurrent writes at 5 write rates (0–100/s), 2 journal modes (default DELETE vs WAL), 2 batch sizes (1 vs 10). 10K pre-populated papers. Each test runs for 10 seconds. `busy_timeout=5000ms`.

### Search p50 Latency During Concurrent Writes

**Batch size 1 (individual INSERT+COMMIT per paper):**

| Journal Mode | 0/s (baseline) | 1/s | 10/s | 50/s | 100/s |
|-------------|---------------|------|------|------|-------|
| DELETE | 1.3ms | 1.7ms | 1.9ms | **27.6ms** | **180.7ms** |
| WAL | 1.3ms | 1.5ms | 1.4ms | 1.6ms | 1.6ms |

**Batch size 10 (10 INSERTs per COMMIT):**

| Journal Mode | 0/s (baseline) | 1/s | 10/s | 50/s | 100/s |
|-------------|---------------|------|------|------|-------|
| DELETE | 1.3ms | 1.4ms | 1.6ms | 1.5ms | 1.9ms |
| WAL | 1.3ms | 1.2ms | 1.4ms | 1.5ms | 1.5ms |

### Search p95 Latency During Concurrent Writes

**Batch size 1:**

| Journal Mode | 0/s | 1/s | 10/s | 50/s | 100/s |
|-------------|------|------|------|------|-------|
| DELETE | 7.6ms | 8.2ms | 10.4ms | **59.7ms** | **3714ms** |
| WAL | 7.7ms | 7.6ms | 7.5ms | 8.2ms | 8.1ms |

**Batch size 10:**

| Journal Mode | 0/s | 1/s | 10/s | 50/s | 100/s |
|-------------|------|------|------|------|-------|
| DELETE | 7.5ms | 7.6ms | 8.1ms | 8.6ms | 11.1ms |
| WAL | 7.4ms | 7.3ms | 7.6ms | 8.1ms | 7.8ms |

### Search Throughput

| Config | 0/s writes | 100/s writes (batch=1) | 100/s writes (batch=10) |
|--------|-----------|----------------------|------------------------|
| DELETE | 406/s | **1/s** (99.7% drop) | 264/s (35% drop) |
| WAL | 405/s | 359/s (11% drop) | 378/s (7% drop) |

### Lock Errors

**Zero lock errors across all configurations.** The 5-second `busy_timeout` was never triggered. Contention manifests as latency increase, not errors.

### Key Findings

1. **WAL mode completely eliminates write-induced search latency degradation.** With WAL, search p50 stays at 1.3-1.6ms regardless of write rate (0 to 100/s). Without WAL, search p50 jumps from 1.3ms to 181ms at 100 writes/s with batch=1 — a 140x degradation.

2. **Batch size matters enormously for DELETE mode, barely for WAL.** DELETE mode with batch=1 at 100/s is catastrophic (p95=3.7s). DELETE mode with batch=10 at 100/s is tolerable (p95=11ms). WAL mode doesn't care about batch size — both are under 10ms.

3. **The harvest daemon + MCP server can absolutely coexist on SQLite.** With WAL mode enabled (one `PRAGMA journal_mode=WAL` statement), concurrent access is a non-issue at any realistic write rate. Daily harvest of ~600 papers is 0.007 papers/second sustained — orders of magnitude below where any contention appears.

4. **Even bulk import is fine with WAL.** 100 papers/second with batch=10 in WAL mode: search p50=1.5ms, p95=7.8ms, 378 searches/second. Zero impact on search quality.

5. **DELETE mode with batch=1 is the only dangerous configuration.** Individual commits per paper at high rates cause severe contention. This is easily avoided: either use WAL (preferred) or batch writes.

### What Would Have Surprised Us (Pre-registered Predictions vs Results)

| Prediction | Threshold | Actual | Surprised? |
|-----------|-----------|--------|-----------|
| WAL eliminates contention entirely | No degradation | p50 stays 1.3-1.6ms at all rates | **Yes** — even better than expected, completely flat |
| Search latency doubles during writes | 2x baseline | DELETE+batch1: 140x at 100/s. WAL: 1.0-1.2x | Partial — DELETE is worse than predicted, WAL better |
| SQLITE_BUSY errors at realistic rates | Any busy errors | Zero errors at all rates (with 5s timeout) | **Yes** — expected some at 100/s |

### Methodology Note

Tests run with 10K pre-populated papers. At larger corpus sizes (50K+), absolute search latency would be higher (per A1b findings) but the *relative impact* of concurrent writes should be similar since the contention is at the file/journal level, not query-proportional. WAL mode's advantage is architectural (readers don't block on writers), not scale-dependent.

## What We Know With Evidence

| Claim | Evidence | Confidence |
|-------|----------|-----------|
| Big4 captures most papers a ML/AI researcher would want | 81% of configured categories' papers | High — measured directly |
| SQLite FTS5 search is fast enough at 215K papers | 30ms p50, 38ms p95 | Medium — measured but with duplicated data caveat |
| Storage is not the constraint for SQLite | 553 MB at 215K papers | High — measured directly |
| Annual paper volume for configured categories is ~180K | Extrapolated from 1 month | Medium — seasonal variation not captured |
| TF-IDF matrix fits comfortably in RAM at 215K papers | 157 MB total | High — measured directly, even pessimistic duplication |
| TF-IDF rebuild time is acceptable at 215K papers | 28.5s full rebuild | High — measured directly |
| Brute-force cosine similarity is too slow above ~50-75K papers | 57ms at 50K, 173ms at 100K, 516ms at 215K | Medium — measured with duplicated data; real data may be slightly faster (sparser vectors) |
| Vocabulary pruning has negligible impact on TF-IDF performance | All 5 configs within 10% at scale | High — measured across 5 configurations |
| The TF-IDF feasibility constraint is compute, not memory | 157 MB RAM vs 516ms search at 215K | High — clear separation between the two dimensions |
| WAL mode eliminates concurrent access as a concern | p50 stays 1.3-1.6ms at 0-100 writes/s | High — measured directly, completely flat |
| Harvest daemon + MCP server can coexist on SQLite | Zero degradation at realistic rates (WAL) | High — 600 papers/day is orders of magnitude below threshold |
| DELETE journal mode with unbatched writes is dangerous | p95=3.7s at 100 writes/s, batch=1 | High — measured directly |
| Batch writes eliminate DELETE mode contention | p95=11ms at 100/s with batch=10 | High — measured directly |

## What We Don't Know (Unmeasured)

| Question | Why it matters | Experiment needed |
|----------|---------------|-------------------|
| ~~TF-IDF matrix size vs corpus size~~ | ~~Determines RAM needed~~ | **Answered (A1c.1):** 157 MB at 215K papers |
| ~~TF-IDF rebuild time at scale~~ | ~~Determines feature update latency~~ | **Answered (A1c.1):** 28.5s at 215K papers |
| ~~Brute-force TF-IDF cosine similarity at scale~~ | ~~Determines whether numpy search is practical~~ | **Answered (A1c.1):** Feasible to ~50-75K; 516ms at 215K |
| Embedding computation time (CPU vs GPU) | Determines feasibility of semantic features on different hardware | Embed our 19K papers with all-MiniLM-L6-v2, measure time |
| Brute-force embedding cosine similarity at scale | Determines whether embeddings are practical without pgvector | Benchmark at 19K, 50K, 100K with real embeddings |
| ~~Concurrent read+write on SQLite~~ | ~~Determines harvest daemon + MCP coexistence~~ | **Answered (A1c.2):** WAL mode makes this a non-issue |
| Pre-filtered cosine similarity performance | Does searching within category/time window keep latency under 100ms at 215K? | TF-IDF cosine on pre-filtered subsets |
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

6. **SQLite concurrent access is a solved problem with WAL mode.** We expected this to be a meaningful constraint that might force separate databases for harvest and query. It's not — WAL mode completely eliminates write-induced search degradation. Search latency is flat at 1.3-1.6ms regardless of whether 0 or 100 papers/second are being written concurrently. The deliberation's concern about "concurrent multi-writer access" as a PostgreSQL advantage is invalid for the single-writer scenario (one harvest daemon). WAL should be the default for all SQLite deployments.

7. **The TF-IDF feasibility constraint is compute, not memory.** We expected that RAM might be the bottleneck for TF-IDF recommendations on laptops. It's not — 215K papers need only 157 MB. The bottleneck is brute-force cosine similarity search: O(n) over the full matrix crosses 100ms around 50K-75K papers and hits 500ms at 215K. This means the scaling strategy is pre-filtering (reduce the search space), not approximate nearest neighbors or bigger hardware. Conveniently, an SVM classifier trained on user preferences *is* a pre-filter — you only compute similarity against papers the SVM considers relevant.
