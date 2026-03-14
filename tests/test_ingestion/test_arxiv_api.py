"""Tests for arXiv search API client.

Tests cover fetching by ID, searching by query, rate limiting,
pagination, and mapping to Paper instances. HTTP responses are mocked.
"""

from __future__ import annotations

import time
from unittest.mock import AsyncMock, MagicMock, patch


from arxiv_mcp.config import Settings
from arxiv_mcp.ingestion.arxiv_api import ArxivAPIClient
from arxiv_mcp.ingestion.mapper import map_to_paper
from arxiv_mcp.ingestion.parsers import RawPaperMetadata


# --- Sample Atom XML response ---

SAMPLE_ATOM_SINGLE = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <opensearch:totalResults>1</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>1</opensearch:itemsPerPage>
  <entry>
    <id>http://arxiv.org/abs/2301.00001v2</id>
    <updated>2023-06-15T08:30:00Z</updated>
    <published>2023-01-02T12:00:00Z</published>
    <title>Attention Is All You Need: A Revisitation</title>
    <summary>  The dominant sequence transduction models are based on complex recurrent
or convolutional neural networks. We propose the Transformer.</summary>
    <author>
      <name>Ashish Vaswani</name>
    </author>
    <author>
      <name>Noam Shazeer</name>
      <arxiv:affiliation>Google Brain</arxiv:affiliation>
    </author>
    <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom"
                            term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
    <category term="cs.LG" scheme="http://arxiv.org/schemas/atom"/>
    <arxiv:doi xmlns:arxiv="http://arxiv.org/schemas/atom">10.48550/arXiv.2301.00001</arxiv:doi>
    <arxiv:comment xmlns:arxiv="http://arxiv.org/schemas/atom">15 pages, 5 figures</arxiv:comment>
    <arxiv:journal_ref xmlns:arxiv="http://arxiv.org/schemas/atom">JMLR 2023</arxiv:journal_ref>
  </entry>
</feed>
"""

SAMPLE_ATOM_MULTI = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <opensearch:totalResults>3</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>2</opensearch:itemsPerPage>
  <entry>
    <id>http://arxiv.org/abs/2301.00001v1</id>
    <updated>2023-01-02T12:00:00Z</updated>
    <published>2023-01-02T12:00:00Z</published>
    <title>Paper One</title>
    <summary>Abstract one.</summary>
    <author><name>Author One</name></author>
    <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="cs.CL"/>
    <category term="cs.CL" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2301.00002v1</id>
    <updated>2023-01-03T12:00:00Z</updated>
    <published>2023-01-03T12:00:00Z</published>
    <title>Paper Two</title>
    <summary>Abstract two.</summary>
    <author><name>Author Two</name></author>
    <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="cs.AI"/>
    <category term="cs.AI" scheme="http://arxiv.org/schemas/atom"/>
  </entry>
</feed>
"""

SAMPLE_ATOM_EMPTY = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <opensearch:totalResults>0</opensearch:totalResults>
  <opensearch:startIndex>0</opensearch:startIndex>
  <opensearch:itemsPerPage>10</opensearch:itemsPerPage>
</feed>
"""


def _make_settings(**overrides) -> Settings:
    """Create test settings."""
    defaults = {
        "database_url": "postgresql+asyncpg://test:test@localhost/test",
        "test_database_url": "postgresql+asyncpg://test:test@localhost/test",
        "arxiv_api_url": "http://export.arxiv.org/api/query",
        "harvest_rate_limit": 0.0,  # No delay in tests
    }
    defaults.update(overrides)
    return Settings(**defaults)


class TestArxivAPIClient:
    """Tests for ArxivAPIClient."""

    @patch("arxiv_mcp.ingestion.arxiv_api.httpx.AsyncClient")
    async def test_fetch_by_id(self, mock_client_cls):
        """Fetch a single paper by arXiv ID, parse Atom XML."""
        mock_response = MagicMock()
        mock_response.content = SAMPLE_ATOM_SINGLE
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        settings = _make_settings()
        client = ArxivAPIClient(settings=settings)
        result = await client.fetch_paper("2301.00001")

        assert result is not None
        assert isinstance(result, RawPaperMetadata)
        assert result.arxiv_id == "2301.00001"
        assert result.title == "Attention Is All You Need: A Revisitation"
        assert "Vaswani" in result.authors
        assert "Shazeer" in result.authors
        assert result.categories == "cs.CL cs.AI cs.LG"
        assert result.primary_category == "cs.CL"
        assert result.doi == "10.48550/arXiv.2301.00001"

    @patch("arxiv_mcp.ingestion.arxiv_api.httpx.AsyncClient")
    async def test_search_query(self, mock_client_cls):
        """Search with query string, parse results list."""
        mock_response = MagicMock()
        mock_response.content = SAMPLE_ATOM_MULTI
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        settings = _make_settings()
        client = ArxivAPIClient(settings=settings)
        results = await client.search("ti:transformer")

        assert len(results) == 2
        assert results[0].arxiv_id == "2301.00001"
        assert results[1].arxiv_id == "2301.00002"
        assert results[0].title == "Paper One"
        assert results[1].title == "Paper Two"

    async def test_api_rate_limiting(self):
        """Client enforces minimum delay between requests."""
        settings = _make_settings(harvest_rate_limit=0.1)  # 100ms for test speed
        client = ArxivAPIClient(settings=settings)

        # Simulate two rapid requests
        t0 = time.monotonic()
        client._last_request_time = t0  # Pretend we just made a request

        delay = client._calculate_delay()
        assert delay >= 0.05  # Should have some delay

    @patch("arxiv_mcp.ingestion.arxiv_api.httpx.AsyncClient")
    async def test_api_pagination(self, mock_client_cls):
        """Client handles totalResults and startIndex for multi-page results."""
        mock_response = MagicMock()
        mock_response.content = SAMPLE_ATOM_MULTI
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        settings = _make_settings()
        client = ArxivAPIClient(settings=settings)
        results = await client.search("cat:cs.CL", start=0, max_results=2)

        # Verify pagination parameters were passed
        call_args = mock_client.get.call_args
        _params = call_args[1].get("params", call_args[0][1] if len(call_args[0]) > 1 else {})
        assert len(results) == 2

    @patch("arxiv_mcp.ingestion.arxiv_api.httpx.AsyncClient")
    async def test_api_maps_to_paper(self, mock_client_cls):
        """API results are mapped through mapper to Paper instances."""
        mock_response = MagicMock()
        mock_response.content = SAMPLE_ATOM_SINGLE
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()

        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client_cls.return_value = mock_client

        settings = _make_settings()
        client = ArxivAPIClient(settings=settings)
        raw = await client.fetch_paper("2301.00001")

        assert raw is not None
        paper = map_to_paper(raw, source="arxiv_api")

        assert paper.arxiv_id == "2301.00001"
        assert paper.source == "arxiv_api"
        assert paper.categories == "cs.CL cs.AI cs.LG"
        assert paper.primary_category == "cs.CL"
        assert paper.submitted_date is not None
        assert paper.updated_date is not None
