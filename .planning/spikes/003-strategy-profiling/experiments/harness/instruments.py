"""
Quantitative detection instruments for recommendation strategy profiling.

These instruments detect PROPERTIES of recommendation sets. They produce
readings -- numbers that track mathematical relationships. They do NOT
tell us whether a recommendation set is good, useful, or what a researcher
would want. That interpretation requires qualitative review.

Each instrument returns a dict:
    {"value": float, "detail": {...optional extra data...}}

The "interpretation" field is NOT populated here -- it comes from
qualitative review in later waves.

Metric tensions (by design, not by accident):
    - Seed proximity vs novelty: inversely correlated
    - Coherence vs diversity: inversely correlated
    No strategy should maximize all instruments simultaneously.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


def leave_one_out_mrr(
    strategy,
    cluster_papers: list[str],
    all_paper_ids: list[str],
    top_k: int = 20,
) -> dict:
    """Hold out each paper in cluster, use rest as seeds, measure reciprocal rank.

    For each paper in cluster_papers:
      1. Remove it from the cluster set
      2. Use the remaining cluster papers as seeds
      3. Run the strategy
      4. Find the rank of the held-out paper in the recommendations
      5. Compute reciprocal rank (1/rank, or 0 if not found in top_k)

    This measures whether a strategy can RECOVER a paper from a
    known-coherent set. It rewards convergence toward known good papers
    and is blind to genuinely novel discovery.

    Args:
        strategy: Implements RecommendationStrategy protocol.
        cluster_papers: List of arxiv_ids that form a coherent group.
        all_paper_ids: Full corpus paper IDs (for validating results).
        top_k: How deep to search for the held-out paper.

    Returns:
        {"value": float (mean MRR), "detail": {"per_paper": [...], "n_evaluated": int}}
    """
    if len(cluster_papers) < 3:
        return {"value": 0.0, "detail": {"error": "too few cluster papers", "n_evaluated": 0}}

    reciprocal_ranks = []
    per_paper = []

    for i, held_out in enumerate(cluster_papers):
        seeds = [p for j, p in enumerate(cluster_papers) if j != i]

        # Use more seeds than just 1 for stability, but cap at 10
        seed_subset = seeds[:10]

        recs = strategy.recommend(seed_subset, top_k=top_k)
        rec_ids = [r[0] for r in recs]

        if held_out in rec_ids:
            rank = rec_ids.index(held_out) + 1
            rr = 1.0 / rank
        else:
            rank = None
            rr = 0.0

        reciprocal_ranks.append(rr)
        per_paper.append({"held_out": held_out, "rank": rank, "rr": rr})

    mean_mrr = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0

    return {
        "value": mean_mrr,
        "detail": {
            "per_paper": per_paper,
            "n_evaluated": len(reciprocal_ranks),
            "found_fraction": sum(1 for rr in reciprocal_ranks if rr > 0) / max(len(reciprocal_ranks), 1),
        },
    }


def seed_proximity(
    recommended_ids: list[str],
    seed_ids: list[str],
    embeddings: np.ndarray,
    id_to_idx: dict[str, int],
) -> dict:
    """Mean cosine similarity between recommendations and seed centroid.

    Measures mathematical similarity between what the strategy recommends
    and what the user expressed interest in. High values mean recommendations
    stay close to seeds; low values mean they explore.

    Note: This instrument uses whichever embedding space is provided.
    When evaluating embedding-based strategies on their own embeddings,
    this is partially circular. Cross-model evaluation is more informative.

    Args:
        recommended_ids: IDs of recommended papers.
        seed_ids: IDs of seed papers.
        embeddings: Pre-computed embeddings matrix (n_papers x dim), assumed normalized.
        id_to_idx: Mapping from arxiv_id to row index in embeddings.

    Returns:
        {"value": float (mean cosine to centroid), "detail": {"per_rec": [...]}}
    """
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        return {"value": 0.0, "detail": {"error": "no valid seed indices"}}

    # Compute seed centroid (normalize for cosine)
    centroid = embeddings[seed_indices].mean(axis=0)
    centroid_norm = np.linalg.norm(centroid)
    if centroid_norm < 1e-10:
        return {"value": 0.0, "detail": {"error": "zero centroid"}}
    centroid = centroid / centroid_norm

    rec_indices = [id_to_idx[rid] for rid in recommended_ids if rid in id_to_idx]
    if not rec_indices:
        return {"value": 0.0, "detail": {"error": "no valid rec indices"}}

    # Cosine similarity (embeddings are normalized, so dot product = cosine)
    rec_embeddings = embeddings[rec_indices]
    similarities = rec_embeddings @ centroid

    per_rec = [
        {"arxiv_id": recommended_ids[i], "cosine_to_centroid": float(similarities[j])}
        for j, i in enumerate(
            [i for i, rid in enumerate(recommended_ids) if rid in id_to_idx]
        )
    ]

    return {
        "value": float(np.mean(similarities)),
        "detail": {
            "per_rec": per_rec,
            "std": float(np.std(similarities)),
            "min": float(np.min(similarities)),
            "max": float(np.max(similarities)),
        },
    }


def topical_coherence(
    recommended_ids: list[str],
    embeddings: np.ndarray,
    id_to_idx: dict[str, int],
) -> dict:
    """Mean pairwise cosine similarity within the recommendation set.

    Measures internal consistency. High coherence means the recommendations
    form a tight cluster in embedding space. This can mean "focused" or
    "echo chamber" depending on context -- interpretation requires
    qualitative review.

    Args:
        recommended_ids: IDs of recommended papers.
        embeddings: Pre-computed embeddings matrix, assumed normalized.
        id_to_idx: Mapping from arxiv_id to row index.

    Returns:
        {"value": float (mean pairwise cosine), "detail": {...}}
    """
    rec_indices = [id_to_idx[rid] for rid in recommended_ids if rid in id_to_idx]
    if len(rec_indices) < 2:
        return {"value": 0.0, "detail": {"error": "fewer than 2 valid recs"}}

    rec_embs = embeddings[rec_indices]
    # Pairwise cosine = dot product for normalized vectors
    sim_matrix = rec_embs @ rec_embs.T

    # Extract upper triangle (exclude diagonal)
    n = len(rec_indices)
    triu_indices = np.triu_indices(n, k=1)
    pairwise_sims = sim_matrix[triu_indices]

    return {
        "value": float(np.mean(pairwise_sims)),
        "detail": {
            "std": float(np.std(pairwise_sims)),
            "min": float(np.min(pairwise_sims)),
            "max": float(np.max(pairwise_sims)),
            "n_pairs": len(pairwise_sims),
        },
    }


def cluster_diversity(
    recommended_ids: list[str],
    paper_to_cluster: dict[str, int],
) -> dict:
    """Number of distinct BERTopic clusters represented in recommendations.

    Measures whether recommendations span multiple topical regions.
    High diversity can mean breadth (good) or noise (bad) depending
    on context.

    Args:
        recommended_ids: IDs of recommended papers.
        paper_to_cluster: Mapping from arxiv_id to cluster/topic ID.
            Papers not in the mapping (outliers) get cluster -1.

    Returns:
        {"value": float (distinct cluster count), "detail": {"clusters": {...}}}
    """
    cluster_counts: dict[int, int] = {}
    unmapped = 0

    for rid in recommended_ids:
        cluster = paper_to_cluster.get(rid, -1)
        cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1
        if cluster == -1:
            unmapped += 1

    # Count distinct non-outlier clusters
    distinct = len([c for c in cluster_counts if c != -1])

    return {
        "value": float(distinct),
        "detail": {
            "cluster_distribution": cluster_counts,
            "unmapped_count": unmapped,
            "total_recs": len(recommended_ids),
        },
    }


def novelty(
    recommended_ids: list[str],
    seed_ids: list[str],
    paper_to_cluster: dict[str, int],
) -> dict:
    """Fraction of recommended papers NOT in the same cluster as any seed.

    Measures whether recommendations leave the seeds' immediate
    neighborhood. Novelty without relevance is noise; novelty with
    relevance is discovery. This instrument cannot distinguish between them.

    Args:
        recommended_ids: IDs of recommended papers.
        seed_ids: IDs of seed papers.
        paper_to_cluster: Mapping from arxiv_id to cluster/topic ID.

    Returns:
        {"value": float (fraction novel), "detail": {...}}
    """
    seed_clusters = set()
    for sid in seed_ids:
        c = paper_to_cluster.get(sid, -1)
        if c != -1:
            seed_clusters.add(c)

    if not seed_clusters:
        # All seeds are outliers; can't compute meaningful novelty
        return {"value": 1.0, "detail": {"error": "all seeds are outliers", "seed_clusters": []}}

    novel_count = 0
    in_seed_cluster_count = 0
    per_rec = []

    for rid in recommended_ids:
        rec_cluster = paper_to_cluster.get(rid, -1)
        is_novel = rec_cluster == -1 or rec_cluster not in seed_clusters
        if is_novel:
            novel_count += 1
        else:
            in_seed_cluster_count += 1
        per_rec.append({"arxiv_id": rid, "cluster": rec_cluster, "novel": is_novel})

    fraction = novel_count / max(len(recommended_ids), 1)

    return {
        "value": float(fraction),
        "detail": {
            "novel_count": novel_count,
            "in_seed_cluster_count": in_seed_cluster_count,
            "seed_clusters": sorted(seed_clusters),
            "per_rec": per_rec,
        },
    }


def category_surprise(
    recommended_ids: list[str],
    seed_ids: list[str],
    paper_categories: dict[str, str],
) -> dict:
    """Fraction of recommended papers from a different primary category than seeds.

    Measures whether recommendations cross arXiv category boundaries.
    cs.LG -> cs.CV is a small step; cs.LG -> math.CO is a large one.
    This instrument treats them equally -- it measures boundary-crossing,
    not the semantic distance of the crossing.

    Args:
        recommended_ids: IDs of recommended papers.
        seed_ids: IDs of seed papers.
        paper_categories: Mapping from arxiv_id to primary_category string.

    Returns:
        {"value": float (fraction surprising), "detail": {...}}
    """
    seed_categories = set()
    for sid in seed_ids:
        cat = paper_categories.get(sid)
        if cat:
            seed_categories.add(cat)

    if not seed_categories:
        return {"value": 1.0, "detail": {"error": "no seed categories found"}}

    surprise_count = 0
    same_count = 0
    category_distribution: dict[str, int] = {}

    for rid in recommended_ids:
        rec_cat = paper_categories.get(rid, "unknown")
        category_distribution[rec_cat] = category_distribution.get(rec_cat, 0) + 1
        if rec_cat not in seed_categories:
            surprise_count += 1
        else:
            same_count += 1

    fraction = surprise_count / max(len(recommended_ids), 1)

    return {
        "value": float(fraction),
        "detail": {
            "surprise_count": surprise_count,
            "same_category_count": same_count,
            "seed_categories": sorted(seed_categories),
            "rec_category_distribution": category_distribution,
        },
    }


def coverage(
    recommended_ids: list[str],
    cluster_papers: list[str],
) -> dict:
    """Fraction of cluster papers that appear in recommendations.

    Measures what fraction of a pre-defined "relevant" set the strategy
    finds. "Relevant" here means cluster membership, which is itself
    a mathematical proxy.

    Args:
        recommended_ids: IDs of recommended papers.
        cluster_papers: IDs of papers in the relevant cluster(s).

    Returns:
        {"value": float (fraction covered), "detail": {...}}
    """
    if not cluster_papers:
        return {"value": 0.0, "detail": {"error": "empty cluster"}}

    rec_set = set(recommended_ids)
    found = [p for p in cluster_papers if p in rec_set]
    fraction = len(found) / len(cluster_papers)

    return {
        "value": float(fraction),
        "detail": {
            "found_count": len(found),
            "cluster_size": len(cluster_papers),
            "found_ids": found,
        },
    }


def run_all_instruments(
    strategy,
    recommended_ids: list[str],
    seed_ids: list[str],
    cluster_papers: list[str],
    all_paper_ids: list[str],
    embeddings: np.ndarray,
    id_to_idx: dict[str, int],
    paper_to_cluster: dict[str, int],
    paper_categories: dict[str, str],
    top_k: int = 20,
    run_loo: bool = True,
) -> dict:
    """Run all 7 instruments on a single recommendation set.

    Args:
        strategy: The strategy (needed for leave-one-out).
        recommended_ids: IDs the strategy recommended.
        seed_ids: IDs used as seeds.
        cluster_papers: Papers in seed-relevant clusters (for coverage + LOO).
        all_paper_ids: Full corpus IDs.
        embeddings: Pre-computed embeddings (normalized).
        id_to_idx: ID-to-index mapping.
        paper_to_cluster: Paper-to-cluster mapping.
        paper_categories: Paper-to-primary-category mapping.
        top_k: Depth for LOO evaluation.
        run_loo: Whether to run leave-one-out (expensive). Default True.

    Returns:
        Dict mapping instrument name to its result dict.
    """
    results = {}

    if run_loo and len(cluster_papers) >= 3:
        results["leave_one_out_mrr"] = leave_one_out_mrr(
            strategy, cluster_papers, all_paper_ids, top_k=top_k
        )
    else:
        results["leave_one_out_mrr"] = {"value": None, "detail": {"skipped": True}}

    results["seed_proximity"] = seed_proximity(
        recommended_ids, seed_ids, embeddings, id_to_idx
    )
    results["topical_coherence"] = topical_coherence(
        recommended_ids, embeddings, id_to_idx
    )
    results["cluster_diversity"] = cluster_diversity(
        recommended_ids, paper_to_cluster
    )
    results["novelty"] = novelty(
        recommended_ids, seed_ids, paper_to_cluster
    )
    results["category_surprise"] = category_surprise(
        recommended_ids, seed_ids, paper_categories
    )
    results["coverage"] = coverage(
        recommended_ids, cluster_papers
    )

    return results
