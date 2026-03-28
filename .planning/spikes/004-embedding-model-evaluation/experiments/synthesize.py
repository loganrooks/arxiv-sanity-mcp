#!/usr/bin/env python3
"""
Spike 004 Phase 4: Synthesis.

Enforces pre-synthesis checklist, loads all phase results, and generates
a structured synthesis template for the FINDINGS.md and DECISION.md.

This script does NOT auto-generate conclusions — it assembles the evidence
and produces a template that must be completed with interpretive judgment.

Usage:
  conda activate ml-dev
  python synthesize.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SPIKE_004_DIR = Path(__file__).resolve().parent.parent
CHECKPOINT_DIR = SPIKE_004_DIR / "experiments" / "checkpoints"
REVIEW_DIR = SPIKE_004_DIR / "experiments" / "reviews"


# ---------------------------------------------------------------------------
# Pre-synthesis checklist enforcement
# ---------------------------------------------------------------------------

REQUIRED_CHECKPOINTS = [
    ("phase1_embeddings.json", "All models embedded with provenance"),
    ("phase1_validation.json", "Sample validation gate (go/no-go)"),
    ("phase2_metrics.json", "Quantitative metrics for all models"),
    ("phase2_classification.json", "Branch classification per model"),
    ("phase3_reviews.json", "Qualitative reviews complete"),
]


def verify_checklist() -> bool:
    """Enforce pre-synthesis checklist per PROTOCOL.md Section 5."""
    print("=== Pre-Synthesis Checklist ===\n")
    all_pass = True

    for filename, description in REQUIRED_CHECKPOINTS:
        path = CHECKPOINT_DIR / filename
        if path.exists():
            print(f"  [x] {description}")
        else:
            print(f"  [ ] {description} — MISSING: {filename}")
            all_pass = False

    if not all_pass:
        print("\nCHECKLIST FAILED. Complete all phases before synthesis.")
        return False

    # Additional check: validation verdict
    with open(CHECKPOINT_DIR / "phase1_validation.json") as f:
        validation = json.load(f)
    verdict = validation.get("verdict", "UNKNOWN")
    if verdict == "NO_GO":
        print(f"\n  WARNING: Sample validation was NO_GO")
        print("  Synthesis should document this limitation prominently.")

    print(f"\n  Sample validation verdict: {verdict}")
    print("\nChecklist PASSED.\n")
    return True


# ---------------------------------------------------------------------------
# Evidence assembly
# ---------------------------------------------------------------------------

def load_all_evidence() -> dict:
    """Load all phase results into a single evidence dict."""
    evidence = {}

    for filename, _ in REQUIRED_CHECKPOINTS:
        path = CHECKPOINT_DIR / filename
        with open(path) as f:
            evidence[filename.replace(".json", "")] = json.load(f)

    # Load review content
    reviews = {}
    if REVIEW_DIR.exists():
        for review_file in sorted(REVIEW_DIR.glob("*_review.md")):
            reviews[review_file.stem] = review_file.read_text()
    evidence["reviews"] = reviews

    return evidence


def generate_synthesis_template(evidence: dict) -> str:
    """Generate FINDINGS.md template with evidence summaries."""
    classifications = evidence.get("phase2_classification", {}).get("classifications", {})
    metrics = evidence.get("phase2_metrics", {}).get("metrics", {})
    validation = evidence.get("phase1_validation", {})
    embeddings = evidence.get("phase1_embeddings", {})

    # Build model summary table
    model_rows = []
    for model_key, cls in classifications.items():
        model_info = embeddings.get("models", {}).get(model_key, {})
        dim = model_info.get("dimension", "?")
        time_s = model_info.get("total_time_s", model_info.get("embed_time_s", "?"))
        model_rows.append(
            f"| {model_key} | {dim} | {cls['classification']} | "
            f"{cls['min_jaccard_20']:.3f} | {cls['mean_jaccard_20']:.3f} | {time_s}s |"
        )

    model_table = "\n".join(model_rows)

    # Build per-model sections
    model_sections = []
    for model_key, cls in classifications.items():
        model_metrics = metrics.get(model_key, {})

        # Aggregate key metrics across profiles
        profile_summaries = []
        for pid, pm in sorted(model_metrics.items()):
            j20 = pm.get("jaccard_vs_minilm", {}).get("jaccard_at_20", "?")
            tau = pm.get("rank_correlation_vs_minilm", {}).get("kendall_tau", "?")
            cat_recall = pm.get("category_recall", {}).get("recall", "?")
            n_unique = pm.get("n_truly_unique", "?")
            j20_tfidf = pm.get("jaccard_vs_tfidf", {}).get("jaccard_at_20", "?")
            profile_summaries.append(
                f"| {pid} | {j20} | {tau} | {cat_recall} | {j20_tfidf} | {n_unique} |"
            )

        profile_table = "\n".join(profile_summaries)

        model_sections.append(f"""
### {model_key}

**Classification:** {cls['classification']}
{"**Upgraded:** " + ", ".join(cls.get("upgrade_reasons", [])) if cls.get("upgraded") else ""}

| Profile | J@20 vs MiniLM | Tau | Cat Recall | J@20 vs TF-IDF | Truly Unique |
|---------|---------------|-----|------------|----------------|-------------|
{profile_table}

#### Measurement confidence
[What the instruments detected — high confidence for well-executed measurements]

#### Interpretation
[What the measurements mean — medium confidence, depends on framework entanglements]

#### Extrapolation conditions
[Under what conditions these findings hold — lower confidence, domain-specific]

#### Qualitative review summary
[Summary of qualitative findings for this model — what kind of papers does it find that others don't?]
""")

    template = f"""---
spike: "004"
status: draft
date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
---

# Spike 004 Findings: Embedding Model Evaluation

## Scope and Conditions

These findings hold for:
- **Corpus**: 2000-paper sample from 19,252 arXiv papers (1% selectivity)
- **Domain**: CS/ML (77% of corpus), 130 categories represented
- **Profiles**: 8 interest profiles constructed from MiniLM BERTopic clusters
- **Assessment**: AI qualitative review (no human judges)
- **Sample validation**: {validation.get("verdict", "UNKNOWN")}

### Standing caveats
- Interest profiles are MiniLM-entangled (constructed from MiniLM BERTopic clusters)
- Sample validated primarily from MiniLM's perspective
- API models (Voyage) subject to provider-side drift — findings not reproducible at checkpoint level
- All qualitative judgments are AI-generated substitutes for researcher judgment

## Model Overview

| Model | Dim | Classification | Min J@20 | Mean J@20 | Embed Time |
|-------|-----|---------------|----------|-----------|------------|
{model_table}

## Pre-registered Predictions

| ID | Prediction | Result | Notes |
|----|-----------|--------|-------|
| P1 | Voyage J@20 > 0.717 (Spike 003) on larger sample | [CONFIRMED/FALSIFIED] | |
| P2 | At least one local model J@20 < 0.7 on 2+ profiles | [CONFIRMED/FALSIFIED] | |
| P3 | SPECTER2 redundancy holds across all 8 profiles | [CONFIRMED/FALSIFIED] | |
| P4 | Divergent models show qualitatively different paper types | [CONFIRMED/FALSIFIED] | |
| P5 | At least one model has better score separation than MiniLM | [CONFIRMED/FALSIFIED] | |
| P6 | No single model dominates all 8 profiles | [CONFIRMED/FALSIFIED] | |

## Per-Model Findings
{"".join(model_sections)}

## Cross-Model Analysis

### Signal axes identified
[Do the models cluster into groups that capture different kinds of relatedness?]

### TF-IDF comparison frame
[For models showing promise: do they find papers that BOTH MiniLM and TF-IDF miss?]
[Are any models better complements to MiniLM than TF-IDF?]
[Are any models better replacements for MiniLM?]

### Profile dependence
[Do model rankings vary by profile? Which profiles discriminate most between models?]

## Methodology Notes

### Anomalies encountered during execution
[Anything that didn't fit the design — deviations from protocol, unexpected results]

### Where this spike could not see
[Restate from DESIGN.md, updated with execution-time discoveries]

### What exceeded the design
[Per principle 20: note what happened that DESIGN.md couldn't hold]
"""

    return template


def generate_decision_template(evidence: dict) -> str:
    """Generate DECISION.md template."""
    return f"""---
spike: "004"
status: draft
date: {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
---

# Spike 004 Decision: Embedding Model Evaluation

## Decision-Readiness Classes (per PROTOCOL.md Section 6)

### Retain default (MiniLM + TF-IDF)
[Evidence for or against retaining the current provisional arrangement]

### Candidates: optional experimental view
[Models that merit being offered as an additional view, with evidence]

### Candidates: further investigation
[Models showing promise under conditions our methodology can't fully assess]

### Evidence insufficient
[Models where the spike cannot answer the question]

## Deferred Questions Updated

### From Spike 003
- "Do API embeddings add value?" → [Updated answer with evidence]
- "Would a different second view model be better than TF-IDF?" → [Updated answer]

## Architecture Implications

**Constraint:** Per Codex review, any architectural claim remains at most "Chosen for now"
unless evidence is overwhelming. This spike's evidence base (2000-paper CS/ML sample,
AI qualitative review, MiniLM-entangled profiles) cannot plausibly support "Settled" status
for architecture decisions.

### Current arrangement: MiniLM primary + TF-IDF secondary
[Should this change? Evidence and confidence level]

### View architecture
[Should additional views be offered? Under what conditions?]

## User Situation Considerations (Success Criterion 6)

| Model | API dependency | GPU required | Disk | Latency | Local-first compatible |
|-------|---------------|-------------|------|---------|----------------------|
[Fill from provenance data]

## Limitations of This Decision

[What this spike could not tell us, restated for decision context]
"""


def main():
    print("=" * 60)
    print("SPIKE 004 PHASE 4: SYNTHESIS")
    print("=" * 60)

    if not verify_checklist():
        sys.exit(1)

    evidence = load_all_evidence()

    # Generate templates
    findings = generate_synthesis_template(evidence)
    decision = generate_decision_template(evidence)

    findings_path = SPIKE_004_DIR / "FINDINGS.md"
    decision_path = SPIKE_004_DIR / "DECISION.md"

    findings_path.write_text(findings)
    decision_path.write_text(decision)

    print(f"Generated: {findings_path}")
    print(f"Generated: {decision_path}")
    print("\nThese are TEMPLATES with evidence pre-filled.")
    print("Complete the interpretation sections before finalizing.")

    # Write synthesis checkpoint
    checkpoint = {
        "phase": "phase4_synthesis",
        "status": "templates_generated",
        "findings_path": str(findings_path),
        "decision_path": str(decision_path),
        "evidence_summary": {
            "n_models_compared": len(evidence.get("phase2_classification", {}).get("classifications", {})),
            "n_reviews_completed": len(evidence.get("reviews", {})),
            "sample_validation": evidence.get("phase1_validation", {}).get("verdict", "?"),
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(CHECKPOINT_DIR / "phase4_synthesis.json", "w") as f:
        json.dump(checkpoint, f, indent=2)


if __name__ == "__main__":
    main()
