"""
W0.1: Fix SPECTER2 loading — compute proper embeddings with proximity adapter.

Prior experiments used SentenceTransformer('allenai/specter2_base') which falls
back to mean pooling without the proximity adapter. The correct approach uses the
`adapters` library to load the base model + proximity adapter, producing different
(and presumably better-calibrated) embeddings for paper similarity.

Steps:
  1. Load SPECTER2 base + proximity adapter via `adapters` library
  2. Verify adapter changes outputs (5 papers, base vs adapter)
  3. Compute adapter embeddings for all 19K papers
  4. Sanity check: compare top-10 neighbors for 3 seeds vs MiniLM and base SPECTER2

Requires: conda activate ml-dev (torch 2.2.0+cu118 for GTX 1080 Ti)
"""

import json
import sqlite3
import time
from pathlib import Path

import numpy as np
import torch

# Paths
SPIKE_DIR = Path(__file__).parent.parent
DATA_DIR = SPIKE_DIR / "experiments" / "data"
SPIKE001_DATA = (
    SPIKE_DIR.parent
    / "001-volume-filtering-scoring-landscape"
    / "experiments"
    / "data"
)
SPIKE002_DATA = (
    SPIKE_DIR.parent / "002-backend-comparison" / "experiments" / "data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
MINILM_EMBEDDINGS = SPIKE002_DATA / "embeddings_19k.npy"
MINILM_IDS = SPIKE002_DATA / "arxiv_ids_19k.json"

OUTPUT_EMBEDDINGS = DATA_DIR / "specter2_adapter_19k.npy"
OUTPUT_IDS = DATA_DIR / "specter2_adapter_ids.json"
OUTPUT_RESULTS = DATA_DIR / "w0_1_specter2_fix_results.json"

EMBED_BATCH_SIZE = 64  # Conservative for 11GB VRAM with 768-dim model
TOP_K = 10


class NumpyEncoder(json.JSONEncoder):
    """Handle numpy types in JSON serialization."""

    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def load_papers():
    """Load all papers with abstracts from the corpus."""
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_model_with_adapter():
    """Load SPECTER2 base + proximity adapter using the adapters library."""
    from adapters import AutoAdapterModel
    from transformers import AutoTokenizer

    print("Loading SPECTER2 base model...")
    tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
    model = AutoAdapterModel.from_pretrained("allenai/specter2_base")

    print("Loading proximity adapter...")
    model.load_adapter(
        "allenai/specter2",
        source="hf",
        load_as="specter2_proximity",
        set_active=True,
    )
    print("Adapter loaded and set active")

    model.eval()
    model.to("cuda")
    return tokenizer, model


def load_base_model():
    """Load SPECTER2 base model WITHOUT adapter for comparison."""
    from adapters import AutoAdapterModel
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained("allenai/specter2_base")
    model = AutoAdapterModel.from_pretrained("allenai/specter2_base")
    model.eval()
    model.to("cuda")
    return tokenizer, model


def embed_batch(texts, tokenizer, model, max_length=512):
    """Embed a batch of texts, return CLS token embeddings."""
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=max_length,
    ).to("cuda")
    with torch.no_grad():
        outputs = model(**inputs)
        # CLS token pooling (SPECTER2 convention)
        embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings.cpu().numpy()


def compute_all_embeddings(papers, tokenizer, model, batch_size=EMBED_BATCH_SIZE):
    """Compute embeddings for all papers in batches."""
    # SPECTER2 convention: title [SEP] abstract
    texts = [f"{p['title']} [SEP] {p['abstract']}" for p in papers]
    n = len(texts)

    all_embeddings = []
    t0 = time.perf_counter()

    for i in range(0, n, batch_size):
        batch = texts[i : i + batch_size]
        emb = embed_batch(batch, tokenizer, model)
        all_embeddings.append(emb)

        if (i // batch_size) % 50 == 0:
            elapsed = time.perf_counter() - t0
            done = i + len(batch)
            rate = done / elapsed if elapsed > 0 else 0
            eta = (n - done) / rate if rate > 0 else 0
            print(
                f"  {done:6d}/{n} ({100*done/n:.1f}%) "
                f"| {elapsed:.0f}s elapsed | ~{eta:.0f}s remaining"
            )

    total_time = time.perf_counter() - t0
    embeddings = np.concatenate(all_embeddings, axis=0).astype(np.float32)

    # L2 normalize so dot product = cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.maximum(norms, 1e-10)  # Avoid division by zero
    embeddings = embeddings / norms

    print(f"  Total: {n} papers in {total_time:.1f}s ({total_time/n*1000:.2f}ms/paper)")
    print(f"  Shape: {embeddings.shape}, dtype: {embeddings.dtype}")
    print(f"  Size: {embeddings.nbytes / 1024 / 1024:.1f} MB")

    # Verify normalization
    check_norms = np.linalg.norm(embeddings[:10], axis=1)
    assert np.allclose(check_norms, 1.0, atol=1e-5), f"Normalization failed: {check_norms}"
    print("  Normalization verified (L2 norms = 1.0)")

    return embeddings, total_time


def step1_verify_adapter_effect(papers):
    """Step 1: Verify the adapter actually changes outputs."""
    print("\n" + "=" * 70)
    print("STEP 1: Verify adapter changes outputs")
    print("=" * 70)

    # Pick 5 diverse papers
    sample_indices = np.linspace(0, len(papers) - 1, 5, dtype=int)
    sample_papers = [papers[i] for i in sample_indices]
    sample_texts = [f"{p['title']} [SEP] {p['abstract']}" for p in sample_papers]

    # Base model (no adapter)
    print("\nLoading base model (no adapter)...")
    tokenizer_base, model_base = load_base_model()
    emb_base_raw = embed_batch(sample_texts, tokenizer_base, model_base)
    norms = np.linalg.norm(emb_base_raw, axis=1, keepdims=True)
    emb_base = emb_base_raw / norms
    del model_base
    torch.cuda.empty_cache()

    # Adapter model
    print("Loading adapter model...")
    tokenizer_adp, model_adp = load_model_with_adapter()
    emb_adp_raw = embed_batch(sample_texts, tokenizer_adp, model_adp)
    norms = np.linalg.norm(emb_adp_raw, axis=1, keepdims=True)
    emb_adp = emb_adp_raw / norms

    # Compare
    results = []
    print("\nPer-paper comparison (base vs adapter):")
    print("-" * 70)
    for i, p in enumerate(sample_papers):
        cos_sim = float(np.dot(emb_base[i], emb_adp[i]))
        l2_dist = float(np.linalg.norm(emb_base[i] - emb_adp[i]))
        entry = {
            "arxiv_id": p["arxiv_id"],
            "title": p["title"][:80],
            "category": p["primary_category"],
            "base_vs_adapter_cosine": round(cos_sim, 4),
            "base_vs_adapter_l2": round(l2_dist, 4),
        }
        results.append(entry)
        print(
            f"  [{p['primary_category']:10s}] cosine={cos_sim:.4f}  L2={l2_dist:.4f}  "
            f"{p['title'][:50]}"
        )

    avg_cos = float(np.mean([r["base_vs_adapter_cosine"] for r in results]))
    print(f"\n  Average base-vs-adapter cosine: {avg_cos:.4f}")
    print(f"  Adapter changes embeddings: {'YES' if avg_cos < 0.99 else 'NO (WARNING)'}")

    # Cross-paper similarity comparison
    sim_base = emb_base @ emb_base.T
    sim_adp = emb_adp @ emb_adp.T
    # Extract upper triangle (excluding diagonal)
    mask = np.triu(np.ones_like(sim_base, dtype=bool), k=1)
    delta = sim_adp[mask] - sim_base[mask]
    print(f"\n  Cross-paper similarity delta stats:")
    print(f"    mean={np.mean(delta):.4f}, std={np.std(delta):.4f}")
    print(f"    min={np.min(delta):.4f}, max={np.max(delta):.4f}")

    return {
        "per_paper": results,
        "avg_cosine_base_vs_adapter": round(avg_cos, 4),
        "adapter_changes_outputs": bool(avg_cos < 0.99),
        "cross_paper_delta_mean": round(float(np.mean(delta)), 4),
        "cross_paper_delta_std": round(float(np.std(delta)), 4),
    }, tokenizer_adp, model_adp


def step2_compute_all(papers, tokenizer, model):
    """Step 2: Compute adapter embeddings for all 19K papers."""
    print("\n" + "=" * 70)
    print("STEP 2: Compute adapter embeddings for all 19K papers")
    print("=" * 70)

    arxiv_ids = [p["arxiv_id"] for p in papers]
    embeddings, compute_time = compute_all_embeddings(papers, tokenizer, model)

    # Save
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    np.save(OUTPUT_EMBEDDINGS, embeddings)
    with open(OUTPUT_IDS, "w") as f:
        json.dump(arxiv_ids, f)

    print(f"\n  Saved: {OUTPUT_EMBEDDINGS} ({embeddings.nbytes / 1024 / 1024:.1f} MB)")
    print(f"  Saved: {OUTPUT_IDS}")

    return embeddings, arxiv_ids, {
        "model": "allenai/specter2_base + specter2_proximity adapter",
        "dim": int(embeddings.shape[1]),
        "n_papers": int(embeddings.shape[0]),
        "device": "cuda (GTX 1080 Ti)",
        "batch_size": EMBED_BATCH_SIZE,
        "compute_time_s": round(compute_time, 2),
        "per_paper_ms": round(compute_time / len(papers) * 1000, 3),
        "memory_bytes": int(embeddings.nbytes),
        "memory_mb": round(embeddings.nbytes / 1024 / 1024, 1),
        "dtype": str(embeddings.dtype),
        "normalized": True,
    }


def step3_sanity_check(adapter_emb, arxiv_ids, papers):
    """Step 3: Compare top-10 neighbors across embedding models."""
    print("\n" + "=" * 70)
    print("STEP 3: Sanity check — top-10 neighbor comparison")
    print("=" * 70)

    # Load MiniLM embeddings
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    with open(MINILM_IDS) as f:
        minilm_ids = json.load(f)

    # Verify ID ordering matches
    assert minilm_ids == arxiv_ids, "ID ordering mismatch between MiniLM and adapter!"
    print(f"  ID ordering verified: {len(arxiv_ids)} papers match")

    id_to_paper = {p["arxiv_id"]: p for p in papers}

    # Pick 3 seed papers from different domains
    seed_categories = {"cs.AI": None, "math.NA": None, "q-bio.NC": None}
    for i, aid in enumerate(arxiv_ids):
        p = id_to_paper.get(aid, {})
        cat = p.get("primary_category", "")
        if cat in seed_categories and seed_categories[cat] is None:
            seed_categories[cat] = i
        if all(v is not None for v in seed_categories.values()):
            break

    # Fallback: just use evenly spaced if categories not found
    seed_indices = [v for v in seed_categories.values() if v is not None]
    if len(seed_indices) < 3:
        seed_indices = list(np.linspace(0, len(arxiv_ids) - 1, 3, dtype=int))

    results = []
    for seed_idx in seed_indices:
        seed_id = arxiv_ids[seed_idx]
        seed_paper = id_to_paper.get(seed_id, {})

        # MiniLM top-10
        minilm_scores = minilm_emb[seed_idx : seed_idx + 1] @ minilm_emb.T
        minilm_scores = minilm_scores.flatten()
        minilm_scores[seed_idx] = -1  # exclude self
        minilm_top = np.argsort(minilm_scores)[-TOP_K:][::-1]
        minilm_top_ids = [arxiv_ids[i] for i in minilm_top]

        # Adapter top-10
        adapter_scores = adapter_emb[seed_idx : seed_idx + 1] @ adapter_emb.T
        adapter_scores = adapter_scores.flatten()
        adapter_scores[seed_idx] = -1
        adapter_top = np.argsort(adapter_scores)[-TOP_K:][::-1]
        adapter_top_ids = [arxiv_ids[i] for i in adapter_top]

        # Overlap metrics
        shared = set(minilm_top_ids) & set(adapter_top_ids)
        jaccard = len(shared) / len(set(minilm_top_ids) | set(adapter_top_ids))

        def paper_info(aid):
            p = id_to_paper.get(aid, {})
            return {
                "arxiv_id": aid,
                "title": p.get("title", "")[:80],
                "category": p.get("primary_category", ""),
            }

        entry = {
            "seed_id": seed_id,
            "seed_title": seed_paper.get("title", "")[:100],
            "seed_category": seed_paper.get("primary_category", ""),
            "jaccard": round(float(jaccard), 4),
            "shared_count": int(len(shared)),
            "minilm_only": [paper_info(a) for a in minilm_top_ids if a not in adapter_top_ids][:5],
            "adapter_only": [paper_info(a) for a in adapter_top_ids if a not in minilm_top_ids][:5],
            "minilm_top3": [paper_info(a) for a in minilm_top_ids[:3]],
            "adapter_top3": [paper_info(a) for a in adapter_top_ids[:3]],
        }
        results.append(entry)

        print(f"\n  Seed: [{seed_paper.get('primary_category', '?')}] "
              f"{seed_paper.get('title', '?')[:60]}")
        print(f"    Jaccard: {jaccard:.3f}  shared: {len(shared)}/{TOP_K}")
        print(f"    MiniLM top-3:")
        for a in minilm_top_ids[:3]:
            p = id_to_paper.get(a, {})
            print(f"      [{p.get('primary_category', '?'):10s}] {p.get('title', '?')[:60]}")
        print(f"    Adapter top-3:")
        for a in adapter_top_ids[:3]:
            p = id_to_paper.get(a, {})
            print(f"      [{p.get('primary_category', '?'):10s}] {p.get('title', '?')[:60]}")

    avg_jaccard = float(np.mean([r["jaccard"] for r in results]))
    avg_shared = float(np.mean([r["shared_count"] for r in results]))

    print(f"\n  Average Jaccard (MiniLM vs Adapter): {avg_jaccard:.4f}")
    print(f"  Average shared papers: {avg_shared:.1f}/{TOP_K}")

    return {
        "comparison": "MiniLM-384 vs SPECTER2+adapter-768",
        "top_k": TOP_K,
        "num_seeds": len(results),
        "avg_jaccard": round(avg_jaccard, 4),
        "avg_shared": round(avg_shared, 1),
        "per_seed": results,
    }


def main():
    print("=" * 70)
    print("W0.1: SPECTER2 Proximity Adapter Embeddings")
    print("=" * 70)

    t_start = time.perf_counter()

    # Load corpus
    papers = load_papers()
    print(f"Loaded {len(papers)} papers from corpus")

    # Step 1: Verify adapter effect
    verification, tokenizer, model = step1_verify_adapter_effect(papers)

    # Step 2: Compute all embeddings (reuse the already-loaded adapter model)
    embeddings, arxiv_ids, embedding_info = step2_compute_all(papers, tokenizer, model)

    # Free GPU memory
    del model
    torch.cuda.empty_cache()

    # Step 3: Sanity check
    sanity_check = step3_sanity_check(embeddings, arxiv_ids, papers)

    # Save results
    total_time = time.perf_counter() - t_start
    results = {
        "experiment": "W0.1: SPECTER2 proximity adapter fix",
        "total_time_s": round(total_time, 1),
        "adapter_verification": verification,
        "embedding_info": embedding_info,
        "sanity_check": sanity_check,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "environment": {
            "conda_env": "ml-dev",
            "torch": torch.__version__,
            "cuda": str(torch.cuda.is_available()),
            "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
        },
    }

    with open(OUTPUT_RESULTS, "w") as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    print(f"\nResults saved to {OUTPUT_RESULTS}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Adapter changes outputs: {verification['adapter_changes_outputs']}")
    print(f"  Base-vs-adapter avg cosine: {verification['avg_cosine_base_vs_adapter']:.4f}")
    print(f"  Embeddings computed: {embedding_info['n_papers']}")
    print(f"  Compute time: {embedding_info['compute_time_s']:.1f}s "
          f"({embedding_info['per_paper_ms']:.2f}ms/paper)")
    print(f"  MiniLM-vs-adapter avg Jaccard: {sanity_check['avg_jaccard']:.4f}")
    print(f"  Total experiment time: {total_time:.0f}s")
    print("=" * 70)


if __name__ == "__main__":
    main()
