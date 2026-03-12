"""Tests for ranking pipeline: signal scorers, RankingPipeline, and Pydantic types.

Tests cover all 5 signal types, edge cases (empty inputs, zero division,
self-match exclusion), negative demotion, RankingExplanation, RankerSnapshot,
and ProfileSearchResult model construction.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from arxiv_mcp.interest.ranking import (
    DEFAULT_WEIGHTS,
    ProfileContext,
    RankerSnapshot,
    RankingExplanation,
    RankingPipeline,
    SignalScore,
    SignalType,
    apply_negative_demotion,
    score_category_overlap,
    score_profile_match,
    score_query_match,
    score_recency,
    score_seed_relation,
)
from arxiv_mcp.models.pagination import PaginatedResponse
from arxiv_mcp.models.paper import PaperSummary, ProfileSearchResult, WorkflowSearchResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_paper(
    arxiv_id: str = "2301.00001",
    title: str = "Test Paper",
    authors_text: str = "Author A, Author B",
    categories: str = "cs.CL cs.AI",
    primary_category: str = "cs.CL",
    category_list: list[str] | None = None,
    submitted_date: datetime | None = None,
    announced_date: date | None = None,
) -> PaperSummary:
    """Build a PaperSummary for testing."""
    if category_list is None:
        category_list = ["cs.CL", "cs.AI"]
    if submitted_date is None:
        submitted_date = datetime(2023, 6, 1, tzinfo=timezone.utc)
    if announced_date is None:
        announced_date = date(2023, 6, 2)
    return PaperSummary(
        arxiv_id=arxiv_id,
        title=title,
        authors_text=authors_text,
        abstract_snippet="Abstract snippet.",
        categories=categories,
        primary_category=primary_category,
        category_list=category_list,
        submitted_date=submitted_date,
        announced_date=announced_date,
        oai_datestamp=date(2023, 6, 15),
    )


def _make_profile_context(
    seed_papers: list[PaperSummary] | None = None,
    seed_categories: set[str] | None = None,
    followed_authors: list[str] | None = None,
    negative_papers: list[PaperSummary] | None = None,
    negative_categories: set[str] | None = None,
    negative_weight: float = 0.3,
    query_slugs: list[str] | None = None,
    weights: dict[str, float] | None = None,
    profile_slug: str = "test-profile",
) -> ProfileContext:
    """Build a ProfileContext for testing."""
    return ProfileContext(
        profile_slug=profile_slug,
        seed_papers=seed_papers or [],
        seed_categories=seed_categories or set(),
        followed_authors=followed_authors or [],
        negative_papers=negative_papers or [],
        negative_categories=negative_categories or set(),
        negative_weight=negative_weight,
        query_slugs=query_slugs or [],
        weights=weights or dict(DEFAULT_WEIGHTS),
    )


# ===========================================================================
# TestQueryMatchScorer
# ===========================================================================


class TestQueryMatchScorer:
    """Tests for score_query_match signal scorer."""

    def test_normal_normalization(self):
        """Ranks [0.1, 0.5, 0.9] should normalize to [1.0, 0.5, 0.0]."""
        all_ranks = [0.1, 0.5, 0.9]
        # Best rank = lowest (0.1) -> 1.0, worst (0.9) -> 0.0
        s = score_query_match(0.1, all_ranks)
        assert s.signal_type == SignalType.QUERY_MATCH
        assert s.normalized_score == pytest.approx(1.0)

        s2 = score_query_match(0.5, all_ranks)
        assert s2.normalized_score == pytest.approx(0.5)

        s3 = score_query_match(0.9, all_ranks)
        assert s3.normalized_score == pytest.approx(0.0)

    def test_same_rank_guard(self):
        """All-same ranks should return 1.0 (zero-division guard)."""
        s = score_query_match(0.5, [0.5, 0.5, 0.5])
        assert s.normalized_score == pytest.approx(1.0)

    def test_none_rank_returns_zero(self):
        """None query_rank returns zero SignalScore."""
        s = score_query_match(None, [0.1, 0.5, 0.9])
        assert s.normalized_score == pytest.approx(0.0)
        assert s.weighted_score == pytest.approx(0.0)


# ===========================================================================
# TestCategoryOverlapScorer
# ===========================================================================


class TestCategoryOverlapScorer:
    """Tests for score_category_overlap signal scorer."""

    def test_partial_overlap(self):
        """2 of 3 seed categories -> Jaccard ~0.67."""
        paper = _make_paper(category_list=["cs.CL", "cs.AI"])
        seed_cats = {"cs.CL", "cs.AI", "cs.LG"}
        s = score_category_overlap(paper, seed_cats)
        # Intersection: {cs.CL, cs.AI} = 2, Union: {cs.CL, cs.AI, cs.LG} = 3
        assert s.normalized_score == pytest.approx(2.0 / 3.0, abs=0.01)

    def test_full_overlap(self):
        """Exact match returns 1.0."""
        paper = _make_paper(category_list=["cs.CL", "cs.AI"])
        seed_cats = {"cs.CL", "cs.AI"}
        s = score_category_overlap(paper, seed_cats)
        assert s.normalized_score == pytest.approx(1.0)

    def test_no_overlap(self):
        """No overlap returns 0.0."""
        paper = _make_paper(category_list=["math.AG"])
        seed_cats = {"cs.CL", "cs.AI"}
        s = score_category_overlap(paper, seed_cats)
        assert s.normalized_score == pytest.approx(0.0)

    def test_empty_seed_categories(self):
        """Empty seed categories returns 0.0."""
        paper = _make_paper(category_list=["cs.CL"])
        s = score_category_overlap(paper, set())
        assert s.normalized_score == pytest.approx(0.0)


# ===========================================================================
# TestRecencyScorer
# ===========================================================================


class TestRecencyScorer:
    """Tests for score_recency signal scorer."""

    def test_today_paper(self):
        """Paper submitted today returns ~1.0."""
        now = datetime.now(timezone.utc)
        paper = _make_paper(submitted_date=now)
        s = score_recency(paper, max_date=now, decay_days=90)
        assert s.normalized_score == pytest.approx(1.0, abs=0.01)

    def test_old_paper(self):
        """90-day-old paper returns ~0.0."""
        now = datetime.now(timezone.utc)
        old = now - timedelta(days=90)
        paper = _make_paper(submitted_date=old)
        s = score_recency(paper, max_date=now, decay_days=90)
        assert s.normalized_score == pytest.approx(0.0, abs=0.01)

    def test_beyond_decay_days(self):
        """Paper older than decay_days returns exactly 0.0."""
        now = datetime.now(timezone.utc)
        ancient = now - timedelta(days=120)
        paper = _make_paper(submitted_date=ancient)
        s = score_recency(paper, max_date=now, decay_days=90)
        assert s.normalized_score == pytest.approx(0.0)


# ===========================================================================
# TestSeedRelationScorer
# ===========================================================================


class TestSeedRelationScorer:
    """Tests for score_seed_relation signal scorer."""

    def test_matching_author(self):
        """Paper with matching author returns positive score."""
        paper = _make_paper(authors_text="Author A, Author B")
        seed_papers = [_make_paper(arxiv_id="seed-1")]
        seed_cats = {"cs.CL", "cs.AI"}
        followed = ["author a"]
        s = score_seed_relation(paper, seed_papers, seed_cats, followed)
        assert s.normalized_score > 0.0

    def test_categories_only_returns_zero(self):
        """Paper with matching categories but no author match returns 0.0.

        Category overlap was removed from score_seed_relation to fix
        triple-counting (PREMCP-01). Only author match remains.
        """
        paper = _make_paper(category_list=["cs.CL", "cs.AI"])
        seed_papers = [_make_paper(arxiv_id="seed-1", category_list=["cs.CL", "cs.LG"])]
        seed_cats = {"cs.CL", "cs.LG"}
        s = score_seed_relation(paper, seed_papers, seed_cats, [])
        assert s.normalized_score == pytest.approx(0.0)

    def test_self_exclusion(self):
        """Seed papers themselves are excluded (returns 0.0)."""
        paper = _make_paper(arxiv_id="2301.00001")
        seed_papers = [_make_paper(arxiv_id="2301.00001")]
        seed_ids = {p.arxiv_id for p in seed_papers}
        # score_seed_relation checks if paper.arxiv_id in seed set
        s = score_seed_relation(paper, seed_papers, {"cs.CL"}, [])
        assert s.normalized_score == pytest.approx(0.0)

    def test_no_category_jaccard_in_seed_relation(self):
        """PREMCP-01: score_seed_relation must not compute category Jaccard.

        Verifies that category-only match produces 0.0 (author signal only).
        """
        paper = _make_paper(category_list=["cs.CL", "cs.AI"])
        seed_papers = [_make_paper(arxiv_id="seed-1")]
        seed_cats = {"cs.CL", "cs.AI"}
        # No followed authors -- only category match possible
        s = score_seed_relation(paper, seed_papers, seed_cats, [])
        assert s.normalized_score == pytest.approx(0.0), (
            "score_seed_relation should return 0.0 when only categories match "
            "(category Jaccard removed per PREMCP-01)"
        )


# ===========================================================================
# TestProfileMatchScorer
# ===========================================================================


class TestProfileMatchScorer:
    """Tests for score_profile_match signal scorer."""

    def test_aggregation_correctness(self):
        """Profile match aggregates sub-signals correctly."""
        paper = _make_paper(
            authors_text="Author A",
            category_list=["cs.CL", "cs.AI"],
        )
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1", category_list=["cs.CL", "cs.LG"])],
            seed_categories={"cs.CL", "cs.LG"},
            followed_authors=["author a"],
        )
        s = score_profile_match(paper, ctx)
        assert s.signal_type == SignalType.INTEREST_PROFILE_MATCH
        # Composite of sub-signals, should be positive
        assert s.normalized_score > 0.0
        assert s.normalized_score <= 1.0

    def test_categories_only_returns_query_boost_only(self):
        """Profile match with matching categories but no author returns only query_boost.

        Category Jaccard was removed from score_profile_match to fix
        triple-counting (PREMCP-01). Only author + query_boost remain.
        """
        paper = _make_paper(category_list=["cs.CL", "cs.AI"])
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1", category_list=["cs.CL", "cs.AI"])],
            seed_categories={"cs.CL", "cs.AI"},
            followed_authors=[],  # No authors
            query_slugs=[],  # No queries -> query_boost = 0
        )
        s = score_profile_match(paper, ctx)
        # With no author match and no query slugs, composite should be 0.0
        assert s.normalized_score == pytest.approx(0.0), (
            "score_profile_match should return 0.0 when only categories match "
            "(category Jaccard removed per PREMCP-01)"
        )

    def test_author_match_returns_positive(self):
        """Profile match with author match returns > 0.0."""
        paper = _make_paper(authors_text="Author A, Author B")
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1")],
            seed_categories={"cs.CL"},
            followed_authors=["author a"],
        )
        s = score_profile_match(paper, ctx)
        assert s.normalized_score > 0.0

    def test_no_category_jaccard_in_profile_match(self):
        """PREMCP-01: score_profile_match must not compute category Jaccard."""
        import inspect
        source = inspect.getsource(score_profile_match)
        # Should not contain category Jaccard computation
        assert "intersection" not in source or "union" not in source, (
            "score_profile_match should not compute Jaccard (intersection/union)"
        )


# ===========================================================================
# TestNegativeDemotion
# ===========================================================================


class TestNegativeDemotion:
    """Tests for apply_negative_demotion."""

    def test_demotion_applied(self):
        """Negative example matching reduces scores."""
        paper = _make_paper(arxiv_id="neg-paper", category_list=["cs.CL"])
        ctx = _make_profile_context(
            negative_papers=[_make_paper(arxiv_id="neg-paper")],
            negative_categories={"cs.CL"},
            negative_weight=0.5,
        )
        scores = [
            SignalScore(
                signal_type=SignalType.QUERY_MATCH,
                raw_score=0.8,
                normalized_score=0.8,
                weight=0.35,
                weighted_score=0.28,
                explanation="test",
            ),
        ]
        apply_negative_demotion(scores, paper, ctx)
        # weighted_score should be reduced by factor (1.0 - 0.5) = 0.5
        assert scores[0].weighted_score == pytest.approx(0.14)

    def test_no_negatives_no_effect(self):
        """Without negative matches, scores unchanged."""
        paper = _make_paper(arxiv_id="good-paper", category_list=["math.AG"])
        ctx = _make_profile_context(
            negative_papers=[],
            negative_categories={"cs.CL"},
            negative_weight=0.5,
        )
        scores = [
            SignalScore(
                signal_type=SignalType.QUERY_MATCH,
                raw_score=0.8,
                normalized_score=0.8,
                weight=0.35,
                weighted_score=0.28,
                explanation="test",
            ),
        ]
        apply_negative_demotion(scores, paper, ctx)
        assert scores[0].weighted_score == pytest.approx(0.28)

    def test_category_overlap_does_not_trigger_demotion(self):
        """Category overlap with negative papers should NOT trigger demotion (ADR-0001)."""
        paper = _make_paper(arxiv_id="innocent-paper", category_list=["cs.CL"])
        ctx = _make_profile_context(
            negative_papers=[_make_paper(arxiv_id="neg-paper", category_list=["cs.CL"])],
            negative_categories={"cs.CL"},
            negative_weight=0.5,
        )
        scores = [
            SignalScore(
                signal_type=SignalType.QUERY_MATCH,
                raw_score=0.8,
                normalized_score=0.8,
                weight=0.35,
                weighted_score=0.28,
                explanation="test",
            ),
        ]
        apply_negative_demotion(scores, paper, ctx)
        # Score should be unchanged -- category overlap alone does not trigger demotion
        assert scores[0].weighted_score == pytest.approx(0.28)


# ===========================================================================
# TestRankingPipeline
# ===========================================================================


class TestRankingPipeline:
    """Tests for RankingPipeline.score_paper."""

    def test_with_profile(self):
        """Pipeline with profile returns RankingExplanation with all applicable signals."""
        paper = _make_paper(
            authors_text="Author A",
            category_list=["cs.CL", "cs.AI"],
            submitted_date=datetime.now(timezone.utc),
        )
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1")],
            seed_categories={"cs.CL", "cs.LG"},
            followed_authors=["author a"],
        )
        pipeline = RankingPipeline()
        explanation = pipeline.score_paper(
            paper,
            query_rank=0.5,
            all_ranks=[0.1, 0.5, 0.9],
            profile_context=ctx,
        )
        assert isinstance(explanation, RankingExplanation)
        assert explanation.composite_score > 0.0
        # Should have all 5 signals
        types_present = {s.signal_type for s in explanation.signal_breakdown}
        assert SignalType.QUERY_MATCH in types_present
        assert SignalType.RECENCY in types_present
        assert SignalType.SEED_RELATION in types_present
        assert SignalType.CATEGORY_OVERLAP in types_present
        assert SignalType.INTEREST_PROFILE_MATCH in types_present

    def test_without_profile(self):
        """Pipeline without profile returns only query_match + recency signals."""
        paper = _make_paper(submitted_date=datetime.now(timezone.utc))
        pipeline = RankingPipeline()
        explanation = pipeline.score_paper(
            paper,
            query_rank=0.3,
            all_ranks=[0.1, 0.3, 0.9],
            profile_context=None,
        )
        types_present = {s.signal_type for s in explanation.signal_breakdown}
        assert SignalType.QUERY_MATCH in types_present
        assert SignalType.RECENCY in types_present
        assert SignalType.SEED_RELATION not in types_present
        assert SignalType.CATEGORY_OVERLAP not in types_present
        assert SignalType.INTEREST_PROFILE_MATCH not in types_present

    def test_empty_profile(self):
        """Pipeline with empty profile (no signals) returns only query_match + recency."""
        paper = _make_paper(submitted_date=datetime.now(timezone.utc))
        ctx = _make_profile_context()  # empty
        pipeline = RankingPipeline()
        explanation = pipeline.score_paper(
            paper,
            query_rank=0.3,
            all_ranks=[0.1, 0.3, 0.9],
            profile_context=ctx,
        )
        types_present = {s.signal_type for s in explanation.signal_breakdown}
        assert SignalType.QUERY_MATCH in types_present
        assert SignalType.RECENCY in types_present

    def test_custom_weights(self):
        """Custom weights override DEFAULT_WEIGHTS correctly."""
        custom = {SignalType.QUERY_MATCH: 0.9, SignalType.RECENCY: 0.1}
        pipeline = RankingPipeline(weights=custom)
        paper = _make_paper(submitted_date=datetime.now(timezone.utc))
        explanation = pipeline.score_paper(
            paper,
            query_rank=0.1,
            all_ranks=[0.1, 0.5, 0.9],
        )
        qm = [s for s in explanation.signal_breakdown if s.signal_type == SignalType.QUERY_MATCH][0]
        assert qm.weight == pytest.approx(0.9)

    def test_category_weight_no_triple_count(self):
        """PREMCP-01: Category overlap effective weight is exactly DEFAULT_WEIGHTS[CATEGORY_OVERLAP].

        When a paper matches only via categories (no author match, no query match),
        the total weighted category contribution comes exclusively from
        score_category_overlap with weight 0.15, not from triple-counting.
        """
        # Paper that matches seed categories but has no matching authors
        paper = _make_paper(
            arxiv_id="2301.99999",
            authors_text="Unknown Author",
            category_list=["cs.CL", "cs.AI"],
            submitted_date=datetime.now(timezone.utc),
        )
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1", category_list=["cs.CL", "cs.AI"])],
            seed_categories={"cs.CL", "cs.AI"},
            followed_authors=[],  # No author match possible
            query_slugs=[],  # No query boost
        )
        pipeline = RankingPipeline()
        explanation = pipeline.score_paper(
            paper,
            query_rank=None,  # No query match
            all_ranks=[],
            profile_context=ctx,
        )

        # Find category overlap signal
        co_signals = [
            s for s in explanation.signal_breakdown
            if s.signal_type == SignalType.CATEGORY_OVERLAP
        ]
        assert len(co_signals) == 1
        co = co_signals[0]

        # Category overlap weight must be exactly DEFAULT_WEIGHTS value
        assert co.weight == pytest.approx(DEFAULT_WEIGHTS[SignalType.CATEGORY_OVERLAP])
        assert co.weight == pytest.approx(0.15)

        # Seed relation and profile match should contribute 0 category weight
        sr_signals = [
            s for s in explanation.signal_breakdown
            if s.signal_type == SignalType.SEED_RELATION
        ]
        pm_signals = [
            s for s in explanation.signal_breakdown
            if s.signal_type == SignalType.INTEREST_PROFILE_MATCH
        ]
        # With no author match and no query boost, these should be 0
        assert sr_signals[0].weighted_score == pytest.approx(0.0)
        assert pm_signals[0].weighted_score == pytest.approx(0.0)

        # Total category-related weighted score is exactly co.weighted_score
        # (no hidden category weight in seed_relation or profile_match)
        total_category_contribution = co.weighted_score
        assert total_category_contribution == pytest.approx(
            co.normalized_score * 0.15
        )


# ===========================================================================
# TestRankerSnapshot
# ===========================================================================


class TestRankerSnapshot:
    """Tests for RankerSnapshot capture."""

    def test_snapshot_fields(self):
        """Snapshot captures profile slug, weights, signal counts, ranker_version."""
        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="seed-1"), _make_paper(arxiv_id="seed-2")],
            followed_authors=["author a"],
            negative_papers=[_make_paper(arxiv_id="neg-1")],
            query_slugs=["q-1"],
        )
        pipeline = RankingPipeline()
        snap = pipeline.capture_snapshot(profile_context=ctx)
        assert isinstance(snap, RankerSnapshot)
        assert snap.profile_slug == "test-profile"
        assert snap.ranker_version == RankingPipeline.RANKER_VERSION
        assert snap.seed_paper_count == 2
        assert snap.followed_author_count == 1
        assert snap.negative_example_count == 1
        assert snap.saved_query_count == 1
        assert snap.negative_weight == pytest.approx(0.3)
        assert snap.captured_at is not None

    def test_snapshot_no_profile(self):
        """Snapshot without profile returns None slug and zero counts."""
        pipeline = RankingPipeline()
        snap = pipeline.capture_snapshot(profile_context=None)
        assert snap.profile_slug is None
        assert snap.seed_paper_count == 0


# ===========================================================================
# TestProfileSearchResult
# ===========================================================================


class TestProfileSearchResult:
    """Tests for ProfileSearchResult Pydantic model."""

    def test_construction_with_explanation(self):
        """ProfileSearchResult can be constructed with ranking_explanation."""
        paper = _make_paper()
        explanation = RankingExplanation(
            composite_score=0.75,
            signal_breakdown=[
                SignalScore(
                    signal_type=SignalType.QUERY_MATCH,
                    raw_score=0.8,
                    normalized_score=0.8,
                    weight=0.35,
                    weighted_score=0.28,
                    explanation="query match",
                ),
            ],
            ranker_version="0.3.0",
        )
        result = ProfileSearchResult(
            paper=paper,
            score=0.75,
            triage_state="unseen",
            collection_slugs=[],
            ranking_explanation=explanation,
        )
        assert result.ranking_explanation is not None
        assert result.ranking_explanation.composite_score == pytest.approx(0.75)
        assert result.paper.arxiv_id == "2301.00001"
        assert result.triage_state == "unseen"

    def test_construction_without_explanation(self):
        """ProfileSearchResult defaults to None ranking_explanation."""
        paper = _make_paper()
        result = ProfileSearchResult(
            paper=paper,
            score=0.5,
        )
        assert result.ranking_explanation is None
        assert result.triage_state == "unseen"


# ===========================================================================
# TestProfileRankingService
# ===========================================================================


class MockWorkflowSearchService:
    """Mock WorkflowSearchService returning canned results."""

    def __init__(self, results: list[WorkflowSearchResult] | None = None):
        from arxiv_mcp.models.pagination import PageInfo

        self._results = results or []
        self._page_info = PageInfo(has_next=False, next_cursor=None)
        self.last_kwargs: dict = {}

    async def search_papers(self, **kwargs) -> PaginatedResponse[WorkflowSearchResult]:
        self.last_kwargs = kwargs
        return PaginatedResponse[WorkflowSearchResult](
            items=self._results,
            page_info=self._page_info,
        )

    async def browse_recent(self, **kwargs) -> PaginatedResponse[WorkflowSearchResult]:
        self.last_kwargs = kwargs
        return PaginatedResponse[WorkflowSearchResult](
            items=self._results,
            page_info=self._page_info,
        )


def _make_workflow_results(count: int = 3) -> list[WorkflowSearchResult]:
    """Build a list of WorkflowSearchResult for testing."""
    results = []
    now = datetime.now(timezone.utc)
    for i in range(count):
        paper = _make_paper(
            arxiv_id=f"2301.{i:05d}",
            title=f"Test Paper {i}",
            authors_text=f"Author {i}",
            category_list=["cs.CL", "cs.AI"] if i % 2 == 0 else ["math.AG"],
            submitted_date=now - timedelta(days=i * 5),
        )
        results.append(
            WorkflowSearchResult(
                paper=paper,
                score=0.9 - (i * 0.2),
                triage_state="unseen",
                collection_slugs=[],
            )
        )
    return results


class TestProfileRankingService:
    """Tests for ProfileRankingService wrapping WorkflowSearchService."""

    async def test_search_without_profile(self):
        """Without profile_slug, results pass through as ProfileSearchResults with no explanation."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(3))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
        )
        response = await service.search_papers(profile_slug=None, query_text="test")
        assert response.ranker_snapshot is None
        assert len(response.results.items) == 3
        for item in response.results.items:
            assert isinstance(item, ProfileSearchResult)
            assert item.ranking_explanation is None

    async def test_search_with_profile(self):
        """With profile_slug, results are re-ranked with explanations and snapshot."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(3))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
            _test_profile_context=_make_profile_context(
                seed_papers=[_make_paper(arxiv_id="seed-1")],
                seed_categories={"cs.CL", "cs.LG"},
                followed_authors=["author 0"],
            ),
        )
        response = await service.search_papers(
            profile_slug="test-profile",
            query_text="test",
            page_size=3,
        )
        assert response.ranker_snapshot is not None
        assert response.ranker_snapshot.profile_slug == "test-profile"
        assert len(response.results.items) <= 3
        for item in response.results.items:
            assert isinstance(item, ProfileSearchResult)
            assert item.ranking_explanation is not None
            assert item.ranking_explanation.composite_score >= 0.0

    async def test_search_with_empty_profile(self):
        """Empty profile returns results with only query_match + recency signals."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(2))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
            _test_profile_context=_make_profile_context(),  # empty
        )
        response = await service.search_papers(
            profile_slug="empty-profile",
            query_text="test",
            page_size=2,
        )
        assert response.ranker_snapshot is not None
        for item in response.results.items:
            assert item.ranking_explanation is not None
            types = {s.signal_type for s in item.ranking_explanation.signal_breakdown}
            assert SignalType.QUERY_MATCH in types
            assert SignalType.RECENCY in types

    async def test_browse_with_profile(self):
        """browse_recent with profile_slug applies ranking."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(3))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
            _test_profile_context=_make_profile_context(
                seed_papers=[_make_paper(arxiv_id="seed-1")],
                seed_categories={"cs.CL"},
            ),
        )
        response = await service.browse_recent(
            profile_slug="test-profile",
            page_size=3,
        )
        assert response.ranker_snapshot is not None
        assert len(response.results.items) <= 3

    async def test_ranker_snapshot_present(self):
        """Response includes ranker_snapshot with correct metadata."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(1))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        ctx = _make_profile_context(
            seed_papers=[_make_paper(arxiv_id="s1"), _make_paper(arxiv_id="s2")],
            followed_authors=["auth a"],
            negative_papers=[_make_paper(arxiv_id="n1")],
            query_slugs=["q1"],
        )
        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
            _test_profile_context=ctx,
        )
        response = await service.search_papers(
            profile_slug="test-profile",
            query_text="test",
            page_size=1,
        )
        snap = response.ranker_snapshot
        assert snap is not None
        assert snap.seed_paper_count == 2
        assert snap.followed_author_count == 1
        assert snap.negative_example_count == 1
        assert snap.saved_query_count == 1
        assert snap.ranker_version == RankingPipeline.RANKER_VERSION

    async def test_overfetch_strategy(self):
        """Service requests page_size * 3 from base service for re-ranking."""
        mock_wss = MockWorkflowSearchService(results=_make_workflow_results(6))

        from arxiv_mcp.interest.search_augment import ProfileRankingService

        service = ProfileRankingService(
            session_factory=None,
            settings=None,
            workflow_search_service=mock_wss,
            _test_profile_context=_make_profile_context(
                seed_papers=[_make_paper(arxiv_id="seed-1")],
                seed_categories={"cs.CL"},
            ),
        )
        response = await service.search_papers(
            profile_slug="test-profile",
            query_text="test",
            page_size=2,
        )
        # Service should have passed page_size * 3 = 6 to the mock
        assert mock_wss.last_kwargs.get("page_size") == 6
        # But response should be trimmed to original page_size
        assert len(response.results.items) <= 2
