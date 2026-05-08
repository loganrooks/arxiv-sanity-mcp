"""Phase A1 supplement: FTS5 search performance benchmark.

Tests SQLite FTS5 search at multiple corpus sizes using real paper data
(duplicated with modified IDs to reach target sizes). Measures search
latency, index build time, and disk usage at each scale point.

Usage:
    conda run -n ml-dev python a1_fts5_benchmark.py

Requires: spike_001_harvest.db from a1_volume_mapping.py (19K+ papers).
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import statistics
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
BENCH_DB = DATA_DIR / "fts5_benchmark.db"
RESULTS_FILE = DATA_DIR / "fts5_benchmark_results.json"

# Scale points to test
SCALE_POINTS = [5_000, 10_000, 19_000, 50_000, 100_000, 215_000, 500_000]

# Queries to benchmark — mix of simple, boolean, multi-word, specific
QUERIES = [
    ("single_common", "transformer"),
    ("single_specific", "phenomenology"),
    ("two_word", "language model"),
    ("three_word", "reinforcement learning agent"),
    ("boolean_and", "attention AND mechanism"),
    ("boolean_or", "consciousness OR awareness"),
    ("phrase", '"large language model"'),
    ("multi_field_broad", "neural network optimization"),
    ("narrow_specific", "RLHF alignment"),
    ("long_query", "multi-agent system cooperative reinforcement learning"),
]

RUNS_PER_QUERY = 10  # number of times to run each query for stable timing


def load_source_papers() -> list[dict]:
    """Load all papers from the harvest database."""
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, primary_category FROM papers"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_benchmark_db(papers: list[dict], target_size: int) -> tuple[float, float, int]:
    """Create a benchmark DB at target size, return (insert_time, fts_build_time, db_bytes).

    Duplicates papers with modified IDs to reach target size.
    """
    if BENCH_DB.exists():
        os.remove(BENCH_DB)

    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    # Create base table
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            authors_text TEXT,
            abstract TEXT,
            categories TEXT,
            primary_category TEXT
        )
    """)

    # Insert papers, cycling through source data with modified IDs
    insert_start = time.perf_counter()
    batch = []
    for i in range(target_size):
        source = papers[i % len(papers)]
        # Generate unique ID by appending a suffix
        if i < len(papers):
            aid = source["arxiv_id"]
        else:
            aid = f"synth.{i:07d}"

        batch.append((
            aid,
            source["title"],
            source["authors_text"],
            source["abstract"],
            source["categories"],
            source["primary_category"],
        ))

        if len(batch) >= 1000:
            conn.executemany(
                "INSERT OR IGNORE INTO papers VALUES (?, ?, ?, ?, ?, ?)", batch
            )
            batch = []

    if batch:
        conn.executemany(
            "INSERT OR IGNORE INTO papers VALUES (?, ?, ?, ?, ?, ?)", batch
        )

    conn.commit()
    insert_time = time.perf_counter() - insert_start

    # Build FTS5 index
    fts_start = time.perf_counter()
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers',
            content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("""
        INSERT INTO papers_fts(papers_fts) VALUES('rebuild')
    """)
    conn.commit()
    fts_time = time.perf_counter() - fts_start

    conn.close()

    db_bytes = os.path.getsize(BENCH_DB)
    return insert_time, fts_time, db_bytes


def run_search_benchmark(query_name: str, query_text: str, runs: int) -> dict:
    """Run a search query multiple times, return timing statistics."""
    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")

    # Warmup — 2 runs discarded
    for _ in range(2):
        conn.execute(
            "SELECT p.arxiv_id, p.title, rank FROM papers_fts f "
            "JOIN papers p ON f.rowid = p.rowid "
            "WHERE papers_fts MATCH ? "
            "ORDER BY rank LIMIT 20",
            (query_text,),
        ).fetchall()

    # Timed runs
    latencies = []
    result_count = 0
    for _ in range(runs):
        start = time.perf_counter()
        results = conn.execute(
            "SELECT p.arxiv_id, p.title, rank FROM papers_fts f "
            "JOIN papers p ON f.rowid = p.rowid "
            "WHERE papers_fts MATCH ? "
            "ORDER BY rank LIMIT 20",
            (query_text,),
        ).fetchall()
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)
        result_count = len(results)

    conn.close()

    return {
        "query_name": query_name,
        "query_text": query_text,
        "result_count": result_count,
        "runs": runs,
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(runs * 0.95)], 3) if runs >= 20 else round(max(latencies), 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
        "stdev_ms": round(statistics.stdev(latencies), 3) if runs > 1 else 0,
    }


def run_count_benchmark() -> dict:
    """Benchmark a COUNT query (full table scan)."""
    conn = sqlite3.connect(str(BENCH_DB))

    latencies = []
    for _ in range(10):
        start = time.perf_counter()
        conn.execute("SELECT COUNT(*) FROM papers").fetchone()
        elapsed = (time.perf_counter() - start) * 1000
        latencies.append(elapsed)

    conn.close()
    return {
        "query_name": "count_all",
        "p50_ms": round(statistics.median(latencies), 3),
        "mean_ms": round(statistics.mean(latencies), 3),
    }


def main():
    print("Loading source papers...")
    papers = load_source_papers()
    print(f"Loaded {len(papers):,} papers from {SOURCE_DB.name}")

    if len(papers) < 1000:
        print("ERROR: Need at least 1000 papers. Run a1_volume_mapping.py first.")
        return

    all_results = []

    for target in SCALE_POINTS:
        print(f"\n{'='*60}")
        print(f"SCALE: {target:,} papers")
        print(f"{'='*60}")

        # Build DB and FTS index
        insert_time, fts_time, db_bytes = create_benchmark_db(papers, target)
        db_mb = db_bytes / (1024 * 1024)
        print(f"  Insert: {insert_time:.2f}s | FTS build: {fts_time:.2f}s | DB: {db_mb:.1f} MB")

        # Run search benchmarks
        scale_result = {
            "scale": target,
            "insert_seconds": round(insert_time, 3),
            "fts_build_seconds": round(fts_time, 3),
            "db_size_mb": round(db_mb, 1),
            "db_size_bytes": db_bytes,
            "queries": [],
        }

        for qname, qtext in QUERIES:
            try:
                qresult = run_search_benchmark(qname, qtext, RUNS_PER_QUERY)
                scale_result["queries"].append(qresult)
                status = "OK" if qresult["p50_ms"] < 500 else "SLOW"
                print(f"  {qname:25s} p50={qresult['p50_ms']:7.2f}ms  "
                      f"p95={qresult['p95_ms']:7.2f}ms  "
                      f"results={qresult['result_count']:4d}  [{status}]")
            except Exception as e:
                print(f"  {qname:25s} ERROR: {e}")
                scale_result["queries"].append({
                    "query_name": qname, "error": str(e)
                })

        # Count benchmark
        count_result = run_count_benchmark()
        scale_result["count_p50_ms"] = count_result["p50_ms"]
        print(f"  {'count_all':25s} p50={count_result['p50_ms']:7.2f}ms")

        all_results.append(scale_result)

    # Save results
    with open(RESULTS_FILE, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {RESULTS_FILE}")

    # Print summary table
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"{'Scale':>10s} {'Insert':>8s} {'FTS Build':>10s} {'DB Size':>8s} {'Search p50':>11s} {'Search p95':>11s}")
    for r in all_results:
        # Average across all queries
        query_p50s = [q["p50_ms"] for q in r["queries"] if "p50_ms" in q]
        query_p95s = [q["p95_ms"] for q in r["queries"] if "p95_ms" in q]
        avg_p50 = statistics.mean(query_p50s) if query_p50s else 0
        avg_p95 = statistics.mean(query_p95s) if query_p95s else 0
        print(f"{r['scale']:>10,d} {r['insert_seconds']:>7.1f}s {r['fts_build_seconds']:>9.1f}s "
              f"{r['db_size_mb']:>7.1f}MB {avg_p50:>10.2f}ms {avg_p95:>10.2f}ms")

    # Cleanup
    if BENCH_DB.exists():
        os.remove(BENCH_DB)
    print("\nBenchmark DB cleaned up.")


if __name__ == "__main__":
    main()
