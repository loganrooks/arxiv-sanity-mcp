"""Signal validation and author name normalization.

Provides validation for interest signal types and values,
and author name normalization for consistent storage.
"""

from __future__ import annotations

import re

VALID_SIGNAL_TYPES = {"seed_paper", "saved_query", "followed_author", "negative_example"}
VALID_SIGNAL_STATUSES = {"active", "pending", "dismissed"}


def normalize_author(name: str) -> str:
    """Normalize an author name: lowercase and collapse whitespace.

    Examples:
        normalize_author("  John  DOE ") -> "john doe"
        normalize_author("") -> ""
    """
    name = name.strip().lower()
    name = re.sub(r"\s+", " ", name)
    return name


def parse_authors(authors_text: str) -> list[str]:
    """Parse comma-separated author names into a list of normalized strings.

    Examples:
        parse_authors("John Doe, Jane Smith") -> ["john doe", "jane smith"]
    """
    if not authors_text.strip():
        return []
    return [normalize_author(a) for a in authors_text.split(",") if a.strip()]


def validate_signal(signal_type: str, signal_value: str) -> str:
    """Validate a signal type and normalize the value.

    For followed_author signals, the value is normalized via normalize_author.
    For all other valid types, the value is returned unchanged.

    Args:
        signal_type: One of VALID_SIGNAL_TYPES.
        signal_value: The signal value to validate/normalize.

    Returns:
        The (possibly normalized) signal value.

    Raises:
        ValueError: If signal_type is not in VALID_SIGNAL_TYPES.
    """
    if signal_type not in VALID_SIGNAL_TYPES:
        raise ValueError(
            f"Invalid signal type: {signal_type!r}. "
            f"Must be one of: {', '.join(sorted(VALID_SIGNAL_TYPES))}"
        )

    if signal_type == "followed_author":
        return normalize_author(signal_value)

    return signal_value
