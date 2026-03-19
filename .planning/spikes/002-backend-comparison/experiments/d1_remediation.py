"""
D1 Remediation: Fix query-parsing confound, stemming analysis, result inspection.

D1-R1: Test plainto_tsquery alongside websearch_to_tsquery. Escape hyphens for FTS5.
D1-R2: Compare Porter vs Snowball stems for all query terms.
D1-R3: For top-5 divergent queries, display papers unique to each backend.

Prerequisites:
- setup_spike002.py has been run (PostgreSQL loaded)
- spike_001_harvest.db available

Usage:
    python d1_remediation.py
"""

import json
import sqlite3
import time
from pathlib import Path

import psycopg2
from nltk.stem import PorterStemmer, SnowballStemmer

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DATA = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data"
)
SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
RESULTS_PATH = DATA_DIR / "d1_remediation_results.json"
INSPECTION_PATH = DATA_DIR / "d1_divergent_inspection.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"
TOP_K = 20

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


# ======================================================================
# D1-R1: Query-parsing confound
# ======================================================================

def setup_fts5() -> Path:
    """Create FTS5-indexed SQLite DB."""
    fts_db = DATA_DIR / "d1r_fts5_temp.db"
    conn = sqlite3.connect(str(fts_db))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute(f"ATTACH DATABASE '{SOURCE_DB}' AS src")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            arxiv_id TEXT PRIMARY KEY, title TEXT, authors_text TEXT,
            abstract TEXT, categories TEXT, primary_category TEXT
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO papers
        SELECT arxiv_id, title, authors_text, abstract, categories, primary_category
        FROM src.papers WHERE abstract IS NOT NULL AND abstract != ''
    """)
    conn.commit()
    conn.execute("DETACH DATABASE src")
    conn.execute("DROP TABLE IF EXISTS papers_fts")
    conn.execute("""
        CREATE VIRTUAL TABLE papers_fts USING fts5(
            title, abstract, authors_text,
            content='papers', content_rowid='rowid',
            tokenize='porter unicode61'
        )
    """)
    conn.execute("INSERT INTO papers_fts(papers_fts) VALUES('rebuild')")
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
    print(f"  FTS5 DB: {count} papers")
    conn.close()
    return fts_db


def escape_fts5_query(query: str) -> str:
    """Escape hyphens and other FTS5 special characters for safe matching."""
    # Replace hyphens with spaces (FTS5 interprets - as column separator)
    escaped = query.replace("-", " ")
    return escaped


def search_fts5(db_path: Path, query: str) -> list[str]:
    """FTS5 search, return arxiv_ids."""
    conn = sqlite3.connect(str(db_path))
    try:
        results = conn.execute(
            """SELECT p.arxiv_id FROM papers_fts f
               JOIN papers p ON f.rowid = p.rowid
               WHERE papers_fts MATCH ? ORDER BY f.rank LIMIT ?""",
            (query, TOP_K),
        ).fetchall()
        return [r[0] for r in results]
    except Exception as e:
        return []
    finally:
        conn.close()


def search_fts5_and(db_path: Path, query: str) -> list[str]:
    """FTS5 search with explicit AND between terms."""
    terms = query.replace('"', '').replace('-', ' ').split()
    # Filter out boolean operators
    terms = [t for t in terms if t.upper() not in ('AND', 'OR')]
    if not terms:
        return []
    fts_query = " AND ".join(terms)
    return search_fts5(db_path, fts_query)


def search_pg(query: str, tsquery_fn: str = "websearch_to_tsquery") -> list[str]:
    """PostgreSQL tsvector search with specified tsquery function."""
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    try:
        cur.execute(
            f"""SELECT arxiv_id,
                       ts_rank_cd(search_vector, {tsquery_fn}('english', %s)) AS rank
                FROM papers
                WHERE search_vector @@ {tsquery_fn}('english', %s)
                ORDER BY rank DESC LIMIT %s""",
            (query, query, TOP_K),
        )
        return [r[0] for r in cur.fetchall()]
    except Exception as e:
        conn.rollback()
        return []
    finally:
        cur.close()
        conn.close()


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def run_d1_r1(fts_db: Path) -> dict:
    """D1-R1: Compare query parser variants."""
    print("\n--- D1-R1: Query-parsing confound ---")
    results = []

    for qname, qtext in QUERIES:
        # Original FTS5 (may fail on hyphens)
        fts5_original = search_fts5(fts_db, qtext)

        # FTS5 with escaped hyphens
        fts5_escaped = search_fts5(fts_db, escape_fts5_query(qtext))

        # FTS5 with explicit AND
        fts5_and = search_fts5_and(fts_db, qtext)

        # PostgreSQL with websearch_to_tsquery (original)
        pg_websearch = search_pg(qtext, "websearch_to_tsquery")

        # PostgreSQL with plainto_tsquery
        pg_plain = search_pg(qtext, "plainto_tsquery")

        # Compute Jaccards for each pairing
        j_original = jaccard(set(fts5_original), set(pg_websearch))
        j_escaped_vs_websearch = jaccard(set(fts5_escaped), set(pg_websearch))
        j_escaped_vs_plain = jaccard(set(fts5_escaped), set(pg_plain))
        j_and_vs_plain = jaccard(set(fts5_and), set(pg_plain))
        j_websearch_vs_plain = jaccard(set(pg_websearch), set(pg_plain))

        entry = {
            "query_name": qname,
            "query_text": qtext,
            "counts": {
                "fts5_original": len(fts5_original),
                "fts5_escaped": len(fts5_escaped),
                "fts5_and": len(fts5_and),
                "pg_websearch": len(pg_websearch),
                "pg_plain": len(pg_plain),
            },
            "jaccards": {
                "fts5_orig_vs_pg_websearch": round(j_original, 4),
                "fts5_escaped_vs_pg_websearch": round(j_escaped_vs_websearch, 4),
                "fts5_escaped_vs_pg_plain": round(j_escaped_vs_plain, 4),
                "fts5_and_vs_pg_plain": round(j_and_vs_plain, 4),
                "pg_websearch_vs_pg_plain": round(j_websearch_vs_plain, 4),
            },
        }
        results.append(entry)

        # Summary line
        print(
            f"  {qname:25s}  "
            f"orig={j_original:.3f}  "
            f"esc/ws={j_escaped_vs_websearch:.3f}  "
            f"esc/pl={j_escaped_vs_plain:.3f}  "
            f"AND/pl={j_and_vs_plain:.3f}  "
            f"ws/pl={j_websearch_vs_plain:.3f}"
        )

    # Compute averages
    avg_original = sum(r["jaccards"]["fts5_orig_vs_pg_websearch"] for r in results) / len(results)
    avg_escaped_ws = sum(r["jaccards"]["fts5_escaped_vs_pg_websearch"] for r in results) / len(results)
    avg_escaped_pl = sum(r["jaccards"]["fts5_escaped_vs_pg_plain"] for r in results) / len(results)
    avg_and_pl = sum(r["jaccards"]["fts5_and_vs_pg_plain"] for r in results) / len(results)
    avg_ws_pl = sum(r["jaccards"]["pg_websearch_vs_pg_plain"] for r in results) / len(results)

    summary = {
        "avg_fts5_orig_vs_pg_websearch": round(avg_original, 4),
        "avg_fts5_escaped_vs_pg_websearch": round(avg_escaped_ws, 4),
        "avg_fts5_escaped_vs_pg_plain": round(avg_escaped_pl, 4),
        "avg_fts5_and_vs_pg_plain": round(avg_and_pl, 4),
        "avg_pg_websearch_vs_pg_plain": round(avg_ws_pl, 4),
    }

    print(f"\n  Averages:")
    print(f"    Original (Round 1):     {avg_original:.4f}")
    print(f"    Escaped vs websearch:   {avg_escaped_ws:.4f}")
    print(f"    Escaped vs plainto:     {avg_escaped_pl:.4f}")
    print(f"    AND vs plainto:         {avg_and_pl:.4f}")
    print(f"    websearch vs plainto:   {avg_ws_pl:.4f}")

    parser_contribution = avg_escaped_pl - avg_original
    print(f"\n  Parser-driven improvement: {parser_contribution:+.4f} Jaccard")
    print(f"  (Escaped+plainto vs original = how much was parser, not search engine)")

    return {"per_query": results, "summary": summary}


# ======================================================================
# D1-R2: Stemming analysis
# ======================================================================

def run_d1_r2() -> dict:
    """D1-R2: Compare Porter vs Snowball stems."""
    print("\n--- D1-R2: Stemming analysis ---")

    porter = PorterStemmer()
    snowball = SnowballStemmer("english")

    # Also get PostgreSQL's actual stems
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()

    # Collect all unique terms from queries
    all_terms = set()
    for _, qtext in QUERIES:
        terms = qtext.replace('"', '').replace('-', ' ').split()
        terms = [t for t in terms if t.upper() not in ('AND', 'OR')]
        all_terms.update(t.lower() for t in terms)

    results = []
    divergent_terms = []

    for term in sorted(all_terms):
        p_stem = porter.stem(term)
        s_stem = snowball.stem(term)

        # Get PostgreSQL's actual token
        cur.execute("SELECT * FROM ts_debug('english', %s)", (term,))
        debug_rows = cur.fetchall()
        # ts_debug returns: alias, description, token, dictionaries, dictionary, lexemes
        pg_lexemes = []
        for row in debug_rows:
            if row[5]:  # lexemes column
                pg_lexemes.extend(row[5])
        pg_stem = pg_lexemes[0] if pg_lexemes else "(stopped)"

        match = p_stem == s_stem == pg_stem
        entry = {
            "term": term,
            "porter": p_stem,
            "snowball": s_stem,
            "postgresql": pg_stem,
            "all_match": match,
        }
        results.append(entry)

        if not match:
            divergent_terms.append(entry)

    cur.close()
    conn.close()

    print(f"  Total terms analyzed: {len(results)}")
    print(f"  Divergent stems: {len(divergent_terms)}")
    print(f"\n  {'Term':<25s} {'Porter':<15s} {'Snowball':<15s} {'PostgreSQL':<15s}")
    print(f"  {'-' * 70}")
    for t in results:
        marker = " ***" if not t["all_match"] else ""
        print(f"  {t['term']:<25s} {t['porter']:<15s} {t['snowball']:<15s} {t['postgresql']:<15s}{marker}")

    return {"terms": results, "divergent_count": len(divergent_terms), "divergent_terms": divergent_terms}


# ======================================================================
# D1-R3: Divergent result inspection
# ======================================================================

def run_d1_r3(fts_db: Path) -> dict:
    """D1-R3: Inspect papers unique to each backend for top-5 divergent queries."""
    print("\n--- D1-R3: Divergent result inspection ---")

    # Load Round 1 results to find highest-divergence queries
    r1_path = DATA_DIR / "d1_search_quality_results.json"
    with open(r1_path) as f:
        r1_data = json.load(f)

    # Sort by Jaccard (ascending = most divergent)
    sorted_queries = sorted(r1_data["per_query"], key=lambda x: x["jaccard"])

    # Take top 5 most divergent (excluding zero-result queries)
    top_divergent = [
        q for q in sorted_queries
        if q["fts5_count"] > 0 or q["tsvector_count"] > 0
    ][:5]

    # Load paper details from SQLite
    conn_sqlite = sqlite3.connect(str(SOURCE_DB))
    conn_pg = psycopg2.connect(PG_DSN)
    cur_pg = conn_pg.cursor()

    inspections = []

    for q in top_divergent:
        qname = q["query_name"]
        qtext = q["query_text"]
        print(f"\n  Query: {qname} ({qtext}) — Jaccard={q['jaccard']:.3f}")

        # Get results from both backends
        fts5_ids = search_fts5(fts_db, escape_fts5_query(qtext))
        pg_ids = search_pg(qtext, "websearch_to_tsquery")

        fts5_only = set(fts5_ids) - set(pg_ids)
        pg_only = set(pg_ids) - set(fts5_ids)
        shared = set(fts5_ids) & set(pg_ids)

        # Fetch paper details for unique results
        def get_paper_info(arxiv_id):
            row = conn_sqlite.execute(
                "SELECT arxiv_id, title, abstract, primary_category FROM papers WHERE arxiv_id = ?",
                (arxiv_id,),
            ).fetchone()
            if row:
                return {
                    "arxiv_id": row[0],
                    "title": row[1],
                    "abstract": row[2][:200] + "..." if row[2] and len(row[2]) > 200 else row[2],
                    "category": row[3],
                }
            return {"arxiv_id": arxiv_id, "title": "(not found)", "abstract": "", "category": ""}

        fts5_only_papers = [get_paper_info(aid) for aid in sorted(fts5_only)[:5]]
        pg_only_papers = [get_paper_info(aid) for aid in sorted(pg_only)[:5]]

        inspection = {
            "query_name": qname,
            "query_text": qtext,
            "jaccard": q["jaccard"],
            "shared_count": len(shared),
            "fts5_only_count": len(fts5_only),
            "pg_only_count": len(pg_only),
            "fts5_only_sample": fts5_only_papers,
            "pg_only_sample": pg_only_papers,
        }
        inspections.append(inspection)

        print(f"    Shared: {len(shared)}, FTS5-only: {len(fts5_only)}, PG-only: {len(pg_only)}")
        if fts5_only_papers:
            print(f"    FTS5-only sample:")
            for p in fts5_only_papers[:3]:
                print(f"      [{p['category']}] {p['title'][:80]}")
        if pg_only_papers:
            print(f"    PG-only sample:")
            for p in pg_only_papers[:3]:
                print(f"      [{p['category']}] {p['title'][:80]}")

    conn_sqlite.close()
    cur_pg.close()
    conn_pg.close()

    return {"inspections": inspections}


# ======================================================================
# Main
# ======================================================================

def main():
    print("=" * 80)
    print("D1 Remediation: Query parsing, stemming, result inspection")
    print("=" * 80)

    # Ensure PostgreSQL has data (setup_spike002.py should have been run)
    conn = psycopg2.connect(PG_DSN)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM papers WHERE search_vector IS NOT NULL")
    pg_count = cur.fetchone()[0]
    cur.close()
    conn.close()

    if pg_count == 0:
        print("ERROR: PostgreSQL has no papers. Run setup_spike002.py first.")
        return

    print(f"PostgreSQL: {pg_count} papers with tsvector")

    # Setup FTS5
    print("\nSetting up FTS5...")
    fts_db = setup_fts5()

    # D1-R1
    r1_results = run_d1_r1(fts_db)

    # D1-R2
    r2_results = run_d1_r2()

    # D1-R3
    r3_results = run_d1_r3(fts_db)

    # Save all results
    output = {
        "d1_r1_query_parsing": r1_results,
        "d1_r2_stemming": r2_results,
        "d1_r3_inspection": r3_results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH.name}")

    # Save inspection separately for easy reading
    with open(INSPECTION_PATH, "w") as f:
        json.dump(r3_results, f, indent=2)
    print(f"Inspection saved to {INSPECTION_PATH.name}")

    # Cleanup
    fts_db.unlink(missing_ok=True)
    print("Temp FTS5 DB cleaned up.")


if __name__ == "__main__":
    main()
