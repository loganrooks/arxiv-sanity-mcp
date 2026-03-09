"""SQLAlchemy ORM models for arxiv-mcp.

Paper model and supporting types are defined here. The Base
declarative class is imported by alembic/env.py for autogenerate.
"""

from __future__ import annotations

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# Paper model will be added in Task 2
