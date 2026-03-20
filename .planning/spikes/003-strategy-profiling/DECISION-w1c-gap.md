# W1C-gap Decision: OpenAlex Enrichment Expansion + Bibliographic Coupling Re-Profile

**Completed:** 2026-03-20
**Question:** Does bibliographic coupling (S3a) become a viable recommendation strategy when given adequate reference data, and does related_works (S3c) become functional?
**Answer:** S3a shows valid algorithmic discrimination (78% of topic groups positive) but remains far below embedding-based strategies on harness metrics. S3c becomes technically functional but shows zero signal on the harness. Neither strategy is competitive as a standalone; both are potential supplementary signals in combinations.

## Summary

W1C found S3a (bibliographic coupling) had a valid algorithm (0.467 mean discrimination in focused evaluation) but was severely data-limited: only 1/120 seed papers and 95/19,252 corpus papers had referenced_works from OpenAlex. S3c (related_works) was entirely non-functional with zero papers having that field populated.

This experiment expanded OpenAlex enrichment from 500 to 1,444 papers by querying the API for 120 seed papers and their top-100 MiniLM neighbors (4,718 target papers). The free-tier daily API budget allowed 944 successful lookups before rate limiting (HTTP 429). The expanded data yielded 307 papers with referenced_works (was 95) and 467 with related_works (was 0). Seed coverage improved from 1/120 to 11/120 with refs and 20/120 with related_works.

Re-profiling reveals that even with 3.2x more reference data, S3a's harness performance is marginal: LOO MRR 0.019 (vs 0.398 for MiniLM, 0.184 for SPECTER2), seed proximity 0.355 (vs 0.764), coverage 0.021 (vs 0.686). The focused evaluation shows the algorithm CAN discriminate topically related papers (78% of 27 groups show positive intra > inter-group coupling) but the discrimination magnitude drops from 0.467 (5 groups) to 0.081 (27 groups) with more data -- the original small-sample result was inflated. S3c, while now technically functional, produces LOO MRR of 0.000 and coverage of 0.000 -- it cannot find any cluster papers.

## Findings

### Experiment 1: OpenAlex Enrichment Expansion

**Result:** Partial enrichment achieved; daily API budget exhausted at 20.5% of target.

**Data:**

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Cache entries | 500 | 1,444 | +944 |
| Papers with referenced_works | 95 | 307 | +212 |
| Papers with related_works | 0 | 467 | +467 |
| Seeds with refs | 1/120 | 11/120 | +10 |
| Seeds with related_works | 0/120 | 20/120 | +20 |
| API calls made | - | 944 | - |
| API calls rate-limited (429) | - | 3,607 | - |

OpenAlex free tier budget: ~$0.10/day, ~$0.0001/request, ~1,000 requests/day. Full enrichment of the 4,603-paper target would take 4-5 days of sequential daily runs.

**Publication year vs referenced_works availability:**

| Year | Papers | With refs | Rate |
|------|--------|-----------|------|
| Pre-2020 | ~30 | ~28 | 93% |
| 2020-2021 | ~20 | ~18 | 90% |
| 2022-2023 | ~104 | ~25 | 24% |
| 2024 | 260 | 30 | 12% |
| 2025 | 641 | 131 | 20% |
| 2026 | 332 | 62 | 19% |

The reference availability rate for recent papers (2022+) is ~19%, regardless of corpus age. This is a structural limitation of OpenAlex's indexing pipeline for very new papers, not a data collection issue we can fix by enriching more papers.

### Experiment 2: S3a Re-Profile with Expanded Data

**Result:** S3a improved from non-functional to marginal, but remains far below embedding strategies.

**Harness results (cross-strategy comparison):**

| Strategy | LOO MRR | Seed Prox | Coherence | Coverage |
|----------|---------|-----------|-----------|----------|
| S1a MiniLM centroid | 0.398 | 0.764 | 0.643 | 0.686 |
| S1c SPECTER2 adapter | 0.184 | 0.736 | 0.616 | 0.336 |
| S1d TF-IDF | 0.104 | 0.698 | 0.564 | 0.247 |
| S6d Same category | 0.004 | 0.454 | - | 0.033 |
| **S3a expanded** | **0.019** | **0.355** | **0.254** | **0.021** |
| S3a W1C data-limited | 0.000 | 0.312 | - | - |
| S3c expanded | 0.000 | 0.312 | 0.238 | 0.000 |
| S6a Random | 0.000 | 0.282 | 0.178 | 0.000 |

S3a expanded is marginally above random baseline on proximity (+0.073) and coherence (+0.076), but close to zero on LOO MRR and coverage. It ranks below same-category filtering (S6d).

**Focused evaluation (algorithm validity test):**

| Metric | W1C (95 papers, 5 groups) | Expanded (307 papers, 27 groups) |
|--------|---------------------------|----------------------------------|
| Mean intra-group Jaccard | high | 0.0814 |
| Mean inter-group Jaccard | low | 0.0004 |
| Mean discrimination | 0.467 | 0.081 |
| Positive discrimination | 80% | 78% |

The algorithm validly discriminates (78% positive discrimination), but the effect size dropped 5.8x with more data. The W1C result (0.467) was inflated by small-sample effects (5 groups, small N). With 27 groups and more diverse topics, discrimination is 0.081 -- still positive, but the Jaccard overlaps between related papers are themselves very small (mean intra-group 0.081).

Top discriminating groups confirm the algorithm works best for tightly-defined fields:
- Complex Systems (3 papers): disc = 1.000
- Computational Physics (3 papers): disc = 0.999
- Quantum Computing (15 papers): disc = 0.004

The smaller the field, the higher the overlap. Broad fields show near-zero discrimination.

### Experiment 3: S3c (related_works) First Profile

**Result:** S3c becomes technically functional (467 papers have related_works) but produces zero signal on the harness.

LOO MRR: 0.000, coverage: 0.000. The related_works field exists but does not point to papers in our corpus -- the OpenAlex-to-arxiv ID mapping (1,397 entries) does not overlap with the OpenAlex work IDs in the related_works lists.

### Experiment 4: Query Latency

**S3a latency:** p50 = 7.3ms, p95 = 11.3ms. Very fast because it's a simple set intersection + Jaccard computation, no matrix operations needed.

## Analysis

| Option | Pros | Cons | Spike Evidence |
|--------|------|------|----------------|
| Include S3a as standalone strategy | Fast (7ms), algorithm is valid | LOO MRR 0.019, coverage 0.021 -- far below alternatives | Ranking: dead last among non-random strategies |
| Include S3a as combination signal | Adds orthogonal signal (citation graph vs content), low compute cost | Marginal lift expected given low coverage; 19% ref rate caps potential | Algorithm discriminates but magnitude is small |
| Include S3c | Leverages OpenAlex graph | Zero signal on harness -- related_works don't map to corpus | Non-functional in practice |
| Defer graph strategies until full enrichment | More data might improve coverage | Structural 19% ref rate limits upside; 4-5 more API days needed | Even with 3x data, S3a is 20x worse than MiniLM |
| Drop graph strategies entirely | Simplifies system, no API dependency | Loses potential future value as corpus matures | Current evidence shows no competitive signal |

## Decision

**Chosen approach:** Classify S3a as a supplementary signal for future combination testing, not a standalone strategy. Drop S3c. Do not invest further in OpenAlex enrichment expansion for this spike.

**Rationale:**

1. S3a's algorithm is valid (78% positive discrimination) but its harness performance (LOO MRR 0.019) is 21x worse than MiniLM (0.398). Even with perfect reference coverage, the structural ~19% ref rate for recent papers means S3a can never score 81% of the corpus.

2. S3c is non-functional -- the related_works field does not contain IDs that map back to papers in our corpus.

3. The focused evaluation shows discrimination magnitude is small (0.081 mean) and drops with more data, suggesting the W1C result (0.467) was inflated by small-sample bias.

4. The enrichment infrastructure works and the API budget issue is solvable (polite pool email or multi-day runs), but additional enrichment won't change the strategic conclusion: bibliographic coupling is not competitive as a standalone strategy for recent arXiv papers.

5. S3a may have value as a weak supplementary signal in combinations (its signal is orthogonal to content similarity), but this is speculative and not supported by current data.

**Confidence:** HIGH

The conclusion is robust because:
- We tested with 3.2x more data than W1C (307 vs 95 papers with refs)
- The harness comparison uses the same evaluation protocol as all other strategies
- The structural 19% ref rate for recent papers is a hard limit on coverage
- Even the focused evaluation (which controls for data availability) shows small effect sizes

## Implications

- S3a should be retained in the strategy catalog as "data-limited, supplementary signal" -- not promoted to any tier that implies standalone viability
- S3c should be marked as non-functional and not included in any configuration
- The OpenAlex enrichment pipeline works and can be reused if future decisions require citation data for other purposes (e.g., FWCI-based ranking S2d uses the same cache)
- No further API enrichment days are needed for this spike's purposes
- The combination profiling (W3) should test S3a as a supplement to embedding strategies, but expectations should be low given its marginal individual signal

## Metadata

**Spike duration:** ~24 minutes (enrichment API: ~23.9 min, profiling: ~0.2 min)
**Iterations:** 1
**Originating phase:** Spike 003, W1C gap fill
**API calls:** 944 successful + 3,607 rate-limited (HTTP 429)
**Data artifacts:** expanded_openalex_cache.json (4,603 entries), w1c_gap_s3a_profiles.json
