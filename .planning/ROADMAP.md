# Roadmap: arXiv Discovery MCP

> **Status:** `v0.1` (Phases 1-10) is complete and frozen as the shipped milestone roadmap. `v0.2` (Phases 12-17) is the active multi-lens substrate milestone, committed via [ADR-0005](../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md) on 2026-04-25.
> **Current work:** v0.2 multi-lens substrate planning. See [v0.2-MILESTONE.md](./milestones/v0.2-MILESTONE.md), [VISION.md](./VISION.md), [LONG-ARC.md](./LONG-ARC.md).

## Overview

`v0.1` (Phases 1-6) built the core: metadata foundation, workflow state, interest modeling with inspectable ranking, enrichment adapters, MCP server (13 tools, 4 resources, 3 prompts), validation with real workflows, and content normalization. Phases 7-8 closed gaps identified by the v1 milestone audit. Phases 9-10 handled release packaging and real-world agent integration testing.

`v0.2` (Phases 12-17) ships a multi-lens MCP substrate honoring [ADR-0001](../docs/adrs/ADR-0001-exploration-first.md)'s coexistence commitment in implementation, not only in design. At least two lenses (existing semantic + new citation/community) ship; the profile primitive generalizes to a bundle-of-signals shape; lens-disagreement and intersection are first-class MCP operations; the superseded `008` tournament is replaced with a longitudinal pilot harness. Architectural commit: [ADR-0005](../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md). Property-audit-grounded Option B selection: [`audits/2026-04-25-phase-3-property-audit-opus.md`](./audits/2026-04-25-phase-3-property-audit-opus.md).

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Metadata Substrate** - Paper model, arXiv ingestion, lexical search, and recent-paper browsing
- [x] **Phase 2: Workflow State** - Collections, triage states, saved queries, watches, and delta/checkpoint handling
- [x] **Phase 3: Interest Modeling & Ranking** - Interest profiles with multiple signal types and structured ranking explanations
- [x] **Phase 4: Enrichment Adapters** - OpenAlex integration, external ID resolution, and lazy enrichment with provenance
- [x] **Phase 5: MCP Validation & Iteration** - Real workflow validation, doc 06 resolution, prompt design, tool iteration
- [x] **Phase 6: Content Normalization** - Content variant model, multi-backend parsing, rights-gated content serving, MCP content tool
- [x] **Phase 7: MCP Surface Parity** - Wire profile-ranked search, workflow-enriched results, create_profile, and suggest_signals into MCP (GAP CLOSURE) (completed 2026-03-13)
- [x] **Phase 8: Infrastructure Fixes** - Enrichment schema alignment, test fixture scoping, docstring and import fixes (GAP CLOSURE)
- [x] **Phase 9: Release Packaging** - LICENSE, README rewrite, pyproject.toml metadata, CHANGELOG, GitHub repo, CI pipeline, v0.1.0 tag
- [x] **Phase 10: Agent Integration Test** - Real MCP server configuration, agent research session, setup documentation from actual usage (completed 2026-03-14)

### v0.2 Phases (Multi-Lens Substrate, planned 2026-04-25)

- [ ] **Phase 12: Lens Abstraction Primitives** - `Lens` protocol, scorer registry, `ProfileRankingService` as dispatcher, generalized `SearchResult` with backward compat
- [ ] **Phase 13: MCP Surface Lens-Awareness** - `lens=` parameter on the four discovery tools, `RankerSnapshot` lens identity, CLI updates
- [ ] **Phase 14: Citation Graph Data Integration** - OpenAlex coverage spike, citation edge storage retrieval-shaped, backfill from existing 126 papers, ingestion path for new papers
- [ ] **Phase 15: Citation/Community Lens** - Lens implementation, per-lens scorers and explanations, lens-extensibility design walkthrough for hypothetical third lens
- [ ] **Phase 16: Lens-Disagreement and Intersection Operations** - First-class MCP operations: papers in lens A but not lens B, set intersection, per-paper cross-lens explanation
- [ ] **Phase 17: Longitudinal Pilot Harness** - Pilot with Logan replacing the superseded `008` tournament; capture lens usage, selections, dismissals, returns

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
- [x] 01-02-PLAN.md -- Ingestion: OAI-PMH harvester, arXiv API client, XML parsers, metadata mapper
- [x] 01-03-PLAN.md -- Search: fielded search, browse recent, find related, cursor pagination, CLI

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
- [x] 02-01-PLAN.md -- Schema foundation: ORM models, Pydantic schemas, Alembic migration 002, test infrastructure
- [x] 02-02-PLAN.md -- Collection and triage services: CRUD, membership, merge, archive, triage mark/batch/log
- [x] 02-03-PLAN.md -- Saved queries, watches, export/import, stats, paper show, and CLI commands

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
- [x] 03-01-PLAN.md -- Interest profile data model, migration, ProfileService with CRUD and signal management
- [x] 03-02-PLAN.md -- Composable ranking pipeline with 5 signal scorers, ProfileRankingService
- [x] 03-03-PLAN.md -- Suggestion engine, profile CLI, search CLI integration with --profile and --explain

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
- [x] 04-01-PLAN.md -- Data model, Pydantic schemas, OpenAlexAdapter with DOI-based resolution, migration 004, test fixtures
- [x] 04-02-PLAN.md -- EnrichmentService orchestration, CLI subgroup, paper show integration, batch operations

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
- [x] 04.1-02-PLAN.md -- MCP server scaffold with FastMCP lifespan, 4 discovery tools, test infrastructure
- [x] 04.1-03-PLAN.md -- 5 workflow/interest/enrichment tools, 4 resource templates, tool naming tests

### Phase 5: MCP Validation & Iteration (RESEQUENCED — was Phase 6)

**Goal:** MCP v1 is validated with real literature review workflows. Doc 06 open questions are resolved with evidence from agent usage. MCP prompts are designed and tested. Tool granularity is iterated based on real usage patterns.
**Depends on**: Phase 04.1
**Requirements**: MCP-05, MCPV-01, MCPV-02, MCPV-03
**Success Criteria** (what must be TRUE):
  1. At least one real literature review session completed through MCP (search -> triage -> collect -> expand -> enrich)
  2. Doc 06 open questions (tool granularity, resource design, prompt reusability) have evidence-based answers
  3. MCP prompts for daily-digest, literature-map-from-seeds, and triage-shortlist are available and produce useful agent workflows
  4. Tool set has been iterated at least once based on validation feedback
**Plans**: 3 plans

Plans:
- [x] 05-01-PLAN.md -- Import script: arxiv-scan data bootstrap (157 papers, triage states, tension profile)
- [x] 05-02-PLAN.md -- MCP prompts: literature_review_session, daily_digest, triage_shortlist
- [x] 05-03-PLAN.md -- Validation session, doc 06 resolution, evidence-based MCP surface iteration

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
**Plans**: 4 plans

Plans:
- [x] 06-01-PLAN.md -- Data foundation: ContentVariant ORM, Pydantic models, RightsChecker, migration 008, Settings extension
- [x] 06-02-PLAN.md -- Content adapters and service: ContentAdapter protocol, MarkerAdapter, HTML fetcher, ContentService orchestration
- [x] 06-03-PLAN.md -- MCP integration: get_content_variant tool, paper resource extension, content CLI, tool count update
- [x] 06-04-PLAN.md -- Gap closure: add missing beautifulsoup4 dependency, verify full test suite

### Phase 7: MCP Surface Parity (GAP CLOSURE)

**Goal:** MCP tools expose the same capabilities available in the CLI — profile-ranked search, workflow-enriched search results, profile creation, and signal suggestions — so agents using MCP have full parity with CLI users.
**Depends on:** Phase 6
**Gap Closure:** Closes integration gaps and degraded Interest-Driven Discovery flow from v1 audit
**Success Criteria** (what must be TRUE):
  1. An MCP client can search papers with a profile_slug parameter and receive profile-ranked results with RankingExplanation on each result
  2. MCP search_papers and browse_recent return WorkflowSearchResult-enriched results (triage_state, collection_slugs) not bare SearchResult
  3. An MCP client can create an interest profile via create_profile tool
  4. An MCP client can generate and review signal suggestions via suggest_signals tool
  5. AppContext includes ProfileRankingService (or equivalent) and all new tools are tested
**Plans**: 2 plans

Plans:
- [x] 07-01-PLAN.md -- AppContext expansion (ProfileRankingService + SuggestionService), create_profile and suggest_signals tools
- [x] 07-02-PLAN.md -- Discovery tool enhancement: reroute search_papers and browse_recent through ProfileRankingService with profile_slug parameter

### Phase 8: Infrastructure Fixes (GAP CLOSURE)

**Goal:** Fix pre-existing infrastructure issues: enrichment schema mismatch blocking live enrichment, test fixture conflicts, and minor documentation/import issues.
**Depends on:** Phase 6
**Gap Closure:** Closes tech debt items from v1 audit
**Success Criteria** (what must be TRUE):
  1. Enrichment schema (migration) aligns with code expectations — enrich_paper works against real database
  2. Test fixtures use consistent scoping — no UniqueViolationError from concurrent table creation
  3. create_watch docstring references watch://{slug}/deltas resource (not non-existent get_delta tool)
  4. content/__init__.py uses lazy import for html_fetcher (no eager import propagation)
**Plans**: 2 plans

Plans:
- [x] 08-01-PLAN.md -- Test fixture consolidation, create_watch docstring fix, content lazy import fix
- [x] 08-02-PLAN.md -- Live database migration alignment (alembic upgrade 004 -> 008)

## Progress

**Execution Order:**
- v0.1: 1 -> 2 -> 3 -> 4 -> 04.1 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 (complete)
- v0.2: 12 -> 13 -> 16 -> 17 with 14 and 15 in parallel where dependencies permit. Critical path: 12 → 13 → 16 → 17. Phase 14 parallels 12; Phase 15 follows 12 and 14.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Metadata Substrate | 3/3 | Complete | 2026-03-09 |
| 2. Workflow State | 3/3 | Complete | 2026-03-09 |
| 3. Interest Modeling & Ranking | 3/3 | Complete | 2026-03-10 |
| 4. Enrichment Adapters | 2/2 | Complete | 2026-03-10 |
| 04.1. MCP v1 | 3/3 | Complete | 2026-03-12 |
| 5. MCP Validation & Iteration | 3/3 | Complete | 2026-03-12 |
| 6. Content Normalization | 4/4 | Complete | 2026-03-13 |
| 7. MCP Surface Parity | 2/2 | Complete | 2026-03-13 |
| 8. Infrastructure Fixes | 2/2 | Complete | 2026-03-13 |
| 9. Release Packaging | 3/3 | Complete | 2026-03-14 |
| 10. Agent Integration Test | 3/3 | Complete   | 2026-03-14 |
| 12. Lens Abstraction Primitives | 0/3 | Planned | — |
| 13. MCP Surface Lens-Awareness | 0/2 | Planned | — |
| 14. Citation Graph Data Integration | 0/3 | Planned | — |
| 15. Citation/Community Lens | 0/3 | Planned | — |
| 16. Lens-Disagreement and Intersection Ops | 0/2 | Planned | — |
| 17. Longitudinal Pilot Harness | 0/2 | Planned | — |

### Phase 9: Release Packaging

**Goal:** The project is distributable: legally licensed, documented for users (not just designers), hosted on GitHub with CI, and tagged as v0.1.0. A new user can find, install, configure, and run the MCP server from the README alone.
**Depends on:** Phase 8
**Success Criteria** (what must be TRUE):
  1. LICENSE file exists at repo root with a recognized open-source license
  2. README contains: project description, feature overview, installation instructions, quick-start guide, MCP server configuration example, and link to design docs
  3. pyproject.toml has complete metadata: author, license, classifiers, repository URL, keywords
  4. CHANGELOG.md exists with v0.1.0 entry summarizing capabilities
  5. GitHub repository exists and is the configured remote
  6. GitHub Actions CI runs tests + lint on push/PR and passes
  7. Git tag v0.1.0 exists on the release commit
**Plans:** 3 plans

Plans:
- [x] 09-01-PLAN.md -- License, pyproject.toml metadata, CHANGELOG, ruff lint fixes
- [x] 09-02-PLAN.md -- README rewrite for users (install, quick-start, MCP config)
- [x] 09-03-PLAN.md -- GitHub repo creation, CI workflow, push, v0.1.0 tag

### Phase 10: Agent Integration Test

**Goal:** The MCP server is configured as a real MCP server in Claude Code (or equivalent client), and an agent completes a genuine research session without builder intervention. Setup documentation is written from the actual experience of getting it running, not from assumptions.
**Depends on:** Phase 9
**Success Criteria** (what must be TRUE):
  1. MCP server is configured in Claude Code MCP settings (.mcp.json) and connects successfully
  2. An agent completes a full research workflow (search -> triage -> collect -> profile -> enrich) without manual tool-call construction
  3. Friction points and ergonomic issues are documented (tool descriptions, error messages, missing affordances)
  4. Setup/configuration guide exists and was validated by actually following it from scratch
  5. Any critical ergonomic fixes identified are either resolved or tracked as v0.2.0 items
**Plans:** 3/3 plans complete

Plans:
- [ ] 10-01-PLAN.md -- MCP server configuration in Claude Code, database verification, connectivity test
- [ ] 10-02-PLAN.md -- Agent research session (5 E2E flows), session log, friction report
- [ ] 10-03-PLAN.md -- README validation, critical ergonomic fixes, friction report finalization

### Phase 12: Lens Abstraction Primitives

**Goal:** Refactor the existing single-lens ranking pipeline into a multi-lens substrate without behavioral regression. `Lens` protocol exists with a scorer registry; `ProfileRankingService` becomes a dispatcher; `SearchResult` carries per-lens score components alongside legacy composite for backward compatibility.
**Depends on:** Nothing (refactor of existing code)
**Requirements:** LENS-01, LENS-02 (semantic side), LENS-04, LENS-05
**Success Criteria** (what must be TRUE):
  1. A `Lens` protocol exists in `interest/` (or equivalent location) and the existing semantic-lens scorers are registered as the first lens implementation
  2. `ProfileRankingService` dispatches to a registered lens by name; existing single-pipeline behavior is preserved by default and validated against v0.1 regression tests
  3. `RankingPipeline.score_paper`'s hard-sequenced calls are replaced by a registry-driven dispatcher; new scorers register without modifying `score_paper`
  4. `SearchResult` (and `ProfileSearchResult`) carry `lens_scores: dict[str, float]` and `per_lens_explanations: dict[str, RankingExplanation]` as additive optional fields; legacy `score` and `ranking_explanation` continue to mean composite over the active lens
  5. All v0.1 tests pass without modification (backward-compat verification)
**Plans:** 3 plans

Plans:
- [ ] 12-01-PLAN.md -- `Lens` protocol design, scorer registry, semantic-lens registration, regression tests preserving v0.1 behavior
- [ ] 12-02-PLAN.md -- `ProfileRankingService` refactor to dispatcher pattern; `_load_profile_context` generalized; default lens preserved
- [ ] 12-03-PLAN.md -- `SearchResult` generalization with backward-compat default; `RankerSnapshot` lens identity; per-lens explanation surface

### Phase 13: MCP Surface Lens-Awareness

**Goal:** The four discovery MCP tools accept a `lens=` parameter; default behavior is unchanged for existing consumers; new consumers can request specific lenses or combinations. CLI mirrors the surface.
**Depends on:** Phase 12
**Requirements:** MCP-08, MCP-09
**Success Criteria** (what must be TRUE):
  1. `search_papers`, `browse_recent`, `find_related_papers`, `get_paper` accept an optional `lens=` parameter (single lens name or list); when omitted, behavior matches v0.1
  2. `find_related_papers` (which lacked profile awareness in v0.1) accepts both `lens=` and `profile_slug=` parameters
  3. `RankerSnapshot` (and equivalent provenance objects) records which lens(es) produced the result set and which scorers ran
  4. CLI flags mirror MCP parameters; CLI tests cover the new flag combinations
  5. MCP tool docstrings document the new parameter; tool naming tests confirm semantics
  6. Multi-value `lens=` semantics implemented per ADR-0005's per-lens-dict default; explicit `mode=` parameters route to Phase 16 ops; fusion is opt-in via `mode='fusion'`
**Plans:** 2 plans

Plans:
- [ ] 13-01-PLAN.md -- `lens=` parameter on the four discovery tools; dispatcher wiring; backward-compat tests; `RankerSnapshot` lens identity
- [ ] 13-02-PLAN.md -- CLI flag updates; CLI integration tests; tool naming and docstring updates

### Phase 14: Citation Graph Data Integration

**Goal:** Citation edge data is stored in retrieval-shaped form (queryable table or denormalized projection from `PaperEnrichment.related_works`); existing 126 papers are backfilled; new papers acquire citation edges via the existing OpenAlex enrichment path. Provenance fields per ADR-0003 record source, retrieval timestamp, and freshness window.
**Depends on:** Nothing (parallelizable with Phase 12)
**Requirements:** CITE-01, CITE-04
**Success Criteria** (what must be TRUE):
  1. OpenAlex coverage spike completes: edge density per paper, freshness profile, missingness pattern characterized for the 126-paper corpus; results recorded in a spike artifact
  2. Citation edge schema designed: edges table or `PaperEnrichment` projection (decision recorded with rationale); migration written and applied
  3. Provenance fields per edge: source API (`openalex` initially), retrieval timestamp, freshness window; schema review confirms ADR-0003 compliance
  4. Backfill of existing 126 papers complete; edge counts and sample queries verify integration
  5. Ingestion path: new papers acquire citation edges via `EnrichmentService` (or equivalent) without bulk re-fetch
**Plans:** 3 plans

Plans:
- [ ] 14-01-PLAN.md -- OpenAlex coverage spike (1-2 days); citation source decision artifact (OpenAlex first, Semantic Scholar deferred)
- [ ] 14-02-PLAN.md -- Citation edge schema design and migration; provenance fields per ADR-0003
- [ ] 14-03-PLAN.md -- Backfill from existing `PaperEnrichment.related_works`; new-paper ingestion path; integration tests

### Phase 15: Citation/Community Lens

**Goal:** A working citation/community lens implementation: traversal of citation edges, co-citation neighborhood computation, freshness handling, per-lens scorers, per-lens explanations naming cited papers and relationship types. Includes a design walkthrough demonstrating that adding a hypothetical third lens (e.g., author/affiliation) requires no consumer-side changes.
**Depends on:** Phase 12, Phase 14
**Requirements:** LENS-02 (citation/community side), LENS-03, CITE-02, CITE-03
**Success Criteria** (what must be TRUE):
  1. `CitationCommunityLens` implementation registered in the lens registry from Phase 12
  2. Lens performs at minimum: direct-citation retrieval (papers cited by seed), citation depth-2 traversal, co-citation neighborhood (papers cited together with seed)
  3. Per-lens scorers compute relevance scores from citation graph features (e.g., shortest path, co-citation count, citation recency)
  4. Per-lens explanations name cited papers, relationship type (direct citation, co-citation, citation depth), and the evidence basis (which edges contributed)
  5. Freshness handling: lens reports edge retrieval timestamps; stale-edge policy documented
  6. Design walkthrough document: walks through how a hypothetical author/affiliation lens would register and function, surfacing any abstraction gaps in the lens interface; produced before Phase 16 begins
**Plans:** 3 plans

Plans:
- [ ] 15-01-PLAN.md -- `CitationCommunityLens` implementation: edge traversal, co-citation neighborhoods, freshness handling
- [ ] 15-02-PLAN.md -- Per-lens scorers and explanations; integration with `RankingPipeline` registry; tests
- [ ] 15-03-PLAN.md -- Lens-extensibility design walkthrough for hypothetical third lens; abstraction-gap audit

### Phase 16: Lens-Disagreement and Intersection Operations

**Goal:** First-class MCP operations exposing lens-disagreement, set intersection, and per-paper cross-lens explanation across the two shipped lenses. These operations are not fusion; they preserve per-lens results and expose the structure of agreement and disagreement.
**Depends on:** Phase 13, Phase 15
**Requirements:** LDIS-01, LDIS-02, LDIS-03
**Success Criteria** (what must be TRUE):
  1. MCP exposes a way to request "papers in lens A but not lens B" — either a dedicated tool, a `mode=disagreement` parameter on existing tools, or a composable filter; design choice recorded with rationale
  2. MCP exposes set intersection across two or more lenses: papers surfaced by all selected lenses
  3. Per-paper cross-lens explanation: when a paper is returned from a multi-lens query, the response includes which lenses surfaced it and per-lens score components
  4. Tests cover: pure agreement, pure disagreement, partial overlap, single-lens edge cases
  5. CLI flags mirror MCP operations
**Plans:** 2 plans

Plans:
- [ ] 16-01-PLAN.md -- Operation design (separate tools vs mode parameter vs composable filter); MCP surface; CLI flags
- [ ] 16-02-PLAN.md -- Implementation, cross-lens explanation surface, tests, agent-flow validation

### Phase 17: Longitudinal Pilot Harness

**Goal:** Replace the superseded `008` tournament with a longitudinal pilot harness running with one user (Logan). Capture lens usage at session level, triage events with timestamps, lens-of-record per event. Pilot runs continuously for at least four weeks; capture is durable and exportable.
**Depends on:** Phase 13, Phase 15, Phase 16
**Requirements:** LPILOT-01, LPILOT-02, LPILOT-03
**Success Criteria** (what must be TRUE):
  1. Capture schema designed: session-level lens usage, query log with lens(es) selected, triage events (selection, dismissal, return-to-paper), per-event lens-of-record, durable storage
  2. Capture is opt-in / explicit; no silent profile mutation (LONG-ARC anti-pattern: silent defaults)
  3. Pilot kickoff: weekly review cadence with Logan; first capture window starts and runs for at least four weeks
  4. Mid-pilot review at week 2: friction surfaced, lens-usage patterns characterized, capture-schema gaps recorded
  5. End-of-window review: pilot artifact produced summarizing lens usage, agreement/disagreement patterns, suspected v0.3 priorities
  6. `008/SUPERSESSION.md` is finalized as part of this phase's documentation; the longitudinal-pilot harness is the canonical successor
**Plans:** 2 plans

Plans:
- [ ] 17-01-PLAN.md -- Harness design, capture schema, durable storage, opt-in mechanism, MCP integration
- [ ] 17-02-PLAN.md -- Pilot kickoff, weekly review cadence, mid-pilot review, end-of-window review, `008` supersession finalization
