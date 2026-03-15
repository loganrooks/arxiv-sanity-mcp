# Spike Program: Deployment, Filtering, and Backend Architecture

**Created:** 2026-03-15
**Status:** Active
**Origin:** Post-Phase-10 deliberation on deployment and portability

## Context

After completing v0.1 (Phase 10: Agent Integration Test), three interconnected areas of design uncertainty emerged that cannot be resolved through discussion alone — they require empirical investigation.

### How We Got Here

**Deliberation: deployment-portability.md** (2026-03-14, concluded)

The initial question was "how would someone install this on another computer?" Investigation revealed:
- Current install is 8 manual steps, ~15 min, requires PostgreSQL
- arxiv-sanity-lite (our inspiration) runs entirely on SQLite + pickle files on a $5 VPS
- The MCP ecosystem standard is zero-install via `uvx` (Python) or `npx` (Node.js)
- Our PostgreSQL dependency is the main barrier to frictionless distribution

This led to a tiered deployment proposal (SQLite for personal, PostgreSQL for power users, HTTP for hosted). But before committing to that architecture, we identified assumptions that need empirical testing.

**Key assumptions that need testing:**
1. "SQLite handles our scale" — stated without knowing what our scale actually is
2. "FTS5 search quality is equivalent to tsvector" — asserted without comparison
3. "100K papers is the realistic corpus size" — based on arXiv stats research, never validated against our actual filtering pipeline
4. "The storage interface will be clean and narrow" — architectural claim, untested

**Deeper questions that emerged during deliberation:**
- The promotion pipeline (how papers move from metadata-only → enriched → embedded) has no scoring system — it's entirely manual/demand-driven
- Open Question 16 in docs/10-open-questions.md asks: "What is the right processing intensity promotion strategy?" and lists four candidates, none implemented
- The volume of papers isn't just a backend concern — it's entangled with filtering strategy, scoring design, and the regret/coverage tradeoff
- We need to understand the filtering landscape BEFORE we can design meaningful backend benchmarks

### Architectural References

- ADR-0002: Metadata-first, lazy enrichment ("ingest eagerly, enrich lazily, embed selectively")
- Doc 05 §4: Stack A → B trajectory (metadata + lexical first, selective semantic later)
- Doc 05 §7: Compute profiles (Bronze/Silver/Gold)
- Doc 10 Q16: Processing promotion strategies (demand-driven, cohort, budget-constrained, two-phase)
- Doc 10 Q17: Retrospective demotion
- ProcessingTier enum: METADATA_ONLY → FTS_INDEXED → ENRICHED → EMBEDDED → CONTENT_PARSED
- categories.toml: 15 categories across 4 archives (cs, stat, math, eess)

## Spike Sequence

### Known Spikes

| # | Question | Type | Depends On | Status |
|---|----------|------|------------|--------|
| 001 | Volume, filtering, and scoring landscape | Exploratory | — | Designing |
| 002 | Backend performance benchmarking (SQLite vs PostgreSQL) | Comparative | 001 (volume estimates inform test parameters) | Blocked on 001 |

### Anticipated (may emerge from Spike 001-002 findings)

| Question | Would be triggered if... |
|----------|------------------------|
| Promotion pipeline strategies | Spike 001 reveals that scoring signals at ingestion time are predictive enough to automate promotion |
| Migration mechanics (SQLite → PostgreSQL) | Spike 002 confirms both backends are viable and migration is part of the tier system |
| Scoring system design | Spike 001 reveals a clear candidate scoring approach worth prototyping |
| Continuous indexing daemon | Volume mapping reveals that daily incremental harvest needs automation |
| Hosted mode resource profiling | Spike 002 reveals viable hosted deployment and someone wants to test multi-user performance |

### Principles

1. **Each spike answers one question.** Comparative questions ("A vs B") are one spike with multiple experiments.
2. **Spikes produce findings, not decisions.** The deliberation process uses spike findings to make decisions.
3. **Spikes chain.** Later spikes use earlier findings to design better experiments.
4. **New spikes can emerge.** This roadmap is a living document. Unexpected findings create new questions.
5. **Rigor over speed.** Experiments should be designed to produce epistemologically reliable results — reproducible, falsifiable, with clear metrics and controlled variables.

## Decision Flow

```
Spike findings
      ↓
Update deliberation (deployment-portability.md)
      ↓
Conclude deployment architecture decisions
      ↓
Create implementation phases (11, 12, etc.)
      ↓
Execute
```

The spike program feeds back into the deployment deliberation. We don't create implementation phases until the spikes give us enough evidence to make confident architectural decisions.
