"""ContentService: orchestrates content acquisition, conversion, and storage.

Implements the source-aware priority chain (abstract -> HTML -> PDF markdown),
delegates to ContentAdapter for PDF conversion, stores results in content_variants
with full provenance, and promotes Paper.processing_tier to CONTENT_PARSED.

Follows the EnrichmentService DI pattern: session_factory + settings + optional
adapter/client injection for testing.
"""

from __future__ import annotations

import hashlib
import tempfile
from datetime import datetime, timezone

import httpx
import structlog
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.content.adapters import MarkerAdapter, MockContentAdapter
from arxiv_mcp.content.html_fetcher import fetch_arxiv_html
from arxiv_mcp.content.models import ContentConversionResult
from arxiv_mcp.db.models import ContentVariant, Paper, ProcessingTier
from arxiv_mcp.enrichment.openalex import RateLimiter

logger = structlog.get_logger(__name__)


class ContentService:
    """Orchestrates content acquisition with priority chain and caching.

    Constructor follows the EnrichmentService DI pattern:
    session_factory + settings + optional adapter/client injection.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        adapter=None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.adapter = adapter
        self._http_client = http_client
        self._rate_limiter = RateLimiter(1.0 / settings.content_rate_limit)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def get_variant(
        self, arxiv_id: str, variant_type: str
    ) -> dict | None:
        """Look up a cached content variant from the database.

        Returns dict with variant fields or None if not found.
        """
        async with self.session_factory() as session:
            stmt = select(ContentVariant).where(
                ContentVariant.arxiv_id == arxiv_id,
                ContentVariant.variant_type == variant_type,
            )
            result = await session.execute(stmt)
            variant = result.scalar_one_or_none()

            if variant is None:
                return None

            return self._variant_to_dict(variant)

    async def get_or_create_variant(
        self, arxiv_id: str, preferred_variant: str = "best"
    ) -> dict:
        """Get or create a content variant using the priority chain.

        Args:
            arxiv_id: The arXiv paper ID.
            preferred_variant: One of "abstract", "html", "pdf_markdown", "best".
                "best" tries HTML first, falls back to PDF markdown.

        Returns:
            Dict with variant_type, content, and provenance metadata.
            On failure, returns {"error": "..."}.
        """
        if preferred_variant == "abstract":
            return await self._get_abstract(arxiv_id)

        if preferred_variant in ("best", "html"):
            # Check cache first
            cached = await self.get_variant(arxiv_id, "html")
            if cached is not None:
                return cached

            # Try HTML acquisition
            html_result = await self._acquire_html(arxiv_id)
            if html_result is not None:
                return html_result

            # If only HTML was requested (not "best"), stop here
            if preferred_variant == "html":
                return {"error": f"HTML variant not available for {arxiv_id}"}

        if preferred_variant in ("best", "pdf_markdown"):
            # Check cache first
            cached = await self.get_variant(arxiv_id, "pdf_markdown")
            if cached is not None:
                return cached

            # Try PDF markdown acquisition
            pdf_result = await self._acquire_pdf_markdown(arxiv_id)
            if pdf_result is not None:
                return pdf_result

        return {"error": f"No content variant available for {arxiv_id}"}

    async def list_variants(self, arxiv_id: str) -> list[dict]:
        """List all cached variants for a paper (without full content).

        Returns list of dicts with variant_type and converted_at.
        """
        async with self.session_factory() as session:
            stmt = select(
                ContentVariant.variant_type,
                ContentVariant.converted_at,
                ContentVariant.backend,
            ).where(ContentVariant.arxiv_id == arxiv_id)

            result = await session.execute(stmt)
            rows = result.all()

            return [
                {
                    "variant_type": row[0],
                    "converted_at": row[1].isoformat() if row[1] else None,
                    "backend": row[2],
                }
                for row in rows
            ]

    # ------------------------------------------------------------------
    # Abstract (trivial -- already in Paper model)
    # ------------------------------------------------------------------

    async def _get_abstract(self, arxiv_id: str) -> dict:
        """Return Paper.abstract as content dict (CONT-01)."""
        async with self.session_factory() as session:
            paper = await session.get(Paper, arxiv_id)
            if paper is None:
                return {"error": f"Paper '{arxiv_id}' not found"}

            return {
                "arxiv_id": arxiv_id,
                "variant_type": "abstract",
                "content": paper.abstract or "",
                "source_url": None,
                "backend": None,
                "backend_version": None,
                "extraction_method": "metadata",
                "license_uri": paper.license_uri,
                "quality_warnings": [],
                "content_hash": hashlib.sha256(
                    (paper.abstract or "").encode()
                ).hexdigest(),
                "converted_at": None,
            }

    # ------------------------------------------------------------------
    # HTML acquisition
    # ------------------------------------------------------------------

    async def _acquire_html(self, arxiv_id: str) -> dict | None:
        """Fetch arXiv HTML, store in content_variants, promote tier."""
        client = self._get_http_client()
        html_content, source_url = await fetch_arxiv_html(
            arxiv_id, client, self._rate_limiter
        )

        if html_content is None:
            return None

        return await self._store_variant(
            arxiv_id=arxiv_id,
            variant_type="html",
            content=html_content,
            result=None,
            source_url=source_url,
            backend="arxiv_html",
            extraction_method="direct_fetch",
        )

    # ------------------------------------------------------------------
    # PDF markdown acquisition
    # ------------------------------------------------------------------

    async def _acquire_pdf_markdown(self, arxiv_id: str) -> dict | None:
        """Download PDF, convert via adapter, store markdown, clean up."""
        if self.adapter is None:
            logger.warning("no_content_adapter", arxiv_id=arxiv_id)
            return None

        # Download PDF to temp file
        client = self._get_http_client()
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        try:
            await self._rate_limiter.acquire()
            response = await client.get(pdf_url)
            response.raise_for_status()
        except (httpx.TimeoutException, httpx.HTTPStatusError) as exc:
            logger.warning(
                "pdf_download_failed",
                arxiv_id=arxiv_id,
                error=str(exc),
            )
            return None

        # Write to temp file and convert
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(response.content)
            tmp.flush()

            conversion_result = await self.adapter.convert(tmp.name, arxiv_id)

        return await self._store_variant(
            arxiv_id=arxiv_id,
            variant_type="pdf_markdown",
            content=conversion_result.content,
            result=conversion_result,
            source_url=pdf_url,
            backend=conversion_result.backend,
            extraction_method=conversion_result.extraction_method,
        )

    # ------------------------------------------------------------------
    # Shared storage
    # ------------------------------------------------------------------

    async def _store_variant(
        self,
        arxiv_id: str,
        variant_type: str,
        content: str,
        result: ContentConversionResult | None,
        source_url: str | None,
        backend: str | None = None,
        extraction_method: str | None = None,
    ) -> dict:
        """Store a content variant with provenance and promote tier.

        Uses INSERT ON CONFLICT for upsert (same pattern as enrichment).
        """
        now = datetime.now(timezone.utc)
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        async with self.session_factory() as session:
            # Get license_uri from Paper
            paper = await session.get(Paper, arxiv_id)
            license_uri = paper.license_uri if paper else None

            # Build variant values
            backend_val = backend or (result.backend if result else None)
            backend_version = result.backend_version if result else None
            extraction_method_val = extraction_method or (
                result.extraction_method if result else None
            )
            quality_warnings = result.quality_warnings if result else None

            values = {
                "arxiv_id": arxiv_id,
                "variant_type": variant_type,
                "content": content,
                "content_hash": content_hash,
                "source_url": source_url,
                "backend": backend_val,
                "backend_version": backend_version,
                "extraction_method": extraction_method_val,
                "license_uri": license_uri,
                "quality_warnings": quality_warnings,
                "fetched_at": now,
                "converted_at": now,
            }

            stmt = pg_insert(ContentVariant).values(**values)
            stmt = stmt.on_conflict_do_update(
                index_elements=["arxiv_id", "variant_type"],
                set_={
                    k: v
                    for k, v in values.items()
                    if k not in ("arxiv_id", "variant_type")
                },
            )
            await session.execute(stmt)

            # Promote processing tier to CONTENT_PARSED
            if paper and paper.processing_tier < ProcessingTier.CONTENT_PARSED:
                paper.processing_tier = ProcessingTier.CONTENT_PARSED
                paper.promotion_reason = f"content_{variant_type}"

            await session.commit()

        return {
            "arxiv_id": arxiv_id,
            "variant_type": variant_type,
            "content": content,
            "source_url": source_url,
            "backend": backend_val,
            "backend_version": backend_version,
            "extraction_method": extraction_method_val,
            "license_uri": license_uri,
            "quality_warnings": quality_warnings or [],
            "content_hash": content_hash,
            "converted_at": now.isoformat(),
        }

    # ------------------------------------------------------------------
    # HTTP client
    # ------------------------------------------------------------------

    def _get_http_client(self) -> httpx.AsyncClient:
        """Lazy-init HTTP client."""
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(
                follow_redirects=True,
                timeout=30.0,
            )
        return self._http_client

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _variant_to_dict(variant: ContentVariant) -> dict:
        """Convert a ContentVariant ORM instance to a response dict."""
        return {
            "arxiv_id": variant.arxiv_id,
            "variant_type": variant.variant_type,
            "content": variant.content,
            "source_url": variant.source_url,
            "backend": variant.backend,
            "backend_version": variant.backend_version,
            "extraction_method": variant.extraction_method,
            "license_uri": variant.license_uri,
            "quality_warnings": variant.quality_warnings or [],
            "content_hash": variant.content_hash,
            "converted_at": (
                variant.converted_at.isoformat()
                if variant.converted_at
                else None
            ),
        }
