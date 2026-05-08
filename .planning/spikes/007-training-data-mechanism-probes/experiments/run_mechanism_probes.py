#!/usr/bin/env python3
"""
Spike 007 phase 3 quantitative probe wave.

Runs the mechanism probes that survived the phase 1/2 gate:
  - profile-specialization sensitivity
  - vocabulary/category proxy surfaces for representative profiles

Outputs:
  - checkpoints/phase2_mechanism_probes.json
  - review_inputs/phase2_probe_cases.json

This script does not close Spike 007 on its own. It narrows the qualitative
review surface and records the bounded quantitative evidence that later
artifacts must cite.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SPIKE_007_DIR = Path(__file__).resolve().parent.parent
EXPERIMENTS_DIR = SPIKE_007_DIR / "experiments"
CHECKPOINT_DIR = EXPERIMENTS_DIR / "checkpoints"
REVIEW_INPUT_DIR = EXPERIMENTS_DIR / "review_inputs"
SPIKE_004_REVIEW_INPUTS = (
    SPIKE_007_DIR.parent / "004-embedding-model-evaluation" / "experiments" / "review_inputs"
)
SPIKE_004_METRICS = (
    SPIKE_007_DIR.parent
    / "004-embedding-model-evaluation"
    / "experiments"
    / "checkpoints"
    / "phase2_metrics.json"
)
SPIKE_006_QUANT = (
    SPIKE_007_DIR.parent
    / "006-model-retrieval-interactions"
    / "experiments"
    / "checkpoints"
    / "phase1_quantitative.json"
)
SPIKE_007_GATE = CHECKPOINT_DIR / "phase1_probe_gate.json"

TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9\\-]{2,}")
STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "using", "via",
    "under", "over", "between", "their", "they", "have", "has", "had", "are",
    "was", "were", "will", "can", "our", "not", "but", "more", "than", "how",
    "why", "what", "which", "when", "where", "while", "within", "without",
    "about", "across", "through", "toward", "towards", "also", "these", "those",
    "them", "its", "such", "both", "only", "each", "other", "new", "based",
    "models", "model", "learning", "paper", "papers", "study", "work",
}

FAMILY_CONFIG = {
    "specter2": {
        "claim": "specialized scientific / citation-community style relatedness is strongest on narrow technical domains",
        "target_profiles": ["P3", "P8"],
        "control_profiles": ["P1", "P4", "P5"],
        "review_profiles": ["P3", "P8", "P2"],
        "contradiction_profile": "P2",
        "claim_strength_note": "direct citation/community verification remains blocked, so support can only be partial",
    },
    "stella": {
        "claim": "practical / deployment-oriented extension rather than pure topic matching",
        "target_profiles": ["P6", "P7"],
        "control_profiles": ["P1", "P4", "P5"],
        "review_profiles": ["P6", "P7", "P2"],
        "contradiction_profile": "P2",
        "claim_strength_note": "this is the most proxy-dependent claim in the shortlist",
    },
    "gte": {
        "claim": "broader methodological envelope that stays near the incumbent ranking structure",
        "target_profiles": ["P2", "P8"],
        "control_profiles": ["P1", "P4", "P5"],
        "review_profiles": ["P8", "P2", "P7"],
        "contradiction_profile": "P2",
        "claim_strength_note": "support should favor controlled widening rather than raw divergence",
    },
    "voyage": {
        "claim": "broader conceptual similarity that diverges most on open-ended conceptual profiles",
        "target_profiles": ["P2", "P7"],
        "control_profiles": ["P1", "P4", "P5"],
        "review_profiles": ["P2", "P1", "P3"],
        "contradiction_profile": "P1",
        "claim_strength_note": "operational caveats remain outside the mechanism question",
    },
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def tokenize(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_PATTERN.findall(text)
        if token.lower() not in STOPWORDS
    ]


def vectorize(text: str) -> tuple[Counter, float]:
    counts = Counter(tokenize(text))
    norm = math.sqrt(sum(value * value for value in counts.values()))
    return counts, norm


def cosine_similarity(vec_a: Counter, norm_a: float, vec_b: Counter, norm_b: float) -> float:
    if not norm_a or not norm_b:
        return 0.0
    if len(vec_a) > len(vec_b):
        vec_a, vec_b = vec_b, vec_a
    dot = sum(value * vec_b.get(key, 0) for key, value in vec_a.items())
    return dot / (norm_a * norm_b)


def load_profile_surface(model_key: str, profile_id: str) -> dict:
    matches = sorted(SPIKE_004_REVIEW_INPUTS.glob(f"{model_key}_{profile_id}*.json"))
    if not matches:
        raise FileNotFoundError(f"No review input found for {model_key=} {profile_id=}")

    path = matches[0]
    payload = load_json(path)
    if payload["type"] == "characterization":
        model_papers = payload["model_top20"]
        minilm_papers = payload["minilm_top20"]
    else:
        key = payload["_key"]
        if key["Model A"] == model_key:
            model_papers = payload["model_a_papers"]
            minilm_papers = payload["model_b_papers"]
        else:
            model_papers = payload["model_b_papers"]
            minilm_papers = payload["model_a_papers"]

    seed_ids = {paper["arxiv_id"] for paper in payload["seeds"]}
    model_ids = {paper["arxiv_id"] for paper in model_papers}
    minilm_ids = {paper["arxiv_id"] for paper in minilm_papers}

    model_unique_nonseed = [
        paper for paper in model_papers
        if paper["arxiv_id"] not in minilm_ids and paper["arxiv_id"] not in seed_ids
    ]
    minilm_unique_nonseed = [
        paper for paper in minilm_papers
        if paper["arxiv_id"] not in model_ids and paper["arxiv_id"] not in seed_ids
    ]

    seed_text = " ".join(
        (paper.get("title", "") + " " + paper.get("abstract", "")).strip()
        for paper in payload["seeds"]
    )
    seed_vec, seed_norm = vectorize(seed_text)
    seed_categories = {paper.get("category") for paper in payload["seeds"] if paper.get("category")}

    def avg_seed_overlap(papers: list[dict]) -> float | None:
        if not papers:
            return None
        overlaps = []
        for paper in papers:
            paper_vec, paper_norm = vectorize(
                (paper.get("title", "") + " " + paper.get("abstract", "")).strip()
            )
            overlaps.append(cosine_similarity(paper_vec, paper_norm, seed_vec, seed_norm))
        return round(mean(overlaps), 4)

    def category_match_rate(papers: list[dict]) -> float | None:
        if not papers:
            return None
        matches = sum(1 for paper in papers if paper.get("category") in seed_categories)
        return round(matches / len(papers), 4)

    return {
        "review_input_path": str(path),
        "review_input_type": payload["type"],
        "profile_name": payload["profile_name"],
        "seed_count": len(payload["seeds"]),
        "seed_categories": sorted(seed_categories),
        "model_unique_nonseed_count": len(model_unique_nonseed),
        "minilm_unique_nonseed_count": len(minilm_unique_nonseed),
        "avg_seed_token_overlap_model_unique": avg_seed_overlap(model_unique_nonseed),
        "avg_seed_token_overlap_minilm_unique": avg_seed_overlap(minilm_unique_nonseed),
        "seed_category_match_rate_model_unique": category_match_rate(model_unique_nonseed),
        "seed_category_match_rate_minilm_unique": category_match_rate(minilm_unique_nonseed),
        "representative_model_unique_titles": [
            paper["title"] for paper in model_unique_nonseed[:5]
        ],
        "representative_minilm_unique_titles": [
            paper["title"] for paper in minilm_unique_nonseed[:5]
        ],
    }


def specialization_probe(model_key: str, metrics: dict, targets: list[str], controls: list[str]) -> dict:
    model_metrics = metrics["metrics"][model_key]
    all_profiles = sorted(model_metrics.keys())
    non_targets = [profile for profile in all_profiles if profile not in targets]

    target_jaccards = [
        model_metrics[profile]["jaccard_vs_minilm"]["jaccard_at_20"] for profile in targets
    ]
    target_unique = [model_metrics[profile]["n_truly_unique"] for profile in targets]
    target_taus = [
        model_metrics[profile]["rank_correlation_vs_minilm"]["kendall_tau"] for profile in targets
    ]
    control_jaccards = [
        model_metrics[profile]["jaccard_vs_minilm"]["jaccard_at_20"] for profile in controls
    ]
    control_unique = [model_metrics[profile]["n_truly_unique"] for profile in controls]
    non_target_jaccards = [
        model_metrics[profile]["jaccard_vs_minilm"]["jaccard_at_20"] for profile in non_targets
    ]
    non_target_unique = [
        model_metrics[profile]["n_truly_unique"] for profile in non_targets
    ]

    jaccard_gap = mean(non_target_jaccards) - mean(target_jaccards)
    unique_lift = mean(target_unique) - mean(non_target_unique)

    if jaccard_gap >= 0.15 and unique_lift >= 2.0:
        signal_strength = "strong"
    elif jaccard_gap >= 0.05 and unique_lift >= 1.0:
        signal_strength = "moderate"
    else:
        signal_strength = "weak"

    return {
        "targets": targets,
        "controls": controls,
        "per_target_profile": {
            profile: {
                "jaccard_at_20": round(model_metrics[profile]["jaccard_vs_minilm"]["jaccard_at_20"], 4),
                "n_truly_unique": int(model_metrics[profile]["n_truly_unique"]),
                "kendall_tau_vs_minilm": round(
                    model_metrics[profile]["rank_correlation_vs_minilm"]["kendall_tau"], 4,
                ),
            }
            for profile in targets
        },
        "target_mean_jaccard_at_20": round(mean(target_jaccards), 4),
        "non_target_mean_jaccard_at_20": round(mean(non_target_jaccards), 4),
        "control_mean_jaccard_at_20": round(mean(control_jaccards), 4),
        "target_mean_truly_unique": round(mean(target_unique), 4),
        "non_target_mean_truly_unique": round(mean(non_target_unique), 4),
        "control_mean_truly_unique": round(mean(control_unique), 4),
        "target_mean_tau": round(mean(target_taus), 4),
        "jaccard_gap_vs_non_targets": round(jaccard_gap, 4),
        "truly_unique_lift_vs_non_targets": round(unique_lift, 4),
        "signal_strength": signal_strength,
    }


def interaction_summary(model_key: str, phase1_quant: dict) -> dict:
    saved = phase1_quant["results"]["minilm_saved"]["interaction_summaries"][model_key]
    category = phase1_quant["results"]["category_lexical"]["interaction_summaries"][model_key]
    return {
        "mean_knn_union_delta_vs_tfidf_at_20": round(
            mean([
                saved["mean_knn_union_delta_vs_tfidf_at_20"],
                category["mean_knn_union_delta_vs_tfidf_at_20"],
            ]),
            4,
        ),
        "mean_centroid_union_delta_vs_tfidf_at_20": round(
            mean([
                saved["mean_centroid_union_delta_vs_tfidf_at_20"],
                category["mean_centroid_union_delta_vs_tfidf_at_20"],
            ]),
            4,
        ),
        "mean_method_jaccard_centroid_vs_knn_at_20": round(
            mean([
                saved["mean_jaccard_centroid_vs_knn_at_20"],
                category["mean_jaccard_centroid_vs_knn_at_20"],
            ]),
            4,
        ),
        "saved_family_read": saved["provisional_interaction_read"],
        "category_family_read": category["provisional_interaction_read"],
    }


def main() -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_INPUT_DIR.mkdir(parents=True, exist_ok=True)

    gate = load_json(SPIKE_007_GATE)
    metrics = load_json(SPIKE_004_METRICS)
    phase1_quant = load_json(SPIKE_006_QUANT)

    family_results = {}
    review_cases = []

    for model_key, config in FAMILY_CONFIG.items():
        surfaces = {
            profile_id: load_profile_surface(model_key, profile_id)
            for profile_id in config["review_profiles"]
        }
        spec_probe = specialization_probe(
            model_key,
            metrics,
            config["target_profiles"],
            config["control_profiles"],
        )
        interaction = interaction_summary(model_key, phase1_quant)
        mean_tau = round(
            mean(
                [
                    metrics["metrics"][model_key][profile]["rank_correlation_vs_minilm"]["kendall_tau"]
                    for profile in metrics["metrics"][model_key]
                ]
            ),
            4,
        )

        family_results[model_key] = {
            "claim": config["claim"],
            "claim_strength_note": config["claim_strength_note"],
            "specialization_probe": spec_probe,
            "profile_surfaces": surfaces,
            "interaction_context_from_006": interaction,
            "mean_tau_vs_minilm_from_004": mean_tau,
            "structural_distinctness_proxy": round(1.0 - mean_tau, 4),
        }

        if spec_probe["signal_strength"] == "strong":
            support_profile = min(
                config["target_profiles"],
                key=lambda profile: metrics["metrics"][model_key][profile]["jaccard_vs_minilm"]["jaccard_at_20"],
            )
        else:
            support_profile = config["review_profiles"][0]

        contradiction_profile = config.get("contradiction_profile")
        if contradiction_profile is None:
            contradiction_profile = max(
                config["review_profiles"],
                key=lambda profile: (
                    surfaces[profile]["avg_seed_token_overlap_model_unique"] or 0.0,
                    surfaces[profile]["seed_category_match_rate_model_unique"] or 0.0,
                ),
            )

        review_cases.append(
            {
                "family": model_key,
                "claim": config["claim"],
                "support_case_profile": support_profile,
                "support_case_surface": surfaces[support_profile],
                "contradiction_case_profile": contradiction_profile,
                "contradiction_case_surface": surfaces[contradiction_profile],
                "specialization_probe": spec_probe,
                "interaction_context_from_006": interaction,
            }
        )

    checkpoint = {
        "phase": "phase2_mechanism_probes",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source_gate": str(SPIKE_007_GATE),
        "source_metrics": str(SPIKE_004_METRICS),
        "source_interaction_checkpoint": str(SPIKE_006_QUANT),
        "blocked_subprobes": gate["gate_verdict"]["blocked_subprobes"],
        "family_results": family_results,
    }

    checkpoint_path = CHECKPOINT_DIR / "phase2_mechanism_probes.json"
    review_input_path = REVIEW_INPUT_DIR / "phase2_probe_cases.json"
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2) + "\n")
    review_input_path.write_text(json.dumps(review_cases, indent=2) + "\n")

    print("Spike 007 mechanism probe outputs written:")
    print(f"  {checkpoint_path}")
    print(f"  {review_input_path}")
    print()
    for model_key, result in family_results.items():
        probe = result["specialization_probe"]
        print(
            f"{model_key}: signal={probe['signal_strength']} "
            f"jaccard_gap={probe['jaccard_gap_vs_non_targets']:.4f} "
            f"unique_lift={probe['truly_unique_lift_vs_non_targets']:.4f}",
        )


if __name__ == "__main__":
    main()
