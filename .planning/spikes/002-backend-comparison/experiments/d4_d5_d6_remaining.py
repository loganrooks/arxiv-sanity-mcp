"""
Dimensions 4-6: Write Performance, Operational Characteristics, Workflow Comparison

D4: Bulk import, incremental writes, concurrent read+write
D5: Connection setup, backup/restore, disk footprint
D6: Simulated multi-tool MCP workflow

Prerequisites:
- setup_spike002.py has been run
- spike_001_harvest.db available

Usage:
    python d4_d5_d6_remaining.py
"""

import json
import os
import shutil
import sqlite3
import statistics
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
RESULTS_PATH = DATA_DIR / "d4_d5_d6_results.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"

SCALE_POINTS = [5_000, 10_000, 19_252, 50_000, 100_000, 215_000]


def load_source_papers() -> list[dict]:
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ======================================================================
# DIMENSION 4: Write Performance
# ======================================================================

def d4_sqlite_bulk_import(papers: list[dict], target: int) -> dict:
    """Measure SQLite bulk import time."""
    db_path = DATA_DIR / "d4_sqlite_temp.db"
    if db_path.exists():
        os.remove(db_path)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT, authors_text TEXT, abstract TEXT,
            categories TEXT, primary_category TEXT
        )
    """)

    t0 = time.perf_counter()
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
    wall_time = time.perf_counter() - t0

    # Build FTS index
    t1 = time.perf_counter()
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers', content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()
    fts_time = time.perf_counter() - t1

    db_size = os.path.getsize(db_path)
    conn.close()
    os.remove(db_path)

    return {
        "insert_time_s": round(wall_time, 3),
        "fts_build_time_s": round(fts_time, 3),
        "total_time_s": round(wall_time + fts_time, 3),
        "db_size_bytes": db_size,
    }


def d4_pg_bulk_import(papers: list[dict], target: int) -> dict:
    """Measure PostgreSQL bulk import time."""
    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS paper_embeddings CASCADE")
    cur.execute("DROP TABLE IF EXISTS papers CASCADE")
    cur.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT NOT NULL, authors_text TEXT, abstract TEXT,
            categories TEXT, primary_category TEXT,
            search_vector tsvector
        )
    """)

    conn.autocommit = False
    t0 = time.perf_counter()

    values = []
    for i in range(target):
        src = papers[i % len(papers)]
        aid = src["arxiv_id"] if i < len(papers) else f"synth.{i:07d}"
        values.append((aid, src["title"], src["authors_text"],
                        src["abstract"], src["categories"], src["primary_category"]))

    for bs in range(0, len(values), 1000):
        batch = values[bs:bs + 1000]
        execute_values(
            cur,
            "INSERT INTO papers (arxiv_id,title,authors_text,abstract,categories,primary_category) "
            "VALUES %s ON CONFLICT DO NOTHING",
            batch, page_size=1000,
        )
    conn.commit()
    insert_time = time.perf_counter() - t0

    # Build tsvector + GIN
    conn.autocommit = True
    t1 = time.perf_counter()
    cur.execute("""
        UPDATE papers SET search_vector =
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(abstract, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(authors_text, '')), 'C')
    """)
    cur.execute("CREATE INDEX idx_papers_search ON papers USING GIN (search_vector)")
    tsv_time = time.perf_counter() - t1

    # Get size
    cur.execute("SELECT pg_total_relation_size('papers')")
    db_size = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "insert_time_s": round(insert_time, 3),
        "tsvector_build_time_s": round(tsv_time, 3),
        "total_time_s": round(insert_time + tsv_time, 3),
        "db_size_bytes": db_size,
    }


def d4_concurrent_readwrite_pg() -> dict:
    """Measure search latency during sustained writes on PostgreSQL."""
    # First, ensure 19K papers are loaded
    papers = load_source_papers()
    d4_pg_bulk_import(papers, 19_252)

    results = {"write_rates": []}

    for writes_per_sec in [10, 50, 100]:
        write_interval = 1.0 / writes_per_sec
        search_latencies = []
        write_errors = 0
        write_count = 0
        stop_writing = False

        def writer():
            nonlocal write_errors, write_count, stop_writing
            conn = psycopg2.connect(PG_DSN)
            conn.autocommit = True
            cur = conn.cursor()
            i = 0
            while not stop_writing:
                try:
                    aid = f"concurrent.{i:07d}"
                    cur.execute(
                        "INSERT INTO papers (arxiv_id,title,authors_text,abstract,categories,primary_category) "
                        "VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (arxiv_id) DO NOTHING",
                        (aid, f"Test paper {i}", "Author", "Abstract text", "cs.AI", "cs.AI"),
                    )
                    write_count += 1
                except Exception:
                    write_errors += 1
                i += 1
                time.sleep(write_interval)
            cur.close()
            conn.close()

        # Start writer thread
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(writer)

            # Let writes stabilize
            time.sleep(0.5)

            # Run search queries
            conn = psycopg2.connect(PG_DSN)
            cur = conn.cursor()
            for _ in range(20):
                t0 = time.perf_counter()
                cur.execute(
                    "SELECT arxiv_id, ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) "
                    "FROM papers WHERE search_vector @@ websearch_to_tsquery('english', %s) "
                    "ORDER BY ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) DESC LIMIT 20",
                    ("transformer", "transformer", "transformer"),
                )
                cur.fetchall()
                search_latencies.append((time.perf_counter() - t0) * 1000)
            cur.close()
            conn.close()

            stop_writing = True
            future.result()

        results["write_rates"].append({
            "target_writes_per_sec": writes_per_sec,
            "actual_writes": write_count,
            "write_errors": write_errors,
            "search_p50_ms": round(statistics.median(search_latencies), 3),
            "search_p95_ms": round(sorted(search_latencies)[int(len(search_latencies) * 0.95)], 3),
            "search_mean_ms": round(statistics.mean(search_latencies), 3),
        })

    # Cleanup concurrent rows
    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DELETE FROM papers WHERE arxiv_id LIKE 'concurrent.%'")
    cur.close()
    conn.close()

    return results


# ======================================================================
# DIMENSION 5: Operational Characteristics
# ======================================================================

def d5_connection_setup() -> dict:
    """Measure connection setup time for both backends."""
    # SQLite
    db_path = DATA_DIR / "d5_sqlite_temp.db"
    sqlite3.connect(str(db_path)).close()  # Create file

    sqlite_times = []
    for _ in range(50):
        t0 = time.perf_counter()
        conn = sqlite3.connect(str(db_path))
        conn.execute("SELECT 1")
        conn.close()
        sqlite_times.append((time.perf_counter() - t0) * 1000)

    os.remove(db_path)

    # PostgreSQL
    pg_times = []
    for _ in range(50):
        t0 = time.perf_counter()
        conn = psycopg2.connect(PG_DSN)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        pg_times.append((time.perf_counter() - t0) * 1000)

    return {
        "sqlite": {
            "p50_ms": round(statistics.median(sqlite_times), 3),
            "p95_ms": round(sorted(sqlite_times)[int(len(sqlite_times) * 0.95)], 3),
            "mean_ms": round(statistics.mean(sqlite_times), 3),
        },
        "postgresql": {
            "p50_ms": round(statistics.median(pg_times), 3),
            "p95_ms": round(sorted(pg_times)[int(len(pg_times) * 0.95)], 3),
            "mean_ms": round(statistics.mean(pg_times), 3),
        },
    }


def d5_backup_restore() -> dict:
    """Measure backup and restore times."""
    results = {}

    # SQLite: just file copy
    # First create a populated DB
    papers = load_source_papers()
    db_path = DATA_DIR / "d5_sqlite_backup_test.db"
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY, title TEXT, authors_text TEXT,
            abstract TEXT, categories TEXT, primary_category TEXT
        )
    """)
    for i in range(0, len(papers), 1000):
        batch = [(p["arxiv_id"], p["title"], p["authors_text"],
                   p["abstract"], p["categories"], p["primary_category"])
                  for p in papers[i:i+1000]]
        conn.executemany("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?)", batch)
    conn.commit()
    conn.close()

    backup_path = DATA_DIR / "d5_sqlite_backup.db"
    # Backup
    t0 = time.perf_counter()
    shutil.copy2(db_path, backup_path)
    sqlite_backup = time.perf_counter() - t0

    # Restore
    os.remove(db_path)
    t0 = time.perf_counter()
    shutil.copy2(backup_path, db_path)
    sqlite_restore = time.perf_counter() - t0

    sqlite_size = os.path.getsize(db_path)
    os.remove(db_path)
    os.remove(backup_path)

    results["sqlite_19k"] = {
        "backup_time_s": round(sqlite_backup, 3),
        "restore_time_s": round(sqlite_restore, 3),
        "file_size_bytes": sqlite_size,
    }

    # PostgreSQL: pg_dump / pg_restore
    dump_path = DATA_DIR / "d5_pg_dump.sql"

    # Ensure 19K data is loaded
    d4_pg_bulk_import(papers, 19_252)

    t0 = time.perf_counter()
    result = subprocess.run(
        ["pg_dump", "-h", "localhost", "-U", "arxiv_mcp", "-d", "arxiv_mcp_spike002",
         "-f", str(dump_path), "--format=plain"],
        env={**os.environ, "PGPASSWORD": "arxiv_mcp_dev"},
        capture_output=True, text=True,
    )
    pg_backup = time.perf_counter() - t0

    pg_dump_size = dump_path.stat().st_size if dump_path.exists() else 0

    results["postgresql_19k"] = {
        "backup_time_s": round(pg_backup, 3),
        "dump_size_bytes": pg_dump_size,
        "backup_error": result.stderr if result.returncode != 0 else None,
    }

    # Cleanup
    dump_path.unlink(missing_ok=True)

    return results


def d5_disk_footprint(papers: list[dict]) -> dict:
    """Measure disk usage at each scale point."""
    results = []

    for scale in SCALE_POINTS:
        # SQLite
        db_path = DATA_DIR / "d5_disk_temp.db"
        if db_path.exists():
            os.remove(db_path)

        conn = sqlite3.connect(str(db_path))
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE papers (
                arxiv_id TEXT PRIMARY KEY, title TEXT, authors_text TEXT,
                abstract TEXT, categories TEXT, primary_category TEXT
            )
        """)
        for i in range(0, scale, 1000):
            batch = []
            for j in range(i, min(i + 1000, scale)):
                src = papers[j % len(papers)]
                aid = src["arxiv_id"] if j < len(papers) else f"synth.{j:07d}"
                batch.append((aid, src["title"], src["authors_text"],
                               src["abstract"], src["categories"], src["primary_category"]))
            conn.executemany("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?)", batch)
        conn.commit()

        # Add FTS
        conn.execute("""
            CREATE VIRTUAL TABLE papers_fts USING fts5(
                title, abstract, authors_text,
                content='papers', content_rowid='rowid',
                tokenize='porter unicode61'
            )
        """)
        conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
        conn.commit()
        conn.close()

        sqlite_size = os.path.getsize(db_path)
        # Check WAL size
        wal_path = Path(str(db_path) + "-wal")
        sqlite_wal = wal_path.stat().st_size if wal_path.exists() else 0
        os.remove(db_path)
        wal_path.unlink(missing_ok=True)
        Path(str(db_path) + "-shm").unlink(missing_ok=True)

        # PostgreSQL
        pg_info = d4_pg_bulk_import(papers, scale)

        results.append({
            "scale": scale,
            "sqlite_bytes": sqlite_size,
            "sqlite_wal_bytes": sqlite_wal,
            "sqlite_total_bytes": sqlite_size + sqlite_wal,
            "pg_bytes": pg_info["db_size_bytes"],
            "ratio": round(pg_info["db_size_bytes"] / sqlite_size, 2) if sqlite_size > 0 else None,
        })

    return results


# ======================================================================
# DIMENSION 6: Workflow-Level Comparison
# ======================================================================

def d6_workflow_sqlite(papers: list[dict]) -> dict:
    """Simulate a 6-tool MCP workflow on SQLite."""
    db_path = DATA_DIR / "d6_sqlite_temp.db"
    if db_path.exists():
        os.remove(db_path)

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY, title TEXT, authors_text TEXT,
            abstract TEXT, categories TEXT, primary_category TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE collections (
            id INTEGER PRIMARY KEY, name TEXT UNIQUE
        )
    """)
    conn.execute("""
        CREATE TABLE collection_papers (
            collection_id INTEGER, arxiv_id TEXT,
            PRIMARY KEY (collection_id, arxiv_id)
        )
    """)
    conn.execute("""
        CREATE TABLE triage_states (
            arxiv_id TEXT PRIMARY KEY, state TEXT
        )
    """)

    for i in range(0, len(papers), 1000):
        batch = [(p["arxiv_id"], p["title"], p["authors_text"],
                   p["abstract"], p["categories"], p["primary_category"])
                  for p in papers[i:i+1000]]
        conn.executemany("INSERT OR IGNORE INTO papers VALUES (?,?,?,?,?,?)", batch)
    conn.commit()
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers', content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()

    latencies = []
    for run in range(10):
        t0 = time.perf_counter()

        # 1. search
        results = conn.execute(
            "SELECT p.arxiv_id, f.rank FROM papers_fts f "
            "JOIN papers p ON f.rowid = p.rowid "
            "WHERE papers_fts MATCH 'transformer' ORDER BY f.rank LIMIT 20",
        ).fetchall()

        # 2. get_paper (first result)
        if results:
            paper_id = results[0][0]
            conn.execute("SELECT * FROM papers WHERE arxiv_id = ?", (paper_id,)).fetchone()

            # 3. find_related (same category)
            cat = conn.execute(
                "SELECT primary_category FROM papers WHERE arxiv_id = ?", (paper_id,)
            ).fetchone()[0]
            conn.execute(
                "SELECT arxiv_id, title FROM papers WHERE primary_category = ? LIMIT 10",
                (cat,),
            ).fetchall()

            # 4. triage
            conn.execute(
                "INSERT OR REPLACE INTO triage_states VALUES (?, 'interesting')",
                (paper_id,),
            )

            # 5. add_to_collection
            conn.execute("INSERT OR IGNORE INTO collections (name) VALUES ('research')")
            col_id = conn.execute("SELECT id FROM collections WHERE name = 'research'").fetchone()[0]
            conn.execute(
                "INSERT OR IGNORE INTO collection_papers VALUES (?, ?)", (col_id, paper_id)
            )

            # 6. check_watch (recent papers)
            conn.execute(
                "SELECT arxiv_id, title FROM papers ORDER BY rowid DESC LIMIT 20"
            ).fetchall()

        conn.commit()
        latencies.append((time.perf_counter() - t0) * 1000)

    conn.close()
    os.remove(db_path)
    Path(str(db_path) + "-wal").unlink(missing_ok=True)
    Path(str(db_path) + "-shm").unlink(missing_ok=True)

    return {
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(max(latencies), 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "runs": len(latencies),
    }


def d6_workflow_pg(papers: list[dict]) -> dict:
    """Simulate a 6-tool MCP workflow on PostgreSQL."""
    # Ensure full schema
    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS collection_papers CASCADE")
    cur.execute("DROP TABLE IF EXISTS triage_states CASCADE")
    cur.execute("DROP TABLE IF EXISTS collections CASCADE")
    cur.execute("DROP TABLE IF EXISTS paper_embeddings CASCADE")
    cur.execute("DROP TABLE IF EXISTS papers CASCADE")
    cur.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY, title TEXT NOT NULL, authors_text TEXT,
            abstract TEXT, categories TEXT, primary_category TEXT,
            search_vector tsvector
        )
    """)
    cur.execute("CREATE TABLE collections (id SERIAL PRIMARY KEY, name TEXT UNIQUE)")
    cur.execute("""
        CREATE TABLE collection_papers (
            collection_id INT REFERENCES collections(id),
            arxiv_id TEXT REFERENCES papers(arxiv_id),
            PRIMARY KEY (collection_id, arxiv_id)
        )
    """)
    cur.execute("""
        CREATE TABLE triage_states (
            arxiv_id TEXT PRIMARY KEY REFERENCES papers(arxiv_id),
            state TEXT NOT NULL
        )
    """)

    # Load papers
    conn.autocommit = False
    values = [(p["arxiv_id"], p["title"], p["authors_text"],
                p["abstract"], p["categories"], p["primary_category"])
               for p in papers]
    for bs in range(0, len(values), 1000):
        batch = values[bs:bs + 1000]
        execute_values(
            cur,
            "INSERT INTO papers (arxiv_id,title,authors_text,abstract,categories,primary_category) "
            "VALUES %s ON CONFLICT DO NOTHING",
            batch, page_size=1000,
        )
    conn.commit()
    conn.autocommit = True

    cur.execute("""
        UPDATE papers SET search_vector =
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(abstract, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(authors_text, '')), 'C')
    """)
    cur.execute("CREATE INDEX idx_papers_search ON papers USING GIN (search_vector)")
    cur.execute("ANALYZE papers")

    # Run workflow
    latencies = []
    for run in range(10):
        t0 = time.perf_counter()

        # 1. search
        cur.execute(
            "SELECT arxiv_id, ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) AS rank "
            "FROM papers WHERE search_vector @@ websearch_to_tsquery('english', %s) "
            "ORDER BY rank DESC LIMIT 20",
            ("transformer", "transformer"),
        )
        results = cur.fetchall()

        if results:
            paper_id = results[0][0]

            # 2. get_paper
            cur.execute("SELECT * FROM papers WHERE arxiv_id = %s", (paper_id,))
            cur.fetchone()

            # 3. find_related
            cur.execute("SELECT primary_category FROM papers WHERE arxiv_id = %s", (paper_id,))
            cat = cur.fetchone()[0]
            cur.execute(
                "SELECT arxiv_id, title FROM papers WHERE primary_category = %s LIMIT 10",
                (cat,),
            )
            cur.fetchall()

            # 4. triage
            cur.execute(
                "INSERT INTO triage_states (arxiv_id, state) VALUES (%s, 'interesting') "
                "ON CONFLICT (arxiv_id) DO UPDATE SET state = 'interesting'",
                (paper_id,),
            )

            # 5. add_to_collection
            cur.execute(
                "INSERT INTO collections (name) VALUES ('research') "
                "ON CONFLICT (name) DO UPDATE SET name = 'research' RETURNING id"
            )
            col_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO collection_papers (collection_id, arxiv_id) VALUES (%s, %s) "
                "ON CONFLICT DO NOTHING",
                (col_id, paper_id),
            )

            # 6. check_watch
            cur.execute("SELECT arxiv_id, title FROM papers ORDER BY arxiv_id DESC LIMIT 20")
            cur.fetchall()

        latencies.append((time.perf_counter() - t0) * 1000)

    cur.close()
    conn.close()

    return {
        "p50_ms": round(statistics.median(latencies), 3),
        "p95_ms": round(max(latencies), 3),
        "mean_ms": round(statistics.mean(latencies), 3),
        "runs": len(latencies),
    }


def main():
    print("=" * 80)
    print("Dimensions 4-6: Writes, Operations, Workflow")
    print("=" * 80)

    papers = load_source_papers()
    print(f"Loaded {len(papers)} source papers")

    all_results = {}

    # --- D4: Write Performance ---
    print(f"\n{'=' * 80}")
    print("DIMENSION 4: Write Performance")
    print(f"{'=' * 80}")

    d4_bulk = {"sqlite": [], "postgresql": []}
    for scale in SCALE_POINTS:
        print(f"\n  Scale: {scale:,}")
        sqlite_result = d4_sqlite_bulk_import(papers, scale)
        pg_result = d4_pg_bulk_import(papers, scale)

        d4_bulk["sqlite"].append({"scale": scale, **sqlite_result})
        d4_bulk["postgresql"].append({"scale": scale, **pg_result})

        print(f"    SQLite:  insert={sqlite_result['insert_time_s']:.2f}s  "
              f"FTS={sqlite_result['fts_build_time_s']:.2f}s  "
              f"size={sqlite_result['db_size_bytes']/1024/1024:.1f}MB")
        print(f"    PG:      insert={pg_result['insert_time_s']:.2f}s  "
              f"tsv={pg_result['tsvector_build_time_s']:.2f}s  "
              f"size={pg_result['db_size_bytes']/1024/1024:.1f}MB")

    # Concurrent read+write (PG)
    print("\n  Concurrent read+write (PostgreSQL)...")
    d4_concurrent = d4_concurrent_readwrite_pg()
    for wr in d4_concurrent["write_rates"]:
        print(f"    {wr['target_writes_per_sec']:3d} w/s: search p50={wr['search_p50_ms']:.2f}ms  "
              f"errors={wr['write_errors']}")

    all_results["D4"] = {"bulk_import": d4_bulk, "concurrent_pg": d4_concurrent}

    # --- D5: Operational Characteristics ---
    print(f"\n{'=' * 80}")
    print("DIMENSION 5: Operational Characteristics")
    print(f"{'=' * 80}")

    print("\n  Connection setup time...")
    d5_conn = d5_connection_setup()
    print(f"    SQLite:  p50={d5_conn['sqlite']['p50_ms']:.3f}ms")
    print(f"    PG:      p50={d5_conn['postgresql']['p50_ms']:.3f}ms")

    print("\n  Backup/restore (19K)...")
    d5_backup = d5_backup_restore()
    print(f"    SQLite:  backup={d5_backup['sqlite_19k']['backup_time_s']:.3f}s  "
          f"restore={d5_backup['sqlite_19k']['restore_time_s']:.3f}s")
    print(f"    PG:      backup={d5_backup['postgresql_19k']['backup_time_s']:.3f}s")

    print("\n  Disk footprint at scale...")
    d5_disk = d5_disk_footprint(papers)
    for entry in d5_disk:
        print(f"    {entry['scale']:>10,d}:  SQLite={entry['sqlite_bytes']/1024/1024:.1f}MB  "
              f"PG={entry['pg_bytes']/1024/1024:.1f}MB  ratio={entry['ratio']:.1f}x")

    all_results["D5"] = {
        "connection_setup": d5_conn,
        "backup_restore": d5_backup,
        "disk_footprint": d5_disk,
    }

    # --- D6: Workflow Comparison ---
    print(f"\n{'=' * 80}")
    print("DIMENSION 6: Workflow-Level Comparison (6-tool MCP workflow, 19K papers)")
    print(f"{'=' * 80}")

    print("\n  SQLite workflow...")
    d6_sqlite = d6_workflow_sqlite(papers)
    print(f"    p50={d6_sqlite['p50_ms']:.2f}ms  p95={d6_sqlite['p95_ms']:.2f}ms")

    print("\n  PostgreSQL workflow...")
    d6_pg = d6_workflow_pg(papers)
    print(f"    p50={d6_pg['p50_ms']:.2f}ms  p95={d6_pg['p95_ms']:.2f}ms")

    ratio = d6_pg["p50_ms"] / d6_sqlite["p50_ms"] if d6_sqlite["p50_ms"] > 0 else 0
    print(f"\n  Ratio (PG/SQLite): {ratio:.1f}x")

    all_results["D6"] = {"sqlite": d6_sqlite, "postgresql": d6_pg, "ratio": round(ratio, 2)}

    # Save all results
    all_results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"All results saved to {RESULTS_PATH.name}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
