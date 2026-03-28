#!/usr/bin/env python3
"""
Spike 004 Phase 3a: Generate qualitative review inputs.

Reads Phase 2 classifications to determine which models need review and at what depth.
Generates review input JSON files per model per profile with paper details for
qualitative assessment.

Usage:
  conda activate ml-dev
  python generate_reviews.py
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
SPIKE_003_DIR = SPIKE_004_DIR.parent / "003-strategy-profiling"
SPIKE_001_DIR = SPIKE_004_DIR.parent / "001-volume-filtering-scoring-landscape"

DATA_DIR = SPIKE_004_DIR / "experiments" / "data"
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"
REVIEW_DIR = SPIKE_004_DIR / "experiments" / "review_inputs"
PROFILES_PATH = SPIKE_003_DIR / "experiments" / "data" / "interest_profiles.json"
HARVEST_DB = SPIKE_001_DIR / "experiments" / "data" / "spike_001_harvest.db"


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# Coverage rules from PROTOCOL.md Section 2
COVERAGE = {
    "divergent": {"n_profiles": 8, "depth": "full", "blind_comparisons": 2},
    "mid_overlap": {"n_profiles": 5, "depth": "full", "blind_comparisons": 1},
    "high_overlap": {"n_profiles": 3, "depth": "abbreviated", "blind_comparisons": 0},
    "near_identical": {"n_profiles": 2, "depth": "abbreviated", "blind_comparisons": 0},
}


def load_paper_details(paper_ids: list[str]) -> dict[str, dict]:
    """Load title, abstract, categories for papers."""
    conn = sqlite3.connect(str(HARVEST_DB))
    conn.row_factory = sqlite3.Row
    placeholders = ",".join("?" for _ in paper_ids)
    rows = conn.execute(
        f"SELECT arxiv_id, title, abstract, primary_category FROM papers "
        f"WHERE arxiv_id IN ({placeholders})",
        paper_ids,
    ).fetchall()
    conn.close()
    return {r["arxiv_id"]: dict(r) for r in rows}


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


def select_review_profiles(
    classification: dict,
    per_profile_jaccards: dict[str, float],
    coverage: dict,
) -> list[str]:
    """Select which profiles to review based on classification."""
    n = coverage["n_profiles"]
    all_profiles = list(per_profile_jaccards.keys())

    if n >= len(all_profiles):
        return all_profiles

    # Sort by Jaccard ascending (most divergent first)
    sorted_profiles = sorted(all_profiles, key=lambda p: per_profile_jaccards[p])

    if coverage["depth"] == "full" and n == 5:
        # mid_overlap: 3 most divergent + 1 median + 1 highest
        most_div = sorted_profiles[:3]
        median_idx = len(sorted_profiles) // 2
        median_p = sorted_profiles[median_idx]
        highest_p = sorted_profiles[-1]
        selected = list(dict.fromkeys(most_div + [median_p, highest_p]))
        return selected[:n]
    elif n == 3:
        # high_overlap: 2 most divergent + 1 random (pick median)
        return [sorted_profiles[0], sorted_profiles[1], sorted_profiles[len(sorted_profiles) // 2]]
    elif n == 2:
        # near_identical: most divergent + 1 random (pick last)
        return [sorted_profiles[0], sorted_profiles[-1]]
    else:
        return sorted_profiles[:n]


def generate_review_input(
    model_key: str,
    profile_id: str,
    profile: dict,
    model_emb: np.ndarray,
    model_ids: list[str],
    minilm_emb: np.ndarray,
    minilm_ids: list[str],
    depth: str,
    is_blind: bool = False,
) -> dict:
    """Generate review input for one model-profile pair."""
    seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]

    # Get top-20 for model and MiniLM
    model_scores = centroid_scores(model_emb, model_ids, seed_ids)
    minilm_scores = centroid_scores(minilm_emb, minilm_ids, seed_ids)

    model_top20_idx = np.argsort(model_scores)[-20:][::-1]
    minilm_top20_idx = np.argsort(minilm_scores)[-20:][::-1]

    model_top20 = [(model_ids[i], float(model_scores[i])) for i in model_top20_idx]
    minilm_top20 = [(minilm_ids[i], float(minilm_scores[i])) for i in minilm_top20_idx]

    # Identify divergent papers
    model_set = {pid for pid, _ in model_top20}
    minilm_set = {pid for pid, _ in minilm_top20}
    model_unique = model_set - minilm_set
    minilm_unique = minilm_set - model_set

    # Load paper details
    all_paper_ids = list(model_set | minilm_set | set(seed_ids))
    details = load_paper_details(all_paper_ids)

    # Build review input
    seed_info = []
    for sid in seed_ids:
        d = details.get(sid, {})
        seed_info.append({
            "arxiv_id": sid,
            "title": d.get("title", ""),
            "category": d.get("primary_category", ""),
        })

    def paper_entry(pid, score, source_label):
        d = details.get(pid, {})
        return {
            "arxiv_id": pid,
            "title": d.get("title", ""),
            "abstract": d.get("abstract", ""),
            "category": d.get("primary_category", ""),
            "score": round(score, 6),
            "source": source_label,
            "in_model_top20": pid in model_set,
            "in_minilm_top20": pid in minilm_set,
            "divergent": pid in model_unique or pid in minilm_unique,
        }

    if is_blind:
        # Blind comparison: present as "Model A" vs "Model B"
        import random
        rng = random.Random(hash(f"{model_key}_{profile_id}"))
        labels = ["Model A", "Model B"]
        if rng.random() > 0.5:
            labels = labels[::-1]
        model_label, minilm_label = labels

        review_input = {
            "type": "blind_comparison",
            "profile_id": profile_id,
            "profile_name": profile.get("name", profile_id),
            "depth": depth,
            "seeds": seed_info,
            "model_a_label": labels[0],
            "model_b_label": labels[1],
            "model_a_papers": [
                paper_entry(pid, sc, labels[0])
                for pid, sc in (model_top20 if labels[0] == model_label else minilm_top20)
            ],
            "model_b_papers": [
                paper_entry(pid, sc, labels[1])
                for pid, sc in (minilm_top20 if labels[0] == model_label else model_top20)
            ],
            "_key": {model_label: model_key, minilm_label: "minilm"},
        }
    else:
        review_input = {
            "type": "characterization",
            "model_key": model_key,
            "profile_id": profile_id,
            "profile_name": profile.get("name", profile_id),
            "depth": depth,
            "seeds": seed_info,
            "model_top20": [paper_entry(pid, sc, model_key) for pid, sc in model_top20],
            "minilm_top20": [paper_entry(pid, sc, "minilm") for pid, sc in minilm_top20],
            "model_unique_count": len(model_unique),
            "minilm_unique_count": len(minilm_unique),
            "shared_count": len(model_set & minilm_set),
        }

    return review_input


def main():
    print("=" * 60)
    print("SPIKE 004 PHASE 3a: GENERATE REVIEW INPUTS")
    print("=" * 60)

    # Check prerequisites
    cls_path = CHECKPOINT_DIR / "phase2_classification.json"
    if not cls_path.exists():
        print("ERROR: Phase 2 classification checkpoint not found.")
        sys.exit(1)

    with open(cls_path) as f:
        cls_data = json.load(f)

    with open(PROFILES_PATH) as f:
        profiles = json.load(f)["profiles"]

    # Load MiniLM baseline
    minilm_emb = np.load(str(DATA_DIR / "minilm_2000.npy"))
    with open(DATA_DIR / "minilm_2000_ids.json") as f:
        minilm_ids = json.load(f)

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    generated = []

    for model_key, cls in cls_data["classifications"].items():
        classification = cls["classification"]
        coverage = COVERAGE[classification]
        per_profile_j = cls["per_profile_jaccard_20"]

        print(f"\n--- {model_key}: {classification} ---")
        print(f"  Coverage: {coverage['n_profiles']} profiles, {coverage['depth']} depth, "
              f"{coverage['blind_comparisons']} blind comparisons")

        # Select profiles
        review_profiles = select_review_profiles(cls, per_profile_j, coverage)
        print(f"  Profiles: {', '.join(review_profiles)}")

        # Load model embeddings
        model_emb = np.load(str(DATA_DIR / f"{model_key}_2000.npy"))
        with open(DATA_DIR / f"{model_key}_2000_ids.json") as f:
            model_ids = json.load(f)

        # Select blind comparison profiles (most divergent)
        blind_profiles = sorted(review_profiles, key=lambda p: per_profile_j[p])[:coverage["blind_comparisons"]]

        for pid in review_profiles:
            is_blind = pid in blind_profiles

            review_input = generate_review_input(
                model_key, pid, profiles[pid],
                model_emb, model_ids,
                minilm_emb, minilm_ids,
                coverage["depth"],
                is_blind=is_blind,
            )

            # Save
            suffix = "_blind" if is_blind else ""
            filename = f"{model_key}_{pid}{suffix}.json"
            output_path = REVIEW_DIR / filename
            with open(output_path, "w") as f:
                json.dump(review_input, f, indent=2, cls=NumpyEncoder)

            generated.append({
                "model": model_key,
                "profile": pid,
                "type": "blind_comparison" if is_blind else "characterization",
                "depth": coverage["depth"],
                "path": str(output_path),
            })
            print(f"  Generated: {filename}")

    # Save manifest
    manifest = {
        "phase": "phase3_review_inputs",
        "n_reviews": len(generated),
        "reviews": generated,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(REVIEW_DIR / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Generated {len(generated)} review inputs in {REVIEW_DIR}/")
    print("Next: Run qualitative reviews (run_reviews.py)")


if __name__ == "__main__":
    main()
