---
question: "What does the arXiv paper landscape look like for our configured categories, what signals predict paper importance, and how do different filtering/promotion strategies trade off volume against coverage?"
type: exploratory
status: designing
linked_deliberation: deployment-portability.md
linked_questions:
  - "docs/10-open-questions.md Q16: Processing promotion strategy"
  - "docs/10-open-questions.md Q17: Retrospective demotion"
---

# Spike 001: Volume, Filtering, and Scoring Landscape

## Question

What does the arXiv paper landscape look like for our configured categories? What signals — both raw and computed — predict paper importance? How do different filtering and promotion strategies trade off volume against coverage?

## Why This Matters

We need empirical understanding before making architectural decisions about:
- Backend choice (SQLite vs PostgreSQL — depends on expected corpus size)
- Promotion pipeline design (depends on which scoring signals exist and work)
- Filtering strategy (depends on the volume-quality tradeoff shape)
- User-facing tier recommendations (depends on all of the above)

We currently have zero empirical data. This spike explores the landscape before we commit to any particular approach.

## Background

### What the architecture currently says
- **ADR-0002:** "Ingest metadata eagerly, enrich lazily, embed selectively"
- **Ingestion filtering:** Category-only (categories.toml: 15 categories across cs, stat, math, eess)
- **Promotion:** Demand-driven only — entirely manual
- **Processing tiers:** METADATA_ONLY(0) → FTS_INDEXED(1) → ENRICHED(2) → EMBEDDED(3) → CONTENT_PARSED(4)

### What we don't know
- The actual volume dynamics of our pipeline at realistic scale
- What the corpus looks like structurally (clusters, distributions, outliers)
- Which features — raw or computed — correlate with paper importance
- Whether "importance" is even one thing or multiple dimensions
- What the coverage-regret tradeoff looks like at different filtering levels
- How different promotion strategies compare in resource requirements

## Design Principles

1. **Explore before operationalize.** Don't define "important paper = >50 citations" upfront. Let the data reveal what importance looks like.
2. **Compute signals, don't just read them.** Metadata fields are inputs. Interesting signals are often derived (author network centrality, category entropy, temporal patterns).
3. **Visualize before quantify.** Maps and distributions reveal structure that summary statistics hide.
4. **Leave room for emergence.** The most interesting findings will be things we didn't think to look for.

## Phases

This spike has three phases. Each phase's design may be refined based on previous phase findings.

### Phase A: Landscape Exploration

**Objective:** Understand what our slice of arXiv looks like — volume, structure, distributions, clusters.

**A1: Volume Mapping**
- Harvest 1 calendar month of real data (January 2026) at multiple category configs:
  - Config A: Big 4 (cs.AI, cs.CL, cs.CV, cs.LG)
  - Config B: All 15 configured categories
  - Config C: All of CS (37 subcategories)
- Measure: unique papers/day, cross-listing overlap, category distribution
- Extrapolate to annual and historical volumes
- Output: volume estimates per config with deduplication rates

**A2: Corpus Visualization and Structure**
- Using the harvested sample, explore the corpus structure:
  - Topic modeling (LDA or BERTopic) on abstracts — what clusters emerge naturally?
  - Dimensionality reduction (UMAP or t-SNE) of TF-IDF vectors — visualize the paper space
  - Category co-occurrence heatmap — how do categories overlap?
  - Temporal patterns — submission rate by day/week/month, seasonal effects
  - Author network — who publishes together, prolific author distribution
- Output: visualizations, cluster descriptions, structural observations
- **This is the most open-ended part.** We're looking at the data to see what patterns exist before deciding what to measure.

**A3: Distribution Analysis**
- For the harvested sample, compute distributions of:
  - Papers per category per day
  - Authors per paper
  - Categories per paper (cross-listing breadth)
  - Submission timing patterns
  - Any other features that the visualization in A2 suggests are interesting
- Output: distribution plots, summary statistics, outlier identification

### Phase B: Signal Research and Discovery

**Objective:** Identify and evaluate candidate signals that could predict paper importance or relevance. Start with research, then compute and test.

**B1: Research — What Signals Could We Use?**
- Literature review: what do existing paper recommendation systems use as features?
  - arxiv-sanity-lite: TF-IDF + SVM on user tags
  - Semantic Scholar: SPECTER embeddings, citation velocity
  - OpenAlex: topics, concepts, citation graph metrics
  - Others in the literature
- Catalog of possible signals, organized by:
  - When available (at ingestion vs after enrichment vs after user interaction)
  - Computational cost (free metadata field vs API call vs GPU compute)
  - What they might predict (importance, relevance to a profile, novelty)
- Output: signal catalog document

**B2: Computed Signal Exploration**
- Using a retrospective sample (papers from 2024 with 2+ years of citation history via OpenAlex), compute candidate signals:
  - **Raw metadata signals:** author count, category count, primary category, etc.
  - **Computed signals:** things we derive from metadata that aren't directly stored
    - Author publication frequency in corpus (proxy for productivity/influence)
    - Category entropy (how cross-disciplinary is this paper?)
    - Title/abstract textual features (TF-IDF similarity to high-impact papers, keyword patterns)
    - Temporal features (submission timing relative to conference deadlines, trending topic overlap)
    - Author network features (co-author graph centrality, institutional diversity)
    - Whatever else Phase A's exploration suggests
  - **Enrichment signals (available after tier 2):**
    - OpenAlex topic scores
    - Related works count
    - Early citation velocity (citations in first N months)
- For each signal, visualize its distribution and relationship to citation outcomes
- Unsupervised analysis: do papers cluster by these signals in ways that map to importance?
- Output: signal analysis with visualizations, ranked by apparent informativeness

**B3: "Importance" — Is It One Thing?**
- Using the enriched retrospective sample, explore what "important" means:
  - Citation count distribution — what does the tail look like?
  - Citation velocity vs cumulative citations — are fast-cited papers different from slow-burn papers?
  - Is there a meaningful boundary between "important" and "not important" or is it a continuum?
  - Do different categories have different importance distributions? (A paper with 50 citations in stat.TH might be landmark; in cs.AI it might be average)
  - Cluster analysis: do importance dimensions (citations, breadth of citing fields, longevity) form natural groups?
- Output: operational definition(s) of importance grounded in data, not assumed upfront

### Phase C: Tradeoff Mapping

**Objective:** Given what we learned in Phases A and B, map the tradeoffs between filtering strategies, promotion strategies, and resource requirements.

**C1: Coverage-Regret Analysis**
- Using the best signals from Phase B, construct candidate filtering/scoring strategies
- Apply each strategy to the retrospective sample
- Measure coverage (% of important papers retained) vs volume (papers kept)
- Plot coverage curves — look for elbows, natural thresholds
- Analyze regret: which important papers does each strategy miss, and why?
- Test sensitivity: how do results change with different importance definitions from B3?
- Output: coverage-regret curves, strategy comparison, regret analysis

**C2: Promotion Pipeline Simulation**
- Simulate 1 year of operation under different promotion strategies:
  - Demand-only (current: user touches paper → promote)
  - Cohort-based (auto-promote top N% daily)
  - Budget-constrained (fixed daily enrichment budget, allocated by score)
  - Two-phase (ingest broadly, build triage data, then auto-promote)
- Estimate for each: API calls/day, disk usage growth, compute requirements
- Cross-reference with backend capacity (from volume estimates in Phase A)
- Output: resource projections per strategy, backend implications

**C3: Backend Implications**
- Using volume estimates from A1 and resource projections from C2:
  - At what corpus sizes do different operations become slow? (This feeds Spike 002)
  - What are the disk usage projections for each tier over 1-3 years?
  - At what point would a user need to consider migrating from SQLite to PostgreSQL?
  - What are the concrete feature tradeoffs at each backend (from our earlier analysis)?
- Output: preliminary backend sizing guidance (to be validated by Spike 002 benchmarks)

## Success Criteria

Exploratory spike — success is learning, not confirming.

**The spike succeeds if we can provide grounded answers to:**
1. What are the realistic paper volumes at each category configuration?
2. What does the arXiv landscape look like structurally for our categories?
3. Which 3-5 signals are most worth computing for paper scoring?
4. What shape is the coverage-regret tradeoff? Is there an elbow?
5. What promotion strategy best fits our architectural values (ADR-0002)?
6. What are the approximate resource requirements for 1 year of operation?

**The spike surfaces new questions if:**
- Unsupervised analysis reveals unexpected structure worth investigating further
- Signal analysis suggests a scoring approach worth prototyping (→ potential new spike)
- Coverage analysis reveals that aggressive filtering is too risky OR that broad ingestion is too cheap to bother filtering (→ revises the whole question)

**The spike fails if:**
- We can't harvest enough data for meaningful analysis (arXiv rate limits, API issues)
- OpenAlex enrichment is too slow to get citation data for the retrospective sample
- The analysis is too shallow to inform architectural decisions

## Practical Constraints

- arXiv OAI-PMH: 3s between requests (our harvester rate limit)
- OpenAlex: 10 req/s with email configured
- Storage: /scratch (87GB free) for experiment data, /data (1.4TB) for large datasets
- GPU: GTX 1080 Ti available for BERTopic / UMAP if needed
- Python environment: conda or project venv, scikit-learn + matplotlib + umap-learn + bertopic
- All experiment code lives in this spike workspace

## Experiment Code Location

`.planning/spikes/001-volume-filtering-scoring-landscape/experiments/`

## Output

- **FINDINGS.md:** Data, visualizations, analysis organized by phase
- **DECISION.md:** Answers to the six success criteria questions + recommendations
- **Artifacts:** Notebooks, scripts, datasets in experiments/
- **Feeds into:** Spike 002 (backend benchmarking), deployment-portability deliberation, potentially new spikes
