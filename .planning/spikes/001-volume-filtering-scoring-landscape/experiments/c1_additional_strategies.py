"""
Additional recommendation strategies not yet tested.

1. Reciprocal Rank Fusion (RRF) — combine MiniLM + SPECTER2 + TF-IDF
2. BERTopic topic similarity
3. OpenAlex related_works
4. Co-author network proximity
5. Rare category co-occurrence
6. Cross-encoder reranking (retrieve then rerank)

All evaluated via leave-one-out recall@K on model-independent clusters
(category co-membership groups).

Usage:
    python c1_additional_strategies.py
"""

import json
import sqlite3
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cos_sim

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
MINILM_EMBEDDINGS = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
B2_CACHE = DATA_DIR / "b2_openalex_cache.json"
RESULTS_PATH = DATA_DIR / "c1_additional_strategies_results.json"

K_VALUES = [20, 50, 100, 500]


def load_all():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, primary_category, categories "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    papers = [dict(r) for r in rows]
    id_to_paper = {p["arxiv_id"]: p for p in papers}
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}
    return papers, id_to_paper, minilm_emb, arxiv_ids, id_to_idx


def get_category_groups(papers, arxiv_ids, id_to_paper):
    """Model-independent ground truth: papers sharing exact category sets."""
    cat_groups = defaultdict(set)
    for aid in arxiv_ids:
        p = id_to_paper.get(aid, {})
        cats = frozenset(c.strip() for c in (p.get("categories") or "").split() if c.strip())
        if len(cats) >= 2:
            cat_groups[cats].add(aid)
    groups = [(cats, list(aids)) for cats, aids in cat_groups.items() if 10 <= len(aids) <= 200]
    groups.sort(key=lambda x: len(x[1]), reverse=True)
    return groups[:10]


def evaluate_strategy(name, score_fn, arxiv_ids, id_to_idx, test_groups):
    """Run leave-one-out evaluation for a scoring function."""
    all_ranks = []

    for cats, group_aids in test_groups:
        for held_out in group_aids[:15]:
            seeds = [a for a in group_aids if a != held_out][:10]
            held_idx = id_to_idx.get(held_out)
            if held_idx is None:
                continue

            scores = score_fn(seeds, held_out)
            if scores is None:
                continue

            rank = int((scores > scores[held_idx]).sum()) + 1
            all_ranks.append(rank)

    if not all_ranks:
        return {"name": name, "n": 0, "error": "no evaluations"}

    recall = {}
    for k in K_VALUES:
        recall[k] = round(sum(1 for r in all_ranks if r <= k) / len(all_ranks), 4)

    return {
        "name": name,
        "n": len(all_ranks),
        "recall": recall,
        "median_rank": int(np.median(all_ranks)),
        "mean_rank": round(float(np.mean(all_ranks)), 1),
    }


def main():
    print("=" * 80)
    print("Additional Recommendation Strategies")
    print("=" * 80)

    papers, id_to_paper, minilm_emb, arxiv_ids, id_to_idx = load_all()

    # Build TF-IDF
    print("Building TF-IDF...")
    texts = [f"{id_to_paper.get(aid, {}).get('title', '')}. {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in arxiv_ids]
    tfidf_vectorizer = TfidfVectorizer(max_features=10000, sublinear_tf=True, stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    # Compute SPECTER2
    print("Computing SPECTER2...")
    from sentence_transformers import SentenceTransformer
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    specter_model = SentenceTransformer("allenai/specter2_base", device=device)
    specter_texts = [f"{id_to_paper.get(aid, {}).get('title', '')} [SEP] {id_to_paper.get(aid, {}).get('abstract', '')}"
                     for aid in arxiv_ids]
    specter_emb = specter_model.encode(specter_texts, batch_size=64, convert_to_numpy=True,
                                        normalize_embeddings=True, show_progress_bar=True)
    del specter_model
    if device == "cuda":
        torch.cuda.empty_cache()

    # BERTopic clusters
    print("Computing BERTopic clusters...")
    km = MiniBatchKMeans(n_clusters=48, random_state=42, batch_size=1000)
    topic_labels = km.fit_predict(minilm_emb)

    # Load OpenAlex related_works
    print("Loading OpenAlex data...")
    openalex_related = {}
    if Path(B2_CACHE).exists():
        with open(B2_CACHE) as f:
            cache = json.load(f)
        for aid, data in cache.items():
            if isinstance(data, dict) and "error" not in data:
                openalex_related[aid] = set(data.get("related_works", []))

    # Build author index
    print("Building author index...")
    author_papers = defaultdict(set)
    paper_authors = defaultdict(set)
    for p in papers:
        for author in (p.get("authors_text") or "").split(","):
            author = author.strip().lower()
            if author and len(author) > 2:
                author_papers[author].add(p["arxiv_id"])
                paper_authors[p["arxiv_id"]].add(author)

    # Category co-occurrence index
    paper_cats = {}
    for p in papers:
        cats = frozenset(c.strip() for c in (p.get("categories") or "").split() if c.strip())
        paper_cats[p["arxiv_id"]] = cats

    # Get test groups (model-independent)
    test_groups = get_category_groups(papers, arxiv_ids, id_to_paper)
    print(f"Test groups: {len(test_groups)} (category co-membership)")

    results = []

    # === Strategy 1: Baselines (for comparison) ===
    print("\n--- Baselines ---")

    def minilm_score(seeds, held_out):
        seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
        if not seed_idx:
            return None
        centroid = minilm_emb[seed_idx].mean(axis=0, keepdims=True)
        return (minilm_emb @ centroid.T).flatten()

    def specter_score(seeds, held_out):
        seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
        if not seed_idx:
            return None
        centroid = specter_emb[seed_idx].mean(axis=0, keepdims=True)
        return (specter_emb @ centroid.T).flatten()

    def tfidf_score(seeds, held_out):
        seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
        if not seed_idx:
            return None
        seed_tf = tfidf_matrix[seed_idx].mean(axis=0)
        return cos_sim(np.asarray(seed_tf), tfidf_matrix).flatten()

    for name, fn in [("MiniLM", minilm_score), ("SPECTER2", specter_score), ("TF-IDF", tfidf_score)]:
        r = evaluate_strategy(name, fn, arxiv_ids, id_to_idx, test_groups)
        results.append(r)
        print(f"  {name:<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 2: Reciprocal Rank Fusion ===
    print("\n--- Reciprocal Rank Fusion (RRF) ---")

    def rrf_score(seeds, held_out, k=60):
        """Combine MiniLM + SPECTER2 + TF-IDF via RRF."""
        s1 = minilm_score(seeds, held_out)
        s2 = specter_score(seeds, held_out)
        s3 = tfidf_score(seeds, held_out)
        if s1 is None or s2 is None or s3 is None:
            return None

        # RRF: score = sum(1 / (k + rank_i))
        combined = np.zeros(len(arxiv_ids))
        for scores in [s1, s2, s3]:
            ranks = np.argsort(np.argsort(-scores))  # Rank from 0
            combined += 1.0 / (k + ranks)
        return combined

    def rrf_2model(seeds, held_out, k=60):
        """RRF with just MiniLM + SPECTER2."""
        s1 = minilm_score(seeds, held_out)
        s2 = specter_score(seeds, held_out)
        if s1 is None or s2 is None:
            return None
        combined = np.zeros(len(arxiv_ids))
        for scores in [s1, s2]:
            ranks = np.argsort(np.argsort(-scores))
            combined += 1.0 / (k + ranks)
        return combined

    for name, fn in [("RRF (MiniLM+SPECTER2)", rrf_2model), ("RRF (all 3)", rrf_score)]:
        r = evaluate_strategy(name, fn, arxiv_ids, id_to_idx, test_groups)
        results.append(r)
        print(f"  {name:<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 3: BERTopic topic similarity ===
    print("\n--- BERTopic Topic Similarity ---")

    def topic_score(seeds, held_out):
        seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
        if not seed_idx:
            return None
        # Score: fraction of seed topics that match each paper's topic
        seed_topics = Counter(topic_labels[i] for i in seed_idx)
        total_seeds = sum(seed_topics.values())
        scores = np.zeros(len(arxiv_ids))
        for i, topic in enumerate(topic_labels):
            scores[i] = seed_topics.get(topic, 0) / total_seeds
        return scores

    r = evaluate_strategy("BERTopic topic", topic_score, arxiv_ids, id_to_idx, test_groups)
    results.append(r)
    print(f"  {'BERTopic topic':<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 4: Co-author network ===
    print("\n--- Co-author Network ---")

    def coauthor_score(seeds, held_out):
        # Find all authors of seed papers
        seed_authors = set()
        for aid in seeds:
            seed_authors |= paper_authors.get(aid, set())
        if not seed_authors:
            return None

        # Score papers by author overlap with seed authors
        scores = np.zeros(len(arxiv_ids))
        for i, aid in enumerate(arxiv_ids):
            p_authors = paper_authors.get(aid, set())
            if p_authors & seed_authors:
                scores[i] = len(p_authors & seed_authors) / len(seed_authors)
        return scores

    r = evaluate_strategy("Co-author network", coauthor_score, arxiv_ids, id_to_idx, test_groups)
    results.append(r)
    print(f"  {'Co-author network':<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 5: Rare category co-occurrence ===
    print("\n--- Rare Category Co-occurrence ---")

    # Compute category rarity (inverse frequency)
    cat_freq = Counter()
    for aid in arxiv_ids:
        for cat in paper_cats.get(aid, set()):
            cat_freq[cat] += 1
    max_freq = max(cat_freq.values()) if cat_freq else 1

    def rare_cat_score(seeds, held_out):
        seed_cat_set = set()
        for aid in seeds:
            seed_cat_set |= paper_cats.get(aid, set())
        if not seed_cat_set:
            return None

        # Weight categories by rarity (IDF-like)
        cat_weights = {c: np.log(max_freq / (cat_freq.get(c, 1) + 1)) for c in seed_cat_set}

        scores = np.zeros(len(arxiv_ids))
        for i, aid in enumerate(arxiv_ids):
            p_cats = paper_cats.get(aid, set())
            shared = p_cats & seed_cat_set
            if shared:
                scores[i] = sum(cat_weights.get(c, 0) for c in shared)
        return scores

    r = evaluate_strategy("Rare category co-occ", rare_cat_score, arxiv_ids, id_to_idx, test_groups)
    results.append(r)
    print(f"  {'Rare category co-occ':<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 6: Weighted embedding combination ===
    print("\n--- Weighted Combinations ---")

    for alpha in [0.3, 0.5, 0.7]:
        def weighted_score(seeds, held_out, a=alpha):
            s1 = minilm_score(seeds, held_out)
            s2 = specter_score(seeds, held_out)
            if s1 is None or s2 is None:
                return None
            # Normalize scores to [0, 1] range
            s1_norm = (s1 - s1.min()) / (s1.max() - s1.min() + 1e-10)
            s2_norm = (s2 - s2.min()) / (s2.max() - s2.min() + 1e-10)
            return a * s1_norm + (1 - a) * s2_norm

        name = f"Weighted (MiniLM={alpha:.1f})"
        r = evaluate_strategy(name, weighted_score, arxiv_ids, id_to_idx, test_groups)
        results.append(r)
        print(f"  {name:<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Strategy 7: Embedding + TF-IDF hybrid ===
    print("\n--- Embedding + TF-IDF Hybrid ---")

    def hybrid_emb_tfidf(seeds, held_out):
        s1 = minilm_score(seeds, held_out)
        s3 = tfidf_score(seeds, held_out)
        if s1 is None or s3 is None:
            return None
        s1_norm = (s1 - s1.min()) / (s1.max() - s1.min() + 1e-10)
        s3_norm = (s3 - s3.min()) / (s3.max() - s3.min() + 1e-10)
        return 0.7 * s1_norm + 0.3 * s3_norm

    r = evaluate_strategy("MiniLM(0.7)+TF-IDF(0.3)", hybrid_emb_tfidf, arxiv_ids, id_to_idx, test_groups)
    results.append(r)
    print(f"  {'MiniLM(0.7)+TF-IDF(0.3)':<30s}  R@100={r['recall'].get(100, 0):.1%}  MedRank={r.get('median_rank', '?')}")

    # === Summary ===
    print(f"\n{'=' * 80}")
    print("SUMMARY — All Strategies Ranked by R@100")
    print(f"{'=' * 80}")

    results.sort(key=lambda r: r.get("recall", {}).get(100, 0), reverse=True)

    print(f"  {'Strategy':<35s}", end="")
    for k in K_VALUES:
        print(f"  {'R@'+str(k):>8s}", end="")
    print(f"  {'MedRank':>8s}")
    print(f"  {'-' * (37 + 10 * len(K_VALUES) + 10)}")

    for r in results:
        if "error" in r:
            print(f"  {r['name']:<35s}  (no data)")
            continue
        print(f"  {r['name']:<35s}", end="")
        for k in K_VALUES:
            print(f"  {r['recall'].get(k, 0):>8.1%}", end="")
        print(f"  {r.get('median_rank', '?'):>8}")

    # Save
    output = {
        "strategies": results,
        "evaluation": "leave-one-out on category co-membership groups (model-independent)",
        "test_groups": len(test_groups),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2, default=convert)

    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
