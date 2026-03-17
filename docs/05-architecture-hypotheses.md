# Architecture Hypotheses

**Status:** Draft  
**Date:** 2026-03-08

This document lays out candidate architecture shapes without pretending that one has already won.

## 1. Architectural goals

The architecture should make it easy to:

- compare retrieval families,
- add workflow-state features,
- attach multiple external enrichments,
- produce structured explanations,
- and stay cost-aware.

## 2. Core internal object model

Regardless of storage or ranking choices, the following conceptual objects look durable:

- **Paper**
- **ContentVariant**
- **InterestProfile**
- **Collection**
- **SavedQuery**
- **Watch**
- **TriageEntry**
- **ResultSet**
- **RankingExplanation**
- **DeltaCheckpoint**

### Paper
Canonical metadata record with arXiv identity plus external identifiers and enrichment metadata.

### ContentVariant
A specific retrievable representation of a paper:
- abstract
- snippet set
- HTML
- source-derived text
- PDF-derived markdown
- TEI/XML
- chunked section set

### InterestProfile
A user- or agent-steerable profile composed of multiple signals, for example:
- tag membership,
- seed papers,
- followed authors,
- saved query,
- negative examples.

### ResultSet
A materialized search / browse / recommendation output with query inputs, ranking mode, provenance, and timestamp.

## 3. Candidate stack shapes

## Stack A — Metadata + lexical + graph
**Cheapest and simplest serious starting point**

Components:
- arXiv metadata mirror
- lexical index
- optional OpenAlex / Semantic Scholar enrichment
- citation / related-work edges
- workflow-state store
- no local full-corpus embeddings initially

Pros:
- cheap
- explainable
- fast to stand up
- strong baseline for recent feed, search, and graph expansion

Cons:
- weaker semantic recall
- query vocabulary mismatch remains a challenge

## Stack B — Metadata + lexical + selective local semantic
**Balanced local-first option**

Components:
- everything in Stack A
- local embeddings for:
  - recent window,
  - user-touched papers,
  - or high-value cohorts
- optional vector store
- reranking over blended lexical + semantic candidate sets

Pros:
- better semantic discovery
- still cost-conscious
- easier to compare against lexical baseline

Cons:
- more moving parts
- embedding coverage policy becomes a design choice

## Stack C — Metadata + lexical + external API enrichments
**Lean local infrastructure, more remote dependencies**

Components:
- local metadata and workflow state
- lexical index
- OpenAlex / Semantic Scholar used on demand for semantic search, related works, or graph signals

Pros:
- minimal local ML infrastructure
- fast to prototype

Cons:
- rate limits
- dependency risk
- potentially weaker repeatability and higher long-run API costs

## Stack D — Full local hybrid research platform
**Ambitious and powerful, but not a day-one default**

Components:
- full metadata mirror
- broad embedding coverage
- multi-stage retrieval
- content normalization workers
- graph store
- advanced reranking
- cached external signals

Pros:
- strongest long-term control
- high performance potential

Cons:
- highest complexity
- easiest way to overbuild too early

## 4. Recommended starting hypothesis

The best opening move is probably **Stack A moving toward Stack B**, not Stack D.

That means:

1. mirror metadata,
2. build a strong lexical + fielded baseline,
3. add workflow state,
4. attach graph enrichments,
5. then layer in selective semantic retrieval.

This preserves optionality and keeps costs low.

## 5. Functional subsystems

A likely module decomposition:

### Ingestion
- arXiv metadata ingestion
- delta / checkpoint handling
- enrichment scheduling

### Canonical store
- papers
- content variants
- workflow state
- ranking runs and provenance

### Retrieval adapters
- lexical
- semantic
- graph
- metadata-first
- external-provider wrappers

### Ranking layer
- recency
- relevance
- popularity
- profile match
- novelty / diversity
- explanation assembly

### Content layer
- HTML acquisition
- source acquisition
- PDF parsing
- markdown / TEI / chunk generation
- caching + provenance

### MCP adapter
- tools
- resources
- prompts
- argument completion
- auth and identity model later

## 6. Cost-control principles

To keep costs low and architecture elegant:

- ingest metadata eagerly,
- enrich lazily,
- embed selectively,
- cache aggressively,
- separate candidate generation from expensive reranking,
- and keep heavy content conversion off the critical path unless explicitly requested.

## 7. Compute profiles

Given modest single-node hardware, the project should support several modes.

### Bronze
- metadata mirror
- lexical retrieval
- external graph enrichments on demand
- no local embeddings required

### Silver
- Bronze plus selective local embeddings
- recent/touched paper cohorts only
- lightweight vector retrieval or reranking

### Gold
- Silver plus content-normalization workers
- broader embedding coverage
- more sophisticated reranking and graph analytics

The repo should be designed so Bronze is fully useful and Silver/Gold are incremental upgrades.

## 8. Canonical retrieval pipeline hypothesis

A clean default pattern is:

1. **candidate generation**
   - lexical, graph, semantic, metadata, or feed-based

2. **constraint filtering**
   - time basis
   - category / topic / author / license / workflow state

3. **reranking**
   - objective-specific ranker

4. **diversification**
   - reduce redundancy where needed

5. **explanation assembly**
   - structured reasons and provenance

This pipeline keeps methods swappable without changing the whole system.

## 9. What this document deliberately does not decide

It does not yet decide:

- the vector database,
- the lexical engine,
- the final schema for interest profiles,
- the final content parser backend,
- or the final MCP surface.

Those should be informed by early experiments and implementation constraints.
