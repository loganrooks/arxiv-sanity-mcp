"""Generate qualitative review input files for missing review checkpoints.

Produces JSON files with full paper data (title, abstract, categories) for:
- W3: Best RRF combination vs standalone MiniLM (P1, P4, P8)
- W4.1: Cold start at 1 and 3 seeds (MiniLM and TF-IDF, P1, P3, P4)
- W5.4: Parallel views presentation (MiniLM + TF-IDF + SPECTER2, P1, P3, P4)
- Extensions: kNN/MMR vs centroid (from existing retrieved_ids)
"""

import json
import sqlite3
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = Path(".planning/spikes/003-strategy-profiling/experiments")
DATA = BASE / "data"
DB_PATH = Path(".planning/spikes/001-volume-filtering-scoring-landscape/experiments/data/spike_001_harvest.db")

# Output directory
REVIEW_INPUTS = BASE / "review_inputs"
REVIEW_INPUTS.mkdir(exist_ok=True)


def load_corpus():
    """Load all papers from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT arxiv_id, title, abstract, categories, primary_category FROM papers")
    papers = {row["arxiv_id"]: dict(row) for row in c.fetchall()}
    conn.close()
    return papers


def load_embeddings():
    """Load MiniLM and SPECTER2 embeddings with ID mapping."""
    with open(DATA / "specter2_adapter_ids.json") as f:
        ids = json.load(f)

    minilm = np.load(Path(".planning/spikes/002-backend-comparison/experiments/data/embeddings_19k.npy"))
    specter2 = np.load(DATA / "specter2_adapter_19k.npy")

    id_to_idx = {aid: i for i, aid in enumerate(ids)}
    return ids, id_to_idx, minilm, specter2


def load_profiles():
    """Load interest profiles."""
    with open(DATA / "interest_profiles.json") as f:
        data = json.load(f)
    return data["profiles"]


def build_tfidf(corpus_papers, ids):
    """Build TF-IDF matrix aligned with embedding IDs."""
    texts = []
    for aid in ids:
        p = corpus_papers.get(aid, {})
        abstract = p.get("abstract", "") or ""
        title = p.get("title", "") or ""
        texts.append(f"{title} {abstract}")

    vectorizer = TfidfVectorizer(max_features=20000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)
    return tfidf_matrix


def get_paper_details(paper_ids, corpus):
    """Look up full paper details for a list of IDs."""
    return [
        {
            "arxiv_id": pid,
            "title": corpus.get(pid, {}).get("title", "UNKNOWN"),
            "abstract": corpus.get(pid, {}).get("abstract", "UNKNOWN"),
            "categories": corpus.get(pid, {}).get("categories", ""),
            "primary_category": corpus.get(pid, {}).get("primary_category", ""),
        }
        for pid in paper_ids
    ]


def recommend_centroid(seed_ids, embeddings, id_to_idx, all_ids, top_k=20):
    """Centroid-based recommendation using embeddings."""
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        return []

    seed_embs = embeddings[seed_indices]
    centroid = seed_embs.mean(axis=0, keepdims=True)

    # Normalize
    centroid_norm = centroid / (np.linalg.norm(centroid) + 1e-10)
    emb_norms = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-10)

    scores = (emb_norms @ centroid_norm.T).flatten()

    # Exclude seeds
    seed_set = set(seed_indices)
    ranked = []
    for idx in np.argsort(scores)[::-1]:
        if idx not in seed_set:
            ranked.append((all_ids[idx], float(scores[idx])))
        if len(ranked) >= top_k:
            break

    return ranked


def recommend_tfidf(seed_ids, tfidf_matrix, id_to_idx, all_ids, top_k=20):
    """TF-IDF centroid-based recommendation."""
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        return []

    seed_vecs = tfidf_matrix[seed_indices]
    centroid = np.asarray(seed_vecs.mean(axis=0))

    scores = cosine_similarity(centroid, tfidf_matrix).flatten()

    seed_set = set(seed_indices)
    ranked = []
    for idx in np.argsort(scores)[::-1]:
        if idx not in seed_set:
            ranked.append((all_ids[idx], float(scores[idx])))
        if len(ranked) >= top_k:
            break

    return ranked


def recommend_rrf(rankings_list, k=60, top_k=20):
    """Reciprocal Rank Fusion across multiple rankings."""
    scores = {}
    for ranking in rankings_list:
        for rank, (pid, _score) in enumerate(ranking):
            scores[pid] = scores.get(pid, 0) + 1.0 / (k + rank + 1)

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [(pid, score) for pid, score in sorted_scores[:top_k]]


def get_profile_seeds(profile, subset_key="subset_5"):
    """Get seed paper IDs from a profile."""
    subsets = profile.get("seed_subsets", {})
    if subset_key in subsets:
        return subsets[subset_key]
    # Fallback to first N seed papers
    papers = profile.get("seed_papers", [])
    n = int(subset_key.split("_")[1]) if "_" in subset_key else 5
    return [p["arxiv_id"] for p in papers[:n]]


def generate_w3_reviews(corpus, ids, id_to_idx, minilm, specter2, tfidf_matrix, profiles):
    """W3: Blind pairwise — best individual (MiniLM) vs best RRF combination."""
    print("Generating W3 review inputs...")

    review_profiles = ["P1", "P4", "P8"]
    results = {}

    for pid in review_profiles:
        profile = profiles[pid]
        seed_ids = get_profile_seeds(profile)

        # Strategy A: MiniLM standalone
        minilm_recs = recommend_centroid(seed_ids, minilm, id_to_idx, ids, top_k=20)

        # Strategy B: Best RRF combination (MiniLM + TF-IDF, k=60)
        tfidf_recs = recommend_tfidf(seed_ids, tfidf_matrix, id_to_idx, ids, top_k=100)
        rrf_recs = recommend_rrf([minilm_recs[:100] if len(minilm_recs) < 100
                                  else recommend_centroid(seed_ids, minilm, id_to_idx, ids, top_k=100),
                                  tfidf_recs], k=60, top_k=20)

        # Get full 100 from MiniLM for RRF
        minilm_100 = recommend_centroid(seed_ids, minilm, id_to_idx, ids, top_k=100)
        rrf_recs = recommend_rrf([minilm_100, tfidf_recs], k=60, top_k=20)

        # Consensus analysis
        minilm_set = {pid for pid, _ in minilm_recs}
        rrf_set = {pid for pid, _ in rrf_recs}
        consensus = minilm_set & rrf_set
        a_only = minilm_set - rrf_set
        b_only = rrf_set - minilm_set

        results[pid] = {
            "profile_id": pid,
            "profile_name": profile["name"],
            "profile_breadth": profile.get("breadth", "unknown"),
            "seed_papers": get_paper_details(seed_ids, corpus),
            "strategy_a": {
                "label": "Strategy A",  # blind
                "papers": get_paper_details([p for p, _ in minilm_recs], corpus),
                "scores": {p: s for p, s in minilm_recs},
            },
            "strategy_b": {
                "label": "Strategy B",  # blind
                "papers": get_paper_details([p for p, _ in rrf_recs], corpus),
                "scores": {p: s for p, s in rrf_recs},
            },
            "consensus_ids": list(consensus),
            "a_only_ids": list(a_only),
            "b_only_ids": list(b_only),
        }

    with open(REVIEW_INPUTS / "w3_blind_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved W3 review input: {len(results)} profiles")


def generate_w4_1_reviews(corpus, ids, id_to_idx, minilm, tfidf_matrix, profiles):
    """W4.1: Cold start at seed count = 1 and 3."""
    print("Generating W4.1 review inputs...")

    review_profiles = ["P1", "P3", "P4"]
    seed_counts = [1, 3]
    results = {}

    for pid in review_profiles:
        profile = profiles[pid]
        all_seeds = get_profile_seeds(profile, "subset_10")
        if len(all_seeds) < 3:
            all_seeds = get_profile_seeds(profile)

        results[pid] = {
            "profile_id": pid,
            "profile_name": profile["name"],
            "profile_breadth": profile.get("breadth", "unknown"),
        }

        for n_seeds in seed_counts:
            seeds = all_seeds[:n_seeds]

            minilm_recs = recommend_centroid(seeds, minilm, id_to_idx, ids, top_k=20)
            tfidf_recs = recommend_tfidf(seeds, tfidf_matrix, id_to_idx, ids, top_k=20)

            results[pid][f"seeds_{n_seeds}"] = {
                "seed_papers": get_paper_details(seeds, corpus),
                "n_seeds": n_seeds,
                "minilm": {
                    "papers": get_paper_details([p for p, _ in minilm_recs], corpus),
                    "scores": {p: s for p, s in minilm_recs},
                },
                "tfidf": {
                    "papers": get_paper_details([p for p, _ in tfidf_recs], corpus),
                    "scores": {p: s for p, s in tfidf_recs},
                },
            }

    with open(REVIEW_INPUTS / "w4_1_cold_start.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved W4.1 review input: {len(results)} profiles x {len(seed_counts)} seed counts")


def generate_w5_4_reviews(corpus, ids, id_to_idx, minilm, specter2, tfidf_matrix, profiles):
    """W5.4: Parallel views presentation — all 3 strategies side by side."""
    print("Generating W5.4 review inputs...")

    review_profiles = ["P1", "P3", "P4"]
    results = {}

    for pid in review_profiles:
        profile = profiles[pid]
        seed_ids = get_profile_seeds(profile)

        minilm_recs = recommend_centroid(seed_ids, minilm, id_to_idx, ids, top_k=20)
        specter2_recs = recommend_centroid(seed_ids, specter2, id_to_idx, ids, top_k=20)
        tfidf_recs = recommend_tfidf(seed_ids, tfidf_matrix, id_to_idx, ids, top_k=20)

        # Overlap analysis
        sets = {
            "minilm": {p for p, _ in minilm_recs},
            "specter2": {p for p, _ in specter2_recs},
            "tfidf": {p for p, _ in tfidf_recs},
        }
        all_three = sets["minilm"] & sets["specter2"] & sets["tfidf"]
        any_two = (
            (sets["minilm"] & sets["specter2"])
            | (sets["minilm"] & sets["tfidf"])
            | (sets["specter2"] & sets["tfidf"])
        ) - all_three

        results[pid] = {
            "profile_id": pid,
            "profile_name": profile["name"],
            "profile_breadth": profile.get("breadth", "unknown"),
            "seed_papers": get_paper_details(seed_ids, corpus),
            "views": {
                "semantic_precision": {
                    "label": "Similar Ideas (MiniLM)",
                    "papers": get_paper_details([p for p, _ in minilm_recs], corpus),
                    "scores": {p: s for p, s in minilm_recs},
                },
                "keyword_precision": {
                    "label": "Same Vocabulary (TF-IDF)",
                    "papers": get_paper_details([p for p, _ in tfidf_recs], corpus),
                    "scores": {p: s for p, s in tfidf_recs},
                },
                "cross_community": {
                    "label": "Adjacent Communities (SPECTER2)",
                    "papers": get_paper_details([p for p, _ in specter2_recs], corpus),
                    "scores": {p: s for p, s in specter2_recs},
                },
            },
            "overlap": {
                "all_three": list(all_three),
                "any_two": list(any_two),
                "unique_per_view": {
                    "minilm": list(sets["minilm"] - sets["specter2"] - sets["tfidf"]),
                    "specter2": list(sets["specter2"] - sets["minilm"] - sets["tfidf"]),
                    "tfidf": list(sets["tfidf"] - sets["minilm"] - sets["specter2"]),
                },
            },
        }

    with open(REVIEW_INPUTS / "w5_4_parallel_views.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved W5.4 review input: {len(results)} profiles")


def generate_extension_reviews(corpus, ids, id_to_idx, minilm, profiles):
    """Extensions: kNN/MMR vs centroid — look up paper details for existing results."""
    print("Generating extension review inputs...")

    with open(DATA / "w5b_knn_mmr_results.json") as f:
        knn_results = json.load(f)

    # Pick 3 representative configs: P1/5seeds, P3/5seeds, P4/5seeds
    review_configs = []
    for cfg in knn_results["per_config_results"]:
        if cfg["n_seeds"] == 5 and cfg["profile_id"] in ("P1", "P3", "P4"):
            review_configs.append(cfg)

    results = {}
    for cfg in review_configs:
        pid = cfg["profile_id"]
        profile = profiles[pid]
        seed_ids = get_profile_seeds(profile)

        strategies = {}
        for strat_name in ["centroid", "knn_per_seed", "mmr"]:
            strat = cfg["strategies"][strat_name]
            paper_ids = strat["retrieved_ids"]
            strategies[strat_name] = {
                "papers": get_paper_details(paper_ids, corpus),
            }

        # Overlap
        sets = {s: set(cfg["strategies"][s]["retrieved_ids"]) for s in ["centroid", "knn_per_seed", "mmr"]}

        results[pid] = {
            "profile_id": pid,
            "profile_name": profile["name"],
            "profile_breadth": profile.get("breadth", "unknown"),
            "seed_papers": get_paper_details(seed_ids, corpus),
            "strategies": strategies,
            "overlap": {
                "centroid_knn": len(sets["centroid"] & sets["knn_per_seed"]),
                "centroid_mmr": len(sets["centroid"] & sets["mmr"]),
                "knn_mmr": len(sets["knn_per_seed"] & sets["mmr"]),
            },
        }

    with open(REVIEW_INPUTS / "ext_knn_mmr.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"  Saved extension review input: {len(results)} profiles")


def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"  {len(corpus)} papers")

    print("Loading embeddings...")
    ids, id_to_idx, minilm, specter2 = load_embeddings()
    print(f"  {len(ids)} embeddings, MiniLM {minilm.shape}, SPECTER2 {specter2.shape}")

    print("Loading profiles...")
    profiles = load_profiles()
    print(f"  {len(profiles)} profiles")

    print("Building TF-IDF matrix...")
    tfidf_matrix = build_tfidf(corpus, ids)
    print(f"  TF-IDF shape: {tfidf_matrix.shape}")

    generate_w3_reviews(corpus, ids, id_to_idx, minilm, specter2, tfidf_matrix, profiles)
    generate_w4_1_reviews(corpus, ids, id_to_idx, minilm, tfidf_matrix, profiles)
    generate_w5_4_reviews(corpus, ids, id_to_idx, minilm, specter2, tfidf_matrix, profiles)
    generate_extension_reviews(corpus, ids, id_to_idx, minilm, profiles)

    print("\nAll review inputs generated.")


if __name__ == "__main__":
    main()
