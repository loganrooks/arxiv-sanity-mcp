"""
A1c.2: Concurrent SQLite Read+Write Benchmark

Measures the impact of concurrent writes on FTS5 search latency.
Simulates the real-world scenario: harvest daemon inserting papers
while MCP server handles search queries on the same database.

Tests WAL mode vs default journal mode at multiple write rates.

Output: JSON results file + console summary.
"""

import json
import os
import shutil
import sqlite3
import threading
import time
from pathlib import Path

import numpy as np

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
BENCH_DB = DATA_DIR / "concurrent_benchmark.db"
RESULTS_PATH = DATA_DIR / "concurrent_benchmark_results.json"

# Write rates to test (papers per second)
WRITE_RATES = [0, 1, 10, 50, 100]

# Journal modes to test
JOURNAL_MODES = ["delete", "wal"]

# Batch sizes for writes (papers per INSERT transaction)
BATCH_SIZES = [1, 10]

# Duration of each test run in seconds
RUN_DURATION = 10

# Pre-populate with this many papers before testing
PREPOPULATE = 10_000

# Search queries (representative mix from A1b)
QUERIES = [
    "transformer",
    "language model",
    "reinforcement learning agent",
    "attention AND mechanism",
    '"large language model"',
    "neural network optimization",
    "RLHF alignment",
]

# --- Helpers ---


def load_papers(db_path: str) -> list[dict]:
    """Load all papers with abstracts from the harvest DB."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date FROM papers "
        "WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def create_bench_db(journal_mode: str, papers: list[dict], n_prepopulate: int) -> str:
    """Create a fresh benchmark DB with FTS5 and pre-populated papers."""
    if BENCH_DB.exists():
        BENCH_DB.unlink()
    # Also remove WAL/SHM files
    for ext in ["-wal", "-shm"]:
        p = Path(str(BENCH_DB) + ext)
        if p.exists():
            p.unlink()

    conn = sqlite3.connect(str(BENCH_DB))

    # Set journal mode
    conn.execute(f"PRAGMA journal_mode={journal_mode}")
    conn.execute("PRAGMA busy_timeout=5000")  # 5 second busy timeout

    # Create tables
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            authors_text TEXT,
            abstract TEXT,
            categories TEXT,
            primary_category TEXT,
            submitted_date TEXT
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers',
            content_rowid='rowid',
            tokenize='porter'
        )
    """)
    # Triggers to keep FTS in sync
    conn.execute("""
        CREATE TRIGGER papers_ai AFTER INSERT ON papers BEGIN
            INSERT INTO papers_fts(rowid, title, abstract, authors_text)
            VALUES (new.rowid, new.title, new.abstract, new.authors_text);
        END
    """)

    # Pre-populate
    for i in range(min(n_prepopulate, len(papers))):
        p = papers[i]
        conn.execute(
            "INSERT INTO papers (arxiv_id, title, authors_text, abstract, "
            "categories, primary_category, submitted_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (p["arxiv_id"], p["title"], p["authors_text"], p["abstract"],
             p["categories"], p["primary_category"], p["submitted_date"]),
        )
    conn.commit()
    conn.close()
    return str(BENCH_DB)


def fmt_ms(seconds: float) -> str:
    return f"{seconds * 1000:.1f}ms"


# --- Worker threads ---


def reader_worker(
    db_path: str,
    journal_mode: str,
    stop_event: threading.Event,
    latencies: list,
    errors: list,
):
    """Continuously run FTS5 searches, recording latency for each."""
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute(f"PRAGMA journal_mode={journal_mode}")
    conn.execute("PRAGMA busy_timeout=5000")
    query_idx = 0

    while not stop_event.is_set():
        query = QUERIES[query_idx % len(QUERIES)]
        query_idx += 1

        try:
            t0 = time.monotonic()
            # Use MATCH for FTS5 search, same as real MCP server
            rows = conn.execute(
                "SELECT p.arxiv_id, p.title, rank "
                "FROM papers_fts fts "
                "JOIN papers p ON p.rowid = fts.rowid "
                "WHERE papers_fts MATCH ? "
                "ORDER BY rank "
                "LIMIT 20",
                (query,),
            ).fetchall()
            elapsed = time.monotonic() - t0
            latencies.append(elapsed)
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                errors.append(("read_locked", time.monotonic()))
            else:
                errors.append(("read_error", str(e)))

    conn.close()


def writer_worker(
    db_path: str,
    journal_mode: str,
    papers: list[dict],
    write_rate: float,
    batch_size: int,
    stop_event: threading.Event,
    write_counts: list,
    errors: list,
    start_id: int,
):
    """Insert papers at a target rate, recording throughput and errors."""
    if write_rate == 0:
        # No writes — just wait for stop
        stop_event.wait()
        return

    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute(f"PRAGMA journal_mode={journal_mode}")
    conn.execute("PRAGMA busy_timeout=5000")

    interval = batch_size / write_rate  # seconds between batches
    paper_idx = start_id
    total_written = 0

    while not stop_event.is_set():
        batch_start = time.monotonic()

        try:
            for _ in range(batch_size):
                p = papers[paper_idx % len(papers)]
                # Generate unique ID to avoid conflicts
                new_id = f"bench.{paper_idx:08d}"
                conn.execute(
                    "INSERT OR IGNORE INTO papers "
                    "(arxiv_id, title, authors_text, abstract, categories, "
                    "primary_category, submitted_date) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_id, p["title"], p["authors_text"], p["abstract"],
                     p["categories"], p["primary_category"], p["submitted_date"]),
                )
                paper_idx += 1
            conn.commit()
            total_written += batch_size
            write_counts.append((time.monotonic(), batch_size))
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                errors.append(("write_locked", time.monotonic()))
            else:
                errors.append(("write_error", str(e)))

        # Sleep to maintain target rate
        elapsed = time.monotonic() - batch_start
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    conn.close()


# --- Main benchmark ---


def run_single_test(
    journal_mode: str,
    write_rate: int,
    batch_size: int,
    papers: list[dict],
    duration: int,
) -> dict:
    """Run a single concurrent read+write test."""
    db_path = create_bench_db(journal_mode, papers, PREPOPULATE)

    stop_event = threading.Event()
    read_latencies = []
    read_errors = []
    write_counts = []
    write_errors = []

    # Start reader
    reader = threading.Thread(
        target=reader_worker,
        args=(db_path, journal_mode, stop_event, read_latencies, read_errors),
    )

    # Start writer
    writer = threading.Thread(
        target=writer_worker,
        args=(db_path, journal_mode, papers, write_rate, batch_size,
              stop_event, write_counts, write_errors, PREPOPULATE),
    )

    reader.start()
    writer.start()

    # Let it run
    time.sleep(duration)
    stop_event.set()

    reader.join(timeout=10)
    writer.join(timeout=10)

    # Compute statistics
    latencies = np.array(read_latencies) if read_latencies else np.array([0])
    total_writes = sum(c for _, c in write_counts)
    actual_write_rate = total_writes / duration if duration > 0 else 0

    result = {
        "journal_mode": journal_mode,
        "target_write_rate": write_rate,
        "batch_size": batch_size,
        "duration_s": duration,
        "prepopulated": PREPOPULATE,
        "search_count": len(read_latencies),
        "search_rate": len(read_latencies) / duration if duration > 0 else 0,
        "search_p50_ms": round(float(np.median(latencies)) * 1000, 2),
        "search_p95_ms": round(float(np.percentile(latencies, 95)) * 1000, 2),
        "search_p99_ms": round(float(np.percentile(latencies, 99)) * 1000, 2),
        "search_max_ms": round(float(np.max(latencies)) * 1000, 2),
        "search_min_ms": round(float(np.min(latencies)) * 1000, 2),
        "total_writes": total_writes,
        "actual_write_rate": round(actual_write_rate, 1),
        "read_lock_errors": sum(1 for e in read_errors if e[0] == "read_locked"),
        "write_lock_errors": sum(1 for e in write_errors if e[0] == "write_locked"),
        "read_other_errors": sum(1 for e in read_errors if e[0] != "read_locked"),
        "write_other_errors": sum(1 for e in write_errors if e[0] != "write_locked"),
    }

    return result


def run_benchmark():
    print(f"Loading papers from {SOURCE_DB}...")
    papers = load_papers(str(SOURCE_DB))
    print(f"Loaded {len(papers)} papers")

    all_results = []

    for journal_mode in JOURNAL_MODES:
        for batch_size in BATCH_SIZES:
            print(f"\n{'=' * 70}")
            print(f"Journal mode: {journal_mode.upper()}, Batch size: {batch_size}")
            print(f"{'=' * 70}")

            for write_rate in WRITE_RATES:
                label = f"  {write_rate:>3} writes/s (batch={batch_size})"
                print(f"\n{label}")

                result = run_single_test(
                    journal_mode, write_rate, batch_size, papers, RUN_DURATION
                )
                all_results.append(result)

                print(f"    Searches:    {result['search_count']} ({result['search_rate']:.0f}/s)")
                print(f"    Search p50:  {result['search_p50_ms']:.1f}ms")
                print(f"    Search p95:  {result['search_p95_ms']:.1f}ms")
                print(f"    Search p99:  {result['search_p99_ms']:.1f}ms")
                print(f"    Search max:  {result['search_max_ms']:.1f}ms")
                print(f"    Writes:      {result['total_writes']} ({result['actual_write_rate']}/s actual)")
                print(f"    Lock errors: read={result['read_lock_errors']}, write={result['write_lock_errors']}")

    # Save results
    with open(RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")

    # Print comparison tables
    print_summary(all_results)


def print_summary(results: list[dict]):
    """Print summary comparison tables."""
    print(f"\n{'=' * 90}")
    print("SUMMARY: Search p50 latency (ms) by journal mode and write rate")
    print(f"{'=' * 90}")

    for batch_size in BATCH_SIZES:
        print(f"\nBatch size: {batch_size}")
        header = f"{'Mode':<10}"
        for wr in WRITE_RATES:
            header += f"  {wr}/s".rjust(12)
        print(header)
        print("-" * 80)

        for jm in JOURNAL_MODES:
            row = f"{jm:<10}"
            for wr in WRITE_RATES:
                match = [r for r in results
                         if r["journal_mode"] == jm
                         and r["target_write_rate"] == wr
                         and r["batch_size"] == batch_size]
                if match:
                    row += f"  {match[0]['search_p50_ms']:.1f}ms".rjust(12)
                else:
                    row += "  —".rjust(12)
            print(row)

    print(f"\n{'=' * 90}")
    print("SUMMARY: Search p95 latency (ms) by journal mode and write rate")
    print(f"{'=' * 90}")

    for batch_size in BATCH_SIZES:
        print(f"\nBatch size: {batch_size}")
        header = f"{'Mode':<10}"
        for wr in WRITE_RATES:
            header += f"  {wr}/s".rjust(12)
        print(header)
        print("-" * 80)

        for jm in JOURNAL_MODES:
            row = f"{jm:<10}"
            for wr in WRITE_RATES:
                match = [r for r in results
                         if r["journal_mode"] == jm
                         and r["target_write_rate"] == wr
                         and r["batch_size"] == batch_size]
                if match:
                    row += f"  {match[0]['search_p95_ms']:.1f}ms".rjust(12)
                else:
                    row += "  —".rjust(12)
            print(row)

    print(f"\n{'=' * 90}")
    print("SUMMARY: Lock errors by journal mode and write rate")
    print(f"{'=' * 90}")

    for batch_size in BATCH_SIZES:
        print(f"\nBatch size: {batch_size}")
        header = f"{'Mode':<10}"
        for wr in WRITE_RATES:
            header += f"  {wr}/s".rjust(12)
        print(header)
        print("-" * 80)

        for jm in JOURNAL_MODES:
            row = f"{jm:<10}"
            for wr in WRITE_RATES:
                match = [r for r in results
                         if r["journal_mode"] == jm
                         and r["target_write_rate"] == wr
                         and r["batch_size"] == batch_size]
                if match:
                    total = match[0]["read_lock_errors"] + match[0]["write_lock_errors"]
                    row += f"  {total}".rjust(12)
                else:
                    row += "  —".rjust(12)
            print(row)


if __name__ == "__main__":
    run_benchmark()
