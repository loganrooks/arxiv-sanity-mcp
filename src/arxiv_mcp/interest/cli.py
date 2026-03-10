"""CLI subgroup for interest profile management.

Provides Click commands for profile CRUD, signal management (add/remove
for all 4 signal types), signal inspection with provenance display,
and suggestion workflow (generate, confirm, dismiss).

Follows the established CLI pattern: sync Click handlers wrapping
asyncio.run(), Rich table output, --json flag for machine-readable output.
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
    """Create session factory, settings, and interest services."""
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


# Source colors for provenance display
_SOURCE_COLORS = {
    "manual": "green",
    "suggestion": "yellow",
    "agent": "cyan",
}


# ========================================================================
# PROFILE GROUP
# ========================================================================


@click.group("profile")
def profile_group():
    """Manage interest profiles and signals."""
    pass


# ---------------------------------------------------------------
# Profile CRUD
# ---------------------------------------------------------------


@profile_group.command("create")
@click.argument("name")
@click.option("--negative-weight", type=float, default=None, help="Negative example demotion weight")
def profile_create(name, negative_weight):
    """Create a new interest profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.create_profile(name, negative_weight=negative_weight))
        console.print(f"[green]Created profile '{result.slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@profile_group.command("list")
@click.option("--include-archived", is_flag=True, help="Include archived profiles")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def profile_list(include_archived, output_json):
    """List all interest profiles."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    profiles = asyncio.run(svc.list_profiles(include_archived=include_archived))

    if output_json:
        data = [p.model_dump(mode="json") for p in profiles]
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if not profiles:
        console.print("[yellow]No profiles found.[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Slug", width=24)
    table.add_column("Name", ratio=2)
    table.add_column("Signals", width=8, justify="right")
    table.add_column("Neg. Wt.", width=8, justify="right")
    table.add_column("Archived", width=10)
    table.add_column("Created", width=18)

    for p in profiles:
        archived = "[dim]yes[/dim]" if p.is_archived else ""
        table.add_row(
            p.slug, p.name, str(p.signal_count),
            f"{p.negative_weight:.2f}", archived, _format_dt(p.created_at),
        )

    console.print(table)


@profile_group.command("show")
@click.argument("slug")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def profile_show(slug, output_json):
    """Show profile detail with all signals grouped by type."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        detail = asyncio.run(svc.get_profile(slug))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if output_json:
        click.echo(detail.model_dump_json(indent=2))
        return

    console.print(f"\n[bold]{detail.name}[/bold] ({detail.slug})")
    console.print(f"Signals: {detail.signal_count}")
    console.print(f"Negative weight: {detail.negative_weight:.2f}")
    console.print(f"Archived: {'yes' if detail.is_archived else 'no'}")
    console.print(f"Created: {_format_dt(detail.created_at)}")
    console.print(f"Updated: {_format_dt(detail.updated_at)}")

    if detail.signal_counts_by_type:
        console.print("\n[bold]Signal counts by type:[/bold]")
        for stype, count in sorted(detail.signal_counts_by_type.items()):
            console.print(f"  {stype}: {count}")

    if detail.signal_counts_by_source:
        console.print("\n[bold]Signal counts by source:[/bold]")
        for source, count in sorted(detail.signal_counts_by_source.items()):
            color = _SOURCE_COLORS.get(source, "white")
            console.print(f"  [{color}]{source}[/{color}]: {count}")


@profile_group.command("delete")
@click.argument("slug")
@click.option("--confirm", "confirmed", is_flag=True, help="Skip confirmation prompt")
def profile_delete(slug, confirmed):
    """Delete a profile and all its signals."""
    from arxiv_mcp.interest.profiles import ProfileService

    if not confirmed:
        click.confirm(f"Delete profile '{slug}'?", abort=True)

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.delete_profile(slug))
        console.print(f"[green]Deleted profile '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@profile_group.command("rename")
@click.argument("slug")
@click.argument("new_name")
def profile_rename(slug, new_name):
    """Rename a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        result = asyncio.run(svc.rename_profile(slug, new_name))
        console.print(f"[green]Renamed to '{result.slug}' ({result.name})[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@profile_group.command("archive")
@click.argument("slug")
def profile_archive(slug):
    """Archive a profile (hide from default listing)."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.archive_profile(slug))
        console.print(f"[green]Archived profile '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


@profile_group.command("unarchive")
@click.argument("slug")
def profile_unarchive(slug):
    """Unarchive a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        asyncio.run(svc.unarchive_profile(slug))
        console.print(f"[green]Unarchived profile '{slug}'[/green]")
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)


# ---------------------------------------------------------------
# Signal management
# ---------------------------------------------------------------


@profile_group.command("add-seed")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
@click.option("--reason", default=None, help="Reason for adding this signal")
def profile_add_seed(slug, arxiv_ids, reason):
    """Add seed paper(s) to a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    added = 0
    for arxiv_id in arxiv_ids:
        try:
            asyncio.run(svc.add_seed_paper(slug, arxiv_id, reason=reason))
            added += 1
        except ValueError as e:
            console.print(f"[red]Error adding {arxiv_id}: {e}[/red]")

    console.print(f"[green]Added {added} seed paper(s) to '{slug}'[/green]")


@profile_group.command("remove-seed")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
def profile_remove_seed(slug, arxiv_ids):
    """Remove seed paper(s) from a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    removed = 0
    for arxiv_id in arxiv_ids:
        try:
            asyncio.run(svc.remove_seed_paper(slug, arxiv_id))
            removed += 1
        except ValueError as e:
            console.print(f"[red]Error removing {arxiv_id}: {e}[/red]")

    console.print(f"[green]Removed {removed} seed paper(s) from '{slug}'[/green]")


@profile_group.command("add-query")
@click.argument("slug")
@click.argument("query_slugs", nargs=-1, required=True)
@click.option("--reason", default=None, help="Reason for adding this signal")
def profile_add_query(slug, query_slugs, reason):
    """Add saved query signal(s) to a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    added = 0
    for qs in query_slugs:
        try:
            asyncio.run(svc.add_saved_query(slug, qs, reason=reason))
            added += 1
        except ValueError as e:
            console.print(f"[red]Error adding {qs}: {e}[/red]")

    console.print(f"[green]Added {added} query signal(s) to '{slug}'[/green]")


@profile_group.command("remove-query")
@click.argument("slug")
@click.argument("query_slugs", nargs=-1, required=True)
def profile_remove_query(slug, query_slugs):
    """Remove saved query signal(s) from a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    removed = 0
    for qs in query_slugs:
        try:
            asyncio.run(svc.remove_saved_query(slug, qs))
            removed += 1
        except ValueError as e:
            console.print(f"[red]Error removing {qs}: {e}[/red]")

    console.print(f"[green]Removed {removed} query signal(s) from '{slug}'[/green]")


@profile_group.command("follow")
@click.argument("slug")
@click.argument("author_names", nargs=-1, required=True)
@click.option("--reason", default=None, help="Reason for following this author")
def profile_follow(slug, author_names, reason):
    """Follow author(s) in a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    added = 0
    for name in author_names:
        try:
            asyncio.run(svc.add_followed_author(slug, name, reason=reason))
            added += 1
        except ValueError as e:
            console.print(f"[red]Error following {name}: {e}[/red]")

    console.print(f"[green]Followed {added} author(s) in '{slug}'[/green]")


@profile_group.command("unfollow")
@click.argument("slug")
@click.argument("author_names", nargs=-1, required=True)
def profile_unfollow(slug, author_names):
    """Unfollow author(s) in a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    removed = 0
    for name in author_names:
        try:
            asyncio.run(svc.remove_followed_author(slug, name))
            removed += 1
        except ValueError as e:
            console.print(f"[red]Error unfollowing {name}: {e}[/red]")

    console.print(f"[green]Unfollowed {removed} author(s) in '{slug}'[/green]")


@profile_group.command("add-negative")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
@click.option("--reason", default=None, help="Reason for adding negative example")
def profile_add_negative(slug, arxiv_ids, reason):
    """Add negative example paper(s) to a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    added = 0
    for arxiv_id in arxiv_ids:
        try:
            asyncio.run(svc.add_negative_example(slug, arxiv_id, reason=reason))
            added += 1
        except ValueError as e:
            console.print(f"[red]Error adding {arxiv_id}: {e}[/red]")

    console.print(f"[green]Added {added} negative example(s) to '{slug}'[/green]")


@profile_group.command("remove-negative")
@click.argument("slug")
@click.argument("arxiv_ids", nargs=-1, required=True)
def profile_remove_negative(slug, arxiv_ids):
    """Remove negative example paper(s) from a profile."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    removed = 0
    for arxiv_id in arxiv_ids:
        try:
            asyncio.run(svc.remove_negative_example(slug, arxiv_id))
            removed += 1
        except ValueError as e:
            console.print(f"[red]Error removing {arxiv_id}: {e}[/red]")

    console.print(f"[green]Removed {removed} negative example(s) from '{slug}'[/green]")


# ---------------------------------------------------------------
# Signal inspection
# ---------------------------------------------------------------


@profile_group.command("signals")
@click.argument("slug")
@click.option("--type", "signal_type", default=None, help="Filter by signal type")
@click.option("--status", "signal_status", default=None, help="Filter by status (active/pending/dismissed)")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def profile_signals(slug, signal_type, signal_status, output_json):
    """List all signals in a profile with provenance."""
    from arxiv_mcp.interest.profiles import ProfileService

    sf, settings = _make_services()
    svc = ProfileService(session_factory=sf, settings=settings)

    try:
        detail = asyncio.run(svc.get_profile(slug))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    signals = detail.signals
    if signal_type:
        signals = [s for s in signals if s.signal_type == signal_type]
    if signal_status:
        signals = [s for s in signals if s.status == signal_status]

    if output_json:
        data = [s.model_dump(mode="json") for s in signals]
        click.echo(json.dumps(data, indent=2, default=str))
        return

    if not signals:
        console.print(f"[yellow]No signals in profile '{slug}'")
        if signal_type:
            console.print(f" (filtered by type={signal_type})")
        if signal_status:
            console.print(f" (filtered by status={signal_status})")
        console.print("[/yellow]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Type", width=18)
    table.add_column("Value", ratio=2)
    table.add_column("Status", width=12)
    table.add_column("Source", width=12)
    table.add_column("Added", width=18)
    table.add_column("Reason", ratio=2)

    for s in signals:
        source_color = _SOURCE_COLORS.get(s.source, "white")
        status_display = s.status
        if s.status == "pending":
            status_display = "[yellow][pending][/yellow]"
        elif s.status == "dismissed":
            status_display = "[dim]dismissed[/dim]"
        elif s.status == "active":
            status_display = "[green]active[/green]"

        table.add_row(
            s.signal_type,
            s.signal_value,
            status_display,
            f"[{source_color}]{s.source}[/{source_color}]",
            _format_dt(s.added_at),
            s.reason or "",
        )

    console.print(f"\n[bold]Signals in '{slug}'[/bold] ({len(signals)} total)\n")
    console.print(table)


# ---------------------------------------------------------------
# Suggestion commands
# ---------------------------------------------------------------


@profile_group.command("suggest")
@click.argument("slug")
@click.option("--apply", "apply_suggestions", is_flag=True,
              help="Add suggestions as pending signals")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON")
def profile_suggest(slug, apply_suggestions, output_json):
    """Generate suggestions from workflow activity.

    Without --apply: shows candidates.
    With --apply: adds candidates as pending signals.
    """
    from arxiv_mcp.interest.profiles import ProfileService
    from arxiv_mcp.interest.suggestions import SuggestionService

    sf, settings = _make_services()
    profile_svc = ProfileService(session_factory=sf, settings=settings)
    svc = SuggestionService(
        session_factory=sf, settings=settings, profile_service=profile_svc,
    )

    try:
        candidates = asyncio.run(svc.generate_suggestions(slug))
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if not candidates:
        console.print("[yellow]No suggestions available.[/yellow]")
        return

    if output_json:
        data = [
            {"signal_type": c.signal_type, "signal_value": c.signal_value,
             "reason": c.reason, "score": c.score}
            for c in candidates
        ]
        click.echo(json.dumps(data, indent=2))
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", width=4, justify="right")
    table.add_column("Type", width=18)
    table.add_column("Value", ratio=2)
    table.add_column("Reason", ratio=3)
    table.add_column("Score", width=8, justify="right")

    for i, c in enumerate(candidates, 1):
        table.add_row(
            str(i), c.signal_type, c.signal_value,
            c.reason, f"{c.score:.1f}",
        )

    console.print(f"\n[bold]Suggestions for '{slug}'[/bold] ({len(candidates)} candidates)\n")
    console.print(table)

    if apply_suggestions:
        added = asyncio.run(svc.add_suggestions_to_profile(slug, candidates))
        console.print(
            f"\n[green]Added {len(added)} suggestion(s) as pending signals. "
            f"Use 'profile confirm' to accept or 'profile dismiss' to reject.[/green]"
        )


@profile_group.command("confirm")
@click.argument("slug")
@click.argument("signal_ids", nargs=-1, required=True)
def profile_confirm(slug, signal_ids):
    """Confirm pending suggestion(s).

    SIGNAL_IDS can be type:value pairs (e.g., seed_paper:2301.00001).
    """
    from arxiv_mcp.interest.profiles import ProfileService
    from arxiv_mcp.interest.suggestions import SuggestionService

    sf, settings = _make_services()
    profile_svc = ProfileService(session_factory=sf, settings=settings)
    svc = SuggestionService(
        session_factory=sf, settings=settings, profile_service=profile_svc,
    )

    confirmed = 0
    for sid in signal_ids:
        if ":" not in sid:
            console.print(f"[red]Invalid format: {sid} (expected type:value)[/red]")
            continue
        signal_type, signal_value = sid.split(":", 1)
        try:
            asyncio.run(svc.confirm_suggestion(slug, signal_type, signal_value))
            confirmed += 1
        except ValueError as e:
            console.print(f"[red]Error confirming {sid}: {e}[/red]")

    console.print(f"[green]Confirmed {confirmed} suggestion(s) in '{slug}'[/green]")


@profile_group.command("dismiss")
@click.argument("slug")
@click.argument("signal_ids", nargs=-1, required=True)
def profile_dismiss(slug, signal_ids):
    """Dismiss pending suggestion(s).

    SIGNAL_IDS can be type:value pairs (e.g., seed_paper:2301.00001).
    """
    from arxiv_mcp.interest.profiles import ProfileService
    from arxiv_mcp.interest.suggestions import SuggestionService

    sf, settings = _make_services()
    profile_svc = ProfileService(session_factory=sf, settings=settings)
    svc = SuggestionService(
        session_factory=sf, settings=settings, profile_service=profile_svc,
    )

    dismissed = 0
    for sid in signal_ids:
        if ":" not in sid:
            console.print(f"[red]Invalid format: {sid} (expected type:value)[/red]")
            continue
        signal_type, signal_value = sid.split(":", 1)
        try:
            asyncio.run(svc.dismiss_suggestion(slug, signal_type, signal_value))
            dismissed += 1
        except ValueError as e:
            console.print(f"[red]Error dismissing {sid}: {e}[/red]")

    console.print(f"[green]Dismissed {dismissed} suggestion(s) in '{slug}'[/green]")
