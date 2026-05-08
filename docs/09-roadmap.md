# Roadmap

**Status:** Draft  
**Date:** 2026-03-08

This roadmap is deliberately staged to preserve reversibility.

## Phase 0 — Repo bootstrap
- initialize docs
- define object vocabulary
- define ADR and experiment process
- define initial golden workflows
- scaffold repo for shared core + adapters + MCP layer

## Phase 1 — Metadata-first substrate
- arXiv metadata ingestion
- canonical paper model
- explicit time semantics
- lexical baseline
- recent feed / delta handling
- minimal workflow-state store

Deliverable:
- useful recent browsing and search over arXiv metadata

## Phase 2 — Workflow-state primitives
- collections
- triage states
- saved queries
- checkpoints / deltas
- basic explanations

Deliverable:
- an agent can run repeated discovery and triage loops without a web UI

## Phase 3 — Open enrichment adapters
- OpenAlex integration
- optional Semantic Scholar adapter
- optional Crossref / OpenCitations enrichment
- paper identity / external ID resolution
- related-work graph support

Deliverable:
- stronger seed expansion, graph exploration, and metadata enrichment

## Phase 4 — MCP v1
- small but meaningful MCP tool set
- canonical resources
- a few high-value prompts
- batch operations where clearly necessary

Deliverable:
- first external MCP interface suitable for real workflows

## Phase 5 — Content normalization
- content variant model
- HTML / source / PDF strategy
- multiple parsing backends
- provenance and warnings
- chunking for downstream use

Deliverable:
- markdown and structured content on demand where feasible

## Phase 6 — Semantic and hybrid experiments
- selective embeddings
- semantic retrieval
- hybrid candidate generation and reranking
- profile-driven recommendation experiments

Deliverable:
- comparative data on whether semantic or hybrid retrieval should become part of the core default

## Phase 7 — Hardening and refinement
- caching
- auth / user identity
- hosted vs local deployment policy
- operational observability
- more robust rate-limit handling
- more refined watch / digest workflows

## Phase 8 — Optional advanced directions
- citation-context signals
- code / benchmark / dataset linkages
- richer project workspaces
- collaborative workflows
- more advanced reranking

## Guidance for sequencing

The sequencing discipline is:

1. shared objects and metadata first,
2. workflow state second,
3. enrichments third,
4. semantic sophistication fourth.

That keeps the project useful early while preserving flexibility.
