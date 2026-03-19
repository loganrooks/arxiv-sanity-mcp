"""
QV3: MiniLM vs SPECTER2 embedding quality for academic abstracts.

Compares:
1. Top-10 similarity overlap for seed papers
2. Qualitative inspection of results
3. Compute time per paper
4. Memory footprint
5. Brute-force search latency (384-dim vs 768-dim)

Usage:
    python qv3_specter2_comparison.py
"""

import json
import sqlite3
import time
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
MINILM_EMBEDDINGS = DATA_DIR / "embeddings_19k.npy"
MINILM_IDS = DATA_DIR / "arxiv_ids_19k.json"
RESULTS_PATH = DATA_DIR / "qv3_specter2_results.json"

EMBED_BATCH_SIZE = 128
NUM_SEED_PAPERS = 10
TOP_K = 10
SEARCH_RUNS = 20


def load_papers():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def compute_specter2_embeddings(papers):
    """Compute SPECTER2 embeddings on GPU."""
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Device: {device}")

    # SPECTER2 expects title + SEP + abstract format
    model = SentenceTransformer("allenai/specter2_base", device=device)
    dim = model.get_sentence_embedding_dimension()
    print(f"  Model: allenai/specter2_base, dim={dim}")

    # SPECTER2 convention: title [SEP] abstract
    texts = [f"{p['title']} [SEP] {p['abstract']}" for p in papers]

    t0 = time.perf_counter()
    embeddings = model.encode(
        texts,
        batch_size=EMBED_BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    compute_time = time.perf_counter() - t0

    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)

    print(f"  Computed {len(embeddings)} embeddings in {compute_time:.1f}s")
    print(f"  Shape: {embeddings.shape}, size: {embeddings.nbytes / 1024 / 1024:.1f} MB")
    print(f"  Per paper: {compute_time / len(papers) * 1000:.2f}ms")

    del model
    if device == "cuda":
        import torch
        torch.cuda.empty_cache()

    return embeddings, {
        "model": "allenai/specter2_base",
        "dim": dim,
        "device": device,
        "compute_time_s": round(compute_time, 2),
        "per_paper_ms": round(compute_time / len(papers) * 1000, 3),
        "memory_bytes": embeddings.nbytes,
        "memory_mb": round(embeddings.nbytes / 1024 / 1024, 1),
    }


def compare_similarity(
    minilm_emb, specter_emb, arxiv_ids, papers, seed_indices
):
    """Compare top-K similar papers for seed papers across both models."""
    id_to_paper = {p["arxiv_id"]: p for p in papers}
    results = []

    for seed_idx in seed_indices:
        seed_id = arxiv_ids[seed_idx]
        seed_paper = id_to_paper.get(seed_id, {})

        # MiniLM similarity
        minilm_scores = minilm_emb[seed_idx:seed_idx+1] @ minilm_emb.T
        minilm_top = np.argsort(minilm_scores.flatten())[-TOP_K-1:-1][::-1]  # Exclude self
        minilm_ids = [arxiv_ids[i] for i in minilm_top]

        # SPECTER2 similarity
        specter_scores = specter_emb[seed_idx:seed_idx+1] @ specter_emb.T
        specter_top = np.argsort(specter_scores.flatten())[-TOP_K-1:-1][::-1]
        specter_ids = [arxiv_ids[i] for i in specter_top]

        # Overlap
        shared = set(minilm_ids) & set(specter_ids)
        jaccard = len(shared) / len(set(minilm_ids) | set(specter_ids)) if minilm_ids else 0

        # Paper details for inspection
        def paper_info(aid):
            p = id_to_paper.get(aid, {})
            return {
                "arxiv_id": aid,
                "title": p.get("title", "")[:100],
                "category": p.get("primary_category", ""),
            }

        minilm_only = [paper_info(aid) for aid in minilm_ids if aid not in specter_ids][:3]
        specter_only = [paper_info(aid) for aid in specter_ids if aid not in minilm_ids][:3]

        entry = {
            "seed_id": seed_id,
            "seed_title": seed_paper.get("title", "")[:100],
            "seed_category": seed_paper.get("primary_category", ""),
            "jaccard": round(jaccard, 4),
            "shared_count": len(shared),
            "minilm_only_sample": minilm_only,
            "specter_only_sample": specter_only,
        }
        results.append(entry)

        print(f"  Seed: [{seed_paper.get('primary_category', '?')}] "
              f"{seed_paper.get('title', '?')[:60]}")
        print(f"    Jaccard: {jaccard:.3f}  shared: {len(shared)}/{TOP_K}")

    avg_jaccard = np.mean([r["jaccard"] for r in results])
    return results, round(float(avg_jaccard), 4)


def bench_search_latency(embeddings, label):
    """Benchmark brute-force search latency."""
    query = embeddings[0:1]
    # Warmup
    for _ in range(3):
        query @ embeddings.T

    latencies = []
    for _ in range(SEARCH_RUNS):
        t0 = time.perf_counter()
        scores = query @ embeddings.T
        top_idx = np.argpartition(scores.flatten(), -TOP_K)[-TOP_K:]
        latencies.append((time.perf_counter() - t0) * 1000)

    return {
        "label": label,
        "dim": embeddings.shape[1],
        "n_papers": embeddings.shape[0],
        "p50_ms": round(float(np.median(latencies)), 3),
        "p95_ms": round(float(np.percentile(latencies, 95)), 3),
    }


def main():
    print("=" * 80)
    print("QV3: MiniLM vs SPECTER2 Embedding Quality")
    print("=" * 80)

    papers = load_papers()
    print(f"Loaded {len(papers)} papers")

    # Load MiniLM embeddings
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    with open(MINILM_IDS) as f:
        arxiv_ids = json.load(f)
    print(f"MiniLM: {minilm_emb.shape}, {minilm_emb.nbytes / 1024 / 1024:.1f} MB")

    # Compute SPECTER2 embeddings
    print("\nComputing SPECTER2 embeddings...")
    specter_emb, specter_info = compute_specter2_embeddings(papers)

    # Pick seed papers (evenly spaced, diverse categories)
    seed_indices = np.linspace(0, len(arxiv_ids) - 1, NUM_SEED_PAPERS, dtype=int)
    print(f"\nComparing top-{TOP_K} similarity for {NUM_SEED_PAPERS} seed papers:")
    print("-" * 70)

    similarity_results, avg_jaccard = compare_similarity(
        minilm_emb, specter_emb, arxiv_ids, papers, seed_indices
    )

    print(f"\nAverage Jaccard (MiniLM vs SPECTER2 top-{TOP_K}): {avg_jaccard:.4f}")

    # Search latency comparison
    print("\nSearch latency comparison (brute-force, 19K papers):")
    minilm_latency = bench_search_latency(minilm_emb, "MiniLM-384")
    specter_latency = bench_search_latency(specter_emb, "SPECTER2-768")
    print(f"  MiniLM  (384-dim): p50={minilm_latency['p50_ms']:.2f}ms")
    print(f"  SPECTER2 (768-dim): p50={specter_latency['p50_ms']:.2f}ms")
    print(f"  Ratio: {specter_latency['p50_ms'] / minilm_latency['p50_ms']:.1f}x")

    # Memory comparison
    print("\nMemory comparison at 19K and extrapolated 215K:")
    for label, dim, actual in [("MiniLM", 384, minilm_emb.nbytes),
                                ("SPECTER2", 768, specter_emb.nbytes)]:
        at_215k = 215000 * dim * 4
        print(f"  {label:10s}: {actual / 1024 / 1024:.1f} MB (19K), "
              f"~{at_215k / 1024 / 1024:.0f} MB (215K)")

    # Compute cost comparison
    minilm_info = {
        "model": "all-MiniLM-L6-v2",
        "dim": 384,
        # From Spike 001 A1c.3
        "per_paper_ms_gpu": 1.7,
        "per_paper_ms_cpu": 35,
    }

    results = {
        "minilm": minilm_info,
        "specter2": specter_info,
        "similarity_comparison": {
            "num_seeds": NUM_SEED_PAPERS,
            "top_k": TOP_K,
            "avg_jaccard": avg_jaccard,
            "per_seed": similarity_results,
        },
        "search_latency": {
            "minilm": minilm_latency,
            "specter2": specter_latency,
        },
        "memory_at_215k": {
            "minilm_mb": round(215000 * 384 * 4 / 1024 / 1024, 0),
            "specter2_mb": round(215000 * 768 * 4 / 1024 / 1024, 0),
        },
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    # Verdict
    print(f"\n{'=' * 80}")
    if avg_jaccard > 0.6:
        print(f"VERDICT: Models agree well (Jaccard {avg_jaccard:.3f}). "
              "MiniLM may be sufficient — SPECTER2 finds similar papers.")
    elif avg_jaccard > 0.3:
        print(f"VERDICT: Models moderately agree (Jaccard {avg_jaccard:.3f}). "
              "SPECTER2 finds meaningfully different papers. Worth considering.")
    else:
        print(f"VERDICT: Models strongly disagree (Jaccard {avg_jaccard:.3f}). "
              "SPECTER2 captures different similarity — domain-specific value.")
    print(f"Cost: SPECTER2 is {specter_info['per_paper_ms']:.1f}ms/paper GPU "
          f"vs MiniLM {minilm_info['per_paper_ms_gpu']}ms/paper ("
          f"{specter_info['per_paper_ms'] / minilm_info['per_paper_ms_gpu']:.1f}x slower)")
    print(f"Memory: SPECTER2 is 2x larger ({specter_emb.nbytes / 1024 / 1024:.0f} MB vs "
          f"{minilm_emb.nbytes / 1024 / 1024:.0f} MB at 19K)")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
