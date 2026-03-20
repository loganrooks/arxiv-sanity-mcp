# W3 Findings: Combination and Pipeline Profiling

**Completed:** 2026-03-19
**Duration:** 17 minutes (1024s)
**Scope:** 5 RRF pairwise/triple combos, 2 k-sensitivity sweeps, 1 weighted sweep, 5-step marginal value chain, consensus analysis across 8 profiles x 3 seed sets
**Corpus:** 19,252 papers, 8 interest profiles

## Executive Summary

**Every combination tested underperforms MiniLM alone on LOO-MRR and coverage.** The best combination (MiniLM + SPECTER2 RRF k=60) achieves MRR 0.310 vs MiniLM's 0.398 -- a 22% degradation. However, the consensus analysis reveals that MiniLM and TF-IDF produce 70% non-overlapping top-20 lists (Jaccard 0.179), and TF-IDF-exclusive papers account for 9 held-out recoveries that MiniLM misses entirely. The combination framework dilutes MiniLM's focused signal more than it gains from TF-IDF's complementary coverage, but the strategies genuinely access different paper populations.

The implication: simple RRF/weighted fusion is the wrong combination paradigm. The correct architecture is asymmetric -- MiniLM as primary ranker, TF-IDF as a candidate expander that feeds papers into MiniLM's ranking, not a co-equal partner whose rank signal competes with MiniLM.

## W3.1: Pairwise Combination Screening

All combinations tested via RRF (k=60), compared to S1a baseline (MRR 0.398, Coverage 0.686):

| Combo | Components | MRR | dMRR | Coverage | Novelty | Diversity |
|-------|-----------|-----|------|----------|---------|-----------|
| S1a (baseline) | MiniLM | 0.398 | -- | 0.686 | 0.046 | 2.5 |
| C2 | MiniLM + SPECTER2 | 0.310 | -0.088 | 0.550 | 0.029 | 2.3 |
| C4 | MiniLM + TF-IDF + SPECTER2 | 0.305 | -0.093 | 0.535 | 0.042 | 2.4 |
| C1 | MiniLM + TF-IDF | 0.279 | -0.119 | 0.510 | 0.073 | 2.9 |
| C3 | TF-IDF + SPECTER2 | 0.202 | -0.197 | 0.403 | 0.050 | 2.7 |
| C5 | MiniLM + Category | 0.117 | -0.281 | 0.365 | 0.244 | 5.1 |

### Finding 1: RRF combination always degrades the stronger signal

RRF treats all contributing strategies as equal-rank partners. When a strong strategy (MiniLM, MRR 0.398) is combined with a weaker one (TF-IDF, MRR 0.104), the weak strategy's rank signal disrupts the strong one. A paper ranked #3 by MiniLM but #150 by TF-IDF gets pulled down, while a paper ranked #50 by MiniLM but #5 by TF-IDF gets pulled up. The net effect: MiniLM's well-calibrated rankings are corrupted by TF-IDF's poorly-calibrated ones.

This is not a deficiency of RRF specifically. It reflects a fundamental asymmetry: MiniLM and TF-IDF have different discrimination power. RRF cannot account for this asymmetry -- it gives each strategy one "vote."

### Finding 2: Per-profile results reveal one exception

C1 (MiniLM+TF-IDF) beats S1a on exactly one profile:

| Profile | S1a MRR | C1 MRR | Delta |
|---------|---------|--------|-------|
| P1: RL for robotics | 0.468 | 0.178 | -0.290 |
| P2: Language model reasoning | 0.282 | 0.180 | -0.102 |
| P3: Quantum computing | 0.347 | 0.310 | -0.038 |
| P4: AI safety | 0.500 | 0.277 | -0.223 |
| P5: GNNs | 0.464 | 0.307 | -0.157 |
| **P6: Diffusion models** | **0.310** | **0.383** | **+0.073** |
| P7: Federated learning | 0.505 | 0.347 | -0.158 |
| P8: Math foundations | 0.307 | 0.251 | -0.056 |

P6 (diffusion models) is the only profile where combination helps. This aligns with the W1 qualitative finding that TF-IDF excels when topics share distinctive vocabulary with adjacent fields. Diffusion model papers use specialized technical terms (denoising, score matching, Langevin dynamics) that TF-IDF captures as discriminative keywords.

C4 (all three) also beats S1a on P6 (MRR 0.409 vs 0.310) and marginally on P3 (0.351 vs 0.347). These are the profiles with the most distinctive vocabulary.

### Finding 3: Category filter (C5) is destructive as a ranking signal

C5 (MiniLM + Category RRF) collapses to MRR 0.117 -- worse than TF-IDF alone (0.104 by itself). Category filtering produces binary scores (1/0), which when combined via RRF creates a strong bias toward in-category papers regardless of content relevance. Category is useful as a pre-filter (reduce candidate set), not as a ranking signal.

## W3.2: RRF k-Parameter Sensitivity

For the top 2 combos (C2, C4), varied k across {10, 30, 60, 100}:

**C2 (MiniLM + SPECTER2):**

| k | MRR | Coverage |
|---|-----|----------|
| 10 | 0.320 | 0.579 |
| 30 | 0.314 | 0.558 |
| 60 | 0.310 | 0.550 |
| 100 | 0.308 | 0.550 |

MRR range: 0.013 (from 0.308 to 0.320). k=10 is best but the difference is trivial.

**C4 (MiniLM + TF-IDF + SPECTER2):**

| k | MRR | Coverage |
|---|-----|----------|
| 10 | 0.317 | 0.546 |
| 30 | 0.308 | 0.548 |
| 60 | 0.305 | 0.535 |
| 100 | 0.297 | 0.529 |

MRR range: 0.020. Slightly more sensitive than C2, but still minor.

### Finding 4: k does not materially change combination quality

Lower k amplifies top-rank differences (giving more weight to each strategy's top picks). This marginally helps because it preserves more of MiniLM's signal. But the improvement is small (0.01-0.02 MRR) -- nowhere near closing the gap to S1a alone (0.398). The k parameter is not the bottleneck.

## W3.3: Weighted Combination

For C2 (MiniLM + SPECTER2), varied weights:

| Weights (MiniLM/SPECTER2) | MRR | Coverage | Novelty |
|---------------------------|-----|----------|---------|
| 0.2 / 0.8 | 0.241 | 0.418 | 0.042 |
| 0.4 / 0.6 | 0.296 | 0.508 | 0.040 |
| 0.5 / 0.5 | 0.322 | 0.546 | 0.042 |
| 0.6 / 0.4 | 0.354 | 0.585 | 0.033 |
| 0.8 / 0.2 | 0.380 | 0.665 | 0.040 |
| **S1a alone** | **0.398** | **0.686** | **0.046** |

### Finding 5: Weighted combination approaches but never reaches MiniLM alone

At 0.8/0.2 weighting (SPECTER2 contributes 20%), MRR reaches 0.380 -- within 0.018 of S1a alone. But this "nearly as good as doing nothing" result highlights that the optimal combination is somewhere around 95%+ MiniLM, making SPECTER2's contribution negligible.

The monotonic improvement as MiniLM weight increases (from 0.241 at 0.2 to 0.380 at 0.8) confirms that SPECTER2 provides negative marginal value when score-combined. The one possible exception: using SPECTER2 for candidate generation (not scoring) in a pipeline architecture.

## W3.5: Marginal Signal Value

Starting from MiniLM alone, incrementally adding signals via RRF:

| Step | Components | MRR | Delta | Coverage | Novelty | Diversity |
|------|-----------|-----|-------|----------|---------|-----------|
| 0 | MiniLM | 0.398 | -- | 0.686 | 0.046 | 2.5 |
| 1 | + TF-IDF | 0.279 | -0.119 | 0.510 | 0.073 | 2.9 |
| 2 | + SPECTER2 | 0.305 | +0.026 | 0.535 | 0.042 | 2.4 |
| 3 | + Category | 0.235 | -0.070 | 0.516 | 0.042 | 2.5 |
| 4 | + Co-author | 0.203 | -0.032 | 0.506 | 0.052 | 2.8 |

### Finding 6: Every signal addition degrades the baseline

There is no diminishing returns point because returns are negative from step 1. Adding TF-IDF drops MRR by 0.119 (30% degradation). Adding SPECTER2 to the TF-IDF combo recovers 0.026 -- but this is recovering from the TF-IDF damage, not improving over baseline. Category and co-author each make things worse.

The fact that SPECTER2 partially recovers from TF-IDF's damage is notable: it suggests SPECTER2's signal is somewhat aligned with MiniLM's, acting as a "corrective" that pulls rankings back toward MiniLM-like ordering. This is consistent with SPECTER2 and MiniLM both being dense embedding strategies, while TF-IDF's sparse signal is the disruptive one.

## W3.6: Consensus Validation

Overlap between MiniLM and TF-IDF top-20 lists:

| Metric | Value |
|--------|-------|
| Mean papers in both top-20 | 5.9 / 20 |
| Mean Jaccard similarity | 0.179 |
| Min consensus (per evaluation) | 0 |
| Max consensus (per evaluation) | 14 |

Per-profile overlap:

| Profile | Consensus | Jaccard | TF-IDF-only in cluster | TF-IDF-only held-out |
|---------|-----------|---------|----------------------|---------------------|
| P5: GNNs | 10.3 | 0.349 | 2 | 2 |
| P3: Quantum | 7.3 | 0.226 | 1 | 3 |
| P4: AI safety | 6.7 | 0.200 | 0 | 0 |
| P1: RL robotics | 5.7 | 0.172 | 2 | 0 |
| P7: Federated | 5.3 | 0.154 | 1 | 1 |
| P2: Language | 4.3 | 0.122 | 1 | 0 |
| P6: Diffusion | 4.0 | 0.112 | 1 | 0 |
| P8: Math found. | 3.7 | 0.101 | 2 | 3 |

**Total across all evaluations:**
- TF-IDF-exclusive papers in clusters: 10
- TF-IDF-exclusive held-out paper recoveries: 9

### Finding 7: MiniLM and TF-IDF access genuinely different paper populations

With only 5.9/20 papers in common (Jaccard 0.179), these strategies produce 70% non-overlapping recommendation lists. This is not noise -- TF-IDF finds 10 cluster-relevant papers and 9 held-out papers that MiniLM misses entirely.

The held-out recovery finding is particularly important: 9 papers that were deliberately reserved as "ground truth relevant" appear in TF-IDF's top-20 but not MiniLM's. These are papers where keyword patterns provide better retrieval than semantic embeddings -- likely papers with distinctive technical vocabulary that MiniLM's general-purpose embedding space does not capture well.

### Finding 8: Overlap varies strongly by profile

P5 (GNNs) has 10.3/20 consensus (high overlap) -- both strategies agree on GNN papers. P8 (Math foundations) has only 3.7/20 consensus (low overlap) -- mathematical terminology creates a large gap between keyword and semantic retrieval. P8 also has 3 TF-IDF-only held-out recoveries, the most of any profile, suggesting mathematical papers benefit most from keyword-based retrieval.

## Synthesis: Why Combination Fails, What To Do Instead

### The failure mode

RRF and weighted fusion assume contributing strategies are approximately equal in quality and that their differences are complementary. Neither assumption holds:

1. **Quality asymmetry:** MiniLM MRR 0.398 vs TF-IDF 0.104 is a 4:1 ratio. Giving TF-IDF equal voting power (RRF) or even 20% weight corrupts MiniLM's rankings.

2. **Signal interference:** TF-IDF's top picks are genuinely different from MiniLM's (70% non-overlap), but this means TF-IDF actively promotes papers that MiniLM ranked low, pulling them up at the expense of MiniLM's top picks.

### The right architecture

The consensus analysis shows TF-IDF finds papers MiniLM misses. The marginal value analysis shows adding TF-IDF's ranking signal hurts. The resolution:

**TF-IDF should expand the candidate pool, not compete in ranking.**

Pipeline architecture:
1. TF-IDF retrieves top-N candidates (N >> 20)
2. MiniLM retrieves top-N candidates
3. Take the union of both candidate sets
4. Re-rank the union using MiniLM scores alone
5. Return top-20

This preserves MiniLM's ranking quality while gaining TF-IDF's coverage breadth. The 9 held-out papers TF-IDF finds but MiniLM misses would enter the candidate pool and then be ranked by MiniLM -- if MiniLM scores them reasonably (even if not in its own top-20), they would surface.

This architecture was NOT tested in W3 (it requires a different experimental design). It is the natural next step if combination value is to be captured.

### Practical implication for the product

For a Phase 1 MCP server:
- **Default strategy: MiniLM centroid** -- no combination needed
- **Optional: TF-IDF as diversity mode** -- expose as a separate tool or parameter, not blended
- **Do not ship RRF combination** as a default -- it degrades quality
- **Future: pipeline architecture** if held-out recovery is valued

## Data Files

- Full results: `experiments/data/w3_combination_profiles.json`
- Script: `experiments/w3_combinations.py`
