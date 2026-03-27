# API Embedding & LLM Reranking Cost-Feasibility Analysis

**Date:** 2026-03-20
**Context:** Spike 001/003 supplement -- evaluating whether API-based embedding or LLM reranking services offer quality or cost advantages over the local models already profiled (MiniLM 384-dim, SPECTER2 768-dim on GTX 1080 Ti + Xeon W-2125).

**Corpus:** 19,252 arXiv papers, average abstract ~157 words (~200 tokens each).

---

## 1. API Embedding Services -- Pricing & Specifications

All prices sourced March 2026. Prices change frequently; verify before committing.

### 1a. Pricing Table

| Service | Model | Dims | Max Tokens | Price/1M Tokens | Corpus Cost (3.85M tok) | Per-Query Cost | Free Tier |
|---------|-------|------|------------|-----------------|------------------------|----------------|-----------|
| OpenAI | text-embedding-3-small | 1,536 | 8,192 | $0.020 [1] | $0.08 | $0.000004 | None |
| OpenAI | text-embedding-3-large | 3,072 | 8,192 | $0.130 [1] | $0.50 | $0.000026 | None |
| Voyage AI | voyage-4 | 1,024 | 32,000 | $0.060 | $0.23 | $0.000012 | 200M tokens |
| Voyage AI | voyage-4-large | 1,024 | 32,000 | $0.120 | $0.46 | $0.000024 | 200M tokens |
| Voyage AI | voyage-3 | 1,024 | 32,000 | $0.060 | $0.23 | $0.000012 | None |
| Google | gemini-embedding-001 | 768-3,072 | 2,048 | $0.150 | $0.58 | $0.00003 | Free tier exists [2] |
| Google | gemini-embedding-2-preview | 768-3,072 | 8,192 | $0.200 | $0.77 | $0.00004 | Free tier exists [2] |
| Cohere | embed-english-v3.0 | 1,024 | 512 | ~$0.10 [3] | ~$0.39 | ~$0.00002 | Trial key free (rate-limited) |
| Cohere | embed-v4.0 | 256-1,536 | 128K | ~$0.10 [3] | ~$0.39 | ~$0.00002 | Trial key free (rate-limited) |

**Notes:**
- [1] OpenAI embedding pricing from Azure documentation cross-referenced with community sources. The $0.020/1M for text-embedding-3-small and $0.130/1M for text-embedding-3-large are well-established as of early 2025 and confirmed in Azure's published specifications. OpenAI's own pricing page blocked automated access for verification.
- [2] Google offers a free tier for Gemini API with rate limits; paid tier pricing as listed.
- [3] Cohere has moved to Model Vault (instance-based) pricing for Embed 4 ($4.00/hr). Legacy embed-v3 pricing is not prominently published. The trial API key is free for non-commercial use with rate limits. The $0.10/1M estimate is interpolated from legacy Command model pricing patterns and community reports; it may be lower.

### 1b. Corpus Embedding Cost Summary

**One-time cost to embed 19,252 papers (~3.85M tokens):**

| Service | Cheapest Model | Cost |
|---------|---------------|------|
| OpenAI text-embedding-3-small | $0.08 |
| Voyage AI voyage-4 | $0.23 (or FREE within 200M token allowance) |
| OpenAI text-embedding-3-large | $0.50 |
| Voyage AI voyage-4-large | $0.46 (or FREE within 200M token allowance) |
| Google gemini-embedding-001 | $0.58 |
| Cohere embed-v3 | ~$0.39 |

**The entire corpus fits within Voyage AI's free tier (3.85M tokens << 200M free tokens).** This means you could embed the full corpus with voyage-4-large at zero cost.

### 1c. Daily Update Cost (~600 new papers/day, ~120K tokens)

| Service | Model | Daily Cost | Monthly Cost | Annual Cost |
|---------|-------|-----------|-------------|------------|
| OpenAI | text-embedding-3-small | $0.002 | $0.07 | $0.88 |
| OpenAI | text-embedding-3-large | $0.016 | $0.47 | $5.69 |
| Voyage AI | voyage-4 | $0.007 | $0.22 | $2.63 |
| Voyage AI | voyage-4-large | $0.014 | $0.44 | $5.26 |
| Google | gemini-embedding-001 | $0.018 | $0.54 | $6.57 |

**Annual embedding cost for daily updates: $0.88-$6.57/year.** This is negligible.

---

## 2. LLM Reranking Cost (S4f)

### 2a. Model Pricing

| Service | Model | Input/1M Tokens | Output/1M Tokens | Source |
|---------|-------|----------------|-----------------|--------|
| Anthropic | Claude Sonnet 4.6 | $3.00 | $15.00 | Anthropic docs (March 2026) |
| Anthropic | Claude Haiku 4.5 | $1.00 | $5.00 | Anthropic docs (March 2026) |
| OpenAI | GPT-4o-mini | $0.15 [4] | $0.60 [4] | Community consensus pricing |
| Google | Gemini 2.5 Flash | $0.30 | $2.50 | Google AI pricing page |

**Note [4]:** GPT-4o-mini pricing was not directly confirmed from OpenAI's pricing page (403 error). The $0.15/$0.60 per 1M tokens is the widely reported pricing from multiple independent sources as of early 2025. Verify at https://openai.com/api/pricing/.

### 2b. Per-Pair and Per-Session Cost

**Per reranking pair:** ~500 input tokens (seed abstract + candidate abstract + prompt) + ~50 output tokens (score + explanation).

| Model | Cost/Pair | Cost/Query (20 pairs) | Cost/Session (5 queries, 100 pairs) |
|-------|-----------|----------------------|-------------------------------------|
| Claude Sonnet 4.6 | $0.0023 | $0.045 | $0.225 |
| Claude Haiku 4.5 | $0.0008 | $0.015 | $0.075 |
| GPT-4o-mini | $0.0001 | $0.002 | $0.011 |
| Gemini 2.5 Flash | $0.0003 | $0.005 | $0.028 |

**Calculation:** Cost/pair = (500 tokens * input_rate) + (50 tokens * output_rate).

### 2c. Annual Reranking Cost (assuming 1 session/day, 365 days)

| Model | Annual Cost |
|-------|------------|
| Claude Sonnet 4.6 | $82.13 |
| Claude Haiku 4.5 | $27.38 |
| GPT-4o-mini | $4.02 |
| Gemini 2.5 Flash | $10.22 |

### 2d. Reranking Assessment

GPT-4o-mini and Gemini Flash are the only models where reranking cost is genuinely low. Claude Sonnet at $82/year is non-trivial for a personal tool. The real question is whether LLM reranking adds enough quality over MiniLM centroid similarity (MRR 0.398) to justify any API dependency.

---

## 3. Quality Expectations

### 3a. MTEB Benchmark Scores (retrieval-relevant)

| Model | MTEB Avg | Dims | Type | Source |
|-------|----------|------|------|--------|
| gte-Qwen2-7B-instruct | 70.24 | 3,584 | Open-source (7B params) | HuggingFace model card |
| OpenAI text-embedding-3-large | 64.6 | 3,072 | API | Azure docs / MTEB |
| OpenAI text-embedding-3-small | 62.3 | 1,536 | API | Azure docs / MTEB |
| OpenAI text-embedding-ada-002 | 61.0 | 1,536 | API (legacy) | Azure docs / MTEB |
| e5-mistral-7b-instruct | 66.63 | 4,096 | Open-source (7B params) | MTEB leaderboard |
| SPECTER2 (with adapter) | ~69 (SciRepEval) | 768 | Open-source (110M params) | HuggingFace model card |
| all-MiniLM-L6-v2 | ~56-58 (est.) | 384 | Open-source (22.7M params) | Community benchmarks |

**Critical caveat:** MTEB measures general-purpose embedding quality across 56 tasks (STS, clustering, reranking, retrieval, classification, etc.). It is NOT a scientific document retrieval benchmark. A model that scores higher on MTEB may or may not be better for arXiv paper recommendation.

### 3b. Scientific Document Embedding: SPECTER2 vs General Models

From the SPECTER2 model card (SciRepEval benchmark, which IS scientific-document-specific):

| Model | SciRepEval Avg | MDCR MAP | Trained On |
|-------|---------------|----------|------------|
| BM-25 (keyword baseline) | -- | 33.7 | -- |
| SPECTER (v1) | 67.5 | 30.6 | Citation triplets |
| SciNCL | 68.8 | 32.6 | Citation triplets |
| SPECTER2 Base | 69.1 | 38.0 | 6M+ citation triplets |
| SPECTER2 + Adapters | 71.1 | 38.4 | + task-specific fine-tuning |

**SPECTER2 is purpose-built for scientific documents** using citation graph structure. General-purpose API embeddings (OpenAI, Cohere, Voyage) are NOT trained on citation graphs and have NOT been benchmarked on SciRepEval. There is no published evidence that API embeddings outperform SPECTER2 on scientific document retrieval tasks.

### 3c. What the Literature Says

From Spike 001 Phase B1 literature review (6 production systems + 2 surveys covering 117 systems, 2019-2024):

- **SPECTER2 is considered SOTA for scientific document embeddings** (citation-graph-trained)
- **50.79% of recent recommendation systems use dense embeddings** vs ~6% TF-IDF
- **Hybrid/adaptive systems dominate** (55.56% use multiple signal types)
- **No published comparison exists** pitting OpenAI/Cohere API embeddings against SPECTER2 on scientific paper retrieval
- The MTEB leaderboard does not include a "scientific paper retrieval" subtask that would allow direct comparison

### 3d. What Spike 003 Found About Local Models

From the strategy profiling spike:

- **MiniLM (S1a):** MRR 0.398, coverage 0.686, held-out recovery 2/15. Character: semantic precision.
- **SPECTER2 (S1c):** MRR 0.184, coverage 0.336, held-out recovery 0/15. Character: cross-community discovery. Score compression issue (range 0.009).
- **TF-IDF (S1d):** MRR 0.104, coverage 0.247, held-out recovery 5/15. Character: keyword precision.
- **Fusion of any kind degrades MiniLM** (all tested combinations: RRF, weighted, pipeline).
- **The three strategies are complementary** (Jaccard overlap 0.179) -- they find different papers.

**Critical note on evaluation bias:** The LOO-MRR evaluation framework is circularly biased toward MiniLM (clusters defined by MiniLM embeddings). TF-IDF and SPECTER2 are systematically underrated by the quantitative metrics.

### 3e. Quality Assessment Summary

| Claim | Evidence Level | Verdict |
|-------|---------------|---------|
| API embeddings beat MiniLM on MTEB | Strong (published benchmarks) | text-embedding-3-large scores 64.6 vs MiniLM ~57. A ~7-point gap. |
| API embeddings beat SPECTER2 on scientific retrieval | None | No published comparison exists. SPECTER2 uses citation-graph training that API models lack. |
| API embeddings beat MiniLM on arXiv paper recommendation | None | MTEB is a general benchmark; our task is domain-specific. Would need direct testing. |
| Higher MTEB score = better paper recommendations | Uncertain | MTEB retrieval subtasks use web/general corpora, not scientific papers. |
| LLM reranking improves recommendation quality | Plausible but unquantified | No published evidence for this specific task. Spike 003 lists it as an open question. |

---

## 4. Feasibility Assessment

### 4a. One-Time Corpus Embedding

| Factor | Assessment |
|--------|-----------|
| Cost | Trivially cheap. $0.08 (OpenAI small) to $0.77 (Google). Voyage AI: FREE. |
| Latency | API round-trip for 19,252 papers in batches. Estimated 5-15 minutes depending on rate limits. |
| Dependency | Requires internet. Embeddings stored locally once computed. |
| Verdict | **Viable. The cost barrier is zero.** |

### 4b. Daily Updates (~600 papers/day)

| Factor | Assessment |
|--------|-----------|
| Cost | $0.002-$0.018/day. Under $7/year. |
| Latency | ~30 seconds API round-trip for 600 papers. |
| Dependency | Requires internet daily. Could batch and retry on failure. |
| Comparison | Local MiniLM: 21s on CPU, 1s on GPU. Local SPECTER2: 13s on GPU. |
| Verdict | **Viable, but adds internet dependency for negligible cost savings vs local GPU.** |

### 4c. LLM Reranking Per-Session

| Factor | Assessment |
|--------|-----------|
| Cost | $0.011/session (GPT-4o-mini) to $0.225/session (Claude Sonnet). |
| Latency | 20 sequential API calls, ~1-3 seconds each = 20-60 seconds per query. Could parallelize. |
| Quality benefit | Unknown. No published evidence for this task. Spike 003 lists it as open question #2. |
| Comparison | MiniLM similarity search: 5ms at 19K papers. Zero cost. |
| Verdict | **Marginal viability. Low cost but high latency and unknown quality benefit.** |

### 4d. Break-Even vs Local GPU (GTX 1080 Ti)

The local GPU already runs MiniLM at 1.7ms/paper and SPECTER2 at ~8ms/paper. Full corpus embedding takes 33 seconds (MiniLM) or 463 seconds (SPECTER2) on GPU.

| Scenario | API Advantage | Local Advantage |
|----------|--------------|-----------------|
| Initial corpus (19K papers) | Cheaper than electricity for GPU? (moot -- pennies either way) | No internet dependency. Already benchmarked. |
| Daily updates (600/day) | Marginal | 1 second on GPU. No API calls. |
| Quality | Unknown. Possibly better MTEB scores. | SPECTER2 has domain-specific training. MiniLM profiled with known MRR. |
| Latency | Seconds of API round-trip | Milliseconds |
| Scale to 215K | Still cheap ($0.50-$5) | 6.3 min GPU, 2hr CPU. Already measured. |

**There is no break-even point because the local GPU is already fast enough and the API costs are too low to matter.** The question is purely about quality, not cost.

---

## 5. Recommendation

### Embedding Services

| Service | Verdict | Rationale |
|---------|---------|-----------|
| OpenAI text-embedding-3-small | **Worth testing** | Cheapest API option. 7-point MTEB advantage over MiniLM. $0.08 to test on full corpus. Could reveal whether general-purpose embeddings outperform domain-specific MiniLM on your actual recommendations. |
| OpenAI text-embedding-3-large | **Worth testing** | Best MTEB score among API embeddings. $0.50 for full corpus. Test alongside small to measure the marginal value of 3,072 vs 1,536 dims. |
| Voyage AI voyage-4 | **Worth testing** | FREE for full corpus (within 200M token tier). Comparable MTEB performance. Zero-cost experiment. |
| Voyage AI voyage-4-large | **Worth testing** | Also FREE. Higher quality tier. No reason not to include if testing voyage-4. |
| Google gemini-embedding-001 | **Not worth testing first** | Higher cost ($0.58), limited max tokens (2,048), no clear quality advantage over OpenAI/Voyage. Could test later if others disappoint. |
| Cohere embed-v3/v4 | **Not worth testing first** | Unclear pricing. 512-token limit on v3 (our abstracts fit, but tight). Model Vault pricing ($4/hr) inappropriate for batch use. Trial key is free but rate-limited. |

### LLM Reranking

| Service | Verdict | Rationale |
|---------|---------|-----------|
| GPT-4o-mini | **Research inconclusive** | At $0.011/session, cost is not the barrier. The barrier is that no published evidence shows LLM reranking improves paper recommendation quality over embedding similarity. This is Spike 003 open question #2. Would need an experiment with human relevance judgments. |
| Gemini 2.5 Flash | **Research inconclusive** | Same reasoning. $0.028/session. |
| Claude Haiku 4.5 | **Not worth testing** | At $0.075/session, 7x more expensive than GPT-4o-mini for a task with no evidence of benefit. |
| Claude Sonnet 4.6 | **Not worth testing** | At $0.225/session ($82/year), too expensive for an unproven quality benefit on a personal tool. |

### Overall Assessment

**The cost barrier for API embeddings is effectively zero.** The entire corpus can be embedded for under $1 (or free with Voyage AI). Daily updates cost under $7/year. This means the decision is purely about quality, not cost.

**The quality question is genuinely open.** No published evidence compares API embeddings to SPECTER2/MiniLM on scientific paper recommendation. The MTEB advantage of API models (64.6 vs ~57 for MiniLM) is measured on general tasks, not scientific retrieval. SPECTER2's citation-graph training is a domain advantage that API models lack.

**Recommended experiment:** Embed the full 19,252-paper corpus with OpenAI text-embedding-3-small, text-embedding-3-large, and Voyage AI voyage-4-large (all under $1 total, or free for Voyage). Run the same LOO-MRR and qualitative evaluation from Spike 003. Compare head-to-head against MiniLM and SPECTER2. This directly answers whether the MTEB advantage translates to paper recommendation quality. Cost: ~$1. Time: ~2 hours of setup + compute. Risk: zero (local models remain the fallback).

**LLM reranking is a separate question** that requires human relevance judgments to evaluate. It should not be tested until the embedding comparison is complete, because reranking operates on a candidate set -- and the candidate set quality depends on which embedding model you use.

---

## 6. Sources and Verification Status

| Source | URL | Access Status | Date Checked |
|--------|-----|--------------|-------------|
| Anthropic model pricing | platform.claude.com/docs | Accessible | 2026-03-20 |
| Voyage AI pricing | docs.voyageai.com/docs/pricing | Accessible | 2026-03-20 |
| Voyage AI model specs | docs.voyageai.com/docs/embeddings | Accessible | 2026-03-20 |
| Google AI pricing | ai.google.dev/pricing | Accessible | 2026-03-20 |
| Google embedding specs | ai.google.dev/gemini-api/docs/embeddings | Accessible | 2026-03-20 |
| Azure OpenAI model specs | learn.microsoft.com | Accessible | 2026-03-20 |
| Cohere pricing page | cohere.com/pricing | Accessible | 2026-03-20 |
| Cohere embed API docs | docs.cohere.com/reference/embed | Accessible | 2026-03-20 |
| OpenAI pricing page | openai.com/api/pricing | BLOCKED (403) | 2026-03-20 |
| OpenAI platform docs | platform.openai.com/docs | BLOCKED (403) | 2026-03-20 |
| SPECTER2 model card | huggingface.co/allenai/specter2_base | Accessible | 2026-03-20 |
| MiniLM model card | huggingface.co/sentence-transformers/all-MiniLM-L6-v2 | Accessible | 2026-03-20 |
| gte-Qwen2-7B MTEB scores | huggingface.co/Alibaba-NLP | Accessible | 2026-03-20 |
| MTEB paper (arXiv:2210.07316) | arxiv.org | Accessible | 2026-03-20 |
| Nomic Embed paper (arXiv:2402.01613) | arxiv.org | Accessible | 2026-03-20 |

### Pricing Confidence Levels

| Service | Confidence | Notes |
|---------|-----------|-------|
| Anthropic | HIGH | Directly from official docs, confirmed March 2026 |
| Voyage AI | HIGH | Directly from official docs |
| Google | HIGH | Directly from official pricing page |
| OpenAI embeddings | MEDIUM | Confirmed via Azure docs + community consensus. OpenAI's own page blocked. These prices have been stable since Jan 2024 launch. |
| OpenAI GPT-4o-mini | LOW | Community-reported pricing only. Could not confirm from primary source. |
| Cohere | LOW | Instance-based pricing confirmed. Per-token pricing for embed not prominently published. Estimate interpolated. |

---

## 7. Summary Table

| Scenario | Cost | Quality vs Local | Dependency | Verdict |
|----------|------|-----------------|------------|---------|
| API embed: initial corpus | $0-$1 | Unknown (MTEB +7pts, but wrong benchmark) | One-time internet | Worth testing |
| API embed: daily updates | $1-$7/year | Unknown | Daily internet | Viable but unnecessary if local GPU works |
| LLM rerank: per session | $0.01-$0.23 | Unknown (no evidence) | Per-query internet | Research inconclusive |
| LLM rerank: annual (daily use) | $4-$82/year | Unknown (no evidence) | Continuous internet | Not justified without quality evidence |
| Local MiniLM + SPECTER2 | $0 (electricity) | Profiled: MRR 0.398 / 0.184 | None | Known quantity |
