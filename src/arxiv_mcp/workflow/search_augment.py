"""Workflow-aware search augmentation service.

Wraps SearchService to post-process results with triage state and
collection context per paper. Does NOT modify Phase 1's SearchService
or query builders (compose by wrapping, not by editing).
"""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Collection, CollectionPaper, TriageState
from arxiv_mcp.models.pagination import PaginatedResponse
from arxiv_mcp.models.paper import SearchResult, WorkflowSearchResult
from arxiv_mcp.search.service import SearchService


class WorkflowSearchService:
    """Wraps SearchService with triage state and collection context enrichment.

    Post-processes search/browse results using two batch queries
    (triage states + collection memberships) to avoid N+1. Does not
    modify Phase 1's query builders or SearchService.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
        search_service: SearchService,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings
        self.search_service = search_service

    async def search_papers(self, **kwargs) -> PaginatedResponse[WorkflowSearchResult]:
        """Delegates to SearchService, then enriches results with workflow state."""
        result = await self.search_service.search_papers(**kwargs)
        return await self._augment_results(result)

    async def browse_recent(self, **kwargs) -> PaginatedResponse[WorkflowSearchResult]:
        """Delegates to SearchService, then enriches results with workflow state."""
        result = await self.search_service.browse_recent(**kwargs)
        return await self._augment_results(result)

    async def _augment_results(
        self, result: PaginatedResponse[SearchResult]
    ) -> PaginatedResponse[WorkflowSearchResult]:
        """Batch-fetch triage states and collection memberships for all papers."""
        if not result.items:
            return PaginatedResponse[WorkflowSearchResult](
                items=[], page_info=result.page_info
            )

        paper_ids = [item.paper.arxiv_id for item in result.items]

        async with self.session_factory() as session:
            triage_map = await self._get_triage_states(session, paper_ids)
            collection_map = await self._get_collection_memberships(
                session, paper_ids
            )

        augmented = []
        for item in result.items:
            pid = item.paper.arxiv_id
            augmented.append(
                WorkflowSearchResult(
                    paper=item.paper,
                    score=item.score,
                    triage_state=triage_map.get(pid, "unseen"),
                    collection_slugs=collection_map.get(pid, []),
                )
            )

        return PaginatedResponse[WorkflowSearchResult](
            items=augmented, page_info=result.page_info
        )

    async def _get_triage_states(
        self, session: AsyncSession, paper_ids: list[str]
    ) -> dict[str, str]:
        """Batch query: triage states for all paper_ids.

        Returns mapping {paper_id: state}. Missing papers default to "unseen".
        """
        stmt = select(TriageState.paper_id, TriageState.state).where(
            TriageState.paper_id.in_(paper_ids)
        )
        result = await session.execute(stmt)
        return {row.paper_id: row.state for row in result.all()}

    async def _get_collection_memberships(
        self, session: AsyncSession, paper_ids: list[str]
    ) -> dict[str, list[str]]:
        """Batch query: collection memberships for all paper_ids.

        Returns mapping {paper_id: [collection_slug, ...]}.
        """
        stmt = (
            select(CollectionPaper.paper_id, Collection.slug)
            .join(Collection, Collection.id == CollectionPaper.collection_id)
            .where(CollectionPaper.paper_id.in_(paper_ids))
        )
        result = await session.execute(stmt)

        memberships: dict[str, list[str]] = defaultdict(list)
        for row in result.all():
            memberships[row.paper_id].append(row.slug)

        return dict(memberships)
