# Phase 1: Metadata Substrate - Research

**Researched:** 2026-03-08
**Domain:** arXiv metadata ingestion, PostgreSQL full-text search, Python data pipeline
**Confidence:** HIGH

## Summary

Phase 1 builds the foundational data layer: ingesting arXiv paper metadata via OAI-PMH (and the arXiv API for targeted queries), storing it in PostgreSQL with correct time semantics across four distinct date types, enabling fielded full-text search with AND/OR composition, recent-paper browsing by category and time basis, seed-based related-paper discovery via lexical similarity, and per-paper provenance and license tracking. This is a greenfield Python project targeting PostgreSQL 16.11 already running on the target machine.

The core technical challenges are: (1) parsing arXiv's three OAI-PMH metadata formats (especially `arXivRaw` for version history), (2) correctly modeling arXiv's four time semantics (submission, update, announcement, OAI datestamp) which have different meanings and different availability across data sources, (3) building weighted multi-field full-text search with PostgreSQL tsvector/GIN that supports both fielded queries and ranked results, and (4) implementing keyset-based cursor pagination for predictable result sizes across large datasets.

**Primary recommendation:** Use Python with SQLAlchemy 2.0 + asyncpg for the database layer, Alembic for migrations, oaipmh-scythe for OAI-PMH harvesting, and PostgreSQL's native tsvector/GIN for full-text search. Project management via `uv`. No external search engine needed at this scale.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Configurable category subset inspired by arxiv-sanity's original scope (cs.*, stat.ML, stat.TH, and ML-adjacent math categories). Philosophy excluded.
- Categories configurable at runtime via config file, not hardcoded.
- Historical depth uses recency-weighted influence threshold (NOT simple date cutoff). Recent papers (~2 years): include all. Older papers: require increasing influence signal (citation count via OpenAlex as proxy). Exact thresholds are empirical.
- Phase 1 ingests all metadata but influence-based filtering may need Phase 4 (OpenAlex enrichment) data to fully work. Phase 1 should ingest broadly and support filtering at query time.
- Single paper record stores all arXiv categories; primary category tracked separately.
- Daily incremental harvest matching arXiv's announcement cycle (OAI-PMH updates nightly).
- Rich search results: title, authors, abstract snippet, all categories, all four dates, version info, license.
- Phase 1 schema must anticipate multi-tier processing: include `processing_tier` column, `promotion_reason` provenance field.
- Ingest all new papers at Tier 0-1 (metadata + FTS) with no discrimination at ingestion time.
- Retrospective demotion: soft-demote only expensive artifacts, never delete metadata.

### Claude's Discretion
- Harvesting strategy: CLI command vs background job, resume-on-failure approach
- Influence proxy implementation details (citation count tiers, decay function)
- Project scaffolding: repo layout, dependency management, migration strategy
- Cross-listing dedup strategy
- Lexical similarity method for find_related_papers (tsvector similarity vs TF-IDF)

### Deferred Ideas (OUT OF SCOPE)
- Spike needed: measure influence-based pruning effectiveness across category sets
- Philosophy-adjacent categories (physics.hist-ph, quant-ph)
- Cross-corpus expansion beyond arXiv
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INGS-01 | OAI-PMH bulk harvesting with resumption token handling | oaipmh-scythe handles resumption tokens automatically; arXiv OAI-PMH base URL is `https://oaipmh.arxiv.org/oai`; three metadata formats available (oai_dc, arXiv, arXivRaw) |
| INGS-02 | arXiv API for incremental/targeted queries | arXiv API at `http://export.arxiv.org/api/query` supports fielded search (ti, au, abs, cat), Boolean ops, date ranges, pagination up to 2000 results per call |
| INGS-03 | Four distinct time semantics per paper | arXivRaw format provides version history with per-version dates (submission); arXiv format provides created/updated; OAI datestamp is separate; announcement date derivable from schedule rules or RSS feed pubDate |
| INGS-04 | Per-paper license/rights metadata | License URI available in arXiv and arXivRaw OAI-PMH formats and in RSS dc:rights field |
| INGS-05 | Incremental harvesting with datestamp-based checkpoints | OAI-PMH ListRecords supports `from` parameter for incremental harvesting; arXiv updates metadata nightly ~10:30pm ET Sun-Thu |
| PAPR-01 | Canonical paper model with arXiv ID as primary identifier | arXivRaw schema: id, submitter, version[], categories, title, authors, comments, proxy, report-no, acm-class, msc-class, journal-ref, doi, license, abstract |
| PAPR-02 | Title, authors, abstract, categories, version history | All available from arXivRaw format; arXiv format provides structured author parsing (keyname, forenames, suffix, affiliation) |
| PAPR-03 | External identifiers (DOI, OpenAlex ID, Semantic Scholar ID) | DOI available from arXiv/arXivRaw metadata directly; OpenAlex ID and S2 ID are nullable columns populated in Phase 4 |
| PAPR-04 | Provenance tracking: data source, fetch timestamp, enrichment history | Schema design pattern: source enum, fetched_at timestamp, processing_tier, promotion_reason |
| SRCH-01 | Search by title, author, abstract, category, date range | PostgreSQL weighted tsvector (title=A, authors=B, abstract=C) with GIN index; category and date via SQL WHERE clauses |
| SRCH-02 | AND/OR query composition | PostgreSQL tsquery supports & (AND), \| (OR) operators; websearch_to_tsquery provides natural syntax |
| SRCH-03 | Browse recently announced papers filtered by category | SQL query on announcement_date with category filter; keyset pagination |
| SRCH-04 | Time basis switching (submission, update, announcement) | Store all four dates as separate columns; parameterize ORDER BY / WHERE to use selected time basis |
| SRCH-05 | Find related papers from seed via lexical similarity | PostgreSQL ts_rank_cd on seed paper's tsvector against corpus; alternative: extract top terms from seed abstract and use as tsquery |
| SRCH-06 | Cursor-based pagination with predictable result sizes | Keyset pagination using (sort_field, id) compound cursor; base64-encoded cursor token |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | 3.13 | Runtime | Already installed on target; latest stable |
| SQLAlchemy | 2.0+ | ORM + query builder | Industry standard; async support; PostgreSQL dialect with TSVECTOR, GIN |
| asyncpg | 0.30+ | PostgreSQL async driver | 5x faster than psycopg3; native binary protocol; connection pooling |
| Alembic | 1.14+ | Database migrations | Only serious migration tool for SQLAlchemy; autogenerate support |
| Pydantic | 2.10+ | Data validation + settings | Type-safe config, API model validation, serialization |
| pydantic-settings | 2.7+ | Configuration from env/dotenv | Loads DATABASE_URL, arXiv config from environment |
| oaipmh-scythe | 0.14.0 | OAI-PMH harvesting | Modern fork of Sickle; Python 3.10+; httpx + lxml; handles resumption tokens |
| lxml | 5.3+ | XML parsing | Required by oaipmh-scythe; fast C-based XML parsing for arXivRaw |
| httpx | 0.28+ | HTTP client | Required by oaipmh-scythe; async support; used for arXiv API calls |
| click | 8.1+ | CLI framework | Mature, composable, decorator-based; good for harvest/search commands |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | 1.0+ | .env file loading | Used by pydantic-settings for local dev config |
| structlog | 24.4+ | Structured logging | JSON logs for harvest runs, search queries, error tracking |
| rich | 13.9+ | Terminal output | CLI progress bars during harvest, table display for search results |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| oaipmh-scythe | Sickle 0.7 | Sickle is older, unmaintained; scythe is actively maintained fork with httpx |
| oaipmh-scythe | Raw httpx+lxml | More control but reinvents resumption token handling, pagination |
| click | Typer | Typer is simpler (type hints) but click has better composability for complex CLIs |
| asyncpg | psycopg3 | psycopg3 has sync+async but asyncpg is significantly faster for PostgreSQL |
| SQLAlchemy | Raw asyncpg | Raw asyncpg is faster but loses migration support, schema declaration, query building |
| Elasticsearch | PostgreSQL FTS | Overkill for metadata-only corpus; PostgreSQL FTS handles millions of docs well |

**Installation:**
```bash
uv init arxiv-sanity-mcp
cd arxiv-sanity-mcp
uv add sqlalchemy[asyncio] asyncpg alembic pydantic pydantic-settings
uv add oaipmh-scythe lxml httpx click structlog rich python-dotenv
uv add --dev pytest pytest-asyncio pytest-cov ruff mypy
```

## Architecture Patterns

### Recommended Project Structure
```
arxiv-sanity-mcp/
├── pyproject.toml
├── uv.lock
├── .python-version          # 3.13
├── .env.example             # Template for DATABASE_URL, config
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
├── src/
│   └── arxiv_mcp/
│       ├── __init__.py
│       ├── config.py         # Pydantic Settings (DB, arXiv, categories)
│       ├── cli.py            # Click CLI entry point
│       ├── db/
│       │   ├── __init__.py
│       │   ├── engine.py     # async engine, session factory
│       │   ├── models.py     # SQLAlchemy ORM models (Paper, PaperVersion, etc.)
│       │   └── queries.py    # Query builders (search, browse, related)
│       ├── ingestion/
│       │   ├── __init__.py
│       │   ├── oai_pmh.py    # OAI-PMH harvester (bulk + incremental)
│       │   ├── arxiv_api.py  # arXiv search API client
│       │   ├── parsers.py    # XML parsers for arXiv, arXivRaw, oai_dc formats
│       │   └── mapper.py     # Raw metadata -> canonical Paper model
│       ├── search/
│       │   ├── __init__.py
│       │   ├── service.py    # Search orchestration (fielded, FTS, browse, related)
│       │   ├── pagination.py # Cursor encoding/decoding, keyset logic
│       │   └── ranking.py    # ts_rank weighting, result shaping
│       └── models/
│           ├── __init__.py
│           ├── paper.py      # Pydantic schemas for Paper, SearchResult, etc.
│           └── pagination.py # Pydantic schemas for cursor, page info
├── tests/
│   ├── conftest.py           # Fixtures: test DB, sample papers
│   ├── test_ingestion/
│   ├── test_search/
│   └── test_models/
└── data/
    └── categories.toml       # Default category configuration
```

### Pattern 1: Weighted Multi-Field tsvector with Trigger
**What:** Combine title, authors, and abstract into a single weighted tsvector column using PostgreSQL trigger function.
**When to use:** Always -- this is the core search index.
**Why trigger over generated column:** PostgreSQL GENERATED ALWAYS columns cannot use `setweight()` with multiple source columns in a single expression that concatenates weighted vectors. A trigger function provides full control.

```sql
-- Migration: create tsvector column and trigger
ALTER TABLE papers ADD COLUMN search_vector tsvector;

CREATE FUNCTION papers_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', COALESCE(NEW.title, '')), 'A') ||
    setweight(to_tsvector('simple', COALESCE(NEW.authors_text, '')), 'B') ||
    setweight(to_tsvector('english', COALESCE(NEW.abstract, '')), 'C');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER papers_search_vector_trigger
  BEFORE INSERT OR UPDATE ON papers
  FOR EACH ROW EXECUTE FUNCTION papers_search_vector_update();

CREATE INDEX idx_papers_search_vector ON papers USING GIN (search_vector);
```

### Pattern 2: Keyset Cursor Pagination
**What:** Encode last-seen (sort_value, id) as base64 cursor token for stable pagination.
**When to use:** All search and browse endpoints (SRCH-06).

```python
import base64, json
from dataclasses import dataclass

@dataclass
class Cursor:
    sort_value: str  # ISO date or float score
    paper_id: str    # arXiv ID as tiebreaker

    def encode(self) -> str:
        return base64.urlsafe_b64encode(
            json.dumps([self.sort_value, self.paper_id]).encode()
        ).decode()

    @classmethod
    def decode(cls, token: str) -> "Cursor":
        sort_value, paper_id = json.loads(
            base64.urlsafe_b64decode(token.encode())
        )
        return cls(sort_value=sort_value, paper_id=paper_id)

# SQL pattern: WHERE (sort_col, id) > (:last_sort, :last_id) ORDER BY sort_col, id LIMIT :page_size
```

### Pattern 3: arXivRaw XML Parser with Version History
**What:** Parse arXivRaw metadata format to extract all fields including per-version history.
**When to use:** Primary harvesting format for bulk ingestion (INGS-01).

```python
from lxml import etree
from dataclasses import dataclass, field

ARXIV_RAW_NS = "http://arxiv.org/OAI/arXivRaw/"

@dataclass
class PaperVersion:
    version: str          # "v1", "v2", etc.
    date: str             # submission date of this version
    size: str | None = None
    source_type: str | None = None

@dataclass
class RawPaperMetadata:
    arxiv_id: str
    submitter: str
    versions: list[PaperVersion]
    categories: str
    title: str | None = None
    authors: str | None = None
    abstract: str | None = None
    comments: str | None = None
    journal_ref: str | None = None
    doi: str | None = None
    license: str | None = None
    report_no: str | None = None
    # Derived fields
    submission_date: str | None = None    # v1 date
    update_date: str | None = None        # latest version date
    primary_category: str | None = None   # first in categories list

def parse_arxiv_raw(xml_element) -> RawPaperMetadata:
    ns = {"ar": ARXIV_RAW_NS}
    # ... parse using lxml xpath with namespace
```

### Pattern 4: Time Semantics Storage
**What:** Store four distinct timestamps per paper with clear semantics.
**When to use:** Core paper model (INGS-03).

| Column | Type | Source | Meaning |
|--------|------|--------|---------|
| `submitted_date` | `TIMESTAMP WITH TIME ZONE` | arXivRaw v1 date | When first version was submitted |
| `updated_date` | `TIMESTAMP WITH TIME ZONE NULL` | arXivRaw latest version date | When most recent version was submitted (NULL if only v1) |
| `announced_date` | `DATE NULL` | Derived from arXiv schedule rules or RSS pubDate | When paper appeared in daily listings |
| `oai_datestamp` | `DATE` | OAI-PMH response header | When OAI record was last modified (includes admin changes) |

### Anti-Patterns to Avoid
- **Single "date" column:** arXiv has four distinct temporal concepts. Collapsing them loses critical semantics for browsing and time-basis switching.
- **Storing categories as a single string:** Use both a `categories` text field (for display/search) AND a `categories` array column or junction table (for filtering). The primary category should be a separate column.
- **Hardcoded category lists:** Categories must come from config, not code. The user has explicitly required this.
- **Offset-based pagination:** OFFSET degrades with table size. Keyset pagination is O(1) regardless of page depth.
- **Expression-only GIN index (no stored tsvector):** Without a stored column, every search query must recompute to_tsvector, defeating the purpose. Also prevents using setweight for field prioritization.
- **Using generated column for weighted tsvector:** PostgreSQL GENERATED ALWAYS AS cannot reference the same row's columns in a way that allows multiple setweight calls with concatenation. Use a trigger instead.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| OAI-PMH protocol handling | Custom HTTP + XML resumption token logic | oaipmh-scythe | Resumption tokens, retry, pagination, XML namespaces are all handled |
| Database migrations | Manual DDL scripts | Alembic | Schema versioning, rollback, autogenerate from SQLAlchemy models |
| Configuration management | Custom TOML/YAML parser with validation | pydantic-settings | Type-safe, env var support, .env files, validation errors |
| Full-text search engine | Elasticsearch/Solr/Meilisearch | PostgreSQL tsvector + GIN | Already running; handles millions of docs; no extra service to maintain |
| Date parsing | Manual string parsing | `datetime.fromisoformat` / `dateutil.parser` | arXiv dates come in various formats; dateutil handles them all |
| CLI framework | argparse | click | Subcommands, options, help generation, composability |

**Key insight:** The entire Phase 1 data pipeline can run on PostgreSQL alone. No external search engine, no Redis (yet), no separate queue. PostgreSQL's FTS is sufficient for the metadata corpus size (est. 2.5M papers total arXiv, subset by configured categories likely 500K-1M).

## Common Pitfalls

### Pitfall 1: arXiv OAI-PMH URL Changed in March 2025
**What goes wrong:** Code uses old base URL `http://export.arxiv.org/oai2` which may redirect or fail.
**Why it happens:** Most tutorials and blog posts reference the old URL.
**How to avoid:** Use the new URL: `https://oaipmh.arxiv.org/oai`
**Warning signs:** 301 redirects, connection errors during harvesting.

### Pitfall 2: OAI Datestamp != Submission Date
**What goes wrong:** Treating OAI-PMH datestamp as submission or announcement date produces incorrect time-based queries.
**Why it happens:** arXiv has bulk-updated metadata records on several occasions, resetting datestamps. Administrative/bibliographic changes also update datestamps without being "new" papers.
**How to avoid:** Store OAI datestamp separately. Use it ONLY for incremental harvesting checkpoints (the `from` parameter). Use arXivRaw version history for actual submission/update dates.
**Warning signs:** Papers from 2010 appearing in "recently announced" lists.

### Pitfall 3: Announcement Date Is Not Directly Available from OAI-PMH
**What goes wrong:** No single OAI-PMH field gives the announcement date. Developers assume submission date = announcement date.
**Why it happens:** arXiv's announcement schedule has day-of-week rules, holidays, and moderation holds. A paper submitted Monday at 13:55 ET is announced that evening; submitted at 14:05 ET, it's announced Tuesday evening.
**How to avoid:** Derive announcement date from: (1) RSS feed pubDate if available, (2) the arXiv schedule rules (Mon-Thu 14:00 ET cutoff, announcements at 20:00 ET, weekend batching), or (3) approximate from arXiv ID which encodes the announcement month/sequence.
**Warning signs:** Off-by-one-day errors in "recent papers" browsing, weekend papers appearing on wrong day.

### Pitfall 4: arXivRaw Author String Is Unstructured
**What goes wrong:** arXivRaw provides authors as a single free-text string. The `arXiv` format provides structured author parsing (keyname, forenames, suffix, affiliation).
**Why it happens:** arXivRaw is close to arXiv's internal format. Structured author data requires the `arXiv` metadata prefix.
**How to avoid:** Harvest with BOTH `arXivRaw` (for version history, full metadata) AND `arXiv` (for structured authors). Or harvest arXivRaw and parse authors heuristically, accepting some noise.
**Recommended approach:** Harvest arXivRaw as primary format. Store raw author string. For structured author data, make a supplementary pass with `arXiv` format or defer to Phase 4 enrichment via OpenAlex.

### Pitfall 5: Alembic Autogenerate + tsvector GIN Index Instability
**What goes wrong:** Alembic's autogenerate repeatedly detects "changes" to GIN indexes using to_tsvector expressions, producing spurious migration files.
**Why it happens:** Known Alembic issue (#1390) where expression-based index comparison fails for FTS expressions.
**How to avoid:** Write the initial FTS migration manually (not autogenerated). Add the tsvector trigger and GIN index in a hand-written migration. Mark the index in Alembic's `include_object` exclusion list to prevent autogenerate churn.
**Warning signs:** New migration files appearing that only drop and recreate the same index.

### Pitfall 6: Rate Limiting on arXiv APIs
**What goes wrong:** Hammering arXiv's API or OAI-PMH endpoint gets your IP throttled or blocked.
**Why it happens:** arXiv explicitly requests: API = 3 second delay between requests; OAI-PMH = bursts of 4 req/sec with 1 second sleep.
**How to avoid:** Implement configurable rate limiting. For bulk harvest, OAI-PMH resumption tokens naturally pace requests. For API queries, enforce minimum 3-second inter-request delay.
**Warning signs:** HTTP 429 or 503 responses, connection resets.

### Pitfall 7: Cross-Listed Paper Duplication
**What goes wrong:** Papers cross-listed to multiple categories appear in multiple OAI-PMH set harvests, creating duplicate records.
**Why it happens:** OAI-PMH set-based harvesting (e.g., `set=cs`) returns all papers in any cs.* category, including cross-listings.
**How to avoid:** Use arXiv ID as natural dedup key. On INSERT, use `ON CONFLICT (arxiv_id) DO UPDATE` to merge category lists and update metadata. Track primary_category separately from all categories.
**Warning signs:** Duplicate paper counts, category lists that don't include all cross-listings.

## Code Examples

### Example 1: OAI-PMH Bulk Harvest with oaipmh-scythe
```python
# Source: oaipmh-scythe docs + arXiv OAI-PMH docs
from oaipmh_scythe import Scythe
from datetime import date

ARXIV_OAI_URL = "https://oaipmh.arxiv.org/oai"

def harvest_papers(
    from_date: date | None = None,
    category_set: str | None = None,  # e.g., "cs" for all CS
    metadata_prefix: str = "arXivRaw",
) -> Iterator[Record]:
    """Harvest arXiv metadata via OAI-PMH."""
    with Scythe(ARXIV_OAI_URL) as scythe:
        params = {"metadataPrefix": metadata_prefix}
        if from_date:
            params["from"] = from_date.isoformat()
        if category_set:
            params["set"] = category_set
        records = scythe.list_records(**params)
        for record in records:
            yield record  # resumption tokens handled automatically
```

### Example 2: SQLAlchemy Paper Model with FTS
```python
# Source: SQLAlchemy 2.0 docs + PostgreSQL FTS docs
from sqlalchemy import (
    Column, String, Text, DateTime, Date, Integer,
    Index, text, ARRAY, Enum
)
from sqlalchemy.dialects.postgresql import TSVECTOR, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime, date
import enum

class Base(DeclarativeBase):
    pass

class ProcessingTier(enum.IntEnum):
    METADATA_ONLY = 0
    FTS_INDEXED = 1
    ENRICHED = 2
    EMBEDDED = 3
    CONTENT_PARSED = 4

class Paper(Base):
    __tablename__ = "papers"

    # Identity
    arxiv_id: Mapped[str] = mapped_column(String(20), primary_key=True)

    # Core metadata
    title: Mapped[str | None] = mapped_column(Text)
    authors_text: Mapped[str | None] = mapped_column(Text)  # Raw author string
    abstract: Mapped[str | None] = mapped_column(Text)
    submitter: Mapped[str | None] = mapped_column(String(256))
    comments: Mapped[str | None] = mapped_column(Text)
    journal_ref: Mapped[str | None] = mapped_column(Text)
    report_no: Mapped[str | None] = mapped_column(String(256))

    # Classification
    categories: Mapped[str] = mapped_column(Text)                # Space-separated, all categories
    primary_category: Mapped[str | None] = mapped_column(String(20))
    category_list: Mapped[list[str] | None] = mapped_column(ARRAY(String))  # For array ops
    msc_class: Mapped[str | None] = mapped_column(String(256))
    acm_class: Mapped[str | None] = mapped_column(String(256))

    # External identifiers
    doi: Mapped[str | None] = mapped_column(String(256))
    openalex_id: Mapped[str | None] = mapped_column(String(32))      # Phase 4
    semantic_scholar_id: Mapped[str | None] = mapped_column(String(64))  # Phase 4

    # Time semantics (INGS-03)
    submitted_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    announced_date: Mapped[date | None] = mapped_column(Date)
    oai_datestamp: Mapped[date | None] = mapped_column(Date)

    # Rights (INGS-04)
    license_uri: Mapped[str | None] = mapped_column(String(256))

    # Version info
    latest_version: Mapped[int | None] = mapped_column(Integer)
    version_history: Mapped[dict | None] = mapped_column(JSONB)  # [{version, date, size}]

    # Processing tier (anticipates multi-tier processing)
    processing_tier: Mapped[int] = mapped_column(Integer, default=0)
    promotion_reason: Mapped[str | None] = mapped_column(String(64))

    # Provenance (PAPR-04)
    source: Mapped[str] = mapped_column(String(32), default="oai_pmh")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_metadata_update: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Full-text search vector (populated by trigger)
    search_vector: Mapped[str | None] = mapped_column(TSVECTOR)

    __table_args__ = (
        Index("idx_papers_search_vector", "search_vector", postgresql_using="gin"),
        Index("idx_papers_primary_category", "primary_category"),
        Index("idx_papers_submitted_date", "submitted_date"),
        Index("idx_papers_announced_date", "announced_date"),
        Index("idx_papers_updated_date", "updated_date"),
        Index("idx_papers_oai_datestamp", "oai_datestamp"),
        Index("idx_papers_categories_gin", "category_list", postgresql_using="gin"),
        Index("idx_papers_processing_tier", "processing_tier"),
    )
```

### Example 3: Fielded Search with AND/OR Composition
```python
# Source: PostgreSQL 18 docs on text search controls
from sqlalchemy import select, func, text, or_, and_
from sqlalchemy.dialects.postgresql import TSVECTOR

async def search_papers(
    session,
    query_text: str | None = None,
    title: str | None = None,
    author: str | None = None,
    category: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    time_basis: str = "announced",  # "submitted" | "updated" | "announced"
    cursor: Cursor | None = None,
    page_size: int = 20,
):
    """Fielded search with AND/OR composition (SRCH-01, SRCH-02)."""
    stmt = select(Paper)

    # Full-text search on combined fields
    if query_text:
        tsquery = func.websearch_to_tsquery("english", query_text)
        stmt = stmt.where(Paper.search_vector.op("@@")(tsquery))
        stmt = stmt.order_by(
            func.ts_rank_cd(Paper.search_vector, tsquery).desc(),
            Paper.arxiv_id,
        )

    # Fielded search: title only
    if title:
        title_tsquery = func.plainto_tsquery("english", title)
        title_vector = func.to_tsvector("english", Paper.title)
        stmt = stmt.where(title_vector.op("@@")(title_tsquery))

    # Fielded search: author only (use 'simple' config for names)
    if author:
        author_tsquery = func.plainto_tsquery("simple", author)
        author_vector = func.to_tsvector("simple", Paper.authors_text)
        stmt = stmt.where(author_vector.op("@@")(author_tsquery))

    # Category filter
    if category:
        stmt = stmt.where(Paper.category_list.any(category))

    # Date range filter on selected time basis
    date_col = {
        "submitted": Paper.submitted_date,
        "updated": Paper.updated_date,
        "announced": Paper.announced_date,
    }[time_basis]
    if date_from:
        stmt = stmt.where(date_col >= date_from)
    if date_to:
        stmt = stmt.where(date_col <= date_to)

    # Keyset pagination
    if cursor:
        # ... apply cursor WHERE clause
        pass

    stmt = stmt.limit(page_size + 1)  # Fetch one extra to detect has_more
    # ...
```

### Example 4: Browse Recent Papers by Category and Time Basis
```python
async def browse_recent(
    session,
    category: str | None = None,
    time_basis: str = "announced",
    days: int = 7,
    cursor: Cursor | None = None,
    page_size: int = 50,
):
    """Browse recently announced papers (SRCH-03, SRCH-04)."""
    date_col = {
        "submitted": Paper.submitted_date,
        "updated": Paper.updated_date,
        "announced": Paper.announced_date,
    }[time_basis]

    cutoff = date.today() - timedelta(days=days)
    stmt = (
        select(Paper)
        .where(date_col >= cutoff)
        .order_by(date_col.desc(), Paper.arxiv_id.desc())
    )

    if category:
        stmt = stmt.where(Paper.category_list.any(category))

    # Apply cursor, limit, execute...
```

### Example 5: Find Related Papers via Lexical Similarity
```python
async def find_related_papers(
    session,
    seed_arxiv_id: str,
    page_size: int = 20,
):
    """Find related papers from a seed via lexical similarity (SRCH-05).

    Strategy: Extract the seed paper's tsvector, then rank all other papers
    by ts_rank_cd against a tsquery derived from the seed's top terms.
    """
    # Step 1: Get seed paper's abstract
    seed = await session.get(Paper, seed_arxiv_id)
    if not seed or not seed.abstract:
        return []

    # Step 2: Use websearch_to_tsquery on key terms from seed abstract
    # Alternative: use ts_stat to get top terms from seed's tsvector
    seed_query = func.websearch_to_tsquery("english", seed.title + " " + seed.abstract[:500])

    stmt = (
        select(Paper, func.ts_rank_cd(Paper.search_vector, seed_query).label("score"))
        .where(Paper.arxiv_id != seed_arxiv_id)
        .where(Paper.search_vector.op("@@")(seed_query))
        .order_by(text("score DESC"))
        .limit(page_size)
    )
    # ...
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| arXiv OAI-PMH at export.arxiv.org/oai2 | New URL: oaipmh.arxiv.org/oai | March 2025 | Must use new URL; old may redirect |
| Sickle for OAI-PMH | oaipmh-scythe (modernized fork) | 2024-2025 | httpx backend, Python 3.10+, active maintenance |
| SQLAlchemy 1.x with psycopg2 | SQLAlchemy 2.0 with asyncpg | 2023+ | Native async, mapped_column, type hints throughout |
| pip + requirements.txt | uv + pyproject.toml + uv.lock | 2024+ | 10-100x faster installs, lockfile, deterministic builds |
| to_tsquery (strict syntax) | websearch_to_tsquery (natural syntax) | PostgreSQL 11+ | Users can type "machine learning" not "machine & learning" |
| TF-IDF in application code (arxiv-sanity-lite) | PostgreSQL ts_rank_cd with weighted tsvector | Always available | No external computation needed; database handles ranking |
| Offset pagination | Keyset/cursor pagination | Best practice | O(1) vs O(n) for deep pages; stable across insertions |

**Deprecated/outdated:**
- **Sickle 0.7:** Unmaintained since ~2020. Use oaipmh-scythe instead.
- **arXiv OAI-PMH old URL:** `http://export.arxiv.org/oai2` replaced by `https://oaipmh.arxiv.org/oai` in March 2025.
- **SQLAlchemy 1.x patterns:** `Column()` and `Session()` patterns replaced by `mapped_column()` and async session in 2.0.

## Open Questions

1. **Announcement date derivation strategy**
   - What we know: OAI-PMH does not directly provide announcement date. RSS pubDate has it. arXiv schedule rules (Mon-Thu 14:00 ET cutoff) can approximate it.
   - What's unclear: For bulk historical harvesting, RSS is impractical (no historical archive). Should we derive from schedule rules + v1 submission date, or leave NULL for historical papers?
   - Recommendation: For incremental daily harvests, capture from RSS. For historical bulk, derive from arXiv ID + schedule rules (arXiv ID encodes year-month and sequence). Accept imprecision for historical data. Store derivation method in provenance.

2. **arXiv format vs arXivRaw for primary harvest**
   - What we know: arXivRaw has version history (critical for INGS-03). arXiv format has structured authors (keyname, forenames, suffix, affiliation). oai_dc has neither.
   - What's unclear: Should we harvest both formats per paper, or just arXivRaw and parse authors heuristically?
   - Recommendation: Use arXivRaw as primary (version history is essential). Store raw author string. Defer structured author parsing to Phase 4 OpenAlex enrichment, which provides disambiguated authors.

3. **Lexical similarity algorithm for find_related_papers**
   - What we know: PostgreSQL ts_rank_cd can rank by query similarity. TF-IDF is what arxiv-sanity-lite used. PostgreSQL has no built-in document-to-document similarity beyond tsvector operations.
   - What's unclear: Whether ts_rank_cd on a seed paper's abstract terms provides good enough "related papers" ranking.
   - Recommendation: Start with extracting key terms from seed paper's title + abstract, forming a tsquery, and ranking corpus by ts_rank_cd. This is simple, fast, and uses existing infrastructure. If quality is insufficient, consider a complementary approach in a later phase. This is in Claude's discretion area.

4. **Category-based OAI-PMH harvesting granularity**
   - What we know: OAI-PMH supports sets like `cs` (all CS) or `cs:cs:AI` (specific). Harvesting by broad set (e.g., `cs`) gets cross-listings automatically but includes categories outside the configured subset.
   - What's unclear: Whether to harvest by individual category (more targeted, more requests) or by archive (fewer requests, more data to filter).
   - Recommendation: Harvest by archive-level set (e.g., `cs`, `stat`), then filter to configured categories at ingestion time. Simpler, fewer requests, and cross-listings are naturally captured.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | none -- see Wave 0 |
| Quick run command | `uv run pytest tests/ -x --timeout=30` |
| Full suite command | `uv run pytest tests/ -v --cov=src/arxiv_mcp` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INGS-01 | OAI-PMH bulk harvest with resumption tokens | integration | `uv run pytest tests/test_ingestion/test_oai_pmh.py -x` | Wave 0 |
| INGS-02 | arXiv API incremental queries | integration | `uv run pytest tests/test_ingestion/test_arxiv_api.py -x` | Wave 0 |
| INGS-03 | Four time semantics stored correctly | unit | `uv run pytest tests/test_models/test_paper.py::test_time_semantics -x` | Wave 0 |
| INGS-04 | Per-paper license metadata stored | unit | `uv run pytest tests/test_models/test_paper.py::test_license -x` | Wave 0 |
| INGS-05 | Incremental harvesting with datestamp checkpoints | integration | `uv run pytest tests/test_ingestion/test_oai_pmh.py::test_incremental -x` | Wave 0 |
| PAPR-01 | Canonical paper model with arXiv ID PK | unit | `uv run pytest tests/test_models/test_paper.py::test_canonical_model -x` | Wave 0 |
| PAPR-02 | Title, authors, abstract, categories, versions | unit | `uv run pytest tests/test_models/test_paper.py::test_full_metadata -x` | Wave 0 |
| PAPR-03 | External identifier columns (DOI, OpenAlex, S2) | unit | `uv run pytest tests/test_models/test_paper.py::test_external_ids -x` | Wave 0 |
| PAPR-04 | Provenance: source, fetch timestamp, enrichment | unit | `uv run pytest tests/test_models/test_paper.py::test_provenance -x` | Wave 0 |
| SRCH-01 | Fielded search (title, author, abstract, category, date) | integration | `uv run pytest tests/test_search/test_service.py::test_fielded_search -x` | Wave 0 |
| SRCH-02 | AND/OR query composition | integration | `uv run pytest tests/test_search/test_service.py::test_boolean_queries -x` | Wave 0 |
| SRCH-03 | Browse recent papers by category | integration | `uv run pytest tests/test_search/test_service.py::test_browse_recent -x` | Wave 0 |
| SRCH-04 | Time basis switching (submission/update/announcement) | integration | `uv run pytest tests/test_search/test_service.py::test_time_basis -x` | Wave 0 |
| SRCH-05 | Find related papers from seed via lexical similarity | integration | `uv run pytest tests/test_search/test_service.py::test_find_related -x` | Wave 0 |
| SRCH-06 | Cursor-based pagination | unit+integration | `uv run pytest tests/test_search/test_pagination.py -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest tests/ -x --timeout=30`
- **Per wave merge:** `uv run pytest tests/ -v --cov=src/arxiv_mcp`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `pyproject.toml` -- project initialization with uv
- [ ] `tests/conftest.py` -- shared fixtures (test database, sample paper data, mock OAI-PMH responses)
- [ ] `pytest.ini` or `pyproject.toml [tool.pytest]` -- pytest configuration
- [ ] Test database setup (separate PostgreSQL database for tests)
- [ ] Mock XML responses for OAI-PMH tests (sample arXivRaw, arXiv format records)

## Sources

### Primary (HIGH confidence)
- arXiv OAI-PMH docs (https://info.arxiv.org/help/oa/index.html) -- base URL, metadata formats, sets, datestamp semantics, update schedule
- arXivRaw XSD (https://arxiv.org/OAI/arXivRaw.xsd) -- complete field list: id, submitter, version[], categories, title, authors, comments, proxy, report-no, acm-class, msc-class, journal-ref, doi, license, abstract
- arXiv format XSD (http://arxiv.org/OAI/arXiv.xsd) -- structured author format: keyname, forenames, suffix, affiliation
- arXiv API User's Manual (https://info.arxiv.org/help/api/user-manual.html) -- search fields, Boolean ops, date ranges, rate limits, Atom response format
- arXiv availability/schedule (https://info.arxiv.org/help/availability.html) -- Mon-Thu 14:00 ET cutoff, 20:00 ET announcements, weekend batching
- arXiv RSS specs (https://info.arxiv.org/help/rss_specifications.html) -- announce_type (new/cross/replace/replace-cross), dc:rights, pubDate
- PostgreSQL 18 FTS docs (https://www.postgresql.org/docs/current/textsearch-controls.html) -- tsvector, tsquery, setweight, ts_rank_cd, GIN indexes
- SQLAlchemy 2.0 PostgreSQL dialect (https://docs.sqlalchemy.org/en/20/dialects/postgresql.html) -- TSVECTOR type, match(), GIN index creation

### Secondary (MEDIUM confidence)
- oaipmh-scythe GitHub (https://github.com/afuetterer/oaipmh-scythe) -- v0.14.0, Python 3.10+, httpx+lxml, OAI verb support
- Keyset pagination guides (https://blog.sequinstream.com/keyset-cursors-not-offsets-for-postgres-pagination/) -- compound cursor pattern, WHERE tuple comparison
- Alembic GIN index issue (https://github.com/sqlalchemy/alembic/issues/1390) -- autogenerate churn with tsvector expression indexes

### Tertiary (LOW confidence)
- arXiv total paper count estimate (~2.5M as of early 2026) -- extrapolated from 2023 report (2.4M) + ~210K/year growth rate
- Announcement date derivation from arXiv ID -- common practice but not officially documented

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries verified via official docs, versions confirmed on target machine
- Architecture: HIGH -- PostgreSQL FTS patterns well-documented; SQLAlchemy 2.0 + asyncpg widely used
- Pitfalls: HIGH -- arXiv OAI-PMH gotchas confirmed via official documentation
- arXiv time semantics: HIGH -- four distinct temporal concepts confirmed across multiple official sources
- Lexical similarity approach: MEDIUM -- ts_rank_cd approach is sound but quality for "related papers" is untested
- Announcement date derivation: MEDIUM -- no single official source for historical announcement dates

**Research date:** 2026-03-08
**Valid until:** 2026-04-08 (30 days -- stable domain, arXiv APIs change slowly)
