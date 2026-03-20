"""
W1 Qualitative Review: Generate top-20 recommendations for each strategy x profile combination.

Strategies:
  S1a - MiniLM centroid similarity
  S1c - SPECTER2 adapter centroid similarity
  S1d - TF-IDF centroid cosine similarity

Profiles (subset_10):
  P1 - RL for robotics (Medium breadth)
  P3 - Quantum computing / quantum ML (Narrow)
  P4 - AI safety / alignment (Broad)

Output: JSON with recommendations + paper details for each of the 9 combinations.
"""

import json
import numpy as np
import sqlite3
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp")
SPIKE_003 = BASE / ".planning/spikes/003-strategy-profiling"
SPIKE_002 = BASE / ".planning/spikes/002-backend-comparison"
SPIKE_001 = BASE / ".planning/spikes/001-volume-filtering-scoring-landscape"

# Load data
print("Loading embeddings...")
miniLM_emb = np.load(SPIKE_002 / "experiments/data/embeddings_19k.npy")
specter2_emb = np.load(SPIKE_003 / "experiments/data/specter2_adapter_19k.npy")

print(f"  MiniLM: {miniLM_emb.shape}")
print(f"  SPECTER2: {specter2_emb.shape}")

with open(SPIKE_002 / "experiments/data/arxiv_ids_19k.json") as f:
    miniLM_ids = json.load(f)

with open(SPIKE_003 / "experiments/data/specter2_adapter_ids.json") as f:
    specter2_ids = json.load(f)

# Verify IDs match
assert miniLM_ids == specter2_ids, "ID orderings differ between embedding files!"
all_ids = miniLM_ids
id_to_idx = {aid: i for i, aid in enumerate(all_ids)}

print(f"  {len(all_ids)} papers indexed")

# Load interest profiles
with open(SPIKE_003 / "experiments/data/interest_profiles.json") as f:
    profiles_data = json.load(f)

# Load paper details from harvest DB
print("Loading paper details from harvest DB...")
db = sqlite3.connect(str(SPIKE_001 / "experiments/data/spike_001_harvest.db"))
db.row_factory = sqlite3.Row

paper_details = {}
for row in db.execute("SELECT arxiv_id, title, abstract, categories, primary_category, authors_text FROM papers"):
    paper_details[row["arxiv_id"]] = {
        "arxiv_id": row["arxiv_id"],
        "title": row["title"],
        "abstract": row["abstract"],
        "categories": row["categories"],
        "primary_category": row["primary_category"],
        "authors": row["authors_text"][:200] if row["authors_text"] else ""
    }
db.close()
print(f"  {len(paper_details)} papers loaded")

# Build TF-IDF matrix
print("Building TF-IDF matrix...")
texts = []
for aid in all_ids:
    p = paper_details.get(aid, {})
    title = p.get("title", "")
    abstract = p.get("abstract", "")
    texts.append(f"{title} {abstract}")

tfidf = TfidfVectorizer(max_features=50000, stop_words="english", sublinear_tf=True)
tfidf_matrix = tfidf.fit_transform(texts)
print(f"  TF-IDF matrix: {tfidf_matrix.shape}")

# Profile configs
profile_ids = ["P1", "P3", "P4"]
strategies = ["S1a", "S1c", "S1d"]

results = {}

for pid in profile_ids:
    profile = profiles_data["profiles"][pid]
    seed_ids = profile["seed_subsets"]["subset_10"]
    held_out_ids = [h["arxiv_id"] for h in profile["held_out_papers"]]
    all_profile_ids = set(seed_ids) | set(held_out_ids) | set(sp["arxiv_id"] for sp in profile["seed_papers"])

    print(f"\n{'='*60}")
    print(f"Profile {pid}: {profile['name']} ({profile['breadth']})")
    print(f"  Seeds (subset_10): {len(seed_ids)}")

    # Get seed indices
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    missing = [sid for sid in seed_ids if sid not in id_to_idx]
    if missing:
        print(f"  WARNING: {len(missing)} seed IDs not in embedding index: {missing}")

    for strategy in strategies:
        print(f"\n  Strategy {strategy}:")

        if strategy == "S1a":
            # MiniLM centroid
            seed_embs = miniLM_emb[seed_indices]
            centroid = seed_embs.mean(axis=0)
            # Dot product similarity (embeddings are normalized for MiniLM)
            scores = miniLM_emb @ centroid

        elif strategy == "S1c":
            # SPECTER2 adapter centroid
            seed_embs = specter2_emb[seed_indices]
            centroid = seed_embs.mean(axis=0)
            # Normalize centroid and compute cosine similarity
            centroid_norm = centroid / (np.linalg.norm(centroid) + 1e-10)
            norms = np.linalg.norm(specter2_emb, axis=1, keepdims=True) + 1e-10
            scores = (specter2_emb / norms) @ centroid_norm

        elif strategy == "S1d":
            # TF-IDF centroid cosine similarity
            seed_vecs = tfidf_matrix[seed_indices]
            centroid_sparse = seed_vecs.mean(axis=0)
            # Convert sparse matrix result to proper format for cosine_similarity
            centroid_arr = np.asarray(centroid_sparse)
            if centroid_arr.ndim == 1:
                centroid_arr = centroid_arr.reshape(1, -1)
            scores = cosine_similarity(tfidf_matrix, centroid_arr).flatten()

        # Rank all papers, exclude seeds
        ranked_indices = np.argsort(-scores)

        top_20 = []
        for idx in ranked_indices:
            aid = all_ids[idx]
            if aid in seed_ids:
                continue
            if len(top_20) >= 20:
                break

            detail = paper_details.get(aid, {})
            is_held_out = aid in held_out_ids
            is_any_profile = aid in all_profile_ids

            top_20.append({
                "rank": len(top_20) + 1,
                "arxiv_id": aid,
                "score": float(scores[idx]),
                "title": detail.get("title", "UNKNOWN"),
                "abstract": detail.get("abstract", ""),
                "categories": detail.get("categories", ""),
                "primary_category": detail.get("primary_category", ""),
                "authors": detail.get("authors", ""),
                "is_held_out": is_held_out,
                "is_profile_paper": is_any_profile
            })

        held_out_found = sum(1 for r in top_20 if r["is_held_out"])
        profile_found = sum(1 for r in top_20 if r["is_profile_paper"])

        print(f"    Top score: {top_20[0]['score']:.4f}")
        print(f"    Score range: {top_20[0]['score']:.4f} - {top_20[-1]['score']:.4f}")
        print(f"    Held-out papers in top-20: {held_out_found}/{len(held_out_ids)}")
        print(f"    Profile papers in top-20: {profile_found}")

        # Also get seed paper details
        seed_details = []
        for sid in seed_ids:
            d = paper_details.get(sid, {})
            seed_details.append({
                "arxiv_id": sid,
                "title": d.get("title", "UNKNOWN"),
                "abstract": d.get("abstract", ""),
                "categories": d.get("categories", ""),
                "primary_category": d.get("primary_category", ""),
            })

        key = f"{strategy}_{pid}"
        results[key] = {
            "strategy": strategy,
            "profile_id": pid,
            "profile_name": profile["name"],
            "profile_breadth": profile["breadth"],
            "seed_papers": seed_details,
            "recommendations": top_20,
            "stats": {
                "top_score": float(top_20[0]["score"]),
                "bottom_score": float(top_20[-1]["score"]),
                "score_range": float(top_20[0]["score"] - top_20[-1]["score"]),
                "held_out_found": held_out_found,
                "held_out_total": len(held_out_ids),
                "profile_papers_found": profile_found
            }
        }

# Save results
output_path = SPIKE_003 / "experiments/data/w1_review_recommendations.json"
with open(output_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"\n\nSaved to {output_path}")
print(f"Total combinations: {len(results)}")
