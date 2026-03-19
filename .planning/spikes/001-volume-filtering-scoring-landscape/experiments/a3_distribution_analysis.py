"""
A3: Distribution Analysis

Compute and visualize distributions of key corpus features:
1. Category distribution (bar chart + Gini)
2. Abstract/title length distributions
3. Author count per paper
4. Category count per paper
5. Temporal distribution within month
6. Vocabulary analysis (Zipf's law)

Usage:
    python a3_distribution_analysis.py
"""

import json
import re
import sqlite3
import time
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
RESULTS_PATH = DATA_DIR / "a3_distribution_results.json"
VIZ_DIR = DATA_DIR / "a3_visualizations"


def load_papers() -> list[dict]:
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def gini_coefficient(values: list) -> float:
    """Compute Gini coefficient (0 = perfect equality, 1 = max inequality)."""
    arr = np.sort(np.array(values, dtype=float))
    n = len(arr)
    if n == 0 or arr.sum() == 0:
        return 0
    index = np.arange(1, n + 1)
    return float((2 * np.sum(index * arr) - (n + 1) * np.sum(arr)) / (n * np.sum(arr)))


def analyze_categories(papers):
    print("  1. Category distribution...")
    cat_counts = Counter(p["primary_category"] for p in papers)
    sorted_cats = cat_counts.most_common()
    gini = gini_coefficient([c for _, c in sorted_cats])

    fig, ax = plt.subplots(figsize=(12, 6))
    cats = [c for c, _ in sorted_cats[:20]]
    counts = [c for _, c in sorted_cats[:20]]
    ax.barh(cats[::-1], counts[::-1], color='steelblue')
    ax.set_xlabel("Paper count")
    ax.set_title(f"Papers by primary category (top 20, Gini={gini:.3f})")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "category_distribution.png", dpi=150)
    plt.close()

    print(f"    {len(cat_counts)} unique categories, Gini={gini:.3f}")
    print(f"    Top 5: {sorted_cats[:5]}")

    return {
        "n_categories": len(cat_counts),
        "gini": round(gini, 4),
        "top_10": [(c, n) for c, n in sorted_cats[:10]],
    }


def analyze_lengths(papers):
    print("  2. Abstract/title length distributions...")
    abstract_lens = [len(p["abstract"].split()) for p in papers if p["abstract"]]
    title_lens = [len(p["title"].split()) for p in papers if p["title"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.hist(abstract_lens, bins=50, color='steelblue', edgecolor='white')
    ax1.set_xlabel("Word count")
    ax1.set_ylabel("Papers")
    ax1.set_title(f"Abstract length (mean={np.mean(abstract_lens):.0f}, median={np.median(abstract_lens):.0f})")
    ax1.axvline(np.median(abstract_lens), color='red', linestyle='--', alpha=0.7)

    ax2.hist(title_lens, bins=30, color='coral', edgecolor='white')
    ax2.set_xlabel("Word count")
    ax2.set_ylabel("Papers")
    ax2.set_title(f"Title length (mean={np.mean(title_lens):.0f}, median={np.median(title_lens):.0f})")
    ax2.axvline(np.median(title_lens), color='red', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / "length_distributions.png", dpi=150)
    plt.close()

    return {
        "abstract": {
            "mean": round(float(np.mean(abstract_lens)), 1),
            "median": round(float(np.median(abstract_lens)), 1),
            "std": round(float(np.std(abstract_lens)), 1),
            "min": min(abstract_lens),
            "max": max(abstract_lens),
        },
        "title": {
            "mean": round(float(np.mean(title_lens)), 1),
            "median": round(float(np.median(title_lens)), 1),
            "std": round(float(np.std(title_lens)), 1),
            "min": min(title_lens),
            "max": max(title_lens),
        },
    }


def analyze_author_counts(papers):
    print("  3. Author count per paper...")
    author_counts = []
    for p in papers:
        authors = [a.strip() for a in (p.get("authors_text") or "").split(",") if a.strip()]
        author_counts.append(len(authors))

    fig, ax = plt.subplots(figsize=(10, 5))
    max_authors = min(max(author_counts), 30)
    ax.hist(author_counts, bins=range(1, max_authors + 2), color='steelblue', edgecolor='white')
    ax.set_xlabel("Number of authors")
    ax.set_ylabel("Papers")
    ax.set_title(f"Authors per paper (median={np.median(author_counts):.0f})")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "authors_per_paper.png", dpi=150)
    plt.close()

    return {
        "mean": round(float(np.mean(author_counts)), 1),
        "median": round(float(np.median(author_counts)), 1),
        "p90": round(float(np.percentile(author_counts, 90)), 1),
        "max": max(author_counts),
        "single_author_fraction": round(sum(1 for c in author_counts if c == 1) / len(author_counts), 4),
    }


def analyze_category_counts(papers):
    print("  4. Category count per paper...")
    cat_counts = []
    for p in papers:
        cats = [c.strip() for c in (p.get("categories") or "").split() if c.strip()]
        cat_counts.append(len(cats))

    single_cat = sum(1 for c in cat_counts if c == 1)
    multi_cat = sum(1 for c in cat_counts if c > 1)

    print(f"    Single category: {single_cat} ({single_cat/len(cat_counts)*100:.1f}%)")
    print(f"    Multi-category: {multi_cat} ({multi_cat/len(cat_counts)*100:.1f}%)")
    print(f"    Mean categories/paper: {np.mean(cat_counts):.1f}")

    return {
        "mean": round(float(np.mean(cat_counts)), 2),
        "median": round(float(np.median(cat_counts)), 1),
        "max": max(cat_counts),
        "single_category_fraction": round(single_cat / len(cat_counts), 4),
        "multi_category_fraction": round(multi_cat / len(cat_counts), 4),
    }


def analyze_temporal(papers):
    print("  5. Temporal distribution...")
    day_counts = Counter()
    weekday_counts = Counter()

    from datetime import datetime

    for p in papers:
        date_str = p.get("submitted_date") or ""
        if date_str and len(date_str) >= 10:
            day_counts[date_str[:10]] += 1
            try:
                dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
                weekday_counts[dt.strftime("%A")] += 1
            except ValueError:
                pass

    if not day_counts:
        return {"error": "no date data"}

    # Weekday distribution
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_vals = [weekday_counts.get(d, 0) for d in weekday_order]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(weekday_order, weekday_vals, color='steelblue')
    ax.set_xlabel("Day of week")
    ax.set_ylabel("Papers")
    ax.set_title("Submissions by day of week")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "weekday_distribution.png", dpi=150)
    plt.close()

    return {
        "total_days": len(day_counts),
        "papers_per_day_mean": round(float(np.mean(list(day_counts.values()))), 1),
        "weekday_distribution": {d: weekday_counts.get(d, 0) for d in weekday_order},
    }


def analyze_vocabulary(papers):
    print("  6. Vocabulary analysis...")
    word_counts = Counter()
    total_words = 0

    for p in papers:
        words = re.findall(r'\b[a-z]{3,}\b', (p.get("abstract") or "").lower())
        word_counts.update(words)
        total_words += len(words)

    unique_terms = len(word_counts)
    sorted_counts = sorted(word_counts.values(), reverse=True)

    # 80% coverage
    cumsum = np.cumsum(sorted_counts)
    threshold_80 = total_words * 0.8
    terms_for_80 = int(np.searchsorted(cumsum, threshold_80)) + 1

    # Zipf's law check: log-log plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ranks = np.arange(1, len(sorted_counts) + 1)
    ax.loglog(ranks, sorted_counts, '.', markersize=1, alpha=0.5)
    ax.set_xlabel("Rank (log)")
    ax.set_ylabel("Frequency (log)")
    ax.set_title(f"Term frequency distribution ({unique_terms:,} unique terms, Zipf's law)")
    # Reference Zipf line
    zipf_ref = sorted_counts[0] / ranks
    ax.loglog(ranks, zipf_ref, '--', color='red', alpha=0.5, label="Zipf reference")
    ax.legend()
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "zipf_distribution.png", dpi=150)
    plt.close()

    print(f"    Total words: {total_words:,}")
    print(f"    Unique terms: {unique_terms:,}")
    print(f"    Terms for 80% coverage: {terms_for_80:,} ({terms_for_80/unique_terms*100:.1f}% of vocabulary)")

    return {
        "total_words": total_words,
        "unique_terms": unique_terms,
        "terms_for_80pct_coverage": terms_for_80,
        "coverage_fraction": round(terms_for_80 / unique_terms, 4),
        "top_20_terms": word_counts.most_common(20),
    }


def main():
    print("=" * 80)
    print("A3: Distribution Analysis")
    print("=" * 80)

    VIZ_DIR.mkdir(parents=True, exist_ok=True)
    papers = load_papers()
    print(f"Loaded {len(papers)} papers")

    results = {}
    results["categories"] = analyze_categories(papers)
    results["lengths"] = analyze_lengths(papers)
    results["authors_per_paper"] = analyze_author_counts(papers)
    results["categories_per_paper"] = analyze_category_counts(papers)
    results["temporal"] = analyze_temporal(papers)
    results["vocabulary"] = analyze_vocabulary(papers)
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"Visualizations saved to {VIZ_DIR.name}/")
    print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
