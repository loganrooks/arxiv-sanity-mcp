# Technology Stack

**Project:** arXiv Discovery MCP
**Researched:** 2026-03-08
**Overall Confidence:** HIGH

## Recommended Stack

### Language & Runtime

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| Python | 3.13+ | Primary language | The entire scholarly ecosystem lives in Python: sentence-transformers, Docling, Marker, GROBID clients, the `arxiv` library, OAI-PMH harvesters, and SQLAlchemy. The MCP Python SDK (FastMCP) is mature, widely adopted, and decorator-based. TypeScript has a slightly newer MCP SDK, but would mean reimplementing or bridging every data science dependency. This project is not IO-bound enough for TS to matter. | HIGH |

**Language decision rationale:** The question of Python vs TypeScript is answered by the dependency graph. Every external data source library (arxiv.py, oaipmh-scythe, httpx for OpenAlex/S2), every ML library (sentence-transformers, PyTorch), every document parser (Docling, Marker, GROBID client), and the ORM layer (SQLAlchemy) are Python-native. TypeScript would require maintaining FFI bridges or HTTP microservices for each. The MCP Python SDK is production-grade (v1.26.0, FastMCP powering ~70% of MCP servers). Performance differences between Python and TS MCP servers are irrelevant at this project's scale -- database queries and API calls dominate latency, not runtime overhead.

**Note on Python vs TS MCP performance:** Benchmarks show Python MCP servers achieve ~18% of Go/Java throughput and higher latency variability. This does not matter here. The dominant latencies are: PostgreSQL queries (1-50ms), external API calls (100-500ms), and embedding inference (50-200ms per batch). Python's ~2ms overhead per MCP call is noise. If raw MCP throughput ever matters, the architecture supports extracting hot paths to Go/Rust services behind the same Python MCP surface.

### MCP Framework

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| `mcp` (official Python SDK) | >=1.26,<2 | MCP server framework | Official SDK with FastMCP included (`from mcp.server.fastmcp import FastMCP`). Decorator-based API for tools, resources, prompts. Auto-generates JSON schemas from type hints and Pydantic models. Supports stdio and Streamable HTTP transports. Spec-current as of 2025-11-25. | HIGH |

**Note on FastMCP standalone vs official SDK:** FastMCP 1.0 was incorporated into the official `mcp` package in 2024. The standalone `fastmcp` package (now at 3.1.0) adds features like OpenTelemetry, multi-auth, SearchTools (BM25 over tool names), and UI generation. Start with the official `mcp` package's built-in FastMCP. If advanced features are needed later (multi-auth, OpenTelemetry), evaluate upgrading to standalone `fastmcp`. Do NOT depend on both simultaneously -- they share the same core classes and will conflict.

**MCP SDK v2 status:** The Python SDK v2 is in pre-alpha on the main branch as of March 2026. The plan was for v2 to ship in Q1 2026 with significant transport layer changes. Stay on v1.x until v2 reaches stable release. v1.x will receive bug fixes for at least 6 months after v2 ships.

### Database & Storage

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| PostgreSQL | 16.11 (installed) | Primary data store | Already running on this machine. Handles relational data (papers, collections, triage states, profiles), full-text search (tsvector + GIN), and vector similarity (pgvector). One database for everything avoids operational complexity of separate search engines. PG 16 supports all needed features. | HIGH |
| pgvector | >=0.8.0 | Vector similarity search | PostgreSQL extension for HNSW/IVFFlat vector indexes. Needed only for Phase 6 (selective semantic search). Install via `apt install postgresql-16-pgvector` from the PostgreSQL APT repository. At the project's scale (selective embedding of ~50K-200K papers), pgvector with HNSW handles this comfortably. v0.8.0 adds iterative index scans for filtered queries. | HIGH |
| Redis | 7.0.15 (installed) | Caching, rate limiting, job queues | Already running. Use for: API response caching (OpenAlex, S2), rate-limit tracking for arXiv/OpenAlex APIs, lightweight job scheduling for enrichment workers, and delta checkpoint markers. Do NOT use as primary data store. | HIGH |

**Why one database:** PostgreSQL handles relational data, full-text search (tsvector+GIN), and vector similarity (pgvector) in a single system. This eliminates synchronization problems between separate stores. At the project's scale (<5M papers, <200K embeddings), PostgreSQL handles all three workloads without performance concerns. The only reason to split would be if vector search latency at >1M embeddings becomes a bottleneck -- pgvector v0.8.0 with HNSW delivers 40.5 QPS at 0.998 recall, which is more than sufficient for this workload.

### Full-Text Search Strategy

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| PostgreSQL FTS (tsvector + GIN) | Built-in (PG 16) | Lexical search over metadata/abstracts | Pre-computed tsvector columns with GIN indexes achieve sub-second queries on millions of rows. A 50x improvement is achievable over naive FTS by: (1) storing pre-computed tsvector columns instead of calling `to_tsvector()` at query time, (2) creating GIN indexes on those columns, and (3) tuning `maintenance_work_mem`. Supports fielded search (title, abstract, authors, categories), `ts_rank` scoring, phrase matching, and weighted field queries. | HIGH |
| pg_trgm | 1.6 (installed via postgresql-contrib) | Fuzzy matching, typo tolerance | Trigram similarity for author name matching and typo-tolerant search. Already available. Complements tsvector for prefix/fuzzy queries. Use GIN index on trigrams for fast `%` and `similarity()` queries. | HIGH |
| btree_gin | Built-in (contrib) | Multi-column GIN indexes | Allows combining tsvector search with equality filters (category, date range) in a single GIN index. Reduces query planning overhead for common filtered-search patterns. | HIGH |

**Why NOT a separate search engine:**

| Alternative | Why Not | Reconsider When |
|-------------|---------|-----------------|
| Tantivy (tantivy-py 0.25.1) | Excellent Rust-based search engine with BM25 scoring, but adds an external index to keep synchronized with PostgreSQL. For <5M documents with metadata-heavy queries, PostgreSQL FTS is sufficient. Python bindings are stable but add a build dependency (maturin, Rust toolchain). | If BM25 scoring quality or faceted search (aggregations by category, date, author) become critical requirements that PostgreSQL FTS cannot serve well. |
| Meilisearch / Typesense | Designed for user-facing typo-tolerant autocomplete search. This is an MCP server, not a web UI -- the LLM handles query reformulation. Operational overhead of a separate service is not justified. | If a web UI is added and needs instant-search UX. |
| ParadeDB (pg_search) | BM25-in-PostgreSQL via embedded Tantivy. Promising (1.2M docs/sec indexing, 3x faster than ES 8.x). But adds a non-standard extension dependency that may not be in the Ubuntu apt repository. | If PostgreSQL native FTS proves inadequate for ranking quality. This is the upgrade path -- not Elasticsearch. |
| Elasticsearch / OpenSearch | Massive operational overhead for a single-node scholarly project. Requires JVM, separate cluster, index management. PostgreSQL FTS covers the need at this scale. | Never for this project's scope. |

### Embedding Models (Phase 6 -- Selective Semantic Search)

| Model | Parameters | Dims | Purpose | Why | Confidence |
|-------|-----------|------|---------|-----|------------|
| `allenai/specter2` + adapters | ~110M (SciBERT base) | 768 | Scientific paper embeddings | Purpose-built for scholarly documents. Trained on 6M citation triplets across 23 fields of study. Task-specific adapters (proximity for similarity, adhoc_query for search, classification for categorization). Best-in-class on SciRepEval benchmark for scientific document retrieval. Fits comfortably on GTX 1080 Ti (11GB VRAM, model uses <500MB). Static paper embeddings also available free via Semantic Scholar API as a bootstrap option. | HIGH |
| `nomic-ai/nomic-embed-text-v1.5` | 137M | 768 (Matryoshka: down to 256) | General fallback / query embedding | Strong general-purpose model. Matryoshka Representation Learning allows trading accuracy for storage (768 -> 512 -> 256 dims). Useful for embedding user queries when they diverge from scholarly language. Also 100% open source with reproducible training. | MEDIUM |

**Why NOT other models:**

| Alternative | Why Not |
|-------------|---------|
| `all-MiniLM-L6-v2` (22M params, 384 dims) | Fast and tiny but underperforms on modern retrieval benchmarks. 56% Top-5 accuracy vs SPECTER2's domain-specific superiority on SciRepEval. Not worth the quality tradeoff when SPECTER2 fits on the same GPU. |
| Snowflake Arctic Embed M 2.0 (305M params) | Strong general-purpose model but not trained on scientific citation signals. SPECTER2 is domain-specific and better for scholarly paper retrieval. |
| Nomic Embed v2 MoE | Newer MoE architecture, but the MoE overhead may not be worth it for a domain where SPECTER2 already excels. Monitor for scientific retrieval benchmarks. |
| Large LLM-based embedders (NV-Embed/Mistral-7B, GTE-Qwen2-7B) | Too large for GTX 1080 Ti (11GB VRAM). NV-Embed requires ~14GB. Not viable without upgrading hardware. |

**Embedding strategy:** Embed selectively, not the full corpus. Priority cohorts:
1. **User-touched papers** -- papers added to collections, triaged, or used as seeds
2. **Recent window** -- papers from the last 30-90 days in subscribed categories
3. **Seed neighborhoods** -- papers cited-by or citing seed papers
4. **High-interest cohorts** -- papers matching active saved queries

This keeps the vector index manageable (~50K-200K vectors, ~150MB-600MB in pgvector) and GPU usage intermittent (batch embedding, not real-time).

### ORM & Data Access

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| SQLAlchemy | >=2.0,<3 | ORM and query builder | Industry standard for Python database access. Supports async via `create_async_engine` + `AsyncSession`. Rich type system, relationship mapping, and composable query building. Works with asyncpg driver. Migration support via Alembic. | HIGH |
| asyncpg | >=0.30,<1 | Async PostgreSQL driver | 5x faster than psycopg3 for simple queries due to C implementation and PostgreSQL binary protocol. Best choice for the read-heavy workload of search queries and metadata lookups. Used as SQLAlchemy's async backend via `postgresql+asyncpg://` URL scheme. | HIGH |
| Alembic | >=1.18,<2 | Database migrations | Standard companion to SQLAlchemy. Supports async engines via `op.run_async()`. Critical for schema evolution across phases (time semantics, enrichment fields, vector columns). v1.18.4 is current. | HIGH |
| Pydantic | >=2.12,<3 | Data validation & serialization | FastMCP auto-generates MCP tool schemas from Pydantic models. Also used for API response validation, configuration management, and domain object serialization. Rust-backed core (pydantic-core) for performance. v2.12.5 stable, v2.13 in beta with further perf improvements. | HIGH |

**Why asyncpg over psycopg3:** asyncpg is faster for simple read-heavy queries (the dominant workload -- paper lookups, search result assembly, collection listings). psycopg3 offers richer features (Row Factories for Pydantic mapping, sync+async unified API, COPY support) but the performance edge of asyncpg matters more for a search server. psycopg3's Row Factory advantage is partially addressed by SQLAlchemy's ORM layer doing the object mapping anyway. If advanced PostgreSQL features are needed later (e.g., LISTEN/NOTIFY for real-time watch notifications), psycopg3 is the fallback.

### HTTP Client & API Integration

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| httpx | >=0.28,<1 | Async HTTP client | Unified sync/async API. HTTP/2 support. Used for: arXiv API queries, OpenAlex API calls, Semantic Scholar API calls, arXiv HTML/source content fetching. Connection pooling via `AsyncClient` with configurable timeouts and retries. | HIGH |
| arxiv (arxiv.py) | >=2.4,<3 | arXiv search API wrapper | Well-maintained (47K weekly downloads, v2.4.1 released March 2026). Handles Atom feed parsing, pagination, and rate limiting. Result objects with `download_pdf()` and `download_source()` helpers. Not used for bulk harvesting (use OAI-PMH for that). | HIGH |
| oaipmh-scythe | >=1.0,<2 | OAI-PMH bulk harvesting | Modern fork of Sickle. Uses httpx + lxml internally. Python 3.10+ required. Supports all six OAI verbs. Handles resumption tokens for large harvests. Use for initial bulk metadata ingestion and daily incremental updates. | HIGH |
| feedparser | >=6.0,<7 | RSS/Atom feed parsing | For arXiv RSS feeds (daily announcement parsing). Lightweight, battle-tested. RSS feeds provide `announce_type` (new/cross/replace) and `dc:rights` (license URI) which are valuable for delta computation and rights tracking. | MEDIUM |

### Content Parsing (Phase 5)

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| Docling | >=2.70,<3 | PDF/DOCX to structured output | IBM Research project (v2.76.0 current). Best structured output quality: tables, formulas, reading order, code blocks. MIT license. Fully local execution. Multiple export formats (Markdown, JSON, HTML, DocTags). Python 3.10+ required. Primary PDF parser for quality. | HIGH |
| Marker | >=1.10,<2 | PDF to markdown (GPU-accelerated) | v1.10.2 current. Fast GPU-accelerated conversion (~25 pages/sec on H100; proportionally slower on 1080 Ti but still fast). Good equation and table handling. Use as secondary parser for batch processing where throughput matters over structure granularity. Optional `--use_llm` flag for highest accuracy. | MEDIUM |
| grobid-client-python | >=0.1,<1 | GROBID TEI/XML extraction | v0.1.2 (Nov 2025). Client for GROBID Docker service. Excellent scholarly PDF extraction to structured TEI/XML with bibliographic parsing, reference extraction, and author disambiguation. Requires running GROBID Docker container (not yet installed; PaddleOCR already on port 8765). | MEDIUM |
| lxml | >=5.0,<6 | XML parsing | Fast C-backed XML/HTML parser. Used by oaipmh-scythe internally. Also needed for: parsing arXiv API Atom responses, processing OAI-PMH XML records, parsing GROBID TEI/XML output, and extracting arXiv HTML content. | HIGH |

**Content parser strategy:** Multiple backends behind one `ContentNormalizer` interface (aligns with project design docs). Preferred acquisition order:
1. **Abstract** -- always available, no rights issues, free
2. **arXiv HTML** -- best structured option when available (growing coverage but not universal)
3. **arXiv source-derived text** -- often stronger than PDF when LaTeX source is clean
4. **OpenAlex GROBID XML** -- structured fallback via `content_url` when available
5. **PDF parsing via Docling/Marker** -- most universal, least reliable, most expensive

All behind a common interface with provenance tracking per ADR-0003.

### ML & Computation

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| sentence-transformers | >=4.0,<5 | Embedding generation | High-level API for loading and running embedding models (SPECTER2, nomic-embed). Handles batching, GPU acceleration, normalization. Integrates with PyTorch. Over 15,000 pre-trained models on Hugging Face. | HIGH |
| PyTorch | >=2.5,<3 | ML runtime | Required by sentence-transformers. CUDA 12.4 compatible (driver 550.163.01 installed on this machine). Install with CUDA 12.4 wheels for GPU acceleration. | HIGH |
| scikit-learn | >=1.6,<2 | TF-IDF, classical ML | For TF-IDF feature computation (arxiv-sanity-lite's approach), SVM-based recommendation experiments, cosine similarity computation, and evaluation metrics. Lightweight, CPU-only, no GPU needed. | HIGH |
| numpy | >=2.0,<3 | Numerical computation | Required by scikit-learn, sentence-transformers, and general numerical work. | HIGH |

### Development & Operations

| Technology | Version | Purpose | Why | Confidence |
|------------|---------|---------|-----|------------|
| uv | latest | Package management & virtual environments | 10-100x faster than pip. Lockfile support (`uv.lock`). Better dependency resolution. Replaces pip + venv + pip-tools. Handles Python version management too. | HIGH |
| pytest | >=8.0 | Testing | Standard Python testing framework. Rich plugin ecosystem. | HIGH |
| pytest-asyncio | >=0.25 | Async test support | Required for testing async MCP handlers, database operations, and HTTP client calls. | HIGH |
| ruff | latest | Linting & formatting | Fast Rust-based linter/formatter. Replaces flake8 + black + isort in a single tool. ~100x faster than the tools it replaces. | HIGH |
| mypy | latest | Type checking | Static type checking. Important for a project with many Pydantic models, typed interfaces, and async code. Catches type errors before runtime. | MEDIUM |

### Recommended Project Structure

```
arxiv-sanity-mcp/
  src/
    arxiv_mcp/
      __init__.py
      server.py              # MCP server entry point (FastMCP instance)
      config.py              # Pydantic Settings for configuration
      #
      # --- Domain Models (Pydantic) ---
      models/
        __init__.py
        paper.py             # Paper, ExternalIds, TimeSemantics
        content.py           # ContentVariant, ContentSource, License
        workflow.py          # Collection, TriageEntry, SavedQuery, Watch
        profile.py           # InterestProfile, SeedSet, FollowedAuthor
        result.py            # ResultSet, RankingExplanation
        provenance.py        # ProvenanceRecord, AcquisitionMetadata
      #
      # --- Database Layer ---
      db/
        __init__.py
        engine.py            # SQLAlchemy async engine + session factory
        orm.py               # ORM table models (mapped from Pydantic)
        queries/             # Typed query functions (no raw SQL in services)
          papers.py
          workflow.py
          search.py
          content.py
        redis.py             # Redis client, cache helpers, rate-limit tracking
      #
      # --- Ingestion ---
      ingestion/
        __init__.py
        oai_pmh.py           # OAI-PMH harvester with checkpointing
        arxiv_api.py         # arXiv search API client (arxiv.py wrapper)
        rss.py               # RSS feed parser for announcements
        enrichment/          # External enrichment adapters
          openalex.py        # OpenAlex works/authors/topics
          semantic_scholar.py # S2 recommendations/embeddings (optional)
          crossref.py        # DOI/citation enrichment (optional)
        scheduler.py         # Background job scheduling via Redis
      #
      # --- Retrieval & Ranking ---
      retrieval/
        __init__.py
        pipeline.py          # Multi-stage retrieval pipeline executor
        types.py             # CandidateSet, ScoredPaper, PipelineContext
        adapters/            # Pluggable retrieval backends
          lexical.py         # PostgreSQL FTS (tsvector + GIN)
          semantic.py        # pgvector HNSW (Phase 6)
          graph.py           # OpenAlex related_works (Phase 3)
          metadata.py        # Fielded SQL queries
        rankers/             # Pluggable ranking strategies
          recency.py
          relevance.py
          profile_match.py
          diversity.py
        explanation.py       # Explanation assembly from ranking signals
      #
      # --- Content Normalization ---
      content/
        __init__.py
        normalizer.py        # Common ContentNormalizer interface
        backends/
          arxiv_html.py      # arXiv HTML fetcher
          arxiv_source.py    # arXiv source extraction
          docling_backend.py # Docling PDF parser
          marker_backend.py  # Marker PDF parser
          grobid_backend.py  # GROBID TEI/XML extraction
        provenance.py        # Content provenance tracking
      #
      # --- MCP Surface (thin layer) ---
      tools/
        __init__.py
        discovery.py         # search_papers, browse_recent, find_related
        workflow.py          # create_collection, mark_triage, save_query
        content.py           # get_content_variant
        explain.py           # explain_result, inspect_profile
      resources/
        __init__.py
        paper.py             # paper://{id}, paper://{id}/abstract
        collection.py        # collection://{id}
        result_set.py        # resultset://{id}
      prompts/
        __init__.py
        daily_digest.py
        literature_map.py
        triage_shortlist.py
  #
  tests/
    conftest.py              # Shared fixtures (test DB, mock APIs)
    test_ingestion/
    test_retrieval/
    test_workflow/
    test_tools/
  #
  alembic/                   # Database migrations
    versions/
    env.py
    alembic.ini
  #
  pyproject.toml
  uv.lock
```

**Structure rationale:**
- **models/** -- Pydantic domain models shared across all layers. Schema source of truth.
- **db/** -- All database access centralized. Services never write raw SQL. ORM models map from Pydantic models.
- **ingestion/** -- Separate operational concern: runs on schedules, has different failure modes, manages external API rate limits. Decoupled from request-time code.
- **retrieval/** -- Heart of exploration-first architecture (ADR-0001). Pipeline is composable; adapters implement common interface; rankers are pluggable.
- **content/** -- Isolated because content normalization is expensive, rights-sensitive, and involves multiple backends. Runs lazily per ADR-0002.
- **tools/resources/prompts/** -- Thin MCP protocol translation. Validates input, calls services, formats output. No business logic.

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Language | Python 3.13 | TypeScript | Every dependency (ML, parsers, OAI-PMH, arxiv.py) is Python-native. TS would require bridges or microservices for each. |
| MCP SDK | `mcp` (official, with built-in FastMCP) | Standalone `fastmcp` 3.x | Start with official SDK. Upgrade to standalone only if OpenTelemetry/multi-auth needed. Avoid depending on both. |
| Search | PostgreSQL FTS (tsvector + GIN) | Tantivy / tantivy-py | Extra index to sync with PG. PG FTS sufficient for <5M documents. Tantivy adds Rust build dependency. |
| Search | PostgreSQL FTS | Meilisearch / Typesense | Designed for web UI autocomplete, not MCP server queries. Extra service to operate. |
| Search | PostgreSQL FTS | ParadeDB pg_search | BM25-in-PG via embedded Tantivy. Promising but non-standard extension. Upgrade path if PG FTS proves insufficient. |
| Vector DB | pgvector (in PostgreSQL) | Qdrant / Weaviate / Milvus | Separate service to operate and synchronize. pgvector keeps everything in one database. Scale is modest (<200K vectors). |
| Vector DB | pgvector | ChromaDB | In-process but limited query capabilities and no SQL integration. pgvector is more mature. |
| ORM | SQLAlchemy 2.0 | Raw asyncpg queries | SQLAlchemy provides migration support (Alembic), relationship mapping, type safety, and composable queries. Worth the abstraction for a schema this complex. |
| PG Driver | asyncpg | psycopg3 | asyncpg is 5x faster for read-heavy workloads. psycopg3 has richer features but performance matters more here. |
| Embedding | SPECTER2 | all-MiniLM-L6-v2 | MiniLM underperforms on modern retrieval benchmarks (56% Top-5). SPECTER2 is domain-specific for scientific papers. |
| Embedding | SPECTER2 | Large LLM embedders (NV-Embed, GTE-Qwen) | Too large for GTX 1080 Ti (11GB VRAM). 7B+ backbone models require 14GB+. |
| PDF Parser | Docling (primary) + Marker (secondary) | Marker only | Docling produces better structured output (section hierarchy, reading order). Marker is faster but less structured. Both behind common interface. |
| Package Mgmt | uv | pip + venv / conda | uv is 10-100x faster, has lockfile support, better dependency resolution, and handles Python versioning. |

## Installation

```bash
# Create project environment with uv
cd ~/workspace/projects/arxiv-sanity-mcp
uv init --python 3.13

# Core dependencies
uv add "mcp>=1.26,<2" "pydantic>=2.12,<3" "sqlalchemy[asyncio]>=2.0,<3" \
       "asyncpg>=0.30,<1" "alembic>=1.18,<2" "httpx>=0.28,<1" "lxml>=5.0,<6"

# arXiv / OAI-PMH / feeds
uv add "arxiv>=2.4,<3" "oaipmh-scythe>=1.0,<2" "feedparser>=6.0,<7"

# Classical ML (needed from Phase 1 for TF-IDF)
uv add "scikit-learn>=1.6,<2" "numpy>=2.0,<3"

# ML/embedding (Phase 6 -- install when needed)
uv add --optional semantic "sentence-transformers>=4.0,<5" "torch>=2.5,<3"

# Content parsing (Phase 5 -- install when needed)
uv add --optional content "docling>=2.70,<3" "marker-pdf>=1.10,<2" \
       "grobid-client-python>=0.1,<1"

# Dev dependencies
uv add --dev pytest pytest-asyncio ruff mypy

# System: install pgvector extension (Phase 6, requires sudo)
# sudo apt install postgresql-16-pgvector
# Then in PostgreSQL: CREATE EXTENSION vector;

# PostgreSQL extensions (Phase 1, available via postgresql-contrib):
# CREATE EXTENSION IF NOT EXISTS pg_trgm;
# CREATE EXTENSION IF NOT EXISTS btree_gin;
# CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## Version Pinning Strategy

Pin major versions, allow minor/patch updates. Use optional dependency groups to defer heavy installs.

```toml
[project]
name = "arxiv-discovery-mcp"
requires-python = ">=3.13"
dependencies = [
    "mcp>=1.26,<2",
    "pydantic>=2.12,<3",
    "sqlalchemy[asyncio]>=2.0,<3",
    "asyncpg>=0.30,<1",
    "alembic>=1.18,<2",
    "httpx>=0.28,<1",
    "lxml>=5.0,<6",
    "arxiv>=2.4,<3",
    "oaipmh-scythe>=1.0,<2",
    "feedparser>=6.0,<7",
    "scikit-learn>=1.6,<2",
    "numpy>=2.0,<3",
]

[project.optional-dependencies]
semantic = [
    "sentence-transformers>=4.0,<5",
    "torch>=2.5,<3",
]
content = [
    "docling>=2.70,<3",
    "marker-pdf>=1.10,<2",
    "grobid-client-python>=0.1,<1",
]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.25",
    "ruff",
    "mypy",
]
```

## Infrastructure Requirements

| Requirement | Status | Action Needed | Phase |
|-------------|--------|---------------|-------|
| PostgreSQL 16.11 | Installed, running | Create `arxiv_discovery` database | Phase 1 |
| postgresql-contrib | Installed | `CREATE EXTENSION pg_trgm; CREATE EXTENSION btree_gin;` | Phase 1 |
| Redis 7.0.15 | Installed, running | No action needed | Phase 1 |
| Python 3.13 | Installed (system) | Create uv venv for project | Phase 1 |
| pgvector 0.8.0 | NOT installed | `sudo apt install postgresql-16-pgvector` then `CREATE EXTENSION vector;` | Phase 6 |
| GTX 1080 Ti | Available (652MB/11264MB used) | No action. ~10.5GB free for embedding models. | Phase 6 |
| CUDA 12.4 | Driver 550.163.01 installed | PyTorch CUDA 12.4 wheels available | Phase 6 |
| GROBID Docker | NOT installed | `docker pull lfoppiano/grobid:0.8.1` (Phase 5). PaddleOCR already on port 8765. | Phase 5 |

## Technology-Phase Mapping

Which stack components are needed in which phase:

| Phase | Components Needed | Optional Deps |
|-------|-------------------|---------------|
| 1: Metadata substrate | mcp, pydantic, sqlalchemy, asyncpg, alembic, httpx, lxml, oaipmh-scythe, arxiv.py, feedparser | -- |
| 2: Workflow state | (same as Phase 1, no new deps) | -- |
| 3: Enrichment adapters | httpx (already included) | -- |
| 4: MCP v1 | (same as Phase 1, no new deps) | -- |
| 5: Content normalization | docling, marker-pdf, grobid-client-python | `[content]` group |
| 6: Semantic search | sentence-transformers, torch, pgvector | `[semantic]` group |

This staging means Phase 1-4 have a small, fast-to-install dependency set. Heavy ML and content parsing deps are deferred until actually needed.

## Sources

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) -- Official SDK, v1.26.0, FastMCP included. v2 pre-alpha in development.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) -- v1.27.1, for comparison only.
- [FastMCP standalone](https://github.com/jlowin/fastmcp) -- v3.1.0. Advanced features (multi-auth, OTel, SearchTools).
- [MCP SDK comparison](https://www.stainless.com/mcp/mcp-sdk-comparison-python-vs-typescript-vs-go-implementations) -- Python vs TS vs Go performance.
- [MCP Python vs TS benchmark](https://www.tmdevlab.com/mcp-server-performance-benchmark.html) -- Python 18% of Go throughput; irrelevant at this scale.
- [pgvector](https://github.com/pgvector/pgvector) -- v0.8.0. HNSW/IVFFlat. 5.7x query improvement over v0.7.4.
- [pgvector 2026 guide](https://www.instaclustr.com/education/vector-database/pgvector-key-features-tutorial-and-pros-and-cons-2026-guide/) -- Scaling considerations.
- [PostgreSQL FTS docs](https://www.postgresql.org/docs/16/textsearch.html) -- Built-in full-text search reference.
- [PostgreSQL FTS optimization](https://blog.vectorchord.ai/postgresql-full-text-search-fast-when-done-right-debunking-the-slow-myth) -- 50x improvement with proper tsvector/GIN setup.
- [PostgreSQL FTS vs dedicated engines](https://nomadz.pl/en/blog/postgres-full-text-search-or-meilisearch-vs-typesense) -- When PG FTS is sufficient.
- [PostgreSQL GIN index guide](https://pganalyze.com/blog/gin-index) -- GIN index internals and optimization.
- [SPECTER2](https://huggingface.co/allenai/specter2) -- Scientific document embeddings. 110M params, 768 dims.
- [SPECTER2 blog](https://allenai.org/blog/specter2-adapting-scientific-document-embeddings-to-multiple-fields-and-task-formats-c95676c06567) -- Training details, SciRepEval benchmark.
- [Nomic Embed v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5) -- 137M params, Matryoshka dims.
- [Nomic Embed v2 MoE](https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe) -- Newer MoE architecture.
- [Best open-source embedding models 2026](https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models) -- Model comparison guide.
- [Tantivy Python](https://github.com/quickwit-oss/tantivy-py) -- v0.25.1. Considered but deferred.
- [ParadeDB pg_search](https://www.paradedb.com/blog/introducing-search) -- BM25-in-PostgreSQL via Tantivy. Upgrade path.
- [arxiv.py](https://github.com/lukasschwab/arxiv.py) -- v2.4.1 (March 2026). arXiv API wrapper.
- [oaipmh-scythe](https://github.com/afuetterer/oaipmh-scythe) -- v1.0.0. Modern OAI-PMH client (httpx + lxml).
- [Docling](https://github.com/docling-project/docling) -- v2.76.0. Structured PDF parsing. MIT license.
- [Marker](https://github.com/datalab-to/marker) -- v1.10.2. GPU-accelerated PDF to markdown.
- [GROBID client](https://github.com/kermitt2/grobid-client-python) -- v0.1.2. Scholarly PDF extraction.
- [SQLAlchemy async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) -- Async patterns and best practices.
- [asyncpg](https://github.com/MagicStack/asyncpg) -- Fast async PostgreSQL driver. C implementation.
- [asyncpg vs psycopg3](https://fernandoarteaga.dev/blog/psycopg-vs-asyncpg/) -- Performance comparison.
- [Pydantic v2](https://docs.pydantic.dev/latest/) -- v2.12.5 stable. Rust-backed core.
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) -- v1.18.4. Async migration support.
