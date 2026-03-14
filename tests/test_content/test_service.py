"""Integration tests for ContentService.

Tests content acquisition orchestration: abstract variant, HTML variant,
PDF markdown variant, priority chain ("best"), caching, tier promotion,
provenance tracking, and variant listing. Uses MockContentAdapter and
respx-mocked HTTP for HTML/PDF fetching.
"""

from __future__ import annotations


import httpx
import pytest
import respx

from arxiv_mcp.config import Settings
from arxiv_mcp.content.adapters import MockContentAdapter
from arxiv_mcp.db.models import Paper, ProcessingTier
from tests.conftest import sample_paper_data


SAMPLE_HTML_RESPONSE = """
<!DOCTYPE html>
<html>
<body>
<nav>Nav</nav>
<article>
<h2>Introduction</h2>
<p>This paper presents important results in deep learning.</p>
<h2>Methods</h2>
<p>We propose a novel architecture based on attention mechanisms.</p>
</article>
<footer>Footer</footer>
</body>
</html>
"""

SAMPLE_PDF_BYTES = b"%PDF-1.4 fake pdf content"

HTML_URL = "https://arxiv.org/html/2301.00001"
PDF_URL = "https://arxiv.org/pdf/2301.00001"


@pytest.fixture
def test_settings() -> Settings:
    """Settings configured for testing."""
    return Settings(
        database_url="postgresql+asyncpg://test:test@localhost/test",
        test_database_url="postgresql+asyncpg://test:test@localhost/test",
        content_rate_limit=100.0,  # Fast for tests
        deployment_mode="local",
        content_max_pdf_pages=100,
    )


@pytest.fixture
async def paper_in_db(content_session_factory) -> Paper:
    """Insert a sample paper and return it."""
    async with content_session_factory() as session:
        data = sample_paper_data(
            arxiv_id="2301.00001",
            license_uri="http://creativecommons.org/licenses/by/4.0/",
        )
        paper = Paper(**data)
        session.add(paper)
        await session.commit()
        await session.refresh(paper)
        return paper


def _mock_html_client() -> httpx.AsyncClient:
    """Create a mock transport client for testing (no real HTTP)."""
    return httpx.AsyncClient(transport=respx.mock.transport)


class TestGetAbstractVariant:
    """Tests for abstract variant (returns Paper.abstract directly)."""

    @pytest.mark.asyncio
    async def test_get_abstract_variant(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """Abstract variant returns Paper.abstract as content dict."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()
        svc = ContentService(content_session_factory, test_settings, adapter=adapter)

        result = await svc.get_or_create_variant("2301.00001", preferred_variant="abstract")

        assert result["variant_type"] == "abstract"
        assert "Transformer" in result["content"]
        assert result["extraction_method"] == "metadata"
        assert result["backend"] is None


class TestGetVariant:
    """Tests for get_variant (cache lookup)."""

    @pytest.mark.asyncio
    async def test_get_variant_returns_none_for_missing(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """get_variant returns None when no cached variant exists."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()
        svc = ContentService(content_session_factory, test_settings, adapter=adapter)

        result = await svc.get_variant("2301.00001", "html")
        assert result is None


class TestHtmlVariant:
    """Tests for HTML variant acquisition."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_or_create_html_variant(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """HTML variant fetches from arXiv, stores, and returns content dict."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        assert result["variant_type"] == "html"
        assert "important results" in result["content"]
        assert result["backend"] == "arxiv_html"
        assert result["extraction_method"] == "direct_fetch"
        assert result["source_url"] == "https://arxiv.org/html/2301.00001"


class TestPdfMarkdownVariant:
    """Tests for PDF markdown variant acquisition."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_get_or_create_pdf_markdown_variant(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """PDF markdown variant downloads PDF, converts via adapter, stores result."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=SAMPLE_PDF_BYTES)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant(
            "2301.00001", preferred_variant="pdf_markdown"
        )
        await client.aclose()

        assert result["variant_type"] == "pdf_markdown"
        assert result["backend"] == "mock_marker"
        assert result["extraction_method"] == "pdf_parse"
        assert len(adapter.convert_calls) == 1


class TestBestVariant:
    """Tests for 'best' variant priority chain."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_best_variant_tries_html_first(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """'best' variant attempts HTML before PDF markdown."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant("2301.00001", preferred_variant="best")
        await client.aclose()

        assert result["variant_type"] == "html"
        # No PDF conversion should have been called
        assert len(adapter.convert_calls) == 0

    @respx.mock
    @pytest.mark.asyncio
    async def test_best_variant_falls_back_to_pdf(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """When HTML unavailable (404), 'best' falls back to PDF markdown."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(404))
        respx.get(PDF_URL).mock(
            return_value=httpx.Response(200, content=SAMPLE_PDF_BYTES)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant("2301.00001", preferred_variant="best")
        await client.aclose()

        assert result["variant_type"] == "pdf_markdown"
        assert len(adapter.convert_calls) == 1


class TestCaching:
    """Tests for variant caching behavior."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_cached_variant_returned_without_refetch(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """Second call returns from DB without making HTTP requests."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        # First call: fetch and store HTML
        head_route = respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        get_route = respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result1 = await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        assert head_route.call_count == 1
        assert get_route.call_count == 1

        # Second call: should hit cache, no HTTP
        svc2 = ContentService(content_session_factory, test_settings, adapter=adapter)
        result2 = await svc2.get_or_create_variant("2301.00001", preferred_variant="html")

        assert result2["variant_type"] == "html"
        assert result2["content"] == result1["content"]


class TestTierPromotion:
    """Tests for processing tier promotion."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_processing_tier_promoted(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """Paper.processing_tier updated to CONTENT_PARSED after conversion."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        # Verify tier promotion in DB
        async with content_session_factory() as session:
            paper = await session.get(Paper, "2301.00001")
            assert paper.processing_tier == ProcessingTier.CONTENT_PARSED


class TestProvenance:
    """Tests for provenance field population."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_license_uri_copied(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """ContentVariant.license_uri matches Paper.license_uri."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        assert result["license_uri"] == "http://creativecommons.org/licenses/by/4.0/"

    @respx.mock
    @pytest.mark.asyncio
    async def test_provenance_fields_populated(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """All provenance fields are non-null on stored variants."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        result = await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        assert result["source_url"] is not None
        assert result["backend"] is not None
        assert result["extraction_method"] is not None
        assert result["content_hash"] is not None
        assert result["license_uri"] is not None


class TestListVariants:
    """Tests for listing available variants."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_list_variants_returns_summary(
        self, content_session_factory, test_settings, paper_in_db
    ):
        """list_variants returns variant types without full content."""
        from arxiv_mcp.content.service import ContentService

        adapter = MockContentAdapter()

        # Store an HTML variant first
        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_RESPONSE)
        )

        client = httpx.AsyncClient()
        svc = ContentService(
            content_session_factory, test_settings,
            adapter=adapter, http_client=client,
        )
        await svc.get_or_create_variant("2301.00001", preferred_variant="html")
        await client.aclose()

        # List variants
        svc2 = ContentService(content_session_factory, test_settings, adapter=adapter)
        variants = await svc2.list_variants("2301.00001")

        assert len(variants) >= 1
        for v in variants:
            assert "variant_type" in v
            assert "converted_at" in v
            # Content should NOT be included in listing
            assert "content" not in v
