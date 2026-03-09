---
phase: 01-metadata-substrate
plan: 03
subsystem: search
tags: [postgresql-fts, tsvector, websearch-to-tsquery, cursor-pagination, click-cli, rich, sqlalchemy]

# Dependency graph
requires:
  - "01-01: Paper SQLAlchemy model with tsvector trigger and GIN indexes"
  - "01-01: Pydantic schemas (PaperSummary, SearchResult, Cursor, PaginatedResponse)"
  - "01-01: Async engine/session factory"
  - "01-01: Settings with pagination config"
  - "01-01: Click CLI skeleton"
provides:
  - "SearchService with search_papers, browse_recent, find_related_papers operations"
  - "SQLAlchemy query builders: build_search_query, build_browse_query, build_related_query"
  - "Keyset cursor pagination with build_page_info for stable O(1) page navigation"
  - "Result shaping: SearchResult with PaperSummary, truncated abstracts, relevance scores"
  - "CLI commands: arxiv-mcp search query, browse, related with rich output + JSON mode"
affects: [02-workflow-state, 04-mcp-surface]

# Tech tracking
tech-stack:
  added: []
  patterns: [websearch-to-tsquery-for-boolean-search, plainto-tsquery-for-names-and-titles, keyset-cursor-pagination-with-compound-tuple, tsvector-or-combination-for-related-papers]

key-files:
  created:
    - src/arxiv_mcp/db/queries.py
    - src/arxiv_mcp/search/service.py
    - src/arxiv_mcp/search/pagination.py
    - src/arxiv_mcp/search/ranking.py
    - src/arxiv_mcp/search/cli.py
    - tests/test_search/__init__.py
    - tests/test_search/conftest.py
    - tests/test_search/test_service.py
    - tests/test_search/test_pagination.py
  modified:
    - src/arxiv_mcp/search/__init__.py
    - src/arxiv_mcp/cli.py

key-decisions:
  - "Used websearch_to_tsquery for boolean search (supports AND/OR natural syntax out of the box)"
  - "Used plainto_tsquery with 'simple' config for author names (avoids English stemming of names)"
  - "Used title AND + abstract OR tsquery combination for related papers (balanced precision and recall)"
  - "Browse recent uses max(date) subquery for cutoff instead of current_date (deterministic tests)"
  - "Keyset cursor uses tuple comparison with rank expression, not label (PostgreSQL cannot reference SELECT aliases in WHERE)"

patterns-established:
  - "SearchService pattern: session_factory + settings DI, async methods, query builder delegation"
  - "Query builder pattern: pure functions returning Select statements, caller executes"
  - "Result shaping: rows -> shape_search_results -> SearchResult with PaperSummary"
  - "CLI pattern: sync Click handler wrapping asyncio.run() with rich table output"
  - "Test isolation: drop_all before create_all in search conftest to avoid pg_type collision"

requirements-completed: [SRCH-01, SRCH-02, SRCH-03, SRCH-04, SRCH-05, SRCH-06]

# Metrics
duration: 8min
completed: 2026-03-09
---

# Phase 1 Plan 03: Search, Browse, and Discovery Summary

**Fielded search with AND/OR boolean composition via websearch_to_tsquery, category browsing with time basis switching, seed-based related papers via combined title/abstract tsvector ranking, and cursor-based keyset pagination across all operations**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-09T14:36:39Z
- **Completed:** 2026-03-09T14:44:42Z
- **Tasks:** 2
- **Files modified:** 11 created/modified

## Accomplishments
- Three search operations (search_papers, browse_recent, find_related_papers) with full integration test coverage (20 tests)
- Fielded search supporting title, author, abstract text, category, and date range filters with AND/OR boolean composition
- Keyset cursor pagination with stable page navigation and no result duplication across all operations
- CLI commands (search query, search browse, search related) with rich table display and JSON output mode

## Task Commits

Each task was committed atomically:

1. **Task 1: Query builders and search service (TDD)**
   - RED: `c8361ce` (test) - 20 failing tests for search service, pagination, browse, related
   - GREEN: `94267ac` (feat) - Full implementation passing all 20 tests

2. **Task 2: CLI commands** - `040bbfc` (feat) - search/browse/related CLI with rich output

## Files Created/Modified
- `src/arxiv_mcp/db/queries.py` - SQLAlchemy query builders for search, browse, and related queries
- `src/arxiv_mcp/search/service.py` - SearchService orchestrating query building, execution, shaping, pagination
- `src/arxiv_mcp/search/pagination.py` - Keyset cursor pagination with build_page_info
- `src/arxiv_mcp/search/ranking.py` - Result shaping: Row objects to SearchResult with truncated abstracts
- `src/arxiv_mcp/search/cli.py` - Click CLI subcommands with rich table and JSON output
- `src/arxiv_mcp/search/__init__.py` - Re-exports SearchService
- `src/arxiv_mcp/cli.py` - Updated to register search subgroup with graceful import handling
- `tests/test_search/conftest.py` - 15 sample papers across 4 categories with search_session fixtures
- `tests/test_search/test_service.py` - 17 integration tests for fielded search, boolean, browse, related
- `tests/test_search/test_pagination.py` - 3 cursor pagination integration tests

## Decisions Made
- **websearch_to_tsquery for boolean search:** PostgreSQL's websearch_to_tsquery natively supports AND/OR natural syntax, avoiding custom query parsing. Users write "transformer OR attention" directly.
- **'simple' config for author names:** Using 'simple' instead of 'english' text search configuration for author name matching prevents stemming that would mangle proper nouns (e.g., "Vaswani" would be stemmed incorrectly with 'english').
- **Combined title/abstract tsquery for related papers:** plainto_tsquery on the full title+abstract is too restrictive (all terms ANDed). Instead, use title as an AND query for precision combined with abstract keywords as an OR query for recall, then merge with tsquery || operator.
- **max(date) subquery for browse cutoff:** Using `SELECT max(date_col)` as the reference point instead of `current_date` makes tests deterministic regardless of when they run.
- **Rank expression in WHERE instead of label:** PostgreSQL does not allow referencing SELECT aliases in WHERE clauses. Cursor pagination must use the actual `ts_rank_cd(...)` expression for tuple comparison.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] PostgreSQL cannot reference SELECT label in WHERE clause**
- **Found during:** Task 1 (cursor pagination with text search)
- **Issue:** `text("rank")` in WHERE clause fails because PostgreSQL does not allow referencing SELECT aliases in WHERE. The query `WHERE (rank, arxiv_id) < ($1, $2)` errors with "column rank does not exist".
- **Fix:** Used the actual `ts_rank_cd(Paper.search_vector, tsquery)` expression in the tuple comparison instead of the label name.
- **Files modified:** src/arxiv_mcp/db/queries.py
- **Verification:** test_pagination_with_text_search passes
- **Committed in:** 94267ac (Task 1 GREEN commit)

**2. [Rule 1 - Bug] plainto_tsquery too restrictive for related-paper seed text**
- **Found during:** Task 1 (find_related_papers test)
- **Issue:** `plainto_tsquery('english', title + abstract)` creates an AND of all terms. With a long seed text (title + 500 chars abstract), the resulting tsquery has 30+ ANDed terms, matching zero other papers in the corpus.
- **Fix:** Changed to a two-part approach: title as AND query (precise) combined with abstract keywords (first 15 words > 3 chars) as OR query (broad recall), merged with tsquery `||` operator.
- **Files modified:** src/arxiv_mcp/db/queries.py
- **Verification:** test_find_related_papers and test_find_related_excludes_seed both pass
- **Committed in:** 94267ac (Task 1 GREEN commit)

**3. [Rule 3 - Blocking] Test isolation collision with pg_type for papers table**
- **Found during:** Task 1 (full suite run after search tests pass)
- **Issue:** When model tests and search tests run in the same pytest session, the search_session fixture's `create_all` hits "duplicate key violates unique constraint pg_type_typname_nsp_index" because the model tests' papers table type still exists.
- **Fix:** Added explicit `drop_all` before `create_all` in search conftest for clean table isolation.
- **Files modified:** tests/test_search/conftest.py
- **Verification:** Full test suite (64 tests) passes without errors
- **Committed in:** 94267ac (Task 1 GREEN commit)

---

**Total deviations:** 3 auto-fixed (2 bugs, 1 blocking)
**Impact on plan:** All fixes necessary for correctness. No scope creep.

## Issues Encountered
None beyond the auto-fixed deviations above.

## User Setup Required
None - uses existing PostgreSQL test database from Plan 01.

## Next Phase Readiness
- Search service ready to be exposed via MCP tools in Phase 4
- Query builders ready for extension with additional ranking signals (Phase 3 enrichments)
- CLI commands provide immediate utility for manual testing and exploration
- All 64 tests passing as regression suite baseline (24 foundation + 15 ingestion + 5 harvest + 20 search)

## Self-Check: PASSED

- All 10 created files verified present on disk
- All 3 task commits (c8361ce, 94267ac, 040bbfc) verified in git log
- Full test suite: 64 passed

---
*Phase: 01-metadata-substrate*
*Completed: 2026-03-09*
