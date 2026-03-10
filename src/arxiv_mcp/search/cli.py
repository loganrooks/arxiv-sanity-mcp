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


def _get_search_service(settings: Settings | None = None):
    """Create a search service with engine and session factory.

    Returns WorkflowSearchService (triage + collection enrichment) if
    the workflow module is available, otherwise falls back to bare
    SearchService for Phase 1 compatibility.
    """
    if settings is None:
        settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    search_svc = SearchService(session_factory=sf, settings=settings)

    try:
        from arxiv_mcp.workflow.search_augment import WorkflowSearchService

        return WorkflowSearchService(
            session_factory=sf, settings=settings, search_service=search_svc
        )
    except (ImportError, ModuleNotFoundError):
        return search_svc


def _get_profile_ranking_service(settings: Settings | None = None):
    """Build the full service chain: SearchService -> WorkflowSearchService -> ProfileRankingService.

    Returns (ProfileRankingService, session_factory) tuple. The session_factory
    is returned so callers can also construct ProfileService if needed.
    """
    if settings is None:
        settings = get_settings()
    engine = create_engine(settings.database_url)
    sf = session_factory(engine)
    search_svc = SearchService(session_factory=sf, settings=settings)

    from arxiv_mcp.interest.search_augment import ProfileRankingService
    from arxiv_mcp.workflow.search_augment import WorkflowSearchService

    workflow_svc = WorkflowSearchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )
    profile_svc = ProfileRankingService(
        session_factory=sf, settings=settings,
        workflow_search_service=workflow_svc,
    )
    return profile_svc, sf


def _display_ranking_explanation(item, console_obj) -> None:
    """Display ranking explanation for a ProfileSearchResult."""
    if item.ranking_explanation is None:
        return

    expl = item.ranking_explanation
    console_obj.print(f"  [dim]Composite score: {expl.composite_score:.4f} (ranker {expl.ranker_version})[/dim]")
    for signal in expl.signal_breakdown:
        # Score bar: visual representation
        bar_len = int(signal.normalized_score * 20)
        bar = "=" * bar_len + "-" * (20 - bar_len)
        console_obj.print(
            f"    [{bar}] {signal.signal_type}: "
            f"norm={signal.normalized_score:.3f} "
            f"wt={signal.weight:.2f} "
            f"wtd={signal.weighted_score:.4f} "
            f"-- {signal.explanation}"
        )


def _display_ranker_snapshot(snapshot, console_obj) -> None:
    """Display a RankerSnapshot at the top of profile-ranked results."""
    console_obj.print("\n[bold]Ranker Snapshot[/bold]")
    console_obj.print(f"  Profile: {snapshot.profile_slug or '(none)'}")
    console_obj.print(f"  Version: {snapshot.ranker_version}")
    console_obj.print(f"  Negative weight: {snapshot.negative_weight:.2f}")
    console_obj.print(f"  Seed papers: {snapshot.seed_paper_count}")
    console_obj.print(f"  Followed authors: {snapshot.followed_author_count}")
    console_obj.print(f"  Negative examples: {snapshot.negative_example_count}")
    console_obj.print(f"  Saved queries: {snapshot.saved_query_count}")
    console_obj.print(f"  Weights: {', '.join(f'{k}={v:.2f}' for k, v in snapshot.weights.items())}")
    console_obj.print(f"  Signal types: {', '.join(snapshot.signal_types_applied)}")
    console_obj.print()


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


_TRIAGE_COLORS = {
    "shortlisted": "green",
    "read": "blue",
    "cite-later": "cyan",
    "dismissed": "red",
    "archived": "dim",
    "unseen": "dim",
}


def _display_results_table(items, show_score: bool = True) -> None:
    """Display search results in a rich table.

    Detects WorkflowSearchResult items (have triage_state attr) and
    adds Triage and Collections columns with color coding.
    """
    has_workflow = len(items) > 0 and hasattr(items[0], "triage_state")

    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("arxiv_id", width=14)
    table.add_column("Title", ratio=3)
    table.add_column("Authors", ratio=2)
    table.add_column("Category", width=8)
    table.add_column("Date", width=12)
    if has_workflow:
        table.add_column("Triage", width=12)
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
        if has_workflow:
            state = item.triage_state
            color = _TRIAGE_COLORS.get(state, "white")
            row.append(f"[{color}]{state}[/{color}]")
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
@click.option("--profile", "profile_slug", default=None, help="Profile slug for ranked results")
@click.option("--explain", "explain", is_flag=True, help="Show ranker snapshot (requires --profile)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def search_query(
    query_text, title, author, category, date_from, date_to, time_basis, cursor, page_size,
    profile_slug, explain, output_json
):
    """Search papers by text, author, category, date."""
    if not any([query_text, title, author, category, date_from, date_to]):
        click.echo("Error: at least one search criterion is required.", err=True)
        raise SystemExit(1)

    search_kwargs = dict(
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

    if profile_slug:
        # Profile-ranked search
        profile_svc, _ = _get_profile_ranking_service()
        response = asyncio.run(
            profile_svc.search_papers(profile_slug=profile_slug, **search_kwargs)
        )

        if output_json:
            click.echo(response.model_dump_json(indent=2))
            return

        result = response.results
        if not result.items:
            console.print("[yellow]No results found.[/yellow]")
            return

        # Show ranker snapshot if --explain
        if explain and response.ranker_snapshot:
            _display_ranker_snapshot(response.ranker_snapshot, console)

        console.print(f"\n[bold]Found {len(result.items)} results[/bold] (profile: {profile_slug})\n")
        for item in result.items:
            p = item.paper
            triage_state = item.triage_state
            triage_color = _TRIAGE_COLORS.get(triage_state, "white")
            score_str = f"{item.score:.4f}" if item.score is not None else ""
            console.print(
                f"[bold]{p.arxiv_id}[/bold] {_truncate(p.title, 60)} "
                f"[dim]{_truncate(p.authors_text, 30)}[/dim] "
                f"[{triage_color}]{triage_state}[/{triage_color}] "
                f"[cyan]{score_str}[/cyan]"
            )
            _display_ranking_explanation(item, console)

        _display_pagination_info(result.page_info)
    else:
        # Standard search (no profile)
        service = _get_search_service()
        result = asyncio.run(service.search_papers(**search_kwargs))

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
@click.option("--profile", "profile_slug", default=None, help="Profile slug for ranked results")
@click.option("--explain", "explain", is_flag=True, help="Show ranker snapshot (requires --profile)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def browse_recent(category, time_basis, days, cursor, page_size, profile_slug, explain, output_json):
    """Browse recently announced papers."""
    browse_kwargs = dict(
        category=category,
        time_basis=time_basis,
        days=days,
        cursor_token=cursor,
        page_size=page_size,
    )

    if profile_slug:
        # Profile-ranked browse
        profile_svc, _ = _get_profile_ranking_service()
        response = asyncio.run(
            profile_svc.browse_recent(profile_slug=profile_slug, **browse_kwargs)
        )

        if output_json:
            click.echo(response.model_dump_json(indent=2))
            return

        result = response.results
        if not result.items:
            console.print("[yellow]No recent papers found.[/yellow]")
            return

        # Show ranker snapshot if --explain
        if explain and response.ranker_snapshot:
            _display_ranker_snapshot(response.ranker_snapshot, console)

        title = f"Recent papers"
        if category:
            title += f" in {category}"
        title += f" (last {days} days, profile: {profile_slug})"

        console.print(f"\n[bold]{title}[/bold] - {len(result.items)} results\n")
        for item in result.items:
            p = item.paper
            triage_state = item.triage_state
            triage_color = _TRIAGE_COLORS.get(triage_state, "white")
            score_str = f"{item.score:.4f}" if item.score is not None else ""
            console.print(
                f"[bold]{p.arxiv_id}[/bold] {_truncate(p.title, 60)} "
                f"[dim]{_truncate(p.authors_text, 30)}[/dim] "
                f"[{triage_color}]{triage_state}[/{triage_color}] "
                f"[cyan]{score_str}[/cyan]"
            )
            _display_ranking_explanation(item, console)

        _display_pagination_info(result.page_info)
    else:
        # Standard browse (no profile)
        service = _get_search_service()
        result = asyncio.run(service.browse_recent(**browse_kwargs))

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
