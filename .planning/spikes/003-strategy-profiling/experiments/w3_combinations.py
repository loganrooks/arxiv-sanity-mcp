"""
W3: Combination and Pipeline Profiling.

Tests strategy combinations to exploit complementarity discovered in W1 qualitative review:
  - MiniLM (semantic precision) + TF-IDF (keyword precision / held-out recall)
  - MiniLM + SPECTER2 (cross-field discovery)
  - TF-IDF + SPECTER2
  - All three content strategies
  - MiniLM + category filter (S2a) and co-author (S2f)

Sub-experiments:
  W3.1: Pairwise combination screening via RRF (k=60)
  W3.2: RRF k-parameter sensitivity for top 2 combos
  W3.3: Weighted combination exploration for top 2 combos
  W3.5: Marginal signal value (incremental addition from MiniLM base)
  W3.6: Consensus validation (overlap analysis for MiniLM+TF-IDF)

Key context from W1 qualitative review:
  - MiniLM's MRR dominance is partially circular (LOO clusters from MiniLM embeddings)
  - TF-IDF is underrated: best held-out paper recovery (5/15) despite worst MRR (0.104)
  - SPECTER2 has catastrophic score compression (spread 0.009) -- must use rank-based fusion
  - Strategies are complementary, not ranked
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from collections import Counter, defaultdict
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
OUTPUT_PATH = SPIKE_003_DATA / "w3_combination_profiles.json"


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
# Combination methods
# ---------------------------------------------------------------------------

def rrf_combine(rankings_list: list[list[tuple[str, float]]], k: int = 60) -> list[tuple[str, float]]:
    """Combine multiple ranked lists via Reciprocal Rank Fusion.

    RRF score for paper p = sum_i(1 / (k + rank_i(p)))

    This is rank-based, not score-based, making it robust to score compression
    (critical for SPECTER2 whose score spread is only 0.009).

    Args:
        rankings_list: List of ranked lists, each [(paper_id, score), ...] in descending score order.
        k: RRF constant. Higher k reduces the influence of top ranks.

    Returns:
        Combined ranked list [(paper_id, rrf_score), ...] in descending score order.
    """
    scores = {}
    for rankings in rankings_list:
        # Sort by score descending to get proper ranks
        sorted_rankings = sorted(rankings, key=lambda x: -x[1])
        for rank, (pid, _) in enumerate(sorted_rankings):
            scores[pid] = scores.get(pid, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: -x[1])


def weighted_combine(
    rankings_list: list[list[tuple[str, float]]],
    weights: list[float],
) -> list[tuple[str, float]]:
    """Combine multiple ranked lists with explicit weights and min-max normalization.

    Each strategy's scores are normalized to [0,1] before weighting.
    This is score-based, so it is sensitive to score distribution shape.
    NOT suitable for SPECTER2 (score compression makes normalization degenerate).

    Args:
        rankings_list: List of ranked lists, each [(paper_id, score), ...].
        weights: Weight per strategy. Need not sum to 1.

    Returns:
        Combined ranked list [(paper_id, weighted_score), ...] in descending score order.
    """
    scores = {}
    for rankings, w in zip(rankings_list, weights):
        if not rankings:
            continue
        all_scores = [s for _, s in rankings]
        max_s = max(all_scores)
        min_s = min(all_scores)
        range_s = max_s - min_s if max_s != min_s else 1.0
        for pid, s in rankings:
            norm_s = (s - min_s) / range_s
            scores[pid] = scores.get(pid, 0.0) + w * norm_s
    return sorted(scores.items(), key=lambda x: -x[1])


# ---------------------------------------------------------------------------
# Strategy builders (reuse from W1A/W1B patterns)
# ---------------------------------------------------------------------------

def make_embedding_strategy(embeddings, paper_ids, id_to_idx, name, strategy_id):
    """Build embedding centroid similarity strategy."""
    from harness.strategy_protocol import SimpleStrategy

    def score_fn(seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return embeddings @ centroid

    return SimpleStrategy(name=name, strategy_id=strategy_id,
                          score_fn=score_fn, paper_ids=paper_ids)


def make_tfidf_strategy(abstracts, paper_ids, id_to_idx):
    """Build TF-IDF cosine similarity strategy. Returns (strategy, tfidf_matrix)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from harness.strategy_protocol import SimpleStrategy

    print("  Building TF-IDF matrix (max_features=50000)...")
    t0 = time.perf_counter()
    vectorizer = TfidfVectorizer(max_features=50000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    print(f"  TF-IDF: {tfidf_matrix.shape}, built in {time.perf_counter()-t0:.1f}s")

    def score_fn(seed_ids):
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = np.asarray(tfidf_matrix[seed_indices].mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return np.asarray(tfidf_matrix.dot(centroid)).flatten()

    strategy = SimpleStrategy(name="TF-IDF cosine", strategy_id="S1d",
                              score_fn=score_fn, paper_ids=paper_ids)
    return strategy, tfidf_matrix


def make_category_strategy(corpus, paper_ids):
    """Build S2a: primary category filter."""
    from harness.strategy_protocol import SimpleStrategy

    all_cats = {aid: corpus[aid].get("primary_category", "") for aid in paper_ids}

    def score_fn(seed_ids):
        seed_cats = [all_cats.get(sid, "") for sid in seed_ids if sid in all_cats]
        if not seed_cats:
            return np.zeros(len(paper_ids))
        cat_counts = Counter(seed_cats)
        dominant_cat = cat_counts.most_common(1)[0][0]
        return np.array([1.0 if all_cats.get(aid, "") == dominant_cat else 0.0
                         for aid in paper_ids])

    return SimpleStrategy(name="Category filter (primary)", strategy_id="S2a",
                          score_fn=score_fn, paper_ids=paper_ids)


def make_coauthor_strategy(corpus, paper_ids):
    """Build S2f: co-author count."""
    import re
    from harness.strategy_protocol import SimpleStrategy

    def normalize_name(name):
        name = name.strip().lower().replace(".", " ")
        if "," in name:
            parts = name.split(",", 1)
            name = parts[1].strip() + " " + parts[0].strip()
        return re.sub(r"\s+", " ", name).strip()

    def extract_names(text):
        if not text:
            return set()
        text = text.replace(" and ", ", ")
        return {normalize_name(n) for n in text.split(",") if n.strip() and len(n.strip()) > 1}

    author_sets = {aid: extract_names(corpus[aid].get("authors_text", "")) for aid in paper_ids}

    def score_fn(seed_ids):
        seed_authors = set()
        for sid in seed_ids:
            if sid in author_sets:
                seed_authors.update(author_sets[sid])
        if not seed_authors:
            return np.zeros(len(paper_ids))
        return np.array([float(len(author_sets.get(aid, set()) & seed_authors))
                         for aid in paper_ids], dtype=np.float64)

    return SimpleStrategy(name="Co-author count", strategy_id="S2f",
                          score_fn=score_fn, paper_ids=paper_ids)


# ---------------------------------------------------------------------------
# CombinedStrategy wrapper: wraps combination logic into the Strategy protocol
# ---------------------------------------------------------------------------

class CombinedStrategy:
    """A strategy that combines multiple base strategies via a fusion function.

    Implements the RecommendationStrategy protocol so it can be profiled
    by the standard harness.
    """

    def __init__(
        self,
        name: str,
        strategy_id: str,
        base_strategies: list,
        fusion_fn,
        paper_ids: list[str],
        top_k_base: int = 200,
    ):
        self._name = name
        self._strategy_id = strategy_id
        self._base_strategies = base_strategies
        self._fusion_fn = fusion_fn
        self._paper_ids = paper_ids
        self._top_k_base = top_k_base

    @property
    def name(self):
        return self._name

    @property
    def strategy_id(self):
        return self._strategy_id

    def recommend(self, seed_arxiv_ids: list[str], top_k: int = 20) -> list[tuple[str, float]]:
        """Get rankings from each base strategy, then fuse."""
        # Get FULL rankings from each base strategy (not just top-k)
        # so RRF has complete rank information
        base_rankings = []
        for strat in self._base_strategies:
            recs = strat.recommend(seed_arxiv_ids, top_k=self._top_k_base)
            base_rankings.append(recs)

        combined = self._fusion_fn(base_rankings)
        # Filter out seeds
        seed_set = set(seed_arxiv_ids)
        combined = [(pid, score) for pid, score in combined if pid not in seed_set]
        return combined[:top_k]


# ---------------------------------------------------------------------------
# W3.1: Pairwise combination screening
# ---------------------------------------------------------------------------

def run_w3_1(profiler, strategies, paper_ids):
    """W3.1: Screen pairwise and triple combinations via RRF (k=60).

    Tests:
      C1: S1a + S1d (MiniLM + TF-IDF) -- most promising from qualitative review
      C2: S1a + S1c (MiniLM + SPECTER2)
      C3: S1d + S1c (TF-IDF + SPECTER2)
      C4: S1a + S1d + S1c (all three)
      C5: S1a + S2a (MiniLM + category filter)
    """
    print("\n" + "=" * 70)
    print("W3.1: Pairwise Combination Screening (RRF k=60)")
    print("=" * 70)

    s1a = strategies["S1a"]
    s1c = strategies["S1c"]
    s1d = strategies["S1d"]
    s2a = strategies["S2a"]

    combos = [
        ("C1", "MiniLM + TF-IDF (RRF)", [s1a, s1d],
         lambda rl: rrf_combine(rl, k=60)),
        ("C2", "MiniLM + SPECTER2 (RRF)", [s1a, s1c],
         lambda rl: rrf_combine(rl, k=60)),
        ("C3", "TF-IDF + SPECTER2 (RRF)", [s1d, s1c],
         lambda rl: rrf_combine(rl, k=60)),
        ("C4", "MiniLM + TF-IDF + SPECTER2 (RRF)", [s1a, s1d, s1c],
         lambda rl: rrf_combine(rl, k=60)),
        ("C5", "MiniLM + Category (RRF)", [s1a, s2a],
         lambda rl: rrf_combine(rl, k=60)),
    ]

    results = {}
    for cid, name, base_strats, fusion_fn in combos:
        print(f"\n--- {cid}: {name} ---")
        combined_strat = CombinedStrategy(
            name=name,
            strategy_id=cid,
            base_strategies=base_strats,
            fusion_fn=fusion_fn,
            paper_ids=paper_ids,
            top_k_base=200,  # Get deep rankings for complete RRF
        )

        t0 = time.perf_counter()
        card = profiler.profile(
            combined_strat,
            config={
                "components": [s.strategy_id for s in base_strats],
                "fusion": "RRF",
                "rrf_k": 60,
                "top_k_base": 200,
            },
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=50,
        )
        dt = time.perf_counter() - t0

        # Print summary
        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        prox = inst.get("seed_proximity", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)
        lat = card.get("resources", {}).get("query_latency_ms", {}).get("p50", 0)
        print(f"  MRR={mrr:.4f} Prox={prox:.3f} Cov={cov:.3f} Nov={nov:.3f} Div={div_:.1f} p50={lat:.1f}ms [{dt:.1f}s]")

        results[cid] = {
            "card": card,
            "profiling_time_s": round(dt, 1),
        }

    return results


# ---------------------------------------------------------------------------
# W3.2: RRF k-parameter sensitivity
# ---------------------------------------------------------------------------

def run_w3_2(profiler, strategies, paper_ids, top_combo_ids, w3_1_results):
    """W3.2: Vary RRF k for top 2 combinations from W3.1.

    Tests k = 10, 30, 60, 100 for the best two combos.
    """
    print("\n" + "=" * 70)
    print("W3.2: RRF k-Parameter Sensitivity")
    print("=" * 70)

    s1a = strategies["S1a"]
    s1c = strategies["S1c"]
    s1d = strategies["S1d"]
    s2a = strategies["S2a"]

    combo_map = {
        "C1": ("MiniLM + TF-IDF", [s1a, s1d]),
        "C2": ("MiniLM + SPECTER2", [s1a, s1c]),
        "C3": ("TF-IDF + SPECTER2", [s1d, s1c]),
        "C4": ("MiniLM + TF-IDF + SPECTER2", [s1a, s1d, s1c]),
        "C5": ("MiniLM + Category", [s1a, s2a]),
    }

    k_values = [10, 30, 60, 100]
    results = {}

    for cid in top_combo_ids[:2]:
        combo_name, base_strats = combo_map[cid]
        print(f"\n--- {cid}: {combo_name} ---")
        k_results = {}

        for k_val in k_values:
            print(f"  k={k_val}...", end=" ")
            combined_strat = CombinedStrategy(
                name=f"{combo_name} (RRF k={k_val})",
                strategy_id=f"{cid}_k{k_val}",
                base_strategies=base_strats,
                fusion_fn=lambda rl, k=k_val: rrf_combine(rl, k=k),
                paper_ids=paper_ids,
                top_k_base=200,
            )

            card = profiler.profile(
                combined_strat,
                config={"components": [s.strategy_id for s in base_strats],
                        "fusion": "RRF", "rrf_k": k_val},
                top_k=20,
                run_loo=True,
                measure_resources=False,
            )

            inst = card.get("instruments", {})
            mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
            cov = inst.get("coverage", {}).get("mean", 0)
            print(f"MRR={mrr:.4f} Cov={cov:.3f}")

            k_results[k_val] = {
                "card": card,
                "mrr": mrr,
                "coverage": cov,
            }

        results[cid] = {
            "combo_name": combo_name,
            "k_sweep": k_results,
        }

        # Report sensitivity
        mrrs = [k_results[k]["mrr"] for k in k_values]
        mrr_range = max(mrrs) - min(mrrs)
        print(f"  MRR range across k: {mrr_range:.4f} (from {min(mrrs):.4f} to {max(mrrs):.4f})")

    return results


# ---------------------------------------------------------------------------
# W3.3: Weighted combination exploration
# ---------------------------------------------------------------------------

def run_w3_3(profiler, strategies, paper_ids, top_combo_ids):
    """W3.3: Test weighted combinations for top 2 combos.

    Tests weights: 0.2/0.8, 0.4/0.6, 0.5/0.5, 0.6/0.4, 0.8/0.2
    Uses min-max normalized score fusion (NOT suitable for SPECTER2 combos).
    """
    print("\n" + "=" * 70)
    print("W3.3: Weighted Combination Exploration")
    print("=" * 70)

    s1a = strategies["S1a"]
    s1c = strategies["S1c"]
    s1d = strategies["S1d"]
    s2a = strategies["S2a"]

    combo_map = {
        "C1": ("MiniLM + TF-IDF", [s1a, s1d]),
        "C2": ("MiniLM + SPECTER2", [s1a, s1c]),
        "C3": ("TF-IDF + SPECTER2", [s1d, s1c]),
        "C4": ("MiniLM + TF-IDF + SPECTER2", [s1a, s1d, s1c]),
        "C5": ("MiniLM + Category", [s1a, s2a]),
    }

    weight_pairs = [(0.2, 0.8), (0.4, 0.6), (0.5, 0.5), (0.6, 0.4), (0.8, 0.2)]
    results = {}

    for cid in top_combo_ids[:2]:
        combo_name, base_strats = combo_map[cid]
        n_strats = len(base_strats)

        # Skip weighted for triple combos -- too many weight configurations
        if n_strats > 2:
            print(f"\n--- {cid}: {combo_name} --- SKIPPED (triple combo, weights not applicable)")
            results[cid] = {"skipped": True, "reason": "triple combo"}
            continue

        print(f"\n--- {cid}: {combo_name} ---")

        # Check if SPECTER2 is involved -- warn about score compression
        has_specter2 = any(s.strategy_id == "S1c" for s in base_strats)
        if has_specter2:
            print("  WARNING: SPECTER2 score compression makes weighted fusion unreliable.")
            print("  Results should be compared to RRF, not taken at face value.")

        weight_results = {}
        for w1, w2 in weight_pairs:
            weights = [w1, w2]
            label = f"{w1:.1f}/{w2:.1f}"
            print(f"  weights={label}...", end=" ")

            combined_strat = CombinedStrategy(
                name=f"{combo_name} (w={label})",
                strategy_id=f"{cid}_w{label.replace('/', '_')}",
                base_strategies=base_strats,
                fusion_fn=lambda rl, w=weights: weighted_combine(rl, w),
                paper_ids=paper_ids,
                top_k_base=200,
            )

            card = profiler.profile(
                combined_strat,
                config={"components": [s.strategy_id for s in base_strats],
                        "fusion": "weighted", "weights": weights},
                top_k=20,
                run_loo=True,
                measure_resources=False,
            )

            inst = card.get("instruments", {})
            mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
            cov = inst.get("coverage", {}).get("mean", 0)
            prox = inst.get("seed_proximity", {}).get("mean", 0)
            nov = inst.get("novelty", {}).get("mean", 0)
            print(f"MRR={mrr:.4f} Cov={cov:.3f} Prox={prox:.3f} Nov={nov:.3f}")

            weight_results[label] = {
                "card": card,
                "weights": weights,
                "mrr": mrr,
                "coverage": cov,
                "proximity": prox,
                "novelty": nov,
            }

        results[cid] = {
            "combo_name": combo_name,
            "has_specter2": has_specter2,
            "weight_sweep": weight_results,
        }

    return results


# ---------------------------------------------------------------------------
# W3.5: Marginal signal value
# ---------------------------------------------------------------------------

def run_w3_5(profiler, strategies, paper_ids):
    """W3.5: Start from MiniLM, add signals incrementally.

    Pipeline:
      Step 0: MiniLM alone (baseline from W1A)
      Step 1: + TF-IDF
      Step 2: + SPECTER2
      Step 3: + Category (S2a)
      Step 4: + Co-author (S2f)

    Uses RRF to combine at each step.
    """
    print("\n" + "=" * 70)
    print("W3.5: Marginal Signal Value (Incremental Addition)")
    print("=" * 70)

    s1a = strategies["S1a"]
    s1d = strategies["S1d"]
    s1c = strategies["S1c"]
    s2a = strategies["S2a"]
    s2f = strategies["S2f"]

    steps = [
        ("Step0", "MiniLM alone", [s1a]),
        ("Step1", "+ TF-IDF", [s1a, s1d]),
        ("Step2", "+ SPECTER2", [s1a, s1d, s1c]),
        ("Step3", "+ Category", [s1a, s1d, s1c, s2a]),
        ("Step4", "+ Co-author", [s1a, s1d, s1c, s2a, s2f]),
    ]

    results = {}
    prev_mrr = None

    for step_id, label, base_strats in steps:
        print(f"\n  {step_id}: {label} ({len(base_strats)} strategies)...", end=" ")

        if len(base_strats) == 1:
            # No combination needed -- just profile the solo strategy
            card = profiler.profile(
                base_strats[0],
                config={"step": step_id, "components": [base_strats[0].strategy_id]},
                top_k=20,
                run_loo=True,
                measure_resources=False,
            )
        else:
            combined_strat = CombinedStrategy(
                name=label,
                strategy_id=step_id,
                base_strategies=base_strats,
                fusion_fn=lambda rl: rrf_combine(rl, k=60),
                paper_ids=paper_ids,
                top_k_base=200,
            )
            card = profiler.profile(
                combined_strat,
                config={"step": step_id,
                        "components": [s.strategy_id for s in base_strats],
                        "fusion": "RRF", "rrf_k": 60},
                top_k=20,
                run_loo=True,
                measure_resources=False,
            )

        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)

        delta_mrr = (mrr - prev_mrr) if prev_mrr is not None else 0
        prev_mrr = mrr

        print(f"MRR={mrr:.4f} (delta={delta_mrr:+.4f}) Cov={cov:.3f} Nov={nov:.3f} Div={div_:.1f}")

        results[step_id] = {
            "label": label,
            "card": card,
            "components": [s.strategy_id for s in base_strats],
            "mrr": mrr,
            "mrr_delta": delta_mrr,
            "coverage": cov,
            "novelty": nov,
            "diversity": div_,
        }

    return results


# ---------------------------------------------------------------------------
# W3.6: Consensus validation
# ---------------------------------------------------------------------------

def run_w3_6(profiler, strategies, paper_ids):
    """W3.6: Analyze overlap between MiniLM and TF-IDF top-20 lists.

    For each profile x seed_set:
      1. Get top-20 from MiniLM and TF-IDF separately
      2. Label papers as consensus, MiniLM-exclusive, TF-IDF-exclusive
      3. Compute quality proxy for each subset
      4. Report overlap statistics
    """
    print("\n" + "=" * 70)
    print("W3.6: Consensus Validation (MiniLM vs TF-IDF Overlap)")
    print("=" * 70)

    s1a = strategies["S1a"]
    s1d = strategies["S1d"]
    profiles = profiler.profiles

    overlap_stats = []
    per_profile = {}

    for prof in profiles:
        profile_overlaps = []

        for si, seed_set in enumerate(prof.seed_sets):
            # Get top-20 from each strategy
            recs_minilm = s1a.recommend(seed_set, top_k=20)
            recs_tfidf = s1d.recommend(seed_set, top_k=20)

            minilm_ids = set(r[0] for r in recs_minilm)
            tfidf_ids = set(r[0] for r in recs_tfidf)

            consensus = minilm_ids & tfidf_ids
            minilm_only = minilm_ids - tfidf_ids
            tfidf_only = tfidf_ids - minilm_ids
            union = minilm_ids | tfidf_ids

            jaccard = len(consensus) / len(union) if union else 0

            # Check which subset contains cluster papers (proxy for relevance)
            cluster_set = set(prof.cluster_papers)
            consensus_in_cluster = len(consensus & cluster_set)
            minilm_only_in_cluster = len(minilm_only & cluster_set)
            tfidf_only_in_cluster = len(tfidf_only & cluster_set)

            # Check held-out paper presence (strongest relevance signal)
            held_out_set = set(prof.held_out)
            consensus_held_out = len(consensus & held_out_set)
            minilm_only_held_out = len(minilm_only & held_out_set)
            tfidf_only_held_out = len(tfidf_only & held_out_set)

            overlap_entry = {
                "profile_id": prof.profile_id,
                "seed_set": si,
                "n_consensus": len(consensus),
                "n_minilm_only": len(minilm_only),
                "n_tfidf_only": len(tfidf_only),
                "n_union": len(union),
                "jaccard": round(jaccard, 4),
                "consensus_in_cluster": consensus_in_cluster,
                "minilm_only_in_cluster": minilm_only_in_cluster,
                "tfidf_only_in_cluster": tfidf_only_in_cluster,
                "consensus_held_out": consensus_held_out,
                "minilm_only_held_out": minilm_only_held_out,
                "tfidf_only_held_out": tfidf_only_held_out,
                "consensus_ids": sorted(consensus),
                "minilm_only_ids": sorted(minilm_only),
                "tfidf_only_ids": sorted(tfidf_only),
            }

            overlap_stats.append(overlap_entry)
            profile_overlaps.append(overlap_entry)

        # Aggregate for this profile
        avg_consensus = np.mean([e["n_consensus"] for e in profile_overlaps])
        avg_jaccard = np.mean([e["jaccard"] for e in profile_overlaps])
        total_tfidf_only_cluster = sum(e["tfidf_only_in_cluster"] for e in profile_overlaps)
        total_tfidf_only_held = sum(e["tfidf_only_held_out"] for e in profile_overlaps)

        per_profile[prof.profile_id] = {
            "name": prof.name,
            "avg_consensus": round(float(avg_consensus), 1),
            "avg_jaccard": round(float(avg_jaccard), 4),
            "total_tfidf_only_in_cluster": total_tfidf_only_cluster,
            "total_tfidf_only_held_out": total_tfidf_only_held,
            "seed_set_details": profile_overlaps,
        }

        print(f"  {prof.profile_id} ({prof.name}): "
              f"consensus={avg_consensus:.1f}/20, "
              f"jaccard={avg_jaccard:.3f}, "
              f"TF-IDF-only-in-cluster={total_tfidf_only_cluster}")

    # Global summary
    all_consensus = [e["n_consensus"] for e in overlap_stats]
    all_jaccard = [e["jaccard"] for e in overlap_stats]
    total_tfidf_unique_cluster = sum(e["tfidf_only_in_cluster"] for e in overlap_stats)
    total_tfidf_unique_held = sum(e["tfidf_only_held_out"] for e in overlap_stats)

    summary = {
        "mean_consensus": round(float(np.mean(all_consensus)), 2),
        "std_consensus": round(float(np.std(all_consensus)), 2),
        "mean_jaccard": round(float(np.mean(all_jaccard)), 4),
        "min_consensus": int(min(all_consensus)),
        "max_consensus": int(max(all_consensus)),
        "total_tfidf_only_in_cluster": total_tfidf_unique_cluster,
        "total_tfidf_only_held_out": total_tfidf_unique_held,
        "n_evaluations": len(overlap_stats),
    }

    print(f"\n  GLOBAL: mean consensus={summary['mean_consensus']:.1f}/20, "
          f"jaccard={summary['mean_jaccard']:.3f}")
    print(f"  TF-IDF-exclusive papers in clusters: {total_tfidf_unique_cluster}")
    print(f"  TF-IDF-exclusive papers that are held-out: {total_tfidf_unique_held}")

    return {
        "summary": summary,
        "per_profile": per_profile,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.perf_counter()
    print("=" * 70)
    print("W3: Combination and Pipeline Profiling")
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
    id_to_idx = profiler.id_to_idx

    # Load abstracts for TF-IDF
    print("\nLoading abstracts...")
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
    abstract_map = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()
    abstracts = [abstract_map.get(pid, "") for pid in paper_ids]

    # Load corpus for metadata strategies
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date FROM papers"
    ).fetchall()
    conn.close()
    corpus = {row["arxiv_id"]: dict(row) for row in rows}

    # ----- Build all base strategies -----
    print("\n--- Building base strategies ---")
    strategies = {}

    print("  S1a: MiniLM embedding centroid...")
    strategies["S1a"] = make_embedding_strategy(
        profiler.embeddings, paper_ids, id_to_idx,
        "MiniLM centroid", "S1a")

    print("  S1c: SPECTER2 adapter centroid...")
    strategies["S1c"] = make_embedding_strategy(
        profiler.specter2_embeddings, paper_ids, profiler.specter2_id_to_idx,
        "SPECTER2 adapter centroid", "S1c")

    print("  S1d: TF-IDF cosine...")
    strategies["S1d"], tfidf_matrix = make_tfidf_strategy(abstracts, paper_ids, id_to_idx)

    print("  S2a: Category filter (primary)...")
    strategies["S2a"] = make_category_strategy(corpus, paper_ids)

    print("  S2f: Co-author count...")
    strategies["S2f"] = make_coauthor_strategy(corpus, paper_ids)

    # ===================================================================
    # W3.1: Pairwise screening
    # ===================================================================
    w3_1_results = run_w3_1(profiler, strategies, paper_ids)

    # Rank combos by MRR to pick top 2 for subsequent experiments
    combo_mrrs = {}
    for cid, cdata in w3_1_results.items():
        card = cdata["card"]
        mrr = card.get("instruments", {}).get("leave_one_out_mrr", {}).get("mean", 0)
        combo_mrrs[cid] = mrr
    ranked_combos = sorted(combo_mrrs, key=lambda c: combo_mrrs[c], reverse=True)
    top_2 = ranked_combos[:2]
    print(f"\n  Top 2 combos by MRR: {top_2[0]}={combo_mrrs[top_2[0]]:.4f}, "
          f"{top_2[1]}={combo_mrrs[top_2[1]]:.4f}")

    # ===================================================================
    # W3.2: RRF k-parameter sensitivity
    # ===================================================================
    w3_2_results = run_w3_2(profiler, strategies, paper_ids, top_2, w3_1_results)

    # ===================================================================
    # W3.3: Weighted combination
    # ===================================================================
    w3_3_results = run_w3_3(profiler, strategies, paper_ids, top_2)

    # ===================================================================
    # W3.5: Marginal signal value
    # ===================================================================
    w3_5_results = run_w3_5(profiler, strategies, paper_ids)

    # ===================================================================
    # W3.6: Consensus validation
    # ===================================================================
    w3_6_results = run_w3_6(profiler, strategies, paper_ids)

    # ===================================================================
    # Summary comparison
    # ===================================================================
    print("\n" + "=" * 70)
    print("W3 SUMMARY")
    print("=" * 70)

    # Baseline: S1a alone
    s1a_mrr = 0.398  # From W1A
    s1a_cov = 0.686

    print(f"\nBaseline: S1a MRR={s1a_mrr:.3f} Coverage={s1a_cov:.3f}")
    print(f"\n{'Combo':<45s} {'MRR':>7s} {'dMRR':>7s} {'Cover':>7s} {'Nov':>7s} {'Div':>5s}")
    print("-" * 80)

    for cid in ranked_combos:
        cdata = w3_1_results[cid]
        card = cdata["card"]
        inst = card.get("instruments", {})
        mrr = inst.get("leave_one_out_mrr", {}).get("mean", 0)
        cov = inst.get("coverage", {}).get("mean", 0)
        nov = inst.get("novelty", {}).get("mean", 0)
        div_ = inst.get("cluster_diversity", {}).get("mean", 0)
        delta = mrr - s1a_mrr
        name = card.get("strategy_name", cid)
        print(f"{cid} {name:<41s} {mrr:7.4f} {delta:+7.4f} {cov:7.3f} {nov:7.3f} {div_:5.1f}")

    # Marginal value summary
    print(f"\nMarginal Signal Value (cumulative from MiniLM):")
    print(f"{'Step':<40s} {'MRR':>7s} {'Delta':>7s}")
    print("-" * 55)
    for step_id, sdata in sorted(w3_5_results.items()):
        print(f"{sdata['label']:<40s} {sdata['mrr']:7.4f} {sdata['mrr_delta']:+7.4f}")

    # Consensus summary
    cons = w3_6_results["summary"]
    print(f"\nConsensus (MiniLM vs TF-IDF, top-20):")
    print(f"  Mean overlap: {cons['mean_consensus']:.1f}/20 (Jaccard={cons['mean_jaccard']:.3f})")
    print(f"  TF-IDF-exclusive papers in clusters: {cons['total_tfidf_only_in_cluster']}")
    print(f"  TF-IDF-exclusive held-out recoveries: {cons['total_tfidf_only_held_out']}")

    # ===================================================================
    # Save all results
    # ===================================================================
    t_end = time.perf_counter()
    total_time = t_end - t_start

    output = {
        "metadata": {
            "experiment": "W3: Combination and Pipeline Profiling",
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "total_time_s": round(total_time, 1),
            "corpus_size": len(paper_ids),
            "n_profiles": len(profiler.profiles),
            "baseline_s1a_mrr": s1a_mrr,
            "baseline_s1a_coverage": s1a_cov,
        },
        "w3_1_pairwise": {
            cid: {
                "card": cdata["card"],
                "profiling_time_s": cdata["profiling_time_s"],
            }
            for cid, cdata in w3_1_results.items()
        },
        "w3_1_ranking": {
            "by_mrr": ranked_combos,
            "mrr_values": combo_mrrs,
            "top_2": top_2,
        },
        "w3_2_k_sensitivity": w3_2_results,
        "w3_3_weighted": w3_3_results,
        "w3_5_marginal": w3_5_results,
        "w3_6_consensus": w3_6_results,
    }

    SPIKE_003_DATA.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)

    print(f"\n{'='*70}")
    print(f"W3 COMPLETE in {total_time:.0f}s ({total_time/60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")

    return output


if __name__ == "__main__":
    main()
