# Spike 002 Findings: SQLite vs PostgreSQL Backend Comparison

**Date:** 2026-03-18
**Status:** ROUND 1 — Provisional. Methodological gaps identified 2026-03-19 require Round 2 remediation before conclusions can be treated as final. See DESIGN.md Round 2 section.
**Hardware:** Intel Xeon W-2125 (4c/8t), 32 GB RAM, GTX 1080 Ti (11 GB), NVMe SSD
**Corpus:** 19,252 real arXiv papers (scaled to 215K via ID cycling for scale tests)
**Embedding model:** all-MiniLM-L6-v2 (384-dim, normalized)

### Methodological Caveats (added 2026-03-19)

These issues were identified after Round 1 and will be addressed in Round 2:

1. **D1 query-parsing confound:** FTS5 MATCH and PostgreSQL `websearch_to_tsquery` parse multi-word queries differently. Some measured divergence may be parser behavior, not search quality. Round 2 tests `plainto_tsquery` alongside.
2. **D1 divergent results not inspected:** Jaccard measures disagreement, not which backend returns better papers. Neither has been evaluated against human relevance. "H1 falsified" should read "backends disagree" — not "one is better."
3. **D1 stemming analysis not done:** DESIGN.md required identifying where stemming differences drive divergence. Not performed.
4. **D2 baseline not reproduced:** DESIGN.md required re-running A1b to confirm measurement stability. Not performed.
5. **Reference design comparison skipped:** Required by DESIGN.md — not performed.
6. **DECISION.md not written:** Blocked on above gaps.
7. **Scale data is synthetic:** 215K benchmarks use 19K unique papers cycled ~11x. Vocabulary doesn't grow with scale.

D3-D6 measurements are methodologically sound and do not require remediation.

## Hypothesis Results

| Hypothesis | Result | Summary |
|------------|--------|---------|
| **H1:** FTS5 and tsvector return substantially similar results | **FALSIFIED** | Average Jaccard 0.39 (below 0.5 threshold). 13/20 queries show low agreement. |
| **H2:** PostgreSQL tsvector latency differs measurably from FTS5 | **CONFIRMED** | tsvector is 3.5–4.8x slower across all scale points. |
| **H3a:** pgvector HNSW latency differs from numpy brute-force | **CONFIRMED** | HNSW is 5–23x faster than numpy, near-constant ~0.8ms regardless of scale. |
| **H3b:** pgvector filtered search provides an advantage | **MIXED** | pgvector filtered is slower than numpy pre-filter at 19K (8ms vs 5.6ms), but ergonomically simpler. |
| **H4:** Write performance differs between backends | **CONFIRMED** | PostgreSQL is 3–5x slower for bulk import; both handle concurrent reads+writes without degradation. |

## Dimension 1: Search Result Quality

**This is the most important finding.** Speed comparisons are moot if the backends return different papers.

| Query Type | Avg Jaccard | Interpretation |
|-----------|-------------|----------------|
| Rare terms (phenomenology, math-adjacent) | 1.0 | Agreement is trivial — small candidate pools |
| Single common (transformer) | 0.67 | Moderate divergence |
| Multi-word (language model) | 0.03 | **Near-complete disagreement** |
| Boolean/phrase | 0.21–0.33 | Substantial divergence |
| Subfield-specific | 0.18–0.33 | Substantial divergence |
| Author names | 1.0 (both empty) | Neither found "Vaswani" in abstracts |

**Overall:** Average Jaccard **0.39**, Average RBO **0.31**

**Root causes of divergence:**
1. **Stemming differences:** FTS5 porter tokenizer vs PostgreSQL english Snowball stemmer produce different stems
2. **Ranking functions:** FTS5 uses BM25 variant; tsvector uses `ts_rank_cd` (cover density). Different ranking → different top-20 even when candidate sets overlap
3. **Query parsing:** FTS5 treats hyphens as column separators ("self-supervised" → error); `websearch_to_tsquery` handles them correctly
4. **Multi-word handling:** FTS5 treats "language model" as implicit OR with proximity boost; tsvector treats it as AND of individual terms

**FTS5 failures:** Two queries fail entirely — "self-supervised contrastive" and "multi-agent system cooperative reinforcement learning" — because FTS5 parses hyphens as syntax. tsvector handles both correctly.

**Implication:** Choosing between FTS5 and tsvector is not just a performance decision — it is a **retrieval quality** decision. They are not interchangeable search backends.

## Dimension 2: Search Latency at Scale

| Scale | FTS5 p50 | tsvector p50 | Ratio |
|------:|--------:|-----------:|------:|
| 5K | 0.91 ms | 3.39 ms | 3.7x |
| 10K | 1.48 ms | 5.15 ms | 3.5x |
| 19K | 1.95 ms | 6.73 ms | 3.5x |
| 50K | 4.91 ms | 19.35 ms | 3.9x |
| 100K | 10.15 ms | 49.06 ms | 4.8x |
| 215K | 22.00 ms | 101.46 ms | 4.6x |

FTS5 is consistently 3.5–4.8x faster for keyword search. Both are well under 500ms at all scale points. At 215K, tsvector's ~100ms is noticeable but not slow. The highest individual query (phrase search at 215K) hits 619ms on tsvector vs 91ms on FTS5.

**Worst-case queries by type (at 215K):**

| Query Type | FTS5 p50 | tsvector p50 |
|-----------|--------:|-----------:|
| phrase ("large language model") | 91 ms | 619 ms |
| two_word ("language model") | 93 ms | 536 ms |
| boolean_or ("consciousness OR awareness") | 36 ms | 291 ms |
| single_common ("transformer") | 34 ms | 236 ms |

Phrases and broad OR queries are the worst case for tsvector.

## Dimension 3: Vector Search

| Scale | Numpy brute-force | pgvector exact | pgvector HNSW | HNSW Recall@20 |
|------:|------------------:|---------------:|--------------:|---------------:|
| 5K | 4.75 ms | 3.03 ms | 0.91 ms | 0.98 |
| 10K | 3.00 ms | 5.69 ms | 0.74 ms | 0.99 |
| 19K | 2.99 ms | 11.38 ms | 0.97 ms | **1.00** |
| 50K | 5.02 ms | 21.06 ms | 0.77 ms | 0.97 |
| 100K | 7.02 ms | 37.37 ms | 0.72 ms | 0.98 |
| 215K | 13.74 ms | 64.84 ms | 0.59 ms | 0.91 |

**Key finding:** pgvector HNSW is dramatically faster than both alternatives and scales near-constantly (~0.6–1.0ms regardless of corpus size). This directly falsifies the Spike 001 claim that "pgvector is unnecessary at personal scale."

- At 19K: HNSW is 3x faster than numpy (1ms vs 3ms) with perfect recall
- At 215K: HNSW is 23x faster than numpy (0.6ms vs 14ms) with 91% recall
- pgvector exact search is slower than numpy (IPC overhead), confirming the HNSW index is the value proposition

**HNSW recall** stays ≥0.91 across all scale points with default parameters (m=16, ef_construction=64, ef_search=40). At 215K the 91% recall means ~2 of the top-20 differ from exact results — acceptable for discovery workflows where diversity has value.

**Filtered search (19K, cs.AI category):**
- Numpy pre-filter: 5.64 ms (filter 19K→1318 IDs, then brute-force)
- pgvector WHERE+ORDER: 8.07 ms
- pgvector filtered is slower here because the planner falls back to sequential scan on a small filtered set. The ergonomic advantage (single SQL query vs manual filter+search) may matter more than the 2.4ms difference.

## Dimension 4: Write Performance

### Bulk Import

| Scale | SQLite total | PG total | Ratio |
|------:|-----------:|--------:|------:|
| 5K | 0.41 s | 2.36 s | 5.8x |
| 10K | 0.72 s | 4.78 s | 6.6x |
| 19K | 1.48 s | 8.56 s | 5.8x |
| 50K | 4.41 s | 23.78 s | 5.4x |
| 100K | 8.26 s | 44.61 s | 5.4x |
| 215K | 19.89 s | 98.00 s | 4.9x |

SQLite bulk import is 5–6x faster. Both include full-text index build time. For cold start with 19K papers, SQLite finishes in 1.5s vs PostgreSQL in 8.6s — neither is a user experience problem.

### Concurrent Read+Write (PostgreSQL)

| Write rate | Search p50 | Errors |
|----------:|----------:|-------:|
| 10/s | 10.24 ms | 0 |
| 50/s | 9.49 ms | 0 |
| 100/s | 10.44 ms | 0 |

PostgreSQL shows zero search degradation under write load (MVCC), matching SQLite's WAL mode result from Spike 001 A1c.2. Both backends handle concurrent read+write without issues.

## Dimension 5: Operational Characteristics

### Connection Setup

| Backend | p50 |
|---------|----:|
| SQLite | 0.225 ms |
| PostgreSQL | 19.463 ms |

PostgreSQL connection setup is ~87x slower. For MCP tool invocations using a connection pool (single long-lived connection), this is irrelevant. For per-tool-call connections, it adds ~20ms overhead per tool call.

### Backup/Restore (19K)

| Backend | Backup | Restore |
|---------|------:|-------:|
| SQLite | 0.028 s | 0.019 s |
| PostgreSQL | 0.733 s | — |

SQLite backup is a file copy (instant). PostgreSQL requires pg_dump (0.7s for 19K). At 215K, SQLite backup would be ~0.3s (proportional to file size); PostgreSQL pg_dump would be ~8s.

### Disk Footprint

| Scale | SQLite (data+FTS) | PostgreSQL (data+tsvector+GIN) | Ratio |
|------:|-----------------:|------------------------------:|------:|
| 5K | 14.6 MB | 30.1 MB | 2.1x |
| 19K | 50.4 MB | 107.0 MB | 2.1x |
| 100K | 259.2 MB | 517.2 MB | 2.0x |
| 215K | 553.2 MB | 1,101 MB | 2.0x |

PostgreSQL uses consistently 2x the disk space. Adding pgvector embeddings (28 MB at 19K for the embedding table + 38 MB for HNSW index) increases the gap further.

## Dimension 6: Workflow-Level Comparison

**6-tool MCP workflow** (search → get_paper → find_related → triage → add_to_collection → check_watch) at 19K papers:

| Backend | p50 | p95 |
|---------|----:|----:|
| SQLite | 14.56 ms | 25.32 ms |
| PostgreSQL | 20.75 ms | 27.70 ms |
| **Ratio** | **1.4x** | **1.1x** |

The compound workflow shows only 1.4x difference (6ms absolute). Both are well under 100ms for a complete 6-tool workflow. At p95, the gap narrows to 1.1x — the variation noise approaches the signal.

**Note:** This workflow does not include vector search. A workflow with semantic search steps would likely favor PostgreSQL+pgvector over SQLite+numpy due to HNSW's speed advantage.

## Tradeoff Map

| Dimension | SQLite advantage | PostgreSQL advantage | Magnitude |
|-----------|-----------------|---------------------|-----------|
| **Search quality** | — | Better stemming, handles hyphens, no parse errors | **Major** (Jaccard 0.39) |
| **Search latency** | 3.5–4.8x faster | — | Moderate (both <500ms) |
| **Vector search** | — | HNSW 5–23x faster, near-constant time | **Major** |
| **Bulk import** | 5–6x faster | — | Minor (cold start only) |
| **Concurrent R+W** | Tie | Tie | None |
| **Connection setup** | 87x faster | — | Minor (pooling negates) |
| **Backup** | File copy (instant) | pg_dump (seconds) | Minor |
| **Disk space** | 2x smaller | — | Moderate |
| **Deployment** | Zero-dependency, single file | Requires PostgreSQL server | Moderate |
| **Multi-writer** | WAL (limited) | MVCC (full) | Depends on use case |
| **Filtered vector search** | — | Single SQL query (ergonomic) | Minor |

## Revised Assessment of Spike 001 Claims

| Spike 001 Claim | Status | Evidence |
|-----------------|--------|----------|
| "SQLite is sufficient for personal scale" | **Partially supported** | True for latency and write performance. False for search quality (FTS5 returns different papers than tsvector) and vector search (HNSW dramatically outperforms numpy). |
| "pgvector unnecessary at personal scale" | **Falsified** | HNSW is 5–23x faster than brute-force numpy and scales near-constantly. At 215K, the gap is 0.6ms vs 14ms. The index provides genuine value even at modest scale. |
| "Tier differentiator is GPU, not database" | **Partially supported** | GPU matters for embedding computation (20x from Spike 001). But the database matters for both search quality and vector search speed. The tier model needs both dimensions. |

## What These Numbers Don't Tell You

1. **Search quality is relative to the user.** We measured Jaccard overlap between backends, not relevance to user intent. FTS5 might return better papers for some queries; tsvector for others. Neither has been evaluated against human relevance judgments.

2. **All latencies are local.** Network latency for hosted deployments would dwarf the SQLite/PostgreSQL differences.

3. **Scale was achieved by cycling.** The 215K benchmark uses 19K unique papers duplicated ~11x. Real 215K corpora would have more vocabulary diversity, potentially affecting search behavior differently.

4. **These are operation-level benchmarks.** Real MCP usage patterns (bursty, agent-driven, with pauses for LLM reasoning) differ from sustained benchmark loops.
