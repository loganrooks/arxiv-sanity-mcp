"""CLI entry point for arxiv-mcp.

Provides the main Click group. Subcommands for harvest and search
are registered by their respective modules in Plans 02 and 03.
"""

from __future__ import annotations

import click


@click.group()
@click.version_option(package_name="arxiv-mcp")
def cli() -> None:
    """arxiv-mcp: arXiv research discovery substrate."""


# Subgroups will be registered here by subsequent plans:
# - cli.add_command(harvest_group)  # Plan 02
# - cli.add_command(search_group)   # Plan 03
