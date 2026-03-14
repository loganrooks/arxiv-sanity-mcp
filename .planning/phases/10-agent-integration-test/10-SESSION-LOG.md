# Phase 10: Agent Research Session Log

**Session date:** 2026-03-14
**MCP client:** Claude Code (Opus 4.6) on dionysus
**Database:** arxiv_mcp (Phase 5 corpus, 126 papers)
**Server config:** ~/.claude.json (local scope, via `claude mcp add-json --scope local`)
**Transport:** stdio, absolute venv Python path, explicit DATABASE_URL

## Flow 1: Literature Review (search -> triage -> collect)

**Prompt intent:** Find papers about agent memory, triage them, organize into a collection.

### Steps executed:
1. `search_papers(query="agent memory", page_size=5)` — Returned 5 results with relevance scores, triage states, collection_slugs. Top result: "Memory in the Age of AI Agents" (2512.13564, score 1.96).
2. `triage_paper(arxiv_id="2512.13564", state="shortlisted")` — Success, `updated: true`.
3. `triage_paper(arxiv_id="2501.13956", state="dismissed")` — Success, `updated: true`.
4. `add_to_collection(arxiv_id="2512.13564", collection_name="Agent Memory Survey")` — Collection auto-created with slug `agent-memory-survey`. `added: true`.
5. `add_to_collection(arxiv_id="2601.01885", collection_name="Agent Memory Survey")` — Added to existing collection. `added: true`.
6. Pagination: `search_papers(query="agent memory", cursor=...)` — Page 2 returned 5 more results.
7. `find_related_papers(seed_arxiv_ids="2512.13564", page_size=3)` — Returned 3 related papers via lexical similarity.

### Observations:
- Agent correctly discovered and used `search_papers`, `triage_paper`, `add_to_collection`, `find_related_papers`.
- Collection auto-creation from name is ergonomic — no need to create separately.
- `find_related_papers` response shape differs from `search_papers` (flat `result` array vs `results.items` + `page_info`).
- `total_estimate: null` on all paginated results — can't report "Found N papers".

### Verdict: **PASS** — Full workflow completed.

## Flow 2: Interest-Driven Discovery (profile-ranked search)

**Prompt intent:** Use interest profile to rank search results with explanations.

### Steps executed:
1. `search_papers(query="reinforcement learning", profile_slug="arxiv-scan-tensions", page_size=3)` — Returned 3 results with full `ranking_explanation` per paper and `ranker_snapshot`.
2. `suggest_signals(profile_slug="arxiv-scan-tensions")` — Returned 97 candidates (8 authors, 89 seed papers).
3. `add_signal(profile_slug="arxiv-scan-tensions", signal_type="followed_author", signal_value="xingyao wang")` — Added successfully.
4. `search_papers(query="agent", profile_slug="test-profile", page_size=3)` — Newly created profile with 1 seed + 1 author correctly boosted matching papers (`seed_relation: author_match=1.000`).

### Observations:
- Ranking explanations are detailed: composite score, per-signal breakdown, weights, normalization.
- `ranker_snapshot` provides good debugging context (profile metadata, weight config).
- `suggest_signals` returned 97 unbounded candidates — overwhelming for agent context. No `limit` or `max_results` parameter.
- Profile signals include philosophical concepts stored as `followed_author` type (import artifact, not a code bug).

### Verdict: **PASS** — Profile ranking works, explanations are informative.

## Flow 3: Watch/Delta Monitoring

**Prompt intent:** Set up monitoring for new papers, check for updates.

### Steps executed:
1. `create_watch(name="Philosophy of Mind", query="philosophy of mind", category="cs.AI")` — Created with slug `philosophy-of-mind`, cadence `daily`.
2. `ReadMcpResource(uri="watch://philosophy-of-mind/deltas")` — Returned empty items (expected for new watch).
3. `ReadMcpResource(uri="profile://arxiv-scan-tensions")` — Full profile with 14 signals returned.
4. `ReadMcpResource(uri="collection://agent-memory-survey")` — 2 papers with triage states returned.
5. Duplicate `create_watch(name="Philosophy of Mind")` — Error: "Saved query with slug 'philosophy-of-mind' already exists".

### Observations:
- Watch creation works cleanly with auto-slug generation.
- MCP resources work when accessed by URI, but `ListMcpResourcesTool` returns empty — template-based URIs not discoverable.
- Duplicate watch error uses internal terminology "Saved query" instead of "watch".
- Resources return JSON as text/plain — functional but not typed.

### Verdict: **PASS with friction** — Workflow works but resource discoverability is poor.

## Flow 4: Content Access

**Prompt intent:** Get full content for a paper beyond the abstract.

### Steps executed:
1. `get_content_variant(arxiv_id="2512.13564", variant="best")` — Error: "No content variant available".
2. `get_content_variant(arxiv_id="2512.13564", variant="abstract")` — Full abstract returned with provenance metadata (extraction_method, content_hash).
3. `get_content_variant(arxiv_id="2512.13564", variant="html")` — Error: "HTML variant not available".
4. `get_content_variant(arxiv_id="2512.13564", variant="pdf_markdown")` — Error: "No content variant available".
5. `enrich_paper(arxiv_id="2512.13564")` — OpenAlex enrichment returned (DOI, topics, cited_by_count, full authorships).

### Observations:
- Abstract variant always works from metadata — good fallback.
- `best` variant error doesn't explain what's needed (fetch HTML? download PDF?). Error message indistinguishable from html/pdf_markdown errors.
- `enrich_paper` response includes massive `raw_response` that duplicates structured fields above it.
- Enrichment topics included "Ferroelectric and Negative Capacitance Devices" — OpenAlex misclassification, not our bug.

### Verdict: **PASS with friction** — Abstract and enrichment work; non-abstract content variants not available (Phase 6 scope).

## Flow 5: Prompt-Guided

**Prompt intent:** Use MCP prompts to guide workflow.

### Steps executed:
1. Reviewed prompt code: 3 prompts exist (`literature_review_session`, `daily_digest`, `triage_shortlist`).
2. `ListMcpResourcesTool(server="arxiv-discovery")` — No resources listed (same discoverability issue).
3. Claude Code client has no built-in mechanism to list or invoke MCP prompts.

### Observations:
- Prompts are well-designed with structured workflow instructions and parameter support.
- MCP prompt protocol support in Claude Code is limited — prompts can't be discovered or invoked.
- This is a client-side ecosystem limitation, not a server bug.

### Verdict: **BLOCKED by client** — Server implements prompts correctly but Claude Code doesn't expose them.

## Edge Case Testing

### Error handling (all passed):
- Non-existent paper (`get_paper`, `enrich_paper`): Clear error messages.
- Invalid triage state: Lists all valid states in error.
- Non-existent profile: Clear "not found" error.
- Empty query: Returns empty results (no crash).
- Very long natural language query: Returns empty (lexical search limitation).

### Error handling (failures):
- `add_to_collection` with non-existent paper: **Leaks raw SQLAlchemy error** with SQL query and parameters.
- `find_related_papers` with non-existent seed: Error raised at MCP level (not graceful JSON error).

### Idempotency:
- Duplicate `add_to_collection`: Returns `added: true` (doesn't indicate already present).
- Duplicate `create_watch`: Error with internal terminology.

### Batch operations:
- `batch_add_signals` with partial failure: Graceful — returns per-signal results with error detail. Excellent.

### Date filtering:
- `search_papers` with `date_from`/`date_to`: Returns empty — filters on `announced_date` (null for all papers).
- `browse_recent(time_basis="submitted")`: Works correctly when using submitted date.

### Scoring:
- Title-only search: `score: null` for all results (no relevance ranking).
- `browse_recent` without profile: `score: null` (expected, chronological order).

## Summary

- **Flows completed:** 4/5 (Flow 5 blocked by client)
- **Tools exercised:** search_papers, browse_recent, find_related_papers, get_paper, triage_paper, add_to_collection, create_watch, add_signal, batch_add_signals, suggest_signals, create_profile, enrich_paper, get_content_variant (13/13)
- **Resources exercised:** watch://deltas, profile://, collection:// (3/4 — paper:// not tested)
- **Agent autonomy:** Tool descriptions were clear enough for natural discovery. No confusion about which tool to use for each task.
- **Critical issues:** 1 blocker (raw SQL leak), 11 friction points, 3 ergonomic items.
