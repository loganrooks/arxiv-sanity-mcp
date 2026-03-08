# Feature Landscape

**Domain:** Scholarly paper discovery, monitoring, and triage (MCP-native)
**Researched:** 2026-03-08
**Overall Confidence:** HIGH

## Product Context

This feature landscape is grounded in analysis of the major scholarly discovery products (arxiv-sanity/lite, Semantic Scholar, Connected Papers, ResearchRabbit, Litmaps, Elicit, Consensus, Scite, OpenAlex, Papers With Code) and existing arXiv MCP servers (blazickjp/arxiv-mcp-server, afrise/academic-search, daheepk/arxiv-paper-mcp). The system targets researchers and AI agents, is MCP-native (tools/resources/prompts), and focuses on discovery/monitoring/triage rather than paper chat.

The key differentiating context: existing arXiv MCP servers are thin search wrappers (search, download, read, list). The scholarly discovery tools are web-only, human-only, and siloed. No product combines discovery-quality features with agent-usable workflow state through MCP.

---

## Table Stakes

Features users expect. Missing = product feels incomplete. These are features present in essentially every serious scholarly discovery tool.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Fielded metadata search** | Every scholarly tool has it. Title, author, abstract, category, date range. Researchers will not use a tool that cannot do basic fielded queries. | Low | arXiv API provides this natively. Must support AND/OR, date ranges, category filters. |
| **Paper metadata retrieval** | Core data model. Users need title, authors, abstract, categories, dates, identifiers. | Low | Canonical paper model with arXiv ID, DOI, OpenAlex ID. Multiple date semantics (submitted, updated, announced). |
| **Recent paper browsing** | arxiv-sanity's most-used feature. "What's new in my field?" is the fundamental use case. | Low | Must support arXiv category filtering and configurable time windows. Time-basis awareness (submission vs. announcement) is important. |
| **Similar/related paper discovery** | Present in arxiv-sanity (SVM), Semantic Scholar (SPECTER2), Connected Papers (co-citation), ResearchRabbit (collection-based). Seed-based expansion is universal. | Medium | Start with lexical similarity (TF-IDF over abstracts), plan for multiple backends. Intent-based tool name (`find_related_papers`), not implementation-based. |
| **Paper collections/libraries** | arxiv-sanity has libraries, Semantic Scholar has My Library, ResearchRabbit has collections, Litmaps has maps. Every tool lets you save papers. | Low | Named collections of papers. Must be first-class MCP resources, not just database rows. Collections power recommendations. |
| **Basic triage workflow** | Researchers universally need to mark papers as "read later," "relevant," "not relevant." arxiv-sanity uses tags; Elicit uses screening states. | Low | Triage states: unseen, seen, shortlisted, dismissed, read, cite-later. Batch operations essential for agents. |
| **Abstract access** | Every tool shows abstracts. Abstracts are the primary triage signal. | Low | Always available as metadata. No rights issues. |
| **External ID resolution** | Researchers reference papers by arXiv ID, DOI, or title. Must resolve across identifier systems. | Low | arXiv ID is canonical. Cross-link to DOI, OpenAlex ID, Semantic Scholar ID. |
| **Result pagination and limits** | Any search system needs bounded result sets. | Low | Cursor-based pagination. Agents need predictable result sizes. |
| **Category/topic filtering** | arXiv has categories (cs.AI, hep-th); OpenAlex has topics. Users expect to scope by field. | Low | Support arXiv categories natively. OpenAlex topics as enrichment layer. |

## Differentiators

Features that set the product apart. Not universally expected, but valued. These are where the project can establish competitive advantage.

### Tier 1 Differentiators: Core Identity

These features define the product's unique position in the landscape: MCP-native workflow substrate with inspectable, steerable discovery.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **MCP-native workflow state** | No existing product exposes collections, triage states, saved queries, watches, and interest profiles as MCP tools/resources/prompts. Existing arXiv MCP servers are stateless search wrappers. This is the primary differentiator. | High | Requires persistent state management (PostgreSQL). Collections, profiles, queries, watches, triage entries as first-class objects. Tools for mutations, resources for retrieval. |
| **Structured ranking explanations** | arxiv-sanity's inspectability was a product virtue, but it only showed TF-IDF signals. No scholarly tool provides structured, machine-readable explanations of why a paper was surfaced. Elicit cites sources but doesn't explain ranking. | Medium | Signal lists with weights, nearest seed exemplars, query match details, category overlap. Structured data first, prose generation second. Must work for both agents and humans. |
| **Delta/checkpoint workflows** | "What's new since I last checked?" is the fundamental monitoring question. No existing MCP server supports this. Web tools use email alerts or feeds but don't expose checkpoints as programmable objects. | Medium | Checkpoint objects tied to saved queries or watches. Delta computation between result sets. Agents can say "run my watch and show me only new papers." |
| **Explicit, steerable interest profiles** | arxiv-sanity used tags/SVMs; Semantic Scholar uses implicit folder-based learning. No tool lets you inspect, edit, and steer a multi-signal interest profile (seeds + queries + authors + negative examples). | High | Interest profile = seed paper sets + saved queries + followed authors + negative examples + topic weights. Inspectable and editable. Machine suggestions require confirmation (ADR principle). |
| **Multiple relatedness modes** | Connected Papers uses bibliographic coupling, Semantic Scholar uses SPECTER2, arxiv-sanity uses TF-IDF. Each finds different things. No tool exposes multiple modes behind a common interface with the user choosing or comparing. | High | Common `find_related_papers` interface with mode parameter. Start with lexical (TF-IDF), add citation-graph (via OpenAlex), then semantic (local embeddings). Results annotated with which mode produced them. |
| **MCP prompts for multi-step workflows** | No existing MCP server packages multi-tool workflows into reusable prompts. Daily digest, literature mapping, triage shortlisting are multi-step workflows that benefit from structured prompt templates. | Medium | `daily-digest`, `literature-map-from-seeds`, `triage-shortlist`, `expand-project-workspace`. Prompts orchestrate multiple tool calls with context. |

### Tier 2 Differentiators: Quality and Depth

These features enhance the product significantly but are not the core identity.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Cost-aware lazy enrichment** | Most tools either embed everything (expensive) or nothing (weak). Selective enrichment on demand means strong results without prohibitive compute. | Medium | Metadata-first. Embeddings computed lazily on touched/saved papers. OpenAlex enrichment triggered by interest, not bulk. Content variants fetched on demand. |
| **OpenAlex graph enrichment** | OpenAlex provides topics, related works, citations, FWCI, institutional data, semantic search -- all free and open. No existing arXiv MCP server uses it. | Medium | Adapter that enriches paper records with OpenAlex topics, citation counts, related works, FWCI. Triggered lazily on papers of interest. |
| **Content variant model** | Papers exist as metadata, abstract, arXiv HTML, LaTeX source, PDF, derived markdown. No tool models these as explicit variants with source-aware acquisition. | Medium | Content variant objects with provenance: source, extraction method, conversion path, rights basis. Enables downstream tools (scholardoc, philo-rag) to consume preferred format. |
| **Provenance tracking** | No discovery tool tracks where each ranking signal or content artifact came from. Critical for research integrity and rights compliance. | Medium | Every content artifact records: source URL, fetch timestamp, extraction method, license. Every ranking signal records: data source, computation method, freshness. |
| **Saved queries as first-class objects** | Litmaps supports monitored searches. No MCP server exposes saved queries as inspectable, runnable, editable objects. | Low | Named queries with parameters, ranking mode, filters. Can be run on demand or attached to watches. MCP resources with stable URIs. |
| **Author following** | ResearchRabbit and Semantic Scholar support this. Useful for tracking specific research groups. | Low | Explicit author follows as part of interest profiles. Delta queries scoped to followed authors. |
| **Batch operations for agents** | No existing scholarly MCP server supports batch triage, batch enrichment, or batch expansion. Agents process lists, not individual items. | Medium | `batch_triage`, `batch_enrich`, `batch_add_to_collection`. Essential for agent efficiency. Single-item-only tools are an anti-pattern for MCP. |

### Tier 3 Differentiators: Future Value

These features are valuable but should be deferred until the core is solid.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Citation-context signals** | Scite pioneered supporting/contrasting/mentioning citation analysis. Richer than raw citation count. | High | Requires full-text analysis of citing papers. OpenCitations may provide some data. Defer until content normalization is mature. |
| **Semantic search (local embeddings)** | Semantic Scholar and OpenAlex both offer this. Local embeddings on a GTX 1080 Ti are feasible for selective corpora. | High | Stack B territory. Selective embedding of saved/touched papers. SPECTER2 or similar model. Do not embed entire corpus eagerly. |
| **Active learning / suggestion loops** | Elicit's Research Agents and Semantic Scholar's feeds learn from user behavior. Powerful but must remain steerable and confirmable. | High | Machine suggests profile updates based on triage behavior. User must confirm. "The system noticed you saved 5 papers on X -- add X to your profile?" |
| **Cross-corpus expansion** | arXiv-first, but researchers need papers from other sources too. Semantic Scholar and OpenAlex cover broader literature. | Medium | OpenAlex adapter already planned. Semantic Scholar as optional. Keep corpus adapters modular. |
| **Popularity/trending signals** | arxiv-sanity had "top hype" views. Papers With Code (now defunct) tracked GitHub stars. HF Trending Papers exists. | Medium | Pluggable popularity ranker. Sources: citation velocity, social mentions, code stars. Not an intrinsic arXiv property. |
| **Email/notification digests** | arxiv-sanity-lite sends daily emails. Standard in monitoring tools. | Low | Low complexity but low priority for MCP-native workflows. Agents don't need email. Human users might want it later. |

## Anti-Features

Features to explicitly NOT build. These are deliberate exclusions based on project identity, competitive landscape, and the risks of scope creep.

### Hard Anti-Features (Never Build)

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **General-purpose paper chatbot** | Discovery is the product, not conversation. Elicit and Consensus own this space. Building a chatbot dilutes the product identity and competes where others are stronger. The project docs explicitly exclude this. | Provide structured content variants that downstream chat tools can consume. Let Claude or other LLMs do the chatting using MCP-provided context. |
| **Full corpus embedding on day one** | Embedding all arXiv papers requires massive compute and storage. The GTX 1080 Ti can handle selective embedding but not millions of papers. Premature optimization before knowing which papers matter. | Lazy, selective embedding of saved/touched/profile-adjacent papers only. Metadata-first design. Use OpenAlex semantic search as a bridge. |
| **Opaque recommendation engine** | arxiv-sanity's value was inspectability. Black-box recommendations violate the core product principle. "We think you'll like this" without "because X" is an anti-feature. | Structured ranking explanations for every surfaced paper. Signal lists, not magic scores. |
| **Automatic profile learning without confirmation** | Implicit learning from behavior creates filter bubbles and removes user agency. The project principle states: explicit > implicit. | Machine suggestions that require user confirmation. "We noticed X -- would you like to add it to your profile?" Never silently adjust profiles. |
| **Benchmark/leaderboard features** | Papers With Code was the leaderboard product (now defunct, absorbed by HF). Building leaderboards is a different product entirely. | Link to external benchmarks if needed. Don't track or display SOTA results. |
| **Real-time collaboration** | Multi-user real-time features (shared annotations, co-triage, comments) are a different product category. Adds enormous complexity for uncertain value. | Single-user/single-agent workflows first. Shared collections as read-only exports at most. |

### Soft Anti-Features (Avoid Unless Evidence Demands)

| Anti-Feature | Why Avoid | Reconsider When |
|--------------|-----------|-----------------|
| **Full-text PDF parsing at ingest time** | Expensive, rights-complex, and unnecessary for discovery. Most triage decisions are made from title + abstract + metadata. | When a specific workflow (e.g., section-level search, figure extraction) proves valuable enough to justify the cost. Content variants should exist as a model but be lazily populated. |
| **Social features (comments, discussions, friends)** | arxiv-sanity had a "friends" view and discussions. Low usage, high maintenance. Social features require critical mass to be valuable. | Only if the system is deployed multi-user and users explicitly request it. |
| **Visual graph rendering** | Connected Papers and Litmaps are visual-first tools. MCP is not a visual medium. Building graph visualization is a UI project, not a discovery substrate project. | When a web frontend is built. The backend should expose graph data structures; rendering is a client concern. |
| **Citation count as a primary signal** | Raw citation count is a popularity proxy, not a quality signal. Biases toward older papers and dominant paradigms. | Use citation velocity (recent citations per unit time) as one signal among many. Never as the default sort. |
| **Broad literature warehouse** | Trying to index all of scholarly literature before arXiv works well is scope creep. OpenAlex, Semantic Scholar, and Google Scholar already do this. | After arXiv ingestion, search, and monitoring are solid. Then add OpenAlex-sourced non-arXiv papers selectively. |
| **Mobile or web UI** | The product is MCP-native. Building a web UI is a separate project that can come later. The MCP surface IS the interface. | When the MCP surface is stable and proven. A web UI is a client of the MCP server, not the product itself. |

## Feature Dependencies

```
Fielded metadata search ─────────────────────────────────────────────────┐
                                                                         │
Paper metadata retrieval ──────────┬──────────────────────────────────────┤
                                   │                                     │
Recent paper browsing ─────────────┤                                     │
                                   │                                     │
Category/topic filtering ──────────┘                                     │
                                                                         │
                                   ┌──── Collections ◄───────────────────┤
                                   │         │                           │
External ID resolution ────────────┤         ▼                           │
                                   │  Interest profiles ◄── Author      │
Abstract access ───────────────────┤         │              following    │
                                   │         ▼                           │
Result pagination ─────────────────┤  Saved queries                      │
                                   │         │                           │
                                   │         ▼                           │
                                   │  Watches + Deltas                   │
                                   │         │                           │
                                   │         ▼                           │
                                   │  Ranking explanations               │
                                   │                                     │
Similar/related papers ────────────┤                                     │
       │                           │                                     │
       ▼                           │                                     │
Multiple relatedness modes         │                                     │
       │                           │                                     │
       ▼                           │                                     │
OpenAlex enrichment                │                                     │
       │                           │                                     │
       ▼                           │                                     │
Semantic search (local)            │                                     │
                                   │                                     │
Basic triage workflow ─────────────┘                                     │
       │                                                                 │
       ▼                                                                 │
Batch operations                                                         │
                                                                         │
Content variant model ◄──── Provenance tracking                          │
       │                                                                 │
       ▼                                                                 │
Lazy enrichment ◄───────── Cost-aware design ◄───────────────────────────┘
       │
       ▼
Citation-context signals (future)
```

**Critical path:** Paper metadata + search + recent browsing --> collections + triage --> saved queries + interest profiles --> watches + deltas --> ranking explanations.

**Parallel track:** Similar papers --> multiple relatedness modes --> OpenAlex enrichment --> semantic search.

**Content track (can lag):** Content variant model --> lazy enrichment --> content normalization.

## MVP Recommendation

The MVP should establish the MCP-native workflow substrate with enough discovery quality to be genuinely useful. It should NOT try to compete on search quality with Semantic Scholar or on visualization with Connected Papers. It should compete on being the only agent-usable, stateful, inspectable arXiv discovery system.

### Phase 1: Core Substrate (Must Ship)

1. **Paper metadata retrieval** -- canonical paper model with arXiv identity
2. **Fielded metadata search** -- title, author, abstract, category, date range
3. **Recent paper browsing** -- "what's new in cs.AI this week"
4. **Category filtering** -- arXiv categories as first-class filters
5. **Collections** -- named paper sets, add/remove, list
6. **Basic triage states** -- unseen/shortlisted/dismissed/read
7. **MCP server** -- tools + resources for above

### Phase 2: Discovery Quality

1. **Similar/related paper discovery** -- TF-IDF baseline
2. **Saved queries** -- named, rerunnable, with parameters
3. **Delta/checkpoint workflows** -- "what's new since last check"
4. **External ID resolution** -- arXiv ID <-> DOI <-> OpenAlex ID
5. **Content variant model** -- abstract + metadata, lazy full-text

### Phase 3: Intelligence

1. **Interest profiles** -- seed sets + queries + authors + negatives
2. **Ranking explanations** -- structured "why this paper"
3. **OpenAlex enrichment** -- topics, citations, related works
4. **Multiple relatedness modes** -- lexical + citation graph
5. **Author following** -- as part of interest profiles
6. **MCP prompts** -- daily-digest, triage-shortlist, literature-map

### Defer

- **Semantic search (local embeddings)**: Until profile-adjacent selective embedding is justified
- **Citation-context signals**: Until content normalization is mature
- **Active learning**: Until interest profiles prove useful
- **Popularity/trending**: Until basic discovery is solid
- **Email notifications**: Low priority for MCP-native workflows
- **Cross-corpus expansion**: After arXiv is well-served

## Competitive Positioning Summary

| Competitor | Their Strength | Our Advantage |
|-----------|---------------|---------------|
| arxiv-sanity/lite | Inspectable taste modeling, fast triage | MCP-native, richer interest representation, agent-usable, still alive |
| Semantic Scholar | Massive corpus, SPECTER2, research feeds | Steerable profiles, structured explanations, workflow state, local-first |
| Connected Papers | Beautiful graph visualization | Multiple relatedness modes, programmable, not single-seed-only |
| ResearchRabbit | Collection-based discovery, free | Agent-usable, explicit profiles, not web-only |
| Litmaps | Citation maps, monitored searches | First-class watches/deltas as MCP objects, not just email alerts |
| Elicit | Evidence workflows, screening | Discovery-focused (complementary), not trying to be Elicit |
| Existing arXiv MCP servers | Easy to set up | Stateful workflows, discovery quality, not just search+download |

## Sources

- [arxiv-sanity-lite (Karpathy)](https://github.com/karpathy/arxiv-sanity-lite) -- feature analysis, SVM/TF-IDF approach
- [Semantic Scholar Review 2025](https://skywork.ai/blog/semantic-scholar-review-2025/) -- TLDR, Reader, Research Feeds
- [Semantic Scholar Review 2026](https://agentaya.com/ai-review/semantic-scholar/) -- current feature set
- [Semantic Scholar Recommendations API](https://api.semanticscholar.org/api-docs/recommendations) -- programmatic recommendations
- [Litmaps vs ResearchRabbit vs Connected Papers 2025](https://effortlessacademic.com/litmaps-vs-researchrabbit-vs-connected-papers-the-best-literature-review-tool-in-2025/) -- comparative features
- [ResearchRabbit 2025 Revamp](https://aarontay.substack.com/p/researchrabbits-2025-revamp-iterative) -- acquisition by Litmaps, new features
- [ResearchRabbit 2026 Review](https://effortlessacademic.com/research-rabbit-2026-review-for-researchers/) -- current state
- [Elicit AI Research Tool Dec 2025 Update](https://scrollwell.com/guide/tools/elicit-ai-research-tool-review-new-features-2025/) -- Research Agents, API
- [Elicit vs Consensus 2026](https://paperguide.ai/blog/elicit-vs-consensus/) -- feature comparison
- [OpenAlex New Features 2026](https://blog.openalex.org/openalex-api-new-features-and-usage-based-pricing/) -- semantic search, advanced search
- [OpenAlex Topics Documentation](https://docs.openalex.org/api-entities/topics) -- topic system details
- [OpenAlex Work Object](https://docs.openalex.org/api-entities/works/work-object) -- related_works, citations, FWCI
- [Papers With Code Shutdown](https://blog.tib.eu/2025/10/02/papers-with-code-went-offline-the-knowledge-doesnt-have-to/) -- Meta sunset July 2025
- [blazickjp/arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) -- existing MCP server feature analysis
- [Scholarly Recommendation Systems Survey](https://www.mdpi.com/2227-9709/12/4/108) -- features, approaches, open directions
- [SPECTER2 Announcement](https://allenai.org/blog/specter2-adapting-scientific-document-embeddings-to-multiple-fields-and-task-formats-c95686c06567) -- embedding model details
- [Justification vs Transparency in Recommender Systems](https://www.mdpi.com/2078-2489/14/7/401) -- explanation design patterns
