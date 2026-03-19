"""
Dimension 3: Vector Search — pgvector vs Brute-Force Numpy

Compares pgvector (exact + HNSW) against brute-force numpy dot product
at the same scale points. Also tests filtered vector search.

Prerequisites:
- setup_spike002.py has been run
- embeddings_19k.npy and arxiv_ids_19k.json in data/

Usage:
    python d3_vector_search.py
"""

import json
import sqlite3
import statistics
import time
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2.extras import execute_values

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
EMBEDDINGS_PATH = DATA_DIR / "embeddings_19k.npy"
ARXIV_IDS_PATH = DATA_DIR / "arxiv_ids_19k.json"
RESULTS_PATH = DATA_DIR / "d3_vector_search_results.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"

SCALE_POINTS = [5_000, 10_000, 19_252, 50_000, 100_000, 215_000]
TOP_K = 20
RUNS = 20
WARMUP = 3

# Use 5 different query vectors for more robust measurement
NUM_QUERY_VECTORS = 5


def load_base_data():
    """Load embeddings and arxiv IDs."""
    embeddings = np.load(EMBEDDINGS_PATH)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    return embeddings, arxiv_ids


def load_categories() -> dict[str, str]:
    """Load primary_category for each paper from SQLite."""
    conn = sqlite3.connect(str(SOURCE_DB))
    rows = conn.execute(
        "SELECT arxiv_id, primary_category FROM papers"
    ).fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}


def scale_data(embeddings: np.ndarray, arxiv_ids: list[str], target: int):
    """Scale embeddings and IDs to target size by cycling."""
    if target <= len(arxiv_ids):
        return embeddings[:target], arxiv_ids[:target]

    n_base = len(arxiv_ids)
    scaled_emb = np.zeros((target, embeddings.shape[1]), dtype=np.float32)
    scaled_ids = []

    for i in range(target):
        scaled_emb[i] = embeddings[i % n_base]
        if i < n_base:
            scaled_ids.append(arxiv_ids[i])
        else:
            scaled_ids.append(f"synth.{i:07d}")

    return scaled_emb, scaled_ids


def setup_pgvector_at_scale(
    embeddings: np.ndarray,
    arxiv_ids: list[str],
    categories: dict[str, str],
    scale: int,
):
    """Load pgvector table at given scale with HNSW index."""
    emb, ids = scale_data(embeddings, arxiv_ids, scale)
    dim = emb.shape[1]

    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()

    # Recreate tables
    cur.execute("DROP TABLE IF EXISTS paper_embeddings CASCADE")
    cur.execute("DROP TABLE IF EXISTS papers CASCADE")

    cur.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            primary_category TEXT
        )
    """)
    cur.execute(f"""
        CREATE TABLE paper_embeddings (
            arxiv_id TEXT PRIMARY KEY REFERENCES papers(arxiv_id),
            embedding vector({dim})
        )
    """)

    # Insert papers (minimal — just IDs and categories)
    conn.autocommit = False
    paper_values = [
        (aid, categories.get(aid.split('.')[0] if 'synth' not in aid else arxiv_ids[int(aid.split('.')[1]) % len(arxiv_ids)],
                             categories.get(arxiv_ids[i % len(arxiv_ids)], 'cs.AI')))
        for i, aid in enumerate(ids)
    ]
    for batch_start in range(0, len(paper_values), 1000):
        batch = paper_values[batch_start:batch_start + 1000]
        execute_values(
            cur,
            "INSERT INTO papers (arxiv_id, primary_category) VALUES %s ON CONFLICT DO NOTHING",
            batch,
            page_size=1000,
        )
    conn.commit()

    # Insert embeddings
    t0 = time.perf_counter()
    for batch_start in range(0, len(ids), 500):
        batch_ids = ids[batch_start:batch_start + 500]
        batch_emb = emb[batch_start:batch_start + 500]
        values = [(aid, e.tolist()) for aid, e in zip(batch_ids, batch_emb)]
        execute_values(
            cur,
            "INSERT INTO paper_embeddings (arxiv_id, embedding) VALUES %s",
            values,
            template="(%s, %s::vector)",
            page_size=500,
        )
    conn.commit()
    insert_time = time.perf_counter() - t0

    # Build HNSW index
    conn.autocommit = True
    t0 = time.perf_counter()
    cur.execute("""
        CREATE INDEX idx_emb_hnsw ON paper_embeddings
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)
    hnsw_time = time.perf_counter() - t0

    cur.execute("ANALYZE paper_embeddings")
    cur.close()
    conn.close()

    return emb, ids, {
        "insert_time_s": round(insert_time, 3),
        "hnsw_build_time_s": round(hnsw_time, 3),
    }


def bench_numpy_bruteforce(
    embeddings: np.ndarray,
    query_vectors: np.ndarray,
    top_k: int = TOP_K,
) -> dict:
    """Benchmark brute-force numpy dot product search."""
    latencies = []

    for qv in query_vectors:
        qv = qv.reshape(1, -1)

        # Warmup
        for _ in range(WARMUP):
            scores = qv @ embeddings.T
            np.argpartition(scores.flatten(), -top_k)[-top_k:]

        # Timed runs
        for _ in range(RUNS):
            t0 = time.perf_counter()
            scores = qv @ embeddings.T
            top_idx = np.argpartition(scores.flatten(), -top_k)[-top_k:]
            top_idx = top_idx[np.argsort(scores.flatten()[top_idx])[::-1]]
            latencies.append((time.perf_counter() - t0) * 1000)

    return {
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
    }


def bench_pgvector_exact(query_vectors: np.ndarray, top_k: int = TOP_K) -> dict:
    """Benchmark pgvector exact (sequential) search — no index."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    # Disable index for exact search
    cur.execute("SET enable_indexscan = off")
    cur.execute("SET enable_bitmapscan = off")

    latencies = []
    for qv in query_vectors:
        vec_str = "[" + ",".join(str(float(x)) for x in qv) + "]"

        # Warmup
        for _ in range(WARMUP):
            cur.execute(
                f"SELECT arxiv_id, embedding <=> %s::vector AS dist "
                f"FROM paper_embeddings ORDER BY dist LIMIT %s",
                (vec_str, top_k),
            )
            cur.fetchall()

        # Timed runs
        for _ in range(RUNS):
            t0 = time.perf_counter()
            cur.execute(
                f"SELECT arxiv_id, embedding <=> %s::vector AS dist "
                f"FROM paper_embeddings ORDER BY dist LIMIT %s",
                (vec_str, top_k),
            )
            cur.fetchall()
            latencies.append((time.perf_counter() - t0) * 1000)

    cur.execute("RESET enable_indexscan")
    cur.execute("RESET enable_bitmapscan")
    cur.close()
    conn.close()

    return {
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
    }


def bench_pgvector_hnsw(query_vectors: np.ndarray, top_k: int = TOP_K) -> dict:
    """Benchmark pgvector HNSW (approximate) search."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    # Set ef_search for recall/speed tradeoff
    cur.execute("SET hnsw.ef_search = 40")

    latencies = []
    for qv in query_vectors:
        vec_str = "[" + ",".join(str(float(x)) for x in qv) + "]"

        # Warmup
        for _ in range(WARMUP):
            cur.execute(
                "SELECT arxiv_id, embedding <=> %s::vector AS dist "
                "FROM paper_embeddings ORDER BY dist LIMIT %s",
                (vec_str, top_k),
            )
            cur.fetchall()

        # Timed runs
        for _ in range(RUNS):
            t0 = time.perf_counter()
            cur.execute(
                "SELECT arxiv_id, embedding <=> %s::vector AS dist "
                "FROM paper_embeddings ORDER BY dist LIMIT %s",
                (vec_str, top_k),
            )
            cur.fetchall()
            latencies.append((time.perf_counter() - t0) * 1000)

    cur.close()
    conn.close()

    return {
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
    }


def measure_hnsw_recall(
    query_vectors: np.ndarray,
    embeddings: np.ndarray,
    arxiv_ids: list[str],
    top_k: int = TOP_K,
) -> float:
    """Measure HNSW recall against exact (numpy) results."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("SET hnsw.ef_search = 40")

    recalls = []
    for qv in query_vectors:
        # Ground truth from numpy
        scores = qv.reshape(1, -1) @ embeddings.T
        true_top = set(
            arxiv_ids[i]
            for i in np.argpartition(scores.flatten(), -top_k)[-top_k:]
        )

        # HNSW result
        vec_str = "[" + ",".join(str(float(x)) for x in qv) + "]"
        cur.execute(
            "SELECT arxiv_id FROM paper_embeddings "
            "ORDER BY embedding <=> %s::vector LIMIT %s",
            (vec_str, top_k),
        )
        hnsw_top = set(r[0] for r in cur.fetchall())

        recall = len(true_top & hnsw_top) / top_k
        recalls.append(recall)

    cur.close()
    conn.close()
    return round(statistics.mean(recalls), 4)


def bench_filtered_search(
    query_vectors: np.ndarray,
    embeddings: np.ndarray,
    arxiv_ids: list[str],
    categories: dict[str, str],
    filter_category: str = "cs.AI",
) -> dict:
    """Compare filtered vector search: pgvector WHERE vs manual numpy pre-filter."""
    # Find indices matching the category
    cat_indices = [
        i for i, aid in enumerate(arxiv_ids)
        if categories.get(
            aid if 'synth' not in aid else arxiv_ids[int(aid.split('.')[1]) % len([a for a in arxiv_ids if 'synth' not in a])],
            categories.get(arxiv_ids[i % len([a for a in arxiv_ids if 'synth' not in a])], '')
        ) == filter_category
    ]

    if not cat_indices:
        return {"error": f"No papers with category {filter_category}"}

    # Numpy pre-filter
    filtered_emb = embeddings[cat_indices]
    filtered_ids = [arxiv_ids[i] for i in cat_indices]

    numpy_latencies = []
    for qv in query_vectors:
        qv_r = qv.reshape(1, -1)
        for _ in range(WARMUP):
            qv_r @ filtered_emb.T

        for _ in range(RUNS):
            t0 = time.perf_counter()
            scores = qv_r @ filtered_emb.T
            k = min(TOP_K, len(filtered_ids))
            top_idx = np.argpartition(scores.flatten(), -k)[-k:]
            numpy_latencies.append((time.perf_counter() - t0) * 1000)

    # pgvector filtered
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("SET hnsw.ef_search = 40")

    pg_latencies = []
    for qv in query_vectors:
        vec_str = "[" + ",".join(str(float(x)) for x in qv) + "]"

        for _ in range(WARMUP):
            cur.execute(
                """SELECT pe.arxiv_id, pe.embedding <=> %s::vector AS dist
                   FROM paper_embeddings pe
                   JOIN papers p ON pe.arxiv_id = p.arxiv_id
                   WHERE p.primary_category = %s
                   ORDER BY dist LIMIT %s""",
                (vec_str, filter_category, TOP_K),
            )
            cur.fetchall()

        for _ in range(RUNS):
            t0 = time.perf_counter()
            cur.execute(
                """SELECT pe.arxiv_id, pe.embedding <=> %s::vector AS dist
                   FROM paper_embeddings pe
                   JOIN papers p ON pe.arxiv_id = p.arxiv_id
                   WHERE p.primary_category = %s
                   ORDER BY dist LIMIT %s""",
                (vec_str, filter_category, TOP_K),
            )
            cur.fetchall()
            pg_latencies.append((time.perf_counter() - t0) * 1000)

    cur.close()
    conn.close()

    return {
        "filter_category": filter_category,
        "filtered_count": len(cat_indices),
        "numpy_prefilter": {
            "p50_ms": round(statistics.median(numpy_latencies), 3),
            "p95_ms": round(sorted(numpy_latencies)[int(len(numpy_latencies) * 0.95)], 3),
        },
        "pgvector_filtered": {
            "p50_ms": round(statistics.median(pg_latencies), 3),
            "p95_ms": round(sorted(pg_latencies)[int(len(pg_latencies) * 0.95)], 3),
        },
    }


def main():
    print("=" * 80)
    print("Dimension 3: Vector Search (pgvector vs Brute-Force Numpy)")
    print("=" * 80)

    base_emb, base_ids = load_base_data()
    categories = load_categories()
    print(f"Loaded {len(base_ids)} base embeddings, {len(categories)} categories")

    # Pick query vectors (use papers at evenly-spaced indices)
    query_indices = np.linspace(0, len(base_ids) - 1, NUM_QUERY_VECTORS, dtype=int)
    query_vectors = base_emb[query_indices]
    print(f"Using {NUM_QUERY_VECTORS} query vectors from indices {query_indices.tolist()}")

    all_results = []

    for scale in SCALE_POINTS:
        print(f"\n{'=' * 80}")
        print(f"SCALE: {scale:,}")
        print(f"{'=' * 80}")

        # Scale data
        scaled_emb, scaled_ids = scale_data(base_emb, base_ids, scale)
        print(f"  Embeddings: {scaled_emb.shape}")

        # Setup pgvector
        print("  Loading pgvector + HNSW index...")
        _, _, setup_info = setup_pgvector_at_scale(base_emb, base_ids, categories, scale)
        print(f"  Insert: {setup_info['insert_time_s']}s, HNSW: {setup_info['hnsw_build_time_s']}s")

        # Benchmark numpy brute-force
        print("  Benchmarking numpy brute-force...")
        numpy_result = bench_numpy_bruteforce(scaled_emb, query_vectors)
        print(f"    p50={numpy_result['p50_ms']:.2f}ms  p95={numpy_result['p95_ms']:.2f}ms")

        # Benchmark pgvector exact
        print("  Benchmarking pgvector exact (no index)...")
        exact_result = bench_pgvector_exact(query_vectors)
        print(f"    p50={exact_result['p50_ms']:.2f}ms  p95={exact_result['p95_ms']:.2f}ms")

        # Benchmark pgvector HNSW
        print("  Benchmarking pgvector HNSW...")
        hnsw_result = bench_pgvector_hnsw(query_vectors)
        print(f"    p50={hnsw_result['p50_ms']:.2f}ms  p95={hnsw_result['p95_ms']:.2f}ms")

        # Measure recall
        print("  Measuring HNSW recall...")
        recall = measure_hnsw_recall(query_vectors, scaled_emb, scaled_ids)
        print(f"    Recall@{TOP_K}: {recall:.4f}")

        scale_result = {
            "scale": scale,
            "setup": setup_info,
            "numpy_bruteforce": numpy_result,
            "pgvector_exact": exact_result,
            "pgvector_hnsw": hnsw_result,
            "hnsw_recall": recall,
        }

        # Filtered search only at 19K (real data, meaningful categories)
        if scale == 19_252:
            print("  Benchmarking filtered vector search (cs.AI)...")
            filtered = bench_filtered_search(
                query_vectors, scaled_emb, scaled_ids, categories, "cs.AI"
            )
            scale_result["filtered_search"] = filtered
            if "error" not in filtered:
                print(f"    Numpy pre-filter: p50={filtered['numpy_prefilter']['p50_ms']:.2f}ms")
                print(f"    pgvector WHERE:   p50={filtered['pgvector_filtered']['p50_ms']:.2f}ms")
                print(f"    Filtered set: {filtered['filtered_count']} papers")

        all_results.append(scale_result)

        # Summary line
        print(f"\n  {'Method':<25s} {'p50':>10s} {'p95':>10s}")
        print(f"  {'-' * 47}")
        print(f"  {'Numpy brute-force':<25s} {numpy_result['p50_ms']:>8.2f}ms {numpy_result['p95_ms']:>8.2f}ms")
        print(f"  {'pgvector exact':<25s} {exact_result['p50_ms']:>8.2f}ms {exact_result['p95_ms']:>8.2f}ms")
        print(f"  {'pgvector HNSW':<25s} {hnsw_result['p50_ms']:>8.2f}ms {hnsw_result['p95_ms']:>8.2f}ms")
        print(f"  {'HNSW recall@20':<25s} {recall:.4f}")

    # Save results
    output = {
        "dimension": "D3",
        "description": "Vector Search — pgvector vs Brute-Force Numpy",
        "model": "all-MiniLM-L6-v2",
        "embedding_dim": 384,
        "top_k": TOP_K,
        "runs_per_query": RUNS,
        "num_query_vectors": NUM_QUERY_VECTORS,
        "hnsw_params": {"m": 16, "ef_construction": 64, "ef_search": 40},
        "per_scale": all_results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)

    # Print summary table
    print(f"\n{'=' * 80}")
    print("SUMMARY: Vector search p50 latency by scale")
    print(f"{'=' * 80}")
    print(f"  {'Scale':>10s} {'Numpy':>10s} {'PG exact':>10s} {'PG HNSW':>10s} {'Recall':>8s}")
    print(f"  {'-' * 52}")
    for r in all_results:
        print(
            f"  {r['scale']:>10,d} "
            f"{r['numpy_bruteforce']['p50_ms']:>8.2f}ms "
            f"{r['pgvector_exact']['p50_ms']:>8.2f}ms "
            f"{r['pgvector_hnsw']['p50_ms']:>8.2f}ms "
            f"{r['hnsw_recall']:>7.4f}"
        )

    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
