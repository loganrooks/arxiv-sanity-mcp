#!/usr/bin/env python3
"""
Pre-spike analyses for the next spike round.

Produces three grounded artifacts from existing Spike 004 assets:
1. Full pairwise model-to-model tau matrix
2. Seed sensitivity characterization across available grounded seed variants
3. MiniLM+challenger vs MiniLM+TF-IDF complementarity comparison

Usage:
  python .planning/spikes/004-embedding-model-evaluation/experiments/pre_spike_analyses.py
"""

from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import compare_models as base


SPIKE_004_DIR = Path(__file__).resolve().parent.parent
SPIKE_005_DIR = SPIKE_004_DIR.parent / "005-next-round-suite"
ARTIFACT_DIR = SPIKE_005_DIR / "artifacts"
SAMPLE_PATH = base.SPIKE_003_DIR / "experiments" / "data" / "sample_2000.json"

MODELS = ["minilm", "specter2", "stella", "qwen3", "gte", "voyage"]
PAIRWISE_MODELS = MODELS + ["tfidf"]
K_VALUES = [20, 50, 100]
K5_VARIANT_NAMES = [
    "seed_papers_first5",
    "subset_5",
    "subset_10_first5",
    "subset_15_first5",
]
COUNT_VARIANT_NAMES = [
    "subset_5",
    "subset_10",
    "subset_15",
]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def load_sample_metadata() -> dict[str, dict]:
    data = json.loads(SAMPLE_PATH.read_text())
    papers = data.get("papers", data)
    return {paper["arxiv_id"]: paper for paper in papers}


def load_profiles() -> dict:
    return base.load_profiles()


def load_all_embeddings() -> dict[str, tuple[np.ndarray, list[str]]]:
    loaded = {}
    for model_key in MODELS:
        data = base.load_embeddings(model_key)
        if data is None:
            raise FileNotFoundError(f"Embeddings missing for {model_key}")
        loaded[model_key] = data
    return loaded


def build_tfidf(paper_ids: list[str]):
    _, tfidf_matrix = base.build_tfidf(paper_ids)
    return tfidf_matrix


def get_seed_variants(profile: dict) -> dict[str, list[str]]:
    subsets = profile.get("seed_subsets", {})
    subset_10 = subsets.get("subset_10", [])
    subset_15 = subsets.get("subset_15", [])

    variants = {
        "seed_papers_first5": [s["arxiv_id"] for s in profile["seed_papers"][:5]],
        "subset_5": list(subsets.get("subset_5", [])),
        "subset_10_first5": list(subset_10[:5]),
        "subset_15_first5": list(subset_15[:5]),
        "subset_10": list(subset_10),
        "subset_15": list(subset_15),
    }
    return {name: ids for name, ids in variants.items() if ids}


def pairwise_tau_for_profile(
    embeddings: dict[str, tuple[np.ndarray, list[str]]],
    tfidf_matrix,
    seed_ids: list[str],
) -> dict[str, dict[str, float]]:
    scores = {}
    for model_key, (emb, ids) in embeddings.items():
        scores[model_key] = base.centroid_scores(emb, ids, seed_ids)
    _, canonical_ids = embeddings["minilm"]
    scores["tfidf"] = base.tfidf_scores(tfidf_matrix, canonical_ids, seed_ids)

    matrix = {model_a: {} for model_a in PAIRWISE_MODELS}
    for model_a in PAIRWISE_MODELS:
        for model_b in PAIRWISE_MODELS:
            if model_a == model_b:
                matrix[model_a][model_b] = 1.0
                continue
            tau = base.compute_rank_correlation(scores[model_a], scores[model_b])["kendall_tau"]
            matrix[model_a][model_b] = tau
    return matrix


def summarize_pairwise(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {
        "mean": round(float(np.mean(arr)), 4),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "range": round(float(np.max(arr) - np.min(arr)), 4),
        "std": round(float(np.std(arr)), 4),
    }


def summarize_metric(values: list[float]) -> dict[str, float]:
    arr = np.asarray(values, dtype=float)
    return {
        "mean": round(float(np.mean(arr)), 4),
        "min": round(float(np.min(arr)), 4),
        "max": round(float(np.max(arr)), 4),
        "range": round(float(np.max(arr) - np.min(arr)), 4),
        "std": round(float(np.std(arr)), 4),
    }


def top_k_lists(scores: np.ndarray, ids: list[str], k: int) -> list[str]:
    top_idx = np.argsort(scores)[-k:][::-1]
    return [ids[i] for i in top_idx]


def category_summary_for_ids(
    ids: set[str],
    seed_categories: set[str],
    paper_categories: dict[str, list[str]],
) -> dict[str, float]:
    if not ids:
        return {"seed_category_matches": 0, "seed_category_match_rate": 0.0}
    matches = sum(
        1 for pid in ids if any(cat in seed_categories for cat in paper_categories.get(pid, []))
    )
    return {
        "seed_category_matches": matches,
        "seed_category_match_rate": round(matches / len(ids), 4),
    }


def run_pairwise_analysis(
    profiles: dict,
    embeddings: dict[str, tuple[np.ndarray, list[str]]],
    tfidf_matrix,
) -> dict:
    per_profile = {}
    pair_summaries = defaultdict(list)

    for profile_id, profile in profiles.items():
        variants = get_seed_variants(profile)
        variant_matrices = {}
        for variant_name in K5_VARIANT_NAMES:
            seed_ids = variants.get(variant_name)
            if not seed_ids:
                continue
            matrix = pairwise_tau_for_profile(embeddings, tfidf_matrix, seed_ids)
            variant_matrices[variant_name] = matrix
            for model_a in PAIRWISE_MODELS:
                for model_b in PAIRWISE_MODELS:
                    if model_a >= model_b:
                        continue
                    pair_summaries[(model_a, model_b)].append(matrix[model_a][model_b])

        per_profile[profile_id] = {
            "profile_name": profile.get("name", profile_id),
            "variant_matrices": variant_matrices,
        }

    mean_matrix = {model_a: {} for model_a in PAIRWISE_MODELS}
    pair_stats = {}
    for model_a in PAIRWISE_MODELS:
        for model_b in PAIRWISE_MODELS:
            if model_a == model_b:
                mean_matrix[model_a][model_b] = 1.0
                continue
            key = tuple(sorted((model_a, model_b)))
            stats = summarize_pairwise(pair_summaries[key])
            mean_matrix[model_a][model_b] = stats["mean"]
            if key not in pair_stats:
                pair_stats[f"{key[0]}__{key[1]}"] = stats

    return {
        "analysis": "pairwise_tau_matrix",
        "seed_variants_used": K5_VARIANT_NAMES,
        "models": PAIRWISE_MODELS,
        "mean_tau_matrix_across_profiles_and_grounded_k5_variants": mean_matrix,
        "pair_statistics": pair_stats,
        "per_profile": per_profile,
    }


def run_seed_sensitivity_analysis(
    profiles: dict,
    embeddings: dict[str, tuple[np.ndarray, list[str]]],
    tfidf_matrix,
    paper_categories: dict[str, list[str]],
) -> dict:
    results = {
        "analysis": "seed_sensitivity",
        "variants": {
            "grounded_k5_variants": K5_VARIANT_NAMES,
            "explicit_seed_count_variants": COUNT_VARIANT_NAMES,
        },
        "profiles": {},
    }

    minilm_emb, minilm_ids = embeddings["minilm"]

    for profile_id, profile in profiles.items():
        variants = get_seed_variants(profile)
        seed_variant_metrics = {}

        for variant_name, seed_ids in variants.items():
            variant_metrics = {}
            minilm_scores = base.centroid_scores(minilm_emb, minilm_ids, seed_ids)
            tfidf_scores = base.tfidf_scores(tfidf_matrix, minilm_ids, seed_ids)

            for model_key in MODELS:
                if model_key == "minilm":
                    continue
                model_emb, model_ids = embeddings[model_key]
                model_scores = base.centroid_scores(model_emb, model_ids, seed_ids)

                variant_metrics[model_key] = {
                    "seed_count": len(seed_ids),
                    "jaccard_vs_minilm": base.compute_jaccard_at_k(
                        model_scores, model_ids, minilm_scores, minilm_ids, K_VALUES
                    ),
                    "jaccard_vs_tfidf": base.compute_jaccard_at_k(
                        model_scores, model_ids, tfidf_scores, minilm_ids, K_VALUES
                    ),
                    "tau_vs_minilm": base.compute_rank_correlation(model_scores, minilm_scores)["kendall_tau"],
                    "category_recall": base.compute_category_recall(
                        model_scores, model_ids, seed_ids, paper_categories
                    )["recall"],
                    "n_truly_unique": len(
                        base.top_k_set(model_scores, model_ids, 20)
                        - base.top_k_set(minilm_scores, minilm_ids, 20)
                        - base.top_k_set(tfidf_scores, minilm_ids, 20)
                    ),
                }

            seed_variant_metrics[variant_name] = variant_metrics

        model_summaries = {}
        for model_key in MODELS:
            if model_key == "minilm":
                continue

            k5_variant_values = defaultdict(list)
            count_variant_values = defaultdict(list)

            for variant_name, metrics_by_model in seed_variant_metrics.items():
                if model_key not in metrics_by_model:
                    continue
                metrics = metrics_by_model[model_key]
                flat_metrics = {
                    "tau_vs_minilm": metrics["tau_vs_minilm"],
                    "jaccard_vs_minilm_at_20": metrics["jaccard_vs_minilm"]["jaccard_at_20"],
                    "jaccard_vs_minilm_at_50": metrics["jaccard_vs_minilm"]["jaccard_at_50"],
                    "jaccard_vs_minilm_at_100": metrics["jaccard_vs_minilm"]["jaccard_at_100"],
                    "jaccard_vs_tfidf_at_20": metrics["jaccard_vs_tfidf"]["jaccard_at_20"],
                    "jaccard_vs_tfidf_at_50": metrics["jaccard_vs_tfidf"]["jaccard_at_50"],
                    "jaccard_vs_tfidf_at_100": metrics["jaccard_vs_tfidf"]["jaccard_at_100"],
                    "category_recall": metrics["category_recall"],
                    "n_truly_unique": metrics["n_truly_unique"],
                }
                target = k5_variant_values if variant_name in K5_VARIANT_NAMES else count_variant_values
                for metric_name, value in flat_metrics.items():
                    target[metric_name].append(value)

            model_summaries[model_key] = {
                "grounded_k5_variant_summary": {
                    metric_name: summarize_metric(values)
                    for metric_name, values in k5_variant_values.items()
                    if values
                },
                "explicit_seed_count_summary": {
                    metric_name: summarize_metric(values)
                    for metric_name, values in count_variant_values.items()
                    if values
                },
            }

        results["profiles"][profile_id] = {
            "profile_name": profile.get("name", profile_id),
            "seed_variant_metrics": seed_variant_metrics,
            "model_summaries": model_summaries,
        }

    return results


def run_complementarity_analysis(
    profiles: dict,
    embeddings: dict[str, tuple[np.ndarray, list[str]]],
    tfidf_matrix,
    paper_categories: dict[str, list[str]],
) -> dict:
    minilm_emb, minilm_ids = embeddings["minilm"]
    results = {
        "analysis": "tfidf_complementarity",
        "k_values": K_VALUES,
        "profiles": {},
        "model_summary": {},
    }
    model_rollups = defaultdict(lambda: defaultdict(list))

    for profile_id, profile in profiles.items():
        seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]
        seed_categories = set()
        for sid in seed_ids:
            seed_categories.update(paper_categories.get(sid, []))

        minilm_scores = base.centroid_scores(minilm_emb, minilm_ids, seed_ids)
        tfidf_scores = base.tfidf_scores(tfidf_matrix, minilm_ids, seed_ids)

        minilm_top = {
            k: set(top_k_lists(minilm_scores, minilm_ids, k))
            for k in K_VALUES
        }
        tfidf_top = {
            k: set(top_k_lists(tfidf_scores, minilm_ids, k))
            for k in K_VALUES
        }

        per_model = {}
        for model_key in MODELS:
            if model_key == "minilm":
                continue
            model_emb, model_ids = embeddings[model_key]
            model_scores = base.centroid_scores(model_emb, model_ids, seed_ids)
            model_top = {k: set(top_k_lists(model_scores, model_ids, k)) for k in K_VALUES}

            k_results = {}
            for k in K_VALUES:
                union_with_model = minilm_top[k] | model_top[k]
                union_with_tfidf = minilm_top[k] | tfidf_top[k]
                model_only = model_top[k] - minilm_top[k]
                tfidf_only = tfidf_top[k] - minilm_top[k]
                model_truly_unique = model_top[k] - minilm_top[k] - tfidf_top[k]
                tfidf_truly_unique = tfidf_top[k] - minilm_top[k] - model_top[k]

                union_model_cats = category_summary_for_ids(
                    union_with_model, seed_categories, paper_categories
                )
                union_tfidf_cats = category_summary_for_ids(
                    union_with_tfidf, seed_categories, paper_categories
                )

                row = {
                    "union_size_minilm_plus_model": len(union_with_model),
                    "union_size_minilm_plus_tfidf": len(union_with_tfidf),
                    "union_delta_vs_tfidf": len(union_with_model) - len(union_with_tfidf),
                    "model_only_count": len(model_only),
                    "tfidf_only_count": len(tfidf_only),
                    "model_truly_unique_count": len(model_truly_unique),
                    "tfidf_truly_unique_count": len(tfidf_truly_unique),
                    "union_seed_category_matches_minilm_plus_model": union_model_cats["seed_category_matches"],
                    "union_seed_category_match_rate_minilm_plus_model": union_model_cats["seed_category_match_rate"],
                    "union_seed_category_matches_minilm_plus_tfidf": union_tfidf_cats["seed_category_matches"],
                    "union_seed_category_match_rate_minilm_plus_tfidf": union_tfidf_cats["seed_category_match_rate"],
                }
                k_results[str(k)] = row

                for field, value in row.items():
                    model_rollups[model_key][f"k{k}__{field}"].append(value)

            per_model[model_key] = k_results

        results["profiles"][profile_id] = {
            "profile_name": profile.get("name", profile_id),
            "per_model": per_model,
        }

    for model_key, fields in model_rollups.items():
        results["model_summary"][model_key] = {
            field: summarize_metric(values)
            for field, values in fields.items()
        }

    return results


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, cls=NumpyEncoder) + "\n")


def main():
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    profiles = load_profiles()
    embeddings = load_all_embeddings()
    paper_categories = base.load_paper_categories()
    _, minilm_ids = embeddings["minilm"]
    tfidf_matrix = build_tfidf(minilm_ids)

    pairwise = run_pairwise_analysis(profiles, embeddings, tfidf_matrix)
    seed_sensitivity = run_seed_sensitivity_analysis(
        profiles, embeddings, tfidf_matrix, paper_categories
    )
    complementarity = run_complementarity_analysis(
        profiles, embeddings, tfidf_matrix, paper_categories
    )

    timestamp = datetime.now(timezone.utc).isoformat()

    pairwise["timestamp"] = timestamp
    seed_sensitivity["timestamp"] = timestamp
    complementarity["timestamp"] = timestamp

    write_json(ARTIFACT_DIR / "pairwise-tau-matrix.json", pairwise)
    write_json(ARTIFACT_DIR / "seed-sensitivity.json", seed_sensitivity)
    write_json(ARTIFACT_DIR / "tfidf-complementarity.json", complementarity)

    print(f"Wrote {ARTIFACT_DIR / 'pairwise-tau-matrix.json'}")
    print(f"Wrote {ARTIFACT_DIR / 'seed-sensitivity.json'}")
    print(f"Wrote {ARTIFACT_DIR / 'tfidf-complementarity.json'}")


if __name__ == "__main__":
    main()
