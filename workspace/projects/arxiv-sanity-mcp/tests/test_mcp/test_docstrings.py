"""Docstring regression tests for MCP tools.

Ensures tool docstrings reference correct MCP resources and tools,
preventing stale references to non-existent tools.
"""
from arxiv_mcp.mcp.tools.workflow import create_watch


class TestWorkflowToolDocstrings:
    def test_create_watch_references_watch_resource(self):
        """SC-3: create_watch docstring must reference watch:// resource, not get_delta."""
        doc = create_watch.__doc__
        assert doc is not None, "create_watch must have a docstring"
        assert "watch://" in doc, (
            "create_watch docstring must reference watch:// resource"
        )
        assert "/deltas" in doc, (
            "create_watch docstring must reference /deltas"
        )
