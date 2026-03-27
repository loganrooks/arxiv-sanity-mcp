"""Build a representative 2000-paper sample for proper embedding model comparison.

Design principles:
- Stratified by category: proportional to corpus distribution
- Stratified by time: include recent and older papers
- Include all seed/held-out papers from all 8 interest profiles
- Include random papers for realistic retrieval selectivity
- At top-20 selection from 2000 papers = 1% selectivity (vs 20% in old screening)

Output: sample_2000.json with paper IDs, metadata, and sampling rationale
"""

import json
import sqlite3
import random
from collections import Counter, defaultdict
from email.utils import parsedate_to_datetime
from pathlib import Path

DB_PATH = Path(".planning/spikes/001-volume-filtering-scoring-landscape/experiments/data/spike_001_harvest.db")
PROFILES_PATH = Path(".planning/spikes/003-strategy-profiling/experiments/data/interest_profiles.json")
OUTPUT = Path(".planning/spikes/003-strategy-profiling/experiments/data/sample_2000.json")

random.seed(42)  # Reproducibility


def load_corpus():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""SELECT arxiv_id, title, abstract, categories, primary_category, submitted_date
                 FROM papers""")
    papers = []
    for row in c.fetchall():
        d = dict(row)
        try:
            dt = parsedate_to_datetime(d["submitted_date"])
            d["year"] = dt.year
            d["month"] = dt.month
            d["date_parsed"] = dt.isoformat()
        except:
            d["year"] = None
            d["month"] = None
            d["date_parsed"] = None
        papers.append(d)
    conn.close()
    return papers


def load_profile_papers():
    """Get all paper IDs from all 8 interest profiles (seeds + held-out)."""
    with open(PROFILES_PATH) as f:
        data = json.load(f)

    profile_ids = set()
    profile_map = {}  # arxiv_id -> list of profile IDs
    for pid, profile in data["profiles"].items():
        for p in profile.get("seed_papers", []):
            profile_ids.add(p["arxiv_id"])
            profile_map.setdefault(p["arxiv_id"], []).append(pid)
        for p in profile.get("held_out_papers", []):
            profile_ids.add(p["arxiv_id"])
            profile_map.setdefault(p["arxiv_id"], []).append(pid)

    return profile_ids, profile_map


def build_sample(papers, profile_ids, target_size=2000):
    """Build stratified sample."""

    # Step 1: Always include all profile papers (seeds + held-out)
    profile_papers = [p for p in papers if p["arxiv_id"] in profile_ids]
    non_profile = [p for p in papers if p["arxiv_id"] not in profile_ids]

    guaranteed = set(p["arxiv_id"] for p in profile_papers)
    remaining_budget = target_size - len(guaranteed)

    print(f"Profile papers (guaranteed): {len(guaranteed)}")
    print(f"Remaining budget: {remaining_budget}")

    # Step 2: Stratify remaining by category (proportional)
    cat_counts = Counter(p["primary_category"] for p in non_profile)
    total_non_profile = len(non_profile)

    # Group non-profile papers by category
    by_category = defaultdict(list)
    for p in non_profile:
        by_category[p["primary_category"]].append(p)

    # Allocate 70% of budget proportionally by category
    category_budget = int(remaining_budget * 0.70)
    cat_allocations = {}
    for cat, count in cat_counts.most_common():
        alloc = max(1, int(category_budget * count / total_non_profile))
        cat_allocations[cat] = alloc

    # Normalize to fit budget
    total_alloc = sum(cat_allocations.values())
    if total_alloc > category_budget:
        scale = category_budget / total_alloc
        cat_allocations = {c: max(1, int(a * scale)) for c, a in cat_allocations.items()}

    # Step 3: Within each category, stratify by time
    # 50% from Jan 2026, 25% from 2025, 15% from 2024, 10% from pre-2024
    time_weights = [
        (lambda p: p["year"] == 2026, 0.50, "2026"),
        (lambda p: p["year"] == 2025, 0.25, "2025"),
        (lambda p: p["year"] == 2024, 0.15, "2024"),
        (lambda p: p["year"] is not None and p["year"] < 2024, 0.10, "pre-2024"),
    ]

    category_sampled = set()
    category_sample_log = {}

    for cat, alloc in cat_allocations.items():
        cat_papers = by_category[cat]
        sampled_from_cat = []

        for filter_fn, weight, label in time_weights:
            eligible = [p for p in cat_papers if filter_fn(p) and p["arxiv_id"] not in category_sampled]
            n_want = max(1, int(alloc * weight))
            n_take = min(n_want, len(eligible))
            if n_take > 0:
                chosen = random.sample(eligible, n_take)
                sampled_from_cat.extend(chosen)
                category_sampled.update(p["arxiv_id"] for p in chosen)

        # Fill remainder if under-sampled
        while len(sampled_from_cat) < alloc:
            eligible = [p for p in cat_papers if p["arxiv_id"] not in category_sampled]
            if not eligible:
                break
            chosen = random.choice(eligible)
            sampled_from_cat.append(chosen)
            category_sampled.add(chosen["arxiv_id"])

        category_sample_log[cat] = len(sampled_from_cat)

    # Step 4: Random papers for remaining budget (ensures diversity beyond categories)
    random_budget = target_size - len(guaranteed) - len(category_sampled)
    all_remaining = [p for p in non_profile if p["arxiv_id"] not in category_sampled]

    if random_budget > 0 and all_remaining:
        random_sample = random.sample(all_remaining, min(random_budget, len(all_remaining)))
        random_ids = set(p["arxiv_id"] for p in random_sample)
    else:
        random_ids = set()

    # Combine
    all_sample_ids = guaranteed | category_sampled | random_ids
    sample_papers = [p for p in papers if p["arxiv_id"] in all_sample_ids]

    return sample_papers, {
        "profile_papers": len(guaranteed),
        "category_stratified": len(category_sampled),
        "random_fill": len(random_ids),
        "total": len(sample_papers),
        "category_log": dict(sorted(category_sample_log.items(), key=lambda x: -x[1])[:20]),
    }


def analyze_sample(sample, all_papers, profile_map):
    """Analyze representativeness of the sample."""
    # Category distribution comparison
    corpus_cats = Counter(p["primary_category"] for p in all_papers)
    sample_cats = Counter(p["primary_category"] for p in sample)

    # Time distribution
    corpus_years = Counter(p["year"] for p in all_papers if p["year"])
    sample_years = Counter(p["year"] for p in sample if p["year"])

    # Profile coverage
    sample_ids = set(p["arxiv_id"] for p in sample)
    profile_coverage = {}
    for pid, papers in profile_map.items():
        if pid in sample_ids:
            profile_coverage[pid] = True

    # Top-10 category comparison
    top_cats = corpus_cats.most_common(15)
    cat_comparison = []
    for cat, corpus_count in top_cats:
        sample_count = sample_cats.get(cat, 0)
        corpus_pct = corpus_count / len(all_papers) * 100
        sample_pct = sample_count / len(sample) * 100
        cat_comparison.append({
            "category": cat,
            "corpus_count": corpus_count,
            "corpus_pct": round(corpus_pct, 1),
            "sample_count": sample_count,
            "sample_pct": round(sample_pct, 1),
        })

    return {
        "category_comparison": cat_comparison,
        "corpus_categories": len(corpus_cats),
        "sample_categories": len(sample_cats),
        "year_distribution": {
            "corpus": {str(k): v for k, v in sorted(corpus_years.items()) if k and k >= 2023},
            "sample": {str(k): v for k, v in sorted(sample_years.items()) if k and k >= 2023},
        },
        "profile_papers_in_sample": sum(1 for v in profile_coverage.values() if v),
        "total_profile_papers": len(profile_map),
    }


def main():
    print("Loading corpus...")
    papers = load_corpus()
    print(f"  {len(papers)} papers")

    print("Loading profile papers...")
    profile_ids, profile_map = load_profile_papers()
    print(f"  {len(profile_ids)} profile papers across {len(set(v for vals in profile_map.values() for v in vals))} profiles")

    print("Building sample...")
    sample, sampling_stats = build_sample(papers, profile_ids, target_size=2000)
    print(f"  Sample size: {sampling_stats['total']}")
    print(f"  Profile: {sampling_stats['profile_papers']}, "
          f"Category-stratified: {sampling_stats['category_stratified']}, "
          f"Random: {sampling_stats['random_fill']}")

    print("Analyzing representativeness...")
    analysis = analyze_sample(sample, papers, profile_map)

    print("\n=== CATEGORY REPRESENTATIVENESS ===")
    print(f"{'Category':<12} {'Corpus':>8} {'Corpus%':>8} {'Sample':>8} {'Sample%':>8}")
    for row in analysis["category_comparison"]:
        print(f"{row['category']:<12} {row['corpus_count']:>8} {row['corpus_pct']:>7.1f}% {row['sample_count']:>8} {row['sample_pct']:>7.1f}%")

    print(f"\nCategories: {analysis['sample_categories']}/{analysis['corpus_categories']} represented")

    print("\n=== TIME REPRESENTATIVENESS ===")
    print(f"{'Year':<8} {'Corpus':>8} {'Sample':>8}")
    for year in sorted(set(list(analysis["year_distribution"]["corpus"].keys()) +
                          list(analysis["year_distribution"]["sample"].keys()))):
        c = analysis["year_distribution"]["corpus"].get(year, 0)
        s = analysis["year_distribution"]["sample"].get(year, 0)
        print(f"{year:<8} {c:>8} {s:>8}")

    print(f"\nSelectivity: top-20 from {len(sample)} = {20/len(sample)*100:.1f}%")
    print(f"(vs old screening: top-20 from 100 = 20%)")
    print(f"(vs full corpus: top-20 from 19,252 = 0.1%)")

    # Save
    output = {
        "metadata": {
            "purpose": "Representative 2000-paper sample for embedding model comparison",
            "corpus_size": len(papers),
            "sample_size": len(sample),
            "selectivity_pct": round(20 / len(sample) * 100, 2),
            "seed": 42,
            "sampling_method": "Stratified: all profile papers (guaranteed) + "
                              "70% category-proportional with time stratification + "
                              "30% random fill",
        },
        "sampling_stats": sampling_stats,
        "representativeness": analysis,
        "paper_ids": [p["arxiv_id"] for p in sample],
        "papers": [
            {
                "arxiv_id": p["arxiv_id"],
                "title": p["title"],
                "abstract": p["abstract"],
                "primary_category": p["primary_category"],
                "categories": p["categories"],
                "year": p["year"],
            }
            for p in sample
        ],
    }

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to {OUTPUT}")


if __name__ == "__main__":
    main()
