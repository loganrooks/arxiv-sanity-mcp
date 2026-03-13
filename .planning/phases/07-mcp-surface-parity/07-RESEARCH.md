# Phase 7: MCP Surface Parity - Research

**Researched:** 2026-03-12
**Domain:** MCP tool wiring -- exposing existing Python services through MCP protocol
**Confidence:** HIGH

## Summary

Phase 7 is a wiring phase, not a feature phase. All business logic already exists in `ProfileRankingService`, `SuggestionService`, `ProfileService`, and `WorkflowSearchService`. The implementation work consists of (1) adding two services to `AppContext`, (2) rerouting two existing discovery tools through the richer service chain, and (3) adding two new tool functions.

The research identified one critical architectural gap: `AppContext.search` is `SearchService` (bare results), but the CLI goes through `WorkflowSearchService` then `ProfileRankingService`. MCP discovery tools currently return `SearchResult` (paper + score only), while the CLI returns `WorkflowSearchResult` (paper + score + triage_state + collection_slugs) and optionally `ProfileSearchResult` (+ ranking_explanation). Fixing this requires changing how `app_lifespan()` initializes and composes services, and how `search_papers`/`browse_recent` tools delegate.

All patterns are already established: tool registration via `@mcp.tool()`, dict returns via `.model_dump(mode="json")`, `_get_app(ctx)` helpers, `{"error": ...}` error handling. The test pattern uses mock `AppContext` with `AsyncMock` services. Phase 7 follows these patterns exactly.

**Primary recommendation:** Add `ProfileRankingService` and `SuggestionService` to `AppContext`, reroute discovery tools through `ProfileRankingService` (which wraps `WorkflowSearchService` which wraps `SearchService`), and add `create_profile` + `suggest_signals` as new tools in `interest.py`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

1. **AppContext Expansion** -- Add `ProfileRankingService` and `SuggestionService` to `AppContext` dataclass and initialize in `app_lifespan()`. Field names: `profile_ranking` and `suggestions`.

2. **Discovery Tool Enhancement** -- Add `profile_slug: str | None = None` parameter to `search_papers` and `browse_recent`. When None, current behavior unchanged. When provided, call `app.profile_ranking.search_papers(profile_slug=..., ...)` and return `ProfileSearchResponse`.

3. **WorkflowSearchResult enrichment** -- `search_papers` and `browse_recent` must return `WorkflowSearchResult`-enriched results (triage_state, collection_slugs) not bare `SearchResult`.

4. **New Tool: create_profile** -- In `interest.py`. Parameters: `name: str` (required), `negative_weight: float | None = None`. Returns `ProfileSummary.model_dump(mode="json")`.

5. **New Tool: suggest_signals** -- In `interest.py`. Parameters: `profile_slug: str` (required), `auto_add: bool = False`. Returns dict with `candidates` list and `added_count`.

6. **Response format for profile-ranked results** -- Use `ProfileSearchResponse.model_dump(mode="json")` which bundles results + snapshot.

7. **SuggestionCandidate is a dataclass** -- Serialize manually via `asdict()` or explicit dict construction (not `.model_dump()`).

8. **No new business logic** -- MCP wraps existing services only.

### Claude's Discretion

- Whether to add `explain: bool = False` parameter to discovery tools (CLI has `--explain` flag) or always include explanations when profile_slug is present
- Whether `find_related_papers` should also support `profile_slug`
- Test file organization: extend existing test files vs. create new ones
- Whether `SuggestionCandidate` should be converted to Pydantic or keep manual dict conversion

### Deferred Ideas (OUT OF SCOPE)

- Suggestion confirmation UI flow (confirm/dismiss individual suggestions)
- Profile description field
- Profile snapshots / version history
- Bulk triage via MCP
- Cross-source relatedness in MCP (OpenAlex related_works)
</user_constraints>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| mcp | 1.26.0 | MCP protocol SDK | Project dependency, FastMCP lifespan pattern |
| FastMCP | (bundled in mcp) | Tool/resource/prompt registration | `@mcp.tool()` decorator pattern |
| SQLAlchemy | 2.0+ | Async ORM, session factory | All services use `async_sessionmaker` |
| Pydantic | 2.10+ | Model serialization | `.model_dump(mode="json")` for MCP transport |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| dataclasses | stdlib | `SuggestionCandidate`, `AppContext` | Dataclass serialization via `asdict()` |
| pytest | 9.0.2 | Test framework | All unit tests |
| pytest-asyncio | (auto mode) | Async test support | `asyncio_mode = "auto"` in pyproject.toml |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual `asdict()` for SuggestionCandidate | Convert to Pydantic | More consistent `.model_dump()` but unnecessary churn for 4 fields; manual dict is fine |
| Always include explanations | Add `explain` param | CLI has `--explain` as opt-in but MCP callers always want ranking_explanation when using profiles; always include is simpler |

## Architecture Patterns

### Service Composition Chain

The critical architectural pattern is the service wrapping chain:

```
SearchService (bare results)
  -> WorkflowSearchService (adds triage_state, collection_slugs)
    -> ProfileRankingService (adds ranking_explanation, ranker_snapshot)
```

The CLI already builds this chain in `_get_profile_ranking_service()` (search/cli.py:48-70). Phase 7 replicates this in `app_lifespan()`.

### Current vs Target AppContext

**Current** (`server.py` line 36):
```python
@dataclass
class AppContext:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    settings: Settings
    search: SearchService           # <-- bare, no workflow enrichment
    collections: CollectionService
    triage: TriageService
    saved_queries: SavedQueryService
    watches: WatchService
    profiles: ProfileService
    enrichment: EnrichmentService
    content: ContentService
```

**Target:**
```python
@dataclass
class AppContext:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    settings: Settings
    search: SearchService
    collections: CollectionService
    triage: TriageService
    saved_queries: SavedQueryService
    watches: WatchService
    profiles: ProfileService
    enrichment: EnrichmentService
    content: ContentService
    profile_ranking: ProfileRankingService   # NEW
    suggestions: SuggestionService           # NEW
```

### Initialization Order in app_lifespan()

Dependencies dictate initialization order:
1. `SearchService(sf, settings)` -- no deps
2. `WorkflowSearchService(sf, settings, search)` -- needs SearchService
3. `ProfileRankingService(sf, settings, workflow_svc)` -- needs WorkflowSearchService
4. `ProfileService(sf, settings)` -- no service deps
5. `SuggestionService(sf, settings, profiles)` -- needs ProfileService

Note: `WorkflowSearchService` is an intermediate service -- it is NOT added to `AppContext` as a field. It is constructed in `app_lifespan()` only to be passed to `ProfileRankingService.__init__()`. This mirrors the CLI pattern where `_get_profile_ranking_service()` constructs the chain internally.

### Tool Function Pattern

Every MCP tool follows the same structure (from Phase 04.1):

```python
from arxiv_mcp.mcp.server import AppContext, mcp

def _get_app(ctx: Context) -> AppContext:
    return ctx.request_context.lifespan_context

@mcp.tool()
async def tool_name(
    param1: type,
    param2: type = default,
    ctx: Context = None,
) -> dict:
    """Docstring describes user intent."""
    app = _get_app(ctx)
    try:
        result = await app.service.method(...)
    except ValueError as e:
        return {"error": str(e)}
    return result.model_dump(mode="json")
```

### Discovery Tool Enhancement Pattern

The `search_papers` tool needs branching logic based on `profile_slug`:

```python
@mcp.tool()
async def search_papers(
    query: str | None = None,
    # ... existing params ...
    profile_slug: str | None = None,    # NEW
    ctx: Context = None,
) -> dict:
    app = _get_app(ctx)
    parsed_date_from = date.fromisoformat(date_from) if date_from else None
    parsed_date_to = date.fromisoformat(date_to) if date_to else None

    search_kwargs = dict(
        query_text=query,
        title=title,
        author=author,
        category=category,
        date_from=parsed_date_from,
        date_to=parsed_date_to,
        time_basis=time_basis,
        page_size=page_size,
        cursor_token=cursor,
    )

    # ProfileRankingService handles both paths:
    # - profile_slug=None -> delegates to WorkflowSearchService (workflow-enriched)
    # - profile_slug=provided -> over-fetches, re-ranks, adds explanations
    result = await app.profile_ranking.search_papers(
        profile_slug=profile_slug,
        **search_kwargs,
    )
    return result.model_dump(mode="json")
```

Key insight: `ProfileRankingService.search_papers(profile_slug=None)` already handles the no-profile case by delegating to `WorkflowSearchService` and wrapping results as `ProfileSearchResult` without ranking_explanation. This means the discovery tools can ALWAYS go through `profile_ranking` -- the service handles both paths internally. This automatically fixes the WorkflowSearchResult gap (success criteria 2) while also enabling profile-ranked search (success criteria 1).

### SuggestionCandidate Serialization

`SuggestionCandidate` is a `dataclass` (not Pydantic). Use `dataclasses.asdict()`:

```python
from dataclasses import asdict

candidates = await app.suggestions.generate_suggestions(profile_slug)
return {
    "candidates": [asdict(c) for c in candidates],
    "added_count": 0,
}
```

### Test Pattern

All MCP tool tests use mock `AppContext` (from `tests/test_mcp/conftest.py`):

```python
@pytest.fixture
def mock_app_context():
    ctx = MagicMock(spec=AppContext)
    ctx.search = AsyncMock()
    # ... mock each service
    return ctx

@pytest.fixture
def mock_ctx(mock_app_context):
    ctx = MagicMock()
    ctx.request_context.lifespan_context = mock_app_context
    return ctx
```

Tests call tool functions directly with `mock_ctx`, assert service method was awaited with correct args, and verify the return type is `dict`.

### Anti-Patterns to Avoid

- **Adding WorkflowSearchService to AppContext:** It is an internal composition detail. Only `profile_ranking` should be on AppContext. Discovery tools always go through `profile_ranking`.
- **Modifying SearchService or WorkflowSearchService:** Phase 7 composes by wrapping, not by editing. No changes to existing service code.
- **Returning Pydantic models from tools:** MCP transport requires JSON-serializable dicts. Always `.model_dump(mode="json")`.
- **Throwing exceptions from tools:** Always catch and return `{"error": ...}` dict.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Profile-ranked search | Custom re-ranking in tool layer | `ProfileRankingService.search_papers()` | Over-fetch, score, sort, trim logic already correct + tested |
| Workflow enrichment | Manual triage/collection queries in tool | `WorkflowSearchService` (via ProfileRankingService) | Batch N+1 avoidance already implemented |
| Profile creation | Direct ORM in tool | `ProfileService.create_profile()` | Slug collision checks, soft limits, timestamp management |
| Suggestion generation | Custom suggestion logic in tool | `SuggestionService.generate_suggestions()` | Threshold logic, exclusion sets, multi-type generation |
| Serialization of results | Manual dict construction | `.model_dump(mode="json")` / `asdict()` | Consistent with all other tools |

**Key insight:** Phase 7 should contain zero business logic. Every tool is a thin wrapper: parse params, call service, serialize response, handle errors.

## Common Pitfalls

### Pitfall 1: Breaking Existing Tool Signatures
**What goes wrong:** Adding `profile_slug` to `search_papers` changes the MCP tool schema. Existing clients that do not send `profile_slug` must continue working identically.
**Why it happens:** Forgetting that `profile_slug=None` is the default and must produce the same result shape as before.
**How to avoid:** `ProfileRankingService.search_papers(profile_slug=None)` wraps results as `ProfileSearchResult` (which has all `WorkflowSearchResult` fields plus `ranking_explanation=None`). The serialized dict shape will have additional keys (`triage_state`, `collection_slugs`, `ranking_explanation`) compared to the old bare `SearchResult`. This is an additive change -- existing clients that ignore unknown keys will work fine. But tests must verify backward compatibility.
**Warning signs:** Old tests failing because result dict shape changed (now has `triage_state` etc).

### Pitfall 2: Mock AppContext Spec Mismatch
**What goes wrong:** Adding `profile_ranking` and `suggestions` to `AppContext` changes the dataclass spec. The test fixture `mock_app_context` uses `MagicMock(spec=AppContext)` -- this will fail if the spec doesn't include the new fields.
**Why it happens:** `spec=AppContext` validates attribute access. New fields must exist.
**How to avoid:** Update `tests/test_mcp/conftest.py` to include `ctx.profile_ranking = AsyncMock()` and `ctx.suggestions = AsyncMock()` in the `mock_app_context` fixture.
**Warning signs:** `AttributeError: Mock object has no attribute 'profile_ranking'` in tests.

### Pitfall 3: SuggestionCandidate Is Not Pydantic
**What goes wrong:** Calling `.model_dump()` on a `SuggestionCandidate` raises `AttributeError`.
**Why it happens:** It is a `dataclass`, not a `BaseModel`.
**How to avoid:** Use `dataclasses.asdict(candidate)` for serialization.
**Warning signs:** `AttributeError: 'SuggestionCandidate' object has no attribute 'model_dump'`.

### Pitfall 4: ProfileSearchResponse Result Shape
**What goes wrong:** `ProfileSearchResponse.model_dump(mode="json")` produces `{"results": {"items": [...], "page_info": {...}}, "ranker_snapshot": {...}}`. This is a different top-level shape than the current `search_papers` return (which is `{"items": [...], "page_info": {...}}`).
**Why it happens:** `ProfileSearchResponse` wraps `PaginatedResponse` inside a `results` key.
**How to avoid:** This shape change is intentional and necessary. The response now has two top-level keys: `results` (paginated items) and `ranker_snapshot` (profile config). When `profile_slug=None`, `ranker_snapshot` is `null`. Document this in the tool docstring.
**Warning signs:** Clients expecting `result["items"]` instead of `result["results"]["items"]`.

### Pitfall 5: Service Dependency Ordering
**What goes wrong:** `ProfileRankingService` needs `WorkflowSearchService`, which needs `SearchService`. Creating them out of order causes `NameError` or `None` references.
**Why it happens:** Dataclass fields don't enforce creation order; `app_lifespan()` must sequence manually.
**How to avoid:** Follow the CLI pattern in `_get_profile_ranking_service()`: SearchService first, WorkflowSearchService second, ProfileRankingService third.
**Warning signs:** `AttributeError: 'NoneType' object has no attribute 'search_papers'` at runtime.

### Pitfall 6: ProfileRankingService Constructor Signature
**What goes wrong:** `ProfileRankingService.__init__` takes `workflow_search_service` as a parameter (not `search_service`). Passing the wrong service type produces incorrect results.
**Why it happens:** The parameter name is `workflow_search_service` but the type hint is `object` (duck typing).
**How to avoid:** Pass the `WorkflowSearchService` instance, not the `SearchService` instance.
**Warning signs:** Calls to `self.workflow_search.search_papers()` return `SearchResult` instead of `WorkflowSearchResult`.

## Code Examples

### AppContext Expansion (server.py)

```python
# Source: Existing pattern in server.py + CLI chain in search/cli.py:48-70

from arxiv_mcp.interest.search_augment import ProfileRankingService
from arxiv_mcp.interest.suggestions import SuggestionService
from arxiv_mcp.workflow.search_augment import WorkflowSearchService

@dataclass
class AppContext:
    # ... existing fields ...
    profile_ranking: ProfileRankingService
    suggestions: SuggestionService

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)

    search = SearchService(sf, settings)
    workflow_search = WorkflowSearchService(sf, settings, search)  # intermediate
    collections = CollectionService(sf, settings)
    triage = TriageService(sf, settings)
    saved_queries = SavedQueryService(sf, settings, search)
    watches = WatchService(sf, settings, search)
    profiles = ProfileService(sf, settings)
    enrichment = EnrichmentService(sf, settings)
    content = ContentService(sf, settings)
    profile_ranking = ProfileRankingService(sf, settings, workflow_search)
    suggestions = SuggestionService(sf, settings, profiles)

    try:
        yield AppContext(
            engine=engine,
            session_factory=sf,
            settings=settings,
            search=search,
            collections=collections,
            triage=triage,
            saved_queries=saved_queries,
            watches=watches,
            profiles=profiles,
            enrichment=enrichment,
            content=content,
            profile_ranking=profile_ranking,
            suggestions=suggestions,
        )
    finally:
        await engine.dispose()
```

### Enhanced search_papers Tool (discovery.py)

```python
# Source: Existing search_papers + CLI pattern in search/cli.py:234-268

@mcp.tool()
async def search_papers(
    query: str | None = None,
    title: str | None = None,
    author: str | None = None,
    category: str | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
    time_basis: str = "announced",
    page_size: int = 20,
    cursor: str | None = None,
    profile_slug: str | None = None,
    ctx: Context = None,
) -> dict:
    """Search for arXiv papers by text, title, author, or category.

    Returns paginated results with paper metadata and relevance scores.
    Optionally provide profile_slug to get profile-ranked results with
    ranking explanations on each result.

    Without profile_slug: results include triage_state and collection_slugs.
    With profile_slug: results additionally include ranking_explanation
    and the response includes a ranker_snapshot.
    """
    app = _get_app(ctx)
    parsed_date_from = date.fromisoformat(date_from) if date_from else None
    parsed_date_to = date.fromisoformat(date_to) if date_to else None

    result = await app.profile_ranking.search_papers(
        profile_slug=profile_slug,
        query_text=query,
        title=title,
        author=author,
        category=category,
        date_from=parsed_date_from,
        date_to=parsed_date_to,
        time_basis=time_basis,
        page_size=page_size,
        cursor_token=cursor,
    )
    return result.model_dump(mode="json")
```

### create_profile Tool (interest.py)

```python
# Source: CLI pattern in interest/cli.py:68-83

@mcp.tool()
async def create_profile(
    name: str,
    negative_weight: float | None = None,
    ctx: Context = None,
) -> dict:
    """Create a new interest profile for personalized paper ranking.

    Returns the created profile summary with slug, name, and settings.
    """
    app = _get_app(ctx)
    try:
        result = await app.profiles.create_profile(name, negative_weight=negative_weight)
    except ValueError as e:
        return {"error": str(e)}
    return result.model_dump(mode="json")
```

### suggest_signals Tool (interest.py)

```python
# Source: CLI pattern in interest/cli.py:493-553

from dataclasses import asdict

@mcp.tool()
async def suggest_signals(
    profile_slug: str,
    auto_add: bool = False,
    ctx: Context = None,
) -> dict:
    """Generate signal suggestions for an interest profile based on workflow activity.

    Analyzes triaged papers, saved queries, and recurring authors to suggest
    new signals. Set auto_add=True to automatically add suggestions as pending signals.
    """
    app = _get_app(ctx)
    try:
        candidates = await app.suggestions.generate_suggestions(profile_slug)
    except ValueError as e:
        return {"error": str(e)}

    added_count = 0
    if auto_add and candidates:
        added = await app.suggestions.add_suggestions_to_profile(profile_slug, candidates)
        added_count = len(added)

    return {
        "candidates": [asdict(c) for c in candidates],
        "added_count": added_count,
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| MCP search returns bare `SearchResult` | Should return `WorkflowSearchResult` / `ProfileSearchResult` | Phase 7 | Agents see triage state + collection context on every search result |
| No profile-ranked search in MCP | `profile_slug` param on discovery tools | Phase 7 | Agents can use interest profiles for personalized discovery |
| No profile creation via MCP | `create_profile` tool | Phase 7 | Full profile lifecycle available to agents |
| No suggestion generation via MCP | `suggest_signals` tool | Phase 7 | Agents can discover relevant signals automatically |

**Not changing:**
- MCP protocol version (mcp 1.26.0)
- FastMCP patterns (lifespan, decorators)
- Existing 11 tools continue working (additive change only)
- Service layer code (no modifications to any service)

## Discretion Recommendations

### 1. explain Parameter: Always include explanations when profile_slug is present

**Recommendation:** Do NOT add an `explain` parameter. Always include `ranking_explanation` when `profile_slug` is provided (and `null` when not). Rationale: the MCP response is structured data consumed by agents, not a CLI display. Agents will want the explanation data to make decisions. Omitting it saves nothing (the field is already computed by `ProfileRankingService`). The CLI needs `--explain` because it controls display formatting; MCP just returns data.

### 2. find_related_papers: Do NOT add profile_slug support

**Recommendation:** Skip this. The CLI does not support it, and `find_related_papers` returns a flat `list[dict]` (not paginated). Adding profile ranking to a flat list is architecturally awkward. If needed in the future, it can be added as a separate phase.

### 3. Test file organization: Add new test file

**Recommendation:** Create `tests/test_mcp/test_interest_tools.py` for `create_profile` and `suggest_signals` tests, and add profile-slug tests to the existing `test_discovery_tools.py`. Rationale: the existing `test_workflow_tools.py` already covers `add_signal` and `batch_add_signals` from `interest.py` -- but creating a dedicated interest tools test file keeps things focused and avoids making `test_workflow_tools.py` even larger.

### 4. SuggestionCandidate: Keep as dataclass with manual dict conversion

**Recommendation:** Use `dataclasses.asdict()`. Converting to Pydantic would mean modifying service-layer code (which Phase 7 should not do). The `asdict()` approach is simple for 4 fields and introduces no circular import risk.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 + pytest-asyncio (auto mode) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` |
| Quick run command | `python -m pytest tests/test_mcp/ -x -q` |
| Full suite command | `python -m pytest tests/ -x -q` |

### Phase Requirements -> Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SC-1 | search_papers with profile_slug returns profile-ranked results with RankingExplanation | unit | `python -m pytest tests/test_mcp/test_discovery_tools.py::TestSearchPapersProfileRanked -x` | Wave 0 |
| SC-2 | search_papers and browse_recent return WorkflowSearchResult-enriched results | unit | `python -m pytest tests/test_mcp/test_discovery_tools.py::TestSearchPapersWorkflowEnriched -x` | Wave 0 |
| SC-3 | create_profile tool creates profile and returns ProfileSummary dict | unit | `python -m pytest tests/test_mcp/test_interest_tools.py::TestCreateProfile -x` | Wave 0 |
| SC-4 | suggest_signals tool generates suggestions, optionally auto-adds | unit | `python -m pytest tests/test_mcp/test_interest_tools.py::TestSuggestSignals -x` | Wave 0 |
| SC-5 | AppContext includes profile_ranking and suggestions services | unit | `python -m pytest tests/test_mcp/test_import.py -x` | Extend existing |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_mcp/ -x -q`
- **Per wave merge:** `python -m pytest tests/ -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_mcp/test_interest_tools.py` -- covers SC-3, SC-4
- [ ] Update `tests/test_mcp/conftest.py` -- add `profile_ranking` and `suggestions` to `mock_app_context`
- [ ] New test classes in `tests/test_mcp/test_discovery_tools.py` -- covers SC-1, SC-2

*(Existing test infrastructure covers framework, fixtures, and import checks)*

## Open Questions

1. **Result shape backward compatibility**
   - What we know: Adding `profile_slug=None` and routing through `ProfileRankingService` changes the return shape from `PaginatedResponse[SearchResult]` to `ProfileSearchResponse` (which has `results` and `ranker_snapshot` top-level keys, where items inside `results` have extra fields like `triage_state`, `collection_slugs`, `ranking_explanation`).
   - What's unclear: Whether any MCP client currently depends on the exact shape of `search_papers` return data. Since MCP clients are internal/development, this is LOW risk.
   - Recommendation: Accept the shape change as additive. Document it in tool docstrings. The new shape is strictly richer.

## Sources

### Primary (HIGH confidence)
- Codebase analysis: `src/arxiv_mcp/mcp/server.py` -- AppContext dataclass and app_lifespan initialization
- Codebase analysis: `src/arxiv_mcp/mcp/tools/discovery.py` -- current discovery tool implementations
- Codebase analysis: `src/arxiv_mcp/mcp/tools/interest.py` -- existing interest tool patterns
- Codebase analysis: `src/arxiv_mcp/interest/search_augment.py` -- ProfileRankingService API
- Codebase analysis: `src/arxiv_mcp/interest/suggestions.py` -- SuggestionService API and SuggestionCandidate dataclass
- Codebase analysis: `src/arxiv_mcp/interest/profiles.py` -- ProfileService.create_profile API
- Codebase analysis: `src/arxiv_mcp/workflow/search_augment.py` -- WorkflowSearchService wrapping pattern
- Codebase analysis: `src/arxiv_mcp/search/cli.py:48-70` -- CLI service chain (authoritative reference)
- Codebase analysis: `tests/test_mcp/conftest.py` -- mock AppContext fixture pattern
- Codebase analysis: `tests/test_mcp/test_discovery_tools.py` -- discovery tool test pattern
- Codebase analysis: `tests/test_mcp/test_workflow_tools.py` -- workflow/interest tool test pattern

### Secondary (MEDIUM confidence)
- mcp package v1.26.0 installed -- FastMCP API verified via import analysis

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all libraries already in use, versions verified
- Architecture: HIGH - patterns directly visible in codebase, CLI reference implementation exists
- Pitfalls: HIGH - identified from concrete code analysis, not speculation

**Research date:** 2026-03-12
**Valid until:** Indefinite (internal codebase patterns, not external library evolution)
