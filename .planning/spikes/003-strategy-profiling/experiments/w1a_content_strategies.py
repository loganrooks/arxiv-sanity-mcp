"""
W1A: Content-based strategy profiling.

Profiles the core content-based recommendation strategies:
  S1a - MiniLM embedding centroid similarity
  S1c - SPECTER2 adapter embedding centroid similarity
  S1b - SPECTER2 base (SKIPPED -- no persisted base embeddings)
  S1d - TF-IDF cosine similarity
  S1i - SVM on user library (LinearSVC, arxiv-sanity-lite approach)
  S1j - MiniLM centroid dot product (cheapest embedding strategy)
  S1g - Title-only MiniLM (if time permits)
  S1h - Title-only SPECTER2 (if time permits)

All strategies profiled across 8 interest profiles x 3 seed subsets = 24 runs each,
using the evaluation harness (7 quality instruments + resource measurement).
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Ensure experiments dir is on path
EXPERIMENTS_DIR = Path(__file__).resolve().parent
SPIKE_003_DIR = EXPERIMENTS_DIR.parent
sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import StrategyProfiler
from harness.strategy_protocol import SimpleStrategy, RandomBaseline
from harness.resource_meter import measure_latency, measure_setup_time, measure_storage


# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
SPIKE_002_DATA = SPIKE_003_DIR.parent / "002-backend-comparison" / "experiments" / "data"
SPIKE_003_DATA = SPIKE_003_DIR / "experiments" / "data"

DB_PATH = SPIKE_001_DATA / "spike_001_harvest.db"
MINILM_EMB_PATH = SPIKE_002_DATA / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DATA / "arxiv_ids_19k.json"
SPECTER2_EMB_PATH = SPIKE_003_DATA / "specter2_adapter_19k.npy"
SPECTER2_IDS_PATH = SPIKE_003_DATA / "specter2_adapter_ids.json"
PROFILES_PATH = SPIKE_003_DATA / "interest_profiles.json"
OUTPUT_PATH = SPIKE_003_DATA / "w1a_content_profiles.json"


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def make_embedding_centroid_strategy(
    embeddings: np.ndarray,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
    name: str,
    strategy_id: str,
) -> SimpleStrategy:
    """S1a/S1c/S1j: Embedding centroid similarity.

    Compute centroid of seed embeddings, rank all papers by cosine
    similarity (= dot product for L2-normalized vectors) to centroid.
    """

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))

        # Compute seed centroid and normalize
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm

        # Cosine similarity = dot product for normalized embeddings
        scores = embeddings @ centroid
        return scores

    return SimpleStrategy(
        name=name,
        strategy_id=strategy_id,
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_tfidf_strategy(
    abstracts: list[str],
    paper_ids: list[str],
    id_to_idx: dict[str, int],
) -> tuple[SimpleStrategy, object]:
    """S1d: TF-IDF cosine similarity.

    Build TF-IDF matrix from abstracts, compute cosine similarity to
    seed centroid. Returns (strategy, tfidf_matrix) for SVM reuse.
    """
    from sklearn.feature_extraction.text import TfidfVectorizer

    print("  Building TF-IDF matrix (max_features=50000)...")
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    t1 = time.perf_counter()
    print(f"  TF-IDF matrix: {tfidf_matrix.shape}, built in {t1-t0:.1f}s")

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))

        # Compute centroid of seed TF-IDF vectors (sparse -> dense array)
        seed_vectors = tfidf_matrix[seed_indices]
        centroid = np.asarray(seed_vectors.mean(axis=0)).flatten()

        # Normalize centroid for cosine similarity
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm

        # Cosine similarity: sparse TF-IDF matrix @ dense centroid
        scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
        return scores

    strategy = SimpleStrategy(
        name="TF-IDF cosine similarity",
        strategy_id="S1d",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )

    return strategy, tfidf_matrix


def make_svm_strategy(
    tfidf_matrix,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
) -> SimpleStrategy:
    """S1i: SVM on user library (arxiv-sanity-lite approach).

    Train LinearSVC on TF-IDF features. Positive class = seed papers.
    Score all papers by SVM decision function.
    """
    from sklearn.svm import LinearSVC

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = set(id_to_idx[sid] for sid in seed_ids if sid in id_to_idx)
        if not seed_indices:
            return np.zeros(len(paper_ids))

        # Build labels: 1 for seeds, 0 for everything else
        y = np.array([1 if i in seed_indices else 0 for i in range(len(paper_ids))])

        # Train SVM
        svm = LinearSVC(C=0.01, class_weight="balanced", max_iter=5000)
        svm.fit(tfidf_matrix, y)

        # Score all papers by decision function (distance from hyperplane)
        scores = svm.decision_function(tfidf_matrix)
        return scores

    return SimpleStrategy(
        name="SVM on user library (TF-IDF)",
        strategy_id="S1i",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_all_content_strategies():
    """Profile all content-based strategies and save results."""

    print("=" * 70)
    print("W1A: Content-Based Strategy Profiling")
    print("=" * 70)
    t_start = time.perf_counter()

    # ----- Load profiler (handles data loading + clustering) -----
    print("\n--- Data Loading ---")
    profiler = StrategyProfiler.from_spike_data(
        db_path=str(DB_PATH),
        minilm_emb_path=str(MINILM_EMB_PATH),
        minilm_ids_path=str(MINILM_IDS_PATH),
        profiles_path=str(PROFILES_PATH),
        specter2_emb_path=str(SPECTER2_EMB_PATH),
        specter2_ids_path=str(SPECTER2_IDS_PATH),
    )

    paper_ids = profiler.paper_ids
    id_to_idx = profiler.id_to_idx
    n_papers = len(paper_ids)
    print(f"\nCorpus: {n_papers} papers, {len(profiler.profiles)} profiles")

    # ----- Load abstracts for TF-IDF -----
    print("\nLoading abstracts from DB...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
    abstract_map = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    # Build abstracts list in same order as paper_ids
    abstracts = [abstract_map.get(pid, "") for pid in paper_ids]
    missing_abstracts = sum(1 for a in abstracts if not a)
    print(f"  {n_papers - missing_abstracts} abstracts loaded, {missing_abstracts} missing")

    # ----- Build all strategies -----
    print("\n--- Building Strategies ---")
    all_cards = []
    strategy_timings = {}

    # S6a: Random baseline (for comparison floor)
    print("\n[S6a] Random baseline")
    s6a = RandomBaseline(paper_ids, seed=42)

    # S1a: MiniLM embedding centroid
    print("\n[S1a] MiniLM embedding centroid similarity")
    s1a = make_embedding_centroid_strategy(
        profiler.embeddings, paper_ids, id_to_idx,
        name="MiniLM embedding centroid",
        strategy_id="S1a",
    )

    # S1c: SPECTER2 adapter embedding centroid
    print("\n[S1c] SPECTER2 adapter embedding centroid similarity")
    if profiler.specter2_embeddings is not None:
        s1c = make_embedding_centroid_strategy(
            profiler.specter2_embeddings, paper_ids, profiler.specter2_id_to_idx,
            name="SPECTER2 adapter embedding centroid",
            strategy_id="S1c",
        )
    else:
        print("  SKIPPED -- SPECTER2 adapter embeddings not available")
        s1c = None

    # S1b: SPECTER2 base (no adapter) -- NOT AVAILABLE
    print("\n[S1b] SPECTER2 base (no adapter)")
    print("  SKIPPED -- no persisted base embeddings from Spike 002")
    print("  (Spike 002 computed SPECTER2 base transiently for comparison)")
    s1b = None

    # S1d: TF-IDF cosine similarity
    print("\n[S1d] TF-IDF cosine similarity")
    s1d, tfidf_matrix = make_tfidf_strategy(abstracts, paper_ids, id_to_idx)

    # S1i: SVM on user library
    print("\n[S1i] SVM on user library (LinearSVC, C=0.01, balanced)")
    s1i = make_svm_strategy(tfidf_matrix, paper_ids, id_to_idx)

    # S1j: MiniLM centroid dot product (same math as S1a but explicitly
    # the cheapest -- no normalization of centroid, raw dot product)
    print("\n[S1j] MiniLM centroid dot product (unnormalized centroid)")

    def s1j_score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        # Raw mean centroid, no re-normalization
        centroid = profiler.embeddings[seed_indices].mean(axis=0)
        scores = profiler.embeddings @ centroid
        return scores

    s1j = SimpleStrategy(
        name="MiniLM centroid dot product (raw)",
        strategy_id="S1j",
        score_fn=s1j_score_fn,
        paper_ids=paper_ids,
    )

    # ----- Profile each strategy -----
    strategies = [
        ("S6a", s6a, {}),
        ("S1a", s1a, {"embedding": "MiniLM", "dim": 384, "centroid": "normalized"}),
        ("S1c", s1c, {"embedding": "SPECTER2_adapter", "dim": 768, "centroid": "normalized"}),
        ("S1d", s1d, {"features": "TF-IDF", "max_features": 50000, "centroid": "normalized"}),
        ("S1i", s1i, {"features": "TF-IDF", "max_features": 50000, "svm": "LinearSVC", "C": 0.01}),
        ("S1j", s1j, {"embedding": "MiniLM", "dim": 384, "centroid": "raw_mean"}),
    ]

    for sid, strategy, config in strategies:
        if strategy is None:
            print(f"\n{'='*60}")
            print(f"SKIPPING {sid} (not available)")
            print(f"{'='*60}")
            continue

        print(f"\n{'='*60}")
        print(f"PROFILING: {strategy.name} ({strategy.strategy_id})")
        print(f"{'='*60}")
        t0 = time.perf_counter()

        card = profiler.profile(
            strategy,
            config=config,
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=100,
        )
        t1 = time.perf_counter()
        strategy_timings[sid] = t1 - t0

        # Print summary
        print(f"\n  --- Summary for {sid} ---")
        instruments = card.get("instruments", {})
        for inst_name in [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]:
            inst = instruments.get(inst_name, {})
            mean = inst.get("mean")
            std = inst.get("std")
            if mean is not None:
                print(f"    {inst_name:<25s} {mean:.4f} (+/- {std:.4f})")
            else:
                print(f"    {inst_name:<25s} (no data)")

        res = card.get("resources", {})
        lat = res.get("query_latency_ms", {})
        if lat:
            print(f"    latency p50={lat.get('p50', 0):.2f}ms  p95={lat.get('p95', 0):.2f}ms")
        print(f"    profiling time: {strategy_timings[sid]:.1f}s")

        all_cards.append(card)

    # ----- Measure additional resource metrics -----
    print(f"\n{'='*60}")
    print("ADDITIONAL RESOURCE MEASUREMENTS")
    print(f"{'='*60}")

    # Storage footprint
    storage_info = {}
    storage_info["S1a"] = measure_storage([str(MINILM_EMB_PATH), str(MINILM_IDS_PATH)])
    if profiler.specter2_embeddings is not None:
        storage_info["S1c"] = measure_storage([str(SPECTER2_EMB_PATH), str(SPECTER2_IDS_PATH)])
    storage_info["S1d"] = {"total_mb": 0, "note": "TF-IDF matrix computed on-the-fly, not persisted"}
    storage_info["S1i"] = {"total_mb": 0, "note": "SVM model trained per-query, not persisted"}
    storage_info["S1j"] = storage_info["S1a"]  # Same data as S1a

    for sid, info in storage_info.items():
        print(f"  {sid} storage: {info}")

    # TF-IDF build time (setup cost)
    print("\n  Measuring TF-IDF build time...")
    tfidf_setup = measure_setup_time(
        setup_fn=lambda: __import__("sklearn.feature_extraction.text", fromlist=["TfidfVectorizer"]).TfidfVectorizer(
            max_features=50000, stop_words="english"
        ).fit_transform(abstracts),
        n_runs=3,
    )
    print(f"  TF-IDF build: mean={tfidf_setup['mean_s']:.2f}s")

    # SVM training time per query (embedded in query latency, but measure separately)
    print("  Measuring SVM train time (per query)...")
    test_seeds = profiler.profiles[0].seed_sets[0]
    svm_train_times = []
    for _ in range(10):
        t0 = time.perf_counter()
        s1i._score_fn(test_seeds)
        t1 = time.perf_counter()
        svm_train_times.append((t1 - t0) * 1000)
    print(f"  SVM train+score: mean={np.mean(svm_train_times):.1f}ms, p95={np.percentile(svm_train_times, 95):.1f}ms")

    # ----- Comparison -----
    print(f"\n{'='*60}")
    print("CROSS-STRATEGY COMPARISON")
    print(f"{'='*60}")
    comparison = profiler.compare(all_cards)

    # Print comparison table
    print(f"\n{'Strategy':<35s} {'MRR':>7s} {'Prox':>7s} {'Coher':>7s} {'Div':>7s} {'Novel':>7s} {'Surpr':>7s} {'Cover':>7s} {'p50ms':>7s}")
    print("-" * 100)
    for card in all_cards:
        sid = card["strategy_id"]
        name = card["strategy_name"][:32]
        inst = card.get("instruments", {})
        lat = card.get("resources", {}).get("query_latency_ms", {})

        mrr = inst.get("leave_one_out_mrr", {}).get("mean")
        prox = inst.get("seed_proximity", {}).get("mean")
        coher = inst.get("topical_coherence", {}).get("mean")
        div_ = inst.get("cluster_diversity", {}).get("mean")
        nov = inst.get("novelty", {}).get("mean")
        surp = inst.get("category_surprise", {}).get("mean")
        cov = inst.get("coverage", {}).get("mean")
        p50 = lat.get("p50")

        def fmt(v, width=7):
            return f"{v:{width}.4f}" if v is not None else f"{'N/A':>{width}s}"

        print(f"{name:<35s} {fmt(mrr)} {fmt(prox)} {fmt(coher)} {fmt(div_)} {fmt(nov)} {fmt(surp)} {fmt(cov)} {fmt(p50)}")

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "experiment": "W1A: Content-based strategy profiling",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_time_s": round(total_time, 1),
        "corpus_size": n_papers,
        "n_profiles": len(profiler.profiles),
        "strategies_profiled": [c["strategy_id"] for c in all_cards],
        "strategies_skipped": ["S1b"],
        "profile_cards": all_cards,
        "comparison": comparison,
        "additional_resources": {
            "storage": storage_info,
            "tfidf_build_time": tfidf_setup,
            "svm_train_time_ms": {
                "mean": round(float(np.mean(svm_train_times)), 1),
                "p95": round(float(np.percentile(svm_train_times, 95)), 1),
            },
        },
        "strategy_profiling_times_s": {k: round(v, 1) for k, v in strategy_timings.items()},
        "notes": {
            "S1b_skipped": "SPECTER2 base (no adapter) not profiled -- no persisted embeddings from Spike 002. "
                           "Spike 002 computed base embeddings transiently for QV3 comparison. "
                           "Base vs adapter cosine similarity ~0.96 suggests they are very similar.",
            "S1g_S1h_deferred": "Title-only strategies deferred to follow-up if needed.",
            "embeddings_aligned": "MiniLM and SPECTER2 adapter embeddings share identical ID ordering (19252 papers).",
            "normalization": "All embeddings are L2-normalized. Dot product = cosine similarity.",
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print(f"W1A COMPLETE")
    print(f"{'='*60}")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"Strategies profiled: {len(all_cards)}")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    run_all_content_strategies()
