"""Tests for content Pydantic models and VariantType/ContentStatus enums.

Covers:
- VariantType enum values (4 variant types)
- ContentStatus enum values (4 statuses)
- AccessDecision model construction and field defaults
- ContentConversionResult model construction and field defaults
- ContentVariant ORM model structure (composite PK, columns, constraints)
"""

from __future__ import annotations

import enum

import pytest
from sqlalchemy import inspect

from arxiv_mcp.content.models import (
    AccessDecision,
    ContentConversionResult,
    ContentStatus,
    VariantType,
)
from arxiv_mcp.db.models import ContentVariant


class TestVariantType:
    """VariantType enum has exactly 4 values."""

    def test_variant_type_values(self):
        assert VariantType.ABSTRACT == "abstract"
        assert VariantType.HTML == "html"
        assert VariantType.SOURCE_DERIVED == "source_derived"
        assert VariantType.PDF_MARKDOWN == "pdf_markdown"

    def test_variant_type_count(self):
        assert len(VariantType) == 4

    def test_variant_type_is_str_enum(self):
        assert issubclass(VariantType, str)
        assert issubclass(VariantType, enum.Enum)


class TestContentStatus:
    """ContentStatus enum has exactly 4 values."""

    def test_content_status_values(self):
        assert ContentStatus.AVAILABLE == "available"
        assert ContentStatus.PENDING == "pending"
        assert ContentStatus.FAILED == "failed"
        assert ContentStatus.NOT_AVAILABLE == "not_available"

    def test_content_status_count(self):
        assert len(ContentStatus) == 4

    def test_content_status_is_str_enum(self):
        assert issubclass(ContentStatus, str)
        assert issubclass(ContentStatus, enum.Enum)


class TestAccessDecision:
    """AccessDecision Pydantic model with allowed, reason, warning."""

    def test_access_decision_allowed(self):
        d = AccessDecision(allowed=True)
        assert d.allowed is True
        assert d.reason is None
        assert d.warning is None

    def test_access_decision_denied_with_reason(self):
        d = AccessDecision(allowed=False, reason="License is non-permissive")
        assert d.allowed is False
        assert d.reason == "License is non-permissive"
        assert d.warning is None

    def test_access_decision_allowed_with_warning(self):
        d = AccessDecision(allowed=True, warning="Personal use only")
        assert d.allowed is True
        assert d.reason is None
        assert d.warning == "Personal use only"

    def test_access_decision_all_fields(self):
        d = AccessDecision(allowed=False, reason="Blocked", warning="Check license")
        assert d.allowed is False
        assert d.reason == "Blocked"
        assert d.warning == "Check license"


class TestContentConversionResult:
    """ContentConversionResult Pydantic model with required and default fields."""

    def test_content_conversion_result_required_fields(self):
        r = ContentConversionResult(
            content="# Title\n\nSome content",
            backend="marker",
            backend_version="1.0.0",
            extraction_method="pdf_to_markdown",
        )
        assert r.content == "# Title\n\nSome content"
        assert r.backend == "marker"
        assert r.backend_version == "1.0.0"
        assert r.extraction_method == "pdf_to_markdown"
        assert r.quality_warnings == []

    def test_content_conversion_result_with_warnings(self):
        r = ContentConversionResult(
            content="content",
            backend="docling",
            backend_version="2.0.0",
            extraction_method="pdf_to_markdown",
            quality_warnings=["Low OCR confidence", "Table extraction failed"],
        )
        assert len(r.quality_warnings) == 2
        assert "Low OCR confidence" in r.quality_warnings

    def test_content_conversion_result_empty_content(self):
        """Empty string is valid content (e.g. blank page)."""
        r = ContentConversionResult(
            content="",
            backend="marker",
            backend_version="1.0.0",
            extraction_method="pdf_to_markdown",
        )
        assert r.content == ""

    def test_content_conversion_result_quality_warnings_default_factory(self):
        """quality_warnings should be independent list per instance."""
        r1 = ContentConversionResult(
            content="a", backend="b", backend_version="1", extraction_method="m"
        )
        r2 = ContentConversionResult(
            content="c", backend="d", backend_version="2", extraction_method="n"
        )
        r1.quality_warnings.append("test")
        assert r2.quality_warnings == []


class TestContentVariantORM:
    """ContentVariant ORM model structure and constraints."""

    def test_tablename(self):
        assert ContentVariant.__tablename__ == "content_variants"

    def test_composite_primary_key(self):
        mapper = inspect(ContentVariant)
        pk_columns = [col.name for col in mapper.primary_key]
        assert "arxiv_id" in pk_columns
        assert "variant_type" in pk_columns
        assert len(pk_columns) == 2

    def test_has_all_provenance_columns(self):
        mapper = inspect(ContentVariant)
        column_names = [col.name for col in mapper.columns]
        expected = [
            "arxiv_id",
            "variant_type",
            "content",
            "content_hash",
            "source_url",
            "backend",
            "backend_version",
            "extraction_method",
            "license_uri",
            "quality_warnings",
            "fetched_at",
            "converted_at",
        ]
        for name in expected:
            assert name in column_names, f"Missing column: {name}"

    def test_has_check_constraint(self):
        """CHECK constraint on variant_type for 4 valid values."""
        constraints = ContentVariant.__table__.constraints
        check_constraints = [c for c in constraints if hasattr(c, "sqltext")]
        assert len(check_constraints) >= 1
        check_text = str(check_constraints[0].sqltext)
        for vt in ["abstract", "html", "source_derived", "pdf_markdown"]:
            assert vt in check_text

    def test_has_foreign_key_to_papers(self):
        """FK on arxiv_id referencing papers.arxiv_id."""
        mapper = inspect(ContentVariant)
        arxiv_id_col = mapper.columns["arxiv_id"]
        fk_targets = [fk.target_fullname for fk in arxiv_id_col.foreign_keys]
        assert "papers.arxiv_id" in fk_targets
