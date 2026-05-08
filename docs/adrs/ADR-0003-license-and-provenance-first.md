# ADR-0003 — License and provenance first

**Status:** Accepted  
**Date:** 2026-03-08

## Context

This project may ingest metadata, fetch content, convert PDFs, derive markdown, and incorporate external enrichments.

Those artifacts have different rights and provenance semantics.

arXiv permits broad metadata reuse but does not generally permit third-party redistribution of full e-prints unless paper-level rights allow it.

## Decision

We will treat rights and provenance as first-class across the system.

That means:

- every content artifact records source and acquisition path,
- every derived artifact records conversion backend and warnings,
- every ranking signal records provenance where practical,
- and hosted/public deployments are more conservative than local/private ones.

## Consequences

### Positive
- lower legal and operational risk,
- clearer trust model,
- easier auditing and debugging.

### Negative
- more metadata to store,
- slightly higher implementation overhead.

## Notes

This ADR is especially important because content normalization is a likely feature area.
