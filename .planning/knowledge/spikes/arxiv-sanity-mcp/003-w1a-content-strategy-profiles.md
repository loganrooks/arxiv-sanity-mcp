---
id: spk-2026-03-19-003-w1a-content-strategy-profiles
type: spike
project: arxiv-sanity-mcp
tags: [recommendation-strategies, embeddings, MiniLM, SPECTER2, TF-IDF, SVM, content-based-filtering, centroid-similarity]
created: 2026-03-19T23:09:00Z
updated: 2026-03-19T23:09:00Z
durability: convention
status: active
hypothesis: "Content-based strategies differ meaningfully in quality profiles across interest profiles, with embedding-based strategies outperforming lexical strategies on recovery metrics."
outcome: confirmed
rounds: 1
runtime: claude-code
model: claude-opus-4-6
gsd_version: 1.17.5+dev
---

## Hypothesis

Content-based recommendation strategies (MiniLM embeddings, SPECTER2 adapter embeddings, TF-IDF cosine, SVM, embedding centroid) produce meaningfully different quality profiles across diverse interest profiles, and embedding-based strategies outperform lexical strategies on cluster recovery metrics.

## Experiment

Profiled 6 strategies across 8 interest profiles (RL for robotics, language model reasoning, quantum computing, AI safety, GNNs, diffusion models, federated learning, math foundations) with 3 seed subsets each (5, 10, 15 seeds). Evaluation harness computed 7 instruments (LOO-MRR, seed proximity, topical coherence, cluster diversity, novelty, category surprise, coverage) plus resource metrics (latency, storage). Corpus: 19,252 papers from January 2026 arXiv.

Strategies tested:
- S6a: Random baseline
- S1a: MiniLM (384-dim) embedding centroid, normalized
- S1c: SPECTER2 adapter (768-dim) embedding centroid
- S1d: TF-IDF cosine similarity (50K features)
- S1i: SVM on user library (LinearSVC, C=0.01, balanced)
- S1j: MiniLM centroid dot product (unnormalized, cheapest variant)

## Results

MiniLM (S1a) dominates all content strategies:
- MRR: S1a=0.398, S1c=0.184, S1d=0.104, S1i=0.103 (S1a wins every profile, 1.54x-4.21x over SPECTER2)
- Coverage: S1a=0.686, S1c=0.336, S1d=0.247, S1i=0.241
- Latency: all ~5-20ms per query; SVM is 192ms (trains per-query)

S1a and S1j produce mathematically identical rankings (centroid normalization is a no-op for L2-normalized embeddings).

TF-IDF and SVM are near-identical in quality (deltas < 0.02 on all instruments), but SVM is 10x slower.

Embedding strategies produce tighter recommendations (lower diversity, lower novelty) than TF-IDF strategies. This is a behavioral difference, not necessarily a quality difference.

## Decision

- S1a (MiniLM centroid) is the primary content strategy for the recommendation system.
- SPECTER2 adapter does not justify its 2x storage cost for substantially worse recovery metrics at the individual strategy level. Its value may emerge in combination strategies (tested in W3).
- SVM is eliminated -- no quality advantage over TF-IDF centroid at 10x the latency.
- S1j is eliminated as a distinct strategy -- identical to S1a.
- TF-IDF centroid (S1d) is the lexical fallback for environments without pre-computed embeddings.

## Consequences

- The recommendation system default should use MiniLM embeddings, not SPECTER2.
- SPECTER2 should be tested in combination with MiniLM (W3) before being included or excluded from the system.
- The SVM (arxiv-sanity-lite approach) does not add value at this corpus size (19K papers, 5-15 seeds).
- Profile-dependent quality variation (MRR ranges 0.282-0.505 for S1a) suggests interest breadth affects strategy performance -- to be investigated in W4.2.
