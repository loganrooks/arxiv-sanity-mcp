# Phase 3: Interest Modeling & Ranking - Context

**Gathered:** 2026-03-09
**Status:** Ready for planning
**Source:** Inferred from Phase 1-2 context, ADRs, codebase patterns, and project principles

<domain>
## Phase Boundary

Users can build explicit interest profiles from multiple signal types (seed papers, saved queries, followed authors, negative examples) and get structured ranking explanations for every result. This phase builds on the Phase 1 metadata substrate (search, browse, related) and Phase 2 workflow state (collections, triage, saved queries). No enrichment data, no MCP server, no semantic/vector search yet — ranking uses lexical signals, metadata overlap, and workflow-derived interest signals only.

</domain>

<decisions>
## Implementation Decisions

### Interest profile semantics
- Named profiles with slug-style identifiers (same convention as collections and saved queries)
- Multiple profiles allowed per user — different research threads get separate profiles (e.g., "attention-mechanisms", "philosophy-of-ai")
- Profiles are explicit and user-controlled: every signal is user-added or system-suggested-then-confirmed (no implicit learning, per Out of Scope: "Automatic profile adjustment")
- Profile is a container of typed signals, not a single vector or embedding
- Empty profile is valid (degrades gracefully to unranked/lexical-only results)
- Profiles renamable after creation
- Profiles support archive (same pattern as collections: hidden from default listing, queryable with flag)

### Signal types and storage
- Four signal types as specified: seed_papers, saved_queries, followed_authors, negative_examples
- Each signal records provenance: source ("manual", "suggestion", "agent"), added_at timestamp, optional reason/note
- Seed papers: list of arxiv_ids (FK to Paper) — represent "papers like this"
- Saved queries: list of saved_query slugs (FK to SavedQuery) — represent "topics I care about"
- Followed authors: list of author name strings (not FK — arXiv has no author entity table; store normalized name strings) — represent "people whose work I follow"
- Negative examples: list of arxiv_ids (FK to Paper) — represent "not like this" (soft demotion, NOT hard exclusion)
- System-suggested signals: derived from workflow activity (triage shortlists → seed candidates, frequent queries → query signal candidates, authors of saved papers → follow candidates) — BUT always surface as suggestions requiring user confirmation before activation
- Suggestion mechanism is advisory: generate candidates, present to user, user confirms/rejects — never auto-activate

### Signal inspection and provenance (INTR-06)
- Every signal in a profile is individually inspectable: type, value, source (user-added vs system-suggested), added_at, reason
- Profiles expose signal counts by type and by source
- System-suggested signals that are pending confirmation are visually distinct from active signals
- Suggestion history: track what was suggested even if rejected (avoids re-suggesting dismissed items)

### Negative example behavior
- Negative examples are soft demotions, not hard filters — papers similar to negatives get score penalties but are never fully hidden
- Rationale: hard exclusion violates exploration-first (ADR-0001) — user might miss serendipitous connections
- Negative weight is configurable per-profile (default: moderate demotion, not aggressive)
- A paper that matches both a positive seed and a negative example: net effect depends on signal strengths, not a simple cancel-out

### Ranking architecture (RANK-01, RANK-02, RANK-03)
- Ranking is a composable pipeline, not a monolithic scorer — consistent with ADR-0001 (multiple retrieval/ranking strategies coexist)
- Current lexical ranking (ts_rank_cd) becomes one signal among several
- Signal types for ranking explanations: query_match (lexical relevance), seed_relation (similarity to seed papers), category_overlap (shared categories with profile seeds), interest_profile_match (composite profile affinity), recency (how recent the paper is)
- Each signal produces a normalized sub-score [0.0, 1.0] and a human-readable explanation fragment
- Final composite score combines sub-scores with configurable weights — but the sub-scores and their explanations are always preserved (never reduced to a single opaque number)
- Default weight profile ships with sensible defaults; user can adjust weights per profile (optional, not required for v1)
- Ranking without a profile: falls back to current behavior (lexical + recency) with explanation showing only those signals

### Ranking explanation structure (RANK-01, RANK-02)
- Every result in a ranked result set includes a RankingExplanation object
- RankingExplanation contains: composite_score (float), signal_breakdown (list of SignalScore), ranker_version (string for reproducibility)
- SignalScore: signal_type (enum), raw_score (float), normalized_score (float), weight (float), weighted_score (float), explanation (human-readable string, e.g., "Strong title match on 'transformer attention'", "Shares 3 categories with seed paper 2301.12345")
- Explanations are generated at query time, not stored (computed, not cached — avoids stale explanations when profiles change)

### Result set inspection (RANK-03)
- "Inspect ranker inputs" means: for a given result set, user can see the full ranker configuration that produced it — which profile was active, what weights were used, what signals existed at query time
- This is a snapshot: captured at query time and available for the lifetime of the paginated result set
- Implementation: encode ranker config into cursor metadata or return as top-level field on PaginatedResponse

### Profile-aware search integration
- Extend the WorkflowSearchService composition pattern (not modify Phase 1 SearchService)
- New: ProfileRankingService wraps WorkflowSearchService, applies profile-aware re-ranking as post-processing
- Flow: SearchService → WorkflowSearchService (adds triage/collection context) → ProfileRankingService (applies profile ranking + explanations)
- Profile is optional parameter on search/browse — if omitted, no profile ranking applied (backward compatible)
- find_related_papers gains profile context: seed relation scoring uses profile seeds in addition to the explicitly provided seed paper

### Suggestion generation
- Suggestions are batch-generated on demand (not continuous background process) — e.g., "suggest signals for profile X"
- Sources for suggestions:
  - Papers with triage state "shortlisted" or "cite-later" → seed paper candidates
  - Saved queries with high run_count → query signal candidates
  - Authors appearing 3+ times in shortlisted/cite-later papers → follow candidates
- Suggestions include explanation of why they were suggested ("You shortlisted 4 papers by this author", "This query has been run 12 times")
- User confirms individually or in bulk (same batch pattern as triage)

### CLI structure
- `arxiv-mcp profile create/list/show/delete/rename/archive/unarchive` — profile CRUD
- `arxiv-mcp profile add-seed/remove-seed <profile> <arxiv_id...>` — seed paper signals
- `arxiv-mcp profile add-query/remove-query <profile> <query_slug...>` — saved query signals
- `arxiv-mcp profile follow/unfollow <profile> <author_name...>` — author signals
- `arxiv-mcp profile add-negative/remove-negative <profile> <arxiv_id...>` — negative examples
- `arxiv-mcp profile signals <profile>` — inspect all signals with provenance
- `arxiv-mcp profile suggest <profile>` — generate and display suggestions
- `arxiv-mcp profile confirm <profile> <signal_id...>` — confirm pending suggestions
- `arxiv-mcp profile dismiss <profile> <signal_id...>` — reject suggestions
- Search/browse commands gain `--profile <slug>` flag to activate profile-aware ranking
- `arxiv-mcp search papers --profile my-profile` → results include RankingExplanation
- `arxiv-mcp search explain <result_set_id>` or inline `--explain` flag for detailed ranker input inspection

### Phase 4+ anticipation
- Ranking pipeline is extensible: enrichment signals (citation count, FWCI, topics from OpenAlex) slot in as additional SignalScore types without restructuring
- Category overlap scoring uses Paper.category_list (already GIN-indexed) — no new indices needed for this signal
- Seed relation scoring uses existing lexical similarity (build_related_query pattern) — when semantic embeddings arrive in v2, they plug into the same signal slot
- Interest profiles become the primary input for Phase 6 MCP prompts (daily-digest uses profile, triage-shortlist filters by profile affinity)

### Hardware constraints and compute strategy
- Target hardware: Xeon W-2125 (4c/8t), 32GB RAM, GTX 1080 Ti (11GB VRAM), PostgreSQL + Redis local
- Phase 3 ranking is entirely CPU-bound and PostgreSQL-bound — no GPU, no embeddings, no external API calls needed
- All ranking computation (lexical scoring, category overlap, recency weighting) happens in PostgreSQL queries or lightweight Python post-processing — well within single-node constraints
- This phase is solidly "Bronze" compute profile (docs/05, §7): metadata + lexical retrieval + workflow-derived signals, no embeddings required
- Storage: interest profiles and signals are small metadata rows — negligible impact on /home (82% used) even at scale
- Secondary hardware: M4 MacBook Air (apollo) available over Tailscale — strong Neural Engine / unified memory for MLX inference, but not needed for Phase 3. Potential future use as secondary compute node for embedding inference (v2 semantic features) if it outperforms the 1080 Ti for specific model formats. For now it's the development client, not a compute node.

### Cost and sustainability model
- Self-hosted first: Phase 3 requires zero cloud services or external APIs — everything runs on local PostgreSQL
- Budget-conscious default: the ranking pipeline should never require paid services to function at its core level
- Cloud-optional upgrade path: if donation/contribution revenue arrives, the ranking pipeline should have clear slots where cloud services add value:
  - Semantic reranking via hosted embedding API (e.g., Voyage, Cohere) → plugs into the signal pipeline as an additional SignalScore type
  - Hosted vector DB for broader embedding coverage → Silver/Gold compute tier, not required for Bronze
  - GPU compute for local SPECTER2 embeddings → uses the 1080 Ti (11GB VRAM) for v2 semantic features, no cloud needed
- Design principle: Bronze (fully local, free) must be complete and useful. Silver/Gold are incremental improvements, not requirements.
- Donation model precedent: arxiv-sanity was donation-supported. If this project follows that path, investment priorities should be: (1) broader OpenAlex enrichment budget (Phase 4), (2) hosted embedding API for semantic reranking (v2), (3) better hardware for local inference. Phase 3 itself needs none of this.

### Claude's Discretion
- Database schema: single InterestProfile + InterestSignal tables vs per-signal-type tables (recommended: single signal table with type discriminator, same pattern as triage log)
- Scoring normalization approach (min-max vs sigmoid vs percentile)
- Exact default weights for composite scoring
- Whether to refactor WorkflowSearchService or create parallel ProfileRankingService
- Suggestion generation algorithm details (threshold tuning for "3+ shortlisted papers by author")
- Cursor encoding strategy for ranker config snapshot
- Test strategy: unit test individual signal scorers, integration test composite ranking
- Performance optimization: whether to pre-compute any signal components or compute everything at query time
- Alembic migration strategy (single migration vs incremental)
- Author name normalization approach (exact match vs fuzzy)
- How to handle deleted saved queries that are profile signals (same resilience pattern as watch with deleted collection: signal survives, invalid reference logged as warning)
- Result set ID generation and lifecycle (ephemeral vs persisted)

</decisions>

<specifics>
## Specific Ideas

- The ranking pipeline design mirrors Phase 2's WorkflowSearchService composition: each layer adds context without modifying the layer below. Phase 3 adds a ranking/explanation layer on top of the workflow-enriched results.
- Negative examples as soft demotions (not hard filters) is a direct application of ADR-0001's exploration-first principle — the system should never hide papers entirely based on user preferences.
- System suggestions from workflow activity create a natural feedback loop: triage → suggestions → confirmed signals → better ranking → more useful triage. But the user always stays in the loop (no implicit filter bubbles).
- Author following via name strings (not entity table) accepts the reality that arXiv has no canonical author ID. Normalization can improve over time without schema changes. When OpenAlex enrichment arrives (Phase 4), author disambiguation can leverage OpenAlex author IDs as a second-pass refinement.
- The "explain" capability is the product's core differentiator from opaque recommendation systems — every ranking decision is inspectable and traceable back to specific profile signals.
- Suggestion dismissal tracking prevents re-suggesting papers/authors the user has already considered and rejected — reduces suggestion fatigue over time.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `search/service.py`: SearchService (search_papers, browse_recent, find_related_papers) — base retrieval layer
- `search/ranking.py`: shape_search_results, TSVECTOR_WEIGHTS — current lexical ranking to wrap/extend
- `search/queries.py`: build_search_query, build_browse_query, build_related_query — composable query builders
- `workflow/search_augment.py`: WorkflowSearchService composition pattern — template for ProfileRankingService
- `db/models.py`: Single Base, all ORM models — add InterestProfile + InterestSignal here
- `models/paper.py`: SearchResult, WorkflowSearchResult — extend with ProfileSearchResult + RankingExplanation
- `models/workflow.py`: Pydantic schema patterns — follow for profile schemas
- `workflow/util.py`: slugify() — reuse for profile names
- `config.py`: Settings with soft limits — add profile soft limits

### Established Patterns
- SQLAlchemy ORM with async engine, single Base class in db/models.py
- Hand-written Alembic migrations (not autogenerated)
- Keyset cursor pagination (PaginatedResponse[T])
- Service layer with session_factory + settings DI
- Composition over modification (WorkflowSearchService wraps SearchService)
- Click subgroups for CLI organization
- Absence-means-default pattern (no row = unseen triage state)
- Provenance on all user actions (source, timestamp, reason)
- Slug-style unique identifiers for named entities
- Soft limits with warnings (not hard enforcement)
- JSONB for flexible/evolving parameter storage
- Batch operations with dry-run/confirm pattern

### Integration Points
- Paper.arxiv_id as FK target for seed papers and negative examples
- SavedQuery.slug for saved query signal references
- Paper.category_list (GIN indexed) for category overlap scoring
- Paper.search_vector for lexical similarity scoring in seed relation
- WorkflowSearchService.search_papers() as base for profile-aware search
- TriageState/TriageLog for suggestion generation (shortlisted papers → seed candidates)
- CollectionPaper for suggestion generation (collection patterns → signal candidates)
- SavedQuery.run_count for suggestion generation (frequently run queries)

</code_context>

<deferred>
## Deferred Ideas

- Semantic similarity scoring using embeddings — v2 (SEMA requirements), plugs into same signal slot
- Citation-based interest signals from OpenAlex — Phase 4 enrichment, integrates as additional signal type
- Cross-profile analysis ("your ML profile and NLP profile overlap on these 12 papers") — future capability
- Profile sharing/import between users — single-user system for now
- Active learning loop with automatic suggestion generation on triage activity — requires careful UX to avoid filter bubbles (ADVW-01 is v2)
- Temporal signal decay (older seeds/queries weighted less) — interesting but premature optimization
- Collaborative filtering signals — single-user, out of scope
- Profile-to-collection auto-population ("add top-ranked papers to collection automatically") — compose in Phase 6 MCP prompts

</deferred>

---

*Phase: 03-interest-modeling-ranking*
*Context gathered: 2026-03-09 via inference from Phase 1-2 patterns, ADRs, and project principles*
