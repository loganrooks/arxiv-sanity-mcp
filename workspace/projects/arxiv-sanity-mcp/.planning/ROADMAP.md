# Roadmap: arXiv Discovery MCP

## Overview

This roadmap delivers an MCP-native research discovery substrate in six phases. The first phase builds the metadata foundation (paper model, ingestion, lexical search). The next two phases add workflow state and interest modeling -- at which point the system has the core differentiators (explicit taste modeling, inspectable ranking, stateful workflows). Enrichment and content normalization extend the data available for discovery. The final phase wires everything into the MCP protocol surface with tools, resources, and prompts. Semantic search is deferred to v2.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Metadata Substrate** - Paper model, arXiv ingestion, lexical search, and recent-paper browsing
- [ ] **Phase 2: Workflow State** - Collections, triage states, saved queries, watches, and delta/checkpoint handling
- [ ] **Phase 3: Interest Modeling & Ranking** - Interest profiles with multiple signal types and structured ranking explanations
- [ ] **Phase 4: Enrichment Adapters** - OpenAlex integration, external ID resolution, and lazy enrichment with provenance
- [ ] **Phase 5: MCP Validation & Iteration** - Real workflow validation, doc 06 resolution, prompt design, tool iteration
- [ ] **Phase 6: Content Normalization** - Content variant model, multi-backend parsing, rights-gated content serving, MCP content tool

## Phase Details

### Phase 1: Metadata Substrate
**Goal**: Researchers can ingest arXiv papers, search them by metadata fields, and browse recent announcements with correct time semantics
**Depends on**: Nothing (foundation)
**Requirements**: INGS-01, INGS-02, INGS-03, INGS-04, INGS-05, PAPR-01, PAPR-02, PAPR-03, PAPR-04, SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05, SRCH-06
**Success Criteria** (what must be TRUE):
  1. User can trigger OAI-PMH bulk harvest and see papers appear in the database with all four time semantics (submission, update, announcement, OAI datestamp) correctly stored
  2. User can search papers by title, author, abstract, category, and date range with AND/OR composition and get paginated results
  3. User can browse recently announced papers filtered by arXiv category and switch between time bases (submission vs announcement vs update)
  4. User can find related papers from a seed paper via lexical similarity
  5. Every stored paper has provenance metadata (source, fetch timestamp) and per-paper license/rights data
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md -- Foundation: project scaffolding, DB schema, paper model, test infrastructure
- [ ] 01-02-PLAN.md -- Ingestion: OAI-PMH harvester, arXiv API client, XML parsers, metadata mapper
- [ ] 01-03-PLAN.md -- Search: fielded search, browse recent, find related, cursor pagination, CLI

### Phase 2: Workflow State
**Goal**: Users can organize their research workflow with collections, triage states, saved queries, and delta tracking to answer "what's new since I last checked"
**Depends on**: Phase 1
**Requirements**: WKFL-01, WKFL-02, WKFL-03, WKFL-04, WKFL-05, WKFL-06, WKFL-07, WKFL-08
**Success Criteria** (what must be TRUE):
  1. User can create named collections and add/remove papers from them
  2. User can mark papers with triage states (unseen, shortlisted, dismissed, read, cite-later) and batch-triage multiple papers at once
  3. User can save a query with parameters, ranking mode, and filters, then re-run it on demand
  4. User can create a watch (saved query + cadence + checkpoint) and get delta results showing only papers new since the last checkpoint
**Plans**: 3 plans

Plans:
- [ ] 02-01-PLAN.md -- Schema foundation: ORM models, Pydantic schemas, Alembic migration 002, test infrastructure
- [ ] 02-02-PLAN.md -- Collection and triage services: CRUD, membership, merge, archive, triage mark/batch/log
- [ ] 02-03-PLAN.md -- Saved queries, watches, export/import, stats, paper show, and CLI commands

### Phase 3: Interest Modeling & Ranking
**Goal**: Users can build explicit interest profiles from multiple signal types and get structured explanations for why each paper surfaced in results
**Depends on**: Phase 2
**Requirements**: INTR-01, INTR-02, INTR-03, INTR-04, INTR-05, INTR-06, RANK-01, RANK-02, RANK-03
**Success Criteria** (what must be TRUE):
  1. User can create an interest profile composed of seed paper sets, saved queries, followed authors, and negative examples
  2. User can inspect all signals in a profile and see which were user-added vs system-suggested
  3. Every result in a result set includes a structured ranking explanation exposing signal types (query match, seed relation, category overlap, interest profile match, recency)
  4. User can inspect the full ranker inputs for any result set
**Plans**: 3 plans

Plans:
- [ ] 03-01-PLAN.md -- Interest profile data model, migration, ProfileService with CRUD and signal management
- [ ] 03-02-PLAN.md -- Composable ranking pipeline with 5 signal scorers, ProfileRankingService
- [ ] 03-03-PLAN.md -- Suggestion engine, profile CLI, search CLI integration with --profile and --explain

### Phase 4: Enrichment Adapters
**Goal**: Papers are lazily enriched with OpenAlex data (topics, citations, related works) on demand, with external ID resolution and full provenance tracking
**Depends on**: Phase 1, Phase 2
**Requirements**: ENRC-01, ENRC-02, ENRC-03, ENRC-04
**Success Criteria** (what must be TRUE):
  1. User can trigger OpenAlex enrichment for a paper and see topics, citation counts, related works, and FWCI appear on the paper record
  2. Enrichment happens on demand (not bulk) and the system tracks which papers have been enriched and when
  3. System resolves arXiv ID to DOI to OpenAlex ID bidirectionally
  4. All enrichment data records provenance (source API, timestamp, API version)
**Plans**: 2 plans

Plans:
- [ ] 04-01-PLAN.md -- Data model, Pydantic schemas, OpenAlexAdapter with DOI-based resolution, migration 004, test fixtures
- [ ] 04-02-PLAN.md -- EnrichmentService orchestration, CLI subgroup, paper show integration, batch operations

### Phase 04.1: MCP v1 — expose existing services as MCP tools and resources (INSERTED)

**Goal:** An MCP server exposes existing search, workflow, interest, and enrichment services as tools and resources. Pre-MCP quality fixes (ranking triple-counting, "seen" triage state) are applied first. An MCP client can perform a complete literature review workflow: search, triage, collect, profile, enrich.
**Depends on:** Phase 4
**Requirements**: PREMCP-01, PREMCP-02, PREMCP-03, MCP-01, MCP-02, MCP-04, MCP-06, MCP-07
**Success Criteria** (what must be TRUE):
  1. Category overlap is scored exactly once in the ranking pipeline (effective weight = DEFAULT_WEIGHTS[CATEGORY_OVERLAP], not 2.5x)
  2. "Seen" triage state exists and is distinct from absence (never encountered) and from shortlisted/dismissed (decision made)
  3. An MCP client can discover papers via search_papers, browse_recent, find_related_papers, and get_paper tools
  4. An MCP client can manage workflow state via triage_paper, add_to_collection, and create_watch tools, plus add_signal for interest profiles and enrich_paper for enrichment
  5. MCP resources expose paper, collection, profile, and watch deltas as canonical objects
  6. Tool names describe user intent, not implementation
**Plans**: 3 plans

Plans:
- [x] 04.1-01-PLAN.md -- Pre-MCP quality fixes: ranking triple-counting, "seen" triage state, pagination documentation
- [ ] 04.1-02-PLAN.md -- MCP server scaffold with FastMCP lifespan, 4 discovery tools, test infrastructure
- [ ] 04.1-03-PLAN.md -- 5 workflow/interest/enrichment tools, 4 resource templates, tool naming tests

### Phase 5: MCP Validation & Iteration (RESEQUENCED — was Phase 6)

**Goal:** MCP v1 is validated with real literature review workflows. Doc 06 open questions are resolved with evidence from agent usage. MCP prompts are designed and tested. Tool granularity is iterated based on real usage patterns.
**Depends on**: Phase 04.1
**Requirements**: MCP-05, MCPV-01, MCPV-02, MCPV-03
**Success Criteria** (what must be TRUE):
  1. At least one real literature review session completed through MCP (search → triage → collect → expand → enrich)
  2. Doc 06 open questions (tool granularity, resource design, prompt reusability) have evidence-based answers
  3. MCP prompts for daily-digest, literature-map-from-seeds, and triage-shortlist are available and produce useful agent workflows
  4. Tool set has been iterated at least once based on validation feedback
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD

**Rationale for resequencing:** Content normalization blocks MCP validation. For literature review, metadata + abstracts + triage + ranking are the high-value loops. Full-text parsing is secondary. Validate the MCP surface with real workflows before adding content complexity. See `.planning/ECOSYSTEM-COMMENTARY.md` §3.

### Phase 6: Content Normalization (RESEQUENCED — was Phase 5)

**Goal**: Users can access paper content at multiple fidelity levels (abstract through full-text markdown) with source-aware acquisition, rights-gated serving, and full provenance. Content tools exposed via MCP.
**Depends on**: Phase 04.1
**Requirements**: CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06, MCP-03
**Success Criteria** (what must be TRUE):
  1. User can retrieve paper content as abstract (always available) or as richer variants (HTML, source-derived, PDF-derived markdown) when available
  2. Content variants are acquired in source-aware priority order (abstract then arXiv HTML then source then PDF) and each records its extraction method and conversion path
  3. Multiple parsing backends (Docling, Marker, GROBID) work behind a common interface and can be swapped without changing the content API
  4. Content serving refuses to return full-text for papers whose license does not permit it, with a clear explanation of why
  5. An MCP client can access paper content variants via get_content_variant tool
**Plans**: TBD

Plans:
- [ ] 06-01: TBD
- [ ] 06-02: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 04.1 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Metadata Substrate | 3/3 | Complete | 2026-03-09 |
| 2. Workflow State | 3/3 | Complete | 2026-03-09 |
| 3. Interest Modeling & Ranking | 3/3 | Complete | 2026-03-10 |
| 4. Enrichment Adapters | 2/2 | Complete | 2026-03-10 |
| 04.1. MCP v1 | 1/3 | In progress | - |
| 5. MCP Validation & Iteration | 0/? | Not started | - |
| 6. Content Normalization | 0/? | Not started | - |
