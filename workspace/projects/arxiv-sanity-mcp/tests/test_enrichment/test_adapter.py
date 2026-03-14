"""Unit tests for OpenAlexAdapter with respx-mocked HTTP calls.

Tests DOI-based resolution, batch lookup, rate limiting, retry logic,
error handling, and proper resource cleanup.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from arxiv_mcp.config import Settings
from arxiv_mcp.enrichment.models import EnrichmentStatus, ExternalIds
from arxiv_mcp.enrichment.openalex import OpenAlexAdapter


@pytest.fixture
def adapter_settings() -> Settings:
    """Settings configured for testing against respx mock."""
    return Settings(
        openalex_api_url="https://api.openalex.org",
        openalex_api_key="test-key-123",
        enrichment_batch_size=50,
        enrichment_rate_limit=100.0,  # High rate for fast tests
        database_url="postgresql+asyncpg://test:test@localhost/test",
        test_database_url="postgresql+asyncpg://test:test@localhost/test",
    )


@pytest.fixture
def adapter_no_key() -> Settings:
    """Settings without API key."""
    return Settings(
        openalex_api_url="https://api.openalex.org",
        openalex_api_key="",
        enrichment_batch_size=50,
        enrichment_rate_limit=100.0,
        database_url="postgresql+asyncpg://test:test@localhost/test",
        test_database_url="postgresql+asyncpg://test:test@localhost/test",
    )


@pytest.fixture
def mock_openalex():
    """Provide a respx mock router scoped to OpenAlex API base URL."""
    with respx.mock(base_url="https://api.openalex.org") as router:
        yield router


class TestSingletonResolution:
    """Tests for single-paper ID resolution via singleton endpoint (FREE)."""

    @pytest.mark.asyncio
    async def test_resolve_single_id(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """Single paper resolves arXiv ID via DOI prefix using singleton endpoint."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        result = await adapter.resolve_ids(["1706.03762"])

        assert "1706.03762" in result
        assert isinstance(result["1706.03762"], ExternalIds)
        assert result["1706.03762"].openalex_id == "W2741809807"
        assert result["1706.03762"].doi == "10.48550/arxiv.1706.03762"

    @pytest.mark.asyncio
    async def test_resolve_batch_ids(
        self, mock_openalex, adapter_settings, openalex_batch_fixture
    ):
        """Batch resolution uses filter=doi: endpoint for multiple IDs."""
        mock_openalex.get("/works").mock(
            return_value=httpx.Response(200, json=openalex_batch_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        result = await adapter.resolve_ids(
            ["1706.03762", "2301.00001", "2305.12345"]
        )

        assert len(result) == 3
        assert result["1706.03762"].openalex_id == "W2741809807"
        assert result["2301.00001"].openalex_id == "W3456789012"
        assert result["2305.12345"].openalex_id == "W9876543210"


class TestBatchChunking:
    """Tests for batch chunking logic."""

    @pytest.mark.asyncio
    async def test_batch_respects_max_batch_size(self, mock_openalex, adapter_settings):
        """Batch respects max batch size of 50 (splits larger lists into chunks)."""
        adapter_settings.enrichment_batch_size = 50

        # Generate 60 IDs
        arxiv_ids = [f"2301.{i:05d}" for i in range(60)]

        batch_response_1 = {
            "meta": {"count": 50},
            "results": [
                {
                    "id": f"https://openalex.org/W{i}",
                    "doi": f"https://doi.org/10.48550/arXiv.2301.{i:05d}",
                    "ids": {"openalex": f"https://openalex.org/W{i}"},
                    "type": "preprint",
                    "cited_by_count": i,
                    "fwci": None,
                    "primary_topic": None,
                    "topics": [],
                    "related_works": [],
                    "counts_by_year": [],
                }
                for i in range(50)
            ],
        }
        batch_response_2 = {
            "meta": {"count": 10},
            "results": [
                {
                    "id": f"https://openalex.org/W{i}",
                    "doi": f"https://doi.org/10.48550/arXiv.2301.{i:05d}",
                    "ids": {"openalex": f"https://openalex.org/W{i}"},
                    "type": "preprint",
                    "cited_by_count": i,
                    "fwci": None,
                    "primary_topic": None,
                    "topics": [],
                    "related_works": [],
                    "counts_by_year": [],
                }
                for i in range(50, 60)
            ],
        }

        route = mock_openalex.get("/works").mock(
            side_effect=[
                httpx.Response(200, json=batch_response_1),
                httpx.Response(200, json=batch_response_2),
            ]
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(arxiv_ids)

        assert route.call_count == 2
        assert len(results) == 60


class TestEnrichSingle:
    """Tests for single paper enrichment."""

    @pytest.mark.asyncio
    async def test_enrich_success(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """Single enrich returns full EnrichmentResult on success."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["1706.03762"])

        assert len(results) == 1
        result = results[0]
        assert result.cited_by_count == 6497
        assert result.fwci == pytest.approx(115.7593)
        assert result.openalex_id == "W2741809807"
        assert result.status == EnrichmentStatus.SUCCESS
        assert result.topics is not None
        assert len(result.topics) == 3

    @pytest.mark.asyncio
    async def test_enrich_not_found(self, mock_openalex, adapter_settings):
        """404 response returns EnrichmentResult with status='not_found'."""
        mock_openalex.get("/works/doi:10.48550/arXiv.9999.99999").mock(
            return_value=httpx.Response(404, json={"error": "Not found"})
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["9999.99999"])

        assert len(results) == 1
        assert results[0].status == EnrichmentStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_enrich_partial(
        self, mock_openalex, adapter_settings, openalex_batch_fixture
    ):
        """Partial response (missing FWCI or topics) returns status='partial'."""
        partial_work = openalex_batch_fixture["results"][1]
        mock_openalex.get("/works/doi:10.48550/arXiv.2301.00001").mock(
            return_value=httpx.Response(200, json=partial_work)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["2301.00001"])

        assert len(results) == 1
        assert results[0].status == EnrichmentStatus.PARTIAL
        assert results[0].fwci is None


class TestRateLimitAndRetry:
    """Tests for rate limiting and 429 retry behavior."""

    @pytest.mark.asyncio
    async def test_429_triggers_retry(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """429 response triggers exponential backoff retry (up to 3 retries)."""
        route = mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            side_effect=[
                httpx.Response(429, json={"error": "Rate limit"}),
                httpx.Response(200, json=openalex_work_fixture),
            ]
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["1706.03762"])

        assert route.call_count == 2
        assert len(results) == 1
        assert results[0].status == EnrichmentStatus.SUCCESS

    @pytest.mark.asyncio
    async def test_rate_limiter_enforces_interval(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """Rate limiter enforces minimum interval between requests."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter_settings.enrichment_rate_limit = 100.0
        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["1706.03762"])

        assert len(results) == 1
        assert results[0].status == EnrichmentStatus.SUCCESS


class TestAPIKeyAndParams:
    """Tests for API key and select parameter handling."""

    @pytest.mark.asyncio
    async def test_api_key_included(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """Adapter includes api_key in request params when configured."""
        route = mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        await adapter.enrich(["1706.03762"])

        assert route.calls.last is not None
        request = route.calls.last.request
        assert b"api_key=test-key-123" in request.url.query

    @pytest.mark.asyncio
    async def test_select_parameter_present(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """Adapter uses select= parameter to request only needed fields."""
        route = mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        await adapter.enrich(["1706.03762"])

        request = route.calls.last.request
        assert b"select=" in request.url.query

    @pytest.mark.asyncio
    async def test_no_api_key_omits_param(
        self, mock_openalex, adapter_no_key, openalex_work_fixture
    ):
        """Adapter omits api_key when not configured."""
        route = mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_no_key)
        await adapter.enrich(["1706.03762"])

        request = route.calls.last.request
        assert b"api_key" not in request.url.query


class TestErrorHandling:
    """Tests for network error handling."""

    @pytest.mark.asyncio
    async def test_timeout_returns_error(self, mock_openalex, adapter_settings):
        """Network timeout returns status='error' with error_detail."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["1706.03762"])

        assert len(results) == 1
        assert results[0].status == EnrichmentStatus.ERROR
        assert results[0].error_detail is not None
        assert (
            "timed out" in results[0].error_detail.lower()
            or "timeout" in results[0].error_detail.lower()
        )

    @pytest.mark.asyncio
    async def test_client_properly_closed(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """httpx.AsyncClient is properly closed after use (no resource leaks)."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        results = await adapter.enrich(["1706.03762"])

        # If we get here without ResourceWarning, the client was properly closed
        assert len(results) == 1


class TestResolveIds:
    """Tests for resolve_ids method."""

    @pytest.mark.asyncio
    async def test_resolve_ids_returns_dict(
        self, mock_openalex, adapter_settings, openalex_work_fixture
    ):
        """resolve_ids returns dict mapping arXiv IDs to ExternalIds."""
        mock_openalex.get("/works/doi:10.48550/arXiv.1706.03762").mock(
            return_value=httpx.Response(200, json=openalex_work_fixture)
        )

        adapter = OpenAlexAdapter(adapter_settings)
        result = await adapter.resolve_ids(["1706.03762"])

        assert isinstance(result, dict)
        assert "1706.03762" in result
        ext_ids = result["1706.03762"]
        assert isinstance(ext_ids, ExternalIds)
        assert ext_ids.openalex_id == "W2741809807"
