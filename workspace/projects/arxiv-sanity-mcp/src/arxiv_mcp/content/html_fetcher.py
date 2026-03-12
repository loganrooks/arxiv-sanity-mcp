"""arXiv HTML fetching with sanitization and rate limiting.

Fetches arXiv HTML5 renderings (ar5iv) for papers, extracts the
article content, and strips navigation/header/footer elements.
Handles 404 gracefully for papers without HTML versions.
"""

from __future__ import annotations

import httpx
import structlog
from bs4 import BeautifulSoup

logger = structlog.get_logger(__name__)


async def fetch_arxiv_html(
    arxiv_id: str,
    client: httpx.AsyncClient,
    rate_limiter,
) -> tuple[str | None, str | None]:
    """Fetch and sanitize arXiv HTML for a paper.

    Performs HEAD request first to check availability, then GET to
    retrieve content. Strips nav/header/footer elements and extracts
    the article/main/body container.

    Args:
        arxiv_id: The arXiv paper ID.
        client: httpx.AsyncClient for making requests.
        rate_limiter: Rate limiter with async acquire() method.

    Returns:
        Tuple of (html_content, source_url) or (None, None) if unavailable.
    """
    url = f"https://arxiv.org/html/{arxiv_id}"

    try:
        # HEAD request to check availability
        await rate_limiter.acquire()
        head_response = await client.head(url)

        if head_response.status_code == 404:
            logger.debug("html_not_available", arxiv_id=arxiv_id)
            return None, None

        if head_response.status_code >= 400:
            logger.warning(
                "html_head_error",
                arxiv_id=arxiv_id,
                status=head_response.status_code,
            )
            return None, None

        # GET the full HTML
        await rate_limiter.acquire()
        response = await client.get(url)
        response.raise_for_status()

    except httpx.TimeoutException:
        logger.warning("html_fetch_timeout", arxiv_id=arxiv_id)
        return None, None
    except httpx.HTTPStatusError as exc:
        logger.warning(
            "html_fetch_error",
            arxiv_id=arxiv_id,
            status=exc.response.status_code,
        )
        return None, None

    # Parse and extract content
    soup = BeautifulSoup(response.text, "lxml")

    # Find content container: article > main > body
    container = soup.find("article") or soup.find("main") or soup.find("body")

    if container is None:
        logger.warning("html_no_container", arxiv_id=arxiv_id)
        return None, None

    # Strip navigation, header, and footer elements
    for tag_name in ("nav", "header", "footer"):
        for tag in container.find_all(tag_name):
            tag.decompose()

    return str(container), url
