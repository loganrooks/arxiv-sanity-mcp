---
type: index
created: 2026-04-26
purpose: |
  Directory index for .planning/deliberations/. Lists each deliberation with
  date, title, status, one-line summary, and any ADR or phase plan it produced.
  Added per governance audit synthesis G-S3 (SV F3 finding: directory unindexed).
note: |
  Status markings use the vocabulary: active, produced-ADR, superseded,
  exploratory, concluded, policy-adopted. Where status is ambiguous from
  frontmatter or content, marked "status: unknown — verify".
---

# Deliberations Index

*Note: prior PROJECT.md designated `local-gap-propagation-and-signal-interpretation.md` as a "primary active reference"; the 2026-04-26 PROJECT.md refresh dropped that designation since the deliberation is about GSDR signal-system discipline (an open methodology question), not about current v0.2 milestone work. The file remains active per its own status (open, undated section below).*

## Dated deliberations (2026-04-25 session)

These seven files were produced in the 2026-04-25 multi-lens redirection and spike-program critique session.

| File | Date | Status | Summary | Produced |
|---|---|---|---|---|
| [2026-04-25-long-arc-and-multi-lens-redirection.md](2026-04-25-long-arc-and-multi-lens-redirection.md) | 2026-04-25 | **produced-ADR** (decided — implementation open) | The central redirection deliberation: surfaced that the 005-008 spike program had drifted toward tournament-narrowing in violation of ADR-0001; committed v0.2 to multi-lens substrate; enumerated roadmap options | ADR-0005; v0.2 MILESTONE.md; LONG-ARC.md |
| [2026-04-25-audience-reframe-arxiv-ai.md](2026-04-25-audience-reframe-arxiv-ai.md) | 2026-04-25 | **concluded** (correction accepted; followed through) | Corrected over-focus on philosophy register → AI-research audience; reframe accepted and propagated to VISION.md | VISION.md audience correction |
| [2026-04-25-load-bearing-assumptions-audit.md](2026-04-25-load-bearing-assumptions-audit.md) | 2026-04-25 | **policy-adopted** (discipline articulated; reusable) | Before adopting remedies, audit the load-bearing assumptions underneath them; worked example on operationalization slate | Reusable discipline pattern |
| [2026-04-25-mediation-vs-position-taking.md](2026-04-25-mediation-vs-position-taking.md) | 2026-04-25 | **policy-adopted** (principle articulated; partial follow-through) | Multi-perspective mediation is insufficient; must take a position and defend it; pattern required re-prompting twice in same session | Writing-posture discipline |
| [2026-04-25-pass-fail-vs-nuance-of-differences.md](2026-04-25-pass-fail-vs-nuance-of-differences.md) | 2026-04-25 | **policy-adopted** (principle articulated; pattern recurring) | Don't reduce audit findings to survive/retract verdicts; ask what nuances of differences demand; pattern recurred in subsequent prose | Evaluation-posture discipline |
| [2026-04-25-pressure-artifacts-before-remedy.md](2026-04-25-pressure-artifacts-before-remedy.md) | 2026-04-25 | **policy-adopted** (workflow articulated; reusable) | Pressure the artifacts and reviews before deciding how to proceed; not the findings themselves but the artifact-reading that grounds them | Reusable workflow discipline; feeds METHODOLOGY.md |
| [2026-04-25-recording-deliberations-extensively.md](2026-04-25-recording-deliberations-extensively.md) | 2026-04-25 | **policy-adopted** (self-referential; being acted on) | Meta-deliberation: the decision to record deliberations as first-class artifacts; motivated by traces-over-erasure orientation | Documentation policy; this INDEX is downstream |

---

## Undated deliberations (pre-2026-04-25)

These files use the template format without `---` frontmatter; dates are from inline `**Date:**` field.

| File | Date | Status | Summary | Produced |
|---|---|---|---|---|
| [local-gap-propagation-and-signal-interpretation.md](local-gap-propagation-and-signal-interpretation.md) | 2026-03-31 | **active** (open) | When a project detects a local workflow gap, how should the signal be interpreted and propagated upstream without mistaking a context-bound symptom for a universal defect? Scoped to GSDR signal-system / spike-review-workflow discipline (NOT directly about long-horizon planning content / gsd-2 uplift) | No ADR produced; open |
| [sequential-narrowing-anti-regret-and-spike-inference-limits.md](sequential-narrowing-anti-regret-and-spike-inference-limits.md) | 2026-04-16 | **superseded** (open at write-time; recommendation deferred pending pressure pass; subsequently addressed by multi-lens redirection) | Critique of 005-008 spike suite's narrowing logic: is the sequence genuinely anti-regret and challenge-seeking, or does it prematurely close options? | Pressure-pass discipline; contributed to 2026-04-25 redirection deliberation |
| [comparative-characterization-and-nonadditive-evaluation-praxis.md](comparative-characterization-and-nonadditive-evaluation-praxis.md) | 2026-03-21 | **exploratory** (open) | How to operationalize rigor and repeatability in spike evaluation without collapsing to winner-picking benchmark or additive spike sequence; cites van Fraassen, Mayo, Cartwright | No ADR produced; open |
| [deployment-portability.md](deployment-portability.md) | 2026-03-14 | **exploratory** (open; blocked on spike completion) | After Phase 10, deployment-readiness surfaced as a gap: backend flexibility, deployment tiers, PyPI distribution, arxiv-sanity-lite architecture comparison | Feeds v0.1.x release scope; partially addressed by Phase 9/10 |
| [v2-literature-review-features.md](v2-literature-review-features.md) | 2026-03-13 | **exploratory** (open) | Which Ecosystem Commentary §5 literature review feature priorities belong in v2? Triggered by v1 milestone audit | Feeds REQUIREMENTS.md v2 section, ROADMAP.md |
| [spike-epistemic-rigor-and-framework-reflexivity.md](spike-epistemic-rigor-and-framework-reflexivity.md) **(symlink → `~/workspace/projects/get-shit-done-reflect/.planning/deliberations/`)** | 2026-03-20 | **exploratory** (open; note: scoped to GSD Reflect framework, not arxiv-sanity-mcp project-specific) | Spike design rigor and framework reflexivity; evidence from arxiv-sanity-mcp spike artifacts; canonical location is GSD Reflect repo | No arxiv-sanity-mcp ADR; framework-level deliberation |

---

## Reviews subdirectory

| File | Date | Status | Summary |
|---|---|---|---|
| [reviews/2026-04-16-sequential-narrowing-deliberation-review.md](reviews/2026-04-16-sequential-narrowing-deliberation-review.md) | 2026-04-16 | **concluded** (critique, unincorporated at write-time; subsequently superseded by multi-lens redirection) | Independent Opus 4.7 read of the sequential-narrowing deliberation; verdict: framing mostly right, conclusion directionally right but procedurally understrength |

---

*Index created 2026-04-26 per governance audit synthesis G-S3. If new deliberations are added, append to the appropriate section. Status should be updated when a deliberation produces an ADR, is superseded, or is closed.*
