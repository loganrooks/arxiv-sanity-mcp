"""
W1A Gap Fill: BM25 keyword search via FTS5 (S1e).

This fills the gap in W1A where BM25 keyword search strategies were listed
in DESIGN.md but never profiled. TF-IDF cosine similarity (S1d) was profiled,
but BM25 keyword search is a fundamentally different approach:

  - S1d (TF-IDF cosine): compute centroid of seed TF-IDF vectors, rank all
    papers by cosine similarity to centroid. This is a vector similarity
    operation over a shared vocabulary space.

  - S1e (BM25 keyword search): extract distinctive terms from seed papers,
    search via FTS5 full-text index, rank by BM25 scoring. This is a term
    matching operation with frequency-based ranking (term frequency, inverse
    document frequency, document length normalization).

They may find different papers because:
  - BM25 rewards exact term matches; TF-IDF cosine rewards vocabulary overlap
  - BM25 saturates on high-frequency terms (sublinear TF); TF-IDF cosine
    does not (linear TF in the centroid dot product)
  - BM25 normalizes by document length; TF-IDF cosine normalizes by vector norm

S1f (PostgreSQL tsvector BM25) is noted but not profiled here. Spike 002
already showed FTS5 and tsvector return different results (Jaccard 0.39),
and the project PostgreSQL DB only has 126 papers vs 19K in the harvest DB.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# Ensure experiments dir is on path
EXPERIMENTS_DIR = Path(__file__).resolve().parent
SPIKE_003_DIR = EXPERIMENTS_DIR.parent
sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import StrategyProfiler
from harness.strategy_protocol import SimpleStrategy
from harness.resource_meter import measure_latency, measure_setup_time


# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
SPIKE_002_DATA = SPIKE_003_DIR.parent / "002-backend-comparison" / "experiments" / "data"
SPIKE_003_DATA = SPIKE_003_DIR / "experiments" / "data"

DB_PATH = SPIKE_001_DATA / "spike_001_harvest.db"
MINILM_EMB_PATH = SPIKE_002_DATA / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DATA / "arxiv_ids_19k.json"
SPECTER2_EMB_PATH = SPIKE_003_DATA / "specter2_adapter_19k.npy"
SPECTER2_IDS_PATH = SPIKE_003_DATA / "specter2_adapter_ids.json"
PROFILES_PATH = SPIKE_003_DATA / "interest_profiles.json"
OUTPUT_PATH = SPIKE_003_DATA / "w1a_gap_bm25_profiles.json"


# ---------------------------------------------------------------------------
# FTS5 setup
# ---------------------------------------------------------------------------

def ensure_fts5_table(db_path: str) -> bool:
    """Create FTS5 table if it does not exist. Returns True if created."""
    conn = sqlite3.connect(db_path)
    # Check if table exists
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='papers_fts'"
    )
    if cursor.fetchone():
        # Verify row count matches
        fts_count = conn.execute("SELECT COUNT(*) FROM papers_fts").fetchone()[0]
        papers_count = conn.execute("SELECT COUNT(*) FROM papers").fetchone()[0]
        conn.close()
        print(f"  FTS5 table already exists ({fts_count} rows, papers table has {papers_count})")
        return False

    print("  Creating FTS5 table with porter tokenizer...")
    t0 = time.perf_counter()
    conn.execute(
        "CREATE VIRTUAL TABLE papers_fts USING fts5("
        "arxiv_id, title, abstract, tokenize='porter')"
    )
    conn.execute(
        "INSERT INTO papers_fts(arxiv_id, title, abstract) "
        "SELECT arxiv_id, title, abstract FROM papers"
    )
    conn.commit()
    t1 = time.perf_counter()

    count = conn.execute("SELECT COUNT(*) FROM papers_fts").fetchone()[0]
    conn.close()
    print(f"  FTS5 table created: {count} rows in {t1-t0:.2f}s")
    return True


# ---------------------------------------------------------------------------
# Key term extraction
# ---------------------------------------------------------------------------

def extract_key_terms(
    seed_ids: list[str],
    paper_ids: list[str],
    abstracts: list[str],
    n_terms: int = 10,
    tfidf_matrix=None,
    vectorizer=None,
    id_to_idx: dict[str, int] | None = None,
) -> list[str]:
    """Extract top TF-IDF terms from seed abstracts.

    Takes the mean TF-IDF vector across seed abstracts and returns the
    terms with the highest weights. These are the most distinctive terms
    for this set of seeds relative to the corpus.

    Args:
        seed_ids: arXiv IDs of seed papers.
        paper_ids: Ordered list of all paper IDs.
        abstracts: Abstracts in same order as paper_ids.
        n_terms: Number of top terms to extract.
        tfidf_matrix: Pre-computed TF-IDF matrix (optional, avoids rebuild).
        vectorizer: Pre-fitted TfidfVectorizer (optional, avoids rebuild).
        id_to_idx: ID-to-index mapping.

    Returns:
        List of n_terms most distinctive terms for the seed set.
    """
    if tfidf_matrix is None or vectorizer is None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(abstracts)

    if id_to_idx is None:
        id_to_idx = {pid: i for i, pid in enumerate(paper_ids)}

    feature_names = vectorizer.get_feature_names_out()
    seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
    if not seed_indices:
        return []

    # Mean TF-IDF vector across seeds
    seed_tfidf = tfidf_matrix[seed_indices].mean(axis=0).A1
    top_indices = seed_tfidf.argsort()[-n_terms:][::-1]
    return [feature_names[i] for i in top_indices]


# ---------------------------------------------------------------------------
# BM25 strategy via FTS5
# ---------------------------------------------------------------------------

def make_bm25_fts5_strategy(
    db_path: str,
    paper_ids: list[str],
    abstracts: list[str],
    id_to_idx: dict[str, int],
    n_terms: int = 10,
    tfidf_matrix=None,
    vectorizer=None,
) -> SimpleStrategy:
    """S1e: BM25 keyword search via FTS5.

    1. Extract top TF-IDF terms from seed abstracts
    2. Build FTS5 MATCH query (OR of terms)
    3. Query FTS5 table, ranked by BM25
    4. Map FTS5 results back to full corpus scoring array

    FTS5's rank column returns negative BM25 scores (lower = better match).
    We negate to get positive scores where higher = better.

    The strategy returns scores for ALL papers in paper_ids (0 for non-matches)
    so it works with the standard SimpleStrategy.recommend() top-k logic.
    """

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        # Extract distinctive terms
        terms = extract_key_terms(
            seed_ids, paper_ids, abstracts, n_terms=n_terms,
            tfidf_matrix=tfidf_matrix, vectorizer=vectorizer,
            id_to_idx=id_to_idx,
        )
        if not terms:
            return np.zeros(len(paper_ids))

        # Build FTS5 MATCH query: OR of terms
        # FTS5 query syntax: term1 OR term2 OR term3
        match_query = " OR ".join(terms)

        # Query FTS5 -- rank is negative BM25 (lower = better match)
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT arxiv_id, rank FROM papers_fts "
                "WHERE papers_fts MATCH ? "
                "ORDER BY rank "
                "LIMIT 500",  # Get generous set for scoring
                (match_query,),
            )
            results = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"    FTS5 query error: {e}")
            print(f"    Query was: {match_query}")
            conn.close()
            return np.zeros(len(paper_ids))
        finally:
            conn.close()

        # Map results to full corpus score array
        scores = np.zeros(len(paper_ids))
        for arxiv_id, rank_val in results:
            if arxiv_id in id_to_idx:
                # Negate rank (FTS5 rank is negative; more negative = better)
                scores[id_to_idx[arxiv_id]] = -rank_val

        return scores

    return SimpleStrategy(
        name="BM25 keyword search (FTS5)",
        strategy_id="S1e",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_bm25_fts5_wide_strategy(
    db_path: str,
    paper_ids: list[str],
    abstracts: list[str],
    id_to_idx: dict[str, int],
    n_terms: int = 20,
    tfidf_matrix=None,
    vectorizer=None,
) -> SimpleStrategy:
    """S1e-wide: BM25 keyword search with more terms (20 vs 10).

    Tests whether extracting more terms improves recall at the cost of
    precision. More terms = broader query = more matches but potentially
    less focused.
    """

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        terms = extract_key_terms(
            seed_ids, paper_ids, abstracts, n_terms=n_terms,
            tfidf_matrix=tfidf_matrix, vectorizer=vectorizer,
            id_to_idx=id_to_idx,
        )
        if not terms:
            return np.zeros(len(paper_ids))

        match_query = " OR ".join(terms)

        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT arxiv_id, rank FROM papers_fts "
                "WHERE papers_fts MATCH ? "
                "ORDER BY rank "
                "LIMIT 500",
                (match_query,),
            )
            results = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f"    FTS5 query error: {e}")
            conn.close()
            return np.zeros(len(paper_ids))
        finally:
            conn.close()

        scores = np.zeros(len(paper_ids))
        for arxiv_id, rank_val in results:
            if arxiv_id in id_to_idx:
                scores[id_to_idx[arxiv_id]] = -rank_val

        return scores

    return SimpleStrategy(
        name="BM25 keyword search (FTS5, 20 terms)",
        strategy_id="S1e-wide",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Overlap analysis: BM25 vs TF-IDF cosine vs embedding strategies
# ---------------------------------------------------------------------------

def compute_overlap(
    strategy_a, strategy_b,
    seed_ids: list[str],
    top_k: int = 20,
) -> dict:
    """Compute recommendation overlap between two strategies.

    Returns Jaccard similarity and set counts for a given seed set.
    """
    recs_a = set(r[0] for r in strategy_a.recommend(seed_ids, top_k=top_k))
    recs_b = set(r[0] for r in strategy_b.recommend(seed_ids, top_k=top_k))

    intersection = recs_a & recs_b
    union = recs_a | recs_b

    jaccard = len(intersection) / len(union) if union else 0.0

    return {
        "jaccard": jaccard,
        "intersection_size": len(intersection),
        "a_only": len(recs_a - recs_b),
        "b_only": len(recs_b - recs_a),
        "a_size": len(recs_a),
        "b_size": len(recs_b),
    }


def run_overlap_analysis(
    bm25_strategy,
    comparison_strategies: list[tuple[str, object]],
    profiles,
    top_k: int = 20,
) -> dict:
    """Compute overlap between BM25 and other strategies across all profiles.

    This answers: "Does BM25 find different papers than TF-IDF cosine /
    embedding centroid?"
    """
    results = {}

    for comp_id, comp_strategy in comparison_strategies:
        profile_overlaps = []
        for prof in profiles:
            for seed_set in prof.seed_sets:
                overlap = compute_overlap(
                    bm25_strategy, comp_strategy,
                    seed_ids=seed_set,
                    top_k=top_k,
                )
                overlap["profile_id"] = prof.profile_id
                profile_overlaps.append(overlap)

        jaccards = [o["jaccard"] for o in profile_overlaps]
        results[comp_id] = {
            "mean_jaccard": float(np.mean(jaccards)),
            "std_jaccard": float(np.std(jaccards)),
            "min_jaccard": float(np.min(jaccards)),
            "max_jaccard": float(np.max(jaccards)),
            "per_profile": profile_overlaps,
        }

    return results


# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------

def run_bm25_profiling():
    """Profile BM25 keyword search strategies and compare with W1A baselines."""

    print("=" * 70)
    print("W1A GAP FILL: BM25 Keyword Search (S1e) via FTS5")
    print("=" * 70)
    t_start = time.perf_counter()

    # ----- Ensure FTS5 table -----
    print("\n--- FTS5 Setup ---")
    fts5_created = ensure_fts5_table(str(DB_PATH))

    # ----- Load profiler (handles data loading + clustering) -----
    print("\n--- Data Loading ---")
    profiler = StrategyProfiler.from_spike_data(
        db_path=str(DB_PATH),
        minilm_emb_path=str(MINILM_EMB_PATH),
        minilm_ids_path=str(MINILM_IDS_PATH),
        profiles_path=str(PROFILES_PATH),
        specter2_emb_path=str(SPECTER2_EMB_PATH),
        specter2_ids_path=str(SPECTER2_IDS_PATH),
    )

    paper_ids = profiler.paper_ids
    id_to_idx = profiler.id_to_idx
    n_papers = len(paper_ids)
    print(f"\nCorpus: {n_papers} papers, {len(profiler.profiles)} profiles")

    # ----- Load abstracts for TF-IDF term extraction -----
    print("\nLoading abstracts from DB...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
    abstract_map = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    abstracts = [abstract_map.get(pid, "") for pid in paper_ids]
    missing_abstracts = sum(1 for a in abstracts if not a)
    print(f"  {n_papers - missing_abstracts} abstracts loaded, {missing_abstracts} missing")

    # ----- Build TF-IDF for term extraction (shared across strategies) -----
    print("\nBuilding TF-IDF matrix for key term extraction...")
    from sklearn.feature_extraction.text import TfidfVectorizer
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    t1 = time.perf_counter()
    print(f"  TF-IDF matrix: {tfidf_matrix.shape}, built in {t1-t0:.1f}s")

    # ----- Demonstrate key term extraction for one profile -----
    print("\n--- Key Term Extraction Demo ---")
    for prof in profiler.profiles[:3]:
        seed_set = prof.seed_sets[0]
        terms = extract_key_terms(
            seed_set, paper_ids, abstracts, n_terms=10,
            tfidf_matrix=tfidf_matrix, vectorizer=vectorizer,
            id_to_idx=id_to_idx,
        )
        print(f"  {prof.profile_id} ({prof.name}): {terms}")

    # ----- Build BM25 strategies -----
    print("\n--- Building BM25 Strategies ---")

    # S1e: BM25 with 10 key terms
    print("\n[S1e] BM25 keyword search (FTS5, 10 terms)")
    s1e = make_bm25_fts5_strategy(
        str(DB_PATH), paper_ids, abstracts, id_to_idx,
        n_terms=10, tfidf_matrix=tfidf_matrix, vectorizer=vectorizer,
    )

    # S1e-wide: BM25 with 20 key terms
    print("[S1e-wide] BM25 keyword search (FTS5, 20 terms)")
    s1e_wide = make_bm25_fts5_wide_strategy(
        str(DB_PATH), paper_ids, abstracts, id_to_idx,
        n_terms=20, tfidf_matrix=tfidf_matrix, vectorizer=vectorizer,
    )

    # ----- Quick sanity check: verify FTS5 returns results -----
    print("\n--- Sanity Check ---")
    test_seeds = profiler.profiles[0].seed_sets[0]
    test_recs = s1e.recommend(test_seeds, top_k=20)
    print(f"  S1e returned {len(test_recs)} recommendations for {profiler.profiles[0].profile_id}")
    if test_recs:
        print(f"  Top-3 scores: {[f'{r[1]:.4f}' for r in test_recs[:3]]}")
        # Show the titles of top-3
        for aid, score in test_recs[:3]:
            title = profiler.corpus.get(aid, {}).get("title", "?")[:80]
            print(f"    {aid}: {score:.4f} - {title}")

    # ----- Profile each BM25 strategy -----
    strategies = [
        ("S1e", s1e, {"search": "FTS5", "tokenizer": "porter", "n_terms": 10, "limit": 500}),
        ("S1e-wide", s1e_wide, {"search": "FTS5", "tokenizer": "porter", "n_terms": 20, "limit": 500}),
    ]

    all_cards = []
    strategy_timings = {}

    for sid, strategy, config in strategies:
        print(f"\n{'='*60}")
        print(f"PROFILING: {strategy.name} ({strategy.strategy_id})")
        print(f"{'='*60}")
        t0 = time.perf_counter()

        card = profiler.profile(
            strategy,
            config=config,
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=100,
        )
        t1 = time.perf_counter()
        strategy_timings[sid] = t1 - t0

        # Print summary
        print(f"\n  --- Summary for {sid} ---")
        instruments = card.get("instruments", {})
        for inst_name in [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]:
            inst = instruments.get(inst_name, {})
            mean = inst.get("mean")
            std = inst.get("std")
            if mean is not None:
                print(f"    {inst_name:<25s} {mean:.4f} (+/- {std:.4f})")
            else:
                print(f"    {inst_name:<25s} (no data)")

        res = card.get("resources", {})
        lat = res.get("query_latency_ms", {})
        if lat:
            print(f"    latency p50={lat.get('p50', 0):.2f}ms  p95={lat.get('p95', 0):.2f}ms")
        print(f"    profiling time: {strategy_timings[sid]:.1f}s")

        all_cards.append(card)

    # ----- Cross-strategy comparison (within BM25 variants) -----
    print(f"\n{'='*60}")
    print("BM25 INTERNAL COMPARISON")
    print(f"{'='*60}")
    bm25_comparison = profiler.compare(all_cards)

    # ----- Overlap analysis with W1A strategies -----
    print(f"\n{'='*60}")
    print("OVERLAP ANALYSIS: BM25 vs W1A Strategies")
    print(f"{'='*60}")

    # Rebuild TF-IDF cosine strategy for overlap comparison
    print("\n  Rebuilding S1d (TF-IDF cosine) for overlap analysis...")

    def tfidf_score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        seed_vectors = tfidf_matrix[seed_indices]
        centroid = np.asarray(seed_vectors.mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
        return scores

    s1d = SimpleStrategy(
        name="TF-IDF cosine similarity",
        strategy_id="S1d",
        score_fn=tfidf_score_fn,
        paper_ids=paper_ids,
    )

    # MiniLM centroid strategy
    print("  Rebuilding S1a (MiniLM centroid) for overlap analysis...")

    def minilm_score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = profiler.embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return profiler.embeddings @ centroid

    s1a = SimpleStrategy(
        name="MiniLM embedding centroid",
        strategy_id="S1a",
        score_fn=minilm_score_fn,
        paper_ids=paper_ids,
    )

    # Compute overlaps
    overlap_results = run_overlap_analysis(
        s1e,
        [
            ("S1d", s1d),
            ("S1a", s1a),
        ],
        profiler.profiles,
        top_k=20,
    )

    print("\n  Overlap summary (Jaccard similarity, top-20):")
    for comp_id, data in overlap_results.items():
        print(f"    S1e vs {comp_id}: Jaccard={data['mean_jaccard']:.3f} "
              f"(+/- {data['std_jaccard']:.3f})")

    # Also compute S1e-wide overlaps
    overlap_wide_results = run_overlap_analysis(
        s1e_wide,
        [
            ("S1e", s1e),
            ("S1d", s1d),
            ("S1a", s1a),
        ],
        profiler.profiles,
        top_k=20,
    )

    print("\n  S1e-wide overlaps:")
    for comp_id, data in overlap_wide_results.items():
        print(f"    S1e-wide vs {comp_id}: Jaccard={data['mean_jaccard']:.3f} "
              f"(+/- {data['std_jaccard']:.3f})")

    # ----- Per-profile comparison with W1A reference data -----
    print(f"\n{'='*60}")
    print("PER-PROFILE COMPARISON: S1e vs S1d vs S1a")
    print(f"{'='*60}")

    # Load W1A reference data for comparison
    w1a_ref_path = SPIKE_003_DATA / "w1a_content_profiles.json"
    w1a_ref = {}
    if w1a_ref_path.exists():
        with open(w1a_ref_path) as f:
            w1a_data = json.load(f)
        for card in w1a_data.get("profile_cards", []):
            w1a_ref[card["strategy_id"]] = card

    # Print per-profile MRR comparison
    s1e_card = all_cards[0]  # S1e (10 terms)
    s1e_wide_card = all_cards[1]  # S1e-wide (20 terms)

    print(f"\n{'Profile':<45s} {'S1e':>7s} {'S1e-w':>7s} {'S1d':>7s} {'S1a':>7s}")
    print("-" * 75)

    for prof in profiler.profiles:
        pid = prof.profile_id

        def get_mrr(card, pid):
            bp = card.get("by_profile", {}).get(pid, {})
            inst = bp.get("instruments", {}).get("leave_one_out_mrr", {})
            return inst.get("mean")

        s1e_mrr = get_mrr(s1e_card, pid)
        s1ew_mrr = get_mrr(s1e_wide_card, pid)

        # Get W1A reference values
        s1d_mrr = None
        s1a_mrr = None
        if "S1d" in w1a_ref:
            s1d_mrr = get_mrr(w1a_ref["S1d"], pid)
        if "S1a" in w1a_ref:
            s1a_mrr = get_mrr(w1a_ref["S1a"], pid)

        def fmt(v):
            return f"{v:.4f}" if v is not None else "  N/A "

        label = f"{pid}: {prof.name}"[:44]
        print(f"{label:<45s} {fmt(s1e_mrr):>7s} {fmt(s1ew_mrr):>7s} {fmt(s1d_mrr):>7s} {fmt(s1a_mrr):>7s}")

    # ----- FTS5 index build time -----
    print(f"\n{'='*60}")
    print("FTS5 INDEX BUILD TIME")
    print(f"{'='*60}")

    fts5_build_time = measure_setup_time(
        setup_fn=lambda: _rebuild_fts5(str(DB_PATH)),
        n_runs=3,
    )
    print(f"  FTS5 build: mean={fts5_build_time['mean_s']:.2f}s")

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "experiment": "W1A Gap Fill: BM25 keyword search (S1e) via FTS5",
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "total_time_s": round(total_time, 1),
        "corpus_size": n_papers,
        "n_profiles": len(profiler.profiles),
        "strategies_profiled": [c["strategy_id"] for c in all_cards],
        "profile_cards": all_cards,
        "bm25_comparison": bm25_comparison,
        "overlap_analysis": {
            "S1e_vs_others": {
                k: {kk: vv for kk, vv in v.items() if kk != "per_profile"}
                for k, v in overlap_results.items()
            },
            "S1e_wide_vs_others": {
                k: {kk: vv for kk, vv in v.items() if kk != "per_profile"}
                for k, v in overlap_wide_results.items()
            },
            "full_overlap_S1e": overlap_results,
            "full_overlap_S1e_wide": overlap_wide_results,
        },
        "additional_resources": {
            "fts5_build_time": fts5_build_time,
        },
        "strategy_profiling_times_s": {k: round(v, 1) for k, v in strategy_timings.items()},
        "notes": {
            "S1f_not_profiled": (
                "S1f (PostgreSQL tsvector BM25) not profiled. The project PostgreSQL DB "
                "has only 126 papers vs 19K in the harvest DB. Spike 002 already showed "
                "FTS5 and tsvector return different results (Jaccard 0.39). Setting up "
                "PostgreSQL with 19K papers would add substantial overhead for this spike."
            ),
            "term_extraction": (
                "Key terms extracted using TF-IDF weights from seed abstracts. "
                "Top-N terms by mean TF-IDF weight across seed papers form the "
                "FTS5 MATCH query (OR of terms)."
            ),
            "bm25_scoring": (
                "FTS5 rank column returns negative BM25 scores (Okapi BM25 variant). "
                "Negated for positive-higher-is-better convention. "
                "FTS5 uses k1=1.2, b=0.75 defaults."
            ),
            "limit_500": (
                "FTS5 query returns up to 500 results. Papers not in FTS5 results "
                "receive score 0. This means BM25 can only rank papers that contain "
                "at least one search term, unlike TF-IDF cosine which scores all papers."
            ),
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\n{'='*60}")
    print("W1A GAP FILL COMPLETE")
    print(f"{'='*60}")
    print(f"Total time: {total_time:.1f}s ({total_time/60:.1f}m)")
    print(f"Strategies profiled: {len(all_cards)}")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


def _rebuild_fts5(db_path: str):
    """Drop and recreate FTS5 table (for timing measurement)."""
    conn = sqlite3.connect(db_path)
    conn.execute("DROP TABLE IF EXISTS papers_fts_temp")
    conn.execute(
        "CREATE VIRTUAL TABLE papers_fts_temp USING fts5("
        "arxiv_id, title, abstract, tokenize='porter')"
    )
    conn.execute(
        "INSERT INTO papers_fts_temp(arxiv_id, title, abstract) "
        "SELECT arxiv_id, title, abstract FROM papers"
    )
    conn.commit()
    conn.execute("DROP TABLE papers_fts_temp")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_bm25_profiling()
