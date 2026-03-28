#!/usr/bin/env python3
"""
Spike 004 Phase 1b: Sample validation gate.

Three checks per PROTOCOL.md Section 3:
  1. MiniLM baseline validation (sample vs full corpus top-20)
  2. Challenger degeneracy check (score spread, gap, ceiling per profile)
  3. Structural comparison (top-100 Jaccard per model vs MiniLM)

This is a GO/NO-GO gate. Phase 2 will not proceed without this checkpoint.

Usage:
  conda activate ml-dev
  python validate_sample.py
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
SPIKE_003_DIR = SPIKE_004_DIR.parent / "003-strategy-profiling"
SPIKE_002_DIR = SPIKE_004_DIR.parent / "002-backend-comparison"

DATA_DIR = SPIKE_004_DIR / "experiments" / "data"
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"
PROFILES_PATH = SPIKE_003_DIR / "experiments" / "data" / "interest_profiles.json"

# Full 19K MiniLM embeddings (for baseline validation)
MINILM_19K_PATH = SPIKE_002_DIR / "experiments" / "data" / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DIR / "experiments" / "data" / "arxiv_ids_19k.json"

# Thresholds from PROTOCOL.md
DEGENERACY_SCORE_SPREAD = 0.005   # Flag if std(top-20) < this
DEGENERACY_SCORE_GAP = 0.01      # Flag if mean(top-20) - mean(rest) < this
DEGENERACY_CEILING = 0.15        # Flag if max(score) < this
BASELINE_JACCARD_THRESHOLD = 0.8  # MiniLM sample vs full must exceed this

# Models to validate (must have embeddings in data/)
MODELS = ["minilm", "specter2", "stella", "qwen3", "gte", "voyage"]


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
        data = json.load(f)
    return data["profiles"]


def load_model_embeddings(model_key: str) -> tuple[np.ndarray, list[str]] | None:
    emb_path = DATA_DIR / f"{model_key}_2000.npy"
    ids_path = DATA_DIR / f"{model_key}_2000_ids.json"
    if not emb_path.exists():
        return None
    emb = np.load(str(emb_path))
    with open(ids_path) as f:
        ids = json.load(f)
    return emb, ids


def centroid_scores(
    embeddings: np.ndarray,
    paper_ids: list[str],
    seed_ids: list[str],
) -> np.ndarray:
    """Compute centroid cosine similarity scores."""
    id_to_idx = {pid: i for i, pid in enumerate(paper_ids)}
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        return np.zeros(len(paper_ids))

    centroid = embeddings[seed_indices].mean(axis=0)
    norm = np.linalg.norm(centroid)
    if norm < 1e-10:
        return np.zeros(len(paper_ids))
    centroid = centroid / norm

    return embeddings @ centroid


def top_k_ids(scores: np.ndarray, paper_ids: list[str], k: int = 20) -> set[str]:
    """Get top-K paper IDs by score."""
    top_indices = np.argsort(scores)[-k:][::-1]
    return {paper_ids[i] for i in top_indices}


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    return len(set_a & set_b) / len(set_a | set_b)


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------

def check_baseline_validation(profiles: dict) -> dict:
    """Step 1: MiniLM sample vs full corpus top-20 comparison."""
    print("\n=== Step 1: MiniLM Baseline Validation ===")

    sample_data = load_model_embeddings("minilm")
    if sample_data is None:
        return {"status": "SKIP", "reason": "MiniLM sample embeddings not found"}

    sample_emb, sample_ids = sample_data
    full_emb = np.load(str(MINILM_19K_PATH))
    with open(MINILM_IDS_PATH) as f:
        full_ids = json.load(f)

    # L2 normalize full embeddings
    norms = np.linalg.norm(full_emb, axis=1, keepdims=True)
    norms[norms == 0] = 1
    full_emb = full_emb / norms

    test_profiles = ["P1", "P3", "P4"]
    results = {}

    for pid in test_profiles:
        profile = profiles[pid]
        seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]

        # Top-20 on sample
        sample_scores = centroid_scores(sample_emb, sample_ids, seed_ids)
        sample_top20 = top_k_ids(sample_scores, sample_ids, k=20)

        # Top-20 on full corpus (intersected with sample IDs for fair comparison)
        full_scores = centroid_scores(full_emb, full_ids, seed_ids)
        full_top20_all = top_k_ids(full_scores, full_ids, k=20)
        # Also get top-20 from full corpus restricted to sample papers
        sample_id_set = set(sample_ids)
        full_id_to_idx = {pid_: i for i, pid_ in enumerate(full_ids)}
        sample_mask = np.array([pid_ in sample_id_set for pid_ in full_ids])
        masked_scores = np.where(sample_mask, full_scores, -np.inf)
        full_top20_in_sample = top_k_ids(masked_scores, full_ids, k=20)

        j = jaccard(sample_top20, full_top20_in_sample)
        results[pid] = {
            "jaccard_sample_vs_full_restricted": round(j, 4),
            "pass": j >= BASELINE_JACCARD_THRESHOLD,
            "sample_top20_in_full_top20": len(sample_top20 & full_top20_all),
        }
        status = "PASS" if j >= BASELINE_JACCARD_THRESHOLD else "FAIL"
        print(f"  {pid}: Jaccard={j:.3f} [{status}]")

    all_pass = all(r["pass"] for r in results.values())
    return {
        "status": "PASS" if all_pass else "FAIL",
        "threshold": BASELINE_JACCARD_THRESHOLD,
        "profiles": results,
    }


def check_challenger_degeneracy(profiles: dict) -> dict:
    """Step 2: Check each model for degenerate score distributions."""
    print("\n=== Step 2: Challenger Degeneracy Check ===")

    all_results = {}

    for model_key in MODELS:
        data = load_model_embeddings(model_key)
        if data is None:
            all_results[model_key] = {"status": "SKIP", "reason": "embeddings not found"}
            continue

        emb, paper_ids = data
        profile_flags = {}
        n_flagged = 0

        for pid, profile in profiles.items():
            seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]
            scores = centroid_scores(emb, paper_ids, seed_ids)

            top_20_indices = np.argsort(scores)[-20:][::-1]
            top_20_scores = scores[top_20_indices]
            rest_scores = np.delete(scores, top_20_indices)

            spread = float(np.std(top_20_scores))
            gap = float(np.mean(top_20_scores) - np.mean(rest_scores))
            ceiling = float(np.max(scores))

            flags = []
            if spread < DEGENERACY_SCORE_SPREAD:
                flags.append("low_spread")
            if gap < DEGENERACY_SCORE_GAP:
                flags.append("low_gap")
            if ceiling < DEGENERACY_CEILING:
                flags.append("low_ceiling")

            profile_flags[pid] = {
                "top20_spread": round(spread, 6),
                "top20_gap": round(gap, 6),
                "max_score": round(ceiling, 6),
                "flags": flags,
            }
            if flags:
                n_flagged += 1

        status = "WARN" if n_flagged >= 3 else "PASS"
        all_results[model_key] = {
            "status": status,
            "n_flagged_profiles": n_flagged,
            "profiles": profile_flags,
        }
        print(f"  {model_key}: {n_flagged}/8 profiles flagged [{status}]")

    return all_results


def check_structural_comparison(profiles: dict) -> dict:
    """Step 3: Top-100 Jaccard per model vs MiniLM per profile."""
    print("\n=== Step 3: Structural Comparison (top-100 Jaccard vs MiniLM) ===")

    minilm_data = load_model_embeddings("minilm")
    if minilm_data is None:
        return {"status": "SKIP", "reason": "MiniLM embeddings not found"}

    minilm_emb, minilm_ids = minilm_data
    all_results = {}

    for model_key in MODELS:
        if model_key == "minilm":
            continue

        data = load_model_embeddings(model_key)
        if data is None:
            all_results[model_key] = {"status": "SKIP"}
            continue

        emb, paper_ids = data

        # Align IDs — both should be in the same order from embed_models.py
        # but verify
        if paper_ids != minilm_ids:
            # Build intersection mapping
            shared = set(paper_ids) & set(minilm_ids)
            print(f"  WARNING: {model_key} has {len(shared)}/{len(paper_ids)} shared IDs with MiniLM")

        profile_jaccards = {}
        for pid, profile in profiles.items():
            seed_ids = [s["arxiv_id"] for s in profile["seed_papers"][:5]]

            minilm_scores = centroid_scores(minilm_emb, minilm_ids, seed_ids)
            model_scores = centroid_scores(emb, paper_ids, seed_ids)

            minilm_top100 = top_k_ids(minilm_scores, minilm_ids, k=100)
            model_top100 = top_k_ids(model_scores, paper_ids, k=100)

            j = jaccard(minilm_top100, model_top100)
            profile_jaccards[pid] = round(j, 4)

        mean_j = np.mean(list(profile_jaccards.values()))
        min_j = min(profile_jaccards.values())

        all_results[model_key] = {
            "per_profile_jaccard_100": profile_jaccards,
            "mean_jaccard_100": round(float(mean_j), 4),
            "min_jaccard_100": round(float(min_j), 4),
            "note": "High (>0.9) = same pool; Low (<0.5) = investigate bias vs real difference",
        }
        print(f"  {model_key}: mean J@100={mean_j:.3f}, min={min_j:.3f}")

    return all_results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("SPIKE 004 PHASE 1b: SAMPLE VALIDATION GATE")
    print("=" * 60)

    profiles = load_profiles()

    # Check prerequisites
    emb_checkpoint = CHECKPOINT_DIR / "phase1_embeddings.json"
    if not emb_checkpoint.exists():
        print("ERROR: Phase 1 embeddings checkpoint not found.")
        print("Run embed_models.py first.")
        sys.exit(1)

    # Run all three checks
    baseline = check_baseline_validation(profiles)
    degeneracy = check_challenger_degeneracy(profiles)
    structural = check_structural_comparison(profiles)

    # Determine overall go/no-go
    baseline_pass = baseline["status"] == "PASS"
    any_warns = any(
        v.get("status") == "WARN"
        for v in degeneracy.values()
        if isinstance(v, dict)
    )

    if baseline_pass and not any_warns:
        verdict = "GO"
    elif baseline_pass and any_warns:
        verdict = "GO_WITH_CAVEATS"
    else:
        verdict = "NO_GO"

    print("\n" + "=" * 60)
    print(f"VALIDATION VERDICT: {verdict}")
    print("=" * 60)

    if verdict == "GO_WITH_CAVEATS":
        warned = [k for k, v in degeneracy.items()
                  if isinstance(v, dict) and v.get("status") == "WARN"]
        print(f"  Caveats: {', '.join(warned)} have degenerate score distributions")
        print("  These models' findings carry lower extrapolation confidence")

    if verdict == "NO_GO":
        print("  MiniLM baseline validation FAILED — sample may not be representative")
        print("  Action: investigate before proceeding to Phase 2")

    # Save checkpoint
    checkpoint = {
        "phase": "phase1_validation",
        "verdict": verdict,
        "baseline_validation": baseline,
        "challenger_degeneracy": degeneracy,
        "structural_comparison": structural,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    checkpoint_path = CHECKPOINT_DIR / "phase1_validation.json"
    with open(checkpoint_path, "w") as f:
        json.dump(checkpoint, f, indent=2, cls=NumpyEncoder)
    print(f"\nCheckpoint saved: {checkpoint_path}")


if __name__ == "__main__":
    main()
