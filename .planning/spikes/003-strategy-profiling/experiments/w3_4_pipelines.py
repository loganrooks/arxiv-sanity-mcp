"""
W3.4: Asymmetric Pipeline Comparison — Retrieve + Re-rank Architectures.

Key insight from W3: RRF and weighted fusion DEGRADE MiniLM quality because
co-equal fusion gives weaker strategies (TF-IDF, SPECTER2) corrupting
voting power. Best RRF combo MRR=0.310 vs MiniLM alone MRR=0.398.

But W3.6 consensus analysis proved TF-IDF finds 9 held-out papers MiniLM
misses entirely (Jaccard=0.179 overlap). The strategies are complementary
in candidate coverage, but not in ranking quality.

Solution: asymmetric pipeline — use one strategy to EXPAND the candidate
pool, then use MiniLM to RE-RANK.

Pipelines tested:
  P1: TF-IDF retrieve top-200 -> MiniLM re-rank -> top-20
  P2: TF-IDF retrieve top-100 -> MiniLM re-rank -> top-20
  P3: MiniLM retrieve top-200 -> TF-IDF re-rank -> top-20 (reverse control)
  P4: SPECTER2 retrieve top-200 -> MiniLM re-rank -> top-20
  P5: (TF-IDF top-100 + MiniLM top-100) -> MiniLM re-rank -> top-20
  P6: (TF-IDF + MiniLM + SPECTER2 top-100 each) -> MiniLM re-rank -> top-20

Compare against:
  - S1a alone (MRR=0.398, Coverage=0.686) — the baseline to beat
  - Best RRF combo C2 (MRR=0.310) — from W3.1
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

EXPERIMENTS_DIR = Path(__file__).resolve().parent
SPIKE_003_DIR = EXPERIMENTS_DIR.parent
SPIKES_DIR = SPIKE_003_DIR.parent
sys.path.insert(0, str(EXPERIMENTS_DIR))

SPIKE_001_DATA = SPIKES_DIR / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
SPIKE_002_DATA = SPIKES_DIR / "002-backend-comparison" / "experiments" / "data"
SPIKE_003_DATA = SPIKE_003_DIR / "experiments" / "data"

DB_PATH = SPIKE_001_DATA / "spike_001_harvest.db"
MINILM_EMB_PATH = SPIKE_002_DATA / "embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002_DATA / "arxiv_ids_19k.json"
SPECTER2_EMB_PATH = SPIKE_003_DATA / "specter2_adapter_19k.npy"
SPECTER2_IDS_PATH = SPIKE_003_DATA / "specter2_adapter_ids.json"
PROFILES_PATH = SPIKE_003_DATA / "interest_profiles.json"
OUTPUT_PATH = SPIKE_003_DATA / "w3_4_pipeline_profiles.json"


# ---------------------------------------------------------------------------
# JSON encoder for numpy types
# ---------------------------------------------------------------------------

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, (np.bool_,)):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


# ---------------------------------------------------------------------------
# PipelineStrategy: retrieve + re-rank architecture
# ---------------------------------------------------------------------------

class PipelineStrategy:
    """A strategy that retrieves candidates with one scorer, re-ranks with another.

    This is the key architectural difference from CombinedStrategy (W3.1-W3.3):
    the retriever expands the candidate pool, but the ranker has SOLE authority
    over the final ordering. No co-equal voting, no fusion.

    Implements the RecommendationStrategy protocol for profiler compatibility.
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        retriever_fn,
        ranker_fn,
        paper_ids: list[str],
        retrieve_k: int = 200,
    ):
        """
        Args:
            name: Human-readable name.
            strategy_id: Machine identifier (e.g., 'P1').
            retriever_fn: (seed_ids) -> list[(arxiv_id, score)] in retriever's score space.
                          Returns a FULL ranked list of all papers, sorted desc.
            ranker_fn: (candidate_ids, seed_ids) -> list[(arxiv_id, score)] re-ranked.
                       Only scores the given candidate set.
            paper_ids: Full corpus paper IDs.
            retrieve_k: How many candidates the retriever returns.
        """
        self._name = name
        self._strategy_id = strategy_id
        self._retriever_fn = retriever_fn
        self._ranker_fn = ranker_fn
        self._paper_ids = paper_ids
        self._retrieve_k = retrieve_k

    @property
    def name(self):
        return self._name

    @property
    def strategy_id(self):
        return self._strategy_id

    def recommend(self, seed_arxiv_ids: list[str], top_k: int = 20) -> list[tuple[str, float]]:
        """Retrieve candidates, then re-rank with the ranker."""
        seed_set = set(seed_arxiv_ids)

        # Step 1: Retrieve candidates (exclude seeds)
        retriever_results = self._retriever_fn(seed_arxiv_ids)
        candidates = [
            (pid, score) for pid, score in retriever_results
            if pid not in seed_set
        ][:self._retrieve_k]

        if not candidates:
            return []

        candidate_ids = [pid for pid, _ in candidates]

        # Step 2: Re-rank candidates using the ranker
        reranked = self._ranker_fn(candidate_ids, seed_arxiv_ids)

        # Return top-k from re-ranked list
        return reranked[:top_k]


class UnionPipelineStrategy:
    """Like PipelineStrategy, but takes the UNION of multiple retrievers' candidates.

    Deduplicates before re-ranking. This tests candidate pool expansion
    without giving any retriever voting power over final rankings.
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        retriever_fns: list,
        ranker_fn,
        paper_ids: list[str],
        retrieve_k_each: int = 100,
    ):
        self._name = name
        self._strategy_id = strategy_id
        self._retriever_fns = retriever_fns
        self._ranker_fn = ranker_fn
        self._paper_ids = paper_ids
        self._retrieve_k_each = retrieve_k_each

    @property
    def name(self):
        return self._name

    @property
    def strategy_id(self):
        return self._strategy_id

    def recommend(self, seed_arxiv_ids: list[str], top_k: int = 20) -> list[tuple[str, float]]:
        """Union of retriever candidates, then re-rank."""
        seed_set = set(seed_arxiv_ids)

        # Step 1: Get candidates from each retriever
        all_candidates = set()
        for retriever_fn in self._retriever_fns:
            results = retriever_fn(seed_arxiv_ids)
            non_seed = [(pid, s) for pid, s in results if pid not in seed_set]
            for pid, _ in non_seed[:self._retrieve_k_each]:
                all_candidates.add(pid)

        if not all_candidates:
            return []

        candidate_ids = sorted(all_candidates)  # Deterministic order

        # Step 2: Re-rank the union
        reranked = self._ranker_fn(candidate_ids, seed_arxiv_ids)
        return reranked[:top_k]


# ---------------------------------------------------------------------------
# Scoring functions (retrieval and re-ranking building blocks)
# ---------------------------------------------------------------------------

def build_embedding_scorer(embeddings, paper_ids, id_to_idx):
    """Return a function: (seed_ids) -> list[(arxiv_id, score)] sorted desc.

    Uses centroid cosine similarity in the given embedding space.
    """
    def scorer(seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return [(pid, 0.0) for pid in paper_ids]
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return [(pid, 0.0) for pid in paper_ids]
        centroid = centroid / norm
        scores = embeddings @ centroid
        ranked = sorted(
            [(pid, float(scores[i])) for i, pid in enumerate(paper_ids)],
            key=lambda x: -x[1],
        )
        return ranked
    return scorer


def build_tfidf_scorer(tfidf_matrix, paper_ids, id_to_idx):
    """Return a function: (seed_ids) -> list[(arxiv_id, score)] sorted desc.

    Uses TF-IDF centroid cosine similarity.
    """
    def scorer(seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return [(pid, 0.0) for pid in paper_ids]
        centroid = np.asarray(tfidf_matrix[seed_indices].mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return [(pid, 0.0) for pid in paper_ids]
        centroid = centroid / norm
        scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
        ranked = sorted(
            [(pid, float(scores[i])) for i, pid in enumerate(paper_ids)],
            key=lambda x: -x[1],
        )
        return ranked
    return scorer


def build_embedding_reranker(embeddings, id_to_idx):
    """Return a function: (candidate_ids, seed_ids) -> list[(arxiv_id, score)] sorted desc.

    Scores only the given candidates by cosine similarity to seed centroid.
    """
    def reranker(candidate_ids, seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return [(pid, 0.0) for pid in candidate_ids]
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return [(pid, 0.0) for pid in candidate_ids]
        centroid = centroid / norm

        scored = []
        for pid in candidate_ids:
            if pid in id_to_idx:
                sim = float(embeddings[id_to_idx[pid]] @ centroid)
                scored.append((pid, sim))
            else:
                scored.append((pid, 0.0))

        scored.sort(key=lambda x: -x[1])
        return scored
    return reranker


def build_tfidf_reranker(tfidf_matrix, paper_ids, id_to_idx):
    """Return a function: (candidate_ids, seed_ids) -> list[(arxiv_id, score)] sorted desc.

    Scores only the given candidates by TF-IDF cosine similarity to seed centroid.
    """
    def reranker(candidate_ids, seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return [(pid, 0.0) for pid in candidate_ids]
        centroid = np.asarray(tfidf_matrix[seed_indices].mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return [(pid, 0.0) for pid in candidate_ids]
        centroid = centroid / norm

        # Score all papers, then filter to candidates
        all_scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
        scored = []
        for pid in candidate_ids:
            if pid in id_to_idx:
                scored.append((pid, float(all_scores[id_to_idx[pid]])))
            else:
                scored.append((pid, 0.0))

        scored.sort(key=lambda x: -x[1])
        return scored
    return reranker


# ---------------------------------------------------------------------------
# Pipeline construction
# ---------------------------------------------------------------------------

def build_pipelines(
    minilm_embeddings, specter2_embeddings, tfidf_matrix,
    paper_ids, minilm_id_to_idx, specter2_id_to_idx,
):
    """Build all 6 pipeline strategies.

    Returns dict mapping pipeline ID to (strategy, config_dict).
    """
    # Build scoring/ranking primitives
    minilm_scorer = build_embedding_scorer(minilm_embeddings, paper_ids, minilm_id_to_idx)
    specter2_scorer = build_embedding_scorer(specter2_embeddings, paper_ids, specter2_id_to_idx)
    tfidf_scorer = build_tfidf_scorer(tfidf_matrix, paper_ids, minilm_id_to_idx)

    minilm_reranker = build_embedding_reranker(minilm_embeddings, minilm_id_to_idx)
    tfidf_reranker = build_tfidf_reranker(tfidf_matrix, paper_ids, minilm_id_to_idx)

    pipelines = {}

    # P1: TF-IDF retrieve top-200 -> MiniLM re-rank
    pipelines["P1"] = (
        PipelineStrategy(
            name="TF-IDF->MiniLM (k=200)",
            strategy_id="P1",
            retriever_fn=tfidf_scorer,
            ranker_fn=minilm_reranker,
            paper_ids=paper_ids,
            retrieve_k=200,
        ),
        {
            "retriever": "S1d (TF-IDF cosine)",
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k": 200,
            "architecture": "retrieve-rerank",
        },
    )

    # P2: TF-IDF retrieve top-100 -> MiniLM re-rank (narrower pool)
    pipelines["P2"] = (
        PipelineStrategy(
            name="TF-IDF->MiniLM (k=100)",
            strategy_id="P2",
            retriever_fn=tfidf_scorer,
            ranker_fn=minilm_reranker,
            paper_ids=paper_ids,
            retrieve_k=100,
        ),
        {
            "retriever": "S1d (TF-IDF cosine)",
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k": 100,
            "architecture": "retrieve-rerank",
        },
    )

    # P3: MiniLM retrieve top-200 -> TF-IDF re-rank (REVERSE -- control experiment)
    pipelines["P3"] = (
        PipelineStrategy(
            name="MiniLM->TF-IDF (k=200)",
            strategy_id="P3",
            retriever_fn=minilm_scorer,
            ranker_fn=tfidf_reranker,
            paper_ids=paper_ids,
            retrieve_k=200,
        ),
        {
            "retriever": "S1a (MiniLM centroid)",
            "ranker": "S1d (TF-IDF cosine)",
            "retrieve_k": 200,
            "architecture": "retrieve-rerank (reversed)",
            "note": "Control: tests whether asymmetry direction matters",
        },
    )

    # P4: SPECTER2 retrieve top-200 -> MiniLM re-rank
    pipelines["P4"] = (
        PipelineStrategy(
            name="SPECTER2->MiniLM (k=200)",
            strategy_id="P4",
            retriever_fn=specter2_scorer,
            ranker_fn=minilm_reranker,
            paper_ids=paper_ids,
            retrieve_k=200,
        ),
        {
            "retriever": "S1c (SPECTER2 adapter centroid)",
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k": 200,
            "architecture": "retrieve-rerank",
            "note": "Tests SPECTER2 candidate expansion despite score compression",
        },
    )

    # P5: Union(TF-IDF top-100, MiniLM top-100) -> MiniLM re-rank
    pipelines["P5"] = (
        UnionPipelineStrategy(
            name="(TF-IDF+MiniLM)->MiniLM (k=100 each)",
            strategy_id="P5",
            retriever_fns=[tfidf_scorer, minilm_scorer],
            ranker_fn=minilm_reranker,
            paper_ids=paper_ids,
            retrieve_k_each=100,
        ),
        {
            "retrievers": ["S1d (TF-IDF)", "S1a (MiniLM)"],
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k_each": 100,
            "architecture": "union-retrieve-rerank",
            "note": "Candidate pool expansion without equal-weight fusion",
        },
    )

    # P6: Union(TF-IDF, MiniLM, SPECTER2 top-100 each) -> MiniLM re-rank
    pipelines["P6"] = (
        UnionPipelineStrategy(
            name="(TF-IDF+MiniLM+SPECTER2)->MiniLM (k=100 each)",
            strategy_id="P6",
            retriever_fns=[tfidf_scorer, minilm_scorer, specter2_scorer],
            ranker_fn=minilm_reranker,
            paper_ids=paper_ids,
            retrieve_k_each=100,
        ),
        {
            "retrievers": ["S1d (TF-IDF)", "S1a (MiniLM)", "S1c (SPECTER2)"],
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k_each": 100,
            "architecture": "union-retrieve-rerank",
            "note": "Maximum candidate expansion, MiniLM sole ranker",
        },
    )

    return pipelines


# ---------------------------------------------------------------------------
# Candidate overlap analysis
# ---------------------------------------------------------------------------

def analyze_candidate_pools(pipelines_dict, profiler):
    """Analyze what each pipeline retriever contributes to the candidate pool.

    For each profile x seed_set, measure:
    - How many unique candidates each retriever contributes
    - Overlap between retriever candidate pools
    - How many held-out papers are in the candidate pool but NOT in MiniLM top-200

    IMPORTANT: Retriever scorers return sorted lists. We must preserve sort
    order when taking top-k, then convert to set for overlap analysis.
    """
    print("\n" + "=" * 70)
    print("CANDIDATE POOL ANALYSIS")
    print("=" * 70)

    # Extract retrievers from P1, P4, and the MiniLM baseline
    p1_strategy = pipelines_dict["P1"][0]
    p4_strategy = pipelines_dict["P4"][0]
    p5_strategy = pipelines_dict["P5"][0]

    profiles = profiler.profiles
    pool_stats = []

    for prof in profiles:
        for si, seed_set in enumerate(prof.seed_sets):
            seed_set_set = set(seed_set)

            # Get retriever candidate pools -- PRESERVE SORT ORDER before set conversion
            # Scorers return list[(pid, score)] sorted by score desc

            # TF-IDF top-200 (non-seed)
            tfidf_retrieval = p1_strategy._retriever_fn(seed_set)
            tfidf_non_seed = [
                (pid, s) for pid, s in tfidf_retrieval if pid not in seed_set_set
            ]
            tfidf_top200 = set(pid for pid, _ in tfidf_non_seed[:200])

            # MiniLM top-200 (non-seed)
            minilm_retrieval = p5_strategy._retriever_fns[1](seed_set)
            minilm_non_seed = [
                (pid, s) for pid, s in minilm_retrieval if pid not in seed_set_set
            ]
            minilm_top200 = set(pid for pid, _ in minilm_non_seed[:200])

            # SPECTER2 top-200 (non-seed)
            specter2_retrieval = p4_strategy._retriever_fn(seed_set)
            specter2_non_seed = [
                (pid, s) for pid, s in specter2_retrieval if pid not in seed_set_set
            ]
            specter2_top200 = set(pid for pid, _ in specter2_non_seed[:200])

            # Overlap analysis
            tfidf_minilm_overlap = len(tfidf_top200 & minilm_top200)
            tfidf_only = tfidf_top200 - minilm_top200
            minilm_only = minilm_top200 - tfidf_top200
            specter2_only = specter2_top200 - minilm_top200 - tfidf_top200

            # Held-out coverage in candidate pools
            held_out_set = set(prof.held_out)
            tfidf_held = len(tfidf_top200 & held_out_set)
            minilm_held = len(minilm_top200 & held_out_set)
            specter2_held = len(specter2_top200 & held_out_set)
            tfidf_only_held = len(tfidf_only & held_out_set)
            specter2_only_held = len(specter2_only & held_out_set)

            # Union sizes
            union_2 = tfidf_top200 | minilm_top200
            union_3 = union_2 | specter2_top200

            pool_stats.append({
                "profile_id": prof.profile_id,
                "seed_set": si,
                "tfidf_minilm_overlap": tfidf_minilm_overlap,
                "tfidf_only": len(tfidf_only),
                "minilm_only": len(minilm_only),
                "specter2_only": len(specter2_only),
                "union_tfidf_minilm": len(union_2),
                "union_all_three": len(union_3),
                "tfidf_held_out": tfidf_held,
                "minilm_held_out": minilm_held,
                "specter2_held_out": specter2_held,
                "tfidf_only_held_out": tfidf_only_held,
                "specter2_only_held_out": specter2_only_held,
            })

    # Aggregate
    n = len(pool_stats)
    def mean_field(field):
        return sum(s[field] for s in pool_stats) / n if n > 0 else 0

    summary = {
        "mean_tfidf_minilm_overlap": round(mean_field("tfidf_minilm_overlap"), 1),
        "mean_tfidf_only": round(mean_field("tfidf_only"), 1),
        "mean_minilm_only": round(mean_field("minilm_only"), 1),
        "mean_specter2_only": round(mean_field("specter2_only"), 1),
        "mean_union_2": round(mean_field("union_tfidf_minilm"), 1),
        "mean_union_3": round(mean_field("union_all_three"), 1),
        "total_tfidf_only_held_out": sum(s["tfidf_only_held_out"] for s in pool_stats),
        "total_specter2_only_held_out": sum(s["specter2_only_held_out"] for s in pool_stats),
        "total_tfidf_held_out": sum(s["tfidf_held_out"] for s in pool_stats),
        "total_minilm_held_out": sum(s["minilm_held_out"] for s in pool_stats),
        "total_specter2_held_out": sum(s["specter2_held_out"] for s in pool_stats),
        "n_evaluations": n,
    }

    print(f"  Candidate pool overlap (top-200 each, {n} evaluations):")
    print(f"    TF-IDF n MiniLM: {summary['mean_tfidf_minilm_overlap']:.1f}/200")
    print(f"    TF-IDF only: {summary['mean_tfidf_only']:.1f}")
    print(f"    MiniLM only: {summary['mean_minilm_only']:.1f}")
    print(f"    SPECTER2 only: {summary['mean_specter2_only']:.1f}")
    print(f"    Union (TF-IDF+MiniLM): {summary['mean_union_2']:.1f}")
    print(f"    Union (all three): {summary['mean_union_3']:.1f}")
    print(f"  Held-out paper recovery in candidate pools:")
    print(f"    TF-IDF-only held-out: {summary['total_tfidf_only_held_out']}")
    print(f"    SPECTER2-only held-out: {summary['total_specter2_only_held_out']}")
    print(f"    TF-IDF total: {summary['total_tfidf_held_out']}")
    print(f"    MiniLM total: {summary['total_minilm_held_out']}")
    print(f"    SPECTER2 total: {summary['total_specter2_held_out']}")

    return {"summary": summary, "per_evaluation": pool_stats}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.perf_counter()
    print("=" * 70)
    print("W3.4: Asymmetric Pipeline Comparison -- Retrieve + Re-rank")
    print("=" * 70)

    # ----- Load data -----
    print("\n--- Loading data ---")
    from harness import StrategyProfiler

    profiler = StrategyProfiler.from_spike_data(
        db_path=str(DB_PATH),
        minilm_emb_path=str(MINILM_EMB_PATH),
        minilm_ids_path=str(MINILM_IDS_PATH),
        profiles_path=str(PROFILES_PATH),
        specter2_emb_path=str(SPECTER2_EMB_PATH),
        specter2_ids_path=str(SPECTER2_IDS_PATH),
    )

    paper_ids = profiler.paper_ids
    minilm_id_to_idx = profiler.id_to_idx
    specter2_id_to_idx = profiler.specter2_id_to_idx

    # Load abstracts for TF-IDF
    print("\nLoading abstracts for TF-IDF...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
    abstract_map = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    abstracts = [abstract_map.get(pid, "") for pid in paper_ids]

    # Build TF-IDF matrix
    from sklearn.feature_extraction.text import TfidfVectorizer

    print("Building TF-IDF matrix (max_features=50000)...")
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    print(f"  TF-IDF: {tfidf_matrix.shape}, built in {time.perf_counter()-t0:.1f}s")

    # ----- Build pipelines -----
    print("\n--- Building pipeline strategies ---")
    pipelines = build_pipelines(
        minilm_embeddings=profiler.embeddings,
        specter2_embeddings=profiler.specter2_embeddings,
        tfidf_matrix=tfidf_matrix,
        paper_ids=paper_ids,
        minilm_id_to_idx=minilm_id_to_idx,
        specter2_id_to_idx=specter2_id_to_idx,
    )

    for pid, (strat, config) in pipelines.items():
        print(f"  {pid}: {strat.name}")

    # ----- Also build S1a baseline for direct comparison -----
    print("\n--- Building S1a baseline ---")
    from harness.strategy_protocol import SimpleStrategy

    def s1a_score_fn(seed_ids):
        seed_indices = [minilm_id_to_idx[sid] for sid in seed_ids if sid in minilm_id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = profiler.embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return profiler.embeddings @ centroid

    s1a_baseline = SimpleStrategy(
        name="MiniLM centroid (baseline)",
        strategy_id="S1a",
        score_fn=s1a_score_fn,
        paper_ids=paper_ids,
    )

    # ----- Candidate pool analysis (corrected: preserves sort order) -----
    pool_analysis = analyze_candidate_pools(pipelines, profiler)

    # ----- Profile all pipelines -----
    print("\n" + "=" * 70)
    print("PROFILING PIPELINES")
    print("=" * 70)

    pipeline_cards = {}

    # Profile S1a baseline first for fresh comparison
    print(f"\n--- Baseline: S1a (MiniLM centroid) ---")
    t0 = time.perf_counter()
    s1a_card = profiler.profile(
        s1a_baseline,
        config={"type": "baseline", "model": "MiniLM"},
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=50,
    )
    dt = time.perf_counter() - t0
    inst = s1a_card.get("instruments", {})
    mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
    prox = inst.get("seed_proximity", {}).get("mean", 0)
    cov = inst.get("coverage", {}).get("mean", 0)
    nov = inst.get("novelty", {}).get("mean", 0)
    div_ = inst.get("cluster_diversity", {}).get("mean", 0)
    lat = s1a_card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
    print(f"  MRR={mrr:.4f} Prox={prox:.3f} Cov={cov:.3f} Nov={nov:.3f} Div={div_:.1f} p50={lat:.1f}ms [{dt:.1f}s]")
    pipeline_cards["S1a"] = {"card": s1a_card, "profiling_time_s": round(dt, 1)}

    # Profile each pipeline
    for pid in ["P1", "P2", "P3", "P4", "P5", "P6"]:
        strat, config = pipelines[pid]
        print(f"\n--- {pid}: {strat.name} ---")

        t0 = time.perf_counter()
        card = profiler.profile(
            strat,
            config=config,
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=50,
        )
        dt = time.perf_counter() - t0

        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        prox = inst.get("seed_proximity", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)
        lat = card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
        print(f"  MRR={mrr:.4f} Prox={prox:.3f} Cov={cov:.3f} Nov={nov:.3f} Div={div_:.1f} p50={lat:.1f}ms [{dt:.1f}s]")

        pipeline_cards[pid] = {"card": card, "profiling_time_s": round(dt, 1)}

    # ----- Summary table -----
    print("\n" + "=" * 70)
    print("W3.4 SUMMARY: Pipeline Comparison")
    print("=" * 70)

    # Baseline references
    s1a_mrr = pipeline_cards["S1a"]["card"]["instruments"].get(
        "leave_one_out_mrr", {}).get("mean", 0)
    best_rrf_mrr = 0.310  # C2 from W3.1

    header = f"{'ID':<5s} {'Pipeline':<45s} {'MRR':>7s} {'dMRR':>7s} {'Prox':>7s} {'Cover':>7s} {'Nov':>7s} {'Div':>5s} {'p50ms':>7s}"
    print(f"\n{header}")
    print("-" * len(header))

    for pid in ["S1a", "P1", "P2", "P3", "P4", "P5", "P6"]:
        card = pipeline_cards[pid]["card"]
        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        prox = inst.get("seed_proximity", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)
        lat = card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
        delta = mrr - s1a_mrr
        name = card.get("strategy_name", pid)
        marker = " *" if mrr > s1a_mrr else (" !" if mrr < best_rrf_mrr else "")
        print(f"{pid:<5s} {name:<45s} {mrr:7.4f} {delta:+7.4f} {prox:7.3f} {cov:7.3f} {nov:7.3f} {div_:5.1f} {lat:7.1f}{marker}")

    print()
    print(f"  Baseline S1a MRR: {s1a_mrr:.4f}")
    print(f"  Best RRF (C2): {best_rrf_mrr:.4f}")
    print(f"  * = exceeds S1a baseline, ! = worse than best RRF")

    # Per-profile breakdown for top pipeline
    pipeline_mrrs = {
        pid: pipeline_cards[pid]["card"]["instruments"].get(
            "leave_one_out_mrr", {}).get("mean", 0)
        for pid in ["P1", "P2", "P3", "P4", "P5", "P6"]
    }
    best_pipeline = max(pipeline_mrrs, key=lambda k: pipeline_mrrs[k])

    print(f"\n  Best pipeline: {best_pipeline} "
          f"(MRR={pipeline_mrrs[best_pipeline]:.4f})")

    # Per-profile detail for best pipeline + S1a
    print(f"\n  Per-profile MRR comparison ({best_pipeline} vs S1a):")
    best_card = pipeline_cards[best_pipeline]["card"]
    s1a_by_profile = pipeline_cards["S1a"]["card"].get("by_profile", {})
    best_by_profile = best_card.get("by_profile", {})

    for pid in sorted(s1a_by_profile.keys()):
        s1a_prof_mrr = s1a_by_profile[pid].get("instruments", {}).get(
            "leave_one_out_mrr", {}).get("mean", 0)
        best_prof_mrr = best_by_profile.get(pid, {}).get("instruments", {}).get(
            "leave_one_out_mrr", {}).get("mean", 0)
        delta = best_prof_mrr - s1a_prof_mrr if s1a_prof_mrr and best_prof_mrr else 0
        s1a_name = s1a_by_profile[pid].get("profile_name", pid)
        marker = "+" if delta > 0 else "-" if delta < 0 else "="
        print(f"    {pid} ({s1a_name}): S1a={s1a_prof_mrr:.4f}, "
              f"{best_pipeline}={best_prof_mrr:.4f} ({delta:+.4f}) {marker}")

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "metadata": {
            "experiment": "W3.4: Asymmetric Pipeline Comparison",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_time_s": round(total_time, 1),
            "corpus_size": len(paper_ids),
            "n_profiles": len(profiler.profiles),
            "baseline_s1a_mrr_fresh": float(
                pipeline_cards["S1a"]["card"]["instruments"].get(
                    "leave_one_out_mrr", {}).get("mean", 0)
            ),
            "baseline_best_rrf_mrr": best_rrf_mrr,
        },
        "pipeline_cards": {
            pid: {
                "card": data["card"],
                "profiling_time_s": data["profiling_time_s"],
            }
            for pid, data in pipeline_cards.items()
        },
        "pipeline_ranking": {
            "by_mrr": sorted(
                pipeline_mrrs.keys(),
                key=lambda k: pipeline_mrrs[k],
                reverse=True,
            ),
            "mrr_values": {k: round(v, 6) for k, v in pipeline_mrrs.items()},
            "best_pipeline": best_pipeline,
            "best_pipeline_mrr": round(pipeline_mrrs[best_pipeline], 6),
            "beats_s1a": pipeline_mrrs[best_pipeline] > s1a_mrr,
            "beats_rrf": pipeline_mrrs[best_pipeline] > best_rrf_mrr,
        },
        "candidate_pool_analysis": pool_analysis,
    }

    SPIKE_003_DATA.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\n{'='*70}")
    print(f"W3.4 COMPLETE in {total_time:.0f}s ({total_time/60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    main()
