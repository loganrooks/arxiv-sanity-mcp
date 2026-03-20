# Spike Decision: Comprehensive Strategy Profiling

**Completed:** 2026-03-20
**Question:** What are the complete quality, resource, and behavioral profiles of every viable recommendation/filtering strategy?
**Answer:** Three viable content strategies (MiniLM, TF-IDF, SPECTER2) capture complementary quality dimensions that cannot be fused. The correct architecture is parallel views with MiniLM as primary.

## Summary

Spike 003 profiled 17 strategies across 5 waves using 6 quantitative instruments, 9 qualitative reviews, and 4 context sensitivity dimensions on a 19,252-paper arXiv corpus. Three content-based strategies survived: MiniLM centroid (S1a) as the primary recommendation engine, TF-IDF cosine (S1d) as a keyword-precision alternative view, and SPECTER2 proximity adapter (S1c) as a cross-community discovery view. Four strategies were eliminated with measured cause (SVM, title-only variants, raw centroid). Metadata strategies function as pre-filters and boosters, not rankers. Graph strategies are algorithmically valid but data-limited at current enrichment coverage.

The most significant finding is that fusion fails: all tested combination methods (RRF, weighted linear, pipeline) either degrade MiniLM's quality or converge to MiniLM standalone. The three strategies ARE complementary -- they find different papers (Jaccard 0.179) and TF-IDF recovers held-out papers MiniLM misses (5/15 vs 2/15) -- but their quality dimensions are incommensurable. The correct architecture is parallel views: each strategy presented as a named perspective on the recommendation space.

A secondary but important finding is that the LOO-MRR evaluation framework is circularly biased toward MiniLM (clusters defined by MiniLM embeddings). TF-IDF is systematically underrated by quantitative metrics. This bias was detected through qualitative review and held-out recovery analysis, demonstrating the value of multi-instrument evaluation.

## Findings

Detailed findings with all measurements are in FINDINGS.md. Key numbers below.

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

### Combination Results

| Method | Best MRR | vs S1a Alone |
|--------|----------|-------------|
| RRF (MiniLM + TF-IDF) | 0.279 | -30% |
| Weighted (0.7/0.3) | 0.310 | -22% |
| Pipeline (cat -> MiniLM) | 0.398 | 0% (identical) |

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
| Parallel views (MiniLM primary) | Maximum information; no quality loss; user chooses perspective | More complex UI; user must understand views | Complementarity confirmed (Jaccard 0.179, 9 unique recoveries) |
| TF-IDF primary | Best held-out recovery (5/15); widest score spread | Collapses at scale (-54%); degrades with breadth | Context sensitivity data rules this out for general use |
| All three views | Maximum coverage; discovery mode | SPECTER2 cannot rank standalone; needs secondary ranking signal | Score compression (0.009) confirmed |

## Decision

**Chosen approach:** Parallel views architecture with MiniLM (S1a) as primary view, TF-IDF (S1d) as keyword-precision secondary view, and SPECTER2 (S1c) as optional cross-community discovery view.

**Rationale:** This is the only architecture that preserves the complementarity between strategies without degrading any individual strategy. Every tested fusion method loses information. The parallel views approach:

1. Preserves MiniLM's 0.398 MRR (fusion would drop it to 0.279-0.310)
2. Preserves TF-IDF's held-out recovery advantage (5/15, lost in fusion)
3. Preserves SPECTER2's unique cross-community discoveries (lost in all pipelines)
4. Gives users agency to browse the perspective most relevant to their current need

**Confidence:** HIGH for the parallel views architecture. MEDIUM for specific strategy characterizations (limited by circular evaluation bias and single-month data).

## Success Criteria Assessment

| # | Question | Answer | Grounded? |
|---|----------|--------|-----------|
| 1 | Quality profiles of each viable strategy? | 3 viable + 7 eliminated + 4 data-limited, all with profile cards | YES: 24 observations per strategy, 8 profiles, 7 instruments |
| 2 | Which complement, which are redundant? | S1a/S1d/S1c complement (Jaccard 0.179). S1i/S1j redundant with S1d/S1a. | YES: pairwise overlap measured, qualitative review confirms |
| 3 | Minimum viable config? | S1a (MiniLM) with 3+ seeds, K=20, float16 storage | YES: cold-start curve shows 3-seed coverage 0.567, above useful threshold |
| 4 | Recommended config and cost? | S1a primary + S1d secondary. 14.1 MB storage, 33s GPU one-time, 2.2s TF-IDF build. | YES: resource measurements from profiling |
| 5 | Maximum quality config? | All three views (S1a + S1d + S1c). Adds 28.3 MB + 463s GPU for SPECTER2. | YES: resource measurements from profiling |
| 6 | Cold start curve? | MiniLM: 1 seed functional, 5 saturated. TF-IDF: 5 seed minimum. | YES: 5-point curve per strategy |
| 7 | Narrow vs broad behavior? | MiniLM improves with breadth (+52%). TF-IDF degrades (-27%). | YES: 3 breadth levels measured |
| 8 | SPECTER2 adapter impact? | Adapter loaded correctly. MRR 0.184 with score compression 0.009. Prior findings confirmed: different signal, cannot rank standalone. | YES: W0 verified adapter output, W1 profiled |
| 9 | Installer-consumable data? | strategy_profiles.json with full profile cards, context recommendations, resource requirements | YES: structured JSON produced |
| 10 | Prior epistemic failures addressed? | Circular eval bias detected and documented. SPECTER2 adapter fixed. Synthetic scale caveat acknowledged. | PARTIAL: detected and documented but not fully resolved (would need model-independent ground truth) |

## Implications

- **Recommendation engine architecture:** Implement three named views rather than a single fused ranking. This is a departure from the "best single strategy" model assumed in earlier planning.

- **UI design:** The frontend must support view switching or tab-based display of recommendations. Each view should be labeled with its character: "Similar papers," "Keyword matches," "Related communities."

- **MCP tool design:** The `recommend` tool should accept a `view` parameter (or return all three views with labels). The tool response should include which view(s) produced each paper.

- **Embedding storage:** Use float16 for all stored embeddings. Compute in float32. This halves storage with zero quality impact.

- **Cold-start UX:** The system should work with a single seed paper (MiniLM provides coverage 0.366). Show a "add more seeds for better results" prompt until 5 seeds are reached (saturation point).

- **Scale planning:** TF-IDF will need attention above 10K papers. Options: vocabulary pruning, pre-filtered TF-IDF on category subsets, or accept degradation with a user-facing caveat. MiniLM scales without intervention.

- **Graph strategy potential:** Bibliographic coupling is algorithmically valid (discrimination 0.467) but needs enrichment expansion from 95 to ~2000+ papers. This is a future enrichment pipeline task, not a strategy architecture task.

- **Negative signals:** Do not implement in v1. No evidence of benefit; risk of degrading small profiles.

## Metadata

**Spike duration:** W0-W5 in one session
**Iterations:** 1
**Originating phase:** Phase 6 planning (deployment-portability deliberation)
**Strategies profiled:** 17 (6 content, 10 metadata, 2 graph, 4 baselines)
**Strategies eliminated:** 7 (with measured cause)
**Data assets produced:** strategy_profiles.json (installer-consumable), 11 wave data files
