"""Tests for RightsChecker license classification and access decisions.

Covers all 6 arXiv license URIs x 2 deployment modes + None license.
Tests both permissive and personal-use license classifications, and
verifies that local mode always allows access (with warnings) while
hosted mode blocks non-permissive licenses.
"""

from __future__ import annotations

import pytest

from arxiv_mcp.content.rights import RightsChecker


# All 6 arXiv license URIs
CC_BY_40 = "http://creativecommons.org/licenses/by/4.0/"
CC_BY_SA_40 = "http://creativecommons.org/licenses/by-sa/4.0/"
CC0_10 = "http://creativecommons.org/publicdomain/zero/1.0/"
ARXIV_NONEXCLUSIVE = "http://arxiv.org/licenses/nonexclusive-distrib/1.0/"
CC_BY_NC_SA_40 = "http://creativecommons.org/licenses/by-nc-sa/4.0/"
CC_BY_NC_ND_40 = "http://creativecommons.org/licenses/by-nc-nd/4.0/"


@pytest.fixture
def checker():
    return RightsChecker()


class TestPermissiveLicensesHostedMode:
    """Permissive licenses should allow access in hosted mode without warning."""

    def test_cc_by_40_hosted(self, checker):
        d = checker.check_access(CC_BY_40, "hosted")
        assert d.allowed is True
        assert d.warning is None

    def test_cc_by_sa_40_hosted(self, checker):
        d = checker.check_access(CC_BY_SA_40, "hosted")
        assert d.allowed is True
        assert d.warning is None

    def test_cc0_10_hosted(self, checker):
        d = checker.check_access(CC0_10, "hosted")
        assert d.allowed is True
        assert d.warning is None


class TestPermissiveLicensesLocalMode:
    """Permissive licenses should allow access in local mode with informational warning."""

    def test_cc_by_40_local(self, checker):
        d = checker.check_access(CC_BY_40, "local")
        assert d.allowed is True
        assert d.warning is not None

    def test_cc_by_sa_40_local(self, checker):
        d = checker.check_access(CC_BY_SA_40, "local")
        assert d.allowed is True
        assert d.warning is not None

    def test_cc0_10_local(self, checker):
        d = checker.check_access(CC0_10, "local")
        assert d.allowed is True
        assert d.warning is not None


class TestPersonalUseLicensesHostedMode:
    """Non-permissive licenses should block access in hosted mode."""

    def test_arxiv_nonexclusive_hosted(self, checker):
        d = checker.check_access(ARXIV_NONEXCLUSIVE, "hosted")
        assert d.allowed is False
        assert d.reason is not None

    def test_cc_by_nc_sa_40_hosted(self, checker):
        d = checker.check_access(CC_BY_NC_SA_40, "hosted")
        assert d.allowed is False
        assert d.reason is not None

    def test_cc_by_nc_nd_40_hosted(self, checker):
        d = checker.check_access(CC_BY_NC_ND_40, "hosted")
        assert d.allowed is False
        assert d.reason is not None


class TestPersonalUseLicensesLocalMode:
    """Non-permissive licenses should allow access in local mode with warning."""

    def test_arxiv_nonexclusive_local(self, checker):
        d = checker.check_access(ARXIV_NONEXCLUSIVE, "local")
        assert d.allowed is True
        assert d.warning is not None

    def test_cc_by_nc_sa_40_local(self, checker):
        d = checker.check_access(CC_BY_NC_SA_40, "local")
        assert d.allowed is True
        assert d.warning is not None

    def test_cc_by_nc_nd_40_local(self, checker):
        d = checker.check_access(CC_BY_NC_ND_40, "local")
        assert d.allowed is True
        assert d.warning is not None


class TestNoneLicense:
    """None license (unknown) should be treated as restrictive."""

    def test_none_license_hosted(self, checker):
        d = checker.check_access(None, "hosted")
        assert d.allowed is False
        assert d.reason is not None

    def test_none_license_local(self, checker):
        d = checker.check_access(None, "local")
        assert d.allowed is True
        assert d.warning is not None


class TestUnknownLicense:
    """Unknown license URI should be treated as restrictive."""

    def test_unknown_license_hosted(self, checker):
        d = checker.check_access("http://example.com/unknown-license", "hosted")
        assert d.allowed is False
        assert d.reason is not None

    def test_unknown_license_local(self, checker):
        d = checker.check_access("http://example.com/unknown-license", "local")
        assert d.allowed is True
        assert d.warning is not None
