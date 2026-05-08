#!/usr/bin/env python3
"""
Spike 006 quantitative pass.

This script loads the carried profile families from Spike 005 and evaluates
centroid vs kNN-per-seed retrieval for each challenger model on the same 2000-paper
sample used in Spikes 004-005.

Outputs:
  - checkpoints/phase1_quantitative.json
  - review_inputs/phase1_interaction_cases.json

The script is intentionally quantitative only. It narrows the review surface for
the mandatory qualitative pass rather than trying to settle 006 in one shot.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


SPIKE_006_DIR = Path(__file__).resolve().parent.parent
SPIKE_004_EXPERIMENTS = SPIKE_006_DIR.parent / "004-embedding-model-evaluation" / "experiments"
if str(SPIKE_004_EXPERIMENTS) not in sys.path:
    sys.path.insert(0, str(SPIKE_004_EXPERIMENTS))

import compare_models as base  # noqa: E402


EXPERIMENTS_DIR = SPIKE_006_DIR / "experiments"
CHECKPOINT_DIR = EXPERIMENTS_DIR / "checkpoints"
REVIEW_INPUT_DIR = EXPERIMENTS_DIR / "review_inputs"
SPIKE_005_CHECKPOINT = (
    SPIKE_006_DIR.parent
    / "005-evaluation-framework-robustness"
    / "experiments"
    / "checkpoints"
    / "phase1_quantitative.json"
)

MODELS = ["specter2", "stella", "qwen3", "gte", "voyage"]
FAMILY_IDS = ["minilm_saved", "category_lexical"]
METHODS = ["centroid", "knn_per_seed"]
K = 20


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def top_k_ranked_list(scores: np.ndarray, ids: list[str], k: int) -> list[str]:
    top_idx = np.argsort(scores)[-k:][::-1]
    return [ids[i] for i in top_idx]


def load_carried_families() -> dict[str, dict]:
    checkpoint = json.loads(SPIKE_005_CHECKPOINT.read_text())
    return {
        family_id: checkpoint["family_results"][family_id]["profiles"]
        for family_id in FAMILY_IDS
    }


def centroid_scores_without_seeds(embeddings: np.ndarray, ids: list[str], seed_ids: list[str]) -> np.ndarray:
    scores = base.centroid_scores(embeddings, ids, seed_ids)
    id_to_idx = {pid: idx for idx, pid in enumerate(ids)}
    for seed_id in seed_ids:
        idx = id_to_idx.get(seed_id)
        if idx is not None:
            scores[idx] = -np.inf
    return scores


def knn_per_seed_scores(
    embeddings: np.ndarray,
    ids: list[str],
    seed_ids: list[str],
    total_k: int,
) -> tuple[np.ndarray, list[int], list[float], list[int]]:
    id_to_idx = {pid: idx for idx, pid in enumerate(ids)}
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        scores = np.full(len(ids), -np.inf)
        return scores, [], [], []

    k_per_seed = max(5, math.ceil(total_k / len(seed_indices)) + 2)
    seed_set = set(seed_indices)

    best_scores = np.full(len(ids), -np.inf)
    mean_scores = np.zeros(len(ids), dtype=float)
    score_counts = np.zeros(len(ids), dtype=int)
    nomination_counts = np.zeros(len(ids), dtype=int)

    for seed_idx in seed_indices:
        scores = embeddings @ embeddings[seed_idx]
        for excluded in seed_set:
            scores[excluded] = -np.inf
        top_indices = np.argsort(scores)[::-1][:k_per_seed]
        for idx in top_indices:
            idx_int = int(idx)
            score = float(scores[idx_int])
            if score > best_scores[idx_int]:
                best_scores[idx_int] = score
            mean_scores[idx_int] += score
            score_counts[idx_int] += 1
            nomination_counts[idx_int] += 1

    nominated = [idx for idx in np.where(nomination_counts > 0)[0] if idx not in seed_set]
    for idx in nominated:
        mean_scores[idx] = mean_scores[idx] / max(1, score_counts[idx])

    nominated.sort(
        key=lambda idx: (
            best_scores[idx],
            mean_scores[idx],
            nomination_counts[idx],
            -idx,
        ),
        reverse=True,
    )
    top_indices = nominated[:total_k]

    output_scores = np.full(len(ids), -np.inf)
    for rank, idx in enumerate(top_indices):
        output_scores[idx] = best_scores[idx] + (mean_scores[idx] * 1e-6) + (nomination_counts[idx] * 1e-9)

    top_scores = [float(best_scores[idx]) for idx in top_indices]
    top_nominations = [int(nomination_counts[idx]) for idx in top_indices]
    return output_scores, top_indices, top_scores, top_nominations


def method_metrics(
    *,
    method: str,
    model_emb: np.ndarray,
    model_ids: list[str],
    minilm_emb: np.ndarray,
    minilm_ids: list[str],
    tfidf_matrix,
    seed_ids: list[str],
    categories: dict[str, list[str]],
) -> dict:
    minilm_centroid_scores = centroid_scores_without_seeds(minilm_emb, minilm_ids, seed_ids)
    tfidf_scores = base.tfidf_scores(tfidf_matrix, minilm_ids, seed_ids)
    minilm_centroid_top20 = set(top_k_ranked_list(minilm_centroid_scores, minilm_ids, K))
    tfidf_top20 = set(top_k_ranked_list(tfidf_scores, minilm_ids, K))

    if method == "centroid":
        model_scores = centroid_scores_without_seeds(model_emb, model_ids, seed_ids)
        top_indices = None
        top_scores = None
        nomination_counts = None
    else:
        model_scores, top_indices, top_scores, nomination_counts = knn_per_seed_scores(
            model_emb, model_ids, seed_ids, K,
        )

    model_top20_ranked = top_k_ranked_list(model_scores, model_ids, K)
    model_top20 = set(model_top20_ranked)

    model_cat_recall = base.compute_category_recall(model_scores, model_ids, seed_ids, categories)
    minilm_cat_recall = base.compute_category_recall(minilm_centroid_scores, minilm_ids, seed_ids, categories)

    return {
        "jaccard_vs_minilm_centroid_at_20": round(base.jaccard(model_top20, minilm_centroid_top20), 4),
        "jaccard_vs_tfidf_centroid_at_20": round(base.jaccard(model_top20, tfidf_top20), 4),
        "union_size_minilm_model_at_20": len(model_top20 | minilm_centroid_top20),
        "union_size_minilm_tfidf_at_20": len(minilm_centroid_top20 | tfidf_top20),
        "union_delta_vs_tfidf_at_20": len(model_top20 | minilm_centroid_top20) - len(minilm_centroid_top20 | tfidf_top20),
        "category_recall": model_cat_recall,
        "minilm_category_recall": minilm_cat_recall,
        "top20_model_ranked_ids": model_top20_ranked,
        "n_truly_unique_vs_both": len(model_top20 - minilm_centroid_top20 - tfidf_top20),
        "truly_unique_vs_both_ids": sorted(model_top20 - minilm_centroid_top20 - tfidf_top20),
        "top_indices": top_indices,
        "top_scores": top_scores,
        "nomination_counts": nomination_counts,
    }


def summarize_interaction(centroid_profiles: dict[str, dict], knn_profiles: dict[str, dict]) -> dict:
    method_jaccards = []
    centroid_union = []
    knn_union = []
    centroid_cat = []
    knn_cat = []
    profiles_knn_better = 0
    profiles_centroid_better = 0

    for profile_id in sorted(centroid_profiles):
        centroid = centroid_profiles[profile_id]
        knn = knn_profiles[profile_id]
        centroid_top = set(centroid["top20_model_ranked_ids"])
        knn_top = set(knn["top20_model_ranked_ids"])
        method_jaccards.append(base.jaccard(centroid_top, knn_top))
        centroid_union.append(centroid["union_delta_vs_tfidf_at_20"])
        knn_union.append(knn["union_delta_vs_tfidf_at_20"])
        centroid_cat.append(centroid["category_recall"]["recall"])
        knn_cat.append(knn["category_recall"]["recall"])
        if knn["union_delta_vs_tfidf_at_20"] > centroid["union_delta_vs_tfidf_at_20"]:
            profiles_knn_better += 1
        elif knn["union_delta_vs_tfidf_at_20"] < centroid["union_delta_vs_tfidf_at_20"]:
            profiles_centroid_better += 1

    mean_centroid_union = float(np.mean(centroid_union))
    mean_knn_union = float(np.mean(knn_union))
    mean_method_jaccard = float(np.mean(method_jaccards))
    mean_centroid_cat = float(np.mean(centroid_cat))
    mean_knn_cat = float(np.mean(knn_cat))

    if mean_method_jaccard >= 0.6 and abs(mean_knn_union - mean_centroid_union) <= 0.5:
        provisional = "retrieval-stable"
        reasons = ["methods_overlap_strongly_and_benchmark_gap_is_small"]
    elif mean_knn_union >= mean_centroid_union + 1.0 and mean_knn_cat >= mean_centroid_cat - 0.05:
        provisional = "knn-candidate-niche"
        reasons = ["knn_improves_union_without_large_category_recall_loss"]
    elif mean_knn_union <= mean_centroid_union - 1.0 and mean_knn_cat < mean_centroid_cat - 0.05:
        provisional = "knn-weakened"
        reasons = ["knn_reduces_union_and_category_recall"]
    else:
        provisional = "method-sensitive"
        reasons = ["retrieval_choice_changes_story_without_clean_winner"]

    return {
        "mean_centroid_union_delta_vs_tfidf_at_20": round(mean_centroid_union, 4),
        "mean_knn_union_delta_vs_tfidf_at_20": round(mean_knn_union, 4),
        "mean_centroid_category_recall": round(mean_centroid_cat, 4),
        "mean_knn_category_recall": round(mean_knn_cat, 4),
        "mean_jaccard_centroid_vs_knn_at_20": round(mean_method_jaccard, 4),
        "profiles_knn_better_on_union_at_20": profiles_knn_better,
        "profiles_centroid_better_on_union_at_20": profiles_centroid_better,
        "provisional_interaction_read": provisional,
        "provisional_reasons": reasons,
    }


def build_review_cases(results: dict[str, dict]) -> list[dict]:
    cases = []
    for family_id in FAMILY_IDS:
        for model_key in MODELS:
            centroid_profiles = results[family_id]["per_method_metrics"][model_key]["centroid"]
            knn_profiles = results[family_id]["per_method_metrics"][model_key]["knn_per_seed"]
            summary = results[family_id]["interaction_summaries"][model_key]
            if summary["provisional_interaction_read"] == "retrieval-stable":
                continue

            deltas = []
            for profile_id in sorted(centroid_profiles):
                centroid = centroid_profiles[profile_id]
                knn = knn_profiles[profile_id]
                deltas.append(
                    {
                        "profile_id": profile_id,
                        "method_jaccard_at_20": round(
                            base.jaccard(
                                set(centroid["top20_model_ranked_ids"]),
                                set(knn["top20_model_ranked_ids"]),
                            ),
                            4,
                        ),
                        "centroid_union_delta_vs_tfidf": centroid["union_delta_vs_tfidf_at_20"],
                        "knn_union_delta_vs_tfidf": knn["union_delta_vs_tfidf_at_20"],
                        "centroid_category_recall": centroid["category_recall"]["recall"],
                        "knn_category_recall": knn["category_recall"]["recall"],
                        "centroid_top20_ranked_ids": centroid["top20_model_ranked_ids"],
                        "knn_top20_ranked_ids": knn["top20_model_ranked_ids"],
                        "knn_nomination_counts": knn["nomination_counts"],
                    }
                )
            deltas.sort(
                key=lambda item: (
                    abs(item["knn_union_delta_vs_tfidf"] - item["centroid_union_delta_vs_tfidf"]),
                    1.0 - item["method_jaccard_at_20"],
                    abs(item["knn_category_recall"] - item["centroid_category_recall"]),
                ),
                reverse=True,
            )
            cases.append(
                {
                    "family_id": family_id,
                    "model_key": model_key,
                    "provisional_interaction_read": summary["provisional_interaction_read"],
                    "provisional_reasons": summary["provisional_reasons"],
                    "review_profiles": deltas[:3],
                }
            )
    return cases


def main() -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_INPUT_DIR.mkdir(parents=True, exist_ok=True)

    carried_families = load_carried_families()
    categories = base.load_paper_categories()
    minilm_emb, minilm_ids = base.load_embeddings("minilm")
    _, tfidf_matrix = base.build_tfidf(minilm_ids)

    embeddings = {}
    for model_key in MODELS:
        data = base.load_embeddings(model_key)
        if data is None:
            raise RuntimeError(f"Embeddings missing for {model_key}")
        embeddings[model_key] = data

    results = {}
    for family_id in FAMILY_IDS:
        family_profiles = carried_families[family_id]
        per_method_metrics = {model_key: {method: {} for method in METHODS} for model_key in MODELS}
        interaction_summaries = {}

        for model_key, (model_emb, model_ids) in embeddings.items():
            for profile_id, family_profile in family_profiles.items():
                seed_ids = [paper["arxiv_id"] for paper in family_profile["seed_papers"][:5]]
                per_method_metrics[model_key]["centroid"][profile_id] = method_metrics(
                    method="centroid",
                    model_emb=model_emb,
                    model_ids=model_ids,
                    minilm_emb=minilm_emb,
                    minilm_ids=minilm_ids,
                    tfidf_matrix=tfidf_matrix,
                    seed_ids=seed_ids,
                    categories=categories,
                )
                per_method_metrics[model_key]["knn_per_seed"][profile_id] = method_metrics(
                    method="knn_per_seed",
                    model_emb=model_emb,
                    model_ids=model_ids,
                    minilm_emb=minilm_emb,
                    minilm_ids=minilm_ids,
                    tfidf_matrix=tfidf_matrix,
                    seed_ids=seed_ids,
                    categories=categories,
                )

            interaction_summaries[model_key] = summarize_interaction(
                per_method_metrics[model_key]["centroid"],
                per_method_metrics[model_key]["knn_per_seed"],
            )

        results[family_id] = {
            "profiles": family_profiles,
            "per_method_metrics": per_method_metrics,
            "interaction_summaries": interaction_summaries,
        }

    review_cases = build_review_cases(results)
    checkpoint = {
        "phase": "phase1_quantitative_model_retrieval_interactions",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_profile_families": str(SPIKE_005_CHECKPOINT),
        "family_ids": FAMILY_IDS,
        "models": MODELS,
        "methods": METHODS,
        "k": K,
        "results": results,
        "review_cases": review_cases,
    }

    checkpoint_path = CHECKPOINT_DIR / "phase1_quantitative.json"
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2, cls=NumpyEncoder) + "\n")

    review_path = REVIEW_INPUT_DIR / "phase1_interaction_cases.json"
    review_path.write_text(
        json.dumps(
            {
                "generated_at": checkpoint["timestamp"],
                "source_checkpoint": str(checkpoint_path),
                "cases": review_cases,
            },
            indent=2,
            cls=NumpyEncoder,
        ) + "\n"
    )

    print("Spike 006 quantitative checkpoint written:")
    print(f"  {checkpoint_path}")
    print("Review input written:")
    print(f"  {review_path}")
    print()
    print("Per-family interaction summaries:")
    for family_id in FAMILY_IDS:
        print(f"  {family_id}:")
        for model_key in MODELS:
            summary = results[family_id]["interaction_summaries"][model_key]
            print(
                f"    {model_key}: {summary['provisional_interaction_read']} "
                f"(centroid={summary['mean_centroid_union_delta_vs_tfidf_at_20']:.3f}, "
                f"knn={summary['mean_knn_union_delta_vs_tfidf_at_20']:.3f}, "
                f"J={summary['mean_jaccard_centroid_vs_knn_at_20']:.3f})"
            )
    print()
    print(f"Review cases requiring qualitative pass: {len(review_cases)}")


if __name__ == "__main__":
    main()
