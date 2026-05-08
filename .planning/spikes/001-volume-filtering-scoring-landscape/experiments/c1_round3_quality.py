"""
C1 Round 3: Quality measurement, parameterized curves, adaptive simulation.

C1-R7: Quality metrics (coherence, diversity, seed-relevance, novelty)
C1-R8: Parameterized precision-recall curves
C1-R9: Adaptive learning simulation (30-day user behavior)

Usage:
    python c1_round3_quality.py
"""

import json
import sqlite3
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
EMBEDDINGS_PATH = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
A2_RESULTS = DATA_DIR / "a2_corpus_visualization_results.json"
RESULTS_PATH = DATA_DIR / "c1_round3_results.json"


def load_all():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, primary_category "
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


def get_bertopic_clusters(arxiv_ids):
    """Get BERTopic cluster assignments from A2 results."""
    # Re-run BERTopic to get assignments (A2 didn't save per-paper assignments)
    # Use a simpler approach: k-means on embeddings
    from sklearn.cluster import MiniBatchKMeans

    embeddings = np.load(EMBEDDINGS_PATH)
    n_clusters = 48  # Match A2's BERTopic count

    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=42, batch_size=1000)
    labels = km.fit_predict(embeddings)

    return {aid: int(labels[i]) for i, aid in enumerate(arxiv_ids)}


# ======================================================================
# Simulated Research Interests (seed paper sets)
# ======================================================================

def get_research_interests(papers, id_to_idx, embeddings):
    """Define 5 research interests as seed paper sets."""
    interests = []

    # Helper: find papers matching keywords
    def find_seeds(keywords, n=5):
        scored = []
        for p in papers:
            text = f"{p['title']} {p['abstract']}".lower()
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scored.append((p["arxiv_id"], score))
        scored.sort(key=lambda x: -x[1])
        return [aid for aid, _ in scored[:n]]

    interests.append({
        "name": "RL for Robotics",
        "seeds": find_seeds(["reinforcement learning", "robot", "manipulation", "policy"]),
    })
    interests.append({
        "name": "LLM Reasoning",
        "seeds": find_seeds(["language model", "reasoning", "chain of thought", "in-context"]),
    })
    interests.append({
        "name": "Diffusion Models",
        "seeds": find_seeds(["diffusion", "denoising", "score matching", "generative"]),
    })
    interests.append({
        "name": "Graph ML",
        "seeds": find_seeds(["graph neural", "node classification", "message passing", "relational"]),
    })
    interests.append({
        "name": "AI Safety",
        "seeds": find_seeds(["alignment", "safety", "adversarial", "robustness", "red team"]),
    })

    return interests


# ======================================================================
# Quality Metrics
# ======================================================================

def measure_quality(filtered_ids, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters):
    """Compute quality metrics for a filtered paper set relative to seeds."""
    if not filtered_ids or not seed_ids:
        return {"error": "empty set"}

    # Get embeddings
    seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
    filtered_indices = [id_to_idx[aid] for aid in filtered_ids if aid in id_to_idx]

    if not seed_indices or not filtered_indices:
        return {"error": "no embeddings for papers"}

    seed_emb = embeddings[seed_indices]
    filtered_emb = embeddings[filtered_indices]
    filtered_aids = [aid for aid in filtered_ids if aid in id_to_idx]

    # 1. Topical coherence: mean pairwise cosine similarity within filtered set
    if len(filtered_emb) > 1:
        # Sample for efficiency (max 200 pairs)
        n = min(len(filtered_emb), 200)
        sample_idx = np.random.choice(len(filtered_emb), size=n, replace=False)
        sample = filtered_emb[sample_idx]
        pairwise = sample @ sample.T
        # Upper triangle (excluding diagonal)
        mask = np.triu(np.ones(pairwise.shape, dtype=bool), k=1)
        coherence = float(pairwise[mask].mean())
    else:
        coherence = 1.0

    # 2. Seed relevance: mean cosine similarity between filtered papers and seed centroid
    seed_centroid = seed_emb.mean(axis=0, keepdims=True)
    seed_sims = (filtered_emb @ seed_centroid.T).flatten()
    seed_relevance = float(seed_sims.mean())

    # 3. Diversity: number of distinct clusters represented
    filtered_clusters = set(clusters.get(aid, -1) for aid in filtered_aids)
    diversity = len(filtered_clusters)

    # Also: entropy of cluster distribution
    cluster_counts = Counter(clusters.get(aid, -1) for aid in filtered_aids)
    total = sum(cluster_counts.values())
    if total > 0 and len(cluster_counts) > 1:
        probs = np.array(list(cluster_counts.values())) / total
        cluster_entropy = float(-np.sum(probs * np.log2(probs + 1e-10)))
    else:
        cluster_entropy = 0.0

    # 4. Novelty: fraction of filtered papers NOT in same cluster as any seed
    seed_clusters = set(clusters.get(aid, -1) for aid in seed_ids if aid in clusters)
    novel_count = sum(1 for aid in filtered_aids if clusters.get(aid, -1) not in seed_clusters)
    novelty = novel_count / len(filtered_aids) if filtered_aids else 0

    return {
        "coherence": round(coherence, 4),
        "seed_relevance": round(seed_relevance, 4),
        "diversity_clusters": diversity,
        "cluster_entropy": round(cluster_entropy, 4),
        "novelty": round(float(novelty), 4),
        "volume": len(filtered_ids),
    }


# ======================================================================
# C1-R7: Quality profiles per strategy
# ======================================================================

def run_r7(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters):
    """Quality measurement for each filtering strategy × each interest."""
    print("=" * 70)
    print("C1-R7: Quality Measurement")
    print("=" * 70)

    interests = get_research_interests(papers, id_to_idx, embeddings)
    all_ids = set(arxiv_ids)

    results = []

    for interest in interests:
        print(f"\n  Interest: {interest['name']} ({len(interest['seeds'])} seeds)")
        seed_ids = set(interest["seeds"])
        seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
        if not seed_indices:
            continue
        seed_emb = embeddings[seed_indices]
        seed_centroid = seed_emb.mean(axis=0, keepdims=True)

        # Strategy 1: Embedding top-N (varying N)
        sims = (embeddings @ seed_centroid.T).flatten()
        sorted_indices = np.argsort(sims)[::-1]

        for frac_label, n in [("top-100", 100), ("top-500", 500), ("top-2000", 2000)]:
            top_ids = {arxiv_ids[i] for i in sorted_indices[:n]}
            quality = measure_quality(top_ids, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters)
            quality["strategy"] = f"embedding_{frac_label}"
            quality["interest"] = interest["name"]
            results.append(quality)

        # Strategy 2: Keyword match
        keywords = interest["name"].lower().split()
        kw_ids = set()
        for aid in all_ids:
            p = id_to_paper.get(aid, {})
            text = f"{p.get('title', '')} {p.get('abstract', '')}".lower()
            if any(kw in text for kw in keywords):
                kw_ids.add(aid)
        if kw_ids:
            quality = measure_quality(kw_ids, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters)
            quality["strategy"] = "keyword_match"
            quality["interest"] = interest["name"]
            results.append(quality)

        # Strategy 3: Same-category papers
        seed_cats = {id_to_paper.get(aid, {}).get("primary_category") for aid in seed_ids}
        cat_ids = {p["arxiv_id"] for p in papers if p["primary_category"] in seed_cats}
        quality = measure_quality(cat_ids, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters)
        quality["strategy"] = "same_category"
        quality["interest"] = interest["name"]
        results.append(quality)

    # Print summary table
    print(f"\n  {'Interest':<20s} {'Strategy':<20s} {'Vol':>6s} {'Coher':>7s} {'SeedRel':>8s} {'Divers':>7s} {'Novel':>7s}")
    print(f"  {'-' * 70}")
    for r in results:
        if "error" in r:
            continue
        print(f"  {r['interest']:<20s} {r['strategy']:<20s} {r['volume']:>6d} "
              f"{r['coherence']:>7.3f} {r['seed_relevance']:>8.3f} "
              f"{r['diversity_clusters']:>7d} {r['novelty']:>7.3f}")

    return results


# ======================================================================
# C1-R8: Parameterized curves
# ======================================================================

def run_r8(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters):
    """Precision-recall-like curves at varying thresholds."""
    print(f"\n{'=' * 70}")
    print("C1-R8: Parameterized Curves")
    print(f"{'=' * 70}")

    # Use first interest as example
    interests = get_research_interests(papers, id_to_idx, embeddings)
    interest = interests[0]  # RL for Robotics
    seed_ids = set(interest["seeds"])
    seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
    seed_emb = embeddings[seed_indices]
    seed_centroid = seed_emb.mean(axis=0, keepdims=True)

    sims = (embeddings @ seed_centroid.T).flatten()
    sorted_indices = np.argsort(sims)[::-1]

    print(f"\n  Interest: {interest['name']}")
    print(f"  {'Threshold':>10s} {'Volume':>8s} {'Coherence':>10s} {'SeedRel':>10s} {'Diversity':>10s} {'Novelty':>10s}")
    print(f"  {'-' * 60}")

    curve_points = []
    for n in [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 19252]:
        top_ids = {arxiv_ids[i] for i in sorted_indices[:n]}
        quality = measure_quality(top_ids, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters)
        if "error" not in quality:
            quality["top_n"] = n
            curve_points.append(quality)
            print(f"  {n:>10d} {quality['volume']:>8d} {quality['coherence']:>10.4f} "
                  f"{quality['seed_relevance']:>10.4f} {quality['diversity_clusters']:>10d} "
                  f"{quality['novelty']:>10.4f}")

    # Identify elbows
    if len(curve_points) >= 3:
        coherences = [p["coherence"] for p in curve_points]
        relevances = [p["seed_relevance"] for p in curve_points]

        # Find where coherence drops fastest
        coherence_drops = [coherences[i] - coherences[i+1] for i in range(len(coherences)-1)]
        max_drop_idx = np.argmax(coherence_drops)
        elbow_n = curve_points[max_drop_idx + 1]["top_n"]
        print(f"\n  Coherence elbow: ~{elbow_n} papers (steepest coherence drop)")

        relevance_drops = [relevances[i] - relevances[i+1] for i in range(len(relevances)-1)]
        max_rel_drop_idx = np.argmax(relevance_drops)
        rel_elbow_n = curve_points[max_rel_drop_idx + 1]["top_n"]
        print(f"  Relevance elbow: ~{rel_elbow_n} papers (steepest relevance drop)")

    return {"interest": interest["name"], "curve": curve_points}


# ======================================================================
# C1-R9: Adaptive learning simulation
# ======================================================================

def run_r9(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters):
    """Simulate 30 days of user behavior with adaptive model."""
    print(f"\n{'=' * 70}")
    print("C1-R9: Adaptive Learning Simulation")
    print(f"{'=' * 70}")

    interests = get_research_interests(papers, id_to_idx, embeddings)
    all_results = []

    for interest in interests[:3]:  # Test 3 interests for time
        print(f"\n  Simulating: {interest['name']}")
        seed_ids = set(interest["seeds"])
        seed_indices = [id_to_idx[aid] for aid in seed_ids if aid in id_to_idx]
        if not seed_indices:
            continue

        # The "ground truth" — papers genuinely related to this interest
        # Use embedding similarity to seeds as ground truth relevance
        seed_emb = embeddings[seed_indices]
        seed_centroid = seed_emb.mean(axis=0, keepdims=True)
        true_sims = (embeddings @ seed_centroid.T).flatten()
        true_relevant = set(arxiv_ids[i] for i in np.argsort(true_sims)[-200:])  # Top 200 = "truly relevant"

        # Adaptive model state
        positive_ids = list(seed_ids)
        negative_ids = []
        daily_metrics = []

        rng = np.random.RandomState(42)

        for day in range(30):
            # Current model: centroid of positive papers
            pos_indices = [id_to_idx[aid] for aid in positive_ids if aid in id_to_idx]
            if not pos_indices:
                break
            pos_emb = embeddings[pos_indices]
            model_centroid = pos_emb.mean(axis=0, keepdims=True)

            # Negative adjustment
            if negative_ids:
                neg_indices = [id_to_idx[aid] for aid in negative_ids if aid in id_to_idx]
                if neg_indices:
                    neg_emb = embeddings[neg_indices]
                    neg_centroid = neg_emb.mean(axis=0, keepdims=True)
                    # Move centroid away from negatives
                    model_centroid = model_centroid - 0.3 * neg_centroid
                    model_centroid /= np.linalg.norm(model_centroid) + 1e-10

            # Score all papers
            scores = (embeddings @ model_centroid.T).flatten()

            # Exclude already-seen papers
            seen = set(positive_ids) | set(negative_ids)
            for aid in seen:
                if aid in id_to_idx:
                    scores[id_to_idx[aid]] = -1

            # Surface top 20
            top_20_indices = np.argsort(scores)[-20:][::-1]
            surfaced = [arxiv_ids[i] for i in top_20_indices]

            # Simulate user behavior: papers in true_relevant → interesting (3), not (5), skip (12)
            interesting = [aid for aid in surfaced if aid in true_relevant][:3]
            not_interesting = [aid for aid in surfaced if aid not in true_relevant][:5]

            # Measure quality
            surfaced_set = set(surfaced)
            quality = measure_quality(surfaced_set, seed_ids, embeddings, arxiv_ids, id_to_idx, clusters)

            # Precision: how many surfaced are truly relevant?
            precision = len(set(surfaced) & true_relevant) / len(surfaced) if surfaced else 0

            daily_metrics.append({
                "day": day + 1,
                "precision": round(float(precision), 4),
                "seed_relevance": quality.get("seed_relevance", 0),
                "coherence": quality.get("coherence", 0),
                "positive_pool": len(positive_ids),
                "negative_pool": len(negative_ids),
            })

            # Update model with feedback
            positive_ids.extend(interesting)
            negative_ids.extend(not_interesting)

        # Report convergence
        precisions = [m["precision"] for m in daily_metrics]
        relevances = [m["seed_relevance"] for m in daily_metrics]

        # Convergence: when does precision stabilize (std of last 5 < 0.05)?
        converged_day = 30
        for d in range(5, 30):
            window = precisions[d-5:d]
            if np.std(window) < 0.05:
                converged_day = d
                break

        print(f"    Day 1  precision={precisions[0]:.3f}  relevance={relevances[0]:.3f}")
        print(f"    Day 10 precision={precisions[min(9, len(precisions)-1)]:.3f}  relevance={relevances[min(9, len(relevances)-1)]:.3f}")
        print(f"    Day 30 precision={precisions[-1]:.3f}  relevance={relevances[-1]:.3f}")
        print(f"    Converged by day: {converged_day}")
        print(f"    Improvement: {precisions[-1] - precisions[0]:+.3f} precision, "
              f"{relevances[-1] - relevances[0]:+.3f} relevance")

        all_results.append({
            "interest": interest["name"],
            "daily_metrics": daily_metrics,
            "converged_day": converged_day,
            "precision_improvement": round(float(precisions[-1] - precisions[0]), 4),
            "relevance_improvement": round(float(relevances[-1] - relevances[0]), 4),
        })

    return all_results


def main():
    print("=" * 80)
    print("C1 Round 3: Quality, Parameterization, Adaptation")
    print("=" * 80)

    papers, id_to_paper, embeddings, arxiv_ids, id_to_idx = load_all()
    print(f"Loaded {len(papers)} papers, {embeddings.shape} embeddings")

    print("\nComputing cluster assignments...")
    clusters = get_bertopic_clusters(arxiv_ids)
    n_clusters = len(set(clusters.values()))
    print(f"  {n_clusters} clusters")

    results = {}
    results["C1_R7_quality"] = run_r7(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters)
    results["C1_R8_curves"] = run_r8(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters)
    results["C1_R9_adaptive"] = run_r9(papers, id_to_paper, embeddings, arxiv_ids, id_to_idx, clusters)
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
