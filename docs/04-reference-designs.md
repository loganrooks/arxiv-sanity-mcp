# Reference Designs

**Status:** Draft  
**Date:** 2026-03-08

This document surveys relevant systems and patterns.  
The purpose is to steal useful ideas, not to imitate any one product wholesale.

## 1. arxiv-sanity / arxiv-sanity-lite

### What they contributed
- recent-paper monitoring,
- explicit taste signals,
- similar-paper exploration,
- popularity / ranking views,
- low-friction browsing,
- inspectable recommendation logic. [S25][S26]

### What to preserve
- the sense that paper overload is a *product problem*,
- not just a search problem,
- and that user taste should remain explicit enough to inspect and steer.

### What not to freeze
- web-only interaction,
- TF-IDF as the final substrate,
- tag strings as the only interest representation.

## 2. Connected Papers

### Pattern
Graph-first exploration from a seed paper, with a force-directed similarity view. [S27]

### Lesson
A good discovery system should not only rank lists.
It should also support **neighborhood exploration**.

### Possible transplant
Provide a graph-oriented expansion operator or resource, even if there is no visual UI yet.

## 3. ResearchRabbit

### Pattern
Collections as workspaces; adaptive recommendations; author following; citation-map exploration. [S28][S29]

### Lesson
Collections are not just folders. They can be the context that powers better discovery.

### Possible transplant
Make “collection” or “workspace” a first-class workflow object for agents.

## 4. Litmaps

### Pattern
Citation-network discovery plus monitored searches and alerting. It emphasizes relevance from citation connections and recurring monitors on exact searches. [S30][S31][S32]

### Lesson
Monitoring should be based on explicit user intent objects, not just ad hoc repeated search calls.

### Possible transplant
Saved queries + watches + deltas should be first-class objects, not an afterthought.

## 5. Elicit

### Pattern
Question-centric literature workflows: multi-source search, screening criteria, extraction, and evidence-backed reports. [S33][S34]

### Lesson
Discovery is often only step 1.
A strong substrate should also help move from “find papers” to “screen, extract, and synthesize.”

### Possible transplant
Support structured downstream workflows such as:
- screening states,
- extraction-friendly content variants,
- and evidence-oriented prompts.

## 6. Scite

### Pattern
Citation-context-aware signals: supporting, contrasting, and mentioning citations, plus dashboards and alerts. [S35]

### Lesson
Raw citation count is often too blunt. Citation **context** is a meaningful quality signal.

### Possible transplant
Treat citation stance / context as an optional signal family for trust and ranking.

## 7. OpenAlex

### Pattern
Open knowledge-graph substrate: works, authors, institutions, topics, related works, content availability, snapshots, semantic search, and aboutness tagging. [S10][S11][S12][S13][S14][S15]

### Lesson
A strong open graph can act as a flexible enrichment layer rather than forcing us to invent all taxonomies ourselves.

### Possible transplant
Use OpenAlex as:
- graph enrichment,
- topic enrichment,
- entity resolution,
- and content availability metadata.

## 8. Semantic Scholar

### Pattern
API surface with citations, recommendations, datasets, and SPECTER2 embeddings. [S16][S17]

### Lesson
Scientific recommendations and embedding-based discovery are useful, but they are best treated as part of a broader discovery stack, not the whole product.

### Possible transplant
Use Semantic Scholar as an optional recommendation / relatedness / citation enrichment adapter.

## 9. Crossref and OpenCitations

### Pattern
Open metadata and open citation infrastructure. [S18][S19]

### Lesson
Journal and citation enrichments do not need to come from a single provider.

### Possible transplant
Keep external citation / metadata adapters modular.

## 10. Hugging Face Trending Papers / Papers with Code lineage

### Pattern
Community-driven “what is hot right now?” paper discovery, now tied to recent GitHub star activity. [S36]

### Lesson
“Popular” often lives outside the source repository itself.
It is usually an aggregate of external activity signals.

### Possible transplant
Treat “popular” as a pluggable ranker assembled from external signals, not an intrinsic arXiv property.

## 11. Existing scholarly MCP servers

There are already community MCP servers for arXiv, OpenAlex, Semantic Scholar, and multi-source scholarly search. Most of them focus on search, fetch, download, and lightweight analysis. [S24][S40]

### Lesson
The differentiator for this project should not be “there is an MCP wrapper.”
The differentiator should be:

- better discovery semantics,
- stronger workflow state,
- clearer explanations,
- better content normalization,
- and elegant cost-aware architecture.

## Synthesis

The landscape suggests three major product patterns:

1. **Discovery maps**  
   Connected Papers, ResearchRabbit, Litmaps

2. **Evidence workflows**  
   Elicit, Scite

3. **Open data substrates**  
   OpenAlex, Semantic Scholar, Crossref, OpenCitations

A strong arXiv Discovery MCP should probably combine all three layers:

- substrate quality,
- workflow support,
- and richer discovery affordances.
