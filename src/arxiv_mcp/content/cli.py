"""CLI subgroup for content operations.

Provides Click commands for retrieving content variants and checking
content status for papers. Follows the established CLI pattern: sync
Click handlers wrapping asyncio.run(), Rich formatted output.
"""

from __future__ import annotations

import asyncio
import json

import click
from rich.console import Console
from rich.table import Table

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory

console = Console()


def _make_services():
    """Create session factory and settings for content commands."""
    settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    return sf, settings


# ========================================================================
# CONTENT GROUP
# ========================================================================


@click.group("content")
def content_group():
    """Content variant operations (get, status)."""
    pass


# ---------------------------------------------------------------
# content get
# ---------------------------------------------------------------


@content_group.command("get")
@click.argument("arxiv_id")
@click.option(
    "--variant",
    default="best",
    type=click.Choice(["best", "abstract", "html", "pdf_markdown"]),
    help="Content variant to retrieve (default: best)",
)
@click.option("--full", is_flag=True, help="Show full content instead of preview")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def content_get(arxiv_id, variant, full, quiet):
    """Get content for a paper at the requested fidelity level."""
    from arxiv_mcp.content.service import ContentService

    sf, settings = _make_services()
    svc = ContentService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.get_or_create_variant(arxiv_id, variant))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if "error" in result:
        if quiet:
            click.echo(json.dumps(result, indent=2, default=str))
        else:
            console.print(f"[red]Error: {result['error']}[/red]")
        raise SystemExit(1)

    if quiet:
        click.echo(json.dumps(result, indent=2, default=str))
        return

    # Rich formatted output
    console.print(f"\n[bold]Content for {arxiv_id}:[/bold]")
    console.print(f"  Variant: [cyan]{result.get('variant_type', 'unknown')}[/cyan]")

    if result.get("backend"):
        console.print(f"  Backend: {result['backend']}")
    if result.get("backend_version"):
        console.print(f"  Version: {result['backend_version']}")
    if result.get("extraction_method"):
        console.print(f"  Method: {result['extraction_method']}")
    if result.get("source_url"):
        console.print(f"  Source: {result['source_url']}")
    if result.get("license_uri"):
        console.print(f"  License: {result['license_uri']}")
    if result.get("content_hash"):
        console.print(f"  Hash: {result['content_hash'][:16]}...")
    if result.get("converted_at"):
        console.print(f"  Converted: {result['converted_at']}")

    warnings = result.get("quality_warnings", [])
    if warnings:
        console.print(f"  [yellow]Warnings: {', '.join(warnings)}[/yellow]")

    content = result.get("content", "")
    console.print()
    if full:
        console.print(content)
    else:
        preview = content[:500]
        if len(content) > 500:
            preview += f"\n\n[dim]... ({len(content)} chars total, use --full for complete content)[/dim]"
        console.print(preview)


# ---------------------------------------------------------------
# content status
# ---------------------------------------------------------------


@content_group.command("status")
@click.argument("arxiv_id")
@click.option("-q", "--quiet", is_flag=True, help="Output machine-readable JSON only")
def content_status(arxiv_id, quiet):
    """List all cached content variants for a paper."""
    from arxiv_mcp.content.service import ContentService

    sf, settings = _make_services()
    svc = ContentService(session_factory=sf, settings=settings)

    try:
        variants = asyncio.run(svc.list_variants(arxiv_id))
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if quiet:
        click.echo(json.dumps(variants, indent=2, default=str))
        return

    if not variants:
        console.print(f"[yellow]No content variants cached for {arxiv_id}[/yellow]")
        return

    console.print(f"\n[bold]Content variants for {arxiv_id}:[/bold]\n")

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Variant Type", width=16)
    table.add_column("Backend", width=14)
    table.add_column("Converted At", width=20)

    for v in variants:
        table.add_row(
            v.get("variant_type", "-"),
            v.get("backend", "-"),
            v.get("converted_at", "-"),
        )

    console.print(table)
