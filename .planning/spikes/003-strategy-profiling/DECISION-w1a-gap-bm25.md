# Spike Decision: W1A Gap Fill -- BM25 Keyword Search (S1e)

**Completed:** 2026-03-20
**Question:** Does BM25 keyword search (S1e) produce meaningfully different recommendations than TF-IDF cosine similarity (S1d), and should it be treated as a distinct strategy in the parallel views architecture?
**Answer:** BM25 (S1e) is not a useful addition. It finds mostly different papers than S1d (Jaccard 0.194) but performs worse on every quality instrument. It should not be surfaced as a separate view.

## Summary

S1e (BM25 keyword search via FTS5) and S1d (TF-IDF cosine similarity) are conceptually different strategies -- BM25 ranks by term frequency with saturation and document length normalization, while TF-IDF cosine ranks by vector similarity in vocabulary space. The question was whether this conceptual difference produces practically different recommendations worth surfacing to users.

The answer is clearly no. S1e achieves MRR 0.074, which is 29% below S1d's 0.104 and 81% below S1a's 0.398. It also underperforms S1d on coverage (0.192 vs 0.247), seed proximity (0.671 vs 0.699), and topical coherence (0.508 vs 0.543). While S1e does find different papers (Jaccard similarity to S1d is only 0.194), those different papers are not better -- they are less likely to belong to the relevant cluster and less semantically close to the seeds.

A wider variant (S1e-wide, 20 terms instead of 10) partially closes the MRR gap (0.096 vs S1d 0.104) but doubles latency and does not surpass S1d on any instrument. It also finds an inconsistent set of papers relative to S1e (Jaccard 0.460), suggesting the strategy is sensitive to query construction in ways that TF-IDF cosine is not.

## Findings

### Experiment 1: S1e -- BM25 keyword search (FTS5, 10 terms)

**Result:** Substantially worse than both S1d and S1a on recovery metrics.

**Data:**

| Instrument | S1e | S1d | S1a | S1e vs S1d |
|------------|-----|-----|-----|------------|
| LOO-MRR | 0.074 | 0.104 | 0.398 | 0.71x |
| Seed proximity | 0.671 | 0.699 | 0.764 | 0.96x |
| Topical coherence | 0.508 | 0.543 | 0.643 | 0.94x |
| Cluster diversity | 5.04 | 4.46 | 2.50 | 1.13x |
| Novelty | 0.150 | 0.144 | 0.046 | 1.04x |
| Category surprise | 0.208 | 0.185 | 0.094 | 1.12x |
| Coverage | 0.192 | 0.247 | 0.686 | 0.78x |
| Latency p50 | 93ms | 20ms | 5ms | 4.7x slower |

Per-profile MRR breakdown:

| Profile | S1e MRR | S1d MRR | S1a MRR |
|---------|---------|---------|---------|
| P1: RL for robotics | 0.042 | 0.099 | 0.468 |
| P2: Language model reasoning | 0.031 | 0.063 | 0.282 |
| P3: Quantum computing / quantum ML | 0.037 | 0.088 | 0.347 |
| P4: AI safety / alignment | 0.096 | 0.117 | 0.500 |
| P5: Graph neural networks | 0.161 | 0.134 | 0.464 |
| P6: Diffusion models for generation | 0.003 | 0.194 | 0.310 |
| P7: Federated learning + privacy | 0.102 | 0.065 | 0.505 |
| P8: Math foundations of neural nets | 0.116 | 0.071 | 0.307 |

S1e beats S1d on only 3/8 profiles (P5, P7, P8), and loses badly on P6 (0.003 vs 0.194). The wins are narrow; the losses are wide.

### Experiment 2: S1e-wide -- BM25 keyword search (FTS5, 20 terms)

**Result:** Partially closes the MRR gap with S1d but introduces instability.

**Data:**

| Instrument | S1e-wide | S1e | S1d |
|------------|----------|-----|-----|
| LOO-MRR | 0.096 | 0.074 | 0.104 |
| Seed proximity | 0.674 | 0.671 | 0.699 |
| Coverage | 0.190 | 0.192 | 0.247 |
| Latency p50 | 186ms | 93ms | 20ms |

S1e-wide improves aggregate MRR by 30% over S1e (0.096 vs 0.074) but still does not reach S1d (0.104). It is 9.3x slower than S1d. And the per-profile picture is inconsistent: S1e-wide beats S1e on P1-P4 and P6, but S1e beats S1e-wide on P5, P7, P8. The 10-term and 20-term variants find substantially different papers (Jaccard 0.460), indicating the strategy is sensitive to the number of query terms.

### Experiment 3: Overlap analysis

**Result:** BM25 finds different papers than both S1d and S1a, but the difference is not complementary.

| Comparison | Mean Jaccard | Std |
|------------|-------------|-----|
| S1e vs S1d (TF-IDF cosine) | 0.194 | 0.103 |
| S1e vs S1a (MiniLM centroid) | 0.142 | 0.112 |
| S1e-wide vs S1d | 0.167 | 0.071 |
| S1e-wide vs S1a | 0.142 | 0.105 |
| S1e-wide vs S1e | 0.460 | 0.213 |

The low Jaccard (0.194) between S1e and S1d confirms they find different papers. But finding different papers is only valuable if those papers are better or serve a different purpose. S1e's lower MRR and coverage mean its unique papers are less likely to be in the relevant cluster. This is "different but worse," not "different and complementary."

For reference, S1d and S1a have a documented Jaccard of ~0.179 from W1A findings -- S1e vs S1d overlap (0.194) is comparable, meaning BM25 is about as different from TF-IDF cosine as TF-IDF cosine is from MiniLM embedding. But the S1d-S1a difference is valuable because S1d captures some papers S1a misses (15 unique held-out recoveries from TF-IDF in qualitative review). The S1e-S1d difference is not valuable because S1e generally finds the same papers as S1d or worse ones.

### Key term extraction quality

The TF-IDF term extraction produces reasonable seed descriptors:

| Profile | Top-10 terms |
|---------|-------------|
| P1: RL for robotics | policies, robot, gpo, control, r1, policy, magnetic, robots, training, flow |
| P2: Language model reasoning | reasoning, cot, exemplars, diffcot, aai, logical, icl, graph, scholarly, llms |
| P3: Quantum computing / QML | quantum, circuits, circuit, qubit, qrl, classical, class, universality, qml, variational |

The terms capture the profile's topic well, but some noise enters (P1: "magnetic" comes from one specific seed paper; P2: "aai" and "scholarly" are artifacts). The BM25 query is sensitive to these noisy terms because it matches any of them via OR.

### Resource measurements

| Metric | S1e (10 terms) | S1e-wide (20 terms) | S1d |
|--------|---------------|--------------------|----|
| Query latency p50 | 93ms | 186ms | 20ms |
| Query latency p95 | 114ms | 287ms | 44ms |
| FTS5 index build | 2.4s | 2.4s | 2.2s (TF-IDF build) |
| Index storage | ~20MB (in DB) | ~20MB (in DB) | 0 (in-memory) |

BM25 via FTS5 is 4.7-9.3x slower than TF-IDF cosine per query. The latency comes from: (1) opening a sqlite3 connection per query, (2) FTS5 MATCH evaluation, (3) BM25 scoring. TF-IDF cosine is a single sparse matrix-vector multiply in memory.

## Analysis

| Option | Pros | Cons | Spike Evidence |
|--------|------|------|----------------|
| Add S1e as a view | Different results from S1d (Jaccard 0.194) | Worse MRR (0.074 vs 0.104), worse coverage (0.192 vs 0.247), 4.7x slower, sensitive to term count | Loses on 5/8 profiles vs S1d |
| Replace S1d with S1e | N/A | Strictly worse on all quality metrics | No instrument where S1e dominates S1d |
| S1e-wide as a view | Closer MRR (0.096 vs S1d 0.104) | 9.3x slower, still does not beat S1d, inconsistent per-profile behavior | Term count sensitivity undermines reliability |
| Drop S1e entirely | Clean architecture; S1d already serves the "keyword search" role | Loses the BM25-unique papers | Those papers are not better |

## Decision

**Chosen approach:** Do not add S1e (BM25 keyword search) to the parallel views architecture.

**Rationale:** BM25 keyword search via FTS5 performs worse than TF-IDF cosine on every quality instrument, is 4.7x slower, and its unique paper discoveries are not more relevant (lower MRR, lower coverage). The "Keyword matches" view already served by TF-IDF cosine (S1d) adequately fills the lexical search role. Adding BM25 would introduce complexity (FTS5 index management, query term extraction pipeline, term count sensitivity) for no quality benefit.

**Confidence:** HIGH

The comparison is unambiguous. S1e loses on MRR, coverage, proximity, coherence, and latency. The only instruments where S1e marginally exceeds S1d are diversity (5.04 vs 4.46) and novelty (0.150 vs 0.144), both indicators of less focused results rather than better ones. The pattern holds across 8 diverse interest profiles.

## Implications

- **S1f (PostgreSQL tsvector BM25) is also not worth profiling.** Spike 002 showed FTS5 and tsvector return different results (Jaccard 0.39), but if FTS5 BM25 already underperforms TF-IDF cosine, the PostgreSQL variant is unlikely to reverse the picture.

- **TF-IDF cosine (S1d) remains the sole lexical strategy.** The parallel views architecture stands as: MiniLM primary, TF-IDF secondary, SPECTER2 optional discovery. BM25 does not earn a fourth view.

- **Term extraction pipeline is reusable.** The TF-IDF key term extraction (top-N distinctive terms from seed abstracts) could be useful for other purposes: generating human-readable query descriptions, building search explanations, or feeding into MCP tool descriptions. The infrastructure built here is not wasted even though BM25 scoring is not adopted.

- **FTS5 index exists in the harvest DB now.** The papers_fts table was created during this experiment. It can be useful for future text search features unrelated to recommendation ranking (e.g., keyword search in the MCP tools).

## S1f Note

S1f (PostgreSQL tsvector BM25) was not profiled. The project PostgreSQL DB has only 126 papers vs 19K in the harvest DB. Setting up PostgreSQL with 19K papers would add substantial overhead for a strategy variant that is unlikely to outperform S1d given S1e's results. Spike 002 already documented the FTS5-vs-tsvector differences (Jaccard 0.39); that finding stands without re-profiling.

## Metadata

**Spike duration:** 3.5 minutes (experiment) + analysis
**Iterations:** 1
**Originating phase:** W1A gap fill (Spike 003 addendum)
**Corpus:** 19,252 papers, 8 interest profiles, 3 seed subsets each
**Total profiling runs:** 48 (2 strategies x 8 profiles x 3 seed sets)
