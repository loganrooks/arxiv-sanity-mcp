# W5 Findings: Voyage AI Screening + Strategy Pattern Experiments

**Date:** 2026-03-20
**Experiments:** w5_voyage_screening.py, w5b_knn_mmr_patterns.py

## W5a: Voyage AI Embedding Screening

### Hypothesis

Voyage AI's general-purpose embedding models (voyage-4, voyage-4-large) may capture a signal distinct from both MiniLM (semantic similarity) and SPECTER2 (scientific proximity), warranting full corpus embedding and profiling.

### Method

- 100-paper sample: 40 seed/held-out papers from P1 (RL for robotics) and P3 (Quantum computing / quantum ML), plus 60 random papers
- 10 query seeds (5 from P1 subset_5, 5 from P3 subset_5)
- Embedded with 4 models: MiniLM (384d), SPECTER2 (768d), voyage-4 (1024d), voyage-4-large (1024d)
- For each query seed: found top-20 neighbors under each model
- Computed pairwise Jaccard overlap of neighbor lists across all 6 model pairs

### Decision Thresholds

| Jaccard range | Interpretation |
|---------------|----------------|
| > 0.8 with MiniLM | Redundant with MiniLM, do not proceed |
| < 0.6 with BOTH local models | Genuinely different signal, proceed to full corpus |
| Overlaps one heavily, not the other | Better version of that model, not a new signal axis |

### Results

| Model pair | Mean Jaccard | Std | Range |
|------------|-------------|-----|-------|
| voyage-4 vs voyage-4-large | 0.920 | 0.104 | 0.667-1.000 |
| SPECTER2 vs voyage-4 | 0.772 | 0.125 | 0.481-0.905 |
| SPECTER2 vs voyage-4-large | 0.772 | 0.125 | 0.481-0.905 |
| MiniLM vs SPECTER2 (baseline) | 0.732 | 0.115 | 0.538-0.905 |
| miniLM vs voyage-4 | 0.717 | 0.115 | 0.481-0.905 |
| miniLM vs voyage-4-large | 0.705 | 0.126 | 0.429-0.905 |

### Key Observations

1. **voyage-4 and voyage-4-large are near-identical** (Jaccard 0.920). On 6 of 10 seeds, they produced exactly the same top-20 list (Jaccard 1.000). There is no value in testing both.

2. **Both Voyage models overlap SPECTER2 more than MiniLM** (0.772 vs 0.717/0.705). This suggests Voyage captures a signal closer to SPECTER2's scientific proximity axis than to MiniLM's general semantic axis.

3. **Voyage overlaps with both local models at nearly the same level** as MiniLM vs SPECTER2 (0.717-0.772 vs 0.732). This means Voyage embeddings are not a third independent signal axis -- they sit in the overlap zone between the two existing models.

4. **No seed showed Voyage capturing a genuinely different signal.** Even the lowest overlap (seed 2601.18811, Jaccard 0.429-0.481) tracks with MiniLM vs SPECTER2 both being low for that seed (0.538), indicating a generally hard paper for embedding-based retrieval rather than Voyage seeing something unique.

### Verdict: INCONCLUSIVE (methodology insufficient)

> **Epistemic qualification (2026-03-20):** This verdict was originally STOP (PARTIAL_OVERLAP). It has been revised to INCONCLUSIVE after reviewing the methodology against the spike's own epistemic standards. See signal `sig-2026-03-20-jaccard-screening-methodology`.

The original Jaccard-based screening has fundamental limitations that prevent a confident stop/go decision:

1. **Top-K Jaccard is a coarse instrument.** It collapses "different how?" into a single number. Papers at rank #19 vs #21 count as categorical disagreement. All disagreements are treated equally regardless of magnitude. The measure cannot distinguish boundary noise from meaningful divergence.

2. **The sample is too narrow.** Only 2 of 8 interest profiles were tested (P1, P3). Per-seed Jaccard ranged from 0.429 to 0.905 — variance too high for the aggregate to be representative. Profiles where Voyage might add the most value (broad/cross-domain P4, P7; trending P6) were never tested.

3. **The baseline is invalid.** Decision thresholds were calibrated against MiniLM-SPECTER2 overlap (Jaccard 0.732) as the "known different" reference point. The W5.4 qualitative review subsequently found SPECTER2 is qualitatively redundant with MiniLM (45-60% paper overlap, score compression makes ranking noise). The "known different" baseline was not actually different.

4. **No qualitative layer.** The spike's DESIGN.md states "instruments detect, they don't evaluate" and "qualitative review is first-class, not a validation step." Yet this screening used a single quantitative instrument as the sole decision criterion. The ~28% of papers Voyage finds differently from MiniLM were never examined for what *kind* of papers they are.

5. **Contradicted by other findings.** The W3 qualitative review found fusion helps narrow topics despite worse MRR. The W5.4 review found SPECTER2 is redundant despite looking different on Jaccard. Both demonstrate that quantitative overlap measures can mislead in either direction.

**What survives from the original screening:**
- voyage-4 and voyage-4-large are near-identical (Jaccard 0.920) — testing both is unnecessary
- Voyage overlaps SPECTER2 more than MiniLM — it may sit closer to the citation-graph signal axis
- Cost is negligible ($0.04-0.50 for full corpus)

**What is needed for a proper verdict:**
- Qualitative review of Voyage-unique papers (the ~28% MiniLM doesn't find) across a broader profile set
- Rank correlation (Kendall's tau) alongside or instead of top-K Jaccard
- Semantic clustering of divergent papers to determine if divergence is signal or noise
- Testing across all 8 profiles, especially P4 (broad) and P7 (cross-domain)

### Cost of the Screening

- API calls: 14 total (7 batches x 2 models)
- Estimated tokens consumed: ~70K (well within 200M free tier)
- Wall time: ~13 minutes (dominated by 65s rate limit pauses)
- Dimension confirmed: 1024 for both models (as documented)

---

## W5b: kNN-per-Seed and MMR Strategy Patterns

### Hypothesis

The centroid approach may wash out distinctive seeds by averaging embeddings, losing subgroup-specific papers. kNN-per-seed (find neighbors for each seed individually, union results) might recover these. MMR (Maximal Marginal Relevance) might improve diversity without sacrificing too much relevance.

### Method

Tested three retrieval strategies using MiniLM embeddings on the full 19,252-paper corpus:

1. **Centroid top-K** (baseline): Average seed embeddings into centroid, find K=20 nearest neighbors
2. **kNN per seed**: For each seed, find its k nearest neighbors. Union all neighbor sets, ranked by best score to any seed. k_per_seed = max(5, K/n_seeds + 2)
3. **MMR**: Iteratively select papers maximizing lambda * relevance - (1-lambda) * max_diversity. lambda=0.7

Evaluated across all 8 interest profiles, each with 3 seed subsets (5, 10, 15 seeds) = 24 configurations.

Metrics: MRR (held-out paper retrieval), Recall@20, Hit@5, diversity (average pairwise dissimilarity of retrieved set).

### Results

| Strategy | Mean MRR | Mean R@20 | Mean Hit@5 | Mean Diversity |
|----------|----------|-----------|------------|----------------|
| Centroid | 0.354 | 0.308 | 0.417 | 0.456 |
| kNN/seed | 0.149 | 0.167 | 0.125 | 0.572 |
| MMR | 0.344 | 0.250 | 0.458 | 0.486 |

### Inter-Strategy Overlap

| Pair | Mean Jaccard |
|------|-------------|
| Centroid vs kNN | 0.245 |
| Centroid vs MMR | 0.628 |
| kNN vs MMR | 0.220 |

### Key Observations

1. **kNN-per-seed catastrophically degrades retrieval quality.** MRR drops 58% (0.354 to 0.149), recall drops 46% (0.308 to 0.167). The per-seed approach finds papers related to individual seeds but misses the intersection of interest. Many seeds nominate tangentially related papers that are not relevant to the overall interest profile.

2. **kNN-per-seed DOES produce higher diversity** (+25%, 0.572 vs 0.456) but at the cost of coherence. The higher diversity is achieved by returning papers from different semantic neighborhoods, but these neighborhoods are not coherently related to each other.

3. **MMR preserves quality** (MRR 0.344, only -2.8% vs centroid) while modestly improving diversity (+6.6%, 0.486 vs 0.456). However, the diversity improvement is small. Hit@5 actually slightly improves (0.458 vs 0.417).

4. **Centroid vs MMR have 62.8% overlap**, meaning MMR mostly returns the same papers as centroid but in a slightly different order. The diversity gain comes from swapping out a few redundant papers in the bottom of the top-20.

5. **kNN-per-seed produces a nearly orthogonal result set** (Jaccard 0.245 with centroid, 0.220 with MMR). It genuinely finds different papers, but these are mostly worse papers from a retrieval-quality perspective.

6. **Profile P7 (Federated learning + privacy) is an exception.** This is a tight, well-defined cluster where kNN-per-seed performs comparably (MRR 1.000, R@20 0.800 with 5 seeds). For very focused topics where all seeds are in one tight cluster, per-seed retrieval works fine because the union of per-seed neighborhoods converges with the centroid neighborhood.

### Verdict

**Centroid remains the correct default.** MMR is a viable optional mode that could be offered as a "diverse results" toggle, but the improvement is marginal (+6.6% diversity at -2.8% MRR). kNN-per-seed should not be implemented -- it trades relevance for incoherent diversity.

### Implication for Architecture

The centroid approach's robustness validates the current architecture. The "views" approach (MiniLM vs TF-IDF vs SPECTER2) provides far more meaningful diversity than intra-view retrieval tricks like MMR or kNN-per-seed. If a user wants diverse results, they should switch views, not change the retrieval method within a view.
