# W3.4 Gap Fill: Cross-Encoder Reranking Findings

**Completed:** 2026-03-20
**Duration:** 9.4 minutes (566s)
**Scope:** 2 cross-encoder pipeline strategies, S1a baseline, P5 convergent baseline. 8 profiles x 3 seed sets = 24 observations per strategy. Latency profiling at 3 pool sizes. Divergence and TF-IDF rescue analysis.
**Corpus:** 19,252 papers, 8 interest profiles
**Cross-encoder model:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (MS MARCO, 512 token limit)

## Context

W3.4 tested retrieve+rerank pipelines but only used MiniLM embedding similarity as the reranker. This produced the "convergence to MiniLM" pattern: P5/P6 (union retrieval + MiniLM rerank) produced MRR 0.3979, bit-identical to S1a standalone. MiniLM as reranker re-imposes its own ranking, discarding TF-IDF's unique candidates.

B1 (signal literature review) found that production IR systems use multi-stage pipelines with cross-encoder reranking. Cross-encoders are architecturally different from bi-encoders: they take raw (query, document) text pairs and produce relevance scores via cross-attention, rather than comparing pre-computed embedding vectors. This means a cross-encoder could potentially value TF-IDF's unique candidates differently than MiniLM does.

## Strategies Tested

| ID | Pipeline | Architecture |
|----|----------|-------------|
| S4a | MiniLM top-50 -> cross-encoder rerank | retrieve-crossencoder-rerank |
| S4a-union | (TF-IDF top-100 + MiniLM top-100) -> cross-encoder rerank | union-crossencoder-rerank |
| S1a | MiniLM centroid (baseline) | direct embedding similarity |
| P5 | (TF-IDF + MiniLM) top-100 -> MiniLM rerank | union-embedding-rerank (convergent) |

Query construction: concatenation of top-3 seed paper titles separated by ` | `. Titles average ~25 tokens, so 3 titles consume ~75 of the 512 token budget, leaving ~437 tokens for the candidate abstract (~350 tokens typical). This fits within the cross-encoder's positional embedding limit.

## Results

### Quality Metrics

| Strategy | MRR | dMRR vs S1a | Coverage | Novelty | Diversity | p50 (ms) |
|----------|-----|-------------|----------|---------|-----------|----------|
| S1a (baseline) | 0.398 | -- | 0.686 | 0.046 | 2.5 | 56.7 |
| P5 (MiniLM rerank) | 0.398 | 0.000 | 0.686 | 0.046 | 2.5 | 136.0 |
| S4a (CE k=50) | 0.117 | -0.281 | 0.395 | 0.044 | 3.0 | 231.6 |
| S4a-union (CE k=100) | 0.058 | -0.340 | 0.214 | 0.090 | 3.9 | 572.4 |

### Per-Profile Breakdown

| Profile | S1a MRR | P5 MRR | S4a MRR | S4a-union MRR |
|---------|---------|--------|---------|---------------|
| P1: RL for robotics | 0.468 | 0.468 | 0.144 | 0.064 |
| P2: Language model reasoning | 0.282 | 0.282 | 0.104 | 0.034 |
| P3: Quantum computing | 0.347 | 0.347 | 0.091 | 0.079 |
| P4: AI safety | 0.500 | 0.500 | 0.126 | 0.088 |
| P5: GNNs | 0.464 | 0.464 | 0.129 | 0.098 |
| P6: Diffusion models | 0.310 | 0.310 | 0.090 | 0.025 |
| P7: Federated learning | 0.505 | 0.505 | 0.082 | 0.057 |
| P8: Math foundations | 0.307 | 0.307 | 0.167 | 0.020 |

Cross-encoder degrades quality uniformly across all 8 profiles. No profile benefits.

## Analysis

### Finding 1: Cross-encoder breaks the convergence pattern but in the wrong direction

The cross-encoder does produce genuinely different rankings from MiniLM:

- **Jaccard overlap (S4a-union vs S1a):** 0.168 (only 5.6/20 papers in common)
- **CE-unique papers per evaluation:** 14.4/20
- **Rank correlation of shared papers:** 0.029 (near zero -- effectively uncorrelated)

This confirms the cross-encoder is NOT simply re-implementing MiniLM's rankings. It applies a fundamentally different relevance function. But that different function produces dramatically worse results on our evaluation framework: MRR 0.058 vs 0.398. The cross-encoder values different papers, but the papers it values are not the ones in our held-out ground truth.

### Finding 2: The cross-encoder does rescue TF-IDF candidates -- but the wrong ones

The TF-IDF rescue analysis shows:

| Metric | Value |
|--------|-------|
| Total TF-IDF-unique candidates across evaluations | 1,274 |
| Rescued by cross-encoder to top-20 | 120 (9.4%) |
| Rescued by S1a to top-20 | 0 (0%) |
| Rescued into top-20 AND in held-out set | 6 |

The cross-encoder does promote TF-IDF-unique candidates (9.4% rescue rate vs 0% for MiniLM reranker). And 6 of those rescued candidates were held-out ground truth papers. But it also promotes many TF-IDF candidates that are NOT relevant, while simultaneously demoting MiniLM's high-quality candidates. The net effect is strongly negative.

### Finding 3: Domain mismatch explains the degradation

`cross-encoder/ms-marco-MiniLM-L-6-v2` is trained on MS MARCO passage ranking -- web search queries matched to web passages. The query-document paradigm (short informational query -> relevant web passage) does not match the academic paper recommendation paradigm (paper titles as query -> paper abstracts as documents).

Key mismatches:
1. **Query format:** MS MARCO queries are natural language questions ("what causes rain"). Our "queries" are concatenated paper titles -- formal, jargon-heavy, structurally unlike search queries.
2. **Document format:** MS MARCO passages are web text. Our documents are scientific abstracts with domain-specific vocabulary, mathematical notation, and citation patterns.
3. **Relevance definition:** MS MARCO relevance is "does this passage answer this question." Our relevance is "is this paper related to these seed papers" -- a fundamentally different task (topical similarity, not answer retrieval).

The cross-encoder's relevance judgments reflect web-search relevance, not academic relatedness. A paper abstract that "answers" the seed title query (by matching surface terms) is scored highly, even if it is topically unrelated. Conversely, a semantically related paper that uses different vocabulary is scored low because it does not "answer" the query.

### Finding 4: Latency is prohibitive for real-time use

| Pool Size | Cross-Encoder p50 | MiniLM Reranker p50 | Ratio |
|-----------|-------------------|---------------------|-------|
| 50 | 157 ms | 0.2 ms | 941x |
| 100 | 283 ms | 0.4 ms | 742x |
| 200 | 557 ms | 0.7 ms | 764x |

Cross-encoder latency: ~2.8 ms per candidate pair. For a 100-candidate pool, total rerank time is 283 ms. This is marginal for interactive use (under 500ms) but 700-940x slower than embedding-based reranking. For batch processing it is acceptable; for real-time MCP tool responses, it adds significant latency to an already-fast pipeline.

The per-candidate cost is roughly constant (2.8-3.1 ms), indicating GPU batching is working but the transformer forward pass per pair is the bottleneck.

## Conclusions

### Cross-encoder reranking is not viable for this application

The MS MARCO cross-encoder fails on both axes:
1. **Quality:** MRR drops from 0.398 to 0.058-0.117 (71-85% degradation)
2. **Latency:** 700-940x slower than embedding reranking

The quality failure is not inherent to cross-encoders as an architecture -- it is a domain mismatch. A cross-encoder fine-tuned on academic paper relevance judgments might perform differently. But:

1. No such model exists as a readily available checkpoint
2. Fine-tuning would require labeled academic relevance data we do not have
3. The latency cost would remain (though acceptable for batch processing)

### The convergence-to-MiniLM pattern is confirmed as fundamental

The W3.4 findings now cover both possible reranker types:
- **Embedding reranker (MiniLM):** Converges to S1a standalone (MRR 0.398 = 0.398). The reranker simply re-imposes its own ranking.
- **Cross-encoder reranker (MS MARCO):** Diverges dramatically (Jaccard 0.168) but to worse quality (MRR 0.058). A different relevance function does not help if it is the wrong relevance function.

The implication: within the tools currently available, there is no reranker that can break MiniLM's convergence pattern while also improving quality. The pipeline architecture cannot rescue TF-IDF's unique candidates without either (a) a domain-specific cross-encoder or (b) a fundamentally different approach to combining signals.

This reinforces the parallel views decision: since no combination or pipeline architecture improves over individual strategies, presenting strategies as separate views is the correct architecture.

## Data Files

- Full results: `experiments/data/w3_4_gap_crossencoder_profiles.json`
- Script: `experiments/w3_4_gap_crossencoder.py`
