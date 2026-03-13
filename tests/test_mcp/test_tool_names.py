"""Tests for MCP tool naming convention, total tool count, and resource count.

Verifies MCP-06 (user-intent tool names) and MCP-07 (tool count) requirements.
"""

from __future__ import annotations

import asyncio

import pytest


class TestToolCount:
    """MCP-07: Total tool count should be exactly 11."""

    def test_tool_count_is_eleven(self):
        # Import triggers all tool module registrations via server.py bottom imports
        from arxiv_mcp.mcp.server import mcp

        tools = asyncio.run(mcp.list_tools())
        tool_names = [t.name for t in tools]
        assert len(tools) == 11, (
            f"Expected 11 tools, got {len(tools)}: {sorted(tool_names)}"
        )


class TestToolNames:
    """MCP-06: All tool names describe user intent, not implementation details."""

    def test_tool_names_match_expected_set(self):
        from arxiv_mcp.mcp.server import mcp

        expected = {
            "search_papers",
            "browse_recent",
            "find_related_papers",
            "get_paper",
            "triage_paper",
            "add_to_collection",
            "create_watch",
            "add_signal",
            "batch_add_signals",
            "enrich_paper",
            "get_content_variant",
        }
        tools = asyncio.run(mcp.list_tools())
        actual = {t.name for t in tools}
        assert actual == expected, f"Tool name mismatch: extra={actual - expected}, missing={expected - actual}"

    def test_no_implementation_leaking_names(self):
        from arxiv_mcp.mcp.server import mcp

        banned_terms = ["embedding", "database", "sql", "query_db", "fetch_rows", "orm"]
        tools = asyncio.run(mcp.list_tools())
        for tool in tools:
            for term in banned_terms:
                assert term not in tool.name.lower(), (
                    f"Tool name '{tool.name}' contains implementation-leaking term '{term}'"
                )


class TestResourceCount:
    """Resource template count should be exactly 4."""

    def test_resource_count_is_four(self):
        from arxiv_mcp.mcp.server import mcp

        templates = asyncio.run(mcp.list_resource_templates())
        template_uris = [t.uriTemplate for t in templates]
        assert len(templates) == 4, (
            f"Expected 4 resource templates, got {len(templates)}: {template_uris}"
        )
