"""
C1 Round 2: B1-informed filtering strategies + importance proxy sensitivity.

C1-R1: Keyword filtering
C1-R2: Author-based filtering
C1-R3: SVM classifier (arxiv-sanity-lite approach)
C1-R4: Hybrid union
C1-R5: SPECTER2 embedding filter
C1-R6: Importance proxy sensitivity

Usage:
    python c1_round2_filtering.py
"""

import json
import re
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
MINILM_EMBEDDINGS = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
B2_CACHE = DATA_DIR / "b2_openalex_cache.json"
RESULTS_PATH = DATA_DIR / "c1_round2_results.json"


def load_papers():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def load_enrichment():
    with open(B2_CACHE) as f:
        cache = json.load(f)
    return {aid: data for aid, data in cache.items()
            if isinstance(data, dict) and "error" not in data}


def get_importance_proxies(enrichment):
    """Build multiple importance proxies."""
    proxies = {}

    # Proxy 1: citation count
    citations = {aid: data.get("cited_by_count", 0) for aid, data in enrichment.items()}

    # Proxy 2: reference count
    refs = {aid: len(data.get("referenced_works", [])) for aid, data in enrichment.items()}

    # Proxy 3: FWCI
    fwci = {}
    for aid, data in enrichment.items():
        f = data.get("fwci")
        if f is not None:
            fwci[aid] = f
        else:
            fwci[aid] = 0

    proxies["citations"] = citations
    proxies["references"] = refs
    proxies["fwci"] = fwci
    return proxies


def get_important_ids(proxy_values, percentile=80):
    """Get IDs above the given percentile threshold."""
    vals = list(proxy_values.values())
    threshold = np.percentile(vals, percentile)
    threshold = max(threshold, np.percentile(vals, 50))  # At least median
    return {aid for aid, v in proxy_values.items() if v >= threshold}


def coverage_stats(filtered_ids, important_ids, total_ids):
    """Compute coverage, regret, efficiency."""
    covered = len(filtered_ids & important_ids)
    coverage = covered / len(important_ids) if important_ids else 0
    volume_frac = len(filtered_ids) / len(total_ids) if total_ids else 0
    efficiency = coverage / volume_frac if volume_frac > 0 else 0
    return {
        "volume": len(filtered_ids),
        "volume_fraction": round(volume_frac, 4),
        "coverage": round(coverage, 4),
        "regret": round(1 - coverage, 4),
        "efficiency": round(efficiency, 4),
    }


def run_c1_r1(papers, enriched_ids, important_ids):
    """Keyword-based filtering."""
    print("\n--- C1-R1: Keyword filtering ---")

    id_to_paper = {p["arxiv_id"]: p for p in papers}

    keyword_sets = [
        ("RL+robotics", ["reinforcement learning", "robot", "manipulation", "control"]),
        ("LLM+reasoning", ["language model", "reasoning", "chain of thought", "prompt"]),
        ("diffusion+generation", ["diffusion", "generation", "image", "synthesis"]),
        ("graph+network", ["graph neural", "node", "edge", "relational"]),
        ("security+privacy", ["privacy", "federated", "attack", "adversarial", "security"]),
    ]

    results = []
    for name, keywords in keyword_sets:
        matched = set()
        for aid in enriched_ids:
            p = id_to_paper.get(aid, {})
            text = f"{p.get('title', '')} {p.get('abstract', '')}".lower()
            if any(kw in text for kw in keywords):
                matched.add(aid)

        stats = coverage_stats(matched, important_ids, enriched_ids)
        results.append({"keyword_set": name, "keywords": keywords, **stats})
        print(f"  {name:25s}  vol={stats['volume']:>4d} ({stats['volume_fraction']:.1%})  "
              f"cov={stats['coverage']:.1%}  eff={stats['efficiency']:.2f}x")

    return results


def run_c1_r2(papers, enriched_ids, important_ids):
    """Author-based filtering."""
    print("\n--- C1-R2: Author filtering ---")

    # Count author appearances across full corpus
    author_paper_count = Counter()
    paper_authors = defaultdict(set)
    for p in papers:
        for author in (p.get("authors_text") or "").split(","):
            author = author.strip()
            if author:
                author_paper_count[author] += 1
                paper_authors[p["arxiv_id"]].add(author)

    # Strategy 1: prolific authors (>= 5 papers)
    prolific = {a for a, c in author_paper_count.items() if c >= 5}
    prolific_papers = {
        aid for aid in enriched_ids
        if paper_authors.get(aid, set()) & prolific
    }

    # Strategy 2: top 10 most prolific as "followed"
    top10 = {a for a, _ in author_paper_count.most_common(10)}
    followed_papers = {
        aid for aid in enriched_ids
        if paper_authors.get(aid, set()) & top10
    }

    results = []
    for name, filtered in [("prolific (>=5 papers)", prolific_papers),
                            ("top 10 followed", followed_papers)]:
        stats = coverage_stats(filtered, important_ids, enriched_ids)
        results.append({"strategy": name, **stats})
        print(f"  {name:25s}  vol={stats['volume']:>4d} ({stats['volume_fraction']:.1%})  "
              f"cov={stats['coverage']:.1%}  eff={stats['efficiency']:.2f}x")

    return results


def run_c1_r3(papers, enriched_ids, important_ids):
    """SVM classifier filtering (arxiv-sanity-lite approach)."""
    print("\n--- C1-R3: SVM classifier filtering ---")

    id_to_paper = {p["arxiv_id"]: p for p in papers}
    enriched_list = sorted(enriched_ids)

    # Build TF-IDF
    texts = [f"{id_to_paper.get(aid, {}).get('title', '')}. {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in enriched_list]
    vectorizer = TfidfVectorizer(max_features=10000, sublinear_tf=True, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)

    # Run 5 trials with different random "user libraries"
    rng = np.random.RandomState(42)
    trial_results = []

    for trial in range(5):
        # Simulate user library: 20 random papers as positive
        positive_indices = rng.choice(len(enriched_list), size=20, replace=False)
        labels = np.zeros(len(enriched_list))
        labels[positive_indices] = 1

        # Train SVM
        try:
            clf = LinearSVC(C=0.01, class_weight='balanced', max_iter=10000)
            clf.fit(tfidf, labels)
            scores = clf.decision_function(tfidf)
        except Exception as e:
            print(f"  Trial {trial}: SVM failed — {e}")
            continue

        # Score-based filtering at different thresholds
        for pct_label, pct in [("top50%", 50), ("top20%", 20), ("top10%", 10)]:
            threshold = np.percentile(scores, 100 - pct)
            filtered = {enriched_list[i] for i, s in enumerate(scores) if s >= threshold}
            stats = coverage_stats(filtered, important_ids, enriched_ids)
            trial_results.append({"trial": trial, "threshold": pct_label, **stats})

    # Average across trials
    aggregated = defaultdict(lambda: {"coverages": [], "volumes": [], "efficiencies": []})
    for tr in trial_results:
        key = tr["threshold"]
        aggregated[key]["coverages"].append(tr["coverage"])
        aggregated[key]["volumes"].append(tr["volume_fraction"])
        aggregated[key]["efficiencies"].append(tr["efficiency"])

    results = []
    for key, vals in aggregated.items():
        avg_cov = np.mean(vals["coverages"])
        avg_vol = np.mean(vals["volumes"])
        avg_eff = np.mean(vals["efficiencies"])
        results.append({
            "threshold": key,
            "avg_coverage": round(float(avg_cov), 4),
            "avg_volume_fraction": round(float(avg_vol), 4),
            "avg_efficiency": round(float(avg_eff), 4),
            "coverage_std": round(float(np.std(vals["coverages"])), 4),
        })
        print(f"  SVM {key:8s}  vol={avg_vol:.1%}  cov={avg_cov:.1%}±{np.std(vals['coverages']):.1%}  "
              f"eff={avg_eff:.2f}x")

    return results


def run_c1_r4(papers, enriched_ids, important_ids, minilm_emb, arxiv_ids):
    """Hybrid union filtering."""
    print("\n--- C1-R4: Hybrid union ---")

    id_to_paper = {p["arxiv_id"]: p for p in papers}
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}

    # Component 1: keyword (use broadest keyword set)
    keyword_papers = set()
    keywords = ["language model", "reinforcement learning", "diffusion", "graph neural",
                "transformer", "attention", "optimization", "privacy"]
    for aid in enriched_ids:
        p = id_to_paper.get(aid, {})
        text = f"{p.get('title', '')} {p.get('abstract', '')}".lower()
        if any(kw in text for kw in keywords):
            keyword_papers.add(aid)

    # Component 2: embedding top 50%
    enriched_with_idx = [(aid, id_to_idx[aid]) for aid in enriched_ids if aid in id_to_idx]
    if enriched_with_idx:
        indices = [idx for _, idx in enriched_with_idx]
        emb_subset = minilm_emb[indices]
        centroid = emb_subset.mean(axis=0, keepdims=True)
        sims = (emb_subset @ centroid.T).flatten()
        median_sim = np.median(sims)
        embedding_papers = {aid for (aid, _), sim in zip(enriched_with_idx, sims) if sim >= median_sim}
    else:
        embedding_papers = set()

    # Component 3: prolific authors
    author_counts = Counter()
    paper_authors = defaultdict(set)
    for p in papers:
        for a in (p.get("authors_text") or "").split(","):
            a = a.strip()
            if a:
                author_counts[a] += 1
                paper_authors[p["arxiv_id"]].add(a)
    prolific = {a for a, c in author_counts.items() if c >= 5}
    author_papers = {aid for aid in enriched_ids if paper_authors.get(aid, set()) & prolific}

    # Union
    union = keyword_papers | embedding_papers | author_papers
    # Intersection (all three agree)
    intersection = keyword_papers & embedding_papers & author_papers

    results = []
    for name, filtered in [
        ("keyword only", keyword_papers),
        ("embedding top50%", embedding_papers),
        ("prolific authors", author_papers),
        ("union (any)", union),
        ("intersection (all)", intersection),
    ]:
        stats = coverage_stats(filtered, important_ids, enriched_ids)
        results.append({"strategy": name, **stats})
        print(f"  {name:25s}  vol={stats['volume']:>4d} ({stats['volume_fraction']:.1%})  "
              f"cov={stats['coverage']:.1%}  eff={stats['efficiency']:.2f}x")

    return results


def run_c1_r5(papers, enriched_ids, important_ids, arxiv_ids):
    """SPECTER2 embedding filter comparison."""
    print("\n--- C1-R5: SPECTER2 vs MiniLM embedding filter ---")

    # Check if SPECTER2 embeddings exist (from QV3)
    # If not, compute just the subset
    specter_path = SPIKE002_DATA / "qv3_specter2_results.json"
    if not specter_path.exists():
        print("  SPECTER2 results not available — skipping")
        return {"skipped": True, "reason": "QV3 not run"}

    # We need the actual SPECTER2 embeddings, but QV3 didn't save them.
    # Recompute for the enriched subset.
    id_to_paper = {p["arxiv_id"]: p for p in papers}
    enriched_list = sorted(enriched_ids)

    # Use MiniLM for comparison (we have those)
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}

    enriched_with_idx = [(aid, id_to_idx[aid]) for aid in enriched_list if aid in id_to_idx]
    if not enriched_with_idx:
        return {"skipped": True, "reason": "no embeddings for enriched papers"}

    indices = [idx for _, idx in enriched_with_idx]
    aids = [aid for aid, _ in enriched_with_idx]
    minilm_subset = minilm_emb[indices]

    # Compute SPECTER2 for this subset
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer("allenai/specter2_base", device=device)

    texts = [f"{id_to_paper.get(aid, {}).get('title', '')} [SEP] {id_to_paper.get(aid, {}).get('abstract', '')}"
             for aid in aids]
    specter_subset = model.encode(texts, batch_size=64, convert_to_numpy=True,
                                   normalize_embeddings=True, show_progress_bar=False)
    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    # MiniLM top 50%
    minilm_centroid = minilm_subset.mean(axis=0, keepdims=True)
    minilm_sims = (minilm_subset @ minilm_centroid.T).flatten()
    minilm_filtered = {aids[i] for i, s in enumerate(minilm_sims) if s >= np.median(minilm_sims)}

    # SPECTER2 top 50%
    specter_centroid = specter_subset.mean(axis=0, keepdims=True)
    specter_sims = (specter_subset @ specter_centroid.T).flatten()
    specter_filtered = {aids[i] for i, s in enumerate(specter_sims) if s >= np.median(specter_sims)}

    # Compare
    overlap = len(minilm_filtered & specter_filtered)
    jaccard = overlap / len(minilm_filtered | specter_filtered) if (minilm_filtered | specter_filtered) else 0

    results = []
    for name, filtered in [("MiniLM top50%", minilm_filtered), ("SPECTER2 top50%", specter_filtered)]:
        stats = coverage_stats(filtered, important_ids, enriched_ids)
        results.append({"strategy": name, **stats})
        print(f"  {name:25s}  vol={stats['volume']:>4d} ({stats['volume_fraction']:.1%})  "
              f"cov={stats['coverage']:.1%}  eff={stats['efficiency']:.2f}x")

    print(f"\n  Filter overlap (MiniLM vs SPECTER2): Jaccard={jaccard:.3f}, shared={overlap}/{len(minilm_filtered)}")

    return {
        "strategies": results,
        "filter_overlap_jaccard": round(jaccard, 4),
        "shared_count": overlap,
    }


def run_c1_r6(enrichment, enriched_ids):
    """Importance proxy sensitivity analysis."""
    print("\n--- C1-R6: Importance proxy sensitivity ---")

    proxies = get_importance_proxies(enrichment)

    # For each proxy, get important papers
    proxy_important = {}
    for name, values in proxies.items():
        subset = {aid: v for aid, v in values.items() if aid in enriched_ids}
        important = get_important_ids(subset)
        proxy_important[name] = important
        print(f"  Proxy '{name}': {len(important)} important papers (threshold: "
              f"{np.percentile(list(subset.values()), 80):.1f})")

    # Cross-proxy agreement
    print(f"\n  Cross-proxy overlap:")
    proxy_names = list(proxy_important.keys())
    for i, n1 in enumerate(proxy_names):
        for n2 in proxy_names[i+1:]:
            s1 = proxy_important[n1]
            s2 = proxy_important[n2]
            overlap = len(s1 & s2)
            j = overlap / len(s1 | s2) if (s1 | s2) else 0
            print(f"    {n1} vs {n2}: Jaccard={j:.3f} ({overlap} shared)")

    # Re-run embedding top-50% filter against each proxy
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}

    enriched_with_idx = [(aid, id_to_idx[aid]) for aid in enriched_ids if aid in id_to_idx]
    indices = [idx for _, idx in enriched_with_idx]
    aids = [aid for aid, _ in enriched_with_idx]
    emb_subset = minilm_emb[indices]
    centroid = emb_subset.mean(axis=0, keepdims=True)
    sims = (emb_subset @ centroid.T).flatten()
    emb_filtered = {aids[i] for i, s in enumerate(sims) if s >= np.median(sims)}

    print(f"\n  Embedding top-50% coverage by proxy:")
    sensitivity = []
    for name, important in proxy_important.items():
        stats = coverage_stats(emb_filtered, important, enriched_ids)
        sensitivity.append({"proxy": name, **stats})
        print(f"    {name:15s}: coverage={stats['coverage']:.1%}  efficiency={stats['efficiency']:.2f}x")

    return {
        "proxy_sizes": {n: len(s) for n, s in proxy_important.items()},
        "sensitivity": sensitivity,
    }


def main():
    print("=" * 80)
    print("C1 Round 2: B1-Informed Filtering Strategies")
    print("=" * 80)

    papers = load_papers()
    enrichment = load_enrichment()
    enriched_ids = set(enrichment.keys())
    print(f"Papers: {len(papers)}, Enriched: {len(enriched_ids)}")

    # Load embeddings
    minilm_emb = np.load(MINILM_EMBEDDINGS)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)

    # Default importance proxy: citations
    proxies = get_importance_proxies(enrichment)
    important_ids = get_important_ids(
        {aid: v for aid, v in proxies["citations"].items() if aid in enriched_ids}
    )
    print(f"Important papers (citation proxy): {len(important_ids)}/{len(enriched_ids)}")

    results = {}
    results["C1_R1_keyword"] = run_c1_r1(papers, enriched_ids, important_ids)
    results["C1_R2_author"] = run_c1_r2(papers, enriched_ids, important_ids)
    results["C1_R3_svm"] = run_c1_r3(papers, enriched_ids, important_ids)
    results["C1_R4_hybrid"] = run_c1_r4(papers, enriched_ids, important_ids, minilm_emb, arxiv_ids)
    results["C1_R5_specter2"] = run_c1_r5(papers, enriched_ids, important_ids, arxiv_ids)
    results["C1_R6_sensitivity"] = run_c1_r6(enrichment, enriched_ids)

    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
