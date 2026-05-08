#!/usr/bin/env python3
"""
W1C-gap: OpenAlex enrichment expansion + S3a/S3c re-profiling.

W1C found S3a (bibliographic coupling) has a valid algorithm (0.467 mean
discrimination) but is SEVERELY DATA-LIMITED: only 95/19,252 papers have
referenced_works, and only 1/120 seed papers has references.

This script:
  1. Collects all seed papers + their top-100 MiniLM neighbors
  2. Enriches them via OpenAlex title search API
  3. Re-profiles S3a with the expanded data
  4. Checks if S3c (related_works) becomes viable

Data flow:
  - Input: interest_profiles.json, miniLM_title_19k.npy, arxiv_ids_19k.json,
    b2_openalex_cache.json, spike_001_harvest.db
  - Output: expanded_openalex_cache.json, w1c_gap_s3a_profiles.json
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------

SPIKE_003_DIR = Path(__file__).resolve().parent.parent
SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
SPIKE_002_DATA = SPIKE_003_DIR.parent / "002-backend-comparison" / "experiments" / "data"
EXPERIMENTS_DIR = SPIKE_003_DIR / "experiments"
DATA_DIR = EXPERIMENTS_DIR / "data"

sys.path.insert(0, str(EXPERIMENTS_DIR))

from harness import StrategyProfiler
from harness.strategy_protocol import SimpleStrategy

# ---------------------------------------------------------------------------
# Data paths
# ---------------------------------------------------------------------------

HARVEST_DB = str(SPIKE_001_DATA / "spike_001_harvest.db")
EXISTING_CACHE = str(SPIKE_001_DATA / "b2_openalex_cache.json")
MINIML_EMB = str(DATA_DIR / "miniLM_title_19k.npy")
ARXIV_IDS = str(SPIKE_002_DATA / "arxiv_ids_19k.json")
PROFILES_PATH = str(DATA_DIR / "interest_profiles.json")
ENRICHMENT_PLAN = str(DATA_DIR / "papers_needing_enrichment.json")

OUTPUT_CACHE = str(DATA_DIR / "expanded_openalex_cache.json")
OUTPUT_PROFILES = str(DATA_DIR / "w1c_gap_s3a_profiles.json")

# ---------------------------------------------------------------------------
# OpenAlex API configuration
# ---------------------------------------------------------------------------

OPENALEX_BASE = "https://api.openalex.org/works"
# Polite pool email - gets faster rate limits
OPENALEX_EMAIL = os.environ.get("OPENALEX_EMAIL", "")
# Fields we need from the API
OPENALEX_SELECT = ",".join([
    "id", "doi", "title", "cited_by_count",
    "citation_normalized_percentile",
    "topics", "referenced_works", "related_works",
    "authorships", "type", "publication_year",
])

# Rate limiting: 10 req/s without polite pool, ~50 req/s with
REQUESTS_PER_SECOND = 9  # Conservative, below 10 limit
BATCH_SIZE = 50  # Papers per batch (OpenAlex supports pipe-delimited OR)
CHECKPOINT_INTERVAL = 200  # Save progress every N papers


# ---------------------------------------------------------------------------
# Step 1: Identify papers needing enrichment
# ---------------------------------------------------------------------------

def identify_papers_to_enrich() -> dict:
    """Load pre-computed enrichment plan or recompute."""
    if os.path.exists(ENRICHMENT_PLAN):
        with open(ENRICHMENT_PLAN) as f:
            plan = json.load(f)
        print(f"  Loaded enrichment plan: {plan['need_enrichment']} papers needed")
        return plan

    # If no pre-computed plan, compute it
    print("  Computing enrichment plan...")
    with open(PROFILES_PATH) as f:
        profiles_data = json.load(f)
    with open(ARXIV_IDS) as f:
        all_ids = json.load(f)
    with open(EXISTING_CACHE) as f:
        existing_cache = json.load(f)

    emb = np.load(MINIML_EMB)
    id_to_idx = {aid: i for i, aid in enumerate(all_ids)}

    # Collect seeds
    all_seeds = set()
    for pname, pdata in profiles_data['profiles'].items():
        for sp in pdata['seed_papers']:
            all_seeds.add(sp['arxiv_id'])

    # Top-100 neighbors per seed
    emb_normed = emb / np.linalg.norm(emb, axis=1, keepdims=True)
    all_neighbors = set()
    for sid in all_seeds:
        if sid in id_to_idx:
            sidx = id_to_idx[sid]
            sims = emb_normed[sidx] @ emb_normed.T
            top_100 = np.argsort(sims)[-101:]
            for idx in top_100:
                nid = all_ids[idx]
                if nid != sid:
                    all_neighbors.add(nid)

    papers_to_enrich = all_seeds | all_neighbors
    need_enrichment = papers_to_enrich - set(existing_cache.keys())

    plan = {
        'total_seeds': len(all_seeds),
        'total_neighbors': len(all_neighbors),
        'total_unique': len(papers_to_enrich),
        'already_cached': len(papers_to_enrich) - len(need_enrichment),
        'need_enrichment': len(need_enrichment),
        'paper_ids': sorted(need_enrichment),
    }

    with open(ENRICHMENT_PLAN, 'w') as f:
        json.dump(plan, f, indent=2)

    return plan


# ---------------------------------------------------------------------------
# Step 2: OpenAlex API enrichment
# ---------------------------------------------------------------------------

def load_title_index() -> dict[str, str]:
    """Load arxiv_id -> title mapping from harvest DB."""
    conn = sqlite3.connect(HARVEST_DB)
    cur = conn.execute("SELECT arxiv_id, title FROM papers")
    index = {row[0]: row[1] for row in cur}
    conn.close()
    return index


def openalex_search_by_title(title: str) -> dict | None:
    """Search OpenAlex for a paper by its exact title.

    Returns the first result or None if no match found.
    Uses quoted title search for exact match.
    """
    # Clean title for search query
    clean_title = title.strip()
    # Use quoted search for exact title matching
    params = {
        "search": f'"{clean_title}"',
        "per_page": "1",
        "select": OPENALEX_SELECT,
    }
    if OPENALEX_EMAIL:
        params["mailto"] = OPENALEX_EMAIL

    url = f"{OPENALEX_BASE}?{urllib.parse.urlencode(params)}"

    headers = {}
    if OPENALEX_EMAIL:
        headers["User-Agent"] = f"arxiv-sanity-mcp/0.1 (mailto:{OPENALEX_EMAIL})"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
            if data.get("results") and len(data["results"]) > 0:
                return data["results"][0]
            return None
    except Exception as e:
        return {"error": str(e)}


def extract_cache_entry(oa_result: dict) -> dict:
    """Extract the fields we need from an OpenAlex result."""
    # Handle FWCI - may be in different fields
    fwci = None
    cnp = oa_result.get("citation_normalized_percentile")
    if cnp and isinstance(cnp, dict):
        fwci = cnp.get("value", 0.0)

    # Simplify authorships
    authorships = []
    for auth in oa_result.get("authorships", [])[:20]:  # Cap at 20 authors
        a = auth.get("author", {})
        authorships.append({
            "name": a.get("display_name", ""),
            "id": a.get("id", ""),
        })

    # Simplify topics
    topics = []
    for topic in oa_result.get("topics", [])[:5]:  # Cap at 5 topics
        topics.append({
            "id": topic.get("id", ""),
            "display_name": topic.get("display_name", ""),
            "score": topic.get("score", 0.0),
        })

    return {
        "id": oa_result.get("id"),
        "doi": oa_result.get("doi"),
        "cited_by_count": oa_result.get("cited_by_count"),
        "fwci": fwci,
        "citation_normalized_percentile": cnp,
        "topics": topics,
        "referenced_works": oa_result.get("referenced_works", []),
        "related_works": oa_result.get("related_works", []),
        "authorships": authorships,
        "type": oa_result.get("type"),
        "publication_year": oa_result.get("publication_year"),
    }


def run_enrichment(paper_ids: list[str], title_index: dict[str, str]) -> dict:
    """Enrich papers via OpenAlex title search.

    Returns dict mapping arxiv_id -> cache entry (or error entry).
    Saves checkpoint files periodically.
    """
    # Load existing expanded cache (for resumption)
    expanded = {}
    if os.path.exists(OUTPUT_CACHE):
        with open(OUTPUT_CACHE) as f:
            expanded = json.load(f)
        print(f"  Resuming from {len(expanded)} previously cached entries")

    # Filter to papers not yet in expanded cache
    remaining = [pid for pid in paper_ids if pid not in expanded]
    print(f"  Papers to fetch: {len(remaining)} (of {len(paper_ids)} total)")

    if not remaining:
        print("  All papers already enriched!")
        return expanded

    stats = {
        "total": len(remaining),
        "found": 0,
        "not_found": 0,
        "errors": 0,
        "no_title": 0,
        "with_refs": 0,
        "with_related": 0,
    }

    t_start = time.time()
    request_times = []

    for i, pid in enumerate(remaining):
        # Rate limiting
        if request_times:
            # Maintain target rate
            elapsed_since_last = time.time() - request_times[-1]
            target_interval = 1.0 / REQUESTS_PER_SECOND
            if elapsed_since_last < target_interval:
                time.sleep(target_interval - elapsed_since_last)

        title = title_index.get(pid)
        if not title:
            expanded[pid] = {"error": "no_title_in_db", "arxiv_id": pid}
            stats["no_title"] += 1
            continue

        result = openalex_search_by_title(title)
        request_times.append(time.time())

        if result is None:
            expanded[pid] = {
                "error": "not_found",
                "arxiv_id": pid,
                "searched_title": title,
            }
            stats["not_found"] += 1
        elif "error" in result and isinstance(result.get("error"), str):
            expanded[pid] = {
                "error": result["error"],
                "arxiv_id": pid,
                "searched_title": title,
            }
            stats["errors"] += 1
        else:
            entry = extract_cache_entry(result)
            expanded[pid] = entry
            stats["found"] += 1
            if entry.get("referenced_works"):
                stats["with_refs"] += 1
            if entry.get("related_works"):
                stats["with_related"] += 1

        # Progress reporting
        if (i + 1) % 50 == 0 or (i + 1) == len(remaining):
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (len(remaining) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i+1}/{len(remaining)}] "
                  f"found={stats['found']} not_found={stats['not_found']} "
                  f"errors={stats['errors']} "
                  f"refs={stats['with_refs']} related={stats['with_related']} "
                  f"rate={rate:.1f}/s ETA={eta:.0f}s")

        # Checkpoint save
        if (i + 1) % CHECKPOINT_INTERVAL == 0:
            with open(OUTPUT_CACHE, 'w') as f:
                json.dump(expanded, f, indent=2)
            print(f"  -- Checkpoint saved at {i+1} papers --")

    # Final save
    with open(OUTPUT_CACHE, 'w') as f:
        json.dump(expanded, f, indent=2)

    stats["elapsed_s"] = round(time.time() - t_start, 1)
    stats["effective_rate"] = round(len(remaining) / max(stats["elapsed_s"], 0.1), 1)

    return expanded


# ---------------------------------------------------------------------------
# Step 3: Merge caches and re-profile S3a
# ---------------------------------------------------------------------------

def merge_caches(existing_cache_path: str, expanded_cache: dict) -> dict:
    """Merge existing B2 cache with new expanded cache.

    Existing cache entries take priority (they were the original enrichment).
    Expanded cache fills in the gaps.
    """
    with open(existing_cache_path) as f:
        existing = json.load(f)

    merged = dict(existing)
    new_count = 0
    for pid, entry in expanded_cache.items():
        if pid not in merged and not entry.get("error"):
            merged[pid] = entry
            new_count += 1

    print(f"  Merged cache: {len(existing)} existing + {new_count} new = {len(merged)} total")
    return merged


def make_bibliographic_coupling_strategy(
    paper_ids: list[str],
    cache: dict,
) -> tuple[SimpleStrategy, dict]:
    """S3a: Bibliographic coupling via Jaccard similarity of reference sets.

    Same algorithm as w1c_graph_strategies.py, but with expanded data.
    """
    ref_index: dict[str, set[str]] = {}
    for arxiv_id, entry in cache.items():
        refs = entry.get("referenced_works", [])
        if refs:
            ref_index[arxiv_id] = set(refs)

    id_to_idx = {aid: i for i, aid in enumerate(paper_ids)}
    corpus_papers_with_refs = set(ref_index.keys()) & set(paper_ids)

    build_info = {
        "total_corpus": len(paper_ids),
        "papers_in_ref_index": len(ref_index),
        "corpus_papers_with_refs": len(corpus_papers_with_refs),
        "coverage_fraction": len(corpus_papers_with_refs) / len(paper_ids),
    }

    def score_fn(seed_ids: list[str]) -> np.ndarray:
        scores = np.zeros(len(paper_ids), dtype=np.float64)
        seed_ref_sets = []
        for sid in seed_ids:
            if sid in ref_index:
                seed_ref_sets.append(ref_index[sid])

        if not seed_ref_sets:
            return scores

        for cand_id in corpus_papers_with_refs:
            cand_refs = ref_index[cand_id]
            idx = id_to_idx.get(cand_id)
            if idx is None:
                continue
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
        name="Bibliographic coupling / Jaccard (S3a) [expanded]",
        strategy_id="S3a_expanded",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )

    return strategy, build_info


def make_related_works_strategy(
    paper_ids: list[str],
    cache: dict,
) -> tuple[SimpleStrategy | None, dict]:
    """S3c: OpenAlex related_works scoring, with expanded data."""
    related_index: dict[str, set[str]] = {}
    for arxiv_id, entry in cache.items():
        related = entry.get("related_works", [])
        if related:
            related_index[arxiv_id] = set(related)

    oa_to_arxiv: dict[str, str] = {}
    for arxiv_id, entry in cache.items():
        oa_id = entry.get("id")
        if oa_id and arxiv_id in set(paper_ids):
            oa_to_arxiv[oa_id] = arxiv_id

    build_info = {
        "papers_with_related_works": len(related_index),
        "oa_to_arxiv_mappings": len(oa_to_arxiv),
        "corpus_papers_with_related": len(set(related_index.keys()) & set(paper_ids)),
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
                arxiv_id = oa_to_arxiv.get(related_oa_id)
                if arxiv_id is not None:
                    idx = id_to_idx.get(arxiv_id)
                    if idx is not None:
                        scores[idx] += 1.0
        return scores

    strategy = SimpleStrategy(
        name="OpenAlex related_works (S3c) [expanded]",
        strategy_id="S3c_expanded",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )

    return strategy, build_info


def analyze_expanded_coverage(
    merged_cache: dict,
    profiler: StrategyProfiler,
) -> dict:
    """Analyze reference coverage after enrichment expansion."""
    papers_with_refs = {}
    papers_with_related = {}
    for arxiv_id, entry in merged_cache.items():
        if entry.get("error"):
            continue
        refs = entry.get("referenced_works", [])
        related = entry.get("related_works", [])
        if refs:
            papers_with_refs[arxiv_id] = set(refs)
        if related:
            papers_with_related[arxiv_id] = set(related)

    corpus_ids = set(profiler.paper_ids)

    # Seed paper coverage
    all_seed_ids = set()
    profile_seed_coverage = {}
    for prof in profiler.profiles:
        prof_seeds = set()
        for seed_set in prof.seed_sets:
            prof_seeds.update(seed_set)
        all_seed_ids.update(prof_seeds)

        seeds_with_refs = prof_seeds & set(papers_with_refs.keys())
        seeds_with_related = prof_seeds & set(papers_with_related.keys())
        profile_seed_coverage[prof.profile_id] = {
            "total_seeds": len(prof_seeds),
            "seeds_in_cache": len(prof_seeds & set(merged_cache.keys())),
            "seeds_with_refs": len(seeds_with_refs),
            "seeds_with_related": len(seeds_with_related),
            "seed_ids_with_refs": sorted(seeds_with_refs),
        }

    # Build OpenAlex ID -> arxiv_id mapping
    corpus_oa_ids = {}
    for arxiv_id, entry in merged_cache.items():
        if entry.get("error"):
            continue
        oa_id = entry.get("id")
        if oa_id and arxiv_id in corpus_ids:
            corpus_oa_ids[oa_id] = arxiv_id

    # Count how many referenced_works point to papers in our corpus
    all_ref_ids = set()
    for ref_set in papers_with_refs.values():
        all_ref_ids.update(ref_set)
    refs_to_corpus = all_ref_ids & set(corpus_oa_ids.keys())

    # Reference count stats
    ref_counts = [len(v) for v in papers_with_refs.values()]

    return {
        "total_cache_entries": len(merged_cache),
        "valid_entries": sum(1 for v in merged_cache.values() if not v.get("error")),
        "papers_with_referenced_works": len(papers_with_refs),
        "papers_with_related_works": len(papers_with_related),
        "corpus_papers_with_refs": len(set(papers_with_refs.keys()) & corpus_ids),
        "corpus_papers_with_related": len(set(papers_with_related.keys()) & corpus_ids),
        "unique_referenced_work_ids": len(all_ref_ids),
        "referenced_works_pointing_to_corpus": len(refs_to_corpus),
        "oa_to_arxiv_mappings": len(corpus_oa_ids),
        "ref_count_stats": {
            "min": int(min(ref_counts)) if ref_counts else 0,
            "max": int(max(ref_counts)) if ref_counts else 0,
            "mean": round(float(np.mean(ref_counts)), 1) if ref_counts else 0,
            "median": float(np.median(ref_counts)) if ref_counts else 0,
        },
        "seed_paper_coverage": {
            "total_unique_seeds": len(all_seed_ids),
            "seeds_in_cache": len(all_seed_ids & set(merged_cache.keys())),
            "seeds_with_refs": len(all_seed_ids & set(papers_with_refs.keys())),
            "seeds_with_related": len(all_seed_ids & set(papers_with_related.keys())),
            "by_profile": profile_seed_coverage,
        },
    }


def focused_evaluation(
    cache: dict,
    profiler: StrategyProfiler,
) -> dict:
    """Focused evaluation of coupling among papers with references.

    Same as w1c_graph_strategies.py but with expanded data.
    """
    ref_papers = {}
    for arxiv_id, entry in cache.items():
        if entry.get("error"):
            continue
        refs = entry.get("referenced_works", [])
        if refs and arxiv_id in set(profiler.paper_ids):
            ref_papers[arxiv_id] = {
                "refs": set(refs),
                "topics": entry.get("topics", []),
            }

    if len(ref_papers) < 10:
        return {
            "status": "insufficient_data",
            "papers_with_refs": len(ref_papers),
        }

    # Group by primary topic
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

    viable_groups = {
        topic: papers
        for topic, papers in topic_groups.items()
        if len(papers) >= 3
    }

    ref_sets = {aid: data["refs"] for aid, data in ref_papers.items()}
    group_results = []

    for topic, group_papers in sorted(viable_groups.items(), key=lambda x: -len(x[1])):
        group_set = set(group_papers)
        non_group = [aid for aid in ref_papers if aid not in group_set]

        # Intra-group Jaccard
        intra_jaccards = []
        for p1, p2 in combinations(group_papers, 2):
            intersection = ref_sets[p1] & ref_sets[p2]
            union = ref_sets[p1] | ref_sets[p2]
            intra_jaccards.append(len(intersection) / len(union) if union else 0.0)

        # Inter-group Jaccard
        inter_jaccards = []
        rng = np.random.RandomState(42)
        sample_size = min(30, len(non_group))
        if sample_size > 0:
            sample_non_group = rng.choice(non_group, size=sample_size, replace=False)
            for gp in group_papers[:10]:  # Cap to avoid combinatorial explosion
                for ngp in sample_non_group:
                    if ngp in ref_sets:
                        intersection = ref_sets[gp] & ref_sets[ngp]
                        union = ref_sets[gp] | ref_sets[ngp]
                        inter_jaccards.append(
                            len(intersection) / len(union) if union else 0.0
                        )

        disc = None
        if intra_jaccards and inter_jaccards:
            disc = float(np.mean(intra_jaccards)) - float(np.mean(inter_jaccards))

        group_results.append({
            "topic": topic,
            "n_papers": len(group_papers),
            "intra_group_jaccard": {
                "mean": float(np.mean(intra_jaccards)) if intra_jaccards else 0.0,
                "max": float(max(intra_jaccards)) if intra_jaccards else 0.0,
                "nonzero_fraction": (
                    sum(1 for j in intra_jaccards if j > 0) / len(intra_jaccards)
                    if intra_jaccards else 0.0
                ),
                "n_pairs": len(intra_jaccards),
            },
            "inter_group_jaccard": {
                "mean": float(np.mean(inter_jaccards)) if inter_jaccards else 0.0,
                "max": float(max(inter_jaccards)) if inter_jaccards else 0.0,
                "nonzero_fraction": (
                    sum(1 for j in inter_jaccards if j > 0) / len(inter_jaccards)
                    if inter_jaccards else 0.0
                ),
                "n_pairs": len(inter_jaccards),
            },
            "discrimination": disc,
        })

    all_discriminations = [g["discrimination"] for g in group_results
                          if g["discrimination"] is not None]

    return {
        "status": "completed",
        "n_papers_with_refs": len(ref_papers),
        "n_topic_groups": len(topic_groups),
        "n_viable_groups": len(viable_groups),
        "group_results": group_results,
        "summary": {
            "mean_intra_jaccard": float(np.mean(
                [g["intra_group_jaccard"]["mean"] for g in group_results]
            )) if group_results else 0.0,
            "mean_inter_jaccard": float(np.mean(
                [g["inter_group_jaccard"]["mean"] for g in group_results]
            )) if group_results else 0.0,
            "mean_discrimination": (
                float(np.mean(all_discriminations)) if all_discriminations else 0.0
            ),
            "positive_discrimination_fraction": (
                sum(1 for d in all_discriminations if d > 0) / len(all_discriminations)
                if all_discriminations else 0.0
            ),
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("W1C-gap: OpenAlex Enrichment Expansion + S3a/S3c Re-Profile")
    print("=" * 70)
    t_start = time.time()

    # -----------------------------------------------------------------------
    # 1. Identify papers needing enrichment
    # -----------------------------------------------------------------------
    print("\n--- Step 1: Identify papers needing enrichment ---")
    plan = identify_papers_to_enrich()
    print(f"  Seeds: {plan['total_seeds']}")
    print(f"  Neighbors: {plan['total_neighbors']}")
    print(f"  Total unique: {plan['total_unique']}")
    print(f"  Already cached: {plan['already_cached']}")
    print(f"  Need enrichment: {plan['need_enrichment']}")

    # -----------------------------------------------------------------------
    # 2. Enrich via OpenAlex API
    # -----------------------------------------------------------------------
    print(f"\n--- Step 2: Enrich {plan['need_enrichment']} papers via OpenAlex ---")
    title_index = load_title_index()
    print(f"  Loaded {len(title_index)} titles from harvest DB")

    expanded = run_enrichment(plan['paper_ids'], title_index)
    print(f"\n  Expanded cache: {len(expanded)} entries")

    # Count successes
    found = sum(1 for v in expanded.values() if not v.get("error"))
    with_refs = sum(1 for v in expanded.values()
                    if v.get("referenced_works") and len(v["referenced_works"]) > 0)
    with_related = sum(1 for v in expanded.values()
                       if v.get("related_works") and len(v["related_works"]) > 0)
    print(f"  Found: {found}, with refs: {with_refs}, with related: {with_related}")

    # -----------------------------------------------------------------------
    # 3. Merge caches
    # -----------------------------------------------------------------------
    print(f"\n--- Step 3: Merge existing cache with expanded data ---")
    merged = merge_caches(EXISTING_CACHE, expanded)

    # -----------------------------------------------------------------------
    # 4. Load profiler and analyze coverage
    # -----------------------------------------------------------------------
    print(f"\n--- Step 4: Analyze expanded coverage ---")
    profiler = StrategyProfiler.from_spike_data()
    coverage = analyze_expanded_coverage(merged, profiler)

    seed_cov = coverage["seed_paper_coverage"]
    print(f"\n  Total cache: {coverage['total_cache_entries']} entries "
          f"({coverage['valid_entries']} valid)")
    print(f"  Papers with referenced_works: {coverage['papers_with_referenced_works']}")
    print(f"  Papers with related_works: {coverage['papers_with_related_works']}")
    print(f"  Corpus papers with refs: {coverage['corpus_papers_with_refs']}")
    print(f"  Corpus papers with related: {coverage['corpus_papers_with_related']}")
    print(f"  Seed coverage: {seed_cov['seeds_with_refs']}/{seed_cov['total_unique_seeds']} "
          f"seeds with refs, {seed_cov['seeds_with_related']} with related_works")
    print(f"  Referenced works pointing to corpus: "
          f"{coverage['referenced_works_pointing_to_corpus']}")
    print(f"  OA-to-arxiv mappings: {coverage['oa_to_arxiv_mappings']}")

    for pid, pdata in seed_cov["by_profile"].items():
        print(f"    {pid}: {pdata['total_seeds']} seeds, "
              f"{pdata['seeds_with_refs']} with refs, "
              f"{pdata.get('seeds_with_related', 0)} with related")

    # -----------------------------------------------------------------------
    # 5. Build and profile S3a (expanded)
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Step 5: Profile S3a (bibliographic coupling) with expanded data")
    print("=" * 70)

    s3a, s3a_build = make_bibliographic_coupling_strategy(profiler.paper_ids, merged)
    print(f"  Papers in ref index: {s3a_build['papers_in_ref_index']}")
    print(f"  Corpus papers with refs: {s3a_build['corpus_papers_with_refs']}")
    print(f"  Coverage: {s3a_build['coverage_fraction']:.2%}")

    s3a_card = profiler.profile(
        s3a,
        config={
            "type": "graph",
            "strategy_class": "S3a",
            "data_source": "expanded OpenAlex enrichment",
            "enrichment_expansion": True,
        },
        top_k=20,
        run_loo=True,
        measure_resources=True,
        latency_n_runs=50,
    )

    # Print S3a profile summary
    print(f"\n  --- S3a expanded harness summary ---")
    for inst_name, inst_data in s3a_card.get("instruments", {}).items():
        mean = inst_data.get("mean")
        std = inst_data.get("std")
        if mean is not None:
            print(f"  {inst_name:<30s} mean={mean:.4f}  std={std:.4f}")

    res = s3a_card.get("resources", {})
    latency = res.get("query_latency_ms", {})
    if latency:
        print(f"  latency p50={latency.get('p50', '?'):.2f}ms  "
              f"p95={latency.get('p95', '?'):.2f}ms")

    # -----------------------------------------------------------------------
    # 6. Focused evaluation with expanded data
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Step 6: Focused evaluation (intra vs inter-group coupling)")
    print("=" * 70)

    focused = focused_evaluation(merged, profiler)
    if focused["status"] == "completed":
        fsummary = focused["summary"]
        print(f"  Papers with refs: {focused['n_papers_with_refs']}")
        print(f"  Topic groups: {focused['n_topic_groups']} total, "
              f"{focused['n_viable_groups']} viable (>= 3 papers)")
        print(f"  Mean intra-group Jaccard: {fsummary['mean_intra_jaccard']:.4f}")
        print(f"  Mean inter-group Jaccard: {fsummary['mean_inter_jaccard']:.4f}")
        print(f"  Mean discrimination: {fsummary['mean_discrimination']:.4f}")
        print(f"  Groups with positive discrimination: "
              f"{fsummary['positive_discrimination_fraction']:.0%}")

        # Top 10 groups by discrimination
        sorted_groups = sorted(
            [g for g in focused["group_results"] if g["discrimination"] is not None],
            key=lambda g: g["discrimination"],
            reverse=True,
        )
        print(f"\n  Top discriminating groups:")
        for g in sorted_groups[:10]:
            print(f"    [{g['n_papers']}p] {g['topic'][:55]:<55s} "
                  f"disc={g['discrimination']:+.4f}")
    else:
        print(f"  Status: {focused['status']}")

    # -----------------------------------------------------------------------
    # 7. Check S3c (related_works) viability
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Step 7: Check S3c (related_works) viability")
    print("=" * 70)

    s3c, s3c_build = make_related_works_strategy(profiler.paper_ids, merged)
    print(f"  Papers with related_works: {s3c_build['papers_with_related_works']}")
    print(f"  Corpus papers with related: {s3c_build.get('corpus_papers_with_related', 0)}")
    print(f"  OA-to-arxiv mappings: {s3c_build['oa_to_arxiv_mappings']}")
    print(f"  Status: {s3c_build['status']}")

    s3c_card = None
    if s3c is not None:
        print("\n  S3c is now viable! Profiling...")
        s3c_card = profiler.profile(
            s3c,
            config={
                "type": "graph",
                "strategy_class": "S3c",
                "data_source": "expanded OpenAlex enrichment",
            },
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=50,
        )
        for inst_name, inst_data in s3c_card.get("instruments", {}).items():
            mean = inst_data.get("mean")
            std = inst_data.get("std")
            if mean is not None:
                print(f"  {inst_name:<30s} mean={mean:.4f}  std={std:.4f}")
    else:
        print("  S3c remains non-functional (no related_works data)")

    # -----------------------------------------------------------------------
    # 8. Comparison with W1C data-limited results
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("Step 8: Comparison - W1C data-limited vs expanded")
    print("=" * 70)

    # Load original W1C results for comparison
    w1c_path = DATA_DIR / "w1c_graph_profiles.json"
    w1c_comparison = None
    if w1c_path.exists():
        with open(w1c_path) as f:
            w1c_data = json.load(f)

        orig_coverage = w1c_data.get("coverage_analysis", {})
        orig_focused = w1c_data.get("strategies", {}).get("S3a", {}).get(
            "focused_evaluation", {}
        )

        w1c_comparison = {
            "original": {
                "cache_entries": orig_coverage.get("openalex_cache_total", 0),
                "papers_with_refs": orig_coverage.get("papers_with_referenced_works", 0),
                "seeds_with_refs": orig_coverage.get("seed_paper_coverage", {}).get(
                    "seeds_with_refs", 0
                ),
                "focused_discrimination": orig_focused.get("summary", {}).get(
                    "mean_discrimination", None
                ),
            },
            "expanded": {
                "cache_entries": coverage["total_cache_entries"],
                "papers_with_refs": coverage["papers_with_referenced_works"],
                "seeds_with_refs": seed_cov["seeds_with_refs"],
                "focused_discrimination": (
                    fsummary["mean_discrimination"]
                    if focused["status"] == "completed" else None
                ),
            },
        }

        print(f"\n  {'Metric':<35s} {'Original':>10s} {'Expanded':>10s} {'Change':>10s}")
        print(f"  {'-' * 65}")
        for metric in ["cache_entries", "papers_with_refs", "seeds_with_refs"]:
            orig_val = w1c_comparison["original"][metric]
            exp_val = w1c_comparison["expanded"][metric]
            change = f"{exp_val - orig_val:+d}" if isinstance(orig_val, int) else "N/A"
            print(f"  {metric:<35s} {str(orig_val):>10s} {str(exp_val):>10s} {change:>10s}")

        orig_disc = w1c_comparison["original"]["focused_discrimination"]
        exp_disc = w1c_comparison["expanded"]["focused_discrimination"]
        if orig_disc is not None and exp_disc is not None:
            print(f"  {'focused_discrimination':<35s} "
                  f"{orig_disc:>10.4f} {exp_disc:>10.4f} "
                  f"{exp_disc - orig_disc:>+10.4f}")

    # -----------------------------------------------------------------------
    # 9. Save results
    # -----------------------------------------------------------------------
    print(f"\n--- Saving results ---")

    output = {
        "metadata": {
            "task": "W1C-gap: OpenAlex enrichment expansion + S3a/S3c re-profile",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "corpus_size": len(profiler.paper_ids),
            "n_profiles": len(profiler.profiles),
            "enrichment_stats": {
                "papers_requested": plan["need_enrichment"],
                "total_expanded_cache": len(expanded),
                "found": sum(1 for v in expanded.values() if not v.get("error")),
                "with_refs": with_refs,
                "with_related": with_related,
            },
            "duration_s": round(time.time() - t_start, 1),
        },
        "coverage_analysis": coverage,
        "w1c_comparison": w1c_comparison,
        "strategies": {
            "S3a_expanded": {
                "build_info": s3a_build,
                "harness_card": s3a_card,
                "focused_evaluation": focused,
            },
            "S3c_expanded": {
                "build_info": s3c_build,
                "harness_card": s3c_card,
                "status": s3c_build["status"],
            },
        },
    }

    with open(OUTPUT_PROFILES, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"  Profiles saved to: {OUTPUT_PROFILES}")

    # -----------------------------------------------------------------------
    # 10. Summary
    # -----------------------------------------------------------------------
    print(f"\n{'=' * 70}")
    print("W1C-gap SUMMARY")
    print("=" * 70)

    print(f"\n  Enrichment expansion:")
    print(f"    Papers enriched: {plan['need_enrichment']}")
    print(f"    Found in OpenAlex: {found}")
    print(f"    With referenced_works: {with_refs}")
    print(f"    With related_works: {with_related}")

    print(f"\n  S3a (Bibliographic coupling) with expanded data:")
    print(f"    Seed coverage: {seed_cov['seeds_with_refs']}/{seed_cov['total_unique_seeds']} "
          f"seeds with refs")
    print(f"    Corpus coverage: {s3a_build['corpus_papers_with_refs']} papers with refs "
          f"({s3a_build['coverage_fraction']:.1%})")

    s3a_instruments = s3a_card.get("instruments", {})
    for metric_name in ["leave_one_out_mrr", "seed_proximity", "topical_coherence",
                        "cluster_diversity", "novelty", "category_surprise", "coverage"]:
        val = s3a_instruments.get(metric_name, {}).get("mean")
        if val is not None:
            print(f"    {metric_name}: {val:.4f}")

    if focused["status"] == "completed":
        print(f"    Focused discrimination: {fsummary['mean_discrimination']:.4f}")

    print(f"\n  S3c (related_works):")
    if s3c is not None:
        print(f"    NOW VIABLE with {s3c_build['papers_with_related_works']} papers")
    else:
        print(f"    Still non-functional ({s3c_build['papers_with_related_works']} papers)")

    print(f"\n  Total duration: {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
