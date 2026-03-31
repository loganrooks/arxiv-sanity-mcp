# Open Questions

**Status:** Open  
**Date:** 2026-03-08

These questions are intentionally unresolved.

## 1. What is the right default notion of interest state?
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: four signal types (seed_paper, saved_query, followed_author, negative_example). Signal type set is now application-validated, not DB-constrained, allowing future extension without migration. See FINDINGS.md I1, I5.

Should the default user-facing abstraction be:
- tags,
- collections,
- seed sets,
- saved queries,
- or a more general profile object?

## 2. What are the minimum workflow objects for MCP v1?
Do we need:
- collections only,
- collections + triage,
- saved queries + watches,
- or full checkpoint / delta semantics immediately?

## 3. What does “related paper” mean in this system?
Should we expose multiple relatedness modes explicitly?
If yes, how many without overwhelming the user?

## 4. Which external enrichments are worth the dependency cost?
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: OpenAlex as sole enrichment source (demand-driven, not bulk). Schema now supports composite PK (arxiv_id, source_api) for multi-source extensibility. See FINDINGS.md I4, I5.

Should OpenAlex be considered core?
Should Semantic Scholar be optional?
Where do Crossref and OpenCitations fit?

## 5. What is the cheapest path to strong “popular” ranking?
Which signals matter most:
- citation velocity,
- GitHub / code activity,
- collection saves,
- watch inclusions,
- other community behavior?

## 6. When should embeddings enter the critical path?
Can we get far enough with:
- lexical + graph,
- then use embeddings only for reranking or selective cohorts?

## 7. What is the right content-normalization contract?
Should the system return:
- plain markdown,
- section-aware markdown,
- markdown + structured JSON,
- TEI/XML,
- or all of the above as content variants?

## 8. What should be cached locally by default?
- metadata only?
- recent content?
- user-touched papers?
- converted markdown?
- embeddings?

## 9. How should hosted/public deployments differ from local/private ones?
What do we disable or restrict in hosted mode for rights reasons?

## 10. What is the smallest MCP surface that still feels powerful?
Where is the boundary between:
- “clean and composable”
- and “too thin for real workflows”?

## 11. How much of the original arxiv-sanity “personality” should be preserved?
What must remain recognizably the same?
What can change radically without losing the soul?

## 12. What is the right first benchmark set?
How do we create a high-quality evaluation asset that covers:
- exact queries,
- exploratory queries,
- seeds,
- deltas,
- and workflow resumption?

## 13. What is the right first implementation language and stack?
What best balances:
- MCP ergonomics,
- performance,
- operational simplicity,
- contributor friendliness,
- and available ecosystem libraries?

## 14. What should never become implicit?
Candidates:
- time basis,
- provenance,
- rights model,
- confidence,
- profile source,
- and explanation signals.

## 16. What is the right processing intensity promotion strategy?
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: demand-driven promotion only (enrich when user/agent touches the paper). Budget-constrained and cohort-based strategies remain viable future options. See FINDINGS.md I5.

Papers can be processed at multiple tiers: metadata-only (free), FTS-indexed (free), OpenAlex-enriched (API call), embedded (GPU), content-parsed (expensive). The question is which papers get promoted to higher tiers and when.

Candidate strategies:
- **Demand-driven**: promote only when a user/agent touches the paper.
- **Cohort-based**: auto-promote recent window to Tier 2, user-touched to Tier 3, saved to Tier 4.
- **Budget-constrained exploration**: daily compute budget allocated by a scoring function balancing recency, category relevance, author overlap, lexical similarity to interests, and an exploration bonus for diversity.
- **Two-phase**: ingest everything at Tier 0-1, build up triage data, train a lightweight relevance classifier, then switch to budget-constrained promotion.

Key sub-questions:
- What is the right daily budget shape? (N enrichments, M embeddings, K conversions, X% exploration)
- Should the budget be a first-class observable configuration object?
- How do you bootstrap the relevance classifier without historical triage data?

## 17. How should retrospective demotion work?

Papers that turn out irrelevant (dismissed, never touched, no citations after N months):
- Soft demotion: keep metadata, drop expensive artifacts (embeddings, parsed content). Recoverable.
- Negative signal: use as negative examples for relevance classifier.
- Never delete metadata — too cheap to worry about.

## 18. How do you discover undervalued papers?

Finding papers that are important but not yet recognized:
- Low-citation, high-similarity to user interests.
- Novel cross-pollination from adjacent categories.
- Author emergence: new authors citing established work.
- Contrarian signals: papers that challenge highly-cited work.
- Serendipity budget: reserve a configurable fraction of recommendations for random exploration outside the interest profile.

This is an experiment-worthy question — the system should support A/B comparison of discovery strategies.

## 15. Which future directions are attractive but dangerous too early?
Examples:
- automatic profile learning,
- heavy online learning,
- full corpus embedding,
- highly opinionated popularity scores,
- generic long-context paper chat.

These are not forbidden.
They are simply not default assumptions.

## 19. How should delegated reviews and external critiques be artifactized by default?

When an agent or external model performs a design review, critique, or evaluation pass, should the output be required to land in a designated artifact rather than only appearing in terminal output?

Sub-questions:
- Should review requests default to a named artifact such as `REVIEW.md`, `CRITIQUE.md`, or a dated file under `.planning/`?
- Should the artifact path be part of the review contract, alongside scope, epistemic schema, and output format?
- How should temporary exploratory reviews differ from durable review artifacts that influence planning decisions?
- If a workflow later becomes a reusable skill, what persistence contract should that skill enforce by default?
