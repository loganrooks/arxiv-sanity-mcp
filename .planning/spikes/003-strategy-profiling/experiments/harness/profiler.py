"""
StrategyProfiler: the main evaluation orchestrator.

Takes any strategy implementing RecommendationStrategy and produces
a structured profile card with all quality instruments and resource
metrics.
"""

from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np

from .instruments import run_all_instruments
from .resource_meter import measure_latency, measure_memory


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_corpus_db(db_path: str) -> dict[str, dict]:
    """Load paper metadata from the harvest database.

    Returns:
        Dict mapping arxiv_id to {"title", "abstract", "primary_category",
        "categories", "authors_text", "submitted_date"}.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, abstract, primary_category, categories, "
        "authors_text, submitted_date FROM papers"
    ).fetchall()
    conn.close()

    return {
        row["arxiv_id"]: dict(row)
        for row in rows
    }


def load_embeddings(
    emb_path: str, ids_path: str
) -> tuple[np.ndarray, list[str], dict[str, int]]:
    """Load embeddings and paper IDs.

    Returns:
        (embeddings_matrix, paper_ids_list, id_to_index_dict)
    """
    embeddings = np.load(emb_path)
    with open(ids_path) as f:
        paper_ids = json.load(f)

    assert len(paper_ids) == embeddings.shape[0], (
        f"ID count {len(paper_ids)} != embedding rows {embeddings.shape[0]}"
    )

    id_to_idx = {aid: i for i, aid in enumerate(paper_ids)}
    return embeddings, paper_ids, id_to_idx


def compute_clusters(
    embeddings: np.ndarray, n_clusters: int = 48, seed: int = 42
) -> np.ndarray:
    """Compute KMeans cluster assignments (proxy for BERTopic).

    Uses MiniBatchKMeans for consistency with Spike 001.

    Returns:
        Array of cluster labels, shape (n_papers,).
    """
    from sklearn.cluster import MiniBatchKMeans

    km = MiniBatchKMeans(n_clusters=n_clusters, random_state=seed, batch_size=1000)
    return km.fit_predict(embeddings)


def build_paper_to_cluster(
    paper_ids: list[str], cluster_labels: np.ndarray
) -> dict[str, int]:
    """Build paper-to-cluster mapping from arrays."""
    return {aid: int(label) for aid, label in zip(paper_ids, cluster_labels)}


def build_paper_categories(corpus: dict[str, dict]) -> dict[str, str]:
    """Build paper-to-primary-category mapping from corpus."""
    return {
        aid: meta.get("primary_category", "unknown")
        for aid, meta in corpus.items()
    }


# ---------------------------------------------------------------------------
# Interest profile schema
# ---------------------------------------------------------------------------

class InterestProfile:
    """An interest profile defines a simulated user's research interest.

    Each profile has:
        - seed_sets: multiple random selections of seed papers (for variance estimation)
        - cluster_papers: papers in the relevant clusters (for LOO and coverage)
        - held_out: papers reserved for LOO evaluation (never used as seeds)
    """

    def __init__(
        self,
        profile_id: str,
        name: str,
        description: str,
        breadth: str,
        seed_sets: list[list[str]],
        cluster_papers: list[str],
        held_out: list[str],
    ):
        self.profile_id = profile_id
        self.name = name
        self.description = description
        self.breadth = breadth  # "narrow", "medium", "broad"
        self.seed_sets = seed_sets  # 3 random selections
        self.cluster_papers = cluster_papers
        self.held_out = held_out

    @classmethod
    def from_dict(cls, d: dict) -> "InterestProfile":
        """Construct from either canonical format or W0.3 output format.

        Canonical format:
            {"profile_id", "name", "seed_sets", "cluster_papers", "held_out", ...}

        W0.3 format:
            {"profile_id", "name", "seed_papers": [{"arxiv_id": ...}],
             "held_out_papers": [{"arxiv_id": ...}],
             "seed_subsets": {"subset_5": [...], "subset_10": [...], "subset_15": [...]},
             "cluster_mapping": {"top_200_by_similarity": [{"arxiv_id": ..., "strongly_related": bool}]}}
        """
        # Check which format we have
        if "seed_sets" in d:
            # Canonical format
            return cls(
                profile_id=d["profile_id"],
                name=d["name"],
                description=d.get("description", ""),
                breadth=d.get("breadth", "medium"),
                seed_sets=d["seed_sets"],
                cluster_papers=d["cluster_papers"],
                held_out=d.get("held_out", []),
            )

        # W0.3 format -- adapt
        profile_id = d["profile_id"]
        name = d["name"]
        description = d.get("description", "")
        breadth = d.get("breadth", "medium")

        # Extract seed IDs from seed_papers list of dicts
        all_seed_ids = [
            sp["arxiv_id"] for sp in d.get("seed_papers", [])
            if isinstance(sp, dict) and "arxiv_id" in sp
        ]

        # Build 3 seed sets from the seed_subsets
        seed_subsets = d.get("seed_subsets", {})
        seed_sets = []
        for key in ["subset_5", "subset_10", "subset_15"]:
            subset = seed_subsets.get(key, [])
            if subset:
                seed_sets.append(subset)

        # Fallback: if no subsets, create 3 overlapping selections from all seeds
        if not seed_sets:
            rng = np.random.RandomState(hash(profile_id) % (2**31))
            n = len(all_seed_ids)
            if n >= 5:
                for _ in range(3):
                    size = min(max(5, n // 2), n)
                    indices = rng.choice(n, size=size, replace=False)
                    seed_sets.append([all_seed_ids[i] for i in sorted(indices)])
            elif all_seed_ids:
                seed_sets = [all_seed_ids]  # Single seed set if too few

        # Extract held-out paper IDs
        held_out = [
            hp["arxiv_id"] for hp in d.get("held_out_papers", [])
            if isinstance(hp, dict) and "arxiv_id" in hp
        ]

        # Extract cluster papers from cluster_mapping
        # "strongly_related" papers are the most reliable cluster members
        cluster_mapping = d.get("cluster_mapping", {})
        top_similar = cluster_mapping.get("top_200_by_similarity", [])

        # Use strongly_related papers as cluster papers for LOO/coverage
        cluster_papers = [
            entry["arxiv_id"]
            for entry in top_similar
            if isinstance(entry, dict) and entry.get("strongly_related", False)
        ]

        # Fallback: use all top-200 if no strongly_related field
        if not cluster_papers and top_similar:
            cluster_papers = [
                entry["arxiv_id"]
                for entry in top_similar
                if isinstance(entry, dict) and "arxiv_id" in entry
            ]

        return cls(
            profile_id=profile_id,
            name=name,
            description=description,
            breadth=breadth,
            seed_sets=seed_sets,
            cluster_papers=cluster_papers,
            held_out=held_out,
        )

    def to_dict(self) -> dict:
        return {
            "profile_id": self.profile_id,
            "name": self.name,
            "description": self.description,
            "breadth": self.breadth,
            "seed_sets": self.seed_sets,
            "cluster_papers": self.cluster_papers,
            "held_out": self.held_out,
        }


def load_interest_profiles(path: str) -> list[InterestProfile]:
    """Load interest profiles from JSON file.

    Handles two formats:
    1. List format: [{"profile_id": ..., ...}, ...]
    2. W0.3 format: {"metadata": ..., "profiles": {"P1": {...}, ...}}

    Returns empty list if file doesn't exist (W0.3 runs in parallel).
    """
    p = Path(path)
    if not p.exists():
        return []

    with open(p) as f:
        data = json.load(f)

    # W0.3 format: top-level dict with "profiles" key
    if isinstance(data, dict) and "profiles" in data:
        profiles_dict = data["profiles"]
        return [
            InterestProfile.from_dict(prof_data)
            for prof_data in profiles_dict.values()
        ]

    # List format (canonical)
    if isinstance(data, list):
        return [InterestProfile.from_dict(d) for d in data]

    return []


# ---------------------------------------------------------------------------
# StrategyProfiler
# ---------------------------------------------------------------------------

class StrategyProfiler:
    """Run a strategy across interest profiles, computing all instruments + resources.

    Usage:
        profiler = StrategyProfiler.from_spike_data()
        card = profiler.profile(my_strategy)
        comparison = profiler.compare([card1, card2, card3])
    """

    def __init__(
        self,
        corpus: dict[str, dict],
        embeddings: np.ndarray,
        paper_ids: list[str],
        id_to_idx: dict[str, int],
        paper_to_cluster: dict[str, int],
        paper_categories: dict[str, str],
        profiles: list[InterestProfile],
        specter2_embeddings: Optional[np.ndarray] = None,
        specter2_id_to_idx: Optional[dict[str, int]] = None,
    ):
        self.corpus = corpus
        self.embeddings = embeddings
        self.paper_ids = paper_ids
        self.id_to_idx = id_to_idx
        self.paper_to_cluster = paper_to_cluster
        self.paper_categories = paper_categories
        self.profiles = profiles

        # SPECTER2 loaded lazily (W0.1 runs in parallel)
        self.specter2_embeddings = specter2_embeddings
        self.specter2_id_to_idx = specter2_id_to_idx

    @classmethod
    def from_spike_data(
        cls,
        db_path: Optional[str] = None,
        minilm_emb_path: Optional[str] = None,
        minilm_ids_path: Optional[str] = None,
        profiles_path: Optional[str] = None,
        specter2_emb_path: Optional[str] = None,
        specter2_ids_path: Optional[str] = None,
        n_clusters: int = 48,
    ) -> "StrategyProfiler":
        """Construct from spike data file paths.

        Uses default paths from the spike data layout if not specified.
        Path resolution: profiler.py -> harness/ -> experiments/ -> 003-*/ -> spikes/
        """
        # harness/ -> experiments/ -> 003-strategy-profiling/ -> spikes/
        spikes_dir = Path(__file__).resolve().parent.parent.parent.parent

        # Default paths
        spike_001_data = spikes_dir / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
        spike_002_data = spikes_dir / "002-backend-comparison" / "experiments" / "data"
        spike_003_data = spikes_dir / "003-strategy-profiling" / "experiments" / "data"

        db_path = db_path or str(spike_001_data / "spike_001_harvest.db")
        minilm_emb_path = minilm_emb_path or str(spike_002_data / "embeddings_19k.npy")
        minilm_ids_path = minilm_ids_path or str(spike_002_data / "arxiv_ids_19k.json")
        profiles_path = profiles_path or str(spike_003_data / "interest_profiles.json")

        print(f"Loading corpus from {db_path}...")
        corpus = load_corpus_db(db_path)
        print(f"  {len(corpus)} papers loaded")

        print(f"Loading MiniLM embeddings from {minilm_emb_path}...")
        embeddings, paper_ids, id_to_idx = load_embeddings(minilm_emb_path, minilm_ids_path)
        print(f"  {embeddings.shape[0]} embeddings, dim={embeddings.shape[1]}")

        print("Computing cluster assignments (KMeans, n=48)...")
        cluster_labels = compute_clusters(embeddings, n_clusters=n_clusters)
        paper_to_cluster = build_paper_to_cluster(paper_ids, cluster_labels)
        print(f"  {n_clusters} clusters assigned")

        paper_categories = build_paper_categories(corpus)

        print(f"Loading interest profiles from {profiles_path}...")
        profiles = load_interest_profiles(profiles_path)
        if profiles:
            print(f"  {len(profiles)} profiles loaded:")
            for p in profiles:
                print(f"    {p.profile_id}: {p.name} ({p.breadth}, "
                      f"{len(p.seed_sets)} seed sets, "
                      f"{len(p.cluster_papers)} cluster papers, "
                      f"{len(p.held_out)} held out)")
        else:
            print("  No profiles found (W0.3 not yet complete)")

        # Load SPECTER2 if available
        specter2_emb = None
        specter2_id_to_idx = None
        specter2_emb_path = specter2_emb_path or str(spike_003_data / "specter2_adapter_19k.npy")
        specter2_ids_path = specter2_ids_path or minilm_ids_path  # Same paper order assumed

        if Path(specter2_emb_path).exists():
            print(f"Loading SPECTER2 embeddings from {specter2_emb_path}...")
            specter2_emb = np.load(specter2_emb_path)
            with open(specter2_ids_path) as f:
                specter2_ids = json.load(f)
            specter2_id_to_idx = {aid: i for i, aid in enumerate(specter2_ids)}
            print(f"  {specter2_emb.shape[0]} SPECTER2 embeddings, dim={specter2_emb.shape[1]}")
        else:
            print(f"  SPECTER2 not yet available at {specter2_emb_path}")

        return cls(
            corpus=corpus,
            embeddings=embeddings,
            paper_ids=paper_ids,
            id_to_idx=id_to_idx,
            paper_to_cluster=paper_to_cluster,
            paper_categories=paper_categories,
            profiles=profiles,
            specter2_embeddings=specter2_emb,
            specter2_id_to_idx=specter2_id_to_idx,
        )

    def profile(
        self,
        strategy,
        config: Optional[dict] = None,
        top_k: int = 20,
        run_loo: bool = True,
        measure_resources: bool = True,
        latency_n_runs: int = 100,
        profiles_override: Optional[list[InterestProfile]] = None,
    ) -> dict:
        """Run a strategy across all interest profiles, compute all instruments + resources.

        This is the main entry point. For each profile x seed_set combination,
        it runs the strategy and computes all 7 instruments. Then aggregates
        across seed sets (mean, std) for each profile, and across profiles
        for the overall score.

        Args:
            strategy: Implements RecommendationStrategy protocol.
            config: Optional config dict to include in the profile card.
            top_k: Number of recommendations per run.
            run_loo: Whether to run leave-one-out (expensive).
            measure_resources: Whether to measure latency/memory.
            latency_n_runs: Number of latency measurement runs.
            profiles_override: Use these profiles instead of self.profiles.

        Returns:
            A strategy profile card dict matching the schema in DESIGN.md.
        """
        profiles = profiles_override or self.profiles

        if not profiles:
            print("WARNING: No interest profiles available. Running with empty profile set.")
            return self._empty_card(strategy, config)

        profile_results = {}
        all_instrument_values = {
            "leave_one_out_mrr": [],
            "seed_proximity": [],
            "topical_coherence": [],
            "cluster_diversity": [],
            "novelty": [],
            "category_surprise": [],
            "coverage": [],
        }

        for prof in profiles:
            print(f"\n  Profile {prof.profile_id} ({prof.name}):")
            seed_set_results = []

            for si, seed_set in enumerate(prof.seed_sets):
                print(f"    Seed set {si+1}/{len(prof.seed_sets)} ({len(seed_set)} seeds)...", end=" ")

                # Run strategy
                recs = strategy.recommend(seed_set, top_k=top_k)
                rec_ids = [r[0] for r in recs]

                if not rec_ids:
                    print("no results")
                    seed_set_results.append(None)
                    continue

                # Run instruments
                instruments = run_all_instruments(
                    strategy=strategy,
                    recommended_ids=rec_ids,
                    seed_ids=seed_set,
                    cluster_papers=prof.cluster_papers,
                    all_paper_ids=self.paper_ids,
                    embeddings=self.embeddings,
                    id_to_idx=self.id_to_idx,
                    paper_to_cluster=self.paper_to_cluster,
                    paper_categories=self.paper_categories,
                    top_k=top_k,
                    run_loo=run_loo,
                )

                seed_set_results.append(instruments)

                # Collect values for aggregation
                for inst_name, inst_result in instruments.items():
                    val = inst_result.get("value")
                    if val is not None:
                        all_instrument_values[inst_name].append(val)

                # Brief progress indicator
                mrr_val = instruments["leave_one_out_mrr"].get("value")
                prox_val = instruments["seed_proximity"].get("value", 0)
                print(f"MRR={mrr_val}, prox={prox_val:.3f}" if mrr_val is not None else "done")

            # Aggregate across seed sets for this profile
            profile_results[prof.profile_id] = self._aggregate_seed_sets(
                seed_set_results, prof
            )

        # Aggregate across all profiles
        aggregated_instruments = self._aggregate_across_profiles(
            all_instrument_values
        )

        # Resource metrics
        resources = {}
        if measure_resources and profiles:
            print("\n  Measuring resources...")
            # Use first profile's first seed set for resource measurement
            test_seeds = profiles[0].seed_sets[0]
            resources = self._measure_resources(
                strategy, test_seeds, top_k, latency_n_runs
            )

        # Build profile card
        card = {
            "strategy_id": strategy.strategy_id,
            "strategy_name": strategy.name,
            "config": config or {},
            "instruments": aggregated_instruments,
            "by_profile": profile_results,
            "resources": resources,
            "qualitative": {},  # Populated by qualitative review (later waves)
            "metadata": {
                "evaluated_at": datetime.now(timezone.utc).isoformat(),
                "n_profiles": len(profiles),
                "n_seed_sets_per_profile": len(profiles[0].seed_sets) if profiles else 0,
                "top_k": top_k,
                "corpus_size": len(self.paper_ids),
                "embedding_dim": self.embeddings.shape[1],
                "n_clusters": len(set(self.paper_to_cluster.values())),
            },
        }

        return card

    def _aggregate_seed_sets(
        self, seed_set_results: list, profile: InterestProfile
    ) -> dict:
        """Aggregate instrument values across seed sets for one profile."""
        instrument_names = [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]

        aggregated = {}
        for inst_name in instrument_names:
            values = []
            for ssr in seed_set_results:
                if ssr is None:
                    continue
                val = ssr.get(inst_name, {}).get("value")
                if val is not None:
                    values.append(val)

            if values:
                aggregated[inst_name] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "values": values,
                    "interpretation": "",  # Filled by qualitative review
                }
            else:
                aggregated[inst_name] = {"mean": None, "std": None, "values": []}

        return {
            "profile_id": profile.profile_id,
            "profile_name": profile.name,
            "breadth": profile.breadth,
            "instruments": aggregated,
        }

    def _aggregate_across_profiles(
        self, all_values: dict[str, list[float]]
    ) -> dict:
        """Aggregate instrument values across all profiles."""
        aggregated = {}
        for inst_name, values in all_values.items():
            if values:
                aggregated[inst_name] = {
                    "mean": float(np.mean(values)),
                    "std": float(np.std(values)),
                    "n_observations": len(values),
                    "interpretation": "",  # Filled by qualitative review
                    "by_profile": {},  # Filled per-profile above
                }
            else:
                aggregated[inst_name] = {
                    "mean": None,
                    "std": None,
                    "n_observations": 0,
                }

        return aggregated

    def _measure_resources(
        self, strategy, seed_ids: list[str], top_k: int, n_runs: int
    ) -> dict:
        """Measure resource consumption of the strategy."""
        latency = measure_latency(
            strategy_fn=strategy.recommend,
            seed_ids=seed_ids,
            top_k=top_k,
            n_warmup=5,
            n_runs=n_runs,
        )

        return {
            "query_latency_ms": {
                "p50": latency["p50_ms"],
                "p95": latency["p95_ms"],
                "mean": latency["mean_ms"],
            },
            # These require strategy-specific measurement functions:
            "index_time_s": None,  # Measured per-strategy in wave code
            "incremental_update_ms": None,
            "memory_mb": None,
            "storage_mb": None,
            "api_cost_per_paper": None,
            "gpu_required": None,
            "gpu_speedup": None,
        }

    def _empty_card(self, strategy, config: Optional[dict]) -> dict:
        """Return a skeleton profile card when no profiles are available."""
        return {
            "strategy_id": strategy.strategy_id,
            "strategy_name": strategy.name,
            "config": config or {},
            "instruments": {},
            "by_profile": {},
            "resources": {},
            "qualitative": {},
            "metadata": {
                "evaluated_at": datetime.now(timezone.utc).isoformat(),
                "n_profiles": 0,
                "note": "No interest profiles available. Run W0.3 first.",
            },
        }

    def compare(self, cards: list[dict]) -> dict:
        """Side-by-side comparison of multiple strategy profile cards.

        Produces a comparison table with per-instrument rankings
        and a summary of which strategy leads on which dimension.

        Args:
            cards: List of profile card dicts from profile() calls.

        Returns:
            Comparison report dict.
        """
        if not cards:
            return {"error": "no cards to compare"}

        instrument_names = [
            "leave_one_out_mrr", "seed_proximity", "topical_coherence",
            "cluster_diversity", "novelty", "category_surprise", "coverage",
        ]

        comparison = {
            "strategies": [
                {"id": c["strategy_id"], "name": c["strategy_name"]}
                for c in cards
            ],
            "instruments": {},
            "resources": {},
            "rankings": {},
        }

        # Compare instruments
        for inst_name in instrument_names:
            values = []
            for card in cards:
                inst = card.get("instruments", {}).get(inst_name, {})
                values.append({
                    "strategy_id": card["strategy_id"],
                    "mean": inst.get("mean"),
                    "std": inst.get("std"),
                })

            # Rank (higher is "more" of this property -- not necessarily better)
            sorted_vals = sorted(
                [v for v in values if v["mean"] is not None],
                key=lambda x: x["mean"],
                reverse=True,
            )

            comparison["instruments"][inst_name] = {
                "values": values,
                "ranking": [v["strategy_id"] for v in sorted_vals],
            }

        # Compare resources (latency: lower is better)
        for card in cards:
            res = card.get("resources", {})
            latency = res.get("query_latency_ms", {})
            comparison["resources"][card["strategy_id"]] = {
                "p50_ms": latency.get("p50"),
                "p95_ms": latency.get("p95"),
            }

        # Per-profile comparison
        comparison["by_profile"] = {}
        all_profile_ids = set()
        for card in cards:
            for pid in card.get("by_profile", {}):
                all_profile_ids.add(pid)

        for pid in sorted(all_profile_ids):
            profile_comparison = {}
            for inst_name in instrument_names:
                vals = []
                for card in cards:
                    prof_data = card.get("by_profile", {}).get(pid, {})
                    inst_data = prof_data.get("instruments", {}).get(inst_name, {})
                    vals.append({
                        "strategy_id": card["strategy_id"],
                        "mean": inst_data.get("mean"),
                    })
                profile_comparison[inst_name] = vals
            comparison["by_profile"][pid] = profile_comparison

        comparison["generated_at"] = datetime.now(timezone.utc).isoformat()

        return comparison


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

def _smoke_test():
    """Quick smoke test with random baseline strategy.

    Tests that the harness machinery works end-to-end, not that
    any strategy produces good results.
    """
    print("=" * 60)
    print("SMOKE TEST: StrategyProfiler with RandomBaseline")
    print("=" * 60)

    from .strategy_protocol import RandomBaseline

    # Try to load real data
    try:
        profiler = StrategyProfiler.from_spike_data()
    except Exception as e:
        print(f"\nCannot load spike data: {e}")
        print("Running with synthetic data instead.\n")

        # Synthetic fallback
        n_papers = 200
        dim = 384
        rng = np.random.RandomState(42)
        embeddings = rng.randn(n_papers, dim).astype(np.float32)
        # Normalize
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        embeddings = embeddings / norms

        paper_ids = [f"test.{i:04d}" for i in range(n_papers)]
        id_to_idx = {aid: i for i, aid in enumerate(paper_ids)}

        from sklearn.cluster import MiniBatchKMeans
        labels = MiniBatchKMeans(n_clusters=10, random_state=42).fit_predict(embeddings)
        paper_to_cluster = {aid: int(labels[i]) for i, aid in enumerate(paper_ids)}
        paper_categories = {aid: f"cs.{chr(65 + i % 5)}{chr(65 + i % 3)}" for i, aid in enumerate(paper_ids)}

        corpus = {
            aid: {
                "title": f"Test paper {aid}",
                "abstract": f"Abstract for {aid}",
                "primary_category": paper_categories[aid],
            }
            for aid in paper_ids
        }

        # Create a synthetic profile
        cluster_0_papers = [aid for aid, c in paper_to_cluster.items() if c == 0]
        profile = InterestProfile(
            profile_id="T1",
            name="Test profile",
            description="Synthetic test",
            breadth="medium",
            seed_sets=[cluster_0_papers[:5], cluster_0_papers[5:10]],
            cluster_papers=cluster_0_papers,
            held_out=cluster_0_papers[10:15] if len(cluster_0_papers) > 15 else [],
        )

        profiler = StrategyProfiler(
            corpus=corpus,
            embeddings=embeddings,
            paper_ids=paper_ids,
            id_to_idx=id_to_idx,
            paper_to_cluster=paper_to_cluster,
            paper_categories=paper_categories,
            profiles=[profile],
        )

    # Create random baseline
    random_strat = RandomBaseline(profiler.paper_ids, seed=42)

    # Profile it
    print(f"\nProfiling: {random_strat.name} ({random_strat.strategy_id})")
    card = profiler.profile(
        random_strat,
        config={"type": "random_baseline"},
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=50,
    )

    # Print summary
    print("\n" + "=" * 60)
    print("PROFILE CARD SUMMARY")
    print("=" * 60)
    print(f"Strategy: {card['strategy_name']} ({card['strategy_id']})")
    print(f"Profiles evaluated: {card['metadata'].get('n_profiles', 0)}")

    print("\nInstruments (aggregate):")
    for inst_name, inst_data in card.get("instruments", {}).items():
        mean = inst_data.get("mean")
        std = inst_data.get("std")
        if mean is not None:
            print(f"  {inst_name:<25s} mean={mean:.4f}  std={std:.4f}")
        else:
            print(f"  {inst_name:<25s} (no data)")

    print("\nResources:")
    res = card.get("resources", {})
    latency = res.get("query_latency_ms", {})
    if latency:
        print(f"  Latency p50={latency.get('p50', '?'):.2f}ms  p95={latency.get('p95', '?'):.2f}ms")

    print("\nPer-profile breakdown:")
    for pid, pdata in card.get("by_profile", {}).items():
        print(f"  {pid} ({pdata.get('profile_name', '?')}):")
        for inst_name, inst_data in pdata.get("instruments", {}).items():
            mean = inst_data.get("mean")
            if mean is not None:
                print(f"    {inst_name:<23s} {mean:.4f}")

    # Validate card structure
    required_top_keys = {"strategy_id", "strategy_name", "config", "instruments", "resources", "metadata"}
    missing = required_top_keys - set(card.keys())
    if missing:
        print(f"\nWARNING: Missing top-level keys: {missing}")
    else:
        print("\nProfile card structure: VALID")

    print("\nSmoke test PASSED")
    return card


if __name__ == "__main__":
    _smoke_test()
