---
id: spk-2026-03-20-crossencoder-reranking
type: spike
project: arxiv-sanity-mcp
tags: [cross-encoder, reranking, pipeline, ms-marco, retrieve-rerank, combination-strategies, latency]
created: 2026-03-20T16:41:00Z
updated: 2026-03-20T16:41:00Z
durability: convention
status: active
hypothesis: "A cross-encoder reranker (ms-marco-MiniLM-L-6-v2) can break the MiniLM convergence pattern in retrieve+rerank pipelines by valuing TF-IDF's unique candidates differently than MiniLM embedding similarity does"
outcome: rejected
rounds: 1
runtime: claude-code
model: claude-opus-4-6[1m]
gsd_version: 1.17.5+dev
---

## Hypothesis

W3.4 found that MiniLM as reranker in retrieve+rerank pipelines converges exactly to MiniLM standalone (MRR 0.398 = 0.398). A cross-encoder reranker, which uses cross-attention on raw (query, document) text pairs rather than pre-computed embedding comparison, might value TF-IDF's unique candidates differently, breaking the convergence pattern and improving pipeline quality.

## Experiment

Tested two cross-encoder pipeline architectures against the S1a baseline and the convergent P5 pipeline on the same 19,252-paper corpus with 8 interest profiles and 24 observations per strategy:

- **S4a:** MiniLM retrieve top-50 -> cross-encoder rerank -> top-20
- **S4a-union:** (TF-IDF top-100 + MiniLM top-100) union -> cross-encoder rerank -> top-20

Cross-encoder model: `cross-encoder/ms-marco-MiniLM-L-6-v2` (MS MARCO passage ranking, 512 token limit). Query: concatenation of top-3 seed paper titles. Document: candidate abstract. Measured all 7 quality instruments plus latency profiling at pool sizes 50, 100, and 200.

## Results

Cross-encoder breaks convergence (Jaccard 0.168 vs S1a, rank correlation 0.029) but to dramatically worse quality: S4a MRR 0.117 (-71%), S4a-union MRR 0.058 (-85%). Quality degradation is uniform across all 8 profiles. Cross-encoder does rescue TF-IDF-unique candidates (9.4% rescue rate, 120 candidates promoted, 6 held-out) but simultaneously demotes MiniLM's high-quality candidates, netting strongly negative.

Root cause: MS MARCO domain mismatch. The cross-encoder evaluates web-search-style query-passage relevance ("does this passage answer this question?"), not academic paper relatedness ("is this paper topically similar to these seed papers?"). Paper titles as queries and abstracts as documents do not match the training distribution.

Latency: 2.8 ms per candidate pair (700-940x slower than MiniLM embedding reranking). Pool of 100 candidates: 283 ms CE vs 0.4 ms MiniLM. Marginal for interactive use, prohibitive if pipeline runs on every query.

## Decision

Cross-encoder reranking is not viable with available checkpoints. This closes the last untested pipeline architecture from the W3.4 design. The two reranker types produce opposite failure modes: MiniLM reranking converges (no benefit); cross-encoder reranking diverges (catastrophic loss). No middle ground exists with available models, reinforcing the parallel views architecture as the correct approach.

## Consequences

- Cross-encoder reranking eliminated from architecture options (S4a added to eliminated strategies list)
- Pipeline architecture decisively ruled out -- both embedding and cross-encoder rerankers fail to improve over S1a standalone
- Domain-specific cross-encoder (trained on academic paper relatedness) is a potential future investigation, but requires labeled training data and fine-tuning infrastructure that do not exist
- Parallel views architecture further strengthened as the only viable approach to combining complementary strategies
- Latency measurements establish cross-encoder cost: ~3 ms per candidate pair, usable in batch processing but not for real-time reranking at scale
