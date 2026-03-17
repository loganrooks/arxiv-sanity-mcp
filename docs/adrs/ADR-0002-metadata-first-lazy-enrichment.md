# ADR-0002 — Metadata-first, lazy enrichment

**Status:** Accepted  
**Date:** 2026-03-08

## Context

Embeddings, PDF parsing, and external enrichments can all improve quality, but they also increase cost, latency, and operational complexity.

The project explicitly values elegance and low cost.

## Decision

We will begin with:

- eager metadata ingestion,
- strong metadata and lexical workflows,
- and lazy / selective enrichment for:
  - embeddings,
  - graph enrichments,
  - content conversion,
  - and external popularity signals.

## Consequences

### Positive
- cheap baseline,
- fast to stand up,
- easier to reason about,
- better fit for local-first deployments.

### Negative
- semantic and content-rich features may lag slightly behind the metadata substrate,
- some discovery modes may initially be weaker than the eventual target state.

## Notes

This does not prohibit broader enrichment later.
It only sets the early default posture.
