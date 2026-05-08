"""
Dimension 1: Search Result Quality — FTS5 vs tsvector

Measures whether SQLite FTS5 and PostgreSQL tsvector return the same papers
for the same queries. Speed is irrelevant here; this is about retrieval quality.

Metrics:
- Jaccard similarity of top-20 result sets
- Rank-biased overlap (RBO) — weighted rank correlation
- Unique results per backend — sampled and inspected

Prerequisites:
- setup_spike002.py has been run (PostgreSQL loaded, tsvector indexed)
- spike_001_harvest.db available (SQLite FTS5 source)

Usage:
    python d1_search_quality.py
"""

import json
import math
import sqlite3
import time
from pathlib import Path

import psycopg2

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
RESULTS_PATH = DATA_DIR / "d1_search_quality_results.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"

TOP_K = 20

# Full query set from DESIGN.md
QUERIES = [
    # From Spike 001 A1b
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
    # Extended for Spike 002
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


# --- SQLite FTS5 search ---

def setup_sqlite_fts(source_db: Path) -> Path:
    """Create a temporary FTS5-indexed SQLite DB from the harvest DB."""
    fts_db = DATA_DIR / "d1_fts5_temp.db"

    # Copy and build FTS
    conn = sqlite3.connect(str(fts_db))
    conn.execute("PRAGMA journal_mode=WAL")

    # Attach source
    conn.execute(f"ATTACH DATABASE '{source_db}' AS src")

    # Create local papers table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            authors_text TEXT,
            abstract TEXT,
            categories TEXT,
            primary_category TEXT
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO papers
        SELECT arxiv_id, title, authors_text, abstract, categories, primary_category
        FROM src.papers
        WHERE abstract IS NOT NULL AND abstract != ''
    """)
    conn.commit()
    conn.execute("DETACH DATABASE src")

    # Build FTS5 index (porter tokenizer — same as Spike 001)
    conn.execute("DROP TABLE IF EXISTS papers_fts")
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers',
            content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"  SQLite FTS5 DB: {count} papers, {fts_db.stat().st_size / 1024 / 1024:.1f} MB")
    conn.close()
    return fts_db


def search_fts5(db_path: Path, query: str, top_k: int = TOP_K) -> list[tuple[str, float]]:
    """Search FTS5 and return [(arxiv_id, rank_score), ...]."""
    conn = sqlite3.connect(str(db_path))
    try:
        results = conn.execute(
            """SELECT p.arxiv_id, f.rank
               FROM papers_fts f
               JOIN papers p ON f.rowid = p.rowid
               WHERE papers_fts MATCH ?
               ORDER BY f.rank
               LIMIT ?""",
            (query, top_k),
        ).fetchall()
        return [(r[0], float(r[1])) for r in results]
    except Exception as e:
        print(f"    FTS5 error for '{query}': {e}")
        return []
    finally:
        conn.close()


# --- PostgreSQL tsvector search ---

def search_tsvector(query: str, top_k: int = TOP_K) -> list[tuple[str, float]]:
    """Search tsvector and return [(arxiv_id, rank_score), ...]."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    # Convert query to tsquery — use websearch_to_tsquery for natural syntax
    # This handles AND/OR/phrases similarly to how a user would type them
    try:
        cur.execute(
            """SELECT arxiv_id,
                      ts_rank_cd(search_vector, websearch_to_tsquery('english', %s)) AS rank
               FROM papers
               WHERE search_vector @@ websearch_to_tsquery('english', %s)
               ORDER BY rank DESC
               LIMIT %s""",
            (query, query, top_k),
        )
        results = [(r[0], float(r[1])) for r in cur.fetchall()]
    except Exception as e:
        print(f"    tsvector error for '{query}': {e}")
        conn.rollback()
        results = []
    finally:
        cur.close()
        conn.close()

    return results


# --- Metrics ---

def jaccard_similarity(set_a: set, set_b: set) -> float:
    """Jaccard similarity between two sets."""
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def rank_biased_overlap(list_a: list[str], list_b: list[str], p: float = 0.9) -> float:
    """Rank-biased overlap (Webber et al. 2010).

    p controls top-heaviness: p=0.9 means top positions matter ~10x more
    than positions near k=20.
    """
    if not list_a or not list_b:
        return 0.0

    k = min(len(list_a), len(list_b))
    rbo_sum = 0.0

    for d in range(1, k + 1):
        set_a = set(list_a[:d])
        set_b = set(list_b[:d])
        overlap = len(set_a & set_b) / d
        rbo_sum += (p ** (d - 1)) * overlap

    # Extrapolated RBO
    return (1 - p) * rbo_sum


def analyze_query(
    query_name: str,
    query_text: str,
    fts5_results: list[tuple[str, float]],
    tsvector_results: list[tuple[str, float]],
) -> dict:
    """Analyze a single query's results across both backends."""
    fts5_ids = [r[0] for r in fts5_results]
    tsv_ids = [r[0] for r in tsvector_results]

    fts5_set = set(fts5_ids)
    tsv_set = set(tsv_ids)

    jaccard = jaccard_similarity(fts5_set, tsv_set)
    rbo = rank_biased_overlap(fts5_ids, tsv_ids)

    # Unique to each backend
    fts5_only = fts5_set - tsv_set
    tsv_only = tsv_set - fts5_set
    shared = fts5_set & tsv_set

    return {
        "query_name": query_name,
        "query_text": query_text,
        "fts5_count": len(fts5_results),
        "tsvector_count": len(tsvector_results),
        "jaccard": round(jaccard, 4),
        "rbo_p09": round(rbo, 4),
        "shared_count": len(shared),
        "fts5_only_count": len(fts5_only),
        "tsvector_only_count": len(tsv_only),
        "fts5_only_ids": sorted(fts5_only)[:5],  # Sample for inspection
        "tsvector_only_ids": sorted(tsv_only)[:5],
        "fts5_top5": fts5_ids[:5],
        "tsvector_top5": tsv_ids[:5],
    }


def main():
    print("=" * 70)
    print("Dimension 1: Search Result Quality (FTS5 vs tsvector)")
    print("=" * 70)

    source_db = SPIKE001_DATA / "spike_001_harvest.db"
    if not source_db.exists():
        print(f"ERROR: Source DB not found: {source_db}")
        return

    # Setup FTS5
    print("\nSetting up SQLite FTS5 index...")
    fts_db = setup_sqlite_fts(source_db)

    # Verify PostgreSQL is ready
    print("\nVerifying PostgreSQL...")
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM papers WHERE search_vector IS NOT NULL")
    pg_count = cur.fetchone()[0]
    print(f"  PostgreSQL: {pg_count} papers with tsvector")
    cur.close()
    conn.close()

    # Run queries
    print(f"\nRunning {len(QUERIES)} queries on both backends (top-{TOP_K})...")
    print("-" * 70)

    all_results = []

    for query_name, query_text in QUERIES:
        fts5_results = search_fts5(fts_db, query_text)
        tsv_results = search_tsvector(query_text)

        analysis = analyze_query(query_name, query_text, fts5_results, tsv_results)
        all_results.append(analysis)

        # Print summary line
        j = analysis["jaccard"]
        rbo = analysis["rbo_p09"]
        f_count = analysis["fts5_count"]
        t_count = analysis["tsvector_count"]
        shared = analysis["shared_count"]

        # Color-code by agreement level
        if j >= 0.7:
            tag = "HIGH"
        elif j >= 0.4:
            tag = "MED "
        else:
            tag = "LOW "

        print(
            f"  [{tag}] {query_name:25s}  "
            f"J={j:.3f}  RBO={rbo:.3f}  "
            f"shared={shared:2d}/{TOP_K}  "
            f"fts5={f_count:2d} tsv={t_count:2d}"
        )

    # Summary statistics
    jaccards = [r["jaccard"] for r in all_results]
    rbos = [r["rbo_p09"] for r in all_results]

    avg_jaccard = sum(jaccards) / len(jaccards)
    avg_rbo = sum(rbos) / len(rbos)
    min_jaccard = min(jaccards)
    max_jaccard = max(jaccards)

    # Hypothesis test: H1 says avg Jaccard >= 0.5
    h1_supported = avg_jaccard >= 0.5

    summary = {
        "avg_jaccard": round(avg_jaccard, 4),
        "avg_rbo": round(avg_rbo, 4),
        "min_jaccard": round(min_jaccard, 4),
        "max_jaccard": round(max_jaccard, 4),
        "h1_result": "SUPPORTED" if h1_supported else "FALSIFIED",
        "h1_description": (
            f"Average Jaccard {avg_jaccard:.3f} "
            f"{'≥' if h1_supported else '<'} 0.5 threshold"
        ),
        "high_agreement_queries": [
            r["query_name"] for r in all_results if r["jaccard"] >= 0.7
        ],
        "low_agreement_queries": [
            r["query_name"] for r in all_results if r["jaccard"] < 0.4
        ],
    }

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Average Jaccard:   {avg_jaccard:.4f}")
    print(f"  Average RBO(0.9):  {avg_rbo:.4f}")
    print(f"  Range:             [{min_jaccard:.4f}, {max_jaccard:.4f}]")
    print(f"  H1 (Jaccard≥0.5):  {summary['h1_result']}")
    print(f"  High agreement:    {len(summary['high_agreement_queries'])} queries")
    print(f"  Low agreement:     {len(summary['low_agreement_queries'])} queries")

    if summary["low_agreement_queries"]:
        print(f"  Low-agreement queries: {', '.join(summary['low_agreement_queries'])}")

    # Save results
    output = {
        "dimension": "D1",
        "description": "Search Result Quality — FTS5 vs tsvector",
        "corpus_size": pg_count,
        "top_k": TOP_K,
        "query_count": len(QUERIES),
        "summary": summary,
        "per_query": all_results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH.name}")

    # Cleanup temp FTS5 DB
    fts_db.unlink(missing_ok=True)
    print("Temp FTS5 DB cleaned up.")


if __name__ == "__main__":
    main()
