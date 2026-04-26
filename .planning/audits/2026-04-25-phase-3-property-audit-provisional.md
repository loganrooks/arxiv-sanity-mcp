---
type: property-audit
status: superseded
date: 2026-04-25
scope: Phase 3 (interest modeling) lens-extensibility audit
gates: v0.2 multi-lens roadmap commit (Option A vs B vs C)
superseded_by: 2026-04-25-phase-3-property-audit-opus.md
provenance:
  reviewer: Explore agent (built-in, model unverified at dispatch time)
  validated: false
  caveat: |
    This audit was dispatched without an explicit model override. The Explore
    agent default model is unverified (likely Haiku or Sonnet, not Opus).
    A parallel Opus 4.7 audit (2026-04-25-phase-3-property-audit-opus.md)
    found Property 1's "coupled" verdict factually wrong: this audit cited
    alembic migration 003's CHECK constraint as current state, missing that
    migration 005 (2026-03-11) explicitly drops it. The factual error was
    confirmed by direct read of migration 005. Property 2 verdict ("partly")
    also softer than Opus's "coupled" — register, not substance.
    Do not act on this audit. Use the Opus rerun.
---

# Phase 3 Property Audit — 2026-04-25 (SUPERSEDED)

> **Status note (2026-04-25):** SUPERSEDED by
> [2026-04-25-phase-3-property-audit-opus.md](./2026-04-25-phase-3-property-audit-opus.md).
> Property 1's "coupled" verdict is factually wrong (missed migration 005
> dropping the CHECK constraint cited as load-bearing). Preserved as evidence
> of a methodology failure (delegating gating audit to default Explore agent
> without model verification), not as live evidence about the codebase.

## Verdict summary

| Property | Verdict |
|---|---|
| 1. Profile primitive lens-extensible | **coupled** |
| 2. MCP tool signatures lens-aware | **partly** |
| 3. Storage per-lens abstracted | **coupled** |

## Property 1 — Profile primitive

**Verdict: COUPLED**

The `InterestSignal` primitive is hard-coupled to four signal types via a database CHECK constraint and application validation, making schema-migration-free extensibility impossible. The constraint is declared in two places: `alembic/versions/003_interest_tables.py:53` hardcodes `'seed_paper', 'saved_query', 'followed_author', 'negative_example'` in the SQL CHECK, and `src/arxiv_mcp/interest/signals.py:11` replicates it as `VALID_SIGNAL_TYPES`. Adding a citation-graph or community-derived signal would require an alembic migration to drop the CHECK and re-add it with the new type — a rigid migration, not extensionless. The `signal_value` column is typed loosely enough (`String(256)` at `db/models.py:384`) to hold non-paper-id values (tags, prose, graph node IDs), but the type whitelist at the DB level blocks new signal categories entirely.

- Existing shape: four signal types baked into db/models.py:366-412 ORM and alembic migration 003:53.
- What's missing: open signal_type enum (e.g., no CHECK, or CHECK on a table-driven registry).
- Coupling point: alembic migration 003, signals.py validation, all callers assume exactly these four types.

## Property 2 — MCP tool signatures

**Verdict: PARTLY**

MCP tools accept a `profile_slug` parameter, which is already a lens selector, but there is no explicit `strategy=` or `lens=` parameter and no multi-lens awareness at the tool surface. `search_papers` (`mcp/tools/discovery.py:23-72`) and `browse_recent` (`mcp/tools/discovery.py:75-113`) both accept `profile_slug` as optional and pass it to `app.profile_ranking.search_papers()` and `.browse_recent()` respectively. The lens choice is implicit: pick a profile (one per signal bundle), not a separate strategy parameter. Adding a second lens tomorrow (e.g., `lens="citation_community"` alongside `profile_slug="my-interests"`) would require: at the tool surface, adding a `lens` parameter (trivial); at the service layer, refactoring `ProfileRankingService._load_profile_context()` to accept and dispatch based on lens name (moderate — currently hardcoded to load seed_papers, followed_authors, negative_papers). The wiring is not hostile to lens parameters, but the service is shaped around one profile+one ranking strategy, not multiple strategies per profile.

- Existing shape: profile_slug steering at tools (discovery.py:34, 82), passed through to ProfileRankingService (search_augment.py:99).
- What's missing: explicit lens/strategy parameter; ProfileRankingService._load_profile_context (search_augment.py:236) hardcodes which signals to load and how to score them.
- Coupling point: RankingPipeline.score_paper (ranking.py:415) always applies the five signal types in DEFAULT_WEIGHTS order; new lenses require new pipeline subclasses or a lookup table.

## Property 3 — Storage per-lens abstracted

**Verdict: COUPLED**

Storage is committed to PostgreSQL full-text search (TSVECTOR, ts_rank_cd, GIN indexes) with no abstraction for alternative similarity types. The Paper table (`db/models.py:54-122`) has indexes on `search_vector` (TSVECTOR GIN), dates, and `category_list` (ARRAY GIN); no pgvector column, no embedding table, no graph edge storage. All search queries (`db/queries.py:32-127`) use `websearch_to_tsquery` and `ts_rank_cd` directly — there is no query builder or strategy pattern to swap in a vector-db lookup or citation-graph traversal. PaperEnrichment (`db/models.py:131-178`) stores `cited_by_count`, `related_works` (JSONB list), and `topics` (JSONB dict) from OpenAlex, but these are write-once metadata columns, not shaped for ranking (no denormalization into a queryable citations table, no topic-similarity index). A citation-graph lens would require: new tables for citation edges, query builder logic to traverse them, and index strategy — none of which can be added in an alembic migration without structural changes to the service layer (SearchService, ProfileRankingService both assume lexical-PG queries).

- Existing shape: tsvector search (db/models.py:111), postgres GIN indexes (db/models.py:114, 120), lexical queries (db/queries.py:70-73, 82-88), tsvector/ts_rank_cd hardcoded (db/queries.py:71, 159).
- What's missing: pgvector or graph edge tables; query abstraction (strategy pattern); ProfileRankingService decoupled from lexical scoring.
- Coupling point: db/queries.py build_search_query, build_browse_query, SearchService.search_papers, ProfileRankingService._ranked_search all assume single retrieval model.

## Implications for Option A/B/C

The code **favors Option B** (refactor + ship 2 lenses, ~2 months) as the most realistic path.

**Option A (full substrate, ~3-4 months)** is theoretically sound but requires dismantling coupling at all three levels: (1) remove CHECK constraint, implement signal type registry; (2) add lens parameter to tools and service layer, refactor RankingPipeline to dispatch by lens; (3) abstract queries with a strategy pattern, add pgvector/citation-edge tables. This is feasible but expensive.

**Option B (refactor + 2 lenses, ~2 months)** is practical: (1) remove/relax signal_type CHECK to allow new types via migration (doable in one migration, not schema-free but low risk); (2) add `lens` parameter to tools and ProfileRankingService, implement two RankingPipeline subclasses (semantic = current; citation_community = new loader for cited_by counts + related_works traversal); (3) keep storage single (PostgreSQL) but add a citations denormalization pipeline to PaperEnrichment and query it alongside tsvector. ProfileRankingService becomes a lens dispatcher, not a rewrite.

**Option C (refactor for extensibility, ~1 month)** ships only the refactor without the second lens (semantic lens only), validates the lens abstraction in v0.3. This is the safest path: unbind the signal type constraint, add lens parameter plumbing, leave citation/community signals as future work. Risk: shipping a refactor with only one lens looks incomplete and may not convince stakeholders that multi-lens is feasible.

ADR-0001 commits to "multiple retrieval/ranking strategies must coexist." Property 2 is already partly shaped for it (tools accept profile_slug as a lens proxy). Properties 1 and 3 are blockers; Option B addresses both without full substrate investment.

## What I am not telling you

- **Ingestion-side coupling**: This audit examines retrieval/ranking, not enrichment pipelines. The `arxiv_mcp.enrichment` module's coupling to OpenAlex (openalex.py) is out of scope.
- **MCP resources and prompts**: The discovery tools surface is audited, but MCP resources (e.g., paper-detail resources) and prompts (triage_shortlist.py, literature_review.py) are not evaluated for lens-awareness here.
- **Test coverage of the abstraction**: v0.1 ships frozen at 31/31 plans, 403 tests. This audit does not measure whether tests would support multi-lens refactoring; that is a follow-on concern.

