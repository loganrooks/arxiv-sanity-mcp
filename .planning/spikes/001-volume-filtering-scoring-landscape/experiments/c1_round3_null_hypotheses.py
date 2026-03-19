"""
C1 Round 3 Null Hypothesis Testing

For each design recommendation, test the null hypothesis (simple model
is sufficient) before accepting the alternative (complex model needed).

H0-adapt: Centroid degradation is a simulation artifact
H0-experts: Single centroid with bounded updates = multiple centroids
H0-svm: SVM adaptive model degrades the same way
H0-ground-truth: Results change when ground truth definition changes

Usage:
    python c1_round3_null_hypotheses.py
"""

import json
import sqlite3
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
EMBEDDINGS_PATH = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
RESULTS_PATH = DATA_DIR / "c1_round3_null_hypothesis_results.json"


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
    embeddings = np.load(EMBEDDINGS_PATH)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}
    return papers, id_to_paper, embeddings, arxiv_ids, id_to_idx


def find_seeds(papers, keywords, n=5):
    scored = []
    for p in papers:
        text = f"{p['title']} {p['abstract']}".lower()
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scored.append((p["arxiv_id"], score))
    scored.sort(key=lambda x: -x[1])
    return [aid for aid, _ in scored[:n]]


def run_adaptive_sim(
    embeddings, arxiv_ids, id_to_idx,
    seed_ids, ground_truth_ids,
    model_type="centroid",  # "centroid", "bounded_centroid", "multi_centroid", "svm"
    days=30,
    papers_for_tfidf=None,
    id_to_paper=None,
):
    """Run adaptive simulation with specified model type."""
    positive_ids = list(seed_ids)
    negative_ids = []
    daily_metrics = []
    rng = np.random.RandomState(42)

    # For SVM, pre-compute TF-IDF
    tfidf_matrix = None
    if model_type == "svm" and papers_for_tfidf is not None:
        texts = [f"{id_to_paper.get(aid, {}).get('title', '')}. {id_to_paper.get(aid, {}).get('abstract', '')}"
                 for aid in arxiv_ids]
        vectorizer = TfidfVectorizer(max_features=10000, sublinear_tf=True, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(texts)

    for day in range(days):
        seen = set(positive_ids) | set(negative_ids)

        if model_type in ("centroid", "bounded_centroid"):
            pos_indices = [id_to_idx[aid] for aid in positive_ids if aid in id_to_idx]
            if not pos_indices:
                break
            pos_emb = embeddings[pos_indices]
            model_centroid = pos_emb.mean(axis=0, keepdims=True)

            if model_type == "bounded_centroid":
                # Only use last 10 positive papers (bounded memory)
                recent_pos = positive_ids[-10:]
                recent_indices = [id_to_idx[aid] for aid in recent_pos if aid in id_to_idx]
                if recent_indices:
                    model_centroid = embeddings[recent_indices].mean(axis=0, keepdims=True)

            # Negative adjustment
            if negative_ids:
                neg_indices = [id_to_idx[aid] for aid in negative_ids[-10:] if aid in id_to_idx]
                if neg_indices:
                    neg_centroid = embeddings[neg_indices].mean(axis=0, keepdims=True)
                    model_centroid = model_centroid - 0.3 * neg_centroid
                    model_centroid /= np.linalg.norm(model_centroid) + 1e-10

            scores = (embeddings @ model_centroid.T).flatten()

        elif model_type == "multi_centroid":
            # K-means on positive embeddings to find multiple interest centers
            from sklearn.cluster import KMeans
            pos_indices = [id_to_idx[aid] for aid in positive_ids if aid in id_to_idx]
            if not pos_indices:
                break
            pos_emb = embeddings[pos_indices]

            k = min(3, len(pos_indices))
            if k < 2:
                centroids = pos_emb.mean(axis=0, keepdims=True)
            else:
                km = KMeans(n_clusters=k, random_state=42, n_init=3)
                km.fit(pos_emb)
                centroids = km.cluster_centers_

            # Score = max similarity to any centroid
            all_sims = embeddings @ centroids.T  # (N, k)
            scores = all_sims.max(axis=1)

        elif model_type == "svm":
            if tfidf_matrix is None:
                break
            # Train SVM on current positive/negative
            labels = np.zeros(len(arxiv_ids))
            for aid in positive_ids:
                if aid in id_to_idx:
                    labels[id_to_idx[aid]] = 1
            for aid in negative_ids:
                if aid in id_to_idx:
                    labels[id_to_idx[aid]] = -1

            # Only train if we have both classes
            if labels.max() > 0:
                try:
                    clf = LinearSVC(C=0.01, class_weight='balanced', max_iter=5000)
                    # Use labeled + sample of unlabeled for training
                    labeled_mask = labels != 0
                    unlabeled_idx = np.where(~labeled_mask)[0]
                    sample_unlabeled = rng.choice(unlabeled_idx, size=min(500, len(unlabeled_idx)), replace=False)

                    train_idx = np.concatenate([np.where(labeled_mask)[0], sample_unlabeled])
                    train_labels = labels[train_idx].copy()
                    train_labels[train_labels == 0] = -1  # Treat unlabeled as negative
                    train_labels[train_labels == -1] = 0  # Original negatives stay 0? No:
                    # Actually: positive=1, negative/unlabeled=0
                    train_labels_binary = (labels[train_idx] == 1).astype(int)

                    clf.fit(tfidf_matrix[train_idx], train_labels_binary)
                    scores = clf.decision_function(tfidf_matrix).astype(float)
                except Exception:
                    # Fallback to centroid if SVM fails
                    pos_indices = [id_to_idx[aid] for aid in positive_ids if aid in id_to_idx]
                    scores = (embeddings @ embeddings[pos_indices].mean(axis=0, keepdims=True).T).flatten()
            else:
                pos_indices = [id_to_idx[aid] for aid in positive_ids if aid in id_to_idx]
                scores = (embeddings @ embeddings[pos_indices].mean(axis=0, keepdims=True).T).flatten()

        # Exclude seen
        for aid in seen:
            if aid in id_to_idx:
                scores[id_to_idx[aid]] = -999

        # Surface top 20
        top_20_indices = np.argsort(scores)[-20:][::-1]
        surfaced = [arxiv_ids[i] for i in top_20_indices]

        # Precision against ground truth
        precision = len(set(surfaced) & ground_truth_ids) / len(surfaced) if surfaced else 0

        # Seed relevance
        seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
        seed_centroid = embeddings[seed_indices].mean(axis=0, keepdims=True)
        surfaced_indices = [id_to_idx[aid] for aid in surfaced if aid in id_to_idx]
        if surfaced_indices:
            surfaced_emb = embeddings[surfaced_indices]
            seed_rel = float((surfaced_emb @ seed_centroid.T).mean())
        else:
            seed_rel = 0

        daily_metrics.append({
            "day": day + 1,
            "precision": round(float(precision), 4),
            "seed_relevance": round(float(seed_rel), 4),
        })

        # Simulate user feedback
        interesting = [aid for aid in surfaced if aid in ground_truth_ids][:3]
        not_interesting = [aid for aid in surfaced if aid not in ground_truth_ids][:5]
        positive_ids.extend(interesting)
        negative_ids.extend(not_interesting)

    return daily_metrics


def main():
    print("=" * 80)
    print("C1 Round 3: Null Hypothesis Testing")
    print("=" * 80)

    papers, id_to_paper, embeddings, arxiv_ids, id_to_idx = load_all()

    # Test interest: RL for Robotics (where degradation was observed)
    seeds_rl = find_seeds(papers, ["reinforcement learning", "robot", "manipulation", "policy"])
    seeds_llm = find_seeds(papers, ["language model", "reasoning", "chain of thought", "in-context"])

    results = {}

    for interest_name, seed_ids in [("RL_Robotics", seeds_rl), ("LLM_Reasoning", seeds_llm)]:
        print(f"\n{'=' * 70}")
        print(f"Interest: {interest_name} ({len(seed_ids)} seeds)")
        print(f"{'=' * 70}")

        seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
        seed_emb = embeddings[seed_indices]
        seed_centroid = seed_emb.mean(axis=0, keepdims=True)

        # === H0-ground-truth: Test with different ground truth definitions ===
        print("\n  H0-ground-truth: Does ground truth definition affect degradation?")

        gt_definitions = {}

        # GT1: Top 200 by seed similarity (original — potentially circular)
        sims = (embeddings @ seed_centroid.T).flatten()
        gt1 = set(arxiv_ids[i] for i in np.argsort(sims)[-200:])
        gt_definitions["seed_sim_top200"] = gt1

        # GT2: Same primary category as seeds (independent of embeddings)
        seed_cats = {id_to_paper.get(aid, {}).get("primary_category") for aid in seed_ids}
        gt2 = {p["arxiv_id"] for p in papers if p["primary_category"] in seed_cats}
        # Sample 200 from category
        gt2_list = sorted(gt2)
        rng = np.random.RandomState(42)
        if len(gt2_list) > 200:
            gt2 = set(rng.choice(gt2_list, 200, replace=False))
        gt_definitions["same_category_200"] = gt2

        # GT3: Keyword match (independent of embeddings AND categories)
        keywords = interest_name.lower().replace("_", " ").split()
        gt3 = set()
        for p in papers:
            text = f"{p['title']} {p['abstract']}".lower()
            if any(kw in text for kw in keywords):
                gt3.add(p["arxiv_id"])
        gt3_list = sorted(gt3)
        if len(gt3_list) > 200:
            gt3 = set(rng.choice(gt3_list, 200, replace=False))
        gt_definitions["keyword_match_200"] = gt3

        gt_results = {}
        for gt_name, gt_ids in gt_definitions.items():
            metrics = run_adaptive_sim(
                embeddings, arxiv_ids, id_to_idx,
                seed_ids, gt_ids,
                model_type="centroid", days=30,
            )
            p1 = metrics[0]["precision"]
            p30 = metrics[-1]["precision"]
            delta = p30 - p1
            gt_results[gt_name] = {
                "day1_precision": p1,
                "day30_precision": p30,
                "delta": round(float(delta), 4),
                "degrades": delta < -0.1,
            }
            status = "DEGRADES" if delta < -0.1 else "STABLE" if abs(delta) < 0.1 else "IMPROVES"
            print(f"    GT={gt_name:25s}  day1={p1:.3f}  day30={p30:.3f}  delta={delta:+.3f}  [{status}]")

        results[f"{interest_name}_gt_sensitivity"] = gt_results

        # === H0-experts: Does bounded centroid match multi-centroid? ===
        print(f"\n  H0-experts: Bounded centroid vs multi-centroid vs full centroid")

        # Use keyword GT (most independent)
        gt_ids = gt_definitions["keyword_match_200"]

        model_results = {}
        for model_type in ["centroid", "bounded_centroid", "multi_centroid", "svm"]:
            metrics = run_adaptive_sim(
                embeddings, arxiv_ids, id_to_idx,
                seed_ids, gt_ids,
                model_type=model_type, days=30,
                papers_for_tfidf=papers if model_type == "svm" else None,
                id_to_paper=id_to_paper,
            )
            p1 = metrics[0]["precision"]
            p10 = metrics[min(9, len(metrics)-1)]["precision"]
            p30 = metrics[-1]["precision"]
            r1 = metrics[0]["seed_relevance"]
            r30 = metrics[-1]["seed_relevance"]

            model_results[model_type] = {
                "day1_precision": p1,
                "day10_precision": p10,
                "day30_precision": p30,
                "precision_delta": round(float(p30 - p1), 4),
                "day1_relevance": r1,
                "day30_relevance": r30,
                "relevance_delta": round(float(r30 - r1), 4),
            }
            status = "DEGRADES" if (p30 - p1) < -0.1 else "STABLE" if abs(p30 - p1) < 0.1 else "IMPROVES"
            print(f"    {model_type:20s}  p1={p1:.3f}  p10={p10:.3f}  p30={p30:.3f}  "
                  f"delta={p30-p1:+.3f}  [{status}]")

        results[f"{interest_name}_model_comparison"] = model_results

    # === Summary: Can we reject the null hypotheses? ===
    print(f"\n{'=' * 70}")
    print("NULL HYPOTHESIS ASSESSMENT")
    print(f"{'=' * 70}")

    print("""
    H0-ground-truth: "Degradation is a simulation artifact"
    → Check if degradation persists across all GT definitions.
    If degradation only appears with circular GT (seed_sim), it's an artifact.
    If it appears with independent GTs (category, keyword), it's real.
    """)

    print("""
    H0-experts: "Single centroid with bounded updates = multiple centroids"
    → Check if bounded_centroid matches or exceeds multi_centroid.
    If bounded_centroid is equal, the simple model is sufficient.
    If multi_centroid is clearly better, complexity is justified.
    """)

    print("""
    H0-svm: "SVM degrades the same way"
    → Check SVM delta. If SVM also degrades, the problem isn't centroid-specific.
    If SVM is stable, centroid models are specifically problematic.
    """)

    # Save
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
