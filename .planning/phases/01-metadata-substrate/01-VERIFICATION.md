---
phase: 01-metadata-substrate
verified: 2026-03-09T15:10:00Z
status: passed
score: 5/5 success criteria verified
must_haves:
  truths:
    - "User can trigger OAI-PMH bulk harvest and see papers appear in the database with all four time semantics correctly stored"
    - "User can search papers by title, author, abstract, category, and date range with AND/OR composition and get paginated results"
    - "User can browse recently announced papers filtered by arXiv category and switch between time bases"
    - "User can find related papers from a seed paper via lexical similarity"
    - "Every stored paper has provenance metadata and per-paper license/rights data"
  artifacts:
    - path: "src/arxiv_mcp/db/models.py"
      status: verified
    - path: "src/arxiv_mcp/models/paper.py"
      status: verified
    - path: "src/arxiv_mcp/models/pagination.py"
      status: verified
    - path: "src/arxiv_mcp/config.py"
      status: verified
    - path: "src/arxiv_mcp/db/engine.py"
      status: verified
    - path: "alembic/versions/001_initial_schema.py"
      status: verified
    - path: "data/categories.toml"
      status: verified
    - path: "tests/conftest.py"
      status: verified
    - path: "src/arxiv_mcp/ingestion/parsers.py"
      status: verified
    - path: "src/arxiv_mcp/ingestion/mapper.py"
      status: verified
    - path: "src/arxiv_mcp/ingestion/oai_pmh.py"
      status: verified
    - path: "src/arxiv_mcp/ingestion/arxiv_api.py"
      status: verified
    - path: "src/arxiv_mcp/ingestion/cli.py"
      status: verified
    - path: "src/arxiv_mcp/db/queries.py"
      status: verified
    - path: "src/arxiv_mcp/search/service.py"
      status: verified
    - path: "src/arxiv_mcp/search/pagination.py"
      status: verified
    - path: "src/arxiv_mcp/search/ranking.py"
      status: verified
    - path: "src/arxiv_mcp/search/cli.py"
      status: verified
---

# Phase 1: Metadata Substrate Verification Report

**Phase Goal:** Researchers can ingest arXiv papers, search them by metadata fields, and browse recent announcements with correct time semantics
**Verified:** 2026-03-09T15:10:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths (from ROADMAP.md Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can trigger OAI-PMH bulk harvest and see papers appear in the database with all four time semantics correctly stored | VERIFIED | OAIPMHHarvester in oai_pmh.py (306 lines) with harvest_bulk/harvest_incremental methods; parsers.py extracts submission_date (v1 date), update_date (latest version), announced_date, oai_datestamp; mapper.py maps all four to Paper ORM; Paper model has DateTime(timezone=True) for submitted/updated, Date for announced/oai_datestamp; 7 OAI-PMH tests pass; CLI commands `harvest bulk/incremental/fetch` wired |
| 2 | User can search papers by title, author, abstract, category, and date range with AND/OR composition and get paginated results | VERIFIED | build_search_query in queries.py supports websearch_to_tsquery (AND/OR), plainto_tsquery for title/author, category_list.any() filter, date range WHERE; SearchService.search_papers orchestrates; 12 search tests including test_boolean_and, test_boolean_or, test_combined_filters, test_cursor_pagination_forward all pass |
| 3 | User can browse recently announced papers filtered by arXiv category and switch between time bases | VERIFIED | build_browse_query with time_basis parameter selecting submitted_date/updated_date/announced_date; SearchService.browse_recent wired; test_browse_recent_all, test_browse_recent_by_category, test_browse_recent_time_basis all pass; CLI `search browse --time-basis` available |
| 4 | User can find related papers from a seed paper via lexical similarity | VERIFIED | build_related_query combines plainto_tsquery on title (AND precision) with websearch_to_tsquery OR-joined abstract keywords (recall), ranked by ts_rank_cd, seed excluded; SearchService.find_related_papers wired; test_find_related_papers and test_find_related_excludes_seed pass |
| 5 | Every stored paper has provenance metadata and per-paper license/rights data | VERIFIED | Paper model has source (String(32), default="oai_pmh"), fetched_at (DateTime TZ), last_metadata_update (DateTime TZ), processing_tier (Integer, default 0), promotion_reason; license_uri column present; mapper sets source, fetched_at=datetime.now(UTC), processing_tier=FTS_INDEXED; test_provenance and test_license pass |

**Score:** 5/5 truths verified

### Required Artifacts

All 18 artifacts across 3 plans verified at all three levels (exists, substantive, wired).

| Artifact | Min Lines | Actual | Status | Details |
|----------|-----------|--------|--------|---------|
| `src/arxiv_mcp/db/models.py` | 80 | 108 | VERIFIED | Paper model with 25+ columns, 8 indexes, ProcessingTier enum, Base |
| `src/arxiv_mcp/models/paper.py` | 60 | 119 | VERIFIED | PaperSummary, PaperDetail, PaperVersion, SearchResult with from_attributes |
| `src/arxiv_mcp/models/pagination.py` | 30 | 72 | VERIFIED | Cursor encode/decode, PageInfo, PaginatedResponse[T] generic |
| `src/arxiv_mcp/config.py` | 30 | 80 | VERIFIED | Settings with DB URLs, arXiv endpoints, category loading, get_settings() |
| `src/arxiv_mcp/db/engine.py` | 20 | 63 | VERIFIED | create_engine, session_factory, get_session context manager |
| `alembic/versions/001_initial_schema.py` | 50 | 132 | VERIFIED | Hand-written migration with papers table, tsvector trigger, GIN indexes, downgrade |
| `data/categories.toml` | 10 | 25 | VERIFIED | Default categories: cs, stat, math, eess archives with specific categories |
| `tests/conftest.py` | 40 | 145 | VERIFIED | Async DB fixtures, tsvector trigger SQL, sample_paper_data factory |
| `src/arxiv_mcp/ingestion/parsers.py` | 80 | 261 | VERIFIED | parse_arxiv_raw, parse_arxiv_format, parse_oai_dc; RawPaperMetadata dataclass |
| `src/arxiv_mcp/ingestion/mapper.py` | 40 | 108 | VERIFIED | map_to_paper with date parsing, category splitting, version serialization |
| `src/arxiv_mcp/ingestion/oai_pmh.py` | 80 | 306 | VERIFIED | OAIPMHHarvester with bulk/incremental, batch upsert ON CONFLICT, checkpoint |
| `src/arxiv_mcp/ingestion/arxiv_api.py` | 60 | 228 | VERIFIED | ArxivAPIClient with fetch_paper, search, rate limiting, Atom XML parsing |
| `src/arxiv_mcp/ingestion/cli.py` | 40 | 148 | VERIFIED | Click subgroup: harvest bulk/incremental/fetch with Rich progress |
| `src/arxiv_mcp/db/queries.py` | 80 | 238 | VERIFIED | build_search_query, build_browse_query, build_related_query with tsvector |
| `src/arxiv_mcp/search/service.py` | 100 | 176 | VERIFIED | SearchService with search_papers, browse_recent, find_related_papers |
| `src/arxiv_mcp/search/pagination.py` | 40 | 54 | VERIFIED | build_page_info with keyset cursor construction |
| `src/arxiv_mcp/search/ranking.py` | 30 | 51 | VERIFIED | shape_search_results converting rows to SearchResult with scores |
| `src/arxiv_mcp/search/cli.py` | 50 | 227 | VERIFIED | Click subgroup: search query/browse/related with Rich table + JSON output |

### Key Link Verification

All key links from the three plans verified.

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `db/models.py` | `db/engine.py` | Base declarative import | WIRED | engine.py is independent; models.py defines Base; alembic/env.py imports `from arxiv_mcp.db.models import Base` (line 21) confirming the link |
| `config.py` | `data/categories.toml` | Category config loading | WIRED | `load_categories()` reads `PROJECT_ROOT / self.categories_file` using tomllib |
| `alembic/env.py` | `db/models.py` | target_metadata | WIRED | Line 31: `target_metadata = Base.metadata` after importing Base from models |
| `ingestion/oai_pmh.py` | `ingestion/parsers.py` | parse_arxiv_raw call | WIRED | Line 131: `raw = parse_arxiv_raw(record.metadata)` in harvest loop |
| `ingestion/parsers.py` | `ingestion/mapper.py` | RawPaperMetadata | WIRED | mapper.py imports `from arxiv_mcp.ingestion.parsers import RawPaperMetadata` and uses it in map_to_paper signature |
| `ingestion/mapper.py` | `db/models.py` | Creates Paper instances | WIRED | Line 84: `return Paper(arxiv_id=raw.arxiv_id, ...)` with import on line 13 |
| `ingestion/oai_pmh.py` | `db/engine.py` | async session for inserts | WIRED | Constructor takes session_factory; _upsert_batch uses `async with self.session_factory() as session` |
| `ingestion/cli.py` | `cli.py` | Click subgroup registration | WIRED | cli.py line 21: `cli.add_command(harvest_group)` |
| `search/service.py` | `db/queries.py` | Query builder calls | WIRED | Imports build_search_query, build_browse_query, build_related_query (line 16); calls each in respective methods |
| `db/queries.py` | `db/models.py` | Paper model references | WIRED | Line 14: `from arxiv_mcp.db.models import Paper`; uses Paper.search_vector, Paper.category_list, Paper.arxiv_id throughout |
| `search/service.py` | `search/pagination.py` | Pagination applied | WIRED | Line 19: `from arxiv_mcp.search.pagination import build_page_info`; called in search_papers and browse_recent |
| `search/service.py` | `search/ranking.py` | Result shaping | WIRED | Line 20: `from arxiv_mcp.search.ranking import shape_search_results`; called in all three service methods |
| `search/cli.py` | `cli.py` | Click subgroup registration | WIRED | cli.py lines 24-29: imports and adds search_group |

### Requirements Coverage

All 16 phase requirements verified.

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| INGS-01 | 01-02 | OAI-PMH bulk harvesting with resumption token handling | SATISFIED | OAIPMHHarvester.harvest_bulk uses oaipmh-scythe which handles resumption tokens; 7 harvest tests pass |
| INGS-02 | 01-02 | arXiv API for incremental/targeted queries | SATISFIED | ArxivAPIClient with fetch_paper and search methods; 5 API tests pass |
| INGS-03 | 01-01 | Four distinct time semantics per paper | SATISFIED | Paper model has submitted_date, updated_date, announced_date, oai_datestamp as separate typed columns; test_time_semantics passes |
| INGS-04 | 01-01 | Per-paper license/rights metadata | SATISFIED | Paper.license_uri column; parsers extract license from arXivRaw; test_license passes |
| INGS-05 | 01-02 | Incremental harvesting with datestamp-based checkpoints | SATISFIED | harvest_incremental reads/saves checkpoint JSON file; test_harvest_incremental_uses_from_date and test_harvest_incremental_saves_checkpoint pass |
| PAPR-01 | 01-01 | Canonical paper model with arXiv ID as primary key | SATISFIED | Paper.arxiv_id = mapped_column(String(20), primary_key=True); test_canonical_model passes |
| PAPR-02 | 01-01 | Title, authors, abstract, categories, version history | SATISFIED | All present as columns; version_history as JSONB; test_full_metadata passes |
| PAPR-03 | 01-01 | External identifiers (DOI, OpenAlex, Semantic Scholar) | SATISFIED | doi, openalex_id, semantic_scholar_id as nullable columns; test_external_ids passes |
| PAPR-04 | 01-01 | Provenance: data source, fetch timestamp, enrichment history | SATISFIED | source, fetched_at, last_metadata_update, processing_tier columns; test_provenance passes |
| SRCH-01 | 01-03 | Search by title, author, abstract, category, date range | SATISFIED | build_search_query supports all five field types; tests for each pass |
| SRCH-02 | 01-03 | AND/OR query composition | SATISFIED | websearch_to_tsquery natively supports AND/OR; test_boolean_and, test_boolean_or pass |
| SRCH-03 | 01-03 | Browse recently announced papers filtered by category | SATISFIED | build_browse_query with category filter; test_browse_recent_by_category passes |
| SRCH-04 | 01-03 | Time basis switching (submission, update, announcement) | SATISFIED | _get_date_column maps time_basis param to correct column; test_browse_recent_time_basis passes |
| SRCH-05 | 01-03 | Find related papers from seed via lexical similarity | SATISFIED | build_related_query with title AND + abstract OR tsvector combination; test_find_related_papers passes |
| SRCH-06 | 01-03 | Cursor-based pagination with predictable result sizes | SATISFIED | Cursor encode/decode, build_page_info, page_size capping; test_cursor_pagination_forward, test_page_size_capped pass |

No orphaned requirements: REQUIREMENTS.md maps INGS-01 through INGS-05, PAPR-01 through PAPR-04, SRCH-01 through SRCH-06 to Phase 1, and all 16 appear in plan frontmatter `requirements` fields.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | No anti-patterns detected |

No TODO, FIXME, PLACEHOLDER, or stub patterns found in any source file. All `pass` statements are structurally required (DeclarativeBase body, Click group bodies, silent ValueError catch).

### Human Verification Required

### 1. OAI-PMH Live Harvest Test

**Test:** Run `arxiv-mcp harvest bulk --set cs --from-date 2026-03-08 --batch-size 10` against real arXiv OAI-PMH endpoint
**Expected:** Papers appear in the database with correct metadata, time semantics, and category filtering
**Why human:** Tests use mocked oaipmh-scythe; actual OAI-PMH response format, network errors, and arXiv rate limiting cannot be verified programmatically without making real API calls

### 2. arXiv API Live Fetch Test

**Test:** Run `arxiv-mcp harvest fetch 2301.00001` against real arXiv API
**Expected:** Paper metadata displayed with correct title, authors, categories, dates
**Why human:** Tests mock httpx responses; real Atom XML parsing and edge cases in arXiv data cannot be verified without live calls

### 3. Search CLI Output Quality

**Test:** Populate database with sample papers, then run `arxiv-mcp search query -q "transformer attention"` and `arxiv-mcp search browse -c cs.CL`
**Expected:** Rich table output is readable, scores are meaningful, pagination cursor works for next page
**Why human:** Output formatting and relevance quality are visual/subjective assessments

### Gaps Summary

No gaps found. All 5 success criteria from ROADMAP.md are satisfied. All 16 requirements mapped to Phase 1 have passing tests. All 18 artifacts exist, are substantive (exceed min_lines), and are fully wired. All 13 key links across the three plans are connected. No anti-patterns detected. 64 tests pass in 4.91 seconds.

The phase delivers a complete metadata substrate: paper model with all columns and indexes, ingestion pipeline with OAI-PMH and arXiv API, and search/browse/discovery with PostgreSQL FTS. The only unverified aspects are live integration with arXiv's actual API endpoints, which require network access and are flagged for human testing.

---

_Verified: 2026-03-09T15:10:00Z_
_Verifier: Claude (gsd-verifier)_
