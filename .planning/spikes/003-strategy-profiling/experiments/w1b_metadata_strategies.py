"""
W1B: Profile metadata-based recommendation strategies.

These strategies use paper metadata (categories, authors, dates, enrichment)
without reading content. They span:

  S2a: Category filtering (primary only)
  S2b: Category filtering (any listed)
  S2c: Category co-occurrence boost
  S2d: FWCI ranking (OpenAlex enriched subset)
  S2e: Citation count ranking (OpenAlex enriched subset)
  S2f: Author network (co-author count)
  S2g: Followed author boost (binary co-author)
  S2i: OpenAlex topic matching
  S2j: Recency decay (exponential, 30-day half-life)
  S2m: Cross-listing breadth

Methodology:
  - Each strategy implements the RecommendationStrategy protocol via SimpleStrategy
  - Profiled using the same harness and instruments as embedding strategies (W1A)
  - LOO disabled for strategies with sparse/binary scores (prevents trivial 0 MRR)
  - Resource metrics measured with standard latency harness

Data sources:
  - Harvest DB: 19252 papers with metadata
  - OpenAlex cache: 500 enriched papers (FWCI, citations, topics, authorships)
  - A2 results: Category co-occurrence matrix from Spike 001
  - Interest profiles: 8 profiles with 3 seed sets each
"""

import json
import math
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SPIKE_DIR = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = SPIKE_DIR / "experiments"
DATA_DIR = EXPERIMENTS_DIR / "data"
SPIKES_DIR = SPIKE_DIR.parent

SPIKE001_DATA = SPIKES_DIR / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
SPIKE002_DATA = SPIKES_DIR / "002-backend-comparison" / "experiments" / "data"

SOURCE_DB = SPIKE001_DATA / "spike_001_harvest.db"
OPENALEX_CACHE = SPIKE001_DATA / "b2_openalex_cache.json"
A2_RESULTS = SPIKE001_DATA / "a2_corpus_visualization_results.json"
PROFILES_PATH = DATA_DIR / "interest_profiles.json"

OUTPUT_PATH = DATA_DIR / "w1b_metadata_profiles.json"


class NumpyEncoder(json.JSONEncoder):
    """Handle numpy types in JSON serialization."""

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
# Data loading
# ---------------------------------------------------------------------------

def load_corpus():
    """Load all paper metadata from harvest DB."""
    conn = sqlite3.connect(str(SOURCE_DB))
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT arxiv_id, title, authors_text, abstract, categories, "
        "primary_category, submitted_date FROM papers"
    ).fetchall()
    conn.close()
    corpus = {row["arxiv_id"]: dict(row) for row in rows}
    print(f"Loaded corpus: {len(corpus)} papers")
    return corpus


def load_openalex():
    """Load OpenAlex enrichment cache."""
    with open(OPENALEX_CACHE) as f:
        data = json.load(f)
    print(f"Loaded OpenAlex cache: {len(data)} enriched papers")
    return data


def load_cooccurrence():
    """Load category co-occurrence data from A2 results."""
    with open(A2_RESULTS) as f:
        data = json.load(f)
    cooc = data["category_cooccurrence"]
    # Build co-occurrence matrix as dict: (catA, catB) -> count
    matrix = {}
    for pair_count in cooc["top_cooccurrences"]:
        pair, count = pair_count
        a, b = pair[0], pair[1]
        matrix[(a, b)] = count
        matrix[(b, a)] = count
    # Also extract category frequencies
    cat_freq = {}
    for cat_count in cooc["top_categories"]:
        cat_freq[cat_count[0]] = cat_count[1]
    print(f"Loaded co-occurrence matrix: {len(matrix)} pairs, {len(cat_freq)} categories")
    return matrix, cat_freq


# ---------------------------------------------------------------------------
# Helper: parse categories from corpus record
# ---------------------------------------------------------------------------

def get_categories(paper: dict) -> list[str]:
    """Extract category list from a paper record."""
    cats_str = paper.get("categories", "")
    if not cats_str:
        return []
    return cats_str.strip().split()


def parse_date(date_str: str) -> datetime | None:
    """Parse the submitted_date field.

    Format examples:
      'Thu, 22 Oct 2020 05:19:58 GMT'
      'Mon, 06 Jan 2025 18:00:01 GMT'
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
    except ValueError:
        return None


def normalize_author_name(name: str) -> str:
    """Normalize an author name for matching.

    Handles:
      'First Last' -> 'first last'
      'Last, First' -> 'first last'
      Extra whitespace, periods
    """
    name = name.strip().lower()
    # Remove periods (e.g., 'H. M.' -> 'h m')
    name = name.replace(".", " ")
    # Handle 'Last, First' format
    if "," in name:
        parts = name.split(",", 1)
        name = parts[1].strip() + " " + parts[0].strip()
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name


def extract_author_names(authors_text: str) -> list[str]:
    """Extract individual author names from an authors_text field.

    Field format: comma-separated names, sometimes with 'and'.
    Examples:
      'Alessandro Epasto, Mohammad Mahdian, Vahab Mirrokni, Manolis Zampetakis'
      'Xu Yang and Juantao Zhong and Daoyuan Wu'
    """
    if not authors_text:
        return []
    # Split on ' and ' first, then commas within each part
    # Some entries use 'and' as separator instead of commas
    text = authors_text.replace(" and ", ", ")
    names = [n.strip() for n in text.split(",") if n.strip()]
    return [normalize_author_name(n) for n in names if len(n.strip()) > 1]


# ---------------------------------------------------------------------------
# Strategy implementations
# ---------------------------------------------------------------------------

def build_s2a_primary_category(corpus, paper_ids):
    """S2a: Category filtering (primary only).

    Score = 1.0 if paper's primary_category matches the most common
    primary_category among seed papers, else 0.0.
    """
    all_cats = {aid: corpus[aid].get("primary_category", "") for aid in paper_ids}

    def score_fn(seed_ids):
        # Find most common primary category among seeds
        seed_cats = [all_cats.get(sid, "") for sid in seed_ids if sid in all_cats]
        if not seed_cats:
            return np.zeros(len(paper_ids))
        cat_counts = Counter(seed_cats)
        dominant_cat = cat_counts.most_common(1)[0][0]
        scores = np.array([
            1.0 if all_cats.get(aid, "") == dominant_cat else 0.0
            for aid in paper_ids
        ])
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Category filtering (primary)",
        strategy_id="S2a",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2b_category_listed(corpus, paper_ids):
    """S2b: Category filtering (any listed).

    Score = number of shared categories between paper and seed set.
    """
    all_cats_sets = {aid: set(get_categories(corpus[aid])) for aid in paper_ids}

    def score_fn(seed_ids):
        # Collect all categories from seed papers
        seed_cats = set()
        for sid in seed_ids:
            if sid in all_cats_sets:
                seed_cats.update(all_cats_sets[sid])
        if not seed_cats:
            return np.zeros(len(paper_ids))
        scores = np.array([
            len(all_cats_sets.get(aid, set()) & seed_cats)
            for aid in paper_ids
        ], dtype=np.float64)
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Category filtering (listed)",
        strategy_id="S2b",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2c_cooccurrence_boost(corpus, paper_ids, cooc_matrix, cat_freq):
    """S2c: Category co-occurrence boost.

    Score = sum over paper's categories of: sum over seed categories of
    co-occurrence_count(paper_cat, seed_cat) / max_cooccurrence.

    Uses the category co-occurrence matrix from Spike 001 A2.
    """
    all_cats_lists = {aid: get_categories(corpus[aid]) for aid in paper_ids}

    # Normalize co-occurrence counts by maximum for stability
    max_cooc = max(cooc_matrix.values()) if cooc_matrix else 1.0

    def score_fn(seed_ids):
        # Collect seed categories
        seed_cats = set()
        for sid in seed_ids:
            if sid in all_cats_lists:
                seed_cats.update(all_cats_lists[sid])
        if not seed_cats:
            return np.zeros(len(paper_ids))

        scores = np.zeros(len(paper_ids))
        for i, aid in enumerate(paper_ids):
            paper_cats = all_cats_lists.get(aid, [])
            total = 0.0
            for pc in paper_cats:
                for sc in seed_cats:
                    if pc == sc:
                        # Same category: use that category's frequency as proxy
                        total += cat_freq.get(pc, 0) / max_cooc
                    else:
                        total += cooc_matrix.get((pc, sc), 0) / max_cooc
            scores[i] = total
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Category co-occurrence boost",
        strategy_id="S2c",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2d_fwci(corpus, paper_ids, openalex):
    """S2d: FWCI ranking.

    Score = field-weighted citation impact from OpenAlex.
    Only works for the ~500 enriched papers; score = 0 for unenriched.
    """
    # Pre-compute FWCI lookup
    fwci_lookup = {}
    for aid, oadata in openalex.items():
        fwci = oadata.get("fwci")
        if fwci is not None:
            fwci_lookup[aid] = float(fwci)

    # Note: FWCI is query-independent (doesn't use seeds)
    # but we still follow the protocol
    scores_array = np.array([
        fwci_lookup.get(aid, 0.0) for aid in paper_ids
    ])

    def score_fn(seed_ids):
        return scores_array

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="FWCI ranking",
        strategy_id="S2d",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2e_citation_count(corpus, paper_ids, openalex):
    """S2e: Citation count ranking.

    Score = cited_by_count from OpenAlex.
    Same enriched-subset limitation as S2d.
    """
    cite_lookup = {}
    for aid, oadata in openalex.items():
        count = oadata.get("cited_by_count")
        if count is not None:
            cite_lookup[aid] = float(count)

    scores_array = np.array([
        cite_lookup.get(aid, 0.0) for aid in paper_ids
    ])

    def score_fn(seed_ids):
        return scores_array

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Citation count ranking",
        strategy_id="S2e",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2f_author_network(corpus, paper_ids):
    """S2f: Author network (co-author count).

    Score = number of authors shared between paper and seed set.
    Uses normalized author names from authors_text field.
    """
    # Pre-compute author sets for all papers
    author_sets = {}
    for aid in paper_ids:
        authors_text = corpus[aid].get("authors_text", "")
        author_sets[aid] = set(extract_author_names(authors_text))

    def score_fn(seed_ids):
        # Collect all authors from seed papers
        seed_authors = set()
        for sid in seed_ids:
            if sid in author_sets:
                seed_authors.update(author_sets[sid])
        if not seed_authors:
            return np.zeros(len(paper_ids))

        scores = np.array([
            len(author_sets.get(aid, set()) & seed_authors)
            for aid in paper_ids
        ], dtype=np.float64)
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Author network (co-author count)",
        strategy_id="S2f",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2g_author_boost(corpus, paper_ids):
    """S2g: Followed author boost (binary).

    Score = 1.0 if paper has ANY author in common with seeds, else 0.0.
    """
    author_sets = {}
    for aid in paper_ids:
        authors_text = corpus[aid].get("authors_text", "")
        author_sets[aid] = set(extract_author_names(authors_text))

    def score_fn(seed_ids):
        seed_authors = set()
        for sid in seed_ids:
            if sid in author_sets:
                seed_authors.update(author_sets[sid])
        if not seed_authors:
            return np.zeros(len(paper_ids))

        scores = np.array([
            1.0 if author_sets.get(aid, set()) & seed_authors else 0.0
            for aid in paper_ids
        ], dtype=np.float64)
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Followed author boost",
        strategy_id="S2g",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2i_topic_matching(corpus, paper_ids, openalex):
    """S2i: OpenAlex topic matching.

    Score = number of shared OpenAlex topic IDs between paper and seed set.
    Limited to enriched subset (~500 papers).
    """
    # Pre-compute topic sets
    topic_sets = {}
    for aid, oadata in openalex.items():
        topics = oadata.get("topics", [])
        topic_ids = set()
        for t in topics:
            if isinstance(t, dict) and "id" in t:
                topic_ids.add(t["id"])
        if topic_ids:
            topic_sets[aid] = topic_ids

    def score_fn(seed_ids):
        # Collect topic IDs from seed papers
        seed_topics = set()
        for sid in seed_ids:
            if sid in topic_sets:
                seed_topics.update(topic_sets[sid])
        if not seed_topics:
            return np.zeros(len(paper_ids))

        scores = np.array([
            len(topic_sets.get(aid, set()) & seed_topics)
            for aid in paper_ids
        ], dtype=np.float64)
        return scores

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="OpenAlex topic matching",
        strategy_id="S2i",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2j_recency_decay(corpus, paper_ids):
    """S2j: Recency decay.

    Score = exp(-lambda * days_since_submission) where lambda = ln(2)/30
    (30-day half-life). Query-independent.
    """
    # Parse all dates and find the reference date (latest submission)
    dates = {}
    for aid in paper_ids:
        dt = parse_date(corpus[aid].get("submitted_date", ""))
        if dt:
            dates[aid] = dt

    if not dates:
        print("  WARNING: No parseable dates found")
        scores_array = np.zeros(len(paper_ids))
    else:
        ref_date = max(dates.values())
        half_life_days = 30.0
        lam = math.log(2) / half_life_days

        scores_array = np.array([
            math.exp(-lam * (ref_date - dates[aid]).total_seconds() / 86400.0)
            if aid in dates else 0.0
            for aid in paper_ids
        ])
        # Report date range
        min_date = min(dates.values())
        days_range = (ref_date - min_date).total_seconds() / 86400.0
        print(f"  Date range: {min_date.strftime('%Y-%m-%d')} to {ref_date.strftime('%Y-%m-%d')} ({days_range:.0f} days)")
        print(f"  Parseable dates: {len(dates)}/{len(paper_ids)}")
        print(f"  Score range: [{scores_array[scores_array > 0].min():.6f}, {scores_array.max():.6f}]")

    def score_fn(seed_ids):
        return scores_array

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Recency decay (30d half-life)",
        strategy_id="S2j",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


def build_s2m_crosslisting_breadth(corpus, paper_ids):
    """S2m: Cross-listing breadth.

    Score = number of categories a paper is listed in.
    Query-independent (doesn't use seeds).
    """
    scores_array = np.array([
        float(len(get_categories(corpus[aid])))
        for aid in paper_ids
    ])

    def score_fn(seed_ids):
        return scores_array

    from harness.strategy_protocol import SimpleStrategy
    return SimpleStrategy(
        name="Cross-listing breadth",
        strategy_id="S2m",
        score_fn=score_fn,
        paper_ids=paper_ids,
    )


# ---------------------------------------------------------------------------
# Enriched-subset profiling wrapper
# ---------------------------------------------------------------------------

def profile_enriched_subset(profiler, strategy, openalex_ids, config_extra=None):
    """Profile a strategy on only the enriched (OpenAlex) paper subset.

    For strategies that only score enriched papers (S2d, S2e, S2i), we need
    to report that coverage is limited. We run on the full corpus but note
    coverage in config.
    """
    config = {
        "enriched_only": True,
        "enriched_count": len(openalex_ids),
        "corpus_count": len(profiler.paper_ids),
        "coverage_fraction": len(openalex_ids) / len(profiler.paper_ids),
    }
    if config_extra:
        config.update(config_extra)

    card = profiler.profile(
        strategy,
        config=config,
        top_k=20,
        run_loo=False,  # LOO meaningless for citation-only ranking
        measure_resources=True,
        latency_n_runs=100,
    )
    return card


# ---------------------------------------------------------------------------
# Coverage analysis
# ---------------------------------------------------------------------------

def analyze_coverage(strategy_name, strategy, paper_ids, profiles):
    """Report how many papers actually get non-zero scores."""
    coverage_info = {}
    for prof in profiles:
        seed_set = prof.seed_sets[0]  # Use first seed set
        recs = strategy.recommend(seed_set, top_k=len(paper_ids))
        non_zero = sum(1 for _, score in recs if score > 0)
        coverage_info[prof.profile_id] = {
            "non_zero_scored": non_zero,
            "total_candidates": len(recs),
            "fraction": non_zero / max(len(recs), 1),
        }
    return coverage_info


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    t_start = time.time()
    print("=" * 70)
    print("W1B: Metadata Strategy Profiling")
    print("=" * 70)

    # Add experiment dir to path for harness imports
    sys.path.insert(0, str(EXPERIMENTS_DIR))
    from harness import StrategyProfiler

    # Load data
    print("\n--- Loading data ---")
    corpus = load_corpus()
    openalex = load_openalex()
    cooc_matrix, cat_freq = load_cooccurrence()

    # Load profiler (loads embeddings, clusters, profiles)
    print("\n--- Initializing profiler ---")
    profiler = StrategyProfiler.from_spike_data()
    paper_ids = profiler.paper_ids
    profiles = profiler.profiles

    openalex_ids = set(openalex.keys())

    # Pre-analysis: author and category stats
    print("\n--- Pre-analysis ---")

    # Author stats
    all_author_counts = []
    total_unique_authors = set()
    for aid in paper_ids:
        names = extract_author_names(corpus[aid].get("authors_text", ""))
        all_author_counts.append(len(names))
        total_unique_authors.update(names)
    print(f"Author stats: {len(total_unique_authors)} unique normalized names")
    print(f"  Authors per paper: mean={np.mean(all_author_counts):.1f}, "
          f"max={max(all_author_counts)}, papers_with_0={sum(1 for c in all_author_counts if c == 0)}")

    # Category distribution
    cat_counts = Counter()
    for aid in paper_ids:
        cats = get_categories(corpus[aid])
        cat_counts.update(cats)
    print(f"Category stats: {len(cat_counts)} distinct categories")
    print(f"  Top 5: {cat_counts.most_common(5)}")

    # Date coverage
    dates_parsed = sum(1 for aid in paper_ids if parse_date(corpus[aid].get("submitted_date", "")))
    print(f"Date coverage: {dates_parsed}/{len(paper_ids)} parseable dates")

    # OpenAlex coverage relative to seeds
    print(f"\nOpenAlex enriched: {len(openalex_ids)} papers ({100*len(openalex_ids)/len(paper_ids):.1f}% of corpus)")
    for prof in profiles:
        seed_enriched = sum(1 for sid in prof.seed_sets[0] if sid in openalex_ids)
        cluster_enriched = sum(1 for cid in prof.cluster_papers if cid in openalex_ids)
        print(f"  {prof.profile_id} ({prof.name}): "
              f"seeds {seed_enriched}/{len(prof.seed_sets[0])} enriched, "
              f"cluster {cluster_enriched}/{len(prof.cluster_papers)} enriched")

    # ===================================================================
    # Build all strategies
    # ===================================================================
    print("\n" + "=" * 70)
    print("Building strategies...")
    print("=" * 70)

    strategies = {}

    print("\nS2a: Category filtering (primary)...")
    strategies["S2a"] = build_s2a_primary_category(corpus, paper_ids)

    print("S2b: Category filtering (listed)...")
    strategies["S2b"] = build_s2b_category_listed(corpus, paper_ids)

    print("S2c: Category co-occurrence boost...")
    strategies["S2c"] = build_s2c_cooccurrence_boost(corpus, paper_ids, cooc_matrix, cat_freq)

    print("S2d: FWCI ranking...")
    strategies["S2d"] = build_s2d_fwci(corpus, paper_ids, openalex)

    print("S2e: Citation count ranking...")
    strategies["S2e"] = build_s2e_citation_count(corpus, paper_ids, openalex)

    print("S2f: Author network (co-author count)...")
    strategies["S2f"] = build_s2f_author_network(corpus, paper_ids)

    print("S2g: Followed author boost...")
    strategies["S2g"] = build_s2g_author_boost(corpus, paper_ids)

    print("S2i: OpenAlex topic matching...")
    strategies["S2i"] = build_s2i_topic_matching(corpus, paper_ids, openalex)

    print("S2j: Recency decay (30d half-life)...")
    strategies["S2j"] = build_s2j_recency_decay(corpus, paper_ids)

    print("S2m: Cross-listing breadth...")
    strategies["S2m"] = build_s2m_crosslisting_breadth(corpus, paper_ids)

    # ===================================================================
    # Profile each strategy
    # ===================================================================
    print("\n" + "=" * 70)
    print("Profiling strategies...")
    print("=" * 70)

    results = {}

    # Category strategies: full LOO for S2a and S2b (category-aware, reasonable LOO)
    # S2c: full LOO (still category-aware)
    for sid in ["S2a", "S2b", "S2c"]:
        strat = strategies[sid]
        print(f"\n--- Profiling {sid}: {strat.name} ---")
        t0 = time.time()
        card = profiler.profile(
            strat,
            config={"type": "category", "coverage": "full_corpus"},
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=100,
        )
        dt = time.time() - t0
        card["profiling_time_s"] = round(dt, 1)
        # Coverage analysis
        card["coverage_analysis"] = analyze_coverage(sid, strat, paper_ids, profiles)
        results[sid] = card
        print(f"  Completed in {dt:.1f}s")

    # Enriched-only strategies: S2d, S2e, S2i
    # These rank mostly zeros since only 500/19252 papers are enriched.
    # LOO is disabled because it would be meaningless.
    for sid in ["S2d", "S2e", "S2i"]:
        strat = strategies[sid]
        print(f"\n--- Profiling {sid}: {strat.name} (enriched subset) ---")
        t0 = time.time()
        config_extra = {"type": "enrichment"}
        if sid == "S2d":
            # Report FWCI stats
            fwcis = [openalex[aid].get("fwci", 0) for aid in openalex if openalex[aid].get("fwci") is not None]
            config_extra["fwci_stats"] = {
                "n_with_fwci": len(fwcis),
                "non_zero": sum(1 for f in fwcis if f > 0),
                "mean": float(np.mean(fwcis)) if fwcis else 0,
                "median": float(np.median(fwcis)) if fwcis else 0,
            }
        elif sid == "S2e":
            cites = [openalex[aid].get("cited_by_count", 0) for aid in openalex]
            config_extra["citation_stats"] = {
                "n_with_citations": sum(1 for c in cites if c > 0),
                "mean": float(np.mean(cites)),
                "median": float(np.median(cites)),
                "max": int(max(cites)),
            }
        elif sid == "S2i":
            topics_per = [len(openalex[aid].get("topics", [])) for aid in openalex]
            config_extra["topic_stats"] = {
                "papers_with_topics": sum(1 for t in topics_per if t > 0),
                "mean_topics_per_paper": float(np.mean(topics_per)),
            }
        card = profile_enriched_subset(profiler, strat, openalex_ids, config_extra)
        dt = time.time() - t0
        card["profiling_time_s"] = round(dt, 1)
        card["coverage_analysis"] = analyze_coverage(sid, strat, paper_ids, profiles)
        results[sid] = card
        print(f"  Completed in {dt:.1f}s")

    # Author strategies: S2f, S2g
    # LOO is meaningful here -- can a co-author strategy find held-out cluster papers?
    for sid in ["S2f", "S2g"]:
        strat = strategies[sid]
        print(f"\n--- Profiling {sid}: {strat.name} ---")
        t0 = time.time()
        card = profiler.profile(
            strat,
            config={"type": "author", "coverage": "full_corpus"},
            top_k=20,
            run_loo=True,
            measure_resources=True,
            latency_n_runs=100,
        )
        dt = time.time() - t0
        card["profiling_time_s"] = round(dt, 1)
        card["coverage_analysis"] = analyze_coverage(sid, strat, paper_ids, profiles)
        results[sid] = card
        print(f"  Completed in {dt:.1f}s")

    # Query-independent strategies: S2j, S2m
    # LOO disabled -- recency and breadth are not seed-sensitive
    for sid in ["S2j", "S2m"]:
        strat = strategies[sid]
        print(f"\n--- Profiling {sid}: {strat.name} ---")
        t0 = time.time()
        card = profiler.profile(
            strat,
            config={"type": "query_independent", "coverage": "full_corpus"},
            top_k=20,
            run_loo=False,
            measure_resources=True,
            latency_n_runs=100,
        )
        dt = time.time() - t0
        card["profiling_time_s"] = round(dt, 1)
        card["coverage_analysis"] = analyze_coverage(sid, strat, paper_ids, profiles)
        results[sid] = card
        print(f"  Completed in {dt:.1f}s")

    # ===================================================================
    # Comparison
    # ===================================================================
    print("\n" + "=" * 70)
    print("Comparing all strategies...")
    print("=" * 70)

    all_cards = [results[sid] for sid in sorted(results.keys())]
    comparison = profiler.compare(all_cards)

    # ===================================================================
    # Summary table
    # ===================================================================
    print("\n" + "=" * 70)
    print("SUMMARY: Metadata Strategy Profiles")
    print("=" * 70)

    # Header
    inst_names = [
        "leave_one_out_mrr", "seed_proximity", "topical_coherence",
        "cluster_diversity", "novelty", "category_surprise", "coverage",
    ]
    short_names = {
        "leave_one_out_mrr": "LOO-MRR",
        "seed_proximity": "SeedProx",
        "topical_coherence": "Coherence",
        "cluster_diversity": "ClustDiv",
        "novelty": "Novelty",
        "category_surprise": "CatSurp",
        "coverage": "Coverage",
    }

    header = f"{'Strategy':<35s}"
    for iname in inst_names:
        header += f" {short_names[iname]:>9s}"
    header += f" {'p50ms':>7s} {'p95ms':>7s}"
    print(header)
    print("-" * len(header))

    for sid in sorted(results.keys()):
        card = results[sid]
        row = f"{sid} {card['strategy_name']:<31s}"
        instruments = card.get("instruments", {})
        for iname in inst_names:
            val = instruments.get(iname, {}).get("mean")
            if val is not None:
                row += f" {val:9.4f}"
            else:
                row += f" {'---':>9s}"
        # Latency
        lat = card.get("resources", {}).get("query_latency_ms", {})
        p50 = lat.get("p50")
        p95 = lat.get("p95")
        row += f" {p50:7.2f}" if p50 is not None else f" {'---':>7s}"
        row += f" {p95:7.2f}" if p95 is not None else f" {'---':>7s}"
        print(row)

    # Coverage summary
    print(f"\n{'Strategy':<35s} {'NonZero%':>9s} (avg across profiles)")
    print("-" * 50)
    for sid in sorted(results.keys()):
        card = results[sid]
        cov = card.get("coverage_analysis", {})
        if cov:
            fracs = [v["fraction"] for v in cov.values()]
            avg_frac = np.mean(fracs) if fracs else 0
            print(f"{sid} {card['strategy_name']:<31s} {100*avg_frac:8.1f}%")

    # ===================================================================
    # Save results
    # ===================================================================
    output = {
        "metadata": {
            "worklet": "W1B",
            "description": "Metadata strategy profiles",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "corpus_size": len(paper_ids),
            "n_enriched": len(openalex_ids),
            "n_profiles": len(profiles),
            "strategies_profiled": sorted(results.keys()),
            "total_time_s": round(time.time() - t_start, 1),
        },
        "pre_analysis": {
            "author_stats": {
                "unique_normalized_names": len(total_unique_authors),
                "mean_per_paper": float(np.mean(all_author_counts)),
                "max_per_paper": max(all_author_counts),
                "papers_with_zero_authors": sum(1 for c in all_author_counts if c == 0),
            },
            "category_stats": {
                "distinct_categories": len(cat_counts),
                "top_10": cat_counts.most_common(10),
            },
            "date_coverage": {
                "parseable": dates_parsed,
                "total": len(paper_ids),
                "fraction": dates_parsed / len(paper_ids),
            },
            "openalex_coverage": {
                "enriched_papers": len(openalex_ids),
                "corpus_papers": len(paper_ids),
                "fraction": len(openalex_ids) / len(paper_ids),
            },
        },
        "strategy_profiles": results,
        "comparison": comparison,
    }

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"\nResults saved to {OUTPUT_PATH}")
    print(f"Total time: {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
