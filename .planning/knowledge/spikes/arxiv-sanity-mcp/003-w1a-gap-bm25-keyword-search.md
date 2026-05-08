---
id: spk-2026-03-20-bm25-keyword-search
type: spike
project: arxiv-sanity-mcp
tags: [bm25, fts5, keyword-search, tfidf, recommendation-strategies, content-strategies]
created: 2026-03-20T16:00:00Z
updated: 2026-03-20T16:00:00Z
durability: convention
status: active
hypothesis: "BM25 keyword search via FTS5 (S1e) produces meaningfully different and potentially better recommendations than TF-IDF cosine similarity (S1d)"
outcome: rejected
rounds: 1
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## Hypothesis

BM25 keyword search (extracting key TF-IDF terms from seeds, querying FTS5 with OR-of-terms, ranking by BM25) may find different and complementary papers compared to TF-IDF cosine similarity, justifying a separate view in the parallel views architecture.

## Experiment

Profiled S1e (BM25 via FTS5, 10 key terms) and S1e-wide (20 key terms) against the same 19,252-paper corpus, 8 interest profiles, and 7 quality instruments used in the original W1A content strategy profiling. Computed recommendation overlap (Jaccard similarity) between BM25 and both S1d (TF-IDF cosine) and S1a (MiniLM centroid). Tested term count sensitivity by comparing 10-term vs 20-term variants.

## Results

S1e MRR 0.074 (29% below S1d 0.104, 81% below S1a 0.398). S1e coverage 0.192 vs S1d 0.247. BM25 finds different papers (Jaccard 0.194 vs S1d) but those papers are less relevant, not more. S1e 4.7x slower than S1d (93ms vs 20ms p50). The 20-term variant partially closes the MRR gap (0.096) but is 9.3x slower and inconsistent across profiles. BM25 is sensitive to term count selection in ways TF-IDF cosine is not.

## Decision

Do not add BM25 keyword search to the parallel views architecture. TF-IDF cosine (S1d) adequately fills the lexical search role with better quality and lower latency. BM25 finds different papers but not better ones. S1f (PostgreSQL tsvector) also deprioritized given these results.

## Consequences

- TF-IDF cosine remains the sole lexical strategy (confirmed, not just default)
- S1f profiling unnecessary -- FTS5 BM25 already loses to TF-IDF cosine
- Term extraction pipeline (TF-IDF top-N terms) reusable for query explanations
- FTS5 index now exists in harvest DB for potential future text search features
