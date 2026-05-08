"""
Per-category resource estimation model.

Computes monthly paper volumes, overlap structure, and resource projections
for arbitrary category selections. Output is a JSON data file suitable for
use by an interactive installer.

Usage:
    python category_resource_model.py
"""

import json
import sqlite3
import time
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
RESULTS_PATH = DATA_DIR / "category_resource_model.json"


def load_papers():
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, categories, primary_category "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def build_category_model(papers):
    """Build per-category statistics and overlap structure."""

    # Per-category: papers with this as primary
    primary_counts = Counter(p["primary_category"] for p in papers)

    # Per-category: papers that list this category (primary or secondary)
    listed_counts = Counter()
    for p in papers:
        for cat in (p.get("categories") or "").split():
            cat = cat.strip()
            if cat:
                listed_counts[cat] += 1

    # Papers per category set: for each paper, which categories does it belong to?
    paper_categories = {}
    for p in papers:
        cats = frozenset(c.strip() for c in (p.get("categories") or "").split() if c.strip())
        paper_categories[p["arxiv_id"]] = cats

    # Pairwise overlap: how many papers appear in both categories?
    # Use listed_counts (not primary) for overlap
    cat_papers = defaultdict(set)
    for aid, cats in paper_categories.items():
        for cat in cats:
            cat_papers[cat].add(aid)

    # Build overlap matrix for top categories
    top_cats = [c for c, _ in listed_counts.most_common(30)]

    pairwise_overlap = {}
    for c1, c2 in combinations(top_cats, 2):
        overlap = len(cat_papers[c1] & cat_papers[c2])
        if overlap > 0:
            pairwise_overlap[f"{c1}+{c2}"] = overlap

    return primary_counts, listed_counts, cat_papers, pairwise_overlap, top_cats


def estimate_unique_papers(cat_papers, selected_categories):
    """Estimate unique papers for a category selection using inclusion-exclusion."""
    if not selected_categories:
        return 0
    union = set()
    for cat in selected_categories:
        union |= cat_papers.get(cat, set())
    return len(union)


def compute_resource_estimates(n_papers_month):
    """Compute resource estimates for a given monthly paper volume."""
    # Constants from measured experiments
    EMBED_GPU_MS_MINILM = 1.7
    EMBED_GPU_MS_SPECTER2 = 20.6
    EMBED_CPU_MS_MINILM = 35.0
    OPENALEX_RATE = 10  # req/s
    SQLITE_BYTES_PER_PAPER = int(50.4 * 1024 * 1024 / 19252)
    PG_BYTES_PER_PAPER = int(107.0 * 1024 * 1024 / 19252)
    EMB_BYTES_384 = 384 * 4
    EMB_BYTES_768 = 768 * 4
    FTS5_OVERHEAD = 1.7  # FTS index is ~1.7x the base table

    per_day = n_papers_month / 30

    return {
        "papers_per_month": n_papers_month,
        "papers_per_day": round(per_day, 1),
        "papers_per_year": n_papers_month * 12,
        "daily_compute": {
            "embed_gpu_minilm_seconds": round(per_day * EMBED_GPU_MS_MINILM / 1000, 2),
            "embed_gpu_specter2_seconds": round(per_day * EMBED_GPU_MS_SPECTER2 / 1000, 2),
            "embed_cpu_minilm_seconds": round(per_day * EMBED_CPU_MS_MINILM / 1000, 2),
            "openalex_enrich_seconds": round(per_day / OPENALEX_RATE, 2),
        },
        "cold_start": {
            "embed_gpu_minilm_minutes": round(n_papers_month * EMBED_GPU_MS_MINILM / 1000 / 60, 1),
            "embed_gpu_specter2_minutes": round(n_papers_month * EMBED_GPU_MS_SPECTER2 / 1000 / 60, 1),
            "embed_cpu_minilm_minutes": round(n_papers_month * EMBED_CPU_MS_MINILM / 1000 / 60, 1),
            "openalex_enrich_minutes": round(n_papers_month / OPENALEX_RATE / 60, 1),
        },
        "storage_per_year": {
            "sqlite_db_mb": round(n_papers_month * 12 * SQLITE_BYTES_PER_PAPER * FTS5_OVERHEAD / (1024 * 1024), 1),
            "postgresql_db_mb": round(n_papers_month * 12 * PG_BYTES_PER_PAPER / (1024 * 1024), 1),
            "embeddings_minilm_mb": round(n_papers_month * 12 * EMB_BYTES_384 / (1024 * 1024), 1),
            "embeddings_specter2_mb": round(n_papers_month * 12 * EMB_BYTES_768 / (1024 * 1024), 1),
        },
        "memory_at_1year": {
            "tfidf_matrix_mb": round(n_papers_month * 12 * 20000 * 0.001 * 4 / (1024 * 1024), 1),  # sparse, ~0.1% density
            "embeddings_minilm_mb": round(n_papers_month * 12 * EMB_BYTES_384 / (1024 * 1024), 1),
            "embeddings_specter2_mb": round(n_papers_month * 12 * EMB_BYTES_768 / (1024 * 1024), 1),
        },
    }


def main():
    print("=" * 80)
    print("Per-Category Resource Estimation Model")
    print("=" * 80)

    papers = load_papers()
    print(f"Loaded {len(papers)} papers (January 2026)")

    primary_counts, listed_counts, cat_papers, pairwise_overlap, top_cats = build_category_model(papers)

    # Per-category stats
    print(f"\n  {'Category':<12s} {'Primary':>8s} {'Listed':>8s} {'Description'}")
    print(f"  {'-' * 60}")

    category_descriptions = {
        "cs.LG": "Machine Learning",
        "cs.CV": "Computer Vision",
        "cs.CL": "Computation and Language (NLP)",
        "cs.AI": "Artificial Intelligence",
        "cs.RO": "Robotics",
        "cs.CR": "Cryptography and Security",
        "cs.SE": "Software Engineering",
        "cs.DC": "Distributed Computing",
        "cs.IT": "Information Theory",
        "cs.NI": "Networking",
        "stat.ML": "Machine Learning (Statistics)",
        "eess.SY": "Systems and Control",
        "math.OC": "Optimization and Control",
        "cs.MA": "Multiagent Systems",
        "cs.IR": "Information Retrieval",
        "cs.HC": "Human-Computer Interaction",
        "cs.DS": "Data Structures and Algorithms",
        "cs.SI": "Social and Information Networks",
        "cs.CY": "Computers and Society",
        "math.NA": "Numerical Analysis",
    }

    per_category = []
    for cat in top_cats:
        desc = category_descriptions.get(cat, "")
        primary = primary_counts.get(cat, 0)
        listed = listed_counts.get(cat, 0)
        resources = compute_resource_estimates(listed)

        per_category.append({
            "category": cat,
            "description": desc,
            "papers_primary": primary,
            "papers_listed": listed,
            "resources": resources,
        })

        print(f"  {cat:<12s} {primary:>8d} {listed:>8d}  {desc}")

    # Common presets
    presets = [
        {
            "name": "ML Researcher",
            "description": "Core machine learning + NLP + AI",
            "categories": ["cs.LG", "cs.CL", "cs.AI", "stat.ML"],
        },
        {
            "name": "CV Researcher",
            "description": "Computer vision + ML",
            "categories": ["cs.CV", "cs.LG"],
        },
        {
            "name": "NLP Researcher",
            "description": "NLP + AI + Information Retrieval",
            "categories": ["cs.CL", "cs.AI", "cs.IR"],
        },
        {
            "name": "Robotics",
            "description": "Robotics + control + multiagent",
            "categories": ["cs.RO", "eess.SY", "cs.MA"],
        },
        {
            "name": "Broad CS",
            "description": "Top 10 CS categories",
            "categories": ["cs.LG", "cs.CV", "cs.CL", "cs.AI", "cs.RO",
                          "cs.CR", "cs.SE", "cs.DC", "cs.IR", "cs.HC"],
        },
        {
            "name": "Everything",
            "description": "All 15 configured categories",
            "categories": top_cats[:15],
        },
    ]

    print(f"\n{'=' * 80}")
    print("Preset Configurations")
    print(f"{'=' * 80}")
    print(f"  {'Preset':<20s} {'Categories':>5s} {'Papers/mo':>10s} {'GPU/day':>10s} {'CPU/day':>10s} {'Storage/yr':>12s}")
    print(f"  {'-' * 70}")

    preset_results = []
    for preset in presets:
        unique = estimate_unique_papers(cat_papers, preset["categories"])
        resources = compute_resource_estimates(unique)

        gpu_daily = resources["daily_compute"]["embed_gpu_minilm_seconds"]
        cpu_daily = resources["daily_compute"]["embed_cpu_minilm_seconds"]
        storage_yr = (resources["storage_per_year"]["sqlite_db_mb"] +
                      resources["storage_per_year"]["embeddings_minilm_mb"])

        print(
            f"  {preset['name']:<20s} "
            f"{len(preset['categories']):>5d} "
            f"{unique:>10,d} "
            f"{gpu_daily:>8.1f}s "
            f"{cpu_daily:>8.1f}s "
            f"{storage_yr:>10.0f}MB"
        )

        preset_results.append({
            "name": preset["name"],
            "description": preset["description"],
            "categories": preset["categories"],
            "unique_papers_per_month": unique,
            "resources": resources,
        })

    # Output model
    model = {
        "description": (
            "Per-category resource estimation model for arxiv-mcp interactive installer. "
            "Based on January 2026 harvest data (19,252 papers across 130 categories). "
            "Resource costs derived from Spike 001 (A1c) and Spike 002 (QV3, C2) measurements."
        ),
        "data_source": "spike_001_harvest.db (January 2026)",
        "total_papers_month": len(papers),
        "total_categories": len(listed_counts),
        "per_category": per_category,
        "presets": preset_results,
        "overlap_pairs": {k: v for k, v in sorted(pairwise_overlap.items(), key=lambda x: -x[1])[:30]},
        "cost_constants": {
            "embed_gpu_minilm_ms_per_paper": 1.7,
            "embed_gpu_specter2_ms_per_paper": 20.6,
            "embed_cpu_minilm_ms_per_paper": 35.0,
            "openalex_rate_per_sec": 10,
            "sqlite_bytes_per_paper": int(50.4 * 1024 * 1024 / 19252),
            "pg_bytes_per_paper": int(107.0 * 1024 * 1024 / 19252),
            "embedding_bytes_384_per_paper": 384 * 4,
            "embedding_bytes_768_per_paper": 768 * 4,
        },
        "usage_notes": (
            "To estimate resources for a custom category selection: "
            "1. Sum listed_counts for selected categories. "
            "2. Subtract pairwise overlaps (inclusion-exclusion). "
            "3. Multiply unique paper count by cost constants. "
            "The overlap_pairs table provides the largest pairwise overlaps. "
            "For 3+ categories, full inclusion-exclusion is more accurate but "
            "pairwise subtraction is a reasonable approximation."
        ),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(model, f, indent=2)

    print(f"\n{'=' * 80}")
    print(f"Model saved to {RESULTS_PATH.name}")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
