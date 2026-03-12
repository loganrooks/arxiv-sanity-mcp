"""Content conversion adapters for PDF-to-markdown conversion.

Defines the ContentAdapter protocol and concrete implementations:
- MarkerAdapter: wraps Marker PdfConverter for GPU/CPU PDF parsing
- MockContentAdapter: test double with call tracking and configurable results

Follows the EnrichmentAdapter pattern from enrichment/openalex.py.
"""

from __future__ import annotations

import asyncio
from typing import Protocol

import structlog

from arxiv_mcp.config import Settings
from arxiv_mcp.content.models import ContentConversionResult

logger = structlog.get_logger(__name__)


class ContentAdapter(Protocol):
    """Protocol for content conversion adapters.

    Any PDF-to-markdown backend must implement this protocol.
    Mirrors EnrichmentAdapter: adapter_name property + async method.
    """

    @property
    def adapter_name(self) -> str:
        """Name identifying this adapter (e.g., 'marker', 'docling')."""
        ...

    async def convert(
        self, pdf_path: str, arxiv_id: str
    ) -> ContentConversionResult:
        """Convert a PDF file to markdown text.

        Args:
            pdf_path: Path to the PDF file on disk.
            arxiv_id: arXiv ID for logging and result tracking.

        Returns:
            ContentConversionResult with content, backend, version, warnings.
        """
        ...


class MarkerAdapter:
    """Marker PDF-to-markdown adapter using PdfConverter.

    Initializes Marker's PdfConverter once in __init__ (not per-call)
    and wraps the synchronous conversion in asyncio.to_thread for
    non-blocking operation. Falls back to CPU if CUDA is unavailable.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._converter = None
        self._version = "unknown"
        self._init_converter()

    def _init_converter(self) -> None:
        """Initialize Marker PdfConverter with GPU fallback to CPU."""
        try:
            from marker.converters.pdf import PdfConverter
            from marker.models import create_model_dict

            try:
                self._converter = PdfConverter(artifact_dict=create_model_dict())
                logger.info("marker_initialized", device="auto")
            except Exception as exc:
                logger.warning(
                    "marker_gpu_fallback",
                    error=str(exc),
                    fallback="cpu",
                )
                # Attempt CPU fallback
                import os

                os.environ["TORCH_DEVICE"] = "cpu"
                self._converter = PdfConverter(artifact_dict=create_model_dict())

            self._version = self._get_version()
        except ImportError:
            logger.warning("marker_not_installed", msg="Marker package not available")
            self._converter = None

    @property
    def adapter_name(self) -> str:
        return "marker"

    async def convert(
        self, pdf_path: str, arxiv_id: str
    ) -> ContentConversionResult:
        """Convert PDF to markdown using Marker PdfConverter.

        Uses asyncio.to_thread to offload the blocking conversion.
        """
        if self._converter is None:
            return ContentConversionResult(
                content="",
                backend="marker",
                backend_version=self._version,
                extraction_method="pdf_parse",
                quality_warnings=["marker_not_available"],
            )

        logger.info("marker_converting", arxiv_id=arxiv_id, pdf_path=pdf_path)

        rendered = await asyncio.to_thread(self._converter, pdf_path)
        text = rendered.markdown

        warnings = self._detect_warnings(text)

        return ContentConversionResult(
            content=text,
            backend="marker",
            backend_version=self._version,
            extraction_method="pdf_parse",
            quality_warnings=warnings,
        )

    def _detect_warnings(self, text: str) -> list[str]:
        """Detect quality issues in converted text.

        Checks for:
        - very_short_output: less than 500 characters
        - math_heavy: more than 30% non-ASCII characters
        - no_structure_detected: no markdown heading lines
        """
        warnings: list[str] = []

        if len(text) < 500:
            warnings.append("very_short_output")

        if text:
            non_ascii = sum(1 for c in text if ord(c) > 127)
            if non_ascii / len(text) > 0.30:
                warnings.append("math_heavy")

        if not any(line.lstrip().startswith("#") for line in text.splitlines()):
            warnings.append("no_structure_detected")

        return warnings

    def _get_version(self) -> str:
        """Get Marker package version."""
        try:
            import marker

            return getattr(marker, "__version__", "unknown")
        except ImportError:
            return "unknown"


class MockContentAdapter:
    """Test double for ContentAdapter with call tracking.

    Mirrors MockAdapter from enrichment tests. Tracks convert calls
    and returns predetermined or default results.
    """

    adapter_name = "mock_marker"

    def __init__(
        self, results: dict[str, ContentConversionResult] | None = None
    ) -> None:
        self._results = results or {}
        self.convert_calls: list[tuple[str, str]] = []

    async def convert(
        self, pdf_path: str, arxiv_id: str
    ) -> ContentConversionResult:
        """Return predetermined result or default mock content.

        Tracks each call as (pdf_path, arxiv_id) tuple for assertion.
        """
        self.convert_calls.append((pdf_path, arxiv_id))

        if arxiv_id in self._results:
            return self._results[arxiv_id]

        return ContentConversionResult(
            content=f"Mock markdown content for {arxiv_id}. "
            "This is a simulated PDF conversion result with "
            "sufficient length to avoid quality warnings.",
            backend="mock_marker",
            backend_version="0.0.0",
            extraction_method="pdf_parse",
            quality_warnings=[],
        )
