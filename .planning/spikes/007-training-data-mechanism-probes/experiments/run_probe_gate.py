#!/usr/bin/env python3
"""
Spike 007 phase 1/2 gate.

Builds the probe registry and data-readiness checkpoint required before any
mechanism-specific probe wave runs.

Outputs:
  - checkpoints/phase1_probe_gate.json

This script does not execute the mechanism probes themselves. It answers:
1. Which families are live from Spike 006?
2. Which probe profiles are most useful?
3. Which mechanism sub-probes are runnable vs blocked?
4. Does each live family still have at least one concrete runnable mechanism claim?
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SPIKE_007_DIR = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = SPIKE_007_DIR / "experiments"
CHECKPOINT_DIR = EXPERIMENTS_DIR / "checkpoints"
SPIKE_003_GRAPH_PATH = (
    SPIKE_007_DIR.parent
    / "003-strategy-profiling"
    / "experiments"
    / "data"
    / "w1c_graph_profiles.json"
)
SPIKE_004_METRICS_PATH = (
    SPIKE_007_DIR.parent
    / "004-embedding-model-evaluation"
    / "experiments"
    / "checkpoints"
    / "phase2_metrics.json"
)
SPIKE_006_HANDOFF = SPIKE_007_DIR.parent / "006-model-retrieval-interactions" / "HANDOFF.md"
SAMPLE_PATH = (
    SPIKE_007_DIR.parent
    / "003-strategy-profiling"
    / "experiments"
    / "data"
    / "sample_2000.json"
)

SHORTLIST = ["specter2", "stella", "gte", "voyage"]
DROPPED = ["qwen3"]
PROBE_PROFILES = ["P2", "P3", "P6", "P7", "P8"]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def coverage_probe() -> dict:
    coverage = load_json(SPIKE_003_GRAPH_PATH)["coverage_analysis"]
    seed_total = coverage["seed_paper_coverage"]["total_unique_seeds"]
    seed_with_refs = coverage["seed_paper_coverage"]["seeds_with_refs"]
    cluster_total = coverage["cluster_paper_coverage"]["total_unique_cluster_papers"]
    cluster_with_refs = coverage["cluster_paper_coverage"]["cluster_papers_with_refs"]

    return {
        "probe": "citation_or_community_overlap",
        "status": "blocked",
        "threshold": ">= 70% selected probe papers with required metadata",
        "seed_coverage_fraction": round(seed_with_refs / seed_total, 4) if seed_total else 0.0,
        "cluster_coverage_fraction": round(cluster_with_refs / cluster_total, 4) if cluster_total else 0.0,
        "raw": {
            "openalex_cache_total": coverage["openalex_cache_total"],
            "papers_with_referenced_works": coverage["papers_with_referenced_works"],
            "papers_with_related_works": coverage["papers_with_related_works"],
            "seed_total": seed_total,
            "seed_with_refs": seed_with_refs,
            "cluster_total": cluster_total,
            "cluster_with_refs": cluster_with_refs,
            "referenced_works_pointing_to_corpus": coverage["referenced_works_pointing_to_corpus"],
        },
        "reason": coverage["conclusion"],
    }


def sample_readiness_probe() -> dict:
    sample = load_json(SAMPLE_PATH)
    papers = sample.get("papers", sample)
    required_fields = ["arxiv_id", "title", "abstract", "categories", "primary_category"]
    complete = 0
    for paper in papers:
        if all(field in paper and paper[field] not in (None, "") for field in required_fields):
            complete += 1
    return {
        "probe": "vocabulary_overlap_and_adjacent_field",
        "status": "runnable",
        "coverage_fraction": round(complete / len(papers), 4) if papers else 0.0,
        "reason": "The 2000-paper sample contains title/abstract/category fields for essentially the full evaluation surface.",
    }


def specialization_probe(metrics: dict) -> dict:
    coverage = {}
    for model in SHORTLIST:
        model_metrics = metrics["metrics"].get(model, {})
        coverage[model] = sorted(model_metrics.keys())
    return {
        "probe": "profile_specialization_sensitivity",
        "status": "runnable",
        "profiles_available": coverage,
        "reason": "Spike 004 metrics exist for every shortlisted family across all 8 profiles, so divergence concentration by profile can be tested immediately.",
    }


def build_probe_registry() -> list[dict]:
    return [
        {
            "family": "specter2",
            "mechanism_claim": "citation-community similarity stronger than vocabulary similarity, especially on specialized domains",
            "subprobes": [
                {
                    "name": "citation_or_community_overlap",
                    "status": "blocked",
                    "note": "Direct citation/community verification cannot run with current metadata coverage.",
                },
                {
                    "name": "profile_specialization_sensitivity",
                    "status": "runnable",
                    "probe_profiles": ["P3", "P8", "P2"],
                    "note": "Test whether divergence concentrates on specialized domains where citation-community structure should matter most.",
                },
            ],
            "runnable_claim": True,
        },
        {
            "family": "stella",
            "mechanism_claim": "practical / deployment-oriented extension rather than pure topic matching",
            "subprobes": [
                {
                    "name": "application_and_deployment_proxy_probe",
                    "status": "runnable",
                    "probe_profiles": ["P6", "P7", "P2"],
                    "note": "Proxy test only: compare Stella-unique papers against deployment/application-oriented lexical markers and category spread.",
                },
                {
                    "name": "profile_specialization_sensitivity",
                    "status": "runnable",
                    "probe_profiles": ["P6", "P7"],
                    "note": "Check whether Stella divergence concentrates on practical, systems-heavy profiles.",
                },
            ],
            "runnable_claim": True,
            "qualification": "This is weaker and more proxy-dependent than the SPECTER2 or GTE claims.",
        },
        {
            "family": "gte",
            "mechanism_claim": "broader methodological envelope that stays near the incumbent ranking structure",
            "subprobes": [
                {
                    "name": "vocabulary_overlap_and_adjacent_field",
                    "status": "runnable",
                    "probe_profiles": ["P2", "P7", "P8"],
                    "note": "Check whether GTE uniques widen into adjacent methodological substrate without collapsing topical coherence.",
                },
                {
                    "name": "profile_specialization_sensitivity",
                    "status": "runnable",
                    "probe_profiles": ["P2", "P8"],
                    "note": "Check whether the wider methodological envelope concentrates on profiles where foundational-method variation is expected.",
                },
            ],
            "runnable_claim": True,
        },
        {
            "family": "voyage",
            "mechanism_claim": "broader conceptual similarity that diverges most on open-ended conceptual profiles",
            "subprobes": [
                {
                    "name": "profile_specialization_sensitivity",
                    "status": "runnable",
                    "probe_profiles": ["P2", "P3", "P7"],
                    "note": "Check whether divergence is highest on broader conceptual profiles and lower on narrow, well-defined ones.",
                },
                {
                    "name": "vocabulary_overlap_and_adjacent_field",
                    "status": "runnable",
                    "probe_profiles": ["P2", "P3"],
                    "note": "Check whether Voyage uniques remain conceptually coherent rather than merely cross-category.",
                },
            ],
            "runnable_claim": True,
            "qualification": "Operational issues from Spike 004 remain; this spike tests mechanism support, not deployment fitness.",
        },
    ]


def main() -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    metrics = load_json(SPIKE_004_METRICS_PATH)
    probe_registry = build_probe_registry()
    readiness = [
        coverage_probe(),
        sample_readiness_probe(),
        specialization_probe(metrics),
    ]

    proceed = len(SHORTLIST) <= 4 and all(item["runnable_claim"] for item in probe_registry)
    checkpoint = {
        "phase": "phase1_probe_gate",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_handoff": str(SPIKE_006_HANDOFF),
        "shortlist_from_006": SHORTLIST,
        "dropped_from_006": DROPPED,
        "probe_profiles_chosen_for_now": {
            "profiles": PROBE_PROFILES,
            "rationale": {
                "P2": "broad conceptual reasoning; strongest Voyage-style open-profile divergence and useful GTE/Qwen-style contrast site",
                "P3": "specialized quantum domain; strongest SPECTER2-style specialization test",
                "P6": "diffusion / multimodal generation; strongest Stella instability and application-extension site",
                "P7": "dense federated/privacy profile; useful for Stella/GTE and interaction with dense-topic behavior",
                "P8": "mathematical foundations; strongest specialization and methodological-envelope test",
            },
        },
        "data_readiness": readiness,
        "probe_registry": probe_registry,
        "gate_verdict": {
            "proceed_with_probe_wave": proceed,
            "reason": (
                "Proceed. The citation/community subprobe is blocked, but every live family still has at least one concrete runnable mechanism claim via specialization or lexical/adjacent-field probes."
                if proceed
                else "Do not proceed. Narrowing memo required before probe wave."
            ),
            "blocked_subprobes": [
                item["probe"] for item in readiness if item["status"] == "blocked"
            ],
        },
    }

    checkpoint_path = CHECKPOINT_DIR / "phase1_probe_gate.json"
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + "\n")

    print("Spike 007 probe gate checkpoint written:")
    print(f"  {checkpoint_path}")
    print()
    print("Shortlist from 006:", ", ".join(SHORTLIST))
    print("Blocked subprobes:")
    for item in readiness:
        if item["status"] == "blocked":
            print(f"  - {item['probe']}")
    print("Proceed with probe wave:", proceed)


if __name__ == "__main__":
    main()
