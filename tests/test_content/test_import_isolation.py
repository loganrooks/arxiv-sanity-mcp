"""Import isolation tests for content package.

Ensures importing content.models does not eagerly load heavy dependencies
(httpx, beautifulsoup4, marker). Uses subprocess for a clean interpreter
to avoid false passes from pre-loaded modules in the test runner.
"""
import subprocess
import sys


class TestContentImportIsolation:
    def test_content_models_does_not_load_httpx_or_bs4(self):
        """SC-4: Importing content.models must not pull in httpx or bs4.

        Uses subprocess to guarantee a clean interpreter state.
        A sys.modules check in the test runner would pass vacuously
        if httpx/bs4 were already loaded by earlier tests.
        """
        script = (
            "import sys; "
            "from arxiv_mcp.content.models import VariantType; "
            "loaded = list(sys.modules.keys()); "
            "problems = [m for m in loaded if 'httpx' in m or 'bs4' in m "
            "or m == 'arxiv_mcp.content.html_fetcher' "
            "or m == 'arxiv_mcp.content.adapters' "
            "or m == 'arxiv_mcp.content.service']; "
            "print(','.join(problems) if problems else 'CLEAN')"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Import script failed: {result.stderr}"
        )
        output = result.stdout.strip()
        assert output == "CLEAN", (
            f"Importing content.models loaded unexpected modules: {output}"
        )

    def test_content_rights_does_not_load_httpx_or_bs4(self):
        """SC-4 extension: content.rights should also be isolated from heavy deps."""
        script = (
            "import sys; "
            "from arxiv_mcp.content.rights import RightsChecker; "
            "loaded = list(sys.modules.keys()); "
            "problems = [m for m in loaded if 'httpx' in m or 'bs4' in m "
            "or m == 'arxiv_mcp.content.html_fetcher' "
            "or m == 'arxiv_mcp.content.adapters']; "
            "print(','.join(problems) if problems else 'CLEAN')"
        )
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Import script failed: {result.stderr}"
        )
        output = result.stdout.strip()
        assert output == "CLEAN", (
            f"Importing content.rights loaded unexpected modules: {output}"
        )
