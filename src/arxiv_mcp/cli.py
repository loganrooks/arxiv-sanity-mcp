"""CLI entry point for arxiv-mcp.

Provides the main Click group. Subcommands for harvest and search
are registered by their respective modules.
"""

from __future__ import annotations

import click


@click.group()
@click.version_option(package_name="arxiv-mcp")
def cli() -> None:
    """arxiv-mcp: arXiv research discovery substrate."""


# Register harvest subgroup (Plan 02)
from arxiv_mcp.ingestion.cli import harvest_group

cli.add_command(harvest_group)

# Search subgroup will be registered by Plan 03
try:
    from arxiv_mcp.search.cli import search_group

    cli.add_command(search_group)
except (ImportError, ModuleNotFoundError):
    pass  # Plan 03 (search) not yet implemented
