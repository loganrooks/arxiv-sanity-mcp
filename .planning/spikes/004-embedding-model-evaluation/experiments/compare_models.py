#!/usr/bin/env python3
"""
Spike 004 Phase 2: Quantitative model comparison.

For each model vs MiniLM (and vs TF-IDF per PROTOCOL.md Section 4):
  1. Kendall's tau (full ranking correlation)
  2. Jaccard @K=20, 50, 100 per profile
  3. Score distribution analysis (spread, separation)
  4. LOO-MRR (reference only — MiniLM-entangled, document caveat)
  5. Category-based recall (model-independent ground truth)
  6. Semantic clustering of divergent papers
  7. Per-profile Jaccard summary

Outputs branch classification per model + full metrics JSON.

Usage:
  conda activate ml-dev
  python compare_models.py
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import stats

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
SPIKE_003_DIR = SPIKE_004_DIR.parent / "003-strategy-profiling"
SPIKE_001_DIR = SPIKE_004_DIR.parent / "001-volume-filtering-scoring-landscape"

DATA_DIR = SPIKE_004_DIR / "experiments" / "data"
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"
PROFILES_PATH = SPIKE_003_DIR / "experiments" / "data" / "interest_profiles.json"
HARVEST_DB = SPIKE_001_DIR / "experiments" / "data" / "spike_001_harvest.db"

MODELS = ["minilm", "specter2", "stella", "qwen3", "gte", "voyage"]
K_VALUES = [20, 50, 100]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_profiles() -> dict:
    with open(PROFILES_PATH) as f:
        return json.load(f)["profiles"]


def load_embeddings(model_key: str) -> tuple[np.ndarray, list[str]] | None:
    emb_path = DATA_DIR / f"{model_key}_2000.npy"
    ids_path = DATA_DIR / f"{model_key}_2000_ids.json"
    if not emb_path.exists():
        return None
    return np.load(str(emb_path)), json.load(open(ids_path))


def load_paper_categories() -> dict[str, list[str]]:
    """Load primary_category for each paper from harvest DB."""
    conn = sqlite3.connect(str(HARVEST_DB))
    rows = conn.execute("SELECT arxiv_id, primary_category FROM papers").fetchall()
    conn.close()
    return {r[0]: [r[1]] if r[1] else [] for r in rows}


def centroid_scores(emb: np.ndarray, ids: list[str], seed_ids: list[str]) -> np.ndarray:
    id_to_idx = {pid: i for i, pid in enumerate(ids)}
    seed_idx = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
    if not seed_idx:
        return np.zeros(len(ids))
    centroid = emb[seed_idx].mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm < 1e-10:
        return np.zeros(len(ids))
    centroid /= norm
    return emb @ centroid


def top_k_set(scores: np.ndarray, ids: list[str], k: int) -> set[str]:
    top_idx = np.argsort(scores)[-k:][::-1]
    return {ids[i] for i in top_idx}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------------------
# TF-IDF setup
# ---------------------------------------------------------------------------

def build_tfidf(paper_ids: list[str]) -> tuple[object, np.ndarray]:
    """Build TF-IDF matrix for 2000-paper sample."""
    from sklearn.feature_extraction.text import TfidfVectorizer

    conn = sqlite3.connect(str(HARVEST_DB))
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in paper_ids)
    rows = conn.execute(
        f"SELECT arxiv_id, abstract FROM papers WHERE arxiv_id IN ({placeholders})",
        paper_ids,
    ).fetchall()
    conn.close()

    id_to_abstract = {r["arxiv_id"]: r["abstract"] or "" for r in rows}
    abstracts = [id_to_abstract.get(pid, "") for pid in paper_ids]

    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    return vectorizer, tfidf_matrix


def tfidf_scores(tfidf_matrix, paper_ids: list[str], seed_ids: list[str]) -> np.ndarray:
    id_to_idx = {pid: i for i, pid in enumerate(paper_ids)}
    seed_idx = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
    if not seed_idx:
        return np.zeros(len(paper_ids))

    centroid = np.asarray(tfidf_matrix[seed_idx].mean(axis=0)).flatten()
    norm = np.linalg.norm(centroid)
    if norm < 1e-10:
        return np.zeros(len(paper_ids))
    centroid /= norm
    return np.asarray(tfidf_matrix.dot(centroid)).flatten()


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_rank_correlation(scores_a: np.ndarray, scores_b: np.ndarray) -> dict:
    """Kendall's tau between two full score arrays."""
    tau, p_value = stats.kendalltau(scores_a, scores_b)
    return {"kendall_tau": round(float(tau), 4), "p_value": float(p_value)}


def compute_jaccard_at_k(
    scores_a: np.ndarray, ids_a: list[str],
    scores_b: np.ndarray, ids_b: list[str],
    k_values: list[int],
) -> dict:
    """Jaccard overlap at multiple K values."""
    result = {}
    for k in k_values:
        top_a = top_k_set(scores_a, ids_a, k)
        top_b = top_k_set(scores_b, ids_b, k)
        result[f"jaccard_at_{k}"] = round(jaccard(top_a, top_b), 4)
    return result


def compute_score_distribution(scores: np.ndarray) -> dict:
    """Analyze score distribution properties."""
    top_20_idx = np.argsort(scores)[-20:][::-1]
    top_20 = scores[top_20_idx]
    rest = np.delete(scores, top_20_idx)

    return {
        "mean": round(float(np.mean(scores)), 6),
        "std": round(float(np.std(scores)), 6),
        "top20_mean": round(float(np.mean(top_20)), 6),
        "top20_std": round(float(np.std(top_20)), 6),
        "rest_mean": round(float(np.mean(rest)), 6),
        "separation": round(float(np.mean(top_20) - np.mean(rest)), 6),
        "max": round(float(np.max(scores)), 6),
        "min": round(float(np.min(scores)), 6),
    }


def compute_category_recall(
    scores: np.ndarray,
    paper_ids: list[str],
    seed_ids: list[str],
    categories: dict[str, list[str]],
    k: int = 20,
) -> dict:
    """Model-independent: how many top-K papers share categories with seeds."""
    seed_cats = set()
    for sid in seed_ids:
        seed_cats.update(categories.get(sid, []))

    if not seed_cats:
        return {"recall": 0.0, "n_seed_categories": 0}

    top_k_ids = top_k_set(scores, paper_ids, k)
    matches = sum(
        1 for pid in top_k_ids
        if any(c in seed_cats for c in categories.get(pid, []))
    )
    return {
        "recall": round(matches / k, 4),
        "matches": matches,
        "k": k,
        "n_seed_categories": len(seed_cats),
    }


def compute_divergent_paper_analysis(
    scores_model: np.ndarray, ids_model: list[str],
    scores_baseline: np.ndarray, ids_baseline: list[str],
    categories: dict[str, list[str]],
    k: int = 20,
) -> dict:
    """Analyze papers in model's top-K but not baseline's."""
    model_top = top_k_set(scores_model, ids_model, k)
    baseline_top = top_k_set(scores_baseline, ids_baseline, k)

    model_unique = model_top - baseline_top
    baseline_unique = baseline_top - model_top

    # Category distribution of divergent papers
    model_cats = Counter()
    for pid in model_unique:
        for cat in categories.get(pid, ["unknown"]):
            model_cats[cat] += 1

    baseline_cats = Counter()
    for pid in baseline_unique:
        for cat in categories.get(pid, ["unknown"]):
            baseline_cats[cat] += 1

    return {
        "n_model_unique": len(model_unique),
        "n_baseline_unique": len(baseline_unique),
        "n_shared": len(model_top & baseline_top),
        "model_unique_categories": dict(model_cats.most_common(10)),
        "baseline_unique_categories": dict(baseline_cats.most_common(10)),
        "model_unique_ids": sorted(model_unique),
        "baseline_unique_ids": sorted(baseline_unique),
    }


def compute_loo_mrr(
    emb: np.ndarray,
    paper_ids: list[str],
    held_out_papers: list[dict],
    seed_papers: list[dict],
    k: int = 20,
) -> dict:
    """Leave-one-out MRR. CAVEAT: MiniLM-entangled via cluster membership."""
    id_to_idx = {pid: i for i, pid in enumerate(paper_ids)}
    seed_ids = [s["arxiv_id"] for s in seed_papers]

    reciprocal_ranks = []
    for ho in held_out_papers:
        ho_id = ho["arxiv_id"]
        if ho_id not in id_to_idx:
            continue

        # Use all seeds (held-out is not in seed set)
        scores = centroid_scores(emb, paper_ids, seed_ids)
        top_k_idx = np.argsort(scores)[-k:][::-1]
        top_k_list = [paper_ids[i] for i in top_k_idx]

        if ho_id in top_k_list:
            rank = top_k_list.index(ho_id) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)

    mrr = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0
    return {
        "mrr": round(mrr, 4),
        "n_evaluated": len(reciprocal_ranks),
        "caveat": "MiniLM-entangled: clusters defined by MiniLM. Use as reference, not decision criterion.",
    }


# ---------------------------------------------------------------------------
# Branch classification
# ---------------------------------------------------------------------------

def classify_model(profile_jaccards: dict[str, float], extra_signals: dict) -> dict:
    """Classify model per PROTOCOL.md Section 2.

    Classification based on most divergent profile Jaccard, upgradable by other signals.
    """
    j_values = list(profile_jaccards.values())
    min_j = min(j_values)
    mean_j = np.mean(j_values)

    # Base classification from Jaccard
    if min_j < 0.8:
        base_class = "divergent"
    elif max(j_values) <= 0.95 and min_j >= 0.8:
        if all(j > 0.9 for j in j_values):
            base_class = "high_overlap"
        else:
            base_class = "mid_overlap"
    else:
        if all(j > 0.95 for j in j_values):
            base_class = "near_identical"
        else:
            base_class = "high_overlap"

    # Check for upgrade signals (can only upgrade, never downgrade)
    upgraded = False
    upgrade_reasons = []

    # Check if category recall diverges significantly
    cat_recall_diffs = extra_signals.get("category_recall_diffs", {})
    if any(abs(d) > 0.1 for d in cat_recall_diffs.values()):
        upgrade_reasons.append("category_recall_diverges_>10pp")

    # Check score distribution differences
    sep_diffs = extra_signals.get("separation_diffs", {})
    if any(abs(d) > 0.05 for d in sep_diffs.values()):
        upgrade_reasons.append("score_separation_differs_notably")

    if upgrade_reasons and base_class in ("high_overlap", "near_identical"):
        upgraded = True
        if base_class == "near_identical":
            base_class = "high_overlap"
        elif base_class == "high_overlap":
            base_class = "mid_overlap"

    return {
        "classification": base_class,
        "min_jaccard_20": round(float(min_j), 4),
        "mean_jaccard_20": round(float(mean_j), 4),
        "upgraded": upgraded,
        "upgrade_reasons": upgrade_reasons,
        "per_profile_jaccard_20": {k: round(v, 4) for k, v in profile_jaccards.items()},
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("SPIKE 004 PHASE 2: QUANTITATIVE COMPARISON")
    print("=" * 60)

    # Check prerequisites
    val_checkpoint = CHECKPOINT_DIR / "phase1_validation.json"
    if not val_checkpoint.exists():
        print("ERROR: Phase 1 validation checkpoint not found.")
        print("Run validate_sample.py first.")
        sys.exit(1)

    with open(val_checkpoint) as f:
        validation = json.load(f)
    if validation["verdict"] == "NO_GO":
        print("ERROR: Sample validation returned NO_GO. Cannot proceed.")
        sys.exit(1)

    # Load data
    profiles = load_profiles()
    categories = load_paper_categories()

    # Load MiniLM as baseline
    minilm_data = load_embeddings("minilm")
    if minilm_data is None:
        print("ERROR: MiniLM embeddings not found.")
        sys.exit(1)
    minilm_emb, minilm_ids = minilm_data

    # Build TF-IDF on sample
    print("\n--- Building TF-IDF on 2000-paper sample ---")
    t0 = time.perf_counter()
    _, tfidf_matrix = build_tfidf(minilm_ids)  # Use MiniLM IDs as canonical order
    print(f"  TF-IDF matrix: {tfidf_matrix.shape} in {time.perf_counter()-t0:.1f}s")

    # Compare each model
    all_metrics = {}
    all_classifications = {}

    for model_key in MODELS:
        if model_key == "minilm":
            continue

        print(f"\n{'='*50}")
        print(f"COMPARING: {model_key} vs MiniLM (+ TF-IDF)")
        print(f"{'='*50}")

        data = load_embeddings(model_key)
        if data is None:
            print(f"  SKIP: {model_key} embeddings not found")
            continue

        model_emb, model_ids = data

        profile_metrics = {}
        profile_jaccards = {}
        cat_recall_diffs = {}
        separation_diffs = {}

        for pid, profile in profiles.items():
            seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]
            print(f"\n  Profile {pid}: {profile.get('name', pid)}")

            # Compute scores
            model_scores = centroid_scores(model_emb, model_ids, seed_ids)
            minilm_scores = centroid_scores(minilm_emb, minilm_ids, seed_ids)
            tfidf_sc = tfidf_scores(tfidf_matrix, minilm_ids, seed_ids)

            # 1. Rank correlation vs MiniLM
            rank_corr = compute_rank_correlation(model_scores, minilm_scores)

            # 2. Jaccard vs MiniLM and vs TF-IDF
            jaccard_vs_minilm = compute_jaccard_at_k(
                model_scores, model_ids, minilm_scores, minilm_ids, K_VALUES,
            )
            jaccard_vs_tfidf = compute_jaccard_at_k(
                model_scores, model_ids, tfidf_sc, minilm_ids, K_VALUES,
            )

            profile_jaccards[pid] = jaccard_vs_minilm["jaccard_at_20"]

            # 3. Score distributions
            model_dist = compute_score_distribution(model_scores)
            minilm_dist = compute_score_distribution(minilm_scores)
            separation_diffs[pid] = model_dist["separation"] - minilm_dist["separation"]

            # 4. Category recall (model-independent)
            model_cat_recall = compute_category_recall(
                model_scores, model_ids, seed_ids, categories,
            )
            minilm_cat_recall = compute_category_recall(
                minilm_scores, minilm_ids, seed_ids, categories,
            )
            cat_recall_diffs[pid] = model_cat_recall["recall"] - minilm_cat_recall["recall"]

            # 5. LOO-MRR (reference only)
            loo_mrr = compute_loo_mrr(
                model_emb, model_ids,
                profile.get("held_out_papers", []),
                profile["seed_papers"],
            )

            # 6. Divergent paper analysis vs MiniLM
            divergent_vs_minilm = compute_divergent_paper_analysis(
                model_scores, model_ids,
                minilm_scores, minilm_ids,
                categories,
            )

            # 7. Divergent paper analysis vs TF-IDF
            divergent_vs_tfidf = compute_divergent_paper_analysis(
                model_scores, model_ids,
                tfidf_sc, minilm_ids,
                categories,
            )

            # Papers unique to this model (not in MiniLM OR TF-IDF top-20)
            model_top20 = top_k_set(model_scores, model_ids, 20)
            minilm_top20 = top_k_set(minilm_scores, minilm_ids, 20)
            tfidf_top20 = top_k_set(tfidf_sc, minilm_ids, 20)
            truly_unique = model_top20 - minilm_top20 - tfidf_top20

            profile_metrics[pid] = {
                "rank_correlation_vs_minilm": rank_corr,
                "jaccard_vs_minilm": jaccard_vs_minilm,
                "jaccard_vs_tfidf": jaccard_vs_tfidf,
                "score_distribution": model_dist,
                "minilm_score_distribution": minilm_dist,
                "category_recall": model_cat_recall,
                "minilm_category_recall": minilm_cat_recall,
                "loo_mrr": loo_mrr,
                "divergent_vs_minilm": divergent_vs_minilm,
                "divergent_vs_tfidf": divergent_vs_tfidf,
                "n_truly_unique": len(truly_unique),
                "truly_unique_ids": sorted(truly_unique),
            }

            j = jaccard_vs_minilm["jaccard_at_20"]
            tau = rank_corr["kendall_tau"]
            print(f"    J@20={j:.3f}  tau={tau:.3f}  cat_recall={model_cat_recall['recall']:.3f}  unique={len(truly_unique)}")

        # Classification
        classification = classify_model(
            profile_jaccards,
            {
                "category_recall_diffs": cat_recall_diffs,
                "separation_diffs": separation_diffs,
            },
        )
        print(f"\n  CLASSIFICATION: {classification['classification']}")
        if classification["upgraded"]:
            print(f"  (upgraded due to: {', '.join(classification['upgrade_reasons'])})")

        all_metrics[model_key] = profile_metrics
        all_classifications[model_key] = classification

    # Save results
    metrics_checkpoint = {
        "phase": "phase2_metrics",
        "models_compared": list(all_metrics.keys()),
        "profiles": list(profiles.keys()),
        "k_values": K_VALUES,
        "metrics": all_metrics,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(CHECKPOINT_DIR / "phase2_metrics.json", "w") as f:
        json.dump(metrics_checkpoint, f, indent=2, cls=NumpyEncoder)

    classification_checkpoint = {
        "phase": "phase2_classification",
        "classifications": all_classifications,
        "review_coverage_table": {
            "divergent": "All 8 profiles, full W1 template, 2 blind comparisons",
            "mid_overlap": "5 profiles (3 divergent + 1 median + 1 high), full W1, 1 blind",
            "high_overlap": "3 profiles (2 divergent + 1 random), abbreviated review",
            "near_identical": "2 profiles (most divergent + 1 random), abbreviated review",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(CHECKPOINT_DIR / "phase2_classification.json", "w") as f:
        json.dump(classification_checkpoint, f, indent=2, cls=NumpyEncoder)

    # Summary
    print("\n" + "=" * 60)
    print("PHASE 2 SUMMARY")
    print("=" * 60)
    for model_key, cls in all_classifications.items():
        print(f"  {model_key}: {cls['classification']} "
              f"(min J@20={cls['min_jaccard_20']:.3f}, mean={cls['mean_jaccard_20']:.3f})")

    print(f"\nCheckpoints saved to {CHECKPOINT_DIR}/")
    print("Next: Phase 3 — qualitative review based on classifications above")


if __name__ == "__main__":
    main()
