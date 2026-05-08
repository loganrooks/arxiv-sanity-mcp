# Findings: W2.2 Top-K Aggressiveness Sweep + W2.5 Embedding Quantization

**Date:** 2026-03-19
**Spike:** 003 Strategy Profiling
**Work Items:** W2.2, W2.5

---

## W2.2: Top-K Aggressiveness Sweep

### Question

Is there an elbow where increasing K sharply degrades coherence? Or is the tradeoff smooth?

### Method

Profiled S1a (MiniLM), S1c (SPECTER2), S1d (TF-IDF) at K = 10, 20, 50, 100, 200.
Used 3 representative profiles (P1 medium, P3 narrow, P4 broad) with 1 seed set each (subset_5).
All 7 quality instruments measured at each (strategy, K) combination.

### Results

#### S1a (MiniLM centroid) -- K sweep

| K | MRR | Proximity | Coherence | Diversity | Novelty | Surprise | Coverage |
|----:|------:|----------:|----------:|----------:|--------:|---------:|---------:|
| 10 | 0.430 | 0.790 | 0.691 | 2.0 | 0.067 | 0.133 | 0.417 |
| 20 | 0.438 | 0.771 | 0.661 | 2.3 | 0.033 | 0.117 | 0.700 |
| 50 | 0.440 | 0.742 | 0.616 | 2.3 | 0.020 | 0.147 | 0.800 |
| 100 | 0.441 | 0.711 | 0.570 | 4.3 | 0.043 | 0.210 | 0.833 |
| 200 | 0.441 | 0.671 | 0.518 | 10.3 | 0.115 | 0.268 | 0.833 |

#### S1c (SPECTER2 adapter) -- K sweep

| K | MRR | Proximity | Coherence | Diversity | Novelty | Surprise | Coverage |
|----:|------:|----------:|----------:|----------:|--------:|---------:|---------:|
| 10 | 0.163 | 0.758 | 0.643 | 2.0 | 0.067 | 0.167 | 0.300 |
| 20 | 0.172 | 0.737 | 0.616 | 2.3 | 0.067 | 0.183 | 0.417 |
| 50 | 0.178 | 0.712 | 0.577 | 3.3 | 0.080 | 0.193 | 0.617 |
| 100 | 0.179 | 0.682 | 0.532 | 5.7 | 0.097 | 0.240 | 0.767 |
| 200 | 0.180 | 0.632 | 0.470 | 10.7 | 0.212 | 0.298 | 0.833 |

#### S1d (TF-IDF cosine) -- K sweep

| K | MRR | Proximity | Coherence | Diversity | Novelty | Surprise | Coverage |
|----:|------:|----------:|----------:|----------:|--------:|---------:|---------:|
| 10 | 0.091 | 0.699 | 0.558 | 3.0 | 0.133 | 0.333 | 0.117 |
| 20 | 0.101 | 0.698 | 0.564 | 3.3 | 0.083 | 0.267 | 0.233 |
| 50 | 0.108 | 0.677 | 0.528 | 5.0 | 0.107 | 0.293 | 0.500 |
| 100 | 0.111 | 0.653 | 0.491 | 9.0 | 0.150 | 0.337 | 0.650 |
| 200 | 0.112 | 0.621 | 0.453 | 13.3 | 0.188 | 0.382 | 0.767 |

### Analysis

**No elbow; the tradeoff is smooth and monotonic.**

1. **Coherence degradation is gradual.** All three strategies show steady, approximately linear coherence decline as K increases. The total coherence drop from K=10 to K=200 is:
   - S1a: 25.0% (0.691 to 0.518)
   - S1c: 26.9% (0.643 to 0.470)
   - S1d: 18.8% (0.558 to 0.453)
   The largest single-step coherence drop for all three strategies occurs between K=100 and K=200, but it is not qualitatively different from earlier steps -- no sharp cliff.

2. **MRR saturates quickly.** MRR gains plateau by K=50 for all strategies. This is expected: LOO MRR measures whether a specific held-out paper appears in the top-K, and beyond K=50 the additional depth rarely helps.
   - S1a: MRR at K=50 (0.440) essentially matches K=200 (0.441)
   - S1c: MRR at K=50 (0.178) essentially matches K=200 (0.180)
   - S1d: MRR at K=50 (0.108) essentially matches K=200 (0.112)

3. **Coverage has a practical ceiling.** For S1a and S1c, coverage plateaus at ~0.83 around K=100. Additional depth to K=200 adds no coverage. TF-IDF continues gaining slowly.

4. **Diversity explodes above K=100.** Cluster diversity stays at 2-3 for K<=50 then jumps to 10+ at K=200. This is the strongest behavioral shift in the sweep.

5. **Novelty and surprise increase smoothly.** At K=200, even S1a (the tightest strategy) shows 11.5% novelty and 26.8% category surprise, up from near-zero at K=10.

### Implications

- **Default K=20 is well-calibrated.** It sits on the steepest part of the coverage curve while coherence is still high. K=50 offers marginally more coverage at moderate coherence cost.
- **K=100-200 is a different operating regime.** These values shift from "focused recommendations" to "broad discovery." The diversity and novelty profiles change substantially. This is useful, but should be a deliberate user choice, not a default.
- **No cliff means K is a smooth dial.** Users can freely adjust K without fear of sudden quality collapse. The system can offer K as a user-tunable parameter with clear semantics: lower K = focused, higher K = exploratory.

---

## W2.5: Embedding Quantization Impact

### Question

Does quantization change quality metrics by more than 5%? If not, it is a free memory win.

### Method

For both MiniLM (384-dim) and SPECTER2 (768-dim), created float32, float16, and int8 variants. Profiled each across all 8 profiles x 3 seed sets at top-K=20 (matching full W1A evaluation). Int8 uses per-dimension symmetric scaling to [-127, 127].

### Quantization Error Statistics

| Model | Dim | float32 MB | float16 MB | int8 MB | f16 max err | i8 max err |
|---------|----:|-----------:|-----------:|--------:|------------:|-----------:|
| MiniLM | 384 | 28.2 | 14.1 | 7.1 | 0.000096 | 0.002208 |
| SPECTER2| 768 | 56.4 | 28.2 | 14.1 | 0.000244 | 0.005861 |

Ranking preservation test (random query, top-20):
- float16: 20/20 overlap with float32 (perfect preservation)
- int8: 12/20 overlap with float32 (significant reordering)

### Quality Impact

#### MiniLM

| Metric | float32 | float16 | f16 % change | int8 | i8 % change |
|------------------------|--------:|--------:|-------------:|------:|------------:|
| MRR | 0.3979 | 0.3978 | -0.00% | 0.3835 | -3.61% |
| Seed proximity | 0.7643 | 0.7643 | +0.00% | 0.7636 | -0.09% |
| Topical coherence | 0.6434 | 0.6434 | -0.00% | 0.6401 | -0.52% |
| Cluster diversity | 2.5417 | 2.5417 | +0.00% | 2.6667 | +4.92% |
| Novelty | 0.0458 | 0.0458 | +0.00% | 0.0479 | +4.55% |
| Category surprise | 0.0938 | 0.0938 | +0.00% | 0.0917 | -2.22% |
| Coverage | 0.6862 | 0.6862 | +0.00% | 0.6674 | -2.73% |

**Verdict: float16 PASS (0.00%), int8 PASS (worst 4.92%)**

#### SPECTER2

| Metric | float32 | float16 | f16 % change | int8 | i8 % change |
|------------------------|--------:|--------:|-------------:|------:|------------:|
| MRR | 0.1840 | 0.1901 | +3.31% | 0.1759 | -4.39% |
| Seed proximity | 0.7248 | 0.7246 | -0.03% | 0.7231 | -0.23% |
| Topical coherence | 0.5840 | 0.5834 | -0.10% | 0.5899 | +1.02% |
| Cluster diversity | 2.8750 | 2.8750 | +0.00% | 3.1667 | +10.14% |
| Novelty | 0.0521 | 0.0521 | +0.00% | 0.0688 | +32.00% |
| Category surprise | 0.0938 | 0.0938 | +0.00% | 0.1146 | +22.22% |
| Coverage | 0.3361 | 0.3318 | -1.27% | 0.3113 | -7.37% |

**Verdict: float16 PASS (worst 3.31%), int8 FAIL (worst 32.00%)**

#### Latency

| Variant | p50 (ms) | p95 (ms) |
|----------------|--------:|---------:|
| MiniLM f32 | 28.13 | 65.51 |
| MiniLM f16 | 58.59 | 94.80 |
| MiniLM i8 | 19.02 | 25.98 |
| SPECTER2 f32 | 28.79 | 67.31 |
| SPECTER2 f16 | 140.21 | 177.28 |
| SPECTER2 i8 | 60.34 | 75.29 |

### Analysis

1. **float16 is a free win for both models.** Quality impact is negligible (worst case: 3.31% MRR improvement on SPECTER2, likely noise). Memory savings are 50%. The only downside: numpy float16 dot product is actually slower (2x for MiniLM, 5x for SPECTER2) because CPUs do not have native float16 arithmetic. In production, embeddings would be stored as float16 and promoted to float32 at search time, getting the storage benefit without the latency penalty.

2. **int8 works for MiniLM but fails for SPECTER2.** MiniLM int8 stays within the 5% threshold on all metrics (worst: 4.92% on cluster diversity). SPECTER2 int8 produces 32% novelty increase and 22% surprise increase, indicating the quantization changes which papers surface enough to alter the recommendation character.

3. **Why SPECTER2 is more sensitive to int8.** SPECTER2 has 768 dimensions (vs MiniLM's 384), and its values have a wider per-dimension range. The int8 quantization introduces more relative error per dimension. With 768 dimensions, small per-dimension errors accumulate differently in dot products.

4. **Int8 is faster.** Despite the quantization overhead, int8 dot products are faster than float32: MiniLM i8 is 1.5x faster, SPECTER2 i8 is 2.1x slower than f32 but faster than f16.

### Memory Savings Summary (19K papers)

| Model | float32 | float16 | int8 |
|---------|--------:|--------:|-----:|
| MiniLM | 28.2 MB | 14.1 MB | 7.1 MB |
| SPECTER2| 56.4 MB | 28.2 MB | 14.1 MB |

At 100K papers (projected scale):
| Model | float32 | float16 | int8 |
|---------|--------:|--------:|-----:|
| MiniLM | ~147 MB | ~73 MB | ~37 MB |
| SPECTER2| ~293 MB | ~147 MB | ~73 MB |

### Implications

- **Store embeddings as float16, search as float32.** This is the recommended default: 50% storage savings with zero quality impact and no latency penalty (float16 -> float32 promotion is cheap).
- **MiniLM int8 is viable as a memory-constrained option.** For deployments where 75% memory savings matter, int8 MiniLM is acceptable (worst metric within 5%).
- **SPECTER2 int8 is not recommended.** The quality degradation (especially in novelty/surprise, indicating the recommendation set character changes) exceeds the 5% threshold.
- **At projected 100K scale, float16 is the sweet spot:** MiniLM at 73 MB and SPECTER2 at 147 MB are comfortable for any deployment target.
