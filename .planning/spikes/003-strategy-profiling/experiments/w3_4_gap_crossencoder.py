"""
W3.4 Gap Fill: Cross-Encoder Reranking Profiling (S4a).

W3.4 tested retrieve+rerank pipelines but only used MiniLM embedding
similarity as the reranker. That produced the "convergence to MiniLM"
pattern: P5/P6 MRR 0.3979 = S1a MRR 0.3979 exactly. MiniLM as reranker
simply re-imposes MiniLM's own ranking, discarding TF-IDF's unique candidates.

Cross-encoders are fundamentally different: they take raw (query, document)
text pairs and produce a relevance score via cross-attention. Unlike bi-encoders
(which compare pre-computed embeddings), cross-encoders can capture fine-grained
query-document interactions.

Key question: Does a cross-encoder reranker VALUE TF-IDF's unique candidates
differently than MiniLM does? If the cross-encoder promotes papers that TF-IDF
found but MiniLM ranked low, the pipeline architecture becomes genuinely useful.

Pipelines tested:
  S4a:  MiniLM retrieve top-50 -> cross-encoder rerank -> top-20
  S4a-union: (TF-IDF top-100 + MiniLM top-100) union -> cross-encoder rerank -> top-20

Compare against:
  S1a:    MiniLM centroid alone (MRR 0.398)
  P5/P6:  Union -> MiniLM rerank (MRR 0.398 -- converged to S1a)

Latency profiling:
  Time per candidate pair across batch sizes (50, 100, 200)
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
OUTPUT_PATH = SPIKE_003_DATA / "w3_4_gap_crossencoder_profiles.json"


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
# Cross-Encoder Reranker
# ---------------------------------------------------------------------------

class CrossEncoderReranker:
    """Cross-encoder reranker using sentence-transformers CrossEncoder.

    Unlike embedding-based rerankers that compare pre-computed vectors,
    the cross-encoder takes raw (query_text, document_text) pairs and
    produces a relevance score via cross-attention. This means it can
    capture fine-grained query-document interactions that bi-encoders miss.

    For multi-seed evaluation: concatenate top-3 seed paper titles as the
    query string (abstracts are too long for 512 token limit).
    """

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2",
                 batch_size: int = 64, max_length: int = 512):
        from sentence_transformers import CrossEncoder

        print(f"  Loading cross-encoder: {model_name}")
        t0 = time.perf_counter()
        self.model = CrossEncoder(model_name)
        self.model_name = model_name
        self.batch_size = batch_size
        self.max_length = max_length
        self._load_time = time.perf_counter() - t0
        print(f"  Cross-encoder loaded in {self._load_time:.1f}s")

    def build_query(self, seed_ids: list[str], title_map: dict[str, str]) -> str:
        """Build query string from seed paper titles.

        Uses top-3 seed titles concatenated with ' | ' separator.
        Titles are short (~20-30 tokens each), so 3 titles is ~90 tokens,
        leaving ~420 tokens for the candidate abstract.
        """
        titles = [title_map.get(sid, "") for sid in seed_ids[:3]]
        return " | ".join(t for t in titles if t)

    def rerank(self, candidate_ids: list[str], seed_ids: list[str],
               title_map: dict[str, str], abstract_map: dict[str, str]
               ) -> list[tuple[str, float]]:
        """Rerank candidates using cross-encoder scores.

        Args:
            candidate_ids: Paper IDs to score.
            seed_ids: Seed paper IDs (used to build query).
            title_map: arxiv_id -> title mapping.
            abstract_map: arxiv_id -> abstract mapping.

        Returns:
            List of (arxiv_id, score) sorted by score descending.
        """
        query = self.build_query(seed_ids, title_map)
        if not query:
            return [(pid, 0.0) for pid in candidate_ids]

        # Build (query, document) pairs
        pairs = []
        valid_ids = []
        for pid in candidate_ids:
            abstract = abstract_map.get(pid, "")
            if abstract:
                pairs.append((query, abstract))
                valid_ids.append(pid)
            # Papers without abstracts get score 0

        if not pairs:
            return [(pid, 0.0) for pid in candidate_ids]

        # Score in batches
        scores = self.model.predict(
            pairs,
            batch_size=self.batch_size,
            show_progress_bar=False,
        )

        # Build scored list
        scored = [(pid, float(s)) for pid, s in zip(valid_ids, scores)]

        # Add papers without abstracts at score 0
        scored_set = set(valid_ids)
        for pid in candidate_ids:
            if pid not in scored_set:
                scored.append((pid, 0.0))

        scored.sort(key=lambda x: -x[1])
        return scored


# ---------------------------------------------------------------------------
# CrossEncoderPipelineStrategy: retrieve + cross-encoder rerank
# ---------------------------------------------------------------------------

class CrossEncoderPipelineStrategy:
    """Pipeline: embedding retrieval -> cross-encoder reranking.

    This is the key architectural test: can a cross-encoder reranker
    break the "convergence to MiniLM" pattern by valuing candidates
    differently than MiniLM's embedding similarity?
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        retriever_fn,
        reranker: CrossEncoderReranker,
        paper_ids: list[str],
        title_map: dict[str, str],
        abstract_map: dict[str, str],
        retrieve_k: int = 50,
    ):
        self._name = name
        self._strategy_id = strategy_id
        self._retriever_fn = retriever_fn
        self._reranker = reranker
        self._paper_ids = paper_ids
        self._title_map = title_map
        self._abstract_map = abstract_map
        self._retrieve_k = retrieve_k

    @property
    def name(self):
        return self._name

    @property
    def strategy_id(self):
        return self._strategy_id

    def recommend(self, seed_arxiv_ids: list[str], top_k: int = 20) -> list[tuple[str, float]]:
        """Retrieve candidates, then cross-encoder rerank."""
        seed_set = set(seed_arxiv_ids)

        # Step 1: Retrieve candidates
        retriever_results = self._retriever_fn(seed_arxiv_ids)
        candidates = [
            (pid, score) for pid, score in retriever_results
            if pid not in seed_set
        ][:self._retrieve_k]

        if not candidates:
            return []

        candidate_ids = [pid for pid, _ in candidates]

        # Step 2: Cross-encoder rerank
        reranked = self._reranker.rerank(
            candidate_ids, seed_arxiv_ids,
            self._title_map, self._abstract_map,
        )

        return reranked[:top_k]


class CrossEncoderUnionPipelineStrategy:
    """Union of multiple retrievers -> cross-encoder reranking.

    Tests whether the cross-encoder can rescue TF-IDF's unique candidates
    that MiniLM's embedding reranker discards.
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        retriever_fns: list,
        reranker: CrossEncoderReranker,
        paper_ids: list[str],
        title_map: dict[str, str],
        abstract_map: dict[str, str],
        retrieve_k_each: int = 100,
    ):
        self._name = name
        self._strategy_id = strategy_id
        self._retriever_fns = retriever_fns
        self._reranker = reranker
        self._paper_ids = paper_ids
        self._title_map = title_map
        self._abstract_map = abstract_map
        self._retrieve_k_each = retrieve_k_each

    @property
    def name(self):
        return self._name

    @property
    def strategy_id(self):
        return self._strategy_id

    def recommend(self, seed_arxiv_ids: list[str], top_k: int = 20) -> list[tuple[str, float]]:
        """Union of retriever candidates, then cross-encoder rerank."""
        seed_set = set(seed_arxiv_ids)

        # Step 1: Union of retriever candidates
        all_candidates = set()
        for retriever_fn in self._retriever_fns:
            results = retriever_fn(seed_arxiv_ids)
            non_seed = [(pid, s) for pid, s in results if pid not in seed_set]
            for pid, _ in non_seed[:self._retrieve_k_each]:
                all_candidates.add(pid)

        if not all_candidates:
            return []

        candidate_ids = sorted(all_candidates)  # Deterministic order

        # Step 2: Cross-encoder rerank the union
        reranked = self._reranker.rerank(
            candidate_ids, seed_arxiv_ids,
            self._title_map, self._abstract_map,
        )
        return reranked[:top_k]


# ---------------------------------------------------------------------------
# Scoring functions (reused from w3_4_pipelines.py)
# ---------------------------------------------------------------------------

def build_embedding_scorer(embeddings, paper_ids, id_to_idx):
    """Return a function: (seed_ids) -> list[(arxiv_id, score)] sorted desc."""
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
    """Return a function: (seed_ids) -> list[(arxiv_id, score)] sorted desc."""
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
    """Return a function: (candidate_ids, seed_ids) -> list[(arxiv_id, score)] sorted desc."""
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


# ---------------------------------------------------------------------------
# Latency profiling
# ---------------------------------------------------------------------------

def profile_crossencoder_latency(reranker: CrossEncoderReranker,
                                  title_map: dict, abstract_map: dict,
                                  sample_ids: list[str],
                                  sample_seed_ids: list[str]) -> dict:
    """Profile cross-encoder latency across batch sizes.

    Measures time per candidate pair for 50, 100, 200 candidate pools.
    This determines whether cross-encoder is viable as real-time reranker
    or only as a batch process.
    """
    print("\n--- Cross-Encoder Latency Profiling ---")

    results = {}
    n_warmup = 2
    n_runs = 5  # Fewer runs since cross-encoder is expensive

    for pool_size in [50, 100, 200]:
        candidates = sample_ids[:pool_size]

        # Warmup
        for _ in range(n_warmup):
            reranker.rerank(candidates, sample_seed_ids, title_map, abstract_map)

        # Timed runs
        times = []
        for _ in range(n_runs):
            t0 = time.perf_counter()
            reranker.rerank(candidates, sample_seed_ids, title_map, abstract_map)
            dt = (time.perf_counter() - t0) * 1000  # ms
            times.append(dt)

        per_candidate = [t / pool_size for t in times]
        results[f"pool_{pool_size}"] = {
            "total_ms": {
                "mean": float(np.mean(times)),
                "std": float(np.std(times)),
                "min": float(np.min(times)),
                "max": float(np.max(times)),
                "p50": float(np.median(times)),
            },
            "per_candidate_ms": {
                "mean": float(np.mean(per_candidate)),
                "std": float(np.std(per_candidate)),
                "p50": float(np.median(per_candidate)),
            },
            "pool_size": pool_size,
            "n_runs": n_runs,
        }

        total_p50 = np.median(times)
        per_cand_p50 = np.median(per_candidate)
        print(f"  Pool {pool_size}: total_p50={total_p50:.0f}ms, "
              f"per_candidate_p50={per_cand_p50:.1f}ms")

    # Also measure MiniLM reranking for comparison
    print("\n  MiniLM reranking comparison:")
    # We'll measure this in main() where we have embeddings loaded

    return results


def profile_minilm_reranker_latency(reranker_fn, sample_candidates: list[str],
                                     sample_seeds: list[str]) -> dict:
    """Profile MiniLM embedding reranker latency for comparison."""
    results = {}
    n_warmup = 5
    n_runs = 20

    for pool_size in [50, 100, 200]:
        candidates = sample_candidates[:pool_size]

        for _ in range(n_warmup):
            reranker_fn(candidates, sample_seeds)

        times = []
        for _ in range(n_runs):
            t0 = time.perf_counter()
            reranker_fn(candidates, sample_seeds)
            dt = (time.perf_counter() - t0) * 1000
            times.append(dt)

        per_candidate = [t / pool_size for t in times]
        results[f"pool_{pool_size}"] = {
            "total_ms": {
                "mean": float(np.mean(times)),
                "p50": float(np.median(times)),
            },
            "per_candidate_ms": {
                "mean": float(np.mean(per_candidate)),
                "p50": float(np.median(per_candidate)),
            },
            "pool_size": pool_size,
        }
        print(f"  MiniLM pool {pool_size}: total_p50={np.median(times):.1f}ms, "
              f"per_candidate_p50={np.median(per_candidate):.2f}ms")

    return results


# ---------------------------------------------------------------------------
# Divergence analysis: does cross-encoder break the MiniLM convergence?
# ---------------------------------------------------------------------------

def analyze_reranker_divergence(
    ce_strategy,
    minilm_strategy,
    s1a_baseline,
    profiler,
    title_map: dict,
    abstract_map: dict,
) -> dict:
    """Analyze how cross-encoder reranking diverges from MiniLM reranking.

    For each profile x seed_set, compare:
    1. Cross-encoder top-20 vs MiniLM-reranked top-20 (Jaccard overlap)
    2. Cross-encoder top-20 vs S1a top-20 (does CE break convergence?)
    3. Papers that cross-encoder promotes from TF-IDF's unique candidates
    4. Rank correlation between cross-encoder and MiniLM scores
    """
    print("\n" + "=" * 70)
    print("RERANKER DIVERGENCE ANALYSIS")
    print("=" * 70)

    profiles = profiler.profiles
    divergence_stats = []

    for prof in profiles:
        for si, seed_set in enumerate(prof.seed_sets):
            # Get recommendations from each strategy
            ce_recs = ce_strategy.recommend(seed_set, top_k=20)
            s1a_recs = s1a_baseline.recommend(seed_set, top_k=20)

            ce_ids = set(r[0] for r in ce_recs)
            s1a_ids = set(r[0] for r in s1a_recs)

            # Jaccard overlap
            intersection = ce_ids & s1a_ids
            union = ce_ids | s1a_ids
            jaccard = len(intersection) / len(union) if union else 0

            # How many of CE's top-20 are NOT in S1a's top-20?
            ce_unique = ce_ids - s1a_ids

            # Check if CE-unique papers are in held-out set
            held_out_set = set(prof.held_out)
            ce_unique_held_out = ce_unique & held_out_set
            s1a_held_out = s1a_ids & held_out_set

            # Rank correlation of shared papers
            ce_rank = {r[0]: i for i, r in enumerate(ce_recs)}
            s1a_rank = {r[0]: i for i, r in enumerate(s1a_recs)}
            shared = ce_ids & s1a_ids
            if len(shared) >= 3:
                shared_list = sorted(shared)
                ce_ranks = [ce_rank[p] for p in shared_list]
                s1a_ranks = [s1a_rank[p] for p in shared_list]
                # Spearman rank correlation
                from scipy.stats import spearmanr
                rho, _ = spearmanr(ce_ranks, s1a_ranks)
            else:
                rho = None

            stat = {
                "profile_id": prof.profile_id,
                "seed_set": si,
                "jaccard_ce_vs_s1a": round(jaccard, 4),
                "ce_unique_count": len(ce_unique),
                "ce_unique_in_held_out": len(ce_unique_held_out),
                "s1a_held_out_count": len(s1a_held_out),
                "shared_count": len(shared),
                "rank_correlation": round(rho, 4) if rho is not None else None,
            }
            divergence_stats.append(stat)

            if si == 0:  # Print first seed set per profile
                print(f"  {prof.profile_id} ({prof.name}): "
                      f"Jaccard={jaccard:.3f}, CE_unique={len(ce_unique)}, "
                      f"CE_held_out={len(ce_unique_held_out)}, "
                      f"rho={rho:.3f}" if rho is not None else
                      f"  {prof.profile_id} ({prof.name}): "
                      f"Jaccard={jaccard:.3f}, CE_unique={len(ce_unique)}, "
                      f"CE_held_out={len(ce_unique_held_out)}")

    # Aggregate
    n = len(divergence_stats)
    mean_jaccard = sum(s["jaccard_ce_vs_s1a"] for s in divergence_stats) / n
    mean_ce_unique = sum(s["ce_unique_count"] for s in divergence_stats) / n
    total_ce_held_out = sum(s["ce_unique_in_held_out"] for s in divergence_stats)
    total_s1a_held_out = sum(s["s1a_held_out_count"] for s in divergence_stats)
    rhos = [s["rank_correlation"] for s in divergence_stats if s["rank_correlation"] is not None]
    mean_rho = sum(rhos) / len(rhos) if rhos else None

    summary = {
        "mean_jaccard_ce_vs_s1a": round(mean_jaccard, 4),
        "mean_ce_unique_in_top20": round(mean_ce_unique, 1),
        "total_ce_unique_held_out_recoveries": total_ce_held_out,
        "total_s1a_held_out_recoveries": total_s1a_held_out,
        "mean_rank_correlation": round(mean_rho, 4) if mean_rho is not None else None,
        "n_evaluations": n,
        "convergence_broken": mean_jaccard < 0.9,  # If < 90% overlap, CE diverges
    }

    print(f"\n  Summary ({n} evaluations):")
    print(f"    Mean Jaccard (CE vs S1a): {mean_jaccard:.4f}")
    print(f"    Mean CE-unique papers: {mean_ce_unique:.1f}/20")
    print(f"    Total CE-unique held-out recoveries: {total_ce_held_out}")
    print(f"    Total S1a held-out recoveries: {total_s1a_held_out}")
    print(f"    Mean rank correlation: {mean_rho:.4f}" if mean_rho else "    Mean rank correlation: N/A")
    print(f"    Convergence broken: {summary['convergence_broken']}")

    return {"summary": summary, "per_evaluation": divergence_stats}


# ---------------------------------------------------------------------------
# TF-IDF candidate rescue analysis
# ---------------------------------------------------------------------------

def analyze_tfidf_rescue(
    ce_union_strategy,
    s1a_baseline,
    tfidf_scorer,
    minilm_scorer,
    profiler,
) -> dict:
    """Analyze whether cross-encoder rescues TF-IDF's unique candidates.

    The core question: does the cross-encoder promote papers that TF-IDF
    found (but MiniLM ranked low) into the top-20?

    For each evaluation:
    1. Identify TF-IDF-unique candidates (in TF-IDF top-100 but not MiniLM top-100)
    2. Check how many of these TF-IDF-unique candidates appear in CE top-20
    3. Compare against how many appear in MiniLM-reranked top-20 (should be ~0)
    """
    print("\n" + "=" * 70)
    print("TF-IDF CANDIDATE RESCUE ANALYSIS")
    print("=" * 70)

    profiles = profiler.profiles
    rescue_stats = []

    for prof in profiles:
        for si, seed_set in enumerate(prof.seed_sets):
            seed_set_set = set(seed_set)

            # TF-IDF top-100 (non-seed)
            tfidf_results = tfidf_scorer(seed_set)
            tfidf_non_seed = [
                (pid, s) for pid, s in tfidf_results if pid not in seed_set_set
            ]
            tfidf_top100 = set(pid for pid, _ in tfidf_non_seed[:100])

            # MiniLM top-100 (non-seed)
            minilm_results = minilm_scorer(seed_set)
            minilm_non_seed = [
                (pid, s) for pid, s in minilm_results if pid not in seed_set_set
            ]
            minilm_top100 = set(pid for pid, _ in minilm_non_seed[:100])

            # TF-IDF-unique candidates
            tfidf_unique = tfidf_top100 - minilm_top100

            # Cross-encoder union top-20
            ce_recs = ce_union_strategy.recommend(seed_set, top_k=20)
            ce_top20 = set(r[0] for r in ce_recs)

            # S1a top-20
            s1a_recs = s1a_baseline.recommend(seed_set, top_k=20)
            s1a_top20 = set(r[0] for r in s1a_recs)

            # How many TF-IDF-unique candidates did CE promote to top-20?
            rescued_by_ce = tfidf_unique & ce_top20
            rescued_by_s1a = tfidf_unique & s1a_top20  # Should be ~0

            # Check held-out
            held_out_set = set(prof.held_out)
            rescued_held_out = rescued_by_ce & held_out_set

            stat = {
                "profile_id": prof.profile_id,
                "seed_set": si,
                "tfidf_unique_count": len(tfidf_unique),
                "rescued_by_ce": len(rescued_by_ce),
                "rescued_by_s1a": len(rescued_by_s1a),
                "rescued_held_out": len(rescued_held_out),
            }
            rescue_stats.append(stat)

    # Aggregate
    n = len(rescue_stats)
    total_tfidf_unique = sum(s["tfidf_unique_count"] for s in rescue_stats)
    total_rescued_ce = sum(s["rescued_by_ce"] for s in rescue_stats)
    total_rescued_s1a = sum(s["rescued_by_s1a"] for s in rescue_stats)
    total_rescued_held_out = sum(s["rescued_held_out"] for s in rescue_stats)

    summary = {
        "total_tfidf_unique_candidates": total_tfidf_unique,
        "total_rescued_by_ce": total_rescued_ce,
        "total_rescued_by_s1a": total_rescued_s1a,
        "total_rescued_held_out": total_rescued_held_out,
        "rescue_rate": round(total_rescued_ce / total_tfidf_unique, 4) if total_tfidf_unique > 0 else 0,
        "n_evaluations": n,
    }

    print(f"  {n} evaluations:")
    print(f"    Total TF-IDF-unique candidates: {total_tfidf_unique}")
    print(f"    Rescued by cross-encoder to top-20: {total_rescued_ce}")
    print(f"    Rescued by S1a to top-20: {total_rescued_s1a}")
    print(f"    Rescued into top-20 AND held-out: {total_rescued_held_out}")
    print(f"    Rescue rate: {summary['rescue_rate']:.4f}")

    return {"summary": summary, "per_evaluation": rescue_stats}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.perf_counter()
    print("=" * 70)
    print("W3.4 Gap Fill: Cross-Encoder Reranking Profiling (S4a)")
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

    # Load abstracts and titles
    print("\nLoading abstracts and titles...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, title, abstract FROM papers")
    title_map = {}
    abstract_map = {}
    for row in cursor.fetchall():
        title_map[row[0]] = row[1]
        abstract_map[row[0]] = row[2]
    conn.close()
    print(f"  {len(title_map)} titles, {len(abstract_map)} abstracts loaded")

    # Build TF-IDF matrix
    from sklearn.feature_extraction.text import TfidfVectorizer

    abstracts_list = [abstract_map.get(pid, "") for pid in paper_ids]
    print("Building TF-IDF matrix (max_features=50000)...")
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts_list)
    print(f"  TF-IDF: {tfidf_matrix.shape}, built in {time.perf_counter()-t0:.1f}s")

    # ----- Build scoring primitives -----
    print("\n--- Building scoring primitives ---")
    minilm_scorer = build_embedding_scorer(profiler.embeddings, paper_ids, minilm_id_to_idx)
    tfidf_scorer = build_tfidf_scorer(tfidf_matrix, paper_ids, minilm_id_to_idx)
    minilm_reranker_fn = build_embedding_reranker(profiler.embeddings, minilm_id_to_idx)

    # ----- Initialize cross-encoder -----
    print("\n--- Initializing cross-encoder ---")
    ce_reranker = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        batch_size=64,
    )

    # ----- Build strategies -----
    print("\n--- Building strategies ---")

    # S4a: MiniLM retrieve top-50 -> cross-encoder rerank
    s4a = CrossEncoderPipelineStrategy(
        name="MiniLM->CrossEncoder (k=50)",
        strategy_id="S4a",
        retriever_fn=minilm_scorer,
        reranker=ce_reranker,
        paper_ids=paper_ids,
        title_map=title_map,
        abstract_map=abstract_map,
        retrieve_k=50,
    )

    # S4a-union: (TF-IDF top-100 + MiniLM top-100) union -> cross-encoder rerank
    s4a_union = CrossEncoderUnionPipelineStrategy(
        name="(TF-IDF+MiniLM)->CrossEncoder (k=100 each)",
        strategy_id="S4a-union",
        retriever_fns=[tfidf_scorer, minilm_scorer],
        reranker=ce_reranker,
        paper_ids=paper_ids,
        title_map=title_map,
        abstract_map=abstract_map,
        retrieve_k_each=100,
    )

    # S1a baseline for comparison
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

    # P5 clone for comparison: Union -> MiniLM rerank (the convergent pipeline)
    from w3_4_pipelines import UnionPipelineStrategy
    p5_clone = UnionPipelineStrategy(
        name="(TF-IDF+MiniLM)->MiniLM (k=100 each)",
        strategy_id="P5",
        retriever_fns=[tfidf_scorer, minilm_scorer],
        ranker_fn=minilm_reranker_fn,
        paper_ids=paper_ids,
        retrieve_k_each=100,
    )

    # ----- Latency profiling -----
    # Get sample candidates for latency tests
    sample_seeds = profiler.profiles[0].seed_sets[0]
    seed_set_set = set(sample_seeds)
    sample_results = minilm_scorer(sample_seeds)
    sample_candidates = [pid for pid, _ in sample_results if pid not in seed_set_set][:200]

    ce_latency = profile_crossencoder_latency(
        ce_reranker, title_map, abstract_map,
        sample_candidates, sample_seeds,
    )

    print("\n  MiniLM embedding reranker comparison:")
    minilm_latency = profile_minilm_reranker_latency(
        minilm_reranker_fn, sample_candidates, sample_seeds,
    )

    # ----- Profile strategies with full harness -----
    print("\n" + "=" * 70)
    print("PROFILING CROSS-ENCODER STRATEGIES")
    print("=" * 70)

    strategy_cards = {}

    # Profile S1a baseline
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
    cov = inst.get("coverage", {}).get("mean", 0)
    lat = s1a_card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
    print(f"  MRR={mrr:.4f} Coverage={cov:.3f} p50={lat:.1f}ms [{dt:.1f}s]")
    strategy_cards["S1a"] = {"card": s1a_card, "profiling_time_s": round(dt, 1)}

    # Profile S4a: MiniLM -> CrossEncoder
    print(f"\n--- S4a: MiniLM->CrossEncoder (k=50) ---")
    t0 = time.perf_counter()
    s4a_card = profiler.profile(
        s4a,
        config={
            "retriever": "S1a (MiniLM centroid)",
            "ranker": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "retrieve_k": 50,
            "architecture": "retrieve-crossencoder-rerank",
        },
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=10,  # Fewer runs since CE is slow
    )
    dt = time.perf_counter() - t0
    inst = s4a_card.get("instruments", {})
    mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
    cov = inst.get("coverage", {}).get("mean", 0)
    lat = s4a_card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
    print(f"  MRR={mrr:.4f} Coverage={cov:.3f} p50={lat:.1f}ms [{dt:.1f}s]")
    strategy_cards["S4a"] = {"card": s4a_card, "profiling_time_s": round(dt, 1)}

    # Profile S4a-union: (TF-IDF+MiniLM) -> CrossEncoder
    print(f"\n--- S4a-union: (TF-IDF+MiniLM)->CrossEncoder (k=100 each) ---")
    t0 = time.perf_counter()
    s4a_union_card = profiler.profile(
        s4a_union,
        config={
            "retrievers": ["S1d (TF-IDF)", "S1a (MiniLM)"],
            "ranker": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "retrieve_k_each": 100,
            "architecture": "union-crossencoder-rerank",
        },
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=5,  # Even fewer -- union pool is large
    )
    dt = time.perf_counter() - t0
    inst = s4a_union_card.get("instruments", {})
    mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
    cov = inst.get("coverage", {}).get("mean", 0)
    lat = s4a_union_card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
    print(f"  MRR={mrr:.4f} Coverage={cov:.3f} p50={lat:.1f}ms [{dt:.1f}s]")
    strategy_cards["S4a-union"] = {"card": s4a_union_card, "profiling_time_s": round(dt, 1)}

    # Profile P5 for fresh MiniLM-rerank comparison
    print(f"\n--- P5: (TF-IDF+MiniLM)->MiniLM (convergent baseline) ---")
    t0 = time.perf_counter()
    p5_card = profiler.profile(
        p5_clone,
        config={
            "retrievers": ["S1d (TF-IDF)", "S1a (MiniLM)"],
            "ranker": "S1a (MiniLM centroid)",
            "retrieve_k_each": 100,
            "architecture": "union-embedding-rerank",
        },
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=50,
    )
    dt = time.perf_counter() - t0
    inst = p5_card.get("instruments", {})
    mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
    cov = inst.get("coverage", {}).get("mean", 0)
    lat = p5_card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
    print(f"  MRR={mrr:.4f} Coverage={cov:.3f} p50={lat:.1f}ms [{dt:.1f}s]")
    strategy_cards["P5"] = {"card": p5_card, "profiling_time_s": round(dt, 1)}

    # ----- Divergence analysis -----
    divergence = analyze_reranker_divergence(
        ce_strategy=s4a_union,
        minilm_strategy=p5_clone,
        s1a_baseline=s1a_baseline,
        profiler=profiler,
        title_map=title_map,
        abstract_map=abstract_map,
    )

    # ----- TF-IDF rescue analysis -----
    rescue = analyze_tfidf_rescue(
        ce_union_strategy=s4a_union,
        s1a_baseline=s1a_baseline,
        tfidf_scorer=tfidf_scorer,
        minilm_scorer=minilm_scorer,
        profiler=profiler,
    )

    # ----- Summary table -----
    print("\n" + "=" * 70)
    print("W3.4 GAP FILL SUMMARY: Cross-Encoder vs MiniLM Reranking")
    print("=" * 70)

    s1a_mrr = strategy_cards["S1a"]["card"]["instruments"].get(
        "leave_one_out_mrr", {}).get("mean", 0)

    header = (f"{'ID':<12s} {'Pipeline':<50s} {'MRR':>7s} {'dMRR':>7s} "
              f"{'Cover':>7s} {'Nov':>7s} {'Div':>5s} {'p50ms':>7s}")
    print(f"\n{header}")
    print("-" * len(header))

    for sid in ["S1a", "P5", "S4a", "S4a-union"]:
        card = strategy_cards[sid]["card"]
        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)
        lat = card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
        delta = mrr - s1a_mrr
        name = card.get("strategy_name", sid)
        marker = " *" if mrr > s1a_mrr else (" !" if mrr < s1a_mrr * 0.9 else "")
        print(f"{sid:<12s} {name:<50s} {mrr:7.4f} {delta:+7.4f} "
              f"{cov:7.3f} {nov:7.3f} {div_:5.1f} {lat:7.1f}{marker}")

    print()
    print(f"  Baseline S1a MRR: {s1a_mrr:.4f}")
    print(f"  * = exceeds S1a, ! = >10% below S1a")

    # Per-profile breakdown for S4a-union vs S1a
    print(f"\n  Per-profile MRR comparison (S4a-union vs S1a vs P5):")
    s1a_by_profile = strategy_cards["S1a"]["card"].get("by_profile", {})
    s4au_by_profile = strategy_cards["S4a-union"]["card"].get("by_profile", {})
    p5_by_profile = strategy_cards["P5"]["card"].get("by_profile", {})

    for pid in sorted(s1a_by_profile.keys()):
        s1a_prof_mrr = s1a_by_profile[pid].get("instruments", {}).get(
            "leave_one_out_mrr", {}).get("mean", 0)
        s4au_prof_mrr = s4au_by_profile.get(pid, {}).get("instruments", {}).get(
            "leave_one_out_mrr", {}).get("mean", 0)
        p5_prof_mrr = p5_by_profile.get(pid, {}).get("instruments", {}).get(
            "leave_one_out_mrr", {}).get("mean", 0)
        delta = s4au_prof_mrr - s1a_prof_mrr
        name = s1a_by_profile[pid].get("profile_name", pid)
        marker = "+" if delta > 0.01 else "-" if delta < -0.01 else "="
        print(f"    {pid} ({name}): S1a={s1a_prof_mrr:.4f}, "
              f"P5={p5_prof_mrr:.4f}, "
              f"S4a-union={s4au_prof_mrr:.4f} ({delta:+.4f}) {marker}")

    # Latency comparison summary
    print(f"\n  Latency comparison (rerank only, p50):")
    for pool_size in [50, 100, 200]:
        ce_lat = ce_latency[f"pool_{pool_size}"]["total_ms"]["p50"]
        ml_lat = minilm_latency[f"pool_{pool_size}"]["total_ms"]["p50"]
        ratio = ce_lat / ml_lat if ml_lat > 0 else float("inf")
        print(f"    Pool {pool_size}: CE={ce_lat:.0f}ms, MiniLM={ml_lat:.1f}ms, "
              f"ratio={ratio:.0f}x")

    # ----- Save results -----
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "metadata": {
            "experiment": "W3.4 Gap Fill: Cross-Encoder Reranking (S4a)",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_time_s": round(total_time, 1),
            "corpus_size": len(paper_ids),
            "n_profiles": len(profiler.profiles),
            "cross_encoder_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "cross_encoder_max_length": 512,
            "cross_encoder_load_time_s": round(ce_reranker._load_time, 2),
            "baseline_s1a_mrr": float(s1a_mrr),
        },
        "strategy_cards": {
            sid: {
                "card": data["card"],
                "profiling_time_s": data["profiling_time_s"],
            }
            for sid, data in strategy_cards.items()
        },
        "latency_profiling": {
            "cross_encoder": ce_latency,
            "minilm_reranker": minilm_latency,
        },
        "divergence_analysis": divergence,
        "tfidf_rescue_analysis": rescue,
    }

    SPIKE_003_DATA.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\n{'='*70}")
    print(f"W3.4 GAP FILL COMPLETE in {total_time:.0f}s ({total_time/60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    main()
