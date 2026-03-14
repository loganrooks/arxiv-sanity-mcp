"""CLI subgroup for enrichment operations.

Provides Click commands for single-paper enrichment, batch enrichment
(collection-scoped and search-scoped), enrichment status/stats, and
forced refresh. Follows the established CLI pattern: sync Click handlers
wrapping asyncio.run(), Rich formatted output, -q flag for JSON output.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory

console = Console()


def _make_services():
    """Create session factory and settings for enrichment commands."""
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    return sf, settings


def _format_dt(dt) -> str:
    """Format a datetime for display."""
    if dt is None:
        return "-"
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M")
    return str(dt)[:16]


def _format_enrichment_result(result, paper_submitted_date=None) -> dict:
    """Format an EnrichmentResult for display.

    Returns a dict suitable for both Rich display and JSON output.
    """
    data = {
        "openalex_id": result.openalex_id,
        "doi": result.doi,
        "cited_by_count": result.cited_by_count,
        "fwci": result.fwci,
        "status": result.status.value if hasattr(result.status, "value") else str(result.status),
    }

    # FWCI interpretation
    if result.fwci is not None:
        interp = f"{result.fwci}x field average"
        if paper_submitted_date:
            from datetime import timezone

            now = datetime.now(timezone.utc)
            if hasattr(paper_submitted_date, "tzinfo") and paper_submitted_date.tzinfo:
                age = now - paper_submitted_date
            else:
                age = now - paper_submitted_date.replace(tzinfo=timezone.utc)
            if age.days < 730:  # ~2 years
                interp += " (FWCI may be unreliable -- paper is recent)"
        data["fwci_interpretation"] = interp

    # Topics
    if result.topics:
        data["topics"] = [t.display_name for t in result.topics]

    # Related works
    if result.related_works:
        data["related_works_count"] = len(result.related_works)

    return data


def _display_enrichment_result(result, paper_submitted_date=None) -> None:
    """Display enrichment result using Rich formatting."""

    status_colors = {
        "success": "green",
        "not_found": "yellow",
        "partial": "cyan",
        "error": "red",
    }

    status_val = result.status.value if hasattr(result.status, "value") else str(result.status)
    color = status_colors.get(status_val, "white")

    console.print(f"\n[bold]Enrichment (OpenAlex, {datetime.now().strftime('%Y-%m-%d')}):[/bold]")

    if result.openalex_id:
        console.print(f"  OpenAlex ID: {result.openalex_id}")
    if result.doi:
        console.print(f"  DOI: {result.doi}")
    if result.cited_by_count is not None:
        console.print(f"  Citations: {result.cited_by_count:,}")
    if result.fwci is not None:
        interp = f"{result.fwci}x field average"
        if paper_submitted_date:
            from datetime import timezone

            now = datetime.now(timezone.utc)
            if hasattr(paper_submitted_date, "tzinfo") and paper_submitted_date.tzinfo:
                age = now - paper_submitted_date
            else:
                age = now - paper_submitted_date.replace(tzinfo=timezone.utc)
            if age.days < 730:
                interp += " (FWCI may be unreliable -- paper is recent)"
        console.print(f"  FWCI: {result.fwci} ({interp})")
    if result.topics:
        topic_names = ", ".join(t.display_name for t in result.topics)
        console.print(f"  Topics: {topic_names}")
    if result.related_works:
        console.print(f"  Related Works: {len(result.related_works)}")

    console.print(f"  Status: [{color}]{status_val}[/{color}]")

    if result.error_detail:
        console.print(f"  [red]Error: {result.error_detail}[/red]")


# ========================================================================
# ENRICH GROUP
# ========================================================================


@click.group("enrich")
def enrich_group():
    """Enrich papers with external metadata (OpenAlex)."""
    pass


# ---------------------------------------------------------------
# enrich paper
# ---------------------------------------------------------------


@enrich_group.command("paper")
@click.argument("arxiv_id")
@click.option("--refresh", is_flag=True, help="Bypass cooldown and re-enrich")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def enrich_paper(arxiv_id, refresh, quiet):
    """Enrich a single paper with OpenAlex metadata."""
    from arxiv_mcp.enrichment.service import EnrichmentService

    sf, settings = _make_services()
    svc = EnrichmentService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.enrich_paper(arxiv_id, refresh=refresh))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if quiet:
        data = _format_enrichment_result(result)
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        # Get submitted_date for FWCI interpretation
        submitted_date = asyncio.run(_get_paper_submitted_date(sf, arxiv_id))
        _display_enrichment_result(result, paper_submitted_date=submitted_date)


async def _get_paper_submitted_date(sf, arxiv_id):
    """Helper to fetch paper's submitted_date for FWCI display."""
    from arxiv_mcp.db.models import Paper

    async with sf() as session:
        paper = await session.get(Paper, arxiv_id)
        return paper.submitted_date if paper else None


# ---------------------------------------------------------------
# enrich collection
# ---------------------------------------------------------------


@enrich_group.command("collection")
@click.argument("slug")
@click.option("--refresh", is_flag=True, help="Bypass cooldown for all papers")
@click.option("--dry-run", is_flag=True, help="Preview without enriching")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def enrich_collection(slug, refresh, dry_run, quiet):
    """Enrich all unenriched papers in a collection."""
    from arxiv_mcp.enrichment.service import EnrichmentService

    sf, settings = _make_services()
    svc = EnrichmentService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.enrich_collection(slug, refresh=refresh, dry_run=dry_run))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if quiet:
        click.echo(json.dumps(result, indent=2, default=str))
        return

    if dry_run:
        console.print(f"\n[bold]Dry-run preview for collection '{slug}':[/bold]")
        console.print(f"  Total papers: {result['total']}")
        console.print(f"  To enrich: {result['to_enrich']}")
        console.print(f"  Skipped (cooldown): {result['skipped_cooldown']}")
        console.print("\n[yellow]This is a dry run. Remove --dry-run to execute.[/yellow]")
    else:
        console.print(f"\n[bold]Enrichment complete for collection '{slug}':[/bold]")
        console.print(f"  Total: {result['total']}")
        console.print(f"  [green]Enriched: {result['enriched']}[/green]")
        if result.get("not_found", 0) > 0:
            console.print(f"  [yellow]Not found: {result['not_found']}[/yellow]")
        if result.get("errors", 0) > 0:
            console.print(f"  [red]Errors: {result['errors']}[/red]")
        if result.get("skipped_cooldown", 0) > 0:
            console.print(f"  [dim]Skipped (cooldown): {result['skipped_cooldown']}[/dim]")


# ---------------------------------------------------------------
# enrich search
# ---------------------------------------------------------------


@enrich_group.command("search")
@click.argument("query")
@click.option("--limit", default=20, help="Max papers to enrich (default 20)")
@click.option("--refresh", is_flag=True, help="Bypass cooldown for all papers")
@click.option("--dry-run", is_flag=True, help="Preview without enriching")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def enrich_search(query, limit, refresh, dry_run, quiet):
    """Search papers and enrich the results."""
    from arxiv_mcp.enrichment.service import EnrichmentService

    sf, settings = _make_services()
    svc = EnrichmentService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(
            svc.enrich_search(query, limit=limit, refresh=refresh, dry_run=dry_run)
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if quiet:
        click.echo(json.dumps(result, indent=2, default=str))
        return

    if dry_run:
        console.print(f"\n[bold]Dry-run preview for search '{query}':[/bold]")
        console.print(f"  Total results: {result['total']}")
        console.print(f"  To enrich: {result['to_enrich']}")
        console.print(f"  Skipped (cooldown): {result['skipped_cooldown']}")
        console.print("\n[yellow]This is a dry run. Remove --dry-run to execute.[/yellow]")
    else:
        console.print(f"\n[bold]Enrichment complete for search '{query}':[/bold]")
        console.print(f"  Total: {result['total']}")
        console.print(f"  [green]Enriched: {result['enriched']}[/green]")
        if result.get("not_found", 0) > 0:
            console.print(f"  [yellow]Not found: {result['not_found']}[/yellow]")
        if result.get("errors", 0) > 0:
            console.print(f"  [red]Errors: {result['errors']}[/red]")
        if result.get("skipped_cooldown", 0) > 0:
            console.print(f"  [dim]Skipped (cooldown): {result['skipped_cooldown']}[/dim]")


# ---------------------------------------------------------------
# enrich status
# ---------------------------------------------------------------


@enrich_group.command("status")
@click.argument("arxiv_id", required=False, default=None)
def enrich_status(arxiv_id):
    """Show enrichment status (aggregate or per-paper).

    Without ARXIV_ID: show aggregate enrichment statistics.
    With ARXIV_ID: show enrichment details for that paper.
    """
    from arxiv_mcp.enrichment.service import EnrichmentService

    sf, settings = _make_services()
    svc = EnrichmentService(session_factory=sf, settings=settings)

    if arxiv_id:
        # Per-paper status
        enrichment = asyncio.run(svc.get_enrichment_status(arxiv_id))
        if enrichment is None:
            console.print(f"[yellow]No enrichment record for {arxiv_id}[/yellow]")
            return

        console.print(f"\n[bold]Enrichment for {arxiv_id}:[/bold]")
        console.print(f"  OpenAlex ID: {enrichment.openalex_id or '-'}")
        console.print(f"  DOI: {enrichment.doi or '-'}")
        console.print(f"  Citations: {enrichment.cited_by_count or '-'}")
        console.print(f"  FWCI: {enrichment.fwci or '-'}")
        console.print(f"  Status: {enrichment.status}")
        console.print(f"  Source API: {enrichment.source_api}")
        console.print(f"  API Version: {enrichment.api_version or '-'}")
        console.print(f"  Enriched At: {_format_dt(enrichment.enriched_at)}")
        console.print(f"  Last Attempted: {_format_dt(enrichment.last_attempted_at)}")
        if enrichment.error_detail:
            console.print(f"  [red]Error: {enrichment.error_detail}[/red]")
        if enrichment.topics:
            topic_names = [t.get("display_name", t.get("id", "?")) for t in enrichment.topics]
            console.print(f"  Topics: {', '.join(topic_names)}")
        if enrichment.related_works:
            console.print(f"  Related Works: {len(enrichment.related_works)}")
    else:
        # Aggregate stats
        stats = asyncio.run(svc.get_enrichment_stats())

        console.print("\n[bold]Enrichment Statistics:[/bold]")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Metric", width=20)
        table.add_column("Value", width=15, justify="right")

        table.add_row("Total enrichments", str(stats["total"]))
        table.add_row("[green]Success[/green]", str(stats["success"]))
        table.add_row("[yellow]Not found[/yellow]", str(stats["not_found"]))
        table.add_row("[cyan]Partial[/cyan]", str(stats["partial"]))
        table.add_row("[red]Error[/red]", str(stats["error"]))
        table.add_row("Last enrichment", _format_dt(stats.get("last_enrichment")))

        console.print(table)


# ---------------------------------------------------------------
# enrich refresh
# ---------------------------------------------------------------


@enrich_group.command("refresh")
@click.argument("arxiv_id")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def enrich_refresh(arxiv_id, quiet):
    """Force re-enrichment of a paper (bypasses cooldown)."""
    from arxiv_mcp.enrichment.service import EnrichmentService

    sf, settings = _make_services()
    svc = EnrichmentService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.enrich_paper(arxiv_id, refresh=True))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if quiet:
        data = _format_enrichment_result(result)
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        submitted_date = asyncio.run(_get_paper_submitted_date(sf, arxiv_id))
        _display_enrichment_result(result, paper_submitted_date=submitted_date)
