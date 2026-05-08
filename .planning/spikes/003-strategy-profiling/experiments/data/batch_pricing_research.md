# Batch API Pricing Research: Embeddings & LLM Services

**Date:** 2026-03-20
**Context:** Supplement to `API-EMBEDDING-COST-ANALYSIS.md` (Spike 001). Focuses on batch pricing specifically.
**Corpus:** 19,252 arXiv papers x ~200 tokens = ~3.85M tokens.
**Daily update:** ~600 papers/day x ~200 tokens = ~120K tokens/day.

---

## 1. OpenAI Batch API

### Does it support embeddings?

**Yes.** The OpenAI Batch API explicitly supports `/v1/embeddings` as a supported endpoint.

Full list of supported endpoints:
- `/v1/responses`
- `/v1/chat/completions`
- `/v1/embeddings`
- `/v1/completions`
- `/v1/moderations`
- `/v1/images/generations` and `/v1/images/edits`
- `/v1/videos`

### Pricing

**50% discount** off standard pricing.

| Model | Standard $/1M tok | Batch $/1M tok | Discount |
|-------|-------------------|----------------|----------|
| text-embedding-3-small | $0.020 | $0.010 | 50% |
| text-embedding-3-large | $0.130 | $0.065 | 50% |

### Turnaround time

- **24-hour completion window.** Batches complete within 24 hours but may finish sooner.
- Azure documentation states: "We aim to process batch requests within 24 hours; we don't expire the jobs that take longer."

### Batch size limits

- **50,000 requests per batch** (max)
- **200 MB file size** per batch
- **For embeddings specifically:** limited to 50,000 embedding inputs across all requests in the batch
- **Batch creation rate:** up to 2,000 batches per hour

### Workflow

Upload a `.jsonl` file with one request per line, create a batch job, poll for status, retrieve results via output file. Results matched by `custom_id`. Output files available for 30 days.

### Source confidence

- **MEDIUM-HIGH.** Confirmed from `developers.openai.com/docs/guides/batch` (official docs). Azure documentation cross-references the 50% discount. OpenAI's pricing page itself returned 403.

### Sources

| Source | URL | Status | Date |
|--------|-----|--------|------|
| OpenAI Batch API Guide | developers.openai.com/docs/guides/batch | Accessible | 2026-03-20 |
| OpenAI Cookbook (redirect) | developers.openai.com/cookbook/examples/batch_processing | Accessible | 2026-03-20 |
| Azure OpenAI Batch Docs | learn.microsoft.com/en-us/azure/ai-services/openai/how-to/batch | Accessible | 2026-03-20 |
| OpenAI Pricing Page | openai.com/api/pricing | BLOCKED (403) | 2026-03-20 |

---

## 2. Google Gemini Batch Embeddings

### Pricing

| Model | Standard $/1M tok | Batch $/1M tok | Discount | Free tier |
|-------|-------------------|----------------|----------|-----------|
| gemini-embedding-001 | $0.150 | $0.075 | 50% | Yes (rate-limited) |
| gemini-embedding-2-preview | $0.200 | Not available | N/A | Yes (rate-limited) |

**Previous research confirmed:** gemini-embedding-001 batch pricing is $0.075/1M tokens (50% discount). gemini-embedding-2-preview has no batch pricing yet.

### Turnaround time

- **Target SLO: 24 hours**, but "in majority of cases, it is much quicker."
- Jobs expire if running/pending for more than **48 hours**.
- Documentation notes: "If latency is not a concern, try using the Gemini Embeddings models with Batch API."

### Batch size limits

- **Inline requests:** Under 20MB total request size
- **File input:** Maximum 2GB per input file
- Submit as JSONL via the File API

### Embeddings batch method

Uses `batches.create_embeddings` method specifically for embedding batches. The embeddings endpoint is explicitly supported.

### Source confidence

- **HIGH.** Confirmed from `ai.google.dev/pricing` and `ai.google.dev/gemini-api/docs/embeddings` and `ai.google.dev/gemini-api/docs/batch-mode`.

### Sources

| Source | URL | Status | Date |
|--------|-----|--------|------|
| Google AI Pricing | ai.google.dev/pricing | Accessible | 2026-03-20 |
| Gemini Embeddings Docs | ai.google.dev/gemini-api/docs/embeddings | Accessible | 2026-03-20 |
| Gemini Batch Mode Docs | ai.google.dev/gemini-api/docs/batch-mode | Accessible | 2026-03-20 |

---

## 3. Voyage AI Batch API

### Pricing

**33% discount** off standard pricing.

| Model | Standard $/1M tok | Batch $/1M tok | Discount | Free tier |
|-------|-------------------|----------------|----------|-----------|
| voyage-4 | $0.060 | $0.040 | 33% | 200M tokens |
| voyage-4-large | $0.120 | $0.080 | 33% | 200M tokens |
| voyage-4-lite | $0.020 | $0.013 | 33% | 200M tokens |
| voyage-context-3 | $0.180 | $0.120 | 33% | 200M tokens |
| voyage-code-3 | $0.180 | $0.120 | 33% | 200M tokens |

### Turnaround time

- **12-hour completion window.** If processing cannot finish within this timeframe, the system completes as many requests as possible and charges only for tokens consumed.

### Batch size limits

- **100,000 inputs per batch** (max)
- Individual requests can contain up to 1,000 examples for embeddings
- Each request subject to model context length (e.g., 32K tokens for voyage-4-large) and total token limits (e.g., 120K tokens)
- **100 in-flight batch jobs** per organization
- **1 billion tokens** across all active batches

### Supported models

voyage-4-large, voyage-4, voyage-4-lite, voyage-3-large, voyage-3.5, voyage-3.5-lite, voyage-context-3, voyage-code-3, voyage-code-2, rerank-2.5, rerank-2.5-lite.

### Key note on free tier

The 200M token free tier should apply to batch usage as well (not explicitly stated, but the pricing page does not differentiate). Our entire corpus (3.85M tokens) fits well within this free tier regardless.

### Source confidence

- **HIGH.** Confirmed from `docs.voyageai.com/docs/pricing` and `docs.voyageai.com/docs/batch-api`.

### Sources

| Source | URL | Status | Date |
|--------|-----|--------|------|
| Voyage AI Pricing | docs.voyageai.com/docs/pricing | Accessible | 2026-03-20 |
| Voyage AI Batch API | docs.voyageai.com/docs/batch-api | Accessible | 2026-03-20 |

---

## 4. Cohere Batch Embedding

### Status

Cohere offers an **Embed Jobs API** for batch embedding, but with significant caveats:

- **No published per-token batch pricing.** Cohere's pricing page does not list per-token rates for embeddings.
- **Model Vault (instance-based) pricing:** Embed 4 is available via Model Vault at $4.00/hr (small instance) or $2,500/month.
- **Trial API key:** Free, rate-limited, non-commercial use only.
- **Embed Jobs API** supports embed-english-v3.0, embed-multilingual-v3.0, and light variants (384/1024 dims). Documentation states it is "only compatible with our embed v3.0 models" though embed-v4.0 may also be supported.
- **No batch discount** is published or mentioned anywhere in the documentation.

### Embed Jobs operational details

- Designed for large-scale (100K+) document encoding
- Upload dataset as CSV or JSONL
- Rate limit: 5 embed jobs/min (trial), 50 embed jobs/min (production)
- Standard embed API: 2,000 inputs/min
- Output formats: float, int8, uint8, binary, ubinary, base64

### Assessment for our use case

Cohere's pricing opacity makes cost comparison impossible. The Model Vault at $4/hr is wildly inappropriate for a 3.85M token corpus (you could embed the entire corpus in seconds via other providers for pennies). The trial key would work for a one-time test but is non-commercial and rate-limited. **Not viable for cost comparison without contacting sales.**

### Source confidence

- **LOW.** Per-token pricing is not published. Instance-based pricing confirmed. Trial key availability confirmed.

### Sources

| Source | URL | Status | Date |
|--------|-----|--------|------|
| Cohere Pricing | cohere.com/pricing | Accessible | 2026-03-20 |
| Cohere Embed API Docs | docs.cohere.com/reference/embed | Accessible | 2026-03-20 |
| Cohere Embed Jobs Docs | docs.cohere.com/v2/docs/embed-jobs-api | Accessible | 2026-03-20 |
| Cohere Rate Limits | docs.cohere.com/docs/rate-limits | Accessible | 2026-03-20 |

---

## 5. LLM Batch Pricing (for Reranking Context)

For completeness, batch pricing for LLM reranking services:

### Anthropic (Message Batches API)

**50% discount.** Most batches finish in less than 1 hour. 24-hour expiry window.

| Model | Standard Input/1M | Batch Input/1M | Standard Output/1M | Batch Output/1M |
|-------|-------------------|----------------|---------------------|-----------------|
| Claude Sonnet 4.6 | $3.00 | $1.50 | $15.00 | $7.50 |
| Claude Haiku 4.5 | $1.00 | $0.50 | $5.00 | $2.50 |

Batch limits: 100,000 requests or 256 MB per batch.

### OpenAI (Batch API for Chat Completions)

**50% discount.** 24-hour completion window.

| Model | Standard Input/1M | Batch Input/1M | Standard Output/1M | Batch Output/1M |
|-------|-------------------|----------------|---------------------|-----------------|
| GPT-4o-mini | $0.15 | $0.075 | $0.60 | $0.30 |

### Google (Gemini Batch)

**50% discount.** 24-hour target SLO, 48-hour expiry.

| Model | Standard Input/1M | Batch Input/1M | Standard Output/1M | Batch Output/1M |
|-------|-------------------|----------------|---------------------|-----------------|
| Gemini 2.5 Flash | $0.30 | $0.15 | $2.50 | $1.25 |

### Source confidence

| Service | Confidence | Notes |
|---------|-----------|-------|
| Anthropic | HIGH | Directly from official batch docs, confirmed March 2026 |
| OpenAI | MEDIUM | 50% discount confirmed from docs, base pricing community-sourced |
| Google | HIGH | From official batch-mode docs |

---

## 6. Comprehensive Cost Comparison Table

### Corpus: 19,252 papers x ~200 tokens = 3.85M tokens
### Daily update: 600 papers x ~200 tokens = 0.12M tokens

| Service | Model | Dims | Standard $/1M | Batch $/1M | Batch Discount | Corpus Cost (Std) | Corpus Cost (Batch) | Daily Update (Batch) | Annual Update (Batch) |
|---------|-------|------|---------------|------------|----------------|-------------------|--------------------|--------------------|----------------------|
| OpenAI | text-embedding-3-small | 1,536 | $0.020 | $0.010 | 50% | $0.08 | $0.04 | $0.0012 | $0.44 |
| OpenAI | text-embedding-3-large | 3,072 | $0.130 | $0.065 | 50% | $0.50 | $0.25 | $0.0078 | $2.85 |
| Voyage AI | voyage-4 | 1,024 | $0.060 | $0.040 | 33% | $0.23 | $0.15 | $0.0048 | $1.75 |
| Voyage AI | voyage-4-large | 1,024 | $0.120 | $0.080 | 33% | $0.46 | $0.31 | $0.0096 | $3.50 |
| Voyage AI | voyage-4-lite | 512 | $0.020 | $0.013 | 33% | $0.08 | $0.05 | $0.0016 | $0.57 |
| Google | gemini-embedding-001 | 768-3,072 | $0.150 | $0.075 | 50% | $0.58 | $0.29 | $0.0090 | $3.29 |
| Google | gemini-embedding-2-preview | 768-3,072 | $0.200 | N/A | N/A | $0.77 | N/A | N/A | N/A |
| Cohere | embed-english-v3.0 | 1,024 | ~$0.10 | Unknown | Unknown | ~$0.39 | Unknown | Unknown | Unknown |

**Notes:**
- Voyage AI models: entire corpus (3.85M tokens) fits within the 200M token free tier, making both standard and batch pricing moot for initial embedding. Free tier likely applies to batch as well.
- Cohere: no published per-token batch pricing. Model Vault instance pricing ($4/hr) is not comparable.
- Google gemini-embedding-2-preview: no batch pricing available yet (preview model).
- Daily update cost = 0.12M tokens x batch rate. Annual = daily x 365.

### Ranked by annual batch update cost (cheapest first)

| Rank | Service | Model | Annual Batch Update Cost | Notes |
|------|---------|-------|------------------------|-------|
| 1 | OpenAI | text-embedding-3-small | $0.44/yr | Cheapest per-token |
| 2 | Voyage AI | voyage-4-lite | $0.57/yr | Low dims (512) |
| 3 | Voyage AI | voyage-4 | $1.75/yr | FREE initial corpus |
| 4 | OpenAI | text-embedding-3-large | $2.85/yr | Highest MTEB |
| 5 | Google | gemini-embedding-001 | $3.29/yr | 50% batch discount |
| 6 | Voyage AI | voyage-4-large | $3.50/yr | FREE initial corpus |

**All annual costs remain under $4/year.** Batch pricing does not materially change the "cost is irrelevant" conclusion from the standard pricing analysis.

---

## 7. Batch Pricing for LLM Reranking (Updated)

Per reranking pair: ~500 input tokens + ~50 output tokens.

| Model | Std Cost/Pair | Batch Cost/Pair | Std Cost/Session (100 pairs) | Batch Cost/Session | Annual Batch (365 sessions) |
|-------|--------------|----------------|-----------------------------|--------------------|----------------------------|
| GPT-4o-mini | $0.0001 | $0.00005 | $0.011 | $0.006 | $2.01 |
| Gemini 2.5 Flash | $0.0003 | $0.00015 | $0.028 | $0.014 | $5.11 |
| Claude Haiku 4.5 | $0.0008 | $0.0004 | $0.075 | $0.038 | $13.69 |
| Claude Sonnet 4.6 | $0.0023 | $0.0011 | $0.225 | $0.113 | $41.06 |

**Batch reranking note:** Batch APIs have 12-24 hour turnaround windows, making them unsuitable for interactive reranking (which needs sub-second response). Batch LLM pricing is only relevant for offline/pre-computed reranking of the full corpus, not per-query use.

---

## 8. Updated "Worth Testing" Verdicts

### Embedding Services

The batch discount does not change any verdicts. Costs were already negligible at standard pricing. The entire corpus can be embedded for $0.04-$0.31 at batch rates (or free with Voyage AI). Annual updates cost $0.44-$3.50.

| Service | Previous Verdict | Updated Verdict | Change? |
|---------|-----------------|-----------------|---------|
| OpenAI text-embedding-3-small | Worth testing | **Worth testing** (even cheaper at $0.04 batch) | No change |
| OpenAI text-embedding-3-large | Worth testing | **Worth testing** ($0.25 batch vs $0.50 standard) | No change |
| Voyage AI voyage-4 | Worth testing | **Worth testing** (FREE regardless) | No change |
| Voyage AI voyage-4-large | Worth testing | **Worth testing** (FREE regardless) | No change |
| Google gemini-embedding-001 | Not worth testing first | **Not worth testing first** (batch helps, but still more expensive than OpenAI/Voyage) | No change |
| Cohere embed-v3/v4 | Not worth testing first | **Not worth testing first** (pricing still opaque) | No change |

### LLM Reranking

Batch pricing halves the cost but introduces latency incompatible with interactive use. This creates a new option: **offline pre-computed reranking.**

| Service | Previous Verdict | Updated Verdict | Change? |
|---------|-----------------|-----------------|---------|
| GPT-4o-mini (interactive) | Research inconclusive | **Research inconclusive** (still $0.011/session) | No change |
| GPT-4o-mini (batch, offline) | Not previously considered | **New option, still research inconclusive** ($2.01/yr but only for pre-computed) | New |
| Gemini 2.5 Flash (batch) | Not previously considered | **New option, research inconclusive** ($5.11/yr, offline only) | New |
| Claude Haiku 4.5 (batch) | Not worth testing | **Marginal** ($13.69/yr batch vs $27.38 standard, but still offline-only) | Slight improvement |
| Claude Sonnet 4.6 (batch) | Not worth testing | **Not worth testing** ($41/yr batch, still expensive for unproven benefit) | No change |

---

## 9. Summary of Batch API Features

| Feature | OpenAI | Google Gemini | Voyage AI | Cohere | Anthropic |
|---------|--------|--------------|-----------|--------|-----------|
| Embeddings supported | Yes | Yes | Yes | Yes (Embed Jobs) | N/A (no embeddings) |
| Discount | 50% | 50% | 33% | Unknown | 50% |
| Turnaround SLO | 24 hours | 24 hours (48h expiry) | 12 hours | Not published | 1 hour typical (24h expiry) |
| Max batch size | 50K requests / 200MB | 2GB file | 100K inputs | Not published | 100K requests / 256MB |
| Workflow | JSONL upload | JSONL or inline | JSONL upload | CSV/JSONL dataset | API request array |
| Free tier | None | Yes (rate-limited) | 200M tokens | Trial key only | None |

---

## 10. Key Takeaway

**Batch pricing does not change the fundamental analysis.** The cost of API embeddings was already negligible at standard prices. Batch pricing makes it even more negligible. The decision between API and local embeddings remains a question of **quality** (does a general MTEB advantage translate to scientific paper recommendation?) and **dependency** (do you want to require internet for daily updates?), not cost.

The one new consideration batch pricing introduces is the possibility of **offline pre-computed LLM reranking** at $2-5/year using GPT-4o-mini or Gemini Flash in batch mode. This is a genuinely cheap option for pre-scoring the corpus, though it requires evidence that LLM reranking improves recommendation quality before it would be worth implementing.

---

## 11. All Sources

| Source | URL | Access Status | Date |
|--------|-----|--------------|------|
| OpenAI Batch API Guide | developers.openai.com/docs/guides/batch | Accessible | 2026-03-20 |
| OpenAI Cookbook (batch processing) | developers.openai.com/cookbook/examples/batch_processing | Accessible (redirect) | 2026-03-20 |
| Azure OpenAI Batch Docs | learn.microsoft.com/en-us/azure/ai-services/openai/how-to/batch | Accessible | 2026-03-20 |
| OpenAI Pricing Page | openai.com/api/pricing | BLOCKED (403) | 2026-03-20 |
| Google AI Pricing | ai.google.dev/pricing | Accessible | 2026-03-20 |
| Gemini Embeddings Docs | ai.google.dev/gemini-api/docs/embeddings | Accessible | 2026-03-20 |
| Gemini Batch Mode Docs | ai.google.dev/gemini-api/docs/batch-mode | Accessible | 2026-03-20 |
| Voyage AI Pricing | docs.voyageai.com/docs/pricing | Accessible | 2026-03-20 |
| Voyage AI Batch API Docs | docs.voyageai.com/docs/batch-api | Accessible | 2026-03-20 |
| Cohere Pricing | cohere.com/pricing | Accessible | 2026-03-20 |
| Cohere Embed API Docs | docs.cohere.com/reference/embed | Accessible | 2026-03-20 |
| Cohere Embed Jobs Docs | docs.cohere.com/v2/docs/embed-jobs-api | Accessible | 2026-03-20 |
| Cohere Rate Limits | docs.cohere.com/docs/rate-limits | Accessible | 2026-03-20 |
| Anthropic Batch Docs | platform.claude.com/docs/en/docs/build-with-claude/batch-processing | Accessible | 2026-03-20 |
