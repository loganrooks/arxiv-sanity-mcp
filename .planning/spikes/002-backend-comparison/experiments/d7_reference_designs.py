"""
D7: Reference Design Comparison

Measure search latency of external systems users actually interact with.
Contextualizes our local benchmarks — "30ms search" means nothing without
knowing what users are accustomed to.

Systems tested:
1. Semantic Scholar API (search endpoint)
2. OpenAlex API (works search endpoint)
3. arXiv API (search endpoint)

Usage:
    python d7_reference_designs.py
"""

import json
import statistics
import time
from pathlib import Path
from urllib.parse import quote

import httpx

DATA_DIR = Path(__file__).parent / "data"
RESULTS_PATH = DATA_DIR / "d7_reference_designs_results.json"

# Representative queries (subset of our 20)
QUERIES = [
    "transformer",
    "language model",
    "reinforcement learning",
    "graph neural network",
    "causal inference",
    "diffusion model",
    "federated learning",
    "self-supervised contrastive",
    "attention mechanism",
    "survey machine learning",
]

RUNS_PER_QUERY = 3
REQUEST_DELAY = 1.0  # Be polite to external APIs


def measure_api(name, url_fn, parse_fn):
    """Measure API latency for a set of queries."""
    print(f"\n  {name}:")
    results = []

    for query in QUERIES:
        url = url_fn(query)
        latencies = []
        result_count = None
        error = None

        for run in range(RUNS_PER_QUERY):
            try:
                t0 = time.perf_counter()
                resp = httpx.get(url, timeout=30, follow_redirects=True)
                elapsed = (time.perf_counter() - t0) * 1000
                latencies.append(elapsed)

                if run == 0 and resp.status_code == 200:
                    result_count = parse_fn(resp)

                time.sleep(REQUEST_DELAY)
            except Exception as e:
                error = str(e)
                break

        if latencies:
            entry = {
                "query": query,
                "p50_ms": round(statistics.median(latencies), 1),
                "mean_ms": round(statistics.mean(latencies), 1),
                "min_ms": round(min(latencies), 1),
                "max_ms": round(max(latencies), 1),
                "result_count": result_count,
            }
            print(f"    {query:35s}  p50={entry['p50_ms']:>8.1f}ms  results={result_count}")
        else:
            entry = {"query": query, "error": error}
            print(f"    {query:35s}  ERROR: {error}")

        results.append(entry)

    # Summary
    valid = [r for r in results if "p50_ms" in r]
    if valid:
        avg_p50 = statistics.mean(r["p50_ms"] for r in valid)
        return {
            "queries": results,
            "avg_p50_ms": round(avg_p50, 1),
            "n_successful": len(valid),
            "n_failed": len(results) - len(valid),
        }
    return {"queries": results, "error": "all queries failed"}


def main():
    print("=" * 80)
    print("D7: Reference Design Comparison")
    print("=" * 80)

    all_results = {}

    # 1. Semantic Scholar
    all_results["semantic_scholar"] = measure_api(
        "Semantic Scholar API",
        lambda q: f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote(q)}&limit=20&fields=title,year,citationCount",
        lambda resp: resp.json().get("total", 0) if resp.status_code == 200 else None,
    )

    # 2. OpenAlex
    all_results["openalex"] = measure_api(
        "OpenAlex API",
        lambda q: f"https://api.openalex.org/works?search={quote(q)}&per_page=20&mailto=arxiv_mcp@example.com",
        lambda resp: resp.json().get("meta", {}).get("count", 0) if resp.status_code == 200 else None,
    )

    # 3. arXiv API
    all_results["arxiv_api"] = measure_api(
        "arXiv API",
        lambda q: f"https://export.arxiv.org/api/query?search_query=all:{quote(q)}&start=0&max_results=20",
        lambda resp: None,  # XML parsing not worth it for latency test
    )

    # Comparison table
    print(f"\n{'=' * 80}")
    print("COMPARISON TABLE")
    print(f"{'=' * 80}")
    print(f"  {'System':<30s} {'Avg p50':>10s} {'Type':>10s} {'Corpus':>12s}")
    print(f"  {'-' * 65}")

    # Our local numbers (from D2 at 19K)
    print(f"  {'Our FTS5 (19K)':<30s} {'~2ms':>10s} {'Local':>10s} {'19K':>12s}")
    print(f"  {'Our tsvector (19K)':<30s} {'~7ms':>10s} {'Local':>10s} {'19K':>12s}")
    print(f"  {'Our HNSW (19K)':<30s} {'~1ms':>10s} {'Local':>10s} {'19K':>12s}")

    for name, data in all_results.items():
        if "avg_p50_ms" in data:
            label = name.replace("_", " ").title()
            corpus = {"semantic_scholar": "200M+", "openalex": "250M+", "arxiv_api": "2M+"}.get(name, "?")
            print(f"  {label:<30s} {data['avg_p50_ms']:>8.1f}ms {'Remote':>10s} {corpus:>12s}")

    print(f"\n  Note: Remote APIs include network latency (this machine → API server).")
    print(f"  Local numbers are database query time only.")

    # Save
    all_results["timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")
    all_results["note"] = (
        "Remote API latencies include network RTT from Dionysus (Tailscale node, "
        "residential internet). Local numbers are database query time only. "
        "Comparison is for user experience context, not engine efficiency."
    )

    with open(RESULTS_PATH, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to {RESULTS_PATH.name}")


if __name__ == "__main__":
    main()
