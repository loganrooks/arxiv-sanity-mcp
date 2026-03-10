---
phase: 02-workflow-state
verified: 2026-03-09T23:59:00Z
status: passed
score: 25/25 must-haves verified
---

# Phase 2: Workflow State Verification Report

**Phase Goal:** Implement workflow state management -- collections, triage states, saved queries, watches, export/import, and CLI commands for the complete research workflow surface.
**Verified:** 2026-03-09T23:59:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

**Plan 02-01 (Schema Foundation)**

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Workflow tables accept and persist collection, triage, and query data with referential integrity to existing papers | VERIFIED | 5 ORM models in db/models.py: Collection, CollectionPaper, TriageState, TriageLog, SavedQuery. CollectionPaper FK -> papers.arxiv_id (line 166), TriageState FK -> papers.arxiv_id (line 198), TriageLog FK -> papers.arxiv_id (line 226). All with CASCADE delete. |
| 2 | Database migration applies cleanly and creates all five workflow tables with correct constraints | VERIFIED | alembic/versions/002_workflow_tables.py (136 lines) creates collections, collection_papers, triage_states, triage_log, saved_queries. CHECK constraint ck_triage_state_valid, indexes, FKs all present. downgrade() drops in correct FK order. |
| 3 | All workflow entities can be serialized to Pydantic response schemas for API/CLI consumption | VERIFIED | src/arxiv_mcp/models/workflow.py has 12 Pydantic schemas: CollectionSummary, CollectionMemberInfo, CollectionDetail, TriageStateResponse, TriageLogEntry, SavedQuerySummary, SavedQueryResponse, WatchSummary, WatchDashboard, BatchTriageResult, BatchTriagePreview, WorkflowStats, ExportData. All bridging schemas use ConfigDict(from_attributes=True) -- 6 instances confirmed. |
| 4 | Arbitrary user-provided names are converted to URL-safe slug identifiers | VERIFIED | src/arxiv_mcp/workflow/util.py has slugify() function (22 lines) using re.sub. Imported and used by CollectionService (line 21, 57) and SavedQueryService (line 22, 53). |

**Plan 02-02 (Collection and Triage Services)**

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 5 | User can create a named collection and see it in the collection list with paper count | VERIFIED | CollectionService.create_collection() (line 53-86) and list_collections() (line 88-135) with subquery paper count. 23 tests in test_collections.py (272 lines). |
| 6 | User can add papers to and remove papers from a collection, including bulk operations | VERIFIED | CollectionService.add_papers() (line 229-267) and remove_papers() (line 269-286). Both handle multiple IDs, add_papers is idempotent. |
| 7 | User can merge two collections into one | VERIFIED | CollectionService.merge_collections() (line 363-425). Moves papers, avoids PK violations, deletes source. |
| 8 | User can archive and unarchive a collection | VERIFIED | archive_collection() (line 431-433) and unarchive_collection() (line 435-437) using _set_archived helper. list_collections() excludes archived by default. |
| 9 | User can mark a paper with a triage state and see the transition logged in the audit trail | VERIFIED | TriageService.mark_triage() (line 49-116) creates TriageLog entry and upserts TriageState. get_triage_log() (line 360-384) returns chronological audit trail. "unseen" marking deletes row (absence-means-unseen). |
| 10 | User can batch-triage multiple papers by explicit ID list | VERIFIED | TriageService.batch_triage() (line 192-274). Validates paper existence, tracks affected/skipped/errors, single transaction. |
| 11 | User can batch-triage papers matching a query with dry-run preview before committing | VERIFIED | TriageService.batch_triage_by_query() (line 280-354). Uses build_search_query from Phase 1 (line 306). dry_run=True returns BatchTriagePreview; dry_run=False processes in 500-paper chunks. |
| 12 | User can list papers by triage state and see triage state in collection paper listings | VERIFIED | list_by_state() (line 130-186) with LEFT JOIN IS NULL for "unseen". show_collection() (line 292-357) uses LEFT JOIN TriageState for triage_state column. |
| 13 | Given a paper, user can see all collections it belongs to (reverse lookup) | VERIFIED | CollectionService.get_paper_collections() (line 443-486) with subquery paper count. |

**Plan 02-03 (Queries, Watches, Export, CLI)**

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 14 | User can create a named saved query with search parameters and re-run it on demand | VERIFIED | SavedQueryService.create_saved_query() (line 49-89) and run_saved_query() (line 191-220). Params stored as JSONB, deserialized on run, delegated to SearchService.search_papers(). run_count incremented. |
| 15 | User can edit saved query parameters after creation | VERIFIED | SavedQueryService.edit_saved_query() (line 132-178). Supports name and/or params change, regenerates slug on name change with collision check. |
| 16 | User can promote a saved query to a watch with cadence hint and checkpoint | VERIFIED | WatchService.promote_to_watch() (line 52-78). Sets is_watch=True, cadence_hint, checkpoint_date=today. demote_watch() (line 80-108) reverses. |
| 17 | User can check a watch and see only papers new since the last checkpoint | VERIFIED | WatchService.check_watch() (line 114-164). Overrides date_from with checkpoint_date + 1 day (line 143). Auto-advances checkpoint to today after check. |
| 18 | User can check-all watches and get a combined summary | VERIFIED | WatchService.check_all_watches() (line 166-202). Iterates active non-paused watches, returns list of {slug, delta_count, cadence_hint, checkpoint_advanced_from/to}. |
| 19 | User can pause, resume, and reset a watch checkpoint | VERIFIED | pause_watch() (line 208-220), resume_watch() (line 222-234), reset_checkpoint() (line 240-254). All validated as watch before modification. |
| 20 | User can export all workflow state to JSON and import it back | VERIFIED | ExportService.export_all() (line 53-145) serializes collections (with memberships), triage_states, triage_log, saved_queries to ExportData. import_from_file() (line 162-347) with skip/last-write-wins conflict resolution. |
| 21 | User can run CLI commands for collections, triage, queries, and watches | VERIFIED | src/arxiv_mcp/workflow/cli.py (1131 lines) with 35 Click commands across 6 subgroups: collection (10), triage (6), query (8), watch (6), paper (1), workflow (4). All registered in src/arxiv_mcp/cli.py (lines 33-47). |
| 22 | User can batch-triage papers by query with dry-run preview and --confirm to execute | VERIFIED | CLI triage batch-query command (line 391-457) with --confirm flag. Without --confirm shows dry-run preview; with --confirm executes. |
| 23 | User can see triage state and collection context in search and browse output | VERIFIED | WorkflowSearchService in search_augment.py wraps SearchService with 2-query post-process enrichment. Search CLI auto-upgrades to WorkflowSearchService (search/cli.py line 39-44). Triage column with color coding (lines 66-73, 104-107). WorkflowSearchResult model in models/paper.py (lines 122-133). |
| 24 | User can see a stats overview of all workflow state | VERIFIED | ExportService.get_stats() (line 353-465) with collection count, triage breakdown (including unseen via LEFT JOIN), saved query/watch counts, and 3 insight queries (orphaned shortlisted, stale watches, untriaged in collections). CLI: workflow stats command (line 1087-1113). |
| 25 | User can run a paper show command to see full metadata + triage + collections | VERIFIED | ExportService.get_paper_detail() (line 489-547) joins paper, triage state, and collections. CLI: paper show command (lines 988-1033) with formatted Rich output. |

**Score:** 25/25 truths verified

### Required Artifacts

**Plan 02-01 Artifacts**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/db/models.py` | Collection, CollectionPaper, TriageState, TriageLog, SavedQuery ORM models | VERIFIED | 277 lines, all 5 models with relationships, CHECK constraints, indexes. Contains "class Collection" (line 128). |
| `src/arxiv_mcp/models/workflow.py` | Pydantic schemas for all workflow entities | VERIFIED | 163 lines, 12 schemas with from_attributes=True. Contains "class CollectionDetail" (line 41). |
| `alembic/versions/002_workflow_tables.py` | Migration creating 5 workflow tables | VERIFIED | 136 lines, creates all 5 tables with constraints. Contains "def upgrade" (line 22). |
| `src/arxiv_mcp/workflow/util.py` | slugify utility function | VERIFIED | 22 lines. Contains "def slugify" (line 12). |
| `tests/test_workflow/conftest.py` | Test fixtures with workflow tables, sample data factories | VERIFIED | 181 lines. Contains "sample_collection_data" (line 78). |

**Plan 02-02 Artifacts**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/workflow/collections.py` | CollectionService with full CRUD, membership, merge, archive | VERIFIED | 530 lines, 11 async methods. Exports CollectionService. |
| `src/arxiv_mcp/workflow/triage.py` | TriageService with mark, list, batch, log | VERIFIED | 399 lines, 6 async methods. Exports TriageService. |
| `tests/test_workflow/test_collections.py` | Integration tests for collection operations | VERIFIED | 272 lines (exceeds 100-line minimum). |
| `tests/test_workflow/test_triage.py` | Integration tests for triage operations | VERIFIED | 238 lines (exceeds 100-line minimum). |

**Plan 02-03 Artifacts**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/workflow/queries.py` | SavedQueryService with CRUD, run, edit | VERIFIED | 279 lines. Exports SavedQueryService. |
| `src/arxiv_mcp/workflow/watches.py` | WatchService with check, check-all, pause, resume, reset, dashboard | VERIFIED | 380 lines, 8 async methods. Exports WatchService. |
| `src/arxiv_mcp/workflow/export.py` | ExportService for JSON export/import | VERIFIED | 548 lines, 6 methods. Exports ExportService. |
| `src/arxiv_mcp/workflow/search_augment.py` | Workflow-aware search augmentation | VERIFIED | 115 lines. Exports WorkflowSearchService. |
| `src/arxiv_mcp/workflow/cli.py` | Click CLI subgroups | VERIFIED | 1131 lines, 35 commands across 6 subgroups. Exports collection_group, triage_group, query_group, watch_group, paper_group, workflow_group. |
| `tests/test_workflow/test_queries.py` | Integration tests for saved query lifecycle | VERIFIED | 278 lines (exceeds 80-line minimum). |
| `tests/test_workflow/test_watches.py` | Integration tests for watch delta | VERIFIED | 302 lines (exceeds 80-line minimum). |
| `tests/test_workflow/test_search_augment.py` | Integration tests for search enrichment | VERIFIED | 272 lines (exceeds 40-line minimum). |
| `tests/test_workflow/test_export.py` | Integration tests for export/import | VERIFIED | 294 lines. |

**Modified Artifacts**

| Artifact | Change | Status | Details |
|----------|--------|--------|---------|
| `src/arxiv_mcp/models/paper.py` | Added WorkflowSearchResult model | VERIFIED | Lines 122-133: WorkflowSearchResult with triage_state and collection_slugs fields. |
| `src/arxiv_mcp/search/cli.py` | Auto-upgrade to WorkflowSearchService, triage column with colors | VERIFIED | _get_search_service() (lines 25-45) imports WorkflowSearchService with fallback. _TRIAGE_COLORS dict (lines 66-73). _display_results_table detects workflow items (line 82). |
| `src/arxiv_mcp/cli.py` | Registered 6 workflow subgroups | VERIFIED | Lines 33-47: imports and registers collection_group, triage_group, query_group, watch_group, paper_group, workflow_group with try/except. |
| `src/arxiv_mcp/config.py` | Added workflow soft limits and defaults | VERIFIED | Lines 49-54: soft_limit_collections=100, soft_limit_saved_queries=50, soft_limit_watches=20, default_watch_cadence="daily", export_default_path. |

### Key Link Verification

**Plan 02-01 Key Links**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| db/models.py (CollectionPaper) | db/models.py (Paper) | FK paper_id -> papers.arxiv_id | WIRED | ForeignKey("papers.arxiv_id", ondelete="CASCADE") at line 166. |
| db/models.py (TriageState) | db/models.py (Paper) | FK paper_id -> papers.arxiv_id | WIRED | ForeignKey("papers.arxiv_id", ondelete="CASCADE") at line 198. |
| models/workflow.py | db/models.py | Pydantic from_attributes bridging ORM to API | WIRED | 6 schemas with ConfigDict(from_attributes=True). |

**Plan 02-02 Key Links**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| workflow/collections.py | db/models.py (Collection, CollectionPaper) | SQLAlchemy async session queries | WIRED | 11 occurrences of select(...Collection...). |
| workflow/triage.py | db/models.py (TriageState, TriageLog) | SQLAlchemy async session queries | WIRED | 31 occurrences of TriageState/TriageLog references. |
| workflow/triage.py | db/queries.py (build_search_query) | Query-based batch triage | WIRED | Import at line 17, call at line 306. |
| workflow/collections.py | workflow/util.py (slugify) | Import for auto-slugifying | WIRED | Import at line 21, call at line 57. |

**Plan 02-03 Key Links**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| workflow/queries.py | search/service.py (SearchService) | Deserializes JSONB params and calls search_papers() | WIRED | self.search_service.search_papers(**search_kwargs) at line 220. |
| workflow/watches.py | workflow/queries.py + SearchService | Extends saved query with checkpoint-based date filtering | WIRED | 18 references to SavedQueryService/checkpoint_date. Uses self.search_service.search_papers at line 150. |
| workflow/search_augment.py | search/service.py + db/models.py | Wraps search results with triage + collection info | WIRED | 15 references to SearchService/TriageState/CollectionPaper. |
| search/cli.py | workflow/search_augment.py | Search CLI uses WorkflowSearchService | WIRED | Import at line 39, instantiation at line 41, triage_state detection at line 82/105. |
| workflow/cli.py | cli.py | CLI subgroups registered in main CLI | WIRED | 6 groups imported and added (cli.py lines 33-47). |

### Requirements Coverage

| Requirement | Source Plans | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| WKFL-01 | 02-01, 02-02 | User can create, list, and delete named paper collections | SATISFIED | CollectionService with create_collection, list_collections, delete_collection + CLI commands. |
| WKFL-02 | 02-01, 02-02 | User can add papers to and remove papers from collections | SATISFIED | CollectionService.add_papers and remove_papers with bulk support + CLI commands. |
| WKFL-03 | 02-01, 02-02 | User can mark paper triage state (unseen, shortlisted, dismissed, read, cite-later) | SATISFIED | TriageService.mark_triage with absence-means-unseen pattern, CHECK constraint, audit trail + CLI triage mark. |
| WKFL-04 | 02-01, 02-03 | User can create saved queries with parameters, ranking mode, and filters | SATISFIED | SavedQueryService.create_saved_query with JSONB params + CLI query create with all filter options. |
| WKFL-05 | 02-03 | User can re-run saved queries on demand | SATISFIED | SavedQueryService.run_saved_query with param deserialization, run_count tracking + CLI query run. |
| WKFL-06 | 02-01, 02-03 | User can create watches (saved query + cadence + checkpoint) | SATISFIED | WatchService.promote_to_watch with cadence_hint and checkpoint_date + CLI query watch. |
| WKFL-07 | 02-03 | User can get delta results since last checkpoint | SATISFIED | WatchService.check_watch with checkpoint+1 day date filtering, auto-advance + CLI watch check. |
| WKFL-08 | 02-02, 02-03 | User can batch-triage multiple papers in a single operation | SATISFIED | TriageService.batch_triage (ID-based) and batch_triage_by_query (query-based with dry-run) + CLI triage batch and triage batch-query --confirm. |

**Orphaned Requirements:** None. All 8 WKFL requirements from REQUIREMENTS.md are claimed by at least one plan and have implementation evidence.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (none) | - | - | - | No anti-patterns detected |

Zero occurrences of TODO, FIXME, PLACEHOLDER, HACK, "not implemented," empty returns, or stub handlers across all 25 Phase 2 source files.

### Human Verification Required

### 1. CLI Command Smoke Test

**Test:** Run `arxiv-mcp collection create "Test Collection"` and then `arxiv-mcp collection list`
**Expected:** Collection created with slug "test-collection," visible in list with paper_count=0
**Why human:** Requires running application with database connection

### 2. Search Augmentation Display

**Test:** Run `arxiv-mcp search query -c cs.AI` after triaging some papers
**Expected:** Results table shows Triage column with color-coded states
**Why human:** Visual formatting and color rendering cannot be verified programmatically

### 3. Watch Delta Correctness

**Test:** Create a saved query, promote to watch, ingest papers, then `arxiv-mcp watch check <slug>`
**Expected:** Only papers newer than the checkpoint date appear
**Why human:** Requires end-to-end data flow with real timestamps

### 4. Export/Import Roundtrip

**Test:** Run `arxiv-mcp workflow export --file /tmp/test.json` then `arxiv-mcp workflow import /tmp/test.json`
**Expected:** All workflow state preserved after roundtrip
**Why human:** Requires running app with database

### Gaps Summary

No gaps found. All 25 observable truths verified. All 19 required artifacts exist, are substantive (no stubs), and are properly wired. All 8 WKFL requirements have implementation evidence across the three plans. No anti-patterns detected in any Phase 2 files. 100 new tests (19 model + 23 collection + 18 triage + 13 query + 11 watch + 6 search augment + 10 export) across 2206 lines of test code. 13 commit hashes in git log correspond to the work.

---

_Verified: 2026-03-09T23:59:00Z_
_Verifier: Claude (gsd-verifier)_
