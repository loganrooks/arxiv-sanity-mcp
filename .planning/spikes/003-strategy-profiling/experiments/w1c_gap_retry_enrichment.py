#!/usr/bin/env python3
"""
Retry enrichment for papers that got HTTP 429 errors.

The initial run got 944 successful lookups before hitting rate limits.
This script retries with:
  - Slower rate (2 req/s instead of 9)
  - Exponential backoff on 429
  - Auto-resume from checkpoint
"""

import json
import os
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

SPIKE_003_DIR = Path(__file__).resolve().parent.parent
SPIKE_001_DATA = SPIKE_003_DIR.parent / "001-volume-filtering-scoring-landscape" / "experiments" / "data"
EXPERIMENTS_DIR = SPIKE_003_DIR / "experiments"
DATA_DIR = EXPERIMENTS_DIR / "data"

HARVEST_DB = str(SPIKE_001_DATA / "spike_001_harvest.db")
OUTPUT_CACHE = str(DATA_DIR / "expanded_openalex_cache.json")

OPENALEX_BASE = "https://api.openalex.org/works"
OPENALEX_EMAIL = os.environ.get("OPENALEX_EMAIL", "")
OPENALEX_SELECT = ",".join([
    "id", "doi", "title", "cited_by_count",
    "citation_normalized_percentile",
    "topics", "referenced_works", "related_works",
    "authorships", "type", "publication_year",
])

# Slower rate to avoid 429s
BASE_DELAY = 0.6  # ~1.7 req/s
MAX_BACKOFF = 120  # Max wait after 429
CHECKPOINT_INTERVAL = 100


def load_title_index() -> dict[str, str]:
    conn = sqlite3.connect(HARVEST_DB)
    cur = conn.execute("SELECT arxiv_id, title FROM papers")
    index = {row[0]: row[1] for row in cur}
    conn.close()
    return index


def openalex_search(title: str, max_retries: int = 5) -> dict | None:
    """Search OpenAlex with retry and exponential backoff on 429."""
    clean_title = title.strip()
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

    backoff = 2.0
    for attempt in range(max_retries):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                if data.get("results") and len(data["results"]) > 0:
                    return data["results"][0]
                return None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = min(backoff * (2 ** attempt), MAX_BACKOFF)
                print(f"    429 rate limit on attempt {attempt+1}, waiting {wait:.0f}s...")
                time.sleep(wait)
                continue
            return {"error": f"HTTP Error {e.code}: {e.reason}"}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "HTTP Error 429: max retries exceeded"}


def extract_cache_entry(oa_result: dict) -> dict:
    fwci = None
    cnp = oa_result.get("citation_normalized_percentile")
    if cnp and isinstance(cnp, dict):
        fwci = cnp.get("value", 0.0)

    authorships = []
    for auth in oa_result.get("authorships", [])[:20]:
        a = auth.get("author", {})
        authorships.append({
            "name": a.get("display_name", ""),
            "id": a.get("id", ""),
        })

    topics = []
    for topic in oa_result.get("topics", [])[:5]:
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


def main():
    print("=" * 70)
    print("W1C-gap: Retry failed enrichment (429 errors)")
    print("=" * 70)

    # Load existing cache
    with open(OUTPUT_CACHE) as f:
        cache = json.load(f)

    # Find papers with 429 errors
    retry_ids = [
        k for k, v in cache.items()
        if v.get("error", "").startswith("HTTP Error 429")
    ]
    print(f"Papers to retry: {len(retry_ids)}")

    if not retry_ids:
        print("No 429 errors to retry!")
        return

    title_index = load_title_index()

    stats = {"found": 0, "not_found": 0, "errors": 0, "with_refs": 0, "with_related": 0}
    t_start = time.time()

    for i, pid in enumerate(retry_ids):
        # Rate limiting
        time.sleep(BASE_DELAY)

        title = title_index.get(pid)
        if not title:
            cache[pid] = {"error": "no_title_in_db", "arxiv_id": pid}
            continue

        result = openalex_search(title)

        if result is None:
            cache[pid] = {"error": "not_found", "arxiv_id": pid, "searched_title": title}
            stats["not_found"] += 1
        elif "error" in result and isinstance(result.get("error"), str):
            cache[pid] = {"error": result["error"], "arxiv_id": pid, "searched_title": title}
            stats["errors"] += 1
            # If we're still getting 429s after retries, slow down more
            if "429" in result["error"]:
                print(f"  Still getting 429s, pausing 60s...")
                time.sleep(60)
        else:
            entry = extract_cache_entry(result)
            cache[pid] = entry
            stats["found"] += 1
            if entry.get("referenced_works"):
                stats["with_refs"] += 1
            if entry.get("related_works"):
                stats["with_related"] += 1

        if (i + 1) % 50 == 0 or (i + 1) == len(retry_ids):
            elapsed = time.time() - t_start
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (len(retry_ids) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i+1}/{len(retry_ids)}] "
                  f"found={stats['found']} not_found={stats['not_found']} "
                  f"errors={stats['errors']} "
                  f"refs={stats['with_refs']} related={stats['with_related']} "
                  f"rate={rate:.1f}/s ETA={eta:.0f}s")

        if (i + 1) % CHECKPOINT_INTERVAL == 0:
            with open(OUTPUT_CACHE, 'w') as f:
                json.dump(cache, f, indent=2)
            print(f"  -- Checkpoint saved at {i+1} --")

    # Final save
    with open(OUTPUT_CACHE, 'w') as f:
        json.dump(cache, f, indent=2)

    # Summary
    total_ok = sum(1 for v in cache.values() if not v.get("error"))
    total_refs = sum(1 for v in cache.values()
                     if v.get("referenced_works") and len(v["referenced_works"]) > 0)
    total_related = sum(1 for v in cache.values()
                        if v.get("related_works") and len(v["related_works"]) > 0)

    print(f"\n  Retry complete in {time.time() - t_start:.1f}s")
    print(f"  This round: found={stats['found']}, not_found={stats['not_found']}, "
          f"errors={stats['errors']}")
    print(f"  Total cache: {len(cache)} entries, {total_ok} valid")
    print(f"  With refs: {total_refs}, with related: {total_related}")

    remaining_429 = sum(1 for v in cache.values()
                        if v.get("error", "").startswith("HTTP Error 429"))
    if remaining_429 > 0:
        print(f"  Remaining 429 errors: {remaining_429} (run again to retry)")


if __name__ == "__main__":
    main()
