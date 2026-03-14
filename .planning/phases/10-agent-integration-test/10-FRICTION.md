# Phase 10: Friction Report

**Session date:** 2026-03-14
**MCP client:** Claude Code (Opus 4.6) on dionysus
**Corpus:** 126 papers (Phase 5 data)

## Blockers

### B-01: `add_to_collection` leaks raw SQLAlchemy error for non-existent paper

**Description:** When calling `add_to_collection` with a paper ID not in the database, the tool returns a raw SQLAlchemy IntegrityError including the full SQL statement and parameters.

**Expected:** Graceful JSON error like `{"error": "Paper '9999.99999' not found in database"}` (matching `enrich_paper` and `get_paper` behavior).

**Actual:** Raw error: `(sqlalchemy.dialects.postgresql.asyncpg.IntegrityError) ... insert or update on table "collection_papers" violates foreign key constraint ... [SQL: INSERT INTO collection_papers ...]`

**Severity:** Critical — leaks internal SQL, unhelpful to agent, inconsistent with other tools.

**Fix policy:** Fix now.

**Resolution:** Fixed in commit 93feb4c. `add_to_collection` now catches `IntegrityError` and returns `{"error": "Paper 'X' not found in database"}`.

---

## Friction

### F-01: `total_estimate` always null on search results

**Description:** All paginated responses (`search_papers`, `browse_recent`) return `total_estimate: null`.

**Expected:** Approximate count so agent can tell the user "Found ~N papers matching your query".

**Actual:** Always null. Agent cannot provide result count context.

**Severity:** Non-critical — search still works, agent can iterate with pagination.

**Fix policy:** v0.2.0 — requires COUNT query optimization. Known from milestone audit.

**Resolution:** Tracked for v0.2.0 -- requires COUNT query optimization that may impact search latency.

### F-02: `find_related_papers` inconsistent response shape

**Description:** `find_related_papers` returns `{"result": [...]}` (flat array), while `search_papers` and `browse_recent` return `{"results": {"items": [...], "page_info": {...}}}`.

**Expected:** Consistent response shape across all search/discovery tools.

**Actual:** Different shapes require different parsing logic. Agent must handle two formats.

**Severity:** Non-critical — works but confusing for agent reasoning about results.

**Fix policy:** v0.2.0 — breaking change to unify response shapes.

**Resolution:** Tracked for v0.2.0 -- breaking change; requires versioned API or migration path for existing clients.

### F-03: `suggest_signals` returns unbounded list (97 candidates)

**Description:** `suggest_signals` returned 97 candidates with no limit/pagination. This overwhelms agent context and makes it hard to identify the most valuable suggestions.

**Expected:** Top-N suggestions with optional `limit` parameter, or paginated results.

**Actual:** All candidates returned in a single response.

**Severity:** Non-critical — works but wasteful of agent context window.

**Fix policy:** v0.2.0 — add `limit` parameter with sensible default (10-20).

**Resolution:** Tracked for v0.2.0 -- add `limit` parameter with default of 20.

### F-04: MCP resources not discoverable via ListMcpResourcesTool

**Description:** `ListMcpResourcesTool(server="arxiv-discovery")` returns "No resources found" despite 4 resource types being available (watch, profile, collection, paper).

**Expected:** Template-based resources listed with URI patterns so agent knows what's available.

**Actual:** Empty list. Agent must already know URI patterns to access resources.

**Severity:** Non-critical — resources work when accessed directly, but agent can't discover them.

**Fix policy:** v0.2.0 — requires MCP resource template registration. May also be a Claude Code client limitation.

**Resolution:** Tracked for v0.2.0 -- requires MCP resource template registration and may be partially a Claude Code client limitation.

### F-05: `browse_recent` default `time_basis=announced` returns empty for corpus

**Description:** Default `browse_recent` call returns empty results because all papers have `announced_date: null`. Only `time_basis=submitted` works.

**Expected:** Default time_basis works with the data we have, or tool description warns about this.

**Actual:** Silent empty results with default parameters.

**Severity:** Non-critical — workaround exists (`time_basis=submitted`), but default behavior is confusing.

**Fix policy:** Fix now — update tool description to note that `submitted` is recommended when `announced_date` may not be populated.

**Resolution:** Fixed in commit 18f9097. Tool description now notes that `submitted` is recommended when `announced_date` may not be populated.

### F-06: Date-filtered search returns empty (filters on `announced_date`)

**Description:** `search_papers(query="agent", date_from="2026-01-01", date_to="2026-03-01")` returns empty despite papers in that submitted_date range.

**Expected:** Date filters use the most populated date field, or the `time_basis` parameter is available on search.

**Actual:** Empty results. Date filters appear to use `announced_date` (null for all papers).

**Severity:** Non-critical — search without date filters works fine.

**Fix policy:** v0.2.0 — align date filtering with `time_basis` parameter, or default to `submitted_date`.

**Resolution:** Tracked for v0.2.0 -- requires aligning search date filters with `time_basis` parameter.

### F-07: Duplicate watch error uses internal terminology

**Description:** Creating a watch with a name that already exists returns: "Saved query with slug 'philosophy-of-mind' already exists".

**Expected:** Error should say "Watch with name/slug 'philosophy-of-mind' already exists" to match tool terminology.

**Actual:** Uses internal "Saved query" concept that doesn't appear in tool descriptions.

**Severity:** Non-critical — error is understandable but inconsistent.

**Fix policy:** Fix now — simple string change.

**Resolution:** Fixed in commit 93feb4c. `create_watch` now catches ValueError and replaces "Saved query" with "Watch" in error message.

### F-08: Content variant errors don't distinguish "not fetched" from "unavailable"

**Description:** `get_content_variant` with `best`, `html`, or `pdf_markdown` all return similar generic errors that don't tell the agent what action could resolve them.

**Expected:** Different messages: "HTML content not yet fetched — try `enrich_paper` first" vs "HTML not available for this paper".

**Actual:** "No content variant available" (generic) or "HTML variant not available" (slightly better but still doesn't explain why).

**Severity:** Non-critical — abstract variant always works as fallback.

**Fix policy:** v0.2.0 — improve error messages with actionable guidance.

**Resolution:** Tracked for v0.2.0 -- requires distinguishing "not fetched yet" from "unavailable" states in content service.

### F-09: Title-only search returns `score: null`

**Description:** `search_papers(title="memory")` returns results but all have `score: null`.

**Expected:** Relevance scores for all search result types.

**Actual:** Title-only search doesn't produce scores. Agent can't rank results.

**Severity:** Non-critical — results are still returned, just unranked.

**Fix policy:** v0.2.0 — title search uses different code path that doesn't produce scores.

**Resolution:** Tracked for v0.2.0 -- title search uses ILIKE path that doesn't produce ts_rank scores.

### F-10: `enrich_paper` response includes duplicative `raw_response`

**Description:** `enrich_paper` returns both structured fields (topics, cited_by_count, etc.) AND a full `raw_response` that duplicates all of it plus more. The raw_response for one paper was ~4KB of JSON.

**Expected:** Only structured fields, or `raw_response` behind an opt-in parameter.

**Actual:** Always included, consuming agent context budget.

**Severity:** Non-critical — data is correct, just verbose.

**Fix policy:** v0.2.0 — consider removing `raw_response` or making it opt-in.

**Resolution:** Tracked for v0.2.0 -- add `include_raw` parameter (default false) or remove `raw_response` entirely.

### F-11: MCP prompts not invocable from Claude Code client

**Description:** Server implements 3 MCP prompts (literature_review_session, daily_digest, triage_shortlist) but Claude Code has no UI to list or invoke them.

**Expected:** Agent can discover and use prompts.

**Actual:** Prompts exist but are inaccessible. This is a Claude Code client limitation.

**Severity:** Non-critical — tools work without prompts, prompts are optional workflow guidance.

**Fix policy:** v0.2.0 — track Claude Code prompt support; consider exposing prompt content as a tool.

**Resolution:** Tracked for v0.2.0 -- Claude Code client limitation. Consider exposing prompt content as a `get_workflow_guide` tool.

## Ergonomic

### E-01: Invalid category silently returns empty results

**Description:** `search_papers(query="agent", category="cs.INVALID")` returns empty results without warning that the category doesn't exist.

**Expected:** Warning or error: "Category 'cs.INVALID' not recognized."

**Actual:** Silent empty results.

**Fix policy:** v0.2.0

**Resolution:** Tracked for v0.2.0 -- add category validation with known arXiv category list.

### E-02: `add_to_collection` duplicate returns `added: true`

**Description:** Adding a paper that's already in a collection returns `added: true` without indicating it was already present.

**Expected:** Response like `{"added": false, "already_present": true}` or `{"added": true, "was_duplicate": true}`.

**Actual:** `{"added": true}` regardless — idempotent but misleading.

**Fix policy:** v0.2.0

**Resolution:** Tracked for v0.2.0 -- return `already_present` field when paper is already in collection.

### E-03: `find_related_papers` error handling differs from other tools

**Description:** `find_related_papers` with a non-existent seed raises an MCP-level error (stack trace) rather than returning a JSON error object.

**Expected:** `{"error": "Seed paper not found: 9999.99999"}` (JSON object like other tools).

**Actual:** `Error executing tool find_related_papers: Seed paper not found: 9999.99999` (MCP-level exception).

**Fix policy:** v0.2.0 — wrap in try/catch to return JSON error.

**Resolution:** Tracked for v0.2.0 -- wrap in try/catch to return JSON error consistent with other tools.

## Known Issues from Milestone Audit (Confirmed)

- **total_estimate: None** — Confirmed in F-01. All paginated responses have null total_estimate.
- **find_related_papers lacks workflow enrichment** — Confirmed. Related papers response has no triage_state or collection_slugs (inconsistent with search_papers).
- **triage_paper "unseen" confusion** — Not reproduced. Triage state transitions all work correctly including reset to "unseen".

## Summary

- **Total issues found:** 15
- **Blockers:** 1 (1 fixed, 0 unresolved)
- **Friction:** 11 (3 fixed, 8 deferred to v0.2.0)
- **Ergonomic:** 3 (all v0.2.0)
- **Critical fixes applied:** 3 commits with fix(10): prefix
  - `93feb4c` -- B-01: add_to_collection IntegrityError catch + F-07: create_watch error terminology
  - `18f9097` -- F-05: browse_recent description updated
  - `f68fef8` -- README setup instructions corrected
