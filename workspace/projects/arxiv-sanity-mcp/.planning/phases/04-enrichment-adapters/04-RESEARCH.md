# Phase 4: Enrichment Adapters - Research

**Researched:** 2026-03-09
**Domain:** OpenAlex API integration, lazy enrichment patterns, external ID resolution
**Confidence:** HIGH

## Summary

Phase 4 implements on-demand paper enrichment via the OpenAlex API, adding topics, citation counts, FWCI, related works, and external ID resolution (arXiv ID <-> DOI <-> OpenAlex ID) with full provenance tracking. The core challenge is building a reliable, rate-limited HTTP client for OpenAlex's credit-based API, designing a clean `PaperEnrichment` table with JSONB fields for semi-structured data, and providing CLI commands for single-paper and batch enrichment operations.

OpenAlex has undergone significant changes since early 2025: API keys are now **mandatory** (as of February 13, 2026), the pricing model is credit-based (not simple request-per-second), and concepts are deprecated in favor of topics. The `ids` object on Work does NOT contain an `arxiv` field -- arXiv papers must be resolved via DOI (`10.48550/arXiv.XXXX.XXXXX` prefix) or via `indexed_in:arxiv` filter + title search. The project already has `httpx` as a dependency, and `respx` is the standard mock library for testing httpx-based clients.

**Primary recommendation:** Build the OpenAlexAdapter with httpx AsyncClient, use DOI-based resolution as primary lookup strategy (arXiv DOI prefix `10.48550/arXiv.`), add `respx` to dev dependencies for HTTP mocking, and store enrichment data in a separate `PaperEnrichment` table with JSONB columns for topics, related_works, counts_by_year, and raw response.

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions
- OpenAlex is the primary (and only Phase 4) enrichment source -- Semantic Scholar deferred to v2
- Lazy, demand-driven enrichment semantics (never autonomous): single paper, collection-scoped, search-scoped triggers
- Default 7-day cooldown with `--refresh` bypass
- Separate `PaperEnrichment` table (not columns on Paper) with defined schema including openalex_raw JSONB
- Also update Paper.openalex_id, Paper.doi, Paper.processing_tier on successful enrichment
- External ID resolution chain: arXiv ID -> OpenAlex (try arXiv first, fall back to DOI)
- Provenance tracking: source_api, api_version, enriched_at on every enrichment record
- Polite pool as default (email-based), optional API key for premium
- Rate limiting: configurable default of 5 req/s
- Batch queries: pipe-separated IDs for multi-paper lookups (up to 50 per request)
- Never overwrite arXiv metadata (title, authors, abstract, categories) with OpenAlex data
- Related works stored as OpenAlex work IDs, resolved at display time
- Use OpenAlex topics (not deprecated concepts)
- EnrichmentAdapter protocol with 2 methods + 1 property
- New `enrich` CLI subgroup with paper/collection/search/status/refresh commands
- Module: `enrichment/` package with service.py, openalex.py, models.py, cli.py
- ORM model in existing db/models.py, Alembic migration 004
- Recorded HTTP fixtures for tests (no live API calls in automated tests)

### Claude's Discretion
- HTTP client choice (httpx recommended -- already a dependency)
- Exact OpenAlex API response field extraction vs leave in openalex_raw
- Rate limiter implementation (token bucket vs simple sleep vs semaphore)
- Progress display format for batch operations
- Whether to add index on PaperEnrichment.enriched_at
- Whether to add GIN index on PaperEnrichment.topics JSONB
- Error retry details (backoff multiplier, jitter)
- Enrichment stats aggregation queries
- Exact format of enrichment section in paper show output
- Whether to log enrichment operations to separate table or structured logging
- OpenAlex select parameter optimization

### Deferred Ideas (OUT OF SCOPE)
- Semantic Scholar adapter (ADVN-01) -- v2
- Crossref/OpenCitations adapter (ADVN-02) -- v2
- Ranking signal integration with enrichment data -- future Phase 3 extension
- Citation velocity computation from counts_by_year
- OpenAlex author disambiguation for followed_author improvement
- Retraction detection/alerting
- Topic-based paper clustering/browsing
- Background enrichment scheduler
- Batch enrichment export

</user_constraints>

<phase_requirements>

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| ENRC-01 | System enriches papers lazily via OpenAlex (topics, citations, related works, FWCI) | OpenAlex Work object confirmed to contain: primary_topic + topics (up to 3), cited_by_count, fwci, related_works (array of 20 OpenAlex IDs), counts_by_year. Topics use 4-level hierarchy (domain > field > subfield > topic). |
| ENRC-02 | OpenAlex enrichment is triggered on demand, not bulk (cost-aware) | OpenAlex credit system: singleton lookups are FREE, list+filter costs 10 credits. $1/day free = 10,000 list calls. Batch via pipe-separated DOIs (up to 100 values per filter) is optimal for collection-scoped enrichment. |
| ENRC-03 | System resolves external IDs: arXiv ID <-> DOI <-> OpenAlex ID | OpenAlex ids object does NOT include arxiv field. Resolution must use: (1) DOI with arXiv prefix `10.48550/arXiv.{id}` for singleton lookup (FREE), (2) DOI filter with pipe-separated values for batch (10 credits). Bidirectional: OpenAlex response provides doi and openalex ID. |
| ENRC-04 | Enrichment data records provenance (source, timestamp, API version) | Store source_api="openalex", enriched_at timestamp, api_version string. OpenAlex API version not explicitly versioned in URL -- use date-based versioning or response header if available. |

</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| httpx | >=0.28 | Async HTTP client for OpenAlex API | Already a project dependency; supports async/sync, excellent typing, built-in timeout/retry support |
| SQLAlchemy | >=2.0 | ORM for PaperEnrichment table, JSONB columns | Already a project dependency; established async pattern with asyncpg |
| Alembic | >=1.14 | Migration 004 for PaperEnrichment table | Already a project dependency; hand-written migration pattern established |
| Pydantic | >=2.10 | EnrichmentResult, ExternalIds, TopicInfo schemas | Already a project dependency; BaseSettings for enrichment config |
| Click | >=8.1 | `enrich` CLI subgroup commands | Already a project dependency; subgroup pattern established |
| structlog | >=24.4 | Structured logging for enrichment operations | Already a project dependency; used throughout codebase |

### Supporting (Dev)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| respx | >=0.22 | Mock httpx requests in tests | All enrichment/adapter tests -- mock OpenAlex API responses |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| httpx | aiohttp | httpx already in project deps, better typing, sync+async support; aiohttp is async-only and would add a new dependency |
| respx | pytest-httpx | respx has better pattern matching, async support, and base_url scoping; pytest-httpx is simpler but less flexible |
| respx | VCR.py/vcrpy | VCR records real requests (requires live API first), respx uses programmatic fixtures (no live dependency); recorded JSON fixtures + respx is cleaner |
| custom rate limiter | tenacity | tenacity handles retries but not rate limiting; custom asyncio.Semaphore + sleep is simpler for this use case |

**Installation:**
```bash
# respx is the only new dependency (dev only)
pip install respx>=0.22
```

Add to pyproject.toml `[dependency-groups] dev`:
```toml
"respx>=0.22",
```

## Architecture Patterns

### Recommended Project Structure
```
src/arxiv_mcp/
  enrichment/
    __init__.py          # Package init, exports
    service.py           # EnrichmentService: orchestrates resolution + enrichment + storage
    openalex.py          # OpenAlexAdapter: HTTP client, response parsing, rate limiting
    models.py            # Pydantic schemas: EnrichmentResult, ExternalIds, TopicInfo, etc.
    cli.py               # Click subgroup: enrich paper/collection/search/status/refresh
  db/
    models.py            # Add PaperEnrichment ORM model (same Base)
  config.py              # Extend Settings with enrichment fields
  cli.py                 # Register enrich subgroup
  models/
    paper.py             # Extend PaperDetail with enrichment display fields
alembic/versions/
  004_enrichment_table.py  # Hand-written migration for paper_enrichments table
tests/
  test_enrichment/
    __init__.py
    conftest.py          # Session factory, sample data, respx fixtures
    fixtures/            # JSON files with recorded OpenAlex API responses
      openalex_work_attention.json    # "Attention Is All You Need" response
      openalex_work_not_found.json    # Empty results response
      openalex_work_partial.json      # Response with missing fields
      openalex_batch_response.json    # Multi-work batch response
    test_adapter.py      # OpenAlexAdapter unit tests (respx mocked)
    test_service.py      # EnrichmentService integration tests (DB + mocked HTTP)
    test_cli.py          # CLI command tests
    test_models.py       # Pydantic schema validation tests
```

### Pattern 1: Adapter Protocol with Service Layer
**What:** Define a minimal `EnrichmentAdapter` protocol that the `EnrichmentService` depends on; implement `OpenAlexAdapter` as the concrete implementation. Service handles DB operations and orchestration; adapter handles HTTP and response parsing.
**When to use:** Always -- this is the locked architecture from CONTEXT.md.
**Example:**
```python
# Source: CONTEXT.md locked decision + codebase patterns
from typing import Protocol

class EnrichmentAdapter(Protocol):
    """Protocol for enrichment source adapters."""
    adapter_name: str

    async def resolve_ids(self, arxiv_ids: list[str]) -> dict[str, ExternalIds]:
        """Resolve arXiv IDs to external identifiers."""
        ...

    async def enrich(self, arxiv_ids: list[str]) -> list[EnrichmentResult]:
        """Fetch enrichment data for papers by arXiv ID."""
        ...
```

### Pattern 2: DOI-Based arXiv Resolution (CRITICAL)
**What:** OpenAlex `ids` object does NOT contain an `arxiv` field. ArXiv papers must be resolved via their DOI, which uses the prefix `10.48550/arXiv.{arxiv_id}`. Singleton lookup by DOI is FREE (0 credits).
**When to use:** Always for single-paper enrichment. For batch, use `filter=doi:DOI1|DOI2|...` (10 credits per call, up to 100 DOIs).
**Example:**
```python
# Singleton lookup (FREE - 0 credits)
# arXiv ID: 1706.03762 -> DOI: 10.48550/arXiv.1706.03762
url = f"https://api.openalex.org/works/doi:10.48550/arXiv.{arxiv_id}"

# Batch lookup (10 credits per call, up to 100 DOIs)
dois = "|".join(f"https://doi.org/10.48550/arXiv.{aid}" for aid in arxiv_ids)
url = f"https://api.openalex.org/works?filter=doi:{dois}&per_page=100"
```

### Pattern 3: Service Layer with Session Factory DI
**What:** EnrichmentService follows the same DI pattern as CollectionService: `session_factory` + `settings` in constructor, each method opens its own session.
**When to use:** All service-layer code.
**Example:**
```python
# Source: existing CollectionService pattern in workflow/collections.py
class EnrichmentService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        adapter: EnrichmentAdapter | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.adapter = adapter or OpenAlexAdapter(settings)

    async def enrich_paper(self, arxiv_id: str, refresh: bool = False) -> EnrichmentResult:
        async with self.session_factory() as session:
            # 1. Verify paper exists
            # 2. Check cooldown (skip if within cooldown and not refresh)
            # 3. Call adapter.enrich([arxiv_id])
            # 4. Upsert PaperEnrichment record
            # 5. Update Paper.openalex_id, Paper.doi, Paper.processing_tier
            ...
```

### Pattern 4: Credit-Aware Request Strategy
**What:** OpenAlex uses credit-based pricing. Singleton lookups by ID/DOI are FREE. List+filter calls cost 10 credits each. Optimize by using singleton endpoints for single papers and batch filter for collections.
**When to use:** All OpenAlex API interactions.
**Example:**
```python
# Single paper: use singleton endpoint (FREE, 0 credits)
response = await client.get(
    f"{base_url}/works/doi:10.48550/arXiv.{arxiv_id}",
    params={"api_key": api_key, "select": SELECTED_FIELDS},
)

# Batch papers: use filter endpoint (10 credits per call)
response = await client.get(
    f"{base_url}/works",
    params={
        "filter": f"doi:{pipe_separated_dois}",
        "per_page": 100,
        "api_key": api_key,
        "select": SELECTED_FIELDS,
    },
)
```

### Pattern 5: Upsert with Provenance Preservation
**What:** INSERT ... ON CONFLICT (arxiv_id) DO UPDATE for PaperEnrichment. On successful enrichment, also update Paper columns. On failure, preserve existing enrichment data.
**When to use:** All enrichment write operations.
**Example:**
```python
# Source: SQLAlchemy 2.0 PostgreSQL dialect
from sqlalchemy.dialects.postgresql import insert as pg_insert

stmt = pg_insert(PaperEnrichment).values(
    arxiv_id=arxiv_id,
    openalex_id=result.openalex_id,
    doi=result.doi,
    cited_by_count=result.cited_by_count,
    fwci=result.fwci,
    topics=result.topics,
    related_works=result.related_works,
    counts_by_year=result.counts_by_year,
    openalex_type=result.openalex_type,
    openalex_raw=result.raw_response,
    source_api="openalex",
    api_version=result.api_version,
    enriched_at=now,
    last_attempted_at=now,
    status="success",
    error_detail=None,
)
stmt = stmt.on_conflict_do_update(
    index_elements=["arxiv_id"],
    set_={
        "openalex_id": stmt.excluded.openalex_id,
        "doi": stmt.excluded.doi,
        # ... all fields
        "enriched_at": stmt.excluded.enriched_at,
        "status": stmt.excluded.status,
    },
)
await session.execute(stmt)
```

### Anti-Patterns to Avoid
- **Creating httpx.AsyncClient per request:** The existing `ArxivAPIClient._request()` creates a new AsyncClient per call. For OpenAlex, create ONE client per adapter instance (or per batch operation) and reuse it. This enables connection pooling and is more efficient.
- **Using `ids.arxiv` in OpenAlex:** This field does not exist. Always use DOI-based resolution.
- **Overwriting arXiv metadata:** Never update Paper.title, Paper.authors_text, Paper.abstract from OpenAlex -- only update Paper.openalex_id, Paper.doi, Paper.processing_tier, Paper.promotion_reason.
- **Using deprecated `concepts` endpoint:** Use `topics` and `primary_topic` fields instead.
- **Hammering OpenAlex for not-found papers:** Record `status="not_found"` with `last_attempted_at` and respect cooldown on failed lookups too.
- **Requesting full Work object when only some fields needed:** Use `select=` parameter to reduce response payload and credit cost.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HTTP mocking for tests | Custom mock classes or monkeypatching | respx library | Pattern matching, async support, base_url scoping, pytest fixtures built-in |
| Exponential backoff | Custom retry loops | asyncio.sleep with exponential formula | Simple enough; tenacity is overkill for 3-retry 429 handling |
| JSON fixture loading | Inline dict literals in tests | JSON files in tests/test_enrichment/fixtures/ | Real API responses are large; keeping them in files makes tests readable and fixtures reusable |
| Rate limiting | Complex token bucket | asyncio.Semaphore + time.monotonic tracking | The project already uses this pattern in ArxivAPIClient; sufficient for 5 req/s target |
| JSONB upsert | Manual SQL strings | SQLAlchemy `pg_insert().on_conflict_do_update()` | Type-safe, handles JSONB serialization automatically |

**Key insight:** This phase is primarily an HTTP client + data mapping problem. The codebase already has all the infrastructure patterns (async engine, session factory, service DI, CLI subgroups, Alembic migrations). The new work is the OpenAlex-specific HTTP client, response parsing, and the enrichment data model.

## Common Pitfalls

### Pitfall 1: OpenAlex API Key Now Required
**What goes wrong:** API calls fail with 409 errors after 100 free credits without a key.
**Why it happens:** As of February 13, 2026, OpenAlex requires API keys. The old "polite pool with email" approach is no longer the primary mechanism.
**How to avoid:** Make `openalex_api_key` a required setting (or at minimum, strongly warn on startup if not set). Free API key provides $1/day = 10,000 list calls or unlimited singleton lookups.
**Warning signs:** Getting 409 or 429 errors immediately.

### Pitfall 2: arXiv ID Not in OpenAlex IDs Object
**What goes wrong:** Code tries to filter by `ids.arxiv` or look up works by arXiv ID directly -- gets empty results or errors.
**Why it happens:** OpenAlex `ids` object only contains: `openalex`, `doi`, `mag`, `pmid`, `pmcid`. No `arxiv` field.
**How to avoid:** Use DOI-based resolution. ArXiv papers have DOIs with prefix `10.48550/arXiv.{id}`. For papers without DOI, fall back to title+author search as last resort.
**Warning signs:** Empty results when enriching papers that definitely exist in OpenAlex.

### Pitfall 3: Batch Filter URL Length Limit
**What goes wrong:** Batch queries with many DOIs fail because URL exceeds 4096 characters.
**Why it happens:** OpenAlex enforces a maximum URL length of 4096 characters. Each arXiv DOI is ~35 characters + separator, so the practical limit is ~80-90 DOIs per batch, not 100.
**How to avoid:** Limit batch size to 50 DOIs per request (as specified in CONTEXT.md). This stays well within the URL length limit. The API also limits to 100 OR values per filter.
**Warning signs:** HTTP 414 (URI Too Long) errors on batch requests.

### Pitfall 4: Credit Exhaustion on Large Collections
**What goes wrong:** Enriching a large collection (1000+ papers) exhausts the daily $1 free credit allocation.
**Why it happens:** Each batch filter call costs 10 credits. 1000 papers / 50 per batch = 20 calls = 200 credits. But combined with other operations, credits can add up.
**How to avoid:** Use singleton lookups (FREE) for single papers. Use batch only for collection-scoped enrichment. Log credit usage. Implement `--dry-run` to preview without API calls.
**Warning signs:** 429 errors partway through a batch operation.

### Pitfall 5: Stale `concepts` Field Usage
**What goes wrong:** Code parses `concepts` from OpenAlex response instead of `topics`.
**Why it happens:** Older documentation and examples still reference concepts. Concepts are deprecated but still returned in API responses.
**How to avoid:** Always use `primary_topic` and `topics` fields. Ignore `concepts` entirely.
**Warning signs:** Getting `concepts` data that uses the old MAG-based classification instead of the new topic hierarchy.

### Pitfall 6: Paper Not in Our Database
**What goes wrong:** User tries to enrich by arXiv ID for a paper that hasn't been ingested. Creates orphaned enrichment record or crashes.
**Why it happens:** Enrichment requires the paper to exist locally (FK constraint).
**How to avoid:** Always verify paper exists in DB before calling the adapter. Return clear error message suggesting ingestion first.
**Warning signs:** IntegrityError on FK constraint during enrichment insert.

### Pitfall 7: Related Works Contain Non-arXiv Publications
**What goes wrong:** Code tries to resolve all related_works to local arXiv papers and fails.
**Why it happens:** OpenAlex related_works contains OpenAlex IDs for ALL related works, not just arXiv papers. Many are journal articles, conference papers, etc.
**How to avoid:** Store related_works as-is (OpenAlex IDs). At display time, resolve against local DB and show "3 in local corpus, 7 external" style summary.
**Warning signs:** Low match rate when resolving related works to local papers.

### Pitfall 8: httpx AsyncClient Not Properly Closed
**What goes wrong:** Connection pool leaks, "Event loop is closed" errors in tests.
**Why it happens:** Creating AsyncClient without proper lifecycle management.
**How to avoid:** Use `async with httpx.AsyncClient() as client:` or manage client lifecycle in adapter `__aenter__`/`__aexit__` methods. For the adapter, create client in a context manager method or pass it from outside.
**Warning signs:** ResourceWarning about unclosed connections, test flakiness.

## Code Examples

### OpenAlex Work Object Structure (Verified from Live API)
```python
# Source: Verified against https://api.openalex.org/works/doi:10.48550/arXiv.1706.03762
# "Attention Is All You Need" - actual response structure

work = {
    "id": "https://openalex.org/W2741809807",
    "doi": "https://doi.org/10.48550/arxiv.1706.03762",
    "ids": {
        "openalex": "https://openalex.org/W2741809807",
        "doi": "https://doi.org/10.48550/arxiv.1706.03762",
        "mag": 2741809807,
        # NOTE: No "arxiv" key exists in ids object
    },
    "type": "preprint",
    "is_retracted": False,
    "cited_by_count": 6497,
    "fwci": 115.7593,  # nullable float
    "citation_normalized_percentile": {
        "value": 0.9996,
        "is_in_top_1_percent": True,
        "is_in_top_10_percent": True,
    },
    "primary_topic": {
        "id": "https://openalex.org/T10032",
        "display_name": "Natural Language Processing Techniques",
        "score": 0.999,
        "subfield": {"id": "...", "display_name": "Artificial Intelligence"},
        "field": {"id": "...", "display_name": "Computer Science"},
        "domain": {"id": "...", "display_name": "Physical Sciences"},
    },
    "topics": [  # Up to 3 topics
        {
            "id": "https://openalex.org/T10032",
            "display_name": "Natural Language Processing Techniques",
            "score": 0.999,
            "subfield": {"id": "...", "display_name": "Artificial Intelligence"},
            "field": {"id": "...", "display_name": "Computer Science"},
            "domain": {"id": "...", "display_name": "Physical Sciences"},
        },
        # ... up to 2 more topics
    ],
    "related_works": [
        "https://openalex.org/W2965373594",
        # ... array of up to 20 OpenAlex work URLs
    ],
    "counts_by_year": [
        {"year": 2026, "cited_by_count": 123},
        {"year": 2025, "cited_by_count": 456},
        # ... spanning multiple years
    ],
    "open_access": {
        "is_oa": True,
        "oa_status": "gold",
        "oa_url": "https://...",
    },
    "indexed_in": ["arxiv", "crossref"],
}
```

### Select Parameter for Reduced Payloads
```python
# Source: https://developers.openalex.org (select fields documentation)
# Request only needed fields to reduce response size and credits
SELECTED_FIELDS = ",".join([
    "id",
    "doi",
    "ids",
    "type",
    "is_retracted",
    "cited_by_count",
    "fwci",
    "citation_normalized_percentile",
    "primary_topic",
    "topics",
    "related_works",
    "counts_by_year",
    "open_access",
    "indexed_in",
    "authorships",  # Stored in raw for future use
])

# Use in API call
params = {"select": SELECTED_FIELDS, "api_key": api_key}
```

### Rate Limiter Pattern
```python
# Source: existing ArxivAPIClient._calculate_delay() pattern in ingestion/arxiv_api.py
import asyncio
import time

class RateLimiter:
    """Simple rate limiter using monotonic clock and asyncio.sleep."""

    def __init__(self, requests_per_second: float = 5.0):
        self._min_interval = 1.0 / requests_per_second
        self._last_request_time: float = 0.0

    async def acquire(self) -> None:
        """Wait until rate limit allows next request."""
        elapsed = time.monotonic() - self._last_request_time
        remaining = self._min_interval - elapsed
        if remaining > 0:
            await asyncio.sleep(remaining)
        self._last_request_time = time.monotonic()
```

### Exponential Backoff for 429 Responses
```python
# Pattern: exponential backoff with jitter for 429 handling
import random

async def _request_with_retry(
    client: httpx.AsyncClient,
    url: str,
    params: dict,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> httpx.Response:
    for attempt in range(max_retries + 1):
        response = await client.get(url, params=params, timeout=30.0)
        if response.status_code != 429 or attempt == max_retries:
            response.raise_for_status()
            return response
        # Exponential backoff with jitter
        delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
        await asyncio.sleep(delay)
    return response  # unreachable but satisfies type checker
```

### respx Test Fixture Pattern
```python
# Source: respx documentation + project test patterns
import json
import respx
import httpx
import pytest

@pytest.fixture
def openalex_fixture():
    """Load recorded OpenAlex API response from fixtures."""
    fixture_path = Path(__file__).parent / "fixtures" / "openalex_work_attention.json"
    return json.loads(fixture_path.read_text())

@pytest.fixture
def mocked_openalex():
    """Provide a respx mock router for OpenAlex API."""
    with respx.mock(base_url="https://api.openalex.org") as mock:
        yield mock

async def test_enrich_single_paper(mocked_openalex, openalex_fixture):
    mocked_openalex.get(
        "/works/doi:10.48550/arXiv.1706.03762",
    ).mock(return_value=httpx.Response(200, json=openalex_fixture))

    adapter = OpenAlexAdapter(settings)
    results = await adapter.enrich(["1706.03762"])
    assert len(results) == 1
    assert results[0].cited_by_count > 0
```

### Alembic Migration Pattern
```python
# Source: existing 003_interest_tables.py migration pattern
# Migration 004: paper_enrichments table

def upgrade() -> None:
    op.create_table(
        "paper_enrichments",
        sa.Column("arxiv_id", sa.String(20),
                  sa.ForeignKey("papers.arxiv_id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("openalex_id", sa.String(64), nullable=True),
        sa.Column("doi", sa.String(256), nullable=True),
        sa.Column("cited_by_count", sa.Integer(), nullable=True),
        sa.Column("fwci", sa.Float(), nullable=True),
        sa.Column("topics", postgresql.JSONB(), nullable=True),
        sa.Column("related_works", postgresql.JSONB(), nullable=True),
        sa.Column("counts_by_year", postgresql.JSONB(), nullable=True),
        sa.Column("openalex_type", sa.String(64), nullable=True),
        sa.Column("openalex_raw", postgresql.JSONB(), nullable=True),
        sa.Column("source_api", sa.String(32), nullable=False, server_default="openalex"),
        sa.Column("api_version", sa.String(32), nullable=True),
        sa.Column("enriched_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_attempted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("error_detail", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "status IN ('success', 'not_found', 'partial', 'error')",
            name="ck_enrichment_status_valid",
        ),
    )
    op.create_index("idx_enrichments_status", "paper_enrichments", ["status"])
    op.create_index("idx_enrichments_enriched_at", "paper_enrichments", ["enriched_at"])
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| OpenAlex email-based "polite pool" | API key required (free tier still available) | February 13, 2026 | Must register for API key; `openalex_api_key` is now essential, not optional |
| Request-per-second rate limiting | Credit-based pricing ($1/day free) | ~Late 2025 | Different endpoints cost different credits; singleton lookups are FREE |
| OpenAlex Concepts (MAG-based) | OpenAlex Topics (4-level hierarchy) | 2024 | Use `topics` and `primary_topic` fields; `concepts` deprecated |
| `mailto` parameter for polite pool | `api_key` query parameter | February 2026 | Authentication mechanism changed |
| Unlimited anonymous API access | 100 credits/day without key | February 2026 | Anonymous access essentially removed for production use |

**Deprecated/outdated:**
- `concepts` field: Still returned in API responses but deprecated. Use `topics` instead.
- `x_concepts` on sources/institutions: Being removed, replaced by topics.
- `mailto` parameter: Was the polite pool mechanism. Now superseded by API key authentication.

## Open Questions

1. **arXiv papers without DOI prefix**
   - What we know: Most modern arXiv papers (2007+) have DOIs with prefix `10.48550/arXiv.{id}`. Older papers may not.
   - What's unclear: What percentage of arXiv papers lack the `10.48550` DOI? Is there a fallback that works reliably?
   - Recommendation: Use DOI prefix as primary strategy. For papers where DOI lookup returns empty, fall back to title-based search (`search=title` with the paper's title). Record `status="not_found"` if both approaches fail. The CONTEXT.md already acknowledges "Papers not in OpenAlex: record status=not_found."

2. **OpenAlex API versioning**
   - What we know: OpenAlex does not have explicit API version numbers in the URL (unlike `/v3/` etc.). The API evolves continuously.
   - What's unclear: How to meaningfully populate `api_version` field.
   - Recommendation: Store the date of the API call as the version string (e.g., "2026-03-09") and include any version headers if present in the response. The `openalex_raw` field preserves the full response regardless.

3. **OpenAlex ID format in related_works**
   - What we know: Related works are returned as full OpenAlex URLs like `https://openalex.org/W2965373594`. The work count is approximately 20 per paper.
   - What's unclear: Whether to store the full URL or just the W-prefixed ID.
   - Recommendation: Store the full URL as returned by the API (consistent with how OpenAlex represents IDs). Extract W-ID only at display time if needed.

4. **Paper.openalex_id column length**
   - What we know: OpenAlex IDs are full URLs like `https://openalex.org/W2741809807` (38+ chars). The existing column is `String(32)`.
   - What's unclear: Whether to store the full URL or the short form.
   - Recommendation: Store the short form `W2741809807` (fits in String(32) easily). Convert from/to full URL in the adapter. This is consistent with how `Paper.doi` stores the DOI without the `https://doi.org/` prefix.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ with pytest-asyncio |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `pytest tests/test_enrichment/ -x -q` |
| Full suite command | `pytest tests/ -x --timeout=30` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| ENRC-01 | Enrich paper with topics, citations, FWCI, related works | integration | `pytest tests/test_enrichment/test_service.py::test_enrich_single_paper -x` | Wave 0 |
| ENRC-01 | Parse OpenAlex topics structure correctly | unit | `pytest tests/test_enrichment/test_models.py::test_parse_topics -x` | Wave 0 |
| ENRC-01 | Parse FWCI as nullable float | unit | `pytest tests/test_enrichment/test_models.py::test_parse_fwci -x` | Wave 0 |
| ENRC-02 | Enrichment respects 7-day cooldown | integration | `pytest tests/test_enrichment/test_service.py::test_cooldown_enforcement -x` | Wave 0 |
| ENRC-02 | Refresh flag bypasses cooldown | integration | `pytest tests/test_enrichment/test_service.py::test_refresh_bypasses_cooldown -x` | Wave 0 |
| ENRC-02 | Collection-scoped batch enrichment | integration | `pytest tests/test_enrichment/test_service.py::test_enrich_collection -x` | Wave 0 |
| ENRC-03 | Resolve arXiv ID to OpenAlex ID via DOI | unit | `pytest tests/test_enrichment/test_adapter.py::test_resolve_via_doi -x` | Wave 0 |
| ENRC-03 | Bidirectional: Paper gets openalex_id and doi populated | integration | `pytest tests/test_enrichment/test_service.py::test_paper_ids_updated -x` | Wave 0 |
| ENRC-03 | Batch DOI resolution with pipe-separated filter | unit | `pytest tests/test_enrichment/test_adapter.py::test_batch_resolution -x` | Wave 0 |
| ENRC-04 | Enrichment record stores source_api, enriched_at, api_version | integration | `pytest tests/test_enrichment/test_service.py::test_provenance_tracking -x` | Wave 0 |
| ENRC-04 | Failed enrichment records status and error_detail | integration | `pytest tests/test_enrichment/test_service.py::test_failed_enrichment -x` | Wave 0 |
| ENRC-04 | Not-found status recorded with last_attempted_at | integration | `pytest tests/test_enrichment/test_service.py::test_not_found_recorded -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `pytest tests/test_enrichment/ -x -q`
- **Per wave merge:** `pytest tests/ -x --timeout=30`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_enrichment/__init__.py` -- package init
- [ ] `tests/test_enrichment/conftest.py` -- session factory, sample data, respx fixtures
- [ ] `tests/test_enrichment/fixtures/` -- directory for JSON fixture files
- [ ] `tests/test_enrichment/fixtures/openalex_work_attention.json` -- recorded response for "Attention Is All You Need"
- [ ] `tests/test_enrichment/fixtures/openalex_work_not_found.json` -- empty results response
- [ ] `tests/test_enrichment/fixtures/openalex_batch_response.json` -- multi-work batch response
- [ ] `tests/test_enrichment/test_adapter.py` -- OpenAlexAdapter unit tests
- [ ] `tests/test_enrichment/test_service.py` -- EnrichmentService integration tests
- [ ] `tests/test_enrichment/test_models.py` -- Pydantic schema validation tests
- [ ] Dev dependency: `respx>=0.22` in pyproject.toml

## Sources

### Primary (HIGH confidence)
- OpenAlex API live response: `https://api.openalex.org/works/doi:10.48550/arXiv.1706.03762` -- verified Work object structure, confirmed ids object lacks arxiv field, confirmed topics/primary_topic/fwci/related_works fields
- OpenAlex Authentication & Pricing: `https://developers.openalex.org/how-to-use-the-api/rate-limits-and-authentication` -- confirmed API key required since Feb 13 2026, credit-based pricing, $1/day free
- OpenAlex Topics: `https://developers.openalex.org/api-entities/topics` -- confirmed 4-level hierarchy, concepts deprecated
- OpenAlex Filter docs: `https://developers.openalex.org/api-entities/works/filter-works` -- pipe-separated OR syntax, 100 values max, 4096 char URL limit
- OpenAlex OpenAPI spec: `https://developers.openalex.org/api-reference/openapi.json` -- Work object schema confirmation
- Existing codebase: `src/arxiv_mcp/` -- verified all patterns (service DI, CLI subgroups, Alembic migrations, config, models)

### Secondary (MEDIUM confidence)
- OpenAlex blog: `https://blog.openalex.org/fetch-multiple-dois-in-one-openalex-api-request/` -- batch DOI query pattern
- respx documentation: `https://lundberg.github.io/respx/` -- v0.22 with httpx 0.28 support, async fixtures
- respx PyPI: `https://pypi.org/project/respx/` -- version 0.22.0, Python 3.13 supported

### Tertiary (LOW confidence)
- OpenAlex community discussion on arXiv lookups: multiple Google Groups threads -- arXiv ID not directly in ids object, DOI prefix approach confirmed by community

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries already in project except respx (well-established, version verified)
- Architecture: HIGH -- patterns directly derived from existing codebase + CONTEXT.md locked decisions
- OpenAlex API: HIGH -- verified against live API response and current documentation (post-Feb 2026 changes)
- Pitfalls: HIGH -- verified API key requirement and missing arxiv field against live API; credit system from official docs
- ID Resolution: HIGH -- DOI-based lookup confirmed working via live API call

**Research date:** 2026-03-09
**Valid until:** 2026-04-09 (stable -- OpenAlex API changes infrequently after the Feb 2026 transition)
