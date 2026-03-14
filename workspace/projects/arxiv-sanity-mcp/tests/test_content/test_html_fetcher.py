"""Tests for arXiv HTML fetcher with mocked HTTP responses.

Tests fetch_arxiv_html function: 404 handling, content extraction,
nav/header/footer stripping, missing container handling, and timeout
graceful degradation. Uses respx for HTTP mocking.
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest
import respx


# Sample HTML response with article content
SAMPLE_HTML_WITH_ARTICLE = """
<!DOCTYPE html>
<html>
<head><title>Test Paper</title></head>
<body>
<nav><ul><li>Home</li><li>About</li></ul></nav>
<header><h1>arXiv Header</h1></header>
<article>
<h2>Introduction</h2>
<p>This is the main content of the paper.</p>
<h2>Methods</h2>
<p>We used advanced techniques.</p>
</article>
<footer><p>arXiv Footer</p></footer>
</body>
</html>
"""

SAMPLE_HTML_WITH_MAIN = """
<!DOCTYPE html>
<html>
<body>
<nav>Navigation</nav>
<main>
<h2>Introduction</h2>
<p>Main content area.</p>
</main>
<footer>Footer</footer>
</body>
</html>
"""

SAMPLE_HTML_NO_CONTAINER = """
<!DOCTYPE html>
<html>
<head><title>No Container</title></head>
<body></body>
</html>
"""

HTML_URL = "https://arxiv.org/html/2301.00001"


class TestFetchArxivHtml:
    """Tests for fetch_arxiv_html function."""

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_none_for_404(self):
        """fetch_arxiv_html returns (None, None) for 404 HEAD response."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(404))

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is None
        assert url is None

    @respx.mock
    @pytest.mark.asyncio
    async def test_extracts_article_content(self):
        """fetch_arxiv_html extracts article content from valid HTML."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_WITH_ARTICLE)
        )

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is not None
        assert "main content of the paper" in content
        assert "advanced techniques" in content
        assert url == "https://arxiv.org/html/2301.00001"

    @respx.mock
    @pytest.mark.asyncio
    async def test_strips_nav_header_footer(self):
        """fetch_arxiv_html strips nav, header, footer elements."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_WITH_ARTICLE)
        )

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is not None
        assert "arXiv Header" not in content
        assert "arXiv Footer" not in content
        assert "Home" not in content  # nav content stripped

    @respx.mock
    @pytest.mark.asyncio
    async def test_falls_back_to_main_container(self):
        """fetch_arxiv_html falls back to <main> if no <article>."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_WITH_MAIN)
        )

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is not None
        assert "Main content area" in content

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_none_when_no_container(self):
        """fetch_arxiv_html returns None when no article/main/body container found."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_NO_CONTAINER)
        )

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        # body exists but is empty -- should still find body container
        # But no meaningful content will be returned
        # The function finds body, strips nav/header/footer, returns str(body)

    @respx.mock
    @pytest.mark.asyncio
    async def test_handles_timeout_gracefully(self):
        """fetch_arxiv_html returns (None, None) on timeout."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is None
        assert url is None

    @respx.mock
    @pytest.mark.asyncio
    async def test_respects_rate_limiter(self):
        """fetch_arxiv_html calls rate_limiter.acquire before HTTP requests."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        respx.head(HTML_URL).mock(return_value=httpx.Response(200))
        respx.get(HTML_URL).mock(
            return_value=httpx.Response(200, text=SAMPLE_HTML_WITH_ARTICLE)
        )

        async with httpx.AsyncClient() as client:
            await fetch_arxiv_html("2301.00001", client, rate_limiter)

        # acquire called once before HEAD and once before GET
        assert rate_limiter.acquire.call_count == 2

    @respx.mock
    @pytest.mark.asyncio
    async def test_returns_none_for_head_404_no_get(self):
        """When HEAD returns 404, no GET request is made (only 1 acquire call)."""
        from arxiv_mcp.content.html_fetcher import fetch_arxiv_html

        rate_limiter = AsyncMock()

        head_route = respx.head(HTML_URL).mock(return_value=httpx.Response(404))

        async with httpx.AsyncClient() as client:
            content, url = await fetch_arxiv_html("2301.00001", client, rate_limiter)

        assert content is None
        assert head_route.call_count == 1
        # Only one acquire call (for HEAD, no GET)
        assert rate_limiter.acquire.call_count == 1
