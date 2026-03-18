# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Updated:** 2026-03-17
**Status:** Spike 001 capability envelope (A1c) complete. Deployment question answered. Remaining spike work addresses scoring/recommendation design (v0.2).
**Origin:** Post-Phase-10 deliberation on deployment and portability

## Context

After completing v0.1 (Phase 10: Agent Integration Test), interconnected areas of design uncertainty emerged around deployment, filtering, recommendation, and backend architecture. A spike program was created to investigate empirically.

### Key Discovery: Two Separate Questions

The spike program started as one question ("how do we deploy this?") but revealed two independent questions:

1. **Deployment architecture** (answered by A1+A1c) — SQLite handles the full feature set at personal scale. PostgreSQL is an opt-in upgrade for multi-writer concurrency. The tier differentiator is GPU availability for embedding computation, not database features for search.

2. **Scoring/recommendation design** (A2, B, C phases) — What signals predict paper importance? How should the recommendation system work? What filtering strategies optimize coverage vs volume? These inform v0.2 features, not deployment architecture.

### Capability Envelope Summary (A1c)

| Operation | Result | Implication |
|-----------|--------|-------------|
| FTS5 search | 30ms at 215K, 71ms at 500K | SQLite keyword search fine to 500K+ |
| TF-IDF similarity | 516ms at 215K, <100ms at 50K | Use embeddings or pre-filter at scale |
| Embedding search | 16ms at 215K (brute-force dot product) | pgvector unnecessary at personal scale |
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

### Deprioritized

| # | Question | Why deprioritized |
|---|----------|-------------------|
| 002 | PostgreSQL performance benchmarking | SQLite handles the workload. PostgreSQL advantage is architectural (multi-writer), not performance. Only relevant if multi-user demand emerges. |

## Open Design Questions

These emerged from the spike and deliberation work. They need design deliberation, not experiments:

1. **Feature lifecycle layer** — Where do TF-IDF/embedding matrices live? How do they update incrementally? Memory-mapped storage, lazy loading, background refresh. This is a new architectural layer between storage and services.

2. **Smart cold-ingestion strategy** — On first install: prioritize user's configured categories for embedding, background the rest. Progress feedback during init. The 2-hour full-corpus embed is an overnight job, not a blocker.

3. **"Project" as first-class concept** — Different recommenders per research project. Not in any design doc yet.

4. **Cold start UX** — What does `arxiv-mcp init` look like? Seed corpus selection, category config, progress bar, "ready to use" threshold.

5. **Embedding model selection** — all-MiniLM-L6-v2 is general-purpose. SPECTER2 is academic-specific. Tradeoff between availability, speed, and domain relevance.

## Decision Flow

```
Spike 001 A1c findings (DONE)
      ↓
Deliberation updated (DONE — 2026-03-17)
      ↓
Phase 11 (Distribution) ← ready to plan/execute
      ↓
Phase 12 (Storage Abstraction) ← ready to plan, revised scope
      ↓
Spike 001 A2/B/C (in parallel with implementation — informs v0.2 recommendation features)
```

The deployment path is unblocked. Spike 001's remaining phases inform v0.2 feature design and can run in parallel with Phase 11/12 implementation.

## Principles

1. **Each spike answers one question.** Comparative questions ("A vs B") are one spike with multiple experiments.
2. **Spikes produce findings, not decisions.** The deliberation process uses spike findings to make decisions.
3. **Spikes chain.** Later spikes use earlier findings to design better experiments.
4. **New spikes can emerge.** This roadmap is a living document. Unexpected findings create new questions.
5. **Rigor over speed.** Experiments should produce epistemologically reliable results — reproducible, falsifiable, with clear metrics and controlled variables.
