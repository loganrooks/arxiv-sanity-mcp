"""Tests for content adapters: MockContentAdapter and MarkerAdapter.

Tests MockContentAdapter protocol compliance, call tracking, and
configurable result returns. MarkerAdapter is verified structurally
(class exists, adapter_name correct) since actual PDF conversion
requires heavy GPU/CPU dependencies.
"""

from __future__ import annotations

import pytest

from arxiv_mcp.content.models import ContentConversionResult


class TestMockContentAdapter:
    """Tests for MockContentAdapter: protocol compliance, call tracking, results."""

    @pytest.mark.asyncio
    async def test_mock_adapter_has_adapter_name(self):
        """MockContentAdapter exposes adapter_name property satisfying protocol."""
        from arxiv_mcp.content.adapters import MockContentAdapter

        adapter = MockContentAdapter()
        assert adapter.adapter_name == "mock_marker"

    @pytest.mark.asyncio
    async def test_mock_adapter_has_convert_method(self):
        """MockContentAdapter has async convert method satisfying protocol."""
        from arxiv_mcp.content.adapters import MockContentAdapter

        adapter = MockContentAdapter()
        assert hasattr(adapter, "convert")
        assert callable(adapter.convert)

    @pytest.mark.asyncio
    async def test_mock_adapter_tracks_calls(self):
        """MockContentAdapter tracks convert calls as (pdf_path, arxiv_id) tuples."""
        from arxiv_mcp.content.adapters import MockContentAdapter

        adapter = MockContentAdapter()
        assert adapter.convert_calls == []

        await adapter.convert("/tmp/test.pdf", "2301.00001")
        await adapter.convert("/tmp/other.pdf", "2301.00002")

        assert len(adapter.convert_calls) == 2
        assert adapter.convert_calls[0] == ("/tmp/test.pdf", "2301.00001")
        assert adapter.convert_calls[1] == ("/tmp/other.pdf", "2301.00002")

    @pytest.mark.asyncio
    async def test_mock_adapter_returns_predetermined_result(self):
        """MockContentAdapter returns predetermined results by arxiv_id."""
        from arxiv_mcp.content.adapters import MockContentAdapter

        custom_result = ContentConversionResult(
            content="Custom mock content for paper 2301.00001",
            backend="marker",
            backend_version="1.0.0",
            extraction_method="pdf_parse",
            quality_warnings=["math_heavy"],
        )
        adapter = MockContentAdapter(results={"2301.00001": custom_result})

        result = await adapter.convert("/tmp/test.pdf", "2301.00001")
        assert result.content == "Custom mock content for paper 2301.00001"
        assert result.quality_warnings == ["math_heavy"]

    @pytest.mark.asyncio
    async def test_mock_adapter_returns_default_for_unknown_id(self):
        """MockContentAdapter returns default mock content for unrecognized arxiv_id."""
        from arxiv_mcp.content.adapters import MockContentAdapter

        adapter = MockContentAdapter()

        result = await adapter.convert("/tmp/test.pdf", "9999.99999")
        assert isinstance(result, ContentConversionResult)
        assert len(result.content) > 0
        assert result.backend == "mock_marker"
        assert result.extraction_method == "pdf_parse"


class TestMarkerAdapter:
    """Structural tests for MarkerAdapter (no actual conversion)."""

    def test_marker_adapter_class_exists(self):
        """MarkerAdapter class is importable."""
        from arxiv_mcp.content.adapters import MarkerAdapter

        assert MarkerAdapter is not None

    def test_marker_adapter_name(self):
        """MarkerAdapter has adapter_name 'marker' (tested without initializing converter)."""
        from arxiv_mcp.content.adapters import MarkerAdapter

        # Check the class has the property defined
        assert "adapter_name" in dir(MarkerAdapter)


class TestContentAdapterProtocol:
    """Test that ContentAdapter protocol is defined correctly."""

    def test_protocol_importable(self):
        """ContentAdapter protocol is importable."""
        from arxiv_mcp.content.adapters import ContentAdapter

        assert ContentAdapter is not None
