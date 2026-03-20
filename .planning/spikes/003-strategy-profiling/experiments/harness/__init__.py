"""
Spike 003 evaluation harness: strategy profiling infrastructure.

Provides a reusable framework for profiling any recommendation strategy
against 7 quality instruments and 7 resource metrics, producing structured
strategy profile cards.
"""

from .strategy_protocol import RecommendationStrategy
from .instruments import (
    leave_one_out_mrr,
    seed_proximity,
    topical_coherence,
    cluster_diversity,
    novelty,
    category_surprise,
    coverage,
    run_all_instruments,
)
from .resource_meter import measure_latency, measure_memory, measure_setup_time
from .profiler import StrategyProfiler
from .review_template import generate_review_template

__all__ = [
    "RecommendationStrategy",
    "leave_one_out_mrr",
    "seed_proximity",
    "topical_coherence",
    "cluster_diversity",
    "novelty",
    "category_surprise",
    "coverage",
    "run_all_instruments",
    "measure_latency",
    "measure_memory",
    "measure_setup_time",
    "StrategyProfiler",
    "generate_review_template",
]
