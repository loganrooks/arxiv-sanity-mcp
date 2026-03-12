"""CLI entry point for arxiv-mcp.

Provides the main Click group. Subcommands for harvest, search,
and workflow operations are registered by their respective modules.
"""

from __future__ import annotations

import click


@click.group()
@click.version_option(package_name="arxiv-mcp")
def cli() -> None:
    """arxiv-mcp: arXiv research discovery substrate."""


# Register harvest subgroup (Phase 1, Plan 02)
from arxiv_mcp.ingestion.cli import harvest_group

cli.add_command(harvest_group)

# Search subgroup (Phase 1, Plan 03)
try:
    from arxiv_mcp.search.cli import search_group

    cli.add_command(search_group)
except (ImportError, ModuleNotFoundError):
    pass

# Workflow subgroups (Phase 2, Plan 03)
try:
    from arxiv_mcp.workflow.cli import (
        collection_group,
        paper_group,
        query_group,
        triage_group,
        watch_group,
        workflow_group,
    )

    cli.add_command(collection_group)
    cli.add_command(triage_group)
    cli.add_command(query_group)
    cli.add_command(watch_group)
    cli.add_command(paper_group)
    cli.add_command(workflow_group)
except (ImportError, ModuleNotFoundError):
    pass

# Interest profile subgroup (Phase 3, Plan 03)
try:
    from arxiv_mcp.interest.cli import profile_group

    cli.add_command(profile_group)
except (ImportError, ModuleNotFoundError):
    pass

# Enrichment subgroup (Phase 4, Plan 02)
try:
    from arxiv_mcp.enrichment.cli import enrich_group

    cli.add_command(enrich_group)
except (ImportError, ModuleNotFoundError):
    pass

# Import subgroup (Phase 5, Plan 01)
try:
    from arxiv_mcp.scripts.import_arxiv_scan import import_scan_group

    cli.add_command(import_scan_group)
except (ImportError, ModuleNotFoundError):
    pass
