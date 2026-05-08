"""
D2-R: Baseline Reproduction — confirm Spike 001 A1b measurement stability.

Re-runs FTS5 benchmark at 19K and 215K, compares against A1b's original
numbers. Acceptable variance: ±20%.

Usage:
    python d2_baseline_reproduction.py
"""

import json
import os
import sqlite3
import statistics
import time
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
A1B_RESULTS = SPIKE001_DATA / "fts5_benchmark_results.json"
BENCH_DB = DATA_DIR / "d2r_fts5_bench.db"
RESULTS_PATH = DATA_DIR / "d2_baseline_reproduction_results.json"

# Same queries as A1b
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

RUNS_PER_QUERY = 10
SCALE_POINTS = [19_000, 215_000]  # Match A1b's scale points
VARIANCE_THRESHOLD = 0.20  # ±20%


def load_source_papers() -> list[dict]:
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_fts5(papers, target):
    if BENCH_DB.exists():
        os.remove(BENCH_DB)
    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY, title TEXT, authors_text TEXT,
            abstract TEXT, categories TEXT, primary_category TEXT
        )
    """)
    batch = []
    for i in range(target):
        src = papers[i % len(papers)]
        aid = src["arxiv_id"] if i < len(papers) else f"synth.{i:07d}"
        batch.append((aid, src["title"], src["authors_text"],
                       src["abstract"], src["categories"], src["primary_category"]))
        if len(batch) >= 1000:
            conn.executemany("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?)", batch)
            batch = []
    if batch:
        conn.executemany("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?)", batch)
    conn.commit()
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text, content='papers', content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()
    conn.close()


def bench_query(qtext):
    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    # Warmup
    for _ in range(2):
        try:
            conn.execute(
                "SELECT p.arxiv_id, f.rank FROM papers_fts f "
                "JOIN papers p ON f.rowid = p.rowid "
                "WHERE papers_fts MATCH ? ORDER BY f.rank LIMIT 20",
                (qtext,),
            ).fetchall()
        except Exception:
            conn.close()
            return None
    latencies = []
    for _ in range(RUNS_PER_QUERY):
        t0 = time.perf_counter()
        conn.execute(
            "SELECT p.arxiv_id, f.rank FROM papers_fts f "
            "JOIN papers p ON f.rowid = p.rowid "
            "WHERE papers_fts MATCH ? ORDER BY f.rank LIMIT 20",
            (qtext,),
        ).fetchall()
        latencies.append((time.perf_counter() - t0) * 1000)
    conn.close()
    return round(statistics.median(latencies), 3)


def main():
    print("=" * 80)
    print("D2-R: Baseline Reproduction — A1b FTS5 Benchmark")
    print("=" * 80)

    # Load A1b original results
    if not A1B_RESULTS.exists():
        print(f"WARNING: A1b results not found at {A1B_RESULTS}")
        print("Will run benchmark but cannot compare against baseline.")
        a1b_data = None
    else:
        with open(A1B_RESULTS) as f:
            a1b_data = json.load(f)
        print(f"Loaded A1b baseline from {A1B_RESULTS.name}")

    papers = load_source_papers()
    print(f"Loaded {len(papers)} papers")

    results = {}
    stable = True

    for scale in SCALE_POINTS:
        print(f"\n{'=' * 60}")
        print(f"Scale: {scale:,}")
        print(f"{'=' * 60}")

        build_fts5(papers, scale)

        # Get A1b baseline for this scale
        a1b_scale = None
        if a1b_data:
            for entry in a1b_data:
                if entry.get("scale") == scale:
                    a1b_scale = entry
                    break

        scale_results = []

        print(f"  {'Query':<25s} {'Now p50':>10s} {'A1b p50':>10s} {'Variance':>10s} {'Status':>8s}")
        print(f"  {'-' * 65}")

        for qname, qtext in QUERIES:
            now_p50 = bench_query(qtext)

            # Find A1b baseline for this query
            a1b_p50 = None
            if a1b_scale:
                for q in a1b_scale.get("queries", []):
                    if q.get("query_name") == qname:
                        a1b_p50 = q.get("p50_ms")
                        break

            if now_p50 is None:
                print(f"  {qname:<25s} {'ERROR':>10s}")
                scale_results.append({"query_name": qname, "error": True})
                continue

            if a1b_p50 and a1b_p50 > 0:
                variance = (now_p50 - a1b_p50) / a1b_p50
                status = "OK" if abs(variance) <= VARIANCE_THRESHOLD else "DRIFT"
                if status == "DRIFT":
                    stable = False
                print(
                    f"  {qname:<25s} {now_p50:>8.2f}ms {a1b_p50:>8.2f}ms "
                    f"{variance:>+8.1%} {status:>8s}"
                )
            else:
                variance = None
                print(f"  {qname:<25s} {now_p50:>8.2f}ms {'—':>10s} {'—':>10s} {'N/A':>8s}")

            scale_results.append({
                "query_name": qname,
                "now_p50_ms": now_p50,
                "a1b_p50_ms": a1b_p50,
                "variance": round(variance, 4) if variance is not None else None,
                "within_threshold": abs(variance) <= VARIANCE_THRESHOLD if variance is not None else None,
            })

        results[str(scale)] = scale_results

        if BENCH_DB.exists():
            os.remove(BENCH_DB)

    # Summary
    print(f"\n{'=' * 80}")
    print(f"MEASUREMENT STABILITY: {'CONFIRMED' if stable else 'DRIFT DETECTED'}")
    print(f"Threshold: ±{VARIANCE_THRESHOLD:.0%}")
    print(f"{'=' * 80}")

    output = {
        "dimension": "D2-R",
        "description": "Baseline reproduction — A1b FTS5 measurement stability",
        "variance_threshold": VARIANCE_THRESHOLD,
        "measurement_stable": stable,
        "per_scale": results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
