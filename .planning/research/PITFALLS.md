# Pitfalls Research

**Domain:** Scholarly paper discovery (arXiv-centered) + MCP server design
**Researched:** 2026-03-08
**Confidence:** HIGH (verified against official arXiv docs, OAI-PMH spec, MCP protocol spec, and community experience reports)

## Critical Pitfalls

### Pitfall 1: Treating arXiv Dates as Simple Timestamps

**What goes wrong:**
The system confuses submission date, announcement date, OAI-PMH datestamp, and identifier month -- leading to incorrect "what's new" feeds, broken delta/checkpoint logic, and papers appearing in wrong time windows. arXiv has at least four distinct temporal semantics:

1. **Submission date** -- when the submitter clicked "Submit Article"
2. **Announcement date** -- when arXiv made it public (8PM ET, Sun-Thu only)
3. **OAI-PMH datestamp** -- last metadata modification, which can be an administrative or bibliographic update unrelated to content changes
4. **Identifier month** -- assigned at announcement, not submission; can differ from submission month

OAI-PMH datestamps are explicitly documented as unreliable for determining submission or replacement times. arXiv has performed bulk metadata updates historically, resetting datestamps for large numbers of older records. The OAI-PMH interface does not support selective harvesting by submission date at all.

**Why it happens:**
Developers assume "datestamp" means "when this paper was submitted or updated" because that is the intuitive interpretation. The arXiv documentation buries this caveat in a single sentence.

**How to avoid:**
- Model time semantics explicitly in the paper schema: separate fields for `submitted_at`, `announced_at`, `oai_datestamp`, and `identifier_month`
- Use the `arXivRaw` OAI-PMH format, which includes version history with per-version submission dates
- For "what's new" feeds, track announcement dates (available from RSS `announce_type` and announcement schedule logic), not OAI-PMH datestamps
- For incremental harvesting, use OAI-PMH datestamps only as a change-detection signal (something changed), not as a content-change signal (the paper was updated)
- Document the arXiv announcement schedule in the codebase: cutoff at 14:00 ET Mon-Fri, announcements at 20:00 ET Sun-Thu, no announcements Fri-Sat

**Warning signs:**
- "New papers" feed shows papers from months ago after a metadata refresh
- Delta checkpoints miss genuinely new papers because their datestamp falls outside the window
- Papers appear to shift between days when viewed by different time semantics
- Weekend/holiday gaps produce unexpected empty or double-size feeds

**Phase to address:**
Phase 1 (Ingestion and canonical store). The paper schema must encode time semantics correctly from day one. Retrofitting temporal semantics is extremely expensive.

---

### Pitfall 2: Naive OAI-PMH Harvesting

**What goes wrong:**
The harvester silently loses data, stalls, or produces an incomplete mirror due to OAI-PMH protocol edge cases specific to arXiv:

- **Resumption token expiry:** As of March 2025, arXiv resumption tokens expire daily and no longer include total counts or cursor positions. A harvest that spans more than a day (common for initial full harvest of 2M+ records) will fail mid-stream with an expired token.
- **Base URL change:** The OAI-PMH endpoint moved from `http://export.arxiv.org/oai2` to `https://oaipmh.arxiv.org/oai` in March 2025. Many existing tools and code examples still reference the old URL.
- **Rate limiting:** arXiv enforces a hard limit of one request every three seconds across all machines under your control. This is not per-endpoint -- it applies collectively to OAI-PMH, API, and RSS.
- **Metadata format differences:** `oai_dc` lacks license info and version history; `arXiv` format lacks version history; only `arXivRaw` has full version history but is larger and closer to internal representation.
- **Set structure:** Categories follow a hierarchical `group:archive:CATEGORY` pattern (e.g., `math:math:NA`), not flat category strings.

**Why it happens:**
OAI-PMH is a 20-year-old protocol, and developers treat it as a simple paginated API. arXiv's implementation has arXiv-specific behaviors that diverge from the generic spec.

**How to avoid:**
- Implement harvest checkpointing: save the last successfully-processed datestamp range so harvests can be resumed from a known good point, independent of resumption tokens
- Use the `arXivRaw` format for the canonical harvest to capture full version history and license metadata
- Implement the 3-second delay strictly, with back-off on HTTP 429/503
- Hard-code the new base URL (`https://oaipmh.arxiv.org/oai`) and flag it as a monitored dependency
- Build initial bulk import as a separate, restartable process (not the same code path as daily incremental updates)

**Warning signs:**
- Harvest completes but paper count is significantly less than expected (~2.5M as of 2026)
- Resumption token errors appear in logs after overnight runs
- License metadata is missing on harvested records (wrong format selected)
- Papers from certain categories never appear (set specification error)

**Phase to address:**
Phase 1 (Ingestion). This is the foundation -- everything downstream depends on a correct and complete metadata mirror.

---

### Pitfall 3: MCP Tool Proliferation and Context Bloat

**What goes wrong:**
The MCP server exposes too many fine-grained tools with verbose descriptions, consuming thousands of tokens from the LLM's context window before any actual work begins. A real-world example: one MCP server with 20 tools consumed 14,214 tokens just for tool definitions. In this project's case, the design docs already sketch ~20+ candidate tools across discovery, state, content, and explanation categories. Exposing all of them simultaneously would bloat context catastrophically, especially when the server is one of multiple MCP servers attached to the same client.

**Why it happens:**
Developers design MCP servers like REST APIs -- one endpoint per operation. But MCP tools are not API endpoints; their definitions are injected into the LLM's context window on every request. Each tool's name, description, and JSON schema parameters consume tokens. The cost is paid whether or not the tool is used.

**How to avoid:**
- Start with 5-8 high-level, intent-based tools maximum for the initial MCP surface
- Combine related operations into single tools with mode parameters (e.g., `manage_collection` with actions `create`, `add`, `remove` rather than three separate tools)
- Use MCP resources for data retrieval that does not require LLM decision-making (paper metadata, content variants, collection contents)
- Use MCP prompts to package multi-step workflows (daily-digest, literature-map) rather than expecting the LLM to compose tool sequences
- Implement tool output schemas (MCP spec feature) so clients can handle structured data without dumping raw JSON into the context
- Keep tool descriptions concise: specify when to use, argument format, and return shape in minimal prose

**Warning signs:**
- Claude Code takes noticeably longer to respond when the server is connected
- The LLM calls the wrong tool or fabricates tool arguments
- Tool descriptions alone exceed 5,000 tokens
- Users report the server feels "noisy" or "confusing"

**Phase to address:**
Phase 3 (MCP surface design). But the awareness must start in Phase 1: design internal APIs with the understanding that the MCP layer will aggregate, not mirror, them.

---

### Pitfall 4: Premature Embedding Commitment

**What goes wrong:**
The project invests heavily in embedding infrastructure (model selection, vector store, GPU pipeline) before establishing whether lexical + graph retrieval is "good enough" for the core use cases. This leads to:

- Wasted compute on embedding millions of abstracts when lexical search already handles most queries well
- Locked-in embedding model choice that becomes expensive to change when better models appear
- Over-complicated architecture from day one that slows iteration on the product features that actually matter (workflow state, delta tracking, interest profiles)

Research shows that pre-trained embedding models without fine-tuning often produce near-random ranking results in domain-specific scenarios. A single model fine-tuned on MS MARCO does not beat BM25 on out-of-domain evaluation (BEIR benchmarks). Single-vector embeddings are a lossy tool with known theoretical limitations on combinatorial precision.

**Why it happens:**
"Semantic search" sounds modern and powerful. The ML community defaults to embedding-first approaches. But for a scholarly discovery system with structured metadata, categories, citation graphs, and explicit interest profiles, lexical + graph retrieval covers a large fraction of use cases effectively.

**How to avoid:**
- Follow the project's own ADR-0002 (metadata-first, lazy enrichment) strictly
- Build Stack A (metadata + lexical + graph) first and measure its failure modes before adding embeddings
- When embeddings are introduced, embed selectively: recent papers, user-touched papers, seed-set neighborhoods -- not the full corpus
- Use the exploration-first architecture (ADR-0001) to make embedding retrieval one adapter among many, not the primary path
- Establish an evaluation benchmark (exact queries, exploratory queries, seed expansion) before investing in embeddings, so you can measure whether they actually improve discovery

**Warning signs:**
- Architecture discussions center on which embedding model to use before the lexical baseline exists
- GPU utilization is discussed before the paper schema is stable
- The project feels slow because embedding pipeline development blocks product feature work
- You cannot answer "what does the embedding approach improve over BM25 for our actual use cases?"

**Phase to address:**
Phase 2 (Retrieval and ranking). Embeddings should enter no earlier than Phase 2, and only after the lexical + graph baseline has been evaluated against real queries.

---

### Pitfall 5: Ignoring arXiv Content Rights in Architecture

**What goes wrong:**
The system stores, serves, or transforms full-text content without per-paper license checking, creating legal liability and making the hosted/public deployment path impossible. The critical facts:

- arXiv metadata (titles, abstracts, authors, identifiers) is CC0 -- freely reusable
- The vast majority of e-prints are under arXiv's non-exclusive distribution license, which does **not** grant third-party redistribution rights
- A smaller fraction carry CC-BY, CC-BY-SA, CC-BY-NC-SA, or CC0 licenses that do permit redistribution
- License metadata is available in OAI-PMH (arXiv and arXivRaw formats) and RSS, but NOT in the search API schema
- Derived artifacts (markdown from PDF, extracted sections) inherit the rights constraints of their source

**Why it happens:**
Developers treat arXiv as a "public repository" and assume all content is freely redistributable. The distinction between "publicly accessible" and "freely redistributable" is non-obvious. Many arXiv tools simply download and serve PDFs without checking.

**How to avoid:**
- Follow ADR-0003 (license and provenance first): store license metadata for every paper at ingestion time
- Implement a rights-checking gate in the content pipeline: before storing, transforming, or serving any full-text artifact, verify the paper's license permits the intended use
- Design two operational modes from the start: local/private (more permissive, caching for personal use) and hosted/public (conservative, metadata + abstracts + links only unless CC-licensed)
- Record provenance on every content variant: source, acquisition timestamp, license basis, conversion path
- Default to metadata + abstract only; full text is an explicit upgrade path, not a default

**Warning signs:**
- Content pipeline has no license field or license-checking logic
- The system serves PDF-derived markdown for papers without verifying their license
- No distinction between local and hosted behavior in the content layer
- A user asks "can I host this?" and the answer requires code archaeology

**Phase to address:**
Phase 1 (Data model and ingestion). License metadata must be captured at ingestion time and the provenance model must be baked into the content variant schema from the start.

---

### Pitfall 6: "Chat with Papers" Feature Creep

**What goes wrong:**
The project drifts from its core identity (discovery, monitoring, triage) toward becoming a generic "chat with papers" or "paper Q&A" system. This is seductive because LLMs make it easy to build and it feels impressive in demos. But it pulls the project away from its distinctive value (explicit taste modeling, inspectable ranking, workflow state) toward a crowded, commoditized space where many well-funded tools already exist (Elicit, Consensus, ChatGPT with search).

**Why it happens:**
Every AI-adjacent project feels pressure to "use the LLM" prominently. Paper Q&A is a visible, demo-friendly feature. Discovery and monitoring are harder to demonstrate but more valuable to repeat users. The design docs explicitly warn against this: "General-purpose paper chatbot -- discovery is the product, not conversation."

**How to avoid:**
- Keep the out-of-scope list visible: general-purpose paper chatbot is out of scope
- Design evaluation criteria around discovery quality (did the user find relevant papers they wouldn't have found otherwise?) not conversation quality
- When tempted to add chat features, ask: "Does this help discovery, monitoring, or triage? Or is this generic paper Q&A?"
- Use MCP prompts for guided workflows (daily-digest, literature-map) rather than open-ended chat
- Channel LLM capability into ranking explanations and structured summaries, not free-form conversation

**Warning signs:**
- Feature discussions start centering on "ask a question about this paper"
- Long-context paper ingestion becomes a priority before the feed system works
- The MCP surface starts looking like a chatbot API rather than a workflow substrate
- User testing focuses on conversational interactions rather than discovery tasks

**Phase to address:**
Every phase (architectural discipline). But especially Phase 3 (MCP surface design), where the temptation to add "chat" tools is strongest.

---

### Pitfall 7: OpenAlex Enrichment as a Blocking Dependency

**What goes wrong:**
The system treats OpenAlex enrichment as part of the critical path for paper display and search, causing cascading failures when the OpenAlex API is slow, rate-limited, or down. OpenAlex has moved to a credit-based rate limiting model (as of 2025): singleton requests cost 1 credit, list requests cost 10, vector search costs 1,000. Free tier provides ~$1/day of credits. Exceeding this produces 409 errors.

Additionally, there is an inherent lag between arXiv announcement and OpenAlex indexing. A new arXiv paper may not appear in OpenAlex for days or weeks. Building features that depend on OpenAlex enrichment for newly announced papers will produce incomplete or broken results.

**Why it happens:**
OpenAlex data is rich and useful (topics, related works, citations, author disambiguation). The temptation is to make it integral to every paper's representation. But enrichment latency and API constraints make it unsuitable as a synchronous dependency.

**How to avoid:**
- Follow ADR-0002: enrichment is lazy, not eager. Papers should be fully functional with arXiv metadata alone.
- Implement a background enrichment scheduler that processes papers in priority order (user-touched > recent > backfill)
- Cache OpenAlex responses aggressively with TTL-based refresh
- Design the UI/MCP surface to gracefully degrade when enrichment data is absent: show what you have, indicate what is pending
- Track OpenAlex credit usage and implement budget-aware scheduling
- Register for an OpenAlex API key (required since Feb 2025) and monitor the rate-limit headers in every response

**Warning signs:**
- Paper detail views hang or error when OpenAlex is unreachable
- New papers appear "incomplete" because enrichment has not run yet
- OpenAlex credit budget is exhausted by mid-day due to eager enrichment
- The system makes synchronous OpenAlex calls on the MCP tool request path

**Phase to address:**
Phase 1 (Data model -- enrichment fields must be nullable/optional) and Phase 2 (Enrichment scheduling -- background processing).

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Flat string categories instead of hierarchical sets | Simpler ingestion code | Cannot properly handle cross-listing, primary vs secondary categories, or arXiv's group:archive:category hierarchy | Never -- arXiv categories are inherently hierarchical |
| Single "date" field instead of explicit time semantics | Simpler schema | Broken delta computation, incorrect "new paper" feeds, confused users | Never -- time semantics are core to the product |
| Embedding everything on first ingest | "Complete" vector coverage | Massive upfront compute cost, locked-in model choice, delays shipping useful features | Only after evaluation proves selective embedding is insufficient |
| Storing full text without license checking | Faster content pipeline | Legal liability, blocked hosted deployment, retroactive cleanup needed | Only in local/private mode with clear documentation |
| One mega `search` MCP tool | Fast to implement | Context bloat, poor agent ergonomics, impossible to add workflow features cleanly | Only as a temporary scaffold replaced within the same phase |
| Hardcoded OpenAlex API calls in retrieval path | Quick enrichment integration | Single point of failure, rate limit exhaustion, no graceful degradation | Never -- enrichment must be async and cacheable |

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| arXiv OAI-PMH | Using old base URL (`export.arxiv.org/oai2`) | Use `https://oaipmh.arxiv.org/oai` (changed March 2025) |
| arXiv OAI-PMH | Using `oai_dc` format for canonical harvest | Use `arXivRaw` to get version history and license info |
| arXiv OAI-PMH | Relying on resumption tokens for multi-day harvests | Implement datestamp-range checkpointing; tokens expire daily |
| arXiv API | Requesting > 1,000 results via search API | Use OAI-PMH for bulk; API search is for targeted queries only |
| arXiv API | Rate limiting per-endpoint instead of globally | The 3-second limit is collective across all arXiv API endpoints and all your machines |
| OpenAlex | Making unauthenticated requests | API keys are required since Feb 2025; unauthenticated gets 100 credits then 409 errors |
| OpenAlex | Using email parameter for "polite" pool | Email parameter is no longer supported; use API keys only |
| OpenAlex | Making one API call per paper for enrichment | Batch using OR syntax to combine up to 50 IDs in one request (10x fewer credits) |
| Semantic Scholar | Assuming stable rate limits | Unauthenticated pool limits have been reduced and may reduce further; get an API key |
| Semantic Scholar | Using `aliases` field | Deprecated to prevent deadnaming |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Full-corpus lexical search without index optimization | Search latency > 1s | Use PostgreSQL tsvector with GIN index or dedicated FTS (Tantivy/SQLite FTS5) | > 500K papers |
| Synchronous enrichment on paper access | Paper detail loads slowly | Background enrichment queue with priority scheduling | > 100 papers/day being viewed |
| Embedding all abstracts on ingest | GPU saturated, ingest bottleneck | Selective embedding (recent, touched, seeds) | > 50K papers to embed |
| Storing all content variants in main database | Database bloat, slow backups | Separate content store (filesystem or object storage) with metadata references | > 10K full-text papers |
| No pagination on MCP tool responses | Context window overflow, slow responses | Hard limit on result count (25-50 papers), with cursor/offset for more | Any search with > 50 results |
| Naive "find related" that scans all papers | O(n) per query | Pre-computed neighborhoods, indexed similarity, or external API (OpenAlex related_works) | > 100K papers |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing arXiv API credentials in code or config files | Credential exposure via git | Use environment variables; credentials in `~/.env` per project conventions |
| MCP server with global mutable state | One user's session state bleeds into another's | Scope all state to explicit session/user identifiers |
| Serving copyrighted full text via hosted MCP | Legal liability | License-gate all full-text operations; default to metadata + abstract |
| Logging full paper content in MCP responses | Disk bloat, potential rights issues | Log metadata only; content delivery via resource URIs |
| No input validation on MCP tool arguments | Injection attacks if tool args reach database queries | Validate and sanitize all tool inputs; use parameterized queries |
| stdout logging in STDIO transport MCP server | Protocol corruption; stray print statements break the JSON-RPC stream | Route all logging to stderr; never write to stdout except protocol messages |

## UX Pitfalls

Common user experience mistakes in this domain for both human users and LLM agents.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No explanation for why a paper surfaced | User cannot calibrate trust in results | Structured ranking explanations with every result (matched terms, seed similarity, graph path) |
| Implicit time basis on search results | User confused about whether results are "new" or "all time" | Always expose time basis explicitly; default to "announced in last 7 days" for browse, "all time" for search |
| Tag-only interest modeling | Forces coarse-grained preferences | Support seed papers, followed authors, saved queries, and negative examples alongside tags |
| Empty results with no guidance | User does not know how to improve their query | Suggest query modifications, related categories, or broader time windows |
| Delta/checkpoint with no "last checked" indicator | User cannot tell if they are caught up | Show explicit "last checked: [timestamp]" and "N new papers since then" |
| Mixing "new submissions" with "updated versions" in feeds | User wastes time re-triaging papers they already saw | Separate new submissions from cross-lists and version updates; use `announce_type` from RSS |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Paper ingestion:** Often missing version history -- verify all versions are captured with per-version dates using `arXivRaw` format
- [ ] **Paper ingestion:** Often missing license metadata -- verify license URI is stored per paper and used in content pipeline gates
- [ ] **Search:** Often missing fielded search -- verify searches can target title, abstract, author, category separately, not just full-text
- [ ] **Delta/checkpoint:** Often missing announcement-date awareness -- verify deltas use announcement schedule logic, not OAI-PMH datestamps
- [ ] **Delta/checkpoint:** Often missing cross-list and replacement handling -- verify `announce_type` (new, cross, replace) is captured and filterable
- [ ] **Content pipeline:** Often missing provenance -- verify every content variant records source, timestamp, license, conversion backend, and cache status
- [ ] **MCP surface:** Often missing resource URIs -- verify papers and collections are addressable as `paper://{id}` resources, not only via tool calls
- [ ] **MCP surface:** Often missing pagination -- verify all list-returning tools have limit/offset or cursor semantics
- [ ] **Interest profiles:** Often missing negative examples -- verify profiles can express "not like this" as well as "like this"
- [ ] **Ranking:** Often missing explanation -- verify every result includes a structured explanation object, not just a score

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Wrong time semantics in schema | HIGH | Schema migration to add separate time fields; re-harvest with `arXivRaw` to populate version dates; audit all delta/checkpoint logic |
| Incomplete OAI-PMH harvest | MEDIUM | Run gap-detection query (compare paper count per category against arXiv stats); re-harvest missing date ranges; validate with random sampling |
| MCP tool bloat | MEDIUM | Audit tool usage (which tools are actually called?); consolidate low-use tools; move data retrieval to resources; measure context token savings |
| Premature embedding lock-in | HIGH | If model is wrong: re-embed entire corpus; if vector store is wrong: migrate and re-index. Prevention is far cheaper. |
| Missing license metadata | HIGH | Re-harvest all papers with `arXivRaw` format; backfill license field; audit content store for unlicensed full-text artifacts; add license gate retroactively |
| Feature creep toward chat | LOW | Prune chat-oriented tools from MCP surface; refocus evaluation criteria on discovery metrics; remove long-context paper ingestion if it exists |
| OpenAlex dependency failure | LOW | All enrichment fields should already be nullable; add circuit breaker to enrichment scheduler; switch to degraded mode (arXiv metadata only) |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Wrong time semantics | Phase 1 (Data model) | Paper schema has separate submitted_at, announced_at, oai_datestamp fields; delta queries use announcement dates |
| Naive OAI-PMH harvesting | Phase 1 (Ingestion) | Full harvest completes successfully with checkpoint/resume; paper count matches expected totals |
| MCP tool proliferation | Phase 3 (MCP surface) | Total tool definitions < 5,000 tokens; tool selection accuracy tested with representative queries |
| Premature embedding commitment | Phase 2 (Retrieval) | Lexical + graph baseline evaluated before any embedding work begins; evaluation benchmark exists |
| Ignoring content rights | Phase 1 (Data model) | License field populated for all papers; content pipeline has license-checking gate; local/hosted modes documented |
| Chat feature creep | All phases | Out-of-scope list reviewed at each phase boundary; no "ask about paper" or "chat with paper" tools in MCP surface |
| OpenAlex blocking dependency | Phase 1 (Data model) + Phase 2 (Enrichment) | All enrichment fields nullable; paper display works with arXiv metadata alone; enrichment runs in background |
| arXiv cross-listing confusion | Phase 1 (Data model) | Paper schema distinguishes primary category from cross-listed categories; search respects both |
| Stale OAI-PMH base URL | Phase 1 (Ingestion) | Endpoint URL is configurable and documented; integration tests hit live endpoint |
| OpenAlex credit exhaustion | Phase 2 (Enrichment) | Credit budget tracking implemented; batch requests using OR syntax; daily usage monitored |

## Sources

- [arXiv API Terms of Use](https://info.arxiv.org/help/api/tou.html) -- rate limits, permitted/prohibited behaviors
- [arXiv OAI-PMH documentation](https://info.arxiv.org/help/oa/index.html) -- datestamp caveats, format differences, base URL change, resumption token behavior
- [arXiv Submission Schedule](https://info.arxiv.org/help/availability.html) -- cutoff times, announcement windows, weekend/holiday behavior
- [arXiv Version Availability](https://info.arxiv.org/help/versions.html) -- version semantics, replacement/withdrawal
- [arXiv Cross-listing](https://info.arxiv.org/help/cross.html) -- multiple category semantics
- [arXiv Identifier for Services](https://info.arxiv.org/help/arxiv_identifier_for_services.html) -- ID format, version resolution
- [OpenAlex Rate Limits](https://docs.openalex.org/how-to-use-the-api/rate-limits-and-authentication) -- credit-based system, API key requirement
- [Semantic Scholar API Release Notes](https://github.com/allenai/s2-folks/blob/main/API_RELEASE_NOTES.md) -- rate limit changes, deprecations
- [NearForm: MCP Tips, Tricks and Pitfalls](https://nearform.com/digital-community/implementing-model-context-protocol-mcp-tips-tricks-and-pitfalls/) -- stdout corruption, tool design, security
- [Phil Schmid: MCP Best Practices](https://www.philschmid.de/mcp-best-practices) -- tool design, context efficiency, argument design
- [CodeRabbit: Ballooning Context in MCP Era](https://www.coderabbit.ai/blog/handling-ballooning-context-in-the-mcp-era-context-engineering-on-steroids) -- context bloat quantification (14K tokens for 20 tools)
- [Glama: Context Bloat in MCP Agents](https://glama.ai/blog/2025-12-16-what-is-context-bloat-in-mcp) -- sub-agent architecture, progressive disclosure
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/resources) -- resource vs tool distinction, protocol semantics
- [Jo Kristian Bergum: Mistakes with Embeddings and Vector Search](https://bergum.medium.com/four-mistakes-when-introducing-embeddings-and-vector-search-d39478a568c5) -- pre-trained model limitations, domain transfer failure
- [Shaped: Vector Bottleneck](https://www.shaped.ai/blog/the-vector-bottleneck-limitations-of-embedding-based-retrieval) -- theoretical limitations of single-vector embeddings
- [OpenAlex Features and Limitations](https://arxiv.org/html/2512.16434v1) -- metadata quality issues, missing fields, indexing lag

---
*Pitfalls research for: arXiv Discovery MCP*
*Researched: 2026-03-08*
