# Research Summary: arXiv Discovery MCP

**Domain:** MCP-native scholarly paper discovery, monitoring, and triage system
**Researched:** 2026-03-08
**Overall confidence:** HIGH

## Executive Summary

The arXiv Discovery MCP project occupies a genuine gap in the scholarly tools ecosystem. Existing arXiv MCP servers (blazickjp, afrise, daheepk) are thin search-and-download wrappers with no workflow state. Existing scholarly discovery tools (Semantic Scholar, Connected Papers, ResearchRabbit, Litmaps) are web-only, human-only, and closed-source. No product combines discovery-quality features with agent-usable workflow state through the MCP protocol.

The technology stack is Python 3.13 with the official MCP SDK (FastMCP), PostgreSQL 16 as the single data store (relational + FTS + vector), Redis for caching/queuing, and a layered architecture separating MCP protocol translation from business logic from retrieval adapters. This stack leverages infrastructure already running on the target machine (PostgreSQL 16.11, Redis 7.0.15, GTX 1080 Ti with CUDA 12.4) and avoids introducing unnecessary services.

The architecture follows the project's own ADRs: exploration-first (multiple retrieval adapters behind common interfaces), metadata-first with lazy enrichment, license and provenance tracking from day one, and MCP as a workflow substrate rather than a thin search wrapper. The retrieval pipeline is designed as composable stages (candidate generation, filtering, reranking, explanation assembly) so retrieval strategies can be compared without rewriting services.

The most critical pitfalls are: (1) treating arXiv dates as simple timestamps when arXiv has four distinct temporal semantics, (2) naive OAI-PMH harvesting that loses data due to resumption token expiry and base URL changes, (3) MCP tool proliferation that bloats LLM context, (4) premature embedding commitment before establishing a lexical+graph baseline, and (5) ignoring per-paper content rights in the architecture.

## Key Findings

**Stack:** Python 3.13 + MCP SDK (FastMCP) + PostgreSQL 16 (FTS + pgvector) + asyncpg + SQLAlchemy 2.0 + SPECTER2 embeddings. Everything in one database. No separate search engine needed at this scale.

**Architecture:** Thin MCP layer over thick services over composable retrieval pipeline. Four-stage pipeline: candidate generation (lexical/semantic/graph/metadata adapters) -> constraint filtering -> reranking -> explanation assembly. PostgreSQL as single canonical store. Redis for caching and job queues.

**Critical pitfall:** arXiv's time semantics (submission date != announcement date != OAI-PMH datestamp != identifier month) must be modeled explicitly in the paper schema from Phase 1. Getting this wrong breaks delta/checkpoint logic and "what's new" feeds -- and retrofitting is extremely expensive.

## Implications for Roadmap

Based on research, suggested phase structure:

1. **Phase 1: Metadata Substrate** -- Repo scaffold, domain models, PostgreSQL schema, OAI-PMH ingestion, tsvector generation, basic lexical search
   - Addresses: Paper model, time semantics, ingestion, lexical search baseline
   - Avoids: Time semantics pitfall, OAI-PMH harvesting pitfall, rights metadata pitfall
   - Dependencies: None (foundation)

2. **Phase 2: Workflow State** -- Collections, triage states, saved queries, delta/checkpoints
   - Addresses: Core MCP differentiator (stateful workflow substrate)
   - Avoids: Tool proliferation (design minimal but meaningful tool set)
   - Dependencies: Phase 1 (paper model, database)

3. **Phase 3: Enrichment Adapters** -- OpenAlex integration, external ID resolution, graph-based related works
   - Addresses: Richer paper metadata, citation graph, seed expansion via graph
   - Avoids: OpenAlex as blocking dependency (lazy enrichment, graceful degradation)
   - Dependencies: Phase 1 (paper model), Phase 2 (workflow state for priority scheduling)

4. **Phase 4: MCP v1** -- Full MCP surface with tools, resources, prompts. Intent-based tool names.
   - Addresses: Agent-usable discovery workflows, daily-digest and triage prompts
   - Avoids: Context bloat (start with 5-8 tools max, use resources for data retrieval)
   - Dependencies: Phase 2 (workflow state), Phase 3 (enrichment data)

5. **Phase 5: Content Normalization** -- Content variant model, Docling/Marker/GROBID backends, provenance tracking
   - Addresses: Full-text access with source-aware acquisition, rights-gated serving
   - Avoids: Storing/serving copyrighted content (license-check gate in content pipeline)
   - Dependencies: Phase 1 (provenance model), Phase 4 (content MCP tools)

6. **Phase 6: Semantic Search** -- SPECTER2 embeddings, pgvector, hybrid retrieval, reranking experiments
   - Addresses: Semantic discovery, profile-driven recommendations
   - Avoids: Premature embedding commitment (evaluate against lexical baseline first)
   - Dependencies: Phase 1 (lexical baseline for comparison), Phase 3 (enrichments)

**Phase ordering rationale:**
- Phases 1-2 establish the core substrate with no ML or external API dependencies. The system is useful after Phase 2.
- Phase 3 (enrichment) comes before Phase 4 (MCP v1) so the MCP surface has enriched data to expose.
- Phase 5 (content) is independent of Phase 6 (semantic) and can run in parallel.
- Phase 6 (semantic) is last among core phases because it requires a baseline to compare against and is the most expensive to get wrong.

**Research flags for phases:**
- Phase 1: Needs deeper research on arXiv OAI-PMH `arXivRaw` format parsing specifics and the new endpoint behavior
- Phase 3: Needs deeper research on OpenAlex credit-based pricing tiers and batch request optimization
- Phase 5: Needs deeper research on Docling vs Marker quality for scholarly PDFs specifically (math, citations, tables)
- Phase 6: Needs deeper research on SPECTER2 adapter selection (proximity vs adhoc_query) for different query types

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack (language, framework, database) | HIGH | Verified against official docs, PyPI releases, system inventory. Python is clearly correct given the dependency graph. PostgreSQL FTS verified sufficient at this scale. |
| Features (table stakes, differentiators) | HIGH | Grounded in analysis of 10+ competitor products and existing MCP servers. Gap analysis is solid. |
| Architecture (patterns, boundaries) | HIGH | Aligns with project's own design documents and ADRs. Retrieval pipeline pattern is well-established in information retrieval. |
| Pitfalls (arXiv specifics) | HIGH | Verified against official arXiv documentation (OAI-PMH, API ToU, announcement schedule, licensing). These are documented behaviors, not speculation. |
| Embedding models (SPECTER2 selection) | MEDIUM | SPECTER2 is the best documented choice for scientific papers, but the embedding landscape moves fast. The Matryoshka models and newer MoE architectures may surpass it by the time Phase 6 arrives. Re-evaluate at Phase 6. |
| Content parsing (Docling/Marker quality) | MEDIUM | Both are well-documented. Comparative quality for scholarly math/physics PDFs specifically needs Phase 5 experimentation. |

## Gaps to Address

- **arXiv OAI-PMH `arXivRaw` parsing:** The exact XML structure of `arXivRaw` records needs implementation-time investigation. Documentation is limited.
- **OpenAlex credit budgeting:** Need to model actual credit consumption for typical enrichment patterns before committing to a scheduling strategy.
- **SPECTER2 vs newer models:** By the time Phase 6 starts, there may be newer domain-specific embedding models. Re-evaluate before committing.
- **MCP SDK v2 migration path:** If MCP SDK v2 ships during development, the migration path needs assessment. v1 will have 6+ months of support.
- **arXiv HTML coverage:** What fraction of papers in the target categories have arXiv HTML available? This affects the content acquisition order's practical impact.
- **PostgreSQL FTS ranking quality:** ts_rank is not BM25. If ranking quality proves insufficient, the upgrade path to ParadeDB pg_search or tantivy-py needs evaluation.
