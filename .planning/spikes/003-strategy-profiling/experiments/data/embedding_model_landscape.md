# Embedding Model Landscape for Academic Paper Retrieval

**Date:** 2026-03-20
**Purpose:** Survey of open-source embedding models (2024-2026) for arXiv paper similarity and retrieval
**Hardware constraint:** GTX 1080 Ti (11GB VRAM, CUDA 11.8, no tensor cores)
**Current models:** all-MiniLM-L6-v2 (384-dim), SPECTER2 proximity adapter (768-dim)

---

## 1. Executive Summary

The embedding model landscape has shifted substantially since 2024. Three trends
dominate: (a) LLM-derived embedders (7-8B parameters) now top MTEB but are too
large for our GPU; (b) a strong tier of 300M-600M parameter models has emerged
that comfortably fits on the GTX 1080 Ti and significantly outperforms MiniLM on
general benchmarks; (c) no new academic-specific embedding model has appeared
since SPECTER2 -- the scientific document embedding niche remains stagnant while
general-purpose models have leapfrogged it on generic benchmarks.

The most promising candidates for our use case are:
- **Stella v5 400M** -- top retrieval performer among sub-1B models, MIT license
- **GTE-large-en-v1.5** -- strong all-around, 8K context, Apache 2.0
- **Qwen3-Embedding-0.6B** -- newest architecture, flexible dims, Apache 2.0
- **Snowflake Arctic Embed L v2.0** -- good retrieval, 8K context, Apache 2.0

None of these are academic-specific. Whether they outperform MiniLM on *our*
task (arXiv paper-to-paper similarity) cannot be determined from MTEB scores
alone -- that requires empirical evaluation on our corpus.

---

## 2. Comprehensive Model Catalog

### 2.1 Models That Fit on GTX 1080 Ti (under ~4GB VRAM in fp16)

These models have under ~1B parameters and will comfortably fit in 11GB VRAM
even with generous batch sizes.

#### Stella v5 400M (NovaSearch)
- **Parameters:** 400M
- **Dimensions:** 256, 512, 768, 1024, 2048, 4096 (Matryoshka)
- **Recommended dim:** 1024 (only 0.001 MTEB loss vs 8192)
- **Max tokens:** 512
- **MTEB overall:** ~65-66 (estimated from task scores)
- **MTEB retrieval:** Top-performing sub-1B model on retrieval leaderboard
- **License:** MIT
- **Base:** Fine-tuned from Alibaba GTE-large-en-v1.5
- **VRAM estimate (fp16):** ~0.8GB model + batch overhead = ~2-3GB
- **Academic specialization:** None
- **HuggingFace:** NovaSearch/stella_en_400M_v5
- **Notes:** Requires task-specific prompts (s2p for retrieval, s2s for similarity). Trained via distillation from larger models. A related 1.5B variant (stella_en_1.5B_v5) and student model Jasper (2B) also exist. Max 512 tokens is a limitation for long abstracts.

#### GTE-large-en-v1.5 (Alibaba DAMO)
- **Parameters:** 434M
- **Dimensions:** 1024
- **Max tokens:** 8192
- **MTEB overall:** 65.39
- **MTEB retrieval:** 57.91
- **License:** Apache 2.0
- **Base:** Transformer++ encoder (BERT + RoPE + GLU)
- **VRAM estimate (fp16):** ~0.9GB model + batch overhead = ~2-3GB
- **Academic specialization:** None
- **HuggingFace:** Alibaba-NLP/gte-large-en-v1.5
- **Notes:** Solid all-around performer. Long context support is valuable for full abstracts. Requires trust_remote_code=True. Parent architecture for Stella v5.

#### Qwen3-Embedding-0.6B (Alibaba/Qwen)
- **Parameters:** 600M (decoder-based architecture, 28 layers)
- **Dimensions:** 32-1024 (Matryoshka), default 1024
- **Max tokens:** 32K
- **MTEB English v2 overall:** 70.70
- **MTEB English v2 retrieval:** 61.83
- **License:** Apache 2.0
- **Base:** Qwen3-0.6B-Base (decoder architecture with bidirectional attention)
- **VRAM estimate (fp16):** ~1.2GB model + batch overhead = ~2-4GB
- **Academic specialization:** None
- **HuggingFace:** Qwen/Qwen3-Embedding-0.6B
- **Notes:** Newest architecture (June 2025). Instruction-aware -- can customize prompts per task. Uses decoder backbone (different from BERT-family encoders). GGUF quantized versions available. Very strong MTEB scores for its size. 100+ language support. The 4B and 8B variants exist but are too large.

#### Snowflake Arctic Embed L v2.0
- **Parameters:** 568M (303M non-embedding)
- **Dimensions:** 1024 (256 via MRL with <3% quality loss)
- **Max tokens:** 8192 (via RoPE)
- **BEIR (retrieval):** 55.6 NDCG@10
- **License:** Apache 2.0
- **Base:** Built on bge-m3-retromae backbone
- **VRAM estimate (fp16):** ~1.1GB model + batch overhead = ~2-4GB
- **Academic specialization:** None
- **HuggingFace:** Snowflake/snowflake-arctic-embed-l-v2.0
- **Notes:** Multilingual (74 languages). Int4 quantization support. Very compression-friendly. Good for production deployment. Medium-sized variant (M v2.0, 305M) also available.

#### ModernBERT Embed Large (LightOn AI)
- **Parameters:** 400M (395M base ModernBERT-large)
- **Dimensions:** 1024 (256 via Matryoshka)
- **Max tokens:** 2048+ (inherited from ModernBERT)
- **MTEB overall:** 63.84
- **MTEB retrieval:** 54.36
- **License:** Apache 2.0
- **Base:** ModernBERT-large (answer.ai architecture)
- **VRAM estimate (fp16):** ~0.8GB model + batch overhead = ~2-3GB
- **Academic specialization:** None
- **HuggingFace:** lightonai/modernbert-embed-large
- **Notes:** Newer BERT replacement architecture with efficiency improvements. Requires search_query/search_document prefixes. Trained on Nomic Embed datasets. ONNX support available.

#### ModernBERT Embed Base (Nomic AI)
- **Parameters:** ~149M
- **Dimensions:** 768 (256 via Matryoshka)
- **Max tokens:** 2048+
- **MTEB overall:** 62.62
- **MTEB retrieval:** 52.89
- **License:** Apache 2.0
- **HuggingFace:** nomic-ai/modernbert-embed-base
- **Notes:** Smaller ModernBERT variant. Competitive with much larger models.

#### Nomic Embed Text v2 MoE
- **Parameters:** 475M total, 305M active (MoE with 8 experts, top-2 routing)
- **Dimensions:** 768 (256 via Matryoshka)
- **Max tokens:** 512
- **BEIR (retrieval):** 52.86
- **License:** Apache 2.0
- **Base:** Custom MoE architecture
- **VRAM estimate (fp16):** ~1.0GB model (full 475M loaded) + batch = ~2-3GB
- **Academic specialization:** None
- **HuggingFace:** nomic-ai/nomic-embed-text-v2-moe
- **Notes:** First MoE embedding model. Open weights, code, AND training data. Competitive multilingual performance. GGUF format available.

#### Nomic Embed Text v1.5
- **Parameters:** ~100M
- **Dimensions:** 768 (adjustable to 64 via Matryoshka)
- **Max tokens:** 8192
- **MTEB overall:** 62.28
- **License:** Apache 2.0
- **HuggingFace:** nomic-ai/nomic-embed-text-v1.5
- **Notes:** Lightweight. Long context. Requires task prefixes. Aligned with vision model. Very close to MiniLM in size class.

#### EmbeddingGemma 300M (Google DeepMind)
- **Parameters:** 308M (100M model + 200M embedding params)
- **Dimensions:** 768 (512, 256, 128 via MRL)
- **Max tokens:** 2048
- **License:** Open weights, commercial use permitted (Gemma terms)
- **VRAM estimate (fp16):** ~0.6GB model + batch = ~1-2GB
- **Academic specialization:** None
- **HuggingFace:** google/embeddinggemma-300m
- **Notes:** Released September 2025. Best-in-class for sub-500M on MTEB. 100+ languages. <22ms latency claim. Runs on <200MB RAM with quantization.

#### BGE-large-en-v1.5 (BAAI)
- **Parameters:** ~335M
- **Dimensions:** 1024
- **Max tokens:** 512
- **MTEB overall:** 64.23
- **MTEB retrieval:** 54.29
- **License:** MIT
- **HuggingFace:** BAAI/bge-large-en-v1.5
- **Notes:** Established model (2023). Well-tested. BERT-based. Still competitive.

#### BGE-base-en-v1.5 (BAAI)
- **Parameters:** ~109M
- **Dimensions:** 768
- **Max tokens:** 512
- **MTEB overall:** 63.55
- **License:** MIT
- **HuggingFace:** BAAI/bge-base-en-v1.5

#### BGE-M3 (BAAI)
- **Parameters:** 568M
- **Dimensions:** 1024 (dense), plus sparse and multi-vector outputs
- **Max tokens:** 8192
- **License:** MIT
- **HuggingFace:** BAAI/bge-m3
- **VRAM estimate (fp16):** ~1.1GB model + batch = ~2-4GB
- **Notes:** Uniquely supports dense + sparse + ColBERT-style multi-vector retrieval in one model. 100+ languages. Long context. This hybrid retrieval capability is distinctive.

#### Jina Embeddings v3
- **Parameters:** 570M
- **Dimensions:** 1024 (32 minimum via Matryoshka)
- **Max tokens:** 8192
- **MTEB overall:** 65.52
- **MTEB retrieval:** strong (ranked 2nd for sub-1B at release)
- **License:** CC BY-NC 4.0 (NON-COMMERCIAL)
- **HuggingFace:** jinaai/jina-embeddings-v3
- **Notes:** Task-specific LoRA adapters (retrieval, classification, clustering, matching). Based on XLM-RoBERTa. Non-commercial license is a significant constraint.

### 2.2 Models That Do NOT Fit on GTX 1080 Ti

These are included for completeness. They require 14-16+ GB VRAM minimum.

| Model | Params | Dims | MTEB | Why excluded |
|-------|--------|------|------|--------------|
| NV-Embed-v2 | 7.5B | 4096 | 72.31 | ~15GB fp16 minimum |
| Qwen3-Embedding-8B | 8B | 4096 | 70.58 (multilingual) | ~16GB fp16 |
| Qwen3-Embedding-4B | 4B | 4096 | -- | ~8GB fp16 + batch = >11GB |
| Llama-Embed-Nemotron-8B | 7.5B | 4096 | SOTA multilingual | ~15GB fp16 |
| GTE-Qwen2-7B-instruct | 7B | 3584 | 70.24 | ~14GB fp16 |
| E5-Mistral-7B-instruct | 7B | 4096 | -- | ~14GB fp16 |
| GritLM-7B | 7B | 4096 | High MTEB | ~14GB fp16 |
| Stella v5 1.5B | 1.5B | 1024+ | Higher than 400M | ~3GB model but tight with batches |
| BGE-en-ICL | 7B | 4096 | 71.24 | ~14GB fp16 |

#### Borderline: NVIDIA Llama-Nemotron-Embed-1B-v2
- **Parameters:** 1B
- **Dimensions:** 2048 (384, 512, 768, 1024 via Matryoshka)
- **Max tokens:** 8192
- **License:** NVIDIA Open Model License (commercial OK)
- **VRAM estimate (fp16):** ~2GB model + batch overhead. Fits, but batch sizes limited.
- **HuggingFace:** nvidia/llama-nemotron-embed-1b-v2
- **Notes:** Decoder-based (Llama 3.2 1B). Strong multilingual and cross-lingual. Tight fit with large batches but feasible at batch_size=16-32.

### 2.3 Academic-Specific Models

#### SPECTER2 (AllenAI) -- Already in use
- **Parameters:** ~110M (SciBERT base) + adapter weights
- **Dimensions:** 768
- **Max tokens:** 512
- **Training:** Citation graph (6M triplets, 23 fields)
- **Adapters:** Proximity, classification, regression, search
- **License:** Apache 2.0
- **Status:** Still the latest academic-specific model. No SPECTER3 exists.

#### SciNCL (AllenAI, 2022)
- **Parameters:** ~110M (SciBERT base)
- **Dimensions:** 768
- **Training:** Citation neighborhood contrastive learning
- **Status:** Predecessor to SPECTER2. Superseded.

#### SciBERT (AllenAI, 2019)
- **Parameters:** ~110M
- **Status:** Base language model, not optimized for embeddings.

#### Citation Importance-Aware Document Representation (Liang et al., 2025)
- **Paper:** arxiv.org/abs/2512.13054
- **Approach:** Fine-tunes SciBERT with citation-importance-aware contrastive learning
- **Key idea:** Uses citation location, frequency, and self-citation to weight training pairs
- **Tested on:** SciDocs, PubMed, 33M Web of Science documents
- **Code availability:** Not confirmed
- **Status:** Research paper only; not a released model checkpoint

**Key finding:** No new academic-specific embedding model checkpoint has been released since SPECTER2 (2023). The academic embedding niche has stagnated while general-purpose models have advanced rapidly.

---

## 3. Frameworks and Tooling

### 3.1 Sentence Transformers (v5.3, current)
- **Status:** Our current framework. Actively maintained by HuggingFace.
- **Recent features:** Alternative InfoNCE formulations, hardness weighting for MNRL, CachedSpladeLoss, hashed batch sampler, 20+ loss functions.
- **Fine-tuning:** Full support for contrastive, triplet, cosine, and Matryoshka losses.
- **Model support:** All models in section 2.1 are compatible.
- **Assessment:** Remains the best choice. No reason to switch.

### 3.2 FlagEmbedding (BAAI)
- **Repository:** github.com/FlagOpen/FlagEmbedding
- **Capabilities:** Training, fine-tuning, evaluation for BGE models. Custom dataset evaluation. Hard negative mining.
- **Assessment:** Useful if we adopt BGE-M3 or want its hybrid retrieval features. Otherwise sentence-transformers is sufficient.

### 3.3 MTEB (Massive Text Embedding Benchmark)
- **Repository:** github.com/embeddings-benchmark/mteb
- **Custom evaluation:** Supports creating custom tasks by subclassing abstract task classes. Can benchmark any model that maps text to vectors.
- **Assessment:** Best tool for systematic model comparison on a custom arXiv dataset. Can create a custom retrieval task from our 19K papers.

### 3.4 txtai
- **Repository:** github.com/neuml/txtai
- **Capabilities:** All-in-one framework for semantic search, embedding database, RAG.
- **Assessment:** More than we need. Sentence-transformers + MTEB custom tasks is more targeted.

---

## 4. VRAM Feasibility for Top Candidates

### Estimation methodology

VRAM for embedding models = model_weights + activations + batch_data

- Model weights (fp16): parameters x 2 bytes
- Activations during forward pass: ~10-15% of model size per batch element
- Batch data: tokens x batch_size x hidden_dim x 2 bytes (for attention)

For the GTX 1080 Ti (11GB, no tensor cores, CUDA 11.8):
- fp16 inference works but is slower than on tensor-core GPUs
- fp32 fallback doubles weight memory
- Practical headroom: ~8-9GB usable after CUDA context (~1-2GB)

### Per-model feasibility

| Model | Params | Weights fp16 | Weights fp32 | Max batch (fp16, 512 tok) | Max batch (fp32, 512 tok) | Fits? |
|-------|--------|-------------|-------------|--------------------------|--------------------------|-------|
| all-MiniLM-L6-v2 (current) | 22M | 44MB | 88MB | 256+ | 256+ | Yes, trivially |
| SPECTER2 + adapter (current) | ~110M | ~220MB | ~440MB | 128+ | 64+ | Yes, easily |
| EmbeddingGemma-300M | 308M | ~616MB | ~1.2GB | 64-128 | 32-64 | Yes |
| Stella v5 400M | 400M | ~800MB | ~1.6GB | 64-128 | 32-64 | Yes |
| GTE-large-en-v1.5 | 434M | ~868MB | ~1.7GB | 64-128 | 32-64 | Yes |
| ModernBERT-embed-large | 400M | ~800MB | ~1.6GB | 64-128 | 32-64 | Yes |
| Nomic Embed v2 MoE | 475M | ~950MB | ~1.9GB | 64 | 32 | Yes |
| BGE-M3 | 568M | ~1.1GB | ~2.3GB | 32-64 | 16-32 | Yes |
| Snowflake Arctic L v2.0 | 568M | ~1.1GB | ~2.3GB | 32-64 | 16-32 | Yes |
| Jina v3 | 570M | ~1.1GB | ~2.3GB | 32-64 | 16-32 | Yes (but NC license) |
| Qwen3-Embedding-0.6B | 600M | ~1.2GB | ~2.4GB | 32-64 | 16-32 | Yes |
| Nemotron-Embed-1B | 1B | ~2GB | ~4GB | 16-32 | 8-16 | Tight but feasible |

### Embedding 19K papers -- time estimates

Assuming ~200 tokens average per title+abstract, fp16 inference:

| Model | Est. speed (papers/sec, GPU) | Time for 19K papers | Notes |
|-------|------------------------------|---------------------|-------|
| MiniLM (current, measured) | ~590/sec GPU | ~32 sec | Baseline |
| SPECTER2 (current, measured) | ~42/sec GPU | ~7.5 min | Baseline |
| 300-400M model | ~100-200/sec (est.) | ~1.5-3 min | 3-6x slower than MiniLM |
| 500-600M model | ~50-100/sec (est.) | ~3-6 min | Similar to SPECTER2 |
| 1B model | ~25-50/sec (est.) | ~6-12 min | Borderline acceptable |

Note: GTX 1080 Ti lacks tensor cores, so fp16 runs on CUDA cores with less
speedup than modern GPUs. Actual speeds need measurement. These estimates
assume batch encoding with sentence-transformers.

---

## 5. Recommendation Table

| Model | Dims | MTEB | VRAM (fp16) | Academic? | License | Worth testing? | Rationale |
|-------|------|------|-------------|-----------|---------|---------------|-----------|
| **Stella v5 400M** | 1024 | ~65-66 | ~2-3GB | No | MIT | **Yes -- priority 1** | Top retrieval among sub-1B. Same size class as our GPU handles well. MIT license. Matryoshka dims. Based on GTE-large which is itself strong. Genuinely different architecture from MiniLM (distillation-trained, instruction-based). |
| **Qwen3-Embedding-0.6B** | 1024 | 70.70 (v2) | ~2-4GB | No | Apache 2.0 | **Yes -- priority 2** | Highest MTEB scores in the size class. Decoder-based architecture (genuinely different from all BERT-family models including MiniLM and SPECTER2). Newest model (June 2025). Flexible Matryoshka dims. |
| **GTE-large-en-v1.5** | 1024 | 65.39 | ~2-3GB | No | Apache 2.0 | **Yes -- priority 3** | Strong MTEB retrieval (57.91). 8K context handles full abstracts. Well-established. Parent of Stella v5. Testing both parent and child reveals whether distillation adds value. |
| **BGE-M3** | 1024 | 63.0 | ~2-4GB | No | MIT | **Maybe** | Unique hybrid retrieval (dense + sparse + ColBERT). The sparse retrieval mode could complement our TF-IDF view. But adds architectural complexity. Test only if we want to explore hybrid retrieval as an alternative to separate TF-IDF. |
| **Snowflake Arctic L v2.0** | 1024 | 55.6 (BEIR) | ~2-4GB | No | Apache 2.0 | **Maybe** | Good compression (4x MRL + Int4). Multilingual. But retrieval scores are not clearly better than GTE or Stella. Worth testing only if we need multilingual support or aggressive compression. |
| **EmbeddingGemma-300M** | 768 | High for size | ~1-2GB | No | Gemma (commercial OK) | **Maybe** | Extremely efficient. Could replace MiniLM if it performs similarly at lower cost. But 768-dim (same as MiniLM class) and 2K context limit. Less likely to capture something MiniLM misses. |
| **ModernBERT-embed-large** | 1024 | 63.84 | ~2-3GB | No | Apache 2.0 | **Lower priority** | Newer architecture but MTEB scores are not clearly superior to GTE or Stella. Main value is if ModernBERT's architectural improvements help on scientific text specifically. |
| **Nomic Embed v2 MoE** | 768 | 52.86 BEIR | ~2-3GB | No | Apache 2.0 | **Lower priority** | Novel MoE architecture. But BEIR retrieval score (52.86) is below GTE and Stella. Fully open (weights + code + data). 512 token limit. |
| **Nomic Embed v1.5** | 768 | 62.28 | ~1GB | No | Apache 2.0 | **No** | Too similar to MiniLM in size, architecture, and likely behavior. 100M params, BERT-based. Would not provide a genuinely different signal. |
| **BGE-large-en-v1.5** | 1024 | 64.23 | ~2GB | No | MIT | **No** | Superseded by GTE-large-en-v1.5 and Stella v5 which are based on similar foundations but perform better. |
| **Jina v3** | 1024 | 65.52 | ~2-4GB | No | CC BY-NC 4.0 | **No** | Non-commercial license eliminates it regardless of performance. |
| **Nemotron-Embed-1B** | 2048 | Good multilingual | ~4-5GB | No | NVIDIA Open | **No** | 1B params is tight on our GPU. Decoder-based like Qwen3 but larger. Qwen3-0.6B is a better fit for the same architectural class. |
| **SPECTER2** (current) | 768 | N/A (academic) | ~1GB | **Yes** | Apache 2.0 | **Already in use** | Keep. No replacement exists. Its citation-graph training captures a signal no general model can replicate without similar training data. |

---

## 6. Analysis and Recommendations

### 6.1 What would be genuinely different from MiniLM and SPECTER2?

Our current models occupy two niches:
- **MiniLM** (22M params, BERT-based, general contrastive training): Fast, small, semantic precision
- **SPECTER2** (110M params, SciBERT-based, citation-graph training): Academic community structure

A new model adds value only if it captures a signal that neither MiniLM nor SPECTER2 captures. Candidates:

1. **Decoder-based architecture (Qwen3-0.6B):** Uses fundamentally different attention patterns than BERT-family encoders. May represent abstracts differently. Worth testing.

2. **Distillation-trained instruction model (Stella v5 400M):** Trained via distillation from larger teacher models with instruction-following. Different training signal than MiniLM's simple contrastive pairs. Worth testing.

3. **Long-context encoder (GTE-large-en-v1.5):** 8K context means it processes the full abstract without truncation, which MiniLM (256 token effective) and SPECTER2 (512 token) cannot. This is a concrete capability difference. Worth testing.

4. **Hybrid dense+sparse retrieval (BGE-M3):** Its built-in sparse retrieval could provide a principled alternative to our TF-IDF view while also offering dense embeddings. Architecturally distinct approach.

Models that are NOT genuinely different:
- Nomic v1.5, BGE-large-en-v1.5, EmbeddingGemma: Same BERT-family, similar size class, similar training approach to MiniLM. Likely to produce correlated rankings.

### 6.2 The academic embedding gap

No new academic-specific model has been released since SPECTER2. The only relevant new work is Liang et al. (2025) on citation-importance-aware training, but they fine-tuned SciBERT and have not released a model checkpoint.

This means:
- SPECTER2 remains the only option for citation-graph-aware embeddings
- General-purpose models may outperform SPECTER2 on generic benchmarks but lack the citation signal
- Fine-tuning a general model (e.g., Stella v5) on citation data could combine the best of both worlds, but requires citation pair training data (which we do not currently have)

### 6.3 Evaluation methodology

MTEB scores cannot predict performance on our specific task (arXiv paper-to-paper similarity based on researcher interest profiles). Key reasons:
- Our evaluation framework (LOO-MRR with MiniLM-defined clusters) has known circular bias toward MiniLM
- MTEB retrieval tasks are query-to-document, not document-to-document similarity
- Academic text is a specific domain; general benchmark scores may not transfer
- The signal we most need to capture (cross-community relatedness, held-out paper recovery) is not measured by any standard benchmark

**Recommended evaluation approach:**
1. Use MTEB custom task API to create an arXiv paper similarity task from our 19K corpus
2. Use the qualitative review methodology from Spike 003 (human/AI assessment of recommendation quality)
3. Measure the same instruments: MRR, coverage, held-out recovery, Jaccard overlap with existing strategies
4. Key question: does the new model find papers that NEITHER MiniLM NOR SPECTER2 finds?

### 6.4 Fine-tuning path

If no off-the-shelf model captures a new signal, fine-tuning is the next option:

**Sentence Transformers v5.3 supports:**
- MultipleNegativesRankingLoss (with new hardness weighting)
- MatryoshkaLoss for flexible dimensions
- Contrastive fine-tuning on custom triplets

**What we would need:**
- Training data: (paper, similar_paper, dissimilar_paper) triplets
- Sources: co-citation pairs, same-author pairs, same-category pairs
- Base model: GTE-large-en-v1.5 or Stella v5 400M (strong starting point)
- Hardware: GTX 1080 Ti can fine-tune 400M models in fp16 with small batch sizes

**FlagEmbedding toolkit** also supports fine-tuning with hard negative mining, which could be useful for creating high-quality training data from our corpus.

### 6.5 Practical testing plan

**Phase 1: Quick screen (1-2 hours)**
- Embed 19K papers with top 3 candidates (Stella v5, Qwen3-0.6B, GTE-large)
- Measure embedding time, VRAM usage, and basic cosine similarity statistics
- Check score distribution (is it compressed like SPECTER2?)

**Phase 2: Quality evaluation (half day)**
- Run LOO-MRR with existing profiles
- Measure Jaccard overlap with MiniLM and SPECTER2 top-K sets
- If Jaccard < 0.5 with both existing models: promising (captures different signal)
- If Jaccard > 0.8 with MiniLM: not worth adding (redundant)

**Phase 3: Qualitative review (if Phase 2 shows promise)**
- Select 3 profiles where new model differs most from existing
- Human review of unique recommendations
- Determine whether differences are meaningful or noise

---

## 7. Sources

### Model repositories
- [Stella v5 400M](https://huggingface.co/NovaSearch/stella_en_400M_v5)
- [GTE-large-en-v1.5](https://huggingface.co/Alibaba-NLP/gte-large-en-v1.5)
- [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [Snowflake Arctic Embed L v2.0](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0)
- [ModernBERT-embed-large](https://huggingface.co/lightonai/modernbert-embed-large)
- [ModernBERT-embed-base](https://huggingface.co/nomic-ai/modernbert-embed-base)
- [Nomic Embed Text v2 MoE](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe)
- [Nomic Embed Text v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5)
- [EmbeddingGemma-300M](https://huggingface.co/google/embeddinggemma-300m)
- [BGE-M3](https://huggingface.co/BAAI/bge-m3)
- [BGE-large-en-v1.5](https://huggingface.co/BAAI/bge-large-en-v1.5)
- [Jina Embeddings v3](https://huggingface.co/jinaai/jina-embeddings-v3)
- [NV-Embed-v2](https://huggingface.co/nvidia/NV-Embed-v2)
- [Llama-Nemotron-Embed-1B-v2](https://huggingface.co/nvidia/llama-nemotron-embed-1b-v2)
- [Llama-Embed-Nemotron-8B](https://huggingface.co/nvidia/llama-embed-nemotron-8b)

### Frameworks and tools
- [Sentence Transformers](https://github.com/huggingface/sentence-transformers) -- v5.3 current
- [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) -- BAAI toolkit
- [MTEB](https://github.com/embeddings-benchmark/mteb) -- benchmark framework
- [txtai](https://github.com/neuml/txtai) -- all-in-one embedding framework

### Leaderboards and surveys
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [Embedding Model Leaderboard March 2026](https://awesomeagents.ai/leaderboards/embedding-model-leaderboard-mteb-march-2026/)
- [Best Open-Source Embedding Models 2026 (BentoML)](https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models)
- [Best Embedding Models for IR 2025 (Dev.to)](https://dev.to/datastax/the-best-embedding-models-for-information-retrieval-in-2025-3dp5)
- [Top Embedding Models on MTEB (Modal)](https://modal.com/blog/mteb-leaderboard-article)

### Academic papers
- [Jasper and Stella: distillation of SOTA embedding models (2024)](https://arxiv.org/abs/2412.19048)
- [Citation importance-aware document representation learning (2025)](https://arxiv.org/abs/2512.13054)
- [GritLM: Generative Representational Instruction Tuning (2024)](https://arxiv.org/abs/2402.09906)
- [Jina Embeddings v3: Multilingual with Task LoRA (2024)](https://arxiv.org/abs/2409.10173)
- [Qwen3 Embedding technical report (2025)](https://arxiv.org/abs/2506.05176)
- [NV-Embed: Training LLMs as Generalist Embedding Models (2024)](https://arxiv.org/abs/2405.17428)
- [ModernBERT: Bringing BERT into modernity (2024)](https://huggingface.co/blog/modernbert)
- [SPECTER2: Adapting scientific document embeddings (2023)](https://allenai.org/blog/specter2)
- [On the Theoretical Limitations of Embedding-Based Retrieval (2025)](https://arxiv.org/abs/2508.21038)

### Hardware references
- [GTX 1080 Ti AI Benchmarks](https://gigachadllc.com/geforce-gtx-1080-ti-ai-benchmarks-breakdown/)
- [GPU Memory Size and Deep Learning Performance (Puget Systems)](https://www.pugetsystems.com/labs/hpc/gpu-memory-size-and-deep-learning-performance-batch-size-12gb-vs-32gb-1080ti-vs-titan-v-vs-gv100-1146/)
