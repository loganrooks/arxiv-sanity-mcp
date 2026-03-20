"""Rebuild W0.1 results JSON from saved embeddings (original run had numpy bool serialization bug)."""
import json
import sqlite3
import time
from pathlib import Path

import numpy as np
import torch

SPIKE_DIR = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/003-strategy-profiling")
DATA_DIR = SPIKE_DIR / "experiments" / "data"
SPIKE002_DATA = SPIKE_DIR.parent / "002-backend-comparison" / "experiments" / "data"
SPIKE001_DATA = SPIKE_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
TOP_K = 10


class NumpyEncoder(json.JSONEncoder):
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


# Load data
adapter_emb = np.load(DATA_DIR / "specter2_adapter_19k.npy")
with open(DATA_DIR / "specter2_adapter_ids.json") as f:
    arxiv_ids = json.load(f)
minilm_emb = np.load(SPIKE002_DATA / "embeddings_19k.npy")

conn = sqlite3.connect(str(SPIKE001_DATA / "spike_001_harvest.db"))
conn.row_factory = sqlite3.Row
papers = [dict(r) for r in conn.execute(
    "SELECT arxiv_id, title, abstract, primary_category "
    "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
).fetchall()]
conn.close()

id_to_paper = {p["arxiv_id"]: p for p in papers}

# Verification data (from terminal output of the original run)
verification = {
    "per_paper": [
        {"arxiv_id": "2010.11450",
         "title": "Optimal Approximation -- Smoothness Tradeoffs for Soft-Max Functions",
         "category": "cs.LG", "base_vs_adapter_cosine": 0.9584, "base_vs_adapter_l2": 0.2885},
        {"arxiv_id": "2511.09555",
         "title": "SpatialActor: Exploring Disentangled Spatial Representations for Robust Robotic",
         "category": "cs.RO", "base_vs_adapter_cosine": 0.9664, "base_vs_adapter_l2": 0.2592},
        {"arxiv_id": "2601.17062",
         "title": "A Computer Vision Pipeline for Iterative Bullet Hole Tracking in Rifle Zeroing",
         "category": "cs.CV", "base_vs_adapter_cosine": 0.9594, "base_vs_adapter_l2": 0.2851},
        {"arxiv_id": "2601.18358",
         "title": "On strong valid inequalities for a class of mixed-integer nonlinear sets with bounds",
         "category": "math.OC", "base_vs_adapter_cosine": 0.9438, "base_vs_adapter_l2": 0.3353},
        {"arxiv_id": "2601.22120",
         "title": "Comparative Assessment of Look-Ahead Economic Dispatch and Ramp Products",
         "category": "eess.SY", "base_vs_adapter_cosine": 0.9601, "base_vs_adapter_l2": 0.2825},
    ],
    "avg_cosine_base_vs_adapter": 0.9576,
    "adapter_changes_outputs": True,
    "cross_paper_delta_mean": -0.0240,
    "cross_paper_delta_std": 0.0179,
}

# Recompute sanity check from saved embeddings
seed_categories = {"cs.AI": None, "math.NA": None, "q-bio.NC": None}
for i, aid in enumerate(arxiv_ids):
    p = id_to_paper.get(aid, {})
    cat = p.get("primary_category", "")
    if cat in seed_categories and seed_categories[cat] is None:
        seed_categories[cat] = i
    if all(v is not None for v in seed_categories.values()):
        break

seed_indices = [v for v in seed_categories.values() if v is not None]

sanity_results = []
for seed_idx in seed_indices:
    seed_id = arxiv_ids[seed_idx]
    seed_paper = id_to_paper.get(seed_id, {})

    minilm_scores = (minilm_emb[seed_idx:seed_idx+1] @ minilm_emb.T).flatten()
    minilm_scores[seed_idx] = -1
    minilm_top = np.argsort(minilm_scores)[-TOP_K:][::-1]
    minilm_top_ids = [arxiv_ids[i] for i in minilm_top]

    adapter_scores = (adapter_emb[seed_idx:seed_idx+1] @ adapter_emb.T).flatten()
    adapter_scores[seed_idx] = -1
    adapter_top = np.argsort(adapter_scores)[-TOP_K:][::-1]
    adapter_top_ids = [arxiv_ids[i] for i in adapter_top]

    shared = set(minilm_top_ids) & set(adapter_top_ids)
    jaccard = len(shared) / len(set(minilm_top_ids) | set(adapter_top_ids))

    def paper_info(aid):
        p = id_to_paper.get(aid, {})
        return {"arxiv_id": aid, "title": p.get("title", "")[:80],
                "category": p.get("primary_category", "")}

    sanity_results.append({
        "seed_id": seed_id,
        "seed_title": seed_paper.get("title", "")[:100],
        "seed_category": seed_paper.get("primary_category", ""),
        "jaccard": round(float(jaccard), 4),
        "shared_count": int(len(shared)),
        "minilm_only": [paper_info(a) for a in minilm_top_ids if a not in adapter_top_ids][:5],
        "adapter_only": [paper_info(a) for a in adapter_top_ids if a not in minilm_top_ids][:5],
        "minilm_top3": [paper_info(a) for a in minilm_top_ids[:3]],
        "adapter_top3": [paper_info(a) for a in adapter_top_ids[:3]],
    })

avg_jaccard = float(np.mean([r["jaccard"] for r in sanity_results]))
avg_shared = float(np.mean([r["shared_count"] for r in sanity_results]))

results = {
    "experiment": "W0.1: SPECTER2 proximity adapter fix",
    "total_time_s": 470.0,
    "adapter_verification": verification,
    "embedding_info": {
        "model": "allenai/specter2_base + specter2_proximity adapter",
        "dim": 768,
        "n_papers": 19252,
        "device": "cuda (GTX 1080 Ti)",
        "batch_size": 64,
        "compute_time_s": 462.9,
        "per_paper_ms": 24.04,
        "memory_bytes": int(adapter_emb.nbytes),
        "memory_mb": round(adapter_emb.nbytes / 1024 / 1024, 1),
        "dtype": "float32",
        "normalized": True,
    },
    "sanity_check": {
        "comparison": "MiniLM-384 vs SPECTER2+adapter-768",
        "top_k": TOP_K,
        "num_seeds": len(sanity_results),
        "avg_jaccard": round(avg_jaccard, 4),
        "avg_shared": round(avg_shared, 1),
        "per_seed": sanity_results,
    },
    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "environment": {
        "conda_env": "ml-dev",
        "torch": torch.__version__,
        "cuda": "True",
        "gpu": "NVIDIA GeForce GTX 1080 Ti",
    },
}

output_path = DATA_DIR / "w0_1_specter2_fix_results.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2, cls=NumpyEncoder)

print(f"Results saved to {output_path}")
print(f"Adapter verification: avg cosine = {verification['avg_cosine_base_vs_adapter']}")
print(f"Sanity check: avg Jaccard = {avg_jaccard:.4f}, avg shared = {avg_shared:.1f}/{TOP_K}")
for s in sanity_results:
    print(f"  [{s['seed_category']}] {s['seed_title'][:50]}  J={s['jaccard']}  shared={s['shared_count']}")
