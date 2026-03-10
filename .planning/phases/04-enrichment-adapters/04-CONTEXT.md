# Phase 4: Enrichment Adapters - Context

**Gathered:** 2026-03-09
**Status:** Ready for planning
**Source:** Inferred from Phases 1-3 context, ADRs, codebase patterns, design docs, open questions, and project principles

<domain>
## Phase Boundary

Papers are lazily enriched with OpenAlex data (topics, citations, related works, FWCI) on demand, with external ID resolution (arXiv ID <-> DOI <-> OpenAlex ID) and full provenance tracking. This phase builds on Phase 1 (paper model with external ID columns and processing tier infrastructure) and Phase 2 (workflow state for collection-scoped enrichment triggers). No Semantic Scholar adapter (v2), no content normalization, no MCP server yet. Enrichment data becomes available for Phase 3 ranking integration later but Phase 4 does not modify the ranking pipeline itself.

</domain>

<decisions>
## Implementation Decisions

### OpenAlex as core enrichment source
- OpenAlex is the primary (and only Phase 4) enrichment source — answers Open Question Q4: "Should OpenAlex be considered core? Yes."
- Semantic Scholar is explicitly deferred to v2 (ADVN-01) — the semantic_scholar_id column stays unpopulated in Phase 4
- Crossref/OpenCitations deferred to v2 (ADVN-02) — DOI resolution comes as a byproduct of OpenAlex enrichment
- The adapter interface should be general enough to accommodate future enrichment sources (Semantic Scholar, Crossref) but Phase 4 implements only OpenAlex

### Lazy, demand-driven enrichment semantics (ENRC-02)
- Enrichment is triggered explicitly by user or agent, never by the system autonomously — direct application of ADR-0002 ("enrich lazily")
- No background enrichment jobs, no automatic promotion, no scheduled enrichment — answers Open Question Q16 with "demand-driven" strategy
- Three trigger scopes:
  1. Single paper: `enrich paper <arxiv_id>` — the atomic unit
  2. Collection-scoped: `enrich collection <slug>` — enrich all unenriched papers in a collection
  3. Search-scoped: `enrich search "<query>"` — enrich results from a search (runs search, enriches returned papers)
- Collection and search scopes are still "on demand" — user explicitly initiates, system doesn't pre-enrich
- Batch enrichment uses OpenAlex batch lookups (up to 50 IDs per request via pipe-separated filter) for efficiency within demand-driven triggers
- No cascading enrichment: enriching paper A does NOT auto-enrich papers in A's related_works — that would violate demand-driven principle

### Enrichment cooldown and staleness
- Default cooldown of 7 days — papers enriched within the cooldown period are skipped (with informational message)
- Cooldown is configurable via settings (`enrichment_cooldown_days`)
- `--refresh` flag bypasses cooldown for explicit re-enrichment
- Staleness is informational only — displayed in paper detail view ("enriched 45 days ago") but no automatic re-enrichment
- Rationale: citation counts and topics do change over time, but auto-refresh violates cost-awareness (ADR-0002) and demand-driven philosophy
- Re-enrichment overwrites previous enrichment data (last-write-wins) and updates the enrichment timestamp

### Enrichment data model
- Separate `PaperEnrichment` table (not columns on Paper) because:
  - Clear lifecycle separation (enrichment can become stale; paper metadata from arXiv is stable)
  - Single-row upsert for refresh operations (not many scattered columns)
  - Sparse storage (most papers won't be enriched; avoid cluttering Paper with nullable columns)
  - Distinct provenance (enrichment timestamp is separate from paper fetch timestamp)
- PaperEnrichment record contains:
  - `arxiv_id` (FK to Paper, unique constraint — one enrichment record per paper)
  - `openalex_id` (String, the resolved OpenAlex work ID)
  - `doi` (String, populated from OpenAlex if available)
  - `cited_by_count` (Integer, for direct use as ranking signal)
  - `fwci` (Float, nullable — not all papers have FWCI)
  - `topics` (JSONB — OpenAlex topic hierarchy: [{id, display_name, subfield, field, domain, score}])
  - `related_works` (JSONB — array of OpenAlex work IDs, typically up to 10)
  - `counts_by_year` (JSONB — [{year, cited_by_count}] for citation velocity analysis)
  - `openalex_type` (String — work type from OpenAlex: "article", "preprint", etc.)
  - `openalex_raw` (JSONB — full raw OpenAlex response for fields we don't extract yet, future-proofing)
  - `source_api` (String — "openalex" for now, extensible to "semantic_scholar" etc.)
  - `api_version` (String — OpenAlex API version used, for reproducibility)
  - `enriched_at` (DateTime with timezone — when this enrichment was performed)
  - `last_attempted_at` (DateTime — tracks even failed attempts to avoid hammering)
  - `status` (String — "success", "not_found", "partial", "error")
  - `error_detail` (String, nullable — error message if status is not "success")
- ALSO update Paper table's existing columns on successful enrichment:
  - `Paper.openalex_id` — populate from enrichment (enables direct lookups)
  - `Paper.doi` — populate if OpenAlex provides it and our DOI is null
  - `Paper.processing_tier` → promote to ProcessingTier.ENRICHED (2)
  - `Paper.promotion_reason` → set to "openalex_enrichment"
- This dual storage is intentional: Paper gets the ID columns for fast lookups; PaperEnrichment holds the full enrichment payload

### External ID resolution chain (ENRC-03)
- Primary resolution: arXiv ID → OpenAlex ID (using OpenAlex filter: `ids.openalex` with arXiv external ID, or `filter=ids.arxiv:<arxiv_id>`)
- Secondary resolution: DOI → OpenAlex ID (using `https://api.openalex.org/works/doi:<doi>`)
- Resolution strategy: try arXiv ID first (most direct), fall back to DOI if available and arXiv ID lookup fails
- Bidirectional: after successful resolution, Paper gets openalex_id and doi populated; enrichment record stores all IDs
- Papers without DOI: perfectly fine — OpenAlex indexes many arXiv preprints directly by arXiv ID. DOI is a nice-to-have, not required
- Papers not in OpenAlex: record status="not_found" with last_attempted_at timestamp. Don't retry automatically (user can force with --refresh)
- Resolution is part of the enrichment operation, not a separate step — when you enrich a paper, the system first resolves its external IDs, then fetches enrichment data

### Provenance tracking (ENRC-04)
- Every enrichment record stores: source_api, api_version, enriched_at — per ADR-0003 ("every content artifact records source and acquisition path")
- Enrichment operations are logged: paper_id, timestamp, api_calls_made, status, response_time_ms
- Enrichment stats available via CLI: total enrichments, success/failure counts, API call counts
- openalex_raw field preserves the complete API response for future field extraction without re-querying

### OpenAlex API strategy
- Polite pool as default: include `mailto` parameter in all requests → 10 req/s rate limit (vs 1 req/s without)
- Optional API key for premium access: configured via settings, used when available, not required
- Rate limiting: configurable default of 5 req/s (conservative within polite pool limits)
- Exponential backoff on 429 responses with configurable max retries (default: 3)
- Request timeout: 30 seconds per request
- Batch queries: use OpenAlex filter API with pipe-separated IDs for multi-paper lookups (up to 50 per request)
- User-Agent header: identify as arxiv-mcp with version for responsible API citizenship
- API base URL configurable (`openalex_api_url`, default: https://api.openalex.org) for testing with mocks

### Error handling and resilience
- Never lose existing enrichment data on failure — if re-enrichment fails, previous enrichment record is preserved
- "Not found" is a valid and recorded result — some arXiv papers simply aren't in OpenAlex. Track last_attempted_at to avoid repeated failed lookups
- Partial enrichment: if OpenAlex returns a response but missing some fields (e.g., no FWCI, no topics), accept what we got and store with status="partial"
- Network failures: fail gracefully, log error, don't update enrichment record
- Batch operation failures: partial success is acceptable — enrich what we can, report failures for the rest
- Rate limit handling: backoff is per-session, not persisted — each CLI invocation starts fresh
- API schema changes: openalex_raw stores the full response; if OpenAlex adds/removes fields, our extraction logic can be updated without losing access to the raw data

### arXiv remains system of record
- OpenAlex data is supplementary enrichment, NEVER overwrites arXiv metadata (title, authors, abstract, categories) — per doc 07 §1: "arXiv should remain the authoritative source"
- If OpenAlex title/authors differ from arXiv (they sometimes do), log a warning but keep arXiv data as canonical
- Processing tier promotion and enrichment data do not affect arXiv metadata integrity
- OAI-PMH re-harvesting already preserves processing_tier and promotion_reason (existing upsert safety in ingestion/oai_pmh.py)

### Related works handling
- Store related_works as JSONB array of OpenAlex work IDs (not arXiv IDs — OpenAlex uses its own ID format like "W2741809807")
- When displaying related works, resolve OpenAlex IDs against our database to find papers we have locally
- Papers in related_works that aren't in our database: show OpenAlex ID with a note ("not in local corpus"). Don't create stub papers — that violates metadata-first (ADR-0002)
- Related works resolution is a read-time operation, not a write-time import

### OpenAlex topics handling
- Use OpenAlex topics API (not deprecated concepts endpoint)
- Store primary_topic and topics (up to 3) as structured JSONB
- Topic structure: {id, display_name, subfield: {id, display_name}, field: {id, display_name}, domain: {id, display_name}, score}
- Topics are OpenAlex's classification, not ours — we display and surface them but don't merge them into arXiv categories
- No GIN index on topics JSONB initially — add if topic-based filtering becomes a common query pattern later

### FWCI (Field-Weighted Citation Impact) handling
- Store as nullable float on PaperEnrichment — not all papers have FWCI
- FWCI > 1.0 means above average for the field; < 1.0 means below average
- Display in paper detail with interpretation hint ("1.5x field average" or "0.8x field average")
- FWCI is most meaningful for papers 2+ years old — for very recent papers, flag as "FWCI may be unreliable (paper is recent)"
- FWCI is a prime candidate for future ranking signal integration (Phase 3 extension) but not implemented in Phase 4

### Citation velocity (counts_by_year)
- Store counts_by_year as JSONB array of {year, cited_by_count} objects
- This enables citation velocity computation (change in citations over time) for future ranking signals
- Not computed or displayed in Phase 4 — raw data stored for future use
- Use case: identify papers with accelerating citation growth ("trending" papers)

### Processing tier promotion
- Automatic promotion to ProcessingTier.ENRICHED (2) on successful OpenAlex enrichment
- promotion_reason set to "openalex_enrichment"
- Papers with status="not_found" stay at their current tier — enrichment was attempted but no data available
- Promotion is a one-way ratchet: later phases can promote further (EMBEDDED=3, CONTENT_PARSED=4) but never demote below ENRICHED
- Retrospective demotion (Open Question Q17): not implemented in Phase 4. If implemented later, it would be soft demotion (keep metadata, drop expensive artifacts), never delete enrichment data

### Enrichment operations on non-existent papers
- Enrichment requires the paper to exist in our database — no enriching by arbitrary arXiv ID that hasn't been ingested
- If user tries to enrich a paper not in the database: clear error message suggesting ingestion first
- This prevents orphaned enrichment records and maintains data integrity

### Concurrent enrichment safety
- Last-write-wins at the database level — enrichment data is idempotent for the same source
- No row-level locking for enrichment — the operation is an upsert (INSERT ON CONFLICT UPDATE)
- If two agents try to enrich the same paper simultaneously, both will succeed with nearly identical data from OpenAlex
- The enriched_at timestamp reflects the latest successful operation

### CLI structure
- New `enrich` subgroup following established Click subgroup pattern:
  - `arxiv-mcp enrich paper <arxiv_id>` — enrich a single paper
  - `arxiv-mcp enrich collection <slug>` — enrich all unenriched papers in a collection
  - `arxiv-mcp enrich search "<query>" [--limit N]` — enrich papers from a search result
  - `arxiv-mcp enrich status [<arxiv_id>]` — show enrichment status (single paper or summary stats)
  - `arxiv-mcp enrich refresh <arxiv_id>` — force re-enrich bypassing cooldown
- All batch commands show progress: "Enriching 47 papers... 23/47 complete (3 not found, 1 error)"
- Dry-run mode for batch commands: `--dry-run` shows what would be enriched without making API calls
- Enrichment data visible in existing `arxiv-mcp paper show <id>` command (extended output section)
- Quiet mode (`-q`) for agent/pipeline use — machine-readable output, no progress bars

### Enrichment display in paper detail
- Extend `paper show` output with enrichment section (only shown if paper has enrichment data):
  ```
  Enrichment (OpenAlex, 2026-03-09):
    OpenAlex ID: W2741809807
    DOI: 10.48550/arXiv.1706.03762
    Citations: 147,832
    FWCI: 245.7 (245.7x field average)
    Topics: Transformers (AI), Natural Language Processing, Deep Learning
    Related Works: 3 in local corpus, 7 external
  ```
- Include enrichment timestamp and source API for provenance transparency
- Related works that exist locally shown with titles; external ones shown as OpenAlex IDs

### Author data from OpenAlex
- OpenAlex provides disambiguated author IDs and institutional affiliations
- Store in openalex_raw for future use, but don't extract into separate fields in Phase 4
- Phase 3's followed_author feature uses name strings; OpenAlex author IDs could improve matching in a future Phase 3 extension
- Not in scope for Phase 4 to modify the interest profile system

### Adapter interface design
- Define a simple EnrichmentAdapter protocol (Python Protocol class):
  - `resolve_ids(arxiv_ids: list[str]) -> dict[str, ExternalIds]`
  - `enrich(arxiv_ids: list[str]) -> list[EnrichmentResult]`
  - `adapter_name: str` (e.g., "openalex")
- OpenAlexAdapter implements this protocol
- Future adapters (SemanticScholarAdapter, CrossrefAdapter) implement the same protocol
- The service layer works with the protocol, not the concrete adapter — following ADR-0001's "multiple strategies coexist" principle

### Configuration settings
- `openalex_email` (String, optional but strongly recommended) — for polite pool access
- `openalex_api_key` (String, optional) — for premium API access
- `openalex_api_url` (String, default: https://api.openalex.org) — configurable for testing
- `enrichment_cooldown_days` (Integer, default: 7) — days before allowing re-enrichment
- `enrichment_batch_size` (Integer, default: 50) — max papers per batch API request
- `enrichment_rate_limit` (Float, default: 5.0) — requests per second
- All loaded from .env via Pydantic Settings (same pattern as existing config)

### Module organization
- New `enrichment/` package under src/arxiv_mcp/:
  - `enrichment/__init__.py`
  - `enrichment/service.py` — EnrichmentService (orchestrates resolution + enrichment + storage)
  - `enrichment/openalex.py` — OpenAlexAdapter (HTTP client, response parsing, rate limiting)
  - `enrichment/models.py` — Pydantic schemas for enrichment data (EnrichmentResult, ExternalIds, TopicInfo, etc.)
  - `enrichment/cli.py` — Click subgroup commands
- ORM model (PaperEnrichment) in existing `db/models.py` (same single-Base pattern)
- Alembic migration 004 for PaperEnrichment table

### Test strategy
- Recorded HTTP fixtures (JSON files) for OpenAlex API responses — no live API calls in automated tests
- Use well-known papers as test fixtures (e.g., "Attention Is All You Need" arXiv:1706.03762)
- Test cases: successful enrichment, not-found, partial data, rate limiting, network failure, cooldown enforcement, batch operations, ID resolution chain
- Integration tests: enrichment → paper detail display, collection-scoped enrichment, processing tier promotion
- Optional `--live` pytest marker for manual verification against real OpenAlex API (skipped in CI)

### Hardware and cost constraints
- Target hardware (Dionysus): same as previous phases — Phase 4 is network-bound (HTTP to OpenAlex API), not CPU or GPU bound
- OpenAlex polite pool (free with email) is sufficient for single-user on-demand enrichment
- At 5 req/s rate limit and 50 papers per batch request, one batch call enriches 50 papers in 0.2 seconds — collections of hundreds of papers enrich in seconds
- No GPU needed, no significant storage impact (enrichment records are small JSONB rows)
- Budget-conscious: zero mandatory API costs. Premium OpenAlex access is optional enhancement, not requirement

### Phase 5+ anticipation
- Content normalization (Phase 5): OpenAlex provides `open_access.oa_url` and content availability metadata — store in openalex_raw for Phase 5 use
- MCP integration (Phase 6): enrichment data accessible via `get_paper` tool and `paper://` resource
- Ranking integration: cited_by_count, FWCI, and topic overlap are ready to become RankingPipeline signal types when wired (small extension to Phase 3's pipeline)
- Semantic Scholar adapter (v2): same protocol interface, different implementation — plug-and-play when ready

### Claude's Discretion
- HTTP client choice (httpx vs aiohttp — httpx recommended for async + sync support and typing)
- Exact OpenAlex API response field extraction (which fields from the raw response to extract vs leave in openalex_raw)
- Rate limiter implementation (token bucket vs simple sleep vs semaphore)
- Progress display format for batch operations (tqdm-style vs simple counter)
- Alembic migration: whether to add index on PaperEnrichment.enriched_at (useful for "recently enriched" queries)
- Whether to add a GIN index on PaperEnrichment.topics JSONB
- Error retry details (exact backoff multiplier, jitter)
- Enrichment stats aggregation queries
- Exact format of enrichment section in paper show output
- Whether to log enrichment operations to a separate table or use structured logging
- OpenAlex select parameter optimization (request only needed fields to reduce response size)

</decisions>

<specifics>
## Specific Ideas

- The dual-storage pattern (key IDs on Paper + full payload on PaperEnrichment) balances fast lookups with clean lifecycle separation. Paper.openalex_id enables direct "find by OpenAlex ID" queries; PaperEnrichment holds the full enrichment context with its own provenance.
- OpenAlex's filter API supports pipe-separated multi-ID lookups: `filter=ids.openalex:W123|W456|W789`. This makes collection-scoped enrichment efficient — 50 papers per API call instead of 50 separate calls.
- Storing openalex_raw (full API response) is cheap insurance: if OpenAlex adds new fields or we discover we need a field we didn't initially extract, we can retroactively parse from stored raw data without re-querying the API.
- The "not found" status with last_attempted_at prevents the system from repeatedly hammering OpenAlex for papers that genuinely aren't indexed. The cooldown applies to successful AND failed lookups.
- Related works stored as OpenAlex IDs (not arXiv IDs) is correct because: (a) OpenAlex uses its own ID namespace, (b) many related works may be non-arXiv publications (journals, conferences), (c) resolution to local papers happens at display time.
- Processing tier promotion creates a natural query filter: `WHERE processing_tier >= 2` gives "all enriched papers" — useful for future features like "browse enriched papers" or "show only papers with citation data."
- The adapter protocol is deliberately minimal (2 methods + 1 property) to make future adapters trivial to implement. Semantic Scholar adapter would resolve IDs via S2 API and return similar enrichment structure.
- Enrichment does not modify the ranking pipeline (Phase 3), but the data model is ranking-ready: cited_by_count as integer is immediately usable as a SignalScore, FWCI as float is immediately usable, topics overlap with profile interests is computable. The wiring is a small future task, not a Phase 4 concern.
- OpenAlex provides `is_retracted` boolean — storing this in openalex_raw enables future retraction alerts without requiring schema changes.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `db/models.py`: Paper model with existing external ID columns (openalex_id, doi, semantic_scholar_id), ProcessingTier enum with ENRICHED=2
- `db/engine.py`: Async engine and session factory — reuse for enrichment service DI
- `config.py`: Pydantic Settings with .env loading and @lru_cache singleton — extend with enrichment settings
- `models/paper.py`: PaperDetail Pydantic schema already includes openalex_id, processing_tier, promotion_reason fields
- `workflow/collections.py`: CollectionService pattern — template for EnrichmentService
- `workflow/export.py`: PaperDetail construction from ORM model — extend for enrichment display
- `ingestion/oai_pmh.py`: Upsert safety that preserves processing_tier and promotion_reason (line ~299)
- `cli.py`: Click subgroup registration pattern for adding `enrich` subgroup

### Established Patterns
- SQLAlchemy ORM with async engine, single Base class in db/models.py
- Hand-written Alembic migrations (not autogenerated)
- Service layer with session_factory + settings DI
- Pydantic BaseSettings for configuration with env_file loading
- Click subgroups for CLI organization
- JSONB for flexible/evolving data storage (SavedQuery params, InterestSignal config)
- Composition over modification (WorkflowSearchService wraps SearchService, ProfileRankingService wraps that)
- Absence-means-default pattern (no enrichment record = not enriched)
- Provenance on all operations (source, timestamp)
- Slug-style identifiers for named entities
- Soft limits with warnings

### Integration Points
- Paper.arxiv_id as FK target for PaperEnrichment
- Paper.openalex_id, Paper.doi — populate during enrichment
- Paper.processing_tier — promote to ENRICHED on success
- Paper.promotion_reason — set to "openalex_enrichment"
- CollectionService.list_papers() — provides paper lists for collection-scoped enrichment
- SearchService.search_papers() — provides paper lists for search-scoped enrichment
- PaperDetail pydantic model — extend with enrichment section for display

</code_context>

<deferred>
## Deferred Ideas

- Semantic Scholar adapter (ADVN-01) — v2, same protocol interface, different API
- Crossref/OpenCitations adapter (ADVN-02) — v2, for broader citation graph
- Ranking signal integration with enrichment data (cited_by_count, FWCI, topic overlap) — future Phase 3 extension, data model ready
- Citation velocity computation from counts_by_year — future ranking signal
- OpenAlex author disambiguation for Phase 3 followed_author improvement — data stored in openalex_raw, wiring is future work
- Retraction detection/alerting via OpenAlex is_retracted — data available in openalex_raw
- Topic-based paper clustering/browsing using OpenAlex topic hierarchy — requires UX design
- Enrichment budget management (daily API call limits, cost tracking dashboard) — only needed if usage scales beyond polite pool
- Background enrichment scheduler (cron-triggered enrichment of recently-triaged papers) — violates demand-driven principle for now, reconsider if user feedback suggests it
- Batch enrichment export (dump all enrichment data as JSON for analysis) — can be done via existing paper show in a loop
- OpenAlex content availability metadata for Phase 5 content acquisition — stored in openalex_raw, Phase 5 extracts when needed

</deferred>

---

*Phase: 04-enrichment-adapters*
*Context gathered: 2026-03-09 via inference from Phases 1-3 patterns, ADRs, design docs, open questions, and codebase analysis*
