#!/usr/bin/env python3
"""
W1D: Profile 4 baseline strategies (S6a-S6d).

These baselines calibrate the quality scale. Every real strategy in W1A-C
must beat these to be worth configuring.

Strategies:
    S6a: Random -- return random papers. Lower bound for everything.
    S6b: Most recent -- return papers by submission date (newest first).
    S6c: Most cited (OpenAlex) -- return papers by cited_by_count.
    S6d: Same primary category -- return papers matching seed category.

Uses the evaluation harness built in W0.2.
"""

from __future__ import annotations

import json
import random
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SPIKE_003_DIR = Path(__file__).resolve().parent.parent
SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
EXPERIMENTS_DIR = SPIKE_003_DIR / "experiments"

sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import StrategyProfiler
from harness.strategy_protocol import SimpleStrategy, RandomBaseline

# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

HARVEST_DB = str(SPIKE_001_DATA / "spike_001_harvest.db")
OPENALEX_CACHE = str(SPIKE_001_DATA / "b2_openalex_cache.json")
PROFILES_PATH = str(EXPERIMENTS_DIR / "data" / "interest_profiles.json")
OUTPUT_PATH = str(EXPERIMENTS_DIR / "data" / "w1d_baseline_profiles.json")


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------

def load_submission_dates(db_path: str) -> dict[str, str]:
    """Load submitted_date for all papers from the harvest DB.

    Returns dict mapping arxiv_id -> submitted_date string.
    """
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT arxiv_id, submitted_date FROM papers").fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows if row[1]}


def load_primary_categories(db_path: str) -> dict[str, str]:
    """Load primary_category for all papers from the harvest DB."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT arxiv_id, primary_category FROM papers").fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows if row[1]}


def load_openalex_citations(cache_path: str) -> dict[str, int]:
    """Load cited_by_count from the OpenAlex cache.

    Returns dict mapping arxiv_id -> cited_by_count (int).
    Papers not in the cache are absent from the dict.
    """
    with open(cache_path) as f:
        data = json.load(f)

    citations = {}
    for arxiv_id, entry in data.items():
        if isinstance(entry, dict):
            count = entry.get("cited_by_count")
            if count is not None:
                citations[arxiv_id] = int(count)
    return citations


def parse_date_to_epoch(date_str: str) -> float:
    """Parse a date string to epoch seconds for sorting.

    Handles the format 'Thu, 22 Oct 2020 05:19:58 GMT' from arXiv OAI.
    Falls back to 0.0 on parse failure.
    """
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(date_str)
        return dt.timestamp()
    except Exception:
        pass

    # Fallback: try ISO format
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.timestamp()
    except Exception:
        return 0.0


# ---------------------------------------------------------------------------
# Baseline strategy factories
# ---------------------------------------------------------------------------

def make_most_recent_strategy(
    paper_ids: list[str], dates: dict[str, str]
) -> SimpleStrategy:
    """S6b: Most recent -- papers sorted by submission date, newest first.

    Score = epoch seconds of submitted_date (higher = more recent = ranked first).
    Papers without dates get score 0.
    """
    # Pre-compute epoch scores for all papers
    epoch_scores = np.zeros(len(paper_ids), dtype=np.float64)
    for i, pid in enumerate(paper_ids):
        date_str = dates.get(pid, "")
        epoch_scores[i] = parse_date_to_epoch(date_str) if date_str else 0.0

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        """Return epoch-second scores (seed-independent)."""
        return epoch_scores

    return SimpleStrategy(
        name="Most recent (S6b)",
        strategy_id="S6b",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_most_cited_strategy(
    paper_ids: list[str], citations: dict[str, int]
) -> SimpleStrategy:
    """S6c: Most cited (OpenAlex) -- papers sorted by cited_by_count.

    Score = cited_by_count. Papers without OpenAlex data get score 0.
    Only ~500 papers have enrichment data, so this is a partial baseline.
    """
    citation_scores = np.zeros(len(paper_ids), dtype=np.float64)
    enriched_count = 0
    for i, pid in enumerate(paper_ids):
        count = citations.get(pid, 0)
        citation_scores[i] = float(count)
        if count > 0:
            enriched_count += 1

    print(f"  S6c citation data: {enriched_count}/{len(paper_ids)} papers "
          f"have cited_by_count > 0 ({100*enriched_count/len(paper_ids):.1f}%)")

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        """Return citation count scores (seed-independent)."""
        return citation_scores

    return SimpleStrategy(
        name="Most cited / OpenAlex (S6c)",
        strategy_id="S6c",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_same_category_strategy(
    paper_ids: list[str], categories: dict[str, str]
) -> SimpleStrategy:
    """S6d: Same primary category -- match seed papers' most common category.

    For each seed set:
      1. Find the most common primary_category among seeds.
      2. Score papers in that category = 1.0, others = 0.0.
      3. Within the category, add a small random tiebreaker.

    This tests whether arXiv category alone provides useful filtering.
    """
    # Pre-build category -> paper index mapping
    category_to_indices: dict[str, list[int]] = {}
    for i, pid in enumerate(paper_ids):
        cat = categories.get(pid, "unknown")
        if cat not in category_to_indices:
            category_to_indices[cat] = []
        category_to_indices[cat].append(i)

    rng = np.random.RandomState(42)

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        """Score 1.0 for papers in the seeds' most common category, 0.0 otherwise."""
        # Find most common category among seeds
        cat_counts: dict[str, int] = {}
        for sid in seed_ids:
            cat = categories.get(sid, "unknown")
            cat_counts[cat] = cat_counts.get(cat, 0) + 1

        if not cat_counts:
            return np.zeros(len(paper_ids), dtype=np.float64)

        dominant_cat = max(cat_counts, key=cat_counts.get)

        scores = np.zeros(len(paper_ids), dtype=np.float64)
        matching_indices = category_to_indices.get(dominant_cat, [])
        for idx in matching_indices:
            # 1.0 base + small tiebreaker to randomize within category
            scores[idx] = 1.0 + rng.random() * 0.001

        return scores

    return SimpleStrategy(
        name="Same primary category (S6d)",
        strategy_id="S6d",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("W1D: Baseline Strategy Profiling (S6a-S6d)")
    print("=" * 70)
    t_start = time.time()

    # -----------------------------------------------------------------------
    # 1. Load profiler (includes corpus, embeddings, clusters, profiles)
    # -----------------------------------------------------------------------
    print("\n--- Loading profiler infrastructure ---")
    profiler = StrategyProfiler.from_spike_data()

    if not profiler.profiles:
        print("ERROR: No interest profiles loaded. Cannot profile baselines.")
        sys.exit(1)

    print(f"\nReady: {len(profiler.paper_ids)} papers, "
          f"{len(profiler.profiles)} profiles")

    # -----------------------------------------------------------------------
    # 2. Load auxiliary data for baselines
    # -----------------------------------------------------------------------
    print("\n--- Loading baseline-specific data ---")

    print("Loading submission dates...")
    dates = load_submission_dates(HARVEST_DB)
    print(f"  {len(dates)} papers with submission dates")

    print("Loading primary categories...")
    categories = load_primary_categories(HARVEST_DB)
    print(f"  {len(categories)} papers with categories")

    print("Loading OpenAlex citation data...")
    citations = load_openalex_citations(OPENALEX_CACHE)
    print(f"  {len(citations)} papers with citation counts")

    # -----------------------------------------------------------------------
    # 3. Create baseline strategies
    # -----------------------------------------------------------------------
    print("\n--- Creating baseline strategies ---")

    s6a = RandomBaseline(profiler.paper_ids, seed=42)
    s6b = make_most_recent_strategy(profiler.paper_ids, dates)
    s6c = make_most_cited_strategy(profiler.paper_ids, citations)
    s6d = make_same_category_strategy(profiler.paper_ids, categories)

    baselines = [s6a, s6b, s6c, s6d]

    # -----------------------------------------------------------------------
    # 4. Profile each baseline
    # -----------------------------------------------------------------------
    cards = []
    for strategy in baselines:
        print(f"\n{'=' * 70}")
        print(f"Profiling: {strategy.name} ({strategy.strategy_id})")
        print("=" * 70)

        card = profiler.profile(
            strategy,
            config={"type": "baseline", "strategy_class": strategy.strategy_id},
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=50,
        )
        cards.append(card)

        # Print summary for this baseline
        print(f"\n  --- {strategy.name} summary ---")
        for inst_name, inst_data in card.get("instruments", {}).items():
            mean = inst_data.get("mean")
            std = inst_data.get("std")
            if mean is not None:
                print(f"  {inst_name:<25s} mean={mean:.4f}  std={std:.4f}")
            else:
                print(f"  {inst_name:<25s} (no data)")

        res = card.get("resources", {})
        latency = res.get("query_latency_ms", {})
        if latency:
            print(f"  latency p50={latency.get('p50', '?'):.2f}ms  "
                  f"p95={latency.get('p95', '?'):.2f}ms")

    # -----------------------------------------------------------------------
    # 5. Comparison
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("BASELINE COMPARISON")
    print("=" * 70)

    comparison = profiler.compare(cards)

    print("\nInstrument rankings (higher value = higher rank):")
    for inst_name, inst_data in comparison.get("instruments", {}).items():
        ranking = inst_data.get("ranking", [])
        values = inst_data.get("values", [])
        val_str = ", ".join(
            f"{v['strategy_id']}={v['mean']:.4f}" if v['mean'] is not None else f"{v['strategy_id']}=n/a"
            for v in values
        )
        print(f"  {inst_name:<25s} [{' > '.join(ranking)}]  ({val_str})")

    # -----------------------------------------------------------------------
    # 6. Save results
    # -----------------------------------------------------------------------
    output = {
        "metadata": {
            "task": "W1D: Baseline strategy profiling",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "corpus_size": len(profiler.paper_ids),
            "n_profiles": len(profiler.profiles),
            "baselines": [s.strategy_id for s in baselines],
            "duration_s": round(time.time() - t_start, 1),
        },
        "cards": {card["strategy_id"]: card for card in cards},
        "comparison": comparison,
    }

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to: {OUTPUT_PATH}")
    print(f"Total duration: {time.time() - t_start:.1f}s")

    # -----------------------------------------------------------------------
    # 7. Print the bar that real strategies must clear
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("BASELINE BAR (mean instrument values across 8 profiles)")
    print("=" * 70)
    print(f"\n{'Instrument':<25s} {'S6a Random':>12s} {'S6b Recent':>12s} "
          f"{'S6c Cited':>12s} {'S6d Category':>12s}")
    print("-" * 73)

    instrument_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]

    for inst_name in instrument_names:
        vals = []
        for card in cards:
            mean = card.get("instruments", {}).get(inst_name, {}).get("mean")
            if mean is not None:
                vals.append(f"{mean:.4f}")
            else:
                vals.append("n/a")
        print(f"  {inst_name:<25s} {vals[0]:>10s}   {vals[1]:>10s}   "
              f"{vals[2]:>10s}   {vals[3]:>10s}")

    print()
    print("Real strategies must beat these numbers to justify their complexity.")


if __name__ == "__main__":
    main()
