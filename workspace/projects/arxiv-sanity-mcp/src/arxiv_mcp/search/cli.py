"""CLI subcommands for search, browse, and find-related.

Provides Click commands that call the async SearchService methods
and display results using rich tables or JSON output.
"""

from __future__ import annotations

import asyncio
import json
from datetime import date

import click
from rich.console import Console
from rich.table import Table

from arxiv_mcp.config import Settings, get_settings
from arxiv_mcp.db.engine import create_engine, session_factory
from arxiv_mcp.search.service import SearchService


console = Console()


def _get_search_service(settings: Settings | None = None) -> SearchService:
    """Create a SearchService with engine and session factory."""
    if settings is None:
        settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    return SearchService(session_factory=sf, settings=settings)


def _truncate(text: str | None, max_len: int = 60) -> str:
    """Truncate text for table display."""
    if text is None:
        return ""
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def _format_date(d) -> str:
    """Format a date or datetime for display."""
    if d is None:
        return ""
    if isinstance(d, date):
        return d.isoformat()
    return str(d)[:10]


def _display_results_table(items, show_score: bool = True) -> None:
    """Display search results in a rich table."""
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("arxiv_id", width=14)
    table.add_column("Title", ratio=3)
    table.add_column("Authors", ratio=2)
    table.add_column("Category", width=8)
    table.add_column("Date", width=12)
    if show_score:
        table.add_column("Score", width=8, justify="right")

    for item in items:
        p = item.paper
        row = [
            p.arxiv_id,
            _truncate(p.title, 60),
            _truncate(p.authors_text, 40),
            p.primary_category or "",
            _format_date(p.announced_date or p.submitted_date),
        ]
        if show_score:
            row.append(f"{item.score:.4f}" if item.score is not None else "")
        table.add_row(*row)

    console.print(table)


def _display_pagination_info(page_info) -> None:
    """Display pagination info at the bottom."""
    if page_info.has_next:
        console.print(
            f"\n[dim]More results available. Next cursor: {page_info.next_cursor}[/dim]"
        )
    else:
        console.print("\n[dim]No more results.[/dim]")


@click.group("search")
def search_group():
    """Search and discover arXiv papers."""
    pass


@search_group.command("query")
@click.option("-q", "--query", "query_text", help="Full-text search query (AND/OR supported)")
@click.option("-t", "--title", help="Search by title")
@click.option("-a", "--author", help="Search by author name")
@click.option("-c", "--category", help="Filter by arXiv category (e.g., cs.AI)")
@click.option(
    "--from", "date_from", type=click.DateTime(formats=["%Y-%m-%d"]), help="Start date (YYYY-MM-DD)"
)
@click.option(
    "--to", "date_to", type=click.DateTime(formats=["%Y-%m-%d"]), help="End date (YYYY-MM-DD)"
)
@click.option(
    "--time-basis",
    type=click.Choice(["submitted", "updated", "announced"]),
    default="announced",
    help="Which date to use for filtering/ordering",
)
@click.option("--cursor", help="Pagination cursor for next page")
@click.option("--limit", "page_size", default=20, help="Results per page")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def search_query(
    query_text, title, author, category, date_from, date_to, time_basis, cursor, page_size,
    output_json
):
    """Search papers by text, author, category, date."""
    if not any([query_text, title, author, category, date_from, date_to]):
        click.echo("Error: at least one search criterion is required.", err=True)
        raise SystemExit(1)

    service = _get_search_service()

    result = asyncio.run(
        service.search_papers(
            query_text=query_text,
            title=title,
            author=author,
            category=category,
            date_from=date_from.date() if date_from else None,
            date_to=date_to.date() if date_to else None,
            time_basis=time_basis,
            cursor_token=cursor,
            page_size=page_size,
        )
    )

    if output_json:
        click.echo(result.model_dump_json(indent=2))
    else:
        if not result.items:
            console.print("[yellow]No results found.[/yellow]")
            return

        has_score = any(item.score is not None for item in result.items)
        console.print(f"\n[bold]Found {len(result.items)} results[/bold]\n")
        _display_results_table(result.items, show_score=has_score)
        _display_pagination_info(result.page_info)


@search_group.command("browse")
@click.option("-c", "--category", help="Filter by arXiv category")
@click.option(
    "--time-basis",
    type=click.Choice(["submitted", "updated", "announced"]),
    default="announced",
    help="Which date to use for recency",
)
@click.option("--days", default=7, help="Number of days to look back")
@click.option("--cursor", help="Pagination cursor")
@click.option("--limit", "page_size", default=50, help="Results per page")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def browse_recent(category, time_basis, days, cursor, page_size, output_json):
    """Browse recently announced papers."""
    service = _get_search_service()

    result = asyncio.run(
        service.browse_recent(
            category=category,
            time_basis=time_basis,
            days=days,
            cursor_token=cursor,
            page_size=page_size,
        )
    )

    if output_json:
        click.echo(result.model_dump_json(indent=2))
    else:
        if not result.items:
            console.print("[yellow]No recent papers found.[/yellow]")
            return

        title = f"Recent papers"
        if category:
            title += f" in {category}"
        title += f" (last {days} days)"

        console.print(f"\n[bold]{title}[/bold] - {len(result.items)} results\n")
        _display_results_table(result.items, show_score=False)
        _display_pagination_info(result.page_info)


@search_group.command("related")
@click.argument("arxiv_id")
@click.option("--limit", "page_size", default=20, help="Number of related papers to return")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def find_related(arxiv_id, page_size, output_json):
    """Find papers related to a seed paper.

    ARXIV_ID is the arXiv identifier of the seed paper (e.g., 2301.00001).
    """
    service = _get_search_service()

    try:
        results = asyncio.run(
            service.find_related_papers(
                seed_arxiv_id=arxiv_id,
                page_size=page_size,
            )
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        data = [r.model_dump() for r in results]
        click.echo(json.dumps(data, indent=2, default=str))
    else:
        if not results:
            console.print(f"[yellow]No related papers found for {arxiv_id}.[/yellow]")
            return

        console.print(f"\n[bold]Papers related to {arxiv_id}[/bold] - {len(results)} results\n")
        _display_results_table(results, show_score=True)
