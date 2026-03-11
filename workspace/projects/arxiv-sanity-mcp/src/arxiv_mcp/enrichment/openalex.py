"""OpenAlex enrichment adapter with DOI-based resolution and rate limiting.

Implements the EnrichmentAdapter protocol for OpenAlex API. Uses DOI-based
resolution (arXiv DOI prefix 10.48550/arXiv.{id}) for ID lookup. Singleton
endpoints are FREE (0 credits); batch filter costs 10 credits per call.
"""

from __future__ import annotations

import asyncio
import random
import time
from typing import Protocol

import httpx
import structlog

from arxiv_mcp.config import Settings
from arxiv_mcp.enrichment.models import (
    EnrichmentResult,
    EnrichmentStatus,
    ExternalIds,
)

logger = structlog.get_logger(__name__)

# Fields to request via select= parameter to reduce response payload
SELECTED_FIELDS = ",".join([
    "id",
    "doi",
    "ids",
    "type",
    "is_retracted",
    "cited_by_count",
    "fwci",
    "citation_normalized_percentile",
    "primary_topic",
    "topics",
    "related_works",
    "counts_by_year",
    "open_access",
    "indexed_in",
    "authorships",
])


class EnrichmentAdapter(Protocol):
    """Protocol for enrichment source adapters."""

    @property
    def adapter_name(self) -> str:
        """Name identifying this adapter (e.g., 'openalex')."""
        ...

    async def resolve_ids(self, arxiv_ids: list[str]) -> dict[str, ExternalIds]:
        """Resolve arXiv IDs to external identifiers."""
        ...

    async def enrich(self, arxiv_ids: list[str]) -> list[EnrichmentResult]:
        """Fetch enrichment data for papers by arXiv ID."""
        ...


class RateLimiter:
    """Simple rate limiter using monotonic clock and asyncio.sleep."""

    def __init__(self, requests_per_second: float = 5.0) -> None:
        self._min_interval = 1.0 / requests_per_second
        self._last_request_time: float = 0.0

    async def acquire(self) -> None:
        """Wait until rate limit allows next request."""
        elapsed = time.monotonic() - self._last_request_time
        remaining = self._min_interval - elapsed
        if remaining > 0:
            await asyncio.sleep(remaining)
        self._last_request_time = time.monotonic()


class OpenAlexAdapter:
    """OpenAlex API adapter with DOI-based resolution and rate limiting.

    Uses singleton endpoint (FREE) for single papers and batch filter
    (10 credits) for multiple papers. Rate limits requests and handles
    429 responses with exponential backoff.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._rate_limiter = RateLimiter(settings.enrichment_rate_limit)

    @property
    def adapter_name(self) -> str:
        return "openalex"

    @staticmethod
    def _build_doi(arxiv_id: str) -> str:
        """Build arXiv DOI from arXiv ID."""
        return f"10.48550/arXiv.{arxiv_id}"

    def _build_params(self) -> dict:
        """Build base request parameters with api_key, mailto, and select."""
        params: dict[str, str] = {"select": SELECTED_FIELDS}
        if self._settings.openalex_api_key:
            params["api_key"] = self._settings.openalex_api_key
        if self._settings.openalex_email:
            params["mailto"] = self._settings.openalex_email
        return params

    def _build_user_agent(self) -> str:
        """Build User-Agent header, including mailto for OpenAlex polite pool."""
        user_agent = "arxiv-mcp/0.1.0"
        if self._settings.openalex_email:
            user_agent += f" (mailto:{self._settings.openalex_email})"
        return user_agent

    async def _request_with_retry(
        self,
        client: httpx.AsyncClient,
        url: str,
        params: dict,
        max_retries: int = 3,
        base_delay: float = 0.1,
    ) -> httpx.Response:
        """Make request with exponential backoff on 429 responses.

        Calls rate_limiter.acquire() before each request attempt.
        Raises httpx.HTTPStatusError on non-429/non-404 errors.
        Returns the response (caller handles 404).
        """
        for attempt in range(max_retries + 1):
            await self._rate_limiter.acquire()
            response = await client.get(url, params=params)

            if response.status_code == 429 and attempt < max_retries:
                delay = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                logger.warning(
                    "rate_limited",
                    attempt=attempt + 1,
                    max_retries=max_retries,
                    delay=delay,
                )
                await asyncio.sleep(delay)
                continue

            # Return 404 responses (caller handles not-found)
            if response.status_code == 404:
                return response

            # Raise on other error statuses
            if response.status_code >= 400:
                response.raise_for_status()

            return response

        # Final 429 after all retries exhausted
        response.raise_for_status()
        return response  # unreachable but satisfies type checker

    async def resolve_ids(self, arxiv_ids: list[str]) -> dict[str, ExternalIds]:
        """Resolve arXiv IDs to external identifiers.

        For a single ID: uses singleton endpoint (FREE, 0 credits).
        For multiple IDs: uses batch filter endpoint (10 credits per call).
        """
        result: dict[str, ExternalIds] = {}

        async with httpx.AsyncClient(
            base_url=self._settings.openalex_api_url,
            headers={"User-Agent": self._build_user_agent()},
            timeout=30.0,
        ) as client:
            if len(arxiv_ids) == 1:
                arxiv_id = arxiv_ids[0]
                result.update(await self._resolve_singleton(client, arxiv_id))
            else:
                result.update(await self._resolve_batch(client, arxiv_ids))

        return result

    async def _resolve_singleton(
        self, client: httpx.AsyncClient, arxiv_id: str
    ) -> dict[str, ExternalIds]:
        """Resolve a single arXiv ID via singleton DOI endpoint."""
        doi = self._build_doi(arxiv_id)
        params = self._build_params()
        url = f"/works/doi:{doi}"

        try:
            response = await self._request_with_retry(client, url, params)
        except (httpx.TimeoutException, httpx.ConnectError):
            return {arxiv_id: ExternalIds(openalex_id=None, doi=None)}

        if response.status_code == 404:
            return {arxiv_id: ExternalIds(openalex_id=None, doi=None)}

        work = response.json()
        return {
            arxiv_id: ExternalIds(
                openalex_id=work.get("id"),
                doi=work.get("doi"),
            )
        }

    async def _resolve_batch(
        self, client: httpx.AsyncClient, arxiv_ids: list[str]
    ) -> dict[str, ExternalIds]:
        """Resolve multiple arXiv IDs via batch filter endpoint."""
        result: dict[str, ExternalIds] = {}
        batch_size = self._settings.enrichment_batch_size

        for i in range(0, len(arxiv_ids), batch_size):
            chunk = arxiv_ids[i : i + batch_size]
            chunk_result = await self._resolve_batch_chunk(client, chunk)
            result.update(chunk_result)

        return result

    async def _resolve_batch_chunk(
        self, client: httpx.AsyncClient, arxiv_ids: list[str]
    ) -> dict[str, ExternalIds]:
        """Resolve a chunk of arXiv IDs via batch filter."""
        # Build pipe-separated DOI filter
        dois = "|".join(
            f"https://doi.org/{self._build_doi(aid)}" for aid in arxiv_ids
        )
        params = self._build_params()
        params["filter"] = f"doi:{dois}"
        params["per_page"] = "100"

        try:
            response = await self._request_with_retry(client, "/works", params)
        except (httpx.TimeoutException, httpx.ConnectError):
            return {aid: ExternalIds(openalex_id=None, doi=None) for aid in arxiv_ids}

        data = response.json()
        results_list = data.get("results", [])

        # Build DOI -> arXiv ID mapping for result matching
        doi_to_arxiv: dict[str, str] = {}
        for aid in arxiv_ids:
            doi_lower = f"https://doi.org/{self._build_doi(aid)}".lower()
            doi_to_arxiv[doi_lower] = aid

        result: dict[str, ExternalIds] = {}
        matched_arxiv_ids: set[str] = set()

        for work in results_list:
            work_doi = (work.get("doi") or "").lower()
            arxiv_id = doi_to_arxiv.get(work_doi)
            if arxiv_id:
                result[arxiv_id] = ExternalIds(
                    openalex_id=work.get("id"),
                    doi=work.get("doi"),
                )
                matched_arxiv_ids.add(arxiv_id)

        # Any unmatched IDs get empty ExternalIds
        for aid in arxiv_ids:
            if aid not in matched_arxiv_ids:
                result[aid] = ExternalIds(openalex_id=None, doi=None)

        return result

    async def enrich(self, arxiv_ids: list[str]) -> list[EnrichmentResult]:
        """Fetch enrichment data for papers by arXiv ID.

        For a single ID: uses singleton GET endpoint (FREE, 0 credits).
        For multiple IDs: uses batch filter endpoint (10 credits per call).
        Chunks batch requests to max enrichment_batch_size.
        """
        async with httpx.AsyncClient(
            base_url=self._settings.openalex_api_url,
            headers={"User-Agent": self._build_user_agent()},
            timeout=30.0,
        ) as client:
            if len(arxiv_ids) == 1:
                return [await self._enrich_singleton(client, arxiv_ids[0])]
            else:
                return await self._enrich_batch(client, arxiv_ids)

    async def _enrich_singleton(
        self, client: httpx.AsyncClient, arxiv_id: str
    ) -> EnrichmentResult:
        """Enrich a single paper via singleton DOI endpoint (FREE)."""
        doi = self._build_doi(arxiv_id)
        params = self._build_params()
        url = f"/works/doi:{doi}"

        try:
            response = await self._request_with_retry(client, url, params)
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            return EnrichmentResult(
                status=EnrichmentStatus.ERROR,
                error_detail=str(exc),
            )
        except httpx.HTTPStatusError as exc:
            return EnrichmentResult(
                status=EnrichmentStatus.ERROR,
                error_detail=f"HTTP {exc.response.status_code}: {exc.response.text}",
            )

        if response.status_code == 404:
            return EnrichmentResult(status=EnrichmentStatus.NOT_FOUND)

        work = response.json()
        return EnrichmentResult.from_openalex_work(work)

    async def _enrich_batch(
        self, client: httpx.AsyncClient, arxiv_ids: list[str]
    ) -> list[EnrichmentResult]:
        """Enrich multiple papers via batch filter endpoint."""
        all_results: list[EnrichmentResult] = []
        batch_size = self._settings.enrichment_batch_size

        for i in range(0, len(arxiv_ids), batch_size):
            chunk = arxiv_ids[i : i + batch_size]
            chunk_results = await self._enrich_batch_chunk(client, chunk)
            all_results.extend(chunk_results)

        return all_results

    async def _enrich_batch_chunk(
        self, client: httpx.AsyncClient, arxiv_ids: list[str]
    ) -> list[EnrichmentResult]:
        """Enrich a chunk of papers via batch filter."""
        dois = "|".join(
            f"https://doi.org/{self._build_doi(aid)}" for aid in arxiv_ids
        )
        params = self._build_params()
        params["filter"] = f"doi:{dois}"
        params["per_page"] = "100"

        try:
            response = await self._request_with_retry(client, "/works", params)
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            return [
                EnrichmentResult(
                    status=EnrichmentStatus.ERROR,
                    error_detail=str(exc),
                )
                for _ in arxiv_ids
            ]
        except httpx.HTTPStatusError as exc:
            return [
                EnrichmentResult(
                    status=EnrichmentStatus.ERROR,
                    error_detail=f"HTTP {exc.response.status_code}",
                )
                for _ in arxiv_ids
            ]

        data = response.json()
        results_list = data.get("results", [])

        # Build DOI -> arXiv ID mapping
        doi_to_arxiv: dict[str, str] = {}
        for aid in arxiv_ids:
            doi_lower = f"https://doi.org/{self._build_doi(aid)}".lower()
            doi_to_arxiv[doi_lower] = aid

        # Parse results and match to arXiv IDs
        matched: dict[str, EnrichmentResult] = {}
        for work in results_list:
            work_doi = (work.get("doi") or "").lower()
            arxiv_id = doi_to_arxiv.get(work_doi)
            if arxiv_id:
                matched[arxiv_id] = EnrichmentResult.from_openalex_work(work)

        # Build ordered results list, marking unmatched as not_found
        results: list[EnrichmentResult] = []
        for aid in arxiv_ids:
            if aid in matched:
                results.append(matched[aid])
            else:
                results.append(EnrichmentResult(status=EnrichmentStatus.NOT_FOUND))

        return results
