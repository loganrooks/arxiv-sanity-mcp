# arxiv-sanity-mcp Codebase Map — Quality / Architecture Audit Lens

**Date:** 2026-05-01
**Scope:** v0.1 codebase as it stood post Phase 10 (10 phases complete; 2026-03-14 ship). `493` test references → `487` `def test_` matches in `tests/`. v0.2 (multi-lens substrate per ADR-0005) is planned but **no production code exists yet** — the `src/` tree is what would be displaced.
**Method:** Read whole files for `mcp/server.py`, `mcp/tools/*`, `mcp/resources/*`, `mcp/prompts/*`, `db/models.py`, `db/queries.py`, `db/engine.py`, `interest/ranking.py`, `interest/profiles.py`, `interest/signals.py`, `interest/search_augment.py`, `search/service.py`, `search/ranking.py`, `workflow/search_augment.py`, `workflow/triage.py`, `workflow/queries.py`, `workflow/watches.py`, `workflow/collections.py`, `interest/suggestions.py`, `content/service.py`, `content/rights.py`, `content/adapters.py`, `enrichment/service.py`, `enrichment/openalex.py`, `models/paper.py`, `models/interest.py`, `config.py`, `cli.py`, `tests/conftest.py`, `tests/test_search/conftest.py`, `tests/test_mcp/conftest.py`, `tests/test_interest/conftest.py`. Skimmed `workflow/cli.py`, `workflow/export.py`, `ingestion/oai_pmh.py`. Cross-checked claims against the prior `2026-04-25-phase-3-property-audit-opus.md` Property audit, which was conducted with the same lens (lens-extensibility) but only audited `interest/`, `mcp/tools/discovery.py`, `mcp/tools/interest.py`, and the storage indexes — this map covers the rest of the surface that audit explicitly left open.

The architecture-relevant centerpiece: this is a **single-implementation system shaped by accident around its single implementation.** The Property audit identified this in `interest/` and `mcp/tools/discovery.py`. This map confirms the same pattern across the full surface: result-shaping (`search/ranking.py:41-49`), pagination (`search/pagination.py` → score-or-date sort_value extractor), workflow-state augmentation (`workflow/search_augment.py:50-81`), MCP serialization (every tool returns `result.model_dump(mode="json")`), and the entire query-builder family (`db/queries.py`) all assume a `(Paper, single_numeric_rank)` tuple shape. The lens-extensibility commitment of ADR-0005 cannot be honored without touching all of these.

---

## 1. Source layout

The source tree under `src/arxiv_mcp/` is organized into eight packages, each scoped to one of the historical phases:

- **`db/`** — `engine.py` (async engine + `session_factory` factory + `get_session` context manager), `models.py` (all SQLAlchemy ORM models in a single `Base` declarative tree at `src/arxiv_mcp/db/models.py:34-461`), `queries.py` (three SQL builders: `build_search_query`, `build_browse_query`, `build_related_query`). The "queries layer" is the **only** layer that owns SQL — every service goes through it for retrieval, but every service can also issue ad-hoc `select(...)` against ORM models inline (e.g., `search/service.py:166`, `enrichment/service.py:74`, `workflow/triage.py:91`).
- **`models/`** — Pydantic v2 response schemas, separate from DB ORM. `paper.py` defines `PaperSummary` / `PaperDetail` / `SearchResult` / `WorkflowSearchResult` / `ProfileSearchResult`. `interest.py` defines `SignalScore` / `RankingExplanation` / `RankerSnapshot` / `SignalType` (StrEnum). `pagination.py` defines `Cursor`, `PageInfo`, `PaginatedResponse[T]` generics. `workflow.py` defines summaries for collection / saved-query / watch / triage. The split is "ORM = `db/models.py`, response = `models/*`."
- **`ingestion/`** — `oai_pmh.py` (bulk + incremental harvest via `oaipmh-scythe` with checkpoint JSON file at `data/harvest_checkpoint.json`), `arxiv_api.py` (Atom-feed-based incremental fetcher), `parsers.py` (XML → dict), `mapper.py` (dict → `Paper` ORM with `ProcessingTier.FTS_INDEXED` set at `src/arxiv_mcp/ingestion/mapper.py:105`), and a `cli.py` Click subgroup. This package is invoked only by CLI/scripts; not wired into MCP.
- **`search/`** — `service.py` (`SearchService` with three methods: `search_papers`, `browse_recent`, `find_related_papers`), `ranking.py` (just 52 lines: `shape_search_results` converts ORM rows to `SearchResult` Pydantic), `pagination.py` (cursor-encoded keyset pagination), `cli.py`. This is the **base lexical lens** — the only retrieval lens that exists, even though the repo never calls it that.
- **`workflow/`** — `collections.py` (`CollectionService`), `triage.py` (`TriageService`), `queries.py` (`SavedQueryService`), `watches.py` (`WatchService`), `search_augment.py` (`WorkflowSearchService` that wraps `SearchService` and post-augments results with triage state + collection memberships), `export.py` (`ExportService`: JSON dump/restore of all workflow tables), `util.py` (`slugify`), and a 1130-line `cli.py` (the largest file in the codebase — monolithic Click command tree for all workflow operations).
- **`interest/`** — `profiles.py` (`ProfileService`: full CRUD + per-signal-type convenience wrappers like `add_seed_paper` / `add_followed_author`), `signals.py` (`VALID_SIGNAL_TYPES` set + author-name normalization + `validate_signal`), `ranking.py` (the 532-line `RankingPipeline` with five hard-sequenced scorer dispatches), `search_augment.py` (`ProfileRankingService` wrapping `WorkflowSearchService`), `suggestions.py` (`SuggestionService` deriving signal candidates from triage history + saved-query usage), `cli.py`.
- **`enrichment/`** — `openalex.py` (the `EnrichmentAdapter` Protocol + `OpenAlexAdapter` concrete impl + `RateLimiter`), `service.py` (`EnrichmentService` orchestrating cooldown + upsert + tier promotion), `models.py` (Pydantic), `cli.py`.
- **`content/`** — `service.py` (`ContentService` with the source-aware priority chain: abstract → HTML → PDF markdown), `adapters.py` (`ContentAdapter` Protocol + `MarkerAdapter` lazy-loaded + `MockContentAdapter`), `html_fetcher.py` (arXiv HTML scraper), `rights.py` (`RightsChecker` for license-aware access decisions per ADR-0003), `models.py`, `cli.py`.
- **`mcp/`** — `server.py` builds the FastMCP `mcp` instance with the 13-field `AppContext` dataclass. Tool/resource/prompt modules register via side-effect imports in `mcp/server.py:96-102`. Subdirectories: `tools/` (5 modules), `resources/` (4 modules), `prompts/` (3 modules).
- **`scripts/`** — `import_arxiv_scan.py`: bulk-import workflow state from a parallel `arxiv-scan` codebase (per `.planning/ECOSYSTEM-COMMENTARY.md`).

The package boundaries are real — there are no cross-imports between `enrichment/` and `interest/` for example, and `content/` is cleanly bolted on. The two layering exceptions:

1. **`interest/` imports `workflow/`**: `interest/search_augment.py:31` imports `WorkflowSearchResult` and depends on a `WorkflowSearchService` instance (passed in via DI). Phase 3 is built **on top of** Phase 2, not parallel to it.
2. **`enrichment/service.py:164`** does an inline import of `SearchService` inside `enrich_search` to avoid a top-level circular import. This is the only `# inline import to avoid circular` smell I found.

CLI is mostly **independent of MCP**. Each package has its own Click subgroup that calls the same service classes the MCP tools call. The shared entry point `src/arxiv_mcp/cli.py:1-82` registers each subgroup behind `try/except ImportError` so partial installs don't crash the whole CLI — note this swallows real import errors silently (every package's CLI is wrapped in `try/except (ImportError, ModuleNotFoundError): pass`, see `src/arxiv_mcp/cli.py:24-81`).

---

## 2. MCP surface

The MCP layer is in `src/arxiv_mcp/mcp/` with **13 tools, 4 resources, 3 prompts** confirmed by direct count (matches the README claim). The instantiation pattern is consistent and tight:

### Composition

`src/arxiv_mcp/mcp/server.py:32-90` defines a single `AppContext` dataclass holding the engine, session factory, settings, and **13 service instances** that are constructed during the FastMCP `lifespan` context. Service construction order at `src/arxiv_mcp/mcp/server.py:54-71` is significant — `SearchService` is built first because `SavedQueryService`, `WatchService`, and `WorkflowSearchService` all take it as a constructor arg; `WorkflowSearchService` is built before `ProfileRankingService` because the latter wraps it. This is **manual constructor wiring**, not a DI container — there is no service registry.

Tools, resources, and prompts all extract the AppContext via the same one-liner helper, e.g. `src/arxiv_mcp/mcp/tools/discovery.py:18-20`:

```python
def _get_app(ctx: Context) -> AppContext:
    return ctx.request_context.lifespan_context
```

This pattern is duplicated verbatim in every tool/resource/prompt module (count: 8 instances of `return ctx.request_context.lifespan_context`).

### Tools (13)

| Module | Tool | Service it wraps |
|---|---|---|
| `mcp/tools/discovery.py:23` | `search_papers` | `app.profile_ranking.search_papers` (which wraps `WorkflowSearchService` which wraps `SearchService`) |
| `mcp/tools/discovery.py:75` | `browse_recent` | `app.profile_ranking.browse_recent` |
| `mcp/tools/discovery.py:116` | `find_related_papers` | `app.search.find_related_papers` (**bypasses** the augmentation chain — see below) |
| `mcp/tools/discovery.py:157` | `get_paper` | direct `select(Paper)` on session — bypasses services |
| `mcp/tools/workflow.py:21` | `triage_paper` | `app.triage.mark_triage` |
| `mcp/tools/workflow.py:44` | `add_to_collection` | `app.collections` (with auto-create-on-missing fallback at `src/arxiv_mcp/mcp/tools/workflow.py:54-65`) |
| `mcp/tools/workflow.py:69` | `create_watch` | `app.saved_queries.create_saved_query` then `app.watches.promote_to_watch` (two-step composition) |
| `mcp/tools/interest.py:21` | `add_signal` | `app.profiles.add_signal` |
| `mcp/tools/interest.py:46` | `batch_add_signals` | loops over `app.profiles.add_signal` (no service-level batch method exists) |
| `mcp/tools/interest.py:90` | `create_profile` | `app.profiles.create_profile` |
| `mcp/tools/interest.py:110` | `suggest_signals` | `app.suggestions.generate_suggestions` then optionally `add_suggestions_to_profile` |
| `mcp/tools/enrichment.py:19` | `enrich_paper` | `app.enrichment.enrich_paper` |
| `mcp/tools/content.py:27` | `get_content_variant` | `app.content.get_or_create_variant` after `RightsChecker` gate |

### Resources (4)

| URI template | File | Composition |
|---|---|---|
| `paper://{arxiv_id}` | `mcp/resources/paper.py:21` | composite: `select(Paper)` + `app.triage.get_triage_state` + `app.enrichment.get_enrichment_status` + `app.collections.get_paper_collections` + `app.content.list_variants` — **5 service calls in one resource** |
| `collection://{slug}` | `mcp/resources/collection.py:18` | thin wrapper, single `app.collections.show_collection` call |
| `profile://{slug}` | `mcp/resources/profile.py:18` | thin wrapper, single `app.profiles.get_profile` call |
| `watch://{slug}/deltas` | `mcp/resources/watch.py:18` | thin wrapper, single `app.watches.check_watch` call (which auto-advances the checkpoint as a side-effect — see `src/arxiv_mcp/workflow/watches.py:152-162`) |

### Prompts (3)

`mcp/prompts/literature_review.py:16`, `mcp/prompts/daily_digest.py:16`, `mcp/prompts/triage_shortlist.py:21`. Each returns a list of `UserMessage`s containing instructions templated with the user's parameters. `triage_shortlist` is the only prompt that calls a service — `app.collections.show_collection(collection_slug)` to inject the live paper count into the prompt template (`src/arxiv_mcp/mcp/prompts/triage_shortlist.py:35-37`). The other two are pure string templates.

### Maturity vs hackiness signals

**Mature:**

- Lifecycle is correct: engine created in `app_lifespan`'s `try`, disposed in `finally` (`src/arxiv_mcp/mcp/server.py:73-90`).
- All tools convert via `result.model_dump(mode="json")` consistently, so the JSON shape is whatever the Pydantic model says it is — no ad-hoc dict assembly except in the two endpoints that return raw dicts (`get_paper`, `get_content_variant`).
- Service-construction order is explicit and commented (`src/arxiv_mcp/mcp/server.py:58`, `:68`).
- `RightsChecker` is constructed as a module-level singleton at `src/arxiv_mcp/mcp/tools/content.py:19`, not per-call — the only mutable state here is the immutable `set` of license URIs.
- Each tool docstring documents its response shape, e.g. `src/arxiv_mcp/mcp/tools/discovery.py:45` ("Response shape: {'results': {'items': [...], 'page_info': {...}}, 'ranker_snapshot': ...}").

**Hacky / load-bearing irregularities:**

- **`get_paper` bypasses services** and does inline `select(Paper)` at `src/arxiv_mcp/mcp/tools/discovery.py:165-169` — note that the `paper://` *resource* gives a richer composite view than the `get_paper` *tool* gives. This is an asymmetry agents will trip on.
- **`find_related_papers` does not pass through the augmentation chain.** Lines 140-151 of `src/arxiv_mcp/mcp/tools/discovery.py` call `app.search.find_related_papers` directly, then merge by `arxiv_id` keeping the highest score per paper. **No triage state, no collection slugs, no profile re-ranking** — even though the same response uses `SearchResult.model_dump(mode="json")`. This was flagged in the Property audit as a coupling problem (Property 2: "find_related_papers has no profile awareness"); it's also an MCP-surface inconsistency at the user-facing level.
- **Watch resource has a side-effect.** Reading `watch://{slug}/deltas` (`src/arxiv_mcp/mcp/resources/watch.py:24`) calls `check_watch`, which **auto-advances `checkpoint_date` to today** (`src/arxiv_mcp/workflow/watches.py:152-162`). This makes resource reads non-idempotent at the data layer. MCP semantically treats resources as readable state; this conflates "read deltas" with "checkpoint that I read them."
- **`add_to_collection` auto-creates collections** at `src/arxiv_mcp/mcp/tools/workflow.py:57-60` — first call attempts add, on `ValueError` (collection not found) it creates the collection and retries. Convenient but masks the distinction between "collection didn't exist" and "paper didn't exist." Both `IntegrityError` cases at lines 61-64 collapse to "Paper not found" (which is wrong if the failure was actually a different FK).
- **Error messages are stringified user-facing.** `triage_paper` returns `{"error": str(e)}` for `ValueError` (`src/arxiv_mcp/mcp/tools/workflow.py:38-39`); `enrich_paper` does the same for **all `Exception`s** (`src/arxiv_mcp/mcp/tools/enrichment.py:33`) — `except (ValueError, Exception)` is essentially a bare except. There is no structured error code or type.
- **`create_watch` does string-replacement on inner exception messages**: `msg = str(e).replace("Saved query", "Watch")` at `src/arxiv_mcp/mcp/tools/workflow.py:91`. Brittle — leaks the underlying naming and breaks if the inner service rephrases.

### Coupling pattern

The MCP layer has **no abstraction over the service layer.** Tools call `app.<svc>.<method>(...)` directly, with the AppContext dataclass acting as a registry of named singletons. There is no per-tool middleware, no auth-check protocol, no instrumentation hook. This is fine for v0.1 scope but means any cross-cutting concern (e.g., "add lens telemetry to every discovery call") requires editing every tool body.

---

## 3. Service layer

There are **13 services** in the system, all instantiated in `mcp/server.py` and held in `AppContext`. The DI pattern is consistent: every service constructor takes `session_factory: async_sessionmaker[AsyncSession]` + `settings: Settings`, plus optionally:

- The next-layer service it wraps (`SavedQueryService`, `WatchService`, `WorkflowSearchService`, `ProfileRankingService`, `SuggestionService`).
- An optional adapter for testability (`EnrichmentService` takes an `adapter=None` and falls back to `OpenAlexAdapter(settings)` at `src/arxiv_mcp/enrichment/service.py:46`; `ContentService` takes optional `adapter` and `http_client`).

This is hand-wired DI, not a container. Service instances are stateless except for the session factory and the configured adapter.

### Layer wrapping pattern

The discovery path stacks **three** services:

```
SearchService             (search/service.py — base lexical retrieval)
  ↑ wrapped by
WorkflowSearchService     (workflow/search_augment.py — adds triage_state + collection_slugs)
  ↑ wrapped by
ProfileRankingService     (interest/search_augment.py — over-fetch + re-rank with RankingPipeline)
```

Each wrapping service composes **by delegation**, never by inheritance. The wrapper takes the inner service in its constructor and forwards `**kwargs`. Critically, this composition lives in the service objects' fields — the wrappers *own* references to their inner service. There is no per-request lens dispatch.

`WorkflowSearchService.search_papers` (`src/arxiv_mcp/workflow/search_augment.py:40-43`) is two lines: delegate, then augment.

`ProfileRankingService.search_papers` (`src/arxiv_mcp/interest/search_augment.py:96-135`) splits on `profile_slug is None`. Without a profile, it passes through with `_wrap_without_ranking` (sets `ranking_explanation=None` on every `ProfileSearchResult`). With a profile, it calls `_ranked_search`, which over-fetches `page_size * 3` from the inner service, scores each result with `RankingPipeline`, sorts by composite score, and trims back to `page_size`.

The over-fetch multiplier is a hardcoded constant `OVERFETCH_MULTIPLIER = 3` at `src/arxiv_mcp/interest/search_augment.py:56`. The known limitation is documented in the docstring at `:174-179`: "page boundaries shift between requests — a paper on page 1 could move to page 2 or vice versa on subsequent queries." This is the only `Note:` in the codebase outside `mcp/tools/discovery.py:88`.

### Service test pattern

Service tests use the **real database** via the `test_session` fixture (`tests/conftest.py:109-135`). The fixture creates the schema with `Base.metadata.create_all`, manually creates the tsvector trigger function and trigger (the SQL is duplicated from `alembic/versions/001_initial_schema.py:98-115` into `tests/conftest.py:21-41`), yields an `AsyncSession`, then drops everything. Function-scoped to avoid asyncpg event-loop conflicts (per `tests/conftest.py:96`).

For services that take a `session_factory`, `tests/test_interest/conftest.py:71-79` provides a `session_factory` fixture that depends on `test_session` (just to ensure tables are created) and returns a fresh `async_sessionmaker`.

The only service-class with non-DB testability infrastructure is `ProfileRankingService`, which has a `_test_profile_context: ProfileContext | None = None` injection point (`src/arxiv_mcp/interest/search_augment.py:80, 244-246`) so tests can bypass the DB-load path. This is a special-case test seam.

### Observation: `EnrichmentService` reaches across packages

`EnrichmentService.enrich_search` does an inline `from arxiv_mcp.search.service import SearchService` then **constructs its own `SearchService` instance** at `src/arxiv_mcp/enrichment/service.py:164-166` rather than receiving one in its constructor. This is the only service that constructs another service inline. The reason is presumably to avoid making `SearchService` a constructor dependency of `EnrichmentService` (which would cycle since `enrichment` is conceptually downstream of `search`). It works but the AppContext could just pass it in.

---

## 4. Database layer

PostgreSQL-only (asyncpg via SQLAlchemy 2.0's async ORM). `src/arxiv_mcp/db/engine.py:20-34` configures pool size 5, max_overflow 10, `pool_pre_ping=True`. Single `Base = DeclarativeBase` shared by all models.

### Schema (8 tables across 8 migrations)

| Migration | Adds | Notes |
|---|---|---|
| `001_initial_schema.py` (132 lines) | `papers` table, GIN index on tsvector, GIN index on category_list array, **hand-written tsvector trigger function** at lines 98-115 | All of `papers`'s 30+ columns. Trigger weights title=A, authors=B, abstract=C — see `src/arxiv_mcp/db/models.py:111` and the duplicated trigger SQL in `tests/conftest.py:21-32`. |
| `002_workflow_tables.py` (135 lines) | `collections`, `collection_papers` (composite PK), `triage_states`, `triage_log`, `saved_queries` | `triage_states` has `CHECK (state IN ...)` constraint (`src/arxiv_mcp/db/models.py:260-263`); `saved_queries.params` is JSONB. |
| `003_interest_tables.py` (76 lines) | `interest_profiles`, `interest_signals` | Initially with a CHECK constraint on `signal_type`. |
| `004_enrichment_table.py` (64 lines) | `paper_enrichments` | First-cut single-source schema. |
| `005_drop_signal_type_check.py` (32 lines) | DROPS `ck_signal_type_valid` from `interest_signals` | This is the **load-bearing migration for lens-extensibility.** Validation moved to application-level `signals.py:11`. See §7. |
| `006_enrichment_composite_pk.py` (59 lines) | Adds composite PK `(arxiv_id, source_api)` to `paper_enrichments` | Allows multiple enrichment sources per paper. |
| `007_add_seen_triage_state.py` (45 lines) | Adds `'seen'` to triage_states CHECK | |
| `008_content_variants_table.py` (71 lines) | `content_variants` table | Composite PK `(arxiv_id, variant_type)`, JSONB `quality_warnings`. |

### Key model patterns

- **`ProcessingTier(IntEnum)`** at `src/arxiv_mcp/db/models.py:40-51`: `METADATA_ONLY=0, FTS_INDEXED=1, ENRICHED=2, EMBEDDED=3, CONTENT_PARSED=4`. The enum is anticipatory — `EMBEDDED=3` exists despite no embedding code anywhere in `src/`. Promotions are done at write time by service code: `mapper.py:105` sets `FTS_INDEXED`, `enrichment/service.py:310` sets `ENRICHED`, `content/service.py:301` sets `CONTENT_PARSED`. Nobody reads `EMBEDDED`.
- **`Paper.search_vector`** is a TSVECTOR column populated by a PG trigger (`alembic/versions/001_initial_schema.py:98-115`). Indexed with GIN. Service code uses `Paper.search_vector.op("@@")(tsquery)` and `func.ts_rank_cd(...)` — see `src/arxiv_mcp/db/queries.py:71-73, 113-117`. **The result-row tuple `(Paper, rank)` is the canonical retrieval shape across the system.**
- **Discriminator-via-string column.** `InterestSignal.signal_type: String(32)` (`src/arxiv_mcp/db/models.py:383`) and `ContentVariant.variant_type: String(32)` (`src/arxiv_mcp/db/models.py:435`) are both schema-level "discriminator columns" without polymorphic inheritance — they're just strings the application validates. `ContentVariant` keeps a `CHECK (variant_type IN ('abstract', 'html', 'source_derived', 'pdf_markdown'))` (`src/arxiv_mcp/db/models.py:449-452`), but `InterestSignal` deliberately dropped its CHECK in migration 005 (above). **This asymmetry is what makes the profile primitive lens-extensible while the content primitive isn't.**
- **JSONB used liberally for "schema-flexible" fields.** `Paper.version_history`, `PaperEnrichment.topics`/`related_works`/`counts_by_year`/`openalex_raw`, `SavedQuery.params`, `InterestProfile.weights`, `ContentVariant.quality_warnings`. Per the Property audit (and confirmed by my read of `db/queries.py`): `PaperEnrichment.related_works` has zero readers in retrieval code. It's write-once metadata.
- **Enrichment is single-table multi-source-by-PK.** `paper_enrichments` has composite PK `(arxiv_id, source_api)` (after migration 006), so multiple enrichment providers per paper coexist as separate rows. But all enrichment fields (`cited_by_count`, `fwci`, `topics`, `related_works`, ...) are OpenAlex-shaped — there's no abstraction over what an enrichment record contains.

### Query layer

`src/arxiv_mcp/db/queries.py` (237 lines) contains the **only** centralized SQL builders: `build_search_query`, `build_browse_query`, `build_related_query`. Each returns a `Select` statement; execution happens in the calling service (`src/arxiv_mcp/search/service.py:79-82, 130-132, 173-175`). This separation is enforced only by convention — services import these builders, but services also issue their own `select(...)` queries inline whenever they need to (especially `enrichment/service.py`, `workflow/triage.py`, `interest/profiles.py`).

The query builders all assume tsvector-based retrieval. Both `build_search_query` and `build_related_query` build a `tsquery` and order by `ts_rank_cd`. There is no abstraction over "kind of query" — the function name is `build_search_query`, not `build_lexical_search_query`. Adding a vector-based or graph-based query requires a parallel module, not an extension.

### Integration test approach

The test suite hits real Postgres for the vast majority of service tests. The `tests/conftest.py:92-106` `test_engine` fixture connects to `arxiv_mcp_test` DB (configured via `Settings.test_database_url`). Schema is created via `Base.metadata.create_all` per test, **not** by running Alembic. The tsvector trigger function and trigger are recreated by hand (the SQL is verbatim-duplicated from `alembic/versions/001_initial_schema.py` into `tests/conftest.py:21-41`) — this means **migrations and tests can drift** if migration 001 is ever modified. Only `001` is duplicated; migrations 002-008 are implicit (assumed via SQLAlchemy autogeneration of the tables they would have created).

Per-test cleanup is `Base.metadata.drop_all` after the trigger and function are explicitly dropped. Function-scoped per `tests/conftest.py:96` ("avoid event loop issues with asyncpg").

---

## 5. Test architecture

`pyproject.toml:50-53` configures `asyncio_mode = "auto"`, `testpaths = ["tests"]`, `timeout = 30`. The suite is organized by package: `tests/test_<package>/conftest.py + test_*.py`.

### Numerical breakdown

- 487 `def test_` matches across 51 test files.
- Top files by test count: `tests/test_interest/test_profiles.py` (42 tests, 657 lines), `tests/test_interest/test_ranking.py` (36 tests, 821 lines), `tests/test_workflow/test_triage.py` (24), `tests/test_mcp/test_discovery_tools.py` (24), `tests/test_workflow/test_collections.py` (23).
- 17 test files (out of 51) use real DB fixtures; 11 use `AsyncMock`/`MagicMock`. The 11 mock-using files map cleanly: `tests/test_mcp/*` (mocks the AppContext to test tool wiring without a DB), plus `test_content/test_html_fetcher.py` (mocks httpx), `test_enrichment/test_adapter.py` (mocks the OpenAlex client), `test_ingestion/test_oai_pmh.py` and `test_ingestion/test_arxiv_api.py` (mock the external scythe + httpx), and `test_enrichment/test_cli.py` (mocks the CLI service layer).

### The split: real-DB for services, mocks for MCP-tool-and-external-API testing

The convention is clean and consistent:

- **Service tests** go through Postgres. `tests/test_search/conftest.py:28-294` defines `SAMPLE_PAPERS` — a fixture of 15 hand-built papers covering cs.CL/cs.AI/cs.CV/stat.ML categories with realistic abstracts. The `search_session` fixture (`tests/test_search/conftest.py:312-343`) bulk-inserts these and yields a session. This means search relevance tests run against a real PG `tsvector @@ tsquery` engine, not a mock.
- **MCP tool tests** mock the AppContext. `tests/test_mcp/conftest.py:81-130` builds a `mock_app_context` with `AsyncMock` services pre-configured to return canned `SearchResult`/`ProfileSearchResponse` instances. This tests the wiring (does `search_papers` correctly forward `profile_slug`?) without exercising the underlying logic.
- **Adapter tests** mock the external service. `OpenAlexAdapter` and `MarkerAdapter` are tested with mocks of httpx/marker.

### Fixture organization

Each `tests/test_*/conftest.py` is package-scoped. The root `tests/conftest.py:44-89` defines `sample_paper_data(**overrides)` as a shared factory; per-package conftests build on top of it. `tests/test_interest/conftest.py:18-67` imports `sample_paper_data` from the root conftest and adds `sample_profile_data`, `sample_signal_data`, `sample_saved_query_data`.

There is **no factory library** like `factory_boy` — everything is hand-rolled dict-overrides.

### Gaps

- **Integration tests across services are sparse.** The bulk of testing is per-service or per-tool. Cross-service flows (e.g., "add signal from MCP tool → re-rank search → check ranking_explanation") are not extensively covered, except indirectly via the workflow-tool tests in `tests/test_mcp/test_workflow_tools.py` (which mock services and so don't exercise real composition).
- **No E2E / system-level test.** The 4 prompt modules and the lifecycle of the MCP server itself (engine setup, service wiring, dispose) are not tested under a running server.
- **Migration tests are absent.** Alembic migrations are not exercised by the test suite — the test schema is built via `Base.metadata.create_all`, not via `alembic upgrade head`. If a migration is buggy, the test suite won't catch it; if a model and migration drift, the test suite won't catch it.
- **No coverage threshold or report.** `pytest-cov` is in dev deps (`pyproject.toml:46`) but `pyproject.toml` defines no coverage target. (CHANGELOG and STATE.md don't quote a coverage number either.)
- **Marker GPU adapter is essentially untested.** `tests/test_content/test_adapter.py` tests `MockContentAdapter`. `MarkerAdapter._init_converter` does dynamic CUDA-or-CPU import (`src/arxiv_mcp/content/adapters.py:64-88`) — this whole code path runs only when Marker is installed at runtime.

---

## 6. Code quality signals

### Largest files by line count

```
1130  src/arxiv_mcp/workflow/cli.py           (Click command tree for collection/triage/queries/watches/paper/workflow)
 617  src/arxiv_mcp/interest/cli.py           (Click subgroup for profiles + signals + suggestions)
 547  src/arxiv_mcp/workflow/export.py        (export/import + stats)
 532  src/arxiv_mcp/interest/ranking.py       (5 scorers + RankingPipeline)
 529  src/arxiv_mcp/workflow/collections.py   (CollectionService)
 460  src/arxiv_mcp/db/models.py              (all 8 ORM models)
 410  src/arxiv_mcp/interest/suggestions.py   (SuggestionService)
 404  src/arxiv_mcp/search/cli.py
 398  src/arxiv_mcp/workflow/triage.py        (TriageService)
 395  src/arxiv_mcp/interest/profiles.py      (ProfileService)
```

The two CLI files (1130 + 617 lines) dominate the "longest files" list. They are flat command-handler files — each `@click.command` decorator wraps a 10-30 line handler that constructs a service, calls one method, and prints a Rich table. Low cyclomatic complexity per command, but the file is long because there are ~30+ commands per CLI. Refactoring suggestion is out of scope per the prompt; the **observation** is that the CLI is **a parallel surface to MCP** with the same coupling pattern (hand-instantiated services, direct method calls). Whatever lens-dispatch is added to MCP also needs to be added to CLI.

### Complexity hotspots

- **`RankingPipeline.score_paper`** at `src/arxiv_mcp/interest/ranking.py:415-495`: 5 if-branches, hard-sequenced scorer dispatch. The `if has_profile_signals:` branch (`:460`) gates the addition of three scorers. **This is the function ADR-0005's "scorer registry" decision points at**. Length is fine (~80 lines), but the structural commitment is what matters.
- **`CollectionService.delete_collection` with `purge_orphans=True`** at `src/arxiv_mcp/workflow/collections.py:137-178`: nested for-loop with two queries per orphan candidate. Probably correct but O(N · 2) DB roundtrips — a single `DELETE WHERE NOT IN (...)` would do it. Not on a hot path.
- **`ProfileRankingService._load_profile_context`** at `src/arxiv_mcp/interest/search_augment.py:236-328`: 92 lines, 4 conditional batch loads. This is the function ADR-0005 calls "hardcodes which signals to load."
- **`OpenAlexAdapter.enrich`** family in `src/arxiv_mcp/enrichment/openalex.py:265-378`: clean separation of singleton vs batch path with cooperative chunking. Retry-with-jitter on 429 at `:117-158`. Sound.

### Unclear abstractions

- **`SearchResult` (`src/arxiv_mcp/models/paper.py:141-145`) is a 4-line wrapper around `(PaperSummary, float | None)`.** `WorkflowSearchResult` (`:148-159`) duplicates the fields rather than inheriting (commented at `:165` "to avoid Pydantic v2 inheritance complexity"). `ProfileSearchResult` (`:162-174`) duplicates them again. The pattern is: each augmentation layer has its own response type that **adds fields by copy-paste**. This is the response shape that ADR-0005 says must be "generalized" to carry per-lens score components.
- **`ProfileContext`** at `src/arxiv_mcp/interest/ranking.py:52-68`: a dataclass with 9 named fields, each shaped to one of the 4 signal types (`seed_papers`, `seed_categories`, `followed_authors`, `negative_papers`, `negative_categories`, `query_slugs`). A new signal type cannot reuse this dataclass; either the dataclass grows or the loader grows a parallel concept. The Property audit's caveat about Property 1 ("the field naming is shaped around the four current types") points here.
- **`AppContext`** at `src/arxiv_mcp/mcp/server.py:32-48`: 13-field dataclass. Adding a service requires editing this dataclass, the lifespan function, and (for tools that use it) every tool body. Not a registry, just a struct.

### Dead-or-near-dead code

- **`ProcessingTier.EMBEDDED = 3`** at `src/arxiv_mcp/db/models.py:50`: never written or read by any code. The whole `ProcessingTier` enum is a four-value system pretending to be five.
- **`PaperEnrichment.related_works`/`topics`/`fwci`/`counts_by_year`**: written by `EnrichmentService._upsert_enrichment` (`src/arxiv_mcp/enrichment/service.py:248-264`) and surfaced in the `paper://` resource as `enrichment_data` (`src/arxiv_mcp/mcp/resources/paper.py:43-51`). **None of these fields are read by retrieval, ranking, or any service-layer query.** They reach the wire as JSON, not as inputs to anything. The Property audit confirmed this; my read confirms it.
- **`SuggestionService.confirm_suggestions_bulk`** at `src/arxiv_mcp/interest/suggestions.py:232-256` is a thin loop over `confirm_suggestion`. No callers — the MCP tool `suggest_signals` uses `add_suggestions_to_profile` (`src/arxiv_mcp/mcp/tools/interest.py:133-135`), not `confirm_*`. Maybe used by CLI only.
- **`SavedQueryService._deserialize_params` warns on `collection_filter` and `triage_filter` keys** with "not yet supported in base SearchService; skipping filter" (`src/arxiv_mcp/workflow/queries.py:253-264`). These are documented param keys that **don't actually do anything** if a saved query stores them.
- The five `try/except (ImportError, ModuleNotFoundError): pass` blocks in `src/arxiv_mcp/cli.py:24-81` will silently swallow import errors during CLI subgroup registration. If a module fails to import for any reason other than its package being absent, that subgroup just disappears from `--help`.

### TODO / FIXME concentrations

`grep -rn "TODO|FIXME|HACK|XXX"` against `src/` returns **zero matches**. The two `Note:` comments are docstrings, not deferred work. There is no debt list embedded in code. Whether this means "no debt" or "debt is not tracked in code" is ambiguous; given the size of `.planning/` (containing `LONG-ARC.md` anti-patterns, audit reports, and the v1-MILESTONE-AUDIT), I'd call it the latter — debt lives in `.planning/`, not in `src/`.

---

## 7. Readiness for v0.2 (multi-lens substrate)

**Bottom line: the codebase is "single-lens by accident" exactly as the Property audit named it.** `grep -rn "lens\|Lens"` in `src/` returns **zero matches**. There is no surface in production code that names what would be displaced by a Lens interface — which is itself the strongest evidence: the abstraction is missing because the system was built when "the lens" was synonymous with "the implementation."

I'll go through each layer with concrete file:line evidence for what a Lens interface would have to displace, and where the seams are clean enough to ship a second lens vs. where contortions are unavoidable.

### Profile primitive (cleanest seam)

**Verdict: extensible by design — the work was done in migration 005.**

`alembic/versions/005_drop_signal_type_check.py:23-24` dropped the CHECK constraint on `interest_signals.signal_type`. The column is now `String(32)` with **only** application-level validation in `src/arxiv_mcp/interest/signals.py:11`:

```python
VALID_SIGNAL_TYPES = {"seed_paper", "saved_query", "followed_author", "negative_example"}
```

A new signal type (e.g. `"citation_anchor"`) requires adding a string to this set and (for paper-typed signals) handling in `ProfileService.add_signal`'s FK-validation switch (`src/arxiv_mcp/interest/profiles.py:271-289`). No migration, no schema change. This is the result of an explicit design decision called out in the migration's own docstring at `alembic/versions/005_drop_signal_type_check.py:9` ("allowing new signal types without DB migrations").

The `InterestProfile.weights: JSONB` column at `src/arxiv_mcp/db/models.py:353` is similarly already-designed to hold per-lens weight overrides — `ProfileRankingService._load_profile_context` already plumbs it into `RankingPipeline(weights=profile_context.weights or None)` (`src/arxiv_mcp/interest/search_augment.py:190`).

### MCP tool surface (high contortion)

**Verdict: coupled — every discovery tool needs a `lens=` parameter, plus the dispatcher.**

`src/arxiv_mcp/mcp/tools/discovery.py:24-186`: I read all four tools end to end. **None take a `lens` parameter.** `profile_slug` is the only "steering knob" (`:34, :82`). The dispatch happens implicitly in `ProfileRankingService.search_papers` at `src/arxiv_mcp/interest/search_augment.py:124-135`, which has no lens branch — only `if profile_slug is None:` for backward compat.

`find_related_papers` is the most rigid: it has no `profile_slug` at all (`src/arxiv_mcp/mcp/tools/discovery.py:117-154`) and unconditionally delegates to `SearchService.find_related_papers`, which is hardwired to `build_related_query`'s tsvector logic (`src/arxiv_mcp/db/queries.py:181-237`). The current implementation merges multi-seed results by max-score on `arxiv_id`, which assumes single-numeric scores per result — incompatible with a per-lens-score-vector return shape.

`get_paper` (the *tool*, not the resource) bypasses services entirely (`src/arxiv_mcp/mcp/tools/discovery.py:165-169`). It would need profile/lens dispatch to participate in lens-aware behavior.

### Storage layer (high contortion)

**Verdict: coupled, exactly as the Property audit said. No vector index, no normalized citations.**

`src/arxiv_mcp/db/models.py:113-122` is the complete index list on the `papers` table: 8 indexes, all GIN-on-tsvector or GIN-on-array or btree-on-date/category. **No pgvector, no embedding column, no edge table.** `PaperEnrichment.related_works` (`src/arxiv_mcp/db/models.py:151`) holds JSONB lists of related-work URIs but is never queried by any retrieval code (confirmed by my read of `src/arxiv_mcp/db/queries.py`, `src/arxiv_mcp/search/service.py`, `src/arxiv_mcp/interest/ranking.py`).

The shape of a query-builder is hardwired:

- `build_search_query` returns `select(Paper, rank_expr.label("rank"))` (`src/arxiv_mcp/db/queries.py:72-76`).
- `build_browse_query` returns `select(Paper, literal(None).label("rank"))` (`:154`).
- `build_related_query` returns `select(Paper, rank_expr.label("rank"))` (`:229-231`).

A second lens needs a parallel query-builder family with a different result row shape (e.g. `(Paper, citation_score, co_citation_score, ...)`).

### Result-shape contagion

`SearchResult` (`src/arxiv_mcp/models/paper.py:141-145`) hardcodes `score: float | None`. This single field flows through:

1. `shape_search_results` builds it from `row[1]` rank (`src/arxiv_mcp/search/ranking.py:43-49`).
2. `WorkflowSearchService._augment_results` carries it forward (`src/arxiv_mcp/workflow/search_augment.py:67-76`).
3. `ProfileRankingService._wrap_without_ranking` propagates it (`src/arxiv_mcp/interest/search_augment.py:339-346`).
4. `ProfileRankingService._ranked_search` **overwrites** it with `composite_score` from `RankingPipeline` (`src/arxiv_mcp/interest/search_augment.py:206-208`).
5. Pagination uses it: `lambda item: item.score` (`src/arxiv_mcp/search/service.py:88`) is the sort_value extractor for keyset cursor encoding when text-search is active.

**All of this assumes a single numeric score per result.** A per-lens result with `{"semantic": 0.7, "citation": 0.3}` cannot ride this pipe without breaking pagination, augmentation, and ranking-pipeline assumptions.

### Ranker (medium contortion)

`RankingPipeline.score_paper` at `src/arxiv_mcp/interest/ranking.py:415-495` dispatches to scorer functions in a hard-sequenced if-tree:

```python
# Always apply: query_match (line 439)
# Always apply: recency (line 446)
# if has_profile_signals (line 460):
#   - seed_relation
#   - category_overlap
#   - interest_profile_match
#   - apply_negative_demotion
```

Adding a sixth scorer (e.g. citation-edge-traversal score) requires editing this method body. The scorer functions themselves (`score_query_match`, `score_category_overlap`, etc.) are pure module-level functions, so the *scorers* are extensible; only the *dispatcher* is hardcoded. The "scorer registry" mentioned in ADR-0005 is precisely the refactor of lines 436-487 into a registered-name → scorer-callable map. The `RANKER_VERSION = "0.3.0"` at `:402` is a hand-bumped string; no enforcement that it changes when the pipeline changes.

### `ProfileContext` (medium contortion)

`src/arxiv_mcp/interest/ranking.py:52-68`'s 9-field dataclass enumerates the four signal types by name. The Property audit flagged this; my read confirms it. Adding `citation_anchor_papers: list[PaperSummary]` requires editing the dataclass + the loader at `src/arxiv_mcp/interest/search_augment.py:274-287`. No DB migration, but a code change at every call site. A "bag of typed signals" representation (e.g. `signals: dict[str, list[Any]]`) would be lens-extensible at the cost of giving up `mypy`-checked field access.

### What's actually clean

- **The `EnrichmentAdapter` Protocol** at `src/arxiv_mcp/enrichment/openalex.py:47-61` and **`ContentAdapter` Protocol** at `src/arxiv_mcp/content/adapters.py:23-47` are good shape for what a `Lens` Protocol would look like: two-method protocols (name property + async method), with the service layer accepting an optional adapter for testing. **This is the only "pluggable backend" pattern that already exists in the codebase.** It does not extend to retrieval — `SearchService` is a single concrete class, not a protocol with implementations.
- **The MCP tool/resource/prompt registration pattern** uses side-effect imports of files that decorate functions with `@mcp.tool()` etc. (`src/arxiv_mcp/mcp/server.py:96-102`). A new lens-aware tool can be added as a new file that just imports `mcp` and decorates — no central registry to edit. (The dispatch *inside* the tool is the hard part.)
- **The composition-by-wrapping pattern** (`ProfileRankingService` wraps `WorkflowSearchService` wraps `SearchService`) is a clean enough seam that a `LensDispatcher` could slide in as a fourth wrapping layer without breaking inner services. The pattern is "do delegate, then transform"; a `LensDispatcher` would do "split, fan out to multiple inner services, merge."

### Single-lens-by-accident evidence summary

| Surface | Single-lens assumption | File:line |
|---|---|---|
| MCP tool signatures | No `lens=` parameter on any of the 4 discovery tools | `mcp/tools/discovery.py:24, 76, 117, 158` |
| Service dispatcher | `ProfileRankingService.search_papers` only branches on `profile_slug is None` | `interest/search_augment.py:124` |
| Result shape | `SearchResult.score: float \| None` (single numeric) | `models/paper.py:141-145` |
| Pagination | Keyset cursor's `sort_value` extractor is `item.score` (single numeric) | `search/service.py:88, 95` |
| Query builder | Three `build_*_query` functions, all return `(Paper, ts_rank_cd score)` | `db/queries.py:32, 130, 181` |
| Storage indexes | 8 indexes on `papers`, all tsvector / array / btree — no vector, no edge | `db/models.py:113-122` |
| Ranking pipeline | `score_paper` hard-sequences 5 scorer calls | `interest/ranking.py:439-487` |
| `ProfileContext` | 9 fields named for the 4 current signal types | `interest/ranking.py:52-68` |
| `RankerSnapshot` | `signal_types_applied: list[str]` is dynamic — this part **is** lens-ready | `models/interest.py:130` |
| Tier enum | `EMBEDDED=3` exists but no embedding code anywhere | `db/models.py:50` |
| `signal_type` column | CHECK dropped in migration 005, application-level validation only | `alembic/versions/005_drop_signal_type_check.py:23-24` + `interest/signals.py:11` |
| `InterestProfile.weights` | JSONB, generic shape — already lens-ready | `db/models.py:353` |

The pattern is clear: **the profile primitive and weights storage were intentionally designed for extensibility (migration 005, JSONB weights). Everything downstream of them — dispatch, query builder, result shape, pagination — was built single-lens.**

---

## 8. Surprising or load-bearing patterns

These are things an external auditor will not see from a directory listing but matter for understanding why the code looks the way it does.

1. **The Property audit at `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` is the load-bearing prior art for any v0.2 code work.** That audit, conducted with explicit Opus model override, surveyed `interest/`, `mcp/tools/discovery.py`, `mcp/tools/interest.py`, and the storage indexes and concluded "Property 1 extensible, Properties 2 & 3 coupled." This map confirms those findings against the rest of the surface (resources, prompts, content, enrichment, workflow, search, db queries) and reaches the same verdict — but the prior audit also lists **what it did not check**: ingestion-side coupling (`enrichment/openalex.py`, `ingestion/`), MCP resources/prompts (which I did read), and test coverage of the abstractions (which I partly characterized in §5). Anyone proposing v0.2 code should read that audit first; this map second.

2. **`ProcessingTier.EMBEDDED = 3` is anticipatory dead code.** The enum at `src/arxiv_mcp/db/models.py:40-51` reserves `EMBEDDED=3` between `ENRICHED=2` and `CONTENT_PARSED=4`, but no code path writes or reads it. This is a slot that was deliberately kept open for an embedding lens — one that the ADR-0005 multi-lens decision foreclosed in favor of citation/community as the second lens (per CLAUDE.md "Stack trajectory: Stack A moving toward Stack B"). If the v0.2 plan ever wants to add embeddings as a third lens, the tier slot is already there.

3. **Phase numbering in `.planning/phases/` is irregular.** There are two `05-` directories (`05-content-normalization` is empty; `05-mcp-validation-iteration` has the actual plans), and `04.1-mcp-v1-...` exists alongside `04-enrichment-adapters`. Content normalization actually shipped under `06-content-normalization`. This isn't a code issue but is the kind of thing that confuses newcomers reading the planning archive.

4. **The watch resource's checkpoint auto-advance is a side-effect on read.** `mcp/resources/watch.py:24` calls `app.watches.check_watch(slug)`, and that method **mutates `checkpoint_date` and `last_checked_at`** at `src/arxiv_mcp/workflow/watches.py:152-162`. This is the only stateful resource in the system. MCP clients that read `watch://{slug}/deltas` twice will get different results — the second read returns only papers since the first read's wall-clock timestamp. The behavior is documented in the docstring but is **not idempotent** — surprising for anyone treating MCP resources as cacheable reads.

5. **`add_to_collection` does opportunistic creation** at `src/arxiv_mcp/mcp/tools/workflow.py:54-65`. This is the only tool that has a "try and on failure create then retry" pattern. The reason is workflow ergonomics — agents shouldn't need a separate `create_collection` tool — but it means: (a) `add_to_collection` can have **two different DB write effects**; (b) the error semantics collapse two distinct `IntegrityError` cases into "Paper not found"; (c) collections can be created with names normalized through `slugify` without the user explicitly opting in.

6. **Tests duplicate the tsvector trigger SQL from migration 001.** `tests/conftest.py:21-41` carries a verbatim copy of the trigger function and trigger from `alembic/versions/001_initial_schema.py:98-115`. If migration 001 ever changes (e.g. weights are rebalanced), the tests will silently use the old trigger and not notice. There is no link between the two.

7. **Marker (PDF→markdown) is dynamically loaded.** `src/arxiv_mcp/content/adapters.py:64-88` does its imports inside `_init_converter` and falls through to `self._converter = None` if Marker isn't installed. The package is **not** in `pyproject.toml` deps. Production deployments must install Marker separately; the test suite uses `MockContentAdapter`. This means `get_content_variant` for non-abstract variants will silently degrade to "markdown not available" if Marker isn't installed at runtime — no startup-time check.

8. **The `Lens` abstraction was anticipated in `RankerSnapshot` but only partially.** `src/arxiv_mcp/models/interest.py:120-138` includes `signal_types_applied: list[str]` and `weights: dict[str, float]`, both of which are **already** lens-shaped (dynamic, dict-based, list-based). What's missing is `lens_name: str | None` or `lenses_consulted: list[str]`. The snapshot also tracks single counts (`seed_paper_count`, `followed_author_count`, ...) per the four current signal types — those would generalize naturally to `signal_counts_by_type: dict[str, int]`.

9. **CLI is a complete second surface that mirrors MCP.** `src/arxiv_mcp/workflow/cli.py` (1130 lines) plus `src/arxiv_mcp/interest/cli.py` (617 lines) plus the smaller `search/cli.py`, `enrichment/cli.py`, `content/cli.py`, `ingestion/cli.py` together provide CLI coverage for every operation the MCP layer exposes. They construct services the same way (`_make_session_factory()` at `src/arxiv_mcp/workflow/cli.py:25-29` mirrors `app_lifespan` from `mcp/server.py:52-90`). **Any v0.2 surface change that adds a `lens=` parameter has to be added to both surfaces.** This is why the prior audit called the work "moderate blast-radius."

10. **The stack imports `InterestProfile` from `db.models` in many places** but there is **no application-level abstraction over "profile."** `ProfileService` does CRUD against the ORM model; `ProfileRankingService` loads it via direct `select(InterestProfile)`; `SuggestionService` does its own `selectinload(InterestProfile.signals)`. There is no `ProfileRepository` or `ProfileLoader` abstraction. This is fine for v0.1 and consistent with the codebase's "thin services over ORM" style, but it means a per-lens profile loader needs to know the ORM shape directly — there's no abstraction layer to slot into.

11. **The cooldown logic in `EnrichmentService.enrich_paper`** at `src/arxiv_mcp/enrichment/service.py:73-94` short-circuits with cached enrichment data if `last_attempted_at >= cooldown_threshold` — but it returns the cached `EnrichmentResult` constructed from the DB row, not a "skipped" signal. Callers cannot distinguish "we just enriched" from "we returned cache-from-cooldown." The docstring at `:65` documents this implicitly ("Skip if within window, unless refresh=True").

12. **Pagination cursors are score-or-date tuples encoded as opaque tokens.** `src/arxiv_mcp/search/service.py:86-102` switches the `sort_value_extractor` based on `has_text_search`. Cursors round-trip the literal sort value (string or float) plus the paper_id. This works only because there is one sort dimension at a time — a per-lens-score result with multiple dimensions would need a richer cursor or per-page deterministic ordering.

13. **No telemetry or metrics layer.** `structlog` is used in `enrichment/`, `content/`, `ingestion/oai_pmh.py` but not in the discovery/workflow path or the MCP server. There is no request-level observability, no per-tool latency metric, no per-lens counter slot. Adding these is out of scope but worth flagging as a gap that any production hardening would have to address.

14. **`search/cli.py` and `interest/cli.py` end with `pass` no-op decorators** at `src/arxiv_mcp/search/cli.py:188` and `src/arxiv_mcp/enrichment/cli.py:135`. Some CLI subgroups are empty parent groups awaiting subcommands (`@click.group(...) def foo(): pass`). This is normal Click usage but worth knowing — those `pass` lines are not dead code, they are required syntax.

15. **`get_settings()` is `@lru_cache`d at `src/arxiv_mcp/config.py:101-104`.** Settings are loaded once at first call from `.env` + environment variables. This is a singleton. Test code that needs to override settings for a single test cannot do so without invalidating the cache (which the test suite does by relying on `Settings.test_database_url` being a separate field, set at import time). For multi-tenant or per-request settings, this would need to change.

---

*Map authored 2026-05-01. Cross-references: prior `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` for the lens-extensibility property audit; `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` for the multi-lens substrate decision; `.planning/STATE.md` for v0.2 planning status.*
