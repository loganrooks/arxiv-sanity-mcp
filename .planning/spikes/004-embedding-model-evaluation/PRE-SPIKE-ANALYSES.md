# Pre-Spike Analyses

**Generated:** 2026-03-30T13:24:14.631705+00:00

## Scope

These analyses run exhaustively over all 3,003 five-of-fifteen seed subsets for each of the 8 profiles from Spike 003/004.
Intervals below are empirical 95% subset ranges (`q025`-`q975`), not inferential confidence intervals.

## Analysis 1: Pairwise Embedding Comparison Matrix

Mean Kendall's tau across all profiles and all 3,003 seed subsets:

| System | MiniLM | SPECTER2 | Stella | Qwen3 | GTE | Voyage-4 |
| --- | --- | --- | --- | --- | --- | --- |
| MiniLM | 1.000 | 0.558 | 0.635 | 0.584 | 0.630 | 0.479 |
| SPECTER2 | 0.558 | 1.000 | 0.596 | 0.533 | 0.567 | 0.444 |
| Stella | 0.635 | 0.596 | 1.000 | 0.681 | 0.631 | 0.525 |
| Qwen3 | 0.584 | 0.533 | 0.681 | 1.000 | 0.593 | 0.500 |
| GTE | 0.630 | 0.567 | 0.631 | 0.593 | 1.000 | 0.479 |
| Voyage-4 | 0.479 | 0.444 | 0.525 | 0.500 | 0.479 | 1.000 |

Mean Jaccard@20 across all profiles and all 3,003 seed subsets:

| System | MiniLM | SPECTER2 | Stella | Qwen3 | GTE | Voyage-4 |
| --- | --- | --- | --- | --- | --- | --- |
| MiniLM | 1.000 | 0.570 | 0.570 | 0.576 | 0.610 | 0.581 |
| SPECTER2 | 0.570 | 1.000 | 0.551 | 0.550 | 0.543 | 0.540 |
| Stella | 0.570 | 0.551 | 1.000 | 0.675 | 0.626 | 0.603 |
| Qwen3 | 0.576 | 0.550 | 0.675 | 1.000 | 0.620 | 0.611 |
| GTE | 0.610 | 0.543 | 0.626 | 0.620 | 1.000 | 0.595 |
| Voyage-4 | 0.581 | 0.540 | 0.603 | 0.611 | 0.595 | 1.000 |

Most and least similar pairs:

| Kind | Pair | Mean tau | Mean J@20 |
| --- | --- | --- | --- |
| Least similar | SPECTER2 vs Voyage-4 | 0.444 | 0.540 |
| Most similar | Stella vs Qwen3 | 0.681 | 0.675 |

## Analysis 2: Seed Sensitivity Characterization

Aggregate distributions versus MiniLM across all profiles and all 3,003 seed subsets per profile:

| System | tau vs MiniLM | J@20 vs MiniLM | J@100 vs MiniLM | Category recall | LOO-MRR | Additional papers vs MiniLM @20 |
| --- | --- | --- | --- | --- | --- | --- |
| SPECTER2 | 0.558 [0.364, 0.690] | 0.570 [0.333, 0.818] | 0.494 [0.333, 0.667] | 0.861 [0.550, 1.000] | 0.050 [0.011, 0.157] | 5.616 [2.000, 10.000] |
| Stella | 0.635 [0.536, 0.724] | 0.570 [0.333, 0.818] | 0.537 [0.389, 0.653] | 0.847 [0.550, 1.000] | 0.045 [0.010, 0.098] | 5.623 [2.000, 10.000] |
| Qwen3 | 0.584 [0.446, 0.678] | 0.576 [0.333, 0.818] | 0.508 [0.389, 0.667] | 0.846 [0.550, 1.000] | 0.046 [0.000, 0.134] | 5.540 [2.000, 10.000] |
| GTE | 0.630 [0.474, 0.725] | 0.610 [0.333, 0.818] | 0.522 [0.408, 0.667] | 0.835 [0.550, 1.000] | 0.047 [0.000, 0.104] | 4.987 [2.000, 10.000] |
| Voyage-4 | 0.479 [0.387, 0.550] | 0.581 [0.379, 0.739] | 0.491 [0.389, 0.600] | 0.848 [0.600, 1.000] | 0.050 [0.000, 0.128] | 5.386 [3.000, 9.000] |
| TF-IDF | 0.463 [0.334, 0.565] | 0.510 [0.290, 0.739] | 0.437 [0.316, 0.587] | 0.793 [0.500, 1.000] | 0.044 [0.012, 0.082] | 6.665 [3.000, 11.000] |

## Analysis 3: Coverage-Only Second-View Check

Question: does `MiniLM + SPECTER2` cover more ground than `MiniLM + TF-IDF`? Here, "cover more ground" means union size of the two top-K lists, not quality.

K=20 union comparison by profile:

| Profile | MiniLM + SPECTER2 | MiniLM + TF-IDF | Delta (S2 - TF) | P(S2 > TF) |
| --- | --- | --- | --- | --- |
| P1 | 23.730 [22.000, 26.000] | 25.678 [23.000, 28.000] | -1.948 [-5.000, 1.000] | 0.044 |
| P2 | 26.692 [24.000, 29.000] | 27.629 [25.000, 30.000] | -0.936 [-4.000, 2.000] | 0.172 |
| P3 | 26.565 [24.000, 29.000] | 26.043 [24.000, 28.000] | 0.522 [-3.000, 4.000] | 0.504 |
| P4 | 23.806 [22.000, 26.000] | 24.434 [22.000, 27.000] | -0.627 [-4.000, 2.000] | 0.219 |
| P5 | 24.955 [23.000, 28.000] | 25.284 [23.000, 28.000] | -0.328 [-4.000, 3.000] | 0.296 |
| P6 | 25.907 [24.000, 28.000] | 28.930 [26.000, 31.000] | -3.023 [-6.000, 0.000] | 0.017 |
| P7 | 25.356 [23.000, 28.000] | 25.713 [23.000, 28.000] | -0.357 [-3.000, 3.000] | 0.285 |
| P8 | 27.913 [24.000, 32.000] | 29.613 [26.000, 33.000] | -1.700 [-5.000, 2.000] | 0.105 |

Overall union-size summaries:

| K | MiniLM + SPECTER2 | MiniLM + TF-IDF | Delta (S2 - TF) | P(S2 > TF) |
| --- | --- | --- | --- | --- |
| 20 | 25.616 [22.000, 30.000] | 26.665 [23.000, 31.000] | -1.050 [-5.000, 3.000] | 0.205 |
| 50 | 64.277 [57.000, 73.000] | 66.182 [59.000, 77.000] | -1.905 [-10.000, 6.000] | 0.264 |
| 100 | 134.293 [120.000, 150.000] | 139.527 [126.000, 152.000] | -5.234 [-17.000, 9.000] | 0.238 |

## Guardrails

- These analyses answer coverage and stability questions only. They do not establish researcher value.
- The pairwise matrix compares embedding-model outputs only. TF-IDF remains in the second-view decision frame via Analysis 3.
- All profile semantics remain MiniLM-entangled because the profiles themselves are MiniLM-derived.
