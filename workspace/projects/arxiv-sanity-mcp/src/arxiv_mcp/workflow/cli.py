"""CLI subgroups for all workflow operations.

Provides Click commands for collections, triage, queries, watches,
paper show, and workflow management (export/import/stats/reset).
Each command creates service instances, runs async calls via asyncio.run(),
and formats output with Rich tables or JSON.
"""

from __future__ import annotations

import asyncio
import json
from datetime import date, datetime

import click
from rich.console import Console
from rich.table import Table

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.engine import create_engine, session_factory

console = Console()


def _make_session_factory():
    """Create session factory from settings."""
    settings = get_settings()
    engine = create_engine(settings.database_url)
    return session_factory(engine), settings


def _format_dt(dt) -> str:
    """Format a datetime/date for display."""
    if dt is None:
        return "-"
    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M")
    if isinstance(dt, date):
        return dt.isoformat()
    return str(dt)[:16]


# ========================================================================
# COLLECTION GROUP
# ========================================================================


@click.group("collection")
def collection_group():
    """Manage paper collections."""
    pass


@collection_group.command("create")
@click.argument("name")
def collection_create(name):
    """Create a new collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.create_collection(name))
        console.print(f"[green]Created collection '{result.slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("list")
@click.option("--include-archived", is_flag=True, help="Include archived collections")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def collection_list(include_archived, output_json):
    """List all collections."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    collections = asyncio.run(svc.list_collections(include_archived=include_archived))

    if output_json:
        data = [c.model_dump(mode="json") for c in collections]
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if not collections:
        console.print("[yellow]No collections found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Slug", width=24)
    table.add_column("Name", ratio=2)
    table.add_column("Papers", width=8, justify="right")
    table.add_column("Archived", width=10)
    table.add_column("Created", width=18)

    for c in collections:
        archived = "[dim]yes[/dim]" if c.is_archived else ""
        table.add_row(c.slug, c.name, str(c.paper_count), archived, _format_dt(c.created_at))

    console.print(table)


@collection_group.command("show")
@click.argument("slug")
@click.option("--sort-by", type=click.Choice(["added", "paper_date", "title"]), default="added")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def collection_show(slug, sort_by, output_json):
    """Show papers in a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.show_collection(slug, sort_by=sort_by))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(result.model_dump_json(indent=2))
        return

    if not result.items:
        console.print(f"[yellow]Collection '{slug}' is empty.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("arxiv_id", width=14)
    table.add_column("Title", ratio=3)
    table.add_column("Triage", width=12)
    table.add_column("Source", width=10)
    table.add_column("Added", width=18)

    for item in result.items:
        table.add_row(
            item.arxiv_id,
            (item.title or "")[:60],
            item.triage_state,
            item.source,
            _format_dt(item.added_at),
        )

    console.print(table)


@collection_group.command("delete")
@click.argument("slug")
@click.option("--purge", is_flag=True, help="Also delete orphaned papers")
@click.option("--confirm", "confirmed", is_flag=True, help="Skip confirmation prompt")
def collection_delete(slug, purge, confirmed):
    """Delete a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    if not confirmed:
        click.confirm(f"Delete collection '{slug}'?", abort=True)

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.delete_collection(slug, purge_orphans=purge))
        console.print(f"[green]Deleted collection '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("rename")
@click.argument("slug")
@click.argument("new_name")
def collection_rename(slug, new_name):
    """Rename a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.rename_collection(slug, new_name))
        console.print(f"[green]Renamed to '{result.slug}' ({result.name})[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("add")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
def collection_add(slug, arxiv_ids):
    """Add papers to a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        added = asyncio.run(svc.add_papers(slug, list(arxiv_ids)))
        console.print(f"[green]Added {added} paper(s) to '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("remove")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
def collection_remove(slug, arxiv_ids):
    """Remove papers from a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        removed = asyncio.run(svc.remove_papers(slug, list(arxiv_ids)))
        console.print(f"[green]Removed {removed} paper(s) from '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("merge")
@click.argument("source_slug")
@click.argument("target_slug")
def collection_merge(source_slug, target_slug):
    """Merge source collection into target."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.merge_collections(source_slug, target_slug))
        console.print(
            f"[green]Merged '{source_slug}' into '{target_slug}' "
            f"({result.paper_count} papers)[/green]"
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("archive")
@click.argument("slug")
def collection_archive(slug):
    """Archive a collection (hide from default listing)."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.archive_collection(slug))
        console.print(f"[green]Archived collection '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@collection_group.command("unarchive")
@click.argument("slug")
def collection_unarchive(slug):
    """Unarchive a collection."""
    from arxiv_mcp.workflow.collections import CollectionService

    sf, settings = _make_session_factory()
    svc = CollectionService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.unarchive_collection(slug))
        console.print(f"[green]Unarchived collection '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


# ========================================================================
# TRIAGE GROUP
# ========================================================================


@click.group("triage")
def triage_group():
    """Manage paper triage states."""
    pass


@triage_group.command("mark")
@click.argument("arxiv_id")
@click.argument("state", type=click.Choice(
    ["unseen", "shortlisted", "dismissed", "read", "cite-later", "archived"]
))
@click.option("--source", default="manual", help="Source of the triage action")
@click.option("--reason", default=None, help="Optional reason for the state change")
def triage_mark(arxiv_id, state, source, reason):
    """Mark a paper with a triage state."""
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(
            svc.mark_triage(arxiv_id, state, source=source, reason=reason)
        )
        console.print(
            f"[green]Marked {result.paper_id} as '{result.state}'[/green]"
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@triage_group.command("show")
@click.argument("arxiv_id")
def triage_show(arxiv_id):
    """Show the current triage state for a paper."""
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    state = asyncio.run(svc.get_triage_state(arxiv_id))
    console.print(f"Paper {arxiv_id}: [bold]{state}[/bold]")


@triage_group.command("list")
@click.argument("state", type=click.Choice(
    ["unseen", "shortlisted", "dismissed", "read", "cite-later", "archived"]
))
@click.option("--page-size", default=20, help="Results per page")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def triage_list(state, page_size, output_json):
    """List papers by triage state."""
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    result = asyncio.run(svc.list_by_state(state, page_size=page_size))

    if output_json:
        click.echo(result.model_dump_json(indent=2))
        return

    if not result.items:
        console.print(f"[yellow]No papers with state '{state}'[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("arxiv_id", width=14)
    table.add_column("State", width=14)
    table.add_column("Updated", width=18)

    for item in result.items:
        table.add_row(item.paper_id, item.state, _format_dt(item.updated_at))

    console.print(table)


@triage_group.command("batch")
@click.argument("state", type=click.Choice(
    ["unseen", "shortlisted", "dismissed", "read", "cite-later", "archived"]
))
@click.argument("arxiv_ids", nargs=-1, required=True)
@click.option("--source", default="manual", help="Source of the triage action")
@click.option("--reason", default=None, help="Optional reason")
def triage_batch(state, arxiv_ids, source, reason):
    """Batch triage papers by explicit ID list."""
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    result = asyncio.run(
        svc.batch_triage(list(arxiv_ids), state, source=source, reason=reason)
    )

    console.print(
        f"[green]Affected: {result.affected_count}, "
        f"Skipped: {result.skipped_count}[/green]"
    )
    if result.errors:
        console.print(f"[red]Not found: {', '.join(result.errors)}[/red]")


@triage_group.command("batch-query")
@click.argument("state", type=click.Choice(
    ["unseen", "shortlisted", "dismissed", "read", "cite-later", "archived"]
))
@click.option("-q", "--query-text", help="Full-text search query")
@click.option("-c", "--category", help="Category filter")
@click.option("-a", "--author", help="Author filter")
@click.option("--from", "date_from", type=click.DateTime(formats=["%Y-%m-%d"]), help="Start date")
@click.option("--to", "date_to", type=click.DateTime(formats=["%Y-%m-%d"]), help="End date")
@click.option("--confirm", "confirmed", is_flag=True, help="Execute (default is dry-run)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def triage_batch_query(state, query_text, category, author, date_from, date_to, confirmed, output_json):
    """Batch triage papers matching a query (dry-run by default).

    Without --confirm: shows preview of matching papers.
    With --confirm: executes the batch triage.
    """
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    query_params = {}
    if query_text:
        query_params["query_text"] = query_text
    if category:
        query_params["category"] = category
    if author:
        query_params["author"] = author
    if date_from:
        query_params["date_from"] = date_from.date()
    if date_to:
        query_params["date_to"] = date_to.date()

    if not query_params:
        click.echo("Error: at least one filter is required.", err=True)
        raise SystemExit(1)

    dry_run = not confirmed
    result = asyncio.run(
        svc.batch_triage_by_query(
            query_params, state, dry_run=dry_run, source="batch"
        )
    )

    if output_json:
        click.echo(json.dumps(result.model_dump(), indent=2, default=str))
        return

    if dry_run:
        # Preview mode
        console.print(f"\n[bold]Dry-run preview for state '{state}'[/bold]")
        console.print(f"Query: {result.query_description}")
        console.print(f"Matching papers: {result.matching_count}")
        if result.sample_ids:
            console.print(f"Sample IDs: {', '.join(result.sample_ids[:5])}")
        console.print("\n[yellow]This is a dry run. Use --confirm to execute.[/yellow]")
    else:
        # Execute mode
        console.print(
            f"[green]Batch triage complete: "
            f"affected={result.affected_count}, "
            f"skipped={result.skipped_count}[/green]"
        )
        if result.errors:
            console.print(f"[red]Errors: {', '.join(result.errors)}[/red]")


@triage_group.command("log")
@click.argument("arxiv_id")
@click.option("--limit", default=50, help="Max entries to show")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def triage_log(arxiv_id, limit, output_json):
    """Show triage audit trail for a paper."""
    from arxiv_mcp.workflow.triage import TriageService

    sf, settings = _make_session_factory()
    svc = TriageService(session_factory=sf, settings=settings)

    entries = asyncio.run(svc.get_triage_log(arxiv_id, limit=limit))

    if output_json:
        data = [e.model_dump(mode="json") for e in entries]
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if not entries:
        console.print(f"[yellow]No triage history for {arxiv_id}[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Timestamp", width=18)
    table.add_column("From", width=14)
    table.add_column("To", width=14)
    table.add_column("Source", width=10)
    table.add_column("Reason", ratio=2)

    for e in entries:
        table.add_row(
            _format_dt(e.timestamp),
            e.old_state,
            e.new_state,
            e.source,
            e.reason or "",
        )

    console.print(table)


# ========================================================================
# QUERY GROUP
# ========================================================================


@click.group("query")
def query_group():
    """Manage saved queries."""
    pass


@query_group.command("create")
@click.argument("name")
@click.option("-q", "--query-text", help="Full-text search query")
@click.option("-c", "--category", help="Category filter")
@click.option("-a", "--author", help="Author filter")
@click.option("--from", "date_from", help="Start date (YYYY-MM-DD)")
@click.option("--to", "date_to", help="End date (YYYY-MM-DD)")
@click.option("--time-basis", default="announced", help="Time basis for date filters")
@click.option("--triage-filter", help="Triage state filter")
@click.option("--collection", "collection_filter", help="Collection slug filter")
def query_create(
    name, query_text, category, author, date_from, date_to, time_basis,
    triage_filter, collection_filter
):
    """Create a saved query with search parameters."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    params = {}
    if query_text:
        params["query_text"] = query_text
    if category:
        params["category"] = category
    if author:
        params["author"] = author
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    if time_basis != "announced":
        params["time_basis"] = time_basis
    if triage_filter:
        params["triage_filter"] = triage_filter
    if collection_filter:
        params["collection_filter"] = collection_filter

    try:
        result = asyncio.run(svc.create_saved_query(name, params))
        console.print(f"[green]Created saved query '{result.slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@query_group.command("list")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def query_list(output_json):
    """List all saved queries."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    queries = asyncio.run(svc.list_saved_queries())

    if output_json:
        data = [q.model_dump(mode="json") for q in queries]
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if not queries:
        console.print("[yellow]No saved queries.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Slug", width=24)
    table.add_column("Name", ratio=2)
    table.add_column("Runs", width=6, justify="right")
    table.add_column("Watch", width=8)
    table.add_column("Cadence", width=10)
    table.add_column("Last Run", width=18)

    for q in queries:
        watch = "[green]yes[/green]" if q.is_watch else ""
        table.add_row(
            q.slug, q.name, str(q.run_count), watch,
            q.cadence_hint or "", _format_dt(q.last_run_at)
        )

    console.print(table)


@query_group.command("show")
@click.argument("slug")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def query_show(slug, output_json):
    """Show a saved query's details."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        detail = asyncio.run(svc.get_saved_query(slug))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(detail.model_dump_json(indent=2))
        return

    console.print(f"\n[bold]{detail.name}[/bold] ({detail.slug})")
    console.print(f"Params: {json.dumps(detail.params, indent=2)}")
    console.print(f"Runs: {detail.run_count}")
    console.print(f"Watch: {'yes' if detail.is_watch else 'no'}")
    if detail.cadence_hint:
        console.print(f"Cadence: {detail.cadence_hint}")
    console.print(f"Last run: {_format_dt(detail.last_run_at)}")
    console.print(f"Created: {_format_dt(detail.created_at)}")
    console.print(f"Updated: {_format_dt(detail.updated_at)}")


@query_group.command("edit")
@click.argument("slug")
@click.option("--name", help="New name")
@click.option("--params-json", help="New params as JSON string")
def query_edit(slug, name, params_json):
    """Edit a saved query's name or params."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    params = None
    if params_json:
        try:
            params = json.loads(params_json)
        except json.JSONDecodeError:
            click.echo("Error: --params-json must be valid JSON", err=True)
            raise SystemExit(1)

    try:
        result = asyncio.run(svc.edit_saved_query(slug, name=name, params=params))
        console.print(f"[green]Updated saved query '{result.slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@query_group.command("run")
@click.argument("slug")
@click.option("--page-size", default=20, help="Results per page")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def query_run(slug, page_size, output_json):
    """Run a saved query."""
    from arxiv_mcp.search.cli import _display_pagination_info, _display_results_table
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        result = asyncio.run(svc.run_saved_query(slug, page_size=page_size))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(result.model_dump_json(indent=2))
        return

    if not result.items:
        console.print("[yellow]No results.[/yellow]")
        return

    has_score = any(item.score is not None for item in result.items)
    console.print(f"\n[bold]Query '{slug}' - {len(result.items)} results[/bold]\n")
    _display_results_table(result.items, show_score=has_score)
    _display_pagination_info(result.page_info)


@query_group.command("delete")
@click.argument("slug")
def query_delete(slug):
    """Delete a saved query."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.queries import SavedQueryService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = SavedQueryService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        asyncio.run(svc.delete_saved_query(slug))
        console.print(f"[green]Deleted saved query '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@query_group.command("watch")
@click.argument("slug")
@click.option("--cadence", default="daily", help="Cadence hint (daily/weekly)")
def query_watch(slug, cadence):
    """Promote a saved query to a watch."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        result = asyncio.run(svc.promote_to_watch(slug, cadence=cadence))
        console.print(
            f"[green]Promoted '{result.slug}' to watch "
            f"(cadence={result.cadence_hint})[/green]"
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@query_group.command("unwatch")
@click.argument("slug")
def query_unwatch(slug):
    """Demote a watch back to a regular saved query."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        result = asyncio.run(svc.demote_watch(slug))
        console.print(f"[green]Demoted '{result.slug}' from watch[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


# ========================================================================
# WATCH GROUP
# ========================================================================


@click.group("watch")
def watch_group():
    """Manage watches (saved queries with delta tracking)."""
    pass


@watch_group.command("check")
@click.argument("slug")
@click.option("--page-size", default=20, help="Results per page")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def watch_check(slug, page_size, output_json):
    """Check a watch for new papers since last checkpoint."""
    from arxiv_mcp.search.cli import _display_pagination_info, _display_results_table
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        result = asyncio.run(svc.check_watch(slug, page_size=page_size))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(result.model_dump_json(indent=2))
        return

    if not result.items:
        console.print(f"[green]No new papers for watch '{slug}'[/green]")
        return

    console.print(
        f"\n[bold]Watch '{slug}' - {len(result.items)} new papers[/bold]\n"
    )
    has_score = any(item.score is not None for item in result.items)
    _display_results_table(result.items, show_score=has_score)
    _display_pagination_info(result.page_info)


@watch_group.command("check-all")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def watch_check_all(output_json):
    """Check all active watches."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    results = asyncio.run(svc.check_all_watches())

    if output_json:
        click.echo(json.dumps(results, indent=2, default=str))
        return

    if not results:
        console.print("[yellow]No active watches.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Watch", width=24)
    table.add_column("New Papers", width=12, justify="right")
    table.add_column("Cadence", width=10)

    for r in results:
        table.add_row(r["slug"], str(r["delta_count"]), r.get("cadence_hint", ""))

    console.print(table)


@watch_group.command("pause")
@click.argument("slug")
def watch_pause(slug):
    """Pause a watch (excluded from check-all)."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        asyncio.run(svc.pause_watch(slug))
        console.print(f"[green]Paused watch '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@watch_group.command("resume")
@click.argument("slug")
def watch_resume(slug):
    """Resume a paused watch."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        asyncio.run(svc.resume_watch(slug))
        console.print(f"[green]Resumed watch '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@watch_group.command("reset")
@click.argument("slug")
@click.argument("date_str", metavar="DATE")
def watch_reset(slug, date_str):
    """Reset a watch's checkpoint date (YYYY-MM-DD)."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    try:
        new_date = date.fromisoformat(date_str)
    except ValueError:
        click.echo(f"Error: invalid date format '{date_str}'. Use YYYY-MM-DD.", err=True)
        raise SystemExit(1)

    try:
        result = asyncio.run(svc.reset_checkpoint(slug, new_date))
        console.print(
            f"[green]Reset checkpoint for '{slug}' to {result.checkpoint_date}[/green]"
        )
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@watch_group.command("dashboard")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def watch_dashboard(output_json):
    """Show watch dashboard with status overview."""
    from arxiv_mcp.search.service import SearchService
    from arxiv_mcp.workflow.watches import WatchService

    sf, settings = _make_session_factory()
    search_svc = SearchService(session_factory=sf, settings=settings)
    svc = WatchService(
        session_factory=sf, settings=settings, search_service=search_svc
    )

    dashboard = asyncio.run(svc.get_watch_dashboard())

    if output_json:
        click.echo(dashboard.model_dump_json(indent=2))
        return

    console.print(
        f"\n[bold]Watch Dashboard[/bold] "
        f"({dashboard.total_active} active, {dashboard.total_paused} paused)\n"
    )

    if not dashboard.watches:
        console.print("[yellow]No watches configured.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Slug", width=24)
    table.add_column("Name", ratio=2)
    table.add_column("Cadence", width=10)
    table.add_column("Checkpoint", width=12)
    table.add_column("Last Check", width=18)
    table.add_column("Pending", width=8, justify="right")
    table.add_column("Status", width=10)

    for w in dashboard.watches:
        status = "[red]paused[/red]" if w.is_paused else "[green]active[/green]"
        pending = str(w.pending_estimate) if w.pending_estimate is not None else "-"
        table.add_row(
            w.slug, w.name, w.cadence_hint or "",
            _format_dt(w.checkpoint_date),
            _format_dt(w.last_checked_at),
            pending, status,
        )

    console.print(table)


# ========================================================================
# PAPER GROUP
# ========================================================================


@click.group("paper")
def paper_group():
    """View paper details."""
    pass


@paper_group.command("show")
@click.argument("arxiv_id")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def paper_show(arxiv_id, output_json):
    """Show full paper metadata, triage state, and collections."""
    from arxiv_mcp.workflow.export import ExportService

    sf, settings = _make_session_factory()
    svc = ExportService(session_factory=sf, settings=settings)

    try:
        detail = asyncio.run(svc.get_paper_detail(arxiv_id))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(json.dumps(detail, indent=2, default=str))
        return

    paper = detail["paper"]
    console.print(f"\n[bold]{paper['title']}[/bold]")
    console.print(f"arXiv ID: {paper['arxiv_id']}")
    console.print(f"Authors: {paper['authors_text']}")
    console.print(f"Categories: {paper['categories']}")
    console.print(f"Submitted: {_format_dt(paper.get('submitted_date'))}")
    console.print(f"Announced: {_format_dt(paper.get('announced_date'))}")

    if paper.get("abstract"):
        console.print(f"\n[dim]Abstract:[/dim]\n{paper['abstract']}")

    console.print(f"\n[bold]Triage state:[/bold] {detail['triage_state']}")

    if detail["collections"]:
        coll_names = ", ".join(c["name"] for c in detail["collections"])
        console.print(f"[bold]Collections:[/bold] {coll_names}")
    else:
        console.print("[bold]Collections:[/bold] none")

    if paper.get("doi"):
        console.print(f"DOI: {paper['doi']}")
    if paper.get("comments"):
        console.print(f"Comments: {paper['comments']}")
    if paper.get("journal_ref"):
        console.print(f"Journal: {paper['journal_ref']}")


# ========================================================================
# WORKFLOW GROUP
# ========================================================================


@click.group("workflow")
def workflow_group():
    """Workflow management: export, import, stats, reset."""
    pass


@workflow_group.command("export")
@click.option("--file", "file_path", default=None, help="Export file path")
@click.option("--types", default=None, help="Comma-separated entity types to export")
def workflow_export(file_path, types):
    """Export workflow state to JSON file."""
    from arxiv_mcp.workflow.export import ExportService

    sf, settings = _make_session_factory()
    svc = ExportService(session_factory=sf, settings=settings)

    if file_path is None:
        file_path = settings.export_default_path

    entity_types = types.split(",") if types else None

    asyncio.run(svc.export_to_file(file_path, entity_types=entity_types))
    console.print(f"[green]Exported workflow state to {file_path}[/green]")


@workflow_group.command("import")
@click.argument("file_path")
@click.option("--conflict", default="skip", type=click.Choice(["skip", "overwrite"]))
def workflow_import(file_path, conflict):
    """Import workflow state from a JSON file."""
    from arxiv_mcp.workflow.export import ExportService

    sf, settings = _make_session_factory()
    svc = ExportService(session_factory=sf, settings=settings)

    result = asyncio.run(
        svc.import_from_file(file_path, conflict_strategy=conflict)
    )

    console.print(
        f"[green]Imported: {result['imported_count']}, "
        f"Skipped: {result['skipped_count']}[/green]"
    )
    for warning in result["warnings"]:
        console.print(f"[yellow]Warning: {warning}[/yellow]")


@workflow_group.command("stats")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def workflow_stats(output_json):
    """Show workflow stats overview."""
    from arxiv_mcp.workflow.export import ExportService

    sf, settings = _make_session_factory()
    svc = ExportService(session_factory=sf, settings=settings)

    stats = asyncio.run(svc.get_stats())

    if output_json:
        click.echo(stats.model_dump_json(indent=2))
        return

    console.print("\n[bold]Workflow Stats[/bold]\n")
    console.print(f"Collections: {stats.collection_count}")
    console.print(f"Saved queries: {stats.saved_query_count}")
    console.print(f"Watches: {stats.watch_count}")
    console.print("\n[bold]Triage breakdown:[/bold]")
    for state, count in sorted(stats.triage_counts.items()):
        console.print(f"  {state}: {count}")

    if stats.insights:
        console.print("\n[bold]Insights:[/bold]")
        for insight in stats.insights:
            console.print(f"  - {insight}")


@workflow_group.command("reset")
@click.option("--confirm", "confirmed", is_flag=True, required=True, help="Required flag to confirm reset")
def workflow_reset(confirmed):
    """Nuclear reset: clear all workflow state (preserves papers)."""
    from arxiv_mcp.workflow.export import ExportService

    if not confirmed:
        click.echo("Error: --confirm flag is required for nuclear reset.", err=True)
        raise SystemExit(1)

    sf, settings = _make_session_factory()
    svc = ExportService(session_factory=sf, settings=settings)

    asyncio.run(svc.nuclear_reset())
    console.print("[green]All workflow state cleared. Paper corpus preserved.[/green]")
