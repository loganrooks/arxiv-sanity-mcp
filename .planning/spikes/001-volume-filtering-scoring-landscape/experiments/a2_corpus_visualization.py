"""
A2: Corpus Visualization and Structure

Explores the structural properties of the 19K paper corpus:
1. UMAP visualization of embedding space, colored by category
2. BERTopic topic modeling
3. Category-topic alignment analysis
4. Category co-occurrence heatmap
5. Temporal patterns (submission rate by day)
6. Author frequency distribution

Uses MiniLM embeddings from Spike 002 (already computed).

Usage:
    python a2_corpus_visualization.py
"""

import json
import sqlite3
import time
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

DATA_DIR = Path(__file__).parent / "data"
SOURCE_DB = DATA_DIR / "spike_001_harvest.db"
SPIKE002_DATA = (
    Path(__file__).parent.parent.parent
    / "002-backend-comparison/experiments/data"
)
EMBEDDINGS_PATH = SPIKE002_DATA / "embeddings_19k.npy"
ARXIV_IDS_PATH = SPIKE002_DATA / "arxiv_ids_19k.json"
RESULTS_PATH = DATA_DIR / "a2_corpus_visualization_results.json"
VIZ_DIR = DATA_DIR / "a2_visualizations"


def load_papers() -> list[dict]:
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date, updated_date "
        "FROM papers WHERE abstract IS NOT NULL AND abstract != ''"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def analyze_umap(embeddings: np.ndarray, papers: list[dict], arxiv_ids: list[str]):
    """UMAP dimensionality reduction + visualization."""
    import umap

    print("  Computing UMAP (2D)...")
    reducer = umap.UMAP(n_components=2, n_neighbors=15, min_dist=0.1, random_state=42)
    coords = reducer.fit_transform(embeddings)

    # Build ID → paper lookup
    id_to_paper = {p["arxiv_id"]: p for p in papers}

    # Get categories for coloring
    categories = []
    for aid in arxiv_ids:
        p = id_to_paper.get(aid, {})
        categories.append(p.get("primary_category", "unknown"))

    # Get unique categories and assign colors
    unique_cats = sorted(set(categories))
    cat_to_idx = {c: i for i, c in enumerate(unique_cats)}
    colors = [cat_to_idx[c] for c in categories]

    # Static plot
    fig, ax = plt.subplots(figsize=(14, 10))
    scatter = ax.scatter(
        coords[:, 0], coords[:, 1],
        c=colors, cmap='tab20', s=3, alpha=0.5,
    )
    ax.set_title(f"UMAP of 19K arXiv papers (MiniLM embeddings, colored by primary category)")
    ax.set_xlabel("UMAP-1")
    ax.set_ylabel("UMAP-2")

    # Legend with top 10 categories
    cat_counts = Counter(categories)
    top_cats = cat_counts.most_common(10)
    legend_elements = []
    cmap = plt.cm.tab20
    for cat, count in top_cats:
        color = cmap(cat_to_idx[cat] / max(len(unique_cats) - 1, 1))
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='w',
                                           markerfacecolor=color, markersize=8,
                                           label=f"{cat} ({count})"))
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    plt.tight_layout()
    plt.savefig(VIZ_DIR / "umap_by_category.png", dpi=150)
    plt.close()
    print(f"    Saved umap_by_category.png")

    return {
        "n_papers": len(coords),
        "n_categories": len(unique_cats),
        "umap_params": {"n_neighbors": 15, "min_dist": 0.1},
    }


def analyze_bertopic(embeddings: np.ndarray, papers: list[dict], arxiv_ids: list[str]):
    """BERTopic topic modeling."""
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer

    print("  Running BERTopic...")
    id_to_paper = {p["arxiv_id"]: p for p in papers}
    docs = [id_to_paper.get(aid, {}).get("abstract", "") for aid in arxiv_ids]

    # Use pre-computed embeddings
    topic_model = BERTopic(
        nr_topics="auto",
        min_topic_size=30,
        vectorizer_model=CountVectorizer(stop_words="english", max_features=5000),
        verbose=False,
    )
    topics, probs = topic_model.fit_transform(docs, embeddings=embeddings)

    # Get topic info
    topic_info = topic_model.get_topic_info()
    n_topics = len(topic_info) - 1  # Exclude -1 (outliers)
    outlier_count = sum(1 for t in topics if t == -1)

    print(f"    Found {n_topics} topics, {outlier_count} outliers ({outlier_count/len(topics)*100:.1f}%)")

    # Top 10 topics
    top_topics = topic_info[topic_info["Topic"] != -1].head(10)
    topic_summary = []
    for _, row in top_topics.iterrows():
        topic_id = row["Topic"]
        count = row["Count"]
        # Get top words
        topic_words = topic_model.get_topic(topic_id)
        words = [w for w, _ in topic_words[:5]]
        topic_summary.append({
            "topic_id": int(topic_id),
            "count": int(count),
            "top_words": words,
        })
        print(f"    Topic {topic_id}: {count} papers — {', '.join(words)}")

    # Category-topic alignment
    print("\n  Analyzing category-topic alignment...")
    cat_topic_matrix = defaultdict(lambda: Counter())
    for aid, topic in zip(arxiv_ids, topics):
        if topic == -1:
            continue
        cat = id_to_paper.get(aid, {}).get("primary_category", "unknown")
        cat_topic_matrix[cat][topic] += 1

    # For each topic, compute category concentration (entropy-based)
    topic_purity = {}
    for topic_id in range(n_topics):
        cat_dist = {}
        for cat, counts in cat_topic_matrix.items():
            if topic_id in counts:
                cat_dist[cat] = counts[topic_id]
        if cat_dist:
            total = sum(cat_dist.values())
            probs_arr = np.array(list(cat_dist.values())) / total
            entropy = -np.sum(probs_arr * np.log2(probs_arr + 1e-10))
            max_entropy = np.log2(len(cat_dist)) if len(cat_dist) > 1 else 1
            purity = 1 - (entropy / max_entropy) if max_entropy > 0 else 1
            dominant_cat = max(cat_dist, key=cat_dist.get)
            topic_purity[topic_id] = {
                "purity": round(float(purity), 4),
                "dominant_category": dominant_cat,
                "dominant_fraction": round(cat_dist[dominant_cat] / total, 4),
                "n_categories": len(cat_dist),
            }

    avg_purity = np.mean([v["purity"] for v in topic_purity.values()]) if topic_purity else 0
    print(f"    Average topic purity: {avg_purity:.4f} (1.0 = perfect category alignment)")

    high_purity = sum(1 for v in topic_purity.values() if v["purity"] > 0.7)
    low_purity = sum(1 for v in topic_purity.values() if v["purity"] < 0.3)
    print(f"    High purity (>0.7): {high_purity}/{n_topics}")
    print(f"    Low purity (<0.3): {low_purity}/{n_topics}")

    return {
        "n_topics": n_topics,
        "outlier_count": outlier_count,
        "outlier_fraction": round(outlier_count / len(topics), 4),
        "top_topics": topic_summary,
        "avg_topic_purity": round(float(avg_purity), 4),
        "high_purity_count": high_purity,
        "low_purity_count": low_purity,
        "topic_purity": {str(k): v for k, v in list(topic_purity.items())[:20]},
    }


def analyze_category_cooccurrence(papers: list[dict]):
    """Category co-occurrence heatmap."""
    print("  Computing category co-occurrence...")

    # Count co-occurrences
    cooccurrence = Counter()
    cat_counts = Counter()
    multi_cat_count = 0

    for p in papers:
        cats = [c.strip() for c in (p.get("categories") or "").split() if c.strip()]
        if len(cats) > 1:
            multi_cat_count += 1
        for c in cats:
            cat_counts[c] += 1
        for i, c1 in enumerate(cats):
            for c2 in cats[i+1:]:
                pair = tuple(sorted([c1, c2]))
                cooccurrence[pair] += 1

    # Top categories
    top_cats = [c for c, _ in cat_counts.most_common(15)]

    # Build matrix
    n = len(top_cats)
    matrix = np.zeros((n, n))
    for i, c1 in enumerate(top_cats):
        for j, c2 in enumerate(top_cats):
            if i == j:
                matrix[i][j] = cat_counts[c1]
            else:
                pair = tuple(sorted([c1, c2]))
                matrix[i][j] = cooccurrence.get(pair, 0)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(matrix, cmap='YlOrRd')
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(top_cats, rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(top_cats, fontsize=8)
    ax.set_title("Category Co-occurrence (top 15 categories)")
    plt.colorbar(im, ax=ax, label="Paper count")
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "category_cooccurrence.png", dpi=150)
    plt.close()
    print(f"    Saved category_cooccurrence.png")

    print(f"    Multi-category papers: {multi_cat_count}/{len(papers)} ({multi_cat_count/len(papers)*100:.1f}%)")
    print(f"    Top 5 co-occurrences:")
    for pair, count in cooccurrence.most_common(5):
        print(f"      {pair[0]} + {pair[1]}: {count}")

    return {
        "multi_category_count": multi_cat_count,
        "multi_category_fraction": round(multi_cat_count / len(papers), 4),
        "top_categories": [(c, count) for c, count in cat_counts.most_common(15)],
        "top_cooccurrences": [(list(pair), count) for pair, count in cooccurrence.most_common(10)],
    }


def analyze_temporal(papers: list[dict]):
    """Temporal patterns."""
    print("  Analyzing temporal patterns...")

    from collections import Counter
    day_counts = Counter()

    for p in papers:
        date = p.get("submitted_date") or p.get("updated_date") or ""
        if date and len(date) >= 10:
            day_counts[date[:10]] += 1

    if not day_counts:
        print("    No date data available")
        return {"error": "no date data"}

    sorted_days = sorted(day_counts.items())

    fig, ax = plt.subplots(figsize=(14, 5))
    days = [d for d, _ in sorted_days]
    counts = [c for _, c in sorted_days]
    ax.bar(range(len(days)), counts, color='steelblue')
    ax.set_xlabel("Day")
    ax.set_ylabel("Papers submitted")
    ax.set_title("Papers per day (January 2026)")
    # Show every 5th label
    tick_positions = list(range(0, len(days), 5))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([days[i] for i in tick_positions], rotation=45, ha='right', fontsize=8)
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "temporal_pattern.png", dpi=150)
    plt.close()
    print(f"    Saved temporal_pattern.png")

    return {
        "total_days": len(day_counts),
        "mean_per_day": round(np.mean(counts), 1),
        "median_per_day": round(float(np.median(counts)), 1),
        "max_per_day": max(counts),
        "min_per_day": min(counts),
    }


def analyze_authors(papers: list[dict]):
    """Author frequency distribution."""
    print("  Analyzing author frequency...")

    author_counts = Counter()
    for p in papers:
        authors = (p.get("authors_text") or "").split(",")
        for a in authors:
            a = a.strip()
            if a:
                author_counts[a] += 1

    total_authors = len(author_counts)
    papers_per_author = list(author_counts.values())

    percentiles = {
        "p50": round(float(np.median(papers_per_author)), 1),
        "p90": round(float(np.percentile(papers_per_author, 90)), 1),
        "p99": round(float(np.percentile(papers_per_author, 99)), 1),
        "max": max(papers_per_author),
    }

    print(f"    Total unique authors: {total_authors}")
    print(f"    Papers/author: median={percentiles['p50']}, p90={percentiles['p90']}, p99={percentiles['p99']}, max={percentiles['max']}")
    print(f"    Top 5 authors:")
    for author, count in author_counts.most_common(5):
        print(f"      {author}: {count} papers")

    # Plot distribution
    fig, ax = plt.subplots(figsize=(10, 5))
    max_papers = min(max(papers_per_author), 20)
    bins = range(1, max_papers + 2)
    ax.hist(papers_per_author, bins=bins, color='steelblue', edgecolor='white')
    ax.set_xlabel("Papers per author")
    ax.set_ylabel("Number of authors")
    ax.set_title(f"Author productivity distribution ({total_authors} unique authors)")
    ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig(VIZ_DIR / "author_frequency.png", dpi=150)
    plt.close()
    print(f"    Saved author_frequency.png")

    return {
        "total_unique_authors": total_authors,
        "percentiles": percentiles,
        "top_authors": [(a, c) for a, c in author_counts.most_common(10)],
    }


def main():
    print("=" * 80)
    print("A2: Corpus Visualization and Structure")
    print("=" * 80)

    VIZ_DIR.mkdir(parents=True, exist_ok=True)

    papers = load_papers()
    print(f"Loaded {len(papers)} papers")

    # Load embeddings
    if not EMBEDDINGS_PATH.exists():
        print(f"ERROR: Embeddings not found at {EMBEDDINGS_PATH}")
        print("Run Spike 002 setup_spike002.py first.")
        return

    embeddings = np.load(EMBEDDINGS_PATH)
    with open(ARXIV_IDS_PATH) as f:
        arxiv_ids = json.load(f)
    print(f"Loaded {len(arxiv_ids)} embeddings ({embeddings.shape})")

    results = {}

    # 1. UMAP
    print("\n1. UMAP visualization...")
    results["umap"] = analyze_umap(embeddings, papers, arxiv_ids)

    # 2. BERTopic
    print("\n2. BERTopic topic modeling...")
    results["bertopic"] = analyze_bertopic(embeddings, papers, arxiv_ids)

    # 3. Category co-occurrence
    print("\n3. Category co-occurrence...")
    results["category_cooccurrence"] = analyze_category_cooccurrence(papers)

    # 4. Temporal patterns
    print("\n4. Temporal patterns...")
    results["temporal"] = analyze_temporal(papers)

    # 5. Author frequency
    print("\n5. Author frequency...")
    results["authors"] = analyze_authors(papers)

    # Save results
    results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n{'=' * 80}")
    print(f"Results saved to {RESULTS_PATH.name}")
    print(f"Visualizations saved to {VIZ_DIR.name}/")
    print(f"{'=' * 80}")

    # Key finding for deployment relevance
    purity = results["bertopic"].get("avg_topic_purity", 0)
    if purity > 0.6:
        print(f"\nDEPLOYMENT RELEVANCE: Topic purity {purity:.2f} — categories align with topics.")
        print("Category-based pre-filtering is likely valid.")
    elif purity > 0.3:
        print(f"\nDEPLOYMENT RELEVANCE: Topic purity {purity:.2f} — moderate alignment.")
        print("Category pre-filtering partially valid but will miss cross-domain papers.")
    else:
        print(f"\nDEPLOYMENT RELEVANCE: Topic purity {purity:.2f} — poor alignment.")
        print("Category pre-filtering is QUESTIONABLE — topics don't follow categories.")


if __name__ == "__main__":
    main()
