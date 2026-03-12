# MCP Validation Session Log

**Date:** 2026-03-12
**Dataset:** arxiv-scan pipeline (126/157 papers imported, 93 triaged, 10-signal interest profile)
**Session type:** Programmatic MCP tool/service validation against live PostgreSQL database

---

## Import Summary

- **Papers fetched:** 126 of 157 (31 failed with 429 rate limiting from arXiv API)
- **Triage states set:** 93 (shortlisted; remaining papers hit FK violations due to missing paper records)
- **Interest profile:** Created "arxiv-scan-tensions" with 10 tension vocabulary signals
- **Pre-existing bug fixed:** arXiv API URL was HTTP, arXiv now requires HTTPS (301 redirect broke httpx)
- **False-negative papers:** None of the 4 false negatives (2501.11733, 2501.11425, 2510.23595, 2506.24119) were imported due to 429 errors

---

## Phase 1: Search

### Observation 1.1: Multi-query search works well
- **Action:** Ran 5 search queries: "multi-agent", "self-reflection", "memory systems", "autonomous agent", "tool use"
- **Tool used:** search_papers (SearchService.search_papers)
- **Result:** All queries returned 10 results with relevance scores. "multi-agent" returned the strongest matches (scores 1.8-2.2). "self-reflection" returned lower-relevance results (scores 0.2), as expected for a term less central to the corpus.
- **Friction:** `total_estimate` is always `None` for search results. An agent cannot know how many total results exist -- pagination feels blind.
- **Doc 06 relevance:** Q4 (resources vs tools) -- search is clearly a tool operation (action with parameters), not a resource.

### Observation 1.2: Search ranking aligns with imported triage states
- **Action:** Compared search results against known triage states from import
- **Tool used:** search_papers
- **Result:** Top-ranked search results for "multi-agent" (2508.13167, 2504.09772, 2512.11213) are papers that were shortlisted in the import (value >= 7). The lexical ranking broadly agrees with human triage decisions.
- **Friction:** No way to see triage state inline with search results through the MCP search tool. The agent must call get_paper or read paper://ID separately for each result to discover its triage state.
- **Doc 06 relevance:** Q1 (workflow state in v1) -- triage state is valuable context during search but not exposed in search results via MCP tools.

---

## Phase 2: Triage

### Observation 2.1: Triage works for state changes but fails on re-triaging some papers
- **Action:** Triaged 15 papers from multi-agent search results: 5 shortlisted, 5 seen, 5 dismissed
- **Tool used:** triage_paper (TriageService.mark_triage)
- **Result:** "shortlisted" and "dismissed" state changes succeeded. Some "seen" state changes failed with IntegrityError (FK violation on triage_log).
- **Friction:** The error from mark_triage is an opaque database exception, not a clear user-facing message. An agent seeing `sqlalchemy.dialects.postgresql.asyncpg.IntegrityError` cannot diagnose the problem.
- **Doc 06 relevance:** Q1 (workflow state) -- triage_paper works and is essential. The error handling needs improvement but the tool concept is validated.

### Observation 2.2: Single-paper triage is natural for agent workflows
- **Action:** Triaged papers one at a time after reviewing search results
- **Tool used:** triage_paper
- **Result:** The workflow felt natural: search -> review -> triage. One call per paper is fine when triaging during interactive review.
- **Friction:** When bulk-triaging (e.g., dismissing the bottom 5 results), calling triage_paper 5 times feels repetitive. A batch_triage accepting `[{arxiv_id, state}]` would reduce friction for bulk operations. However, this is a "nice to have" -- single-paper triage is the common case.
- **Doc 06 relevance:** Q1 (workflow state) -- triage is used and valuable. Batch would help but isn't blocking.

---

## Phase 3: Collections

### Observation 3.1: add_to_collection auto-creates collection smoothly
- **Action:** Created "validation-test" collection and added 5 shortlisted papers
- **Tool used:** add_to_collection (CollectionService.create_collection + add_papers)
- **Result:** Collection created, 5 papers added. Auto-creation on first use (idempotent) works well.
- **Friction:** None -- the auto-create pattern is clean. The agent doesn't need to know whether the collection exists.
- **Doc 06 relevance:** Q2 (profiles vs collections ordering) -- collections were created AFTER search and triage, as a natural grouping step. They serve a different purpose than profiles: collections organize papers, profiles steer ranking. The ordering doesn't matter because they're independent concepts.

### Observation 3.2: Collection resource read provides useful context
- **Action:** Read collection://validation-test to see its contents
- **Tool used:** collection resource (CollectionService.show_collection)
- **Result:** Returned list of papers with titles. `total_estimate` was None.
- **Friction:** `total_estimate` is None for collections too. An agent cannot quickly learn "how many papers are in this collection?" without counting the items array.
- **Doc 06 relevance:** Q4 (resources vs tools) -- collection is a good resource (named, stable, readable). But `total_estimate` being None undermines the resource's value as a quick status check.

---

## Phase 4: Expand (find_related_papers)

### Observation 4.1: Single-seed related papers works well
- **Action:** Called find_related_papers for 3 seed papers
- **Tool used:** find_related_papers (SearchService.find_related_papers)
- **Result:** Each seed returned 10 related papers with relevance scores (4.0-8.4 range). Results are lexically related and make sense thematically.
- **Friction:** No indication which seed produced which result. When reviewing related results from multiple seeds, the agent cannot tell "this paper was related to seed X" vs "this paper was related to seed Y."
- **Doc 06 relevance:** Q4 (resources vs tools) -- find_related_papers is clearly a tool (parameterized action). The lack of provenance (seed->result mapping) is a friction point.

### Observation 4.2: Multi-seed merge deduplicates correctly
- **Action:** Called find_related_papers with 3 seed IDs, merged and deduplicated
- **Tool used:** find_related_papers (MCP tool with list[str] input)
- **Result:** 15 unique results after deduplication, sorted by highest score. Seed IDs correctly excluded from results.
- **Friction:** The merged results lose seed provenance entirely. For a literature review, knowing "paper X was suggested because of seed Y" is valuable for understanding why a paper appeared.
- **Doc 06 relevance:** Q3 (result set persistence) -- after running find_related_papers, the results are ephemeral. If the agent wants to refer back to "the related papers I found earlier," it has no mechanism to do so. The agent must re-run the query or keep results in its context window.

### Observation 4.3: False-negative surfacing test inconclusive
- **Action:** Checked whether false-negative papers appeared in related results
- **Tool used:** find_related_papers
- **Result:** None of the 4 false-negative papers appeared. However, they were never imported into the database (429 errors during import), so this test is inconclusive -- not a failure of the ranking, just missing data.
- **Friction:** N/A -- data limitation, not tool limitation.
- **Doc 06 relevance:** N/A

---

## Phase 5: Enrichment

### Observation 5.1: Enrichment fails due to schema mismatch
- **Action:** Called enrich_paper for 3 papers
- **Tool used:** enrich_paper (EnrichmentService.enrich_paper)
- **Result:** All 3 failed with `InvalidColumnReferenceError: there is no unique or exclusion constraint matching the ON CONFLICT specification`. The enrichment service expects a composite PK on (arxiv_id, source_api) but the DB schema has only arxiv_id as PK.
- **Friction:** Enrichment is completely broken against the live database. The schema migration for composite PK was never applied. This is a pre-existing issue from Quick Task 1 that changed the code but not the migration.
- **Doc 06 relevance:** Q1 (workflow state) -- enrichment is a core workflow step but is currently non-functional due to schema drift. Must be fixed before enrichment can be validated.

---

## Phase 6: Interest Profile

### Observation 6.1: Profile exists with correct tension signals
- **Action:** Read the "arxiv-scan-tensions" profile created by the import
- **Tool used:** profile resource (ProfileService.get_profile)
- **Result:** Profile has 13 signals (10 original tensions + 3 added during validation: 2 seed_papers + 1 followed_author).
- **Friction:** None -- profile read works well.
- **Doc 06 relevance:** Q2 (profiles vs collections) -- profiles were created during import (before any agent interaction). Collections were created during the workflow. Both serve different purposes. Ordering is irrelevant.

### Observation 6.2: add_signal one-at-a-time is mildly painful
- **Action:** Added 3 new signals to the profile (2 seed_paper, 1 followed_author)
- **Tool used:** add_signal (ProfileService.add_signal)
- **Result:** All 3 signals added successfully. Each required a separate MCP tool call.
- **Friction:** For adding 3 signals, 3 calls is tolerable. For initializing a profile with 10+ signals (as the import script does), a batch operation would be significantly more efficient. An agent bootstrapping a new profile would benefit from batch_add_signals.
- **Doc 06 relevance:** Q1 (workflow state) -- add_signal is used and needed. Batch is a valid iteration candidate but not blocking.

### Observation 6.3: Profile-ranked search works but sparse query results limit utility
- **Action:** Ran profile-ranked search with "arxiv-scan-tensions" profile for "multi-agent autonomy"
- **Tool used:** ProfileRankingService.search_papers
- **Result:** Only 2 results returned (vs 10 for plain search with "multi-agent"). The compound query "multi-agent autonomy" matched very few papers in the 126-paper corpus.
- **Friction:** The profile ranking service over-fetches 3x but the base query returned very few results. The utility of profile ranking depends on having a large enough corpus. With 126 papers, most queries return sparse results.
- **Doc 06 relevance:** Q4 (resources vs tools) -- profile is a good resource. Profile-ranked search is a valid tool. The limitation is corpus size, not tool design.

---

## Phase 7: Watch and Delta

### Observation 7.1: create_watch two-step flow works but is hidden
- **Action:** Created a watch "agent-memory-watch" for query "agent memory systems"
- **Tool used:** create_watch (SavedQueryService.create_saved_query + WatchService.promote_to_watch)
- **Result:** Watch created successfully via the MCP create_watch tool (which wraps both steps internally).
- **Friction:** From the MCP agent perspective, create_watch is a single tool call -- the two-step nature is hidden. This is good design. The CONTEXT.md concern about "two-step friction" is already mitigated by the tool wrapper.
- **Doc 06 relevance:** Q1 (workflow state) -- watches work and the tool design is clean. No iteration needed.

---

## Cross-cutting Observations

### Observation C.1: Result set persistence would help agent workflows
- **Action:** After running multiple searches and find_related_papers, wanted to cross-reference earlier results
- **Friction:** Search results are ephemeral. The agent must keep all results in its context window or re-run queries. For a multi-step literature review, this means the agent's context fills up with raw search results rather than being able to reference "result set from search #3."
- **Doc 06 relevance:** Q3 (result set persistence) -- there IS a real need for lightweight result set persistence (or at least result set naming), but it's not blocking for v1. Agents compensate by keeping results in context.

### Observation C.2: Prompts would guide but not transform the workflow
- **Action:** Reflected on whether the 3 prompts (literature_review_session, daily_digest, triage_shortlist) would have helped
- **Result:** literature_review_session would have provided useful step-by-step guidance for an agent new to the system. daily_digest is useful only with active watches. triage_shortlist is useful for batch evaluation.
- **Friction:** The prompts are workflow scaffolding, not essential tools. An experienced agent could perform the same workflow without prompts. They are most useful for onboarding new agents to the system.
- **Doc 06 relevance:** Q5 (prompt reusability) -- literature_review_session and triage_shortlist are genuinely reusable. daily_digest is less reusable (requires active watches, which requires accumulated state). All 3 are useful but not essential.

### Observation C.3: triage_paper error messages need improvement
- **Action:** Observed opaque database exceptions when triage operations fail
- **Friction:** Agents see raw SQLAlchemy IntegrityError traces instead of actionable messages like "Paper not found in database" or "Invalid triage state transition."
- **Doc 06 relevance:** Q1 (workflow state) -- the tool works but error UX is poor.

### Observation C.4: Batch operations (triage, signals) are "nice to have" not blocking
- **Action:** Evaluated friction of single-item operations across the session
- **Result:** Single-item operations (triage_paper, add_signal) are fine for interactive workflows (1-5 items). Batch operations become desirable only for bulk operations (10+ items). Since MCP agents typically work interactively, single-item operations are sufficient for v1.
- **Doc 06 relevance:** Q1 (workflow state) -- batch is an iteration candidate, not a v1 requirement.

---

## Summary of Friction Points (ranked by impact)

1. **Enrichment broken** (schema mismatch) -- blocks entire enrichment workflow
2. **total_estimate always None** -- agents cannot gauge result set sizes
3. **No seed provenance in find_related_papers** -- agents cannot trace why a paper was suggested
4. **Opaque error messages from triage** -- agents cannot diagnose failures
5. **add_signal one-at-a-time** -- mild friction for profile bootstrapping
6. **No result set persistence** -- agents must keep results in context
7. **Batch triage missing** -- mild friction for bulk operations

## Iteration Candidates (evidence-based)

1. **Add batch_add_signals tool** -- Observation 6.2: adding 3+ signals requires 3+ calls
2. **Add seed provenance to find_related_papers** -- Observation 4.1: no way to trace seed-to-result
3. **Fix total_estimate** -- Observations 1.1, 3.2: always None, agents cannot gauge sizes
4. **Improve error messages** -- Observation 2.1: opaque DB exceptions
