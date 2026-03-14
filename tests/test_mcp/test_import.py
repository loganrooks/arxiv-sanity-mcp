"""Tests for arxiv-scan import script data-loading functions.

Validates pure functions: JSON parsing, score-to-triage mapping,
tension signal generation. Uses inline fixture data, NOT /scratch/.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Fixture helpers: write small JSON files to a temp directory
# ---------------------------------------------------------------------------

@pytest.fixture
def data_dir(tmp_path: Path) -> Path:
    """Create a temp directory with minimal pipeline data files."""

    # triage/final-selection.json
    triage_dir = tmp_path / "triage"
    triage_dir.mkdir()
    final_selection = {
        "metadata": {"total_papers": 3},
        "papers": [
            {"arxiv_id": "2301.00001", "title": "Paper One", "normalized_holistic": 9},
            {"arxiv_id": "2301.00002", "title": "Paper Two", "normalized_holistic": 8},
            {"arxiv_id": "2301.00003", "title": "Paper Three", "normalized_holistic": 7},
        ],
    }
    (triage_dir / "final-selection.json").write_text(json.dumps(final_selection))

    # reading/paper-index-data.json
    reading_dir = tmp_path / "reading"
    reading_dir.mkdir()
    paper_index = [
        {"id": "2301.00001", "title": "Paper One", "value": 9},
        {"id": "2301.00002", "title": "Paper Two", "value": 6},
        {"id": "2301.00003", "title": "Paper Three", "value": 7},
    ]
    (reading_dir / "paper-index-data.json").write_text(json.dumps(paper_index))

    # excluded-paper-audit.json
    excluded = [
        {"arxiv_id": "2501.11733", "title": "Excluded One", "verdict": "include"},
        {"arxiv_id": "2501.11425", "title": "Excluded Two", "verdict": "include"},
    ]
    (tmp_path / "excluded-paper-audit.json").write_text(json.dumps(excluded))

    return tmp_path


# ---------------------------------------------------------------------------
# Test: load_final_selection
# ---------------------------------------------------------------------------

class TestLoadFinalSelection:
    """Parsing final-selection.json returns paper dicts."""

    def test_returns_papers_list(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_final_selection

        papers = load_final_selection(data_dir)
        assert isinstance(papers, list)
        assert len(papers) == 3

    def test_papers_have_arxiv_id(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_final_selection

        papers = load_final_selection(data_dir)
        ids = [p["arxiv_id"] for p in papers]
        assert "2301.00001" in ids
        assert "2301.00002" in ids
        assert "2301.00003" in ids

    def test_with_real_data_count(self):
        """If real pipeline data exists, confirm 150 papers."""
        real_dir = Path("/scratch/arxiv-scan/pipeline")
        if not (real_dir / "triage" / "final-selection.json").exists():
            pytest.skip("Real pipeline data not available")

        from arxiv_mcp.scripts.import_arxiv_scan import load_final_selection

        papers = load_final_selection(real_dir)
        assert len(papers) == 150


# ---------------------------------------------------------------------------
# Test: load_excluded_papers
# ---------------------------------------------------------------------------

class TestLoadExcludedPapers:
    """Parsing excluded-paper-audit.json returns paper dicts."""

    def test_returns_list(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_excluded_papers

        papers = load_excluded_papers(data_dir)
        assert isinstance(papers, list)
        assert len(papers) == 2

    def test_papers_have_arxiv_id(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_excluded_papers

        papers = load_excluded_papers(data_dir)
        ids = [p["arxiv_id"] for p in papers]
        assert "2501.11733" in ids
        assert "2501.11425" in ids

    def test_with_real_data_count(self):
        """If real pipeline data exists, confirm 7 excluded papers."""
        real_dir = Path("/scratch/arxiv-scan/pipeline")
        if not (real_dir / "excluded-paper-audit.json").exists():
            pytest.skip("Real pipeline data not available")

        from arxiv_mcp.scripts.import_arxiv_scan import load_excluded_papers

        papers = load_excluded_papers(real_dir)
        assert len(papers) == 7


# ---------------------------------------------------------------------------
# Test: load_paper_index
# ---------------------------------------------------------------------------

class TestLoadPaperIndex:
    """Parsing paper-index-data.json returns dict keyed by arxiv ID."""

    def test_returns_dict(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_paper_index

        index = load_paper_index(data_dir)
        assert isinstance(index, dict)
        assert len(index) == 3

    def test_keyed_by_id(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_paper_index

        index = load_paper_index(data_dir)
        assert "2301.00001" in index
        assert index["2301.00001"]["value"] == 9

    def test_value_accessible(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import load_paper_index

        index = load_paper_index(data_dir)
        assert index["2301.00002"]["value"] == 6


# ---------------------------------------------------------------------------
# Test: map_value_to_triage_state
# ---------------------------------------------------------------------------

class TestMapValueToTriageState:
    """Score-to-triage mapping: >= 7 shortlisted, < 7 seen."""

    @pytest.mark.parametrize("value,expected", [
        (1, "seen"),
        (2, "seen"),
        (3, "seen"),
        (4, "seen"),
        (5, "seen"),
        (6, "seen"),
        (7, "shortlisted"),
        (8, "shortlisted"),
        (9, "shortlisted"),
        (10, "shortlisted"),
    ])
    def test_full_range(self, value: int, expected: str):
        from arxiv_mcp.scripts.import_arxiv_scan import map_value_to_triage_state

        assert map_value_to_triage_state(value) == expected


# ---------------------------------------------------------------------------
# Test: build_tension_signals
# ---------------------------------------------------------------------------

class TestBuildTensionSignals:
    """Tension signal builder returns exactly 10 signals."""

    def test_returns_10_signals(self):
        from arxiv_mcp.scripts.import_arxiv_scan import build_tension_signals

        signals = build_tension_signals()
        assert len(signals) == 10

    def test_signal_structure(self):
        from arxiv_mcp.scripts.import_arxiv_scan import build_tension_signals

        signals = build_tension_signals()
        for s in signals:
            assert "signal_type" in s
            assert "signal_value" in s
            assert "reason" in s
            assert s["signal_type"] == "followed_author"

    def test_signal_values_are_tension_names(self):
        from arxiv_mcp.scripts.import_arxiv_scan import build_tension_signals

        signals = build_tension_signals()
        values = {s["signal_value"] for s in signals}
        # Check a few known tension names
        assert "autonomy_vs_control" in values
        assert "memory_vs_forgetting" in values
        assert "competence_vs_comprehension" in values

    def test_no_duplicate_tensions(self):
        from arxiv_mcp.scripts.import_arxiv_scan import build_tension_signals

        signals = build_tension_signals()
        values = [s["signal_value"] for s in signals]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Test: no overlap between final-selection and excluded-audit IDs
# ---------------------------------------------------------------------------

class TestNoOverlap:
    """Paper IDs from final-selection and excluded-audit must not overlap."""

    def test_no_id_overlap(self, data_dir: Path):
        from arxiv_mcp.scripts.import_arxiv_scan import (
            load_excluded_papers,
            load_final_selection,
        )

        selection_ids = {p["arxiv_id"] for p in load_final_selection(data_dir)}
        excluded_ids = {p["arxiv_id"] for p in load_excluded_papers(data_dir)}
        overlap = selection_ids & excluded_ids
        assert len(overlap) == 0, f"Overlapping IDs: {overlap}"
