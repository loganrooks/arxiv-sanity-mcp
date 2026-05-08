# Data Sources, Content, and Rights

**Status:** Draft  
**Date:** 2026-03-08

This document maps likely data sources and the rights / provenance constraints around them.

## 1. arXiv should remain the system of origin

arXiv should remain the authoritative source for:

- core paper identity,
- subject categories,
- submission / update / announcement semantics,
- source files,
- and hosted HTML when available. [S1][S4][S5][S6][S9]

Important facts:

- arXiv’s search API supports fielded search, Boolean composition, `submittedDate`, and sorting by `submittedDate` or `lastUpdatedDate`. [S1]
- Large result sets are constrained; for bulk metadata, arXiv recommends OAI-PMH. [S1][S3]
- OAI-PMH metadata updates nightly shortly after announcements. [S3][S10]
- RSS exposes `announce_type` and a license URI in `dc:rights`. [S4]
- arXiv now serves HTML for many papers, but not all papers. [S5]
- arXiv source files are downloadable via `/e-print/ID` and `/src/ID`. [S6]

## 2. arXiv rights constraints are non-negotiable

arXiv metadata is reusable, but full e-prints are subject to copyright and license restrictions. [S2][S7]

Important implications:

- Metadata reuse is broad and safe. [S2]
- The overwhelming majority of e-prints are under arXiv’s non-exclusive license, which does **not** automatically grant third-party redistribution rights. [S7]
- Any hosted/public service should be conservative about serving full text or derived full-text artifacts unless paper-level rights clearly allow it. [S2][S7]
- Rights metadata is available in OAI-PMH and RSS, not fully in the search API schema. [S4][S7]

## 3. arXiv does not provide “popular paper” as an official metric

arXiv does not track or publish per-paper public download stats and explicitly does not want to publish potentially misleading individual-paper stats. [S8]

Implication:
- “popular” must be a ranker we define ourselves using external and internal signals.

## 4. OpenAlex is the best open enrichment layer

OpenAlex contributes:

- open graph structure,
- disambiguated authors / institutions / sources,
- topics and keywords,
- related works,
- citation counts and yearly counts,
- content availability metadata,
- semantic search,
- autocomplete,
- and downloadable snapshots. [S10][S11][S12][S13][S14][S15]

Especially useful features:

- `primary_topic`, up to 3 `topics`, and AI-generated keywords. [S11][S12]
- `related_works` as a precomputed algorithmic relatedness signal. [S12]
- content availability metadata such as `has_content` and `content_url`, including possible GROBID XML. [S12]
- an experimental `/text` endpoint that can tag free text with topics/keywords/concepts. [S14]

Cautions:
- the `/text` endpoint is explicitly experimental and paid per request. [S14]
- OpenAlex semantic search is also bounded and not necessarily sufficient as a sole production search layer. [S13]

## 5. Semantic Scholar is a strong optional enrichment adapter

Semantic Scholar contributes:

- paper / author / citation metadata,
- recommendations,
- datasets,
- and SPECTER2 embeddings. [S16][S17]

This makes it a good optional adapter for:

- related-paper signals,
- embedding-based research experiments,
- and cross-checking graph / citation enrichments.

## 6. Crossref and OpenCitations widen the metadata and citation layer

Crossref contributes rich bibliographic metadata including license information, abstracts when deposited, and related metadata fields. [S18]

OpenCitations contributes an open citation graph API. [S19]

These are useful when we want:
- broader citation coverage,
- DOI-based enrichment,
- or more open alternatives to proprietary citation layers.

## 7. External popularity signals should stay optional and pluggable

Potential popularity signals include:

- citation velocity,
- code popularity,
- community saves,
- watchlist inclusion,
- GitHub activity linked to papers,
- and trend feeds.

For example, Hugging Face’s Trending Papers ranks papers using recent GitHub star activity. [S36]

This is a useful signal family, but it should remain:
- external,
- optional,
- and clearly labeled as such.

## 8. Existing scholarly MCP servers confirm the gap

Community scholarly MCP servers already exist for arXiv, OpenAlex, Semantic Scholar, and multi-source paper search. [S24][S40]

They are useful references, but they also show that:
- simple search/fetch/download is already commoditized,
- and the real opportunity is stronger semantics, workflow state, explanation, and rights-aware content handling.

## 9. Content variant strategy

A good content strategy should be source-aware.

### Preferred acquisition order
1. **Abstract only**  
   safest and cheapest default

2. **arXiv HTML**  
   best structured option when available

3. **arXiv source-derived extraction**  
   often stronger than PDF when the source is clean

4. **OpenAlex content URL / GROBID XML when available**  
   strong structured fallback for some works

5. **PDF parsing**  
   most universal, but least trustworthy and most expensive

## 10. PDF-to-markdown backends worth supporting

### Docling
Good general structured document processing with tables, formulas, reading order, OCR, and downstream AI-oriented structured output. [S37]

### Marker
Direct markdown / JSON output; good support for equations, tables, code blocks, and images. Works on GPU or CPU. [S38]

### GROBID
Strong scholarly PDF extraction to structured TEI/XML. Excellent as a machine-readable intermediate representation. [S39]

**Working hypothesis:** support multiple backends behind one content-normalization interface.

## 11. Provenance model requirements

Every content artifact should record:

- source system,
- source URL / identifier,
- acquisition timestamp,
- license / rights basis if known,
- conversion path,
- backend used,
- confidence / warnings,
- and cache status.

## 12. Local vs hosted behavior

### Local/private mode
Can be more permissive about local caching and on-demand full-text conversion, as long as access stays within the user’s environment and terms are respected.

### Hosted/public mode
Should default to:
- metadata,
- abstracts,
- snippets,
- links,
- and full text only where reuse rights clearly permit it.

## Working conclusion

The data strategy should be:

- **arXiv as source of origin**
- **OpenAlex as open enrichment graph**
- **Semantic Scholar as optional recommendations / embedding adapter**
- **Crossref and OpenCitations as optional DOI / citation enrichers**
- **content normalization as provenance-aware multi-backend transformation**
