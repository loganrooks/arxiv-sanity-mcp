# Spike Decision: Comprehensive Strategy Profiling

**Completed:** 2026-03-20
**Status:** CLOSED WITH QUALIFICATIONS — see Section 8
**Question:** What are the complete quality, resource, and behavioral profiles of every viable recommendation/filtering strategy?
**Answer:** Two viable content strategies (MiniLM, TF-IDF) capture complementary quality dimensions that cannot be fused. The correct architecture is parallel views with MiniLM as primary. SPECTER2 is qualitatively redundant with MiniLM and is dropped from the default configuration. API embedding models (Voyage AI) remain inconclusive — the screening methodology was insufficient to produce a verdict. Centroid retrieval is the correct default within each view.

> **Epistemic health warning:** This spike's most important findings came from qualitative reviews that contradicted quantitative metrics. Three of four prescribed qualitative checkpoints were initially skipped and only completed in a follow-up session. Several conclusions that appeared firm on quantitative evidence alone were revised or overturned by qualitative assessment. The remaining unqualified conclusions should be treated as provisional until validated by human evaluation. See Section 8 for specific qualifications.

## Summary

Spike 003 profiled 17+ strategies across 7 waves using 6 quantitative instruments, 21 qualitative reviews (9 W1 + 12 follow-up), and 4 context sensitivity dimensions on a 19,252-paper arXiv corpus. Two content-based strategies survived as default views: MiniLM centroid (S1a) as the primary recommendation engine and TF-IDF cosine (S1d) as a keyword-precision alternative view. SPECTER2 (S1c) was initially included as a third view but was dropped after the W5.4 qualitative review found it qualitatively redundant with MiniLM (45-60% paper overlap, score compression making ranking noise). Four strategies were eliminated with measured cause (SVM, title-only variants, raw centroid). Metadata strategies function as pre-filters and boosters, not rankers. Graph strategies are algorithmically valid but data-limited at current enrichment coverage.

The most significant finding is that fusion is profile-dependent, not universally bad: quantitative metrics showed all fusion methods degrading MiniLM, but the W3 qualitative review found fusion helps narrow technical topics (P8), is neutral for well-defined topics (P4), and dilutes for medium-breadth topics (P1). The MRR verdict was contradicted qualitatively in 2 of 3 cases. The two surviving strategies ARE complementary — they find different papers (Jaccard 0.179) and TF-IDF recovers held-out papers MiniLM misses (5/15 vs 2/15) — but for the default architecture, parallel views is more robust than fusion.

The Voyage AI screening is **inconclusive** — not negative as originally reported. The screening used top-K Jaccard on a 100-paper pool (20% selectivity) with only 2 of 8 profiles tested. This methodology has fundamental limitations (see `sig-2026-03-20-jaccard-screening-methodology`): the small pool inflates agreement, Jaccard collapses the nature of divergence into a single number, and no qualitative review was performed. Spike 004 will re-evaluate with proper methodology.

kNN-per-seed's aggregate -58% MRR hides profile-dependence: it works for densely-populated topics (P4/AI safety) where per-seed neighborhoods all land in relevant territory. MMR provides marginal diversity improvement (+6.6%) at near-zero quality cost (-2.8% MRR).

The most important methodological finding: three of four prescribed qualitative review checkpoints were initially skipped. When performed, they contradicted quantitative conclusions in multiple cases (SPECTER2 redundancy, fusion profile-dependence, kNN niche utility, cold-start echo chambers). This validates the DESIGN.md's principle that qualitative review is first-class, not a validation step — and demonstrates the cost of treating it as optional.

## Findings

Detailed findings with all measurements are in FINDINGS.md. Cross-encoder gap fill findings in `experiments/W3_4_GAP_FINDINGS.md`. Voyage and strategy pattern findings in `experiments/W5_VOYAGE_KNN_MMR_FINDINGS.md`. Key numbers below.

### Strategy Profiles

| Strategy | MRR | Coverage | Held-out Recovery | Character |
|----------|-----|----------|-------------------|-----------|
| S1a MiniLM | 0.398 | 0.686 | 2/15 | Semantic precision |
| S1c SPECTER2 | 0.184 | 0.336 | 0/15 | Cross-community discovery |
| S1d TF-IDF | 0.104 | 0.247 | 5/15 | Keyword precision |
| S6a Random | 0.000 | 0.000 | -- | Floor |
| S6d Category | 0.004 | 0.033 | -- | Baseline |

### Eliminated Strategies

| Strategy | Reason |
|----------|--------|
| S1g MiniLM title-only | 74% MRR collapse |
| S1h SPECTER2 title-only | 77% MRR collapse |
| S1i SVM | Same quality as TF-IDF at 10x latency |
| S1j Raw centroid | Mathematical identity with S1a |
| S2d FWCI | Non-functional at 2.6% enrichment |
| S2e Citations | Non-functional; papers too recent |
| S3c Related works | Zero data populated |
| S4a Cross-encoder rerank | Domain mismatch; 71-85% MRR degradation; 700-940x latency penalty |
| Voyage AI (voyage-4, voyage-4-large) | **INCONCLUSIVE** — Jaccard screening on 100-paper pool (20% selectivity) insufficient; no qualitative review; see sig-2026-03-20. Deferred to Spike 004. |
| kNN-per-seed retrieval | Aggregate -58% MRR, but profile-dependent: works for dense topics (P4). Not a default, but has a niche. |

### Combination Results

| Method | Best MRR | vs S1a Alone |
|--------|----------|-------------|
| RRF (MiniLM + TF-IDF) | 0.279 | -30% |
| Weighted (0.7/0.3) | 0.310 | -22% |
| Pipeline (union -> MiniLM rerank) | 0.398 | 0% (converges to S1a) |
| Pipeline (MiniLM -> CE rerank) | 0.117 | -71% |
| Pipeline (union -> CE rerank) | 0.058 | -85% |

### Cross-Encoder Gap Fill (W3.4)

Cross-encoder reranking (`cross-encoder/ms-marco-MiniLM-L-6-v2`) was the last untested pipeline architecture. Results are unambiguous:

| Strategy | MRR | Coverage | p50 Latency |
|----------|-----|----------|-------------|
| S1a (baseline) | 0.398 | 0.686 | 57 ms |
| P5 (union -> MiniLM rerank) | 0.398 | 0.686 | 136 ms |
| S4a (MiniLM -> CE rerank) | 0.117 | 0.395 | 232 ms |
| S4a-union (union -> CE rerank) | 0.058 | 0.214 | 572 ms |

The cross-encoder breaks the MiniLM convergence pattern (Jaccard 0.168 vs S1a; rank correlation 0.029) but in the wrong direction. It does rescue some TF-IDF-unique candidates (9.4% rescue rate, 6 held-out recoveries) but simultaneously demotes MiniLM's high-quality candidates. Net effect: catastrophic quality loss across all 8 profiles.

Root cause: MS MARCO domain mismatch. The cross-encoder was trained on web search query-passage pairs, not academic paper-to-paper relevance. A domain-specific cross-encoder would be needed, but no such checkpoint exists and fine-tuning would require labeled data we do not have.

### Voyage AI Screening (W5)

| Model pair | Mean Jaccard | Interpretation |
|------------|-------------|----------------|
| voyage-4 vs voyage-4-large | 0.920 | Near-identical models |
| SPECTER2 vs voyage-4/4-large | 0.772 | Moderate overlap, closer to SPECTER2 |
| MiniLM vs voyage-4 | 0.717 | Moderate overlap |
| MiniLM vs voyage-4-large | 0.705 | Moderate overlap |
| MiniLM vs SPECTER2 (baseline) | 0.732 | Baseline inter-model overlap |

**Verdict: INCONCLUSIVE** (originally STOP, revised 2026-03-20). The Jaccard-based screening has fundamental methodological limitations that prevent a confident verdict:

1. **Pool size artifact:** Top-20 from 100 papers = 20% selectivity. At this pool size, models are forced to agree because there aren't enough alternatives. Real selectivity is 0.1% (top-20 from 19K).
2. **Profile coverage:** Only 2 of 8 profiles tested (P1, P3). Per-seed Jaccard ranged 0.429-0.905 — too variable for the aggregate to be representative.
3. **No qualitative review:** The ~28% of papers Voyage finds differently were never examined for what kind of papers they are.
4. **Invalid baseline:** Thresholds calibrated against MiniLM-SPECTER2 overlap as "known different," but W5.4 qualitative review found SPECTER2 qualitatively redundant with MiniLM.
5. **Jaccard as sole criterion:** Contradicts the spike's own principle that "instruments detect, they don't evaluate."

See signal `sig-2026-03-20-jaccard-screening-methodology`. Proper evaluation deferred to Spike 004 with representative 2000-paper sample, multiple metrics, and qualitative review.

### Strategy Patterns (W5b)

| Strategy | Mean MRR | Mean R@20 | Mean Hit@5 | Mean Diversity |
|----------|----------|-----------|------------|----------------|
| Centroid (baseline) | 0.354 | 0.308 | 0.417 | 0.456 |
| kNN-per-seed | 0.149 | 0.167 | 0.125 | 0.572 |
| MMR (lambda=0.7) | 0.344 | 0.250 | 0.458 | 0.486 |

kNN-per-seed catastrophically degrades quality. The per-seed approach finds papers tangentially related to individual seeds, missing the intersection of interest. Centroid averaging is not "washing out" distinctive seeds -- it is correctly capturing the shared topic.

MMR is a marginal improvement: slightly better diversity (+6.6%) at near-zero quality cost (-2.8% MRR), but the diversity gain comes from swapping a few bottom-of-top-20 papers. Not architecturally significant.

### Context Sensitivity

| Context | MiniLM | TF-IDF |
|---------|--------|--------|
| 1 seed | Coverage 0.366 | Coverage 0.165 |
| 5 seeds | Coverage 0.686 | Coverage 0.253 |
| Narrow interest | MRR 0.327 | MRR 0.079 |
| Broad interest | MRR 0.500 (+52%) | MRR 0.117 (-27% rel.) |
| 50K corpus | MRR 0.368 (-7.5%) | MRR 0.048 (-54%) |

## Analysis

| Option | Pros | Cons | Spike Evidence |
|--------|------|------|----------------|
| MiniLM only | Simplest; highest MRR; robust to context | Misses keyword-precise and cross-community papers | MRR 0.398, coverage 0.686, but only 2/15 held-out recovery |
| MiniLM + TF-IDF fusion | -- | Degrades MiniLM by 22-30% | All fusion variants tested; all degrade |
| Cross-encoder reranking | Could break MiniLM convergence | Domain mismatch: -71 to -85% MRR; 700-940x latency | Tested with MS MARCO CE; no domain-specific CE available |
| API embeddings (Voyage) | Higher-dim model; possibly better quality | Partial overlap with local models; API dependency; no new signal | Screening shows Jaccard 0.717-0.772 with local models |
| Parallel views (MiniLM primary) | Maximum information; no quality loss; user chooses perspective | More complex UI; user must understand views | Complementarity confirmed (Jaccard 0.179, 9 unique recoveries) |
| TF-IDF primary | Best held-out recovery (5/15); widest score spread | Collapses at scale (-54%); degrades with breadth | Context sensitivity data rules this out for general use |
| All three views | Maximum coverage; discovery mode | SPECTER2 cannot rank standalone; needs secondary ranking signal | Score compression (0.009) confirmed |
| MMR within views | Marginal diversity improvement | +6.6% diversity, -2.8% MRR; architecturally insignificant | 24-config comparison across 8 profiles |

## Decision

This spike produced two kinds of outcomes: decisions the evidence supports, and questions the evidence clarified but did not resolve. Presenting both as "decisions" would overstate the evidence. See `sig-2026-03-20-premature-spike-decisions`.

### Decided (evidence sufficient)

| Decision | Evidence | Confidence |
|----------|----------|------------|
| **float16 storage, float32 compute** | Paired measurement: zero quality loss, 50% storage savings | HIGH (direct measurement) |
| **Eliminate SVM (S1i)** | Same quality as TF-IDF at 10x latency | HIGH (same-framework comparison) |
| **Eliminate title-only embeddings** | 74-77% MRR collapse for both models | HIGH (direct measurement) |
| **Eliminate cross-encoder reranking (current models)** | MS MARCO domain mismatch: -71 to -85% MRR, 700-940x latency | HIGH (clear cause identified) |
| **MiniLM and TF-IDF are complementary** | Jaccard 0.179, different held-out recoveries (2/15 vs 5/15), qualitative review confirms different paper types | HIGH (quantitative + qualitative alignment, model-independent finding) |
| **Strategies should not be fused by default** | All tested fusion methods degrade aggregate quality; but see deferred item on profile-dependent fusion | MEDIUM-HIGH (aggregate finding solid; per-profile nuance deferred) |
| **TF-IDF has scale and cold-start limitations** | -54% MRR at 50K (synthetic); vocabulary false positives at 1-seed cold start (qualitative) | MEDIUM (scale test was synthetic; cold-start finding is qualitative) |
| **Seed heterogeneity matters more than seed count** | W4.1 qualitative: echo chambers with homogeneous seeds, vocabulary false positives for TF-IDF at narrow cold start | MEDIUM (3-profile AI qualitative review) |

### Deferred (evidence insufficient or qualified — requires Spike 004+)

| Question | What we learned | Why decision is premature | What would resolve it |
|----------|----------------|--------------------------|----------------------|
| **Which embedding model should be primary?** | MiniLM scored highest on MRR (0.398), but the evaluation framework is circularly biased toward MiniLM (clusters, profiles, LOO all built on MiniLM). Qualitative review found all strategies produce ~80% on-topic results. | MiniLM's apparent advantage may be partially or wholly an artifact of framework entanglement. | Model-independent evaluation: human judgments, category-based ground truth, or evaluation clusters from non-MiniLM representation. |
| **How many views? Which models?** | W5.4 qualitative found SPECTER2 redundant with MiniLM in CS/ML (45-60% overlap, score compression). But this was 3 profiles, one domain, AI reviewer. | SPECTER2 may not be redundant in other domains where citation communities diverge from vocabulary. The "two views" conclusion is domain-specific. | Test across non-CS domains. Test with Voyage or other models that might provide a genuinely different second embedding view. |
| **Do API embeddings add value?** | Voyage screening found Jaccard 0.717-0.772 with local models. But the screening used a 100-paper pool (20% selectivity), Jaccard as sole metric, 2/8 profiles, no qualitative review. | Methodology was insufficient for a verdict. Pool size inflated agreement; Jaccard collapses nature of divergence; profiles where Voyage might shine were untested. | Spike 004: 2000-paper representative sample, multiple metrics (rank correlation, score distribution, semantic clustering), qualitative review of divergent papers, all 8 profiles. |
| **Should fusion be offered per-profile?** | W3 qualitative found fusion helps narrow technical topics (P8), is neutral for broad (P4), dilutes for medium (P1). | The blanket "fusion degrades" conclusion was too strong. Fusion's value is profile-dependent. | More profiles tested qualitatively with fusion. Design question: can the system detect when fusion helps? |
| **Is kNN useful for dense topics?** | Extensions qualitative found kNN works for P4 (AI safety) where per-seed neighborhoods all land in relevant territory. Aggregate -58% MRR hides this. | Profile-dependent finding on 1 profile. | Test across more dense-topic profiles to see if the pattern generalizes. |
| **Parallel views vs other architectures?** | Parallel views preserves optionality and avoids fusion degradation. But it's a conservative default, not an empirically validated optimal architecture. | No user testing. The question "would a researcher actually switch views?" is unanswered. | User study or at minimum simulated workflow evaluation. |

### Provisional v1 defaults (pragmatic, not decided)

For implementation purposes, the following are reasonable v1 defaults given current evidence. They are NOT settled decisions — they are the safest starting point given uncertainty. Implementation should remain flexible enough to change these when Spike 004 provides better evidence.

- **MiniLM as initial embedding model** — best-measured performance, even if the measurement is biased. Pragmatic starting point.
- **TF-IDF as second view** — genuinely complementary signal (vocabulary match vs semantic similarity). This complementarity is model-independent and well-supported.
- **Parallel views as presentation** — preserves optionality. Can always add fusion later.
- **Centroid retrieval as default** — well-tested, robust. kNN as optional mode for dense topics.
- **Embedding layer should be model-agnostic** — do NOT hard-code MiniLM. The model may change after Spike 004.

## Success Criteria Assessment

| # | Question | Answer | Grounded? | Qualification |
|---|----------|--------|-----------|---------------|
| 1 | Quality profiles of each viable strategy? | 2 viable default + 1 optional + 10 eliminated + 4 data-limited | YES for measurements | Profiles are accurate for CS/ML arXiv papers; MRR rankings are entangled with MiniLM evaluation framework |
| 2 | Which complement, which are redundant? | S1a/S1d complement. S1c redundant with S1a (W5.4 qualitative). S1i/S1j redundant. Voyage INCONCLUSIVE. | PARTIAL | Complementarity confirmed. Voyage verdict retracted (methodology insufficient). |
| 3 | Minimum viable config? | S1a (MiniLM) with 3+ heterogeneous seeds, K=20, float16 storage | YES | Cold-start qualitative added: seed heterogeneity matters more than count |
| 4 | Recommended config and cost? | S1a primary + S1d secondary. 14.1 MB storage, 33s GPU one-time, 2.2s TF-IDF build. | YES | Resource measurements are direct, not proxy-based |
| 5 | Maximum quality config? | S1a + S1d (two views). SPECTER2 dropped per W5.4 review. | REVISED | Original answer was three views; qualitative review changed this |
| 6 | Cold start curve? | MiniLM: 1 seed functional, 5 saturated. TF-IDF: disqualifying at cold start for narrow domains. | REVISED | W4.1 qualitative found echo chambers and vocabulary false positives not visible in metrics |
| 7 | Narrow vs broad behavior? | MiniLM improves with breadth (+52%). TF-IDF degrades (-27%). | YES | Consistent across quantitative and qualitative |
| 8 | SPECTER2 adapter impact? | Adapter loaded correctly. Different from base model. Qualitatively redundant with MiniLM. | REVISED | W5.4 review overturned the W1 characterization of SPECTER2 as uniquely valuable |
| 9 | Installer-consumable data? | strategy_profiles.json produced but needs update with qualitative revisions | PARTIAL | JSON was written before qualitative reviews; architecture section is outdated |
| 10 | Prior epistemic failures addressed? | Detected and documented. New failures discovered (Jaccard methodology, skipped checkpoints). | PARTIAL | Addressed some old failures, introduced new ones. Net: better awareness but imperfect execution. |

## Implications (revised)

- **Recommendation engine architecture:** Implement two named views (MiniLM + TF-IDF), not three. SPECTER2 dropped from default per W5.4 qualitative review. View switching or tab-based display with labels: "Similar Ideas" and "Wider Field."

- **MCP tool design:** The `recommend` tool should accept a `view` parameter. Consider fusion as a per-profile option (not default) based on W3 finding that it helps narrow topics.

- **Embedding storage:** Use float16 for all stored embeddings. Compute in float32. This halves storage with zero quality impact. (HIGH confidence — direct measurement, not proxy.)

- **API embedding question is open:** Voyage screening was methodologically insufficient. Do not commit to "local-only" architecture until Spike 004 provides proper evaluation. Design the embedding layer to be model-agnostic.

- **Cold-start UX:** MiniLM works from 1 seed, but the system should detect seed homogeneity and prompt for diverse seeds. TF-IDF view should not be offered until 3+ seeds. Show "add different kinds of papers for better results" rather than just "add more."

- **Scale planning:** TF-IDF needs attention above 10K papers (measured). MiniLM robust to 19K (measured), synthetic 50K (-7.5%, medium confidence due to synthetic data).

- **Retrieval pattern:** Centroid top-K as default. kNN-per-seed is not universally catastrophic — consider offering for dense topic profiles. MMR is marginal — not worth the complexity for v1.

- **Negative signals:** Do not implement in v1. No evidence of benefit.

---

## 8. Epistemic Qualifications

This section distinguishes three levels of confidence for each finding, following the principle that a finding's reliability depends on what question you're asking about it.

### Testing conditions

All findings (except Voyage screening) were produced under these conditions:

| Dimension | Value | Implication |
|-----------|-------|-------------|
| **Corpus** | 19,252 arXiv papers from OAI-PMH harvest | Not a "sample" — this is the full harvest for configured categories |
| **Domain** | CS/ML-dominated (77% in top 15 CS categories, 130 total categories) | Findings are about CS/ML academic papers specifically |
| **Temporal** | 57% Jan 2026, 34% 2025, 9% older (updates/revisions) | Very recent papers; citation maturity is low |
| **Language** | ~97% English (646 possibly non-English) | English-language findings only |
| **Interest profiles** | 8 CS/ML topics, constructed from MiniLM-based BERTopic clustering | "Relevant" is defined through MiniLM's representation |
| **Evaluation** | LOO-MRR (primary), 6 other instruments, AI qualitative review | LOO-MRR is entangled with MiniLM; qualitative review partially independent |
| **Scale** | 19,252 papers; scale tests used synthetic duplication to 50K | Quality-at-scale findings limited by synthetic data |

### Three-level confidence framework

**Level 1 — Measurement:** Did the instrument accurately detect what it detects?

These findings are about the measurements themselves. They are reproducible and accurate for what they measure. The question is not whether the numbers are right, but what the numbers mean (Level 2).

| Finding | Measurement confidence | Note |
|---------|----------------------|------|
| MiniLM MRR = 0.398 on this corpus with these profiles | HIGH | Reproducible; code and data exist |
| TF-IDF MRR = 0.104 | HIGH | Same |
| TF-IDF held-out recovery = 5/15 vs MiniLM 2/15 | HIGH | Direct count, not proxy |
| Fusion RRF MRR = 0.279 (vs 0.398 standalone) | HIGH | Same evaluation framework |
| SPECTER2 score spread = 0.009 | HIGH | Direct measurement |
| float16 zero quality loss | HIGH | Same evaluation framework, paired comparison |
| Cold-start MiniLM coverage 0.366 at 1 seed | HIGH | Same |
| Voyage Jaccard 0.717 with MiniLM | MEDIUM | Measured on 100-paper pool; would differ on full corpus |
| kNN aggregate MRR = 0.149 (-58%) | HIGH | Full corpus, 24 configurations |

**Level 2 — Interpretation:** What do the measurements mean for strategy characterization and architecture decisions?

This is where the evaluation framework entanglement matters. MRR 0.398 vs 0.104 is an accurate measurement, but interpreting it as "MiniLM is 4x better than TF-IDF" goes beyond what the measurement supports, because the ground truth is defined by MiniLM's representation.

| Interpretation | Confidence | Conditions for this interpretation to hold |
|---------------|-----------|-------------------------------------------|
| "MiniLM is the best single strategy" | MEDIUM | Holds if MiniLM-defined clusters are a reasonable approximation of relevance. Qualitative review shows the gap is smaller than MRR suggests (~80% on-topic for all strategies). Holds for CS/ML papers where semantic similarity aligns with research relevance. |
| "TF-IDF and MiniLM are complementary" | HIGH | Model-independent finding: TF-IDF uses a fundamentally different signal (vocabulary match vs semantic similarity). Confirmed by both quantitative overlap (Jaccard 0.179) and qualitative review (different papers recovered). Likely holds across domains. |
| "SPECTER2 is redundant with MiniLM" | MEDIUM-HIGH | Holds for CS/ML where vocabulary similarity and citation-community structure largely overlap. May NOT hold for interdisciplinary domains (e.g., computational biology, digital humanities) where citation communities diverge from vocabulary similarity. Based on W5.4 qualitative review across 3 profiles — not all 8. |
| "Fusion degrades quality" | MEDIUM | Holds as a default on aggregate. W3 qualitative found it helps narrow technical topics (P8). The truth is profile-dependent: fusion helps when constituent strategies have complementary blind spots for the specific topic. |
| "Centroid is the correct retrieval method" | MEDIUM-HIGH | Holds for the "general recommendation" use case. kNN has a niche for dense topics (P4). Based on quantitative + qualitative across 8 profiles. |
| "Cold start works from 1 seed" | MEDIUM | Measurement is accurate (coverage 0.366). Interpretation depends on what "works" means: W4.1 qualitative found echo chambers for broad topics and that seed quality matters more than count. "Works" is an overstatement; "produces results" is more accurate. |
| "Voyage adds no new signal" | LOW | Screening methodology was insufficient (100-paper pool, Jaccard only, 2/8 profiles, no qualitative review). Cannot draw this conclusion from available evidence. |
| "kNN is catastrophic" | LOW | Aggregate hides profile-dependence. Works for dense topics. The aggregate -58% MRR is an accurate measurement; "catastrophic" is an overinterpretation. |

**Level 3 — Extrapolation:** Do findings hold beyond the specific testing conditions?

| Target extrapolation | Confidence | Reasoning |
|---------------------|-----------|-----------|
| Same domain (CS/ML), similar corpus size, recent papers | MEDIUM-HIGH | Testing conditions match. Strategy characterizations likely stable. Specific MRR numbers will vary but relative rankings likely hold. |
| Same domain, larger corpus (50K-200K) | MEDIUM for MiniLM, LOW for TF-IDF | MiniLM robustness measured (synthetic, -7.5%). TF-IDF collapse measured (synthetic, -54%). Synthetic scaling doesn't capture real vocabulary growth effects. |
| Same domain, corpus with mature citations (>1 year old) | LOW-MEDIUM | Citation-based strategies (FWCI, bibliographic coupling) were non-functional here due to paper recency. On a mature corpus, they might change the strategy landscape substantially. SPECTER2's citation-graph signal might also differentiate more from MiniLM. |
| Non-CS arXiv domains (physics, math, biology) | LOW | Different vocabulary density, community structure, and citation patterns. MiniLM's advantage may not hold where the embedding space doesn't align well with disciplinary relevance. TF-IDF's keyword precision may be more or less valuable depending on vocabulary distinctiveness. |
| Non-arXiv academic literature | LOW | Different metadata structure, different full-text availability, different community norms. Strategy characterizations are arXiv-specific. |
| Non-English academic literature | VERY LOW | MiniLM and TF-IDF are English-focused. Findings don't transfer. |
| Human relevance judgments (vs AI-defined) | UNKNOWN | All quality assessments are AI-generated or mathematical proxy. The qualitative reviews are informative but may have systematic biases. Whether human researchers would agree with the strategy characterizations is an open question. |

### What the qualitative reviews changed

The three-level framework was not applied in the initial DECISION.md. Qualitative reviews, when finally performed, changed the interpretation of multiple findings:

| Finding | Quantitative-only interpretation | After qualitative review |
|---------|--------------------------------|------------------------|
| SPECTER2 value | Unique cross-community signal, include as third view | Redundant with MiniLM, drop from default |
| Fusion quality | Universally degrades MiniLM | Profile-dependent: helps narrow topics |
| kNN viability | Catastrophic, never use | Niche for dense topics |
| Cold start from 1 seed | Works (coverage 0.366) | Produces results but echo chambers for broad topics; seed quality > quantity |
| MiniLM dominance | 4x better than TF-IDF by MRR | ~80% on-topic for all strategies; gap is smaller than MRR suggests |

This pattern — quantitative metrics producing one verdict, qualitative review producing a different one — is not a flaw in the metrics. The metrics accurately detect what they detect. The error is in treating detection as evaluation: in assuming that what the instrument reads is what the phenomenon means. The qualitative reviews provide the interpretive context that connects instrument readings to situated understanding.

---

## 9. Methodological Limitations and Failures

This section documents where the experimental methodology fell short, both as honest qualification of this spike's findings and as input for improving future spike design.

### 9.1 Evaluation framework entanglement

**The problem:** The entire evaluation pipeline is built on MiniLM's representation of the corpus.

```
MiniLM embeddings
    → BERTopic topic model
        → Interest profile construction (which papers are "on-topic")
            → Seed paper selection
                → Held-out paper selection
                    → LOO-MRR ground truth
```

Every stage inherits MiniLM's biases. A paper that MiniLM embeds poorly will not appear in any interest profile. A strategy that finds papers MiniLM wouldn't cluster together is penalized by LOO-MRR even if those papers are genuinely relevant.

**What this affects:** All cross-family strategy comparisons (MiniLM vs TF-IDF vs SPECTER2). Within-family comparisons (MiniLM float32 vs float16, different K values) are unaffected.

**What partially corrects it:** Qualitative review, which assesses relevance from titles and abstracts rather than cluster membership. Held-out recovery, which measures "did the strategy find this paper at all?" rather than "where did it rank?" But qualitative review was AI-generated, and held-out papers were themselves selected from MiniLM clusters.

**What would fully resolve it:** Model-independent ground truth — either human relevance judgments or evaluation clusters derived from metadata (categories, citation links) rather than any embedding model.

### 9.2 Voyage screening methodology failure

**The problem:** The Voyage embedding screening used a 100-paper pool with top-K Jaccard as the sole metric. Five specific failures documented in `sig-2026-03-20-jaccard-screening-methodology`:
1. Pool size (100) inflated agreement (20% selectivity vs 0.1% real-world)
2. Only 2 of 8 profiles tested
3. No qualitative review of divergent papers
4. Jaccard collapses nature of divergence into one number
5. Baseline (MiniLM-SPECTER2) later shown to be invalid

**What this affects:** The Voyage verdict specifically. The conclusion "no API embeddings needed" is unsupported.

**What would fix it:** Spike 004 with representative 2000-paper sample, multiple metrics (rank correlation, semantic clustering, score distribution), qualitative review, all 8 profiles.

### 9.3 Skipped qualitative review checkpoints

**The problem:** The DESIGN.md prescribed four qualitative review checkpoints (W1, W3, W4.1, W5.4). Only W1 was performed in the initial session. The initial DECISION.md was written with conclusions based on quantitative metrics alone.

**What this affects:** Every conclusion that qualitative review later revised (SPECTER2, fusion, kNN, cold start). The initial DECISION.md's confidence levels were overstated.

**Root cause:** The qualitative reviews were treated as optional validation rather than mandatory methodology. The spike execution framework has no mechanism to enforce prescribed checkpoints before synthesis.

**Lesson for future spikes:** Qualitative review is not a validation step — it is a first-class evaluation method that produces knowledge quantitative metrics cannot. Skipping it doesn't just reduce confidence; it produces materially wrong conclusions. Future spike designs should mark qualitative checkpoints as blocking gates, not optional.

### 9.4 Extension experiment design quality

**The problem:** The core DESIGN.md (W0-W5) was meticulously designed with epistemic hazards, bias mitigations, and evaluation framework reflection. Extension experiments (Voyage screening, kNN/MMR, BM25 gap-fill, cross-encoder gap-fill) were designed ad-hoc without the same rigor. The Voyage screening in particular had no pre-registered sample size justification, no metric limitation analysis, and no qualitative review requirement.

**Pattern:** When a spike grows beyond its original scope, the additional experiments inherit the spike's authority (appearing in FINDINGS.md alongside rigorously designed experiments) without inheriting its methodology. The reader cannot distinguish between a finding backed by 24 observations across 8 profiles with qualitative review and a finding backed by 10 observations on a 100-paper sample with Jaccard only.

**Lesson for future spikes:** Extension experiments should go through the same design review as core experiments, or be explicitly marked as "screening quality" rather than "profiling quality" findings.

### 9.5 Confidence level framework

**The problem:** The initial DECISION.md used blanket HIGH/MEDIUM/LOW confidence levels that collapsed measurement accuracy, interpretation validity, and extrapolation reliability into one word. "HIGH confidence that MiniLM is the best strategy" could mean "we measured it accurately" (true), "the measurement means what we think" (partially true), or "this holds in other domains" (unknown).

**Lesson for future spikes:** Every finding should be qualified along three dimensions: measurement confidence (did the instrument work?), interpretation confidence (does the reading mean what we say?), and extrapolation confidence (does it hold elsewhere?). The conditions under which each level of confidence holds should be explicit.

---

## Metadata

**Spike duration:** W0-W5b across three sessions (initial execution, gap-fills, qualitative review completion)
**Iterations:** 2 (core + qualitative review completion and epistemic revision)
**Originating phase:** Phase 6 planning (deployment-portability deliberation)
**Strategies profiled:** 21 (8 content, 2 API embedding, 2 alternative retrieval patterns, 10 metadata, 2 graph, 4 baselines, 2 cross-encoder pipelines)
**Strategies eliminated:** 9 with measured cause (was 10 — Voyage verdict changed to inconclusive)
**Qualitative reviews:** 21 total (9 W1 characterization + 3 W3 blind comparison + 3 W4.1 cold start + 3 W5.4 parallel views + 3 extensions kNN/MMR)
**Signals logged:** 2 (`sig-2026-03-20-jaccard-screening-methodology`, `sig-2026-03-20-spike-experimental-design-rigor`)
**Data assets produced:** strategy_profiles.json (needs revision), 16 wave data files, 21 qualitative review documents
**Open questions deferred to Spike 004:** Voyage proper evaluation, local model screening, better evaluation metrics
