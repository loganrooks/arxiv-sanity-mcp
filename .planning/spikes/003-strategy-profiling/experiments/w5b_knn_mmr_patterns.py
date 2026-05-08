#!/usr/bin/env python3
"""
Spike 003 / W5b: Strategy Pattern Experiments (kNN per seed, MMR)

Tests two alternative retrieval strategies on MiniLM embeddings:

1. kNN per seed: Instead of computing a centroid of seed embeddings and finding
   nearest neighbors to the centroid, find k nearest neighbors PER SEED paper
   and union all neighbor sets. This tests whether centroid averaging washes out
   distinctive seeds.

2. MMR (Maximal Marginal Relevance): Iteratively select papers that maximize
   lambda * sim(paper, seeds) - (1-lambda) * max_sim(paper, already_selected).
   lambda=0.7 is standard. This directly addresses coherence-diversity tension.

Evaluation: Compare against centroid top-K using the same evaluation harness
(held-out paper recall, MRR, etc.) across interest profiles.
"""

import json
import os
import sys
import time
import sqlite3
import numpy as np
from pathlib import Path

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

# ---- Configuration ----
PROJECT_ROOT = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp")
SPIKE_DIR = PROJECT_ROOT / ".planning/spikes/003-strategy-profiling"
DATA_DIR = SPIKE_DIR / "experiments/data"
ARXIV_IDS_FILE = PROJECT_ROOT / ".planning/spikes/002-backend-comparison/experiments/data/arxiv_ids_19k.json"
MINIML_EMB_FILE = DATA_DIR / "miniLM_title_19k.npy"
PROFILES_FILE = DATA_DIR / "interest_profiles.json"
OUTPUT_FILE = DATA_DIR / "w5b_knn_mmr_results.json"

TOP_K = 20
K_PER_SEED = 10   # neighbors per individual seed in kNN-per-seed
MMR_LAMBDA = 0.7  # standard MMR trade-off


def load_data():
    """Load embeddings, IDs, and profiles."""
    print("=== Loading data ===")

    with open(ARXIV_IDS_FILE) as f:
        all_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(all_ids)}

    embeddings = np.load(str(MINIML_EMB_FILE))
    # L2 normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1
    embeddings = embeddings / norms

    with open(PROFILES_FILE) as f:
        profiles = json.load(f)

    print(f"  Embeddings: {embeddings.shape}")
    print(f"  IDs: {len(all_ids)}")
    print(f"  Profiles: {list(profiles['profiles'].keys())}")

    return all_ids, id_to_idx, embeddings, profiles


# ---- Strategy 1: Centroid top-K (baseline) ----
def centroid_topk(embeddings, seed_indices, k, exclude_seeds=True):
    """Standard centroid-based kNN. Returns (indices, scores)."""
    centroid = embeddings[seed_indices].mean(axis=0)
    centroid = centroid / np.linalg.norm(centroid)

    scores = embeddings @ centroid
    # Exclude seeds from results
    if exclude_seeds:
        for idx in seed_indices:
            scores[idx] = -np.inf

    top_indices = np.argsort(scores)[::-1][:k]
    top_scores = scores[top_indices]
    return top_indices.tolist(), top_scores.tolist()


# ---- Strategy 2: kNN per seed (union) ----
def knn_per_seed(embeddings, seed_indices, k_per_seed, total_k, exclude_seeds=True):
    """Find k nearest neighbors for EACH seed, union by best score.

    Returns top total_k papers from the union, ranked by their best score
    across any seed.
    """
    seed_set = set(seed_indices)
    # For each paper, track its best similarity to any seed
    n_papers = len(embeddings)
    best_scores = np.full(n_papers, -np.inf)
    paper_sources = {}  # paper_idx -> list of seed_indices that nominated it

    for seed_idx in seed_indices:
        scores = embeddings @ embeddings[seed_idx]
        if exclude_seeds:
            for si in seed_indices:
                scores[si] = -np.inf

        top_k = np.argsort(scores)[::-1][:k_per_seed]
        for idx in top_k:
            idx_int = int(idx)
            if scores[idx] > best_scores[idx_int]:
                best_scores[idx_int] = scores[idx]
            if idx_int not in paper_sources:
                paper_sources[idx_int] = []
            paper_sources[idx_int].append(int(seed_idx))

    # Get the union of all nominated papers
    nominated = list(paper_sources.keys())
    if exclude_seeds:
        nominated = [i for i in nominated if i not in seed_set]

    # Sort by best score, take top total_k
    nominated.sort(key=lambda i: best_scores[i], reverse=True)
    top_indices = nominated[:total_k]
    top_scores = [float(best_scores[i]) for i in top_indices]

    # Also compute: how many seeds nominated each result
    n_sources = [len(paper_sources.get(i, [])) for i in top_indices]

    return top_indices, top_scores, n_sources


# ---- Strategy 3: MMR (Maximal Marginal Relevance) ----
def mmr_select(embeddings, seed_indices, k, lam=0.7, exclude_seeds=True):
    """Maximal Marginal Relevance selection.

    At each step, select the paper maximizing:
        lambda * sim(paper, seed_centroid) - (1-lambda) * max_sim(paper, selected)

    This balances relevance (first term) against diversity (second term).
    """
    seed_set = set(seed_indices)
    centroid = embeddings[seed_indices].mean(axis=0)
    centroid = centroid / np.linalg.norm(centroid)

    # Relevance scores to centroid
    relevance = embeddings @ centroid

    if exclude_seeds:
        for idx in seed_indices:
            relevance[idx] = -np.inf

    selected = []
    selected_scores = []
    candidates = set(range(len(embeddings)))
    if exclude_seeds:
        candidates -= seed_set

    for _ in range(k):
        best_score = -np.inf
        best_idx = -1

        for idx in candidates:
            if relevance[idx] == -np.inf:
                continue

            # Diversity term: max similarity to any already selected paper
            if selected:
                sims_to_selected = embeddings[idx] @ embeddings[selected].T
                max_sim_selected = float(np.max(sims_to_selected))
            else:
                max_sim_selected = 0.0

            mmr_score = lam * relevance[idx] - (1 - lam) * max_sim_selected

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        if best_idx < 0:
            break

        selected.append(best_idx)
        selected_scores.append(float(best_score))
        candidates.discard(best_idx)

    return selected, selected_scores


# ---- Evaluation ----
def evaluate_retrieval(retrieved_indices, held_out_indices, all_ids, id_to_idx):
    """Evaluate retrieval quality against held-out papers.

    Metrics:
    - Recall@K: fraction of held-out papers found in top-K
    - MRR: mean reciprocal rank of first held-out paper found
    - Hit@5, Hit@10, Hit@20: whether any held-out paper appears in top-5/10/20
    """
    retrieved_set = set(retrieved_indices)
    held_out_set = set(held_out_indices)

    # Recall
    hits = retrieved_set & held_out_set
    recall = len(hits) / len(held_out_set) if held_out_set else 0

    # MRR - reciprocal rank of first held-out paper in retrieved list
    mrr = 0
    for rank, idx in enumerate(retrieved_indices, 1):
        if idx in held_out_set:
            mrr = 1.0 / rank
            break

    # Hit@K
    hit_at = {}
    for cutoff in [5, 10, 20]:
        top_set = set(retrieved_indices[:cutoff])
        hit_at[cutoff] = 1 if (top_set & held_out_set) else 0

    return {
        "recall": round(recall, 4),
        "mrr": round(mrr, 4),
        "hits_found": len(hits),
        "held_out_total": len(held_out_set),
        "hit_at_5": hit_at[5],
        "hit_at_10": hit_at[10],
        "hit_at_20": hit_at[20],
    }


def compute_diversity(embeddings, indices):
    """Compute average pairwise distance (1 - cosine_sim) among retrieved papers.
    Higher = more diverse.
    """
    if len(indices) < 2:
        return 0.0
    emb = embeddings[indices]
    sim_matrix = emb @ emb.T
    n = len(indices)
    # Average off-diagonal similarity
    total_sim = (sim_matrix.sum() - n) / (n * (n - 1))
    diversity = 1 - total_sim
    return round(float(diversity), 4)


def run_comparison(all_ids, id_to_idx, embeddings, profiles):
    """Run all three strategies across all profiles and seed subsets."""
    print("\n=== Running strategy comparison ===")

    all_results = []

    for pid, profile in profiles["profiles"].items():
        print(f"\n  Profile {pid}: {profile['name']}")

        held_out_ids = [p["arxiv_id"] for p in profile["held_out_papers"]]
        held_out_indices = [id_to_idx[aid] for aid in held_out_ids if aid in id_to_idx]

        for subset_name in ["subset_5", "subset_10", "subset_15"]:
            seed_ids = profile["seed_subsets"].get(subset_name, [])
            if not seed_ids:
                continue

            seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
            n_seeds = len(seed_indices)

            # Strategy 1: Centroid
            centroid_idx, centroid_scores = centroid_topk(
                embeddings, seed_indices, TOP_K
            )
            centroid_eval = evaluate_retrieval(
                centroid_idx, held_out_indices, all_ids, id_to_idx
            )
            centroid_div = compute_diversity(embeddings, centroid_idx)

            # Strategy 2: kNN per seed
            # Use k_per_seed proportional to total_k / n_seeds, min 5
            k_per = max(5, TOP_K // n_seeds + 2)
            knn_idx, knn_scores, knn_sources = knn_per_seed(
                embeddings, seed_indices, k_per, TOP_K
            )
            knn_eval = evaluate_retrieval(
                knn_idx, held_out_indices, all_ids, id_to_idx
            )
            knn_div = compute_diversity(embeddings, knn_idx)

            # Strategy 3: MMR
            mmr_idx, mmr_scores = mmr_select(
                embeddings, seed_indices, TOP_K, lam=MMR_LAMBDA
            )
            mmr_eval = evaluate_retrieval(
                mmr_idx, held_out_indices, all_ids, id_to_idx
            )
            mmr_div = compute_diversity(embeddings, mmr_idx)

            # Overlap between strategies
            centroid_set = set(centroid_idx)
            knn_set = set(knn_idx)
            mmr_set = set(mmr_idx)

            overlap = {
                "centroid_vs_knn": round(len(centroid_set & knn_set) / len(centroid_set | knn_set), 4) if (centroid_set | knn_set) else 0,
                "centroid_vs_mmr": round(len(centroid_set & mmr_set) / len(centroid_set | mmr_set), 4) if (centroid_set | mmr_set) else 0,
                "knn_vs_mmr": round(len(knn_set & mmr_set) / len(knn_set | mmr_set), 4) if (knn_set | mmr_set) else 0,
            }

            # kNN source distribution (how many seeds nominated each result)
            avg_sources = round(np.mean(knn_sources), 2) if knn_sources else 0
            unique_papers = len(set(knn_idx))

            result = {
                "profile_id": pid,
                "profile_name": profile["name"],
                "seed_subset": subset_name,
                "n_seeds": n_seeds,
                "n_held_out": len(held_out_indices),
                "strategies": {
                    "centroid": {
                        "eval": centroid_eval,
                        "diversity": centroid_div,
                        "retrieved_ids": [all_ids[i] for i in centroid_idx],
                    },
                    "knn_per_seed": {
                        "k_per_seed": k_per,
                        "eval": knn_eval,
                        "diversity": knn_div,
                        "avg_seed_sources": avg_sources,
                        "unique_papers": unique_papers,
                        "retrieved_ids": [all_ids[i] for i in knn_idx],
                    },
                    "mmr": {
                        "lambda": MMR_LAMBDA,
                        "eval": mmr_eval,
                        "diversity": mmr_div,
                        "retrieved_ids": [all_ids[i] for i in mmr_idx],
                    },
                },
                "overlap": overlap,
            }

            all_results.append(result)

            print(f"    {subset_name} ({n_seeds} seeds):")
            print(f"      Centroid: MRR={centroid_eval['mrr']:.3f} R@20={centroid_eval['recall']:.3f} div={centroid_div:.3f}")
            print(f"      kNN/seed: MRR={knn_eval['mrr']:.3f} R@20={knn_eval['recall']:.3f} div={knn_div:.3f} (k={k_per}, avg_src={avg_sources})")
            print(f"      MMR:      MRR={mmr_eval['mrr']:.3f} R@20={mmr_eval['recall']:.3f} div={mmr_div:.3f}")
            print(f"      Overlap:  c/k={overlap['centroid_vs_knn']:.3f} c/m={overlap['centroid_vs_mmr']:.3f} k/m={overlap['knn_vs_mmr']:.3f}")

    return all_results


def compute_aggregate_stats(all_results):
    """Aggregate metrics across all profiles and subsets."""
    print("\n=== Aggregate Statistics ===")

    strategies = ["centroid", "knn_per_seed", "mmr"]
    metrics = ["mrr", "recall", "hit_at_5", "hit_at_10", "hit_at_20"]

    agg = {}
    for strat in strategies:
        agg[strat] = {}
        for metric in metrics:
            values = [
                r["strategies"][strat]["eval"][metric]
                for r in all_results
            ]
            agg[strat][metric] = {
                "mean": round(float(np.mean(values)), 4),
                "std": round(float(np.std(values)), 4),
                "min": round(float(np.min(values)), 4),
                "max": round(float(np.max(values)), 4),
            }

        # Diversity
        div_values = [r["strategies"][strat]["diversity"] for r in all_results]
        agg[strat]["diversity"] = {
            "mean": round(float(np.mean(div_values)), 4),
            "std": round(float(np.std(div_values)), 4),
        }

    print(f"\n  {'Strategy':<15} {'MRR':>8} {'R@20':>8} {'Hit@5':>8} {'Div':>8}")
    print(f"  {'-'*47}")
    for strat in strategies:
        mrr = agg[strat]["mrr"]["mean"]
        recall = agg[strat]["recall"]["mean"]
        hit5 = agg[strat]["hit_at_5"]["mean"]
        div_mean = agg[strat]["diversity"]["mean"]
        print(f"  {strat:<15} {mrr:>8.4f} {recall:>8.4f} {hit5:>8.4f} {div_mean:>8.4f}")

    # Overlap stats
    overlap_stats = {}
    for pair in ["centroid_vs_knn", "centroid_vs_mmr", "knn_vs_mmr"]:
        values = [r["overlap"][pair] for r in all_results]
        overlap_stats[pair] = {
            "mean": round(float(np.mean(values)), 4),
            "std": round(float(np.std(values)), 4),
        }

    print(f"\n  Mean overlap:")
    for pair, stats in overlap_stats.items():
        print(f"    {pair}: {stats['mean']:.4f} +/- {stats['std']:.4f}")

    return agg, overlap_stats


def main():
    print("=" * 60)
    print("SPIKE 003 / W5b: Strategy Pattern Experiments")
    print("  kNN per seed vs Centroid vs MMR")
    print("=" * 60)

    all_ids, id_to_idx, embeddings, profiles = load_data()
    all_results = run_comparison(all_ids, id_to_idx, embeddings, profiles)
    agg, overlap_stats = compute_aggregate_stats(all_results)

    output = {
        "experiment": "w5b_knn_mmr_patterns",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "embedding_model": "MiniLM (all-MiniLM-L6-v2)",
        "embedding_dim": 384,
        "corpus_size": len(all_ids),
        "top_k": TOP_K,
        "k_per_seed_base": K_PER_SEED,
        "mmr_lambda": MMR_LAMBDA,
        "n_profiles": len(profiles["profiles"]),
        "n_configs": len(all_results),
        "aggregate": agg,
        "overlap_stats": overlap_stats,
        "per_config_results": all_results,
    }

    with open(str(OUTPUT_FILE), 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
