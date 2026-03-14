"""CLI subcommands for harvesting arXiv paper metadata.

Provides click subgroup 'harvest' with commands for bulk, incremental,
and single-paper fetch operations.
"""

from __future__ import annotations

import asyncio

import click
import structlog
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.ingestion.arxiv_api import ArxivAPIClient
from arxiv_mcp.ingestion.mapper import map_to_paper
from arxiv_mcp.ingestion.oai_pmh import OAIPMHHarvester

logger = structlog.get_logger(__name__)
console = Console()


@click.group("harvest")
def harvest_group():
    """Harvest arXiv paper metadata."""
    pass


@harvest_group.command("bulk")
@click.option("--set", "archive_set", default=None, help="OAI-PMH set (e.g., 'cs')")
@click.option(
    "--from-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="Start date for harvest (YYYY-MM-DD)",
)
@click.option("--batch-size", default=100, help="Batch size for DB inserts")
@click.option("--prefix", default="arXivRaw", help="OAI-PMH metadata prefix")
def bulk_harvest(archive_set, from_date, batch_size, prefix):
    """Bulk harvest via OAI-PMH.

    Fetches all records from arXiv's OAI-PMH endpoint, filters to
    configured categories, and upserts into the database.
    Resumption tokens are handled automatically.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)

    harvester = OAIPMHHarvester(settings=settings, session_factory=sf)

    from_d = from_date.date() if from_date else None

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Harvesting papers...", total=None)

        def on_progress(count):
            progress.update(task, description=f"Harvested {count} records...")

        result = asyncio.run(
            harvester.harvest_bulk(
                archive_set=archive_set,
                from_date=from_d,
                metadata_prefix=prefix,
                batch_size=batch_size,
                progress_callback=on_progress,
            )
        )

    console.print("\n[bold green]Harvest complete![/]")
    console.print(f"  Fetched: {result.total_fetched}")
    console.print(f"  Inserted: {result.total_inserted}")
    console.print(f"  Updated: {result.total_updated}")
    console.print(f"  Skipped: {result.total_skipped}")
    console.print(f"  Duration: {result.duration_seconds:.1f}s")

    asyncio.run(engine.dispose())


@harvest_group.command("incremental")
def incremental_harvest():
    """Incremental harvest since last checkpoint.

    Reads the last checkpoint date from data/harvest_checkpoint.json,
    harvests records updated since then, and saves a new checkpoint.
    """
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)

    harvester = OAIPMHHarvester(settings=settings, session_factory=sf)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        _task = progress.add_task("Incremental harvest...", total=None)
        result = asyncio.run(harvester.harvest_incremental())

    console.print("\n[bold green]Incremental harvest complete![/]")
    console.print(f"  Fetched: {result.total_fetched}")
    console.print(f"  Skipped: {result.total_skipped}")
    console.print(f"  Duration: {result.duration_seconds:.1f}s")
    if result.checkpoint_date:
        console.print(f"  Checkpoint: {result.checkpoint_date}")

    asyncio.run(engine.dispose())


@harvest_group.command("fetch")
@click.argument("arxiv_id")
def fetch_paper(arxiv_id):
    """Fetch a single paper by arXiv ID via API.

    Uses the arXiv search API to fetch metadata for a specific paper
    and insert/update it in the database.
    """
    settings = get_settings()

    async def _fetch():
        client = ArxivAPIClient(settings=settings)
        raw = await client.fetch_paper(arxiv_id)
        if raw is None:
            console.print(f"[red]Paper not found:[/] {arxiv_id}")
            return

        paper = map_to_paper(raw, source="arxiv_api")
        console.print("\n[bold green]Paper fetched:[/]")
        console.print(f"  ID: {paper.arxiv_id}")
        console.print(f"  Title: {paper.title}")
        console.print(f"  Authors: {paper.authors_text}")
        console.print(f"  Categories: {paper.categories}")
        console.print(f"  Primary: {paper.primary_category}")
        if paper.doi:
            console.print(f"  DOI: {paper.doi}")
        if paper.submitted_date:
            console.print(f"  Submitted: {paper.submitted_date}")

    asyncio.run(_fetch())
