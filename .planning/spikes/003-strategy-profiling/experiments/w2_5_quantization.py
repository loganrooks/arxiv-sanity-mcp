"""
W2.5: Embedding Quantization Impact

Test whether quantizing embeddings degrades quality:

For S1a (MiniLM, 384-dim, ~28.5 MB float32):
  - float32 baseline (existing)
  - float16 (~14 MB)
  - int8 (~7 MB) -- scale to [-127, 127], cast, search with int8 dot product

For S1c (SPECTER2, 768-dim, ~56.7 MB float32):
  - Same process

Profile at top-K=20 across all 8 profiles x 3 seed sets (full evaluation
to match W1A baseline precision).

Key question: Does quantization change quality metrics by more than 5%?
If not, it's a free memory win.
"""

from __future__ import annotations

import json
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
from harness.profiler import InterestProfile

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
OUTPUT_PATH = SPIKE_003_DATA / "w2_5_quantization_results.json"


# ---------------------------------------------------------------------------
# Quantization utilities
# ---------------------------------------------------------------------------

def quantize_float16(embeddings: np.ndarray) -> np.ndarray:
    """Quantize to float16.

    Simple cast. float16 has ~3 decimal digits of precision (vs ~7 for float32).
    For normalized embeddings in [-1, 1], this is more than enough for ranking.
    """
    return embeddings.astype(np.float16)


def quantize_int8(embeddings: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Quantize to int8 using per-dimension symmetric scaling.

    For each dimension, find max absolute value, scale to [-127, 127], cast.

    Returns:
        (int8_embeddings, scale_factors) -- scale_factors needed to
        reconstruct approximate float values or to do asymmetric dot product.
    """
    # Per-dimension scale: max absolute value across all vectors
    abs_max = np.abs(embeddings).max(axis=0)  # shape: (dim,)
    # Avoid division by zero
    abs_max = np.where(abs_max < 1e-10, 1.0, abs_max)
    scale = 127.0 / abs_max  # scale factors per dimension

    # Scale and clip to [-127, 127], then cast
    scaled = embeddings * scale[np.newaxis, :]
    scaled = np.clip(scaled, -127, 127)
    int8_emb = scaled.astype(np.int8)

    return int8_emb, abs_max / 127.0  # inverse scale for reconstruction


def int8_cosine_search(
    int8_embeddings: np.ndarray,
    query_float: np.ndarray,
    scale_factors: np.ndarray,
) -> np.ndarray:
    """Approximate cosine search using int8 embeddings.

    Strategy: quantize the query the same way, compute int32 dot product,
    then the ranking is preserved (scale factors cancel in argmax).

    For ranking purposes, we can skip the inverse scale -- the monotonic
    relationship is preserved.
    """
    # Scale query by same factors
    query_scaled = query_float * (127.0 / np.where(scale_factors < 1e-10, 1.0, scale_factors / scale_factors.max()))

    # Actually, the correct approach: quantize query with same scales
    abs_max_query = np.abs(query_float).max()
    if abs_max_query < 1e-10:
        return np.zeros(int8_embeddings.shape[0])

    query_scale = 127.0 / abs_max_query
    query_int8 = np.clip(query_float * query_scale, -127, 127).astype(np.int8)

    # Int8 dot product (numpy promotes to int32 for accumulation)
    # This preserves ranking because the scale factors are monotonic
    scores = int8_embeddings.astype(np.int32) @ query_int8.astype(np.int32)

    return scores.astype(np.float64)


# ---------------------------------------------------------------------------
# Strategy constructors for each precision level
# ---------------------------------------------------------------------------

def make_float32_strategy(
    embeddings: np.ndarray,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
    name: str,
    strategy_id: str,
) -> SimpleStrategy:
    """Float32 baseline strategy (identical to W1A)."""

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


def make_float16_strategy(
    embeddings_f32: np.ndarray,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
    name: str,
    strategy_id: str,
) -> SimpleStrategy:
    """Float16 strategy -- quantize then search in float16 space."""
    embeddings_f16 = quantize_float16(embeddings_f32)

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        # Compute centroid in float16
        centroid = embeddings_f16[seed_indices].astype(np.float32).mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = (centroid / norm).astype(np.float16)
        # Dot product in float16 (numpy may promote internally)
        scores = embeddings_f16.astype(np.float32) @ centroid.astype(np.float32)
        return scores

    return SimpleStrategy(
        name=name,
        strategy_id=strategy_id,
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_int8_strategy(
    embeddings_f32: np.ndarray,
    paper_ids: list[str],
    id_to_idx: dict[str, int],
    name: str,
    strategy_id: str,
) -> SimpleStrategy:
    """Int8 strategy -- quantize embeddings, search with int8 dot product."""
    int8_emb, scale_factors = quantize_int8(embeddings_f32)

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        # Compute centroid from float32 originals (query stays float for accuracy)
        centroid = embeddings_f32[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm

        # Quantize query with same per-dimension scales
        query_scaled = centroid / scale_factors
        query_scaled = np.clip(query_scaled, -127, 127)
        query_int8 = query_scaled.astype(np.int8)

        # Int8 dot product (numpy promotes to int32 for accumulation)
        scores = int8_emb.astype(np.int32) @ query_int8.astype(np.int32)
        return scores.astype(np.float64)

    return SimpleStrategy(
        name=name,
        strategy_id=strategy_id,
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def run_quantization_experiment():
    """Profile float32 vs float16 vs int8 for MiniLM and SPECTER2."""

    print("=" * 70)
    print("W2.5: Embedding Quantization Impact")
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

    # ----- Quantization statistics -----
    print("\n--- Quantization Statistics ---")

    minilm_emb = profiler.embeddings
    print(f"\nMiniLM (384-dim):")
    print(f"  float32: {minilm_emb.nbytes / 1024 / 1024:.1f} MB")
    minilm_f16 = quantize_float16(minilm_emb)
    print(f"  float16: {minilm_f16.nbytes / 1024 / 1024:.1f} MB")
    minilm_i8, minilm_scales = quantize_int8(minilm_emb)
    print(f"  int8:    {minilm_i8.nbytes / 1024 / 1024:.1f} MB")

    # Quantization error analysis
    minilm_f16_error = np.abs(minilm_emb - minilm_f16.astype(np.float32))
    print(f"  float16 max abs error: {minilm_f16_error.max():.6f}")
    print(f"  float16 mean abs error: {minilm_f16_error.mean():.6f}")

    minilm_i8_reconstructed = minilm_i8.astype(np.float32) * minilm_scales[np.newaxis, :]
    minilm_i8_error = np.abs(minilm_emb - minilm_i8_reconstructed)
    print(f"  int8 max abs error: {minilm_i8_error.max():.6f}")
    print(f"  int8 mean abs error: {minilm_i8_error.mean():.6f}")

    # Ranking preservation check: how many of top-20 are preserved?
    print("\n  Ranking preservation (random query, top-20):")
    rng = np.random.RandomState(42)
    test_query = rng.randn(384).astype(np.float32)
    test_query = test_query / np.linalg.norm(test_query)

    f32_scores = minilm_emb @ test_query
    f16_scores = minilm_f16.astype(np.float32) @ test_query
    i8_scores_raw = minilm_i8.astype(np.int32) @ (np.clip(test_query / minilm_scales, -127, 127)).astype(np.int8).astype(np.int32)

    f32_top20 = set(np.argsort(f32_scores)[-20:])
    f16_top20 = set(np.argsort(f16_scores)[-20:])
    i8_top20 = set(np.argsort(i8_scores_raw)[-20:])

    f16_overlap = len(f32_top20 & f16_top20)
    i8_overlap = len(f32_top20 & i8_top20)
    print(f"  float16 top-20 overlap with float32: {f16_overlap}/20")
    print(f"  int8 top-20 overlap with float32: {i8_overlap}/20")

    specter2_emb = profiler.specter2_embeddings
    specter2_id_to_idx = profiler.specter2_id_to_idx
    if specter2_emb is not None:
        print(f"\nSPECTER2 (768-dim):")
        print(f"  float32: {specter2_emb.nbytes / 1024 / 1024:.1f} MB")
        specter2_f16 = quantize_float16(specter2_emb)
        print(f"  float16: {specter2_f16.nbytes / 1024 / 1024:.1f} MB")
        specter2_i8, specter2_scales = quantize_int8(specter2_emb)
        print(f"  int8:    {specter2_i8.nbytes / 1024 / 1024:.1f} MB")

        specter2_f16_error = np.abs(specter2_emb - specter2_f16.astype(np.float32))
        print(f"  float16 max abs error: {specter2_f16_error.max():.6f}")
        print(f"  float16 mean abs error: {specter2_f16_error.mean():.6f}")

        specter2_i8_reconstructed = specter2_i8.astype(np.float32) * specter2_scales[np.newaxis, :]
        specter2_i8_error = np.abs(specter2_emb - specter2_i8_reconstructed)
        print(f"  int8 max abs error: {specter2_i8_error.max():.6f}")
        print(f"  int8 mean abs error: {specter2_i8_error.mean():.6f}")

    # ----- Build strategies for each precision -----
    print("\n--- Building Strategies ---")

    strategies_to_profile = []

    # MiniLM: float32, float16, int8
    strategies_to_profile.append((
        "S1a_f32",
        make_float32_strategy(minilm_emb, paper_ids, id_to_idx,
                              "MiniLM float32 (baseline)", "S1a_f32"),
        {"embedding": "MiniLM", "dim": 384, "precision": "float32",
         "memory_mb": round(minilm_emb.nbytes / 1024 / 1024, 1)},
    ))

    strategies_to_profile.append((
        "S1a_f16",
        make_float16_strategy(minilm_emb, paper_ids, id_to_idx,
                              "MiniLM float16", "S1a_f16"),
        {"embedding": "MiniLM", "dim": 384, "precision": "float16",
         "memory_mb": round(minilm_f16.nbytes / 1024 / 1024, 1)},
    ))

    strategies_to_profile.append((
        "S1a_i8",
        make_int8_strategy(minilm_emb, paper_ids, id_to_idx,
                           "MiniLM int8", "S1a_i8"),
        {"embedding": "MiniLM", "dim": 384, "precision": "int8",
         "memory_mb": round(minilm_i8.nbytes / 1024 / 1024, 1)},
    ))

    # SPECTER2: float32, float16, int8
    if specter2_emb is not None:
        strategies_to_profile.append((
            "S1c_f32",
            make_float32_strategy(specter2_emb, paper_ids, specter2_id_to_idx,
                                  "SPECTER2 float32 (baseline)", "S1c_f32"),
            {"embedding": "SPECTER2_adapter", "dim": 768, "precision": "float32",
             "memory_mb": round(specter2_emb.nbytes / 1024 / 1024, 1)},
        ))

        strategies_to_profile.append((
            "S1c_f16",
            make_float16_strategy(specter2_emb, paper_ids, specter2_id_to_idx,
                                  "SPECTER2 float16", "S1c_f16"),
            {"embedding": "SPECTER2_adapter", "dim": 768, "precision": "float16",
             "memory_mb": round(specter2_f16.nbytes / 1024 / 1024, 1)},
        ))

        strategies_to_profile.append((
            "S1c_i8",
            make_int8_strategy(specter2_emb, paper_ids, specter2_id_to_idx,
                               "SPECTER2 int8", "S1c_i8"),
            {"embedding": "SPECTER2_adapter", "dim": 768, "precision": "int8",
             "memory_mb": round(specter2_i8.nbytes / 1024 / 1024, 1)},
        ))

    # ----- Profile each -----
    print(f"\n--- Profiling {len(strategies_to_profile)} strategy variants ---")
    print("Using all 8 profiles x 3 seed sets (full evaluation)")

    all_cards = []

    for sid, strategy, config in strategies_to_profile:
        print(f"\n{'=' * 60}")
        print(f"PROFILING: {strategy.name} ({sid})")
        print(f"{'=' * 60}")
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

        # Print summary
        print(f"\n  --- Summary for {sid} ({t1 - t0:.1f}s) ---")
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

        lat = card.get("resources", {}).get("query_latency_ms", {})
        if lat:
            print(f"    latency p50={lat.get('p50', 0):.2f}ms  p95={lat.get('p95', 0):.2f}ms")

        all_cards.append(card)

    # ----- Comparison: precision impact -----
    print(f"\n{'=' * 60}")
    print("QUANTIZATION IMPACT ANALYSIS")
    print(f"{'=' * 60}")

    instrument_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]

    # Group by embedding model
    model_groups = {}
    for card in all_cards:
        config = card.get("config", {})
        model = config.get("embedding", "unknown")
        if model not in model_groups:
            model_groups[model] = {}
        precision = config.get("precision", "unknown")
        model_groups[model][precision] = card

    comparison_results = {}

    for model, precision_cards in model_groups.items():
        print(f"\n  {model}:")
        baseline = precision_cards.get("float32")
        if baseline is None:
            print("    No float32 baseline!")
            continue

        comparison_results[model] = {"precisions": {}}

        # Print header
        print(f"    {'Metric':<25s} {'float32':>10s} {'float16':>10s} {'f16 %chg':>10s} {'int8':>10s} {'i8 %chg':>10s}")
        print(f"    {'-' * 75}")

        for inst_name in instrument_names:
            base_val = baseline.get("instruments", {}).get(inst_name, {}).get("mean")
            row = f"    {inst_name:<25s}"

            for precision in ["float32", "float16", "int8"]:
                card = precision_cards.get(precision)
                if card is None:
                    row += f"{'N/A':>10s}" * 2
                    continue

                val = card.get("instruments", {}).get(inst_name, {}).get("mean")

                if precision == "float32":
                    row += f" {val:10.4f}" if val is not None else f"{'N/A':>10s}"
                else:
                    if val is not None:
                        row += f" {val:10.4f}"
                    else:
                        row += f"{'N/A':>10s}"

                    if val is not None and base_val is not None and base_val != 0:
                        pct_change = (val - base_val) / abs(base_val) * 100
                        row += f" {pct_change:+9.2f}%"
                    else:
                        row += f"{'N/A':>10s}"

            print(row)

        # Memory summary
        print(f"\n    Memory:")
        for precision in ["float32", "float16", "int8"]:
            card = precision_cards.get(precision)
            if card:
                mem = card.get("config", {}).get("memory_mb")
                lat = card.get("resources", {}).get("query_latency_ms", {})
                p50 = lat.get("p50", "?")
                print(f"      {precision}: {mem} MB, p50 latency={p50:.2f}ms" if isinstance(p50, float)
                      else f"      {precision}: {mem} MB, p50 latency=?")

                comparison_results[model]["precisions"][precision] = {
                    "memory_mb": mem,
                    "instruments": {
                        name: card.get("instruments", {}).get(name, {}).get("mean")
                        for name in instrument_names
                    },
                    "latency_p50_ms": lat.get("p50"),
                    "latency_p95_ms": lat.get("p95"),
                }

        # Verdict: does any precision exceed 5% degradation on any metric?
        print(f"\n    Verdict (5% threshold):")
        for precision in ["float16", "int8"]:
            card = precision_cards.get(precision)
            if card is None:
                continue

            worst_degradation = 0
            worst_metric = None

            for inst_name in instrument_names:
                base_val = baseline.get("instruments", {}).get(inst_name, {}).get("mean")
                val = card.get("instruments", {}).get(inst_name, {}).get("mean")

                if base_val is not None and val is not None and base_val != 0:
                    # For MRR, coverage, proximity: decrease is degradation
                    # For diversity, novelty, surprise: direction depends on interpretation
                    # Use absolute percent change as conservative check
                    pct = abs(val - base_val) / abs(base_val) * 100
                    if pct > worst_degradation:
                        worst_degradation = pct
                        worst_metric = inst_name

            if worst_degradation <= 5.0:
                print(f"      {precision}: PASS -- worst change {worst_degradation:.2f}% on {worst_metric}")
                comparison_results[model]["precisions"][precision]["verdict"] = "PASS"
            else:
                print(f"      {precision}: FAIL -- {worst_degradation:.2f}% change on {worst_metric} (>5%)")
                comparison_results[model]["precisions"][precision]["verdict"] = "FAIL"

            comparison_results[model]["precisions"][precision]["worst_change_pct"] = round(worst_degradation, 2)
            comparison_results[model]["precisions"][precision]["worst_change_metric"] = worst_metric

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "experiment": "W2.5: Embedding Quantization Impact",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_time_s": round(total_time, 1),
        "config": {
            "top_k": 20,
            "n_profiles": len(profiler.profiles),
            "corpus_size": n_papers,
            "threshold_pct": 5.0,
        },
        "quantization_stats": {
            "MiniLM": {
                "dim": 384,
                "n_vectors": minilm_emb.shape[0],
                "float32_mb": round(minilm_emb.nbytes / 1024 / 1024, 1),
                "float16_mb": round(minilm_f16.nbytes / 1024 / 1024, 1),
                "int8_mb": round(minilm_i8.nbytes / 1024 / 1024, 1),
                "float16_max_abs_error": float(minilm_f16_error.max()),
                "float16_mean_abs_error": float(minilm_f16_error.mean()),
                "int8_max_abs_error": float(minilm_i8_error.max()),
                "int8_mean_abs_error": float(minilm_i8_error.mean()),
                "float16_top20_overlap": f16_overlap,
                "int8_top20_overlap": i8_overlap,
            },
        },
        "profile_cards": all_cards,
        "comparison": comparison_results,
        "notes": {
            "quantization_method": (
                "float16: simple cast. int8: per-dimension symmetric scaling "
                "to [-127, 127], int8 dot product for search."
            ),
            "evaluation": (
                "Full evaluation: all 8 profiles x 3 seed sets at top-K=20 "
                "to match W1A baseline precision."
            ),
            "int8_search": (
                "Int8 search uses quantized query + int8 dot product. "
                "Rankings are preserved because scale factors cancel in argmax."
            ),
        },
    }

    # Add SPECTER2 stats if available
    if specter2_emb is not None:
        output["quantization_stats"]["SPECTER2"] = {
            "dim": 768,
            "n_vectors": specter2_emb.shape[0],
            "float32_mb": round(specter2_emb.nbytes / 1024 / 1024, 1),
            "float16_mb": round(specter2_f16.nbytes / 1024 / 1024, 1),
            "int8_mb": round(specter2_i8.nbytes / 1024 / 1024, 1),
            "float16_max_abs_error": float(specter2_f16_error.max()),
            "float16_mean_abs_error": float(specter2_f16_error.mean()),
            "int8_max_abs_error": float(specter2_i8_error.max()),
            "int8_mean_abs_error": float(specter2_i8_error.mean()),
        }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n{'=' * 60}")
    print(f"W2.5 COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total time: {total_time:.1f}s ({total_time / 60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    run_quantization_experiment()
