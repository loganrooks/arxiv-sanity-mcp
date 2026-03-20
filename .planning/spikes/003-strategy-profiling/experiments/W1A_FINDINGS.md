# W1A Findings: Content-Based Strategy Profiles

**Completed:** 2026-03-19
**Scope:** 6 strategies profiled across 8 interest profiles x 3 seed subsets (24 evaluation runs each)
**Corpus:** 19,252 papers
**Instruments:** LOO-MRR, seed proximity, topical coherence, cluster diversity, novelty, category surprise, coverage

## Summary

MiniLM embedding centroid similarity (S1a) is the clear winner among content-based strategies. It achieves 2.16x the MRR of SPECTER2 adapter (S1c), 3.84x the MRR of TF-IDF (S1d), and 2.04x the coverage of SPECTER2. SPECTER2 adapter adds no quality advantage despite 2x storage cost. TF-IDF and SVM produce near-identical recommendations, but SVM is 10x slower per query. Centroid normalization is mathematically irrelevant for ranking with L2-normalized embeddings -- S1a and S1j produce identical results.

## Aggregate Comparison

| Strategy | ID | MRR | Prox | Coher | Div | Novel | Surpr | Cover | p50 ms |
|----------|----|-----|------|-------|-----|-------|-------|-------|--------|
| Random baseline | S6a | 0.000 | 0.282 | 0.178 | 16.4 | 0.929 | 0.740 | 0.000 | 0.7 |
| MiniLM centroid | S1a | 0.398 | 0.764 | 0.643 | 2.5 | 0.046 | 0.094 | 0.686 | 18* |
| SPECTER2 adapter centroid | S1c | 0.184 | 0.725 | 0.584 | 2.9 | 0.052 | 0.094 | 0.336 | 22 |
| TF-IDF cosine | S1d | 0.104 | 0.699 | 0.543 | 4.5 | 0.144 | 0.185 | 0.247 | 20 |
| SVM (TF-IDF) | S1i | 0.103 | 0.692 | 0.530 | 4.8 | 0.158 | 0.188 | 0.241 | 192 |
| MiniLM centroid (raw) | S1j | 0.398 | 0.764 | 0.643 | 2.5 | 0.046 | 0.094 | 0.686 | 18* |

*Latency: S1a reported 38ms in profiling due to cold-cache ordering; controlled re-measurement shows ~5ms for both S1a and S1j. The profiler's latency measurement captures the order-of-run, not the inherent cost.

## Finding 1: MiniLM dominates SPECTER2 on recovery metrics

S1a achieves 2.16x the LOO-MRR and 2.04x the coverage of S1c. This is not a close call.

| Profile | S1a MRR | S1c MRR | Ratio |
|---------|---------|---------|-------|
| P1: RL for robotics | 0.468 | 0.111 | 4.21x |
| P2: Language model reasoning | 0.282 | 0.095 | 2.97x |
| P3: Quantum computing / quantum ML | 0.347 | 0.193 | 1.80x |
| P4: AI safety / alignment | 0.500 | 0.212 | 2.36x |
| P5: Graph neural networks | 0.464 | 0.301 | 1.54x |
| P6: Diffusion models / generation | 0.310 | 0.169 | 1.83x |
| P7: Federated learning + privacy | 0.505 | 0.278 | 1.82x |
| P8: Math foundations of neural nets | 0.307 | 0.113 | 2.71x |

MiniLM wins on every single profile, with advantages ranging from 1.54x (GNNs) to 4.21x (RL for robotics).

**Important caveat:** MRR and coverage measure recovery of papers that are in the same KMeans cluster as the seeds. This rewards strategies that produce tightly clustered recommendations. MiniLM's 384-dim embedding space may be more aligned with KMeans cluster structure than SPECTER2's 768-dim space. The instruments measure what they measure; whether cluster recovery = good recommendations requires qualitative review.

## Finding 2: TF-IDF and SVM are near-identical in quality

S1d and S1i differ by less than 0.02 on every instrument. They produce essentially the same recommendations.

| Instrument | S1d | S1i | Delta |
|------------|-----|-----|-------|
| MRR | 0.104 | 0.103 | 0.001 |
| Proximity | 0.699 | 0.692 | 0.007 |
| Coherence | 0.543 | 0.530 | 0.013 |
| Coverage | 0.247 | 0.241 | 0.006 |

But SVM is 9.7x slower per query (192ms vs 20ms) because it trains a new model on every query. SVM adds no quality value over TF-IDF centroid at this corpus size and seed count.

At much larger corpus sizes or with more seed papers, SVM's discriminative boundary might outperform TF-IDF's centroid averaging. But at 19K papers with 5-15 seeds, the approaches converge.

**Resource costs:**
- TF-IDF build: 2.2s one-time setup
- SVM per-query: 176ms train + score (includes full corpus prediction)
- TF-IDF per-query: ~20ms (sparse matrix-vector multiply)

## Finding 3: Centroid normalization is a no-op for ranking

S1a (normalized centroid) and S1j (raw mean centroid) produce mathematically identical rankings. Every instrument value is identical to floating-point precision across all 24 evaluation runs.

This is expected: for L2-normalized embeddings, `dot(emb, c/||c||)` produces the same ranking as `dot(emb, c)` because dividing by a positive scalar preserves order. The normalization only affects the scale of scores, not their relative ordering.

**Implication:** Use the simpler implementation (raw mean, no normalization step). Centroid normalization is only useful when comparing scores across different seed sets (e.g., for calibration), not for within-query ranking.

## Finding 4: Embedding strategies are much tighter than TF-IDF strategies

MiniLM and SPECTER2 produce recommendations with:
- Lower diversity (2.5-2.9 clusters vs 4.5-4.8)
- Lower novelty (0.05 vs 0.14-0.16)
- Lower category surprise (0.09 vs 0.19)
- Higher coherence (0.58-0.64 vs 0.53-0.54)

This means embedding strategies produce a "more of the same" recommendation pattern -- tightly focused within the seed neighborhood. TF-IDF strategies explore slightly wider, reaching into adjacent topical regions.

Whether this is an advantage or disadvantage depends on the user's intent:
- Researcher monitoring a specific sub-field: tight focus is better
- Researcher looking for cross-disciplinary connections: wider exploration is better

## Finding 5: Profile-dependent performance variation

MRR varies substantially across profiles for all strategies:

| Strategy | Best Profile (MRR) | Worst Profile (MRR) | Range |
|----------|--------------------|----------------------|-------|
| S1a | P7: Federated (0.505) | P2: Language (0.282) | 0.223 |
| S1c | P5: GNNs (0.301) | P2: Language (0.095) | 0.206 |
| S1d | P6: Diffusion (0.194) | P2: Language (0.063) | 0.131 |

P2 (Language model reasoning) and P8 (Math foundations) are consistently harder across all strategies. P4 (AI safety) and P7 (Federated learning) are consistently easier. This likely reflects topic cohesion in the corpus: well-separated topics are easier to recover than broad, overlapping ones.

## Resource Summary

| Strategy | Storage (MB) | Setup | Per-query p50 | Notes |
|----------|-------------|-------|---------------|-------|
| S1a/S1j | 28.5 | Embedding load (instant from .npy) | ~5ms | Matrix-vector multiply |
| S1c | 56.7 | Embedding load (instant from .npy) | ~5ms | Larger matrix, but same operation |
| S1d | 0 (in-memory) | 2.2s (TF-IDF build) | ~20ms | Sparse matrix, still fast |
| S1i | 0 (in-memory) | 2.2s (TF-IDF build) + per-query train | ~192ms | SVM train dominates |

## Implications for Spike 003

1. **S1a (MiniLM centroid) is the primary content strategy.** It wins on every quality metric against every alternative. SPECTER2 adapter does not justify its 2x storage for substantially worse recovery.

2. **SPECTER2 may capture different relatedness** (as found in Spike 001 qualitative review), but those differences do not manifest as higher MRR or coverage. The value of SPECTER2 may lie in combination strategies or in specific profiles -- this is a W2 or W3 question.

3. **TF-IDF centroid is the lexical fallback.** It is the cheapest content strategy with no embedding dependency. Its quality is lower (MRR 0.104 vs 0.398) but non-trivial, and it captures some papers that embedding strategies miss (higher novelty/diversity).

4. **SVM (S1i) is eliminated.** It offers no quality improvement over TF-IDF centroid at 10x the latency cost. The arxiv-sanity-lite SVM approach does not provide value over simple centroid similarity at this scale.

5. **S1j is eliminated as a distinct strategy.** It is mathematically identical to S1a. Use S1a's implementation (with normalization) for score interpretability when needed.
