# Doc 06 Open Question Answers

**Date:** 2026-03-12
**Source:** validation-log.md observations from Phase 05-03 MCP validation session
**Dataset:** 126 arxiv-scan papers, 93 triaged, 13-signal interest profile

---

## Question 1: How much workflow state belongs in v1?

**Answer:** All current workflow tools (triage_paper, add_to_collection, create_watch, add_signal) are validated as useful. Triage and collections are essential for interactive literature review. Watches and signals serve specialized workflows but are still valuable. No workflow tools should be removed from v1.

**Evidence:**
- Observation 2.1: triage_paper was called 15 times during the validation session. State changes succeeded for shortlisted and dismissed. The tool is essential for interactive paper evaluation.
- Observation 2.2: Single-paper triage is the natural unit of interaction during search-then-triage workflows. Batch triage is "nice to have" but not blocking.
- Observation 3.1: add_to_collection with auto-create was used to group shortlisted papers. The workflow (search -> triage -> collect) was natural and complete.
- Observation 7.1: create_watch worked correctly. The two-step internal implementation is hidden behind a clean single-tool interface.
- Observation 6.2: add_signal was used 3 times to augment the profile. Functional but mildly painful for bulk operations.
- Observation C.4: Single-item operations are sufficient for interactive workflows (the common case for MCP agents).

**Implication for MCP surface:** Keep all 9 tools. Consider adding batch_add_signals as a convenience tool for profile bootstrapping, but this is iteration, not v1 scope.

---

## Question 2: Should interest profiles exist before collections, or vice versa?

**Answer:** The ordering does not matter. Profiles and collections serve fundamentally different purposes and are created at different workflow stages. Profiles steer ranking; collections organize papers. They are independent concepts that can be created in any order.

**Evidence:**
- Observation 6.1: The "arxiv-scan-tensions" profile was created during the import phase (before any agent interaction). It existed before any collections were created.
- Observation 3.1: The "validation-test" collection was created during the interactive workflow, after search and triage had identified papers worth grouping.
- Observation 6.3: Profile-ranked search uses the profile to re-rank results. Collections are not involved in ranking. The two features occupy separate concerns.
- Observation C.2: The literature_review_session prompt references both profiles and collections as independent tools. Neither depends on the other being created first.

**Implication for MCP surface:** No sequencing constraint needed. Both can be created independently. The current design (profiles in Phase 3, collections in Phase 2) is correct.

---

## Question 3: Should result sets be explicit persisted objects or ephemeral?

**Answer:** Result sets should remain ephemeral in v1. There is a real need for referencing earlier results, but agents compensate by keeping results in their context window. Persisted result sets add complexity without clear v1 benefit. This should be revisited in v2 if multi-session workflows become a priority.

**Evidence:**
- Observation C.1: During the multi-step literature review, the agent wanted to cross-reference earlier search results with find_related_papers output. Without persistence, results had to be kept in context.
- Observation 4.2: After running find_related_papers with 3 seeds, the merged results were consumed immediately. There was no need to reference them in a later session.
- Observation 1.1: Search results with `total_estimate=None` already make pagination feel blind. Adding result set persistence on top of a system that cannot count results would be premature.
- Practical: The validation session was a single continuous workflow. Ephemeral results worked because the agent's context window contained all needed state. Multi-session workflows (where an agent resumes a literature review across conversations) would benefit from persistence, but that's a v2 scenario.

**Implication for MCP surface:** No result set resource or persistence mechanism needed for v1. Keep results ephemeral. Add a result_set resource in v2 when multi-session agent workflows are validated.

---

## Question 4: Which operations benefit from resources vs tools?

**Answer:** The current hybrid design (Option D) is validated. Tools are correct for actions with parameters (search, triage, add_signal). Resources are correct for stable named objects (paper, collection, profile). The watch resource (watch://slug/deltas) is correctly a resource because it represents a named, readable state.

**Evidence:**
- Observation 1.1: search_papers is clearly a tool -- it requires parameters (query, filters) and returns different results each time. Making it a resource would be wrong.
- Observation 3.2: collection://validation-test is correctly a resource -- it's a named, stable, readable object that an agent references by URI. However, `total_estimate=None` undermines its value for quick status checks.
- Observation 6.1: profile://arxiv-scan-tensions is correctly a resource -- it's a stable named object with inspectable contents (signal list, signal count).
- Observation 4.1: find_related_papers is correctly a tool -- it requires seed IDs and returns computed results.
- Observation 2.1: triage_paper is correctly a tool -- it's a mutation (state change), not a readable object.
- Observation 7.1: create_watch is correctly a tool -- it creates a new named object. The watch resource (for reading deltas) is correctly a resource.
- No observations suggest that any current tool should be a resource or vice versa. The hybrid design is validated.

**Implication for MCP surface:** Keep the current tool/resource split. No reclassification needed.

---

## Question 5: Which prompts are genuinely reusable?

**Answer:** literature_review_session and triage_shortlist are genuinely reusable. daily_digest is useful but requires accumulated state (active watches) that new users may not have. All 3 prompts are "workflow scaffolding" -- useful for onboarding agents to the system but not essential for experienced agents.

**Evidence:**
- Observation C.2: The validation session followed the literature_review_session workflow pattern naturally (search -> triage -> collect -> expand -> enrich). An agent using this prompt would have been guided through the same steps. This prompt is reusable whenever a new research topic is explored.
- Observation C.2: triage_shortlist is reusable whenever a collection has accumulated papers that need evaluation. It provides clear instructions for batch assessment.
- Observation C.2: daily_digest requires active watches. In the validation session, only one watch was created. The prompt would have been trivially short ("1 watch, 0 new papers"). It becomes useful only after a system has been in use for multiple days with active watches and new paper ingestion.
- Observation C.4: None of the prompts transform the workflow -- they guide it. An experienced agent could perform the same tasks without prompts by knowing the tool names and workflow pattern.

**Implication for MCP surface:** Keep all 3 prompts. They serve an important onboarding function. daily_digest may need a minimum watch count check to avoid producing empty guidance. Consider adding a "getting started" prompt for initial system setup (create profile, add signals, set up watches).
