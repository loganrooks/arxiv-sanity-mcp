"""
A1c.1: TF-IDF Matrix Benchmark

Measures memory footprint, build time, query transform time, and cosine
similarity search time at 6 scale points using real arXiv paper abstracts.

Scale methodology: Same as A1b (FTS5 benchmark). Real 19K papers are
duplicated with modified IDs to reach target sizes. This preserves term
frequency distributions but limits vocabulary to ~19K unique papers' worth.

Output: JSON results file + console summary table.
"""

import json
import os
import sqlite3
import sys
import time

import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- Configuration ---

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "spike_001_harvest.db")
RESULTS_PATH = os.path.join(os.path.dirname(__file__), "data", "tfidf_benchmark_results.json")

SCALE_POINTS = [5_000, 10_000, 19_252, 50_000, 100_000, 215_000]

# Vocabulary pruning configurations to test
VOCAB_CONFIGS = {
    "default": {},
    "max_50k": {"max_features": 50_000},
    "max_20k": {"max_features": 20_000},
    "pruned": {"min_df": 2, "max_df": 0.8},
    "pruned_50k": {"min_df": 2, "max_df": 0.8, "max_features": 50_000},
}

TIMING_RUNS = 5
WARMUP_RUNS = 1
TOP_K = 20

# --- Helpers ---


def load_papers(db_path: str) -> list[dict]:
    """Load all papers with non-empty abstracts from the harvest DB."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def scale_corpus(papers: list[dict], target_size: int) -> list[str]:
    """Scale corpus to target size by cycling through papers with modified IDs.

    Returns list of abstract texts only (for TF-IDF fitting).
    """
    abstracts = [p["abstract"] for p in papers]
    if target_size <= len(abstracts):
        return abstracts[:target_size]

    # Duplicate by cycling
    result = []
    for i in range(target_size):
        result.append(abstracts[i % len(abstracts)])
    return result


def sparse_matrix_bytes(matrix: csr_matrix) -> int:
    """Calculate actual memory usage of a CSR sparse matrix."""
    return matrix.data.nbytes + matrix.indices.nbytes + matrix.indptr.nbytes


def vectorizer_vocab_bytes(vectorizer: TfidfVectorizer) -> int:
    """Estimate memory usage of the vectorizer's vocabulary and IDF weights."""
    vocab_bytes = sum(
        sys.getsizeof(k) + sys.getsizeof(v) for k, v in vectorizer.vocabulary_.items()
    )
    idf_bytes = vectorizer.idf_.nbytes if hasattr(vectorizer, "idf_") else 0
    return vocab_bytes + idf_bytes


def timed(func, runs=TIMING_RUNS, warmup=WARMUP_RUNS):
    """Run function multiple times, return (result, median_seconds, all_times)."""
    # Warmup
    result = None
    for _ in range(warmup):
        result = func()

    times = []
    for _ in range(runs):
        t0 = time.monotonic()
        result = func()
        times.append(time.monotonic() - t0)

    return result, np.median(times), times


def fmt_bytes(b: int) -> str:
    if b < 1024:
        return f"{b} B"
    elif b < 1024**2:
        return f"{b / 1024:.1f} KB"
    elif b < 1024**3:
        return f"{b / 1024**2:.1f} MB"
    else:
        return f"{b / 1024**3:.2f} GB"


def fmt_ms(seconds: float) -> str:
    return f"{seconds * 1000:.1f}ms"


# --- Main benchmark ---


def run_benchmark():
    print(f"Loading papers from {DB_PATH}...")
    papers = load_papers(DB_PATH)
    print(f"Loaded {len(papers)} papers with abstracts")

    # Pick a representative query paper (middle of corpus)
    query_abstract = papers[len(papers) // 2]["abstract"]

    all_results = {}

    for config_name, config_params in VOCAB_CONFIGS.items():
        print(f"\n{'=' * 70}")
        print(f"Vocabulary config: {config_name} ({config_params or 'defaults'})")
        print(f"{'=' * 70}")

        config_results = {}

        for scale in SCALE_POINTS:
            print(f"\n  Scale: {scale:,} papers")

            # 1. Scale corpus
            abstracts = scale_corpus(papers, scale)

            # 2. Fit TF-IDF (timed)
            def fit():
                v = TfidfVectorizer(
                    stop_words="english",
                    dtype=np.float32,
                    **config_params,
                )
                m = v.fit_transform(abstracts)
                return v, m

            (vectorizer, matrix), fit_median, fit_times = timed(fit, runs=3, warmup=1)

            # 3. Measure sizes
            matrix_bytes = sparse_matrix_bytes(matrix)
            vocab_bytes = vectorizer_vocab_bytes(vectorizer)
            vocab_size = len(vectorizer.vocabulary_)
            nnz = matrix.nnz
            sparsity = 1.0 - (nnz / (matrix.shape[0] * matrix.shape[1]))
            total_bytes = matrix_bytes + vocab_bytes

            # 4. Query transform (timed)
            def transform_query():
                return vectorizer.transform([query_abstract])

            query_vec, transform_median, transform_times = timed(transform_query)

            # 5. Cosine similarity search (timed)
            def cosine_search():
                sims = cosine_similarity(query_vec, matrix).flatten()
                top_indices = np.argpartition(sims, -TOP_K)[-TOP_K:]
                top_indices = top_indices[np.argsort(sims[top_indices])[::-1]]
                return top_indices, sims[top_indices]

            (top_idx, top_scores), search_median, search_times = timed(cosine_search)

            # 6. Also time full argsort for comparison
            def full_argsort_search():
                sims = cosine_similarity(query_vec, matrix).flatten()
                return np.argsort(sims)[::-1][:TOP_K]

            _, argsort_median, argsort_times = timed(full_argsort_search)

            result = {
                "scale": scale,
                "vocab_config": config_name,
                "vocab_size": vocab_size,
                "matrix_shape": list(matrix.shape),
                "nnz": nnz,
                "sparsity": round(sparsity, 6),
                "matrix_bytes": matrix_bytes,
                "vocab_bytes": vocab_bytes,
                "total_bytes": total_bytes,
                "fit_time_median_s": round(fit_median, 4),
                "fit_times_s": [round(t, 4) for t in fit_times],
                "transform_time_median_s": round(transform_median, 6),
                "transform_times_s": [round(t, 6) for t in transform_times],
                "cosine_search_median_s": round(search_median, 6),
                "cosine_search_times_s": [round(t, 6) for t in search_times],
                "argsort_search_median_s": round(argsort_median, 6),
                "argsort_search_times_s": [round(t, 6) for t in argsort_times],
                "top_scores": [round(float(s), 4) for s in top_scores[:5]],
            }

            config_results[str(scale)] = result

            # Print summary
            print(f"    Vocab:       {vocab_size:,} terms")
            print(f"    Matrix:      {matrix.shape[0]:,} x {vocab_size:,} ({fmt_bytes(matrix_bytes)}, {sparsity:.4%} sparse)")
            print(f"    + Vocab:     {fmt_bytes(vocab_bytes)}")
            print(f"    = Total:     {fmt_bytes(total_bytes)}")
            print(f"    NNZ:         {nnz:,} ({nnz / scale:.0f} avg/doc)")
            print(f"    Fit time:    {fmt_ms(fit_median)} (median of 3)")
            print(f"    Transform:   {fmt_ms(transform_median)} (median of {TIMING_RUNS})")
            print(f"    Cosine top-{TOP_K}: {fmt_ms(search_median)} (partitioned, median of {TIMING_RUNS})")
            print(f"    Cosine top-{TOP_K}: {fmt_ms(argsort_median)} (full argsort, median of {TIMING_RUNS})")
            print(f"    Top scores:  {[round(float(s), 3) for s in top_scores[:5]]}")

        all_results[config_name] = config_results

    # Save results
    with open(RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")

    # Print comparison table
    print_comparison_table(all_results)


def print_comparison_table(all_results: dict):
    """Print a summary comparison table across configs and scales."""
    print(f"\n{'=' * 100}")
    print("SUMMARY: Total memory (matrix + vocab) by config and scale")
    print(f"{'=' * 100}")

    header = f"{'Config':<15}"
    for scale in SCALE_POINTS:
        header += f"  {scale // 1000}K".rjust(12)
    print(header)
    print("-" * 100)

    for config_name in VOCAB_CONFIGS:
        row = f"{config_name:<15}"
        for scale in SCALE_POINTS:
            data = all_results[config_name][str(scale)]
            row += f"  {fmt_bytes(data['total_bytes'])}".rjust(12)
        print(row)

    print(f"\n{'=' * 100}")
    print("SUMMARY: Cosine search time (partitioned top-20) by config and scale")
    print(f"{'=' * 100}")

    header = f"{'Config':<15}"
    for scale in SCALE_POINTS:
        header += f"  {scale // 1000}K".rjust(12)
    print(header)
    print("-" * 100)

    for config_name in VOCAB_CONFIGS:
        row = f"{config_name:<15}"
        for scale in SCALE_POINTS:
            data = all_results[config_name][str(scale)]
            row += f"  {fmt_ms(data['cosine_search_median_s'])}".rjust(12)
        print(row)

    print(f"\n{'=' * 100}")
    print("SUMMARY: Fit time by config and scale")
    print(f"{'=' * 100}")

    header = f"{'Config':<15}"
    for scale in SCALE_POINTS:
        header += f"  {scale // 1000}K".rjust(12)
    print(header)
    print("-" * 100)

    for config_name in VOCAB_CONFIGS:
        row = f"{config_name:<15}"
        for scale in SCALE_POINTS:
            data = all_results[config_name][str(scale)]
            row += f"  {fmt_ms(data['fit_time_median_s'])}".rjust(12)
        print(row)


if __name__ == "__main__":
    run_benchmark()
