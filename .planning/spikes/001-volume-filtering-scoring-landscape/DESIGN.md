---
question: "What are the volume, filtering, and scoring dynamics of arXiv paper ingestion under different configurations — and what signals available at ingestion time predict paper importance?"
type: exploratory
status: designing
linked_deliberation: deployment-portability.md
linked_questions:
  - "docs/10-open-questions.md Q16: Processing promotion strategy"
  - "docs/10-open-questions.md Q17: Retrospective demotion"
---

# Spike 001: Volume, Filtering, and Scoring Landscape

## Question

What are the real-world volume dynamics of arXiv paper ingestion under different category and scoring configurations — and which signals available at metadata-only tier predict future paper importance?

## Why This Matters

We need to make architectural decisions about:
- Whether SQLite is viable as a default backend (depends on expected corpus size)
- How the promotion pipeline should work (depends on which scoring signals are predictive)
- What filtering strategies to offer users (depends on the volume-quality tradeoff)

We currently have zero empirical data on any of these. The project has 126 papers from manual import. Real-world usage involves daily harvesting from arXiv, producing ~100K papers/year (estimated from arXiv stats, unvalidated against our actual pipeline).

## Background

### What the architecture currently says
- **ADR-0002:** "Ingest metadata eagerly, enrich lazily, embed selectively"
- **Ingestion filtering:** Category-only (configured in `categories.toml`: 15 categories across cs, stat, math, eess)
- **Promotion:** Demand-driven only — papers get enriched/embedded when a user/agent explicitly touches them
- **Processing tiers:** METADATA_ONLY(0) → FTS_INDEXED(1) → ENRICHED(2) → EMBEDDED(3) → CONTENT_PARSED(4)
- **Current behavior:** All ingested papers go straight to tier 1 (FTS_INDEXED) automatically

### What we don't know
1. How many papers/day actually match our configured categories after deduplication?
2. What does the volume look like at different category configurations?
3. What metadata-only signals (available at tier 0-1) correlate with future importance?
4. At what scoring threshold do we start missing important papers (regret)?
5. What's the volume-coverage tradeoff curve look like?

## Hypotheses

These are not predictions to confirm/reject — they're working hypotheses to guide exploration. We expect some to be revised as we learn.

**H1:** The big 4 categories (cs.AI, cs.CL, cs.CV, cs.LG) account for >80% of the papers a philosophy-of-AI researcher would want, despite being only 4 of 15 configured categories.

**H2:** At least one metadata-only signal (author publication frequency, category cross-listing count, abstract length, title keyword patterns) will correlate with future citation count at r > 0.3.

**H3:** An "ingest all, promote selectively" strategy (ADR-0002's approach) produces lower regret than any ingestion-stage filtering strategy, at the cost of larger tier-0/1 storage.

**H4:** There exists a natural elbow in the volume-coverage curve where increasing ingestion volume gives diminishing returns in important-paper coverage.

## Experiments

### Experiment 1: Volume Mapping

**Objective:** Measure actual paper volumes at different category configurations.

**Method:**
1. Use arXiv OAI-PMH to harvest 1 calendar month (e.g., January 2026) for each configuration:
   - Config A: Big 4 only (cs.AI, cs.CL, cs.CV, cs.LG)
   - Config B: All 15 configured categories
   - Config C: All of CS (37 subcategories)
   - Config D: Config B + expanded philosophy-adjacent (e.g., cs.CY, cs.HC, physics categories)
2. Count unique papers per config (accounting for cross-listing deduplication)
3. Extrapolate to annual volume

**Measurements:**
- Unique papers per day, per config
- Cross-listing overlap percentage between configs
- Category distribution within each config (which categories contribute most?)
- Metadata size per paper (average, p50, p95)

**Controls:**
- Same time period for all configs (controls for seasonal variation)
- Deduplication by arxiv_id (controls for cross-listing)

### Experiment 2: Scoring Signal Analysis

**Objective:** Identify which metadata-only signals predict future paper importance.

**Method:**
1. Harvest a retrospective sample: papers from January-March 2024 in Config B categories
2. Enrich all papers via OpenAlex to get current (2026) citation counts
3. For each paper, extract metadata-only signals available at ingestion time:
   - Author count
   - Abstract word count
   - Number of categories (cross-listing breadth)
   - Primary category
   - Title keyword patterns (e.g., contains "survey", "benchmark", "framework")
   - Day of week / month of submission
   - Author name frequency in corpus (proxy for prolific authors)
4. Correlate each signal with citation count at +2 years
5. Build a simple scoring model (logistic regression or decision tree) and evaluate predictiveness

**Measurements:**
- Pearson/Spearman correlation for each signal vs citations
- ROC-AUC of a simple classifier predicting "paper reaches >10 citations within 2 years"
- Feature importance ranking
- Confusion matrix: what types of important papers does the classifier miss?

**Controls:**
- Use 2024 data with 2026 citations (2-year lag gives citations time to accumulate)
- Train/test split (70/30) to avoid overfitting
- Null model comparison (random scoring)

### Experiment 3: Coverage-Regret Analysis

**Objective:** Map the tradeoff between filtering aggressiveness and missed-paper regret.

**Method:**
1. Using the same retrospective sample from Experiment 2
2. Define "important paper" operationally: >50 citations within 2 years (this threshold itself should be explored)
3. Apply different filtering strategies:
   - No filter (keep all) — baseline
   - Category-only (current approach)
   - Category + top-N% by scoring model from Experiment 2
   - Category + minimum cross-listing count
   - Category + author frequency threshold
4. For each strategy, measure:
   - How many papers kept (volume)
   - How many important papers kept (coverage)
   - How many important papers missed (regret)

**Measurements:**
- Coverage: % of important papers retained at each filtering level
- Volume: absolute number of papers at each level
- Regret: list of specific important papers missed, with analysis of why
- Coverage-volume curve: plot coverage (y) vs volume (x) for each strategy
- Elbow detection: where does the curve flatten?

**Controls:**
- Same "importance" definition across all strategies
- Multiple importance thresholds (>10, >50, >100 citations) to test sensitivity
- Time-window controls (does the pattern hold for Q1 2024 vs Q2 2024?)

### Experiment 4: Promotion Pipeline Simulation

**Objective:** Estimate resource requirements of different promotion strategies at realistic volumes.

**Method:**
1. Using volume estimates from Experiment 1 and scoring model from Experiment 2
2. Simulate 1 year of operation under different promotion strategies:
   - **Demand-only:** Only promote papers the user touches (estimate 5-20 papers/day)
   - **Cohort:** Auto-promote top 10% of daily ingest to tier 2
   - **Budget-constrained:** Fixed daily budget of N enrichments, allocated by score
   - **Two-phase:** Ingest all at tier 0-1, promote based on accumulated triage data after 30 days
3. For each strategy, estimate:
   - Enrichment API calls per day/month (OpenAlex rate limit: 10 req/s with email, 1 req/s without)
   - Disk usage growth trajectory
   - Embedding compute requirements (when we reach tier 3)

**Measurements:**
- API calls per day per strategy
- Cumulative disk usage over 12 months
- Time to process daily batch
- Estimated cost (API, compute, storage)

**Controls:**
- Same base corpus for all strategies
- Same user interaction model (estimated from Phase 5 and Phase 10 session data)

## Success Criteria

This is an exploratory spike — success is defined by learning, not by confirming a hypothesis.

**The spike succeeds if we can answer:**
1. How many papers per year at each category configuration? (±20% accuracy)
2. Which 2-3 metadata signals are most predictive of importance? (ranked by effect size)
3. What's the shape of the coverage-regret curve? (is there an elbow?)
4. What are the resource implications of each promotion strategy? (order of magnitude)

**The spike fails if:**
- We can't harvest enough historical data to do the retrospective analysis
- OpenAlex enrichment rate limits prevent us from getting citation data for the sample
- The signals we can extract at metadata-only tier have no predictive value (all r < 0.1)

## Practical Constraints

- arXiv OAI-PMH rate limit: 3 seconds between requests (configurable in our harvester)
- OpenAlex rate limit: 10 req/s with email, 1 req/s without (we have email configured)
- Disk: /home has ~80GB free, /scratch has 87GB free, /data has 1.4TB free
- GPU: GTX 1080 Ti available but not needed for this spike (no embeddings)
- All experiment code lives in this spike workspace — no modification to main project files

## Experiment Code Location

All code in `.planning/spikes/001-volume-filtering-scoring-landscape/experiments/`

## Output

- **FINDINGS.md:** Data, charts, analysis for each experiment
- **DECISION.md:** Answers to the four success criteria questions
- Feeds into: Spike 002 (backend benchmarking) and deployment-portability deliberation
