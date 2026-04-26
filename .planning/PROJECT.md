# arXiv Discovery MCP

## What This Is

An MCP-native research discovery substrate centered on arXiv, designed for agents and humans to discover papers, expand from seeds, track research interests, monitor new publications, and triage efficiently — all with inspectable ranking and provenance. A modern, agent-usable successor to arxiv-sanity that preserves its product soul (discovery over overload, explicit taste modeling, fast triage) while reimagining it for MCP workflows.

## Core Value

Researchers and agents can discover, monitor, and triage arXiv papers through explicit, steerable interest modeling with inspectable results — not a generic "chat with papers" wrapper.

## Current State

`v0.1` shipped 2026-03-14 and is frozen as a completed milestone.

`v0.2` (multi-lens substrate) is the **active milestone**, committed via [ADR-0005](../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md) on 2026-04-25. Phase plans for Phases 12-17 are authored. Phase 12 plan-1 authoring is on hold pending the gsd-2 long-horizon-planning uplift evaluation (see handoff document and LONG-ARC.md). The 2026-04-25/26 plan-revision and governance-audit cycles produced Wave 1 (uncontested fixes), Wave 3 (B-tier doctrine-adjacent edits), and Wave 4 (governance-doc currency refresh) commits; Wave 5 (exemplar AGENTS/CLAUDE harvest) and the gsd-2 uplift initiative are downstream.

Primary active references:

**For current milestone work (v0.2):**
- [milestones/v0.2-MILESTONE.md](./milestones/v0.2-MILESTONE.md) — multi-lens substrate, the active milestone
- [VISION.md](./VISION.md) — product identity
- [LONG-ARC.md](./LONG-ARC.md) — planning doctrine
- [ROADMAP.md](./ROADMAP.md) — phase plan with Phases 12-17 authored

**For methodology / spike work:**
- [spikes/METHODOLOGY.md](./spikes/METHODOLOGY.md) — interpretive lenses + practice disciplines (M1 independent-dispatch sub-discipline at Hypothesis status)

**For post-audit context (2026-04-25/26 cycle):**
- [audits/2026-04-25-v0.2-plan-audit-synthesis.md](./audits/2026-04-25-v0.2-plan-audit-synthesis.md) (revised with dispositions)
- [audits/2026-04-26-governance-audit-synthesis.md](./audits/2026-04-26-governance-audit-synthesis.md) (revised with G-B-tier dispositions in §2.5)
- [handoffs/](./handoffs/) — session continuity records

**Historical (completed):**
- [milestones/v0.1-MILESTONE.md](./milestones/v0.1-MILESTONE.md) — shipped 2026-03-14, frozen

**Likely partially superseded — verify before consulting:**
- [spikes/NEXT-ROUND-SUITE.md](./spikes/NEXT-ROUND-SUITE.md) — pre-redirection spike suite; partially superseded by the ADR-0005 multi-lens reshape

## Requirements

### Validated

`v0.1` shipped. The validated milestone requirement set is the completed `v0.1` requirement surface in [REQUIREMENTS.md](./REQUIREMENTS.md), which is now treated as frozen pending the next milestone.

### Shipped (v0.1, 2026-03-14)

- [x] Ingest arXiv metadata reliably (OAI-PMH bulk + API search)
- [x] Canonical paper model with arXiv identity, external IDs, time semantics (submission/update/announcement)
- [x] Lexical search baseline (fielded metadata + abstract search)
- [x] Recent-paper browsing with time-basis awareness
- [x] Delta/checkpoint handling ("what's new since last check")
- [x] Seed-based paper expansion (find related from seed papers)
- [x] Multiple relatedness modes behind common interface
- [x] Explicit workflow state: collections, triage states, saved queries
- [x] Interest profile objects (seed sets, saved queries, followed authors — not just tags)
- [x] Structured ranking explanations (why a paper surfaced)
- [x] Provenance tracking for content artifacts and ranking signals
- [x] Rights/license metadata per paper and content variant
- [x] MCP server with tools, resources, and prompts (not one mega-search tool) — 13 tools, 4 resources, 3 prompts
- [x] Optional content normalization: abstract → HTML → source → PDF-derived markdown
- [x] Content variant model with source-aware acquisition order
- [x] OpenAlex enrichment adapter (graph, topics, related works, citations)
- [x] Cost-aware design: metadata-first, lazy enrichment, selective embeddings

### Active (v0.2 — multi-lens substrate)

Full surface in [REQUIREMENTS.md](./REQUIREMENTS.md) under v0.2 codes. Summary:

- [ ] LENS-01..05 — Lens architecture and primitive shape
- [ ] CITE-01..04 — Citation/community lens specifics, provenance
- [ ] LDIS-01..03 — Lens-disagreement and intersection ops
- [ ] LPILOT-01..03 — Longitudinal pilot harness (one user; replaces superseded `008` tournament)
- [ ] MCP-08, MCP-09 — MCP surface lens-awareness

17 v0.2 requirement codes total. Phase plans in `ROADMAP.md` Phases 12-17.

### Out of Scope

- General-purpose paper chatbot — discovery is the product, not conversation
- Full corpus embedding on day one — selective/lazy embedding only
- All-literature warehouse before arXiv works well — arXiv first
- Complex distributed infrastructure — single-node, local-first default
- Opaque recommender with hidden state — inspectability is core
- Benchmark leaderboard clone — not the product identity
- Automatic profile learning without user confirmation — explicit > implicit
- Real-time chat or collaboration features — defer to later phases

## Context

### Product Heritage
arxiv-sanity (Karpathy) was valuable for: recent-paper monitoring, explicit taste via libraries/tags, fast browsing/triage, and inspectable similarity. This project preserves those values but reimagines them for MCP-native agent workflows.

### Technical Environment
- Target hardware: single-node with GTX 1080 Ti (11GB), 32GB RAM
- Existing scholarly pipeline on this machine: zlibrary-mcp, scholardoc, philo-rag-simple, philograph-mcp
- Available infrastructure: PostgreSQL, Redis, Docker, PaddleOCR container
- MCP ecosystem: Claude Code with sequential-thinking, context7, tavily, morphllm, philpapers, zlibrary servers

### Data Sources
- **arXiv**: Core corpus. API search, OAI-PMH bulk metadata, RSS feeds, HTML/source/PDF content
- **OpenAlex**: Best open enrichment — graph, topics, related works, citations, semantic search
- **Semantic Scholar**: Optional adapter — recommendations, SPECTER2 embeddings
- **Crossref/OpenCitations**: Optional DOI/citation enrichment

### Key Design Documents
Extensive bootstrap documentation in `docs/01-11` covering vision, product principles, design space, reference designs, architecture hypotheses, MCP surface options, data sources/rights, evaluation framework, roadmap, and open questions. Four accepted ADRs in `docs/adrs/`.

### Architectural Trajectory
Stack A (metadata + lexical + graph) → Stack B (+ selective local semantic). Bronze → Silver → Gold compute profiles. Candidate generation → constraint filtering → reranking → diversification → explanation assembly pipeline.

## Constraints

- **Rights**: arXiv metadata is freely reusable; full e-prints require per-paper license checks. Hosted/public mode must be conservative. No redistribution of full text without rights verification.
- **Cost**: Metadata-first, lazy enrichment, selective embeddings. No expensive infrastructure without strong justification.
- **Explainability**: Structured explanations before prose. Every result must be inspectable.
- **Provenance**: Every content artifact and ranking signal records source, timestamp, rights basis, conversion path.
- **MCP Design**: Workflow substrate, not thin search wrapper. Tools + resources + prompts. Intent-based tool names (not implementation-based).
- **Exploration-first**: Multiple retrieval/ranking strategies coexist. No premature commitment to one approach. ADR-0001.
- **Abstractions**: Use paper, content variant, interest profile, collection, saved query, watch, triage state, result set, ranking explanation. Do not force tags as universal model.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Exploration-first architecture (ADR-0001) | Major uncertainty in retrieval, ranking, interest modeling | Accepted; honored in v0.1 (multiple ranking signals; per-result inspection); upgraded to delivery commitment in v0.2 via ADR-0005 (≥2 shipped lenses) |
| Metadata-first, lazy enrichment (ADR-0002) | Cost-awareness, reversibility | Accepted; OpenAlex enrichment ships as on-demand per-paper rather than bulk |
| License and provenance first (ADR-0003) | Legal compliance, trust | Accepted; RightsChecker + per-content-variant provenance + per-ranking-signal provenance shipped in v0.1 |
| MCP as workflow substrate (ADR-0004) | Agent workflows need explicit state | Accepted; v0.1 ships MCP server with 13 tools, 4 resources, 3 prompts; validated with real workflows in Phase 5 |
| Stack A → B trajectory | Cheapest serious starting point with upgrade path | Stack A operational in v0.1 (metadata + lexical + graph via OpenAlex); Stack B not yet introduced (selective semantic deferred) |
| arXiv as initial corpus | Core use case, manageable scope | In effect; 126 papers ingested for v0.2 spike work; broader corpora not added |
| OpenAlex as primary enrichment | Best open data, free API, rich graph | Accepted; sole external enrichment source in v0.1; Semantic Scholar adapter deferred to v0.3 |
| Multiple content backends behind one interface | Docling, Marker, GROBID all have strengths | Partial; ContentAdapter protocol shipped with MarkerAdapter; Docling/GROBID adapters deferred |
| v0.2 ships multi-lens substrate (ADR-0005) | ADR-0001 honored in implementation; lens abstraction validated by shipping a second lens (citation/community); profile primitive generalized to bundle-of-signals | Accepted 2026-04-25; v0.2 phases 12-17 authored; implementation on hold pending gsd-2 uplift evaluation |

---
*Last updated: 2026-04-26 — full refresh after Wave-3 + Wave-4 plan-revision and governance-doc audit cycles. Prior currency was 2026-04-25 (immediately after ADR-0005); body had not been refreshed to reflect the v0.2 commitment until this pass. Triggered by governance-comparison §5 joint blind spot acknowledgment that PROJECT.md was not in either Wave-2 audit's scope.*
