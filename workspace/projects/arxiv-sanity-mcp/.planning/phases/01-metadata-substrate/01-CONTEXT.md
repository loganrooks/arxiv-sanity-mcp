# Phase 1: Metadata Substrate - Context

**Gathered:** 2026-03-08
**Status:** Ready for planning

<domain>
## Phase Boundary

Ingest arXiv metadata, build canonical paper model with correct time semantics, provide lexical search (fielded + full-text), recent-paper browsing, and seed-based related paper discovery. This is the data foundation — no workflow state, no enrichment, no MCP server yet.

</domain>

<decisions>
## Implementation Decisions

### Initial corpus scope
- Configurable category subset inspired by arxiv-sanity's original scope (cs.*, stat.ML, stat.TH, and ML-adjacent math categories)
- Philosophy papers excluded — separate philpapers/semantic-scholar MCP server handles that domain
- Categories configurable at runtime via config file, not hardcoded
- Default set ships with arxiv-sanity's original categories; user can expand
- Need spike/experiment to measure how influence-based pruning affects effective dataset size before committing to broader category inclusion

### Historical depth strategy
- NOT a simple date cutoff — use recency-weighted influence threshold
- Recent papers (last ~2 years): include all papers in configured categories
- Older papers: require increasing influence signal to be included (citation count via OpenAlex as proxy)
- Exact thresholds are empirical — design the system to support configurable tiers, then tune
- This means Phase 1 ingests all metadata but the influence-based filtering may need Phase 4 (OpenAlex enrichment) data to fully work; Phase 1 should ingest broadly and support filtering at query time

### Cross-listed papers
- Single paper record stores all arXiv categories; primary category tracked separately

### Update frequency
- Daily incremental harvest matching arXiv's announcement cycle (OAI-PMH updates nightly)

### Search result shape
- Rich results: title, authors, abstract snippet, all categories, all four dates (submission, update, announcement, OAI datestamp), version info, license
- Full paper detail available via separate get_paper equivalent

### Claude's Discretion
- Harvesting strategy: CLI command vs background job, resume-on-failure approach
- Influence proxy implementation details (citation count tiers, decay function)
- Project scaffolding: repo layout, dependency management, migration strategy
- Cross-listing dedup strategy
- Lexical similarity method for find_related_papers (tsvector similarity vs TF-IDF)

</decisions>

<specifics>
## Specific Ideas

- Influence-based historical pruning is a novel approach — may need a spike to validate before committing to thresholds. Design the ingestion to support this but don't block Phase 1 on getting it perfect.
- arxiv-sanity's original categories are the baseline default set. The system should make it trivial to add/remove categories.
- The recency-weighted influence idea: "highly influential papers, even from 10-15 years ago, should be included; more recent papers need less of an influence threshold." This is a product-defining feature worth getting right.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- None — greenfield project, no existing code

### Established Patterns
- None yet — Phase 1 establishes all patterns

### Integration Points
- PostgreSQL 16.11 running on target machine (localhost:5432)
- Redis 7.0.15 running on target machine (localhost:6379)
- CUDA 12.4 driver available (GTX 1080 Ti) — not needed for Phase 1
- PaddleOCR container on port 8765 — not needed for Phase 1

</code_context>

<deferred>
## Deferred Ideas

- Spike needed: measure influence-based pruning effectiveness across category sets to determine how broadly to set default categories
- Philosophy-adjacent categories (physics.hist-ph, quant-ph) — separate project handles philosophy papers
- Cross-corpus expansion beyond arXiv — explicitly v2+

</deferred>

---

*Phase: 01-metadata-substrate*
*Context gathered: 2026-03-08*
