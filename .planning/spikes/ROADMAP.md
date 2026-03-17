# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Updated:** 2026-03-17
**Status:** Active — Spike 001 Phase A1 complete, continuing
**Origin:** Post-Phase-10 deliberation on deployment and portability

## Context

After completing v0.1 (Phase 10: Agent Integration Test), interconnected areas of design uncertainty emerged around deployment, filtering, recommendation, and backend architecture. These cannot be resolved through discussion alone — they require empirical investigation.

### How We Got Here

**Deliberation: deployment-portability.md** (2026-03-14, open — pending spike findings)

The initial question was "how would someone install this on another computer?" This expanded through conversation into deeper questions about:
- Backend choice (SQLite vs PostgreSQL) and what each actually enables
- Paper scoring and the promotion pipeline (Open Question 16)
- The NLP layer (TF-IDF, embeddings, topic modeling) and where it runs
- Hardware-adaptive deployment with graceful degradation
- Project-dependent recommenders
- Feature extensibility and how new capabilities declare their requirements
- Migration paths between configurations

**Key discovery during deliberation:** The NLP intelligence (TF-IDF, SVM recommendations, even lightweight embeddings) runs in Python, not the database. The database is storage. This means the "SQLite vs PostgreSQL" question is narrower than we assumed — SQLite + Python can deliver most features, with PostgreSQL only needed for indexed ANN at >500K vectors and multi-user concurrency.

### Architectural References

- ADR-0002: Metadata-first, lazy enrichment
- Doc 05 §4: Stack A → B trajectory
- Doc 05 §7: Compute profiles (Bronze/Silver/Gold)
- Doc 10 Q16: Processing promotion strategies
- Doc 10 Q17: Retrospective demotion
- ProcessingTier enum: METADATA_ONLY → FTS_INDEXED → ENRICHED → EMBEDDED → CONTENT_PARSED
- categories.toml: 15 categories across 4 archives

## Research Program Methodology

### Principles

1. **Inquiry, not verification.** We gather data to understand what's actually happening, not to confirm claims we've already made. Unexpected findings are more valuable than expected ones.
2. **Measure before designing.** Architectural decisions should follow empirical data, not precede it. Design the seams now, fill them in when we have evidence.
3. **Trace assumptions to their roots.** Every claim rests on assumptions. Those assumptions have assumptions. We map the full dependency chain and test the weakest links.
4. **Experiments should be able to surprise us.** If an experiment can only confirm what we already believe, it's not severe enough. Design tests that probe where our understanding is most likely to be wrong.
5. **Spikes chain and branch.** Findings from one spike inform the design of the next. New questions can emerge mid-spike — capture them, don't suppress them.

### Flow

```
Explore (gather data, visualize, discover structure)
    ↓
Identify questions (what patterns need explanation?)
    ↓
Design experiments (what would we observe if our hypothesis is wrong?)
    ↓
Run experiments (measure, don't assume)
    ↓
Revise understanding (update claims, identify new questions)
    ↓
Loop (new questions → new exploration → new experiments)
    ↓
Eventually: enough evidence to make architectural decisions
    ↓
Update deliberation → create implementation phases → execute
```

This is not a linear process. We expect to loop multiple times as findings reshape our questions.

## Spike Sequence

### Active

| # | Question | Type | Status | Key Findings So Far |
|---|----------|------|--------|-------------------|
| 001 | Volume, filtering, scoring, and NLP landscape | Exploratory | Phase A1 complete | Big4 = 12K papers/month. FTS5 search <40ms at 215K papers. Scaling is linear, no knee. |

### Planned

| # | Question | Type | Depends On | Status |
|---|----------|------|------------|--------|
| 002 | Backend performance comparison (PostgreSQL benchmarks at same scales) | Comparative | 001 Phase A1 data | Ready to start |

### Anticipated (may emerge from findings)

| Question | Would be triggered if... |
|----------|------------------------|
| TF-IDF + SVM recommendation quality | Phase B signal analysis reveals TF-IDF is a viable scoring approach |
| Feature lifecycle management | Measurements show pre-computed features need non-trivial persistence strategy |
| Concurrent access patterns | SQLite concurrent read+write test reveals contention issues |
| Promotion pipeline strategies | Retrospective analysis reveals predictive scoring signals |
| Project-level recommendation | Interest profile limitations surface during real usage |
| Hardware-adaptive capability detection | Measurements produce clear hardware → feature mappings |

## Spike 001: What Remains

### Completed
- [x] A1: Volume mapping (3 configs harvested, 19K real papers)
- [x] A1 supplement: FTS5 search benchmark (7 scale points, 10 query types)

### Next Experiments (in priority order)

**Highest priority — most likely to change our design decisions:**

| Experiment | What it measures | Why it matters |
|-----------|-----------------|---------------|
| TF-IDF matrix benchmark | Memory footprint, rebuild time at 19K/50K/100K | Determines whether Silver tier is feasible on a laptop |
| Concurrent SQLite read+write | Search latency during sustained writes | Determines whether harvest daemon + MCP server can coexist |
| Lightweight embedding benchmark | Compute time (CPU vs GPU), memory, brute-force search speed | Determines whether Gold tier works without pgvector |

**Medium priority — informs design but unlikely to block decisions:**

| Experiment | What it measures | Why it matters |
|-----------|-----------------|---------------|
| A2: Corpus visualization (UMAP/BERTopic) | Structural patterns in paper space | Informs scoring system design, reveals natural clusters |
| A2b: Interactive explorer prototype | Usability of visual exploration | Tool for all subsequent analysis |
| FTS5 vs tsvector quality comparison | Do they return the same papers? | Confirms backend equivalence claim |
| MCP server startup with feature loading | Time to load TF-IDF/embeddings on startup | Determines user experience |

**Lower priority — important but dependent on earlier findings:**

| Experiment | Depends on |
|-----------|-----------|
| B1: Signal research (literature review) | A2 visualization insights |
| B2: Computed signal exploration | B1 signal catalog |
| B3: "Importance" exploration | Enriched retrospective sample |
| C1-C3: Tradeoff mapping | Phase B results |

## Open Design Questions (From Deliberation)

These emerged during the deliberation and are not yet addressed by any spike:

1. **Feature lifecycle:** Where do pre-computed features (TF-IDF matrices, embeddings) live between MCP server restarts? How are they updated incrementally?
2. **Capability system vs tiers:** Should we offer fixed tiers or a dependency-resolution system where features declare their requirements?
3. **Project abstraction:** Should "project" be a first-class concept grouping profiles + collections + watches + recommendation feeds?
4. **User transparency:** How much should the init wizard explain vs decide automatically?
5. **Migration paths:** What exactly needs to transfer when moving between configurations (rows, indexes, feature matrices, embeddings)?
6. **Cold start:** How do recommendations work before the user has provided enough triage data?

These don't need spikes — they need design deliberation informed by spike data.

## Decision Flow

```
Spike findings → Update FINDINGS.md
                      ↓
              Enough evidence? ──No──→ Design more experiments
                      │
                     Yes
                      ↓
              Update deliberation (deployment-portability.md)
                      ↓
              Conclude architectural decisions
                      ↓
              Create implementation phases (11, 12, etc.)
                      ↓
              Execute
```
