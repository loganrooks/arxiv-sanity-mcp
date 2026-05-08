---
date: 2026-03-30
status: reference
scope: complete map of tested vs untested strategy configurations
---

# Strategy Space Map

What has been tested, what hasn't, and what the codebase currently supports.

## Models tested

| Model | Dim | Tested in | Retrieval methods tested | Status |
|-------|-----|-----------|------------------------|--------|
| all-MiniLM-L6-v2 | 384 | Spike 002, 003, 004 | Centroid, kNN, MMR, cross-encoder | Provisional default |
| SPECTER2 + proximity adapter | 768 | Spike 003, 004 | Centroid only | Further investigation |
| TF-IDF (lexical) | sparse | Spike 003, 004 | Cosine centroid | Provisional secondary |
| Stella v5 400M | 1024 | Spike 004 | Centroid only | Further investigation |
| Qwen3-Embedding-0.6B | 1024 | Spike 004 | Centroid only | Further investigation |
| GTE-large-en-v1.5 | 1024 | Spike 004 | Centroid only | Further investigation |
| Voyage-4 (API) | 1024 | Spike 003 (screening), 004 | Centroid only | Inconclusive (API dependency) |

## Models not tested

OpenAI text-embedding-3-large, Cohere embed-v3, bge, e5, Jina, all-mpnet, fine-tuned variants of any model.

## Retrieval methods

| Method | Tested with | Result | Untested with |
|--------|------------|--------|---------------|
| Centroid cosine | All 7 models | Provisional default | — |
| kNN-per-seed | MiniLM only | Profile-dependent (-58% aggregate, works on dense topics) | SPECTER2, Stella, Qwen3, GTE, Voyage |
| MMR | MiniLM only | Marginal (+6.6% diversity, -2.8% quality) | All challengers |
| Cross-encoder rerank | MiniLM only (MS MARCO) | Eliminated (domain mismatch, -71 to -85%) | Domain-specific CE, all challengers |
| Fusion (RRF, weighted, pipeline) | MiniLM + TF-IDF only | All degrade aggregate; profile-dependent (helps narrow topics) | MiniLM + SPECTER2, MiniLM + GTE, three-way |

**Critical gap**: Model x retrieval method cross-product has one row filled. We know how MiniLM behaves under different retrieval methods but not how any challenger does.

## Evaluation methods used

| Method | Used in | What it constitutes |
|--------|---------|-------------------|
| Jaccard @K | Spikes 003, 004 | Binary overlap (seed-sensitive at K=20) |
| Kendall's tau | Spike 004 | Full ranking correlation (seed-stable) |
| LOO-MRR | Spike 003 | Held-out recovery (MiniLM-entangled) |
| Category recall | Spike 004 | Model-independent ground truth |
| Score distribution | Spike 004 | Model-internal discrimination |
| AI list-review | Spikes 003, 004 | Situated relevance (one standpoint) |
| Agent-based task evaluation | Never | Function-in-use |
| Human evaluation | Never | Researcher judgment |

## What the codebase implements (src/)

The production codebase implements lexical search ONLY:
- PostgreSQL tsvector full-text search (title + abstract + authors)
- Category filtering
- Date-based browsing
- 5-signal ranking pipeline (query_match, seed_relation, category_overlap, interest_profile_match, recency)
- Interest profiles with seed papers, followed authors, saved queries, negative examples

**NOT implemented in src/:**
- Dense embedding loading, storage, or search
- Any embedding model integration
- Vector similarity (centroid, kNN, MMR)
- Cross-encoder reranking
- Multi-model fusion
- Embedding-based recommendation

All embedding work exists only in spike experiment scripts (.planning/spikes/*/experiments/).

## Data assets (spike experiments)

| Asset | Location | Size |
|-------|----------|------|
| 2000-paper sample | `.planning/spikes/003.../experiments/data/sample_2000.json` | 3 MB |
| 8 interest profiles | `.planning/spikes/003.../experiments/data/interest_profiles.json` | 83 KB |
| MiniLM 19K embeddings | `.planning/spikes/002.../experiments/data/embeddings_19k.npy` | 29 MB |
| SPECTER2 19K embeddings | `.planning/spikes/003.../experiments/data/specter2_adapter_19k.npy` | 57 MB |
| All 2000-paper embeddings | `.planning/spikes/004.../experiments/data/{model}_2000.npy` | 3-8 MB each |
| Phase 2 metrics | `.planning/spikes/004.../experiments/checkpoints/phase2_metrics.json` | 4 MB |
| 40 qualitative reviews | `.planning/spikes/004.../experiments/reviews/` | ~1 MB total |
| Harvest DB (19K papers) | `.planning/spikes/001.../experiments/data/spike_001_harvest.db` | ~50 MB |
