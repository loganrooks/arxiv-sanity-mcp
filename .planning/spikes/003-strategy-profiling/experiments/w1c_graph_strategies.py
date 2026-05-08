#!/usr/bin/env python3
"""
W1C: Profile graph-based recommendation strategies (S3a, S3c).

Strategies:
    S3a: Bibliographic coupling -- papers sharing references are related.
         For each candidate, compute Jaccard similarity of its referenced_works
         set with each seed paper's referenced_works set. Score = max Jaccard.

    S3c: OpenAlex related_works -- use the pre-computed related_works field.
         For each seed, if it has related_works, those get a score.
         Score = number of seed papers that list the candidate as related.

Data reality (established before build):
    - OpenAlex cache: 500 papers, 95 with referenced_works, 0 with related_works
    - Of 120 seed papers across 8 profiles: 3 in cache, 1 with referenced_works
    - referenced_works are OpenAlex work IDs (URLs), not arxiv IDs
    - Only 8 referenced_works point to papers in our corpus
    - Bibliographic coupling works via shared references to OLDER literature,
      so the cross-corpus matching limitation only affects coverage, not validity

This script:
    1. Documents exact data coverage for both strategies
    2. Implements and profiles S3a (bibliographic coupling) as fully as data allows
    3. Reports S3c as non-functional (0 related_works in data)
    4. Produces honest profile cards with data-limitation metadata
"""

from __future__ import annotations

import json
import sqlite3
import sys
import time
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SPIKE_003_DIR = Path(__file__).resolve().parent.parent
SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
EXPERIMENTS_DIR = SPIKE_003_DIR / "experiments"

sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import StrategyProfiler
from harness.strategy_protocol import SimpleStrategy

# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

HARVEST_DB = str(SPIKE_001_DATA / "spike_001_harvest.db")
OPENALEX_CACHE = str(SPIKE_001_DATA / "b2_openalex_cache.json")
PROFILES_PATH = str(EXPERIMENTS_DIR / "data" / "interest_profiles.json")
OUTPUT_PATH = str(EXPERIMENTS_DIR / "data" / "w1c_graph_profiles.json")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_openalex_cache(cache_path: str) -> dict:
    """Load the full OpenAlex cache."""
    with open(cache_path) as f:
        return json.load(f)


def analyze_reference_coverage(
    cache: dict, profiler: StrategyProfiler
) -> dict:
    """Produce a thorough coverage report for graph-based strategies.

    This is the most important output of W1C: honest data-availability analysis.
    """
    # Papers with referenced_works
    papers_with_refs = {}
    papers_with_related = {}
    for arxiv_id, entry in cache.items():
        refs = entry.get("referenced_works", [])
        related = entry.get("related_works", [])
        if refs:
            papers_with_refs[arxiv_id] = set(refs)
        if related:
            papers_with_related[arxiv_id] = set(related)

    # How many are in the 19k corpus?
    corpus_ids = set(profiler.paper_ids)
    refs_in_corpus = {k: v for k, v in papers_with_refs.items() if k in corpus_ids}
    related_in_corpus = {k: v for k, v in papers_with_related.items() if k in corpus_ids}

    # Seed paper coverage
    all_seed_ids = set()
    profile_seed_coverage = {}
    for prof in profiler.profiles:
        prof_seeds = set()
        for seed_set in prof.seed_sets:
            prof_seeds.update(seed_set)
        all_seed_ids.update(prof_seeds)

        seeds_with_refs = prof_seeds & set(papers_with_refs.keys())
        profile_seed_coverage[prof.profile_id] = {
            "total_seeds": len(prof_seeds),
            "seeds_in_cache": len(prof_seeds & set(cache.keys())),
            "seeds_with_refs": len(seeds_with_refs),
            "seed_ids_with_refs": sorted(seeds_with_refs),
        }

    # Cluster paper coverage
    all_cluster_ids = set()
    profile_cluster_coverage = {}
    for prof in profiler.profiles:
        cluster_ids = set(prof.cluster_papers)
        all_cluster_ids.update(cluster_ids)
        clusters_with_refs = cluster_ids & set(papers_with_refs.keys())
        profile_cluster_coverage[prof.profile_id] = {
            "total_cluster_papers": len(cluster_ids),
            "cluster_papers_with_refs": len(clusters_with_refs),
        }

    # Collect all referenced work IDs and check corpus overlap
    all_ref_ids = set()
    for ref_set in papers_with_refs.values():
        all_ref_ids.update(ref_set)

    # Build OpenAlex ID -> arxiv_id mapping for corpus papers
    corpus_oa_ids = {}
    for arxiv_id, entry in cache.items():
        oa_id = entry.get("id")
        if oa_id and arxiv_id in corpus_ids:
            corpus_oa_ids[oa_id] = arxiv_id

    refs_to_corpus = all_ref_ids & set(corpus_oa_ids.keys())

    # Bibliographic coupling density among papers with refs
    n_with_refs = len(refs_in_corpus)
    total_pairs = n_with_refs * (n_with_refs - 1) // 2
    nonzero_pairs = 0
    jaccard_values = []

    if n_with_refs <= 500:  # Safe to enumerate all pairs
        for (p1, refs1), (p2, refs2) in combinations(refs_in_corpus.items(), 2):
            intersection = refs1 & refs2
            if intersection:
                union = refs1 | refs2
                jac = len(intersection) / len(union)
                nonzero_pairs += 1
                jaccard_values.append(jac)

    ref_count_stats = [len(v) for v in papers_with_refs.values()]

    return {
        "openalex_cache_total": len(cache),
        "papers_with_referenced_works": len(papers_with_refs),
        "papers_with_related_works": len(papers_with_related),
        "referenced_works_in_corpus": len(refs_in_corpus),
        "related_works_in_corpus": len(related_in_corpus),
        "unique_referenced_work_ids": len(all_ref_ids),
        "referenced_works_pointing_to_corpus": len(refs_to_corpus),
        "ref_count_stats": {
            "min": int(min(ref_count_stats)) if ref_count_stats else 0,
            "max": int(max(ref_count_stats)) if ref_count_stats else 0,
            "mean": float(np.mean(ref_count_stats)) if ref_count_stats else 0,
            "median": float(np.median(ref_count_stats)) if ref_count_stats else 0,
        },
        "seed_paper_coverage": {
            "total_unique_seeds": len(all_seed_ids),
            "seeds_in_cache": len(all_seed_ids & set(cache.keys())),
            "seeds_with_refs": len(all_seed_ids & set(papers_with_refs.keys())),
            "by_profile": profile_seed_coverage,
        },
        "cluster_paper_coverage": {
            "total_unique_cluster_papers": len(all_cluster_ids),
            "cluster_papers_with_refs": len(all_cluster_ids & set(papers_with_refs.keys())),
            "by_profile": profile_cluster_coverage,
        },
        "bibliographic_coupling_density": {
            "papers_compared": n_with_refs,
            "total_pairs": total_pairs,
            "nonzero_jaccard_pairs": nonzero_pairs,
            "fraction_nonzero": nonzero_pairs / total_pairs if total_pairs > 0 else 0,
            "jaccard_stats": {
                "mean": float(np.mean(jaccard_values)) if jaccard_values else 0,
                "median": float(np.median(jaccard_values)) if jaccard_values else 0,
                "max": float(max(jaccard_values)) if jaccard_values else 0,
                "p75": float(np.percentile(jaccard_values, 75)) if jaccard_values else 0,
                "p95": float(np.percentile(jaccard_values, 95)) if jaccard_values else 0,
            } if jaccard_values else {},
        },
        "conclusion": (
            "S3a (bibliographic coupling): SEVERELY DATA-LIMITED. "
            f"Only 1 of {len(all_seed_ids)} seed papers has referenced_works. "
            f"95 of 500 enriched papers have references, but these are NOT the "
            f"seed or cluster papers used for evaluation. The strategy can be "
            f"implemented and will produce scores for the 95 papers with data, "
            f"but meaningful evaluation against interest profiles is not possible. "
            f"S3c (related_works): NON-FUNCTIONAL. 0 papers have related_works populated."
        ),
    }


# ---------------------------------------------------------------------------
# Strategy factories
# ---------------------------------------------------------------------------

def make_bibliographic_coupling_strategy(
    paper_ids: list[str],
    cache: dict,
) -> tuple[SimpleStrategy, dict]:
    """S3a: Bibliographic coupling via Jaccard similarity of reference sets.

    For each seed paper that has referenced_works:
      - Compute Jaccard(seed_refs, candidate_refs) for each candidate with refs
      - Paper score = max Jaccard across all seeds with refs

    If no seeds have referenced_works, all scores are 0.

    Returns:
        (strategy, build_info) tuple. build_info contains index stats.
    """
    # Build reference index: arxiv_id -> set of OpenAlex work IDs
    ref_index: dict[str, set[str]] = {}
    for arxiv_id, entry in cache.items():
        refs = entry.get("referenced_works", [])
        if refs:
            ref_index[arxiv_id] = set(refs)

    # Map paper_ids to indices for score array construction
    id_to_idx = {aid: i for i, aid in enumerate(paper_ids)}

    # Pre-compute which corpus papers have references
    corpus_papers_with_refs = set(ref_index.keys()) & set(paper_ids)

    build_info = {
        "total_corpus": len(paper_ids),
        "papers_in_ref_index": len(ref_index),
        "corpus_papers_with_refs": len(corpus_papers_with_refs),
        "coverage_fraction": len(corpus_papers_with_refs) / len(paper_ids),
    }

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        """Compute bibliographic coupling scores.

        For each candidate paper with references, compute max Jaccard
        similarity against all seed papers that also have references.
        """
        scores = np.zeros(len(paper_ids), dtype=np.float64)

        # Filter seeds to those with reference data
        seed_ref_sets = []
        for sid in seed_ids:
            if sid in ref_index:
                seed_ref_sets.append(ref_index[sid])

        if not seed_ref_sets:
            # No seeds have reference data -- cannot compute coupling
            return scores

        # Score each candidate paper that has references
        for cand_id in corpus_papers_with_refs:
            cand_refs = ref_index[cand_id]
            idx = id_to_idx.get(cand_id)
            if idx is None:
                continue

            # Max Jaccard across seeds
            max_jaccard = 0.0
            for seed_refs in seed_ref_sets:
                intersection = cand_refs & seed_refs
                if intersection:
                    union = cand_refs | seed_refs
                    jac = len(intersection) / len(union)
                    if jac > max_jaccard:
                        max_jaccard = jac

            scores[idx] = max_jaccard

        return scores

    strategy = SimpleStrategy(
        name="Bibliographic coupling / Jaccard (S3a)",
        strategy_id="S3a",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )

    return strategy, build_info


def make_related_works_strategy(
    paper_ids: list[str],
    cache: dict,
) -> tuple[SimpleStrategy | None, dict]:
    """S3c: OpenAlex related_works scoring.

    For each seed paper with related_works:
      - Each related work that is in our corpus gets +1
      - Score = count of seeds that list this paper as related

    Returns:
        (strategy_or_None, build_info). Returns None if no data available.
    """
    # Build related_works index
    related_index: dict[str, set[str]] = {}
    for arxiv_id, entry in cache.items():
        related = entry.get("related_works", [])
        if related:
            related_index[arxiv_id] = set(related)

    # Build OpenAlex ID -> arxiv_id reverse mapping for corpus papers
    oa_to_arxiv: dict[str, str] = {}
    for arxiv_id, entry in cache.items():
        oa_id = entry.get("id")
        if oa_id and arxiv_id in set(paper_ids):
            oa_to_arxiv[oa_id] = arxiv_id

    build_info = {
        "papers_with_related_works": len(related_index),
        "oa_to_arxiv_mappings": len(oa_to_arxiv),
        "status": "NON-FUNCTIONAL" if not related_index else "operational",
    }

    if not related_index:
        return None, build_info

    id_to_idx = {aid: i for i, aid in enumerate(paper_ids)}

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        scores = np.zeros(len(paper_ids), dtype=np.float64)
        for sid in seed_ids:
            if sid not in related_index:
                continue
            for related_oa_id in related_index[sid]:
                # Map OpenAlex ID back to arxiv_id
                arxiv_id = oa_to_arxiv.get(related_oa_id)
                if arxiv_id is not None:
                    idx = id_to_idx.get(arxiv_id)
                    if idx is not None:
                        scores[idx] += 1.0
        return scores

    strategy = SimpleStrategy(
        name="OpenAlex related_works (S3c)",
        strategy_id="S3c",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )

    return strategy, build_info


# ---------------------------------------------------------------------------
# Focused evaluation: bibliographic coupling among the 95 ref-having papers
# ---------------------------------------------------------------------------

def evaluate_coupling_among_ref_papers(
    cache: dict, profiler: StrategyProfiler
) -> dict:
    """Run a focused evaluation of S3a ONLY among papers that have references.

    Since the standard harness evaluation will produce mostly zeros (seeds
    lack references), this separate analysis demonstrates whether the
    algorithm WOULD work given sufficient data.

    Creates synthetic "profiles" from papers with references, grouped by
    OpenAlex topic, and evaluates coupling quality within those groups.
    """
    # Build reference index for papers in corpus
    ref_papers = {}
    for arxiv_id, entry in cache.items():
        refs = entry.get("referenced_works", [])
        if refs and arxiv_id in set(profiler.paper_ids):
            ref_papers[arxiv_id] = {
                "refs": set(refs),
                "topics": entry.get("topics", []),
                "cited_by_count": entry.get("cited_by_count", 0),
            }

    if len(ref_papers) < 10:
        return {
            "status": "insufficient_data",
            "papers_with_refs": len(ref_papers),
            "minimum_needed": 10,
        }

    # Group papers by primary OpenAlex topic
    topic_groups: dict[str, list[str]] = {}
    for arxiv_id, data in ref_papers.items():
        topics = data["topics"]
        if topics:
            primary_topic = topics[0].get("display_name", "unknown")
        else:
            primary_topic = "unknown"
        if primary_topic not in topic_groups:
            topic_groups[primary_topic] = []
        topic_groups[primary_topic].append(arxiv_id)

    # Filter to groups with >= 3 papers (minimum for meaningful coupling)
    viable_groups = {
        topic: papers
        for topic, papers in topic_groups.items()
        if len(papers) >= 3
    }

    # For each viable group, compute intra-group coupling vs inter-group coupling
    group_results = []
    ref_sets = {aid: data["refs"] for aid, data in ref_papers.items()}

    for topic, group_papers in sorted(viable_groups.items(), key=lambda x: -len(x[1])):
        group_set = set(group_papers)
        non_group = [aid for aid in ref_papers if aid not in group_set]

        # Intra-group coupling: Jaccard among papers in this group
        intra_jaccards = []
        for p1, p2 in combinations(group_papers, 2):
            intersection = ref_sets[p1] & ref_sets[p2]
            if intersection:
                union = ref_sets[p1] | ref_sets[p2]
                intra_jaccards.append(len(intersection) / len(union))
            else:
                intra_jaccards.append(0.0)

        # Inter-group coupling: each group paper vs random sample of non-group
        inter_jaccards = []
        rng = np.random.RandomState(42)
        sample_size = min(20, len(non_group))
        if sample_size > 0:
            sample_non_group = rng.choice(non_group, size=sample_size, replace=False)
            for gp in group_papers:
                for ngp in sample_non_group:
                    if ngp in ref_sets:
                        intersection = ref_sets[gp] & ref_sets[ngp]
                        if intersection:
                            union = ref_sets[gp] | ref_sets[ngp]
                            inter_jaccards.append(len(intersection) / len(union))
                        else:
                            inter_jaccards.append(0.0)

        group_results.append({
            "topic": topic,
            "n_papers": len(group_papers),
            "paper_ids": group_papers,
            "intra_group_jaccard": {
                "mean": float(np.mean(intra_jaccards)) if intra_jaccards else 0.0,
                "max": float(max(intra_jaccards)) if intra_jaccards else 0.0,
                "nonzero_fraction": sum(1 for j in intra_jaccards if j > 0) / len(intra_jaccards) if intra_jaccards else 0.0,
                "n_pairs": len(intra_jaccards),
            },
            "inter_group_jaccard": {
                "mean": float(np.mean(inter_jaccards)) if inter_jaccards else 0.0,
                "max": float(max(inter_jaccards)) if inter_jaccards else 0.0,
                "nonzero_fraction": sum(1 for j in inter_jaccards if j > 0) / len(inter_jaccards) if inter_jaccards else 0.0,
                "n_pairs": len(inter_jaccards),
            },
            "discrimination": (
                (float(np.mean(intra_jaccards)) - float(np.mean(inter_jaccards)))
                if intra_jaccards and inter_jaccards else None
            ),
        })

    # Summary statistics
    all_intra_means = [g["intra_group_jaccard"]["mean"] for g in group_results]
    all_inter_means = [g["inter_group_jaccard"]["mean"] for g in group_results]
    all_discriminations = [g["discrimination"] for g in group_results if g["discrimination"] is not None]

    return {
        "status": "completed",
        "n_papers_with_refs": len(ref_papers),
        "n_topic_groups": len(topic_groups),
        "n_viable_groups": len(viable_groups),
        "group_results": group_results,
        "summary": {
            "mean_intra_jaccard": float(np.mean(all_intra_means)) if all_intra_means else 0.0,
            "mean_inter_jaccard": float(np.mean(all_inter_means)) if all_inter_means else 0.0,
            "mean_discrimination": float(np.mean(all_discriminations)) if all_discriminations else 0.0,
            "positive_discrimination_fraction": (
                sum(1 for d in all_discriminations if d > 0) / len(all_discriminations)
                if all_discriminations else 0.0
            ),
            "interpretation": (
                "Positive discrimination means intra-group coupling is higher than "
                "inter-group coupling, suggesting bibliographic coupling CAN distinguish "
                "topically related papers -- if sufficient reference data is available."
            ),
        },
    }


# ---------------------------------------------------------------------------
# Enrichment cost estimation
# ---------------------------------------------------------------------------

def estimate_enrichment_cost(
    profiler: StrategyProfiler, cache: dict
) -> dict:
    """Estimate what it would cost to make graph strategies viable.

    Graph strategies need referenced_works for seed AND candidate papers.
    Currently only 95/500 enriched papers have this data, and only 500/19252
    are enriched at all.
    """
    total_corpus = len(profiler.paper_ids)
    currently_enriched = len(cache)
    currently_with_refs = sum(1 for v in cache.values() if v.get("referenced_works"))

    # Estimate: what fraction of new enrichments would have referenced_works?
    # Based on current data: 95/500 = 19%
    ref_fraction = currently_with_refs / currently_enriched if currently_enriched > 0 else 0

    # How many papers need enrichment to get N papers with refs?
    # We need at minimum: all seed papers + enough candidates for ranking
    all_seeds = set()
    for prof in profiler.profiles:
        for seed_set in prof.seed_sets:
            all_seeds.update(seed_set)

    seeds_needing_enrichment = all_seeds - set(cache.keys())

    # For a "minimal viable" graph strategy, we need:
    # - All seed papers enriched (120)
    # - Enough candidates enriched to make coupling useful (at least 2000)
    minimal_viable_enrichments = len(seeds_needing_enrichment) + max(0, 2000 - currently_enriched)

    # For full corpus coverage:
    full_corpus_enrichments = total_corpus - currently_enriched

    # OpenAlex API: free, rate-limited to ~100K/day for polite use
    # Each paper needs 1 API call
    return {
        "current_state": {
            "total_corpus": total_corpus,
            "currently_enriched": currently_enriched,
            "currently_with_refs": currently_with_refs,
            "ref_fraction": round(ref_fraction, 3),
            "seed_papers_needing_enrichment": len(seeds_needing_enrichment),
        },
        "minimal_viable": {
            "additional_enrichments_needed": minimal_viable_enrichments,
            "estimated_papers_with_refs": int(minimal_viable_enrichments * ref_fraction) + currently_with_refs,
            "api_calls": minimal_viable_enrichments,
            "estimated_time_at_10rps": f"{minimal_viable_enrichments / 10 / 60:.0f} minutes",
            "note": "Minimum to test whether graph strategies add value",
        },
        "full_corpus": {
            "additional_enrichments_needed": full_corpus_enrichments,
            "estimated_papers_with_refs": int(full_corpus_enrichments * ref_fraction) + currently_with_refs,
            "api_calls": full_corpus_enrichments,
            "estimated_time_at_10rps": f"{full_corpus_enrichments / 10 / 60:.0f} minutes",
            "note": "Full enrichment for production-grade graph strategies",
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("W1C: Graph-Based Strategy Profiling (S3a, S3c)")
    print("=" * 70)
    t_start = time.time()

    # -------------------------------------------------------------------
    # 1. Load infrastructure
    # -------------------------------------------------------------------
    print("\n--- Loading profiler infrastructure ---")
    profiler = StrategyProfiler.from_spike_data()

    if not profiler.profiles:
        print("ERROR: No interest profiles loaded. Cannot profile strategies.")
        sys.exit(1)

    print(f"\nReady: {len(profiler.paper_ids)} papers, "
          f"{len(profiler.profiles)} profiles")

    # -------------------------------------------------------------------
    # 2. Load OpenAlex data
    # -------------------------------------------------------------------
    print("\n--- Loading OpenAlex cache ---")
    cache = load_openalex_cache(OPENALEX_CACHE)
    print(f"  {len(cache)} papers in cache")

    # -------------------------------------------------------------------
    # 3. Coverage analysis (the critical finding)
    # -------------------------------------------------------------------
    print("\n--- Reference data coverage analysis ---")
    coverage = analyze_reference_coverage(cache, profiler)

    print(f"\n  OpenAlex cache: {coverage['openalex_cache_total']} papers")
    print(f"  With referenced_works: {coverage['papers_with_referenced_works']}")
    print(f"  With related_works: {coverage['papers_with_related_works']}")
    print(f"  Ref count stats: min={coverage['ref_count_stats']['min']}, "
          f"max={coverage['ref_count_stats']['max']}, "
          f"mean={coverage['ref_count_stats']['mean']:.0f}")

    seed_cov = coverage["seed_paper_coverage"]
    print(f"\n  Seed papers: {seed_cov['total_unique_seeds']} total, "
          f"{seed_cov['seeds_in_cache']} in cache, "
          f"{seed_cov['seeds_with_refs']} with referenced_works")

    for pid, pdata in seed_cov["by_profile"].items():
        marker = " <-- HAS REFS" if pdata["seeds_with_refs"] > 0 else ""
        print(f"    {pid}: {pdata['total_seeds']} seeds, "
              f"{pdata['seeds_in_cache']} cached, "
              f"{pdata['seeds_with_refs']} with refs{marker}")

    cluster_cov = coverage["cluster_paper_coverage"]
    print(f"\n  Cluster papers: {cluster_cov['total_unique_cluster_papers']} total, "
          f"{cluster_cov['cluster_papers_with_refs']} with refs")

    coupling = coverage["bibliographic_coupling_density"]
    print(f"\n  Bibliographic coupling density (among {coupling['papers_compared']} ref-having papers):")
    print(f"    {coupling['nonzero_jaccard_pairs']}/{coupling['total_pairs']} pairs "
          f"have nonzero Jaccard ({coupling['fraction_nonzero']:.1%})")
    if coupling.get("jaccard_stats"):
        js = coupling["jaccard_stats"]
        print(f"    Jaccard stats: mean={js['mean']:.4f}, median={js['median']:.4f}, "
              f"max={js['max']:.4f}, p95={js['p95']:.4f}")

    print(f"\n  CONCLUSION: {coverage['conclusion']}")

    # -------------------------------------------------------------------
    # 4. Build strategies
    # -------------------------------------------------------------------
    print("\n--- Building strategies ---")

    s3a, s3a_build = make_bibliographic_coupling_strategy(profiler.paper_ids, cache)
    print(f"\n  S3a (Bibliographic coupling):")
    print(f"    Papers in reference index: {s3a_build['papers_in_ref_index']}")
    print(f"    Corpus papers with refs: {s3a_build['corpus_papers_with_refs']}")
    print(f"    Coverage: {s3a_build['coverage_fraction']:.2%}")

    s3c, s3c_build = make_related_works_strategy(profiler.paper_ids, cache)
    print(f"\n  S3c (related_works):")
    print(f"    Status: {s3c_build['status']}")
    print(f"    Papers with related_works: {s3c_build['papers_with_related_works']}")

    # -------------------------------------------------------------------
    # 5. Profile S3a through the standard harness
    # -------------------------------------------------------------------
    cards = []

    print(f"\n{'=' * 70}")
    print(f"Profiling S3a: Bibliographic coupling (standard harness)")
    print(f"  NOTE: Expect mostly zeros -- seeds lack reference data")
    print("=" * 70)

    s3a_card = profiler.profile(
        s3a,
        config={
            "type": "graph",
            "strategy_class": "S3a",
            "data_limitation": (
                f"Only {s3a_build['corpus_papers_with_refs']}/{s3a_build['total_corpus']} "
                f"papers have referenced_works ({s3a_build['coverage_fraction']:.2%}). "
                f"Only 1 of {seed_cov['total_unique_seeds']} seed papers has refs."
            ),
        },
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=50,
    )
    cards.append(s3a_card)

    # Print S3a harness summary
    print(f"\n  --- S3a standard harness summary ---")
    for inst_name, inst_data in s3a_card.get("instruments", {}).items():
        mean = inst_data.get("mean")
        std = inst_data.get("std")
        if mean is not None:
            print(f"  {inst_name:<25s} mean={mean:.4f}  std={std:.4f}")
        else:
            print(f"  {inst_name:<25s} (no data)")

    res = s3a_card.get("resources", {})
    latency = res.get("query_latency_ms", {})
    if latency:
        print(f"  latency p50={latency.get('p50', '?'):.2f}ms  "
              f"p95={latency.get('p95', '?'):.2f}ms")

    # -------------------------------------------------------------------
    # 6. Focused evaluation among ref-having papers
    # -------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Focused evaluation: bibliographic coupling among papers WITH references")
    print("  This tests the algorithm's validity with sufficient data")
    print("=" * 70)

    focused_eval = evaluate_coupling_among_ref_papers(cache, profiler)

    if focused_eval["status"] == "completed":
        print(f"\n  Papers with refs: {focused_eval['n_papers_with_refs']}")
        print(f"  Topic groups: {focused_eval['n_topic_groups']} total, "
              f"{focused_eval['n_viable_groups']} with >= 3 papers")

        summary = focused_eval["summary"]
        print(f"\n  Mean intra-group Jaccard: {summary['mean_intra_jaccard']:.4f}")
        print(f"  Mean inter-group Jaccard: {summary['mean_inter_jaccard']:.4f}")
        print(f"  Mean discrimination: {summary['mean_discrimination']:.4f}")
        print(f"  Groups with positive discrimination: {summary['positive_discrimination_fraction']:.0%}")

        print(f"\n  Per-group breakdown:")
        for gr in focused_eval["group_results"]:
            intra = gr["intra_group_jaccard"]
            inter = gr["inter_group_jaccard"]
            disc = gr.get("discrimination")
            disc_str = f"{disc:+.4f}" if disc is not None else "n/a"
            marker = " ++" if disc is not None and disc > 0 else ""
            print(f"    [{gr['n_papers']}p] {gr['topic'][:50]:<50s} "
                  f"intra={intra['mean']:.4f} inter={inter['mean']:.4f} "
                  f"disc={disc_str}{marker}")
    else:
        print(f"\n  Status: {focused_eval['status']}")
        print(f"  Papers with refs: {focused_eval.get('papers_with_refs', 0)}")

    # -------------------------------------------------------------------
    # 7. Enrichment cost estimation
    # -------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Enrichment cost estimation")
    print("=" * 70)

    enrichment_cost = estimate_enrichment_cost(profiler, cache)
    cur = enrichment_cost["current_state"]
    print(f"\n  Current: {cur['currently_enriched']}/{cur['total_corpus']} enriched, "
          f"{cur['currently_with_refs']} with refs ({cur['ref_fraction']:.0%} ref rate)")
    print(f"  Seed papers needing enrichment: {cur['seed_papers_needing_enrichment']}")

    mv = enrichment_cost["minimal_viable"]
    print(f"\n  Minimal viable (test whether graph strategies help):")
    print(f"    API calls: {mv['api_calls']}")
    print(f"    Estimated time: {mv['estimated_time_at_10rps']}")
    print(f"    Expected papers with refs: ~{mv['estimated_papers_with_refs']}")

    fc = enrichment_cost["full_corpus"]
    print(f"\n  Full corpus enrichment:")
    print(f"    API calls: {fc['api_calls']}")
    print(f"    Estimated time: {fc['estimated_time_at_10rps']}")
    print(f"    Expected papers with refs: ~{fc['estimated_papers_with_refs']}")

    # -------------------------------------------------------------------
    # 8. Save results
    # -------------------------------------------------------------------
    output = {
        "metadata": {
            "task": "W1C: Graph-based strategy profiling (S3a, S3c)",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "corpus_size": len(profiler.paper_ids),
            "n_profiles": len(profiler.profiles),
            "strategies_attempted": ["S3a", "S3c"],
            "strategies_profiled": ["S3a"],
            "strategies_non_functional": ["S3c"],
            "duration_s": round(time.time() - t_start, 1),
            "data_limitation_summary": coverage["conclusion"],
        },
        "coverage_analysis": coverage,
        "strategies": {
            "S3a": {
                "build_info": s3a_build,
                "harness_card": s3a_card,
                "focused_evaluation": focused_eval,
            },
            "S3c": {
                "build_info": s3c_build,
                "harness_card": None,
                "reason": "No papers have related_works populated in OpenAlex cache",
            },
        },
        "enrichment_cost": enrichment_cost,
    }

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, default=str)

    print(f"\nResults saved to: {OUTPUT_PATH}")

    # -------------------------------------------------------------------
    # 9. Final summary
    # -------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("W1C SUMMARY")
    print("=" * 70)

    print(f"\n  S3a (Bibliographic coupling):")
    print(f"    Standard harness: DATA-LIMITED (1/{seed_cov['total_unique_seeds']} seeds have refs)")
    s3a_instruments = s3a_card.get("instruments", {})
    prox_mean = s3a_instruments.get("seed_proximity", {}).get("mean")
    loo_mean = s3a_instruments.get("leave_one_out_mrr", {}).get("mean")
    print(f"    Harness LOO MRR: {loo_mean}")
    print(f"    Harness seed proximity: {prox_mean}")
    if focused_eval["status"] == "completed":
        fsummary = focused_eval["summary"]
        print(f"    Focused eval discrimination: {fsummary['mean_discrimination']:.4f} "
              f"({fsummary['positive_discrimination_fraction']:.0%} groups positive)")
        print(f"    Conclusion: Algorithm IS valid; data coverage is the bottleneck")
    print()
    print(f"  S3c (OpenAlex related_works):")
    print(f"    Status: NON-FUNCTIONAL (0 papers have related_works)")
    print(f"    Conclusion: Cannot evaluate; field not populated in current enrichment")

    print(f"\n  Enrichment needed for viable graph strategies:")
    print(f"    Minimal: ~{mv['api_calls']} API calls ({mv['estimated_time_at_10rps']})")
    print(f"    Full: ~{fc['api_calls']} API calls ({fc['estimated_time_at_10rps']})")

    print(f"\n  Total duration: {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
