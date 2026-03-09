# Phase 2: Workflow State - Context

**Gathered:** 2026-03-09
**Status:** Ready for planning

<domain>
## Phase Boundary

Users can organize their research workflow with collections, triage states, saved queries, and delta tracking to answer "what's new since I last checked." This phase builds on the Phase 1 metadata substrate (paper model, search, browse) and adds stateful workflow primitives. No interest modeling, no enrichment, no MCP server yet.

</domain>

<decisions>
## Implementation Decisions

### Collection semantics
- Flat collections (no hierarchy/nesting)
- Many-to-many: papers can belong to multiple collections simultaneously
- Slug-style unique names (lowercase, hyphens, no spaces) — auto-slugify from input
- Collections renamable after creation
- Metadata: name + created_at + updated_at (minimal)
- No limits on collection count or papers per collection
- Sort at query time (default: date added, newest first; options: by paper date, alphabetical)
- Collection listing includes paper counts
- Search/filter within a collection (compose with Phase 1 search)
- Bulk add and bulk remove supported (list of arxiv_ids)
- Track membership source (manual, saved query, agent) on the join table
- Include merge operation (combine two collections)
- Reverse lookup: given a paper, list all its collections
- Delete dissolves grouping by default; optional --purge for orphaned papers
- Collections can be archived (hidden from default listing, queryable with --include-archived)
- Listing papers in a collection includes each paper's triage state
- CLI: `arxiv-mcp collection create/list/delete/add/remove/show/merge/archive`

### Triage state scope
- Global per-paper (not per-collection) — a paper has one triage state across the system
- Six fixed states: unseen, shortlisted, dismissed, read, cite-later, archived
- States are NOT extensible (fixed enum)
- Free-form transitions (any state to any other, no constraints)
- Default "unseen" inferred from absence (no row = unseen, avoids millions of default rows)
- Triage state transitions logged as audit trail: (paper_id, old_state, new_state, timestamp, source, optional reason)
- Optional reason field on triage transitions (e.g., "not my subfield", "interesting method")
- Batch triage supports both explicit ID lists and query-based bulk operations
- Query-based batch triage: dry-run by default, requires --confirm to execute
- Triage state as a filter dimension composable with search (category, date, text)
- Triage state visible in search and browse output (always shown)
- No undo mechanism — re-triage instead (transitions are free-form)
- Paper version updates: keep triage state, flag the update separately
- CLI: `arxiv-mcp triage mark/list/batch/log` subgroup

### Saved queries & watches
- Saved queries are named (slug-style, same convention as collections)
- Saved queries are editable after creation (update params, rename, change ranking)
- Saved queries track usage: run_count and last_run_at
- Saved queries support triage state and collection membership as filter parameters
- "Save from search" workflow: save the current search as a named query
- JSON import/export for saved queries
- Soft limits with warnings for query/watch proliferation
- Saved queries with deleted collection references: query survives, invalid filter skipped with warning
- Watch = saved query + checkpoint metadata (extends, not separate entity)
- Watch cadence hint stored (daily, weekly) — not enforced, advisory for external schedulers/agents
- Watch checks: on-demand (user/agent triggers explicitly)
- Watch checkpoint auto-advances on check
- Watch delta results: full paper details (same shape as search), paginated
- Check-all command: runs every active watch, returns combined summary
- Watches support pause/resume (paused watches skipped by check-all)
- Manual checkpoint reset ("pretend I haven't checked since date X")
- Watch dashboard: list all watches with status, last checked, pending delta estimate, cadence
- Combined CLI subgroup (Claude's discretion on exact structure)

### State durability & reset
- Full nuclear reset available (wipes all workflow state, preserves paper corpus, requires --confirm)
- JSON export/import for all workflow state (collections, triage states, saved queries, watches)
- Export includes triage transition logs (full audit trail)
- Export is configurable/selective (filter by entity type or specific items)
- Import merge behavior: Claude's discretion on conflict resolution strategy
- Archive status for collections (soft removal, still queryable)
- Stats command: overview of all workflow state with cross-entity insights (orphaned papers, stale watches)

### Paper detail view
- Unified `arxiv-mcp paper show <id>` command showing full metadata + triage state + collection memberships in one view

### Cross-entity search integration
- Search results from search/browse commands to include triage state and collection context per paper
- Hybrid search-to-action workflow: paper IDs for piping (agent-friendly), optional session cache for position references (Claude's discretion)

### Phase 3 anticipation
- Light anticipation: triage logs as interest signals, saved query usage data, collection membership source tracking — all Phase 3-ready without Phase 3 code

### Claude's Discretion
- Service layer vs query-builder pattern (recommended: service layer for workflow operations)
- Session management approach (async context managers for transactions)
- Domain models vs ORM models for return types
- Module organization (per-entity vs flat)
- Result envelope type for consistent paginated responses
- Whether to refactor Phase 1 search into the same pattern
- Configuration system vs hardcoded defaults
- Test strategy details (same Phase 1 patterns vs refactored infrastructure)
- Error handling details: structured vs plain, idempotent vs warning, partial success reporting
- Exit code conventions, verbosity flags, output format options
- Delta determination method (date-based checkpoint vs result set diffing)
- Saved query result snapshot (parameters only vs cached result IDs)
- Save-and-watch combined workflow
- Database schema organization (separate vs public schema)
- Alembic migration strategy (single vs per-entity)
- Import merge conflict resolution
- Auto-backup scheduling
- Data retention policy
- Cross-entity JSON export reference resolution
- Integration test scope
- Soft removal history on collection membership (for debugging agent activity)
- CLI subgroup naming for queries/watches

</decisions>

<specifics>
## Specific Ideas

- Track membership source on collection join table for debugging agent activity — "who added this paper and why?"
- Triage transition log with optional reason field enables agent explanations for triage decisions
- Stats command should include cross-entity insights like "5 shortlisted papers not in any collection" and "3 watches haven't been checked in 7+ days"
- Watch dashboard mirrors the "daily digest" concept from arxiv-sanity — check-all gives a quick morning summary
- Hybrid search-to-action: agent pipelines use paper IDs directly; optional session cache lets humans reference results by position
- Phase 3 anticipation: every workflow action generates data that becomes an interest signal (triage = relevance, saved queries = focus areas, collection composition = topical clusters)

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `db/queries.py`: Query builder pattern (build_search_query, build_browse_query, build_related_query) — composable with workflow filters
- `db/models.py`: Paper model with arxiv_id PK — foreign key target for workflow tables
- `models/pagination.py`: Cursor model for keyset pagination — reusable for collection listing, watch deltas
- `search/service.py`: Search service layer — pattern to follow or extend
- `cli.py`: Click group with subgroup registration pattern — add collection/triage/query subgroups the same way
- `config.py`: Configuration module — extend with workflow defaults

### Established Patterns
- SQLAlchemy ORM with async engine (db/engine.py)
- Alembic migrations (hand-written, not autogenerated — per Phase 1 decision)
- Keyset cursor pagination for all paginated results
- Click subgroups for CLI organization (harvest, search)
- Function-scoped async test fixtures (per Phase 1 decision)

### Integration Points
- Paper.arxiv_id as FK target for collection_papers, triage_states, saved_queries
- Paper.search_vector for composing text search with workflow filters (triage state, collection membership)
- Paper.category_list (GIN indexed) for category-based batch triage
- Paper.announced_date / submitted_date / updated_date for watch checkpoint date comparisons
- Existing search query builder can be extended with JOIN-based workflow filters

</code_context>

<deferred>
## Deferred Ideas

- "Pin to collection" (saved query auto-adds results to a collection) — compose in Phase 6 MCP prompts
- Collection-to-query conversion (derive search params from collection contents) — Phase 3 interest modeling territory
- Auto-export on schedule — low priority, rely on on-demand export + PostgreSQL durability
- Interactive notification digests for watches — Phase 6 MCP prompts (daily-digest)

</deferred>

---

*Phase: 02-workflow-state*
*Context gathered: 2026-03-09*
