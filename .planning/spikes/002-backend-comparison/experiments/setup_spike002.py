"""
Spike 002 Setup: Load papers into PostgreSQL and pre-compute embeddings.

Steps:
1. Load 19K papers from spike_001_harvest.db into PostgreSQL (arxiv_mcp_spike002)
2. Create tsvector GIN index
3. Compute all-MiniLM-L6-v2 embeddings on GPU
4. Save embeddings as .npy file
5. Load embeddings into pgvector table with HNSW index

Usage:
    python setup_spike002.py
"""

import json
import os
import sqlite3
import time
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2.extras import execute_values

# --- Configuration ---

DATA_DIR = Path(__file__).parent / "data"
SPIKE001_DB = (
    Path(__file__).parent.parent.parent
    / "001-volume-filtering-scoring-landscape/experiments/data/spike_001_harvest.db"
)
EMBEDDINGS_PATH = DATA_DIR / "embeddings_19k.npy"
ARXIV_IDS_PATH = DATA_DIR / "arxiv_ids_19k.json"
SETUP_RESULTS_PATH = DATA_DIR / "setup_results.json"

PG_DSN = "postgresql://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_spike002"

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384
EMBED_BATCH_SIZE = 256


def load_source_papers() -> list[dict]:
    """Load all papers from the Spike 001 harvest database."""
    conn = sqlite3.connect(str(SPIKE001_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date, updated_date "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def setup_postgresql(papers: list[dict]) -> dict:
    """Create tables and load papers into PostgreSQL."""
    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()

    # Drop existing tables for clean setup
    cur.execute("DROP TABLE IF EXISTS paper_embeddings CASCADE")
    cur.execute("DROP TABLE IF EXISTS papers CASCADE")

    # Create papers table with tsvector column
    cur.execute("""
        CREATE TABLE papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors_text TEXT,
            abstract TEXT,
            categories TEXT,
            primary_category TEXT,
            submitted_date TEXT,
            updated_date TEXT,
            search_vector tsvector
        )
    """)

    # Insert papers
    conn.autocommit = False
    t0 = time.perf_counter()

    values = [
        (
            p["arxiv_id"], p["title"], p["authors_text"], p["abstract"],
            p["categories"], p["primary_category"],
            p.get("submitted_date"), p.get("updated_date"),
        )
        for p in papers
    ]

    execute_values(
        cur,
        """INSERT INTO papers
           (arxiv_id, title, authors_text, abstract, categories,
            primary_category, submitted_date, updated_date)
           VALUES %s
           ON CONFLICT (arxiv_id) DO NOTHING""",
        values,
        page_size=1000,
    )
    conn.commit()
    insert_time = time.perf_counter() - t0

    # Populate tsvector column
    t0 = time.perf_counter()
    cur.execute("""
        UPDATE papers SET search_vector =
            setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
            setweight(to_tsvector('english', coalesce(abstract, '')), 'B') ||
            setweight(to_tsvector('english', coalesce(authors_text, '')), 'C')
    """)
    conn.commit()
    tsvector_time = time.perf_counter() - t0

    # Create GIN index on tsvector
    t0 = time.perf_counter()
    cur.execute("CREATE INDEX idx_papers_search ON papers USING GIN (search_vector)")
    conn.commit()
    gin_index_time = time.perf_counter() - t0

    # Verify
    cur.execute("SELECT COUNT(*) FROM papers")
    count = cur.fetchone()[0]

    # Get table size
    cur.execute("""
        SELECT pg_total_relation_size('papers') AS total,
               pg_relation_size('papers') AS table_only,
               pg_indexes_size('papers') AS indexes
    """)
    sizes = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "paper_count": count,
        "insert_time_s": round(insert_time, 3),
        "tsvector_time_s": round(tsvector_time, 3),
        "gin_index_time_s": round(gin_index_time, 3),
        "total_size_bytes": sizes[0],
        "table_size_bytes": sizes[1],
        "index_size_bytes": sizes[2],
    }


def compute_embeddings(papers: list[dict]) -> tuple[np.ndarray, list[str], dict]:
    """Compute embeddings on GPU and save to disk."""
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"  Device: {device}")
    if device == "cuda":
        print(f"  GPU: {torch.cuda.get_device_name(0)}")

    # Load model
    t0 = time.perf_counter()
    model = SentenceTransformer(MODEL_NAME, device=device)
    model_load_time = time.perf_counter() - t0
    print(f"  Model loaded in {model_load_time:.1f}s")

    # Prepare texts (title + abstract for richer embeddings)
    texts = [f"{p['title']}. {p['abstract']}" for p in papers]
    arxiv_ids = [p["arxiv_id"] for p in papers]

    # Compute embeddings
    t0 = time.perf_counter()
    embeddings = model.encode(
        texts,
        batch_size=EMBED_BATCH_SIZE,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )
    embed_time = time.perf_counter() - t0

    # Ensure float32
    if embeddings.dtype != np.float32:
        embeddings = embeddings.astype(np.float32)

    print(f"  Computed {embeddings.shape[0]} embeddings in {embed_time:.1f}s")
    print(f"  Shape: {embeddings.shape}, dtype: {embeddings.dtype}")
    print(f"  Size: {embeddings.nbytes / 1024 / 1024:.1f} MB")

    # Save to disk
    np.save(EMBEDDINGS_PATH, embeddings)
    with open(ARXIV_IDS_PATH, "w") as f:
        json.dump(arxiv_ids, f)

    del model
    if device == "cuda":
        torch.cuda.empty_cache()

    return embeddings, arxiv_ids, {
        "model": MODEL_NAME,
        "device": device,
        "model_load_time_s": round(model_load_time, 2),
        "embed_time_s": round(embed_time, 2),
        "per_paper_ms": round(embed_time / len(papers) * 1000, 3),
        "shape": list(embeddings.shape),
        "dtype": str(embeddings.dtype),
        "file_size_bytes": embeddings.nbytes,
    }


def load_pgvector(embeddings: np.ndarray, arxiv_ids: list[str]) -> dict:
    """Load embeddings into pgvector table with HNSW index."""
    conn = psycopg2.connect(PG_DSN)
    conn.autocommit = True
    cur = conn.cursor()

    # Create embeddings table
    cur.execute(f"""
        CREATE TABLE paper_embeddings (
            arxiv_id TEXT PRIMARY KEY REFERENCES papers(arxiv_id),
            embedding vector({EMBEDDING_DIM})
        )
    """)

    # Insert embeddings in batches
    conn.autocommit = False
    t0 = time.perf_counter()

    batch_size = 500
    for i in range(0, len(arxiv_ids), batch_size):
        batch_ids = arxiv_ids[i:i + batch_size]
        batch_emb = embeddings[i:i + batch_size]
        values = [
            (aid, emb.tolist())
            for aid, emb in zip(batch_ids, batch_emb)
        ]
        execute_values(
            cur,
            "INSERT INTO paper_embeddings (arxiv_id, embedding) VALUES %s",
            values,
            template="(%s, %s::vector)",
            page_size=500,
        )
        if (i + batch_size) % 5000 < batch_size:
            print(f"    Inserted {min(i + batch_size, len(arxiv_ids))}/{len(arxiv_ids)}")

    conn.commit()
    insert_time = time.perf_counter() - t0

    # Create HNSW index
    conn.autocommit = True
    print("  Building HNSW index (this may take a moment)...")
    t0 = time.perf_counter()
    cur.execute("""
        CREATE INDEX idx_paper_embeddings_hnsw
        ON paper_embeddings
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
    """)
    hnsw_time = time.perf_counter() - t0

    # Verify
    cur.execute("SELECT COUNT(*) FROM paper_embeddings")
    count = cur.fetchone()[0]

    # Get sizes
    cur.execute("""
        SELECT pg_total_relation_size('paper_embeddings') AS total,
               pg_relation_size('paper_embeddings') AS table_only,
               pg_indexes_size('paper_embeddings') AS indexes
    """)
    sizes = cur.fetchone()

    # Get HNSW index params for documentation
    cur.execute("""
        SELECT pg_size_pretty(pg_relation_size('idx_paper_embeddings_hnsw'))
    """)
    hnsw_size = cur.fetchone()[0]

    cur.close()
    conn.close()

    return {
        "embedding_count": count,
        "insert_time_s": round(insert_time, 3),
        "hnsw_build_time_s": round(hnsw_time, 3),
        "hnsw_params": {"m": 16, "ef_construction": 64},
        "hnsw_index_size": hnsw_size,
        "total_size_bytes": sizes[0],
        "table_size_bytes": sizes[1],
        "index_size_bytes": sizes[2],
    }


def main():
    print("=" * 70)
    print("Spike 002 Setup")
    print("=" * 70)

    # Load source papers
    print(f"\n1. Loading papers from {SPIKE001_DB.name}...")
    papers = load_source_papers()
    print(f"   Loaded {len(papers)} papers")

    # Setup PostgreSQL
    print("\n2. Setting up PostgreSQL (papers + tsvector + GIN index)...")
    pg_results = setup_postgresql(papers)
    print(f"   {pg_results['paper_count']} papers inserted in {pg_results['insert_time_s']}s")
    print(f"   tsvector computed in {pg_results['tsvector_time_s']}s")
    print(f"   GIN index built in {pg_results['gin_index_time_s']}s")
    print(f"   Total size: {pg_results['total_size_bytes'] / 1024 / 1024:.1f} MB")

    # Compute embeddings
    print(f"\n3. Computing embeddings ({MODEL_NAME})...")
    embeddings, arxiv_ids, embed_results = compute_embeddings(papers)

    # Load into pgvector
    print("\n4. Loading embeddings into pgvector...")
    pgvec_results = load_pgvector(embeddings, arxiv_ids)
    print(f"   {pgvec_results['embedding_count']} embeddings loaded in {pgvec_results['insert_time_s']}s")
    print(f"   HNSW index built in {pgvec_results['hnsw_build_time_s']}s")
    print(f"   HNSW index size: {pgvec_results['hnsw_index_size']}")

    # Save all setup results
    results = {
        "postgresql": pg_results,
        "embeddings": embed_results,
        "pgvector": pgvec_results,
        "source_db": str(SPIKE001_DB),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(SETUP_RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 70}")
    print("Setup complete. Results saved to {SETUP_RESULTS_PATH.name}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
