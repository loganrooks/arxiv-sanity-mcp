"""
C1 Round 3: Systematic Filtering Landscape Analysis

R10: Leave-one-out retrieval quality
R11: Retrieval + reranking pipelines
R12: Seed count sensitivity
R13: Interest breadth sensitivity
R14: Marginal signal value
R15: SPECTER2 quality profiles
R16: Bibliographic coupling

Usage:
    python c1_round3_landscape.py
"""

import json
import sqlite3
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
MINILM_EMBEDDINGS = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
B2_CACHE = DATA_DIR / "b2_openalex_cache.json"
RESULTS_PATH = DATA_DIR / "c1_round3_landscape_results.json"


def load_all():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    papers = [dict(r) for r in rows]
    id_to_paper = {p["arxiv_id"]: p for p in papers}
    embeddings = np.load(MINILM_EMBEDDINGS)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}
    return papers, id_to_paper, embeddings, arxiv_ids, id_to_idx


def get_clusters(embeddings, n_clusters=48):
    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1000)
    labels = km.fit_predict(embeddings)
    return labels, km.cluster_centers_


def build_tfidf(papers, arxiv_ids, id_to_paper):
    texts = [f"{id_to_paper.get(aid, {}).get('title', '')}. {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in arxiv_ids]
    vectorizer = TfidfVectorizer(max_features=10000, sublinear_tf=True, stop_words='english')
    matrix = vectorizer.fit_transform(texts)
    return matrix, vectorizer


def load_references():
    """Load bibliographic coupling data from OpenAlex cache."""
    if not Path(B2_CACHE).exists():
        return {}
    with open(B2_CACHE) as f:
        cache = json.load(f)
    refs = {}
    for aid, data in cache.items():
        if isinstance(data, dict) and "error" not in data:
            ref_works = data.get("referenced_works", [])
            refs[aid] = set(ref_works)
    return refs


# ======================================================================
# R10: Leave-One-Out Retrieval Quality
# ======================================================================

def run_r10(embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf, references):
    print("=" * 70)
    print("R10: Leave-One-Out Retrieval Quality")
    print("=" * 70)

    # Find coherent clusters (>= 20 papers)
    cluster_papers = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        cluster_papers[label].append(arxiv_ids[i])

    test_clusters = [(label, papers) for label, papers in cluster_papers.items()
                     if 10 <= len(papers) <= 2000]
    test_clusters.sort(key=lambda x: len(x[1]))
    test_clusters = test_clusters[:10]  # Test 10 clusters

    approaches = ["embedding_minilm", "keyword_tfidf", "svm"]
    if references:
        approaches.append("bibcoupling")

    # Use recall@K — more appropriate for recommendation than MRR
    K_VALUES = [20, 50, 100, 500]
    all_ranks = {a: [] for a in approaches}

    print(f"\n  Testing {len(test_clusters)} clusters, {len(approaches)} approaches")
    print(f"  Metric: recall@K (fraction of held-out papers found in top-K)")

    for cluster_id, cluster_aids in test_clusters:
        cluster_ranks = {a: [] for a in approaches}

        holdout_aids = cluster_aids[:20]

        for held_out in holdout_aids:
            seed_aids = [aid for aid in cluster_aids if aid != held_out][:10]
            seed_indices = [id_to_idx[aid] for aid in seed_aids if aid in id_to_idx]
            if not seed_indices:
                continue

            held_idx = id_to_idx.get(held_out)
            if held_idx is None:
                continue

            # Embedding retrieval
            seed_centroid = embeddings[seed_indices].mean(axis=0, keepdims=True)
            emb_scores = (embeddings @ seed_centroid.T).flatten()
            emb_rank = int((emb_scores > emb_scores[held_idx]).sum()) + 1
            cluster_ranks["embedding_minilm"].append(emb_rank)

            # TF-IDF/keyword retrieval
            seed_tfidf = tfidf[seed_indices].mean(axis=0)
            from sklearn.metrics.pairwise import cosine_similarity as cos_sim
            tfidf_scores = cos_sim(np.asarray(seed_tfidf), tfidf).flatten()
            tfidf_rank = int((tfidf_scores > tfidf_scores[held_idx]).sum()) + 1
            cluster_ranks["keyword_tfidf"].append(tfidf_rank)

            # SVM retrieval
            labels = np.zeros(len(arxiv_ids))
            for aid in seed_aids:
                if aid in id_to_idx:
                    labels[id_to_idx[aid]] = 1
            try:
                clf = LinearSVC(C=0.01, class_weight='balanced', max_iter=5000)
                clf.fit(tfidf, labels)
                svm_scores = clf.decision_function(tfidf)
                svm_rank = int((svm_scores > svm_scores[held_idx]).sum()) + 1
                cluster_ranks["svm"].append(svm_rank)
            except Exception:
                cluster_ranks["svm"].append(len(arxiv_ids))

            # Bibliographic coupling
            if references and held_out in references:
                held_refs = references[held_out]
                bc_scores = np.zeros(len(arxiv_ids))
                for i, aid in enumerate(arxiv_ids):
                    if aid in references and references[aid]:
                        bc_scores[i] = len(held_refs & references[aid]) / len(held_refs | references[aid])
                bc_rank = int((bc_scores > bc_scores[held_idx]).sum()) + 1
                cluster_ranks["bibcoupling"].append(bc_rank)

        for a in approaches:
            all_ranks[a].extend(cluster_ranks.get(a, []))

    # Compute recall@K for each approach
    print(f"\n  {'Approach':<20s}", end="")
    for k in K_VALUES:
        print(f"  {'R@'+str(k):>8s}", end="")
    print(f"  {'MedRank':>8s}  {'MeanRank':>9s}")
    print(f"  {'-' * (22 + 10 * len(K_VALUES) + 20)}")

    summary = {}
    for a in approaches:
        ranks = all_ranks[a]
        if not ranks:
            continue
        recall_at_k = {}
        for k in K_VALUES:
            recall = sum(1 for r in ranks if r <= k) / len(ranks)
            recall_at_k[k] = round(recall, 4)

        median_rank = int(np.median(ranks))
        mean_rank = round(float(np.mean(ranks)), 1)

        print(f"  {a:<20s}", end="")
        for k in K_VALUES:
            print(f"  {recall_at_k[k]:>8.1%}", end="")
        print(f"  {median_rank:>8d}  {mean_rank:>9.1f}")

        summary[a] = {
            "recall_at_k": recall_at_k,
            "median_rank": median_rank,
            "mean_rank": mean_rank,
            "n_evaluations": len(ranks),
        }

    return {"summary": summary}


# ======================================================================
# R12: Seed Count Sensitivity
# ======================================================================

def run_r12(embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf):
    print(f"\n{'=' * 70}")
    print("R12: Seed Count Sensitivity")
    print(f"{'=' * 70}")

    # Pick 3 clusters of different sizes
    cluster_papers = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        cluster_papers[label].append(arxiv_ids[i])

    test_clusters = [(label, papers) for label, papers in cluster_papers.items()
                     if len(papers) >= 50]
    test_clusters.sort(key=lambda x: len(x[1]), reverse=True)
    test_clusters = test_clusters[:3]

    seed_counts = [1, 2, 3, 5, 10, 20]
    results = []

    for cluster_id, cluster_aids in test_clusters:
        print(f"\n  Cluster {cluster_id} ({len(cluster_aids)} papers):")
        print(f"  {'Seeds':>8s} {'Emb MRR':>10s} {'TF-IDF MRR':>12s} {'SVM MRR':>10s}")
        print(f"  {'-' * 42}")

        for n_seeds in seed_counts:
            if n_seeds >= len(cluster_aids):
                continue

            # Hold out 10 papers, use n_seeds as seeds
            mrr_emb, mrr_tfidf, mrr_svm = [], [], []

            for trial in range(5):
                rng = np.random.RandomState(trial)
                perm = rng.permutation(len(cluster_aids))
                holdout_aids = [cluster_aids[i] for i in perm[:10]]
                seed_aids = [cluster_aids[i] for i in perm[10:10+n_seeds]]

                seed_indices = [id_to_idx[aid] for aid in seed_aids if aid in id_to_idx]
                if not seed_indices:
                    continue

                seed_centroid = embeddings[seed_indices].mean(axis=0, keepdims=True)
                emb_scores = (embeddings @ seed_centroid.T).flatten()

                seed_tfidf = tfidf[seed_indices].mean(axis=0)
                from sklearn.metrics.pairwise import cosine_similarity as cos_sim
                tfidf_scores = cos_sim(np.asarray(seed_tfidf), tfidf).flatten()

                # SVM
                labels = np.zeros(len(arxiv_ids))
                for aid in seed_aids:
                    if aid in id_to_idx:
                        labels[id_to_idx[aid]] = 1
                try:
                    clf = LinearSVC(C=0.01, class_weight='balanced', max_iter=5000)
                    clf.fit(tfidf, labels)
                    svm_scores = clf.decision_function(tfidf)
                except Exception:
                    svm_scores = emb_scores  # Fallback

                for held_out in holdout_aids:
                    held_idx = id_to_idx.get(held_out)
                    if held_idx is None:
                        continue
                    emb_rank = int((emb_scores > emb_scores[held_idx]).sum()) + 1
                    mrr_emb.append(1.0 / emb_rank)
                    tf_rank = int((tfidf_scores > tfidf_scores[held_idx]).sum()) + 1
                    mrr_tfidf.append(1.0 / tf_rank)
                    sv_rank = int((svm_scores > svm_scores[held_idx]).sum()) + 1
                    mrr_svm.append(1.0 / sv_rank)

            avg_emb = np.mean(mrr_emb) if mrr_emb else 0
            avg_tfidf = np.mean(mrr_tfidf) if mrr_tfidf else 0
            avg_svm = np.mean(mrr_svm) if mrr_svm else 0

            print(f"  {n_seeds:>8d} {avg_emb:>10.4f} {avg_tfidf:>12.4f} {avg_svm:>10.4f}")

            results.append({
                "cluster": cluster_id,
                "cluster_size": len(cluster_aids),
                "n_seeds": n_seeds,
                "emb_mrr": round(float(avg_emb), 4),
                "tfidf_mrr": round(float(avg_tfidf), 4),
                "svm_mrr": round(float(avg_svm), 4),
            })

    return results


# ======================================================================
# R14: Marginal Signal Value
# ======================================================================

def run_r14(embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf):
    print(f"\n{'=' * 70}")
    print("R14: Marginal Signal Value")
    print(f"{'=' * 70}")

    # Use leave-one-out on 5 clusters
    cluster_papers = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        cluster_papers[label].append(arxiv_ids[i])

    test_clusters = [(l, p) for l, p in cluster_papers.items() if 10 <= len(p) <= 2000]
    test_clusters.sort(key=lambda x: len(x[1]))
    test_clusters = test_clusters[:5]

    def compute_mrr(scores, held_idx):
        rank = int((scores > scores[held_idx]).sum()) + 1
        return 1.0 / rank

    # Signal combinations (cumulative)
    signal_configs = [
        ("embedding_only", ["emb"]),
        ("+ keyword", ["emb", "kw"]),
        ("+ category", ["emb", "kw", "cat"]),
        ("+ citation", ["emb", "kw", "cat", "cite"]),
    ]

    # Load citation data
    citations = {}
    if Path(B2_CACHE).exists():
        with open(B2_CACHE) as f:
            cache = json.load(f)
        for aid, data in cache.items():
            if isinstance(data, dict) and "error" not in data:
                citations[aid] = data.get("cited_by_count", 0)

    results = []

    for config_name, signals in signal_configs:
        mrr_all = []

        for cluster_id, cluster_aids in test_clusters:
            for held_out in cluster_aids[:15]:
                seeds = [a for a in cluster_aids if a != held_out][:10]
                seed_indices = [id_to_idx[a] for a in seeds if a in id_to_idx]
                held_idx = id_to_idx.get(held_out)
                if not seed_indices or held_idx is None:
                    continue

                # Compute combined score
                scores = np.zeros(len(arxiv_ids))

                if "emb" in signals:
                    centroid = embeddings[seed_indices].mean(axis=0, keepdims=True)
                    scores += (embeddings @ centroid.T).flatten()

                if "kw" in signals:
                    from sklearn.metrics.pairwise import cosine_similarity as cs
                    seed_tf = tfidf[seed_indices].mean(axis=0)
                    scores += cs(np.asarray(seed_tf), tfidf).flatten() * 0.5

                if "cat" in signals:
                    seed_cats = {id_to_paper.get(a, {}).get("primary_category") for a in seeds}
                    for i, aid in enumerate(arxiv_ids):
                        if id_to_paper.get(aid, {}).get("primary_category") in seed_cats:
                            scores[i] += 0.1

                if "cite" in signals:
                    max_cite = max(citations.values()) if citations else 1
                    for i, aid in enumerate(arxiv_ids):
                        c = citations.get(aid, 0)
                        scores[i] += (c / max(max_cite, 1)) * 0.2

                mrr_all.append(compute_mrr(scores, held_idx))

        avg_mrr = np.mean(mrr_all) if mrr_all else 0
        results.append({"config": config_name, "mrr": round(float(avg_mrr), 4)})
        print(f"  {config_name:<25s}  MRR={avg_mrr:.4f}")

    # Marginal contributions
    if len(results) >= 2:
        print(f"\n  Marginal contributions:")
        for i in range(1, len(results)):
            delta = results[i]["mrr"] - results[i-1]["mrr"]
            print(f"    {results[i]['config']:25s}  delta={delta:+.4f}")

    return results


# ======================================================================
# R15: SPECTER2 Quality Profiles
# ======================================================================

def run_r15(papers, id_to_paper, arxiv_ids, id_to_idx, cluster_labels):
    print(f"\n{'=' * 70}")
    print("R15: SPECTER2 vs MiniLM Quality Profiles")
    print(f"{'=' * 70}")

    minilm_emb = np.load(MINILM_EMBEDDINGS)

    # Compute SPECTER2 for subset (or load if available)
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("allenai/specter2_base", device=device)

    # Compute for full corpus (needed for leave-one-out)
    texts = [f"{id_to_paper.get(aid, {}).get('title', '')} [SEP] {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in arxiv_ids]
    print("  Computing SPECTER2 embeddings (full corpus)...")
    specter_emb = model.encode(texts, batch_size=64, convert_to_numpy=True,
                                normalize_embeddings=True, show_progress_bar=True)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    # Leave-one-out comparison
    cluster_papers = defaultdict(list)
    for i, label in enumerate(cluster_labels):
        cluster_papers[label].append(arxiv_ids[i])

    test_clusters = [(l, p) for l, p in cluster_papers.items() if 10 <= len(p) <= 2000]
    test_clusters.sort(key=lambda x: len(x[1]))
    test_clusters = test_clusters[:5]

    minilm_ranks, specter_ranks = [], []
    K_VALUES = [20, 50, 100, 500]

    for cluster_id, cluster_aids in test_clusters:
        for held_out in cluster_aids[:15]:
            seeds = [a for a in cluster_aids if a != held_out][:10]
            seed_indices = [id_to_idx[a] for a in seeds if a in id_to_idx]
            held_idx = id_to_idx.get(held_out)
            if not seed_indices or held_idx is None:
                continue

            # MiniLM
            centroid = minilm_emb[seed_indices].mean(axis=0, keepdims=True)
            scores = (minilm_emb @ centroid.T).flatten()
            rank = int((scores > scores[held_idx]).sum()) + 1
            minilm_ranks.append(rank)

            # SPECTER2
            centroid = specter_emb[seed_indices].mean(axis=0, keepdims=True)
            scores = (specter_emb @ centroid.T).flatten()
            rank = int((scores > scores[held_idx]).sum()) + 1
            specter_ranks.append(rank)

    print(f"\n  Leave-one-out recall@K ({len(minilm_ranks)} evaluations):")
    print(f"  {'Model':<15s}", end="")
    for k in K_VALUES:
        print(f"  {'R@'+str(k):>8s}", end="")
    print(f"  {'MedRank':>8s}")
    print(f"  {'-' * (17 + 10 * len(K_VALUES) + 10)}")

    for label, ranks in [("MiniLM", minilm_ranks), ("SPECTER2", specter_ranks)]:
        print(f"  {label:<15s}", end="")
        for k in K_VALUES:
            recall = sum(1 for r in ranks if r <= k) / len(ranks) if ranks else 0
            print(f"  {recall:>8.1%}", end="")
        med = int(np.median(ranks)) if ranks else 0
        print(f"  {med:>8d}")

    # Direct comparison: for each evaluation, which model ranked it higher?
    minilm_wins = sum(1 for m, s in zip(minilm_ranks, specter_ranks) if m < s)
    specter_wins = sum(1 for m, s in zip(minilm_ranks, specter_ranks) if s < m)
    ties = sum(1 for m, s in zip(minilm_ranks, specter_ranks) if m == s)

    print(f"\n  Head-to-head: MiniLM wins {minilm_wins}, SPECTER2 wins {specter_wins}, ties {ties}")

    return {
        "minilm_median_rank": int(np.median(minilm_ranks)) if minilm_ranks else None,
        "specter2_median_rank": int(np.median(specter_ranks)) if specter_ranks else None,
        "minilm_recall_at_100": round(sum(1 for r in minilm_ranks if r <= 100) / max(len(minilm_ranks), 1), 4),
        "specter2_recall_at_100": round(sum(1 for r in specter_ranks if r <= 100) / max(len(specter_ranks), 1), 4),
        "head_to_head": {"minilm_wins": minilm_wins, "specter2_wins": specter_wins, "ties": ties},
        "n_evaluations": len(minilm_ranks),
    }


def main():
    print("=" * 80)
    print("C1 Round 3: Systematic Filtering Landscape")
    print("=" * 80)

    papers, id_to_paper, embeddings, arxiv_ids, id_to_idx = load_all()
    print(f"Papers: {len(papers)}, Embeddings: {embeddings.shape}")

    print("\nBuilding TF-IDF...")
    tfidf, vectorizer = build_tfidf(papers, arxiv_ids, id_to_paper)

    print("Computing clusters...")
    cluster_labels, _ = get_clusters(embeddings)

    print("Loading references...")
    references = load_references()
    print(f"  Papers with references: {len(references)}")

    results = {}

    results["R10_leave_one_out"] = run_r10(
        embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf, references
    )

    results["R12_seed_sensitivity"] = run_r12(
        embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf
    )

    results["R14_marginal_value"] = run_r14(
        embeddings, arxiv_ids, id_to_idx, id_to_paper, cluster_labels, tfidf
    )

    results["R15_specter2_profiles"] = run_r15(
        papers, id_to_paper, arxiv_ids, id_to_idx, cluster_labels
    )

    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Convert numpy types for JSON serialization
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2, default=convert)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
