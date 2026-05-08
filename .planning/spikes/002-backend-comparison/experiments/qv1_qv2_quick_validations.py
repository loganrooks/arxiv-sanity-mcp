"""
QV1: Pre-filtered TF-IDF cosine — does category scoping keep similarity <100ms?
QV2: Memory-mapped feature loading — is mmap actually near-instant for 472 MB?

Usage:
    python qv1_qv2_quick_validations.py
"""

import json
import sqlite3
import time
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
EMBEDDINGS_PATH = DATA_DIR / "embeddings_19k.npy"
RESULTS_PATH = DATA_DIR / "qv1_qv2_results.json"


def load_papers():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ======================================================================
# QV1: Pre-filtered TF-IDF cosine
# ======================================================================

def run_qv1(papers):
    """Test whether category pre-filtering keeps TF-IDF cosine <100ms."""
    print("=" * 70)
    print("QV1: Pre-filtered TF-IDF Cosine")
    print("=" * 70)

    # Group papers by category
    by_category = {}
    for p in papers:
        cat = p["primary_category"]
        by_category.setdefault(cat, []).append(p)

    # Build TF-IDF on full corpus
    print(f"\n  Building TF-IDF on {len(papers)} papers...")
    texts = [f"{p['title']}. {p['abstract']}" for p in papers]
    vectorizer = TfidfVectorizer(max_features=20000, sublinear_tf=True, stop_words='english')
    t0 = time.perf_counter()
    tfidf_matrix = vectorizer.fit_transform(texts)
    build_time = time.perf_counter() - t0
    print(f"  Built in {build_time:.2f}s, shape={tfidf_matrix.shape}, "
          f"size={tfidf_matrix.data.nbytes / 1024 / 1024:.1f} MB (sparse)")

    # Full corpus cosine (baseline — should be slow)
    query_idx = len(papers) // 2
    query_vec = tfidf_matrix[query_idx]

    # Warmup
    cosine_similarity(query_vec, tfidf_matrix[:100])

    print(f"\n  Full corpus cosine search ({len(papers)} papers):")
    full_times = []
    for _ in range(10):
        t0 = time.perf_counter()
        scores = cosine_similarity(query_vec, tfidf_matrix)
        top_indices = np.argsort(scores.flatten())[-20:][::-1]
        full_times.append((time.perf_counter() - t0) * 1000)
    full_p50 = np.median(full_times)
    print(f"    p50: {full_p50:.1f}ms")

    # Category-filtered cosine
    results = {"full_corpus": {"n_papers": len(papers), "p50_ms": round(float(full_p50), 2)}}
    results["by_category"] = []

    # Test top 5 categories + overall
    top_cats = sorted(by_category.keys(), key=lambda c: len(by_category[c]), reverse=True)[:5]

    print(f"\n  Category-filtered cosine:")
    print(f"  {'Category':<15s} {'Papers':>8s} {'p50':>10s} {'vs full':>10s}")
    print(f"  {'-' * 45}")

    for cat in top_cats:
        cat_papers = by_category[cat]
        cat_texts = [f"{p['title']}. {p['abstract']}" for p in cat_papers]
        cat_tfidf = vectorizer.transform(cat_texts)

        # Use first paper in category as query
        cat_query = cat_tfidf[0]

        # Warmup
        cosine_similarity(cat_query, cat_tfidf)

        cat_times = []
        for _ in range(20):
            t0 = time.perf_counter()
            scores = cosine_similarity(cat_query, cat_tfidf)
            top_k = min(20, scores.shape[1])
            top_indices = np.argsort(scores.flatten())[-top_k:][::-1]
            cat_times.append((time.perf_counter() - t0) * 1000)

        cat_p50 = np.median(cat_times)
        ratio = cat_p50 / full_p50 if full_p50 > 0 else 0

        print(f"  {cat:<15s} {len(cat_papers):>8d} {cat_p50:>8.2f}ms {ratio:>8.1%}")
        results["by_category"].append({
            "category": cat,
            "n_papers": len(cat_papers),
            "p50_ms": round(float(cat_p50), 2),
            "ratio_vs_full": round(float(ratio), 4),
        })

    # Simulate 215K scale: extrapolate from measured relationship
    # At 19K full corpus, we have a baseline. Pre-filtering to top category
    # would give ~(19K * 11) * (top_cat_fraction) papers at 215K
    largest_cat_fraction = len(by_category[top_cats[0]]) / len(papers)
    estimated_215k_full = full_p50 * (215000 / len(papers))  # Linear extrapolation
    estimated_215k_filtered = full_p50 * (215000 * largest_cat_fraction / len(papers))

    print(f"\n  215K extrapolation (linear):")
    print(f"    Full corpus: ~{estimated_215k_full:.0f}ms")
    print(f"    Filtered to {top_cats[0]} ({largest_cat_fraction:.1%}): ~{estimated_215k_filtered:.0f}ms")

    results["extrapolation_215k"] = {
        "full_corpus_ms": round(float(estimated_215k_full), 0),
        "filtered_largest_cat_ms": round(float(estimated_215k_filtered), 0),
        "largest_category": top_cats[0],
        "largest_category_fraction": round(float(largest_cat_fraction), 4),
    }

    # Verdict
    under_100ms = all(r["p50_ms"] < 100 for r in results["by_category"])
    results["verdict"] = (
        "VALIDATED" if under_100ms else "PARTIALLY VALIDATED"
    )
    print(f"\n  Verdict: {results['verdict']} — "
          f"{'all' if under_100ms else 'not all'} categories under 100ms at 19K")

    return results


# ======================================================================
# QV2: Memory-mapped feature loading
# ======================================================================

def run_qv2():
    """Test mmap loading time for embeddings and synthetic TF-IDF matrix."""
    print("\n" + "=" * 70)
    print("QV2: Memory-Mapped Feature Loading")
    print("=" * 70)

    results = {}

    # Test with actual embeddings (28 MB)
    if EMBEDDINGS_PATH.exists():
        emb_size = EMBEDDINGS_PATH.stat().st_size / 1024 / 1024
        print(f"\n  Embeddings file: {emb_size:.1f} MB")

        # Standard load
        load_times = []
        for _ in range(5):
            t0 = time.perf_counter()
            arr = np.load(EMBEDDINGS_PATH)
            _ = arr[0]  # Force read
            load_times.append((time.perf_counter() - t0) * 1000)
            del arr

        # mmap load
        mmap_times = []
        for _ in range(5):
            t0 = time.perf_counter()
            arr = np.load(EMBEDDINGS_PATH, mmap_mode='r')
            _ = arr[0]  # Force first page
            mmap_times.append((time.perf_counter() - t0) * 1000)
            del arr

        # mmap + first query (simulates actual usage)
        query_times = []
        for _ in range(5):
            t0 = time.perf_counter()
            arr = np.load(EMBEDDINGS_PATH, mmap_mode='r')
            query_vec = arr[0:1]
            scores = query_vec @ arr.T  # Full dot product — forces all pages
            query_times.append((time.perf_counter() - t0) * 1000)
            del arr

        results["embeddings_28mb"] = {
            "file_size_mb": round(emb_size, 1),
            "np_load_p50_ms": round(float(np.median(load_times)), 2),
            "mmap_open_p50_ms": round(float(np.median(mmap_times)), 2),
            "mmap_first_query_p50_ms": round(float(np.median(query_times)), 2),
        }

        print(f"    np.load():         p50={np.median(load_times):.2f}ms")
        print(f"    mmap open:         p50={np.median(mmap_times):.2f}ms")
        print(f"    mmap+first query:  p50={np.median(query_times):.2f}ms")

    # Create and test with larger synthetic files
    for size_mb, label in [(157, "tfidf_157mb"), (472, "combined_472mb")]:
        print(f"\n  Synthetic {size_mb} MB file:")
        # Calculate dimensions for target size
        # float32 = 4 bytes per element
        n_elements = (size_mb * 1024 * 1024) // 4
        # Make it rectangular: n_papers x dim
        n_papers = 19252
        dim = n_elements // n_papers
        actual_size = n_papers * dim * 4 / 1024 / 1024

        synth_path = DATA_DIR / f"qv2_synth_{size_mb}mb.npy"

        # Create synthetic file
        synth = np.random.randn(n_papers, dim).astype(np.float32)
        np.save(synth_path, synth)
        del synth

        file_size = synth_path.stat().st_size / 1024 / 1024

        # Standard load
        load_times = []
        for _ in range(3):
            t0 = time.perf_counter()
            arr = np.load(synth_path)
            _ = arr[0]
            load_times.append((time.perf_counter() - t0) * 1000)
            del arr

        # mmap open
        mmap_times = []
        for _ in range(3):
            t0 = time.perf_counter()
            arr = np.load(synth_path, mmap_mode='r')
            _ = arr[0]
            mmap_times.append((time.perf_counter() - t0) * 1000)
            del arr

        # mmap + first query
        query_times = []
        for _ in range(3):
            t0 = time.perf_counter()
            arr = np.load(synth_path, mmap_mode='r')
            query_vec = arr[0:1]
            scores = query_vec @ arr.T
            query_times.append((time.perf_counter() - t0) * 1000)
            del arr

        results[label] = {
            "file_size_mb": round(file_size, 1),
            "shape": [n_papers, dim],
            "np_load_p50_ms": round(float(np.median(load_times)), 2),
            "mmap_open_p50_ms": round(float(np.median(mmap_times)), 2),
            "mmap_first_query_p50_ms": round(float(np.median(query_times)), 2),
        }

        print(f"    np.load():         p50={np.median(load_times):.0f}ms")
        print(f"    mmap open:         p50={np.median(mmap_times):.2f}ms")
        print(f"    mmap+first query:  p50={np.median(query_times):.0f}ms")

        # Cleanup
        synth_path.unlink(missing_ok=True)

    # Verdict
    mmap_open_max = max(
        v.get("mmap_open_p50_ms", 0)
        for v in results.values()
        if isinstance(v, dict) and "mmap_open_p50_ms" in v
    )
    results["verdict"] = (
        "VALIDATED" if mmap_open_max < 50
        else "PARTIALLY VALIDATED" if mmap_open_max < 500
        else "NOT VALIDATED"
    )
    print(f"\n  Verdict: {results['verdict']} — "
          f"mmap open max {mmap_open_max:.1f}ms "
          f"({'near-instant' if mmap_open_max < 50 else 'noticeable'})")
    print(f"  Note: first query after mmap forces page faults — measure that too.")

    return results


def main():
    papers = load_papers()
    print(f"Loaded {len(papers)} papers\n")

    results = {}
    results["qv1"] = run_qv1(papers)
    results["qv2"] = run_qv2()
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 70}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
