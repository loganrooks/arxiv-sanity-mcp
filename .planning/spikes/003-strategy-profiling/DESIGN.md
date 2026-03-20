---
question: "What are the complete quality, resource, and behavioral profiles of every viable recommendation/filtering strategy — individually, in combination, and across user contexts — so that users can make informed configuration choices at install time?"
type: exploratory + comparative
status: complete
round: 1
linked_deliberation: deployment-portability.md
depends_on:
  - 001 (corpus, embeddings, B1 signal catalog, quality metrics, qualitative review)
  - 002 (backend tradeoffs, reference design latencies, pgvector measurements)
supersedes:
  - "Spike 003 (SPECTER2 adapter)" as originally planned in Spike 001 DECISION.md
  - Spike 001 Round 3 items C1-R10 through C1-R16 (subsumed into this design)
---

# Spike 003: Comprehensive Strategy Profiling

## Question

What are the complete quality, resource, and behavioral profiles of every viable recommendation and filtering strategy — individually, in combination, and across user contexts — so that at installation time, a user can understand exactly what they're getting, what trade-offs they're making, and what to expect from each configuration?

## Why This Matters

Spikes 001 and 002 tested strategies piecemeal: each experiment answered one question in isolation, using different evaluation protocols, at different scales, against different metrics. The result is a mosaic of findings that can't be directly compared. We know MiniLM and SPECTER2 capture different kinds of relatedness. We know TF-IDF is slower than embedding search above 50K papers. We know SVM filtering exists. But we can't answer: "If a user selects SPECTER2 + author boosting with 5 seed papers on a corpus of 50K papers using SQLite, what quality of recommendations can they expect, at what latency, using how much memory?"

That question — and every variant of it across the configuration space — is what this spike answers.

The output is not prose findings. It is a **strategy profile dataset**: structured data that code (an installer, a configuration wizard, documentation generators) can consume to present users with informed choices.

### What this feeds

1. **Interactive installer**: "Based on your hardware, interests, and preferences, we recommend..."
2. **Configuration documentation**: Per-strategy trade-off cards with measured numbers
3. **Recommendation system design**: Which strategies to offer, which combinations to pre-configure, what defaults to set
4. **The deployment deliberation**: Empirical foundation for concluding the tier model and architecture decisions

## Epistemic Landscape

We are navigating a high-dimensional uncertainty space. Being explicit about what we know, what we don't, what we can learn, and what we can't learn from experiments alone is critical for interpreting results correctly.

### What we know (with evidence)

| Claim | Evidence | Source |
|-------|----------|--------|
| MiniLM captures topical precision; SPECTER2 captures cross-community discovery | Qualitative review: 3 seeds, 15 papers each, AI-assessed | Spike 001 qualitative_review |
| No single strategy dominates across all evaluation frameworks | 12 strategies, category ground truth R@100 | Spike 001 C1 Round 3 |
| Topic purity 0.40 — categories partially align with topical structure | BERTopic on 19K papers | Spike 001 A2 |
| FWCI is the strongest non-tautological metadata signal (r=0.75 with citations) | 460-paper enrichment correlation analysis | Spike 001 B2 |
| Importance is multi-dimensional (bibliometric vs content vs structural) | Factor analysis on signal matrix | Spike 001 B3 |
| All strategies resource-feasible (1-13s GPU/day at 19K/month) | Resource projections from measured per-paper costs | Spike 001 C2 |
| FTS5 and tsvector return different papers (Jaccard 0.39) due to ranking functions | 20-query comparison with remediation | Spike 002 D1+R |
| pgvector HNSW is 5-23x faster than brute-force numpy, with recall >= 0.91 | Scale benchmark 5K-215K | Spike 002 D3 |
| All our operations are 20-100x faster than external APIs users know | Reference design comparison | Spike 002 D7 |
| Hybrid/adaptive systems dominate in production (55.56%) | Survey of 117 systems, 2019-2024 | Spike 001 B1 |
| mmap loading is near-instant (0.2ms open, 47ms first query for 472MB) | QV2 measurement | Spike 002 QV2 |

### What we don't know (open questions this spike addresses)

| Question | Why it matters | Current state |
|----------|---------------|---------------|
| What does SPECTER2 look like with the proper adapter? | Taints all SPECTER2 findings (~35% top-20 change) | Improperly loaded in all prior experiments |
| How do strategies compare on a common evaluation protocol? | Currently incomparable — different metrics, scales, seeds | No common protocol exists |
| What are the interaction effects between strategy combinations? | Combinations may be sub-additive, additive, or super-additive | Only OR-union tested (C1-R4) |
| How does strategy quality change with seed count? | Critical for cold-start UX | Designed (C1-R12) but never run |
| How does strategy quality change with interest breadth? | Different users have different information needs | Designed (C1-R13) but never run |
| How does bibliographic coupling compare to embedding similarity? | Different signal source, works for zero-citation papers | Designed (C1-R16) but never run |
| What does cross-encoder reranking add? | Multi-stage pipelines dominate in production (B1) | Never tested |
| How do API-based embeddings (OpenAI, Cohere) compare? | Users without GPU, cloud deployments | Never tested |
| What is the marginal value of adding each signal? | Determines optimal default configuration | Designed (C1-R14) but never run |
| How do strategies behave at different corpus sizes for quality (not just latency)? | Quality at scale may degrade differently per strategy | Latency at scale tested; quality only at 19K |
| Does the backend choice affect which strategy works best? | Backend × strategy interaction | Only keyword search compared across backends |

### What we can't know from experiments alone (design decisions)

These questions are informed by spike findings but resolved through architectural judgment, not more benchmarks:

1. **Default configuration**: Which strategy/combination ships as default? (Informed by profiles, decided by product values)
2. **Configuration granularity**: How many knobs should the user see? (Trade-off between power and simplicity)
3. **Per-project vs global profiles**: Should each research project have independent strategy config? (Informed by interest breadth findings)
4. **Adaptation rate**: How aggressively should the system learn from triage behavior? (Informed by cold-start data, decided by UX values)
5. **Explanation format**: How to present "why this paper?" to users (Informed by quality dimension findings, decided by design)
6. **Strategy naming**: User-facing labels for each strategy (e.g., "topical precision" vs "cross-community discovery")

### Epistemic hazards

These are ways our experiments could mislead us. Each has a mitigation built into the evaluation framework.

| Hazard | Description | Prior occurrence | Mitigation |
|--------|-------------|------------------|------------|
| **Circular evaluation** | Using embeddings to evaluate embedding-based strategies | sig-2026-03-19-circular-evaluation-bias: MiniLM tested on MiniLM-defined clusters | Leave-one-out on multiple cluster definitions; model-independent ground truth |
| **Proxy drift** | Metrics that track mathematical properties but not user relevance | sig-2026-03-19-measuring-wrong-thing-filtering: coverage against near-zero citations | Quality metrics defined before measurement; multiple proxies; qualitative review as cross-check |
| **Framework bias** | Evaluation framework design that systematically favors certain approaches | Caught 5 times in Spikes 001-002 | Pre-register predictions; test null hypothesis; rotate evaluation framework |
| **Synthetic scaling** | Duplicated data preserves vocabulary but not diversity at scale | All >19K benchmarks use 19K unique papers cycled | Report scale results with caveat; focus quality evaluation at 19K (real data) |
| **One month of data** | January 2026 may not represent typical arXiv distribution | Seasonal, conference deadline effects not captured | Acknowledge limitation; don't over-claim generalizability |
| **AI reviewer bias** | AI qualitative review may have systematic preferences | Unknown | Multiple review protocols; explicit rubric; identify disagreements |
| **Overfitting to seeds** | Strategy profiles may be sensitive to which seed papers are chosen | Unknown until tested | Multiple seed sets spanning different use cases; report variance across seeds |
| **SPECTER2 adapter uncertainty** | Proper adapter may not work as documented, or may have its own biases | Improper loading already caught; adapter behavior uncertain | Verify adapter output differs from base; sanity-check a few results manually |

### What the uncertainty structure looks like

```
                    KNOWN                          UNKNOWN
                      │                               │
   ┌──────────────────┼──────────────────┐            │
   │                  │                  │            │
Individual      Individual         Individual     Interaction
strategy        strategy           strategy       effects
LATENCY         QUALITY            QUALITY        between
(measured)      (proxy metrics     (human         strategies
                at 19K)            relevance)     at scale
   │                  │                  │            │
   │                  │                  │            │
   ▼                  ▼                  ▼            ▼
 CONFIDENT         PARTIALLY         UNKNOWABLE    TESTABLE
                   TESTABLE          (no human     (this spike)
                   (this spike       judges)
                   improves)
```

The fundamental epistemic limit: we have no human relevance judgments. All "quality" measurements are mathematical proxies. The best we can do is:
1. Use multiple complementary proxies (leave-one-out MRR, coherence, diversity, novelty, seed-relevance)
2. Use qualitative AI review as a cross-check
3. Be explicit about what each metric measures and doesn't measure
4. Design the output so users can make their own quality judgments once they start using the system

## Assumptions

Every assumption is marked with a confidence level and what would falsify it.

| ID | Assumption | Confidence | Falsified if | Impact if false |
|----|-----------|------------|-------------|----------------|
| A1 | Our 19K corpus from January 2026 is representative enough to profile strategies for other months/years | Medium | Strategy rankings change dramatically on a different month's data | Would need multi-month profiling |
| A2 | Leave-one-out MRR from BERTopic clusters is a reasonable relevance proxy | Medium | Strategies that rank high on MRR produce recommendations users don't find useful | Would need human evaluation |
| A3 | Quality metrics (coherence, diversity, novelty, seed-relevance) correlate with user-perceived quality | Low-Medium | Users prefer incoherent/undiversified recommendations (seems unlikely, but possible for narrow specialists) | Would need to redefine quality dimensions |
| A4 | Resource metrics scale linearly from 19K to larger corpora | High for compute, Medium for quality | Quality degrades non-linearly (likely for some strategies) | Would need measurements at multiple real corpus sizes |
| A5 | 460 OpenAlex-enriched papers are sufficient for enrichment-dependent strategies | Medium | Bibliographic coupling or FWCI-based strategies need denser enrichment to work | Would need to expand enrichment to 2000+ papers |
| A6 | AI qualitative review is informative for characterizing strategy behavior | Medium | AI systematically mischaracterizes relevance in ways that mislead strategy selection | Would need human review protocol |
| A7 | The evaluation framework doesn't systematically favor certain strategy types after our bias mitigations | Medium | Post-hoc analysis reveals persistent bias | Would need to redesign evaluation |
| A8 | Users' information needs can be approximated by seed papers + category selection | Medium | Users' needs are more contextual (project phase, deadline pressure, literature review vs monitoring) | Would need richer user models |
| A9 | Strategy quality profiles are stable across different random seed selections | Unknown (testable) | Variance across seed sets exceeds variance across strategies | Would need many more seed sets or different profiling approach |
| A10 | The `adapters` library correctly implements SPECTER2's proximity adapter | High (documented, but needs verification) | Output is identical to base model, or differs in unexpected ways | Would need to investigate SPECTER2 loading further |
| A11 | Qualitative review accumulates insight across waves — later reviews are informed by earlier ones | High (by design) | Reviews produce contradictory characterizations across waves, or Part 4 observations don't converge | Would need to re-examine review protocol or reviewer consistency |
| A12 | Emergent quality dimensions from Part 4 observations will be reusable across future evaluations | Medium | Dimensions are too context-specific to generalize | Dimensions are still useful for this spike; generalizability is a bonus |

## Strategy Taxonomy

Every strategy is categorized by signal source, compute profile, maturity, and what data it requires.

### Notation

- **Maturity**: `tested` (profiled in prior spikes), `designed` (protocol exists, not run), `new` (first appearance)
- **Compute**: `trivial` (<1ms/query), `light` (<50ms/query), `moderate` (<500ms/query), `heavy` (>500ms/query or API cost)
- **Data needed**: what must exist before the strategy can operate

### S1. Content-Based Retrieval

These strategies operate on the text content of papers (title, abstract, or both).

| ID | Strategy | Signal | Compute | Maturity | Data needed |
|----|----------|--------|---------|----------|-------------|
| S1a | MiniLM embedding similarity | Semantic similarity via all-MiniLM-L6-v2 (384-dim) | Light (16ms at 215K brute-force; 0.8ms with HNSW) | Tested | Pre-computed embeddings |
| S1b | SPECTER2 embedding similarity (base) | Semantic similarity via SPECTER2 without adapter (768-dim) | Light (est. 32ms at 215K brute-force) | Tested (but baseline for comparison) | Pre-computed embeddings |
| S1c | SPECTER2 embedding similarity (adapter) | Citation-graph-informed proximity via SPECTER2 + proximity adapter | Light (est. 32ms at 215K) | **New** — this is the critical fix | Pre-computed embeddings (with adapter) |
| S1d | TF-IDF cosine similarity | Lexical overlap in abstract terms | Moderate (516ms at 215K; <100ms pre-filtered) | Tested (latency only) | Pre-computed TF-IDF matrix |
| S1e | BM25 / keyword search (FTS5) | Term matching with BM25-variant ranking | Light (30ms at 215K) | Tested | FTS5 index |
| S1f | BM25 / keyword search (tsvector) | Term matching with cover-density ranking | Light (101ms at 215K) | Tested | tsvector + GIN index |
| S1g | Title-only embedding (MiniLM) | Title semantic similarity (cheaper, more focused) | Light | **New** | Pre-computed title embeddings |
| S1h | Title-only embedding (SPECTER2+adapter) | Title citation-proximity | Light | **New** | Pre-computed title embeddings |
| S1i | SVM on user library (arxiv-sanity approach) | Per-user learned classifier over TF-IDF features | Light (prediction is fast; training ~2s) | Tested (basic, C1-R3) | TF-IDF matrix + user library (>=5 papers) |
| S1j | Embedding centroid of saved papers | Mean embedding of user's saved papers, then similarity search | Trivial (one dot product per paper) | **New** | Embeddings + user library |
| S1k | API embeddings (OpenAI text-embedding-3-small) | High-quality general embeddings via API | Heavy (API cost ~$0.02/1M tokens) | **New** | API key + budget |
| S1l | API embeddings (Cohere embed-v3) | Academic-tuned embeddings via API | Heavy (API cost, similar to OpenAI) | **New** | API key + budget |

**ASSUMPTION A10 critical for S1c.** If the adapter doesn't load correctly, S1c degrades to S1b and we lose the comparison.

**Cost estimation needed for S1k, S1l.** Before profiling API embeddings, estimate: cost to embed 19K papers, cost per query, whether a small sample (100 papers) is sufficient for quality comparison.

### S2. Metadata-Based Signals

These strategies use paper metadata without reading content.

| ID | Strategy | Signal | Compute | Maturity | Data needed |
|----|----------|--------|---------|----------|-------------|
| S2a | Category filtering (primary) | Only papers matching user's primary categories | Trivial | Implicit (tested as baseline) | Category config |
| S2b | Category filtering (listed) | Papers listed in user's categories (broader) | Trivial | Tested (A2 co-occurrence) | Category config |
| S2c | Category co-occurrence boost | Papers in categories that frequently co-occur with user's | Light | **New** | Category co-occurrence matrix (from A2) |
| S2d | FWCI ranking | Rank by field-weighted citation impact | Trivial | Correlation only (B2) | OpenAlex enrichment |
| S2e | Citation count ranking | Rank by raw cited_by_count | Trivial | Correlation only (B2) | OpenAlex enrichment |
| S2f | Author network (co-author) | Papers by co-authors of user's seed paper authors | Light | Tested (R@100 category ground truth) | Author extraction from metadata |
| S2g | Followed author boost | Rank boost for papers by user's followed authors | Trivial | Tested (C1-R2 basic) | User's followed_author signals |
| S2h | Author h-index ranking | Rank by max author h-index (prestige signal) | Light | Correlation only (B2) | OpenAlex enrichment with authorship |
| S2i | OpenAlex topic matching | Papers with matching OpenAlex topic IDs | Light | **New** | OpenAlex enrichment with topics |
| S2j | Recency decay | Exponential or linear decay from submission date | Trivial | **New** | Submission dates (already have) |
| S2k | Version update signal | Papers with recent version updates (active revision) | Trivial | **New** | Version history (already have) |
| S2l | Reference count signal | Papers with many references (survey-like, well-grounded) | Trivial | Correlation only (B2, r=0.20) | OpenAlex enrichment |
| S2m | Cross-listing breadth | Papers listed in many categories (interdisciplinary) | Trivial | **New** | Category data (already have) |

### S3. Graph-Based Signals

These strategies use citation or reference graph structure.

| ID | Strategy | Signal | Compute | Maturity | Data needed |
|----|----------|--------|---------|----------|-------------|
| S3a | Bibliographic coupling | Jaccard of reference lists (papers sharing references are related) | Moderate | Designed (C1-R16), never run | OpenAlex referenced_works for both papers |
| S3b | Co-citation | Papers frequently cited together (requires citers' reference lists) | Heavy | **New** — may not be feasible | Would need to fetch reference lists of citing papers |
| S3c | OpenAlex related_works | Pre-computed relatedness from OpenAlex's graph | Light (one API call) | **New** | OpenAlex related_works field (already in enrichment schema) |

**ASSUMPTION A5 critical for S3a.** Bibliographic coupling needs referenced_works for many papers. Currently 460 enriched. May need expansion.

**S3b feasibility check needed.** Co-citation requires knowing which papers cite our papers AND what else those citing papers cite. This may require too many API calls for January 2026 papers (which have few citations). Flag as potentially infeasible.

### S4. Multi-Stage Pipelines

These combine a cheap retrieval stage with an expensive reranking stage.

| ID | Strategy | Retriever → Reranker | Compute | Maturity | Data needed |
|----|----------|---------------------|---------|----------|-------------|
| S4a | Embedding retrieve + cross-encoder rerank | S1a/S1c → cross-encoder (e.g., ms-marco-MiniLM-L-6-v2) | Heavy per candidate (~50ms each) | **New** | Cross-encoder model |
| S4b | Keyword retrieve + embedding rerank | S1e/S1f → S1a/S1c | Light + Light | Designed (C1-R11) | Both indexes |
| S4c | Embedding retrieve + FWCI/citation rerank | S1a/S1c → S2d/S2e | Light + Trivial | **New** | Embeddings + enrichment |
| S4d | Keyword retrieve + SVM rerank | S1e/S1f → S1i | Light + Light | **New** | FTS index + TF-IDF matrix |
| S4e | Category pre-filter + embedding search | S2a/S2b → S1a/S1c | Trivial + Light | **New** (QV1 tested latency, not quality) | Category config + embeddings |
| S4f | Embedding retrieve + LLM rerank | S1a/S1c → LLM relevance scoring (top-20 only) | Heavy ($0.01-0.05 per rerank) | **New** | API key + budget |

**LLM reranking (S4f) is expensive.** Only viable on the final top-20, not as a general strategy. Profile cost carefully. A single research session might rerank 5 sets of 20 = 100 papers at ~$0.50-2.50.

### S5. Ensemble / Combination Methods

These combine multiple strategy scores into one ranking.

| ID | Strategy | Method | Compute | Maturity | Data needed |
|----|----------|--------|---------|----------|-------------|
| S5a | Reciprocal Rank Fusion (RRF) | 1/(k+rank) across strategies, sum | Trivial (post-retrieval) | Tested (category ground truth only) | Multiple strategy rankings |
| S5b | Weighted linear combination | w1*score1 + w2*score2 + ... | Trivial (post-retrieval) | **New** | Normalized scores + weights |
| S5c | Strategy union + dedup (highest score) | Union of top-K from each, dedup by max score | Trivial | Tested (C1-R4 basic) | Multiple strategy rankings |
| S5d | Cascading pipeline with early exit | Cheap strategy eliminates, expensive strategy ranks survivors | Varies | **New** | Multiple strategies |
| S5e | Consensus boosting | Papers found by 2+ strategies get a badge/boost | Trivial | Qualitative only (from review) | Multiple strategy rankings |
| S5f | Per-project learned weights | Each project learns optimal w1...wN from user triage behavior | Light (retrain is fast) | **New** | Triage data (simulated) |

### S6. Baselines

These are essential calibration points.

| ID | Strategy | What it measures | Compute |
|----|----------|-----------------|---------|
| S6a | Random | Lower bound. Any strategy should beat this. | Trivial |
| S6b | Most recent | Recency only. Upper bound for "I just want new papers." | Trivial |
| S6c | Most cited (OpenAlex) | Popularity only. Tests whether prestige alone is useful. | Trivial |
| S6d | Same primary category | Category matching only. Baseline for all content-based strategies. | Trivial |

### Strategy count

- Content-based: 12 (S1a-S1l)
- Metadata-based: 13 (S2a-S2m)
- Graph-based: 3 (S3a-S3c)
- Multi-stage: 6 (S4a-S4f)
- Ensemble: 6 (S5a-S5f)
- Baselines: 4 (S6a-S6d)
- **Total: 44 strategies**

Not all 44 need full profiling. The experiment design below triages which get full treatment vs. screening.

## Configuration Space

For each strategy, these are the "knobs" that can be varied. The spike should measure sensitivity to each knob to determine: which knobs matter (and should be exposed to users) and which don't (and should be set to a good default).

### Per-strategy configuration dimensions

| Dimension | Strategies affected | Values to test | Why it matters |
|-----------|-------------------|----------------|---------------|
| **Feature input** | S1a-S1l, S1i | title-only, abstract-only, title+abstract | Determines what content the strategy "sees." Title is cheaper. Abstract is richer. Combined may be noisy. |
| **Top-K threshold** | All retrieval strategies | 10, 20, 50, 100, 200, 500 | Aggressiveness slider. More candidates = more recall but lower precision. |
| **Similarity metric** | S1a-S1h, S1j-S1l | cosine, dot product, euclidean | Usually cosine and dot product are equivalent for normalized embeddings, but verify. |
| **Embedding quantization** | S1a-S1h | float32, float16, int8 | Affects memory and speed. Does quality degrade? |
| **HNSW parameters** | S1a (pgvector) | m: 16/32, ef_construction: 64/128, ef_search: 40/100/200 | Index build cost vs recall trade-off. Default params may not be optimal. |
| **TF-IDF vocabulary** | S1d, S1i | default, max_20k, max_50k, pruned | Spike 001 A1c.1 showed minimal effect. Confirm in quality evaluation. |
| **SVM regularization** | S1i | C: 0.001, 0.01, 0.1, 1.0 | Controls overfitting. arxiv-sanity-lite uses C=0.01. |
| **SVM training set size** | S1i | 5, 10, 20, 50, 100 "liked" papers | Cold start sensitivity. |
| **Keyword query expansion** | S1e, S1f | raw query, stemmed, with synonyms | Whether preprocessing helps keyword strategies. |
| **Recency decay rate** | S2j | half-life: 7 days, 30 days, 90 days, 365 days | How much to penalize older papers. |
| **FWCI normalization** | S2d | raw, log-transformed, percentile-rank | FWCI is highly skewed; normalization method affects ranking. |
| **Author threshold** | S2f, S2g | followed: top-5/10/20, prolific: >=3/5/10 papers | How selective the author signal is. |
| **Bibliographic coupling normalization** | S3a | raw Jaccard, min-normalized, max-normalized | Affects whether papers with many references dominate. |
| **Retriever top-K for reranking** | S4a-S4f | 50, 100, 200, 500 | How many candidates the reranker sees. More = better recall but slower. |
| **Cross-encoder model** | S4a | ms-marco-MiniLM-L-6-v2, ms-marco-MiniLM-L-12-v2 | Model size vs quality. |
| **RRF k parameter** | S5a | 10, 30, 60, 100 | Controls how much top-rank positions dominate. |
| **Ensemble weights** | S5b, S5f | Equal, content-heavy, metadata-heavy, learned | The core question for combination strategies. |

**Prioritization**: Not every strategy × config combination is worth testing. The experiment design uses a **screening phase** (test each strategy at default config) followed by **sensitivity analysis** (vary configs only for strategies that pass screening).

## Context Dimensions

These are variables external to the strategy that change which strategy works best. They represent different user situations.

| Dimension | Values | Why it matters | How we simulate |
|-----------|--------|---------------|----------------|
| **Seed count** (cold start) | 1, 3, 5, 10, 20 | First-use experience. Some strategies need many seeds; others work with 1. | Vary seed set size, measure quality |
| **Interest breadth** | Narrow (1 BERTopic cluster), Medium (2-3 clusters), Broad (5+ clusters) | Different users: specialist vs surveyor vs interdisciplinary explorer | Define interest profiles by cluster membership |
| **Corpus size** | 5K, 19K, 50K (quality only — not just latency) | Quality may degrade differently per strategy at scale | Use duplicated corpus with different random subsets as seeds |
| **Paper freshness** | All papers < 60 days, mix of new + established | Citation signals useless for new papers; embedding signals work regardless | Filter corpus by date range |
| **Backend** | SQLite + numpy, PostgreSQL + tsvector, PostgreSQL + pgvector | Backend affects keyword search results (FTS5 ≠ tsvector) and vector search speed | Run evaluation on each backend |
| **Hardware profile** | CPU-only (simulated by disabling GPU), GPU (current hardware) | Affects compute cost and which strategies are practical | Measure with and without GPU |
| **Negative signals** | None, 5 "not interested" papers, 20 "not interested" papers | Whether negative feedback improves or distorts recommendations | Add negative signals, re-evaluate |

### Interest profiles for evaluation

We need 5-10 well-defined interest profiles spanning different use cases. Each profile consists of seed papers + a description of what "good" recommendations look like.

| Profile | Description | Seed source | Breadth | Expected character |
|---------|-------------|-------------|---------|-------------------|
| P1 | RL for robotics | Papers from BERTopic cluster(s) matching "reinforcement learning" + "robotics" | Medium | Methodological focus, specific application domain |
| P2 | Language model reasoning | Papers on LLM reasoning, chain-of-thought, etc. | Medium | Hot topic, high volume, many tangential papers |
| P3 | Quantum computing / quantum ML | Cross-domain: physics + CS | Narrow | Small community, distinctive vocabulary |
| P4 | AI safety / alignment | Broad, cross-cutting concern touching many subfields | Broad | Many relevant papers scattered across categories |
| P5 | Graph neural networks | Specific methodology, multiple applications | Medium | Well-defined subfield, clear boundaries |
| P6 | Diffusion models for generation | Trending, fast-moving | Medium | Recent papers dominate; older work is foundational |
| P7 | Federated learning + privacy | Cross-domain: ML + security/privacy | Medium | Dual-focus interest |
| P8 | Mathematical foundations of neural networks | Narrow, theoretical | Narrow | Distinctive formal vocabulary |

**Seed selection protocol**:
1. For each profile, identify relevant BERTopic clusters from A2
2. Select 20 papers from those clusters that a domain expert would recognize as on-topic (using title/abstract)
3. These 20 are the "full seed set." For cold-start experiments, use subsets of 1, 3, 5, 10, 20.
4. Hold out 5 papers for leave-one-out evaluation (never used as seeds)

**ASSUMPTION A9**: Strategy profiles should be stable across different random selections of seeds from the same interest area. If variance across seed selections exceeds variance across strategies, the profiling is uninformative.

**Mitigation**: For each interest profile, run with 3 different random seed selections. Report mean and variance.

## Evaluation Framework

### On the relationship between measurement and evaluation

Quantitative metrics and qualitative review serve different epistemological functions. Conflating them — or treating one as subordinate to the other — produces bad evaluation. Every evaluation methodology embodies epistemological commitments whether we name them or not. This section names ours.

**Quantitative instruments detect properties.** They produce readings: numbers that track mathematical relationships within recommendation sets. "Coherence: 0.52" tells us a property of the embedding space. It does NOT tell us whether the recommendation set is good, useful, or what a researcher would want. That interpretation requires judgment — context about what the researcher is trying to do, what "coherent" means for their situation, whether coherence is even desirable here.

**Qualitative review provides interpretive context.** It is the horizon of meaning within which instrument readings become significant. The Spike 001 qualitative review didn't produce numbers — it produced the insight that "quality" decomposes into topical precision, methodological kinship, and discovery potential. No metric captured that. But the insight reframes what all the metrics mean going forward.

**Neither determines alone; they are co-constitutive.** Metrics detect patterns at scale, flag anomalies, enable systematic comparison. Qualitative review tells us what patterns mean, whether metrics are measuring what we think, and surfaces dimensions the metrics miss. When they disagree, that disagreement is the most valuable signal — it means either the instrument is reaching its limits or the interpretive framework needs revision. Both are productive.

**On "relevance" specifically:** Relevance is not a property of a paper. It is a relation between a paper, a person, a purpose, and a moment. A paper doesn't *have* relevance sitting there waiting to be measured — it *shows up as* relevant within a researcher's particular engagement with their work. The same paper is relevant to researcher A (shared method), irrelevant to researcher B (wrong domain), and will become relevant to researcher B next month when they pivot. Relevance is also not one dimension — a paper can be relevant because it answers your question, provides a tool you need, challenges your assumptions, maps adjacent territory, or introduces you to a community working on the same problem in different language. These are different kinds of connection, partially incommensurable — they are not points on a single scale but distinct modes of relation. No number captures this plurality. What a number CAN do is detect statistical regularities across many papers — patterns that, once interpreted within a framework of understanding, help us characterize HOW a strategy thinks about "related."

**On metrics as situated instruments:** Our metrics embody theories about what matters. Leave-one-out MRR embodies the theory that a good strategy recovers papers from known-coherent groups. Seed proximity embodies the theory that good recommendations are similar to what you've already liked. Novelty embodies the theory that good recommendations take you somewhere new. These theories partially conflict — and they should, because different users need different things. The metrics don't resolve the conflict; they map its shape. The qualitative review, informed by the interest profile's specific context, interprets which theory (which metric) is most appropriate for which situation.

This means: our quantitative metrics are **detection instruments**, not **evaluation criteria**. They tell us what a strategy does. The qualitative review tells us what that means. Strategy profile cards must carry both: the instrument readings provide the systematic, comparable data; the qualitative characterization provides the interpretive context that makes those readings meaningful. Instrument readings without situated interpretation are presented as what they are — numbers awaiting context — never as judgments.

#### How interpretation is made explicit

Every instrument reading in the strategy profile card is accompanied by an **interpretation field** that situates the number:

```json
{
  "coherence": {
    "value": 0.52,
    "context": "For narrow interest profiles (P3, P8), 0.52 indicates tight topical focus — appropriate for specialists. For broad profiles (P4), the same value would indicate over-focusing that misses relevant cross-domain work. Compare: S1a produces 0.38 on the same profiles, which qualitative review characterized as 'creative exploration' rather than 'poor coherence.'",
    "by_profile": {
      "P1": {"value": 0.49, "interpretation": "..."},
      "P3": {"value": 0.58, "interpretation": "..."}
    }
  }
}
```

This ensures that no metric value is ever presented as a bare number. The interpretation field is populated from qualitative review findings and cross-strategy comparison — it is the interpretive layer that connects the instrument reading to a framework of meaning.

### Quantitative detection instruments

These metrics detect properties of recommendation sets. Each measures a specific mathematical relationship. The "what it doesn't measure" column is as important as the "what it measures" column — it defines the boundary of the instrument's reach.

| Instrument | What it detects | How it works | What it cannot detect |
|------------|----------------|-------------|---------------------|
| **Leave-one-out MRR** | Whether a strategy can recover a paper from a known-coherent set | Hold out each paper from a cluster. Use remaining as seeds. Measure rank of held-out paper. | Whether the strategy finds papers the user doesn't already know about. Rewards convergence toward known good papers, blind to genuinely novel discovery. |
| **Seed proximity** | Mathematical similarity between recommendations and seed centroid | Mean cosine similarity between each recommended paper's embedding and the seed embedding centroid. | Whether high similarity is what the user wants. A researcher exploring a new area needs distance from seeds, not proximity. |
| **Topical coherence** | Internal consistency of the recommendation set | Mean pairwise cosine similarity within the recommended set. | Whether coherence is desirable. High coherence can mean "focused" or "echo chamber" depending on context. |
| **Cluster diversity** | Whether recommendations span multiple topical regions | Number of distinct BERTopic clusters represented in top-K. | Whether diversity is breadth (good) or noise (bad). Spanning many clusters is meaningless if the extra clusters are irrelevant. |
| **Novelty** | Whether recommendations leave the seeds' immediate neighborhood | Fraction of recommended papers NOT in the same BERTopic cluster as any seed. | Whether novel papers are relevant. Novelty without relevance is noise. Novelty with relevance is discovery. The metric can't distinguish. |
| **Category surprise** | Whether recommendations cross arXiv category boundaries | Fraction of recommended papers from a different primary_category than seeds. | Whether the category crossing is meaningful. cs.LG → cs.CV is a small step; cs.LG → math.CO is a large one. The metric treats them equally. |
| **Coverage** | Fraction of a pre-defined "relevant" set that appears in recommendations | Of papers in the same BERTopic clusters as seeds, what fraction appears in top-K. | What "relevant" actually means. Coverage is defined against cluster membership, which is itself a mathematical proxy. |

**Metric tensions**: These instruments pull in opposite directions. Seed proximity and novelty are inversely correlated. Coherence and diversity are inversely correlated. No strategy should maximize all instruments simultaneously. The instruments characterize WHERE on these tension curves each strategy sits — the qualitative review interprets whether that position serves a particular user's needs.

**When instruments mislead**: Every instrument has failure modes. Leave-one-out MRR rewards strategies that converge toward cluster centers, penalizing strategies that find relevant papers the cluster definition misses. Seed proximity penalizes exploration. Coherence penalizes breadth. These aren't flaws to fix — they're inherent limitations of any instrument. The mitigation is not better instruments but honest interpretation of what the instruments detect.

**Model-independence requirement**: Leave-one-out clusters must be defined using BOTH embedding models (MiniLM and SPECTER2) plus BERTopic topics. If a paper is in the same cluster under all three, it is "strongly related." This avoids circular evaluation where an embedding model evaluates itself.

### Resource metrics

| Metric | What it measures | How to compute |
|--------|-----------------|----------------|
| **Query latency** (p50, p95) | Time from "give me recommendations" to "here they are" | Benchmark over 100 queries with warmup |
| **Index/setup time** | One-time cost to prepare the strategy's data structures | Measure: TF-IDF build, embedding computation, HNSW index, etc. |
| **Incremental update cost** | Cost to incorporate one new paper | Measure: re-embed, update index, retrain SVM, etc. |
| **Memory footprint** | RAM required during operation | Measure: matrix sizes, model sizes, index sizes |
| **Storage footprint** | Disk space for persisted data | Measure: file sizes, database growth |
| **API cost** (if applicable) | Dollar cost per paper or per query | Calculate from API pricing |
| **GPU requirement** | Whether GPU is needed for acceptable performance | Test with and without GPU; report latency ratio |

### Evaluation protocol

For each strategy × config, the evaluation produces a **strategy profile card**:

```json
{
  "strategy_id": "S1c",
  "strategy_name": "SPECTER2 embedding similarity (with adapter)",
  "config": {
    "feature_input": "abstract",
    "top_k": 20,
    "similarity_metric": "cosine"
  },
  "instruments": {
    "leave_one_out_mrr": {
      "mean": 0.35, "std": 0.08,
      "interpretation": "Moderate recovery rate. Finds known-relevant papers about 1/3 of the time in the top-3 results. Weaker than MiniLM (0.42) on narrow profiles where vocabulary matching suffices, but comparable on broad profiles where citation-network proximity adds value the vocabulary misses.",
      "by_profile": {"P1": {"value": 0.38, "interpretation": "..."}, "...": "..."}
    },
    "seed_proximity": {
      "mean": 0.52, "std": 0.06,
      "interpretation": "Moderate distance from seeds — recommendations share conceptual territory but don't cluster tightly around the seed centroid. Qualitative review characterized this as 'adjacent community exploration' rather than 'poor matching.'",
      "by_profile": {"...": "..."}
    },
    "coherence": {
      "mean": 0.41, "std": 0.05,
      "interpretation": "Lower internal consistency than MiniLM (0.52). For narrow profiles this reads as unfocused; for broad profiles it reads as appropriate breadth. The number is the same — what it means depends on what the researcher needs.",
      "by_profile": {"...": "..."}
    },
    "diversity": {
      "mean": 3.2, "std": 0.7,
      "interpretation": "Spans ~3 topical clusters on average. Qualitative review found this diversity is meaningful (adjacent research communities) not noisy (random scatter).",
      "by_profile": {"...": "..."}
    },
    "novelty": {"mean": 0.35, "std": 0.10, "interpretation": "...", "by_profile": {"...": "..."}},
    "surprise": {"mean": 0.22, "std": 0.08, "interpretation": "...", "by_profile": {"...": "..."}},
    "coverage": {"mean": 0.15, "std": 0.04, "interpretation": "...", "by_profile": {"...": "..."}}
  },
  "resources": {
    "query_latency_ms": {"p50": 32, "p95": 45},
    "index_time_s": 180,
    "incremental_update_ms": 1.7,
    "memory_mb": 630,
    "storage_mb": 560,
    "api_cost_per_paper": null,
    "gpu_required": false,
    "gpu_speedup": 20.0
  },
  "qualitative": {
    "character": "Cross-community discovery. Finds papers from adjacent research communities that use different vocabulary for related problems. Higher novelty and surprise than MiniLM, lower coherence. Best for interdisciplinary exploration.",
    "feels_like": "A colleague who works in a neighboring lab — recommends papers you wouldn't search for but often find valuable.",
    "best_for": ["broad interests", "interdisciplinary exploration", "finding unknown unknowns"],
    "worst_for": ["narrow technical search", "cold start with 1 seed"],
    "false_positive_pattern": "Community neighbors: papers from the same research community but addressing a different problem. Harder to spot than vocabulary squatters.",
    "failure_mode": "With too few seeds, latches onto the dominant research community around the seed rather than the seed's specific question.",
    "strengths": ["Surfaces papers using different vocabulary for the same problem", "Captures citation-network proximity even for zero-citation papers"],
    "gaps": ["Misses papers that are methodologically similar but from distant communities", "Blind to very recent work not yet embedded in citation structure"],
    "emergent_observations": [
      "Three dimensions of quality emerged: topical precision, methodological kinship, discovery potential. SPECTER2 optimizes for discovery potential.",
      "Consensus papers (agreed by both MiniLM and SPECTER2) have higher category overlap with seed (0.40 vs 0.32) — consensus may indicate a different kind of relevance."
    ],
    "metric_divergences": [
      "Coherence metric understates quality for broad interest profiles — low coherence is a feature (breadth), not a bug."
    ],
    "review_sources": ["W1 characterization: P1, P3, P4", "W3 blind comparison vs S1a"],
    "reviewer_confidence": "Medium — AI review; no domain expert validation"
  },
  "cold_start_minimum_seeds": 3,
  "complements": ["S1a (MiniLM)", "S2g (followed author)"],
  "conflicts": [],
  "evaluation_caveats": ["SPECTER2 adapter loading verified", "Quality metrics are proxy-based"]
}
```

### Qualitative Review Protocol

Quantitative metrics tell us WHAT a strategy does numerically. Qualitative review tells us what it FEELS LIKE to receive those recommendations — whether the papers are genuinely interesting, whether the misses are painful, whether the false positives are obvious or subtle, and whether the strategy surfaces things the researcher wouldn't have found otherwise.

The Spike 001 qualitative review produced the most important finding of the entire spike program: that "quality" decomposes into three dimensions (topical precision, methodological kinship, discovery potential) that no quantitative metric captured. That insight emerged because the review protocol created space for observations beyond predefined categories. This spike elevates qualitative review from a final-wave cross-check to a **first-class evaluation method integrated throughout the experiment waves**.

#### When qualitative review happens

| Wave | Review point | Purpose |
|------|-------------|---------|
| W1 (Screening) | After all individual strategies profiled | Characterize each strategy's recommendation "personality." Identify failure modes not visible in metrics. |
| W3 (Combinations) | After best pairwise combinations identified | Do combinations actually feel better? Does consensus boosting work as intended? |
| W4.1 (Cold start) | At seed count = 1 and seed count = 3 | Is the cold-start experience tolerable? Are recommendations useful or garbage? |
| W5.4 (Final) | Top 3 recommended configurations | Final validation. Does the installer's "recommended config" actually produce good recommendations? |

#### Review structure

Each qualitative review session evaluates a **recommendation set** (typically top-20 papers from a strategy) in the context of an **interest profile** (the seed papers defining what the user cares about). The review uses a structured template with both rubric-scored dimensions and open-ended observation fields.

The agent reviewer receives:
1. The seed papers (titles + abstracts) — establishing what the "researcher" is interested in
2. The recommended papers (titles + abstracts) — what the strategy surfaced
3. The strategy identity is withheld for blind reviews where possible (comparing strategies), or disclosed when characterizing a single strategy's behavior

#### Review Template

```markdown
# Qualitative Review: [Strategy ID] for [Profile ID]

## Context
- **Seeds**: [titles of seed papers]
- **Strategy**: [disclosed or "Strategy A" for blind comparison]
- **Config**: [top-K, etc.]
- **Date**: [review date]

## Part 1: Per-Paper Assessment

For each of the top-20 recommended papers, write a short assessment that addresses
three dimensions. Do NOT reduce these to numbers. The point is to articulate
the nature of the connection (or lack thereof) between the paper and the seeds,
not to rank papers on a scale.

For each paper:

```
### Paper [#]: [Title]

**Connection to seeds**: [Describe the relationship. What connects this paper to
the research interest? Is it the same question, the same method, the same community,
the same vocabulary, or something else? If there's no real connection, say so and
explain what might have caused the strategy to surface it.]

**What a researcher would get from this**: [If a researcher read this paper, what
would they gain? A new technique? An alternative framing? Empirical results on
a related question? Context from an adjacent field? Nothing useful?]

**Discoverability**: [How likely is the researcher to find this paper without the
recommendation? Would keyword search surface it? Is it in the obvious citation
chain? Or does it use different vocabulary, sit in a different community, or approach
the problem from an angle the researcher wouldn't think to search for?]

**Tension or surprise**: [Optional. Flag anything interesting: a paper that is
relevant but in a way the seed papers wouldn't predict. A paper that challenges
the seeds' assumptions. A paper that is technically on-topic but feels like it
belongs to a different conversation. A paper where relevance and surprise pull
in opposite directions.]
```

**Why narrative over numbers**: A paper about "attention mechanisms in protein
folding" might be highly relevant to a researcher studying attention mechanisms
(shared method) OR irrelevant (wrong domain) depending on whether their interest
is the mechanism itself or its application to NLP. The number 3/5 collapses this
context. The narrative preserves it — and more importantly, it forces the reviewer
to articulate the nature of the connection, which is the actual data we need for
characterizing the strategy.

**Efficiency note**: Not every paper needs a long assessment. For clearly relevant
or clearly irrelevant papers, a single sentence suffices ("Directly extends the
seed's approach to a new setting" or "Vocabulary match only — different research
question"). Reserve longer assessments for papers where the judgment is interesting
— the ambiguous cases, the surprising connections, the subtle false positives.
These are where strategy character is revealed.

## Part 2: Set-Level Assessment

### Overall character
[In 2-3 sentences: what KIND of recommendations does this strategy produce?
Is it a "more of the same" recommender or a "broaden your horizons" recommender?
Does it feel like a knowledgeable colleague's suggestions or a keyword search?]

### Strengths
[What does this recommendation set do well? What kinds of papers does it find
that a researcher would value?]

### Gaps
[What's missing? What papers should be here but aren't? What kind of relevant
work is this strategy blind to?]

### False positive pattern
[What do the irrelevant recommendations have in common? Are they vocabulary
squatters (share words, not ideas)? Community neighbors (same field, wrong problem)?
Generic popular papers? Something else?]

### Failure modes
[If this strategy fails, HOW does it fail? Is the failure obvious (clearly
irrelevant results) or subtle (plausible-looking but actually off-target)?]

## Part 3: Comparative Assessment (when comparing strategies)

[Only included when reviewing 2+ strategies on the same profile.]

### What each strategy found that the other missed

[For each strategy, identify 1-3 papers that are unique to its recommendation set
and describe WHY this strategy found them and the other didn't. What does this
reveal about how each strategy thinks about "related"?

This is more revealing than "best unique find" as a label — we want to understand
the LOGIC of each strategy's selections, not just rank the outputs.]

### Where they agree and what agreement means

[Identify papers that appear in both recommendation sets. Are the consensus papers
a particular kind of paper — safer, more central, more obvious? Or are they
genuinely the strongest recommendations by both strategies' different logics?
What does the overlap (or lack of it) tell us about whether these strategies
are capturing the same thing or different things?]

### The character of each strategy's errors

[Each strategy produces false positives — papers that aren't actually useful.
Describe what each strategy's false positives look like and what they tell us
about the strategy's blind spots. A strategy that produces "vocabulary squatters"
(shares words, not ideas) has a different failure mode than one that produces
"community neighbors" (same field, wrong problem), and the distinction matters
for knowing when to trust each strategy.]

### If a researcher could only use one

[For this specific interest profile: which strategy would better serve the
researcher, and why? Under what circumstances would you change your answer?
Be specific — "if the researcher is surveying a new field" or "if they're
looking for methods to apply" or "if they're writing a related work section."
The answer should be contextual, not absolute.]

## Part 4: Emergent Observations

[THIS SECTION IS THE MOST IMPORTANT.

This is where findings that exceed the predefined categories go. The Spike 001
discovery that quality has three dimensions (topical precision, methodological
kinship, discovery potential) came from open-ended observation, not from the rubric.

Prompts (use any or none — these are starting points, not constraints):
- Did any recommended paper change how you understand the interest profile?
- Did the recommendation set reveal a sub-community or approach you hadn't considered?
- Is there a pattern in the recommendations that suggests the strategy "thinks"
  about relatedness in a specific way?
- Did you notice something about the seeds themselves when reviewing the
  recommendations? (Sometimes recs reveal what's distinctive about the seeds.)
- Does this strategy surface a type of paper that none of the metrics would capture?
- Is there a quality dimension that the rubric above fails to measure?
- Were there papers rated 2 on relevance but 5 on surprise (or vice versa) —
  and what does that tension tell us?
- Did any paper make you reconsider what "relevant" means for this profile?]

## Part 5: Metric Divergence

[Flag cases where your qualitative impression contradicts the quantitative metrics.

Examples:
- "Metrics say coherence is 0.55 (high), but the set doesn't feel coherent —
  the papers are similar to each other but not to the seeds."
- "MRR is low but the recommendations are actually good — the strategy finds
  DIFFERENT relevant papers than the leave-one-out set expects."
- "Diversity score is high but it feels like noise, not breadth."

These flags are crucial. They indicate where our metrics are measuring the
wrong thing — which is exactly the epistemic hazard we need to catch.]
```

#### Review protocol variants

Different review situations call for different protocols:

| Variant | When to use | What changes |
|---------|------------|-------------|
| **Single-strategy characterization** | Wave 1 screening | Strategy identity disclosed. Focus on Parts 1, 2, 4. No Part 3. |
| **Blind pairwise comparison** | Wave 3 combinations, W4 context | Strategy identity withheld ("A" vs "B"). Focus on Parts 1, 3, 4. |
| **Cold-start review** | Wave 4.1 (seed count 1 and 3) | Modify rubric: add "Would this recommendation help the user refine their interest?" (1-5). Cold-start recs serve a different purpose — bootstrapping, not serving. |
| **Configuration comparison** | Wave 2 sensitivity | Same strategy, different config. Focus on: "What changed? Is the difference visible in the papers, or only in the metrics?" |
| **Combination vs components** | Wave 3.6 consensus | Review consensus papers, A-exclusive, B-exclusive separately. "Is the consensus set actually better, or just the intersection of two decent sets?" |

#### Aggregation across reviews

Individual reviews produce rich qualitative data. Aggregation produces strategy characterizations:

1. **Per-strategy character statement**: After reviewing a strategy across 3+ profiles, synthesize: "This strategy tends to [behavior]. Its strengths are [X]. Its failure mode is [Y]. It is best described as [analogy]."

2. **Cross-strategy comparison matrix**: After reviewing all top strategies, build a matrix of qualitative dimensions:

```
| Dimension | S1a (MiniLM) | S1c (SPECTER2) | S1i (SVM) | S3a (BibCoupling) |
|-----------|-------------|----------------|-----------|-------------------|
| Feels like... | [analogy] | [analogy] | [analogy] | [analogy] |
| Best at finding... | | | | |
| Blind to... | | | | |
| False positive type | | | | |
| Cold-start behavior | | | | |
| [EMERGENT: new dimension] | | | | |
```

3. **Emergent dimension catalog**: Collect all Part 4 observations across all reviews. Cluster them. If a new quality dimension appears across multiple reviews (like "discovery potential" did in Spike 001), it becomes a named dimension and future reviews assess it explicitly.

#### Integration with quantitative instruments

Quantitative instruments and qualitative review are not competing methods where one validates the other. They are complementary modes of inquiry that produce different kinds of knowledge:

- **Instruments** detect regularities across many data points. They can compare 44 strategies across 8 profiles systematically. They can identify that Strategy A clusters at coherence=0.52 while Strategy B clusters at coherence=0.38. They produce the raw material of comparison.

- **Qualitative review** interprets what those regularities mean. It can tell us that Strategy A's coherence=0.52 feels like a focused literature review while Strategy B's 0.38 feels like creative exploration — and that for Profile P4 (broad/AI safety), the lower-coherence strategy actually serves the researcher better despite the "worse" number.

When they agree, confidence in both increases. When they disagree, the disagreement is the most valuable signal in the entire evaluation — it means either the instrument is measuring the wrong thing, or the reviewer is applying the wrong frame. Both are worth investigating.

Three specific functions:

1. **Mutual calibration**: Qualitative review calibrates what metric values mean in practice (is 0.52 coherence "high" or "moderate" for this kind of interest?). Metrics calibrate whether qualitative impressions hold across profiles or are idiosyncratic to one case.

2. **Boundary detection**: Metrics detect patterns. Qualitative review detects the boundaries of those patterns — where the metric stops being informative, where a number that looks good actually corresponds to a bad experience, where a new dimension of quality exists that no metric captures.

3. **Strategy characterization**: The strategy profile card's `qualitative` section — character, best_for, worst_for, failure_mode, feels_like — is populated from qualitative review, not from metrics. These fields are what users actually read when choosing a strategy. The metrics provide supporting evidence; the narrative provides understanding.

#### Practical execution

Qualitative reviews are delegated to AI agents with the following setup:
- Each agent receives the review template, the seed papers, and the recommendation set
- Agents are instructed to be critical, not charitable — a recommendation set that's "fine" should be rated as average, not praised
- For blind comparisons, strategy identity is genuinely withheld (the agent sees "Strategy A" and "Strategy B")
- Multiple agents can review the same set independently to test inter-reviewer agreement
- Reviews are stored as markdown files in `experiments/reviews/` and their structured data extracted into the profile dataset

**ASSUMPTION**: AI agents produce informative (though not authoritative) qualitative assessments. The Spike 001 qualitative review validated this — the AI correctly identified that MiniLM finds "vocabulary squatters" and SPECTER2 finds "community neighbors," characterizations confirmed by the quantitative cross-model evaluation. But AI agents may have blind spots (e.g., unable to judge mathematical correctness of a paper's approach). The review template's Part 4 (emergent observations) and Part 5 (metric divergence) are designed to surface these blind spots.

### Known evaluation biases and mitigations

| Bias | Direction | Mitigation |
|------|-----------|------------|
| BERTopic clusters defined by MiniLM embeddings | Favors MiniLM for leave-one-out | Also define clusters using SPECTER2 embeddings and category co-occurrence |
| Category ground truth favors metadata strategies | Category-based strategies trivially win on category metrics | Use leave-one-out MRR as primary metric, not category recall |
| Near-zero citations for January 2026 papers | Citation-based strategies appear weak | Use FWCI (field-normalized) and reference_count as alternative proxies. Report limitation. |
| AI reviewer may prefer certain recommendation styles | Unknown direction | Use structured rubric; report inter-profile variance |
| Seed papers selected from BERTopic clusters | May favor strategies aligned with BERTopic's notion of topic | Cross-validate with manually selected seeds for 2-3 profiles |

## Experiment Design

### Wave 0: Infrastructure (blocks everything)

**Duration estimate**: 1-2 sessions

**W0.1: Fix SPECTER2 loading**

Compute SPECTER2 embeddings with the proper proximity adapter for all 19K papers.

Protocol:
1. Install `adapters` library (already available per .continue-here.md, but `transformers` was downgraded — verify compatibility)
2. Load SPECTER2 base model + proximity adapter as documented: `model.load_adapter("allenai/specter2", source="hf", set_active=True)` (or equivalent)
3. Verify adapter is active: compare 5 paper embeddings with and without adapter. Expect ~35% top-20 change (from QV3 finding).
4. Compute embeddings for all 19K papers on GPU. Save as `specter2_adapter_19k.npy`.
5. Sanity check: for 3 seed papers, compare top-10 with adapter vs without. Report differences.

**BRANCH POINT W0.1**: If adapter fails to load or produces identical results to base model → investigate further before proceeding. If adapter produces dramatically different results (>50% top-20 change) → the magnitude of change itself is a finding worth documenting.

**W0.2: Build evaluation harness**

Create a reusable Python module that takes any strategy callable and produces a strategy profile card.

Interface:
```python
class StrategyProfiler:
    def __init__(self, corpus, embeddings, clusters, interest_profiles):
        ...

    def profile(self, strategy_fn, config, contexts) -> StrategyProfileCard:
        """Run strategy under each context, compute all quality + resource metrics."""
        ...

    def compare(self, profiles: list[StrategyProfileCard]) -> ComparisonReport:
        """Side-by-side comparison with significance tests."""
        ...
```

The harness:
- Implements all 7 quality metrics
- Implements all 7 resource metrics
- Runs leave-one-out evaluation across interest profiles
- Reports per-profile breakdown and aggregates
- Measures variance across seed selections (3 random selections per profile)
- Produces JSON output matching the profile card schema

**W0.3: Define interest profiles and clusters**

Using existing A2 BERTopic results + manual curation:
1. Select papers for profiles P1-P8
2. For each, identify cluster membership under MiniLM BERTopic, SPECTER2 BERTopic (new, requires W0.1), and category co-occurrence
3. Define "strongly related" papers (agreed by 2+ definitions)
4. Split into seed papers (available for strategy input) and held-out papers (for leave-one-out only)
5. Create 3 random seed selections per profile for variance estimation

**ASSUMPTION A9 tested here.** If variance across seed selections > variance across strategies for any profile, that profile's results are uninformative and need redesign.

**W0.4: Expand OpenAlex enrichment (if needed for S3a)**

Currently 460 papers enriched. Bibliographic coupling (S3a) needs referenced_works for many papers.

Protocol:
1. Check how many of our 460 enriched papers have referenced_works in openalex_raw
2. For bibliographic coupling to work, we need referenced_works for seed papers AND their neighbors. Estimate how many additional enrichment calls are needed.
3. If >500 additional calls needed: batch enrich, respect 10 req/s rate limit
4. If >5000: this is a significant cost. Decide whether to proceed or scope down S3a.

**BRANCH POINT W0.4**: If referenced_works coverage is too sparse for meaningful bibliographic coupling → flag S3a as "data-limited" and report what coverage would be needed.

### Wave 1: Individual Strategy Screening (parallelizable within sub-waves)

**Duration estimate**: 2-3 sessions

**Purpose**: Profile each strategy at its default configuration against all interest profiles. This is the screening phase — strategies that clearly underperform baselines (S6a-S6d) are flagged but still profiled for completeness.

**Sub-wave 1A: Content-based strategies (S1a-S1j)**

These can all be run in parallel (independent, all using pre-computed data).

For each strategy:
1. Run evaluation harness with default config, all 8 interest profiles, 3 seed selections each
2. Produce strategy profile card
3. Record quality metrics, resource metrics, per-profile breakdown

Special handling:
- **S1c (SPECTER2+adapter)**: Compare against S1b (SPECTER2 base) to quantify adapter impact. This is the core Spike 003 question.
- **S1g, S1h (title-only)**: Compute title-only embeddings first (quick — just change input text)
- **S1i (SVM)**: Test with 20-paper "library." Sensitivity to library size deferred to Wave 2.
- **S1j (embedding centroid)**: Simple but may be surprisingly effective. Compare against S1a.
- **S1k, S1l (API embeddings)**: Run on a 100-paper sample first to estimate quality. If quality is not dramatically better than S1a/S1c, full profiling is not worth the API cost.

**Qualitative review checkpoint (1A)**: After all content-based strategies are profiled quantitatively, run single-strategy characterization reviews for the top 4 content-based strategies across profiles P1, P3, P4 (medium, narrow, broad). Purpose: characterize each strategy's recommendation "personality" before combining them in Wave 3. This review produces the `character`, `best_for`, `worst_for`, and `failure_modes` fields in the profile card.

**BRANCH POINT 1A.1**: If S1c (SPECTER2+adapter) is dramatically better than S1b (base) → all prior SPECTER2 findings need revision notes. If they're similar → the adapter issue was overblown and prior findings are approximately correct.

**BRANCH POINT 1A.2**: If S1k/S1l (API embeddings) on the 100-paper sample show >20% quality improvement over S1a/S1c → worth full profiling. If comparable → document as "available but no quality advantage; cost is the only differentiator."

**BRANCH POINT 1A.3**: If S1g/S1h (title-only) are within 10% of S1a/S1c (full abstract) on quality → title-only is a viable cheap alternative worth promoting.

**Sub-wave 1B: Metadata-based strategies (S2a-S2m)**

These are all cheap to compute and can run in parallel.

For each strategy:
1. Run evaluation harness with default config, all 8 interest profiles
2. Produce strategy profile card

Special handling:
- **S2d, S2e (FWCI, citation)**: Limited to 460 enriched papers. Run on enriched subset. Report coverage limitation.
- **S2i (OpenAlex topics)**: Extract topic IDs from enrichment JSONB. Define "match" as shared level-1 or level-2 topic. Test both granularities.
- **S2j (recency decay)**: Test with 30-day and 90-day half-lives. All papers are from January 2026, so this mainly tests whether recency within the month matters.
- **S2k (version update)**: May have too few updated papers in a single month to be informative. Check data first.
- **S2m (cross-listing breadth)**: More of a diversity signal than a relevance signal. May perform poorly on MRR but contribute as an ensemble component.

**EMERGENT QUESTION 1B.1**: If S2d (FWCI) is strong as a standalone strategy → how much does it add when combined with content-based strategies? (Tested in Wave 3.)

**Sub-wave 1C: Graph-based strategies (S3a-S3c)**

Depends on W0.4 (enrichment expansion) for S3a.

- **S3a (bibliographic coupling)**: Run on papers with referenced_works data. Report coverage. This is the Connected Papers approach — if it works well, it's a strong signal for zero-citation papers.
- **S3b (co-citation)**: Check feasibility. If January 2026 papers have too few citations to identify co-cited pairs → mark as "not evaluable with current data" and skip.
- **S3c (OpenAlex related_works)**: Check how many enriched papers have related_works populated. If sufficient, evaluate as a "free" strategy (pre-computed by OpenAlex).

**BRANCH POINT 1C.1**: If S3a (bibliographic coupling) is strong → bibliographic coupling + embedding similarity hybrid should be tested in Wave 3 (it adds a signal dimension no content-based strategy can capture). If weak → likely a data coverage issue, not a strategy issue.

**Sub-wave 1D: Baselines (S6a-S6d)**

Run all baselines. These calibrate the quality scale. Any strategy that doesn't beat S6a (random) is not worth configuring. S6d (same category) is the bar for content-based strategies.

### Wave 2: Configuration Sensitivity (depends on Wave 1)

**Duration estimate**: 1-2 sessions

**Purpose**: For each strategy that passed screening (beat baselines), vary key configuration dimensions and measure sensitivity.

**Which strategies get full config sweeps?**

Decision rule: A strategy gets a config sweep if:
1. It beat S6a (random) on at least 5/8 interest profiles, AND
2. It beat S6d (same category) on at least 3/8 profiles, AND
3. It is a candidate for inclusion in the recommendation system (not just a baseline)

**W2.1: Feature input sensitivity (S1a, S1c, S1i)**

For top embedding strategies and SVM:
1. Compute title-only embeddings (if not done in 1A)
2. Run evaluation with: abstract-only, title-only, title+abstract
3. Compare quality metrics
4. Report: does feature input change strategy quality or just shift it?

**W2.2: Top-K / aggressiveness sweep (all passing strategies)**

For each strategy:
1. Vary top-K: 10, 20, 50, 100, 200, 500
2. Plot: K vs each quality metric
3. Identify: is there an elbow? Does coherence degrade smoothly or sharply?
4. Report: recommended default K per strategy

**W2.3: SVM parameter sensitivity (S1i)**

1. Vary C: 0.001, 0.01, 0.1, 1.0
2. Vary training set size: 5, 10, 20, 50 "liked" papers
3. Measure quality at each combination
4. Report: minimum viable training set, optimal C

**W2.4: HNSW parameter sensitivity (pgvector users)**

1. Vary ef_search: 40, 100, 200, 400
2. Measure: recall vs latency trade-off
3. Report: recommended defaults for different quality/speed preferences

**W2.5: Embedding quantization (S1a, S1c)**

1. Quantize embeddings: float32 → float16 → int8
2. Measure: quality change, memory savings, latency change
3. Report: whether quantization is a free win or a meaningful trade-off

**EMERGENT QUESTION W2**: If feature input (W2.1) makes a large difference → all Wave 3 combinations need to test both abstract and title+abstract variants, doubling the combination space.

### Wave 3: Combinations and Pipelines (depends on Waves 1-2)

**Duration estimate**: 2-3 sessions

**Purpose**: Test how strategies interact when combined. Combinations can be sub-additive (redundant signals), additive (independent signals), or super-additive (complementary signals).

**W3.1: Pairwise combination screening**

For the top ~5 individual strategies (from Wave 1), test all pairwise combinations using RRF (S5a):
1. Strategy A + Strategy B → RRF → evaluate
2. This produces a matrix of combination quality: does A+B > max(A, B)?
3. Report: which pairs are complementary (super-additive) and which are redundant (sub-additive)?

Expected pairings to test (based on prior findings that strategies capture different dimensions):

| Pair | Why it might be complementary |
|------|------------------------------|
| S1a (MiniLM) + S1c (SPECTER2) | Topical precision + cross-community discovery |
| S1a (MiniLM) + S3a (bibliographic coupling) | Content similarity + citation structure |
| S1a (MiniLM) + S2d (FWCI) | Content + bibliometric quality |
| S1c (SPECTER2) + S2g (followed author) | Discovery + personalization |
| S1i (SVM) + S1a (embedding) | Learned preference + content similarity |
| S1a + S2j (recency) | Relevance + freshness |

**W3.2: RRF k-parameter sensitivity**

For the 3 best pairwise combinations:
1. Vary k: 10, 30, 60, 100
2. Measure quality impact
3. Report: does k matter much, or is RRF robust?

**W3.3: Weighted combination exploration**

For the 3 best pairwise combinations:
1. Vary weights: 0.2/0.8, 0.4/0.6, 0.5/0.5, 0.6/0.4, 0.8/0.2
2. Measure quality at each
3. Report: is the optimal weight consistent across interest profiles, or profile-dependent?

**EMERGENT QUESTION W3.3**: If optimal weights are profile-dependent → the per-project learned weights approach (S5f) is necessary, not just nice-to-have. This would require a Wave 3.5 experiment simulating triage behavior.

**W3.4: Multi-stage pipeline comparison (S4a-S4f)**

For each pipeline:
1. Run with top-200 retriever → reranker
2. Compare against best individual strategy and best pairwise combination
3. Report: does the two-stage approach add value?

Special handling:
- **S4a (cross-encoder rerank)**: Profile latency carefully. If reranking 200 candidates takes >10s → test with 50 candidates.
- **S4f (LLM rerank)**: Run on top-20 only (cost constraint). Use Claude API with a structured relevance scoring prompt. Report cost per query.

**BRANCH POINT W3.4**: If cross-encoder reranking (S4a) provides >15% MRR improvement → it should be offered as a "quality boost" option in the installer. If <5% → not worth the compute cost for most users.

**BRANCH POINT W3.4b**: If LLM reranking (S4f) provides >25% MRR improvement → document as "premium option" with cost estimate. If <10% → LLM reranking is not justified for this task.

**W3.5: Marginal signal value analysis (C1-R14)**

Starting from the best individual strategy:
1. Add one additional signal/strategy at a time
2. Measure quality delta after each addition
3. Plot: cumulative quality improvement per signal added
4. Identify: diminishing returns point (adding more signals doesn't help)
5. Report: what's the minimum viable combination? What's the recommended combination? What's the maximum-quality combination?

This directly answers the installer's question: "What's the sweet spot between complexity and quality?"

**W3.6: Consensus boosting validation (S5e)**

1. For pairs that disagree (find non-overlapping recommendations), label papers as consensus (in both), A-exclusive, B-exclusive
2. Compare quality metrics for each subset
3. Test: do consensus papers have higher leave-one-out MRR than exclusive papers?
4. If yes → consensus badge is validated. If no → consensus doesn't indicate quality, just agreement.

**Qualitative review checkpoint (W3)**: After identifying the top 2-3 combinations, run blind pairwise comparison reviews: best individual strategy vs best combination, across profiles P1, P4, P8 (medium, broad, narrow). Key question for Part 4: "Does the combination produce recommendations that feel qualitatively different from the components, or is it just a larger set?" Also run combination-vs-components review (consensus papers vs A-exclusive vs B-exclusive) for the top pair.

### Wave 4: Context Sensitivity (depends on Waves 1-3)

**Duration estimate**: 2-3 sessions

**Purpose**: How do the best strategies and combinations perform under different user contexts? This produces the conditional recommendations for the installer.

**W4.1: Cold-start curve (seed count sensitivity)**

For the top 3 strategies and top 2 combinations:
1. Vary seed count: 1, 3, 5, 10, 20
2. At each seed count, measure all quality metrics
3. Plot: seed count vs quality for each strategy
4. Report: minimum viable seed count per strategy. Below this threshold, the strategy shouldn't be offered.

This is the most important context experiment for UX. It answers: "What can we show a brand-new user?"

**Qualitative review checkpoint (W4.1)**: Run cold-start reviews at seed count = 1 and seed count = 3 for the top 2 strategies. Use the cold-start review variant (adds "Would this recommendation help the user refine their interest?" dimension). This is critical UX data — if 1-seed recommendations are garbage even when metrics say they're "OK," the installer must not offer that option.

**EMERGENT QUESTION W4.1**: If some strategies work well with 1 seed but others need 10+ → the installer should ask "how many papers can you identify as interesting right now?" and filter strategy options accordingly.

**W4.2: Interest breadth sensitivity**

For the top 3 strategies:
1. Run on narrow (P3, P8), medium (P1, P2, P5), and broad (P4) profiles separately
2. Compare quality metrics across breadth levels
3. Report: which strategies degrade on broad interests? Which handle breadth gracefully?

**EMERGENT QUESTION W4.2**: If embedding strategies degrade on broad interests but SVM holds up → SVM should be the recommended strategy for interdisciplinary researchers.

**W4.3: Backend × strategy interaction**

Do strategy quality rankings change between backends?

1. For top 3 strategies that use keyword search (S1e/S1f, S4b, S4d):
   - Run on SQLite (FTS5) and PostgreSQL (tsvector)
   - Compare quality metrics
   - Report: does the FTS5/tsvector divergence (Jaccard 0.39) affect strategy QUALITY, or just change which papers appear?

2. For embedding strategies:
   - Run on numpy brute-force and pgvector HNSW
   - Compare: does HNSW's 91% recall at 215K affect quality metrics?
   - Report: is the recall gap visible in quality, or only in benchmarks?

**W4.4: Scale sensitivity (quality at scale)**

This is more speculative but important for the installer's scale recommendations.

1. For top 3 strategies, subsample corpus at: 5K, 10K, 19K papers (using real data, not duplicates)
2. Measure quality metrics at each scale
3. Report: does quality degrade with more papers, or does the larger pool actually help? (More candidates = more potential good matches, but also more noise)

**NOTE**: This requires careful experimental design. Subsampling changes the candidate pool, which changes what "good" means. The seeds should remain constant across scale points.

**W4.5: Negative signal impact**

1. For top 3 strategies, add 5 "not interested" papers to the profile
2. Measure: does quality improve (noise reduction) or not?
3. If S1i (SVM) benefits most → SVM's value proposition is learning what the user DOESN'T want

### Wave 5: Synthesis (depends on all prior waves)

**Duration estimate**: 1 session

**W5.1: Build strategy profile dataset**

Compile all profile cards into a single structured JSON file.

```json
{
  "metadata": {
    "spike": "003",
    "date": "...",
    "corpus": "19K papers, January 2026",
    "evaluation_protocol": "leave-one-out MRR + 6 quality metrics",
    "caveats": ["proxy-based quality", "one month of data", "no human judges"]
  },
  "profiles": { ... },
  "combinations": { ... },
  "context_sensitivity": { ... },
  "installer_recommendations": { ... }
}
```

**W5.2: Generate installer recommendation logic**

Based on Wave 4 context sensitivity:
1. Define decision tree: hardware → interests → seed count → recommended configuration
2. For each configuration: expected quality (with confidence interval), resource requirements, trade-offs
3. Write this as a data file the installer can consume

**W5.3: Generate strategy comparison documentation**

For each pair of strategies that users might choose between:
1. "Strategy A vs Strategy B: A produces more coherent recommendations (0.52 vs 0.38). B produces more diverse recommendations (4.2 clusters vs 2.8). Choose A if you want focused reading lists. Choose B if you want to discover adjacent fields."

**W5.4: Final qualitative validation of top configurations**

This is the culminating qualitative review. By this point, qualitative reviews have already been run in Waves 1, 3, and 4.1. This wave validates the final recommended configurations.

For the top 3 recommended configurations (minimum viable, recommended, maximum quality):
1. Run full review template across profiles P1-P4 (covering medium, narrow, broad)
2. Run blind pairwise comparison: "recommended" config vs "minimum viable" config
3. Synthesize cross-strategy comparison matrix from all reviews accumulated across waves
4. Compile emergent dimension catalog from all Part 4 observations
5. Write the `qualitative` section of each strategy's profile card
6. Flag any cases where the "recommended" configuration's qualitative character doesn't match what the installer would promise

**Emergent dimension handling**: If Part 4 observations across all reviews have surfaced new quality dimensions beyond the original 7 metrics, document them and assess whether they should become formal metrics in future work. The Spike 001 experience (discovering 3 quality dimensions) suggests this is likely.

**W5.5: Write FINDINGS.md and DECISION.md**

Synthesize all findings. Key questions to answer:
1. Which individual strategy performs best? (Context-dependent answer)
2. Which combination provides the best quality/complexity trade-off?
3. What's the minimum viable configuration for a good experience?
4. What's the maximum-quality configuration and how much does it cost?
5. Does the SPECTER2 adapter change the Spike 001 conclusions?
6. Are the prior epistemic corrections (5 signals) fully addressed?

## Dependency Graph

```
Wave 0 (Infrastructure)
├── W0.1: SPECTER2 adapter fix ──────────────────────┐
├── W0.2: Evaluation harness ────────────────────────┤
├── W0.3: Interest profiles & clusters ──────────────┤
└── W0.4: OpenAlex enrichment expansion ─────────────┤
     │ (S3a feasibility check)                       │
     │                                               │
     ▼                                               │
Wave 1 (Strategy Screening) ◄────────────────────────┘
├── 1A: Content-based (S1a-S1l) ─────────────┐
│   ├── BRANCH: S1c adapter impact?          │
│   ├── BRANCH: API embeddings quality?      │
│   └── BRANCH: Title-only viability?        │
├── 1B: Metadata-based (S2a-S2m) ────────────┤── all parallel within sub-waves
├── 1C: Graph-based (S3a-S3c) ───────────────┤
│   └── BRANCH: Bibliographic coupling data? │
└── 1D: Baselines (S6a-S6d) ─────────────────┘
     │
     │ screening results determine which strategies
     │ get full config sweeps
     ▼
Wave 2 (Configuration Sensitivity) ◄── depends on Wave 1 rankings
├── W2.1: Feature input (title vs abstract) ──┐
├── W2.2: Top-K sweep ───────────────────────┤── parallel
├── W2.3: SVM parameters ───────────────────┤
├── W2.4: HNSW parameters ──────────────────┤
└── W2.5: Embedding quantization ────────────┘
     │
     │ EMERGENT: if feature input matters a lot →
     │ doubles Wave 3 combination space
     ▼
Wave 3 (Combinations & Pipelines) ◄── depends on Waves 1-2
├── W3.1: Pairwise combination screening ──────┐
├── W3.2: RRF k sensitivity ──────────────────┤── sequential
├── W3.3: Weighted combination ────────────────┤   (each depends
├── W3.4: Multi-stage pipelines ───────────────┤    on prior)
│   ├── BRANCH: Cross-encoder value?          │
│   └── BRANCH: LLM reranking value?         │
├── W3.5: Marginal signal value ───────────────┤
└── W3.6: Consensus validation ────────────────┘
     │
     │ EMERGENT: if optimal weights are profile-dependent →
     │ need per-project learned weights (W3.5b)
     ▼
Wave 4 (Context Sensitivity) ◄── depends on Waves 1-3
├── W4.1: Cold-start curve ────────────────────┐
│   └── EMERGENT: min seeds per strategy      │
├── W4.2: Interest breadth ──────────────────┤── parallel
├── W4.3: Backend × strategy ────────────────┤   (independent
├── W4.4: Scale sensitivity ─────────────────┤    contexts)
└── W4.5: Negative signal impact ────────────┘
     │
     ▼
Wave 5 (Synthesis) ◄── depends on all prior
├── W5.1: Strategy profile dataset (JSON) ─────┐
├── W5.2: Installer recommendation logic ──────┤── sequential
├── W5.3: Strategy comparison docs ────────────┤
├── W5.4: Qualitative review ──────────────────┤
└── W5.5: FINDINGS.md + DECISION.md ───────────┘
```

### Parallelization opportunities

**Maximally parallel execution plan:**

| Session | Can run simultaneously | Depends on |
|---------|----------------------|------------|
| Session 1 | W0.1 (SPECTER2) + W0.2 (harness) + W0.3 (profiles) + W0.4 (enrichment) | Nothing |
| Session 2 | 1A + 1B + 1C + 1D (all strategy screening) | W0 complete |
| Session 3 | W2.1 + W2.2 + W2.3 + W2.4 + W2.5 (all config sweeps) | W1 rankings |
| Session 4 | W3.1 → W3.2 → W3.3 (sequential within combinations) | W2 configs |
| Session 5 | W3.4 + W3.5 + W3.6 (pipelines + marginal + consensus) | W3.1-3.3 |
| Session 6 | W4.1 + W4.2 + W4.3 + W4.4 + W4.5 (all context dimensions) | W3 combinations |
| Session 7 | W5.1 → W5.2 → W5.3 → W5.4 → W5.5 (synthesis) | W4 complete |

**Within-session parallelism:** The evaluation harness (W0.2) should support running multiple strategies simultaneously (multiprocessing or agent-based parallelism). Each strategy evaluation is independent.

### Branch points (where results change subsequent design)

| ID | Condition | If true | If false |
|----|-----------|---------|----------|
| BP1 | SPECTER2 adapter dramatically changes results (>40% top-20 delta) | All prior SPECTER2 findings need revision notes; S1c becomes primary academic embedding | Adapter effect is minor; prior findings approximately correct |
| BP2 | API embeddings (S1k/S1l) show >20% quality improvement | Full profiling justified; cloud deployment strategy changes | Document as cost-only option |
| BP3 | Title-only embeddings within 10% of abstract | Title-only becomes a recommended cheap alternative | Abstract remains required |
| BP4 | Cross-encoder reranking adds >15% MRR | Offer as "quality boost" option | Not worth compute cost |
| BP5 | LLM reranking adds >25% MRR | Document as "premium option" with cost | Not justified for this task |
| BP6 | Bibliographic coupling data too sparse | Flag as "data-limited"; needs denser enrichment | Include in combinations |
| BP7 | Optimal combination weights are profile-dependent | Per-project learned weights (S5f) is necessary | Fixed weights suffice |
| BP8 | Some strategies fail below 5 seeds | Installer must gate strategy access behind seed count | All strategies work from cold start |
| BP9 | Strategy quality rankings change between backends | Backend selection affects recommended strategy | Backend choice is purely operational |
| BP10 | Feature input (title vs abstract) makes >20% quality difference | All combinations must be tested with both inputs | Abstract is the default; title-only is a niche option |
| BP11 | Variance across seed selections > variance across strategies | Profiling is uninformative for that interest type | Profiles are stable and reliable |

### Emergent question triggers

These are findings that would require designing NEW experiments not currently in this spike.

| Trigger | If we discover... | New experiment needed |
|---------|------------------|---------------------|
| EQ1 | All strategies perform poorly on Profile P4 (broad/AI safety) | Design a "broad interest" strategy: multi-centroid, category-spanning retrieval |
| EQ2 | Combinations are consistently sub-additive | Investigate WHY — perhaps strategies are more correlated than expected. Compute inter-strategy correlation matrix. |
| EQ3 | Cross-encoder quality is high but latency is prohibitive | Design async/background reranking: show fast results first, refine with cross-encoder in background |
| EQ4 | Cold start is terrible for all strategies | Design "guided cold start" UX: suggest seed papers from popular clusters, bootstrap from category selection alone |
| EQ5 | Backend × strategy interaction is strong | The storage abstraction must account for strategy-specific optimizations per backend |
| EQ6 | SPECTER2 adapter produces unexpectedly low quality | Investigate whether the adapter needs fine-tuning or if the wrong adapter variant was used |
| EQ7 | Embedding quantization (int8) dramatically degrades quality | Memory optimization requires larger model → GPU becomes more important → affects tier model |
| EQ8 | One quality dimension (e.g., novelty) inversely correlates with user satisfaction in qualitative review | Our quality metric definitions are wrong; need to revise evaluation framework |

## Output Specification

### Primary output: `strategy_profiles.json`

Top-level structure:
```json
{
  "metadata": {
    "version": "1.0",
    "spike": "003",
    "generated": "2026-MM-DD",
    "corpus": {
      "source": "arXiv OAI-PMH January 2026",
      "size": 19252,
      "categories": 15,
      "enriched_count": 460
    },
    "evaluation": {
      "protocol": "leave-one-out MRR + 6 quality metrics",
      "interest_profiles": 8,
      "seed_selections_per_profile": 3,
      "caveats": [
        "Quality metrics are mathematical proxies, not human relevance judgments",
        "One month of data; seasonal variation not captured",
        "Near-zero citations; bibliometric signals unreliable as absolute values",
        "AI qualitative review is informative but not authoritative"
      ]
    }
  },
  "strategies": {
    "S1a": { ... strategy profile card ... },
    "S1c": { ... },
    ...
  },
  "combinations": {
    "S1a+S1c": { ... combination profile card ... },
    ...
  },
  "context_sensitivity": {
    "cold_start": { ... seed count curves per strategy ... },
    "breadth": { ... quality by breadth per strategy ... },
    "backend": { ... quality by backend per strategy ... },
    "scale": { ... quality by scale per strategy ... }
  },
  "installer_recommendations": {
    "by_hardware": {
      "cpu_only_8gb": { "recommended": "...", "alternatives": [...], "avoid": [...] },
      "cpu_only_32gb": { ... },
      "gpu_32gb": { ... },
      "cloud_api": { ... }
    },
    "by_interest_breadth": { ... },
    "by_seed_count": { ... },
    "sweet_spot": {
      "minimum_viable": { "strategy": "...", "quality": {...}, "resources": {...} },
      "recommended": { ... },
      "maximum_quality": { ... }
    }
  }
}
```

### Secondary outputs

- `FINDINGS.md`: Prose summary of all findings with tables and figures
- `DECISION.md`: Answers to success criteria + revised recommendations for deliberation
- `experiments/`: All experiment scripts, reproducible
- `experiments/data/`: Raw results as JSON, embeddings as .npy
- `experiments/reviews/`: All qualitative review markdown files, organized by wave and strategy
- `experiments/reviews/emergent_dimensions.md`: Catalog of quality dimensions discovered through Part 4 observations
- `experiments/reviews/cross_strategy_matrix.md`: Synthesized qualitative comparison matrix across all reviewed strategies
- `harness/`: Reusable evaluation harness code (includes review template generator)

## Success Criteria

This spike succeeds if we can provide grounded answers to:

| # | Question | What "grounded" means |
|---|----------|----------------------|
| 1 | What are the quality profiles of each viable strategy? | Profile card with metrics, per-profile breakdown, and confidence intervals |
| 2 | Which strategies complement each other and which are redundant? | Pairwise combination matrix showing additive/sub-additive effects |
| 3 | What is the minimum viable configuration for a good user experience? | Named strategy + config with measured quality above baseline |
| 4 | What is the recommended configuration and what does it cost? | Named strategy/combination with resource requirements |
| 5 | What is the maximum-quality configuration? | Named configuration with all resource costs including API |
| 6 | How does quality change with seed count (cold start)? | Curve per strategy showing quality vs seeds, with minimum viable threshold |
| 7 | How do strategies behave for narrow vs broad interests? | Quality metrics by breadth level for top strategies |
| 8 | Does the SPECTER2 adapter change prior conclusions? | Quantified delta from base model, with revision notes if applicable |
| 9 | Can the installer make informed recommendations from this data? | Structured JSON that maps user context to strategy recommendations |
| 10 | Are prior epistemic failures (5 signals) addressed? | Each signal reviewed, mitigation verified or acknowledged |

## Practical Constraints

| Constraint | Limit | Impact |
|-----------|-------|--------|
| Hardware | Xeon W-2125, 32 GB RAM, GTX 1080 Ti (11 GB VRAM) | All local compute must fit in 11 GB VRAM. SPECTER2 (768-dim) + batch = watch VRAM. |
| Corpus | 19,252 real papers from January 2026 | Quality metrics at this scale only. Latency tested to 215K (duplicated). |
| OpenAlex enrichment | 460 papers enriched, 10 req/s limit | Graph strategies limited by coverage. Expansion possible but time-consuming. |
| API budgets | Unknown — need user confirmation for API embedding costs | S1k, S1l, S4f may be scoped down or skipped if budget is zero |
| Python environment | transformers downgraded to 4.51.3 by adapters library | May affect other model loading. Verify before starting. |
| Time | Each session is ~2-4 hours effective | 7 sessions minimum. Some waves can be partially automated (overnight runs). |
| Disk space | /home has ~80 GB free; /scratch has 92 GB | SPECTER2 embeddings at 19K = ~56 MB. Multiple embedding variants fit easily. |

## Relationship to Prior Spikes

### What this spike supersedes

| Prior item | Status | How addressed here |
|-----------|--------|-------------------|
| Spike 003 (SPECTER2 adapter) as originally planned | Superseded | W0.1 + S1c profiling |
| C1-R10: Leave-one-out retrieval quality | Subsumed | Core evaluation metric in harness |
| C1-R11: Retrieval + reranking pipeline | Subsumed | W3.4 pipeline comparison |
| C1-R12: Seed count sensitivity | Subsumed | W4.1 cold-start curve |
| C1-R13: Interest breadth sensitivity | Subsumed | W4.2 breadth sensitivity |
| C1-R14: Marginal signal value | Subsumed | W3.5 marginal analysis |
| C1-R15: SPECTER2 quality profiles | Subsumed | S1c full profiling |
| C1-R16: Bibliographic coupling | Subsumed | S3a profiling |

### What this spike depends on from prior spikes

| Dependency | Source | What we use |
|-----------|--------|-------------|
| 19K paper corpus | Spike 001 A1 | `spike_001_harvest.db` |
| MiniLM embeddings (19K) | Spike 002 QV3 | `embeddings_19k.npy` |
| SPECTER2 base embeddings (19K) | Spike 002 QV3 | In QV3 results |
| BERTopic clusters | Spike 001 A2 | `a2_corpus_visualization_results.json` |
| TF-IDF matrix | Spike 001 A1c.1 | Rebuild from corpus |
| OpenAlex enrichment (460 papers) | Spike 001 B2 | `b2_openalex_cache.json` |
| B1 signal catalog | Spike 001 B1 | `b1_signal_literature_review.md` |
| Backend latency baselines | Spike 002 D2-D6 | Reference numbers |
| Category co-occurrence data | Spike 001 A2 | `a2_corpus_visualization_results.json` |

### What this spike does NOT replace

- Spike 001 A1/A1b/A1c capability envelope measurements (latency at scale, concurrent access, etc.) — these stand as-is
- Spike 002 backend comparison findings (D1-D6) — these stand as-is with Round 2 caveats
- The deployment-portability deliberation — this spike FEEDS the deliberation but doesn't conclude it
