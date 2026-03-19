# Spike 002 Decision: SQLite vs PostgreSQL Backend Tradeoffs

**Date:** 2026-03-19
**Status:** Complete (with qualified limitations)

## Tradeoff Map

| Dimension | SQLite | PostgreSQL | Confidence | Limitations |
|-----------|--------|------------|------------|-------------|
| **Keyword search speed** | 3.5–4.8x faster (2ms vs 7ms at 19K) | Slower but interactive | High | Both are 20–100x faster than APIs users actually use (D7). The gap is experientially invisible. |
| **Keyword search results** | FTS5 returns different top-20 (Jaccard 0.39) | tsvector returns different top-20 | High | Divergence is ranking-function-driven (BM25 vs cover density), not quality-driven. Both return plausible papers (D1-R3). Neither evaluated against human relevance judgments. |
| **Vector search speed** | Numpy brute-force: 3–14ms (linear) | HNSW: 0.6–1ms (near-constant), recall ≥0.91 | High | HNSW provides genuine value at all tested scales. |
| **Vector search setup** | Zero setup | Requires pgvector extension + HNSW index build (4–80s) | High | — |
| **Bulk import** | 5–6x faster | Slower | High | Neither is a user experience problem (1.5s vs 8.6s at 19K). |
| **Concurrent R+W** | WAL mode: zero degradation | MVCC: zero degradation | High | Both handle harvest daemon + MCP server coexistence. |
| **Multi-writer** | Not supported | Full MVCC | High | Only relevant for shared/hosted deployments. |
| **Connection setup** | 0.2ms | 19ms | High | Negated by connection pooling. |
| **Backup** | File copy (instant) | pg_dump (seconds) | High | — |
| **Disk space** | 2x smaller | 2x larger | High | — |
| **Deployment** | Zero-dependency, single file | Requires PostgreSQL server | High | Docker-compose can reduce PG friction. |

## Qualified Findings

### What we can confidently state

1. **FTS5 and tsvector are not interchangeable** — they return different papers for the same queries. The divergence is driven by different ranking functions (BM25 variant vs cover density), not stemming (only 2/41 terms differ) or query parsing (+0.045 Jaccard from parser fix). Both sets of results are plausible upon inspection.

2. **pgvector HNSW provides genuine value at all tested scales** — 5–23x faster than numpy brute-force, near-constant ~0.8ms regardless of corpus size.

3. **All latency differences are experientially irrelevant** — our slowest operation (tsvector at 215K: 101ms) is faster than the fastest external API users interact with (arXiv API: 148ms).

4. **Both backends handle the workload** — concurrent read+write, daily harvest, MCP tool invocations all work on both.

### What we cannot state (open questions)

1. **Which backend produces "better" search results** — we showed they differ, not which is better. The qualitative review was done for embedding strategies, not for FTS5 vs tsvector. This is an open question.

2. **Whether the 215K benchmark numbers are reliable** — synthetic scaling (19K papers cycled 11x) means vocabulary doesn't grow. Real 215K corpora would behave differently.

3. **Whether HNSW default parameters are optimal** — we used m=16, ef_construction=64, ef_search=40 without testing alternatives.

4. **Measurement stability** — D2-R found 20–60% drift from A1b baseline. Absolute numbers have systematic variance; relative comparisons (ratios) are valid.

## User-Facing Guidance

For a user choosing a backend:

| If you want... | Choose... | Because... |
|----------------|-----------|------------|
| Simplest possible setup | SQLite | Zero dependencies, single file, `pip install` and go |
| Fastest keyword search | SQLite | 3.5–4.8x faster, though both are under 10ms at 19K |
| Best vector/semantic search | PostgreSQL + pgvector | HNSW is dramatically faster and scales near-constantly |
| Hosted/shared deployment | PostgreSQL | Multi-writer concurrency via MVCC |
| Smallest disk footprint | SQLite | 2x smaller than PostgreSQL |
| Both keyword and vector search | PostgreSQL | Unified backend for both capabilities |

**For most users:** PostgreSQL with docker-compose gives the best experience — full feature set, good search quality, vector search via pgvector, minimal setup friction.

**For maximum simplicity:** SQLite works for everything except vector search speed at scale and multi-writer.

## Impact on Deliberation

The deployment deliberation's tier model should reflect:
- Backend choice affects search result diversity (different ranking functions produce different top-20), but NOT quality in a way we can measure
- pgvector is valuable at personal scale, not just at >1M papers (revises Spike 001 claim)
- The latency differences don't matter for user experience (D7 reference comparison)
- The real differentiators are: deployment simplicity (SQLite) vs feature completeness (PostgreSQL + pgvector)

## Open for Spike 003

- Qualitative evaluation of FTS5 vs tsvector results (like we did for embedding models)
- HNSW parameter sensitivity analysis
- Whether docker-compose eliminates enough PostgreSQL friction to make it the default
