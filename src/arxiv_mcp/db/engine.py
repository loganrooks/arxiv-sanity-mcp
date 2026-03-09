"""Async database engine and session factory.

Provides a configured SQLAlchemy async engine and session factory
for use throughout the application.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(url: str, **kwargs) -> AsyncEngine:
    """Create an async SQLAlchemy engine with sensible pool defaults.

    Args:
        url: Database connection URL (postgresql+asyncpg://...).
        **kwargs: Additional engine options passed to create_async_engine.
    """
    defaults = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_pre_ping": True,
        "echo": False,
    }
    defaults.update(kwargs)
    return create_async_engine(url, **defaults)


def session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create a session factory bound to the given engine.

    Args:
        engine: The async engine to bind sessions to.
    """
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@asynccontextmanager
async def get_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Async context manager yielding a database session.

    Commits on successful exit, rolls back on exception.
    """
    factory = session_factory(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
