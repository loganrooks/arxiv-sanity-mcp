---
id: spk-2026-03-20-w1c-gap-openalex-enrichment
type: spike
project: arxiv-sanity-mcp
tags: [bibliographic-coupling, openalex, graph-strategies, reference-data, api-enrichment, related-works]
created: 2026-03-20T07:00:00Z
updated: 2026-03-20T07:00:00Z
durability: convention
status: active
hypothesis: "Bibliographic coupling (S3a) becomes viable with expanded OpenAlex enrichment, and related_works (S3c) becomes functional"
outcome: rejected
rounds: 1
runtime: claude-code
model: claude-opus-4-6[1m]
gsd_version: 1.17.5+dev
---

## Hypothesis

S3a (bibliographic coupling via Jaccard similarity of reference sets) is algorithm-valid but data-limited. Expanding OpenAlex enrichment from 500 to ~4,700 papers should provide enough reference data to produce a competitive recommendation signal. S3c (OpenAlex related_works) should become functional once papers are enriched.

## Experiment

Enriched 944 papers (of 4,603 target) via OpenAlex title search API before hitting daily rate limit. Merged with existing 500-paper B2 cache for 1,444 total entries. Papers with referenced_works increased from 95 to 307 (3.2x). Seed coverage improved from 1/120 to 11/120 with refs. Re-profiled S3a and S3c using the Spike 003 profiling harness across 8 interest profiles. Ran focused intra/inter-group coupling evaluation on 307 papers across 27 topic groups.

## Results

S3a expanded LOO MRR: 0.019 (vs MiniLM 0.398, SPECTER2 0.184). Seed proximity: 0.355 (vs 0.764). Coverage: 0.021 (vs 0.686). The focused evaluation shows valid discrimination (78% of 27 groups positive) but mean discrimination dropped from 0.467 (5 groups, small-sample) to 0.081 (27 groups, more robust). The structural ~19% referenced_works availability rate for recent papers caps coverage potential regardless of enrichment effort. S3c became technically functional (467 papers with related_works) but produces zero signal -- related_works IDs don't map to papers in our corpus (LOO MRR 0.000, coverage 0.000).

## Decision

S3a classified as supplementary signal only, not standalone strategy. S3c dropped as non-functional. No further OpenAlex enrichment expansion needed for strategy profiling. The algorithm works but cannot compete with embedding-based strategies for recent arXiv papers due to structural reference coverage limits (~19%).

## Consequences

- S3a retained in strategy catalog as "data-limited, supplementary" -- not promoted to any viable standalone tier
- S3c excluded from all configurations
- W1C's original 0.467 discrimination finding was small-sample inflated; true value is ~0.081
- OpenAlex enrichment pipeline is reusable for future citation-data needs (FWCI ranking, etc.)
- Combination testing (W3) may include S3a as weak supplement but expectations are low
- The ~19% ref rate for 2022-2026 papers is a structural limit of OpenAlex indexing speed, not fixable by more API calls
