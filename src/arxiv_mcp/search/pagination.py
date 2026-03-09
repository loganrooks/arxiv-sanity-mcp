"""Keyset cursor pagination applied to search query results.

Provides utilities for building PageInfo from query results and
encoding cursor state for stable pagination.
"""

from __future__ import annotations

from typing import Any

from arxiv_mcp.models.pagination import Cursor, PageInfo


def build_page_info(
    items: list[Any],
    page_size: int,
    sort_value_extractor,
    id_extractor=lambda item: item.arxiv_id,
) -> tuple[list[Any], PageInfo]:
    """Build PageInfo from a list that may contain one extra item.

    The query should have fetched page_size + 1 items. If we got more
    than page_size, there's a next page and we trim the extra item.

    Args:
        items: List of result items (may have page_size + 1 entries).
        page_size: The requested page size.
        sort_value_extractor: Callable to extract sort value from last item for cursor.
        id_extractor: Callable to extract paper_id from last item for cursor.

    Returns:
        Tuple of (trimmed items list, PageInfo).
    """
    if len(items) > page_size:
        # More items than requested -- there's a next page
        trimmed = items[:page_size]
        has_next = True
    else:
        trimmed = items
        has_next = len(items) == page_size  # Edge case: exactly page_size could mean more

    # Actually, if we queried for page_size + 1 and got <= page_size, no next page
    has_next = len(items) > page_size
    trimmed = items[:page_size]

    next_cursor = None
    if has_next and trimmed:
        last = trimmed[-1]
        sort_val = sort_value_extractor(last)
        paper_id = id_extractor(last)
        cursor = Cursor(sort_value=str(sort_val), paper_id=str(paper_id))
        next_cursor = cursor.encode()

    return trimmed, PageInfo(has_next=has_next, next_cursor=next_cursor)
