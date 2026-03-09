"""Test fixtures for ingestion tests.

Loads sample XML files and provides parsed lxml elements
for use in parser and harvester tests.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from lxml import etree

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"

# OAI-PMH namespace
OAI_NS = "http://www.openarchives.org/OAI/2.0/"


def _load_xml_fixture(filename: str) -> etree._Element:
    """Load an XML fixture file and return the parsed root element."""
    filepath = FIXTURES_DIR / filename
    tree = etree.parse(str(filepath))
    return tree.getroot()


def _extract_metadata_element(record_element: etree._Element) -> etree._Element:
    """Extract the metadata child element from an OAI-PMH record.

    The OAI-PMH record wraps metadata in <metadata>/<format-specific-element>.
    This returns the format-specific element (e.g., arXivRaw, arXiv, oai_dc:dc).
    """
    ns = {"oai": OAI_NS}
    metadata = record_element.find("oai:metadata", ns)
    if metadata is None:
        raise ValueError("No <metadata> element found in record")
    # Return the first child of <metadata>
    children = list(metadata)
    if not children:
        raise ValueError("No metadata format element found inside <metadata>")
    return children[0]


@pytest.fixture
def arxiv_raw_element() -> etree._Element:
    """Parsed arXivRaw metadata element from sample XML."""
    record = _load_xml_fixture("arxiv_raw_sample.xml")
    return _extract_metadata_element(record)


@pytest.fixture
def arxiv_format_element() -> etree._Element:
    """Parsed arXiv format metadata element from sample XML."""
    record = _load_xml_fixture("arxiv_format_sample.xml")
    return _extract_metadata_element(record)


@pytest.fixture
def oai_dc_element() -> etree._Element:
    """Parsed oai_dc metadata element from sample XML."""
    record = _load_xml_fixture("oai_dc_sample.xml")
    return _extract_metadata_element(record)


@pytest.fixture
def arxiv_raw_record_element() -> etree._Element:
    """Full OAI-PMH record element (including header) for arXivRaw format."""
    return _load_xml_fixture("arxiv_raw_sample.xml")
