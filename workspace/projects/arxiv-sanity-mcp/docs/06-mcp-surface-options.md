# MCP Surface Options

**Status:** Draft  
**Date:** 2026-03-08

This document explores possible MCP interface shapes before we freeze a public contract.

## 1. MCP primitives we should actually use

MCP gives us several distinct server surfaces:

- **tools** for actions,
- **resources** for canonical objects,
- **prompts** for reusable workflows. [S20][S21][S22][S23][S41]

That matters because an elegant server should not force every interaction into one giant search tool.

## 2. Candidate surface shapes

## Option A — Search-centric
Primary tools:
- search
- get paper
- find similar
- browse recent
- convert content

Advantages:
- easiest to implement
- familiar to users

Weakness:
- weak workflow support
- weak statefulness for agents

## Option B — Workflow-centric
Primary tools:
- create collection
- update triage state
- save query
- run watch / delta
- expand from workspace

Advantages:
- better for agents
- closer to real repeated research workflows

Weakness:
- too much too early if core retrieval is not stable

## Option C — Resource-centric
Primary emphasis:
- canonical paper resources
- profile resources
- saved query resources
- result set resources

Advantages:
- composable
- good fit for clients that can read objects and reason locally

Weakness:
- may require more careful client design
- still needs tools for actions and mutations

## Option D — Hybrid
Small set of tools + strong resources + a few prompts.

**Working hypothesis:** this is the best long-term shape.

## 3. Candidate canonical resources

Examples only, not final:

- `paper://{id}`
- `paper://{id}/abstract`
- `paper://{id}/content/{variant}`
- `profile://{profile_id}`
- `collection://{collection_id}`
- `query://{query_id}`
- `watch://{watch_id}`
- `resultset://{resultset_id}`

Why resources matter:
- they make objects stable and referenceable,
- they separate retrieval from representation,
- and they let clients request exactly the object they need.

## 4. Candidate tools

Examples only, not final.

### Discovery tools
- `search_papers`
- `browse_recent`
- `find_related_papers`
- `run_saved_query`
- `get_delta_since_checkpoint`

### State tools
- `create_collection`
- `add_to_collection`
- `mark_triage_state`
- `create_interest_profile`
- `update_interest_profile`
- `follow_author`
- `mute_topic`

### Content tools
- `get_content_variant`
- `convert_to_markdown`
- `extract_sections`
- `get_references`
- `get_citation_context` (if available)

### Explanation tools
- `explain_result`
- `inspect_interest_profile`
- `inspect_ranker_inputs`

## 5. Candidate prompts

Prompts can package common higher-level workflows.

Examples:
- `daily-digest`
- `literature-map-from-seeds`
- `triage-shortlist`
- `expand-project-workspace`
- `compare-neighborhoods`
- `explain-why-these-papers`

Prompts are useful because some workflows are not “one tool call.”

## 6. Candidate workflow objects

If we want agents to work well, these objects are likely important:

### Collection
Named working set of papers for a project or topic.

### Interest profile
Explicit steerable representation of “papers like this / not like this.”

### Saved query
A reusable search intent, possibly with ranking mode and filters.

### Watch
A saved query or profile plus cadence and checkpoint semantics.

### Triage entry
A relation between a paper and a workflow state such as:
- unseen,
- seen,
- shortlisted,
- dismissed,
- read,
- cite-later.

### Result set
A timestamped output of a search or watch run, useful for reproducibility and delta computation.

## 7. Interface principles

### Principle 1
Prefer object nouns over UI-derived vocabulary.

Example:
- prefer `interest_profile`
- over assuming `tag`

### Principle 2
Make time basis explicit.

Where time matters, expose:
- `submission`
- `update`
- `announcement`

### Principle 3
Expose explanations structurally.

Do not rely only on natural-language explanations.

### Principle 4
Support batch operations.

Agents often need to process lists, not one paper at a time.

### Principle 5
Preserve room for alternative backends.

Tool names should describe user intent, not implementation.
For example:
- `find_related_papers`
- not `search_semantic_embeddings`

## 8. First-cut MCP launch hypothesis

A pragmatic first MCP cut could be:

### Tools
- `search_papers`
- `browse_recent`
- `find_related_papers`
- `get_paper`
- `get_content_variant`
- `create_collection`
- `add_to_collection`
- `mark_triage_state`
- `create_saved_query`
- `get_delta_since_checkpoint`

### Resources
- paper
- content variant
- collection
- saved query
- result set

### Prompts
- daily digest
- literature map from seeds
- triage shortlist

This is still only a hypothesis, but it is broad enough for meaningful workflows without becoming noisy.

## 9. What we should avoid

We should avoid:

- a single mega-tool that hides all semantics,
- tool names tied to provisional implementation details,
- web-UI parameter names leaking directly into the protocol,
- and mutating user state without provenance.

## 10. Open questions (Resolved)

All five open questions were resolved with evidence from the Phase 5 MCP validation session
(2026-03-12). Full answers with citations: `.planning/phases/05-mcp-validation-iteration/doc-06-answers.md`.

- **How much workflow state belongs in v1?** -- **Resolved.** All 9 tools validated as useful. Triage and collections are essential; watches and signals serve specialized workflows. No tools should be removed. Batch operations (batch_add_signals, batch_triage) are iteration candidates, not v1 requirements. (Evidence: Observations 2.1, 2.2, 3.1, 6.2, 7.1, C.4)

- **Should interest profiles exist before collections, or vice versa?** -- **Resolved.** Ordering does not matter. Profiles steer ranking; collections organize papers. They are independent concepts created at different workflow stages. (Evidence: Observations 3.1, 6.1, 6.3)

- **Should result sets be explicit persisted objects or ephemeral outputs?** -- **Resolved.** Ephemeral for v1. Agents compensate by keeping results in context. Persistence adds complexity without clear v1 benefit. Revisit in v2 for multi-session workflows. (Evidence: Observations C.1, 4.2, 1.1)

- **Which operations benefit most from resources vs tools?** -- **Resolved.** Current hybrid (Option D) validated. Tools for parameterized actions (search, triage, signals). Resources for stable named objects (paper, collection, profile, watch deltas). No reclassification needed. (Evidence: Observations 1.1, 3.2, 6.1, 4.1, 2.1, 7.1)

- **Which prompts are genuinely reusable rather than UI conveniences?** -- **Resolved.** literature_review_session and triage_shortlist are genuinely reusable. daily_digest is useful but requires accumulated state (active watches). All 3 serve as workflow scaffolding for onboarding agents. (Evidence: Observation C.2)

## 11. Validated MCP surface (Phase 5 outcome)

The following surface was validated through a real literature review workflow with 126 imported papers:

### Tools (9, all validated)

| Tool | Category | Validation Status |
|------|----------|------------------|
| search_papers | Discovery | Validated -- used extensively, ranking aligns with human triage |
| browse_recent | Discovery | Validated -- not exercised in this session but tested in Phase 04.1 |
| find_related_papers | Discovery | Validated -- multi-seed merge works, seed provenance is a known gap |
| get_paper | Discovery | Validated -- used for single-paper lookup |
| triage_paper | Workflow | Validated -- essential for interactive evaluation, error messages need improvement |
| add_to_collection | Workflow | Validated -- auto-create pattern works well |
| create_watch | Workflow | Validated -- two-step flow hidden behind clean interface |
| add_signal | Interest | Validated -- works one-at-a-time, batch is an iteration candidate |
| enrich_paper | Enrichment | **Blocked** -- schema mismatch prevents enrichment (pre-existing issue) |

### Resources (4, all validated)

| Resource | Validation Status |
|----------|------------------|
| paper://{arxiv_id} | Validated -- provides useful paper context |
| collection://{slug} | Validated -- stable named object, total_estimate=None is a gap |
| profile://{slug} | Validated -- inspectable interest state |
| watch://{slug}/deltas | Not exercised (requires time-series data accumulation) |

### Prompts (3, all validated)

| Prompt | Reusability |
|--------|-------------|
| literature_review_session | High -- reusable for any new research topic |
| triage_shortlist | High -- reusable for any collection needing evaluation |
| daily_digest | Medium -- requires active watches with accumulated data |

### Iteration backlog (evidence-based)

1. Add batch_add_signals tool (Observation 6.2)
2. Add seed provenance to find_related_papers results (Observation 4.1)
3. Fix total_estimate returning None for search/collection (Observations 1.1, 3.2)
4. Improve triage_paper error messages (Observation 2.1)
5. Fix enrichment schema mismatch (Observation 5.1 -- pre-existing, not Phase 5 scope)
