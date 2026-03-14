"""Tests for XML parsers and metadata mapper.

Tests cover parsing of arXivRaw, arXiv, and oai_dc OAI-PMH formats,
and mapping parsed metadata to Paper ORM instances.
"""

from __future__ import annotations


from arxiv_mcp.ingestion.parsers import (
    RawPaperMetadata,
    parse_arxiv_format,
    parse_arxiv_raw,
    parse_oai_dc,
)
from arxiv_mcp.ingestion.mapper import map_to_paper
from arxiv_mcp.db.models import Paper, ProcessingTier


# --- arXivRaw parser tests ---


class TestParseArxivRaw:
    """Tests for parse_arxiv_raw()."""

    def test_parse_arxiv_raw_basic(self, arxiv_raw_element):
        """Parse arXivRaw XML element, extract core fields."""
        result = parse_arxiv_raw(arxiv_raw_element)

        assert isinstance(result, RawPaperMetadata)
        assert result.arxiv_id == "2301.00001"
        assert result.title == "Attention Is All You Need: A Revisitation"
        assert "Ashish Vaswani" in result.authors
        assert "Noam Shazeer" in result.authors
        assert result.categories == "cs.CL cs.AI cs.LG"
        assert result.license == "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"
        assert "Transformer" in result.abstract
        assert result.submitter == "Ashish Vaswani"
        assert result.doi == "10.48550/arXiv.2301.00001"
        assert result.comments == "15 pages, 5 figures"
        assert result.journal_ref == "Journal of Machine Learning Research, 2023"
        assert result.report_no == "TR-2023-001"
        assert result.acm_class == "I.2.7"
        assert result.msc_class == "68T05"

    def test_parse_arxiv_raw_versions(self, arxiv_raw_element):
        """Parse version history from arXivRaw."""
        result = parse_arxiv_raw(arxiv_raw_element)

        assert len(result.versions) == 2
        assert result.versions[0].version == "v1"
        assert "Jan 2023" in result.versions[0].date
        assert result.versions[0].size == "45kb"
        assert result.versions[0].source_type == "D"
        assert result.versions[1].version == "v2"
        assert result.versions[1].size == "48kb"

    def test_parse_arxiv_raw_time_derivation(self, arxiv_raw_element):
        """Submission date is v1 date, updated is latest version date."""
        result = parse_arxiv_raw(arxiv_raw_element)

        # submission_date derived from v1
        assert result.submission_date is not None
        assert "Jan 2023" in result.submission_date

        # update_date derived from latest version (v2)
        assert result.update_date is not None
        assert "Jun 2023" in result.update_date

        # primary_category is first in categories list
        assert result.primary_category == "cs.CL"


# --- arXiv format parser tests ---


class TestParseArxivFormat:
    """Tests for parse_arxiv_format()."""

    def test_parse_arxiv_format_authors(self, arxiv_format_element):
        """Parse arXiv format structured authors."""
        result = parse_arxiv_format(arxiv_format_element)

        assert isinstance(result, RawPaperMetadata)
        assert result.arxiv_id == "2301.00001"
        assert result.title == "Attention Is All You Need: A Revisitation"
        # Structured author string should contain all authors
        assert "Vaswani" in result.authors
        assert "Shazeer" in result.authors
        assert "Parmar" in result.authors
        assert "Uszkoreit" in result.authors
        assert result.categories == "cs.CL cs.AI cs.LG"
        assert result.primary_category == "cs.CL"

        # arXiv format has created/updated dates directly
        assert result.submission_date is not None
        assert result.update_date is not None


# --- oai_dc parser tests ---


class TestParseOaiDc:
    """Tests for parse_oai_dc()."""

    def test_parse_oai_dc(self, oai_dc_element):
        """Parse minimal oai_dc format (fallback)."""
        result = parse_oai_dc(oai_dc_element)

        assert isinstance(result, RawPaperMetadata)
        assert result.arxiv_id == "2301.00001"
        assert result.title == "Attention Is All You Need: A Revisitation"
        # oai_dc authors are from dc:creator elements
        assert "Vaswani" in result.authors
        assert "Shazeer" in result.authors
        assert result.categories == "cs.CL cs.AI cs.LG"
        assert "Transformer" in result.abstract


# --- Mapper tests ---


class TestMapper:
    """Tests for map_to_paper()."""

    def test_mapper_to_paper(self, arxiv_raw_element):
        """Map RawPaperMetadata to Paper ORM instance with all fields populated."""
        raw = parse_arxiv_raw(arxiv_raw_element)
        paper = map_to_paper(raw)

        assert isinstance(paper, Paper)
        assert paper.arxiv_id == "2301.00001"
        assert paper.title == "Attention Is All You Need: A Revisitation"
        assert "Ashish Vaswani" in paper.authors_text
        assert "Transformer" in paper.abstract
        assert paper.categories == "cs.CL cs.AI cs.LG"
        assert paper.primary_category == "cs.CL"
        assert paper.processing_tier == ProcessingTier.FTS_INDEXED
        assert paper.source == "oai_pmh"
        assert paper.doi == "10.48550/arXiv.2301.00001"
        assert paper.license_uri == "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"
        assert paper.fetched_at is not None
        assert paper.submitted_date is not None
        assert paper.updated_date is not None
        assert paper.latest_version == 2
        assert isinstance(paper.version_history, list)
        assert len(paper.version_history) == 2

    def test_mapper_category_list(self, arxiv_raw_element):
        """Mapper splits space-separated categories into category_list array."""
        raw = parse_arxiv_raw(arxiv_raw_element)
        paper = map_to_paper(raw)

        assert paper.category_list == ["cs.CL", "cs.AI", "cs.LG"]

    def test_mapper_handles_missing_fields(self):
        """Mapper handles None/missing optional fields gracefully."""
        raw = RawPaperMetadata(
            arxiv_id="9901.00001",
            submitter="Test Author",
            versions=[],
            categories="cs.AI",
            title="Minimal Paper",
            authors="Test Author",
        )
        paper = map_to_paper(raw)

        assert isinstance(paper, Paper)
        assert paper.arxiv_id == "9901.00001"
        assert paper.doi is None
        assert paper.license_uri is None
        assert paper.comments is None
        assert paper.journal_ref is None
        assert paper.report_no is None
        assert paper.version_history == []
        assert paper.primary_category == "cs.AI"
        assert paper.category_list == ["cs.AI"]
