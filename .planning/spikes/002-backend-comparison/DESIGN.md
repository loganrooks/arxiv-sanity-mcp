---
question: "What are the empirical tradeoffs between SQLite and PostgreSQL for our workload, and at what thresholds should a user choose one over the other?"
type: comparative
status: in_progress
round: 2
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

- Same hardware as Spike 001 (Xeon W-2125, 32 GB RAM, GTX 1080 Ti)
- 19K real papers available in `spike_001_harvest.db`
- All experiment code in `.planning/spikes/002-backend-comparison/experiments/`

## Infrastructure State (verified 2026-03-17)

**PostgreSQL:**
- Version: PostgreSQL 16.13 (Ubuntu 24.04)
- Running on port 5432
- Database: `arxiv_mcp` (126 papers from Phase 10 agent test)
- Connection: `postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp` (password in `~/.env`)
- Test database: `arxiv_mcp_test` (same credentials)
- Auth: password auth via localhost TCP (peer auth fails for this user)

**pgvector:**
- NOT currently installed
- Package available: `postgresql-16-pgvector` version 0.6.0-1 (Ubuntu noble)
- Install: `sudo apt install postgresql-16-pgvector` then `CREATE EXTENSION vector;`
- This requires sudo — confirm with user before installing

**Python drivers:**
- `psycopg2` 2.9.10 — available (synchronous PostgreSQL driver)
- `asyncpg` — available (async driver, used by the main project)
- `psycopg3` — NOT available

**Embeddings:**
- A1c.3 computed embeddings on-the-fly and did NOT persist them
- For Spike 002, first step is to compute and save 19K paper embeddings as `.npy` files
- Use all-MiniLM-L6-v2 on GPU (~33 seconds for 19K papers)
- Save as `embeddings_19k.npy` (float32, shape 19252×384, ~28 MB)

**SQLite (Spike 001 data):**
- Harvest DB: `.planning/spikes/001-volume-filtering-scoring-landscape/experiments/data/spike_001_harvest.db` (19,252 papers, 37 MB)
- FTS5 benchmark DB: `fts5_benchmark.db` (contains scaled data + FTS index)
- Scale duplication methodology: cycle through 19K papers with modified IDs

**Existing project database:**
- The main project's PostgreSQL database (`arxiv_mcp`) has 126 papers, 8 Alembic migrations, full schema (papers, collections, triage_states, interest_signals, etc.)
- For fair comparison, Spike 002 should create a SEPARATE database or schema — don't pollute the project DB
- Recommendation: create `arxiv_mcp_spike002` database, or use a separate schema within `arxiv_mcp`

## Query Set

For reproducibility, the full query set used across Dimensions 1-2 should be defined here. Starting from A1b's 10 queries, extended to 20+:

**From A1b (Spike 001):**
1. `transformer` (single common)
2. `phenomenology` (single specific — rare in CS, tests stemming)
3. `language model` (two-word common)
4. `reinforcement learning agent` (three-word)
5. `attention AND mechanism` (boolean AND)
6. `consciousness OR awareness` (boolean OR)
7. `"large language model"` (phrase)
8. `neural network optimization` (multi-field broad)
9. `RLHF alignment` (narrow specific)
10. `multi-agent system cooperative reinforcement learning` (long)

**Extended for Spike 002:**
11. `Vaswani` (author name — tests name handling)
12. `GAN generative adversarial` (acronym + expansion)
13. `diffusion model image generation` (trending topic)
14. `graph neural network` (specific subfield)
15. `federated learning privacy` (cross-domain)
16. `theorem proof verification` (math-adjacent)
17. `robotics manipulation` (applied CS)
18. `causal inference` (statistics-adjacent)
19. `self-supervised contrastive` (method-specific)
20. `survey` (very common, tests ranking quality)

**Query type distribution:** 5 single-term, 5 multi-word, 3 boolean/phrase, 4 subfield-specific, 3 cross-domain/edge-case.

## Experiment Code Location

`.planning/spikes/002-backend-comparison/experiments/`

## Output

- **FINDINGS.md:** Side-by-side comparison tables for each dimension, reference design comparison
- **DECISION.md:** Tradeoff map, user-facing guidance table, revised deliberation input
- **Feeds into:** Deployment deliberation update, Phase 12 storage abstraction design

---

## Round 2: Remediation (added 2026-03-19)

Round 1 executed all 6 dimensions but declared the spike complete prematurely. The following methodological gaps were identified. Each must be addressed before the spike can be considered complete.

See signal: `sig-2026-03-18-premature-spike002-closure`

### Round 1 Progress (what's done vs. what's not)

| Item | Round 1 Status | Gap |
|------|---------------|-----|
| D1: Search quality — run queries, compute Jaccard/RBO | **Done** | Query-parsing confound, no result inspection, no stemming analysis |
| D2: Search latency at scale | **Done** | A1b baseline not formally reproduced |
| D3: Vector search comparison | **Done** | — |
| D4: Write performance | **Done** | — |
| D5: Operational characteristics | **Done** | — |
| D6: Workflow comparison | **Done** | Simplified workflow, no vector search step |
| Reference design comparison | **Not done** | Explicitly required by DESIGN.md, skipped entirely |
| DECISION.md | **Not done** | Blocked on above gaps |

### D1-R: Search Quality Remediation

Round 1's D1 has a **query-parsing confound**. FTS5's MATCH syntax and PostgreSQL's `websearch_to_tsquery` parse multi-word queries differently. Part of the measured divergence is parser behavior, not search engine quality. Additionally, FTS5 "failures" on hyphenated terms are fixable with query preprocessing that any real application would do.

**D1-R1: Control for query parsing**

Hypothesis: Some of the Jaccard divergence is driven by query parser differences, not search quality differences.

Protocol:
1. For PostgreSQL, run all 20 queries with BOTH `websearch_to_tsquery` and `plainto_tsquery`
2. For FTS5, preprocess queries to escape hyphens (replace `-` with space) and retry the 2 failed queries
3. For multi-word queries, test FTS5 with explicit AND (e.g., `language AND model`) to match `plainto_tsquery` semantics
4. Recompute Jaccard and RBO for each parser variant
5. Report: how much of the divergence is parser-driven vs. stemmer/ranker-driven?

**D1-R2: Stemming analysis**

The DESIGN.md requires: "The analysis should identify where stemming differences drive result divergence."

Protocol:
1. For each query term across the 20 queries, compute the stem under both algorithms:
   - FTS5: Porter stemmer (via Python `nltk.stem.PorterStemmer` or manual)
   - PostgreSQL: English Snowball stemmer (via `SELECT to_tsvector('english', term)` to see tokens)
2. Identify terms where stems differ
3. For the highest-divergence queries (Jaccard < 0.3), trace whether stemming differences explain the divergence
4. Report: which specific terms produce different stems, and how does this affect which papers are retrieved?

**D1-R3: Divergent result inspection**

The DESIGN.md requires: "Sample and inspect: are they relevant?"

Protocol:
1. For the 5 highest-divergence queries (by Jaccard), collect the papers unique to each backend
2. Load paper titles and abstracts for each unique paper
3. For each, assess: is this paper plausibly relevant to the query?
4. Report: are the FTS5-only papers worse, equivalent, or just different from the tsvector-only papers?
5. This is qualitative assessment, not a formal relevance judgment — but it provides signal on whether the Jaccard gap represents a quality gap or a diversity gap.

### D2-R: Baseline Reproduction

The DESIGN.md requires (Methodological Control #5): "Reproduce Spike 001 baselines: Re-run A1b FTS5 and A1c.3 embedding benchmarks first to confirm measurement stability."

Protocol:
1. Re-run the FTS5 benchmark at 19K and 215K scale points using the D2 script (which already does this)
2. Compare Round 2's FTS5 numbers against Spike 001 A1b's original results (in `001/.../data/fts5_benchmark_results.json`)
3. Acceptable variance: ±20% (same hardware, same data, minor OS/cache state differences)
4. If variance exceeds 20%: investigate (thermal throttling, background processes, measurement methodology difference)
5. Report: measurement stability confirmed or not, with specific numbers

### D7: Reference Design Comparison

This was specified in the original DESIGN.md and skipped entirely in Round 1.

Protocol:
1. **arxiv-sanity-lite**: Clone repo, examine search implementation, extract any published performance claims. Measure search latency if runnable, or use documented values. Note: this is a different architecture (Python for-loop search, not database full-text).

2. **Semantic Scholar API**: Run 10 representative queries (subset of our 20), measure response times from this machine. Record:
   - Search latency (p50, p95 over 10 calls per query)
   - Result count
   - Qualitative: do results look relevant?

3. **OpenAlex API**: Same protocol as Semantic Scholar. Use `works` endpoint with `search` parameter.

4. **arXiv API**: Same protocol. Use the search API endpoint.

5. Compile into comparison table:

| System | Search p50 | Search p95 | Local/Remote | Corpus size |
|--------|----------|----------|------------|------------|
| Our FTS5 (19K) | from D2 | from D2 | Local | 19K |
| Our tsvector (19K) | from D2 | from D2 | Local | 19K |
| Our HNSW (19K) | from D3 | from D3 | Local | 19K |
| arxiv-sanity-lite | measured/documented | — | Local | ~30K typical |
| Semantic Scholar API | measured | measured | Remote | 200M+ |
| OpenAlex API | measured | measured | Remote | 250M+ |
| arXiv API | measured | measured | Remote | 2M+ |

6. Analysis: where do our numbers sit relative to systems users actually interact with?

### D6-R: Workflow Revision (Optional)

Round 1's D6 workflow used category-matching for "find_related," not actual similarity search. A workflow with embedding search steps would likely change the comparison.

Protocol:
1. Add a 7-tool workflow variant that includes an embedding similarity step
2. Measure on both backends: SQLite+numpy vs PostgreSQL+pgvector
3. Report: does vector search change the compound workflow comparison?

### Quick Validation Experiments (folded into Spike 002)

These validate mitigations asserted in the deployment deliberation. They use Spike 002 infrastructure.

**QV1: Pre-filtered TF-IDF cosine**

Question: Does category scoping keep TF-IDF similarity <100ms at 215K?

Protocol:
1. Load the 19K embeddings (or recompute TF-IDF matrix from Spike 001 A1c.1)
2. Pre-filter to a single primary category (e.g., cs.AI — ~1,300 papers at 19K, ~15K at 215K)
3. Compute cosine similarity on the filtered subset
4. Measure at scale points: full corpus vs. filtered corpus
5. Report: does pre-filtering bring TF-IDF similarity under 100ms at 215K?

**QV2: Memory-mapped feature loading**

Question: Is mmap actually near-instant for loading 472 MB of features?

Protocol:
1. Save embeddings (28 MB) and a synthetic TF-IDF matrix (~157 MB at 215K) as numpy files
2. Measure load time: `np.load()` (full read) vs `np.memmap()` (memory-mapped)
3. Measure time to first query after mmap (does the OS page fault cause a latency spike?)
4. Measure at file sizes: 28 MB, 157 MB, 472 MB (combined)
5. Report: is "instant startup" a valid claim?

**QV3: MiniLM vs SPECTER2 embedding quality**

Question: Is a general-purpose model good enough for academic abstracts, or does a domain-specific model produce meaningfully better embeddings?

Protocol:
1. Install `adapters` or download SPECTER2 model (allenai/specter2, 768-dim)
2. Compute SPECTER2 embeddings for the 19K corpus (GPU)
3. Pick 10 seed papers. For each, find top-10 similar papers under MiniLM and SPECTER2
4. Compute overlap (Jaccard of top-10)
5. Qualitative inspection: for 3 seed papers, do SPECTER2 results look more topically coherent?
6. Measure: compute time per paper, embedding dimension, memory footprint
7. Report: quality difference, compute cost tradeoff
8. Note: if SPECTER2 is 768-dim (vs MiniLM 384-dim), brute-force search time and HNSW index size both ~double. The D3 comparison would need re-evaluation.

### Alternative Architectural Approaches

The D1 finding (FTS5 ≠ tsvector) raises a question that should be noted here but resolved in the deliberation: **should the search layer be separated from the storage layer?**

Options to evaluate in the deliberation (not experiments — design considerations):
1. Extract search as its own abstraction. Storage does CRUD; search has its own backend (embedding-based, tantivy, or delegated to DB).
2. Always use embedding search for primary retrieval. Keyword search becomes a fallback, not the default. This makes backend choice irrelevant for search quality.
3. Use a standalone search library (tantivy via Python bindings, whoosh) for consistent results regardless of storage backend.

These are not spike experiments — they're design options that the deliberation should weigh using spike findings as evidence.

### Revised Completion Checklist

The spike is complete when ALL of the following are done:

- [ ] D1-R1: Query-parsing confound controlled
- [ ] D1-R2: Stemming analysis completed
- [ ] D1-R3: Divergent results inspected
- [ ] D2-R: A1b baseline reproduction confirmed
- [ ] D7: Reference design comparison completed
- [ ] QV1: Pre-filtered TF-IDF validated
- [ ] QV2: mmap loading validated
- [ ] QV3: MiniLM vs SPECTER2 compared
- [ ] D6-R: Workflow with vector search (optional — do if time permits)
- [ ] FINDINGS.md updated with all Round 2 results and caveats
- [ ] DECISION.md written (tradeoff map, guidance table, deliberation input)
