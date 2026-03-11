"""Composable ranking pipeline with five signal scorers.

Provides pure scorer functions for query_match, category_overlap, recency,
seed_relation, and interest_profile_match, plus a RankingPipeline class
that orchestrates scoring with optional negative demotion.

All scorers are module-level pure functions for testability. The pipeline
class handles weight management, scorer dispatch, and snapshot capture.

Type definitions (SignalType, SignalScore, RankingExplanation, RankerSnapshot)
live in models/interest.py to avoid circular imports with models/paper.py.
This module re-exports them for convenience.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from arxiv_mcp.interest.signals import parse_authors
from arxiv_mcp.models.interest import (
    RankerSnapshot,
    RankingExplanation,
    SignalScore,
    SignalType,
)
from arxiv_mcp.models.paper import PaperSummary

# Re-export for consumers that import from ranking
__all__ = [
    "SignalType",
    "SignalScore",
    "RankingExplanation",
    "RankerSnapshot",
    "ProfileContext",
    "RankingPipeline",
    "DEFAULT_WEIGHTS",
    "score_query_match",
    "score_category_overlap",
    "score_recency",
    "score_seed_relation",
    "score_profile_match",
    "apply_negative_demotion",
]


# ---------------------------------------------------------------------------
# ProfileContext (local dataclass -- references PaperSummary)
# ---------------------------------------------------------------------------


@dataclass
class ProfileContext:
    """Pre-loaded profile data needed for ranking.

    Built by ProfileRankingService._load_profile_context to avoid
    N+1 queries during scoring.
    """

    profile_slug: str
    seed_papers: list[PaperSummary]
    seed_categories: set[str]
    followed_authors: list[str]
    negative_papers: list[PaperSummary]
    negative_categories: set[str]
    negative_weight: float
    query_slugs: list[str]
    weights: dict[str, float]


# ---------------------------------------------------------------------------
# Default weights
# ---------------------------------------------------------------------------

DEFAULT_WEIGHTS: dict[str, float] = {
    SignalType.QUERY_MATCH: 0.35,
    SignalType.SEED_RELATION: 0.25,
    SignalType.CATEGORY_OVERLAP: 0.15,
    SignalType.INTEREST_PROFILE_MATCH: 0.15,
    SignalType.RECENCY: 0.10,
}


# ---------------------------------------------------------------------------
# Pure scorer functions
# ---------------------------------------------------------------------------


def score_query_match(
    query_rank: float | None,
    all_ranks: list[float],
) -> SignalScore:
    """Score a paper based on its lexical query rank (min-max normalization).

    Lower rank values mean higher relevance. Normalizes so that the
    best rank maps to 1.0 and worst to 0.0. Guards against zero division
    when all ranks are identical.

    Args:
        query_rank: This paper's search rank score (lower = better), or None.
        all_ranks: All rank scores in the result set for normalization.

    Returns:
        SignalScore with normalized_score in [0.0, 1.0].
    """
    if query_rank is None or not all_ranks:
        return SignalScore(
            signal_type=SignalType.QUERY_MATCH,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="No query rank available",
        )

    min_rank = min(all_ranks)
    max_rank = max(all_ranks)
    spread = max_rank - min_rank

    if spread == 0.0:
        # All ranks identical -- treat as maximum relevance
        normalized = 1.0
    else:
        # Invert: lower rank = higher score
        normalized = (max_rank - query_rank) / spread

    normalized = max(0.0, min(1.0, normalized))

    return SignalScore(
        signal_type=SignalType.QUERY_MATCH,
        raw_score=query_rank,
        normalized_score=normalized,
        weight=0.0,  # Set by pipeline
        weighted_score=0.0,
        explanation=f"Query rank {query_rank:.3f} normalized to {normalized:.3f}",
    )


def score_category_overlap(
    paper: PaperSummary,
    seed_categories: set[str],
) -> SignalScore:
    """Score a paper by Jaccard similarity of its categories with seed categories.

    Args:
        paper: Paper to score.
        seed_categories: Union of all seed paper category_lists.

    Returns:
        SignalScore with Jaccard similarity as normalized_score.
    """
    paper_cats = set(paper.category_list or [])
    if not seed_categories or not paper_cats:
        return SignalScore(
            signal_type=SignalType.CATEGORY_OVERLAP,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="No categories to compare",
        )

    intersection = paper_cats & seed_categories
    union = paper_cats | seed_categories
    jaccard = len(intersection) / len(union) if union else 0.0

    return SignalScore(
        signal_type=SignalType.CATEGORY_OVERLAP,
        raw_score=jaccard,
        normalized_score=jaccard,
        weight=0.0,
        weighted_score=0.0,
        explanation=f"Category Jaccard {len(intersection)}/{len(union)} = {jaccard:.3f}",
    )


def score_recency(
    paper: PaperSummary,
    max_date: datetime,
    decay_days: int = 90,
) -> SignalScore:
    """Score a paper by how recently it was submitted (linear decay).

    Papers submitted on max_date score 1.0. Papers older than decay_days
    score 0.0. Linear interpolation between.

    Args:
        paper: Paper to score.
        max_date: Reference date (typically the most recent paper's date).
        decay_days: Number of days over which score decays to 0.

    Returns:
        SignalScore with linear decay as normalized_score.
    """
    submitted = paper.submitted_date
    if submitted is None:
        return SignalScore(
            signal_type=SignalType.RECENCY,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="No submission date",
        )

    # Ensure both are timezone-aware for comparison
    if submitted.tzinfo is None:
        submitted = submitted.replace(tzinfo=timezone.utc)
    if max_date.tzinfo is None:
        max_date = max_date.replace(tzinfo=timezone.utc)

    delta = (max_date - submitted).total_seconds() / 86400.0  # days
    if delta < 0:
        delta = 0.0

    if delta >= decay_days:
        normalized = 0.0
    else:
        normalized = 1.0 - (delta / decay_days)

    return SignalScore(
        signal_type=SignalType.RECENCY,
        raw_score=delta,
        normalized_score=normalized,
        weight=0.0,
        weighted_score=0.0,
        explanation=f"{delta:.1f} days old, score {normalized:.3f}",
    )


def score_seed_relation(
    paper: PaperSummary,
    seed_papers: list[PaperSummary],
    seed_categories: set[str],
    followed_authors: list[str],
) -> SignalScore:
    """Score a paper by its relation to seed papers and followed authors.

    Composite of:
    - Category overlap with seed paper categories (proxy for topic match)
    - Author match against followed authors list

    Excludes papers whose arxiv_id is in the seed set (self-match exclusion).

    Args:
        paper: Paper to score.
        seed_papers: List of seed papers from the profile.
        seed_categories: Union of seed paper category_lists.
        followed_authors: Normalized author names from the profile.

    Returns:
        SignalScore with composite relation score.
    """
    seed_ids = {p.arxiv_id for p in seed_papers}
    if paper.arxiv_id in seed_ids:
        return SignalScore(
            signal_type=SignalType.SEED_RELATION,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="Paper is a seed paper (self-match excluded)",
        )

    if not seed_papers and not followed_authors:
        return SignalScore(
            signal_type=SignalType.SEED_RELATION,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="No seed papers or followed authors",
        )

    # Sub-signal 1: category overlap with seeds
    paper_cats = set(paper.category_list or [])
    cat_score = 0.0
    if seed_categories and paper_cats:
        intersection = paper_cats & seed_categories
        union = paper_cats | seed_categories
        cat_score = len(intersection) / len(union) if union else 0.0

    # Sub-signal 2: author match
    author_score = 0.0
    if followed_authors:
        paper_authors = parse_authors(paper.authors_text or "")
        matched = sum(1 for a in paper_authors if a in followed_authors)
        author_score = min(1.0, matched / max(1, len(followed_authors)))

    # Weighted composite (60% category, 40% author)
    composite = 0.6 * cat_score + 0.4 * author_score
    composite = max(0.0, min(1.0, composite))

    parts = []
    if cat_score > 0:
        parts.append(f"cat_overlap={cat_score:.3f}")
    if author_score > 0:
        parts.append(f"author_match={author_score:.3f}")
    explanation = f"Seed relation: {', '.join(parts) if parts else 'no match'}"

    return SignalScore(
        signal_type=SignalType.SEED_RELATION,
        raw_score=composite,
        normalized_score=composite,
        weight=0.0,
        weighted_score=0.0,
        explanation=explanation,
    )


def score_profile_match(
    paper: PaperSummary,
    profile_context: ProfileContext,
) -> SignalScore:
    """Score how well a paper matches the overall interest profile.

    Aggregates seed_relation + category_overlap + author match sub-signals
    into a single composite score. Avoids double-counting by using a
    unified formula rather than summing individual signals.

    Args:
        paper: Paper to score.
        profile_context: Pre-loaded profile context.

    Returns:
        SignalScore with normalized composite profile match.
    """
    if not profile_context.seed_papers and not profile_context.followed_authors:
        return SignalScore(
            signal_type=SignalType.INTEREST_PROFILE_MATCH,
            raw_score=0.0,
            normalized_score=0.0,
            weight=0.0,
            weighted_score=0.0,
            explanation="Empty profile, no match possible",
        )

    # Sub-signal 1: category overlap with all seed categories
    paper_cats = set(paper.category_list or [])
    cat_score = 0.0
    if profile_context.seed_categories and paper_cats:
        intersection = paper_cats & profile_context.seed_categories
        union = paper_cats | profile_context.seed_categories
        cat_score = len(intersection) / len(union) if union else 0.0

    # Sub-signal 2: author match against followed authors
    author_score = 0.0
    if profile_context.followed_authors:
        paper_authors = parse_authors(paper.authors_text or "")
        matched = sum(1 for a in paper_authors if a in profile_context.followed_authors)
        author_score = min(1.0, matched / max(1, len(profile_context.followed_authors)))

    # Sub-signal 3: query coverage (does the paper match saved query topics?)
    # For now, just use presence as a binary boost
    query_boost = 0.1 if profile_context.query_slugs else 0.0

    # Weighted composite
    composite = 0.5 * cat_score + 0.35 * author_score + 0.15 * query_boost
    composite = max(0.0, min(1.0, composite))

    return SignalScore(
        signal_type=SignalType.INTEREST_PROFILE_MATCH,
        raw_score=composite,
        normalized_score=composite,
        weight=0.0,
        weighted_score=0.0,
        explanation=f"Profile match: cat={cat_score:.3f}, author={author_score:.3f}",
    )


def apply_negative_demotion(
    scores: list[SignalScore],
    paper: PaperSummary,
    profile_context: ProfileContext,
) -> None:
    """Apply soft demotion to scores for papers matching negative examples.

    Direct ID matching only -- category-based demotion removed per ADR-0001
    (exploration-first). Mutates the scores list in place. If the paper's
    arxiv_id matches a negative example, all weighted_scores are multiplied
    by (1.0 - negative_weight).

    This is soft demotion -- never removes scores entirely.

    Args:
        scores: List of SignalScores to potentially demote (mutated).
        paper: Paper being scored.
        profile_context: Profile context with negative papers.
    """
    if not profile_context.negative_papers:
        return

    negative_ids = {p.arxiv_id for p in profile_context.negative_papers}

    if paper.arxiv_id not in negative_ids:
        return

    demotion_factor = 1.0 - profile_context.negative_weight
    for score in scores:
        score.weighted_score *= demotion_factor


# ---------------------------------------------------------------------------
# RankingPipeline
# ---------------------------------------------------------------------------


class RankingPipeline:
    """Orchestrates multi-signal ranking with composable scorers.

    Dispatches to pure scorer functions, applies weights, handles
    negative demotion, and computes composite scores. Supports
    custom weight overrides from profile settings.

    Attributes:
        RANKER_VERSION: Semver string for result set reproducibility.
    """

    RANKER_VERSION = "0.3.0"

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        """Initialize with optional custom weights.

        Args:
            weights: Override specific signal weights. Missing signals
                use DEFAULT_WEIGHTS values.
        """
        self.weights = dict(DEFAULT_WEIGHTS)
        if weights:
            self.weights.update(weights)

    def score_paper(
        self,
        paper: PaperSummary,
        query_rank: float | None = None,
        all_ranks: list[float] | None = None,
        profile_context: ProfileContext | None = None,
    ) -> RankingExplanation:
        """Score a single paper across all applicable signal types.

        Without a profile, only query_match and recency signals are applied.
        With a profile, all 5 signal types are scored.

        Args:
            paper: Paper to score.
            query_rank: This paper's search rank score (lower = better).
            all_ranks: All rank scores in result set for normalization.
            profile_context: Pre-loaded profile data, or None.

        Returns:
            RankingExplanation with composite_score and full signal_breakdown.
        """
        scores: list[SignalScore] = []

        # Always apply: query_match
        qm = score_query_match(query_rank, all_ranks or [])
        qm.weight = self.weights.get(SignalType.QUERY_MATCH, 0.0)
        qm.weighted_score = qm.normalized_score * qm.weight
        scores.append(qm)

        # Always apply: recency
        max_date = datetime.now(timezone.utc)
        rec = score_recency(paper, max_date=max_date)
        rec.weight = self.weights.get(SignalType.RECENCY, 0.0)
        rec.weighted_score = rec.normalized_score * rec.weight
        scores.append(rec)

        # Profile-dependent signals
        has_profile_signals = (
            profile_context is not None
            and (
                profile_context.seed_papers
                or profile_context.followed_authors
            )
        )

        if has_profile_signals:
            assert profile_context is not None  # type narrowing

            # Seed relation
            sr = score_seed_relation(
                paper,
                profile_context.seed_papers,
                profile_context.seed_categories,
                profile_context.followed_authors,
            )
            sr.weight = self.weights.get(SignalType.SEED_RELATION, 0.0)
            sr.weighted_score = sr.normalized_score * sr.weight
            scores.append(sr)

            # Category overlap
            co = score_category_overlap(paper, profile_context.seed_categories)
            co.weight = self.weights.get(SignalType.CATEGORY_OVERLAP, 0.0)
            co.weighted_score = co.normalized_score * co.weight
            scores.append(co)

            # Interest profile match
            pm = score_profile_match(paper, profile_context)
            pm.weight = self.weights.get(SignalType.INTEREST_PROFILE_MATCH, 0.0)
            pm.weighted_score = pm.normalized_score * pm.weight
            scores.append(pm)

            # Apply negative demotion
            apply_negative_demotion(scores, paper, profile_context)

        composite = sum(s.weighted_score for s in scores)

        return RankingExplanation(
            composite_score=composite,
            signal_breakdown=scores,
            ranker_version=self.RANKER_VERSION,
        )

    def capture_snapshot(
        self,
        profile_context: ProfileContext | None = None,
    ) -> RankerSnapshot:
        """Capture current pipeline configuration as a snapshot.

        Args:
            profile_context: Profile context used for ranking, or None.

        Returns:
            RankerSnapshot with full configuration state.
        """
        if profile_context is not None:
            return RankerSnapshot(
                profile_slug=profile_context.profile_slug,
                ranker_version=self.RANKER_VERSION,
                weights=dict(self.weights),
                signal_types_applied=list(self.weights.keys()),
                seed_paper_count=len(profile_context.seed_papers),
                followed_author_count=len(profile_context.followed_authors),
                negative_example_count=len(profile_context.negative_papers),
                saved_query_count=len(profile_context.query_slugs),
                negative_weight=profile_context.negative_weight,
            )
        else:
            return RankerSnapshot(
                profile_slug=None,
                ranker_version=self.RANKER_VERSION,
                weights=dict(self.weights),
                signal_types_applied=[SignalType.QUERY_MATCH, SignalType.RECENCY],
                seed_paper_count=0,
                followed_author_count=0,
                negative_example_count=0,
                saved_query_count=0,
                negative_weight=0.0,
            )
