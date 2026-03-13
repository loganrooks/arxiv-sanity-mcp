"""Tests for get_content_variant MCP tool.

Covers: content retrieval by variant type, rights enforcement (CONT-06),
error handling for not-found and invalid variants, and rights warning propagation.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest


class TestGetContentVariantAbstract:
    """get_content_variant with variant='abstract' returns content dict."""

    async def test_get_content_variant_abstract(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        mock_app_context.content = AsyncMock()
        mock_app_context.content.get_or_create_variant = AsyncMock(
            return_value={
                "arxiv_id": "2301.00001",
                "variant_type": "abstract",
                "content": "This is a test abstract.",
                "source_url": None,
                "backend": None,
                "backend_version": None,
                "extraction_method": "metadata",
                "license_uri": "http://creativecommons.org/licenses/by/4.0/",
                "quality_warnings": [],
                "content_hash": "abc123",
                "converted_at": None,
            }
        )

        result = await get_content_variant(
            arxiv_id="2301.00001", variant="abstract", ctx=mock_ctx
        )

        assert result["arxiv_id"] == "2301.00001"
        assert result["variant_type"] == "abstract"
        assert result["content"] == "This is a test abstract."
        # Abstract skips rights check -- always allowed
        mock_app_context.content.get_or_create_variant.assert_awaited_once_with(
            "2301.00001", "abstract"
        )


class TestGetContentVariantBest:
    """get_content_variant with variant='best' delegates to service."""

    async def test_get_content_variant_best(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        # Mock Paper lookup for license check
        mock_paper = MagicMock()
        mock_paper.license_uri = "http://creativecommons.org/licenses/by/4.0/"
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(return_value=mock_paper)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        mock_app_context.content = AsyncMock()
        mock_app_context.content.get_or_create_variant = AsyncMock(
            return_value={
                "arxiv_id": "2301.00001",
                "variant_type": "html",
                "content": "<p>HTML content</p>",
                "source_url": "https://arxiv.org/html/2301.00001",
                "backend": "arxiv_html",
                "backend_version": None,
                "extraction_method": "direct_fetch",
                "license_uri": "http://creativecommons.org/licenses/by/4.0/",
                "quality_warnings": [],
                "content_hash": "def456",
                "converted_at": "2026-01-01T00:00:00",
            }
        )
        mock_app_context.settings.deployment_mode = "local"

        result = await get_content_variant(
            arxiv_id="2301.00001", variant="best", ctx=mock_ctx
        )

        assert result["variant_type"] == "html"
        assert result["content"] == "<p>HTML content</p>"


class TestGetContentVariantInvalid:
    """get_content_variant with invalid variant returns error."""

    async def test_get_content_variant_invalid_variant(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        result = await get_content_variant(
            arxiv_id="2301.00001", variant="latex_source", ctx=mock_ctx
        )

        assert "error" in result
        assert "invalid variant" in result["error"].lower() or "valid variants" in result["error"].lower()


class TestGetContentVariantNotFound:
    """get_content_variant returns error dict when paper not found."""

    async def test_get_content_variant_paper_not_found(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        mock_app_context.content = AsyncMock()
        mock_app_context.content.get_or_create_variant = AsyncMock(
            return_value={"error": "Paper '9999.99999' not found"}
        )

        result = await get_content_variant(
            arxiv_id="9999.99999", variant="abstract", ctx=mock_ctx
        )

        assert "error" in result
        assert "9999.99999" in result["error"]


class TestGetContentVariantRightsWarning:
    """get_content_variant in local mode adds rights_warning for restrictive license."""

    async def test_get_content_variant_with_rights_warning(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        # Mock Paper lookup -- restrictive license
        mock_paper = MagicMock()
        mock_paper.license_uri = "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(return_value=mock_paper)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        mock_app_context.content = AsyncMock()
        mock_app_context.content.get_or_create_variant = AsyncMock(
            return_value={
                "arxiv_id": "2301.00001",
                "variant_type": "html",
                "content": "<p>Content</p>",
                "source_url": "https://arxiv.org/html/2301.00001",
                "backend": "arxiv_html",
                "backend_version": None,
                "extraction_method": "direct_fetch",
                "license_uri": "http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
                "quality_warnings": [],
                "content_hash": "ghi789",
                "converted_at": "2026-01-01T00:00:00",
            }
        )
        mock_app_context.settings.deployment_mode = "local"

        result = await get_content_variant(
            arxiv_id="2301.00001", variant="html", ctx=mock_ctx
        )

        # In local mode with restrictive license: allowed but with warning
        assert "error" not in result
        assert "rights_warning" in result
        assert "personal" in result["rights_warning"].lower() or "nonexclusive" in result["rights_warning"].lower()


class TestGetContentVariantRightsBlocked:
    """get_content_variant in hosted mode blocks restrictive license."""

    async def test_get_content_variant_rights_blocked(self, mock_ctx, mock_app_context):
        from arxiv_mcp.mcp.tools.content import get_content_variant

        # Mock Paper lookup -- restrictive license
        mock_paper = MagicMock()
        mock_paper.license_uri = "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"
        mock_session = AsyncMock()
        mock_session.get = AsyncMock(return_value=mock_paper)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)
        mock_app_context.session_factory.return_value = mock_session

        mock_app_context.settings.deployment_mode = "hosted"

        result = await get_content_variant(
            arxiv_id="2301.00001", variant="html", ctx=mock_ctx
        )

        # Hosted mode with restrictive license: blocked
        assert "error" in result
        assert "license_uri" in result
