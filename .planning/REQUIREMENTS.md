# Requirements: arXiv Discovery MCP

**Defined:** 2026-03-08
**Core Value:** Researchers and agents can discover, monitor, and triage arXiv papers through explicit, steerable interest modeling with inspectable results.

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Ingestion

- [x] **INGS-01**: System ingests arXiv metadata via OAI-PMH bulk harvesting with resumption token handling
- [x] **INGS-02**: System ingests arXiv metadata via API for incremental/targeted queries
- [x] **INGS-03**: System tracks four distinct time semantics per paper: submission date, update date, announcement date, OAI-PMH datestamp
- [x] **INGS-04**: System stores per-paper license/rights metadata from OAI-PMH and RSS feeds
- [x] **INGS-05**: System supports incremental harvesting with datestamp-based checkpoints

### Paper Model

- [x] **PAPR-01**: Canonical paper model with arXiv ID as primary identifier
- [x] **PAPR-02**: Paper records include title, authors, abstract, categories, version history
- [x] **PAPR-03**: Paper records support external identifiers (DOI, OpenAlex ID, Semantic Scholar ID)
- [x] **PAPR-04**: Paper records track provenance: data source, fetch timestamp, enrichment history

### Search & Discovery

- [x] **SRCH-01**: User can search papers by title, author, abstract text, category, and date range
- [x] **SRCH-02**: User can compose queries with AND/OR operators
- [x] **SRCH-03**: User can browse recently announced papers filtered by arXiv category
- [x] **SRCH-04**: User can specify time basis (submission, update, announcement) when browsing recent papers
- [x] **SRCH-05**: User can find related papers from one or more seed papers via lexical similarity
- [x] **SRCH-06**: Results include cursor-based pagination with predictable result sizes

### Workflow State

- [x] **WKFL-01**: User can create, list, and delete named paper collections
- [x] **WKFL-02**: User can add papers to and remove papers from collections
- [x] **WKFL-03**: User can mark paper triage state (unseen, shortlisted, dismissed, read, cite-later)
- [x] **WKFL-04**: User can create saved queries with parameters, ranking mode, and filters
- [x] **WKFL-05**: User can re-run saved queries on demand
- [x] **WKFL-06**: User can create watches (saved query + cadence + checkpoint)
- [x] **WKFL-07**: User can get delta results since last checkpoint ("what's new since I last checked")
- [x] **WKFL-08**: User can batch-triage multiple papers in a single operation

### Interest Modeling

- [x] **INTR-01**: User can create and manage interest profiles composed of multiple signal types
- [x] **INTR-02**: Interest profiles support seed paper sets as signals
- [x] **INTR-03**: Interest profiles support saved queries as signals
- [x] **INTR-04**: Interest profiles support followed authors as signals
- [x] **INTR-05**: Interest profiles support negative examples (papers/topics to deprioritize)
- [ ] **INTR-06**: User can inspect all signals in an interest profile and their provenance (user-added vs system-suggested)

### Ranking & Explanation

- [ ] **RANK-01**: Results include structured ranking explanations (why each paper surfaced)
- [ ] **RANK-02**: Explanations expose signal types: query match, seed relation, category overlap, interest profile match, recency
- [ ] **RANK-03**: User can inspect ranker inputs for any result set

### Enrichment

- [ ] **ENRC-01**: System enriches papers lazily via OpenAlex (topics, citations, related works, FWCI)
- [ ] **ENRC-02**: OpenAlex enrichment is triggered on demand, not bulk (cost-aware)
- [ ] **ENRC-03**: System resolves external IDs: arXiv ID <-> DOI <-> OpenAlex ID
- [ ] **ENRC-04**: Enrichment data records provenance (source, timestamp, API version)

### Content

- [ ] **CONT-01**: System provides abstract as default content variant (no rights issues)
- [ ] **CONT-02**: System models content variants explicitly: abstract, HTML, source-derived, PDF-derived markdown
- [ ] **CONT-03**: Content variants record provenance: source, extraction method, conversion path, license basis
- [ ] **CONT-04**: Content variant acquisition follows source-aware priority: abstract -> arXiv HTML -> source -> PDF
- [ ] **CONT-05**: System supports multiple parsing backends behind a common interface (Docling, Marker, GROBID)
- [ ] **CONT-06**: Content serving respects per-paper license restrictions (gated by rights metadata)

### MCP Interface

- [ ] **MCP-01**: MCP server exposes discovery tools: search_papers, browse_recent, find_related_papers, get_paper
- [ ] **MCP-02**: MCP server exposes workflow tools: create_collection, add_to_collection, mark_triage_state, create_saved_query, get_delta_since_checkpoint
- [ ] **MCP-03**: MCP server exposes content tools: get_content_variant
- [ ] **MCP-04**: MCP server exposes canonical resources: paper, collection, saved query, result set
- [ ] **MCP-05**: MCP server exposes reusable prompts: daily-digest, literature-map-from-seeds, triage-shortlist
- [ ] **MCP-06**: Tool names describe user intent, not implementation (find_related_papers, not search_embeddings)
- [ ] **MCP-07**: MCP tool set stays at 5-10 tools maximum to limit context token cost

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Semantic Search

- **SEMA-01**: System computes SPECTER2 embeddings selectively for user-touched/saved papers
- **SEMA-02**: Semantic search via pgvector for embedded paper cohorts
- **SEMA-03**: Hybrid retrieval: lexical candidates + semantic reranking
- **SEMA-04**: Profile-driven recommendation using embedded interest profiles

### Advanced Enrichment

- **ADVN-01**: Semantic Scholar adapter for recommendations and SPECTER2 embeddings
- **ADVN-02**: Crossref/OpenCitations adapter for broader citation graph
- **ADVN-03**: Citation-context analysis (supporting/contrasting/mentioning)
- **ADVN-04**: Popularity/trending signals from external sources (citation velocity, GitHub stars)

### Advanced Workflows

- **ADVW-01**: Active learning suggestions with user confirmation ("noticed you saved 5 papers on X")
- **ADVW-02**: Project workspaces grouping collections, profiles, and queries
- **ADVW-03**: Email/notification digests for watches

## Out of Scope

| Feature | Reason |
|---------|--------|
| General-purpose paper chatbot | Discovery is the product, not conversation. Let downstream LLMs chat using MCP-provided context. |
| Full corpus embedding | Prohibitive compute on target hardware. Selective embedding only. |
| Web or mobile UI | MCP surface is the interface. Web UI is a separate future client project. |
| Visual graph rendering | Connected Papers/Litmaps own this. Graph data exposed via API; rendering is client concern. |
| Real-time collaboration | Different product category, enormous complexity. Single-user/agent first. |
| Benchmark/leaderboard features | Papers With Code (defunct) owned this. Not this product's identity. |
| Opaque recommendations | Violates inspectability principle. Every result must be explainable. |
| Automatic profile adjustment | Implicit learning without user confirmation creates filter bubbles. Suggestions require confirmation. |
| All-literature warehouse | arXiv first. Broader corpora only after arXiv is well-served. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INGS-01 | Phase 1 | Complete |
| INGS-02 | Phase 1 | Complete |
| INGS-03 | Phase 1 | Complete |
| INGS-04 | Phase 1 | Complete |
| INGS-05 | Phase 1 | Complete |
| PAPR-01 | Phase 1 | Complete |
| PAPR-02 | Phase 1 | Complete |
| PAPR-03 | Phase 1 | Complete |
| PAPR-04 | Phase 1 | Complete |
| SRCH-01 | Phase 1 | Complete |
| SRCH-02 | Phase 1 | Complete |
| SRCH-03 | Phase 1 | Complete |
| SRCH-04 | Phase 1 | Complete |
| SRCH-05 | Phase 1 | Complete |
| SRCH-06 | Phase 1 | Complete |
| WKFL-01 | Phase 2 | Complete |
| WKFL-02 | Phase 2 | Complete |
| WKFL-03 | Phase 2 | Complete |
| WKFL-04 | Phase 2 | Complete |
| WKFL-05 | Phase 2 | Complete |
| WKFL-06 | Phase 2 | Complete |
| WKFL-07 | Phase 2 | Complete |
| WKFL-08 | Phase 2 | Complete |
| INTR-01 | Phase 3 | Complete |
| INTR-02 | Phase 3 | Complete |
| INTR-03 | Phase 3 | Complete |
| INTR-04 | Phase 3 | Complete |
| INTR-05 | Phase 3 | Complete |
| INTR-06 | Phase 3 | Pending |
| RANK-01 | Phase 3 | Pending |
| RANK-02 | Phase 3 | Pending |
| RANK-03 | Phase 3 | Pending |
| ENRC-01 | Phase 4 | Pending |
| ENRC-02 | Phase 4 | Pending |
| ENRC-03 | Phase 4 | Pending |
| ENRC-04 | Phase 4 | Pending |
| CONT-01 | Phase 5 | Pending |
| CONT-02 | Phase 5 | Pending |
| CONT-03 | Phase 5 | Pending |
| CONT-04 | Phase 5 | Pending |
| CONT-05 | Phase 5 | Pending |
| CONT-06 | Phase 5 | Pending |
| MCP-01 | Phase 6 | Pending |
| MCP-02 | Phase 6 | Pending |
| MCP-03 | Phase 6 | Pending |
| MCP-04 | Phase 6 | Pending |
| MCP-05 | Phase 6 | Pending |
| MCP-06 | Phase 6 | Pending |
| MCP-07 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 47 total
- Mapped to phases: 47
- Unmapped: 0

---
*Requirements defined: 2026-03-08*
*Last updated: 2026-03-08 after roadmap creation*
