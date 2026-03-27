# Spike 003: Strategy Profiling -- Findings

**Status:** CLOSED WITH QUALIFICATIONS — see Section 8
**Spike duration:** W0-W5 across three sessions (execution, gap-fills, qualitative review completion + epistemic revision)
**Corpus:** 19,252 arXiv papers (OAI-PMH harvest, 57% Jan 2026, 34% 2025, 9% older; CS/ML-dominated)
**Profiles:** 8 interest profiles, 3 seed selections each, 24 observations per strategy. Profiles constructed from MiniLM-based BERTopic clustering (entanglement documented in Section 8).
**Instruments:** leave-one-out MRR (entangled with MiniLM), seed proximity, topical coherence, cluster diversity, novelty, category surprise, coverage
**Qualitative review:** 21 reviews across 4 checkpoints (W1: 9 reviews, W3: 3, W4.1: 3, W5.4: 3, extensions: 3), AI-assessed

---

## 1. Executive Summary

Two content-based strategies survived profiling as default views: MiniLM centroid (S1a) and TF-IDF cosine (S1d). They capture two distinct quality dimensions — semantic precision and keyword precision — that are genuinely complementary (Jaccard overlap 0.179, different held-out recoveries) but incommensurable: fusion degrades quality on aggregate, though W3 qualitative review found it helps narrow technical topics. SPECTER2 proximity adapter (S1c) was initially included as a third view but the W5.4 qualitative review found it qualitatively redundant with MiniLM (45-60% overlap, score compression making ranking noise). The default architecture is two parallel views; fusion and kNN retrieval have profile-dependent niches.

Metadata strategies are boosters or pre-filters, not rankers. Graph strategies are algorithmically valid but data-limited. SVM, title-only variants, and raw centroid were eliminated with measured cause. The Voyage AI embedding verdict is INCONCLUSIVE due to insufficient screening methodology (see Section 8).

**The most important meta-finding:** Three of four prescribed qualitative review checkpoints were initially skipped. When performed, they contradicted quantitative conclusions in multiple cases. Quantitative metrics and qualitative review are not competing methods where one validates the other — they are complementary modes of inquiry that produce different knowledge. Skipping qualitative review doesn't reduce confidence; it produces wrong conclusions.

---

## 2. Per-Wave Findings

### W0: SPECTER2 Adapter Fix

The SPECTER2 proximity adapter was loaded correctly using the `adapters` library, replacing improper prior loading. Adapter-loaded embeddings differ meaningfully from base model (cosine similarity 0.985 mean, not identity). The adapter produces slightly different rankings that better reflect citation-community structure. This fixed a known epistemic failure from Spike 001 where all SPECTER2 findings used the base model without the adapter.

### W1: Individual Strategy Profiling

**Content strategies (W1A):** Six strategies profiled. MiniLM centroid (S1a) leads on MRR (0.398) and coverage (0.686). SPECTER2 adapter (S1c) shows MRR 0.184 with severe score compression (0.009 spread). TF-IDF cosine (S1d) has MRR 0.104 but qualitative review revealed it recovers more held-out papers than MiniLM (5/15 vs 2/15). SVM (S1i) eliminated (same quality as TF-IDF, 10x latency). Raw centroid (S1j) eliminated (mathematical identity with S1a).

**Metadata strategies (W1B):** Ten strategies profiled. Category filtering (S2a) is the strongest with seed proximity 0.454 but MRR 0.004 -- pre-filter only, not a ranker. Co-author network (S2f) has 0.2% coverage -- micro-signal at best. FWCI and citation signals (S2d/S2e) are non-functional at 2.6% enrichment coverage.

**Graph strategies (W1C):** Bibliographic coupling (S3a) has zero MRR because only 1/120 seed papers has reference data. However, focused evaluation on the 95 papers with references shows the algorithm validly discriminates (mean discrimination 0.467). The signal is real; coverage must expand. Related works (S3c) is non-functional (zero papers have the field populated).

**Baselines (W1D):** Random (S6a) scores MRR 0.000 and coverage 0.000 -- confirmed floor. Category baseline (S6d) scores MRR 0.004 -- barely above random. All viable strategies substantially exceed these baselines.

### W2: Configuration Sensitivity

**Title-only embeddings (W2.1):** 74-77% MRR collapse for both MiniLM and SPECTER2 when using only titles. Abstract information is load-bearing. Title-only is not a viable cost-reduction strategy.

**Top-K sweep (W2.2):** Smooth precision-coverage tradeoff with no elbow. K=20 is a good default. MRR saturates by K=50; coverage saturates by K=100. Increasing K beyond 100 adds only diversity (more clusters represented), not quality.

**Quantization (W2.5):** float16 is a free lunch for both models (zero quality loss, 50% storage savings). int8 works for MiniLM (< 5% degradation) but fails for SPECTER2 (quantization error 0.006 vs signal spread 0.009 -- destroys 67% of the signal).

### W3: Combinations and Pipelines

**Pairwise fusion (W3.1-W3.3):** All RRF and weighted combinations degrade MiniLM. Best RRF (MiniLM + TF-IDF) achieves MRR 0.279 vs MiniLM alone at 0.398 (-30%). Best weighted (0.7 MiniLM + 0.3 TF-IDF) achieves 0.310 (-22%). Three-way fusion is worse still.

**Pipeline architectures (W3.4):** Five pipeline architectures tested. Category pre-filter -> MiniLM (P5) and keyword pre-filter -> MiniLM (P6) both produce results bit-identical to MiniLM standalone. The pre-filters do not help because MiniLM already ranks category-relevant and keyword-relevant papers at the top.

**Why fusion fails:** The strategies value different quality dimensions that are incommensurable. Semantic precision (MiniLM), keyword precision (TF-IDF), and community connectivity (SPECTER2) cannot be collapsed into a single ranking without compromising at least one dimension. The complementarity is real but must be surfaced as parallel views.

### W4: Context Sensitivity

**Cold start (W4.1):** MiniLM works from 1 seed (coverage 0.366), improves rapidly to 3 seeds (0.567), and saturates at 5 (0.686). TF-IDF needs 5+ seeds to be functional (1-seed coverage 0.165). MiniLM is the only viable cold-start strategy.

**Breadth (W4.2):** MiniLM improves with breadth: narrow MRR 0.327 -> broad MRR 0.500 (+52%). TF-IDF degrades: narrow 0.079 -> broad 0.117, but coverage drops. Broad interests dilute TF-IDF's keyword signal but improve MiniLM's centroid estimation.

**Scale (W4.4):** MiniLM is robust to corpus growth (-7.5% MRR at synthetic 50K). TF-IDF collapses (-54% MRR at 50K). Vocabulary growth dilutes term discrimination for TF-IDF. Note: scale tests used synthetic duplication, which preserves vocabulary but not diversity.

**Negative signals (W4.3):** Analysis determined that negative signal implementation carries risk of degrading small profiles without demonstrated benefit. Recommendation: do not implement in v1.

---

## 3. The Parallel Views Architecture

### Why fusion fails

Every combination architecture tested -- RRF, weighted linear, pipeline, consensus -- either degrades the best individual strategy (MiniLM) or converges to it. The fundamental reason: the strategies capture different quality dimensions that cannot be reduced to a single ranking.

| Dimension | MiniLM | TF-IDF | SPECTER2 |
|-----------|--------|--------|----------|
| Semantic precision | Best | Moderate | Moderate |
| Keyword precision | Moderate | Best | Low |
| Held-out recovery | 2/15 | 5/15 (Best) | 0/15 |
| Cross-community discovery | Low | Low | Best |
| Score informativeness | Moderate (0.053) | Best (0.072) | None (0.009) |
| Scale robustness | Best (-7.5%) | Poor (-54%) | Unknown |

Fusing these into one number necessarily loses information. A paper that MiniLM ranks #3 and TF-IDF ranks #47 might be semantically close but use different vocabulary -- the fusion has to decide whether it's #10 or #25, and either answer is wrong from one strategy's perspective.

### What works instead

Present each strategy as a **named perspective** on the recommendation space:

- **"Similar papers"** (S1a MiniLM): papers semantically related to your interests
- **"Keyword matches"** (S1d TF-IDF): papers using the same terminology as your seeds
- **"Related communities"** (S1c SPECTER2): papers from research groups that work on related problems

Each view has its own ranking, its own strengths, and its own blind spots. The user can browse all three or focus on the one that matches their current need.

---

## 4. Context Sensitivity Table for Installer

| User Context | Recommended Config | Primary View | Secondary Views | Rationale |
|-------------|-------------------|-------------|----------------|-----------|
| First paper added (cold start) | S1a only, K=20 | Similar papers | None | Only MiniLM is functional at 1 seed |
| 3-5 papers added | S1a + S1d, K=20 | Similar papers | Keyword matches | TF-IDF becomes viable, adds unique recoveries |
| 5+ papers, narrow interest | S1a + S1d, K=20 | Similar papers | Keyword matches | MiniLM excels on distinctive vocabulary; TF-IDF adds keyword precision |
| 5+ papers, broad interest | S1a primary, K=20 | Similar papers | Optional: keywords | MiniLM improves with breadth; TF-IDF degrades |
| Small corpus (<5K papers) | S1a + S1d, K=20 | Similar papers | Keyword matches | TF-IDF competitive at small scale |
| Large corpus (>10K papers) | S1a primary, K=20 | Similar papers | Optional: keywords | TF-IDF collapses at scale (-54% at 50K) |
| Exploration/discovery mode | S1a + S1c + S1d, K=50-100 | All three views | -- | Maximum perspective coverage |

**Storage defaults:**
- float16 for all embeddings (zero quality loss, 50% storage savings)
- float32 for search computation (quantization only for storage)
- TF-IDF rebuilt on startup (2.2s for 19K papers)

---

## 5. Evaluation Framework Reflection

### The circular evaluation bias

The most important methodological finding: LOO-MRR evaluation uses clusters defined by MiniLM embeddings, which circularly favors MiniLM-based strategies. Evidence:

1. TF-IDF scores 0.104 MRR (4x below MiniLM) but 5/15 held-out recovery (2.5x above MiniLM)
2. SPECTER2's score compression (0.009 spread) makes MRR penalize it for inability to rank, not inability to find relevant papers
3. Qualitative review found all three strategies produce approximately 80% on-topic recommendations -- the quality gap is much smaller than MRR suggests

**Corrective:** MRR is still useful for comparing strategies within the same family (e.g., MiniLM float32 vs float16) but should not be used to rank across families without adjustment. Held-out recovery and qualitative assessment provide complementary quality signals.

### Quantitative vs qualitative divergence

The most striking divergence: TF-IDF is the *worst* strategy by MRR and the *best* by held-out recovery. This is not a contradiction -- it reflects the evaluation framework measuring different aspects of quality. MRR measures: "how highly does the strategy rank the held-out paper?" Held-out recovery measures: "does the strategy find the held-out paper at all?"

TF-IDF finds papers that MiniLM misses entirely (different vocabulary routes to the same topic) but ranks them lower in its list. MiniLM finds fewer held-out papers but ranks the ones it finds very highly.

### Quality is multi-dimensional

Three distinct quality dimensions emerged from qualitative review:

1. **Semantic precision:** How well does the strategy match the meaning of the seed papers? (MiniLM best)
2. **Keyword precision:** How well does the strategy match the terminology? (TF-IDF best)
3. **Cross-community discovery:** Does the strategy surface papers from related but differently-named research communities? (SPECTER2 best)

No single metric captures all three. A system offering only one strategy is leaving value on the table.

---

## 6. What We Know With Evidence

| Claim | Evidence | Confidence |
|-------|----------|------------|
| MiniLM is the best single strategy for general use | MRR 0.398, coverage 0.686, context-robust | HIGH |
| TF-IDF recovers papers MiniLM misses | 5/15 held-out vs 2/15, Jaccard 0.179 | HIGH |
| SPECTER2 provides unique cross-community signal | 25/60 unique papers, cross-category discoveries | MEDIUM |
| Fusion degrades the best strategy | 4 RRF variants, 3 weighted variants, 5 pipelines -- all degrade or converge | HIGH |
| MiniLM works from 1 seed paper | Coverage 0.366 at 1 seed | HIGH |
| MiniLM saturates at 5 seeds | Coverage 0.686 at 5, 0.687 at 10 | HIGH |
| TF-IDF collapses at scale | -54% MRR at synthetic 50K | MEDIUM (synthetic data caveat) |
| float16 is free for both models | Zero MRR change, 50% storage savings | HIGH |
| int8 fails for SPECTER2 | Error magnitude 67% of signal spread | HIGH |
| Title-only is not viable | 74-77% MRR collapse | HIGH |
| SVM adds nothing over TF-IDF | MRR 0.099 vs 0.104, 10x latency | HIGH |
| Category filtering is a pre-filter, not a ranker | MRR 0.004, but seed proximity 0.454 | HIGH |
| Bibliographic coupling algorithm is valid | Discrimination 0.467 on 95-paper subset | MEDIUM (tiny sample) |
| Graph strategies need enrichment expansion | 95/19252 papers have references | HIGH |

---

## 7. What We Don't Know

| Question | Why we can't answer | What would resolve it |
|----------|--------------------|-----------------------|
| How do strategies perform with human relevance judgments? | No human evaluation conducted | User study with real researchers |
| How stable are profiles across months? | Only January 2026 data | Multi-month longitudinal study |
| Does TF-IDF really collapse at scale with real (not synthetic) data? | Synthetic duplication preserves vocabulary | Real corpus at 50K+ unique papers |
| How does SPECTER2 perform with full enrichment coverage? | 95/19252 papers enriched | Expand OpenAlex enrichment to full corpus |
| What is the optimal vocabulary overlap threshold for strategy switching? | Vocabulary overlap is qualitatively observed, not measured | Formal vocabulary distinctiveness metric |
| Does the parallel views architecture actually improve user satisfaction? | Architecture derived from analysis, not tested | A/B test with real users |
| Are there quality dimensions we missed? | Only 3 profiles qualitatively reviewed | Broader qualitative review |

---

## 8. Critical Limitations

### Limitations of the experimental apparatus

1. **Evaluation framework entanglement.** The entire evaluation pipeline — BERTopic clusters, interest profiles, seed papers, held-out papers, LOO-MRR ground truth — is built on MiniLM's representation of the corpus. "Relevant" in this evaluation means "relevant as MiniLM would define it." Cross-family comparisons (MiniLM vs TF-IDF vs SPECTER2) are systematically biased toward MiniLM. Within-family comparisons (e.g., MiniLM float32 vs float16) are unaffected. Qualitative review partially corrects the bias by assessing relevance from titles/abstracts directly.

2. **No human relevance judgments.** All quality assessments are mathematical proxies or AI-generated narratives. We have no ground truth for whether human researchers would agree with the strategy characterizations. The AI qualitative reviews are internally consistent and caught real issues (TF-IDF undervaluation, SPECTER2 redundancy), but systematic AI reviewer bias cannot be ruled out.

3. **Interest profiles are AI-constructed.** The 8 profiles were selected by mapping BERTopic topics to research areas by name, then selecting papers from those topics. A paper that MiniLM embeds poorly cannot appear in any profile. Real researchers' interests may not align with MiniLM's clustering of the topic space.

### Limitations of the corpus

4. **Single month of data (primarily).** 57% of papers are from January 2026, 34% from 2025, 9% older updates. Seasonal effects (post-AAAI, pre-ICML) may skew the corpus. Multi-month evaluation would be needed to assess stability.

5. **CS/ML domain dominance.** 77% of papers are in the top 15 CS categories. Findings may not generalize to other arXiv domains (physics, math, biology) where vocabulary density, community structure, and citation patterns differ.

6. **Low citation maturity.** Most papers are weeks to months old. Citation-based strategies (FWCI, bibliographic coupling, co-citation) were effectively non-functional. On a corpus with mature citations, the strategy landscape could be substantially different.

7. **Synthetic scale testing.** The -54% TF-IDF degradation at 50K is from duplicated corpus data that preserves vocabulary but not diversity. Real scaling effects may differ.

### Methodological failures during execution

8. **Skipped qualitative checkpoints.** Three of four prescribed qualitative review checkpoints were skipped in the initial session. When later performed, they contradicted quantitative conclusions in multiple cases (SPECTER2 redundancy, fusion profile-dependence, kNN niche utility, cold-start echo chambers). The initial DECISION.md contained materially wrong conclusions as a result.

9. **Voyage screening methodology.** The Voyage embedding screening used a 100-paper pool (20% selectivity), top-K Jaccard as sole metric, 2/8 profiles, and no qualitative review. Every aspect of this methodology is insufficient. The Voyage verdict has been changed from STOP to INCONCLUSIVE. See `sig-2026-03-20-jaccard-screening-methodology`.

10. **Extension experiments designed ad-hoc.** Gap-fill and extension experiments (Voyage, BM25, cross-encoder, kNN/MMR) were designed without the epistemic rigor of the core DESIGN.md. They appear in FINDINGS.md alongside rigorously designed experiments without distinction. See `sig-2026-03-20-spike-experimental-design-rigor`.

11. **Confidence levels originally overstated.** The initial DECISION.md used blanket HIGH/MEDIUM/LOW confidence that collapsed measurement accuracy, interpretation validity, and extrapolation reliability. Revised to use a three-level framework (measurement / interpretation / extrapolation) with explicit conditions. See DECISION.md Section 8.

### What these limitations mean for downstream decisions

The findings ARE informative about how retrieval strategies behave on recent CS/ML arXiv papers. The strategy characterizations (MiniLM for semantic precision, TF-IDF for keyword precision, their complementarity) are well-supported by both quantitative and qualitative evidence and are likely to hold within the tested domain. The architectural decision (parallel views, two views not three, centroid retrieval) is reasonable as a v1 default.

What the findings CANNOT support: claims about optimal strategy for other domains, claims about API embedding redundancy (Voyage verdict inconclusive), claims that the specific MRR numbers reflect true quality differences between strategies (evaluation framework entanglement), or claims that human researchers would agree with the AI qualitative assessments.

The honest summary: we know more than we did before Spike 003, but less than the initial DECISION.md claimed. The most reliable findings are the qualitative characterizations of strategy behavior and the elimination decisions. The least reliable are the cross-family quantitative rankings and the Voyage screening.
