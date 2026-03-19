# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Updated:** 2026-03-19
**Status:** Both spikes in progress. Spike 001 is 3/8 complete by its success criteria (A1, A1c done; A2, A3, B, C pending). Spike 002 Round 1 dimensions done but has methodological gaps requiring Round 2 remediation. Neither spike can be concluded yet. Deliberation blocked on spike completion.
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

### Complete (verified)

| # | Question | Type | Status | Key Outcome |
|---|----------|------|--------|-------------|
| 001 A1 | Volume mapping | Exploratory | **Complete** | 19K papers/month at 15 categories. Big4 = 12K/month. |
| 001 A1b | FTS5 search benchmark | Exploratory | **Complete** | <40ms p50 at 215K. Linear scaling. |
| 001 A1c | Capability envelope (TF-IDF, concurrent, embeddings) | Exploratory | **Complete** | See summary above. |

### In Progress (Spike 002 Round 2: Remediation)

| Item | What it fixes | Blocks |
|------|-------------|--------|
| D1-R1: Query-parsing confound | plainto_tsquery + FTS5 escaping | Accurate D1 conclusions |
| D1-R2: Stemming analysis | Porter vs Snowball comparison | Understanding *why* results differ |
| D1-R3: Result inspection | Are divergent papers better/worse/just different? | Whether quality gap matters |
| D2-R: A1b baseline reproduction | Measurement stability confirmation | Trust in all latency comparisons |
| D7: Reference design comparison | Our numbers in context of systems users know | Whether our latencies are "good" or "bad" |
| QV1: Pre-filtered TF-IDF | Validates deliberation mitigation | Deliberation tier model |
| QV2: mmap feature loading | Validates "instant startup" claim | Deliberation tier model |
| QV3: MiniLM vs SPECTER2 | Embedding model choice | D3 may need re-evaluation if SPECTER2 is 768-dim |
| D6-R: Workflow with vector search | Optional, if time permits | More accurate compound comparison |

### Pending (Spike 001 remaining — A2, A3, B, C)

**Dependency chain:**
```
A2 (corpus viz) ──┐
A3 (distributions)─┼──→ B2 (computed signals) ──→ B3 (importance) ──→ C1 (coverage-regret) ──→ C2 (promotion sim)
B1 (lit review) ───┘
```

| Phase | Question | Priority | Blocks | Dependencies |
|-------|----------|----------|--------|-------------|
| **A2** | What does the paper space look like structurally? | **High** | Validates pre-filtering, informs B2 | None (uses existing embeddings) |
| **A3** | Statistical properties of corpus features? | **High** | Informs B2-B3 normalization | None |
| **B1** | What do existing recommenders use as signals? | **High** | Informs B2 signal selection | None (research task) |
| **B2** | Which signals predict importance in our data? | Medium | Informs C1, B3 | A2, A3, B1. Needs OpenAlex enrichment (~500 papers). |
| **B3** | Is importance one thing or multiple dimensions? | Medium | Informs C1, ranking model | B2 |
| **C1** | Coverage-regret tradeoff shape? Elbow? | Medium | Informs C2, filtering design | B2, B3 |
| **C2** | Resource costs of promotion strategies (1 year)? | Medium | Informs operational planning | C1, A1 |
| ~~C3~~ | ~~Backend implications~~ | Deprioritized | Answered by A1c + Spike 002 | — |

### Spike 001 Success Criteria Scorecard

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Realistic paper volumes | **Answered** (A1) |
| 2 | Structural landscape | **Unanswered** (A2 pending) |
| 3 | Top 3-5 signals for scoring | **Unanswered** (B1-B3 pending) |
| 4 | Coverage-regret tradeoff shape | **Unanswered** (C1 pending) |
| 5 | Promotion strategy recommendation | **Unanswered** (C2 pending) |
| 6 | 1-year resource requirements | **Unanswered** (C2 pending) |
| 7 | Capability envelope | **Answered** (A1c) |
| 8 | NLP feasibility limits on laptop | **Answered** (A1c) |

**Score: 3/8 answered.**

## Open Design Questions

These emerged from the spike and deliberation work. They need design deliberation, not experiments:

1. **Feature lifecycle layer** — Where do TF-IDF/embedding matrices live? How do they update incrementally? Memory-mapped storage, lazy loading, background refresh. This is a new architectural layer between storage and services.

2. **Smart cold-ingestion strategy** — On first install: prioritize user's configured categories for embedding, background the rest. Progress feedback during init. The 2-hour full-corpus embed is an overnight job, not a blocker.

3. **"Project" as first-class concept** — Different recommenders per research project. Not in any design doc yet.

4. **Cold start UX** — What does `arxiv-mcp init` look like? Seed corpus selection, category config, progress bar, "ready to use" threshold.

5. **Embedding model selection** — all-MiniLM-L6-v2 is general-purpose. SPECTER2 is academic-specific. QV3 provides data; final selection is a design decision.

6. **Search layer separation** — *(new, from Spike 002 D1)* Should search be extracted from the storage abstraction? If FTS5 ≠ tsvector, maybe search shouldn't be delegated to the database at all. Options: embedding-only search, standalone search engine (tantivy), or hybrid. This is a design question informed by D1 findings and QV3 results.

## Decision Flow

```
Spike 001 A1c (DONE) ─────────────────────────┐
                                                │
Spike 002 Round 1 (DONE, has confounds) ───────┤
                                                │
Spike 002 Round 2: Remediation (IN PROGRESS) ──┤
                                                ├──→ Deliberation conclusion
Spike 001 A2 (PENDING — validates mitigations) ┤
                                                │
Spike 001 A3, B1 (PENDING — parallel) ─────────┤
                                                │
Spike 001 B2, B3 (PENDING — needs A2+A3+B1) ──┤
                                                │
Spike 001 C1, C2 (PENDING — needs B2+B3) ──────┘
                                                │
                                                ↓
                                    Phase 11 (Distribution)
                                                ↓
                                    Phase 12 (Storage Abstraction)
```

The deliberation cannot conclude until:
1. Spike 002 methodological gaps are fixed (Round 2)
2. Spike 001 A2 validates the pre-filtering assumption
3. Enough of B/C is done to answer the Spike 001 success criteria

## Execution Order

Recommended execution order considering dependencies and parallelizability:

**Wave 1 (no dependencies, parallelizable):**
- Spike 002 D1-R1, D1-R2, D1-R3 (D1 remediation)
- Spike 002 D2-R (baseline reproduction)
- Spike 001 A2 (corpus visualization — uses existing embeddings)
- Spike 001 A3 (distribution analysis)
- Spike 001 B1 (literature review — research task)

**Wave 2 (depends on Wave 1):**
- Spike 002 D7 (reference design comparison — live API calls)
- Spike 002 QV1, QV2 (pre-filtered TF-IDF, mmap)
- Spike 002 QV3 (MiniLM vs SPECTER2 — may affect D3 conclusions)
- Spike 001 B2 (computed signals — needs A2, A3, B1)

**Wave 3 (depends on Wave 2):**
- Spike 001 B3 (importance analysis — needs B2)
- Spike 002 FINDINGS.md update + DECISION.md

**Wave 4 (depends on Wave 3):**
- Spike 001 C1, C2 (coverage-regret, promotion sim — needs B2, B3)
- Spike 001 FINDINGS.md update + DECISION.md

**Wave 5:**
- Deliberation conclusion
- Phase 11/12 planning

## Principles

1. **Each spike answers one question.** Comparative questions ("A vs B") are one spike with multiple experiments.
2. **Spikes produce findings, not decisions.** The deliberation process uses spike findings to make decisions.
3. **Spikes chain.** Later spikes use earlier findings to design better experiments.
4. **New spikes can emerge.** This roadmap is a living document. Unexpected findings create new questions.
5. **Rigor over speed.** Experiments should produce epistemologically reliable results — reproducible, falsifiable, with clear metrics and controlled variables.
6. **Treat DESIGN.md as a checklist.** *(added 2026-03-19)* Before declaring any spike complete, mechanically verify every protocol item and success criterion. The signal `sig-2026-03-18-premature-spike002-closure` documents what happens when this isn't done.
