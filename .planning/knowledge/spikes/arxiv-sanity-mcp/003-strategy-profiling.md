---
id: spk-2026-03-20-strategy-profiling
type: spike
project: arxiv-sanity-mcp
tags: [recommendation-strategies, MiniLM, SPECTER2, TF-IDF, parallel-views, fusion, evaluation-bias, cold-start, context-sensitivity]
created: 2026-03-20T12:00:00Z
updated: 2026-03-20T12:00:00Z
durability: convention
status: active
hypothesis: "Individual strategy quality profiles, combination effects, and context-sensitive behavior can be measured to produce installer-consumable recommendations"
outcome: confirmed
rounds: 1
runtime: claude-code
model: claude-opus-4-6
gsd_version: unknown
---

## Hypothesis

Complete quality, resource, and behavioral profiles of every viable recommendation strategy -- individually, in combination, and across user contexts -- can be measured and structured so that an installer or configuration wizard can make informed recommendations.

## Experiment

Profiled 17 strategies (6 content, 10 metadata, 2 graph, 4 baselines) on a 19,252-paper arXiv corpus using 6 quantitative instruments (LOO-MRR, seed proximity, topical coherence, cluster diversity, novelty, category surprise, coverage) across 8 interest profiles with 3 seed selections each. Conducted 9 qualitative AI reviews. Tested 7+ fusion variants, 5 pipeline architectures, and measured context sensitivity across cold-start, breadth, and scale dimensions.

## Results

Three content strategies survived as viable: MiniLM centroid (S1a, MRR 0.398), TF-IDF cosine (S1d, MRR 0.104 but 5/15 held-out recovery), and SPECTER2 adapter (S1c, MRR 0.184 with cross-community discovery). All fusion methods degrade MiniLM (best combo MRR 0.310 vs 0.398 standalone). Strategies are complementary (Jaccard 0.179, 9 unique recoveries) but incommensurable. LOO-MRR evaluation is circularly biased toward MiniLM. Cold start: MiniLM works from 1 seed, saturates at 5. Scale: MiniLM robust (-7.5% at 50K), TF-IDF collapses (-54%). float16 is free lunch (zero quality loss, 50% storage). int8 fails for SPECTER2.

## Decision

Parallel views architecture: MiniLM as primary view ("Similar papers"), TF-IDF as secondary view ("Keyword matches"), SPECTER2 as optional discovery view ("Related communities"). No fusion. Each view retains its own ranking and quality characteristics. Installer recommends views based on context: cold start -> MiniLM only; 5+ seeds -> MiniLM + TF-IDF; discovery mode -> all three.

## Consequences

- Recommendation engine must support multiple concurrent views, not a single fused ranking
- MCP `recommend` tool needs a `view` parameter or returns labeled multi-view results
- float16 storage is the default; float32 only for computation
- Cold-start UX: system works at 1 seed, prompts for 5
- TF-IDF needs attention above 10K papers (scale degradation)
- Graph strategies deferred pending enrichment expansion (95 -> 2000+ papers)
- Evaluation framework needs model-independent ground truth to remove circular bias
- Negative signals: do not implement in v1
