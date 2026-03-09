"""XML parsers for arXiv OAI-PMH metadata formats.

Parses three OAI-PMH metadata formats:
- arXivRaw: Full metadata with version history (primary harvest format)
- arXiv: Structured authors with keyname/forenames
- oai_dc: Minimal Dublin Core fallback

All parsers produce RawPaperMetadata dataclass instances for uniform
downstream processing by the mapper.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from lxml import etree

# Namespace constants
ARXIV_RAW_NS = "http://arxiv.org/OAI/arXivRaw/"
ARXIV_NS = "http://arxiv.org/OAI/arXiv/"
OAI_DC_NS = "http://www.openarchives.org/OAI/2.0/oai_dc/"
DC_NS = "http://purl.org/dc/elements/1.1/"


@dataclass
class PaperVersion:
    """A single version of an arXiv paper."""

    version: str  # "v1", "v2", etc.
    date: str  # Date string from arXiv
    size: str | None = None
    source_type: str | None = None


@dataclass
class RawPaperMetadata:
    """Raw parsed metadata from any OAI-PMH format.

    All three parsers produce this dataclass. Fields may be None
    depending on the format used (oai_dc provides fewer fields).
    """

    arxiv_id: str
    submitter: str | None = None
    versions: list[PaperVersion] = field(default_factory=list)
    categories: str = ""
    title: str | None = None
    authors: str | None = None
    abstract: str | None = None
    comments: str | None = None
    journal_ref: str | None = None
    doi: str | None = None
    license: str | None = None
    report_no: str | None = None
    acm_class: str | None = None
    msc_class: str | None = None
    oai_datestamp: str | None = None

    # Derived fields
    submission_date: str | None = None  # v1 date
    update_date: str | None = None  # Latest version date
    primary_category: str | None = None  # First in categories list


def _text(element: etree._Element | None) -> str | None:
    """Extract text content from an XML element, stripping whitespace."""
    if element is None:
        return None
    text = element.text
    if text is None:
        return None
    return text.strip()


def parse_arxiv_raw(xml_element: etree._Element) -> RawPaperMetadata:
    """Parse arXivRaw OAI-PMH metadata format.

    This is the primary harvest format, providing full metadata
    including version history with per-version dates and sizes.

    Args:
        xml_element: The <arXivRaw> element from OAI-PMH response.

    Returns:
        RawPaperMetadata with all available fields populated.
    """
    ns = {"ar": ARXIV_RAW_NS}

    arxiv_id = _text(xml_element.find("ar:id", ns)) or ""
    submitter = _text(xml_element.find("ar:submitter", ns))
    title = _text(xml_element.find("ar:title", ns))
    authors = _text(xml_element.find("ar:authors", ns))
    categories = _text(xml_element.find("ar:categories", ns)) or ""
    abstract = _text(xml_element.find("ar:abstract", ns))
    comments = _text(xml_element.find("ar:comments", ns))
    journal_ref = _text(xml_element.find("ar:journal-ref", ns))
    doi = _text(xml_element.find("ar:doi", ns))
    license_uri = _text(xml_element.find("ar:license", ns))
    report_no = _text(xml_element.find("ar:report-no", ns))
    acm_class = _text(xml_element.find("ar:acm-class", ns))
    msc_class = _text(xml_element.find("ar:msc-class", ns))

    # Parse version history
    versions: list[PaperVersion] = []
    for ver_el in xml_element.findall("ar:version", ns):
        ver_attr = ver_el.get("version", "")
        date_text = _text(ver_el.find("ar:date", ns))
        size_text = _text(ver_el.find("ar:size", ns))
        source_type_text = _text(ver_el.find("ar:source_type", ns))
        versions.append(
            PaperVersion(
                version=ver_attr,
                date=date_text or "",
                size=size_text,
                source_type=source_type_text,
            )
        )

    # Derive time fields from version history
    submission_date = versions[0].date if versions else None
    update_date = versions[-1].date if len(versions) > 1 else None

    # Primary category is first in space-separated list
    primary_category = categories.split()[0] if categories else None

    return RawPaperMetadata(
        arxiv_id=arxiv_id,
        submitter=submitter,
        versions=versions,
        categories=categories,
        title=title,
        authors=authors,
        abstract=abstract,
        comments=comments,
        journal_ref=journal_ref,
        doi=doi,
        license=license_uri,
        report_no=report_no,
        acm_class=acm_class,
        msc_class=msc_class,
        submission_date=submission_date,
        update_date=update_date,
        primary_category=primary_category,
    )


def parse_arxiv_format(xml_element: etree._Element) -> RawPaperMetadata:
    """Parse arXiv OAI-PMH metadata format.

    This format provides structured author data (keyname, forenames,
    suffix, affiliation) and created/updated dates directly.

    Args:
        xml_element: The <arXiv> element from OAI-PMH response.

    Returns:
        RawPaperMetadata with structured author string.
    """
    ns = {"ax": ARXIV_NS}

    arxiv_id = _text(xml_element.find("ax:id", ns)) or ""
    title = _text(xml_element.find("ax:title", ns))
    categories = _text(xml_element.find("ax:categories", ns)) or ""
    abstract = _text(xml_element.find("ax:abstract", ns))
    comments = _text(xml_element.find("ax:comments", ns))
    journal_ref = _text(xml_element.find("ax:journal-ref", ns))
    doi = _text(xml_element.find("ax:doi", ns))
    license_uri = _text(xml_element.find("ax:license", ns))

    created = _text(xml_element.find("ax:created", ns))
    updated = _text(xml_element.find("ax:updated", ns))

    # Parse structured authors
    author_parts: list[str] = []
    authors_el = xml_element.find("ax:authors", ns)
    if authors_el is not None:
        for author_el in authors_el.findall("ax:author", ns):
            keyname = _text(author_el.find("ax:keyname", ns)) or ""
            forenames = _text(author_el.find("ax:forenames", ns)) or ""
            suffix = _text(author_el.find("ax:suffix", ns))
            name_parts = []
            if forenames:
                name_parts.append(forenames)
            if keyname:
                name_parts.append(keyname)
            if suffix:
                name_parts.append(suffix)
            author_parts.append(" ".join(name_parts))

    authors = ", ".join(author_parts) if author_parts else None

    # Primary category is first in space-separated list
    primary_category = categories.split()[0] if categories else None

    return RawPaperMetadata(
        arxiv_id=arxiv_id,
        categories=categories,
        title=title,
        authors=authors,
        abstract=abstract,
        comments=comments,
        journal_ref=journal_ref,
        doi=doi,
        license=license_uri,
        submission_date=created,
        update_date=updated,
        primary_category=primary_category,
    )


def parse_oai_dc(xml_element: etree._Element) -> RawPaperMetadata:
    """Parse oai_dc (Dublin Core) OAI-PMH metadata format.

    This is the minimal fallback format. Provides title, creator(s),
    subject(s), date, description, and identifier.

    Args:
        xml_element: The <oai_dc:dc> element from OAI-PMH response.

    Returns:
        RawPaperMetadata with available DC fields mapped.
    """
    ns = {"dc": DC_NS}

    title = _text(xml_element.find("dc:title", ns))
    description = _text(xml_element.find("dc:description", ns))
    date_str = _text(xml_element.find("dc:date", ns))
    identifier = _text(xml_element.find("dc:identifier", ns))

    # Extract arXiv ID from identifier URL
    arxiv_id = ""
    if identifier:
        # Format: http://arxiv.org/abs/2301.00001
        parts = identifier.rstrip("/").split("/")
        if parts:
            arxiv_id = parts[-1]

    # Collect all creators
    creators = [
        _text(el) for el in xml_element.findall("dc:creator", ns) if _text(el)
    ]
    authors = ", ".join(creators) if creators else None

    # Collect all subjects as space-separated categories
    subjects = [
        _text(el) for el in xml_element.findall("dc:subject", ns) if _text(el)
    ]
    categories = " ".join(subjects)

    # Primary category is first subject
    primary_category = subjects[0] if subjects else None

    return RawPaperMetadata(
        arxiv_id=arxiv_id,
        categories=categories,
        title=title,
        authors=authors,
        abstract=description,
        submission_date=date_str,
        primary_category=primary_category,
    )
