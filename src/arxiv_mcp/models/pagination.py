"""Cursor-based pagination schemas.

Provides keyset cursor encoding/decoding (base64 URL-safe) and
pagination metadata models. Uses compound cursor (sort_value, paper_id)
for stable pagination across insertions.
"""

from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


@dataclass
class Cursor:
    """Keyset cursor for pagination.

    Encodes the last-seen (sort_value, paper_id) pair as a base64
    URL-safe token. The paper_id serves as a tiebreaker for stable
    ordering when multiple papers share the same sort_value.
    """

    sort_value: str  # ISO date string or float score as string
    paper_id: str  # arXiv ID as tiebreaker

    def encode(self) -> str:
        """Encode cursor as base64 URL-safe string."""
        payload = json.dumps([self.sort_value, self.paper_id])
        return base64.urlsafe_b64encode(payload.encode()).decode()

    @classmethod
    def decode(cls, token: str) -> Cursor:
        """Decode a cursor token back to a Cursor instance.

        Args:
            token: Base64 URL-safe encoded cursor string.

        Raises:
            ValueError: If the token is malformed or cannot be decoded.
        """
        try:
            raw = base64.urlsafe_b64decode(token.encode())
            data = json.loads(raw)
            if not isinstance(data, list) or len(data) != 2:
                raise ValueError("Cursor payload must be a 2-element list")
            sort_value, paper_id = data
            return cls(sort_value=str(sort_value), paper_id=str(paper_id))
        except (json.JSONDecodeError, UnicodeDecodeError, Exception) as e:
            if isinstance(e, ValueError):
                raise
            raise ValueError(f"Invalid cursor token: {e}") from e


class PageInfo(BaseModel):
    """Pagination metadata for a result page."""

    has_next: bool
    next_cursor: str | None = None
    total_estimate: int | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapping a list of items with page info."""

    items: list[T]
    page_info: PageInfo
