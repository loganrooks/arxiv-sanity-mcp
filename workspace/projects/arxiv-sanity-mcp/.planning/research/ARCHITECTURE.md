# Architecture Research

**Domain:** MCP-native scholarly discovery system (arXiv-centered)
**Researched:** 2026-03-08
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌───────────────────────────────────────────────────────────────────┐
│                         MCP Layer                                 │
│  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌──────────────┐     │
│  │  Tools   │  │ Resources │  │ Prompts  │  │  Completion  │     │
│  └────┬─────┘  └─────┬─────┘  └────┬─────┘  └──────┬───────┘     │
│       └───────────────┴─────────────┴───────────────┘             │
├───────────────────────────┬───────────────────────────────────────┤
│                     Service Layer                                 │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │ Discovery  │  │  Workflow  │  │  Content   │  │ Enrichment │  │
│  │  Service   │  │  Service   │  │  Service   │  │  Service   │  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  │
├────────┴────────────────┴──────────────┴────────────────┴─────────┤
│                     Retrieval Pipeline                             │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌──────────────┐   │
│  │ Candidate  │  │ Constraint│  │ Reranking │  │ Explanation  │   │
│  │ Generation │→ │ Filtering │→ │           │→ │  Assembly    │   │
│  └───────────┘  └───────────┘  └───────────┘  └──────────────┘   │
├───────────────────────────────────────────────────────────────────┤
│                     Retrieval Adapters                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Lexical  │  │ Semantic │  │  Graph   │  │ Metadata/Field  │  │
│  │ (PG FTS) │  │(pgvector)│  │(OpenAlex)│  │    (PG SQL)     │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘  │
├───────────────────────────────────────────────────────────────────┤
│                     Ingestion Layer                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────────┐  │
│  │  OAI-PMH    │  │ arXiv API   │  │  Enrichment Schedulers   │  │
│  │  Harvester  │  │  Client     │  │  (OpenAlex, S2, etc.)    │  │
│  └──────┬──────┘  └──────┬──────┘  └────────────┬─────────────┘  │
├─────────┴────────────────┴──────────────────────┴─────────────────┤
│                     Canonical Store                                │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                     PostgreSQL                               │  │
│  │  papers | content_variants | workflow_state | provenance     │  │
│  │  tsvectors | pgvector (optional) | rankings | enrichments   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                       Redis                                  │  │
│  │  rate_limits | job_queues | caches | delta_checkpoints       │  │
│  └─────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| MCP Layer | Protocol translation: maps MCP tools/resources/prompts to service calls | `@modelcontextprotocol/sdk` with Zod schema validation; thin wrappers that delegate to services |
| Discovery Service | Orchestrates search, browse, find-related, and delta queries | Composes retrieval pipeline stages; returns ResultSet objects |
| Workflow Service | Manages collections, triage states, saved queries, watches, interest profiles | CRUD + business rules over PostgreSQL workflow tables |
| Content Service | Acquires, converts, and caches content variants (abstract, HTML, source, PDF-derived) | Dispatches to content backends (arXiv HTML fetch, source extraction, Marker, Docling, GROBID); records provenance |
| Enrichment Service | Lazy enrichment scheduling and execution against external APIs | OpenAlex, Semantic Scholar, Crossref adapters; rate-limited; results cached in PG |
| Retrieval Pipeline | Multi-stage candidate generation -> filtering -> reranking -> explanation assembly | Pluggable stages; each stage has a typed interface; pipeline is configurable per query |
| Retrieval Adapters | Individual retrieval backends behind a common interface | Lexical (PG tsvector + GIN), Semantic (pgvector HNSW), Graph (OpenAlex related_works), Metadata (SQL field queries) |
| Ingestion Layer | Pulls metadata from arXiv OAI-PMH and API; schedules enrichment | OAI-PMH harvester with resumption tokens; arXiv search API client; enrichment job queue on Redis |
| Canonical Store | Single source of truth for papers, content, workflow state, provenance | PostgreSQL as primary store; Redis for queues, caches, and rate-limit tracking |

## Recommended Project Structure

```
src/
├── mcp/                    # MCP protocol layer (thin)
│   ├── server.ts           # MCP server setup, transport config
│   ├── tools/              # Tool handler registrations
│   │   ├── discovery.ts    # search_papers, browse_recent, find_related, get_delta
│   │   ├── workflow.ts     # create_collection, mark_triage, save_query
│   │   ├── content.ts      # get_content_variant, convert_to_markdown
│   │   └── explain.ts      # explain_result, inspect_profile
│   ├── resources/          # Resource handler registrations
│   │   ├── paper.ts        # paper://{id}, paper://{id}/abstract
│   │   ├── collection.ts   # collection://{id}
│   │   └── resultset.ts    # resultset://{id}
│   └── prompts/            # Prompt registrations
│       ├── daily-digest.ts
│       ├── literature-map.ts
│       └── triage.ts
├── services/               # Business logic (MCP-independent)
│   ├── discovery.ts        # Search, browse, find-related orchestration
│   ├── workflow.ts         # Collection, triage, saved query management
│   ├── content.ts          # Content acquisition and normalization
│   ├── enrichment.ts       # External API enrichment scheduling
│   ├── ranking.ts          # Ranking and explanation assembly
│   └── ingestion.ts        # Metadata ingestion orchestration
├── retrieval/              # Retrieval pipeline and adapters
│   ├── pipeline.ts         # Multi-stage pipeline executor
│   ├── types.ts            # CandidateSet, RankedResult, Explanation types
│   ├── adapters/           # Pluggable retrieval backends
│   │   ├── lexical.ts      # PostgreSQL FTS adapter
│   │   ├── semantic.ts     # pgvector adapter (optional)
│   │   ├── graph.ts        # OpenAlex related_works adapter
│   │   └── metadata.ts     # Fielded SQL query adapter
│   ├── rankers/            # Pluggable ranking strategies
│   │   ├── recency.ts
│   │   ├── relevance.ts
│   │   ├── profile-match.ts
│   │   └── diversity.ts
│   └── explain.ts          # Explanation assembly from ranked signals
├── ingestion/              # Data acquisition
│   ├── oai-pmh.ts          # OAI-PMH harvester with resumption tokens
│   ├── arxiv-api.ts        # arXiv search API client
│   ├── enrichment/         # External enrichment adapters
│   │   ├── openalex.ts     # OpenAlex works/authors/topics
│   │   ├── semantic-scholar.ts  # S2 recommendations/embeddings
│   │   └── crossref.ts     # DOI/citation enrichment
│   └── scheduler.ts        # Job scheduling for incremental harvests
├── content/                # Content normalization
│   ├── variants.ts         # Content variant model and acquisition order
│   ├── backends/           # Content conversion backends
│   │   ├── arxiv-html.ts   # arXiv HTML fetcher
│   │   ├── source.ts       # arXiv source extraction
│   │   ├── marker.ts       # Marker PDF-to-markdown
│   │   ├── docling.ts      # Docling structured extraction
│   │   └── grobid.ts       # GROBID TEI/XML extraction
│   └── provenance.ts       # Content provenance tracking
├── models/                 # Domain object types and schemas
│   ├── paper.ts            # Paper, ExternalId, TimeSemantics
│   ├── content-variant.ts  # ContentVariant, ContentSource, License
│   ├── workflow.ts         # Collection, TriageEntry, SavedQuery, Watch
│   ├── interest-profile.ts # InterestProfile, SeedSet, FollowedAuthor
│   ├── result-set.ts       # ResultSet, RankingExplanation
│   └── provenance.ts       # ProvenanceRecord, AcquisitionMetadata
├── db/                     # Database layer
│   ├── client.ts           # PostgreSQL connection pool
│   ├── migrations/         # Schema migrations (numbered)
│   ├── queries/            # Typed query functions
│   │   ├── papers.ts
│   │   ├── content.ts
│   │   ├── workflow.ts
│   │   └── search.ts
│   └── redis.ts            # Redis client and queue helpers
├── config/                 # Configuration
│   ├── index.ts            # Zod-validated config from environment
│   ├── compute-profile.ts  # Bronze/Silver/Gold feature flags
│   └── rights-policy.ts    # Local vs hosted rights policy
└── shared/                 # Cross-cutting utilities
    ├── types.ts            # Shared type definitions
    ├── errors.ts           # Error hierarchy
    ├── rate-limiter.ts     # External API rate limiting
    └── logger.ts           # Structured logging
```

### Structure Rationale

- **mcp/:** Thin protocol translation layer. Tool/resource/prompt handlers validate input (Zod) and delegate to services. No business logic lives here. This means the entire discovery engine is testable and usable without MCP.
- **services/:** Business logic orchestration. Each service composes lower-level components (retrieval pipeline, database queries, content backends) to fulfill use cases. Services are the primary unit of testability.
- **retrieval/:** The heart of the exploration-first architecture (ADR-0001). The pipeline is a composable chain of stages. Adapters implement a common interface so lexical, semantic, graph, and metadata retrieval can be mixed, compared, and swapped without touching service code.
- **ingestion/:** Separated because ingestion is a distinct operational concern (runs on schedules, has different failure modes, manages external API rate limits). The harvester and enrichment adapters run independently of request-time code.
- **content/:** Isolated because content normalization is expensive, rights-sensitive, and involves multiple backends. Content acquisition has its own provenance model (ADR-0003) and runs lazily (ADR-0002).
- **models/:** Domain objects shared across all layers. These correspond to the core object model from the architecture hypotheses: Paper, ContentVariant, InterestProfile, Collection, SavedQuery, Watch, TriageEntry, ResultSet, RankingExplanation.
- **db/:** Database access is centralized, not scattered through services. Migrations enforce schema evolution. Typed query functions prevent raw SQL from leaking into business logic.

## Architectural Patterns

### Pattern 1: Retrieval Pipeline as Composable Stages

**What:** Every discovery operation runs through a configurable multi-stage pipeline: candidate generation, constraint filtering, reranking, diversification, and explanation assembly. Each stage is a typed function with a common interface.

**When to use:** Every search, browse, find-related, and recommendation operation. The pipeline is the central abstraction that makes the exploration-first architecture (ADR-0001) possible.

**Trade-offs:**
- Pro: Enables comparing retrieval strategies without rewriting services. Adding a new retrieval adapter or ranker is one new module plus pipeline configuration.
- Pro: Explanations are naturally assembled from the stages that ran, making inspectability structural.
- Con: Slightly more indirection than a monolithic search function. Worth it because the project explicitly needs to experiment with multiple approaches.

**Example:**
```typescript
interface PipelineStage<TIn, TOut> {
  name: string;
  execute(input: TIn, context: PipelineContext): Promise<TOut>;
}

interface CandidateGenerator {
  name: string;
  generate(query: DiscoveryQuery): Promise<CandidateSet>;
}

interface Ranker {
  name: string;
  rank(candidates: ScoredPaper[], context: RankingContext): Promise<RankedResult[]>;
  explain(paper: RankedResult): ExplanationSignal[];
}

// Pipeline composition
const pipeline = createPipeline({
  generators: [lexicalAdapter, graphAdapter],
  filters: [timeBasisFilter, categoryFilter, triageStateFilter],
  rankers: [recencyRanker, relevanceRanker],
  diversifier: topicDiversifier,
  explainer: signalAssembler,
});

const resultSet = await pipeline.execute(query);
```

### Pattern 2: Thin MCP Layer Over Thick Services

**What:** MCP tool/resource/prompt handlers are thin translation layers. They validate input with Zod, call a service method, and format the response. All business logic lives in services.

**When to use:** Always. This is the fundamental separation that keeps the core engine testable and reusable independent of MCP.

**Trade-offs:**
- Pro: The entire discovery engine can be tested without MCP transport. Services can serve future CLI tools, web APIs, or other protocols.
- Pro: MCP surface changes (adding tools, renaming parameters) do not require service rewrites.
- Con: Requires discipline to avoid logic creep into MCP handlers. Enforce through code review.

**Example:**
```typescript
// mcp/tools/discovery.ts -- thin handler
server.tool("search_papers", searchPapersSchema, async (params) => {
  const query = mapToDiscoveryQuery(params);
  const resultSet = await discoveryService.search(query);
  return formatResultSet(resultSet);
});

// services/discovery.ts -- business logic
class DiscoveryService {
  async search(query: DiscoveryQuery): Promise<ResultSet> {
    const pipeline = this.buildPipeline(query);
    const results = await pipeline.execute(query);
    const resultSet = await this.persistResultSet(results);
    return resultSet;
  }
}
```

### Pattern 3: Lazy Enrichment with Provenance Tracking

**What:** Metadata is ingested eagerly (OAI-PMH). Everything else -- embeddings, external graph data, content conversion, citation enrichments -- is triggered lazily (on first access or by explicit request) and records full provenance.

**When to use:** Any operation that fetches external data, runs ML inference, or converts content. This pattern directly implements ADR-0002 (metadata-first, lazy enrichment) and ADR-0003 (license and provenance first).

**Trade-offs:**
- Pro: Cheap to start. The system is useful with metadata alone. Heavy operations only run when their value is proven.
- Pro: Full provenance means every piece of derived data can be audited, refreshed, or invalidated.
- Con: First access to un-enriched papers may be slower. Mitigated by background enrichment of "touched" papers and user-visible cohorts.

**Example:**
```typescript
interface EnrichmentRecord {
  paperId: string;
  source: "openalex" | "semantic_scholar" | "crossref";
  enrichmentType: string;
  data: JsonValue;
  fetchedAt: Date;
  expiresAt: Date | null;
  provenance: ProvenanceRecord;
}

class EnrichmentService {
  async getOrEnrich(paperId: string, type: string): Promise<Enrichment> {
    const cached = await this.db.getEnrichment(paperId, type);
    if (cached && !this.isExpired(cached)) return cached;

    const fresh = await this.fetchFromProvider(paperId, type);
    await this.db.upsertEnrichment(paperId, type, fresh);
    return fresh;
  }
}
```

### Pattern 4: Content Variant Model with Acquisition Order

**What:** Each paper can have multiple content variants (abstract, HTML, source-derived, PDF-derived markdown, TEI/XML). Variants are acquired in a preferred order (cheapest and most reliable first) and each records its source, conversion backend, rights basis, and quality warnings.

**When to use:** Whenever content beyond the abstract is requested. The system tries the preferred acquisition order and stops at the first successful variant that satisfies the request.

**Trade-offs:**
- Pro: Users and agents always get the best available content without knowing the backend details.
- Pro: Rights compliance is built into the variant model -- each variant knows its license basis.
- Con: The variant model requires more schema complexity than a simple "fulltext" column. Justified by the project's commitment to provenance (ADR-0003).

**Preferred acquisition order:**
1. Abstract (always available, always safe)
2. arXiv HTML (best structured, when available)
3. arXiv source-derived (often stronger than PDF, when source is clean)
4. OpenAlex GROBID XML (structured fallback for some works)
5. PDF-derived markdown (most universal, least reliable, most expensive)

### Pattern 5: Compute Profiles as Feature Flags

**What:** The system supports Bronze, Silver, and Gold compute profiles that progressively enable more expensive features. Profiles are runtime configuration, not code branches.

**When to use:** At startup and at feature-gate decision points. The profile determines whether semantic search is available, whether content conversion workers run, and how broadly embeddings are generated.

**Trade-offs:**
- Pro: Bronze is fully useful on day one with zero ML infrastructure. Silver and Gold are incremental upgrades, not rewrites.
- Pro: Same codebase serves a laptop with no GPU and a workstation with a 1080 Ti.
- Con: Feature-gated code paths require testing at each profile level.

```typescript
interface ComputeProfile {
  name: "bronze" | "silver" | "gold";
  features: {
    lexicalSearch: true;          // Always on
    semanticSearch: boolean;      // Silver+
    contentNormalization: boolean; // Gold
    broadEmbeddings: boolean;     // Gold
    advancedReranking: boolean;   // Gold
  };
  embeddingPolicy: "none" | "touched" | "recent_window" | "broad";
}
```

## Data Flow

### Discovery Request Flow

```
Agent/User (MCP client)
    │
    ▼
MCP Tool Handler (search_papers / browse_recent / find_related)
    │  validates input with Zod, translates to DiscoveryQuery
    ▼
Discovery Service
    │  selects pipeline configuration based on query type
    ▼
Retrieval Pipeline
    │
    ├──▶ Candidate Generation
    │      ├── Lexical (PG tsvector)     ─── returns scored candidates
    │      ├── Graph (OpenAlex related)   ─── returns scored candidates
    │      ├── Semantic (pgvector)        ─── returns scored candidates (if Silver+)
    │      └── Metadata (SQL fields)      ─── returns scored candidates
    │      ─── merge candidates ───▶
    │
    ├──▶ Constraint Filtering
    │      ├── Time basis (submission / update / announcement)
    │      ├── Category / topic
    │      ├── Triage state exclusions (already dismissed)
    │      └── Rights filter (if hosted mode)
    │
    ├──▶ Reranking
    │      ├── Relevance ranker
    │      ├── Recency ranker
    │      ├── Profile-match ranker
    │      └── Blending / weighting
    │
    ├──▶ Diversification (optional)
    │      └── Topic-based deduplication
    │
    └──▶ Explanation Assembly
           └── Collects signals from each stage → structured explanation
    │
    ▼
ResultSet (persisted with timestamp, query inputs, provenance)
    │
    ▼
MCP Response (formatted for client)
```

### Ingestion Flow

```
Scheduled Trigger (cron or manual)
    │
    ▼
OAI-PMH Harvester
    │  ├── Uses resumption tokens for incremental harvest
    │  ├── Filters by set (category) if configured
    │  └── Extracts: arXiv ID, metadata, categories, time semantics, license
    │
    ▼
Paper Upsert (PostgreSQL)
    │  ├── Insert or update canonical paper record
    │  ├── Generate tsvector for lexical search
    │  ├── Record delta checkpoint
    │  └── Queue enrichment jobs (lazy, not immediate)
    │
    ▼
Redis Job Queue
    │  ├── OpenAlex enrichment jobs (batched, rate-limited)
    │  ├── Embedding jobs (Silver+, for touched/recent papers only)
    │  └── Content acquisition jobs (Gold, on-demand only)
    │
    ▼
Enrichment Workers (process from queue)
    │  ├── Fetch from OpenAlex → store enrichment with provenance
    │  ├── Generate embeddings → store in pgvector
    │  └── Acquire content → store variant with provenance
    │
    ▼
Enriched Paper (richer metadata, graph edges, optionally embedded)
```

### Workflow State Flow

```
Agent creates collection
    │
    ├── collection persisted in PG
    │
    ▼
Agent runs discovery → gets ResultSet
    │
    ├── agent triages: mark_triage_state(paper, "shortlisted")
    ├── agent triages: mark_triage_state(paper, "dismissed")
    │
    ▼
Agent saves query → SavedQuery persisted
    │
    ├── agent creates watch from saved query
    │
    ▼
Watch runs periodically (or on demand)
    │
    ├── get_delta_since_checkpoint
    │     ├── loads last checkpoint timestamp
    │     ├── runs discovery pipeline with time filter
    │     └── returns only new/updated papers
    │
    ▼
New ResultSet with delta metadata
    │
    ├── agent triages new results
    └── checkpoint updated
```

### Key Data Flows

1. **Metadata ingestion:** OAI-PMH harvester -> paper upsert -> tsvector generation -> enrichment queue. This is the primary data path and runs on a daily schedule. Papers become searchable immediately after upsert.

2. **Discovery request:** MCP tool -> service -> retrieval pipeline (candidate generation across adapters -> filter -> rerank -> explain) -> persisted ResultSet -> MCP response. This is the critical request path and should complete in <2 seconds for metadata-only queries.

3. **Lazy enrichment:** First access or scheduled background job -> enrichment service -> external API (rate-limited) -> store with provenance -> available for subsequent queries. Enrichments are cached with TTL and provenance.

4. **Content acquisition:** Explicit request via `get_content_variant` -> content service -> try preferred acquisition order -> first successful result cached with provenance -> returned. Never on the critical path for search results.

5. **Workflow state mutation:** MCP tool (create_collection, mark_triage, save_query) -> workflow service -> PG write -> ack. Simple CRUD with provenance metadata for agent-added state.

## Scaling Considerations

This system targets single-node deployment (Xeon W-2125, 32GB RAM, GTX 1080 Ti, PostgreSQL, Redis). Scaling considerations are about making that single node work well, not about distributed systems.

| Concern | At 100K papers | At 1M papers | At 2.5M papers (all arXiv) |
|---------|----------------|--------------|---------------------------|
| Metadata storage | ~200MB PG, trivial | ~2GB PG, comfortable | ~5GB PG, comfortable |
| Lexical index (GIN) | Fast, <100ms queries | Fast, <200ms queries | Moderate, may need query tuning |
| Embeddings (pgvector) | ~400MB for 100K at 768-dim | ~4GB, fits in RAM | ~10GB, exceeds RAM -- selective only |
| Content variants | On-demand only | On-demand only | On-demand only, never bulk |
| OAI-PMH harvest | Minutes | Hours for initial; minutes incremental | ~24hrs initial; minutes incremental |
| Redis queues | Trivial | Trivial | Trivial |

### Scaling Priorities

1. **First bottleneck: Initial OAI-PMH harvest time.** A full arXiv harvest takes many hours due to OAI-PMH rate limits. Mitigation: Start with category-scoped harvests (e.g., cs, physics subset) to get useful data fast, then backfill. Daily incremental harvests are always small (hundreds to low thousands of papers).

2. **Second bottleneck: Embedding memory at full corpus scale.** At 2.5M papers with 768-dim float32 embeddings, the vector index alone is ~7.5GB. This exceeds comfortable single-node RAM budgets. Mitigation: The compute profile system (Bronze/Silver) means embeddings are selective -- recent window, user-touched papers, high-value cohorts only. Full-corpus embedding is explicitly a Gold-tier feature and may never be needed.

3. **Third bottleneck: External API rate limits.** OpenAlex allows 10 req/s with polite pool, Semantic Scholar allows 1 req/s unauthenticated. Mitigation: Batch enrichment with rate limiting via Redis. Enrich lazily, not eagerly. Cache with TTL.

## Anti-Patterns

### Anti-Pattern 1: Mega-Search Tool

**What people do:** Expose a single `search` MCP tool with dozens of optional parameters that handles search, browse, find-related, and delta queries.
**Why it's wrong:** Makes the MCP surface opaque to agents. Agents cannot discover distinct capabilities. Contradicts ADR-0004 (MCP as workflow substrate).
**Do this instead:** Use intent-named tools (`search_papers`, `browse_recent`, `find_related_papers`, `get_delta_since_checkpoint`). Each has focused parameters and clear semantics.

### Anti-Pattern 2: Business Logic in MCP Handlers

**What people do:** Put retrieval logic, database queries, ranking, and formatting directly in the tool handler function.
**Why it's wrong:** Makes the core engine untestable without MCP transport. Prevents reuse from CLI, web API, or test harnesses. Creates tight coupling to MCP protocol details.
**Do this instead:** MCP handlers validate input, call a service method, and format the response. Three lines of glue, not fifty lines of logic.

### Anti-Pattern 3: Eager Full-Corpus Enrichment

**What people do:** Immediately enrich every ingested paper with OpenAlex data, generate embeddings, and convert content on ingestion.
**Why it's wrong:** Enormously expensive for a 2.5M paper corpus. Most papers will never be accessed. Violates ADR-0002 (metadata-first, lazy enrichment).
**Do this instead:** Ingest metadata eagerly. Enrich lazily on first access or for explicitly-touched cohorts. Queue background enrichment for user-visible paper sets.

### Anti-Pattern 4: Tags as Universal Interest Representation

**What people do:** Model all user interest state as tag strings (like arxiv-sanity-lite's tags).
**Why it's wrong:** Forecloses richer interest representations like seed paper sets, followed authors, saved queries, and negative examples. Violates ADR-0001 (exploration-first).
**Do this instead:** Model interest as InterestProfile objects that can compose multiple signal types. Tags can be one signal type among several.

### Anti-Pattern 5: Embedding Everything on Day One

**What people do:** Treat semantic/vector search as a prerequisite before shipping anything useful.
**Why it's wrong:** The GTX 1080 Ti has 11GB VRAM. Full-corpus embedding of 2.5M papers is expensive and the value is unproven for this product. PostgreSQL FTS provides a strong baseline for exact and near-exact search.
**Do this instead:** Start with metadata + lexical search (Bronze). Add selective embeddings for recent/touched papers (Silver). Expand coverage only after experiments prove the value (Gold).

### Anti-Pattern 6: Ignoring Time Semantics

**What people do:** Treat all timestamps as equivalent. "New paper" means "recently ingested."
**Why it's wrong:** arXiv has three distinct time concepts: submission date, last update date, and announcement date. Confusing these produces misleading "what's new" results.
**Do this instead:** Expose time basis explicitly in queries and results. Store all three timestamps. Let users and agents choose which time concept they mean.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| arXiv OAI-PMH | Scheduled batch harvest with resumption tokens | Base URL: `https://oaipmh.arxiv.org/oai`. Updates nightly ~10:30pm ET Sun-Thu. Rate-limit to 1 req/3s per arXiv guidelines. |
| arXiv API | On-demand search for queries not well-served by local index | Atom XML responses. Max 2000 results per call, 30000 total. Use for bootstrapping specific topics. |
| arXiv HTML | On-demand fetch for content variant | Available for many but not all papers. Check availability before fetch. |
| arXiv Source | On-demand fetch for content variant | `/e-print/{id}` endpoint. Rights check required per paper. |
| OpenAlex | Lazy enrichment + graph expansion | 10 req/s with polite pool. Rich: works, authors, topics, related_works, citations. Primary enrichment source. |
| Semantic Scholar | Optional lazy enrichment | 1 req/s unauthenticated, 10 req/s with API key. Recommendations, SPECTER2 embeddings. |
| Crossref | Optional DOI enrichment | For papers with DOIs. License and bibliographic metadata. |
| PaddleOCR | PDF OCR fallback | Already running as Docker container on port 8765. Use only for scanned PDFs that other backends cannot handle. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| MCP layer <-> Services | Direct function calls | Same process. MCP handlers hold service references. No HTTP/RPC between these. |
| Services <-> Retrieval Pipeline | Typed function interface | Services configure and execute pipelines. Pipeline stages are pure functions with typed I/O. |
| Services <-> Database | Query function layer | All SQL goes through `db/queries/`. Services never write raw SQL. Enables migration testing. |
| Ingestion <-> Canonical Store | Database writes via query layer | Ingestion workers write to the same PG instance. Use transactions for paper upsert + tsvector generation. |
| Enrichment <-> External APIs | Rate-limited HTTP clients | Each external adapter manages its own rate limiter. Redis tracks request budgets. |
| Content <-> Backends | HTTP or subprocess | arXiv HTML/source via HTTP. Marker/Docling/GROBID via subprocess or container. Each behind a common `ContentBackend` interface. |

## Build Order and Dependencies

The build order follows from the architectural dependencies. Each layer depends on the layers below it.

### Phase 1: Foundation (must come first)

**Build:** Models, database schema, config, PostgreSQL client, Redis client.

**Why first:** Everything else depends on the domain model (Paper, ContentVariant, etc.) and the database layer. Getting the schema right -- especially time semantics, external IDs, and provenance columns -- prevents costly migrations later.

**Enables:** All subsequent phases.

### Phase 2: Ingestion + Lexical Search

**Build:** OAI-PMH harvester, paper upsert, tsvector generation, lexical retrieval adapter, basic retrieval pipeline (candidate generation + filtering only).

**Why second:** Without data, nothing else is testable. The OAI-PMH harvester populates the canonical store. tsvector generation makes papers searchable immediately. This is the "Bronze" profile and should be useful on its own.

**Depends on:** Phase 1 (models, DB).
**Enables:** Discovery service, MCP tools.

### Phase 3: Core Services + Basic MCP

**Build:** Discovery service (search, browse_recent), basic workflow service (collections, triage), MCP server with 4-6 core tools and paper resources.

**Why third:** This is the minimum viable MCP server. An agent can search, browse recent, and triage papers. The discovery service composes the retrieval pipeline. The MCP layer is thin.

**Depends on:** Phase 2 (populated store, lexical search).
**Enables:** Real agent workflows, user testing.

### Phase 4: Workflow State + Delta/Watch

**Build:** Saved queries, watches, delta checkpoints, `get_delta_since_checkpoint` tool, interest profile objects.

**Why fourth:** Workflow state is what differentiates this from a simple search wrapper (ADR-0004). But it requires working discovery and a populated store to be testable.

**Depends on:** Phase 3 (working discovery, basic MCP).
**Enables:** Repeated monitoring workflows, "what's new since last check."

### Phase 5: Enrichment Adapters

**Build:** OpenAlex adapter, enrichment service, enrichment job queue, graph retrieval adapter.

**Why fifth:** External enrichments add value (related works, topics, citation counts) but are not needed for core discovery. Building them after the core works means enrichments can be tested against the lexical baseline.

**Depends on:** Phase 2 (populated store), Phase 3 (services pattern).
**Enables:** Stronger seed expansion, richer explanations, experiment Track A and B.

### Phase 6: Content Normalization

**Build:** Content variant model, content service, arXiv HTML fetcher, source extractor, one PDF backend (Marker), provenance tracking.

**Why sixth:** Content normalization is the most complex and rights-sensitive subsystem. It should be built after the discovery core is stable, so that content issues do not block core discovery development.

**Depends on:** Phase 1 (content variant model), Phase 3 (content MCP tools).
**Enables:** Full-text reading within agent workflows.

### Phase 7: Semantic Search (Silver Profile)

**Build:** Embedding generation worker, pgvector integration, semantic retrieval adapter, hybrid candidate generation, reranking experiments.

**Why seventh:** Semantic search is the "Silver" upgrade. It requires a working lexical baseline to compare against (ADR-0001 exploration-first). Building it last among core features means we have evidence about whether it is worth the cost.

**Depends on:** Phase 2 (lexical baseline), Phase 5 (enrichments for comparison).
**Enables:** Hybrid retrieval, profile-driven recommendations.

## Sources

- [arXiv OAI-PMH interface](https://info.arxiv.org/help/oa/index.html) -- Bulk metadata harvesting documentation
- [arXiv API documentation](https://info.arxiv.org/help/api/index.html) -- Search API reference
- [arXiv Bulk Data Access](https://info.arxiv.org/help/bulk_data.html) -- Bulk data options and constraints
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) -- Official SDK for building MCP servers
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture) -- Protocol architecture documentation
- [Building Production-Ready MCP Servers](https://dev.to/quantbit/building-production-ready-mcp-servers-with-typescript-3b19) -- Production patterns for TypeScript MCP servers
- [Building Scalable MCP Servers with DDD](https://medium.com/@chris.p.hughes10/building-scalable-mcp-servers-with-domain-driven-design-fb9454d4c726) -- Domain-driven design for MCP
- [PostgreSQL Full-Text Search with TypeScript](https://betterstack.com/community/guides/scaling-nodejs/full-text-search-in-postgres-with-typescript/) -- FTS implementation guide
- [pgvector](https://github.com/pgvector/pgvector) -- Vector similarity search for PostgreSQL
- [pgvector 2026 Guide](https://www.instaclustr.com/education/vector-database/pgvector-key-features-tutorial-and-pros-and-cons-2026-guide/) -- Features, indexing, and scaling considerations
- Internal project documentation: `docs/05-architecture-hypotheses.md`, `docs/06-mcp-surface-options.md`, `docs/07-data-sources-content-rights.md`, `docs/09-roadmap.md`, ADR-0001 through ADR-0004

---
*Architecture research for: arXiv Discovery MCP -- MCP-native scholarly discovery system*
*Researched: 2026-03-08*
