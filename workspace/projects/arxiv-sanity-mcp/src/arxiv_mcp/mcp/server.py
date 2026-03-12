"""FastMCP server with lifespan-managed services.

Creates the async engine, session factory, and all service instances
during startup. Disposes the engine on shutdown. Tool modules register
themselves via import side-effects at module bottom.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from arxiv_mcp.config import Settings, get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.enrichment.service import EnrichmentService
from arxiv_mcp.interest.profiles import ProfileService
from arxiv_mcp.search.service import SearchService
from arxiv_mcp.workflow.collections import CollectionService
from arxiv_mcp.workflow.queries import SavedQueryService
from arxiv_mcp.workflow.triage import TriageService
from arxiv_mcp.workflow.watches import WatchService


@dataclass
class AppContext:
    """Application context holding engine, session factory, settings, and all services."""

    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    settings: Settings
    search: SearchService
    collections: CollectionService
    triage: TriageService
    saved_queries: SavedQueryService
    watches: WatchService
    profiles: ProfileService
    enrichment: EnrichmentService


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Create DB engine, session factory, and all services; dispose on shutdown."""
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)

    # SearchService first -- SavedQueryService and WatchService depend on it
    search = SearchService(sf, settings)
    collections = CollectionService(sf, settings)
    triage = TriageService(sf, settings)
    saved_queries = SavedQueryService(sf, settings, search)
    watches = WatchService(sf, settings, search)
    profiles = ProfileService(sf, settings)
    enrichment = EnrichmentService(sf, settings)

    try:
        yield AppContext(
            engine=engine,
            session_factory=sf,
            settings=settings,
            search=search,
            collections=collections,
            triage=triage,
            saved_queries=saved_queries,
            watches=watches,
            profiles=profiles,
            enrichment=enrichment,
        )
    finally:
        await engine.dispose()


mcp = FastMCP("arxiv-mcp", lifespan=app_lifespan)

# Register tool modules (side-effect imports)
from arxiv_mcp.mcp.tools import discovery  # noqa: F401, E402
