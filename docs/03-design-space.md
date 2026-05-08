# Design Space

**Status:** Draft  
**Date:** 2026-03-08

This document maps the main axes of the design space so we do not accidentally shrink the project into the first implementation that happens to work.

## 1. Product identity

Possible product centers of gravity:

- recent-paper discovery system,
- personalized triage and monitoring tool,
- related-work explorer,
- agent-usable research substrate,
- project-based reading workspace,
- evidence and synthesis assistant.

**Working stance:** the center of gravity should remain discovery, monitoring, and explicit interest modeling.

## 2. Corpus scope

Possible scopes:

- narrow arXiv categories,
- configurable arXiv subset,
- all arXiv,
- arXiv + metadata enrichments,
- arXiv + adjacent corpora,
- project-specific slices.

Questions:

- Is the system mainly for recent papers?
- Does historical backfill matter immediately?
- Is all-arXiv worth the complexity on day one?

## 3. Internal paper representation

Candidate representations:

- metadata only,
- sparse lexical vectors,
- dense embeddings,
- topic assignments,
- graph nodes and edges,
- content variants (HTML / source / PDF / XML / markdown),
- generated summaries or snippets,
- code / benchmark links,
- citation-context signals.

## 4. Retrieval families

Candidate retrieval families:

- fielded metadata search,
- lexical search,
- semantic search,
- citation-graph exploration,
- seed-based expansion,
- query-reformulation pipelines,
- staged hybrid retrieval,
- watch / delta retrieval.

Important: “lexical vs dense” is not the whole space.

## 5. Ranking families

Candidate ranking families:

- recency,
- lexical relevance,
- embedding similarity,
- graph centrality,
- citation count,
- citation velocity,
- code popularity,
- interest-profile relevance,
- diversity / novelty blends,
- multi-objective reranking.

The likely future is not one universal ranking mode, but several.

## 6. Interest representation

Candidate forms of explicit interest state:

- tags,
- weighted tags,
- seed paper sets,
- collections,
- followed authors,
- followed topics,
- saved searches,
- negative examples,
- project workspaces,
- learned-but-editable profiles.

**Working stance:** do not force the core system to treat tags as the only enduring abstraction.

## 7. Workflow state

Candidate workflow objects:

- collections,
- triage entries,
- saved queries,
- watches,
- checkpoints,
- dismissed / muted rules,
- session scopes,
- project workspaces,
- review queues.

A web interface can often hide these.
An MCP server usually cannot.

## 8. Explanation model

Possible explanation modes:

- structured metadata only,
- signal lists with weights,
- nearest seeds / exemplars,
- lexical highlights,
- graph-path explanations,
- generated natural-language explanations,
- provenance metadata,
- confidence scores.

**Working stance:** structured explanations should come first; prose explanations can be layered later.

## 9. Content normalization

Possible content sources and outputs:

- metadata only,
- abstract only,
- abstract + snippets,
- arXiv HTML,
- arXiv source extraction,
- OpenAlex GROBID XML / content URL,
- PDF parsing,
- markdown,
- TEI/XML,
- section-aware chunks,
- table / figure extraction.

Questions:

- When should we convert?
- What should be cached?
- What rights model applies to derived artifacts?

## 10. MCP surface shape

Possible shapes:

- search-centric,
- resource-centric,
- workflow-centric,
- profile-centric,
- batch-heavy,
- minimal tools + rich resources,
- rich prompts + a smaller tool set.

This should stay open until we test representative agent workflows.

## 11. Learning and adaptation

Possible adaptation modes:

- static heuristics,
- nightly recompute,
- lazy updates on touched papers,
- online preference updates,
- active-learning loops,
- machine suggestions requiring confirmation,
- continuously learned ranking.

## 12. Deployment profiles

Possible deployment profiles:

- fully local single-user,
- local + external metadata APIs,
- remote shared service,
- hybrid local/private + hosted enrichments.

## 13. First-principles constraints

Any design should be judged against these constraints:

- Does it preserve discovery as the product center?
- Does it remain steerable?
- Does it remain explainable?
- Is it license-aware?
- Is it cheap enough to run?
- Is it modular enough to compare alternatives?

## Working conclusion

The most useful architecture is one that supports experiments across:

- retrieval,
- ranking,
- interest modeling,
- workflow state,
- and content normalization

without treating any one current guess as the permanent boundary of the product.
