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
- [ ] **Phase 5: Content Normalization** - Content variant model, multi-backend parsing, rights-gated content serving
- [ ] **Phase 6: MCP Integration** - Full MCP server with discovery, workflow, and content tools, resources, and prompts

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
**Plans**: TBD

Plans:
- [ ] 04-01: TBD

### Phase 5: Content Normalization
**Goal**: Users can access paper content at multiple fidelity levels (abstract through full-text markdown) with source-aware acquisition, rights-gated serving, and full provenance
**Depends on**: Phase 1
**Requirements**: CONT-01, CONT-02, CONT-03, CONT-04, CONT-05, CONT-06
**Success Criteria** (what must be TRUE):
  1. User can retrieve paper content as abstract (always available) or as richer variants (HTML, source-derived, PDF-derived markdown) when available
  2. Content variants are acquired in source-aware priority order (abstract then arXiv HTML then source then PDF) and each records its extraction method and conversion path
  3. Multiple parsing backends (Docling, Marker, GROBID) work behind a common interface and can be swapped without changing the content API
  4. Content serving refuses to return full-text for papers whose license does not permit it, with a clear explanation of why
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD

### Phase 6: MCP Integration
**Goal**: The full discovery, workflow, and content system is exposed as an MCP server with intent-based tools, canonical resources, and reusable prompts
**Depends on**: Phase 1, Phase 2, Phase 3, Phase 4, Phase 5
**Requirements**: MCP-01, MCP-02, MCP-03, MCP-04, MCP-05, MCP-06, MCP-07
**Success Criteria** (what must be TRUE):
  1. An MCP client (Claude Code) can discover papers via search_papers, browse_recent, find_related_papers, and get_paper tools
  2. An MCP client can manage workflow state via create_collection, add_to_collection, mark_triage_state, create_saved_query, and get_delta_since_checkpoint tools
  3. An MCP client can access paper content variants via get_content_variant tool
  4. MCP resources expose paper, collection, saved query, and result set as canonical objects
  5. MCP prompts for daily-digest, literature-map-from-seeds, and triage-shortlist are available and produce useful agent workflows
**Plans**: TBD

Plans:
- [ ] 06-01: TBD
- [ ] 06-02: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5 -> 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Metadata Substrate | 3/3 | Complete | 2026-03-09 |
| 2. Workflow State | 3/3 | Complete | 2026-03-09 |
| 3. Interest Modeling & Ranking | 0/3 | Not started | - |
| 4. Enrichment Adapters | 0/1 | Not started | - |
| 5. Content Normalization | 0/2 | Not started | - |
| 6. MCP Integration | 0/2 | Not started | - |
