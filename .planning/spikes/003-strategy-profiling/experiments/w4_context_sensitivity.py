"""
W4: Context sensitivity experiments for Spike 003.

Tests how top strategies behave under different USER CONTEXTS:
  W4.1: Cold-start curve (seed count sensitivity)
  W4.2: Interest breadth sensitivity (re-analyze W1A data)
  W4.4: Scale sensitivity (corpus size impact)
  W4.5: Negative signal impact

These findings feed the installer's conditional recommendations.
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

BASE = Path("/home/rookslog/workspace/projects/arxiv-sanity-mcp")
SPIKE_003 = BASE / ".planning/spikes/003-strategy-profiling"
SPIKE_002 = BASE / ".planning/spikes/002-backend-comparison"
SPIKE_001 = BASE / ".planning/spikes/001-volume-filtering-scoring-landscape"

EXPERIMENTS_DIR = SPIKE_003 / "experiments"
DATA_DIR = EXPERIMENTS_DIR / "data"

sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import (
    run_all_instruments,
    seed_proximity,
    topical_coherence,
    cluster_diversity,
    novelty,
    category_surprise,
    coverage,
)
from harness.profiler import (
    StrategyProfiler,
    InterestProfile,
    load_corpus_db,
    load_embeddings,
    compute_clusters,
    build_paper_to_cluster,
    build_paper_categories,
)
from harness.strategy_protocol import SimpleStrategy

# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

DB_PATH = SPIKE_001 / "experiments/data/spike_001_harvest.db"
MINILM_EMB_PATH = SPIKE_002 / "experiments/data/embeddings_19k.npy"
MINILM_IDS_PATH = SPIKE_002 / "experiments/data/arxiv_ids_19k.json"
PROFILES_PATH = DATA_DIR / "interest_profiles.json"
W1A_PATH = DATA_DIR / "w1a_content_profiles.json"
OUTPUT_PATH = DATA_DIR / "w4_context_results.json"


# ---------------------------------------------------------------------------
# Shared data loader
# ---------------------------------------------------------------------------

class SharedData:
    """Lazy-loaded shared data for all W4 experiments."""

    def __init__(self):
        self._embeddings = None
        self._paper_ids = None
        self._id_to_idx = None
        self._corpus = None
        self._abstracts = None
        self._tfidf_matrix = None
        self._tfidf_vectorizer = None
        self._cluster_labels = None
        self._paper_to_cluster = None
        self._paper_categories = None
        self._profiles_data = None
        self._profiles = None

    @property
    def embeddings(self):
        if self._embeddings is None:
            print("Loading MiniLM embeddings...")
            self._embeddings = np.load(str(MINILM_EMB_PATH))
            print(f"  Shape: {self._embeddings.shape}")
        return self._embeddings

    @property
    def paper_ids(self):
        if self._paper_ids is None:
            with open(str(MINILM_IDS_PATH)) as f:
                self._paper_ids = json.load(f)
            print(f"  {len(self._paper_ids)} paper IDs loaded")
        return self._paper_ids

    @property
    def id_to_idx(self):
        if self._id_to_idx is None:
            self._id_to_idx = {aid: i for i, aid in enumerate(self.paper_ids)}
        return self._id_to_idx

    @property
    def corpus(self):
        if self._corpus is None:
            print("Loading corpus from DB...")
            self._corpus = load_corpus_db(str(DB_PATH))
            print(f"  {len(self._corpus)} papers")
        return self._corpus

    @property
    def abstracts(self):
        if self._abstracts is None:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.execute("SELECT arxiv_id, abstract FROM papers")
            abstract_map = {row[0]: (row[1] or "") for row in cursor.fetchall()}
            conn.close()
            self._abstracts = [abstract_map.get(pid, "") for pid in self.paper_ids]
        return self._abstracts

    @property
    def tfidf_matrix(self):
        if self._tfidf_matrix is None:
            from sklearn.feature_extraction.text import TfidfVectorizer
            print("Building TF-IDF matrix...")
            t0 = time.perf_counter()
            self._tfidf_vectorizer = TfidfVectorizer(
                max_features=50000, stop_words="english"
            )
            self._tfidf_matrix = self._tfidf_vectorizer.fit_transform(self.abstracts)
            print(f"  TF-IDF: {self._tfidf_matrix.shape} in {time.perf_counter()-t0:.1f}s")
        return self._tfidf_matrix

    @property
    def cluster_labels(self):
        if self._cluster_labels is None:
            print("Computing clusters (KMeans n=48)...")
            self._cluster_labels = compute_clusters(self.embeddings, n_clusters=48)
        return self._cluster_labels

    @property
    def paper_to_cluster(self):
        if self._paper_to_cluster is None:
            self._paper_to_cluster = build_paper_to_cluster(
                self.paper_ids, self.cluster_labels
            )
        return self._paper_to_cluster

    @property
    def paper_categories(self):
        if self._paper_categories is None:
            self._paper_categories = build_paper_categories(self.corpus)
        return self._paper_categories

    @property
    def profiles_data(self):
        if self._profiles_data is None:
            with open(str(PROFILES_PATH)) as f:
                self._profiles_data = json.load(f)
        return self._profiles_data

    @property
    def profiles(self):
        if self._profiles is None:
            self._profiles = {
                pid: InterestProfile.from_dict(pdata)
                for pid, pdata in self.profiles_data["profiles"].items()
            }
        return self._profiles


# ---------------------------------------------------------------------------
# Strategy builders
# ---------------------------------------------------------------------------

def make_minilm_strategy(data: SharedData) -> SimpleStrategy:
    """S1a: MiniLM centroid cosine similarity."""
    embeddings = data.embeddings
    paper_ids = data.paper_ids
    id_to_idx = data.id_to_idx

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        centroid = embeddings[seed_indices].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return embeddings @ centroid

    return SimpleStrategy(
        name="MiniLM embedding centroid",
        strategy_id="S1a",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def make_tfidf_strategy(data: SharedData) -> SimpleStrategy:
    """S1d: TF-IDF centroid cosine similarity."""
    tfidf_matrix = data.tfidf_matrix
    paper_ids = data.paper_ids
    id_to_idx = data.id_to_idx

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        seed_indices = [id_to_idx[sid] for sid in seed_ids if sid in id_to_idx]
        if not seed_indices:
            return np.zeros(len(paper_ids))
        seed_vectors = tfidf_matrix[seed_indices]
        centroid = np.asarray(seed_vectors.mean(axis=0)).flatten()
        norm = np.linalg.norm(centroid)
        if norm < 1e-10:
            return np.zeros(len(paper_ids))
        centroid = centroid / norm
        return np.asarray(tfidf_matrix.dot(centroid)).flatten()

    return SimpleStrategy(
        name="TF-IDF cosine similarity",
        strategy_id="S1d",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Instrument runner (custom seed sets, no full profiler overhead)
# ---------------------------------------------------------------------------

def run_instruments_for_seeds(
    strategy: SimpleStrategy,
    seed_ids: list[str],
    profile: InterestProfile,
    data: SharedData,
    top_k: int = 20,
    run_loo: bool = False,
) -> dict:
    """Run quality instruments for a given seed set.

    Calls strategy.recommend() and measures all instruments.
    LOO is disabled by default for speed (it's O(cluster_size) per call).
    """
    recs = strategy.recommend(seed_ids, top_k=top_k)
    rec_ids = [r[0] for r in recs]

    if not rec_ids:
        return {name: {"value": None} for name in [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]}

    return run_all_instruments(
        strategy=strategy,
        recommended_ids=rec_ids,
        seed_ids=seed_ids,
        cluster_papers=profile.cluster_papers,
        all_paper_ids=data.paper_ids,
        embeddings=data.embeddings,
        id_to_idx=data.id_to_idx,
        paper_to_cluster=data.paper_to_cluster,
        paper_categories=data.paper_categories,
        top_k=top_k,
        run_loo=run_loo,
    )


def extract_instrument_summary(instruments: dict) -> dict:
    """Extract scalar values from instrument results."""
    return {
        name: instruments.get(name, {}).get("value")
        for name in [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]
    }


# ===================================================================
# W4.1: Cold-start curve (seed count sensitivity)
# ===================================================================

def run_w4_1(data: SharedData) -> dict:
    """Test S1a and S1d with varying seed counts: 1, 3, 5, 10, 15.

    For each strategy x seed count x profile, measure all instruments.
    Seed counts 1 and 3 are subsets of subset_5 (first N papers).
    """
    print("\n" + "=" * 70)
    print("W4.1: Cold-start curve (seed count sensitivity)")
    print("=" * 70)

    s1a = make_minilm_strategy(data)
    s1d = make_tfidf_strategy(data)

    strategies = {"S1a": s1a, "S1d": s1d}
    seed_counts = [1, 3, 5, 10, 15]
    seed_count_to_key = {5: "subset_5", 10: "subset_10", 15: "subset_15"}

    results = {}
    profile_ids = sorted(data.profiles.keys())

    for sid, strategy in strategies.items():
        print(f"\n--- Strategy: {sid} ({strategy.name}) ---")
        results[sid] = {}

        for n_seeds in seed_counts:
            print(f"\n  Seed count: {n_seeds}")
            results[sid][str(n_seeds)] = {}
            profile_instruments = []

            for pid in profile_ids:
                profile = data.profiles[pid]
                pdata = data.profiles_data["profiles"][pid]

                # Get the seed set for this count
                if n_seeds in seed_count_to_key:
                    seeds = pdata["seed_subsets"][seed_count_to_key[n_seeds]]
                elif n_seeds < 5:
                    # Take first N from subset_5
                    seeds = pdata["seed_subsets"]["subset_5"][:n_seeds]
                else:
                    continue

                # Run instruments (skip LOO for speed, it's the same
                # held-out set regardless of seed count)
                instruments = run_instruments_for_seeds(
                    strategy, seeds, profile, data,
                    top_k=20, run_loo=True,
                )
                summary = extract_instrument_summary(instruments)
                results[sid][str(n_seeds)][pid] = summary
                profile_instruments.append(summary)

                print(f"    {pid} ({profile.name[:20]}): "
                      f"MRR={summary.get('leave_one_out_mrr', 0):.4f} "
                      f"Prox={summary.get('seed_proximity', 0):.4f} "
                      f"Cov={summary.get('coverage', 0):.4f}")

            # Aggregate across profiles
            agg = {}
            for inst_name in profile_instruments[0] if profile_instruments else []:
                values = [p[inst_name] for p in profile_instruments
                         if p.get(inst_name) is not None]
                if values:
                    agg[inst_name] = {
                        "mean": float(np.mean(values)),
                        "std": float(np.std(values)),
                    }
            results[sid][str(n_seeds)]["_aggregate"] = agg

            mrr_agg = agg.get("leave_one_out_mrr", {}).get("mean", 0)
            prox_agg = agg.get("seed_proximity", {}).get("mean", 0)
            print(f"  => Aggregate: MRR={mrr_agg:.4f}, Prox={prox_agg:.4f}")

    return results


# ===================================================================
# W4.2: Interest breadth sensitivity (re-analyze W1A data)
# ===================================================================

def run_w4_2(data: SharedData) -> dict:
    """Re-analyze W1A per-profile data grouped by breadth.

    Breadth groups:
      Narrow: P3 (Quantum ML), P8 (Math foundations of NN)
      Medium: P1 (RL robotics), P2 (LLM reasoning), P5 (GNN),
              P6 (Diffusion), P7 (Federated learning)
      Broad:  P4 (AI safety)
    """
    print("\n" + "=" * 70)
    print("W4.2: Interest breadth sensitivity (re-analyzing W1A data)")
    print("=" * 70)

    with open(str(W1A_PATH)) as f:
        w1a = json.load(f)

    breadth_groups = {
        "Narrow": ["P3", "P8"],
        "Medium": ["P1", "P2", "P5", "P6", "P7"],
        "Broad": ["P4"],
    }

    instrument_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]

    results = {}

    for card in w1a["profile_cards"]:
        sid = card["strategy_id"]
        by_profile = card.get("by_profile", {})
        results[sid] = {}

        print(f"\n--- {sid} ({card['strategy_name']}) ---")

        for breadth, pids in breadth_groups.items():
            breadth_values = {name: [] for name in instrument_names}

            for pid in pids:
                prof_data = by_profile.get(pid, {})
                instruments = prof_data.get("instruments", {})
                for name in instrument_names:
                    val = instruments.get(name, {}).get("mean")
                    if val is not None:
                        breadth_values[name].append(val)

            agg = {}
            for name in instrument_names:
                vals = breadth_values[name]
                if vals:
                    agg[name] = {
                        "mean": float(np.mean(vals)),
                        "std": float(np.std(vals)),
                        "n": len(vals),
                        "values": vals,
                    }
                else:
                    agg[name] = {"mean": None, "std": None, "n": 0}

            results[sid][breadth] = {
                "profiles": pids,
                "instruments": agg,
            }

            mrr = agg.get("leave_one_out_mrr", {}).get("mean", 0)
            prox = agg.get("seed_proximity", {}).get("mean", 0)
            cov = agg.get("coverage", {}).get("mean", 0)
            print(f"  {breadth:>7s} ({len(pids)} profiles): "
                  f"MRR={mrr:.4f} Prox={prox:.4f} Cov={cov:.4f}")

    return results


# ===================================================================
# W4.4: Scale sensitivity (corpus size impact)
# ===================================================================

def run_w4_4(data: SharedData) -> dict:
    """Test quality at different corpus sizes: 2K, 5K, 10K, 19K.

    Approach: subsample paper IDs, mask scores to subsampled set.
    Embeddings stay the same -- just filter which papers are considered.
    Test with P1, P3, P4 (Medium, Narrow, Broad).
    """
    print("\n" + "=" * 70)
    print("W4.4: Scale sensitivity (corpus size impact)")
    print("=" * 70)

    test_profiles = ["P1", "P3", "P4"]
    scale_sizes = [2000, 5000, 10000, len(data.paper_ids)]

    # Collect all seed and held-out IDs we must preserve
    preserved_ids = set()
    for pid in test_profiles:
        pdata = data.profiles_data["profiles"][pid]
        for key in ["subset_5", "subset_10", "subset_15"]:
            preserved_ids.update(pdata["seed_subsets"][key])
        for hp in pdata.get("held_out_papers", []):
            preserved_ids.add(hp["arxiv_id"])
        for sp in pdata.get("seed_papers", []):
            preserved_ids.add(sp["arxiv_id"])
        # Also preserve cluster papers for coverage/LOO
        cm = pdata.get("cluster_mapping", {})
        for entry in cm.get("top_200_by_similarity", []):
            if entry.get("strongly_related", False):
                preserved_ids.add(entry["arxiv_id"])

    # Only keep preserved IDs that actually exist in the embedding index
    preserved_ids = preserved_ids & set(data.paper_ids)
    print(f"Preserved IDs (seeds + held-out + cluster): {len(preserved_ids)}")

    rng = np.random.RandomState(42)
    all_ids_set = set(data.paper_ids)
    non_preserved = [pid for pid in data.paper_ids if pid not in preserved_ids]

    results = {}

    for scale in scale_sizes:
        print(f"\n--- Scale: {scale} papers ---")

        if scale >= len(data.paper_ids):
            # Full corpus, no subsampling needed
            sampled_ids_set = all_ids_set
            actual_size = len(data.paper_ids)
        else:
            # Sample non-preserved papers to fill up to scale
            n_to_sample = max(0, scale - len(preserved_ids))
            if n_to_sample >= len(non_preserved):
                sampled_extra = non_preserved
            else:
                indices = rng.choice(
                    len(non_preserved), size=n_to_sample, replace=False
                )
                sampled_extra = [non_preserved[i] for i in indices]
            sampled_ids_set = preserved_ids | set(sampled_extra)
            actual_size = len(sampled_ids_set)

        print(f"  Actual sample size: {actual_size}")

        # Build masked strategies that only return papers in the subsample
        def _make_masked_minilm(mask_set):
            embeddings = data.embeddings
            paper_ids = data.paper_ids
            id_to_idx = data.id_to_idx

            def score_fn(seed_ids):
                seed_indices = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
                if not seed_indices:
                    return np.zeros(len(paper_ids))
                centroid = embeddings[seed_indices].mean(axis=0)
                norm = np.linalg.norm(centroid)
                if norm < 1e-10:
                    return np.zeros(len(paper_ids))
                centroid = centroid / norm
                scores = embeddings @ centroid
                # Mask out papers not in subsample
                for i, pid in enumerate(paper_ids):
                    if pid not in mask_set:
                        scores[i] = -999.0
                return scores

            return SimpleStrategy(
                name=f"MiniLM (scale={actual_size})",
                strategy_id="S1a",
                score_fn=score_fn,
                paper_ids=paper_ids,
            )

        def _make_masked_tfidf(mask_set):
            tfidf_matrix = data.tfidf_matrix
            paper_ids = data.paper_ids
            id_to_idx = data.id_to_idx

            def score_fn(seed_ids):
                seed_indices = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
                if not seed_indices:
                    return np.zeros(len(paper_ids))
                seed_vectors = tfidf_matrix[seed_indices]
                centroid = np.asarray(seed_vectors.mean(axis=0)).flatten()
                norm = np.linalg.norm(centroid)
                if norm < 1e-10:
                    return np.zeros(len(paper_ids))
                centroid = centroid / norm
                scores = np.asarray(tfidf_matrix.dot(centroid)).flatten()
                for i, pid in enumerate(paper_ids):
                    if pid not in mask_set:
                        scores[i] = -999.0
                return scores

            return SimpleStrategy(
                name=f"TF-IDF (scale={actual_size})",
                strategy_id="S1d",
                score_fn=score_fn,
                paper_ids=paper_ids,
            )

        s1a_masked = _make_masked_minilm(sampled_ids_set)
        s1d_masked = _make_masked_tfidf(sampled_ids_set)

        scale_key = str(actual_size)
        results[scale_key] = {"actual_size": actual_size}

        for sid, strategy in [("S1a", s1a_masked), ("S1d", s1d_masked)]:
            results[scale_key][sid] = {}

            for pid in test_profiles:
                profile = data.profiles[pid]
                pdata = data.profiles_data["profiles"][pid]
                seeds = pdata["seed_subsets"]["subset_10"]

                instruments = run_instruments_for_seeds(
                    strategy, seeds, profile, data,
                    top_k=20, run_loo=True,
                )
                summary = extract_instrument_summary(instruments)
                results[scale_key][sid][pid] = summary

                print(f"  {sid} {pid}: "
                      f"MRR={summary.get('leave_one_out_mrr', 0):.4f} "
                      f"Prox={summary.get('seed_proximity', 0):.4f} "
                      f"Cov={summary.get('coverage', 0):.4f}")

            # Aggregate across test profiles
            vals_list = [results[scale_key][sid][p] for p in test_profiles]
            agg = {}
            for name in vals_list[0]:
                vs = [v[name] for v in vals_list if v.get(name) is not None]
                if vs:
                    agg[name] = {"mean": float(np.mean(vs)), "std": float(np.std(vs))}
            results[scale_key][sid]["_aggregate"] = agg

    return results


# ===================================================================
# W4.5: Negative signal impact
# ===================================================================

def run_w4_5(data: SharedData) -> dict:
    """Test negative signals: does demoting anti-interest papers help?

    For S1a: subtract negative centroid from positive centroid.
    For S1d: use SVM with negatives as negative class.
    Test with P1 (Medium) and P4 (Broad).
    """
    print("\n" + "=" * 70)
    print("W4.5: Negative signal impact")
    print("=" * 70)

    test_profiles = ["P1", "P4"]

    # For each test profile, select 5 "negative" papers that are clearly
    # unrelated. Strategy: pick papers from categories with zero overlap
    # with the profile's seed categories.
    def get_negative_papers(pid: str, n: int = 5) -> list[str]:
        """Select N papers clearly unrelated to a profile."""
        pdata = data.profiles_data["profiles"][pid]
        seed_ids = set(pdata["seed_subsets"]["subset_15"])

        # Get seed categories
        seed_cats = set()
        for sid in seed_ids:
            cat = data.paper_categories.get(sid)
            if cat:
                seed_cats.add(cat)

        # Also get broader category family (e.g., cs.* -> cs)
        seed_families = {c.split(".")[0] for c in seed_cats}

        # Find papers from completely different category families
        candidates = []
        for i, aid in enumerate(data.paper_ids):
            if aid in seed_ids:
                continue
            cat = data.paper_categories.get(aid, "")
            if not cat:
                continue
            family = cat.split(".")[0]
            if family not in seed_families and family not in ("", "unknown"):
                # Also check embedding distance -- pick truly distant papers
                candidates.append((aid, i))

        if not candidates:
            # Fallback: just pick lowest-similarity papers
            seeds_idx = [data.id_to_idx[s] for s in seed_ids if s in data.id_to_idx]
            centroid = data.embeddings[seeds_idx].mean(axis=0)
            norm = np.linalg.norm(centroid)
            if norm > 1e-10:
                centroid = centroid / norm
            sims = data.embeddings @ centroid
            lowest_indices = np.argsort(sims)[:n]
            return [data.paper_ids[i] for i in lowest_indices]

        # From category-disjoint candidates, pick those with lowest similarity
        rng = np.random.RandomState(hash(pid) % (2**31))
        if len(candidates) > 200:
            sample_idx = rng.choice(len(candidates), size=200, replace=False)
            candidates = [candidates[i] for i in sample_idx]

        seeds_idx = [data.id_to_idx[s] for s in seed_ids if s in data.id_to_idx]
        centroid = data.embeddings[seeds_idx].mean(axis=0)
        norm = np.linalg.norm(centroid)
        if norm > 1e-10:
            centroid = centroid / norm

        scored = []
        for aid, idx in candidates:
            sim = float(data.embeddings[idx] @ centroid)
            scored.append((aid, sim))
        scored.sort(key=lambda x: x[1])
        return [s[0] for s in scored[:n]]

    results = {}

    for pid in test_profiles:
        profile = data.profiles[pid]
        pdata = data.profiles_data["profiles"][pid]
        seeds = pdata["seed_subsets"]["subset_10"]
        negatives = get_negative_papers(pid, n=5)

        neg_cats = [data.paper_categories.get(n, "?") for n in negatives]
        print(f"\n--- Profile {pid} ({profile.name}) ---")
        print(f"  Negative papers: {negatives}")
        print(f"  Negative categories: {neg_cats}")

        results[pid] = {
            "negative_papers": negatives,
            "negative_categories": neg_cats,
        }

        # --- S1a: Embedding centroid with negative demotion ---
        # Baseline (no negatives)
        s1a_base = make_minilm_strategy(data)
        base_instruments = run_instruments_for_seeds(
            s1a_base, seeds, profile, data, top_k=20, run_loo=True
        )

        # With negatives: subtract weighted negative centroid
        def _make_neg_minilm(neg_ids, alpha=0.5):
            embeddings = data.embeddings
            paper_ids = data.paper_ids
            id_to_idx = data.id_to_idx

            def score_fn(seed_ids):
                seed_indices = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
                neg_indices = [id_to_idx[n] for n in neg_ids if n in id_to_idx]
                if not seed_indices:
                    return np.zeros(len(paper_ids))

                pos_centroid = embeddings[seed_indices].mean(axis=0)
                if neg_indices:
                    neg_centroid = embeddings[neg_indices].mean(axis=0)
                    # Subtract weighted negative centroid
                    adjusted = pos_centroid - alpha * neg_centroid
                else:
                    adjusted = pos_centroid

                norm = np.linalg.norm(adjusted)
                if norm < 1e-10:
                    return np.zeros(len(paper_ids))
                adjusted = adjusted / norm
                return embeddings @ adjusted

            return SimpleStrategy(
                name=f"MiniLM + negatives (alpha={alpha})",
                strategy_id="S1a_neg",
                score_fn=score_fn,
                paper_ids=paper_ids,
            )

        # Test multiple alpha values
        alpha_results = {}
        for alpha in [0.25, 0.5, 0.75, 1.0]:
            s1a_neg = _make_neg_minilm(negatives, alpha=alpha)
            neg_instruments = run_instruments_for_seeds(
                s1a_neg, seeds, profile, data, top_k=20, run_loo=True
            )
            alpha_results[str(alpha)] = extract_instrument_summary(neg_instruments)

        results[pid]["S1a"] = {
            "baseline": extract_instrument_summary(base_instruments),
            "with_negatives": alpha_results,
        }

        base_mrr = results[pid]["S1a"]["baseline"].get("leave_one_out_mrr", 0)
        print(f"  S1a baseline MRR={base_mrr:.4f}")
        for alpha_str, r in alpha_results.items():
            neg_mrr = r.get("leave_one_out_mrr", 0)
            delta = (neg_mrr - base_mrr) if (neg_mrr and base_mrr) else 0
            print(f"  S1a alpha={alpha_str}: MRR={neg_mrr:.4f} (delta={delta:+.4f})")

        # --- S1d: SVM with negatives as negative class ---
        s1d_base = make_tfidf_strategy(data)
        base_instruments_tfidf = run_instruments_for_seeds(
            s1d_base, seeds, profile, data, top_k=20, run_loo=True
        )

        # SVM with explicit negatives
        def _make_svm_with_negatives(neg_ids):
            from sklearn.svm import LinearSVC
            tfidf_matrix = data.tfidf_matrix
            paper_ids = data.paper_ids
            id_to_idx = data.id_to_idx

            def score_fn(seed_ids):
                seed_set = set(id_to_idx[s] for s in seed_ids if s in id_to_idx)
                neg_set = set(id_to_idx[n] for n in neg_ids if n in id_to_idx)
                if not seed_set:
                    return np.zeros(len(paper_ids))

                # Labels: +1 for seeds, -1 for negatives, 0 for rest
                y = np.zeros(len(paper_ids))
                for i in seed_set:
                    y[i] = 1
                for i in neg_set:
                    y[i] = -1

                # For SVM, only train on labeled examples
                labeled_mask = y != 0
                X_train = tfidf_matrix[labeled_mask]
                y_train = y[labeled_mask]

                if len(set(y_train)) < 2:
                    return np.zeros(len(paper_ids))

                svm = LinearSVC(C=0.01, class_weight="balanced", max_iter=5000)
                svm.fit(X_train, y_train)
                scores = svm.decision_function(tfidf_matrix)
                return scores

            return SimpleStrategy(
                name="SVM with explicit negatives",
                strategy_id="S1d_svm_neg",
                score_fn=score_fn,
                paper_ids=paper_ids,
            )

        s1d_svm_neg = _make_svm_with_negatives(negatives)
        svm_neg_instruments = run_instruments_for_seeds(
            s1d_svm_neg, seeds, profile, data, top_k=20, run_loo=True
        )

        # Also test TF-IDF with negative demotion (same approach as MiniLM)
        def _make_neg_tfidf(neg_ids, alpha=0.5):
            tfidf_matrix = data.tfidf_matrix
            paper_ids = data.paper_ids
            id_to_idx = data.id_to_idx

            def score_fn(seed_ids):
                seed_indices = [id_to_idx[s] for s in seed_ids if s in id_to_idx]
                neg_indices = [id_to_idx[n] for n in neg_ids if n in id_to_idx]
                if not seed_indices:
                    return np.zeros(len(paper_ids))

                pos_centroid = np.asarray(
                    tfidf_matrix[seed_indices].mean(axis=0)
                ).flatten()
                if neg_indices:
                    neg_centroid = np.asarray(
                        tfidf_matrix[neg_indices].mean(axis=0)
                    ).flatten()
                    adjusted = pos_centroid - alpha * neg_centroid
                else:
                    adjusted = pos_centroid

                norm = np.linalg.norm(adjusted)
                if norm < 1e-10:
                    return np.zeros(len(paper_ids))
                adjusted = adjusted / norm
                return np.asarray(tfidf_matrix.dot(adjusted)).flatten()

            return SimpleStrategy(
                name=f"TF-IDF + negatives (alpha={alpha})",
                strategy_id="S1d_neg",
                score_fn=score_fn,
                paper_ids=paper_ids,
            )

        tfidf_neg_results = {}
        for alpha in [0.25, 0.5, 0.75]:
            s1d_neg = _make_neg_tfidf(negatives, alpha=alpha)
            neg_instruments = run_instruments_for_seeds(
                s1d_neg, seeds, profile, data, top_k=20, run_loo=True
            )
            tfidf_neg_results[str(alpha)] = extract_instrument_summary(neg_instruments)

        results[pid]["S1d"] = {
            "baseline": extract_instrument_summary(base_instruments_tfidf),
            "svm_with_negatives": extract_instrument_summary(svm_neg_instruments),
            "centroid_with_negatives": tfidf_neg_results,
        }

        base_mrr_td = results[pid]["S1d"]["baseline"].get("leave_one_out_mrr", 0)
        svm_mrr = results[pid]["S1d"]["svm_with_negatives"].get("leave_one_out_mrr", 0)
        print(f"  S1d baseline MRR={base_mrr_td:.4f}")
        print(f"  S1d SVM+neg MRR={svm_mrr:.4f} (delta={svm_mrr - base_mrr_td:+.4f})" if svm_mrr and base_mrr_td else "")
        for a, r in tfidf_neg_results.items():
            m = r.get("leave_one_out_mrr", 0)
            print(f"  S1d centroid+neg alpha={a}: MRR={m:.4f} (delta={m - base_mrr_td:+.4f})" if m and base_mrr_td else "")

    return results


# ===================================================================
# Main
# ===================================================================

def main():
    print("=" * 70)
    print("W4: Context Sensitivity Experiments")
    print(f"Started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 70)

    t_start = time.perf_counter()
    data = SharedData()

    # Force-load shared data upfront
    _ = data.embeddings
    _ = data.paper_ids
    _ = data.id_to_idx
    _ = data.corpus
    _ = data.cluster_labels
    _ = data.paper_to_cluster
    _ = data.paper_categories
    _ = data.profiles
    _ = data.tfidf_matrix

    results = {
        "experiment": "W4: Context sensitivity",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "corpus_size": len(data.paper_ids),
    }

    # Run each sub-experiment
    results["w4_1_cold_start"] = run_w4_1(data)
    results["w4_2_breadth"] = run_w4_2(data)
    results["w4_4_scale"] = run_w4_4(data)
    results["w4_5_negatives"] = run_w4_5(data)

    t_end = time.perf_counter()
    results["completed_at"] = datetime.now(timezone.utc).isoformat()
    results["total_time_s"] = round(t_end - t_start, 1)

    # Save results
    with open(str(OUTPUT_PATH), "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n{'=' * 70}")
    print(f"W4 COMPLETE")
    print(f"Total time: {results['total_time_s']:.1f}s ({results['total_time_s']/60:.1f}m)")
    print(f"Results saved to: {OUTPUT_PATH}")
    print(f"{'=' * 70}")

    return results


if __name__ == "__main__":
    main()
