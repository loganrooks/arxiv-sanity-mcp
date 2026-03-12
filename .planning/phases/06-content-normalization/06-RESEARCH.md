# Phase 6: Content Normalization - Research

**Researched:** 2026-03-12
**Domain:** PDF/HTML content acquisition, parsing, rights-gating, MCP integration
**Confidence:** HIGH

## Summary

Phase 6 adds content normalization to the existing arxiv-mcp system: acquiring paper content at multiple fidelity levels (abstract, arXiv HTML, PDF-derived markdown), storing variants with provenance metadata, enforcing license-based access rights, and exposing content via a new MCP tool. The phase follows established patterns from the enrichment subsystem (Phase 4) -- adapter protocol, service orchestration, DB storage, tier promotion -- applied to a new domain.

The primary technical challenge is PDF-to-markdown conversion quality, which varies by paper. Marker v1.10.2 is the recommended parsing backend: Python-native, direct markdown output, GPU-optional, well-maintained. arXiv HTML (via LaTeXML) provides higher-quality full text when available (new papers since Dec 2023, expanding coverage). The content adapter protocol allows swapping or adding backends (Docling, GROBID) without changing the service or MCP layer.

**Primary recommendation:** Follow the enrichment adapter pattern exactly. Implement abstract (trivial), arXiv HTML fetch, and Marker-based PDF-to-markdown. Defer source-derived (LaTeX) extraction to v2. Use `asyncio.to_thread()` to wrap Marker's synchronous PDF conversion for async compatibility.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **v1 scope:** Build abstract (trivial), HTML (fetch + sanitize), pdf_markdown (one backend). Defer source_derived to v2.
- **Start with Marker** as the PDF parsing backend. Implement ContentAdapter protocol so Docling/GROBID can be added later.
- **Storage:** New `content_variants` table with TEXT column for content (not filesystem). Composite PK (arxiv_id, variant_type).
- **Rights model:** RightsChecker with deployment_mode setting. Local mode: allow + warn. Hosted mode: block + explain. ADR-0003 compliant.
- **MCP tool:** Single `get_content_variant` tool. Returns content + provenance metadata. "best" variant tries HTML first, falls back to PDF markdown.
- **Lazy acquisition per ADR-0002:** Convert on demand only, no batch conversion.
- **Follow enrichment adapter pattern:** ContentAdapter protocol -> concrete adapters -> ContentService orchestration -> ContentVariant storage -> tier promotion to CONTENT_PARSED.
- **arXiv HTML URL:** `https://arxiv.org/html/{arxiv_id}` (verified against live arXiv abstract pages).
- **Rate limiting:** Reuse existing RateLimiter pattern from enrichment. 1 request per 3 seconds for arXiv.
- **Paper resource extension:** Add `content_variants` field listing available variants (type + converted_at) without full content.

### Claude's Discretion
- HTML sanitization strategy (BeautifulSoup vs lxml vs regex)
- Marker configuration details (GPU/CPU detection, page limits, model initialization)
- ContentConversionResult Pydantic model field details
- Test fixture design for content module
- CLI subcommand structure for content operations
- Quality warning detection heuristics

### Deferred Ideas (OUT OF SCOPE)
- Source-derived extraction (LaTeX toolchain) -- interface supports it, implementation deferred to v2
- Section-aware chunking for RAG/embedding workflows
- Semantic search / embeddings (SEMA-01..04)
- Content-based re-ranking
- BibTeX extraction from PDFs
- Batch content conversion for entire corpus
- Multi-backend comparison testing
- Content caching eviction
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CONT-01 | System provides abstract as default content variant | Abstract already stored in Paper.abstract. ContentService returns it directly. Zero effort. |
| CONT-02 | System models content variants explicitly: abstract, HTML, source-derived, PDF-derived markdown | ContentVariant ORM model with variant_type discriminator. All 4 types in model, only 3 implemented in v1. |
| CONT-03 | Content variants record provenance: source, extraction method, conversion path, license basis | ContentVariant table stores source_url, backend, backend_version, extraction_method, license_uri, content_hash. |
| CONT-04 | Content variant acquisition follows source-aware priority | ContentService.get_or_create_variant implements: abstract -> HTML -> (source, skip in v1) -> PDF. |
| CONT-05 | Multiple parsing backends behind common interface | ContentAdapter protocol (adapter_name + convert method). Marker adapter ships. Protocol proves interface extensibility. |
| CONT-06 | Content serving respects per-paper license restrictions | RightsChecker with deployment_mode. Uses Paper.license_uri. Local: allow+warn. Hosted: block+explain. |
| MCP-03 | MCP server exposes content tools: get_content_variant | New @mcp.tool() following existing patterns. Returns content + provenance dict. |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| marker-pdf | 1.10.2 | PDF to markdown conversion | Python-native, direct markdown output, GPU-optional, best equation handling, actively maintained |
| httpx | >=0.28 (already installed) | arXiv HTML fetching | Already used project-wide for HTTP; async-native |
| beautifulsoup4 | 4.x | HTML content extraction/sanitization | Standard HTML parsing, already available via lxml dependency |
| lxml | >=5.3 (already installed) | HTML parser backend for BeautifulSoup | Already a project dependency; fast, handles malformed HTML |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| SQLAlchemy | >=2.0 (already installed) | ContentVariant ORM model + migration | Core data layer, existing pattern |
| Alembic | >=1.14 (already installed) | Migration 008 for content_variants table | Schema evolution, existing pattern |
| Pydantic | >=2.10 (already installed) | ContentConversionResult, RightsChecker models | Validation and serialization, existing pattern |
| structlog | >=24.4 (already installed) | Logging throughout content module | Existing project logger |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Marker | Docling (IBM) | Better table/figure extraction but newer, less battle-tested for scholarly PDFs. Add as second adapter later. |
| Marker | GROBID | Best scholarly metadata extraction but Java dependency, XML output needs markdown conversion. Heavy for this use case. |
| BeautifulSoup | selectolax/lxml.html | Faster but less forgiving with malformed HTML. BS4 is safer for unpredictable arXiv HTML. |
| TEXT column | Filesystem storage | More scalable at very high paper counts but adds path management, backup complexity, transaction issues. TEXT is fine for expected scale (hundreds to low thousands of papers). |

**Installation:**
```bash
pip install marker-pdf beautifulsoup4
```

**Note:** `marker-pdf` pulls in PyTorch and several ML model dependencies. First install will download model weights (~1-2GB). The `beautifulsoup4` package is lightweight. Both are compatible with Python 3.13.

## Architecture Patterns

### Recommended Project Structure
```
src/arxiv_mcp/
├── content/                    # NEW: content normalization module
│   ├── __init__.py
│   ├── models.py              # ContentConversionResult, ContentStatus, RightsDecision Pydantic models
│   ├── adapters.py            # ContentAdapter protocol + MarkerAdapter implementation
│   ├── html_fetcher.py        # arXiv HTML fetch + sanitize logic
│   ├── rights.py              # RightsChecker with license classification
│   ├── service.py             # ContentService orchestration (get_or_create_variant, priority chain)
│   └── cli.py                 # CLI subcommands (arxiv-mcp content get, content status)
├── mcp/
│   └── tools/
│       └── content.py         # NEW: get_content_variant MCP tool
├── db/
│   └── models.py              # EXTEND: add ContentVariant ORM model
└── config.py                  # EXTEND: add deployment_mode, content settings
```

### Pattern 1: ContentAdapter Protocol (mirrors EnrichmentAdapter)
**What:** Protocol class defining the interface for PDF parsing backends
**When to use:** Every parsing backend implements this protocol
**Example:**
```python
# Source: Codebase pattern from enrichment/openalex.py
from typing import Protocol

class ContentAdapter(Protocol):
    @property
    def adapter_name(self) -> str: ...

    async def convert(
        self,
        pdf_path: str,
        arxiv_id: str,
    ) -> ContentConversionResult: ...
```

### Pattern 2: Service Orchestration (mirrors EnrichmentService)
**What:** ContentService manages adapter selection, DB storage, priority chain, and tier promotion
**When to use:** All content operations go through this service
**Example:**
```python
# Source: Codebase pattern from enrichment/service.py
class ContentService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        adapter=None,  # DI for testing (MockAdapter)
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.adapter = adapter or MarkerAdapter(settings)
```

### Pattern 3: Async Wrapper for Synchronous Marker
**What:** Marker's PdfConverter is synchronous. Wrap with asyncio.to_thread() for async compatibility.
**When to use:** MarkerAdapter.convert() method
**Example:**
```python
import asyncio
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

class MarkerAdapter:
    def __init__(self, settings: Settings) -> None:
        # Initialize models once, reuse across conversions
        self._converter = PdfConverter(artifact_dict=create_model_dict())

    async def convert(self, pdf_path: str, arxiv_id: str) -> ContentConversionResult:
        # Offload blocking conversion to thread pool
        rendered = await asyncio.to_thread(self._converter, pdf_path)
        text, _, images = text_from_rendered(rendered)
        return ContentConversionResult(
            content=text,
            backend="marker",
            backend_version=self._get_version(),
            extraction_method="pdf_parse",
            quality_warnings=self._detect_warnings(text),
        )
```

### Pattern 4: MCP Tool Registration (mirrors enrichment.py)
**What:** Single tool file with `_get_app()` helper, `@mcp.tool()` decorator, dict return
**When to use:** The `get_content_variant` tool
**Example:**
```python
# Source: Codebase pattern from mcp/tools/enrichment.py
from arxiv_mcp.mcp.server import AppContext, mcp

def _get_app(ctx: Context) -> AppContext:
    return ctx.request_context.lifespan_context

@mcp.tool()
async def get_content_variant(
    arxiv_id: str,
    variant: str = "best",
    ctx: Context = None,
) -> dict:
    """Get paper content at the requested fidelity level."""
    app = _get_app(ctx)
    # ... rights check, service call, return dict
```

### Anti-Patterns to Avoid
- **Storing PDF binaries in the database:** Download PDFs to temp files, parse, store the markdown, delete the PDF. Never persist raw PDFs in PostgreSQL.
- **Eagerly converting all papers:** ADR-0002 mandates lazy enrichment. Convert on demand only when get_content_variant is called.
- **Blocking the event loop with Marker:** Marker's PdfConverter is CPU/GPU-bound and synchronous. Always wrap with `asyncio.to_thread()`.
- **Tight coupling to Marker internals:** All Marker interaction goes through MarkerAdapter. Service and MCP layers never import from `marker` directly.
- **Ignoring arXiv rate limits:** Both HTML and PDF fetching hit arXiv servers. Reuse the existing RateLimiter class at 1 req/3s.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| PDF to markdown | Custom PDF parser | marker-pdf PdfConverter | Equation handling, table detection, layout analysis are solved problems. Custom is worse. |
| HTML content extraction | Regex-based HTML parsing | BeautifulSoup4 with lxml parser | HTML is not regular. BS4 handles malformed HTML, encoding issues, entity decoding. |
| Rate limiting | Custom sleep/counter logic | Existing RateLimiter class from enrichment/openalex.py | Already battle-tested in the codebase. Monotonic clock + asyncio.sleep. |
| License classification | Ad-hoc string matching | Dedicated RightsChecker class with explicit license sets | License URIs have specific formats. Central authority prevents scattered checks. |
| Content hashing | Manual hash computation | hashlib.sha256 | Standard library, no dependency needed. Used for change detection on re-fetch. |

**Key insight:** The enrichment subsystem (Phase 4) already solved the adapter + service + DB storage + tier promotion pattern. Phase 6 is applying the same architecture to a new domain (content), not inventing new patterns.

## Common Pitfalls

### Pitfall 1: Marker Model Initialization Latency
**What goes wrong:** Creating a new PdfConverter for every conversion triggers model loading (~5-10 seconds and ~2GB memory).
**Why it happens:** `create_model_dict()` downloads/loads PyTorch models on first call.
**How to avoid:** Initialize PdfConverter once in MarkerAdapter.__init__ and reuse across conversions. This is why the adapter holds state.
**Warning signs:** First conversion takes 10+ seconds. Multiple model loads in logs.

### Pitfall 2: arXiv HTML URL Returns 404 vs Missing HTML
**What goes wrong:** Assuming 404 means "paper doesn't exist" when it means "HTML not generated."
**Why it happens:** arXiv only generates HTML for papers submitted after Dec 2023 with TeX source. Older papers or non-TeX submissions get 404.
**How to avoid:** HEAD request first. If 404, fall through to PDF pipeline silently. Log at debug level, not warning.
**Warning signs:** Mass "paper not found" warnings when processing older papers.

### Pitfall 3: Blocking Event Loop During PDF Conversion
**What goes wrong:** Marker conversion takes 5-60 seconds per paper (CPU-bound). Calling it synchronously blocks the entire async event loop.
**Why it happens:** PdfConverter is synchronous, uses PyTorch internally.
**How to avoid:** Always use `asyncio.to_thread(converter, pdf_path)` to offload to thread pool.
**Warning signs:** MCP server becomes unresponsive during content conversion. Other tools time out.

### Pitfall 4: arXiv Rate Limiting (429 Responses)
**What goes wrong:** Rapid HTML+PDF fetching triggers arXiv rate limits, causing 429 errors or IP bans.
**Why it happens:** Content acquisition may issue multiple requests per paper (HEAD for HTML, GET for HTML or PDF).
**How to avoid:** Use the existing RateLimiter at 1 req/3s. Share the rate limiter across HTML and PDF fetching.
**Warning signs:** 429 responses in logs. Subsequent requests failing.

### Pitfall 5: Memory Exhaustion on Large PDFs
**What goes wrong:** Marker loads entire PDF into memory. Textbook-length PDFs (500+ pages) can OOM.
**Why it happens:** Some arXiv "papers" are actually book-length documents.
**How to avoid:** Set a page limit (e.g., first 100 pages). Marker supports `max_pages` configuration. Add quality warning when truncated.
**Warning signs:** Process killed by OOM killer. Memory spikes during conversion.

### Pitfall 6: Missing license_uri on Paper Records
**What goes wrong:** RightsChecker gets None for license_uri and either crashes or silently allows.
**Why it happens:** Some papers ingested without OAI-PMH dc:rights field.
**How to avoid:** Treat missing license as "unknown" -- restrictive in hosted mode, permissive in local mode with warning.
**Warning signs:** NoneType errors in rights checking. Papers served without license audit.

## Code Examples

Verified patterns from the existing codebase:

### ContentVariant ORM Model
```python
# Source: Codebase pattern from db/models.py PaperEnrichment
class ContentVariant(Base):
    __tablename__ = "content_variants"

    arxiv_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("papers.arxiv_id", ondelete="CASCADE"),
    )
    variant_type: Mapped[str] = mapped_column(String(32))
    content: Mapped[str] = mapped_column(Text)
    content_hash: Mapped[str] = mapped_column(String(64))
    source_url: Mapped[str | None] = mapped_column(String(512))
    backend: Mapped[str | None] = mapped_column(String(32))
    backend_version: Mapped[str | None] = mapped_column(String(32))
    extraction_method: Mapped[str | None] = mapped_column(String(32))
    license_uri: Mapped[str | None] = mapped_column(String(256))
    quality_warnings: Mapped[dict | None] = mapped_column(JSONB)
    fetched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    converted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        PrimaryKeyConstraint("arxiv_id", "variant_type", name="content_variants_pkey"),
        CheckConstraint(
            "variant_type IN ('abstract', 'html', 'source_derived', 'pdf_markdown')",
            name="ck_content_variant_type_valid",
        ),
        Index("idx_content_variants_arxiv_id", "arxiv_id"),
    )
```

### RightsChecker
```python
# Source: CONTEXT.md design specification
class RightsChecker:
    PERMISSIVE_LICENSES = {
        "http://creativecommons.org/licenses/by/4.0/",
        "http://creativecommons.org/licenses/by-sa/4.0/",
        "http://creativecommons.org/publicdomain/zero/1.0/",
    }

    PERSONAL_USE_LICENSES = {
        "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        "http://creativecommons.org/licenses/by-nc-sa/4.0/",
        "http://creativecommons.org/licenses/by-nc-nd/4.0/",
    }

    def check_access(self, license_uri: str | None, deployment_mode: str) -> AccessDecision:
        if deployment_mode == "local":
            return AccessDecision(allowed=True, warning=self._local_warning(license_uri))
        # Hosted mode
        if license_uri in self.PERMISSIVE_LICENSES:
            return AccessDecision(allowed=True)
        return AccessDecision(
            allowed=False,
            reason=f"License '{license_uri}' does not permit redistribution"
        )
```

### arXiv HTML Fetching
```python
# Source: Verified against live arxiv.org abstract pages
import httpx
from bs4 import BeautifulSoup

async def fetch_arxiv_html(
    arxiv_id: str,
    client: httpx.AsyncClient,
    rate_limiter: RateLimiter,
) -> str | None:
    url = f"https://arxiv.org/html/{arxiv_id}"
    await rate_limiter.acquire()

    # HEAD first to check availability
    head_resp = await client.head(url, follow_redirects=True)
    if head_resp.status_code == 404:
        return None  # No HTML available, fall through to PDF

    await rate_limiter.acquire()
    resp = await client.get(url, follow_redirects=True)
    resp.raise_for_status()

    # Extract article content, strip navigation/header/footer
    soup = BeautifulSoup(resp.text, "lxml")
    # arXiv HTML uses <article> or <main> container
    article = soup.find("article") or soup.find("main") or soup.find("body")
    if article is None:
        return None

    # Remove nav, header, footer elements
    for tag in article.find_all(["nav", "header", "footer"]):
        tag.decompose()

    return str(article)
```

### Marker PDF Conversion (Async Wrapper)
```python
# Source: Marker v1.10.2 API (PyPI, GitHub README)
import asyncio
import tempfile
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

class MarkerAdapter:
    adapter_name = "marker"

    def __init__(self, settings: Settings) -> None:
        self._converter = PdfConverter(artifact_dict=create_model_dict())

    async def convert(self, pdf_path: str, arxiv_id: str) -> ContentConversionResult:
        rendered = await asyncio.to_thread(self._converter, pdf_path)
        text, _, images = text_from_rendered(rendered)
        return ContentConversionResult(
            content=text,
            backend="marker",
            backend_version=self._get_version(),
            extraction_method="pdf_parse",
            quality_warnings=self._detect_warnings(text, rendered),
        )
```

### MockAdapter for Testing
```python
# Source: Codebase pattern from tests/test_enrichment/test_service.py MockAdapter
class MockContentAdapter:
    adapter_name = "mock_marker"

    def __init__(self, results: dict[str, ContentConversionResult] | None = None):
        self._results = results or {}
        self.convert_calls: list[tuple[str, str]] = []

    async def convert(self, pdf_path: str, arxiv_id: str) -> ContentConversionResult:
        self.convert_calls.append((pdf_path, arxiv_id))
        if arxiv_id in self._results:
            return self._results[arxiv_id]
        return ContentConversionResult(
            content="# Mock Paper Content\n\nThis is mock converted text.",
            backend="mock_marker",
            backend_version="0.0.0",
            extraction_method="pdf_parse",
            quality_warnings=[],
        )
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| ar5iv (separate service) | arxiv.org/html/ (native) | Dec 2023 | HTML now served from arxiv.org directly, expanding coverage |
| Marker CLI-only | Marker Python API (PdfConverter) | 2024 | Programmatic conversion without subprocess calls |
| Single PDF parser | Multi-backend adapter pattern | Industry trend | Common interface enables backend swapping without API changes |
| Store PDFs in DB | Fetch-parse-discard | Best practice | PDFs are large, derived markdown is the value, not the binary |

**Deprecated/outdated:**
- `ar5iv.labs.arxiv.org` as primary HTML source: arXiv now serves HTML natively at `arxiv.org/html/`. ar5iv still exists as a dataset but arXiv's native HTML is the canonical source.
- Marker CLI (`marker_single`, `marker`): Still works but the Python API (`PdfConverter`) is preferred for programmatic use.

## Open Questions

1. **Marker VRAM usage on GTX 1080 Ti**
   - What we know: Marker supports GPU acceleration via PyTorch and the GTX 1080 Ti has 11GB VRAM.
   - What is unclear: Exact VRAM consumption during scholarly PDF conversion (model size + inference overhead).
   - Recommendation: Start with GPU mode (`TORCH_DEVICE=cuda`). If VRAM issues arise, fall back to CPU or set environment variable. Add try/except around GPU initialization.

2. **arXiv HTML content structure consistency**
   - What we know: LaTeXML generates the HTML. Verified one paper has `<article>` structure with sections, math, figures.
   - What is unclear: Whether all arXiv HTML papers use identical structure or if there are variations by submission type.
   - Recommendation: Build flexible extraction (try `<article>`, fall back to `<main>`, then `<body>`). Add quality warnings for unexpected structure. Test against 5-10 diverse papers during implementation.

3. **Marker PdfConverter accepts file path only (not bytes)**
   - What we know: API examples show `converter("FILEPATH")` with string path argument.
   - What is unclear: Whether BytesIO or bytes input is supported directly.
   - Recommendation: Use temp file approach: download PDF to `tempfile.NamedTemporaryFile`, pass path to Marker, delete after conversion. This is the safest, most compatible approach.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `python -m pytest tests/test_content/ -x -q` |
| Full suite command | `python -m pytest tests/ -x -q` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CONT-01 | Abstract returned as default variant | unit | `python -m pytest tests/test_content/test_service.py::test_get_abstract_variant -x` | Wave 0 |
| CONT-02 | Content variants modeled (4 types) | unit | `python -m pytest tests/test_content/test_models.py -x` | Wave 0 |
| CONT-03 | Provenance fields populated on conversion | unit | `python -m pytest tests/test_content/test_service.py::test_provenance_fields -x` | Wave 0 |
| CONT-04 | Priority order: abstract -> HTML -> PDF | unit | `python -m pytest tests/test_content/test_service.py::test_acquisition_priority -x` | Wave 0 |
| CONT-05 | MockAdapter satisfies ContentAdapter protocol | unit | `python -m pytest tests/test_content/test_adapter.py -x` | Wave 0 |
| CONT-06 | Rights check blocks in hosted mode, warns in local | unit | `python -m pytest tests/test_content/test_rights.py -x` | Wave 0 |
| MCP-03 | get_content_variant tool returns content dict | unit | `python -m pytest tests/test_mcp/test_content_tool.py -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `python -m pytest tests/test_content/ -x -q`
- **Per wave merge:** `python -m pytest tests/ -x -q`
- **Phase gate:** Full suite green (target: 403+ existing tests pass + new content tests)

### Wave 0 Gaps
- [ ] `tests/test_content/__init__.py` -- package init
- [ ] `tests/test_content/conftest.py` -- shared fixtures (content_session_factory, mock adapter)
- [ ] `tests/test_content/test_models.py` -- ContentConversionResult, ContentStatus Pydantic model tests
- [ ] `tests/test_content/test_adapter.py` -- MarkerAdapter protocol compliance, MockAdapter
- [ ] `tests/test_content/test_rights.py` -- RightsChecker with all license types, both deployment modes
- [ ] `tests/test_content/test_service.py` -- ContentService orchestration, priority chain, DB storage, tier promotion
- [ ] `tests/test_mcp/test_content_tool.py` -- get_content_variant MCP tool with mock services
- [ ] Update `tests/test_mcp/test_tool_names.py` -- expect 11 tools, include "get_content_variant"

## Sources

### Primary (HIGH confidence)
- Codebase analysis: `enrichment/service.py`, `enrichment/openalex.py`, `enrichment/models.py` -- adapter pattern, service orchestration, mock testing
- Codebase analysis: `db/models.py` -- Paper model (license_uri, processing_tier), PaperEnrichment (composite PK pattern)
- Codebase analysis: `mcp/server.py`, `mcp/tools/enrichment.py`, `mcp/resources/paper.py` -- AppContext, tool registration, resource composition
- Codebase analysis: `config.py` -- Settings pattern for new configuration values
- Codebase analysis: `tests/test_enrichment/test_service.py`, `tests/test_enrichment/conftest.py` -- MockAdapter pattern, session_factory fixture
- PyPI: marker-pdf v1.10.2 (verified 2026-03-12) -- version, Python API, dependencies
- arXiv abstract page (verified): HTML link at `https://arxiv.org/html/{arxiv_id}` confirmed on live arxiv.org
- arXiv HTML paper (verified): `https://arxiv.org/html/2312.06599v1` -- LaTeXML-generated, article structure, math preserved

### Secondary (MEDIUM confidence)
- [arXiv blog (Dec 2023)](https://blog.arxiv.org/2023/12/21/accessibility-update-arxiv-now-offers-papers-in-html-format/) -- HTML launch announcement, coverage expanding
- [arXiv accessible HTML info](https://info.arxiv.org/about/accessible_HTML.html) -- LaTeXML conversion, not all papers have HTML
- [Marker GitHub](https://github.com/datalab-to/marker) -- PdfConverter API, create_model_dict(), text_from_rendered()
- [Marker PyPI](https://pypi.org/project/marker-pdf/) -- v1.10.2, Python 3.10-3.14 support

### Tertiary (LOW confidence)
- Marker VRAM requirements on GTX 1080 Ti -- no specific documentation found, needs empirical validation
- arXiv HTML coverage percentage (~60% for new papers) -- CONTEXT.md estimate, not verified with official data

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - marker-pdf verified on PyPI, existing deps confirmed in pyproject.toml
- Architecture: HIGH - directly follows enrichment adapter pattern already proven in codebase
- Pitfalls: HIGH - based on documented Marker behavior and observed arXiv HTML patterns
- Rights model: HIGH - license URIs verified against sample_paper_data fixture and CONTEXT.md analysis
- arXiv HTML URL: HIGH - verified against live arxiv.org abstract page link

**Research date:** 2026-03-12
**Valid until:** 2026-04-12 (30 days -- stable domain, Marker version may update)
