# W4 Findings: Context Sensitivity

**Completed:** 2026-03-20
**Strategies tested:** S1a (MiniLM centroid), S1d (TF-IDF centroid)
**Total runtime:** 170.9s (2.8 min)

## Summary

Context sensitivity testing reveals that MiniLM (S1a) is remarkably robust across user contexts -- seed count, interest breadth, and corpus scale have minimal impact on its core quality. TF-IDF (S1d) degrades meaningfully at scale and with fewer seeds, confirming it is the more context-sensitive strategy. Negative signals **hurt** MiniLM and are **neutral** for TF-IDF, recommending against implementing negative demotion in v1.

These findings produce three actionable installer recommendations:
1. No minimum seed count gate needed for MiniLM (works with 1 seed)
2. TF-IDF benefits from 5+ seeds and smaller corpora
3. Skip negative signals entirely in v1

---

## W4.1: Cold-Start Curve (Seed Count Sensitivity)

**Question:** At what seed count does quality stabilize? Is there a minimum viable seed count?

### S1a (MiniLM) Results

| Seeds | MRR    | Prox   | Coverage | Coherence | Diversity | Novelty | Surprise |
|-------|--------|--------|----------|-----------|-----------|---------|----------|
| 1     | 0.3979 | 0.6751 | 0.3658   | 0.6029    | 3.5       | 0.2812  | 0.4563   |
| 3     | 0.3979 | 0.7265 | 0.5674   | 0.6306    | 2.5       | 0.1500  | 0.1938   |
| 5     | 0.3979 | 0.7527 | 0.6859   | 0.6437    | 2.6       | 0.1000  | 0.1063   |
| 10    | 0.3979 | 0.7674 | 0.6865   | 0.6448    | 2.8       | 0.0250  | 0.1063   |
| 15    | 0.3979 | 0.7728 | 0.6862   | 0.6418    | 2.2       | 0.0125  | 0.0688   |

**Key finding: MRR is INVARIANT to seed count.** The LOO evaluation uses the profile's cluster papers as seeds (not the user's seed set), so MRR is identical across all seed counts. This is a property of the instrument, not the strategy -- LOO tests recoverability of a coherent paper set, not seed-set sensitivity.

**What does change with seed count:**
- **Proximity** climbs from 0.675 (1 seed) to 0.773 (15 seeds) -- +14.5% absolute. The centroid becomes more representative of the user's actual interest as more seeds are added. The curve plateaus around 5 seeds (0.753), with diminishing returns from 5 to 15 (+2.7%).
- **Coverage** jumps from 0.366 (1 seed) to 0.686 (5 seeds) -- nearly doubling. It then flat-lines from 5 to 15 seeds. This is the most sensitive instrument: with 1 seed, the strategy covers only 37% of ground-truth papers; with 5+, it covers 69%.
- **Novelty and Surprise** drop sharply from 1 to 5 seeds (novelty: 0.281 -> 0.100; surprise: 0.456 -> 0.106), then continue declining. More seeds = tighter centroid = less exploration. This is expected behavior, not degradation.
- **Coherence** rises moderately (0.603 -> 0.644), stabilizing by 3 seeds.

**Interpretation:** MiniLM works acceptably with even 1 seed, but the centroid is poorly calibrated (low coverage, high surprise). At 3 seeds, the centroid is reasonable. At 5 seeds, coverage saturates and performance is near-peak. More than 5 seeds offers marginal improvement in proximity but actually reduces novelty/diversity -- potentially a "comfort zone" effect.

**Recommendation for installer:** Suggest 5 seeds as the default, 3 as minimum for good results, note that 1 is functional but noisy.

### S1d (TF-IDF) Results

| Seeds | MRR    | Prox   | Coverage | Coherence | Diversity | Novelty | Surprise |
|-------|--------|--------|----------|-----------|-----------|---------|----------|
| 1     | 0.1037 | 0.5885 | 0.1648   | 0.4963    | 5.2       | 0.3750  | 0.5437   |
| 3     | 0.1037 | 0.6429 | 0.2148   | 0.5169    | 5.0       | 0.2313  | 0.2938   |
| 5     | 0.1037 | 0.6780 | 0.2533   | 0.5367    | 5.0       | 0.1813  | 0.2375   |
| 10    | 0.1037 | 0.7055 | 0.2783   | 0.5489    | 4.2       | 0.1188  | 0.1812   |
| 15    | 0.1037 | 0.7130 | 0.2092   | 0.5435    | 4.1       | 0.1313  | 0.1375   |

**MRR invariance** applies here too (same instrument artifact).

**TF-IDF shows a similar trajectory but with lower absolute values and a notable regression at 15 seeds:**
- Coverage peaks at 10 seeds (0.278) then drops at 15 (0.209). This suggests the TF-IDF centroid can become over-diluted with too many seeds -- additional seed terms introduce noise that pushes the centroid away from the most relevant vocabulary region.
- Proximity climbs steadily but never reaches MiniLM's levels (0.713 vs 0.773 at 15 seeds).
- TF-IDF maintains consistently higher diversity (4-5 clusters vs 2-3 for MiniLM) and higher novelty/surprise at every seed count.

**Interpretation:** TF-IDF is more sensitive to seed count than MiniLM. Its sparse vocabulary representation means each additional seed introduces new terms that shift the centroid. The sweet spot is 5-10 seeds; fewer gives poor coverage, more can dilute signal.

**Recommendation for installer:** 5-10 seeds for TF-IDF; warn that both too few and too many seeds degrade coverage.

---

## W4.2: Interest Breadth Sensitivity

**Question:** Which strategies degrade on broad interests? Which handle breadth gracefully?

Breadth groups: Narrow (P3, P8), Medium (P1, P2, P5, P6, P7), Broad (P4)

### Cross-Strategy Breadth Comparison

| Strategy | Breadth | MRR    | Prox   | Coverage | Diversity |
|----------|---------|--------|--------|----------|-----------|
| S1a      | Narrow  | 0.3272 | 0.7299 | 0.6667   | 2.5       |
| S1a      | Medium  | 0.4058 | 0.7688 | 0.6946   | 2.4       |
| S1a      | Broad   | 0.4996 | 0.8104 | 0.6833   | 3.0       |
| S1c      | Narrow  | 0.1531 | 0.6787 | 0.2583   | 3.2       |
| S1c      | Medium  | 0.1909 | 0.7330 | 0.3644   | 2.7       |
| S1c      | Broad   | 0.2116 | 0.7759 | 0.3500   | 3.0       |
| S1d      | Narrow  | 0.0794 | 0.6576 | 0.2750   | 4.5       |
| S1d      | Medium  | 0.1108 | 0.7036 | 0.2451   | 4.6       |
| S1d      | Broad   | 0.1166 | 0.7570 | 0.2000   | 5.3       |
| S1i      | Narrow  | 0.0897 | 0.6449 | 0.2583   | 4.7       |
| S1i      | Medium  | 0.1109 | 0.6974 | 0.2347   | 5.1       |
| S1i      | Broad   | 0.0859 | 0.7608 | 0.2333   | 3.7       |

### Key Finding: Broad interests HELP embedding strategies, HURT sparse strategies

**S1a (MiniLM) improves with breadth.** MRR: Narrow 0.327 -> Medium 0.406 -> Broad 0.500. Proximity also rises. This is counterintuitive -- a broad interest like "AI safety" should be harder to model than "quantum ML." The explanation: broad interests have more related papers in the corpus, so the centroid sits in a denser neighborhood where top-20 results are more likely to include held-out papers.

**S1d (TF-IDF) coverage degrades with breadth.** Coverage: Narrow 0.275 -> Medium 0.245 -> Broad 0.200. The sparse vocabulary model struggles when the interest spans diverse terminology. A narrow interest like "quantum ML" uses concentrated vocabulary (quantum, qubit, circuit, etc.) that TF-IDF matches precisely. A broad interest like "AI safety" uses diffuse vocabulary spread across multiple sub-topics, reducing centroid precision.

**S1i (SVM) MRR degrades from Medium (0.111) to Broad (0.086).** The SVM boundary is harder to learn when positive examples span a wide feature space. This is a known limitation of linear classifiers on broad concepts.

**S1c (SPECTER2 adapter) follows the same pattern as S1a** but at lower absolute levels.

### Practical Implication

For users with narrow, well-defined interests: TF-IDF is relatively more competitive (gap to MiniLM is smaller). For users with broad, cross-cutting interests: MiniLM's advantage is largest because dense embeddings capture semantic relationships that sparse features cannot.

---

## W4.4: Scale Sensitivity

**Question:** Does quality degrade when the corpus gets larger (more noise) or improve (more potential matches)?

Tested at 2K, 5K, 10K, and 19K papers with profiles P1, P3, P4.

### S1a (MiniLM) Scale Curve

| Scale  | Mean MRR | Mean Prox | Mean Coverage |
|--------|----------|-----------|---------------|
| 2,000  | 0.4737   | 0.7720    | 0.7167        |
| 5,000  | 0.4503   | 0.7784    | 0.6833        |
| 10,000 | 0.4543   | 0.7816    | 0.6833        |
| 19,252 | 0.4382   | 0.7832    | 0.6833        |

MiniLM MRR degrades by only 7.5% from 2K to 19K (0.474 -> 0.438). Coverage drops slightly from 2K to 5K then stabilizes. Proximity actually *increases* slightly with scale because the centroid sits in a denser region of the embedding space with more papers nearby.

**S1a is remarkably scale-robust.** The embedding similarity metric naturally handles more papers -- noise papers are far from the centroid and never compete with relevant results. The top-20 ranked list is essentially unchanged from 5K onward.

### S1d (TF-IDF) Scale Curve

| Scale  | Mean MRR | Mean Prox | Mean Coverage |
|--------|----------|-----------|---------------|
| 2,000  | 0.2181   | 0.7365    | 0.5167        |
| 5,000  | 0.1664   | 0.7300    | 0.4167        |
| 10,000 | 0.1482   | 0.7288    | 0.3500        |
| 19,252 | 0.1012   | 0.7340    | 0.3167        |

TF-IDF MRR degrades **dramatically** with scale: 53.6% drop from 2K to 19K (0.218 -> 0.101). Coverage drops from 0.517 to 0.317. The degradation is monotonic and roughly logarithmic.

**TF-IDF is scale-sensitive.** The TF-IDF centroid competes with a growing number of partial-vocabulary matches as the corpus grows. Papers that share some but not all relevant terms can score higher than genuinely related papers, pushing good results out of the top-20. This is a fundamental limitation of term-frequency matching at scale -- the "curse of vocabulary overlap."

### Practical Implication

At small corpus sizes (<5K), TF-IDF is meaningfully more competitive with MiniLM (MRR ratio: 0.218/0.474 = 0.46 at 2K vs 0.101/0.438 = 0.23 at 19K). For users with small corpora, TF-IDF is a reasonable zero-dependency alternative. At 50K+ papers (the realistic production range for daily arXiv monitoring), TF-IDF will be even less competitive.

---

## W4.5: Negative Signal Impact

**Question:** Does providing "anti-interest" papers as negative signals improve quality?

Tested with P1 (RL for robotics, Medium breadth) and P4 (AI safety, Broad breadth).

### S1a (MiniLM) with Negative Centroid Subtraction

| Alpha | P1 MRR | P1 Delta | P4 MRR | P4 Delta |
|-------|--------|----------|--------|----------|
| 0     | 0.4677 | --       | 0.4996 | --       |
| 0.25  | 0.4637 | -0.004   | 0.4494 | -0.050   |
| 0.50  | 0.3619 | -0.106   | 0.4152 | -0.084   |
| 0.75  | 0.2893 | -0.178   | 0.4028 | -0.097   |
| 1.00  | 0.2483 | -0.219   | 0.3602 | -0.139   |

**Negative signals universally HURT MiniLM.** Even the gentlest demotion (alpha=0.25) degrades MRR on both profiles. The effect is stronger on P1 (Medium breadth) than P4 (Broad breadth), and worsens monotonically with alpha.

**Why this happens:** Subtracting a negative centroid from a positive centroid in embedding space pushes the query vector away from the negative region. But since the negatives are already distant (category-disjoint, low-similarity papers), the subtraction mostly introduces noise into the positive centroid rather than usefully reshaping it. The dense embedding space is already effective at separating relevant from irrelevant -- negative signals add no information that the cosine ranking doesn't already capture.

### S1d (TF-IDF) with Negative Signals

| Method          | P1 MRR | P1 Delta | P4 MRR | P4 Delta |
|-----------------|--------|----------|--------|----------|
| Baseline        | 0.0987 | --       | 0.1166 | --       |
| SVM + negatives | 0.0988 | +0.000   | 0.1054 | -0.011   |
| Centroid a=0.25 | 0.1003 | +0.002   | 0.1182 | +0.002   |
| Centroid a=0.50 | 0.1069 | +0.008   | 0.1152 | -0.001   |
| Centroid a=0.75 | 0.0991 | +0.000   | 0.1150 | -0.002   |

**TF-IDF negative signals are essentially neutral.** The largest observed effect is +0.008 MRR (P1, alpha=0.5) -- within noise. SVM with explicit negative class shows zero improvement on P1 and slight degradation on P4.

**Why TF-IDF is neutral:** The sparse term vectors of category-disjoint negatives (physics, eess, math, astro-ph papers) have almost zero vocabulary overlap with the positive seeds (CS/AI papers). Subtracting the negative centroid in TF-IDF space mostly subtracts terms that aren't present in the positive centroid anyway. The operation is a near-no-op.

### Practical Implication

**Do not implement negative signals in v1.** For MiniLM, they actively degrade quality. For TF-IDF, they add complexity with no measurable benefit. This finding holds for category-disjoint negatives (the most natural user interaction -- "I don't care about physics papers"). Negatives might help for near-miss papers (e.g., "I like RL but not multi-agent RL"), but that requires a more sophisticated interaction model that is out of scope for the installer configuration.

---

## Summary Table: Context Sensitivity

| Context Variable  | S1a Impact | S1d Impact | Installer Action |
|-------------------|------------|------------|------------------|
| Seed count (1-15) | Minimal MRR change; coverage saturates at 5 | Similar pattern but coverage peaks at 10, regresses at 15 | Recommend 5+ seeds; no hard minimum |
| Interest breadth  | Improves with breadth (MRR +52% narrow to broad) | MRR improves but coverage degrades (-27% narrow to broad) | Note that TF-IDF is more competitive for narrow interests |
| Corpus scale      | -7.5% MRR from 2K to 19K | -53.6% MRR from 2K to 19K | At >10K papers, strongly prefer MiniLM |
| Negative signals  | Actively harmful (up to -22% MRR) | Neutral (within noise) | Do not implement in v1 |

## Confidence Notes

- **W4.1 MRR invariance** is an instrument artifact, not a finding about seed sensitivity. The LOO instrument always uses cluster_papers as seeds, so user seed count has no effect on MRR. The other 6 instruments do respond to seed count and are the relevant data for this question.
- **W4.2 Broad (N=1)** has only one profile (P4), so breadth findings for "Broad" are essentially single-profile observations. The Narrow -> Medium pattern is more reliable (N=2 and N=5 respectively).
- **W4.4 preserved papers** inflate small-corpus results slightly because seed/held-out/cluster papers are always included in the subsample, giving them a relative advantage as the random noise around them is reduced.
- **W4.5 negative selection** used category-disjoint + low-similarity papers. Different negative paper selection strategies (e.g., near-miss negatives from the same category) might produce different results.
