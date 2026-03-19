# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Updated:** 2026-03-18
**Status:** Spike 001 A1c complete (SQLite-only data). Spike 002 designed and active — comparative PostgreSQL benchmarks needed before deployment conclusions. Spike 001 A2/B/C address scoring/recommendation.
**Origin:** Post-Phase-10 deliberation on deployment and portability

## Context

After completing v0.1 (Phase 10: Agent Integration Test), interconnected areas of design uncertainty emerged around deployment, filtering, recommendation, and backend architecture. A spike program was created to investigate empirically.

### Key Discovery: Two Separate Questions

The spike program started as one question ("how do we deploy this?") but revealed two independent questions:

1. **Deployment architecture** (partially answered by A1+A1c, Spike 002 in progress) — SQLite handles the full feature set at personal scale in isolation. PostgreSQL comparative data needed before concluding sufficiency — one-sided benchmarks cannot support comparative claims. Spike 002 provides the other side.

2. **Scoring/recommendation design** (A2, B, C phases) — What signals predict paper importance? How should the recommendation system work? What filtering strategies optimize coverage vs volume? These inform v0.2 features, not deployment architecture.

### Capability Envelope Summary (A1c)

| Operation | Result | Implication |
|-----------|--------|-------------|
| FTS5 search | 30ms at 215K, 71ms at 500K | SQLite keyword search fine to 500K+ |
| TF-IDF similarity | 516ms at 215K, <100ms at 50K | Use embeddings or pre-filter at scale |
| Embedding search | 16ms at 215K (brute-force dot product) | pgvector comparison needed (Spike 002) |
| Concurrent SQLite | Zero degradation with WAL mode | Harvest daemon + MCP server coexist |
| Embedding compute | 35ms/paper CPU, 1.7ms/paper GPU (20x) | CPU incremental: 21s/day. Cold start: 2h overnight |
| Memory (all features) | ~472 MB at 215K (TF-IDF + embeddings) | Fits on any laptop |

### Architectural References

- ADR-0002: Metadata-first, lazy enrichment
- Doc 05 §4: Stack A → B trajectory
- Doc 10 Q16/Q17: Processing promotion strategies
- Deliberation: `.planning/deliberations/deployment-portability.md`
- Full findings: `.planning/spikes/001-volume-filtering-scoring-landscape/FINDINGS.md`

## Spike Sequence

### Complete

| # | Question | Type | Status | Key Outcome |
|---|----------|------|--------|-------------|
| 001 A1+A1c | Volume, scale, and capability envelope | Exploratory | **Complete** | Deployment question answered. SQLite sufficient. See capability summary above. |

### Active (Spike 001 remaining phases)

| Phase | Question | Priority | Blocks |
|-------|----------|----------|--------|
| A2: Corpus visualization | What does the paper space look like structurally? | Medium | Informs B1-B2 signal design |
| A3: Distribution analysis | What are the statistical properties of the corpus? | Medium | Informs B2-B3 |
| B1: Signal literature review | What do existing recommenders use as features? | Medium | Informs B2 |
| B2: Computed signal exploration | Which signals predict importance in our data? | Medium | Informs C1 |
| B3: Importance analysis | Is "importance" one thing or multiple dimensions? | Medium | Informs C1 |
| C1: Coverage-regret | What's the tradeoff shape for filtering strategies? | Lower | Informs promotion pipeline design |
| C2: Promotion simulation | What are the resource costs of different strategies? | Lower | Informs v0.2 planning |
| C3: Backend implications | At what scale do operations become slow? | **Deprioritized** | Mostly answered by A1c |

### Quick Validation Experiments (new, emerged from A1c findings)

Small experiments that validate the mitigations proposed in the deliberation update:

| Experiment | What it validates | Effort |
|-----------|------------------|--------|
| Pre-filtered TF-IDF cosine | Does category scoping keep similarity <100ms at 215K? | Small — reuse A1c.1 script |
| Memory-mapped feature loading | Is mmap actually near-instant for 472 MB? | Small — prototype |
| FTS5 vs tsvector quality | Do they return equivalent results for same queries? | Medium — needs PostgreSQL comparison |
| Embedding quality (MiniLM vs SPECTER2) | Is a general model good enough for academic abstracts? | Medium — needs SPECTER2 |

### Active (Spike 002: Backend Comparison)

| # | Question | Type | Status | Key Outcome |
|---|----------|------|--------|-------------|
| 002 | PostgreSQL vs SQLite comparative benchmarks | Comparative | **Designed** | 6 dimensions: search quality, latency, vector search, writes, ops, workflow. DESIGN.md complete. Awaiting execution. |

> **Epistemic correction (2026-03-17):** Spike 002 was initially deprioritized based on Spike 001's SQLite-only data. This was premature — comparative claims ("SQLite is sufficient") require comparative data. Spike 001 results are hypotheses under test, not conclusions.

## Open Design Questions

These emerged from the spike and deliberation work. They need design deliberation, not experiments:

1. **Feature lifecycle layer** — Where do TF-IDF/embedding matrices live? How do they update incrementally? Memory-mapped storage, lazy loading, background refresh. This is a new architectural layer between storage and services.

2. **Smart cold-ingestion strategy** — On first install: prioritize user's configured categories for embedding, background the rest. Progress feedback during init. The 2-hour full-corpus embed is an overnight job, not a blocker.

3. **"Project" as first-class concept** — Different recommenders per research project. Not in any design doc yet.

4. **Cold start UX** — What does `arxiv-mcp init` look like? Seed corpus selection, category config, progress bar, "ready to use" threshold.

5. **Embedding model selection** — all-MiniLM-L6-v2 is general-purpose. SPECTER2 is academic-specific. Tradeoff between availability, speed, and domain relevance.

## Decision Flow

```
Spike 001 A1c findings (DONE — SQLite-only baseline)
      ↓
Spike 002 execution (ACTIVE — PostgreSQL comparative data)
      ↓
Deliberation conclusion (BLOCKED on Spike 002 — both-backend data required)
      ↓
Phase 11 (Distribution) ← blocked on deployment deliberation
      ↓
Phase 12 (Storage Abstraction) ← blocked on deployment deliberation
      ↓
Spike 001 A2/B/C (in parallel — informs v0.2 recommendation features)
```

The deployment path is blocked on Spike 002 comparative data. Phase 11/12 planning requires both-backend evidence, not SQLite-only measurements.

## Principles

1. **Each spike answers one question.** Comparative questions ("A vs B") are one spike with multiple experiments.
2. **Spikes produce findings, not decisions.** The deliberation process uses spike findings to make decisions.
3. **Spikes chain.** Later spikes use earlier findings to design better experiments.
4. **New spikes can emerge.** This roadmap is a living document. Unexpected findings create new questions.
5. **Rigor over speed.** Experiments should produce epistemologically reliable results — reproducible, falsifiable, with clear metrics and controlled variables.
