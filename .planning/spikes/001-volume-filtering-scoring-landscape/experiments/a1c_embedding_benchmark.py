"""
A1c.3: Lightweight Embedding Benchmark

Measures embedding computation time (CPU vs GPU), memory footprint,
and brute-force cosine similarity search performance at scale points.

Tests whether semantic search is feasible without pgvector at personal
scale, using all-MiniLM-L6-v2 (384-dim, ~22M parameters).

Output: JSON results file + console summary.
"""

import json
import os
import sqlite3
import time
from pathlib import Path

import numpy as np

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
RESULTS_PATH = DATA_DIR / "embedding_benchmark_results.json"

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

SCALE_POINTS = [5_000, 10_000, 19_252, 50_000, 100_000, 215_000]

# Number of search queries to run for timing
SEARCH_RUNS = 20
SEARCH_WARMUP = 2

# Batch size for embedding computation
EMBED_BATCH_SIZE = 256

# --- Helpers ---


def load_abstracts(db_path: str) -> list[str]:
    """Load all paper abstracts from the harvest DB."""
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT abstract FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]


def scale_texts(texts: list[str], target: int) -> list[str]:
    """Scale text list to target size by cycling."""
    if target <= len(texts):
        return texts[:target]
    result = []
    for i in range(target):
        result.append(texts[i % len(texts)])
    return result


def fmt_bytes(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    elif b < 1024**2:
        return f"{b / 1024:.1f} KB"
    elif b < 1024**3:
        return f"{b / 1024**2:.1f} MB"
    else:
        return f"{b / 1024**3:.2f} GB"


def fmt_ms(seconds: float) -> str:
    return f"{seconds * 1000:.1f}ms"


# --- Main benchmark ---


def run_benchmark():
    from sentence_transformers import SentenceTransformer
    import torch

    print(f"Loading abstracts from {SOURCE_DB}...")
    abstracts = load_abstracts(str(SOURCE_DB))
    print(f"Loaded {len(abstracts)} abstracts")

    # Pick a query abstract
    query_text = abstracts[len(abstracts) // 2]

    devices = ["cpu"]
    if torch.cuda.is_available():
        devices.append("cuda")
        print(f"CUDA available: {torch.cuda.get_device_name(0)}")

    all_results = {}

    for device in devices:
        print(f"\n{'=' * 70}")
        print(f"Device: {device.upper()}")
        print(f"{'=' * 70}")

        # Load model on device
        print(f"  Loading {MODEL_NAME} on {device}...")
        t0 = time.monotonic()
        model = SentenceTransformer(MODEL_NAME, device=device)
        load_time = time.monotonic() - t0
        print(f"  Model loaded in {load_time:.1f}s")

        device_results = {"model_load_time_s": round(load_time, 2)}

        for scale in SCALE_POINTS:
            print(f"\n  Scale: {scale:,} papers")

            texts = scale_texts(abstracts, scale)

            # 1. Embedding computation time
            t0 = time.monotonic()
            embeddings = model.encode(
                texts,
                batch_size=EMBED_BATCH_SIZE,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=True,  # Pre-normalize for cosine sim
            )
            embed_time = time.monotonic() - t0
            per_paper = embed_time / scale

            # 2. Memory footprint
            float32_bytes = embeddings.nbytes  # numpy default is float64 from encode
            # Force float32 if not already
            if embeddings.dtype != np.float32:
                embeddings = embeddings.astype(np.float32)
                float32_bytes = embeddings.nbytes
            float16_bytes = scale * EMBEDDING_DIM * 2  # hypothetical float16

            # 3. Brute-force cosine similarity search
            # Since embeddings are pre-normalized, cosine sim = dot product
            query_embedding = model.encode(
                [query_text],
                convert_to_numpy=True,
                normalize_embeddings=True,
            ).astype(np.float32)

            # Warmup
            for _ in range(SEARCH_WARMUP):
                scores = query_embedding @ embeddings.T

            # Timed search runs
            search_times = []
            for _ in range(SEARCH_RUNS):
                t0 = time.monotonic()
                scores = query_embedding @ embeddings.T
                top_indices = np.argpartition(scores.flatten(), -20)[-20:]
                top_indices = top_indices[np.argsort(scores.flatten()[top_indices])[::-1]]
                search_times.append(time.monotonic() - t0)

            search_median = np.median(search_times)
            search_p95 = np.percentile(search_times, 95)

            # Top scores for sanity check
            top_scores = scores.flatten()[top_indices[:5]]

            result = {
                "scale": scale,
                "device": device,
                "embed_time_s": round(embed_time, 2),
                "embed_per_paper_ms": round(per_paper * 1000, 2),
                "float32_bytes": float32_bytes,
                "float16_bytes": float16_bytes,
                "search_median_ms": round(float(search_median) * 1000, 2),
                "search_p95_ms": round(float(search_p95) * 1000, 2),
                "search_times_ms": [round(t * 1000, 2) for t in search_times],
                "top_scores": [round(float(s), 4) for s in top_scores],
            }
            device_results[str(scale)] = result

            print(f"    Embed time:   {embed_time:.1f}s ({per_paper*1000:.2f}ms/paper)")
            print(f"    Memory f32:   {fmt_bytes(float32_bytes)}")
            print(f"    Memory f16:   {fmt_bytes(float16_bytes)}")
            print(f"    Search p50:   {fmt_ms(search_median)}")
            print(f"    Search p95:   {fmt_ms(search_p95)}")
            print(f"    Top scores:   {[round(float(s), 3) for s in top_scores]}")

        # Free GPU memory between devices
        del model
        if device == "cuda":
            torch.cuda.empty_cache()

        all_results[device] = device_results

    # Save results
    with open(RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")

    # Print comparison
    print_summary(all_results, devices)


def print_summary(all_results: dict, devices: list[str]):
    print(f"\n{'=' * 90}")
    print("SUMMARY: Embedding computation time by device and scale")
    print(f"{'=' * 90}")

    header = f"{'Device':<10}"
    for s in SCALE_POINTS:
        header += f"  {s//1000}K".rjust(12)
    print(header)
    print("-" * 90)

    for device in devices:
        row = f"{device:<10}"
        for s in SCALE_POINTS:
            data = all_results[device].get(str(s))
            if data:
                row += f"  {data['embed_time_s']:.1f}s".rjust(12)
            else:
                row += "  —".rjust(12)
        print(row)

    print(f"\n{'=' * 90}")
    print("SUMMARY: Brute-force search time (p50) by device and scale")
    print(f"{'=' * 90}")

    header = f"{'Device':<10}"
    for s in SCALE_POINTS:
        header += f"  {s//1000}K".rjust(12)
    print(header)
    print("-" * 90)

    for device in devices:
        row = f"{device:<10}"
        for s in SCALE_POINTS:
            data = all_results[device].get(str(s))
            if data:
                row += f"  {data['search_median_ms']:.1f}ms".rjust(12)
            else:
                row += "  —".rjust(12)
        print(row)

    print(f"\n{'=' * 90}")
    print("SUMMARY: Memory footprint (float32) by scale")
    print(f"{'=' * 90}")

    header = f"{'Dtype':<10}"
    for s in SCALE_POINTS:
        header += f"  {s//1000}K".rjust(12)
    print(header)
    print("-" * 90)

    row_32 = f"{'float32':<10}"
    row_16 = f"{'float16':<10}"
    for s in SCALE_POINTS:
        data = all_results[devices[0]].get(str(s))
        if data:
            row_32 += f"  {fmt_bytes(data['float32_bytes'])}".rjust(12)
            row_16 += f"  {fmt_bytes(data['float16_bytes'])}".rjust(12)
    print(row_32)
    print(row_16)

    # GPU speedup
    if "cuda" in all_results and "cpu" in all_results:
        print(f"\n{'=' * 90}")
        print("SUMMARY: GPU speedup over CPU (embed time)")
        print(f"{'=' * 90}")
        row = f"{'Speedup':<10}"
        for s in SCALE_POINTS:
            cpu = all_results["cpu"].get(str(s), {}).get("embed_time_s", 0)
            gpu = all_results["cuda"].get(str(s), {}).get("embed_time_s", 0)
            if cpu and gpu:
                row += f"  {cpu/gpu:.1f}x".rjust(12)
        print(row)


if __name__ == "__main__":
    run_benchmark()
