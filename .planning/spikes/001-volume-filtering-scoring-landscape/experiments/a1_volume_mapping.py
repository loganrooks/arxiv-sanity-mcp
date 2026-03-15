"""Phase A1: Volume Mapping

Harvest 1 calendar month of arXiv papers at multiple category configurations
to measure actual volume dynamics. Stores results in a local SQLite database
for analysis (separate from the project's main database).

Usage:
    conda run -n ml-dev python a1_volume_mapping.py --config all
    conda run -n ml-dev python a1_volume_mapping.py --config big4
    conda run -n ml-dev python a1_volume_mapping.py --config configured
    conda run -n ml-dev python a1_volume_mapping.py --config all-cs

Run from the experiments/ directory.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from datetime import date
from pathlib import Path

import structlog
from oaipmh_scythe import Scythe

# Add project root to path for imports
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "src"))

from arxiv_mcp.ingestion.parsers import parse_arxiv_raw

logger = structlog.get_logger(__name__)

# --- Category Configurations ---

CONFIGS = {
    "big4": {
        "description": "Core ML/AI categories (cs.AI, cs.CL, cs.CV, cs.LG)",
        "categories": {"cs.AI", "cs.CL", "cs.CV", "cs.LG"},
        "archives": ["cs"],
    },
    "configured": {
        "description": "All 15 configured categories from categories.toml",
        "categories": {
            "cs.AI", "cs.CL", "cs.CV", "cs.LG", "cs.NE", "cs.IR", "cs.MA", "cs.RO",
            "stat.ML", "stat.TH",
            "math.OC", "math.ST",
            "eess.AS", "eess.IV", "eess.SP",
        },
        "archives": ["cs", "stat", "math", "eess"],
    },
    "all-cs": {
        "description": "All CS subcategories (37 categories)",
        "categories": set(),  # empty = accept all within archive
        "archives": ["cs"],
    },
}

# --- Database Setup ---

DB_PATH = Path(__file__).parent / "data" / "spike_001_harvest.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS papers (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    authors_text TEXT,
    abstract TEXT,
    categories TEXT,
    primary_category TEXT,
    submitted_date TEXT,
    updated_date TEXT,
    announced_date TEXT,
    oai_datestamp TEXT,
    license_uri TEXT,
    latest_version INTEGER,
    harvest_config TEXT,
    harvested_at TEXT
)
"""

CREATE_INDEX = """
CREATE INDEX IF NOT EXISTS idx_papers_config ON papers(harvest_config);
CREATE INDEX IF NOT EXISTS idx_papers_primary_cat ON papers(primary_category);
CREATE INDEX IF NOT EXISTS idx_papers_datestamp ON papers(oai_datestamp);
"""


def init_db() -> sqlite3.Connection:
    """Initialize the spike SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(CREATE_TABLE)
    for stmt in CREATE_INDEX.strip().split(";"):
        if stmt.strip():
            conn.execute(stmt)
    conn.commit()
    return conn


def matches_categories(paper_categories: str, allowed: set[str]) -> bool:
    """Check if any paper category matches the allowed set."""
    if not allowed:
        return True  # empty = accept all
    paper_cats = paper_categories.split() if paper_categories else []
    return bool(set(paper_cats) & allowed)


def harvest_month(
    config_name: str,
    from_date: str = "2026-01-01",
    until_date: str = "2026-01-31",
    rate_limit: float = 3.0,
) -> dict:
    """Harvest one month of data for a given category configuration.

    Returns harvest statistics.
    """
    config = CONFIGS[config_name]
    conn = init_db()

    oai_url = "https://oaipmh.arxiv.org/oai"
    stats = {
        "config": config_name,
        "description": config["description"],
        "from_date": from_date,
        "until_date": until_date,
        "total_fetched": 0,
        "total_matched": 0,
        "total_skipped": 0,
        "total_new": 0,
        "total_duplicate": 0,
        "errors": 0,
        "categories_seen": {},
        "daily_counts": {},
    }

    for archive in config["archives"]:
        print(f"\n--- Harvesting archive: {archive} for config: {config_name} ---")

        try:
            with Scythe(oai_url) as scythe:
                records = scythe.list_records(
                    metadata_prefix="arXivRaw",
                    set_=archive,
                    from_=from_date,
                    until=until_date,
                )

                for record in records:
                    stats["total_fetched"] += 1

                    if stats["total_fetched"] % 500 == 0:
                        print(f"  Fetched {stats['total_fetched']} records, "
                              f"matched {stats['total_matched']}...")

                    try:
                        raw = parse_arxiv_raw(record.metadata)

                        # Category filtering
                        if not matches_categories(raw.categories, config["categories"]):
                            stats["total_skipped"] += 1
                            continue

                        stats["total_matched"] += 1

                        # Track category distribution
                        for cat in (raw.categories or "").split():
                            stats["categories_seen"][cat] = stats["categories_seen"].get(cat, 0) + 1

                        # Track daily distribution
                        datestamp = None
                        if hasattr(record.header, "datestamp") and record.header.datestamp:
                            datestamp = record.header.datestamp
                            stats["daily_counts"][datestamp] = stats["daily_counts"].get(datestamp, 0) + 1

                        # Insert into spike DB
                        try:
                            conn.execute(
                                """INSERT OR IGNORE INTO papers
                                (arxiv_id, title, authors_text, abstract, categories,
                                 primary_category, submitted_date, updated_date,
                                 announced_date, oai_datestamp, license_uri,
                                 latest_version, harvest_config, harvested_at)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
                                (
                                    raw.arxiv_id,
                                    raw.title,
                                    raw.authors,
                                    raw.abstract,
                                    raw.categories,
                                    raw.primary_category,
                                    str(raw.submitted_date) if raw.submitted_date else None,
                                    str(raw.updated_date) if raw.updated_date else None,
                                    None,  # announced_date not in arXivRaw
                                    datestamp,
                                    raw.license_uri,
                                    raw.latest_version,
                                    config_name,
                                ),
                            )
                            stats["total_new"] += 1
                        except sqlite3.IntegrityError:
                            # Paper already exists (cross-listed or already harvested)
                            stats["total_duplicate"] += 1

                    except Exception as exc:
                        stats["errors"] += 1
                        if stats["errors"] <= 5:
                            print(f"  Parse error: {exc}")

                    # Rate limiting
                    if stats["total_fetched"] % 100 == 0:
                        time.sleep(rate_limit)

        except Exception as exc:
            print(f"  Harvest error for archive {archive}: {exc}")
            # OAI-PMH might return noRecordsMatch for some archives in the date range
            continue

    conn.commit()
    conn.close()

    return stats


def print_stats(stats: dict) -> None:
    """Pretty-print harvest statistics."""
    print(f"\n{'='*60}")
    print(f"Config: {stats['config']} — {stats['description']}")
    print(f"{'='*60}")
    print(f"Date range: {stats['from_date']} to {stats['until_date']}")
    print(f"Total records fetched from OAI-PMH: {stats['total_fetched']:,}")
    print(f"Matched category filter: {stats['total_matched']:,}")
    print(f"Skipped (wrong category): {stats['total_skipped']:,}")
    print(f"New papers inserted: {stats['total_new']:,}")
    print(f"Duplicates (cross-listed): {stats['total_duplicate']:,}")
    print(f"Parse errors: {stats['errors']}")

    if stats["categories_seen"]:
        print(f"\nTop categories:")
        sorted_cats = sorted(stats["categories_seen"].items(), key=lambda x: -x[1])
        for cat, count in sorted_cats[:15]:
            print(f"  {cat}: {count:,}")

    if stats["daily_counts"]:
        daily_vals = list(stats["daily_counts"].values())
        avg_daily = sum(daily_vals) / len(daily_vals)
        print(f"\nDaily volume: avg={avg_daily:.0f}, min={min(daily_vals)}, max={max(daily_vals)}")
        print(f"Projected annual: ~{avg_daily * 365:,.0f} papers")


def main():
    parser = argparse.ArgumentParser(description="Phase A1: Volume mapping")
    parser.add_argument(
        "--config",
        choices=list(CONFIGS.keys()) + ["all"],
        default="big4",
        help="Category configuration to harvest (default: big4)",
    )
    parser.add_argument("--from-date", default="2026-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--until-date", default="2026-01-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--rate-limit", type=float, default=3.0, help="Seconds between API batches")
    args = parser.parse_args()

    configs_to_run = list(CONFIGS.keys()) if args.config == "all" else [args.config]

    all_stats = []
    for config_name in configs_to_run:
        print(f"\n{'#'*60}")
        print(f"# Starting harvest: {config_name}")
        print(f"{'#'*60}")

        stats = harvest_month(
            config_name=config_name,
            from_date=args.from_date,
            until_date=args.until_date,
            rate_limit=args.rate_limit,
        )
        print_stats(stats)
        all_stats.append(stats)

    # Save stats to JSON for later analysis
    stats_path = Path(__file__).parent / "data" / "harvest_stats.json"
    with open(stats_path, "w") as f:
        json.dump(all_stats, f, indent=2)
    print(f"\nStats saved to {stats_path}")


if __name__ == "__main__":
    main()
