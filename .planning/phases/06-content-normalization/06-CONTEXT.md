# Phase 6 Context: Content Normalization

**Date:** 2026-03-12
**Source:** Design docs (03, 05, 06, 07, 09, 10), ADR-0002/0003, Phase 5 validation findings, enrichment adapter codebase analysis, arxiv-scan ecosystem context

---

## Phase Character

Phases 1-4 built services. Phase 04.1 exposed them as MCP. Phase 5 validated with real data. Phase 6 returns to building — but with a validated MCP surface that constrains the design (new content tools must integrate cleanly with the existing 10-tool + 4-resource + 3-prompt surface), and with real validation evidence about what matters (abstracts were sufficient for the Phase 5 literature review — full text is for deep reading, not discovery).

This is also the most technically uncertain phase: PDF parsing quality varies wildly, arXiv HTML coverage is incomplete, source extraction requires LaTeX tooling, and rights-gating is a legal compliance concern. The plan should front-load uncertainty resolution (which backend works? what does arXiv HTML actually look like?) before committing to architecture.

---

## Pre-requisites

### Enrichment Schema Migration (must be applied before Phase 6)

The enrichment service is broken against the live database. Quick Task 1 (2026-03-11) changed the code to expect a composite PK `(arxiv_id, source_api)` on `paper_enrichments`, but migration 006 may not have been applied to the live database. The migration exists at `alembic/versions/006_enrichment_composite_pk.py` and is non-destructive.

**Action needed:** Run `alembic upgrade head` against the live database before Phase 6 begins. Verify with `arxiv-mcp enrich --arxiv-id 2504.09772`. This is a prerequisite, not a Phase 6 task — it's a pre-existing fix, not new work.

### Database with imported papers

Phase 5 imported 126/157 papers with triage states and a 10-signal interest profile. 31 papers failed due to arXiv API rate limiting (429 errors), including all 4 known false negatives. The import script is idempotent — re-running it will fill in missing papers if rate limiting allows. This dataset is the test bed for content normalization.

---

## What Already Exists to Build On

### Paper Model (db/models.py)

The Paper model already has fields relevant to Phase 6:
- `license_uri` (String 256) — populated from arXiv OAI-PMH `dc:rights`. This is the basis for rights-gating (CONT-06).
- `source` (String 32, default "oai_pmh") — acquisition provenance.
- `processing_tier` (Integer) — enum: METADATA_ONLY=0, FTS_INDEXED=1, ENRICHED=2, EMBEDDED=3, CONTENT_PARSED=4. Phase 6 promotes papers to tier 4 when content is parsed.
- `abstract` — stored as part of paper metadata. CONT-01 (abstract as default variant) is essentially already satisfied.

### Enrichment Adapter Pattern (enrichment/)

The enrichment subsystem provides the template for Phase 6:
- **Protocol:** `EnrichmentAdapter` defines `adapter_name` property + async methods (openalex.py)
- **Concrete adapter:** `OpenAlexAdapter` handles API communication, rate limiting, result parsing
- **Service orchestration:** `EnrichmentService` manages adapter selection, DB storage, cooldown, single/batch workflows
- **Storage table:** `PaperEnrichment` stores results with provenance (source_api, enriched_at, status, raw response JSONB)
- **Tier promotion:** Service promotes `processing_tier` on success

Phase 6 should follow this exact pattern: `ContentAdapter` protocol → concrete adapters (Marker, etc.) → `ContentService` orchestration → `ContentVariant` storage table → tier promotion to CONTENT_PARSED.

### MCP Patterns (mcp/)

- Tools use `@mcp.tool()` decorator, return dicts via `model_dump(mode='json')`
- Resources use `@mcp.resource()` with URI templates
- AppContext dataclass provides DI for all services
- `_get_app(ctx)` helper extracts AppContext from MCP Context
- All tools use `source="mcp"` for audit trail
- Error pattern: `{"error": "message"}` dicts on failure

### Rights Infrastructure

ADR-0003 ("License and provenance first") is settled. The paper model already stores `license_uri` from arXiv metadata. Phase 6 must check this field before serving full-text content.

Common arXiv licenses (from `license_uri` values):
- `http://arxiv.org/licenses/nonexclusive-distrib/1.0/` — arXiv non-exclusive license. Does NOT grant third-party redistribution rights. Most common.
- `http://creativecommons.org/licenses/by/4.0/` — CC BY. Free to share and adapt with attribution.
- `http://creativecommons.org/licenses/by-sa/4.0/` — CC BY-SA. Share-alike.
- `http://creativecommons.org/licenses/by-nc-sa/4.0/` — CC BY-NC-SA. Non-commercial share-alike.
- `http://creativecommons.org/licenses/by-nc-nd/4.0/` — CC BY-NC-ND. Most restrictive CC license.
- `http://creativecommons.org/publicdomain/zero/1.0/` — CC0. Public domain.

**For a local-only deployment (Logan's setup), rights-gating is simpler:** local caching of conversions for personal use is generally permissible. The rights check should still be implemented (so it works if the system is ever hosted), but in local mode it logs a warning rather than blocking access. This distinction is established in docs/07 §12.

---

## Content Variant Model Design

### Variant Types (from docs/05, docs/07, CONT-02)

Four content variant types, in acquisition priority order (CONT-04):

| Variant | Source | Availability | Quality | Effort |
|---------|--------|-------------|---------|--------|
| **abstract** | Already in Paper model | 100% of papers | High (author-written) | Zero (already stored) |
| **html** | arXiv HTML5 (`arxiv.org/html/{id}`) | ~60% of papers (post-Dec 2023, expanding) | High (structured, math preserved) | Low (HTTP fetch + cleanup) |
| **source_derived** | arXiv source (`arxiv.org/e-print/{id}`) | ~85% of papers (TeX source available) | High (if TeX parses cleanly) | High (LaTeX toolchain) |
| **pdf_markdown** | arXiv PDF (`arxiv.org/pdf/{id}`) | ~100% of papers | Variable (math/tables degrade) | Medium (parsing backend) |

### Recommended v1 Scope

**Build:** abstract (trivial — already done), html (moderate — HTTP fetch + sanitize), pdf_markdown (one parsing backend).

**Defer to v2:** source_derived (requires LaTeX toolchain — pandoc, latexmk, or custom extraction — high complexity for marginal quality gain over HTML when HTML is available). The interface should support it, but don't implement it in Phase 6.

**Rationale:** arXiv HTML is the highest-quality full-text source when available, and its coverage is expanding rapidly. PDF markdown is the universal fallback. Source-derived extraction adds complexity without proportional value gain for v1 — the acquisition priority order (CONT-04) means source is tried only when HTML is unavailable, and PDF covers the same gap with less toolchain complexity.

### Storage Design

New `content_variants` table (following PaperEnrichment pattern):

```
content_variants
├── arxiv_id (FK → papers, part of composite PK)
├── variant_type (VARCHAR — 'abstract', 'html', 'pdf_markdown', 'source_derived')
│                 (part of composite PK with arxiv_id)
├── content (TEXT — the actual content, markdown or HTML)
├── content_hash (VARCHAR 64 — SHA-256 of content, for change detection)
├── source_url (VARCHAR — where the content was fetched from)
├── backend (VARCHAR — 'arxiv_html', 'marker', 'docling', 'grobid', NULL for abstract)
├── backend_version (VARCHAR — version of parsing backend used)
├── extraction_method (VARCHAR — 'direct_fetch', 'pdf_parse', 'tex_extract')
├── license_uri (VARCHAR — copied from Paper at conversion time, for audit)
├── quality_warnings (JSONB — any quality issues detected during conversion)
├── fetched_at (TIMESTAMPTZ — when source was downloaded)
├── converted_at (TIMESTAMPTZ — when conversion completed)
└── INDEX on (arxiv_id, variant_type) — composite PK
```

**Why TEXT not filesystem:** For markdown/HTML content (typically 10-100KB per paper), TEXT column is simpler than filesystem management (no path handling, backup included in pg_dump, transactional consistency). PDF binaries should NOT be stored — fetch on demand, parse, store the markdown result. If storage becomes an issue with thousands of papers, revisit with a filesystem backend behind the same interface.

---

## Parsing Backend Selection

### Assessment (from docs/07 §10, ecosystem analysis)

| Backend | Language | Strengths | Weaknesses | GPU? |
|---------|----------|-----------|------------|------|
| **Marker** | Python | Fast PDF→markdown, good equations (texify), tables, code blocks | Less scholarly-specific than GROBID | Optional (CPU works) |
| **Docling** | Python | IBM-backed, good table/figure extraction, OCR, reading order | Newer, less battle-tested for scholarly PDFs | Optional |
| **GROBID** | Java | Best scholarly extraction, structured TEI/XML, metadata-aware | Java dependency, XML output needs conversion to markdown | No |

### Recommendation: Start with Marker

- **Python-native** — no Java dependency, integrates cleanly with the existing stack
- **Direct markdown output** — matches the target format without conversion
- **GPU-optional** — works on Logan's GTX 1080 Ti but also on CPU
- **Good equation handling** — critical for CS/ML/stats papers
- **Well-maintained** — VikParuchuri actively maintains it

Implement the `ContentAdapter` protocol so Docling and GROBID can be added later without changing the service or MCP layer. But for v1, Marker alone is sufficient.

### Adapter Protocol Design

```python
class ContentAdapter(Protocol):
    @property
    def adapter_name(self) -> str: ...

    async def convert(
        self,
        pdf_bytes: bytes,
        arxiv_id: str,
    ) -> ContentConversionResult: ...
```

Where `ContentConversionResult` is a Pydantic model with: `content` (str), `backend` (str), `backend_version` (str), `quality_warnings` (list[str]), `extraction_method` (str).

---

## Data Acquisition Strategy

### arXiv HTML Fetching

arXiv has been converting papers to HTML5 since December 2023 (ar5iv project). Available at `https://arxiv.org/html/{arxiv_id}`. Not all papers have HTML — need to handle 404 gracefully and fall back to PDF.

**Fetch strategy:**
1. HEAD request to `https://arxiv.org/html/{arxiv_id}` to check availability
2. If 200: GET the page, extract `<article>` content, sanitize (strip nav/header/footer)
3. If 404: fall through to PDF pipeline
4. Rate limit: respect arXiv's rate limiting (same as API — 1 req/s sustained)

**Quality considerations:** arXiv HTML preserves math as MathML/LaTeX, preserves structure (sections, figures, tables). It's the best available full-text format. Main issues: some papers have rendering artifacts, and very old papers (pre-2024) rarely have HTML.

### PDF Fetching + Parsing

Available at `https://arxiv.org/pdf/{arxiv_id}`. Universal fallback.

**Fetch strategy:**
1. Download PDF to temp file (don't store the binary permanently)
2. Run through Marker for markdown conversion
3. Store the resulting markdown in `content_variants`
4. Delete the temp PDF
5. Rate limit: same arXiv rate limiting applies

**Quality considerations:** PDF parsing quality depends heavily on the paper. Math-heavy papers degrade most. Tables are hit-or-miss. Marker is the best available option for general scholarly PDFs but won't be perfect. Quality warnings should be populated based on conversion confidence (Marker provides this).

### Acquisition Orchestration (CONT-04)

The `ContentService` should implement the priority chain:

```
get_or_create_variant(arxiv_id, preferred_variant=None):
    1. If abstract requested → return Paper.abstract (always available)
    2. If html requested or preferred_variant is None:
       a. Check content_variants table for cached html
       b. If not cached → try fetch arXiv HTML
       c. If HTML available → store, return
    3. If pdf_markdown requested or HTML unavailable:
       a. Check content_variants table for cached pdf_markdown
       b. If not cached → fetch PDF, run Marker, store result
       c. Return pdf_markdown
    4. Return best available variant with metadata about what it is
```

---

## Rights Enforcement Model (CONT-06)

### Design

```python
class RightsChecker:
    # Licenses that permit redistribution
    PERMISSIVE_LICENSES = {
        "http://creativecommons.org/licenses/by/4.0/",
        "http://creativecommons.org/licenses/by-sa/4.0/",
        "http://creativecommons.org/publicdomain/zero/1.0/",
    }

    # Licenses that restrict redistribution but allow personal use
    PERSONAL_USE_LICENSES = {
        "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "http://creativecommons.org/licenses/by-nc-sa/4.0/",
        "http://creativecommons.org/licenses/by-nc-nd/4.0/",
    }

    def check_access(self, license_uri: str, mode: str) -> AccessDecision:
        if mode == "local":
            # Local use: allow all, log restrictive licenses
            return AccessDecision(allowed=True, warning=...)
        elif mode == "hosted":
            # Hosted: only serve permissive licenses
            if license_uri in self.PERMISSIVE_LICENSES:
                return AccessDecision(allowed=True)
            return AccessDecision(allowed=False, reason=...)
```

**For v1 (local deployment):** Always allow content access but include the license in the response so the user/agent knows the rights basis. The `content_variants` table stores `license_uri` at conversion time for audit trail. This is ADR-0003 compliant — provenance tracked, rights respected in hosted mode, permissive in local mode.

**Implementation note:** Add a `deployment_mode` setting to config.py (default: "local"). The MCP `get_content_variant` tool checks this before serving.

---

## MCP Integration

### New Tool: `get_content_variant`

```python
@mcp.tool()
async def get_content_variant(
    ctx: Context,
    arxiv_id: str,
    variant: str = "best",  # "abstract", "html", "pdf_markdown", "best"
) -> dict:
    """Get paper content at the requested fidelity level.

    'best' tries HTML first, falls back to PDF markdown, always returns abstract.
    Returns content with provenance metadata (source, backend, license).
    """
```

This satisfies MCP-03. The tool returns a dict with: `arxiv_id`, `variant_type`, `content` (the text), `source_url`, `backend`, `license_uri`, `quality_warnings`, `converted_at`. If conversion fails or rights block access, returns `{"error": ...}` following the established pattern.

### Paper Resource Extension

The existing `paper://{arxiv_id}` composite resource should include a `content_variants` field listing available variants (variant_type + converted_at) without the full content. The agent can then use `get_content_variant` to fetch the actual content. This keeps the resource lightweight while informing the agent what's available.

### Tool Count Impact

Adding `get_content_variant` brings the total to 11 tools. Still within the MCP-07 heuristic of 5-10 (now 11, slightly over but justified — content is a core capability, not bloat). Update `test_tool_names.py` to expect 11.

---

## What NOT to Build in Phase 6

- **Source-derived extraction** (LaTeX toolchain) — defer to v2. Interface supports it, implementation deferred.
- **Section-aware chunking** — deferred. Marker produces section headers in markdown, but structured chunk storage/retrieval is a v2 feature for RAG/embedding workflows.
- **Semantic search / embeddings** — explicitly v2 per REQUIREMENTS.md (SEMA-01..04).
- **Content-based re-ranking** — full-text similarity belongs to semantic search, not content normalization.
- **BibTeX extraction from PDFs** — out of scope. BibTeX export from existing metadata is a potential quick task, not Phase 6.
- **Batch content conversion for entire corpus** — ADR-0002 says lazy. Convert on demand only.
- **Multi-backend comparison testing** — nice to have but not a Phase 6 success criterion. Start with Marker. Add backends later if quality is insufficient.
- **Content caching eviction** — premature optimization. Store all conversions. Deal with storage growth if/when it becomes an issue.

---

## Success Criteria Interpretation

From ROADMAP.md:

1. **"User can retrieve paper content as abstract (always available) or as richer variants (HTML, source-derived, PDF-derived markdown) when available"** — Abstract is already in Paper model. Implement HTML fetch + PDF→markdown conversion. Source-derived is optional (see "defer" above). The MCP tool `get_content_variant` is the retrieval interface.

2. **"Content variants are acquired in source-aware priority order (abstract then arXiv HTML then source then PDF) and each records its extraction method and conversion path"** — The `ContentService` implements the priority chain. Each `ContentVariant` row records `source_url`, `backend`, `extraction_method`, `backend_version`. Source step can be skipped in v1 implementation (interface exists, no adapter yet).

3. **"Multiple parsing backends (Docling, Marker, GROBID) work behind a common interface and can be swapped without changing the content API"** — Implement the `ContentAdapter` protocol. Ship Marker adapter. The protocol proves the interface is backend-agnostic. Docling/GROBID adapters can be added without changing `ContentService` or `get_content_variant`. CONT-05 is "chosen for now" — the common interface is the requirement, not all 3 backends shipping in v1.

4. **"Content serving refuses to return full-text for papers whose license does not permit it, with a clear explanation of why"** — `RightsChecker` with `deployment_mode` setting. In local mode: allow + warn. In hosted mode: block + explain. The explanation is in the response dict.

5. **"An MCP client can access paper content variants via get_content_variant tool"** — One new MCP tool. Returns content + provenance metadata.

---

## Phase 5 Friction Points Relevant to Phase 6

From the validation session (validation-log.md), issues that Phase 6 should be aware of but NOT try to fix (different scope):

- **Enrichment broken** → pre-requisite fix (apply migration 006), not Phase 6 scope
- **total_estimate always None** → pagination issue, not content-related
- **Seed provenance missing** → discovery tool issue, not content-related
- **Opaque triage errors** → error handling issue, not content-related

Phase 6 is content normalization only. Resist the temptation to fix unrelated friction points.

---

## Hardware Considerations

Logan's setup: GTX 1080 Ti (11GB VRAM), 32GB RAM, single node.

- **Marker GPU mode:** Works on GTX 1080 Ti. Significantly faster than CPU for PDF parsing (~2-5x). Use GPU when available, fall back to CPU.
- **Memory:** PDF parsing can be memory-intensive for long papers. Set a reasonable page limit (e.g., first 50 pages) to avoid OOM on textbooks accidentally included in the corpus.
- **Storage:** 126 papers × ~50KB average markdown ≈ 6MB. Even at 1000 papers, this is negligible. TEXT column in PostgreSQL is fine.
- **Rate limiting:** arXiv rate limits apply to HTML and PDF fetching. The existing `RateLimiter` pattern from enrichment should be reused. 1 request per 3 seconds is safe.

---

## Dependency on Other Project: arxiv-scan

The arxiv-scan continuation strategy (`/scratch/arxiv-scan/pipeline/continuation-strategy.md`) envisions content normalization feeding into:
- **Multi-lens evaluation** (feedback-loop-design.md Stage 2) — evaluation lenses need paper content to assess
- **Discovery expansion** — full-text search could improve false-negative detection

These are POST-Phase 6 workflows. Phase 6 should deliver the content infrastructure; downstream use is separate work.
