"""
Resource measurement utilities for strategy profiling.

Measures the operational cost of running a recommendation strategy:
latency, memory, setup time, storage.
"""

from __future__ import annotations

import gc
import os
import time
from typing import Callable, Optional

import numpy as np


def measure_latency(
    strategy_fn: Callable,
    seed_ids: list[str],
    top_k: int = 20,
    n_warmup: int = 5,
    n_runs: int = 100,
) -> dict:
    """Measure query latency of a strategy.

    Runs the strategy n_runs times and reports p50, p95, mean, min, max.
    Includes warmup runs that are excluded from measurement.

    Args:
        strategy_fn: Callable that takes (seed_ids, top_k) and returns results.
            Typically strategy.recommend.
        seed_ids: Seed paper IDs to use for each run.
        top_k: Number of results per query.
        n_warmup: Warmup runs (excluded from stats).
        n_runs: Measurement runs.

    Returns:
        {"p50_ms": float, "p95_ms": float, "mean_ms": float,
         "min_ms": float, "max_ms": float, "n_runs": int}
    """
    # Warmup
    for _ in range(n_warmup):
        strategy_fn(seed_ids, top_k)

    # Measure
    timings = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        strategy_fn(seed_ids, top_k)
        t1 = time.perf_counter()
        timings.append((t1 - t0) * 1000.0)  # ms

    timings_arr = np.array(timings)

    return {
        "p50_ms": float(np.percentile(timings_arr, 50)),
        "p95_ms": float(np.percentile(timings_arr, 95)),
        "mean_ms": float(np.mean(timings_arr)),
        "min_ms": float(np.min(timings_arr)),
        "max_ms": float(np.max(timings_arr)),
        "n_runs": n_runs,
    }


def _get_rss_mb() -> float:
    """Get current process RSS in MB (Linux)."""
    try:
        with open(f"/proc/{os.getpid()}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024.0  # kB to MB
    except (FileNotFoundError, ValueError):
        pass

    # Fallback: resource module
    try:
        import resource
        return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0  # kB to MB
    except ImportError:
        return 0.0


def measure_memory(
    setup_and_run: Callable,
    n_gc_cycles: int = 3,
) -> dict:
    """Measure peak RSS delta during strategy execution.

    Runs GC before and after to isolate the strategy's memory footprint.
    This measures the DELTA in RSS, not absolute memory -- it captures
    what the strategy adds on top of the baseline.

    Args:
        setup_and_run: Callable that performs the strategy's work.
            Should include any data loading the strategy needs.
        n_gc_cycles: GC collection cycles before measurement.

    Returns:
        {"peak_rss_delta_mb": float, "baseline_rss_mb": float,
         "final_rss_mb": float}
    """
    # Force GC and measure baseline
    for _ in range(n_gc_cycles):
        gc.collect()

    baseline_rss = _get_rss_mb()

    # Run the strategy
    setup_and_run()

    final_rss = _get_rss_mb()

    return {
        "peak_rss_delta_mb": round(final_rss - baseline_rss, 2),
        "baseline_rss_mb": round(baseline_rss, 2),
        "final_rss_mb": round(final_rss, 2),
    }


def measure_setup_time(
    setup_fn: Callable,
    n_runs: int = 3,
) -> dict:
    """Measure one-time setup cost (index building, model loading, etc.).

    Args:
        setup_fn: Callable that performs the setup work. Called n_runs times.
        n_runs: How many times to measure (setup is often variable).

    Returns:
        {"mean_s": float, "min_s": float, "max_s": float, "n_runs": int}
    """
    timings = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        setup_fn()
        t1 = time.perf_counter()
        timings.append(t1 - t0)

    timings_arr = np.array(timings)

    return {
        "mean_s": float(np.mean(timings_arr)),
        "min_s": float(np.min(timings_arr)),
        "max_s": float(np.max(timings_arr)),
        "n_runs": n_runs,
    }


def measure_storage(file_paths: list[str]) -> dict:
    """Measure storage footprint of strategy's persisted data.

    Args:
        file_paths: Paths to files the strategy needs on disk.

    Returns:
        {"total_mb": float, "per_file": {path: size_mb}}
    """
    per_file = {}
    total = 0.0

    for path in file_paths:
        try:
            size_bytes = os.path.getsize(path)
            size_mb = size_bytes / (1024 * 1024)
            per_file[path] = round(size_mb, 2)
            total += size_mb
        except OSError:
            per_file[path] = None

    return {
        "total_mb": round(total, 2),
        "per_file": per_file,
    }


def measure_incremental_update(
    update_fn: Callable,
    n_papers: int = 10,
    n_runs: int = 10,
) -> dict:
    """Measure cost to incorporate new papers incrementally.

    Args:
        update_fn: Callable that simulates adding one paper.
            Called n_papers * n_runs times total.
        n_papers: Papers per batch.
        n_runs: Batches to measure.

    Returns:
        {"mean_per_paper_ms": float, "total_batch_ms": float}
    """
    timings = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        for _ in range(n_papers):
            update_fn()
        t1 = time.perf_counter()
        timings.append((t1 - t0) * 1000.0 / n_papers)  # ms per paper

    timings_arr = np.array(timings)

    return {
        "mean_per_paper_ms": float(np.mean(timings_arr)),
        "p95_per_paper_ms": float(np.percentile(timings_arr, 95)),
        "total_batch_ms": float(np.mean(timings_arr) * n_papers),
        "n_runs": n_runs,
    }
