"""Tests for OAI-PMH harvester.

Tests cover bulk and incremental harvesting, category filtering,
batch upsert, and checkpoint management. External services (Scythe,
database) are mocked.
"""

from __future__ import annotations

import json
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from lxml import etree

from arxiv_mcp.config import Settings
from arxiv_mcp.ingestion.oai_pmh import HarvestResult, OAIPMHHarvester


# --- Helper to create mock OAI-PMH records ---

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def _make_mock_record(arxiv_id: str = "2301.00001", categories: str = "cs.CL cs.AI") -> MagicMock:
    """Create a mock oaipmh-scythe Record with arXivRaw XML metadata."""
    # Build minimal arXivRaw XML
    raw_ns = "http://arxiv.org/OAI/arXivRaw/"
    root = etree.Element(f"{{{raw_ns}}}arXivRaw", nsmap={"ar": raw_ns})

    def _add(tag, text):
        el = etree.SubElement(root, f"{{{raw_ns}}}{tag}")
        el.text = text

    _add("id", arxiv_id)
    _add("submitter", "Test Author")
    _add("title", f"Test Paper {arxiv_id}")
    _add("authors", "Test Author, Another Author")
    _add("categories", categories)
    _add("abstract", "This is a test abstract for testing purposes.")
    _add("license", "http://arxiv.org/licenses/nonexclusive-distrib/1.0/")

    # Add a version
    ver = etree.SubElement(root, f"{{{raw_ns}}}version", attrib={"version": "v1"})
    date_el = etree.SubElement(ver, f"{{{raw_ns}}}date")
    date_el.text = "Mon, 2 Jan 2023 12:00:00 GMT"
    size_el = etree.SubElement(ver, f"{{{raw_ns}}}size")
    size_el.text = "45kb"

    record = MagicMock()
    record.metadata = root
    record.header = MagicMock()
    record.header.datestamp = "2023-01-02"
    record.header.identifier = f"oai:arXiv.org:{arxiv_id}"
    return record


def _make_settings(**overrides) -> Settings:
    """Create test settings with sensible defaults."""
    defaults = {
        "database_url": "postgresql+asyncpg://test:test@localhost/test",
        "test_database_url": "postgresql+asyncpg://test:test@localhost/test",
        "arxiv_oai_url": "https://oaipmh.arxiv.org/oai",
        "harvest_rate_limit": 0.0,  # No delay in tests
        "categories_file": "data/categories.toml",
    }
    defaults.update(overrides)
    return Settings(**defaults)


class TestHarvestBulk:
    """Tests for OAIPMHHarvester.harvest_bulk()."""

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_bulk_calls_scythe(self, mock_scythe_cls):
        """Bulk harvest invokes Scythe.list_records with correct params."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_scythe.list_records.return_value = iter([])

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(settings=settings, session_factory=mock_session_factory)

        await harvester.harvest_bulk(
            archive_set="cs",
            metadata_prefix="arXivRaw",
        )

        mock_scythe.list_records.assert_called_once()
        call_kwargs = mock_scythe.list_records.call_args
        assert call_kwargs[1]["metadataPrefix"] == "arXivRaw"
        assert call_kwargs[1]["set"] == "cs"

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_bulk_parses_records(self, mock_scythe_cls):
        """Bulk harvest passes each record through parse_arxiv_raw and map_to_paper."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        records = [_make_mock_record("2301.00001"), _make_mock_record("2301.00002")]
        mock_scythe.list_records.return_value = iter(records)

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(settings=settings, session_factory=mock_session_factory)
        harvester._upsert_batch = AsyncMock()

        result = await harvester.harvest_bulk()

        assert result.total_fetched == 2

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_bulk_upserts(self, mock_scythe_cls):
        """Papers are inserted with upsert logic for cross-listing dedup."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        records = [_make_mock_record("2301.00001")]
        mock_scythe.list_records.return_value = iter(records)

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(settings=settings, session_factory=mock_session_factory)
        harvester._upsert_batch = AsyncMock()

        await harvester.harvest_bulk(batch_size=1)

        harvester._upsert_batch.assert_called()
        # Check that Paper objects were passed to upsert
        call_args = harvester._upsert_batch.call_args
        papers = call_args[0][0]
        assert len(papers) == 1
        assert papers[0].arxiv_id == "2301.00001"

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_filters_categories(self, mock_scythe_cls):
        """Harvested papers are filtered to configured category subset."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        # One paper in cs.CL (configured), one in q-bio.PE (not configured)
        records = [
            _make_mock_record("2301.00001", "cs.CL cs.AI"),
            _make_mock_record("2301.00002", "q-bio.PE"),
        ]
        mock_scythe.list_records.return_value = iter(records)

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(settings=settings, session_factory=mock_session_factory)
        harvester._upsert_batch = AsyncMock()

        result = await harvester.harvest_bulk(batch_size=100)

        assert result.total_fetched == 2
        assert result.total_skipped >= 1  # q-bio.PE should be skipped

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_batch_insert(self, mock_scythe_cls):
        """Papers are inserted in configurable batch sizes."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        records = [_make_mock_record(f"2301.{i:05d}") for i in range(5)]
        mock_scythe.list_records.return_value = iter(records)

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(settings=settings, session_factory=mock_session_factory)
        harvester._upsert_batch = AsyncMock()

        await harvester.harvest_bulk(batch_size=2)

        # 5 papers with batch_size=2 should give 3 upsert calls (2, 2, 1)
        assert harvester._upsert_batch.call_count == 3


class TestHarvestIncremental:
    """Tests for incremental harvesting with checkpoint management."""

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_incremental_uses_from_date(self, mock_scythe_cls, tmp_path):
        """Incremental harvest passes from parameter matching last checkpoint date."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        mock_scythe.list_records.return_value = iter([])

        # Write a checkpoint file
        checkpoint_path = tmp_path / "harvest_checkpoint.json"
        checkpoint_path.write_text(json.dumps({
            "last_datestamp": "2023-06-01",
            "last_run": "2023-06-02T00:00:00Z",
        }))

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(
            settings=settings,
            session_factory=mock_session_factory,
            checkpoint_path=checkpoint_path,
        )

        await harvester.harvest_incremental()

        call_kwargs = mock_scythe.list_records.call_args[1]
        assert call_kwargs["from"] == "2023-06-01"

    @patch("arxiv_mcp.ingestion.oai_pmh.Scythe")
    async def test_harvest_incremental_saves_checkpoint(self, mock_scythe_cls, tmp_path):
        """After successful harvest, the latest datestamp is saved as checkpoint."""
        mock_scythe = MagicMock()
        mock_scythe_cls.return_value.__enter__ = MagicMock(return_value=mock_scythe)
        mock_scythe_cls.return_value.__exit__ = MagicMock(return_value=False)
        records = [_make_mock_record("2301.00001")]
        mock_scythe.list_records.return_value = iter(records)

        checkpoint_path = tmp_path / "harvest_checkpoint.json"

        settings = _make_settings()
        mock_session_factory = AsyncMock()
        harvester = OAIPMHHarvester(
            settings=settings,
            session_factory=mock_session_factory,
            checkpoint_path=checkpoint_path,
        )
        harvester._upsert_batch = AsyncMock()

        await harvester.harvest_incremental()

        assert checkpoint_path.exists()
        checkpoint = json.loads(checkpoint_path.read_text())
        assert "last_datestamp" in checkpoint
        assert "last_run" in checkpoint
