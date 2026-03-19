"""
Dimension 2: Search Latency at Scale — FTS5 vs tsvector

Side-by-side latency comparison at same scale points and same queries.
First reproduces the Spike 001 A1b FTS5 baseline to confirm measurement
stability, then measures PostgreSQL tsvector at matching scale points.

Prerequisites:
- setup_spike002.py has been run
- spike_001_harvest.db available

Usage:
    python d2_search_latency.py
"""

import json
import os
import sqlite3
import statistics
import time
from pathlib import Path

import psycopg2

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
BENCH_DB = DATA_DIR / "d2_fts5_bench.db"
RESULTS_PATH = DATA_DIR / "d2_search_latency_results.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"

# Scale points matching Spike 001 (skip 500K for time — 215K is the max real scale)
SCALE_POINTS = [5_000, 10_000, 19_252, 50_000, 100_000, 215_000]

RUNS_PER_QUERY = 20
WARMUP_RUNS = 3

# Same query set as D1
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
    ("author_name", "Vaswani"),
    ("acronym_expansion", "GAN generative adversarial"),
    ("trending_topic", "diffusion model image generation"),
    ("subfield", "graph neural network"),
    ("cross_domain", "federated learning privacy"),
    ("math_adjacent", "theorem proof verification"),
    ("applied", "robotics manipulation"),
    ("stats_adjacent", "causal inference"),
    ("method_specific", "self-supervised contrastive"),
    ("very_common", "survey"),
]


# --- SQLite FTS5 ---

def load_source_papers() -> list[dict]:
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_fts5_db(papers: list[dict], target_size: int) -> float:
    """Build FTS5 DB at target scale. Returns build time."""
    if BENCH_DB.exists():
        os.remove(BENCH_DB)

    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

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

    # Insert papers cycling through source data
    batch = []
    for i in range(target_size):
        source = papers[i % len(papers)]
        aid = source["arxiv_id"] if i < len(papers) else f"synth.{i:07d}"
        batch.append((
            aid, source["title"], source["authors_text"],
            source["abstract"], source["categories"], source["primary_category"],
        ))
        if len(batch) >= 1000:
            conn.executemany("INSERT OR IGNORE INTO papers VALUES (?, ?, ?, ?, ?, ?)", batch)
            batch = []
    if batch:
        conn.executemany("INSERT OR IGNORE INTO papers VALUES (?, ?, ?, ?, ?, ?)", batch)
    conn.commit()

    # Build FTS5 index
    t0 = time.perf_counter()
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers', content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()
    build_time = time.perf_counter() - t0

    conn.close()
    return build_time


def bench_fts5_query(query_text: str) -> dict:
    """Benchmark a single FTS5 query."""
    conn = sqlite3.connect(str(BENCH_DB))
    conn.execute("PRAGMA journal_mode=WAL")

    # Warmup
    for _ in range(WARMUP_RUNS):
        try:
            conn.execute(
                "SELECT p.arxiv_id, f.rank FROM papers_fts f "
                "JOIN papers p ON f.rowid = p.rowid "
                "WHERE papers_fts MATCH ? ORDER BY f.rank LIMIT 20",
                (query_text,),
            ).fetchall()
        except Exception:
            conn.close()
            return {"error": f"FTS5 parse error for: {query_text}"}

    # Timed runs
    latencies = []
    result_count = 0
    for _ in range(RUNS_PER_QUERY):
        t0 = time.perf_counter()
        results = conn.execute(
            "SELECT p.arxiv_id, f.rank FROM papers_fts f "
            "JOIN papers p ON f.rowid = p.rowid "
            "WHERE papers_fts MATCH ? ORDER BY f.rank LIMIT 20",
            (query_text,),
        ).fetchall()
        latencies.append((time.perf_counter() - t0) * 1000)
        result_count = len(results)

    conn.close()
    return {
        "result_count": result_count,
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
    }


# --- PostgreSQL tsvector ---

def build_pg_at_scale(papers: list[dict], target_size: int) -> float:
    """Load PostgreSQL at target scale. Returns total setup time."""
    from psycopg2.extras import execute_values

    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()

    # Clean and recreate
    cur.execute("DROP TABLE IF EXISTS paper_embeddings CASCADE")
    cur.execute("DROP TABLE IF EXISTS papers CASCADE")
    cur.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors_text TEXT,
            abstract TEXT,
            categories TEXT,
            primary_category TEXT,
            search_vector tsvector
        )
    """)

    # Insert papers
    conn.autocommit = False
    values = []
    for i in range(target_size):
        source = papers[i % len(papers)]
        aid = source["arxiv_id"] if i < len(papers) else f"synth.{i:07d}"
        values.append((
            aid, source["title"], source["authors_text"],
            source["abstract"], source["categories"], source["primary_category"],
        ))

    # Batch insert
    for batch_start in range(0, len(values), 1000):
        batch = values[batch_start:batch_start + 1000]
        execute_values(
            cur,
            """INSERT INTO papers
               (arxiv_id, title, authors_text, abstract, categories, primary_category)
               VALUES %s ON CONFLICT (arxiv_id) DO NOTHING""",
            batch,
            page_size=1000,
        )
    conn.commit()

    # Populate tsvector
    t0 = time.perf_counter()
    cur.execute("""
        UPDATE papers SET search_vector =
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(abstract, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(authors_text, '')), 'C')
    """)
    conn.commit()

    # Create GIN index
    conn.autocommit = True
    cur.execute("CREATE INDEX idx_papers_search ON papers USING GIN (search_vector)")
    build_time = time.perf_counter() - t0

    # ANALYZE for query planner
    cur.execute("ANALYZE papers")

    cur.close()
    conn.close()
    return build_time


def bench_pg_query(query_text: str) -> dict:
    """Benchmark a single tsvector query."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    # Warmup
    for _ in range(WARMUP_RUNS):
        try:
            cur.execute(
                """SELECT arxiv_id,
                          ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) AS rank
                   FROM papers
                   WHERE search_vector @@ websearch_to_tsquery('english', %s)
                   ORDER BY rank DESC LIMIT 20""",
                (query_text, query_text),
            )
            cur.fetchall()
        except Exception:
            conn.rollback()
            cur.close()
            conn.close()
            return {"error": f"tsvector parse error for: {query_text}"}

    # Timed runs
    latencies = []
    result_count = 0
    for _ in range(RUNS_PER_QUERY):
        t0 = time.perf_counter()
        cur.execute(
            """SELECT arxiv_id,
                      ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) AS rank
               FROM papers
               WHERE search_vector @@ websearch_to_tsquery('english', %s)
               ORDER BY rank DESC LIMIT 20""",
            (query_text, query_text),
        )
        cur.fetchall()
        latencies.append((time.perf_counter() - t0) * 1000)
        result_count = len(cur.description) if cur.description else 0

    # Get actual result count from last run
    cur.execute(
        """SELECT COUNT(*) FROM papers
           WHERE search_vector @@ websearch_to_tsquery('english', %s)""",
        (query_text,),
    )
    total_matches = cur.fetchone()[0]

    cur.close()
    conn.close()
    return {
        "result_count": min(total_matches, 20),
        "total_matches": total_matches,
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(sorted(latencies)[int(len(latencies) * 0.95)], 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "min_ms": round(min(latencies), 3),
        "max_ms": round(max(latencies), 3),
    }


def main():
    print("=" * 80)
    print("Dimension 2: Search Latency at Scale (FTS5 vs tsvector)")
    print("=" * 80)

    papers = load_source_papers()
    print(f"Loaded {len(papers)} source papers")

    all_results = []

    for scale in SCALE_POINTS:
        print(f"\n{'=' * 80}")
        print(f"SCALE: {scale:,} papers")
        print(f"{'=' * 80}")

        # Build FTS5
        print("  Building FTS5 index...")
        fts5_build = build_fts5_db(papers, scale)
        fts5_db_size = os.path.getsize(BENCH_DB) / 1024 / 1024
        print(f"  FTS5 built in {fts5_build:.2f}s ({fts5_db_size:.1f} MB)")

        # Build PostgreSQL
        print("  Building tsvector + GIN index...")
        pg_build = build_pg_at_scale(papers, scale)
        print(f"  tsvector+GIN built in {pg_build:.2f}s")

        # Get PG size
        conn = psycopg2.connect(PG_DSN)
        cur = conn.cursor()
        cur.execute("SELECT pg_total_relation_size('papers') / 1024.0 / 1024.0")
        pg_size_mb = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM papers")
        pg_count = cur.fetchone()[0]
        cur.close()
        conn.close()
        print(f"  PostgreSQL: {pg_count} papers, {pg_size_mb:.1f} MB")

        scale_result = {
            "scale": scale,
            "fts5_build_s": round(fts5_build, 3),
            "fts5_size_mb": round(fts5_db_size, 1),
            "pg_build_s": round(pg_build, 3),
            "pg_size_mb": round(float(pg_size_mb), 1),
            "queries": [],
        }

        # Benchmark each query on both backends
        print(f"\n  {'Query':<25s} {'FTS5 p50':>10s} {'tsv p50':>10s} {'Ratio':>8s}")
        print(f"  {'-' * 55}")

        for qname, qtext in QUERIES:
            fts5_result = bench_fts5_query(qtext)
            pg_result = bench_pg_query(qtext)

            query_result = {
                "query_name": qname,
                "query_text": qtext,
                "fts5": fts5_result,
                "tsvector": pg_result,
            }
            scale_result["queries"].append(query_result)

            # Print comparison
            if "error" in fts5_result:
                f_p50 = "ERROR"
                ratio = "—"
            else:
                f_p50 = f"{fts5_result['p50_ms']:.2f}ms"

            if "error" in pg_result:
                t_p50 = "ERROR"
                ratio = "—"
            else:
                t_p50 = f"{pg_result['p50_ms']:.2f}ms"

            if "error" not in fts5_result and "error" not in pg_result:
                if fts5_result["p50_ms"] > 0:
                    r = pg_result["p50_ms"] / fts5_result["p50_ms"]
                    ratio = f"{r:.1f}x"
                else:
                    ratio = "—"

            print(f"  {qname:<25s} {f_p50:>10s} {t_p50:>10s} {ratio:>8s}")

        # Compute averages (excluding errors)
        fts5_p50s = [
            q["fts5"]["p50_ms"] for q in scale_result["queries"]
            if "error" not in q["fts5"]
        ]
        pg_p50s = [
            q["tsvector"]["p50_ms"] for q in scale_result["queries"]
            if "error" not in q["tsvector"]
        ]

        if fts5_p50s and pg_p50s:
            avg_fts5 = statistics.mean(fts5_p50s)
            avg_pg = statistics.mean(pg_p50s)
            scale_result["avg_fts5_p50_ms"] = round(avg_fts5, 3)
            scale_result["avg_pg_p50_ms"] = round(avg_pg, 3)
            scale_result["avg_ratio"] = round(avg_pg / avg_fts5, 2) if avg_fts5 > 0 else None
            print(f"\n  Average: FTS5={avg_fts5:.2f}ms  tsv={avg_pg:.2f}ms  ratio={avg_pg/avg_fts5:.1f}x")

        all_results.append(scale_result)

        # Cleanup FTS5 bench DB between scales
        if BENCH_DB.exists():
            os.remove(BENCH_DB)

    # Save results
    output = {
        "dimension": "D2",
        "description": "Search Latency at Scale — FTS5 vs tsvector",
        "scale_points": SCALE_POINTS,
        "runs_per_query": RUNS_PER_QUERY,
        "warmup_runs": WARMUP_RUNS,
        "per_scale": all_results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)

    # Print summary table
    print(f"\n{'=' * 80}")
    print("SUMMARY: Average p50 latency by scale")
    print(f"{'=' * 80}")
    print(f"  {'Scale':>10s} {'FTS5 p50':>12s} {'tsvector p50':>14s} {'Ratio':>8s}")
    print(f"  {'-' * 48}")
    for r in all_results:
        f = r.get("avg_fts5_p50_ms", 0)
        p = r.get("avg_pg_p50_ms", 0)
        ratio = r.get("avg_ratio", 0)
        print(f"  {r['scale']:>10,d} {f:>10.2f}ms {p:>12.2f}ms {ratio:>7.1f}x")

    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
