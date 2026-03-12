"""Profile-aware search augmentation service.

Wraps WorkflowSearchService to post-process results with profile-based
ranking. Does NOT modify Phase 2's WorkflowSearchService (compose by
wrapping, not by editing). Uses an over-fetch strategy (page_size * 3)
to compensate for re-ranking changing result order.

ProfileSearchResponse provides both the ranked results and a
RankerSnapshot capturing the ranker configuration at query time.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from arxiv_mcp.interest.ranking import (
    DEFAULT_WEIGHTS,
    ProfileContext,
    RankingPipeline,
)
from arxiv_mcp.models.interest import RankerSnapshot
from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.paper import (
    PaperSummary,
    ProfileSearchResult,
    WorkflowSearchResult,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ProfileSearchResponse
# ---------------------------------------------------------------------------


class ProfileSearchResponse(BaseModel):
    """Wraps paginated profile search results with ranker snapshot.

    Returned by ProfileRankingService to provide both the ranked
    results and the ranker configuration that produced them.
    """

    results: PaginatedResponse[ProfileSearchResult]
    ranker_snapshot: RankerSnapshot | None = None


# ---------------------------------------------------------------------------
# Over-fetch multiplier
# ---------------------------------------------------------------------------

OVERFETCH_MULTIPLIER = 3


# ---------------------------------------------------------------------------
# ProfileRankingService
# ---------------------------------------------------------------------------


class ProfileRankingService:
    """Wraps WorkflowSearchService with profile-based ranking.

    When a profile_slug is provided, over-fetches results from the base
    service, scores each paper with RankingPipeline, re-ranks by
    composite_score, and trims to the requested page_size.

    Without a profile, results pass through unchanged (backward compatible).
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession] | None,
        settings: object | None,
        workflow_search_service: object,
        *,
        _test_profile_context: ProfileContext | None = None,
    ) -> None:
        """Initialize ProfileRankingService.

        Args:
            session_factory: Async session factory for DB queries.
            settings: Application settings.
            workflow_search_service: WorkflowSearchService instance to wrap.
            _test_profile_context: Injected ProfileContext for testing
                (bypasses DB loading).
        """
        self.session_factory = session_factory
        self.settings = settings
        self.workflow_search = workflow_search_service
        self._test_profile_context = _test_profile_context

    async def search_papers(
        self,
        *,
        profile_slug: str | None = None,
        page_size: int = 20,
        **kwargs,
    ) -> ProfileSearchResponse:
        """Search papers with optional profile-based re-ranking.

        Without profile_slug, delegates to WorkflowSearchService and
        wraps results as ProfileSearchResult (no ranking explanation).

        With profile_slug:
        1. Over-fetches (page_size * 3) from base service
        2. Loads ProfileContext from DB (or test injection)
        3. Scores each paper via RankingPipeline
        4. Sorts by composite_score descending
        5. Trims to original page_size
        6. Captures RankerSnapshot

        Args:
            profile_slug: Profile to use for ranking, or None.
            page_size: Number of results to return.
            **kwargs: Passed through to WorkflowSearchService.search_papers.

        Returns:
            ProfileSearchResponse with results and optional snapshot.
        """
        if profile_slug is None:
            result = await self.workflow_search.search_papers(
                page_size=page_size, **kwargs
            )
            return self._wrap_without_ranking(result)

        return await self._ranked_search(
            method="search_papers",
            profile_slug=profile_slug,
            page_size=page_size,
            **kwargs,
        )

    async def browse_recent(
        self,
        *,
        profile_slug: str | None = None,
        page_size: int = 20,
        **kwargs,
    ) -> ProfileSearchResponse:
        """Browse recent papers with optional profile-based re-ranking.

        Same pattern as search_papers.
        """
        if profile_slug is None:
            result = await self.workflow_search.browse_recent(
                page_size=page_size, **kwargs
            )
            return self._wrap_without_ranking(result)

        return await self._ranked_search(
            method="browse_recent",
            profile_slug=profile_slug,
            page_size=page_size,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _ranked_search(
        self,
        method: str,
        profile_slug: str,
        page_size: int,
        **kwargs,
    ) -> ProfileSearchResponse:
        """Core ranked search logic shared by search_papers and browse_recent.

        Note: Pagination is approximate when profile-based re-ranking is active.
        Each page independently over-fetches N*3 results from the base service,
        re-ranks, and trims to N. This means page boundaries shift between
        requests -- a paper on page 1 could move to page 2 or vice versa on
        subsequent queries. This is a known limitation of the over-fetch +
        re-rank strategy.
        """
        # Over-fetch for re-ranking (Pitfall 2 mitigation)
        overfetch_size = page_size * OVERFETCH_MULTIPLIER
        search_fn = getattr(self.workflow_search, method)
        base_result = await search_fn(page_size=overfetch_size, **kwargs)

        # Load profile context
        profile_context = await self._load_profile_context(profile_slug)

        # Build pipeline with profile weights
        pipeline = RankingPipeline(weights=profile_context.weights or None)

        # Collect all ranks for min-max normalization
        all_ranks = [
            item.score for item in base_result.items if item.score is not None
        ]

        # Score each paper
        scored_results: list[tuple[float, ProfileSearchResult]] = []
        for item in base_result.items:
            explanation = pipeline.score_paper(
                paper=item.paper,
                query_rank=item.score,
                all_ranks=all_ranks,
                profile_context=profile_context,
            )
            profile_result = ProfileSearchResult(
                paper=item.paper,
                score=explanation.composite_score,
                triage_state=item.triage_state,
                collection_slugs=item.collection_slugs,
                ranking_explanation=explanation,
            )
            scored_results.append((explanation.composite_score, profile_result))

        # Sort by composite_score descending
        scored_results.sort(key=lambda x: x[0], reverse=True)

        # Trim to original page_size
        trimmed = [r for _, r in scored_results[:page_size]]

        # Capture snapshot
        snapshot = pipeline.capture_snapshot(profile_context=profile_context)

        return ProfileSearchResponse(
            results=PaginatedResponse[ProfileSearchResult](
                items=trimmed,
                page_info=PageInfo(
                    has_next=base_result.page_info.has_next or len(scored_results) > page_size,
                    next_cursor=base_result.page_info.next_cursor,
                    total_estimate=base_result.page_info.total_estimate,
                ),
            ),
            ranker_snapshot=snapshot,
        )

    async def _load_profile_context(
        self, profile_slug: str
    ) -> ProfileContext:
        """Load profile context from DB or test injection.

        When _test_profile_context is set (testing), returns it directly.
        Otherwise loads from DB with batch paper metadata queries.
        """
        if self._test_profile_context is not None:
            return self._test_profile_context

        # Production path: load from DB
        from arxiv_mcp.db.models import InterestProfile, InterestSignal, Paper
        from sqlalchemy.orm import selectinload

        async with self.session_factory() as session:
            # Load profile with signals
            stmt = (
                select(InterestProfile)
                .where(InterestProfile.slug == profile_slug)
                .options(selectinload(InterestProfile.signals))
            )
            result = await session.execute(stmt)
            profile = result.scalar_one_or_none()
            if profile is None:
                logger.warning("Profile %r not found, returning empty context", profile_slug)
                return ProfileContext(
                    profile_slug=profile_slug,
                    seed_papers=[],
                    seed_categories=set(),
                    followed_authors=[],
                    negative_papers=[],
                    negative_categories=set(),
                    negative_weight=0.3,
                    query_slugs=[],
                    weights=dict(DEFAULT_WEIGHTS),
                )

            # Categorize signals by type
            active_signals = [s for s in profile.signals if s.status == "active"]
            seed_ids = [
                s.signal_value for s in active_signals if s.signal_type == "seed_paper"
            ]
            negative_ids = [
                s.signal_value for s in active_signals if s.signal_type == "negative_example"
            ]
            followed_authors = [
                s.signal_value for s in active_signals if s.signal_type == "followed_author"
            ]
            query_slugs = [
                s.signal_value for s in active_signals if s.signal_type == "saved_query"
            ]

            # Batch-load seed paper metadata (Pitfall 4 mitigation)
            seed_papers: list[PaperSummary] = []
            if seed_ids:
                paper_stmt = select(Paper).where(Paper.arxiv_id.in_(seed_ids))
                paper_result = await session.execute(paper_stmt)
                for paper_orm in paper_result.scalars().all():
                    seed_papers.append(PaperSummary.from_orm_paper(paper_orm))

            # Batch-load negative paper metadata
            negative_papers: list[PaperSummary] = []
            if negative_ids:
                neg_stmt = select(Paper).where(Paper.arxiv_id.in_(negative_ids))
                neg_result = await session.execute(neg_stmt)
                for paper_orm in neg_result.scalars().all():
                    negative_papers.append(PaperSummary.from_orm_paper(paper_orm))

            # Build seed categories as union of all seed paper category_lists
            seed_categories: set[str] = set()
            for sp in seed_papers:
                seed_categories.update(sp.category_list or [])

            # Build negative categories
            negative_categories: set[str] = set()
            for np_paper in negative_papers:
                negative_categories.update(np_paper.category_list or [])

            # Profile weights (custom or defaults)
            weights = profile.weights if profile.weights else dict(DEFAULT_WEIGHTS)

            return ProfileContext(
                profile_slug=profile_slug,
                seed_papers=seed_papers,
                seed_categories=seed_categories,
                followed_authors=followed_authors,
                negative_papers=negative_papers,
                negative_categories=negative_categories,
                negative_weight=profile.negative_weight,
                query_slugs=query_slugs,
                weights=weights,
            )

    def _wrap_without_ranking(
        self, result: PaginatedResponse[WorkflowSearchResult]
    ) -> ProfileSearchResponse:
        """Convert WorkflowSearchResults to ProfileSearchResults (no ranking).

        Preserves all workflow context (triage_state, collection_slugs)
        while wrapping in ProfileSearchResult with ranking_explanation=None.
        """
        profile_items = [
            ProfileSearchResult(
                paper=item.paper,
                score=item.score,
                triage_state=item.triage_state,
                collection_slugs=item.collection_slugs,
                ranking_explanation=None,
            )
            for item in result.items
        ]
        return ProfileSearchResponse(
            results=PaginatedResponse[ProfileSearchResult](
                items=profile_items,
                page_info=result.page_info,
            ),
            ranker_snapshot=None,
        )
