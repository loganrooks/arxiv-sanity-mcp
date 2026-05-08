"""
W2.2: Top-K Aggressiveness Sweep

For each passing strategy (S1a MiniLM, S1c SPECTER2, S1d TF-IDF),
profile at top-K values: 10, 20, 50, 100, 200.

Uses 3 representative profiles (P1 medium, P3 narrow, P4 broad) x 1 seed
selection (subset_5) to keep it tractable.

Key question: Is there an elbow where increasing K sharply degrades
coherence? Or is the tradeoff smooth?

Metrics collected per (strategy, K):
  - leave_one_out_mrr (LOO at that K depth)
  - seed_proximity
  - topical_coherence
  - cluster_diversity
  - novelty
  - category_surprise
  - coverage
"""

from __future__ import annotations

import json
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
from harness.strategy_protocol import SimpleStrategy
from harness.profiler import InterestProfile, load_interest_profiles

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
OUTPUT_PATH = SPIKE_003_DATA / "w2_2_topk_results.json"

# Sweep parameters
K_VALUES = [10, 20, 50, 100, 200]
REPRESENTATIVE_PROFILES = ["P1", "P3", "P4"]  # medium, narrow, broad
SEED_SET_INDEX = 0  # Use first seed set (subset_5) for each profile


# ---------------------------------------------------------------------------
# Strategy constructors (reused from W1A)
# ---------------------------------------------------------------------------

def make_embedding_centroid_strategy(
    embeddings: np.ndarray,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
    name: str,
    strategy_id: str,
) -> SimpleStrategy:
    """Embedding centroid similarity (dot product on L2-normalized vecs)."""

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
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
) -> SimpleStrategy:
    """TF-IDF cosine similarity."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    print("  Building TF-IDF matrix (max_features=50000)...")
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    t1 = time.perf_counter()
    print(f"  TF-IDF matrix: {tfidf_matrix.shape}, built in {t1 - t0:.1f}s")

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        seed_vectors = tfidf_matrix[seed_indices]
        centroid = np.asarray(seed_vectors.mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
        return scores

    return SimpleStrategy(
        name="TF-IDF cosine similarity",
        strategy_id="S1d",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Main sweep
# ---------------------------------------------------------------------------

def run_topk_sweep():
    """Run the full top-K sweep across strategies and K values."""

    print("=" * 70)
    print("W2.2: Top-K Aggressiveness Sweep")
    print("=" * 70)
    t_start = time.perf_counter()

    # ----- Load data -----
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

    # Filter to representative profiles
    all_profiles = profiler.profiles
    selected_profiles = [p for p in all_profiles if p.profile_id in REPRESENTATIVE_PROFILES]
    print(f"\nUsing {len(selected_profiles)} representative profiles: "
          f"{[p.profile_id for p in selected_profiles]}")
    for p in selected_profiles:
        n_seeds = len(p.seed_sets[SEED_SET_INDEX]) if p.seed_sets else 0
        print(f"  {p.profile_id} ({p.name}): breadth={p.breadth}, "
              f"using seed set {SEED_SET_INDEX} with {n_seeds} seeds, "
              f"{len(p.cluster_papers)} cluster papers")

    # ----- Build abstracts for TF-IDF -----
    print("\nLoading abstracts from DB...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
    abstract_map = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    abstracts = [abstract_map.get(pid, "") for pid in paper_ids]

    # ----- Build strategies -----
    print("\n--- Building Strategies ---")

    s1a = make_embedding_centroid_strategy(
        profiler.embeddings, paper_ids, id_to_idx,
        name="MiniLM embedding centroid",
        strategy_id="S1a",
    )

    s1c = None
    if profiler.specter2_embeddings is not None:
        s1c = make_embedding_centroid_strategy(
            profiler.specter2_embeddings, paper_ids, profiler.specter2_id_to_idx,
            name="SPECTER2 adapter embedding centroid",
            strategy_id="S1c",
        )

    s1d = make_tfidf_strategy(abstracts, paper_ids, id_to_idx)

    strategies = [("S1a", s1a), ("S1c", s1c), ("S1d", s1d)]
    strategies = [(sid, s) for sid, s in strategies if s is not None]

    # ----- Run sweep -----
    print(f"\n--- Running Sweep: {len(strategies)} strategies x {len(K_VALUES)} K values ---")
    print(f"K values: {K_VALUES}")

    # Results structure: {strategy_id: {k_value: {profile_id: instruments}}}
    results = {}

    for sid, strategy in strategies:
        results[sid] = {}
        print(f"\n{'=' * 60}")
        print(f"Strategy: {strategy.name} ({sid})")
        print(f"{'=' * 60}")

        for k in K_VALUES:
            print(f"\n  --- K={k} ---")
            results[sid][k] = {}

            for prof in selected_profiles:
                seed_set = prof.seed_sets[SEED_SET_INDEX]
                print(f"    {prof.profile_id} ({prof.breadth})...", end=" ")

                # Get recommendations at this K
                recs = strategy.recommend(seed_set, top_k=k)
                rec_ids = [r[0] for r in recs]

                if not rec_ids:
                    print("no results")
                    results[sid][k][prof.profile_id] = {"error": "no results"}
                    continue

                # Run all instruments at this K
                from harness.instruments import run_all_instruments
                instruments = run_all_instruments(
                    strategy=strategy,
                    recommended_ids=rec_ids,
                    seed_ids=seed_set,
                    cluster_papers=prof.cluster_papers,
                    all_paper_ids=paper_ids,
                    embeddings=profiler.embeddings,
                    id_to_idx=id_to_idx,
                    paper_to_cluster=profiler.paper_to_cluster,
                    paper_categories=profiler.paper_categories,
                    top_k=k,
                    run_loo=True,
                )

                # Extract scalar values
                scalar_results = {}
                for inst_name, inst_data in instruments.items():
                    scalar_results[inst_name] = inst_data.get("value")

                results[sid][k][prof.profile_id] = scalar_results

                mrr = scalar_results.get("leave_one_out_mrr", 0)
                coher = scalar_results.get("topical_coherence", 0)
                cov = scalar_results.get("coverage", 0)
                print(f"MRR={mrr:.4f}, Coher={coher:.4f}, Cov={cov:.4f}")

    # ----- Aggregate per (strategy, K) -----
    print(f"\n{'=' * 60}")
    print("AGGREGATED RESULTS (mean across 3 profiles)")
    print(f"{'=' * 60}")

    aggregated = {}  # {strategy_id: {k: {metric: mean_value}}}
    instrument_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]

    for sid in results:
        aggregated[sid] = {}
        for k in K_VALUES:
            k_data = results[sid].get(k, {})
            k_agg = {}
            for inst_name in instrument_names:
                values = []
                for pid, prof_data in k_data.items():
                    if isinstance(prof_data, dict) and "error" not in prof_data:
                        val = prof_data.get(inst_name)
                        if val is not None:
                            values.append(val)
                k_agg[inst_name] = {
                    "mean": float(np.mean(values)) if values else None,
                    "std": float(np.std(values)) if values else None,
                    "values": values,
                }
            aggregated[sid][k] = k_agg

    # Print summary table
    print(f"\n{'Strategy':<8s} {'K':>4s} {'MRR':>8s} {'Prox':>8s} {'Coher':>8s} "
          f"{'Div':>6s} {'Nov':>8s} {'Surpr':>8s} {'Cover':>8s}")
    print("-" * 80)

    for sid in sorted(aggregated.keys()):
        for k in K_VALUES:
            k_agg = aggregated[sid][k]

            def fmt(metric_name):
                d = k_agg.get(metric_name, {})
                v = d.get("mean")
                return f"{v:8.4f}" if v is not None else f"{'N/A':>8s}"

            print(f"{sid:<8s} {k:>4d} {fmt('leave_one_out_mrr')} {fmt('seed_proximity')} "
                  f"{fmt('topical_coherence')} {fmt('cluster_diversity'):>6s} "
                  f"{fmt('novelty')} {fmt('category_surprise')} {fmt('coverage')}")
        print()  # blank line between strategies

    # ----- Analyze elbows / tradeoffs -----
    print(f"\n{'=' * 60}")
    print("TRADEOFF ANALYSIS")
    print(f"{'=' * 60}")

    for sid in sorted(aggregated.keys()):
        print(f"\n  {sid}:")
        k_means = {}
        for k in K_VALUES:
            k_agg = aggregated[sid][k]
            k_means[k] = {
                name: k_agg.get(name, {}).get("mean")
                for name in instrument_names
            }

        # Check coherence drop from K=10 to K=200
        c10 = k_means[10].get("topical_coherence")
        c200 = k_means[200].get("topical_coherence")
        if c10 is not None and c200 is not None:
            drop_pct = (c10 - c200) / c10 * 100
            print(f"    Coherence drop K=10 to K=200: {c10:.4f} -> {c200:.4f} ({drop_pct:+.1f}%)")

        # Check coverage gain
        cov10 = k_means[10].get("coverage")
        cov200 = k_means[200].get("coverage")
        if cov10 is not None and cov200 is not None:
            gain_pct = (cov200 - cov10) / max(cov10, 1e-10) * 100
            print(f"    Coverage gain K=10 to K=200: {cov10:.4f} -> {cov200:.4f} ({gain_pct:+.1f}%)")

        # Check MRR trend (should increase or plateau as K increases)
        mrr10 = k_means[10].get("leave_one_out_mrr")
        mrr200 = k_means[200].get("leave_one_out_mrr")
        if mrr10 is not None and mrr200 is not None:
            change = mrr200 - mrr10
            print(f"    MRR change K=10 to K=200: {mrr10:.4f} -> {mrr200:.4f} ({change:+.4f})")

        # Look for elbow: find K where coherence drops most sharply
        coherences = [(k, k_means[k].get("topical_coherence")) for k in K_VALUES]
        coherences = [(k, c) for k, c in coherences if c is not None]
        if len(coherences) >= 2:
            max_drop_k = None
            max_drop_val = 0
            for i in range(1, len(coherences)):
                k_prev, c_prev = coherences[i - 1]
                k_curr, c_curr = coherences[i]
                drop = c_prev - c_curr
                if drop > max_drop_val:
                    max_drop_val = drop
                    max_drop_k = (k_prev, k_curr)
            if max_drop_k:
                print(f"    Largest coherence drop: between K={max_drop_k[0]} and K={max_drop_k[1]} "
                      f"(delta={max_drop_val:.4f})")

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    # Convert integer keys to strings for JSON
    json_results = {}
    for sid, k_dict in results.items():
        json_results[sid] = {}
        for k, prof_dict in k_dict.items():
            json_results[sid][str(k)] = prof_dict

    json_aggregated = {}
    for sid, k_dict in aggregated.items():
        json_aggregated[sid] = {}
        for k, metrics in k_dict.items():
            json_aggregated[sid][str(k)] = metrics

    output = {
        "experiment": "W2.2: Top-K Aggressiveness Sweep",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_time_s": round(total_time, 1),
        "config": {
            "k_values": K_VALUES,
            "representative_profiles": REPRESENTATIVE_PROFILES,
            "seed_set_index": SEED_SET_INDEX,
            "corpus_size": n_papers,
        },
        "per_strategy_per_k_per_profile": json_results,
        "aggregated": json_aggregated,
        "notes": {
            "reduced_profile_set": (
                "Used 3 representative profiles (P1 medium, P3 narrow, P4 broad) "
                "with 1 seed set each (subset_5) to keep computation tractable. "
                "Full W1A used 8 profiles x 3 seed sets."
            ),
            "loo_at_k": (
                "LOO MRR is evaluated at each K value -- the held-out paper must "
                "appear in the top-K to score. Higher K mechanically increases MRR."
            ),
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n{'=' * 60}")
    print(f"W2.2 COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total time: {total_time:.1f}s ({total_time / 60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    run_topk_sweep()
