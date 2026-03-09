# Phase 2: Workflow State - Research

**Researched:** 2026-03-09
**Domain:** PostgreSQL workflow tables, SQLAlchemy ORM relationships, CLI subgroups, JSON export/import
**Confidence:** HIGH

## Summary

Phase 2 adds stateful workflow primitives on top of the Phase 1 metadata substrate: collections (named paper groupings), triage states (per-paper lifecycle tracking), saved queries (named search configurations), and watches (saved queries with checkpoint-based delta tracking). All entities use Paper.arxiv_id as their foreign key anchor. The phase requires four new database tables (collections, collection_papers, triage_states, triage_log, saved_queries), a new Alembic migration (002), four service modules, four CLI subgroups, and JSON export/import functionality.

The technical challenges are: (1) designing the association object pattern for collection_papers with extra columns (source, added_at) while maintaining composability with Phase 1's search query builders, (2) implementing "absence means unseen" triage semantics without materializing rows for millions of papers, (3) building saved query serialization that captures all Phase 1 search parameters plus new workflow filters, and (4) implementing checkpoint-based delta tracking for watches using date comparison against paper announcement dates.

The existing codebase provides strong patterns to follow: SQLAlchemy 2.0 async ORM with mapped_column, Alembic hand-written migrations, service layer with async_sessionmaker injection, Click subgroup registration, keyset cursor pagination, and Pydantic model shaping. Phase 2 extends these patterns to new entities without changing any Phase 1 code.

**Primary recommendation:** Follow Phase 1 patterns exactly. Use the association object pattern for collection_papers (extra columns needed). Store triage states as String column with PostgreSQL CHECK constraint (not native ENUM, for migration simplicity). Store saved query parameters as JSONB. Implement watches as a flag + checkpoint columns on saved_queries (not a separate table). Use a simple `re.sub` slugify function (no external dependency).

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Flat collections (no hierarchy/nesting)
- Many-to-many: papers can belong to multiple collections simultaneously
- Slug-style unique names (lowercase, hyphens, no spaces) -- auto-slugify from input
- Collections renamable after creation
- Metadata: name + created_at + updated_at (minimal)
- No limits on collection count or papers per collection
- Sort at query time (default: date added, newest first; options: by paper date, alphabetical)
- Collection listing includes paper counts
- Search/filter within a collection (compose with Phase 1 search)
- Bulk add and bulk remove supported (list of arxiv_ids)
- Track membership source (manual, saved query, agent) on the join table
- Include merge operation (combine two collections)
- Reverse lookup: given a paper, list all its collections
- Delete dissolves grouping by default; optional --purge for orphaned papers
- Collections can be archived (hidden from default listing, queryable with --include-archived)
- Listing papers in a collection includes each paper's triage state
- CLI: `arxiv-mcp collection create/list/delete/add/remove/show/merge/archive`
- Global per-paper triage (not per-collection) -- a paper has one triage state across the system
- Six fixed states: unseen, shortlisted, dismissed, read, cite-later, archived
- States are NOT extensible (fixed enum)
- Free-form transitions (any state to any other, no constraints)
- Default "unseen" inferred from absence (no row = unseen, avoids millions of default rows)
- Triage state transitions logged as audit trail: (paper_id, old_state, new_state, timestamp, source, optional reason)
- Optional reason field on triage transitions
- Batch triage supports both explicit ID lists and query-based bulk operations
- Query-based batch triage: dry-run by default, requires --confirm to execute
- Triage state as a filter dimension composable with search
- Triage state visible in search and browse output (always shown)
- No undo mechanism -- re-triage instead
- Paper version updates: keep triage state, flag the update separately
- CLI: `arxiv-mcp triage mark/list/batch/log` subgroup
- Saved queries are named (slug-style, same convention as collections)
- Saved queries are editable after creation
- Saved queries track usage: run_count and last_run_at
- Saved queries support triage state and collection membership as filter parameters
- "Save from search" workflow
- JSON import/export for saved queries
- Soft limits with warnings for query/watch proliferation
- Saved queries with deleted collection references: query survives, invalid filter skipped with warning
- Watch = saved query + checkpoint metadata (extends, not separate entity)
- Watch cadence hint stored (daily, weekly) -- not enforced, advisory
- Watch checks: on-demand (user/agent triggers explicitly)
- Watch checkpoint auto-advances on check
- Watch delta results: full paper details, paginated
- Check-all command: runs every active watch, returns combined summary
- Watches support pause/resume
- Manual checkpoint reset
- Watch dashboard: list all watches with status, last checked, pending delta estimate, cadence
- Full nuclear reset available (wipes all workflow state, preserves paper corpus, requires --confirm)
- JSON export/import for all workflow state
- Export includes triage transition logs
- Export is configurable/selective
- Archive status for collections (soft removal)
- Stats command: overview with cross-entity insights
- Unified `arxiv-mcp paper show <id>` command
- Search results include triage state and collection context per paper

### Claude's Discretion
- Service layer vs query-builder pattern (recommended: service layer for workflow operations)
- Session management approach (async context managers for transactions)
- Domain models vs ORM models for return types
- Module organization (per-entity vs flat)
- Result envelope type for consistent paginated responses
- Whether to refactor Phase 1 search into the same pattern
- Configuration system vs hardcoded defaults
- Test strategy details
- Error handling details
- Exit code conventions, verbosity flags, output format options
- Delta determination method (date-based checkpoint vs result set diffing)
- Saved query result snapshot (parameters only vs cached result IDs)
- Save-and-watch combined workflow
- Database schema organization (separate vs public schema)
- Alembic migration strategy (single vs per-entity)
- Import merge conflict resolution
- Auto-backup scheduling
- Data retention policy
- Cross-entity JSON export reference resolution
- Integration test scope
- Soft removal history on collection membership
- CLI subgroup naming for queries/watches

### Deferred Ideas (OUT OF SCOPE)
- "Pin to collection" (saved query auto-adds results to a collection) -- Phase 6
- Collection-to-query conversion (derive search params from collection contents) -- Phase 3
- Auto-export on schedule -- low priority
- Interactive notification digests for watches -- Phase 6

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| WKFL-01 | User can create, list, and delete named paper collections | Collection table with slug name, created_at, updated_at, is_archived; service layer with CRUD; Click subgroup `collection create/list/delete` |
| WKFL-02 | User can add papers to and remove papers from collections | CollectionPaper association object with source, added_at columns; bulk add/remove via list of arxiv_ids; merge operation combines two collections |
| WKFL-03 | User can mark paper triage state (unseen, shortlisted, dismissed, read, cite-later) | TriageState table with paper_id FK + state column; absence = unseen; TriageLog audit trail table with old_state, new_state, timestamp, source, reason |
| WKFL-04 | User can create saved queries with parameters, ranking mode, and filters | SavedQuery table with slug name, JSONB params column storing all search/filter parameters; tracks run_count and last_run_at |
| WKFL-05 | User can re-run saved queries on demand | Service method deserializes JSONB params, calls SearchService, updates run_count/last_run_at; handles deleted collection refs gracefully |
| WKFL-06 | User can create watches (saved query + cadence + checkpoint) | Watch columns on SavedQuery: is_watch, cadence_hint, checkpoint_date, last_checked_at, is_paused; no separate table needed |
| WKFL-07 | User can get delta results since last checkpoint | Delta query filters papers with announced_date > checkpoint_date using existing search params; auto-advances checkpoint after check |
| WKFL-08 | User can batch-triage multiple papers in a single operation | Batch triage via explicit ID lists or query-based selection; dry-run by default for query-based; service method with transaction wrapping |

</phase_requirements>

## Standard Stack

### Core (already installed -- no new dependencies)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| SQLAlchemy | 2.0+ | ORM models for 4 new tables, relationships, query composition | Already in use; relationship() + association object pattern for collection_papers |
| asyncpg | 0.30+ | Async PostgreSQL driver | Already in use; no change |
| Alembic | 1.14+ | Hand-written migration 002 for workflow tables | Already in use; same hand-written pattern as migration 001 |
| Pydantic | 2.10+ | Schema models for collection, triage, saved query responses | Already in use; extend models/ with new schemas |
| Click | 8.1+ | CLI subgroups: collection, triage, query, watch | Already in use; same subgroup registration pattern |
| structlog | 24.4+ | Logging for workflow operations | Already in use |
| rich | 13.9+ | Table display for collection listings, triage state, watch dashboard | Already in use |

### Supporting (no new dependencies needed)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python re module | stdlib | Simple slugify function | Auto-slugify collection/query names; 3-line implementation |
| json module | stdlib | Saved query parameter serialization, JSON export/import | JSONB column storage, file export/import |
| datetime module | stdlib | Timestamps for created_at, checkpoint_date | All timestamp fields |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| String + CHECK constraint for triage states | PostgreSQL native ENUM | Native ENUM is harder to alter in migrations; CHECK constraint is simpler to add/remove states later |
| JSONB for saved query params | Dedicated columns per param | JSONB is more flexible; params may evolve; dedicated columns would require schema migration for each new filter type |
| Watch columns on SavedQuery | Separate Watch table | CONTEXT.md says "Watch = saved query + checkpoint metadata (extends, not separate entity)"; columns avoid join overhead |
| Simple re.sub slugify | python-slugify library | Avoid adding a dependency for a 3-line function; no Unicode transliteration needed for English slug names |
| Association object for collection_papers | Plain secondary Table | Association object required because extra columns (source, added_at) are needed on the join table |

**Installation:**
```bash
# No new dependencies -- all requirements already in pyproject.toml
```

## Architecture Patterns

### Recommended Module Structure
```
src/arxiv_mcp/
├── db/
│   ├── models.py              # Add: Collection, CollectionPaper, TriageState, TriageLog, SavedQuery
│   └── queries.py             # Add: workflow query builders (or keep in service layer)
├── workflow/
│   ├── __init__.py
│   ├── collections.py         # CollectionService: CRUD, add/remove, merge, archive, show
│   ├── triage.py              # TriageService: mark, list, batch, log
│   ├── queries.py             # SavedQueryService: create, run, edit, export/import
│   ├── watches.py             # WatchService: create, check, check-all, pause, reset, dashboard
│   ├── export.py              # ExportService: JSON export/import for all workflow state
│   └── cli.py                 # Click subgroups: collection, triage, query (with watch subcommands)
├── models/
│   ├── paper.py               # Extend PaperSummary/SearchResult with triage_state field
│   ├── pagination.py          # Reuse as-is
│   └── workflow.py            # New: Pydantic schemas for Collection, TriageState, SavedQuery, Watch
└── config.py                  # Add: workflow defaults (soft limits, default cadence)
```

### Pattern 1: Association Object for Collection Membership
**What:** Use a full ORM class (not just a Table) for the collection_papers join table to store extra columns (source, added_at).
**When to use:** Collection membership with provenance tracking (WKFL-02).

```python
# Source: SQLAlchemy 2.0 basic_relationships docs
class CollectionPaper(Base):
    """Association object for collection-paper membership with provenance."""
    __tablename__ = "collection_papers"

    collection_id: Mapped[int] = mapped_column(
        ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True
    )
    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"), primary_key=True
    )
    source: Mapped[str] = mapped_column(String(32), default="manual")  # manual, saved_query, agent
    added_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    # Relationships
    collection: Mapped["Collection"] = relationship(back_populates="paper_associations")
    paper: Mapped["Paper"] = relationship()
```

### Pattern 2: Absence-Means-Unseen Triage State
**What:** Only store rows for papers with non-default triage states. "Unseen" is inferred from the absence of a row.
**When to use:** All triage operations (WKFL-03).

```python
class TriageState(Base):
    """Per-paper triage state (global, not per-collection)."""
    __tablename__ = "triage_states"

    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"), primary_key=True
    )
    state: Mapped[str] = mapped_column(String(20))  # shortlisted, dismissed, read, cite-later, archived
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "state IN ('shortlisted', 'dismissed', 'read', 'cite-later', 'archived')",
            name="ck_triage_state_valid",
        ),
    )
```

**Query pattern for resolving triage state:**
```python
# LEFT JOIN to get triage state, defaulting to "unseen" when NULL
from sqlalchemy import case, literal

triage_state_expr = case(
    (TriageState.state.is_(None), literal("unseen")),
    else_=TriageState.state,
).label("triage_state")

stmt = (
    select(Paper, triage_state_expr)
    .outerjoin(TriageState, Paper.arxiv_id == TriageState.paper_id)
)
```

### Pattern 3: JSONB Saved Query Parameters
**What:** Store all search parameters as a JSONB column so saved queries survive schema evolution.
**When to use:** Saved query storage and re-execution (WKFL-04, WKFL-05).

```python
class SavedQuery(Base):
    """Named, reusable search query with optional watch functionality."""
    __tablename__ = "saved_queries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Usage tracking
    run_count: Mapped[int] = mapped_column(Integer, default=0)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Watch fields (nullable -- not all queries are watches)
    is_watch: Mapped[bool] = mapped_column(Boolean, default=False)
    cadence_hint: Mapped[str | None] = mapped_column(String(20))  # daily, weekly
    checkpoint_date: Mapped[date | None] = mapped_column(Date)
    last_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    is_paused: Mapped[bool] = mapped_column(Boolean, default=False)
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
```

**JSONB params schema:**
```json
{
  "query_text": "transformer attention",
  "title": null,
  "author": null,
  "category": "cs.CL",
  "date_from": "2024-01-01",
  "date_to": null,
  "time_basis": "announced",
  "page_size": 20,
  "triage_filter": ["shortlisted", "read"],
  "collection_filter": "my-reading-list",
  "ranking_mode": "relevance"
}
```

### Pattern 4: Service Layer with Session Factory Injection
**What:** Follow the SearchService pattern: inject async_sessionmaker, manage sessions internally, return Pydantic models.
**When to use:** All workflow services (WKFL-01 through WKFL-08).

```python
class CollectionService:
    """Orchestrates collection CRUD and membership operations."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    async def create_collection(self, name: str) -> CollectionDetail:
        slug = slugify(name)
        async with self.session_factory() as session:
            collection = Collection(slug=slug, name=name, ...)
            session.add(collection)
            await session.commit()
            return CollectionDetail.from_orm(collection)
```

### Pattern 5: Click Subgroup Registration
**What:** Register new subgroups the same way Phase 1 registers harvest and search.
**When to use:** CLI entry points (collection, triage, query subgroups).

```python
# In cli.py -- same pattern as search_group registration
from arxiv_mcp.workflow.cli import collection_group, triage_group, query_group
cli.add_command(collection_group)
cli.add_command(triage_group)
cli.add_command(query_group)
```

### Pattern 6: Composing Workflow Filters with Phase 1 Search
**What:** Extend Phase 1's build_search_query with optional triage state and collection membership filters via JOINs.
**When to use:** When search results need triage state display (always) and when filtering by triage state or collection membership.

```python
def build_search_query_with_workflow(
    *,
    # ... all Phase 1 params ...
    triage_filter: list[str] | None = None,
    collection_slug: str | None = None,
) -> Select:
    """Build search query with optional workflow state joins."""
    # Start with base search query components
    stmt = build_search_query(...)  # Phase 1 query

    # Always LEFT JOIN triage state for display
    stmt = stmt.outerjoin(TriageState, Paper.arxiv_id == TriageState.paper_id)
    stmt = stmt.add_columns(
        case((TriageState.state.is_(None), literal("unseen")), else_=TriageState.state).label("triage_state")
    )

    # Filter by triage state if requested
    if triage_filter:
        if "unseen" in triage_filter:
            # unseen = no row in triage_states
            others = [s for s in triage_filter if s != "unseen"]
            if others:
                stmt = stmt.where(or_(TriageState.state.is_(None), TriageState.state.in_(others)))
            else:
                stmt = stmt.where(TriageState.state.is_(None))
        else:
            stmt = stmt.where(TriageState.state.in_(triage_filter))

    # Filter by collection membership
    if collection_slug:
        stmt = stmt.join(CollectionPaper, Paper.arxiv_id == CollectionPaper.paper_id)
        stmt = stmt.join(Collection, CollectionPaper.collection_id == Collection.id)
        stmt = stmt.where(Collection.slug == collection_slug)

    return stmt
```

### Anti-Patterns to Avoid
- **Materializing "unseen" rows:** Do NOT insert a triage_state row for every paper. With millions of papers, this wastes storage and slows INSERTs. Use LEFT JOIN + COALESCE/CASE instead.
- **Using PostgreSQL native ENUM for triage states:** Native ENUMs require `ALTER TYPE ... ADD VALUE` which cannot be rolled back in a transaction. Use VARCHAR + CHECK constraint for easier evolution.
- **Storing saved query parameters as individual columns:** The parameter set will evolve (new filters in later phases). JSONB allows schema-free evolution without migrations.
- **Separate Watch table:** CONTEXT.md explicitly says "Watch = saved query + checkpoint metadata (extends, not separate entity)." Use nullable columns on SavedQuery.
- **Modifying Phase 1 query builders directly:** Compose by wrapping, not by editing. Add workflow-aware wrappers that call existing builders and add JOINs.
- **Per-collection triage state:** CONTEXT.md explicitly locks this as "Global per-paper (not per-collection)."

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Slug generation | External library (python-slugify) | Simple `re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')` | 3-line function; no Unicode transliteration needed for slug names in this context |
| Cursor pagination | New pagination system | Existing `models/pagination.py` Cursor + PageInfo | Phase 1 already solved this; reuse for collection listing and delta results |
| JSON serialization | Custom serializers | Pydantic model_dump_json() with custom encoders | Pydantic handles datetime, date, enum serialization out of the box |
| Transaction management | Manual begin/commit/rollback | Existing `get_session` context manager or `async with session_factory() as session` | Phase 1 pattern handles commit-on-success, rollback-on-error |
| Audit logging | External audit library | TriageLog table with explicit INSERT on state change | Simple, queryable, no external dependency; ~5 lines of code per triage operation |
| Date-based deltas | Complex result-set diffing | Simple WHERE announced_date > checkpoint_date on existing search | CONTEXT.md leaves delta method to discretion; date-based is simplest, most reliable |

**Key insight:** Phase 2 adds no new external dependencies. Every capability is built from existing libraries (SQLAlchemy, Alembic, Click, Pydantic, Rich) already in pyproject.toml. The entire phase is new tables + new service code + new CLI commands.

## Common Pitfalls

### Pitfall 1: LEFT JOIN Changes Result Shape
**What goes wrong:** Adding LEFT JOIN for triage state to existing search queries changes the row structure. Code expecting (Paper, rank) now gets (Paper, rank, triage_state). Existing result shaping breaks.
**Why it happens:** shape_search_results() expects row[0] = Paper, row[1] = rank. Adding triage_state adds row[2].
**How to avoid:** Create new result shaping functions for workflow-aware queries that handle the additional column. Do NOT modify shape_search_results() -- extend it or create a parallel function.
**Warning signs:** TypeError or IndexError in shape_search_results after adding workflow JOINs.

### Pitfall 2: N+1 Queries for Collection Paper Counts
**What goes wrong:** Listing collections with paper counts by iterating and counting in Python creates N+1 queries.
**Why it happens:** Natural ORM pattern: `for c in collections: count = len(c.papers)`.
**How to avoid:** Use a subquery to count papers: `select(Collection, func.count(CollectionPaper.paper_id)).outerjoin(CollectionPaper).group_by(Collection.id)`.
**Warning signs:** Slow collection listing, increasing query count in logs proportional to collection count.

### Pitfall 3: Batch Triage Transaction Size
**What goes wrong:** Query-based batch triage selects thousands of papers and tries to UPDATE + INSERT log entries in a single transaction. Transaction holds locks too long or runs out of memory.
**Why it happens:** Unrestricted query-based triage against a large result set.
**How to avoid:** Process in batches (e.g., 500 at a time within the transaction). Report total affected count. The dry-run requirement (locked decision) helps by previewing count before committing.
**Warning signs:** Long-running transactions, lock contention on triage_states table.

### Pitfall 4: Saved Query JSONB Schema Drift
**What goes wrong:** Old saved queries reference parameters that no longer exist or miss new required parameters. Re-running fails with KeyError or unexpected behavior.
**Why it happens:** Saved queries persist indefinitely. The parameter schema evolves across phases.
**How to avoid:** Design a parameter deserialization function that provides defaults for missing keys and ignores unknown keys. Version the params schema or use defensive key access: `params.get("triage_filter", None)`.
**Warning signs:** Errors when re-running saved queries created in an earlier phase.

### Pitfall 5: Watch Checkpoint Date vs Paper Date Semantics
**What goes wrong:** Using submission_date for delta comparison when the saved query's time_basis is "announced" produces incorrect deltas (papers appear multiple times or never).
**Why it happens:** Watch delta must use the same time_basis as the underlying saved query's search parameters.
**How to avoid:** Extract time_basis from saved query params. Use the same date column for delta filtering as the underlying search uses for ordering. Default to announced_date.
**Warning signs:** Duplicate papers in delta results, papers showing as "new" that were already seen.

### Pitfall 6: Slug Collision on Rename
**What goes wrong:** Renaming a collection to a name that auto-slugifies to an existing slug causes a unique constraint violation.
**Why it happens:** Slug uniqueness is enforced at the database level (correct), but the error message is unhelpful.
**How to avoid:** Check for slug existence before rename. Return a clear error message ("Collection with slug 'X' already exists"). The same applies to saved query naming.
**Warning signs:** IntegrityError on rename operations.

### Pitfall 7: Circular Import with Workflow Models
**What goes wrong:** Adding workflow ORM models to db/models.py that reference Paper creates import order issues when workflow service modules also import from db/models.py.
**Why it happens:** All models in a single file with circular relationship references.
**How to avoid:** Keep ALL ORM models in db/models.py (they must share the same Base). Use string-based forward references in relationship(): `relationship("Paper")` not `relationship(Paper)`. Import the model class only in type hints with `TYPE_CHECKING`.
**Warning signs:** ImportError at module load time.

## Code Examples

### Slugify Function (No External Dependency)
```python
import re

def slugify(text: str) -> str:
    """Convert text to URL-safe slug (lowercase, hyphens, no spaces)."""
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    return slug.strip('-')
```

### Collection Merge Operation
```python
async def merge_collections(
    self, source_slug: str, target_slug: str
) -> CollectionDetail:
    """Merge source collection into target. Source is deleted after merge."""
    async with self.session_factory() as session:
        source = await self._get_by_slug(session, source_slug)
        target = await self._get_by_slug(session, target_slug)

        # Move all papers from source to target (skip duplicates)
        stmt = (
            select(CollectionPaper)
            .where(CollectionPaper.collection_id == source.id)
        )
        result = await session.execute(stmt)
        source_memberships = result.scalars().all()

        for membership in source_memberships:
            # Check if paper already in target
            existing = await session.execute(
                select(CollectionPaper).where(
                    CollectionPaper.collection_id == target.id,
                    CollectionPaper.paper_id == membership.paper_id,
                )
            )
            if not existing.scalar_one_or_none():
                new_membership = CollectionPaper(
                    collection_id=target.id,
                    paper_id=membership.paper_id,
                    source=membership.source,
                    added_at=membership.added_at,
                )
                session.add(new_membership)

        # Delete source collection (CASCADE deletes its memberships)
        await session.delete(source)
        await session.commit()
        return await self._get_detail(session, target.id)
```

### Watch Delta Check
```python
async def check_watch(self, slug: str) -> PaginatedResponse[SearchResult]:
    """Check a watch for new papers since last checkpoint."""
    async with self.session_factory() as session:
        query = await self._get_by_slug(session, slug)
        if not query.is_watch:
            raise ValueError(f"'{slug}' is not a watch")
        if query.is_paused:
            raise ValueError(f"Watch '{slug}' is paused")

        params = query.params.copy()
        # Override date_from with checkpoint
        if query.checkpoint_date:
            params["date_from"] = query.checkpoint_date.isoformat()

        # Run the search with checkpoint-based date filter
        results = await self.search_service.search_papers(**self._deserialize_params(params))

        # Auto-advance checkpoint
        now = datetime.now(timezone.utc)
        query.checkpoint_date = now.date()
        query.last_checked_at = now
        query.run_count = (query.run_count or 0) + 1
        query.last_run_at = now
        await session.commit()

        return results
```

### Triage Batch with Audit Trail
```python
async def batch_triage(
    self,
    paper_ids: list[str],
    new_state: str,
    source: str = "manual",
    reason: str | None = None,
) -> int:
    """Batch-triage multiple papers. Returns count of papers affected."""
    async with self.session_factory() as session:
        affected = 0
        for paper_id in paper_ids:
            old_state = await self._get_state(session, paper_id)
            if old_state == new_state:
                continue  # No change needed

            # Upsert triage state
            if old_state == "unseen":
                # INSERT new row
                ts = TriageState(paper_id=paper_id, state=new_state, updated_at=now)
                session.add(ts)
            else:
                # UPDATE existing row
                stmt = (
                    update(TriageState)
                    .where(TriageState.paper_id == paper_id)
                    .values(state=new_state, updated_at=now)
                )
                await session.execute(stmt)

            # Log transition
            log = TriageLog(
                paper_id=paper_id,
                old_state=old_state,
                new_state=new_state,
                timestamp=now,
                source=source,
                reason=reason,
            )
            session.add(log)
            affected += 1

        await session.commit()
        return affected
```

### JSON Export Structure
```python
{
    "version": "1.0",
    "exported_at": "2026-03-09T12:00:00Z",
    "collections": [
        {
            "slug": "my-reading-list",
            "name": "My Reading List",
            "is_archived": false,
            "created_at": "2026-03-01T10:00:00Z",
            "papers": [
                {"arxiv_id": "2301.00001", "source": "manual", "added_at": "..."}
            ]
        }
    ],
    "triage_states": [
        {"paper_id": "2301.00001", "state": "shortlisted", "updated_at": "..."}
    ],
    "triage_log": [
        {"paper_id": "2301.00001", "old_state": "unseen", "new_state": "shortlisted", "timestamp": "...", "source": "manual", "reason": "interesting method"}
    ],
    "saved_queries": [
        {
            "slug": "daily-transformers",
            "name": "Daily Transformers",
            "params": {"query_text": "transformer", "category": "cs.CL"},
            "run_count": 15,
            "is_watch": true,
            "cadence_hint": "daily",
            "checkpoint_date": "2026-03-08",
            "is_paused": false
        }
    ]
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Separate association table (no ORM class) | Association object pattern with Mapped class | SQLAlchemy 2.0 (2023+) | Extra columns on join tables now have first-class ORM support |
| PostgreSQL native ENUM | VARCHAR + CHECK constraint | Best practice for evolving schemas | Easier to alter; CHECK constraints are transactional |
| Column-per-parameter saved queries | JSONB parameter storage | PostgreSQL 9.4+ (mainstream) | Schema-free evolution; no migration needed for new filter types |
| SQLAlchemy 1.x backref | Explicit back_populates | SQLAlchemy 2.0 (2023+) | Better type safety, IDE support, no implicit magic |
| Separate Watch model | Watch as extension of SavedQuery (columns) | Domain modeling decision | Matches user's mental model; simpler schema; fewer JOINs |

**Deprecated/outdated:**
- **SQLAlchemy Table() for secondary with extra columns:** Use association object pattern (full ORM class) instead of Table() when join table has additional columns.
- **Python Enum with native_enum=True for PostgreSQL:** Avoid for columns that may need new values; ALTER TYPE ADD VALUE is non-transactional.

## Open Questions

1. **Search result augmentation strategy**
   - What we know: CONTEXT.md requires triage state visible in all search/browse output. This means modifying how results are shaped.
   - What's unclear: Should this be done by modifying Phase 1's SearchService methods (adding optional triage join) or by creating a new WorkflowSearchService that wraps SearchService?
   - Recommendation: Create a thin wrapper or compose at the query level. Do NOT modify existing SearchService methods. Add a new function `build_search_query_with_workflow()` that calls `build_search_query()` and adds the triage LEFT JOIN. Create a parallel `WorkflowSearchResult` model that includes triage_state.

2. **Import merge conflict resolution**
   - What we know: JSON import must handle conflicts (e.g., collection slug already exists, paper already in collection with different triage state).
   - What's unclear: Whether to use "last write wins," "skip conflicts," or "interactive resolution."
   - Recommendation: Default "skip with warning" for collections and saved queries (don't overwrite existing slugs). For triage states, use "last write wins" (most recent timestamp takes precedence). Report all conflicts in the import summary.

3. **Collection paper listing sort with triage state**
   - What we know: Listing papers in a collection includes triage state. Sort options are: date added, paper date, alphabetical.
   - What's unclear: How triage state interacts with sort order.
   - Recommendation: Triage state is displayed alongside each paper but is not a sort dimension. It can be used as a filter (e.g., "show only shortlisted papers in this collection").

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
| WKFL-01 | Create, list, delete collections | integration | `uv run pytest tests/test_workflow/test_collections.py::TestCollectionCRUD -x` | Wave 0 |
| WKFL-02 | Add/remove papers, bulk ops, merge | integration | `uv run pytest tests/test_workflow/test_collections.py::TestCollectionMembership -x` | Wave 0 |
| WKFL-03 | Mark triage state, audit trail | integration | `uv run pytest tests/test_workflow/test_triage.py::TestTriageState -x` | Wave 0 |
| WKFL-04 | Create saved queries with params | integration | `uv run pytest tests/test_workflow/test_queries.py::TestSavedQueryCRUD -x` | Wave 0 |
| WKFL-05 | Re-run saved queries | integration | `uv run pytest tests/test_workflow/test_queries.py::TestSavedQueryRun -x` | Wave 0 |
| WKFL-06 | Create watches from saved queries | integration | `uv run pytest tests/test_workflow/test_watches.py::TestWatchCreate -x` | Wave 0 |
| WKFL-07 | Delta results since checkpoint | integration | `uv run pytest tests/test_workflow/test_watches.py::TestWatchDelta -x` | Wave 0 |
| WKFL-08 | Batch triage (list + query-based) | integration | `uv run pytest tests/test_workflow/test_triage.py::TestBatchTriage -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/ -x --timeout=30`
- **Per wave merge:** `uv run pytest tests/ -v --cov=src/arxiv_mcp`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_workflow/__init__.py` -- package init
- [ ] `tests/test_workflow/conftest.py` -- shared fixtures (test DB with workflow tables, sample collections/triage data)
- [ ] `tests/test_workflow/test_collections.py` -- stubs for WKFL-01, WKFL-02
- [ ] `tests/test_workflow/test_triage.py` -- stubs for WKFL-03, WKFL-08
- [ ] `tests/test_workflow/test_queries.py` -- stubs for WKFL-04, WKFL-05
- [ ] `tests/test_workflow/test_watches.py` -- stubs for WKFL-06, WKFL-07
- [ ] Workflow table creation in test conftest (extending Phase 1's test_session pattern)
- [ ] Sample collection/triage/saved query test data factory functions

## Sources

### Primary (HIGH confidence)
- [SQLAlchemy 2.0 Basic Relationship Patterns](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html) -- association object pattern, many-to-many with extra columns, back_populates
- [SQLAlchemy 2.0 PostgreSQL Dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) -- JSONB type, ARRAY type, native_enum parameter
- [SQLAlchemy 2.0 Constraints](https://docs.sqlalchemy.org/en/20/core/constraints.html) -- CheckConstraint for enum-like validation
- [Click 8.3 Commands and Groups](https://click.palletsprojects.com/en/stable/commands/) -- nested subgroups, command registration
- Existing Phase 1 codebase (verified by reading all source files) -- established patterns for engine, sessions, models, queries, CLI, pagination

### Secondary (MEDIUM confidence)
- [Alembic 1.18 Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html) -- hand-written migration patterns, async engine support
- [SQLAlchemy asyncpg Discussion #5913](https://github.com/sqlalchemy/sqlalchemy/discussions/5913) -- async many-to-many query patterns
- [Alembic async migration Discussion #1208](https://github.com/sqlalchemy/alembic/discussions/1208) -- async migration runner configuration

### Tertiary (LOW confidence)
- Web search results for slug implementation patterns -- verified simple re.sub approach is sufficient for ASCII slugs
- Web search results for PostgreSQL ENUM vs CHECK constraint -- consensus that CHECK is easier to evolve

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- no new dependencies; all libraries already proven in Phase 1
- Architecture: HIGH -- follows established Phase 1 patterns exactly; association object pattern well-documented
- Database schema: HIGH -- straightforward relational design; all patterns verified against SQLAlchemy 2.0 docs
- Pitfalls: HIGH -- identified from direct codebase analysis and known SQLAlchemy/PostgreSQL patterns
- Watch delta mechanism: MEDIUM -- date-based checkpoint is simple and reliable but exact edge cases (timezone, announcement timing) need careful handling
- Import conflict resolution: MEDIUM -- "skip with warning" is sensible but untested at scale

**Research date:** 2026-03-09
**Valid until:** 2026-04-09 (30 days -- stable domain, no external API changes)
