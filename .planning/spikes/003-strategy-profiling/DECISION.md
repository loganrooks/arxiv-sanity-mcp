# Spike Decision: Comprehensive Strategy Profiling

**Completed:** 2026-03-20
**Question:** What are the complete quality, resource, and behavioral profiles of every viable recommendation/filtering strategy?
**Answer:** Three viable content strategies (MiniLM, TF-IDF, SPECTER2) capture complementary quality dimensions that cannot be fused. The correct architecture is parallel views with MiniLM as primary. API embedding models (Voyage AI) add no new signal axis. Centroid retrieval is the correct default within each view.

## Summary

Spike 003 profiled 17+ strategies across 7 waves using 6 quantitative instruments, 9 qualitative reviews, and 4 context sensitivity dimensions on a 19,252-paper arXiv corpus. Three content-based strategies survived: MiniLM centroid (S1a) as the primary recommendation engine, TF-IDF cosine (S1d) as a keyword-precision alternative view, and SPECTER2 proximity adapter (S1c) as a cross-community discovery view. Four strategies were eliminated with measured cause (SVM, title-only variants, raw centroid). Metadata strategies function as pre-filters and boosters, not rankers. Graph strategies are algorithmically valid but data-limited at current enrichment coverage.

The most significant finding is that fusion fails: all tested combination methods (RRF, weighted linear, pipeline, cross-encoder reranking) either degrade MiniLM's quality or converge to MiniLM standalone. The three strategies ARE complementary -- they find different papers (Jaccard 0.179) and TF-IDF recovers held-out papers MiniLM misses (5/15 vs 2/15) -- but their quality dimensions are incommensurable. The correct architecture is parallel views: each strategy presented as a named perspective on the recommendation space.

W5 experiments closed two remaining open questions: (1) whether API embedding models (Voyage AI) capture a distinct signal from local models, and (2) whether alternative retrieval patterns (per-seed kNN, MMR) improve on centroid top-K. Both answers are negative. Voyage embeddings sit in the overlap zone between MiniLM and SPECTER2 (Jaccard 0.717-0.772), adding no new signal axis. kNN-per-seed catastrophically degrades retrieval (-58% MRR). MMR provides marginal diversity improvement (+6.6%) at near-zero quality cost (-2.8% MRR) but does not change the architecture.

A secondary but important finding is that the LOO-MRR evaluation framework is circularly biased toward MiniLM (clusters defined by MiniLM embeddings). TF-IDF is systematically underrated by quantitative metrics. This bias was detected through qualitative review and held-out recovery analysis, demonstrating the value of multi-instrument evaluation.

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
| Voyage AI (voyage-4, voyage-4-large) | Partial overlap with local models (Jaccard 0.717-0.772); no new signal axis |
| kNN-per-seed retrieval | -58% MRR; incoherent diversity; centroid superior |

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

Verdict: Voyage embeddings (1024-dim, API-dependent) sit in the overlap zone between MiniLM and SPECTER2. They do not capture a genuinely different signal (would need Jaccard < 0.6 with both local models). Not worth the API dependency.

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

**Chosen approach:** Parallel views architecture with MiniLM (S1a) as primary view, TF-IDF (S1d) as keyword-precision secondary view, and SPECTER2 (S1c) as optional cross-community discovery view. Centroid top-K retrieval within each view. No API embedding dependencies.

**Rationale:** This is the only architecture that preserves the complementarity between strategies without degrading any individual strategy. Every tested fusion method loses information. The parallel views approach:

1. Preserves MiniLM's 0.398 MRR (fusion would drop it to 0.279-0.310; cross-encoder reranking drops to 0.058-0.117)
2. Preserves TF-IDF's held-out recovery advantage (5/15, lost in fusion)
3. Preserves SPECTER2's unique cross-community discoveries (lost in all pipelines)
4. Gives users agency to browse the perspective most relevant to their current need

The cross-encoder gap fill strengthens this decision. Even switching to a fundamentally different reranking architecture (cross-attention vs embedding similarity) does not rescue the pipeline approach. The two reranker types produce opposite failure modes: MiniLM reranking converges to S1a (no benefit); cross-encoder reranking diverges from S1a (catastrophic loss). There is no middle ground with available models.

The Voyage AI screening confirms that adding API embedding models would not create a new signal axis. Voyage embeddings overlap both local models at Jaccard 0.717-0.772, sitting in the space between MiniLM and SPECTER2 rather than capturing a distinct perspective. This validates the local-only model architecture.

The kNN/MMR experiments confirm that centroid retrieval is the correct default. kNN-per-seed's -58% MRR loss shows that centroid averaging correctly captures the intersection of seed interests rather than "washing out" distinctive seeds. MMR's marginal diversity gain (+6.6%) does not justify architectural complexity. Cross-view switching provides far more meaningful diversity than intra-view retrieval tricks.

**Confidence:** HIGH for the parallel views architecture. HIGH for "no API embeddings needed" (empirical screening, clear thresholds). HIGH for "centroid is correct default" (24-config comparison). MEDIUM for specific strategy characterizations (limited by circular evaluation bias and single-month data).

## Success Criteria Assessment

| # | Question | Answer | Grounded? |
|---|----------|--------|-----------|
| 1 | Quality profiles of each viable strategy? | 3 viable + 10 eliminated + 4 data-limited, all with profile cards | YES: 24 observations per strategy, 8 profiles, 7 instruments |
| 2 | Which complement, which are redundant? | S1a/S1d/S1c complement (Jaccard 0.179). S1i/S1j redundant with S1d/S1a. Voyage redundant with MiniLM+SPECTER2. | YES: pairwise overlap measured, qualitative review confirms, Voyage screening confirms |
| 3 | Minimum viable config? | S1a (MiniLM) with 3+ seeds, K=20, float16 storage | YES: cold-start curve shows 3-seed coverage 0.567, above useful threshold |
| 4 | Recommended config and cost? | S1a primary + S1d secondary. 14.1 MB storage, 33s GPU one-time, 2.2s TF-IDF build. | YES: resource measurements from profiling |
| 5 | Maximum quality config? | All three views (S1a + S1d + S1c). Adds 28.3 MB + 463s GPU for SPECTER2. | YES: resource measurements from profiling |
| 6 | Cold start curve? | MiniLM: 1 seed functional, 5 saturated. TF-IDF: 5 seed minimum. | YES: 5-point curve per strategy |
| 7 | Narrow vs broad behavior? | MiniLM improves with breadth (+52%). TF-IDF degrades (-27%). | YES: 3 breadth levels measured |
| 8 | SPECTER2 adapter impact? | Adapter loaded correctly. MRR 0.184 with score compression 0.009. Prior findings confirmed: different signal, cannot rank standalone. | YES: W0 verified adapter output, W1 profiled |
| 9 | Installer-consumable data? | strategy_profiles.json with full profile cards, context recommendations, resource requirements | YES: structured JSON produced |
| 10 | Prior epistemic failures addressed? | Circular eval bias detected and documented. SPECTER2 adapter fixed. Synthetic scale caveat acknowledged. Cross-encoder gap filled. Voyage API screened. Strategy patterns tested. | PARTIAL: detected and documented but not fully resolved (would need model-independent ground truth) |

## Implications

- **Recommendation engine architecture:** Implement three named views rather than a single fused ranking. This is a departure from the "best single strategy" model assumed in earlier planning.

- **UI design:** The frontend must support view switching or tab-based display of recommendations. Each view should be labeled with its character: "Similar papers," "Keyword matches," "Related communities."

- **MCP tool design:** The `recommend` tool should accept a `view` parameter (or return all three views with labels). The tool response should include which view(s) produced each paper.

- **Embedding storage:** Use float16 for all stored embeddings. Compute in float32. This halves storage with zero quality impact.

- **No API embedding dependencies:** The system should use only local models (MiniLM, SPECTER2, TF-IDF). Voyage AI screening showed API embeddings add no new signal axis. This simplifies deployment (no API keys required) and removes a runtime dependency.

- **Cold-start UX:** The system should work with a single seed paper (MiniLM provides coverage 0.366). Show a "add more seeds for better results" prompt until 5 seeds are reached (saturation point).

- **Scale planning:** TF-IDF will need attention above 10K papers. Options: vocabulary pruning, pre-filtered TF-IDF on category subsets, or accept degradation with a user-facing caveat. MiniLM scales without intervention.

- **Graph strategy potential:** Bibliographic coupling is algorithmically valid (discrimination 0.467) but needs enrichment expansion from 95 to ~2000+ papers. This is a future enrichment pipeline task, not a strategy architecture task.

- **Retrieval pattern:** Centroid top-K is the correct default. MMR could be offered as an optional "diverse results" toggle but the benefit is marginal. Do not implement kNN-per-seed.

- **Negative signals:** Do not implement in v1. No evidence of benefit; risk of degrading small profiles.

- **Cross-encoder reranking:** Not viable with available checkpoints. A domain-specific cross-encoder (trained on academic paper relatedness) would be needed, requiring labeled training data and fine-tuning infrastructure. This is a potential Phase 7+ investigation if multi-stage pipelines become a priority, but there is no low-hanging fruit here.

## Metadata

**Spike duration:** W0-W5b in two sessions
**Iterations:** 1
**Originating phase:** Phase 6 planning (deployment-portability deliberation)
**Strategies profiled:** 21 (8 content, 2 API embedding, 2 alternative retrieval patterns, 10 metadata, 2 graph, 4 baselines, 2 cross-encoder pipelines)
**Strategies eliminated:** 10 (with measured cause)
**Data assets produced:** strategy_profiles.json (installer-consumable), 14 wave data files
