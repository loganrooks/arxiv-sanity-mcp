"""Tests for Pydantic schemas: paper schemas and cursor pagination.

Covers PaperVersion, PaperSummary, PaperDetail, SearchResult,
Cursor encode/decode, PageInfo, and PaginatedResponse.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from arxiv_mcp.models.pagination import Cursor, PageInfo, PaginatedResponse
from arxiv_mcp.models.paper import PaperDetail, PaperSummary, PaperVersion, SearchResult


class TestPaperVersionSchema:
    def test_paper_version_schema(self):
        """PaperVersion validates version string, date, optional size/source_type."""
        v = PaperVersion(
            version="v1",
            date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            size="45kb",
            source_type="tex",
        )
        assert v.version == "v1"
        assert v.date.year == 2023
        assert v.size == "45kb"
        assert v.source_type == "tex"

    def test_paper_version_minimal(self):
        """PaperVersion works with only required fields."""
        v = PaperVersion(
            version="v2",
            date=datetime(2023, 6, 15, tzinfo=timezone.utc),
        )
        assert v.version == "v2"
        assert v.size is None
        assert v.source_type is None


class TestPaperSummarySchema:
    def test_paper_summary_schema(self):
        """PaperSummary has all rich result fields."""
        ps = PaperSummary(
            arxiv_id="2301.00001",
            title="Attention Is All You Need",
            authors_text="Vaswani et al.",
            abstract_snippet="The dominant sequence transduction models...",
            categories="cs.CL cs.AI",
            primary_category="cs.CL",
            category_list=["cs.CL", "cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=datetime(2023, 6, 15, tzinfo=timezone.utc),
            announced_date=date(2023, 1, 2),
            oai_datestamp=date(2023, 6, 15),
            latest_version=2,
            license_uri="http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
        )
        assert ps.arxiv_id == "2301.00001"
        assert ps.title == "Attention Is All You Need"
        assert ps.primary_category == "cs.CL"
        assert ps.category_list == ["cs.CL", "cs.AI"]
        assert ps.latest_version == 2

    def test_paper_summary_from_attributes(self):
        """PaperSummary supports from_attributes for ORM conversion."""
        # Simulate an ORM-like object with attribute access
        class FakePaper:
            arxiv_id = "2301.00001"
            title = "Test Paper"
            authors_text = "Author One"
            abstract = "A" * 500  # Long abstract
            categories = "cs.AI"
            primary_category = "cs.AI"
            category_list = ["cs.AI"]
            submitted_date = datetime(2023, 1, 1, tzinfo=timezone.utc)
            updated_date = None
            announced_date = None
            oai_datestamp = date(2023, 1, 1)
            latest_version = 1
            license_uri = None

        summary = PaperSummary.from_orm_paper(FakePaper())
        assert summary.arxiv_id == "2301.00001"
        assert len(summary.abstract_snippet) <= 303  # 300 + "..."

    def test_paper_summary_nullable_fields(self):
        """PaperSummary allows nullable optional fields."""
        ps = PaperSummary(
            arxiv_id="2301.00001",
            title="Test",
            authors_text="Author",
            abstract_snippet="Test abstract",
            categories="cs.AI",
            primary_category="cs.AI",
            category_list=["cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 1),
            latest_version=None,
            license_uri=None,
        )
        assert ps.updated_date is None
        assert ps.announced_date is None
        assert ps.latest_version is None


class TestPaperDetailSchema:
    def test_paper_detail_schema(self):
        """PaperDetail extends PaperSummary with full abstract, version_history, etc."""
        pd = PaperDetail(
            arxiv_id="2301.00001",
            title="Attention Is All You Need",
            authors_text="Vaswani et al.",
            abstract_snippet="The dominant sequence...",
            abstract="The dominant sequence transduction models are based on...",
            categories="cs.CL cs.AI",
            primary_category="cs.CL",
            category_list=["cs.CL", "cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 1),
            latest_version=2,
            license_uri="http://arxiv.org/licenses/nonexclusive-distrib/1.0/",
            version_history=[
                PaperVersion(version="v1", date=datetime(2023, 1, 1, tzinfo=timezone.utc)),
                PaperVersion(version="v2", date=datetime(2023, 6, 15, tzinfo=timezone.utc)),
            ],
            doi="10.48550/arXiv.2301.00001",
            comments="15 pages",
            journal_ref=None,
            report_no=None,
            source="oai_pmh",
            fetched_at=datetime(2023, 7, 1, tzinfo=timezone.utc),
            processing_tier=0,
            promotion_reason=None,
            openalex_id=None,
            semantic_scholar_id=None,
        )
        assert pd.abstract is not None
        assert len(pd.version_history) == 2
        assert pd.doi == "10.48550/arXiv.2301.00001"
        assert pd.source == "oai_pmh"
        assert pd.processing_tier == 0


class TestSearchResultSchema:
    def test_search_result_schema(self):
        """SearchResult wraps PaperSummary with score."""
        ps = PaperSummary(
            arxiv_id="2301.00001",
            title="Test",
            authors_text="Author",
            abstract_snippet="Abstract",
            categories="cs.AI",
            primary_category="cs.AI",
            category_list=["cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 1),
            latest_version=1,
            license_uri=None,
        )
        sr = SearchResult(paper=ps, score=0.85)
        assert sr.paper.arxiv_id == "2301.00001"
        assert sr.score == 0.85

    def test_search_result_no_score(self):
        """SearchResult works with no score (browse mode)."""
        ps = PaperSummary(
            arxiv_id="2301.00001",
            title="Test",
            authors_text="Author",
            abstract_snippet="Abstract",
            categories="cs.AI",
            primary_category="cs.AI",
            category_list=["cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 1),
            latest_version=1,
            license_uri=None,
        )
        sr = SearchResult(paper=ps, score=None)
        assert sr.score is None


class TestCursorEncodeDecode:
    def test_cursor_encode_decode(self):
        """Cursor(sort_value, paper_id) round-trips through base64 encode/decode."""
        original = Cursor(sort_value="2023-01-15", paper_id="2301.00001")
        token = original.encode()
        assert isinstance(token, str)
        assert len(token) > 0

        decoded = Cursor.decode(token)
        assert decoded.sort_value == "2023-01-15"
        assert decoded.paper_id == "2301.00001"

    def test_cursor_encode_with_float_score(self):
        """Cursor works with float score as sort_value."""
        original = Cursor(sort_value="0.95234", paper_id="2301.00042")
        token = original.encode()
        decoded = Cursor.decode(token)
        assert decoded.sort_value == "0.95234"
        assert decoded.paper_id == "2301.00042"

    def test_cursor_invalid_token(self):
        """Cursor.decode with garbage input raises ValueError."""
        with pytest.raises(ValueError):
            Cursor.decode("not-valid-base64!@#$")

    def test_cursor_invalid_json(self):
        """Cursor.decode with valid base64 but invalid JSON raises ValueError."""
        import base64

        bad_token = base64.urlsafe_b64encode(b"not json").decode()
        with pytest.raises(ValueError):
            Cursor.decode(bad_token)


class TestPageInfo:
    def test_page_info(self):
        """PageInfo has has_next, next_cursor, total_estimate."""
        pi = PageInfo(has_next=True, next_cursor="abc123", total_estimate=1500)
        assert pi.has_next is True
        assert pi.next_cursor == "abc123"
        assert pi.total_estimate == 1500

    def test_page_info_no_next(self):
        """PageInfo with no next page."""
        pi = PageInfo(has_next=False, next_cursor=None, total_estimate=10)
        assert pi.has_next is False
        assert pi.next_cursor is None


class TestPaginatedResponse:
    def test_paginated_response(self):
        """PaginatedResponse is generic over item type, contains items + page_info."""
        pi = PageInfo(has_next=False, next_cursor=None, total_estimate=2)

        ps1 = PaperSummary(
            arxiv_id="2301.00001",
            title="Paper 1",
            authors_text="Author 1",
            abstract_snippet="Abstract 1",
            categories="cs.AI",
            primary_category="cs.AI",
            category_list=["cs.AI"],
            submitted_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 1),
            latest_version=1,
            license_uri=None,
        )
        sr1 = SearchResult(paper=ps1, score=0.9)

        ps2 = PaperSummary(
            arxiv_id="2301.00002",
            title="Paper 2",
            authors_text="Author 2",
            abstract_snippet="Abstract 2",
            categories="cs.LG",
            primary_category="cs.LG",
            category_list=["cs.LG"],
            submitted_date=datetime(2023, 1, 2, tzinfo=timezone.utc),
            updated_date=None,
            announced_date=None,
            oai_datestamp=date(2023, 1, 2),
            latest_version=1,
            license_uri=None,
        )
        sr2 = SearchResult(paper=ps2, score=0.7)

        response = PaginatedResponse[SearchResult](
            items=[sr1, sr2],
            page_info=pi,
        )
        assert len(response.items) == 2
        assert response.items[0].paper.arxiv_id == "2301.00001"
        assert response.page_info.has_next is False
        assert response.page_info.total_estimate == 2
