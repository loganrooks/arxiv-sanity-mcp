---
phase: 03-interest-modeling-ranking
verified: 2026-03-10T01:35:00Z
status: passed
score: 4/4 must-haves verified
re_verification: false
---

# Phase 3: Interest Modeling & Ranking Verification Report

**Phase Goal:** Users can build explicit interest profiles from multiple signal types and get structured explanations for why each paper surfaced in results
**Verified:** 2026-03-10T01:35:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

Phase 3 ROADMAP.md defines 4 success criteria:

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | User can create an interest profile composed of seed paper sets, saved queries, followed authors, and negative examples | VERIFIED | ProfileService in `interest/profiles.py` (396 lines) provides create_profile, add_seed_paper, add_saved_query, add_followed_author, add_negative_example with full validation. InterestProfile and InterestSignal ORM models in `db/models.py` with CHECK constraints on signal_type for all 4 types. CLI commands: create, add-seed, add-query, follow, add-negative. 42 integration tests pass. |
| 2 | User can inspect all signals in a profile and see which were user-added vs system-suggested | VERIFIED | `profile signals <slug>` CLI command with --type and --status filters, color-coded source display (green=manual, yellow=suggestion, cyan=agent), pending signals marked. ProfileDetail includes signals list with SignalInfo (source, status, added_at, reason). SuggestionService creates signals with source="suggestion" and status="pending". |
| 3 | Every result in a result set includes a structured ranking explanation exposing signal types (query match, seed relation, category overlap, interest profile match, recency) | VERIFIED | RankingPipeline.score_paper returns RankingExplanation with composite_score and signal_breakdown (list of SignalScore). Five SignalType enum values: QUERY_MATCH, SEED_RELATION, CATEGORY_OVERLAP, INTEREST_PROFILE_MATCH, RECENCY. ProfileSearchResult has ranking_explanation field. _display_ranking_explanation in search/cli.py shows per-signal score bars. 30 ranking tests pass. |
| 4 | User can inspect the full ranker inputs for any result set | VERIFIED | RankerSnapshot captures profile_slug, ranker_version, weights, signal_types_applied, seed_paper_count, followed_author_count, negative_example_count, saved_query_count, negative_weight. `--explain` flag on search query/browse commands displays RankerSnapshot via _display_ranker_snapshot. Pipeline.capture_snapshot tested. |

**Score:** 4/4 truths verified

### Required Artifacts

**Plan 01 Artifacts:**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/db/models.py` | InterestProfile and InterestSignal ORM models | VERIFIED | Lines 284-355: Both classes with CHECK constraints (ck_signal_type_valid, ck_signal_status_valid), unique constraint, cascade delete, indexes |
| `src/arxiv_mcp/models/interest.py` | Pydantic schemas for profiles and signals | VERIFIED | 143 lines: SignalInfo, ProfileSummary, ProfileDetail, ProfileCreateRequest, ProfileUpdateRequest, SignalType, SignalScore, RankingExplanation, RankerSnapshot |
| `src/arxiv_mcp/interest/profiles.py` | ProfileService with CRUD and signal management | VERIFIED | 396 lines: Full CRUD (create, list, get, rename, archive, unarchive, delete) + signal management for all 4 types with validation, normalization, provenance |
| `src/arxiv_mcp/interest/signals.py` | Signal validation and author name normalization | VERIFIED | 63 lines: normalize_author, parse_authors, validate_signal with VALID_SIGNAL_TYPES and VALID_SIGNAL_STATUSES |
| `alembic/versions/003_interest_tables.py` | Alembic migration for interest tables | VERIFIED | 77 lines: Creates interest_profiles and interest_signals tables with CHECK constraints, unique constraint, FK, indexes. Downgrade drops both. |
| `tests/test_interest/test_profiles.py` | Integration tests for profile CRUD and signals | VERIFIED | 656 lines (min_lines: 100 met): 42 tests across ORM, constraints, validation, service CRUD, all signal types, soft limits |

**Plan 02 Artifacts:**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/interest/ranking.py` | RankingPipeline with 5 signal scorers | VERIFIED | 555 lines: 5 pure scorer functions, apply_negative_demotion, RankingPipeline class, ProfileContext dataclass, DEFAULT_WEIGHTS |
| `src/arxiv_mcp/interest/search_augment.py` | ProfileRankingService wrapping WorkflowSearchService | VERIFIED | 347 lines: ProfileRankingService with search_papers, browse_recent, _ranked_search, _load_profile_context, _wrap_without_ranking. ProfileSearchResponse defined here. |
| `src/arxiv_mcp/models/paper.py` | ProfileSearchResult extending WorkflowSearchResult | VERIFIED | ProfileSearchResult class with paper, score, triage_state, collection_slugs, ranking_explanation fields |
| `tests/test_interest/test_ranking.py` | Unit and integration tests for ranking | VERIFIED | 680 lines (min_lines: 100 met): 30 tests across 9 test classes covering all scorers, pipeline, snapshot, and service |

**Plan 03 Artifacts:**

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/arxiv_mcp/interest/suggestions.py` | SuggestionService for generation, confirm, dismiss | VERIFIED | 412 lines: SuggestionCandidate, SuggestionService with generate_suggestions, add_suggestions_to_profile, confirm_suggestion, dismiss_suggestion, confirm_suggestions_bulk, internal generators for seeds/queries/authors |
| `src/arxiv_mcp/interest/cli.py` | Click subgroup for profile management | VERIFIED | 618 lines: 19 CLI commands covering CRUD (create, list, show, delete, rename, archive, unarchive), signal management (add-seed, remove-seed, add-query, remove-query, follow, unfollow, add-negative, remove-negative), inspection (signals), and suggestions (suggest, confirm, dismiss) |
| `src/arxiv_mcp/search/cli.py` | Extended search CLI with --profile and --explain | VERIFIED | --profile option on query and browse commands, _get_profile_ranking_service builds full service chain, --explain displays RankerSnapshot, _display_ranking_explanation shows per-signal score bars |
| `tests/test_interest/test_suggestions.py` | Integration tests for suggestion lifecycle | VERIFIED | 449 lines (min_lines: 50 met): 15 tests across 7 test classes |

### Key Link Verification

**Plan 01 Links:**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `interest/profiles.py` | `db/models.py` | InterestProfile and InterestSignal ORM queries | WIRED | Direct imports: `from arxiv_mcp.db.models import InterestProfile, InterestSignal, Paper, SavedQuery`. Queries throughout service methods. |
| `interest/profiles.py` | `models/interest.py` | Returns Pydantic schemas from service methods | WIRED | Imports ProfileDetail, ProfileSummary, SignalInfo. _to_summary, _to_detail, model_validate calls. |
| `tests/test_profiles.py` | `interest/profiles.py` | Tests exercise ProfileService methods | WIRED | 42 tests constructing and calling ProfileService |

**Plan 02 Links:**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `interest/search_augment.py` | `workflow/search_augment.py` | ProfileRankingService wraps WorkflowSearchService | WIRED | Constructor takes workflow_search_service, delegates via self.workflow_search.search_papers / browse_recent |
| `interest/search_augment.py` | `interest/ranking.py` | Uses RankingPipeline to score papers | WIRED | Imports RankingPipeline, ProfileContext, DEFAULT_WEIGHTS. Creates pipeline in _ranked_search, calls score_paper per result. |
| `interest/ranking.py` | `interest/profiles.py` | Loads profile context via ProfileService | WIRED | _load_profile_context in search_augment.py loads from DB (InterestProfile with signals), builds ProfileContext. ProfileService used via CLI path. |

**Plan 03 Links:**

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `interest/suggestions.py` | `db/models.py` | Queries TriageState, SavedQuery, Paper | WIRED | Imports TriageState, SavedQuery, Paper, InterestProfile, InterestSignal. Direct DB queries in _suggest_seed_papers, _suggest_queries, _suggest_authors. |
| `interest/suggestions.py` | `interest/profiles.py` | Uses ProfileService.add_signal | WIRED | Takes ProfileService in constructor, calls profile_service.add_signal in add_suggestions_to_profile. |
| `interest/cli.py` | `interest/profiles.py` | CLI commands invoke ProfileService | WIRED | Every CLI command constructs ProfileService and calls its methods (create_profile, list_profiles, get_profile, etc.) |
| `search/cli.py` | `interest/search_augment.py` | Search uses ProfileRankingService when --profile provided | WIRED | _get_profile_ranking_service builds full chain, search_query and browse_recent call profile_svc.search_papers/browse_recent when profile_slug is set. |
| `cli.py` | `interest/cli.py` | profile_group registered | WIRED | Lines 51-56: try/except import of profile_group, cli.add_command(profile_group) |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| INTR-01 | 03-01 | User can create and manage interest profiles composed of multiple signal types | SATISFIED | ProfileService CRUD + InterestProfile ORM + 42 tests |
| INTR-02 | 03-01 | Interest profiles support seed paper sets as signals | SATISFIED | add_seed_paper/remove_seed_paper with Paper FK validation |
| INTR-03 | 03-01 | Interest profiles support saved queries as signals | SATISFIED | add_saved_query/remove_saved_query with warn-not-error for deleted queries |
| INTR-04 | 03-01 | Interest profiles support followed authors as signals | SATISFIED | add_followed_author/remove_followed_author with normalize_author |
| INTR-05 | 03-01 | Interest profiles support negative examples | SATISFIED | add_negative_example/remove_negative_example + soft demotion in ranking |
| INTR-06 | 03-03 | User can inspect all signals in profile with provenance | SATISFIED | `profile signals` CLI with type/status filters, color-coded source, pending markers. ProfileDetail.signals with SignalInfo provenance fields |
| RANK-01 | 03-02, 03-03 | Results include structured ranking explanations | SATISFIED | RankingExplanation with composite_score + signal_breakdown on every ProfileSearchResult. Displayed inline via _display_ranking_explanation |
| RANK-02 | 03-02, 03-03 | Explanations expose 5 signal types | SATISFIED | SignalType enum: QUERY_MATCH, SEED_RELATION, CATEGORY_OVERLAP, INTEREST_PROFILE_MATCH, RECENCY. All 5 scorers implemented and tested |
| RANK-03 | 03-02, 03-03 | User can inspect ranker inputs for any result set | SATISFIED | RankerSnapshot captured on every ProfileSearchResponse. `--explain` flag displays snapshot in CLI |

**Orphaned requirements:** None. All 9 requirements mapped to Phase 3 in REQUIREMENTS.md are claimed by plans.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `interest/cli.py` | 60 | `pass` in profile_group function body | Info | Standard Click group pattern -- empty body is idiomatic |
| `interest/signals.py` | 34 | `return []` in parse_authors for empty input | Info | Correct guard clause, not a stub |

No TODOs, FIXMEs, placeholders, or stub implementations found in any Phase 3 source files.

### Human Verification Required

### 1. CLI Profile Workflow End-to-End

**Test:** Create a profile, add signals of each type, run `profile signals` to inspect provenance display, then search with `--profile` flag
**Expected:** Rich table shows signals color-coded by source (green=manual), search results show inline ranking explanations with score bars
**Why human:** Visual formatting with Rich tables and score bar visualization cannot be verified programmatically

### 2. Profile-Ranked Search Result Quality

**Test:** Create a profile with seed papers and followed authors, run `search query --profile <slug> --explain` on a populated database
**Expected:** Results re-ranked by composite score, ranking explanations show meaningful signal breakdowns, RankerSnapshot displayed at top
**Why human:** Ranking quality and explanation usefulness require human judgment

### 3. Suggestion Generation from Real Workflow

**Test:** Triage several papers as shortlisted, run `profile suggest <slug>` on a profile
**Expected:** Suggested candidates include papers and authors from shortlisted items with human-readable reasons
**Why human:** Suggestion relevance and reason clarity need human assessment

### Gaps Summary

No gaps found. All 4 success criteria are verified through substantive code inspection:

1. **Interest profiles with multiple signal types:** InterestProfile/InterestSignal ORM models, ProfileService with full CRUD and signal management for all 4 types (seed_paper, saved_query, followed_author, negative_example), 42 integration tests.

2. **Signal inspection with provenance:** ProfileDetail returns signals with provenance (source, status, added_at, reason). CLI `profile signals` command with type/status filtering and color-coded source display.

3. **Structured ranking explanations:** RankingPipeline with 5 composable scorers producing RankingExplanation per result. ProfileSearchResult carries ranking_explanation. CLI displays inline signal breakdowns with score bars. 30 ranking tests.

4. **Ranker input inspection:** RankerSnapshot captures full pipeline state (weights, signal counts, profile info). `--explain` flag on search/browse commands displays snapshot.

All 87 interest tests pass (42 profile + 30 ranking + 15 suggestion). All 9 requirements (INTR-01 through INTR-06, RANK-01 through RANK-03) are satisfied with implementation evidence. No anti-patterns detected. All key links verified as wired.

---

_Verified: 2026-03-10T01:35:00Z_
_Verifier: Claude (gsd-verifier)_
