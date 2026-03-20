# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Updated:** 2026-03-19
**Status:** Spike 001: 8/8 success criteria answered (Round 1), Round 2 gap closure in progress (B1-informed filtering strategies). Spike 002: Round 2 remediation 8/9 complete. Per-category resource model built. Deliberation nearing conclusion — awaiting C1-R filtering strategies.
**Origin:** Post-Phase-10 deliberation on deployment and portability

## Context

After completing v0.1 (Phase 10: Agent Integration Test), interconnected areas of design uncertainty emerged around deployment, filtering, recommendation, and backend architecture. A spike program was created to investigate empirically.

### Key Discovery: Two Intertwined Questions

The spike program started as one question ("how do we deploy this?") but revealed two questions. Initially treated as independent, Spike 002 findings showed they are more intertwined than assumed:

1. **Deployment architecture** (Spike 001 A1c + Spike 002) — Which backend, how to distribute. Spike 002 showed backend choice is a search quality decision (not just performance), which means deployment and search/recommendation design are connected.

2. **Scoring/recommendation design** (Spike 001 A2, A3, B, C) — What signals predict paper importance? What filtering strategies work? These inform v0.2 features AND the deployment story (filtering affects scale estimates, which affect backend choice; corpus structure validates pre-filtering mitigations in the deliberation).

### Epistemic Correction (2026-03-19)

Both spikes were prematurely declared closer to done than they are. Spike 001 branched into Spike 002 after A1c, and neither was completed. The deployment deliberation was declared "ready to conclude" when its empirical foundation is 3/8 complete by Spike 001's own success criteria, and Spike 002 has unfixed methodological confounds.

See signal: `sig-2026-03-18-premature-spike002-closure`

### Capability Envelope Summary (A1c — Spike 001)

| Operation | Result | Implication |
|-----------|--------|-------------|
| FTS5 search | 30ms at 215K, 71ms at 500K | SQLite keyword search fine to 500K+ |
| TF-IDF similarity | 516ms at 215K, <100ms at 50K | Use embeddings or pre-filter at scale |
| Embedding search | 16ms at 215K (brute-force dot product) | pgvector is 5-23x faster (Spike 002 D3) |
| Concurrent SQLite | Zero degradation with WAL mode | Harvest daemon + MCP server coexist |
| Embedding compute | 35ms/paper CPU, 1.7ms/paper GPU (20x) | CPU incremental: 21s/day. Cold start: 2h overnight |
| Memory (all features) | ~472 MB at 215K (TF-IDF + embeddings) | Fits on any laptop (but mmap not yet validated) |

### Backend Comparison Summary (Spike 002 Round 1)

| Dimension | SQLite | PostgreSQL | Gap |
|-----------|--------|------------|-----|
| Search quality | FTS5: different results (Jaccard 0.39), fails on hyphens | tsvector: better stemming, handles all queries | **Confound:** query parser differences not controlled for |
| Search latency | 3.5–4.8x faster | Slower but interactive | Clean measurement |
| Vector search | numpy brute-force (3–14ms, linear) | HNSW (0.6–1ms, near-constant, recall ≥0.91) | Clean measurement |
| Writes | 5–6x faster bulk import | Both handle concurrent R+W | Clean measurement |
| Operations | 87x faster connections, instant backup, 2x smaller | — | Clean measurement |
| Workflow | 15ms (6-tool) | 21ms (6-tool), 1.4x | Simplified workflow, no vector search step |

### Architectural References

- ADR-0002: Metadata-first, lazy enrichment
- Doc 05 §4: Stack A → B trajectory
- Doc 10 Q16/Q17: Processing promotion strategies
- Deliberation: `.planning/deliberations/deployment-portability.md`
- Full findings: `.planning/spikes/001-volume-filtering-scoring-landscape/FINDINGS.md`
- Spike 002 findings: `.planning/spikes/002-backend-comparison/FINDINGS.md`

## Spike Sequence

### Complete

| # | Question | Type | Status | Key Outcome |
|---|----------|------|--------|-------------|
| 001 A1 | Volume mapping | Exploratory | **Complete** | 19K papers/month at 15 categories. Big4 = 12K/month. |
| 001 A1b | FTS5 search benchmark | Exploratory | **Complete** | <40ms p50 at 215K. Linear scaling. |
| 001 A1c | Capability envelope (TF-IDF, concurrent, embeddings) | Exploratory | **Complete** | All ops feasible to 215K+. See summary above. |
| 001 A2 | Corpus structure/visualization | Exploratory | **Complete** | Topic purity 0.40, 60.6% multi-category papers |
| 001 A3 | Distribution analysis | Exploratory | **Complete** | Gini 0.83, Zipf vocabulary, median 4 authors |
| 001 B1 | Signal literature review | Exploratory | **Complete** | Embeddings replacing TF-IDF (50.79%), hybrid systems dominate (55.56%) |
| 001 B2 | Computed signal exploration | Exploratory | **Complete** | FWCI r=0.75, content signals near-zero vs citations |
| 001 B3 | Importance analysis | Exploratory | **Complete** | Multi-dimensional: bibliometric vs content vs structural |
| 001 C1 | Coverage-regret + filtering (Rounds 1-3 partial) | Exploratory | **Complete with gaps** | No sharp elbow, 12 strategies profiled, smooth tradeoff. Round 3 items R10-R16 not run. |
| 001 C2 | Promotion pipeline simulation | Exploratory | **Complete** | All strategies feasible (1-13s GPU/day) |
| 002 D1-D6 | Backend comparison (6 dimensions) | Comparative | **Complete** | FTS5≠tsvector (Jaccard 0.39), pgvector HNSW 5-23x faster |
| 002 D1-R | Search quality remediation | Comparative | **Complete** | Divergence is ranking-function-driven, not quality gap |
| 002 D2-R | Baseline reproduction | Comparative | **Complete** | 20-60% drift; ratios valid, absolutes have variance |
| 002 D7 | Reference design comparison | Comparative | **Complete** | All our ops 20-100x faster than external APIs |
| 002 QV1-3 | Quick validations | Exploratory | **Complete** | Pre-filter works, mmap instant, MiniLM/SPECTER2 Jaccard 0.178 |

### Outstanding (from Spikes 001/002 — carried into Spike 003)

These items were designed but never executed. They are subsumed into Spike 003's design.

| # | Item | Original spike | Now addressed by |
|---|------|---------------|-----------------|
| 001 C1-R10 | Leave-one-out retrieval quality | Spike 001 Round 3 | Spike 003 — core evaluation metric in harness |
| 001 C1-R11 | Retrieval + reranking pipeline comparison | Spike 001 Round 3 | Spike 003 W3.4 |
| 001 C1-R12 | Seed count sensitivity (cold-start curve) | Spike 001 Round 3 | Spike 003 W4.1 |
| 001 C1-R13 | Interest breadth sensitivity | Spike 001 Round 3 | Spike 003 W4.2 |
| 001 C1-R14 | Marginal signal value analysis | Spike 001 Round 3 | Spike 003 W3.5 |
| 001 C1-R15 | SPECTER2 quality profiles | Spike 001 Round 3 | Spike 003 S1c profiling |
| 001 C1-R16 | Bibliographic coupling vs embedding similarity | Spike 001 Round 3 | Spike 003 S3a profiling |
| 001 | Round 2 FINDINGS.md integration | Spike 001 | Pending — results exist in data files but not integrated into FINDINGS.md |
| 001 | DESIGN.md checklist update (Round 2+3) | Spike 001 | Pending — experiments were run but checklist items not marked complete |
| 002 D6-R | Workflow + vector search | Spike 002 | Deferred — optional, main comparison done |
| 002 | DESIGN.md checklist update (Round 2) | Spike 002 | Pending — experiments were run but checklist items not marked complete |
| 002 | FINDINGS.md Round 2 integration | Spike 002 | Pending — Round 2 results in DECISION.md but FINDINGS.md still says "ROUND 1" |

### In Progress (Spike 003: Comprehensive Strategy Profiling)

**Status:** DESIGN.md complete. Wave 0 not started.

**Supersedes** the originally planned Spike 003 (SPECTER2 adapter only) and the 7 outstanding Spike 001 Round 3 items above.

Full design: `.planning/spikes/003-strategy-profiling/DESIGN.md`

**Purpose**: Complete quality/resource/behavioral profiles of all 44 viable strategies — individually, in combination, and across user contexts — producing a structured dataset for the installer and recommendation system configuration.

| Wave | Status | Content | Dependencies |
|------|--------|---------|-------------|
| W0 | **Pending** | SPECTER2 fix, eval harness, interest profiles, enrichment expansion | None (4 items parallelizable) |
| W1 | Pending | 44 strategies screened at default config | W0 |
| W2 | Pending | Parameter sensitivity for passing strategies | W1 rankings |
| W3 | Pending | Pairwise combinations, pipelines, ensemble, marginal value | W2 configs |
| W4 | Pending | Cold start, breadth, backend, scale, negative signals | W3 combinations |
| W5 | Pending | Profile dataset, installer logic, documentation | W4 |

### Pending (parallel work)

| Item | Status | Can run parallel with | Blocks |
|------|--------|----------------------|--------|
| Deliberation rewrite | **Not started** | Spike 003 (uses existing Spike 001+002 data) | Deliberation conclusion |
| Spike 001/002 DESIGN.md cleanup | Not started | Anything | Nothing (housekeeping) |
| Spike 001/002 FINDINGS.md integration | Not started | Anything | Nothing (housekeeping) |

### Spike 001 Success Criteria Scorecard

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Realistic paper volumes | **Answered** (A1) — 19K/month at 15 categories |
| 2 | Structural landscape | **Answered** (A2) — topic purity 0.40, 60.6% multi-category |
| 3 | Top 3-5 signals for scoring | **Answered** (B1-B2) — embeddings, FWCI, citations, bibcoupling, user signals |
| 4 | Coverage-regret tradeoff shape | **Answered** (C1) — no sharp elbow, smooth tradeoff, configurable slider |
| 5 | Promotion strategy recommendation | **Answered** (C1-C2) — two-layer: wide ingestion + adaptive promotion |
| 6 | 1-year resource requirements | **Answered** (C2) — 1-13s GPU/day, 1.5-15 GB/year |
| 7 | Capability envelope | **Answered** (A1c) — all ops feasible to 215K+ |
| 8 | NLP feasibility limits on laptop | **Answered** (A1c) — no infeasibility at tested scales |

**Score: 8/8 answered.** Qualified limitations in DECISION.md (SPECTER2 taint, proxy metrics, one month of data).

## Open Design Questions

These emerged from the spike and deliberation work. They need design deliberation, not experiments:

1. **Feature lifecycle layer** — Where do TF-IDF/embedding matrices live? How do they update incrementally? Memory-mapped storage, lazy loading, background refresh. This is a new architectural layer between storage and services.

2. **Smart cold-ingestion strategy** — On first install: prioritize user's configured categories for embedding, background the rest. Progress feedback during init. The 2-hour full-corpus embed is an overnight job, not a blocker.

3. **"Project" as first-class concept** — Different recommenders per research project. Not in any design doc yet.

4. **Cold start UX** — What does `arxiv-mcp init` look like? Seed corpus selection, category config, progress bar, "ready to use" threshold.

5. **Embedding model selection** — all-MiniLM-L6-v2 is general-purpose. SPECTER2 is academic-specific. QV3 provides data; final selection is a design decision.

6. **Search layer separation** — *(new, from Spike 002 D1)* Should search be extracted from the storage abstraction? If FTS5 ≠ tsvector, maybe search shouldn't be delegated to the database at all. Options: embedding-only search, standalone search engine (tantivy), or hybrid. This is a design question informed by D1 findings and QV3 results.

## Decision Flow (current)

```
Spike 001 (COMPLETE — 8/8 criteria) ─────────────┐
                                                   │
Spike 002 (COMPLETE — tradeoff map, DECISION.md) ─┤
                                                   │
Spike 003 (IN PROGRESS — strategy profiling) ──────┤
  W0: SPECTER2 fix + eval harness                 │
  W1: 44 strategies screened                       ├──→ Deliberation conclusion
  W2: Config sensitivity                          │         │
  W3: Combinations + pipelines                    │         ↓
  W4: Context sensitivity                         │    Phase 11 (Distribution)
  W5: Synthesis → strategy_profiles.json          │         │
                                                   │         ↓
Deliberation rewrite (PARALLEL with Spike 003) ────┘    Phase 12 (Storage Abstraction)
```

**What blocks the deliberation:**
1. ~~Spike 002 Round 2~~ — DONE
2. ~~Spike 001 success criteria~~ — DONE (8/8)
3. Spike 003 strategy profiles — needed for installer recommendations and strategy architecture
4. Deliberation rewrite — uses existing Spike 001+002 data, can run NOW in parallel

**Parallelization opportunities:**
- **Deliberation rewrite** can start immediately (uses existing data, doesn't need Spike 003)
- **Spike 003 W0 items** are independent of each other (SPECTER2, harness, profiles, enrichment)
- **Spike 003 W1 sub-waves** (1A, 1B, 1C, 1D) are independent of each other
- **Qualitative reviews** spawn as parallel agents at each review checkpoint

## Principles

1. **Each spike answers one question.** Comparative questions ("A vs B") are one spike with multiple experiments.
2. **Spikes produce findings, not decisions.** The deliberation process uses spike findings to make decisions.
3. **Spikes chain.** Later spikes use earlier findings to design better experiments.
4. **New spikes can emerge.** This roadmap is a living document. Unexpected findings create new questions.
5. **Rigor over speed.** Experiments should produce epistemologically reliable results — reproducible, falsifiable, with clear metrics and controlled variables.
6. **Treat DESIGN.md as a checklist.** *(added 2026-03-19)* Before declaring any spike complete, mechanically verify every protocol item and success criterion. The signal `sig-2026-03-18-premature-spike002-closure` documents what happens when this isn't done.
