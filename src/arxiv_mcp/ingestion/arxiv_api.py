"""arXiv search API client for targeted paper retrieval.

Provides single-paper fetch by ID and fielded search queries
against the arXiv Atom API, with built-in rate limiting.
"""

from __future__ import annotations

import asyncio
import re
import time

import httpx
import structlog
from lxml import etree

from arxiv_mcp.config import Settings
from arxiv_mcp.ingestion.parsers import RawPaperMetadata

logger = structlog.get_logger(__name__)

# Atom feed namespaces
ATOM_NS = "http://www.w3.org/2005/Atom"
OPENSEARCH_NS = "http://a9.com/-/spec/opensearch/1.1/"
ARXIV_NS = "http://arxiv.org/schemas/atom"

NS = {
    "atom": ATOM_NS,
    "opensearch": OPENSEARCH_NS,
    "arxiv": ARXIV_NS,
}

# Regex to extract arXiv ID from URL
ARXIV_ID_RE = re.compile(r"(?:arxiv\.org/abs/)?(\d{4}\.\d{4,5})(?:v\d+)?$")


def _text(element: etree._Element | None) -> str | None:
    """Extract text content from an XML element."""
    if element is None:
        return None
    text = element.text
    if text is None:
        return None
    return text.strip()


def _extract_arxiv_id(id_url: str) -> str:
    """Extract arXiv ID from Atom entry id URL.

    Format: http://arxiv.org/abs/2301.00001v2 -> 2301.00001
    """
    match = ARXIV_ID_RE.search(id_url)
    if match:
        return match.group(1)
    # Fallback: take the last path component and strip version
    parts = id_url.rstrip("/").split("/")
    raw_id = parts[-1]
    # Strip version suffix like v1, v2
    return re.sub(r"v\d+$", "", raw_id)


def parse_atom_entry(entry: etree._Element) -> RawPaperMetadata:
    """Parse an Atom entry element into RawPaperMetadata.

    The arXiv API returns Atom feed format. Each <entry> contains:
    - id (URL with arxiv_id)
    - title, summary (abstract)
    - author(s) with name and optional affiliation
    - arxiv:primary_category, category[]
    - published, updated
    - arxiv:doi, arxiv:comment, arxiv:journal_ref

    Args:
        entry: An Atom <entry> element.

    Returns:
        RawPaperMetadata with available fields populated.
    """
    # Extract arXiv ID from id URL
    id_url = _text(entry.find("atom:id", NS)) or ""
    arxiv_id = _extract_arxiv_id(id_url)

    title = _text(entry.find("atom:title", NS))
    abstract = _text(entry.find("atom:summary", NS))
    published = _text(entry.find("atom:published", NS))
    updated = _text(entry.find("atom:updated", NS))

    # Authors
    author_names = []
    for author_el in entry.findall("atom:author", NS):
        name = _text(author_el.find("atom:name", NS))
        if name:
            author_names.append(name)
    authors = ", ".join(author_names) if author_names else None

    # Primary category
    primary_cat_el = entry.find("arxiv:primary_category", NS)
    primary_category = primary_cat_el.get("term") if primary_cat_el is not None else None

    # All categories
    categories_list = []
    for cat_el in entry.findall("atom:category", NS):
        term = cat_el.get("term")
        if term:
            categories_list.append(term)
    categories = " ".join(categories_list)

    # Ensure primary_category is first if not already
    if primary_category and primary_category not in categories_list:
        categories = primary_category + " " + categories if categories else primary_category

    # arXiv-specific fields
    doi = _text(entry.find("arxiv:doi", NS))
    comment = _text(entry.find("arxiv:comment", NS))
    journal_ref = _text(entry.find("arxiv:journal_ref", NS))

    return RawPaperMetadata(
        arxiv_id=arxiv_id,
        title=title,
        authors=authors,
        abstract=abstract,
        categories=categories,
        primary_category=primary_category,
        submission_date=published,
        update_date=updated,
        doi=doi,
        comments=comment,
        journal_ref=journal_ref,
    )


class ArxivAPIClient:
    """Client for the arXiv search API (Atom feed).

    Provides single-paper fetch and fielded search with
    built-in rate limiting to respect arXiv's policies.
    """

    def __init__(self, settings: Settings):
        self.base_url = settings.arxiv_api_url
        self.rate_limit = settings.harvest_rate_limit
        self._last_request_time: float = 0

    def _calculate_delay(self) -> float:
        """Calculate remaining delay needed before next request."""
        if self.rate_limit <= 0:
            return 0.0
        elapsed = time.monotonic() - self._last_request_time
        remaining = self.rate_limit - elapsed
        return max(0.0, remaining)

    async def _request(self, params: dict) -> bytes:
        """Make a rate-limited request to arXiv API.

        Args:
            params: Query parameters for the API request.

        Returns:
            Response body as bytes.
        """
        # Enforce rate limiting
        delay = self._calculate_delay()
        if delay > 0:
            await asyncio.sleep(delay)

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(self.base_url, params=params)
            response.raise_for_status()
            self._last_request_time = time.monotonic()
            return response.content

    async def fetch_paper(self, arxiv_id: str) -> RawPaperMetadata | None:
        """Fetch a single paper by arXiv ID.

        Args:
            arxiv_id: The arXiv identifier (e.g., '2301.00001').

        Returns:
            Parsed metadata or None if not found.
        """
        params = {"id_list": arxiv_id}
        content = await self._request(params)

        root = etree.fromstring(content)
        entries = root.findall("atom:entry", NS)

        if not entries:
            return None

        return parse_atom_entry(entries[0])

    async def search(
        self,
        query: str,
        start: int = 0,
        max_results: int = 100,
    ) -> list[RawPaperMetadata]:
        """Search arXiv API with query string.

        Supports fielded search (ti:, au:, abs:, cat:) and
        Boolean operators (AND, OR, ANDNOT).

        Args:
            query: Search query string.
            start: Starting index for pagination.
            max_results: Maximum results to return (up to 2000).

        Returns:
            List of parsed metadata results.
        """
        params = {
            "search_query": query,
            "start": str(start),
            "max_results": str(max_results),
        }
        content = await self._request(params)

        root = etree.fromstring(content)
        entries = root.findall("atom:entry", NS)

        results = []
        for entry in entries:
            try:
                results.append(parse_atom_entry(entry))
            except Exception as exc:
                logger.warning("Failed to parse Atom entry", error=str(exc))

        return results
