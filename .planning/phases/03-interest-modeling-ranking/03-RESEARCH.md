# Phase 3: Interest Modeling & Ranking - Research

**Researched:** 2026-03-09
**Domain:** Interest profiles, composable ranking pipelines, ranking explanation models, signal normalization
**Confidence:** HIGH

## Summary

Phase 3 transforms the system from a search-and-browse tool into an interest-driven discovery engine. It adds two tightly coupled capabilities: (1) interest profiles composed of typed signals (seed papers, saved queries, followed authors, negative examples) with full provenance, and (2) a composable ranking pipeline that produces structured explanations for every result. The phase builds on Phase 1's lexical search infrastructure and Phase 2's workflow state (triage, collections, saved queries) to derive interest signals from existing user activity.

The core technical challenge is designing the ranking pipeline as a composable system where each signal type produces an independently normalized sub-score with a human-readable explanation, then combining them into a composite score while preserving all sub-scores for inspection. This must be done without introducing any new external dependencies -- all computation uses existing PostgreSQL FTS capabilities, category overlap via GIN-indexed arrays, and lightweight Python post-processing. The system must degrade gracefully: no profile means current behavior unchanged; empty profile means lexical-only results.

The architecture follows Phase 2's composition pattern: ProfileRankingService wraps WorkflowSearchService, adding profile-aware re-ranking and explanation generation as a post-processing step. Interest profiles and their signals are stored in two new tables (InterestProfile + InterestSignal) following the single-table-with-type-discriminator pattern established by TriageLog. Suggestion generation is batch-on-demand, deriving candidates from workflow activity (shortlisted papers, frequent queries, recurring authors) and requiring explicit user confirmation before activation.

**Primary recommendation:** Use a single InterestSignal table with a `signal_type` discriminator column (same pattern as TriageLog). Implement ranking as a Python post-processing pipeline on WorkflowSearchService results -- each signal scorer is a pure function that takes a paper + profile context and returns a SignalScore. Use min-max normalization within each signal type for the [0.0, 1.0] range. Encode ranker configuration snapshot as a top-level field on PaginatedResponse (not in cursor metadata).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Named profiles with slug-style identifiers (same convention as collections and saved queries)
- Multiple profiles allowed per user -- different research threads get separate profiles
- Profiles are explicit and user-controlled: every signal is user-added or system-suggested-then-confirmed (no implicit learning)
- Profile is a container of typed signals, not a single vector or embedding
- Empty profile is valid (degrades gracefully to unranked/lexical-only results)
- Profiles renamable after creation
- Profiles support archive (same pattern as collections)
- Four signal types: seed_papers, saved_queries, followed_authors, negative_examples
- Each signal records provenance: source ("manual", "suggestion", "agent"), added_at timestamp, optional reason/note
- Seed papers: list of arxiv_ids (FK to Paper)
- Saved queries: list of saved_query slugs (FK to SavedQuery)
- Followed authors: list of author name strings (no FK -- store normalized name strings)
- Negative examples: list of arxiv_ids (FK to Paper) -- soft demotion, NOT hard exclusion
- System-suggested signals derived from workflow activity, but always require user confirmation before activation
- Suggestion mechanism is advisory: generate candidates, present to user, user confirms/rejects -- never auto-activate
- Suggestion dismissal tracking prevents re-suggesting dismissed items
- Signal inspection: every signal individually inspectable with type, value, source, added_at, reason
- Profiles expose signal counts by type and by source
- Pending suggestions visually distinct from active signals
- Negative examples are soft demotions, not hard filters (ADR-0001 exploration-first principle)
- Negative weight configurable per-profile (default: moderate demotion)
- Ranking is a composable pipeline, not a monolithic scorer (ADR-0001)
- Current lexical ranking (ts_rank_cd) becomes one signal among several
- Signal types for explanations: query_match, seed_relation, category_overlap, interest_profile_match, recency
- Each signal produces normalized sub-score [0.0, 1.0] and human-readable explanation
- Final composite score combines sub-scores with configurable weights -- sub-scores always preserved
- Default weight profile with sensible defaults; user can adjust weights per profile (optional, not required for v1)
- Ranking without a profile: falls back to current behavior (lexical + recency)
- Every result includes a RankingExplanation object
- RankingExplanation: composite_score, signal_breakdown (list of SignalScore), ranker_version
- SignalScore: signal_type, raw_score, normalized_score, weight, weighted_score, explanation (human-readable string)
- Explanations generated at query time, not stored (avoids stale explanations)
- "Inspect ranker inputs" = full ranker config snapshot captured at query time for lifetime of paginated result set
- Extend WorkflowSearchService composition pattern (not modify Phase 1 SearchService)
- ProfileRankingService wraps WorkflowSearchService
- Flow: SearchService -> WorkflowSearchService -> ProfileRankingService
- Profile is optional parameter on search/browse -- if omitted, no profile ranking applied
- find_related_papers gains profile context: seed relation scoring uses profile seeds + explicit seed
- Suggestions batch-generated on demand (not background process)
- Suggestion sources: shortlisted/cite-later papers -> seed candidates, high run_count queries -> query candidates, authors appearing 3+ in shortlisted/cite-later -> follow candidates
- Suggestions include explanation of why suggested
- User confirms individually or in bulk (batch pattern)
- CLI: `arxiv-mcp profile create/list/show/delete/rename/archive/unarchive` -- profile CRUD
- CLI: `arxiv-mcp profile add-seed/remove-seed/add-query/remove-query/follow/unfollow/add-negative/remove-negative` -- signal management
- CLI: `arxiv-mcp profile signals/suggest/confirm/dismiss` -- inspection and suggestions
- Search/browse commands gain `--profile <slug>` flag
- `arxiv-mcp search explain <result_set_id>` or inline `--explain` for ranker input inspection
- Phase 3 is entirely CPU-bound and PostgreSQL-bound -- no GPU, no embeddings, no external APIs
- Zero cloud services required -- everything runs on local PostgreSQL

### Claude's Discretion
- Database schema: single InterestProfile + InterestSignal tables vs per-signal-type tables
- Scoring normalization approach (min-max vs sigmoid vs percentile)
- Exact default weights for composite scoring
- Whether to refactor WorkflowSearchService or create parallel ProfileRankingService
- Suggestion generation algorithm details (threshold tuning)
- Cursor encoding strategy for ranker config snapshot
- Test strategy: unit test individual signal scorers, integration test composite ranking
- Performance optimization: pre-compute vs compute everything at query time
- Alembic migration strategy (single migration vs incremental)
- Author name normalization approach (exact match vs fuzzy)
- How to handle deleted saved queries that are profile signals
- Result set ID generation and lifecycle (ephemeral vs persisted)

### Deferred Ideas (OUT OF SCOPE)
- Semantic similarity scoring using embeddings -- v2 (SEMA requirements)
- Citation-based interest signals from OpenAlex -- Phase 4 enrichment
- Cross-profile analysis -- future capability
- Profile sharing/import between users -- single-user system
- Active learning loop with automatic suggestion generation -- v2
- Temporal signal decay -- premature optimization
- Collaborative filtering signals -- single-user, out of scope
- Profile-to-collection auto-population -- compose in Phase 6 MCP prompts

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INTR-01 | User can create and manage interest profiles composed of multiple signal types | InterestProfile table with slug, name, is_archived, negative_weight, weights JSONB; service layer with CRUD; CLI `profile create/list/show/delete/rename/archive/unarchive` |
| INTR-02 | Interest profiles support seed paper sets as signals | InterestSignal with signal_type='seed_paper', signal_value=arxiv_id, FK to Paper; CLI `profile add-seed/remove-seed` |
| INTR-03 | Interest profiles support saved queries as signals | InterestSignal with signal_type='saved_query', signal_value=slug; resilient to deleted queries (warning, not error); CLI `profile add-query/remove-query` |
| INTR-04 | Interest profiles support followed authors as signals | InterestSignal with signal_type='followed_author', signal_value=normalized author name string; CLI `profile follow/unfollow` |
| INTR-05 | Interest profiles support negative examples (papers/topics to deprioritize) | InterestSignal with signal_type='negative_example', signal_value=arxiv_id, FK to Paper; soft demotion scoring (not hard exclusion) with configurable negative_weight |
| INTR-06 | User can inspect all signals in a profile and their provenance (user-added vs system-suggested) | InterestSignal stores source ('manual'/'suggestion'/'agent'), status ('active'/'pending'/'dismissed'), added_at, reason; profile signals CLI shows counts by type and source |
| RANK-01 | Results include structured ranking explanations | ProfileSearchResult extends WorkflowSearchResult with RankingExplanation; every item in PaginatedResponse includes signal_breakdown list |
| RANK-02 | Explanations expose signal types: query match, seed relation, category overlap, interest profile match, recency | Five SignalScorer implementations, each producing SignalScore with signal_type enum, normalized score, human-readable explanation string |
| RANK-03 | User can inspect ranker inputs for any result set | RankerSnapshot captured at query time; returned as top-level field on PaginatedResponse; includes profile slug, active weights, signal types applied, ranker version |

</phase_requirements>

## Standard Stack

### Core (already installed -- no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLAlchemy | 2.0+ | ORM models for InterestProfile + InterestSignal tables, queries | Already in use; same mapped_column + relationship pattern as Phase 2 |
| asyncpg | 0.30+ | Async PostgreSQL driver | Already in use; no change |
| Alembic | 1.14+ | Hand-written migration 003 for interest tables | Already in use; same hand-written pattern as 001/002 |
| Pydantic | 2.10+ | Schema models for profiles, signals, ranking explanations, signal scores | Already in use; extend models/ with interest + ranking schemas |
| Click | 8.1+ | CLI subgroup: profile (with signal management subcommands) | Already in use; same subgroup registration pattern |
| structlog | 24.4+ | Logging for profile operations, ranking pipeline diagnostics | Already in use |
| rich | 13.9+ | Table display for profile listings, signal inspection, ranking explanations | Already in use |

### Supporting (no new dependencies needed)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| enum module | stdlib | SignalType and SignalStatus enums for type safety | Discriminator values for InterestSignal |
| dataclasses module | stdlib | Lightweight scorer result containers | Internal ranking pipeline data flow |
| math module | stdlib | Score normalization (min-max, clamping) | Signal score normalization to [0.0, 1.0] |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Single InterestSignal table with type discriminator | Separate table per signal type (SeedPaper, FollowedAuthor, etc.) | Single table is simpler, matches TriageLog pattern, easier to query all signals for a profile; separate tables add JOINs and migration complexity |
| Min-max normalization | Sigmoid normalization | Min-max is simpler, interpretable (0=worst in batch, 1=best); sigmoid works better for unbounded scores but adds complexity; min-max is sufficient for Phase 3's bounded signal types |
| Top-level ranker snapshot on PaginatedResponse | Encode ranker config in cursor metadata | Top-level field is cleaner, explicit, and does not inflate cursor tokens; cursor metadata approach obscures the snapshot and complicates cursor decoding |
| Python post-processing ranking | PostgreSQL window functions for ranking | Python post-processing allows arbitrary ranking logic without complex SQL; profile-aware scoring requires in-memory profile data that would be cumbersome to pass to SQL; performance is adequate since result sets are already bounded by page_size |
| Ephemeral result set IDs (UUID per search call) | Persisted result sets in database | Ephemeral avoids storage overhead; the ranker snapshot is returned inline on the response; persisted result sets add table, cleanup, and lifecycle management for minimal benefit at this stage |

**Installation:**
```bash
# No new dependencies -- all requirements already in pyproject.toml
```

## Architecture Patterns

### Recommended Module Structure
```
src/arxiv_mcp/
├── db/
│   ├── models.py              # Add: InterestProfile, InterestSignal
│   └── queries.py             # No changes
├── interest/
│   ├── __init__.py
│   ├── profiles.py            # ProfileService: CRUD, signal management, archive
│   ├── signals.py             # Signal validation, author normalization
│   ├── suggestions.py         # SuggestionService: batch generation from workflow activity
│   ├── ranking.py             # RankingPipeline: signal scorers, composite scoring, explanations
│   ├── search_augment.py      # ProfileRankingService: wraps WorkflowSearchService
│   └── cli.py                 # Click subgroup: profile (CRUD + signal + suggestion commands)
├── models/
│   ├── paper.py               # Add: ProfileSearchResult (extends WorkflowSearchResult)
│   ├── pagination.py          # No changes (PaginatedResponse already generic)
│   ├── workflow.py            # No changes
│   └── interest.py            # New: Pydantic schemas for profiles, signals, ranking explanations
├── search/
│   ├── cli.py                 # Add: --profile flag to search/browse, --explain flag
│   └── ...                    # No other changes
└── config.py                  # Add: profile soft limits, default ranking weights
```

### Pattern 1: Single Signal Table with Type Discriminator
**What:** Store all signal types in one InterestSignal table, using a `signal_type` column to discriminate between seed_paper, saved_query, followed_author, and negative_example.
**When to use:** All signal operations (INTR-02 through INTR-06).

```python
# Recommendation: single table with type discriminator
class InterestProfile(Base):
    """Named interest profile containing typed signals."""
    __tablename__ = "interest_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    negative_weight: Mapped[float] = mapped_column(Float, default=0.3)  # 0.0-1.0 demotion strength
    weights: Mapped[dict | None] = mapped_column(JSONB)  # Optional custom signal weights
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    signals: Mapped[list["InterestSignal"]] = relationship(
        "InterestSignal", back_populates="profile", cascade="all, delete-orphan"
    )


class InterestSignal(Base):
    """A single signal in an interest profile with provenance."""
    __tablename__ = "interest_signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(
        ForeignKey("interest_profiles.id", ondelete="CASCADE"), nullable=False
    )
    signal_type: Mapped[str] = mapped_column(String(32), nullable=False)
    # Discriminated by signal_type:
    #   seed_paper -> arxiv_id
    #   saved_query -> saved query slug
    #   followed_author -> normalized author name
    #   negative_example -> arxiv_id
    signal_value: Mapped[str] = mapped_column(String(256), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, pending, dismissed
    source: Mapped[str] = mapped_column(String(32), default="manual")  # manual, suggestion, agent
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    reason: Mapped[str | None] = mapped_column(Text)

    profile: Mapped["InterestProfile"] = relationship(
        "InterestProfile", back_populates="signals"
    )

    __table_args__ = (
        CheckConstraint(
            "signal_type IN ('seed_paper', 'saved_query', 'followed_author', 'negative_example')",
            name="ck_signal_type_valid",
        ),
        CheckConstraint(
            "status IN ('active', 'pending', 'dismissed')",
            name="ck_signal_status_valid",
        ),
        Index("idx_interest_signals_profile_type", "profile_id", "signal_type"),
        # Prevent duplicate signals of same type+value in a profile
        Index(
            "uq_interest_signals_profile_type_value",
            "profile_id", "signal_type", "signal_value",
            unique=True,
        ),
    )
```

### Pattern 2: Composable Ranking Pipeline
**What:** Each signal type has an independent scorer function that receives a paper and profile context, returning a SignalScore. A RankingPipeline orchestrates all scorers and produces the composite result.
**When to use:** All ranking operations (RANK-01, RANK-02).

```python
# interest/ranking.py
from dataclasses import dataclass
from enum import StrEnum

class SignalType(StrEnum):
    QUERY_MATCH = "query_match"
    SEED_RELATION = "seed_relation"
    CATEGORY_OVERLAP = "category_overlap"
    INTEREST_PROFILE_MATCH = "interest_profile_match"
    RECENCY = "recency"

@dataclass
class SignalScore:
    signal_type: SignalType
    raw_score: float
    normalized_score: float  # [0.0, 1.0]
    weight: float
    weighted_score: float    # normalized_score * weight
    explanation: str         # e.g., "Strong title match on 'transformer attention'"

@dataclass
class RankingExplanation:
    composite_score: float
    signal_breakdown: list[SignalScore]
    ranker_version: str

class RankingPipeline:
    """Orchestrates signal scorers and produces composite ranking."""

    RANKER_VERSION = "0.3.0"  # Tracks ranking algorithm version

    DEFAULT_WEIGHTS = {
        SignalType.QUERY_MATCH: 0.35,
        SignalType.SEED_RELATION: 0.25,
        SignalType.CATEGORY_OVERLAP: 0.15,
        SignalType.INTEREST_PROFILE_MATCH: 0.15,
        SignalType.RECENCY: 0.10,
    }

    def __init__(self, weights: dict[SignalType, float] | None = None):
        self.weights = weights or self.DEFAULT_WEIGHTS

    def score_paper(
        self,
        paper: PaperSummary,
        *,
        query_rank: float | None = None,
        profile_context: ProfileContext | None = None,
    ) -> RankingExplanation:
        """Score a single paper against all applicable signals."""
        scores = []

        # 1. Query match (from existing ts_rank_cd)
        if query_rank is not None:
            scores.append(self._score_query_match(query_rank))

        if profile_context:
            # 2. Seed relation
            if profile_context.seed_papers:
                scores.append(self._score_seed_relation(paper, profile_context))
            # 3. Category overlap
            if profile_context.seed_categories:
                scores.append(self._score_category_overlap(paper, profile_context))
            # 4. Interest profile match (composite of all positive signals)
            scores.append(self._score_profile_match(paper, profile_context))

        # 5. Recency
        scores.append(self._score_recency(paper))

        # Apply negative demotion
        if profile_context and profile_context.negative_papers:
            self._apply_negative_demotion(scores, paper, profile_context)

        composite = sum(s.weighted_score for s in scores)
        return RankingExplanation(
            composite_score=composite,
            signal_breakdown=scores,
            ranker_version=self.RANKER_VERSION,
        )
```

### Pattern 3: ProfileRankingService Composition
**What:** Wrap WorkflowSearchService to add profile-aware re-ranking as post-processing, following the same composition-over-modification pattern used in Phase 2.
**When to use:** All profile-aware search operations.

```python
# interest/search_augment.py
class ProfileRankingService:
    """Wraps WorkflowSearchService with profile-aware ranking and explanations.

    When a profile slug is provided, re-ranks results using the
    RankingPipeline and attaches RankingExplanation to each result.
    When no profile is provided, passes through unchanged.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        workflow_search_service: WorkflowSearchService,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.workflow_search = workflow_search_service

    async def search_papers(
        self, *, profile_slug: str | None = None, **kwargs
    ) -> PaginatedResponse[ProfileSearchResult]:
        """Search with optional profile-aware ranking."""
        result = await self.workflow_search.search_papers(**kwargs)

        if profile_slug is None:
            return self._wrap_without_ranking(result)

        profile_ctx = await self._load_profile_context(profile_slug)
        pipeline = RankingPipeline(weights=profile_ctx.weights)

        ranked = []
        for item in result.items:
            explanation = pipeline.score_paper(
                item.paper,
                query_rank=item.score,
                profile_context=profile_ctx,
            )
            ranked.append(ProfileSearchResult(
                paper=item.paper,
                score=explanation.composite_score,
                triage_state=item.triage_state,
                collection_slugs=item.collection_slugs,
                ranking_explanation=explanation,
            ))

        # Re-sort by composite score
        ranked.sort(key=lambda r: r.score or 0, reverse=True)

        return PaginatedResponse[ProfileSearchResult](
            items=ranked,
            page_info=result.page_info,
            ranker_snapshot=self._capture_snapshot(profile_ctx, pipeline),
        )
```

### Pattern 4: Suggestion Generation from Workflow Activity
**What:** Batch-generate signal suggestions by querying triage states, saved query run counts, and author frequency in shortlisted papers.
**When to use:** `profile suggest` command (INTR-06).

```python
# interest/suggestions.py
class SuggestionService:
    """Generates interest signal suggestions from workflow activity."""

    async def generate_suggestions(
        self, profile_slug: str
    ) -> list[SuggestionCandidate]:
        """Batch-generate suggestions for a profile.

        Sources:
        - Papers with triage 'shortlisted' or 'cite-later' -> seed candidates
        - SavedQuery with run_count >= 3 -> query candidates
        - Authors appearing 3+ times in shortlisted/cite-later papers -> follow candidates
        """
        async with self.session_factory() as session:
            profile = await self._get_profile_or_raise(session, profile_slug)
            existing_values = await self._get_existing_signal_values(session, profile.id)
            dismissed_values = await self._get_dismissed_values(session, profile.id)

            candidates = []
            candidates.extend(
                await self._suggest_seed_papers(session, existing_values, dismissed_values)
            )
            candidates.extend(
                await self._suggest_queries(session, existing_values, dismissed_values)
            )
            candidates.extend(
                await self._suggest_authors(session, existing_values, dismissed_values)
            )

            return candidates
```

### Anti-Patterns to Avoid
- **Monolithic scorer function:** Do NOT build a single giant function that computes all signal scores. Each signal type must be an independent scorer for testability, extensibility (Phase 4 enrichment signals plug in), and debuggability.
- **Hard exclusion of negative examples:** Do NOT filter out papers matching negative examples. CONTEXT.md explicitly states soft demotion only (ADR-0001 exploration-first). Apply score penalty, never remove from results.
- **Modifying Phase 1 or Phase 2 services:** Do NOT change SearchService or WorkflowSearchService. Compose by wrapping in ProfileRankingService. The `--profile` flag on search CLI selects which service layer to use.
- **Storing ranking explanations in the database:** CONTEXT.md says explanations are generated at query time, not stored. This avoids stale explanations when profiles change.
- **Auto-activating suggestions:** Suggestions MUST require explicit user confirmation. Never auto-add signals to a profile based on workflow activity.
- **Using PostgreSQL ENUM for signal_type/status:** Same pitfall as Phase 2 -- use VARCHAR + CHECK constraint for migration simplicity.
- **Normalizing scores across different result sets:** Each result set normalizes independently. Do not maintain global score statistics.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Slug generation for profiles | New slugify function | Existing `workflow.util.slugify()` | Already implemented and tested in Phase 2 |
| Cursor pagination for profile listings | New pagination system | Existing `models/pagination.py` PaginatedResponse | Phase 1 already solved this; profile signals list uses same pattern |
| Author name normalization | Complex NLP pipeline | Simple lowercase + whitespace normalization | arXiv has no canonical author IDs; exact-ish matching is sufficient for v1; OpenAlex disambiguation comes in Phase 4 |
| Category set operations | Custom set math | Python set intersection/union on Paper.category_list | category_list is already a list[str]; set operations are trivial |
| Score normalization | Statistical library (scipy, numpy) | Python stdlib min-max: `(x - min) / (max - min)` | Signal scores are bounded and simple; no need for a dependency |
| Recency scoring | Complex temporal decay functions | Simple linear decay from most recent date in result set | Recency is one signal among five; linear decay is interpretable and sufficient |

**Key insight:** Phase 3 adds no new external dependencies. The ranking pipeline is pure Python logic operating on data already available from PostgreSQL queries. The complexity is in the design of the composable pipeline, not in the technology stack.

## Common Pitfalls

### Pitfall 1: Score Normalization with Empty or Single-Element Result Sets
**What goes wrong:** Min-max normalization divides by zero when all scores are the same (min == max) or the result set has one item.
**Why it happens:** `(x - min) / (max - min)` fails when max == min.
**How to avoid:** Guard against zero division: when min == max, assign all items a normalized score of 1.0 (or 0.5 if preferred). When result set has zero items, skip normalization entirely.
**Warning signs:** ZeroDivisionError in ranking pipeline; all normalized scores appearing as NaN or infinity.

### Pitfall 2: Re-ranking Invalidates Keyset Cursor Pagination
**What goes wrong:** Phase 1's keyset pagination assumes stable sort order (by rank or date). Profile re-ranking changes the sort order, making cursor-based "next page" return wrong results.
**Why it happens:** The cursor encodes a (sort_value, paper_id) pair. After re-ranking, the sort_value changes from the original ts_rank_cd to the composite score, but the cursor was built from the original ordering.
**How to avoid:** When profile ranking is active, pagination must account for the re-ranked order. Two approaches: (a) fetch a larger result set from the base query and re-rank the full set (works for small-medium sets), or (b) use offset-based pagination for profile-ranked results (simpler, acceptable for interactive use). Recommended: fetch `page_size * 3` from base query, re-rank, return top `page_size` -- sufficient for Phase 3's lexical-only signals where re-ranking produces modest reordering.
**Warning signs:** Duplicate papers across pages; papers missing from paginated results; inconsistent ordering between pages.

### Pitfall 3: Circular Scoring -- Seed Paper Appears in Results
**What goes wrong:** A seed paper in the profile appears in search results and gets a perfect seed_relation score, always ranking first and providing no discovery value.
**Why it happens:** Seed papers match themselves perfectly on all lexical and category signals.
**How to avoid:** Exclude profile seed papers from the result set (or cap their seed_relation score at 0). They are reference points, not discovery targets. Same for negative examples -- they should still appear but with their scores adjusted, not removed entirely (exploration-first).
**Warning signs:** Seed papers always appearing at rank 1 in profile-ranked results.

### Pitfall 4: N+1 Queries for Seed Paper Metadata
**What goes wrong:** Computing seed_relation and category_overlap requires loading each seed paper's metadata individually, creating N queries for N seed papers.
**Why it happens:** The ranking pipeline needs category_list and search_vector data for each seed paper.
**How to avoid:** Batch-load all seed paper metadata when constructing ProfileContext (single query: `SELECT * FROM papers WHERE arxiv_id IN (:seed_ids)`). Cache in ProfileContext for the duration of the ranking call.
**Warning signs:** Slow profile-ranked searches; query count scaling linearly with number of seed papers.

### Pitfall 5: Author Name Matching False Positives
**What goes wrong:** Following "Li Wang" matches "Li Wang", "Li-Chen Wang", "Wang Li", and possibly "Xiaoli Wang" depending on normalization.
**Why it happens:** Author names in arXiv are free-form text strings with inconsistent formatting.
**How to avoid:** For v1, use case-insensitive exact match on the normalized author string. This will have false negatives (misses name variants) but avoids false positives (wrong person). When OpenAlex enrichment arrives in Phase 4, author disambiguation improves. Document the limitation clearly.
**Warning signs:** Followed author matching papers by completely different people; or, conversely, missing papers by the followed author due to name variants.

### Pitfall 6: Suggestion Re-generation Suggesting Already-Dismissed Items
**What goes wrong:** Running `profile suggest` repeatedly re-suggests items the user already dismissed, creating suggestion fatigue.
**Why it happens:** Dismissal state not checked when generating new suggestions.
**How to avoid:** Store dismissed suggestions as InterestSignal with status='dismissed'. When generating new suggestions, exclude any (profile_id, signal_type, signal_value) tuples that already exist in the signals table regardless of status. This is why the unique index on (profile_id, signal_type, signal_value) is important -- it prevents both duplicates and re-suggestions.
**Warning signs:** Same author/paper/query appearing repeatedly in suggestions despite being dismissed.

### Pitfall 7: PaginatedResponse Generic Type Changes
**What goes wrong:** Adding `ranker_snapshot` as a field on PaginatedResponse breaks existing uses that don't supply it.
**Why it happens:** PaginatedResponse is a generic class used across all search operations.
**How to avoid:** Do NOT modify PaginatedResponse itself. Instead, create a `RankedPaginatedResponse` that extends it with the ranker_snapshot field. Or return the snapshot as a separate top-level field alongside the paginated response. The cleanest approach is a `ProfileSearchResponse` dataclass/model that wraps PaginatedResponse + RankerSnapshot.
**Warning signs:** Pydantic validation errors in existing Phase 1/2 code; unexpected fields in JSON output for non-profile searches.

## Code Examples

### ProfileContext Data Container
```python
# interest/ranking.py
@dataclass
class ProfileContext:
    """Pre-loaded profile data for ranking pipeline."""
    profile_slug: str
    seed_papers: list[PaperSummary]  # Pre-loaded seed paper metadata
    seed_categories: set[str]        # Union of all seed paper categories
    followed_authors: list[str]      # Normalized author names
    negative_papers: list[PaperSummary]  # Pre-loaded negative example metadata
    negative_categories: set[str]    # Union of all negative paper categories
    negative_weight: float           # 0.0-1.0 demotion strength
    query_slugs: list[str]           # Saved query slugs in profile
    weights: dict[str, float]        # Signal type -> weight mapping
```

### Query Match Signal Scorer
```python
def score_query_match(query_rank: float | None, all_ranks: list[float]) -> SignalScore:
    """Score based on lexical search relevance (ts_rank_cd).

    Normalizes the raw ts_rank_cd score to [0.0, 1.0] using min-max
    within the current result set.
    """
    if query_rank is None:
        return SignalScore(
            signal_type=SignalType.QUERY_MATCH,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="No text query active",
        )

    # Min-max normalization within result set
    min_rank = min(all_ranks) if all_ranks else 0.0
    max_rank = max(all_ranks) if all_ranks else 0.0
    if max_rank == min_rank:
        normalized = 1.0  # All same score -> all get max normalized
    else:
        normalized = (query_rank - min_rank) / (max_rank - min_rank)

    weight = DEFAULT_WEIGHTS[SignalType.QUERY_MATCH]
    return SignalScore(
        signal_type=SignalType.QUERY_MATCH,
        raw_score=query_rank,
        normalized_score=round(normalized, 4),
        weight=weight,
        weighted_score=round(normalized * weight, 4),
        explanation=f"Lexical relevance score: {query_rank:.4f} (normalized: {normalized:.2f})",
    )
```

### Category Overlap Signal Scorer
```python
def score_category_overlap(
    paper: PaperSummary,
    seed_categories: set[str],
) -> SignalScore:
    """Score based on category overlap with profile seed papers.

    Uses Jaccard similarity between paper's categories and the union
    of all seed paper categories.
    """
    paper_cats = set(paper.category_list)
    if not paper_cats or not seed_categories:
        return SignalScore(
            signal_type=SignalType.CATEGORY_OVERLAP,
            raw_score=0.0,
            normalized_score=0.0,
            weight=DEFAULT_WEIGHTS[SignalType.CATEGORY_OVERLAP],
            weighted_score=0.0,
            explanation="No category data available",
        )

    overlap = paper_cats & seed_categories
    union = paper_cats | seed_categories
    jaccard = len(overlap) / len(union) if union else 0.0

    weight = DEFAULT_WEIGHTS[SignalType.CATEGORY_OVERLAP]
    overlap_names = ", ".join(sorted(overlap)) if overlap else "none"
    return SignalScore(
        signal_type=SignalType.CATEGORY_OVERLAP,
        raw_score=jaccard,
        normalized_score=round(jaccard, 4),  # Jaccard is already [0, 1]
        weight=weight,
        weighted_score=round(jaccard * weight, 4),
        explanation=f"Shares {len(overlap)}/{len(paper_cats)} categories with seeds ({overlap_names})",
    )
```

### Recency Signal Scorer
```python
def score_recency(
    paper: PaperSummary,
    max_date: date,
    decay_days: int = 90,
) -> SignalScore:
    """Score based on paper recency with linear decay.

    Papers from today get 1.0; papers older than decay_days get 0.0.
    Uses announced_date (or submitted_date as fallback).
    """
    paper_date = paper.announced_date or paper.submitted_date.date()
    days_old = (max_date - paper_date).days
    raw = max(0.0, 1.0 - (days_old / decay_days))

    weight = DEFAULT_WEIGHTS[SignalType.RECENCY]
    return SignalScore(
        signal_type=SignalType.RECENCY,
        raw_score=raw,
        normalized_score=round(raw, 4),  # Linear decay is already [0, 1]
        weight=weight,
        weighted_score=round(raw * weight, 4),
        explanation=f"{days_old} days old (decay window: {decay_days} days)",
    )
```

### Ranker Snapshot for Result Set Inspection (RANK-03)
```python
@dataclass
class RankerSnapshot:
    """Captured ranker configuration at query time for result set inspection."""
    profile_slug: str | None
    ranker_version: str
    weights: dict[str, float]
    signal_types_applied: list[str]
    seed_paper_count: int
    followed_author_count: int
    negative_example_count: int
    saved_query_count: int
    negative_weight: float
    captured_at: datetime

class ProfileSearchResponse(BaseModel):
    """Search response with profile ranking, extending PaginatedResponse."""
    results: PaginatedResponse[ProfileSearchResult]
    ranker_snapshot: RankerSnapshot | None = None
```

### Suggestion Generation: Author Frequency Query
```python
async def _suggest_authors(
    self,
    session: AsyncSession,
    existing_values: set[str],
    dismissed_values: set[str],
) -> list[SuggestionCandidate]:
    """Find authors appearing 3+ times in shortlisted/cite-later papers."""
    # Get all shortlisted/cite-later paper IDs
    stmt = (
        select(Paper.authors_text)
        .join(TriageState, Paper.arxiv_id == TriageState.paper_id)
        .where(TriageState.state.in_(["shortlisted", "cite-later"]))
    )
    result = await session.execute(stmt)
    rows = result.all()

    # Parse and count author occurrences
    author_counts: dict[str, int] = {}
    for (authors_text,) in rows:
        for author in _parse_authors(authors_text):
            normalized = _normalize_author(author)
            author_counts[normalized] = author_counts.get(normalized, 0) + 1

    candidates = []
    for author, count in author_counts.items():
        if count >= 3 and author not in existing_values and author not in dismissed_values:
            candidates.append(SuggestionCandidate(
                signal_type="followed_author",
                signal_value=author,
                reason=f"Appears in {count} shortlisted/cite-later papers",
            ))

    return candidates
```

### Author Name Normalization
```python
def _normalize_author(name: str) -> str:
    """Normalize author name for matching.

    Lowercase, collapse whitespace, strip leading/trailing space.
    Does NOT attempt disambiguation (that requires OpenAlex in Phase 4).
    """
    return " ".join(name.lower().split())

def _parse_authors(authors_text: str) -> list[str]:
    """Parse comma-separated author string into individual names."""
    if not authors_text:
        return []
    return [a.strip() for a in authors_text.split(",") if a.strip()]
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Opaque relevance score (single float) | Structured ranking explanation with signal breakdown | Phase 3 design | Users/agents can understand and debug why papers surfaced |
| Fixed lexical ranking only | Composable multi-signal ranking pipeline | Phase 3 design | Ranking extensible with new signal types in future phases |
| No interest modeling | Explicit interest profiles with typed signals | Phase 3 design | System can personalize discovery without opaque ML |
| Monolithic search result type | Layered result types (SearchResult -> WorkflowSearchResult -> ProfileSearchResult) | Phase 1-3 progression | Each layer adds context without modifying lower layers |

**Deprecated/outdated:**
- **Single `score` field on SearchResult:** Still present for backward compatibility, but profile-ranked results use RankingExplanation.composite_score as the primary score.
- **Implicit taste modeling via tag-based systems:** ADR-0001 explicitly rejects reducing interest to tags. Profiles use multiple signal types with provenance.

## Open Questions

1. **Seed relation scoring without embeddings**
   - What we know: Phase 3 must compute seed relation using lexical signals only (no embeddings until v2/SEMA). The existing `build_related_query` uses title + abstract tsquery matching.
   - What's unclear: How to efficiently compute a seed_relation score for each result paper against multiple seed papers without running N separate full-text queries (one per seed).
   - Recommendation: For each seed paper, extract the combined tsquery (same as `build_related_query`). Pre-compute these at ProfileContext load time. For each result paper, compute `ts_rank_cd(paper.search_vector, seed_tsquery)` for each seed and take the max. This requires the search_vector column on the result papers, which means either: (a) loading it from the database in a batch follow-up query, or (b) computing a proxy using category overlap + author overlap as a stand-in for seed_relation. Approach (b) is simpler and avoids additional database queries. The full lexical seed_relation can be a refinement if performance allows.

2. **Interest profile match as composite signal**
   - What we know: CONTEXT.md lists `interest_profile_match` as one of the five signal types. It is described as "composite profile affinity."
   - What's unclear: How this differs from the sum of seed_relation + category_overlap + followed_author signals, which already capture profile affinity.
   - Recommendation: Define `interest_profile_match` as the normalized sum of the other profile-derived signals (seed_relation + category_overlap + author match). This avoids double-counting while still providing a single "how well does this paper match your profile" number in the explanation. If all profile-derived sub-signals are zero (empty profile), this signal is zero.

3. **Pagination strategy for re-ranked results**
   - What we know: Re-ranking changes result order, which invalidates keyset cursors.
   - What's unclear: Whether to use offset pagination, over-fetch + re-rank, or a different approach.
   - Recommendation: Over-fetch approach: request `page_size * 3` from the base query, re-rank all, return the top `page_size`. For "next page" calls, increase the over-fetch window. This works well for typical interactive use (first 2-3 pages). For deeper pagination, the re-ranking effect diminishes anyway (papers far from the lexical top are unlikely to be re-ranked dramatically). Document this limitation; address in Phase 7 hardening if needed.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` (existing) |
| Quick run command | `uv run pytest tests/ -x --timeout=30` |
| Full suite command | `uv run pytest tests/ -v --cov=src/arxiv_mcp` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INTR-01 | Profile CRUD (create, list, show, delete, rename, archive) | integration | `uv run pytest tests/test_interest/test_profiles.py::TestProfileCRUD -x` | Wave 0 |
| INTR-02 | Seed paper signal management (add/remove) | integration | `uv run pytest tests/test_interest/test_profiles.py::TestSeedPaperSignals -x` | Wave 0 |
| INTR-03 | Saved query signal management (add/remove, resilience to deleted queries) | integration | `uv run pytest tests/test_interest/test_profiles.py::TestSavedQuerySignals -x` | Wave 0 |
| INTR-04 | Followed author signal management (follow/unfollow) | integration | `uv run pytest tests/test_interest/test_profiles.py::TestFollowedAuthorSignals -x` | Wave 0 |
| INTR-05 | Negative example signal management (add/remove, soft demotion) | integration | `uv run pytest tests/test_interest/test_profiles.py::TestNegativeExampleSignals -x` | Wave 0 |
| INTR-06 | Signal inspection with provenance, suggestion lifecycle | integration | `uv run pytest tests/test_interest/test_suggestions.py -x` | Wave 0 |
| RANK-01 | Ranking explanations on search results | integration | `uv run pytest tests/test_interest/test_ranking.py::TestRankingExplanations -x` | Wave 0 |
| RANK-02 | Five signal types produce correct scores and explanations | unit | `uv run pytest tests/test_interest/test_ranking.py::TestSignalScorers -x` | Wave 0 |
| RANK-03 | Ranker input inspection (snapshot) | integration | `uv run pytest tests/test_interest/test_ranking.py::TestRankerSnapshot -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/ -x --timeout=30`
- **Per wave merge:** `uv run pytest tests/ -v --cov=src/arxiv_mcp`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_interest/__init__.py` -- package init
- [ ] `tests/test_interest/conftest.py` -- shared fixtures (test DB with interest tables, sample profiles/signals, pre-loaded seed papers)
- [ ] `tests/test_interest/test_profiles.py` -- stubs for INTR-01 through INTR-05 (profile CRUD and all signal types)
- [ ] `tests/test_interest/test_suggestions.py` -- stubs for INTR-06 (suggestion generation, confirm, dismiss, provenance inspection)
- [ ] `tests/test_interest/test_ranking.py` -- stubs for RANK-01 through RANK-03 (signal scorers, composite ranking, explanations, snapshot)
- [ ] Interest table creation in test conftest (extending Phase 2's test_session pattern with InterestProfile + InterestSignal)
- [ ] Sample profile/signal test data factory functions (`sample_profile_data()`, `sample_signal_data()`)
- [ ] Pre-loaded seed paper fixtures with known categories for deterministic category overlap tests

## Sources

### Primary (HIGH confidence)
- **Existing codebase** (all source files read): Established patterns for ORM models (db/models.py), service layer (workflow/collections.py, workflow/triage.py), search augmentation (workflow/search_augment.py), Pydantic schemas (models/paper.py, models/workflow.py), CLI structure (workflow/cli.py, search/cli.py), pagination (models/pagination.py), configuration (config.py), Alembic migrations (002_workflow_tables.py), test infrastructure (tests/conftest.py, tests/test_workflow/conftest.py)
- **CONTEXT.md** (Phase 3): All locked decisions, signal types, ranking pipeline design, CLI structure, suggestion mechanism, hardware constraints
- **REQUIREMENTS.md**: INTR-01 through INTR-06, RANK-01 through RANK-03 requirement definitions
- **ADR-0001**: Exploration-first architecture -- multiple retrieval/ranking strategies coexist; negative examples as soft demotion not hard exclusion
- **ADR-0002**: Metadata-first, lazy enrichment -- ranking uses metadata signals; enrichment signals come in Phase 4

### Secondary (MEDIUM confidence)
- **SQLAlchemy 2.0 documentation**: CHECK constraint patterns, JSONB column type, relationship cascade options, Index creation with unique constraint
- **PostgreSQL FTS documentation**: ts_rank_cd scoring behavior, tsquery composition for seed relation scoring
- **Pydantic v2 documentation**: Generic model patterns, BaseModel extension, ConfigDict(from_attributes=True)

### Tertiary (LOW confidence)
- **Scoring normalization best practices**: Min-max normalization is standard for bounded score ranges; sigmoid and percentile approaches are alternatives if score distributions prove problematic in practice. Actual weight tuning will require real-world testing with harvested data.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies; all libraries already proven in Phase 1-2
- Architecture: HIGH -- follows established Phase 2 composition pattern exactly; new module structure mirrors workflow/
- Database schema: HIGH -- single-table-with-discriminator pattern proven by TriageLog; straightforward relational design
- Ranking pipeline design: MEDIUM-HIGH -- signal scorer pattern is clean and testable; exact weight defaults and normalization edge cases need real-world tuning
- Suggestion generation: MEDIUM -- algorithm is straightforward; threshold values (3+ shortlisted papers, etc.) are reasonable defaults but may need adjustment
- Pagination with re-ranking: MEDIUM -- over-fetch approach works for typical use but has theoretical limitations for deep pagination; documented as known limitation

**Research date:** 2026-03-09
**Valid until:** 2026-04-09 (30 days -- stable domain, no external API changes)
