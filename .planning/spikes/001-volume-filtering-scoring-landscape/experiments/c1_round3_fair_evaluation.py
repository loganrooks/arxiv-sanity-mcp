"""
C1 Round 3: Fair cross-model evaluation.

Prior experiments used MiniLM-defined clusters, biasing toward MiniLM.
This experiment uses model-independent ground truth and cross-model evaluation.

Approaches:
1. Cross-model clusters: evaluate each model on BOTH cluster sets
2. Model-independent ground truth: bibliographic coupling, category co-occurrence
3. Consensus analysis: what do models agree and disagree on?

Usage:
    python c1_round3_fair_evaluation.py
"""

import json
import sqlite3
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
MINILM_EMBEDDINGS = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
B2_CACHE = DATA_DIR / "b2_openalex_cache.json"
RESULTS_PATH = DATA_DIR / "c1_round3_fair_evaluation_results.json"

N_CLUSTERS = 48
K_VALUES = [20, 50, 100, 500]


def load_all():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category, categories "
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


def compute_specter2(papers, arxiv_ids, id_to_paper):
    from sentence_transformers import SentenceTransformer
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("allenai/specter2_base", device=device)
    texts = [f"{id_to_paper.get(aid, {}).get('title', '')} [SEP] {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in arxiv_ids]
    emb = model.encode(texts, batch_size=64, convert_to_numpy=True,
                        normalize_embeddings=True, show_progress_bar=True)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()
    return emb.astype(np.float32)


def leave_one_out_recall(embeddings, arxiv_ids, id_to_idx, cluster_labels, k_values, label=""):
    """Run leave-one-out evaluation on given clusters."""
    cluster_papers = defaultdict(list)
    for i, lbl in enumerate(cluster_labels):
        cluster_papers[lbl].append(arxiv_ids[i])

    test_clusters = [(l, p) for l, p in cluster_papers.items() if 10 <= len(p) <= 2000]
    test_clusters.sort(key=lambda x: len(x[1]))
    test_clusters = test_clusters[:10]

    all_ranks = []
    for cluster_id, cluster_aids in test_clusters:
        for held_out in cluster_aids[:20]:
            seeds = [a for a in cluster_aids if a != held_out][:10]
            seed_indices = [id_to_idx[a] for a in seeds if a in id_to_idx]
            held_idx = id_to_idx.get(held_out)
            if not seed_indices or held_idx is None:
                continue
            centroid = embeddings[seed_indices].mean(axis=0, keepdims=True)
            scores = (embeddings @ centroid.T).flatten()
            rank = int((scores > scores[held_idx]).sum()) + 1
            all_ranks.append(rank)

    recall = {}
    for k in k_values:
        recall[k] = round(sum(1 for r in all_ranks if r <= k) / max(len(all_ranks), 1), 4)
    median_rank = int(np.median(all_ranks)) if all_ranks else 0
    return recall, median_rank, len(all_ranks)


# ======================================================================
# Experiment 1: Cross-model clusters
# ======================================================================

def run_cross_model(minilm_emb, specter_emb, arxiv_ids, id_to_idx):
    print("=" * 70)
    print("Experiment 1: Cross-Model Cluster Evaluation")
    print("=" * 70)
    print("  Each model evaluated on clusters defined by BOTH models.")
    print("  If a model only wins on its own clusters, the result is circular.")

    # Cluster with each model
    minilm_labels = MiniBatchKMeans(N_CLUSTERS, random_state=42, batch_size=1000).fit_predict(minilm_emb)
    specter_labels = MiniBatchKMeans(N_CLUSTERS, random_state=42, batch_size=1000).fit_predict(specter_emb)

    results = {}

    print(f"\n  {'Retriever':<15s} {'Clusters by':<15s}", end="")
    for k in K_VALUES:
        print(f"  {'R@'+str(k):>8s}", end="")
    print(f"  {'MedRank':>8s}  {'N':>5s}")
    print(f"  {'-' * (32 + 10 * len(K_VALUES) + 16)}")

    for retriever_name, retriever_emb in [("MiniLM", minilm_emb), ("SPECTER2", specter_emb)]:
        for cluster_name, cluster_labels in [("MiniLM", minilm_labels), ("SPECTER2", specter_labels)]:
            recall, med_rank, n = leave_one_out_recall(
                retriever_emb, arxiv_ids, id_to_idx, cluster_labels, K_VALUES
            )
            key = f"{retriever_name}_on_{cluster_name}_clusters"
            results[key] = {"recall": recall, "median_rank": med_rank, "n": n}

            print(f"  {retriever_name:<15s} {cluster_name:<15s}", end="")
            for k in K_VALUES:
                print(f"  {recall[k]:>8.1%}", end="")
            print(f"  {med_rank:>8d}  {n:>5d}")

    # Analysis
    print(f"\n  Analysis:")
    # Does MiniLM win on SPECTER2 clusters too?
    m_on_s = results["MiniLM_on_SPECTER2_clusters"]["recall"][100]
    s_on_s = results["SPECTER2_on_SPECTER2_clusters"]["recall"][100]
    m_on_m = results["MiniLM_on_MiniLM_clusters"]["recall"][100]
    s_on_m = results["SPECTER2_on_MiniLM_clusters"]["recall"][100]

    print(f"    MiniLM on MiniLM clusters:   R@100={m_on_m:.1%}")
    print(f"    MiniLM on SPECTER2 clusters: R@100={m_on_s:.1%}")
    print(f"    SPECTER2 on SPECTER2 clusters: R@100={s_on_s:.1%}")
    print(f"    SPECTER2 on MiniLM clusters:   R@100={s_on_m:.1%}")

    if m_on_m > s_on_m and m_on_s > s_on_s:
        print(f"    → MiniLM wins on BOTH cluster sets — not just circular bias")
    elif m_on_m > s_on_m and s_on_s > m_on_s:
        print(f"    → Each model wins on its own clusters — they capture DIFFERENT things")
        print(f"    → Neither is 'better' — they measure different dimensions of similarity")
    elif s_on_s > m_on_s and s_on_m > m_on_m:
        print(f"    → SPECTER2 wins on BOTH cluster sets")
    else:
        print(f"    → Mixed results — no clear winner")

    return results


# ======================================================================
# Experiment 2: Model-independent ground truth
# ======================================================================

def run_model_independent(minilm_emb, specter_emb, arxiv_ids, id_to_idx, id_to_paper):
    print(f"\n{'=' * 70}")
    print("Experiment 2: Model-Independent Ground Truth")
    print("=" * 70)
    print("  Ground truth defined by metadata, not embeddings.")

    results = {}

    # GT1: Category co-membership — papers sharing multiple categories are related
    print("\n  GT1: Category co-membership")
    cat_groups = defaultdict(set)
    for p_idx, aid in enumerate(arxiv_ids):
        p = id_to_paper.get(aid, {})
        cats = frozenset(c.strip() for c in (p.get("categories") or "").split() if c.strip())
        if len(cats) >= 2:
            cat_groups[cats].add(aid)

    # Find groups with 10+ papers sharing the exact same category set
    test_groups = [(cats, aids) for cats, aids in cat_groups.items() if 10 <= len(aids) <= 200]
    test_groups.sort(key=lambda x: len(x[1]), reverse=True)
    test_groups = test_groups[:10]

    if test_groups:
        for model_name, emb in [("MiniLM", minilm_emb), ("SPECTER2", specter_emb)]:
            all_ranks = []
            for cats, group_aids in test_groups:
                group_aids = list(group_aids)
                for held_out in group_aids[:15]:
                    seeds = [a for a in group_aids if a != held_out][:10]
                    seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
                    held_idx = id_to_idx.get(held_out)
                    if not seed_idx or held_idx is None:
                        continue
                    centroid = emb[seed_idx].mean(axis=0, keepdims=True)
                    scores = (emb @ centroid.T).flatten()
                    rank = int((scores > scores[held_idx]).sum()) + 1
                    all_ranks.append(rank)

            recall_100 = sum(1 for r in all_ranks if r <= 100) / max(len(all_ranks), 1)
            med_rank = int(np.median(all_ranks)) if all_ranks else 0
            results[f"category_comembership_{model_name}"] = {
                "recall_at_100": round(recall_100, 4),
                "median_rank": med_rank,
                "n": len(all_ranks),
            }
            print(f"    {model_name:<15s} R@100={recall_100:.1%}  MedRank={med_rank}  (n={len(all_ranks)})")
    else:
        print("    No category co-membership groups of sufficient size found")

    # GT2: Bibliographic coupling from OpenAlex
    print("\n  GT2: Bibliographic coupling groups")
    if Path(B2_CACHE).exists():
        with open(B2_CACHE) as f:
            cache = json.load(f)

        refs = {}
        for aid, data in cache.items():
            if isinstance(data, dict) and "error" not in data:
                ref_works = data.get("referenced_works", [])
                if ref_works:
                    refs[aid] = set(ref_works)

        # Find papers with high bibliographic coupling (Jaccard > 0.3)
        ref_aids = list(refs.keys())
        bc_groups = []
        checked = set()
        for i, aid1 in enumerate(ref_aids[:200]):  # Limit for speed
            if aid1 in checked:
                continue
            group = {aid1}
            for aid2 in ref_aids[i+1:200]:
                if refs[aid1] and refs[aid2]:
                    j = len(refs[aid1] & refs[aid2]) / len(refs[aid1] | refs[aid2])
                    if j >= 0.2:
                        group.add(aid2)
            if len(group) >= 5:
                bc_groups.append(group)
                checked |= group

        if bc_groups:
            for model_name, emb in [("MiniLM", minilm_emb), ("SPECTER2", specter_emb)]:
                all_ranks = []
                for group_aids in bc_groups[:10]:
                    group_aids = list(group_aids)
                    for held_out in group_aids[:10]:
                        seeds = [a for a in group_aids if a != held_out][:5]
                        seed_idx = [id_to_idx[a] for a in seeds if a in id_to_idx]
                        held_idx = id_to_idx.get(held_out)
                        if not seed_idx or held_idx is None:
                            continue
                        centroid = emb[seed_idx].mean(axis=0, keepdims=True)
                        scores = (emb @ centroid.T).flatten()
                        rank = int((scores > scores[held_idx]).sum()) + 1
                        all_ranks.append(rank)

                recall_100 = sum(1 for r in all_ranks if r <= 100) / max(len(all_ranks), 1)
                med_rank = int(np.median(all_ranks)) if all_ranks else 0
                results[f"bibcoupling_{model_name}"] = {
                    "recall_at_100": round(recall_100, 4),
                    "median_rank": med_rank,
                    "n": len(all_ranks),
                }
                print(f"    {model_name:<15s} R@100={recall_100:.1%}  MedRank={med_rank}  (n={len(all_ranks)})")
        else:
            print("    No bibliographic coupling groups found")
    else:
        print("    OpenAlex cache not available")

    return results


# ======================================================================
# Experiment 3: Consensus analysis
# ======================================================================

def run_consensus(minilm_emb, specter_emb, arxiv_ids, id_to_idx, id_to_paper):
    print(f"\n{'=' * 70}")
    print("Experiment 3: Consensus Analysis")
    print("=" * 70)
    print("  Papers ranked highly by BOTH models are more likely genuinely related.")

    # Pick 10 seed papers
    rng = np.random.RandomState(42)
    seed_indices = rng.choice(len(arxiv_ids), 10, replace=False)

    overlap_at_k = {k: [] for k in K_VALUES}
    consensus_quality = []

    for seed_idx in seed_indices:
        seed_aid = arxiv_ids[seed_idx]

        # MiniLM top-K
        m_scores = (minilm_emb[seed_idx:seed_idx+1] @ minilm_emb.T).flatten()
        m_scores[seed_idx] = -1  # Exclude self

        # SPECTER2 top-K
        s_scores = (specter_emb[seed_idx:seed_idx+1] @ specter_emb.T).flatten()
        s_scores[seed_idx] = -1

        for k in K_VALUES:
            m_top = set(np.argsort(m_scores)[-k:])
            s_top = set(np.argsort(s_scores)[-k:])
            overlap = len(m_top & s_top) / k
            overlap_at_k[k].append(overlap)

        # Consensus set (top-100 from both) vs disagreement sets
        k = 100
        m_top100 = set(np.argsort(m_scores)[-k:])
        s_top100 = set(np.argsort(s_scores)[-k:])
        consensus = m_top100 & s_top100
        m_only = m_top100 - s_top100
        s_only = s_top100 - m_top100

        # Quality proxy: do consensus papers share more categories with seed?
        seed_cats = set((id_to_paper.get(seed_aid, {}).get("categories") or "").split())
        if seed_cats:
            def cat_overlap(paper_set):
                overlaps = []
                for idx in paper_set:
                    aid = arxiv_ids[idx]
                    p_cats = set((id_to_paper.get(aid, {}).get("categories") or "").split())
                    if p_cats:
                        overlaps.append(len(seed_cats & p_cats) / len(seed_cats | p_cats))
                return np.mean(overlaps) if overlaps else 0

            consensus_quality.append({
                "seed": seed_aid,
                "consensus_cat_overlap": round(cat_overlap(consensus), 4),
                "minilm_only_cat_overlap": round(cat_overlap(m_only), 4),
                "specter_only_cat_overlap": round(cat_overlap(s_only), 4),
                "consensus_size": len(consensus),
            })

    # Report
    print(f"\n  Cross-model overlap at top-K:")
    for k in K_VALUES:
        avg_overlap = np.mean(overlap_at_k[k])
        print(f"    Top-{k}: {avg_overlap:.1%} overlap")

    if consensus_quality:
        avg_cons = np.mean([q["consensus_cat_overlap"] for q in consensus_quality])
        avg_m_only = np.mean([q["minilm_only_cat_overlap"] for q in consensus_quality])
        avg_s_only = np.mean([q["specter_only_cat_overlap"] for q in consensus_quality])
        avg_cons_size = np.mean([q["consensus_size"] for q in consensus_quality])

        print(f"\n  Category overlap with seed paper (model-independent quality proxy):")
        print(f"    Consensus papers (both models agree): {avg_cons:.4f}  (n≈{avg_cons_size:.0f})")
        print(f"    MiniLM-only papers:                   {avg_m_only:.4f}")
        print(f"    SPECTER2-only papers:                 {avg_s_only:.4f}")

        if avg_cons > avg_m_only and avg_cons > avg_s_only:
            print(f"    → Consensus papers are more category-similar to seed than either model alone")
            print(f"    → Both models contribute genuine signal — combining is better than choosing")
        elif avg_m_only > avg_s_only:
            print(f"    → MiniLM-only papers are more category-similar — MiniLM captures category structure better")
        else:
            print(f"    → SPECTER2-only papers are more category-similar — SPECTER2 captures category structure better")

    return {
        "overlap_at_k": {str(k): round(float(np.mean(overlap_at_k[k])), 4) for k in K_VALUES},
        "consensus_quality": consensus_quality,
    }


def main():
    print("=" * 80)
    print("C1 Round 3: Fair Cross-Model Evaluation")
    print("=" * 80)

    papers, id_to_paper, minilm_emb, arxiv_ids, id_to_idx = load_all()
    print(f"Papers: {len(papers)}, Embeddings: {minilm_emb.shape}")

    print("\nComputing SPECTER2 embeddings...")
    specter_emb = compute_specter2(papers, arxiv_ids, id_to_paper)
    print(f"SPECTER2: {specter_emb.shape}")

    results = {}
    results["cross_model_clusters"] = run_cross_model(minilm_emb, specter_emb, arxiv_ids, id_to_idx)
    results["model_independent_gt"] = run_model_independent(minilm_emb, specter_emb, arxiv_ids, id_to_idx, id_to_paper)
    results["consensus"] = run_consensus(minilm_emb, specter_emb, arxiv_ids, id_to_idx, id_to_paper)

    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

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
