# arXiv Discovery MCP

## What This Is

An MCP-native research discovery substrate centered on arXiv, designed for agents and humans to discover papers, expand from seeds, track research interests, monitor new publications, and triage efficiently — all with inspectable ranking and provenance. A modern, agent-usable successor to arxiv-sanity that preserves its product soul (discovery over overload, explicit taste modeling, fast triage) while reimagining it for MCP workflows.

## Core Value

Researchers and agents can discover, monitor, and triage arXiv papers through explicit, steerable interest modeling with inspectable results — not a generic "chat with papers" wrapper.

## Current State

`v0.1` has shipped and is now treated as a completed milestone.

The project is currently in **post-v0.1 inter-milestone exploration**:

- the implementation milestone is complete
- the active work is spike and deliberation work
- that work is intended to shape the next milestone rather than extend `v0.1` in-place

Primary active references:

- [v0.1-MILESTONE.md](./milestones/v0.1-MILESTONE.md)
- [NEXT-ROUND-SUITE.md](./spikes/NEXT-ROUND-SUITE.md)
- [local-gap-propagation-and-signal-interpretation.md](./deliberations/local-gap-propagation-and-signal-interpretation.md)

## Requirements

### Validated

`v0.1` shipped. The validated milestone requirement set is the completed `v0.1` requirement surface in [REQUIREMENTS.md](./REQUIREMENTS.md), which is now treated as frozen pending the next milestone.

### Active

- [ ] Ingest arXiv metadata reliably (OAI-PMH bulk + API search)
- [ ] Canonical paper model with arXiv identity, external IDs, time semantics (submission/update/announcement)
- [ ] Lexical search baseline (fielded metadata + abstract search)
- [ ] Recent-paper browsing with time-basis awareness
- [ ] Delta/checkpoint handling ("what's new since last check")
- [ ] Seed-based paper expansion (find related from seed papers)
- [ ] Multiple relatedness modes behind common interface
- [ ] Explicit workflow state: collections, triage states, saved queries
- [ ] Interest profile objects (seed sets, saved queries, followed authors — not just tags)
- [ ] Structured ranking explanations (why a paper surfaced)
- [ ] Provenance tracking for content artifacts and ranking signals
- [ ] Rights/license metadata per paper and content variant
- [ ] MCP server with tools, resources, and prompts (not one mega-search tool)
- [ ] Optional content normalization: abstract → HTML → source → PDF-derived markdown
- [ ] Content variant model with source-aware acquisition order
- [ ] OpenAlex enrichment adapter (graph, topics, related works, citations)
- [ ] Cost-aware design: metadata-first, lazy enrichment, selective embeddings

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
| Exploration-first architecture (ADR-0001) | Major uncertainty in retrieval, ranking, interest modeling | — Pending |
| Metadata-first, lazy enrichment (ADR-0002) | Cost-awareness, reversibility | — Pending |
| License and provenance first (ADR-0003) | Legal compliance, trust | — Pending |
| MCP as workflow substrate (ADR-0004) | Agent workflows need explicit state | — Pending |
| Stack A → B trajectory | Cheapest serious starting point with upgrade path | — Pending |
| arXiv as initial corpus | Core use case, manageable scope | — Pending |
| OpenAlex as primary enrichment | Best open data, free API, rich graph | — Pending |
| Multiple content backends behind one interface | Docling, Marker, GROBID all have strengths | — Pending |

---
*Last updated: 2026-04-16 after v0.1 completion and transition to inter-milestone exploration*
