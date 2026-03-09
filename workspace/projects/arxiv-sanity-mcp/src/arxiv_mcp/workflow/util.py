"""Workflow utility functions.

Provides helper functions used across workflow modules,
including slug generation for collection and query names.
"""

from __future__ import annotations

import re


def slugify(text: str) -> str:
    """Convert text to URL-safe slug (lowercase, hyphens, no spaces).

    Examples:
        slugify("My Reading List") -> "my-reading-list"
        slugify("  Spaces & Symbols!  ") -> "spaces-symbols"
    """
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")
