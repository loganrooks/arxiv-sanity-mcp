"""Import arxiv-scan pipeline data into the MCP substrate.

One-time import script that bootstraps the database with:
- 150 papers from final-selection.json (via arXiv API fetch + upsert)
- 7 false-negative papers from excluded-paper-audit.json
- Triage states from paper-index-data.json value scores
- Interest profile from 10 tension vocabulary categories

Composes existing services (ArxivAPIClient, TriageService, ProfileService).
Idempotent: re-runs skip existing papers (ON CONFLICT DO NOTHING).
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

import click
import structlog
from rich.progress import Progress, SpinnerColumn, TextColumn
from sqlalchemy.dialects.postgresql import insert as pg_insert

from arxiv_mcp.config import Settings, get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.db.models import Paper
from arxiv_mcp.ingestion.arxiv_api import ArxivAPIClient
from arxiv_mcp.ingestion.mapper import map_to_paper
from arxiv_mcp.interest.profiles import ProfileService
from arxiv_mcp.workflow.triage import TriageService

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Tension vocabulary (from evaluation-guidelines.md)
# ---------------------------------------------------------------------------

TENSION_CATEGORIES = [
    {
        "signal_value": "autonomy_vs_control",
        "reason": "How much should agents decide vs. defer? (Stiegler, Bostrom, Dewey, Floridi)",
    },
    {
        "signal_value": "memory_vs_forgetting",
        "reason": "What should persist vs. be pruned? (Stiegler, Clark & Chalmers, Derrida, Dewey)",
    },
    {
        "signal_value": "grounding_vs_fluency",
        "reason": "Verification constrains but prevents confabulation. (Brandom, Goldman, Sellars, Peirce)",
    },
    {
        "signal_value": "efficiency_vs_epistemic_rigor",
        "reason": "Fast approximate vs. careful warranted. (Peirce, Popper, Lakatos, Sosa)",
    },
    {
        "signal_value": "individual_vs_collective_intelligence",
        "reason": "Single agent vs. multi-agent emergence. (Peirce, Goldman, Simondon, List & Pettit)",
    },
    {
        "signal_value": "transparency_vs_capability",
        "reason": "Interpretable but limited vs. powerful but opaque. (Dennett, Heidegger, Floridi)",
    },
    {
        "signal_value": "tool_vs_agent",
        "reason": "Instrument under control vs. autonomous actor. (Simondon, Heidegger, Searle, Dewey)",
    },
    {
        "signal_value": "planning_vs_situated_action",
        "reason": "Deliberate reasoning vs. responsive coping. (Bratman, Suchman, Dreyfus, Dewey)",
    },
    {
        "signal_value": "standardization_vs_context_sensitivity",
        "reason": "Universal protocols vs. local adaptation. (Wittgenstein, Gadamer, Star & Griesemer)",
    },
    {
        "signal_value": "competence_vs_comprehension",
        "reason": "Doing right without understanding why. (Dennett, Dreyfus, Searle, James/Dewey)",
    },
]


# ---------------------------------------------------------------------------
# Pure data-loading functions (testable, no side effects)
# ---------------------------------------------------------------------------


def load_final_selection(data_dir: Path) -> list[dict]:
    """Load final-selection.json and return the papers list.

    Args:
        data_dir: Pipeline data directory (contains triage/ subdirectory).

    Returns:
        List of paper dicts from the "papers" key.
    """
    path = data_dir / "triage" / "final-selection.json"
    with open(path) as f:
        data = json.load(f)
    return data["papers"]


def load_excluded_papers(data_dir: Path) -> list[dict]:
    """Load excluded-paper-audit.json and return the paper list.

    Args:
        data_dir: Pipeline data directory.

    Returns:
        List of excluded paper dicts.
    """
    path = data_dir / "excluded-paper-audit.json"
    with open(path) as f:
        return json.load(f)


def load_paper_index(data_dir: Path) -> dict[str, dict]:
    """Load paper-index-data.json and return dict keyed by arXiv ID.

    Args:
        data_dir: Pipeline data directory (contains reading/ subdirectory).

    Returns:
        Dict mapping arxiv_id -> paper index entry.
    """
    path = data_dir / "reading" / "paper-index-data.json"
    with open(path) as f:
        papers = json.load(f)
    return {p["id"]: p for p in papers}


def map_value_to_triage_state(value: int) -> str:
    """Map paper-index value score to triage state.

    Args:
        value: Value score from paper-index-data.json (1-10).

    Returns:
        "shortlisted" if value >= 7, "seen" otherwise.
    """
    return "shortlisted" if value >= 7 else "seen"


def build_tension_signals() -> list[dict]:
    """Build interest signals from the 10 tension vocabulary categories.

    Uses signal_type="followed_author" with the tension name as signal_value,
    since tensions map to topical interest areas that function like
    followed topics in the interest model.

    Returns:
        List of 10 signal dicts with keys: signal_type, signal_value, reason.
    """
    return [
        {
            "signal_type": "followed_author",
            "signal_value": t["signal_value"],
            "reason": t["reason"],
        }
        for t in TENSION_CATEGORIES
    ]


# ---------------------------------------------------------------------------
# Async import orchestration (composes existing services)
# ---------------------------------------------------------------------------


async def import_arxiv_scan(data_dir: Path, settings: Settings) -> dict:
    """Import arxiv-scan pipeline data into the MCP substrate.

    Orchestrates:
    1. Load all data files
    2. Collect unique arXiv IDs (150 final-selection + 7 excluded-audit)
    3. Fetch each paper via arXiv API (sequential, rate-limited)
    4. Upsert into DB (ON CONFLICT DO NOTHING for idempotency)
    5. Set triage states from paper-index value scores
    6. Create interest profile with tension signals

    Args:
        data_dir: Path to pipeline data directory.
        settings: Application settings.

    Returns:
        Summary dict with counts: papers_fetched, papers_skipped, papers_errors,
        triage_set, profile_created.
    """
    # Step 1: Load all data files
    final_papers = load_final_selection(data_dir)
    excluded_papers = load_excluded_papers(data_dir)
    paper_index = load_paper_index(data_dir)

    # Step 2: Collect unique arXiv IDs
    all_ids = []
    seen_ids: set[str] = set()
    for p in final_papers:
        if p["arxiv_id"] not in seen_ids:
            all_ids.append(p["arxiv_id"])
            seen_ids.add(p["arxiv_id"])
    for p in excluded_papers:
        if p["arxiv_id"] not in seen_ids:
            all_ids.append(p["arxiv_id"])
            seen_ids.add(p["arxiv_id"])

    logger.info("import.start", total_ids=len(all_ids),
                final_selection=len(final_papers), excluded=len(excluded_papers))

    # Create services
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    client = ArxivAPIClient(settings)
    triage_svc = TriageService(sf, settings)
    profile_svc = ProfileService(sf, settings)

    stats = {
        "papers_fetched": 0,
        "papers_skipped": 0,
        "papers_errors": 0,
        "triage_set": 0,
        "profile_created": False,
    }

    # Step 3: Fetch and upsert papers
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("Fetching papers", total=len(all_ids))

        for arxiv_id in all_ids:
            try:
                raw = await client.fetch_paper(arxiv_id)
                if raw is None:
                    logger.warning("import.paper_not_found", arxiv_id=arxiv_id)
                    stats["papers_errors"] += 1
                    progress.advance(task)
                    continue

                paper = map_to_paper(raw, source="arxiv_api")

                # Upsert: ON CONFLICT DO NOTHING for idempotency
                async with sf() as session:
                    stmt = pg_insert(Paper).values(
                        arxiv_id=paper.arxiv_id,
                        title=paper.title,
                        authors_text=paper.authors_text,
                        abstract=paper.abstract,
                        submitter=paper.submitter,
                        comments=paper.comments,
                        journal_ref=paper.journal_ref,
                        report_no=paper.report_no,
                        categories=paper.categories,
                        primary_category=paper.primary_category,
                        category_list=paper.category_list,
                        doi=paper.doi,
                        submitted_date=paper.submitted_date,
                        updated_date=paper.updated_date,
                        oai_datestamp=paper.oai_datestamp,
                        license_uri=paper.license_uri,
                        latest_version=paper.latest_version,
                        version_history=paper.version_history,
                        processing_tier=paper.processing_tier,
                        source=paper.source,
                        fetched_at=paper.fetched_at,
                    ).on_conflict_do_nothing(index_elements=["arxiv_id"])
                    result = await session.execute(stmt)
                    await session.commit()

                    if result.rowcount > 0:
                        stats["papers_fetched"] += 1
                    else:
                        stats["papers_skipped"] += 1

            except Exception as exc:
                logger.error("import.paper_error", arxiv_id=arxiv_id, error=str(exc))
                stats["papers_errors"] += 1

            progress.advance(task)

    # Step 4: Set triage states
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("[progress.percentage]{task.completed}/{task.total}"),
    ) as progress:
        task = progress.add_task("Setting triage states", total=len(all_ids))

        for arxiv_id in all_ids:
            try:
                # Use paper-index value scores; excluded papers default to "seen"
                if arxiv_id in paper_index:
                    value = paper_index[arxiv_id]["value"]
                    state = map_value_to_triage_state(value)
                else:
                    state = "seen"

                await triage_svc.mark_triage(
                    paper_id=arxiv_id,
                    new_state=state,
                    source="import",
                    reason=f"arxiv-scan pipeline import (value={paper_index.get(arxiv_id, {}).get('value', 'N/A')})",
                )
                stats["triage_set"] += 1
            except Exception as exc:
                logger.error("import.triage_error", arxiv_id=arxiv_id, error=str(exc))

            progress.advance(task)

    # Step 5: Create interest profile with tension signals
    try:
        profile = await profile_svc.create_profile(
            name="arxiv-scan-tensions",
            source="import",
        )
        logger.info("import.profile_created", slug=profile.slug)

        tension_signals = build_tension_signals()
        for sig in tension_signals:
            try:
                await profile_svc.add_signal(
                    slug=profile.slug,
                    signal_type=sig["signal_type"],
                    signal_value=sig["signal_value"],
                    source="import",
                    reason=sig["reason"],
                )
            except ValueError as exc:
                # Signal may already exist (idempotent re-run)
                logger.info("import.signal_exists", signal=sig["signal_value"], error=str(exc))

        stats["profile_created"] = True
    except ValueError:
        # Profile already exists (idempotent re-run)
        logger.info("import.profile_exists", name="arxiv-scan-tensions")
        stats["profile_created"] = False

    # Step 6: Print summary
    await engine.dispose()

    logger.info(
        "import.complete",
        papers_fetched=stats["papers_fetched"],
        papers_skipped=stats["papers_skipped"],
        papers_errors=stats["papers_errors"],
        triage_set=stats["triage_set"],
        profile_created=stats["profile_created"],
    )

    return stats


# ---------------------------------------------------------------------------
# Click CLI command
# ---------------------------------------------------------------------------


@click.group("import")
def import_scan_group() -> None:
    """Import data from external pipeline sources."""


@import_scan_group.command("scan")
@click.option(
    "--data-dir",
    type=click.Path(exists=True, path_type=Path),
    default=Path("/scratch/arxiv-scan/pipeline"),
    help="Path to arxiv-scan pipeline data directory.",
)
def scan_command(data_dir: Path) -> None:
    """Import arxiv-scan pipeline data (papers, triage states, interest profile)."""
    settings = get_settings()
    click.echo(f"Importing from: {data_dir}")
    stats = asyncio.run(import_arxiv_scan(data_dir, settings))
    click.echo(f"\nImport complete:")
    click.echo(f"  Papers fetched:  {stats['papers_fetched']}")
    click.echo(f"  Papers skipped:  {stats['papers_skipped']}")
    click.echo(f"  Papers errors:   {stats['papers_errors']}")
    click.echo(f"  Triage states:   {stats['triage_set']}")
    click.echo(f"  Profile created: {stats['profile_created']}")
