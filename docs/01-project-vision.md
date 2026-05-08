# Project Vision

**Status:** Draft  
**Date:** 2026-03-08

## Problem statement

arXiv continues to be a high-volume stream of papers, and the original arxiv-sanity family solved a real problem: it made that stream more legible by combining recent-paper monitoring, search, similarity, and explicit user taste signals. [S25][S26]

Today, the opportunity is broader.

Agents can now participate in research workflows, but most current scholarly MCP servers are still thin wrappers around search/download/fetch. They do not yet fully capture the richer discovery workflows, explicit state, and inspectability that made arxiv-sanity valuable. [S20][S21][S22][S23][S24][S40]

## Vision

Build an **MCP-native research discovery substrate** centered on arXiv, designed for agents and humans to:

- discover new papers,
- expand from seeds,
- track project-specific interests,
- maintain explicit interest state,
- inspect why a paper surfaced,
- and optionally obtain normalized content such as markdown.

This system should feel like a modern descendant of arxiv-sanity, not a generic “chat with papers” wrapper.

## Product thesis

The important thing to preserve from arxiv-sanity is **not** the website, TF-IDF, or tags as such.

The important thing to preserve is:

- recent-paper monitoring,
- explicit and steerable taste / interest modeling,
- fast exploration from seeds and queries,
- inspectability,
- and low-friction triage. [S25][S26]

## Goals

### Primary goals

1. **Preserve the product soul**
   - discovery over overload
   - explicit interest modeling
   - fast browsing and triage

2. **Support multiple discovery modes**
   - search
   - browse recent
   - find similar / related
   - recommend from interest state
   - get deltas since last check

3. **Support multiple retrieval and ranking families**
   - lexical
   - semantic
   - graph-based
   - metadata-first
   - hybrid and future approaches

4. **Make agent workflows first-class**
   - collections
   - triage states
   - watches
   - saved queries
   - structured explanations
   - provenance for machine-added state

5. **Provide optional content normalization**
   - metadata
   - abstract
   - snippets
   - markdown
   - structured content artifacts

6. **Keep the system elegant and affordable**
   - metadata-first
   - lazy enrichment
   - selective embeddings
   - local-first defaults

### Secondary goals

- support multiple clients over one shared core,
- keep open questions visible,
- reduce risk of architectural churn,
- remain licensing- and provenance-aware.

## Non-goals

At least initially, this project is **not** trying to become:

- a general-purpose paper chatbot,
- a giant all-literature warehouse before arXiv works well,
- a complex distributed system by default,
- an opaque recommender with hidden state,
- a benchmark leaderboards clone.

## Primary user types

### 1. Independent research agent
An agent that needs to search, expand, filter, triage, and monitor paper streams without relying on a web UI.

### 2. Human researcher using an MCP-capable client
A researcher who wants explicit controls and inspectable discovery rather than an opaque assistant.

### 3. Human + agent loop
A user who seeds interests, reviews shortlists, accepts or rejects suggestions, and lets agents perform repetitive monitoring and triage.

## User stories

### Discovery
- As a user, I can ask for newly announced papers in a domain and know whether “new” means announcement time, submission time, or update time.
- As a user, I can search by exact terms, authors, categories, or broader semantic intent.

### Expansion
- As a user, I can start from one or more seed papers and explore related work through multiple notions of relatedness.

### Interest state
- As a user, I can maintain an explicit interest profile without being forced into one single representation forever.
- As a user, I can see what signals define my current interest state and which ones were added by me, by an agent, or by the system.

### Workflow
- As a user, I can save a query or watch and ask “what changed since last time?”
- As an agent, I can batch-triage results into states like seen, shortlisted, dismissed, and follow-up.

### Content
- As a user, I can ask for metadata only, abstracts, snippets, or markdown depending on what is legally and technically available.

### Trust
- As a user, I can inspect why a result surfaced: lexical match, semantic similarity, graph relation, popularity signal, interest match, recency, or some combination.

## Key requirements

### Functional
- ingest arXiv metadata reliably,
- expose core discovery via MCP,
- support canonical paper objects,
- support explicit user / agent workflow state,
- support multiple retrieval strategies behind a common interface,
- support optional content conversion.

### Non-functional
- cost-aware,
- explainable,
- license-aware,
- provenance-aware,
- modular,
- easy to run locally for early development.

## Success criteria

### Product success
- It still feels like a discovery system, not a generic conversational layer.
- It can satisfy common discovery workflows without forcing a web interface.
- It supports explicit interest state and useful workflow state.

### Engineering success
- Multiple retrieval and ranking families can be compared without rewrites.
- Shared core logic serves all clients.
- Content handling and rights handling are not afterthoughts.

### Research success
- We can test multiple hypotheses about retrieval, ranking, interest representation, and agent workflow support using evidence rather than intuition.

## Initial posture

The first meaningful version of the project should be **small, sharp, and extensible**:

- metadata mirror,
- lexical baseline,
- explicit workflow state,
- seed expansion,
- recent feed / delta support,
- and a careful path to content normalization and semantic enrichment.

## References

See `11-sources.md`, especially [S1]-[S17], [S20]-[S40].
