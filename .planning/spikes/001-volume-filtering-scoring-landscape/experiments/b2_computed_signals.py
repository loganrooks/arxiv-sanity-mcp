"""
B2: Computed Signal Exploration

Enriches ~500 papers via OpenAlex, computes candidate signals, and
analyzes which ones correlate with importance proxies.

Steps:
1. Sample 500 papers (stratified by category)
2. Fetch OpenAlex enrichment (citation count, FWCI, topics, references)
3. Compute candidate signals
4. Correlation analysis + feature importance

Usage:
    python b2_computed_signals.py
"""

import json
import sqlite3
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx
import numpy as np

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
EMBEDDINGS_PATH = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
RESULTS_PATH = DATA_DIR / "b2_computed_signals_results.json"
ENRICHMENT_CACHE = DATA_DIR / "b2_openalex_cache.json"

SAMPLE_SIZE = 500
OPENALEX_EMAIL = "arxiv_mcp@example.com"
REQUEST_DELAY = 0.15  # ~7 req/s (within 10 req/s polite pool limit)


def load_papers():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def stratified_sample(papers, n):
    """Sample n papers stratified by primary_category."""
    by_cat = defaultdict(list)
    for p in papers:
        by_cat[p["primary_category"]].append(p)

    # Proportional allocation
    total = len(papers)
    sample = []
    for cat, cat_papers in sorted(by_cat.items()):
        k = max(1, round(n * len(cat_papers) / total))
        k = min(k, len(cat_papers))
        indices = np.linspace(0, len(cat_papers) - 1, k, dtype=int)
        sample.extend(cat_papers[i] for i in indices)

    # Trim to exact size
    if len(sample) > n:
        sample = sample[:n]
    return sample


def fetch_openalex(arxiv_ids: list[str]) -> dict:
    """Fetch OpenAlex data for papers by arXiv ID. Uses cache."""
    # Load cache
    cache = {}
    if ENRICHMENT_CACHE.exists():
        with open(ENRICHMENT_CACHE) as f:
            cache = json.load(f)

    to_fetch = [aid for aid in arxiv_ids if aid not in cache]
    print(f"  Cache: {len(cache)} entries, {len(to_fetch)} to fetch")

    if to_fetch:
        # Need titles for search fallback
        conn = sqlite3.connect(str(SOURCE_DB))
        title_map = {}
        for aid in to_fetch:
            row = conn.execute("SELECT title FROM papers WHERE arxiv_id = ?", (aid,)).fetchone()
            if row:
                title_map[aid] = row[0]
        conn.close()

        client = httpx.Client(timeout=30, follow_redirects=True)
        select_fields = ("id,doi,cited_by_count,fwci,citation_normalized_percentile,"
                         "topics,referenced_works,authorships,type,publication_year")

        for i, aid in enumerate(to_fetch):
            from urllib.parse import quote

            # Primary: arXiv URL lookup
            url = (
                f"https://api.openalex.org/works/https://arxiv.org/abs/{aid}"
                f"?mailto={OPENALEX_EMAIL}&select={select_fields}"
            )
            try:
                resp = client.get(url)
                if resp.status_code == 200:
                    cache[aid] = resp.json()
                else:
                    # Fallback: search by title
                    title = title_map.get(aid, "")
                    if title:
                        search_url = (
                            f"https://api.openalex.org/works?search={quote(title[:100])}"
                            f"&per_page=1&mailto={OPENALEX_EMAIL}&select={select_fields}"
                        )
                        time.sleep(REQUEST_DELAY)
                        resp2 = client.get(search_url)
                        if resp2.status_code == 200:
                            results = resp2.json().get("results", [])
                            if results:
                                cache[aid] = results[0]
                            else:
                                cache[aid] = {"error": "not_found"}
                        else:
                            cache[aid] = {"error": resp2.status_code}
                    else:
                        cache[aid] = {"error": "no_title"}
            except Exception as e:
                cache[aid] = {"error": str(e)}

            if (i + 1) % 50 == 0:
                print(f"    Fetched {i + 1}/{len(to_fetch)}")
                with open(ENRICHMENT_CACHE, "w") as f:
                    json.dump(cache, f)

            time.sleep(REQUEST_DELAY)

        client.close()

        # Save final cache
        with open(ENRICHMENT_CACHE, "w") as f:
            json.dump(cache, f)

    return cache


def compute_signals(sample, enrichment, all_papers, embeddings, arxiv_ids):
    """Compute candidate signals for each paper."""
    # Build lookup maps
    id_to_idx = {aid: i for i, aid in enumerate(arxiv_ids)}
    all_by_cat = defaultdict(list)
    for p in all_papers:
        all_by_cat[p["primary_category"]].append(p["arxiv_id"])

    # Compute category centroids for topic novelty
    cat_centroids = {}
    for cat, aids in all_by_cat.items():
        indices = [id_to_idx[a] for a in aids if a in id_to_idx]
        if indices:
            cat_centroids[cat] = embeddings[indices].mean(axis=0)

    signals = []

    for p in sample:
        aid = p["arxiv_id"]
        enr = enrichment.get(aid, {})

        if "error" in enr:
            continue

        # Extract enrichment fields
        cited_by = enr.get("cited_by_count", 0)
        fwci = enr.get("fwci")
        percentile = enr.get("citation_normalized_percentile")
        if isinstance(percentile, dict):
            percentile = percentile.get("value")
        topics = enr.get("topics", [])
        refs = enr.get("referenced_works", [])
        authorships = enr.get("authorships", [])
        pub_year = enr.get("publication_year")

        # Compute signals
        idx = id_to_idx.get(aid)

        # S1: Citation count (raw)
        s_citation = cited_by

        # S2: FWCI
        s_fwci = fwci if fwci is not None else 0

        # S3: Citation percentile
        s_percentile = percentile if percentile is not None else 0

        # S4: Author count
        s_author_count = len(authorships)

        # S5: Max author h-index (if available)
        h_indices = []
        for auth in authorships:
            author_obj = auth.get("author", {})
            # OpenAlex doesn't include h-index in work response — would need separate call
            # Use institution count as proxy for now
            insts = auth.get("institutions", [])
            h_indices.append(len(insts))  # Rough proxy
        s_max_h_proxy = max(h_indices) if h_indices else 0

        # S6: Category count (interdisciplinarity)
        cats = [c.strip() for c in (p.get("categories") or "").split() if c.strip()]
        s_cat_count = len(cats)

        # S7: Category entropy
        if s_cat_count > 1:
            # Equal weight per category → entropy = log2(n_categories)
            s_cat_entropy = float(np.log2(s_cat_count))
        else:
            s_cat_entropy = 0.0

        # S8: Reference count
        s_ref_count = len(refs)

        # S9: Topic count (from OpenAlex)
        s_topic_count = len(topics)

        # S10: Abstract length (words)
        s_abstract_len = len((p.get("abstract") or "").split())

        # S11: Title length (words)
        s_title_len = len((p.get("title") or "").split())

        # S12: Topic novelty (cosine distance from category centroid)
        s_topic_novelty = 0.0
        if idx is not None and p["primary_category"] in cat_centroids:
            paper_emb = embeddings[idx]
            centroid = cat_centroids[p["primary_category"]]
            cos_sim = np.dot(paper_emb, centroid) / (
                np.linalg.norm(paper_emb) * np.linalg.norm(centroid) + 1e-10
            )
            s_topic_novelty = 1.0 - float(cos_sim)  # Distance, not similarity

        entry = {
            "arxiv_id": aid,
            "category": p["primary_category"],
            "signals": {
                "citation_count": s_citation,
                "fwci": round(s_fwci, 4) if s_fwci else 0,
                "citation_percentile": round(s_percentile, 4) if s_percentile else 0,
                "author_count": s_author_count,
                "institution_proxy": s_max_h_proxy,
                "category_count": s_cat_count,
                "category_entropy": round(s_cat_entropy, 4),
                "reference_count": s_ref_count,
                "topic_count": s_topic_count,
                "abstract_length": s_abstract_len,
                "title_length": s_title_len,
                "topic_novelty": round(s_topic_novelty, 4),
            },
        }
        signals.append(entry)

    return signals


def analyze_signals(signals):
    """Correlation analysis and feature importance."""
    # Extract signal matrix
    signal_names = list(signals[0]["signals"].keys())
    matrix = np.array([
        [s["signals"][name] for name in signal_names]
        for s in signals
    ])

    print(f"\n  Signal matrix: {matrix.shape} ({len(signals)} papers × {len(signal_names)} signals)")

    # Correlation matrix
    # Handle constant columns
    stds = matrix.std(axis=0)
    valid_cols = stds > 0
    valid_names = [n for n, v in zip(signal_names, valid_cols) if v]
    valid_matrix = matrix[:, valid_cols]

    corr = np.corrcoef(valid_matrix.T)

    print(f"\n  Correlation with citation_count (importance proxy):")
    citation_idx = valid_names.index("citation_count") if "citation_count" in valid_names else None

    correlations = {}
    if citation_idx is not None:
        for i, name in enumerate(valid_names):
            if i != citation_idx:
                r = corr[citation_idx, i]
                correlations[name] = round(float(r), 4)
                print(f"    {name:25s}  r={r:+.4f}")

    # Feature importance via random forest
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler

    # Binary target: top 20% by citation count
    citation_vals = matrix[:, signal_names.index("citation_count")]
    threshold = np.percentile(citation_vals, 80)
    target = (citation_vals >= threshold).astype(int)

    # If all same class (likely for very new papers), note it
    if len(set(target)) < 2:
        print(f"\n  WARNING: All papers have same citation class (threshold={threshold})")
        print(f"  Citation count distribution: min={citation_vals.min()}, max={citation_vals.max()}, "
              f"median={np.median(citation_vals)}")
        feature_importances = {}
    else:
        scaler = StandardScaler()
        X = scaler.fit_transform(valid_matrix)

        clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
        clf.fit(X, target)

        feature_importances = {}
        print(f"\n  Random Forest feature importances (predicting top-20% citations):")
        for name, imp in sorted(zip(valid_names, clf.feature_importances_), key=lambda x: -x[1]):
            feature_importances[name] = round(float(imp), 4)
            bar = "█" * int(imp * 50)
            print(f"    {name:25s}  {imp:.4f}  {bar}")

    # Signal statistics
    signal_stats = {}
    for i, name in enumerate(signal_names):
        vals = matrix[:, i]
        signal_stats[name] = {
            "mean": round(float(np.mean(vals)), 4),
            "median": round(float(np.median(vals)), 4),
            "std": round(float(np.std(vals)), 4),
            "min": round(float(np.min(vals)), 4),
            "max": round(float(np.max(vals)), 4),
            "zeros": int(np.sum(vals == 0)),
            "zero_fraction": round(float(np.sum(vals == 0)) / len(vals), 4),
        }

    return {
        "correlations_with_citation": correlations,
        "feature_importances": feature_importances,
        "signal_stats": signal_stats,
        "citation_threshold_80pct": round(float(threshold), 2),
        "citation_distribution": {
            "min": round(float(citation_vals.min()), 0),
            "max": round(float(citation_vals.max()), 0),
            "median": round(float(np.median(citation_vals)), 0),
            "mean": round(float(np.mean(citation_vals)), 1),
        },
    }


def main():
    print("=" * 80)
    print("B2: Computed Signal Exploration")
    print("=" * 80)

    papers = load_papers()
    print(f"Loaded {len(papers)} papers")

    # Stratified sample
    sample = stratified_sample(papers, SAMPLE_SIZE)
    print(f"Sampled {len(sample)} papers (stratified by category)")

    cat_dist = Counter(p["primary_category"] for p in sample)
    print(f"  Top categories in sample: {cat_dist.most_common(5)}")

    # Fetch OpenAlex enrichment
    print(f"\nFetching OpenAlex enrichment...")
    sample_ids = [p["arxiv_id"] for p in sample]
    enrichment = fetch_openalex(sample_ids)

    successful = sum(1 for aid in sample_ids if aid in enrichment and "error" not in enrichment[aid])
    print(f"  Successfully enriched: {successful}/{len(sample_ids)}")

    # Load embeddings for topic novelty
    embeddings = np.load(EMBEDDINGS_PATH)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)

    # Compute signals
    print(f"\nComputing signals...")
    signals = compute_signals(sample, enrichment, papers, embeddings, arxiv_ids)
    print(f"  Computed signals for {len(signals)} papers")

    # Analyze
    print(f"\nAnalyzing signals...")
    analysis = analyze_signals(signals)

    # Save results
    results = {
        "sample_size": len(sample),
        "enriched_count": successful,
        "analysis": analysis,
        "signal_data": signals[:10],  # Sample for inspection
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")

    # Key finding
    print(f"\n  Citation distribution: min={analysis['citation_distribution']['min']}, "
          f"max={analysis['citation_distribution']['max']}, "
          f"median={analysis['citation_distribution']['median']}")
    print(f"  80th percentile threshold: {analysis['citation_threshold_80pct']}")

    if analysis["citation_distribution"]["max"] <= 1:
        print(f"\n  CAVEAT: Papers are <2 months old — citation counts are near-zero.")
        print(f"  Citation-based importance proxy is WEAK. Signal correlations should be")
        print(f"  interpreted as structural relationships, not predictive power.")

    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
