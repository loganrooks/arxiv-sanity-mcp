---
question: "What are the empirical tradeoffs between SQLite and PostgreSQL for our workload, and at what thresholds should a user choose one over the other?"
type: comparative
status: designing
round: 1
linked_deliberation: deployment-portability.md
depends_on: 001 (volume estimates, capability envelope)
---

# Spike 002: SQLite vs PostgreSQL Backend Comparison

## Question

What are the measured performance and quality tradeoffs between SQLite and PostgreSQL across each operation in our workload? Where does each backend outperform the other, by how much, and how does the tradeoff shift with scale?

## Why This Matters

Spike 001 measured SQLite's capability envelope in isolation. We then made comparative claims — "pgvector unnecessary," "SQLite sufficient," "tier differentiator is GPU not database" — without measuring PostgreSQL. These claims are grounded in inference from one-sided data, not empirical comparison. Before we can recommend one backend over another, or characterize the tradeoffs for users, we need measurements from both sides.

**Specifically:**
- "SQLite is sufficient" is a comparative claim requiring comparative data
- "pgvector unnecessary at personal scale" was stated without measuring pgvector
- FTS5 and tsvector use different tokenization, stemming, and ranking — speed equivalence does not imply quality equivalence
- Different users have different performance requirements — we don't get to declare what's "fast enough" on their behalf
- The deliberation's tier matrix should present measured tradeoffs, not inferred ones

## Epistemic Posture

This spike measures. It does not pre-judge which findings matter or which don't. We report what we observe across all dimensions and let the tradeoff map speak for itself.

Spike 001's claims about SQLite sufficiency, pgvector irrelevance, and tier differentiation are **hypotheses under test**, not established conclusions. The purpose of this spike is to subject them to empirical scrutiny by measuring the alternative.

The results will be compared against reference designs (arxiv-sanity-lite, Semantic Scholar, OpenAlex API response times) to provide context beyond our own system. Raw numbers in isolation don't tell a user whether their experience will be good — only comparison with systems they've used before does that.

## Experimental Dimensions

All dimensions are measured. Priority emerges from the data, not from our assumptions about what matters.

### Dimension 1: Search Result Quality

Speed tells you "how fast." Quality tells you "how good." A backend that returns the wrong papers fast is worse than one that returns the right papers slowly. We've measured speed extensively; we've measured quality not at all.

**Hypothesis H1:** FTS5 and tsvector return substantially similar results for the same queries.

**Falsification criteria:** Average Jaccard overlap of top-20 results below 0.5 means the backends retrieve materially different papers for the same query.

**Protocol:**
1. Load the 19K paper corpus into both SQLite (FTS5, porter tokenizer) and PostgreSQL (tsvector, english configuration)
2. Run 20+ representative queries covering:
   - Single common terms ("transformer")
   - Single rare terms ("phenomenology")
   - Multi-word ("language model", "reinforcement learning")
   - Phrases ("large language model")
   - Boolean (AND, OR)
   - Author names
   - Domain-specific terminology
3. For each query, collect top-20 results ranked by each backend's native relevance score
4. Measure:
   - **Jaccard similarity** of top-20 result sets
   - **Rank-biased overlap (RBO)** — weighted rank correlation that penalizes differences at top positions more than bottom
   - **Unique results** — papers in one backend's top-20 but not the other's. Sample and inspect: are they relevant?
   - **Per-query divergence** — identify which query types diverge most (to understand *why* they differ)
5. Run at 19K (real unique data, no duplication caveat)

**Stemming note:** FTS5 porter tokenizer and tsvector english configuration use different stemming algorithms. The analysis should identify where stemming differences drive result divergence.

### Dimension 2: Search Latency at Scale

Spike 001 measured SQLite search latency. This dimension measures PostgreSQL at the same scale points with the same queries, producing a side-by-side comparison.

**Hypothesis H2:** PostgreSQL tsvector search latency at each scale point is measurably different from FTS5.

**Protocol:**
1. Load papers into PostgreSQL at same scale points: 5K, 10K, 19K, 50K, 100K, 215K
2. Create tsvector GIN index (standard configuration)
3. Run the same query set from Dimension 1, same methodology as Spike 001 A1b (warmup runs, median of N, p50/p95)
4. Measure:
   - **tsvector search latency** (p50, p95, max) at each scale
   - **Per-query-type breakdown** (common terms, rare terms, boolean, phrases — same categories as A1b)
5. Compare side-by-side with A1b FTS5 numbers
6. **Reproduce A1b baseline first** — re-run FTS5 benchmark to confirm measurement stability before comparing

### Dimension 3: Vector Search (pgvector vs Brute-Force)

Spike 001 measured brute-force numpy dot product. This dimension measures pgvector HNSW at the same scale points, testing both raw ANN search and filtered vector search.

**Hypothesis H3a:** pgvector HNSW search latency at 215K is measurably different from brute-force numpy.

**Hypothesis H3b:** pgvector filtered vector search (category + similarity) provides a latency or ergonomic advantage over manual pre-filter + brute-force.

**Protocol:**
1. Load embeddings into pgvector at same scale points (reuse or recompute all-MiniLM-L6-v2 embeddings from A1c.3)
2. Create HNSW index with default parameters. Document: m, ef_construction, ef_search.
3. Measure at each scale point:
   - **pgvector exact search** (`<->` operator, no index) — the pgvector equivalent of brute-force, for fair comparison
   - **pgvector HNSW search** — approximate, indexed
   - **Recall** — what fraction of true top-20 (from exact search) does HNSW return?
   - **Brute-force numpy** (from A1c.3) for comparison
4. For filtered search at 215K:
   - pgvector: `SELECT ... WHERE category = 'cs.AI' ORDER BY embedding <-> query_vec LIMIT 20`
   - Manual: extract category-filtered paper IDs from SQLite, select corresponding embedding rows from numpy matrix, brute-force
   - Compare latency, result equivalence, code complexity

### Dimension 4: Write Performance

Both backends will handle our write workload. The question is how they compare on bulk import (cold start), incremental writes (daily harvest), and concurrent read+write (measured for SQLite in A1c.2, not for PostgreSQL).

**Hypothesis H4:** Write performance characteristics differ between backends in ways that affect user experience during import, harvest, and concurrent operation.

**Protocol:**
1. Bulk import 19K papers into fresh database on each backend. Measure wall time.
2. Measure incremental insert rate: 1, 10, 50, 100 papers/second (same rates as A1c.2)
3. Measure concurrent read+write: search latency during sustained writes (same protocol as A1c.2, on PostgreSQL)
4. Measure database size on disk after 19K papers
5. Measure at scale: repeat bulk import at 50K, 100K, 215K (duplicated data)

### Dimension 5: Operational Characteristics

These are the non-performance factors that affect a user's day-to-day experience.

**Protocol:**
1. **Connection setup time** — time from "open connection" to "first query returns." Relevant for MCP server tool invocations (each tool call may open a connection, depending on pooling).
2. **Backup/restore** — SQLite: `cp data.db data.db.bak`. PostgreSQL: `pg_dump` / `pg_restore`. Measure time for 19K and 215K paper databases.
3. **Disk footprint** — total size on disk (data + indexes + WAL/journal) at each scale point.
4. **Migration complexity** — qualitative assessment: what does moving data from SQLite to PostgreSQL (or back) look like?

### Dimension 6: Workflow-Level Comparison

Individual operation benchmarks don't capture compound effects across multi-step MCP workflows. An agent research session invokes 10-15 tools in sequence. Per-operation differences accumulate.

**Protocol:**
1. Script a representative 6-tool MCP workflow: search → get_paper → find_related → triage → add_to_collection → check_watch
2. Run 10 times on each backend at 19K papers
3. Measure total workflow time, per-tool breakdown
4. Script a heavier 15-tool workflow (full research session) and repeat

## Reference Design Comparison

After collecting data from all dimensions, compare our measured numbers against reference systems:

| System | What to compare | Source |
|--------|----------------|--------|
| arxiv-sanity-lite | Search latency, recommendation latency, corpus size handled | GitHub repo, published metrics if available |
| Semantic Scholar API | Search latency, result quality (qualitative) | API response times from live calls |
| OpenAlex API | Enrichment/search latency | API response times from live calls |
| arXiv API | Metadata search latency | API response times from live calls |

This comparison contextualizes our numbers. "30ms search" means nothing without knowing that users are accustomed to 200ms from web APIs or 5ms from local tools.

## Methodological Controls

1. **Same data:** Both backends loaded from the same source (spike_001_harvest.db)
2. **Same queries:** Identical query set across all experiments
3. **Same scale points:** 5K, 10K, 19K, 50K, 100K, 215K (matching Spike 001)
4. **Same measurement methodology:** Warmup runs, median of N, p50/p95/max reporting
5. **Reproduce Spike 001 baselines:** Re-run A1b FTS5 and A1c.3 embedding benchmarks first to confirm measurement stability
6. **Fair tuning:** Both backends use recommended default configurations. All configuration documented. No hand-tuning to favor either side.
7. **Same hardware:** All experiments on same machine (Xeon W-2125, 32 GB RAM, GTX 1080 Ti)

## Success Criteria

This is a comparative spike — success is a complete, honest tradeoff map.

**The spike succeeds if:**
1. For each dimension, we can state: "Backend X measures [value] and Backend Y measures [value] at [scale]"
2. We produce a tradeoff table that a user can consult to make an informed backend choice for their specific situation
3. We can compare our numbers against reference designs for context
4. The Spike 001 claims about SQLite sufficiency and pgvector irrelevance are either confirmed with comparative evidence or revised

**The spike fails if:**
- The comparison is unfair (different tuning, different data, methodological flaws)
- We can't reproduce Spike 001's SQLite numbers (measurement instability)
- Results are reported selectively (cherry-picking dimensions that favor a conclusion)

## Practical Constraints

- PostgreSQL is running locally (port 5432)
- 19K real papers available in `spike_001_harvest.db`
- Pre-computed embeddings from A1c.3 (reusable)
- pgvector extension: verify installed, install if not (`CREATE EXTENSION vector`)
- Same hardware as Spike 001 (Xeon W-2125, 32 GB RAM, GTX 1080 Ti)
- All experiment code in `.planning/spikes/002-backend-comparison/experiments/`

## Experiment Code Location

`.planning/spikes/002-backend-comparison/experiments/`

## Output

- **FINDINGS.md:** Side-by-side comparison tables for each dimension, reference design comparison
- **DECISION.md:** Tradeoff map, user-facing guidance table, revised deliberation input
- **Feeds into:** Deployment deliberation update, Phase 12 storage abstraction design
