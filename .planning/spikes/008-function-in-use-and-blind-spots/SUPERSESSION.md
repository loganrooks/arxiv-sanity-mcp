---
type: spike-supersession
date: 2026-04-25
target: ./DESIGN.md
status: superseded — preserved as evidence, not executable
related:
  - ../../../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md
  - ../../deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md
  - ../../milestones/v0.2-MILESTONE.md
  - ../../audits/2026-04-25-phase-3-property-audit-opus.md
---

# Spike 008 — Supersession Rationale

## Why this spike was superseded

`008/DESIGN.md` was drafted (2026-03-30) under a tournament-narrowing frame: three configurations (`MiniLM + TF-IDF` incumbent, plus two carried challengers `SPECTER2` and `Voyage`) compared via task-based evaluation, with the winner shaping the v0.2 architecture commitment. That frame was committed before the methodology audit cycle of 2026-04-25 surfaced that the spike program had drifted from [ADR-0001](../../../docs/adrs/ADR-0001-exploration-first.md)'s coexistence commitment (multiple retrieval / ranking strategies must coexist) toward winner-picking under sequential narrowing — a violation that was invisible from inside the spike program because every step looked locally reasonable.

The redirection deliberation [`2026-04-25-long-arc-and-multi-lens-redirection.md`](../../deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md) committed the project to a multi-lens MCP substrate for v0.2, ratified in [ADR-0005](../../../docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md). With that commit, "which embedding model wins" is no longer the load-bearing v0.2 architectural decision. The `008` design's structural premise (a single best configuration; a two-challenger cap; "winner shapes architecture") does not serve the multi-lens substrate's question.

## What is preserved from 008

- **The function-in-use evaluation question** ("do these configurations help research tasks, and do blind-spot papers actually contribute to outputs?") is preserved in altered form as v0.2 Phase 17 (longitudinal pilot harness).
- **The `selected` vs `contributed` distinction** carries forward — distinguishing what the agent opened from what materially shaped the final output remains a useful signal under multi-lens framing.
- **The pre-registration discipline** — explicit priors on hypotheses, disputed-instance rules, pilot-only fallback when human review is unavailable — is preserved as a pattern; v0.2 Phase 17 inherits it.
- **The mandatory qualitative-review and human-adjudication gates** carry forward into the longitudinal pilot.

## What is discarded

- **Tournament framing.** No "winner" picked; no architectural commit hinges on which configuration scored best. ADR-0005 already committed the multi-lens substrate.
- **Two-challenger cap.** Replaced by lens-by-lens design decisions (semantic lens, citation/community lens), each made on its own grounds.
- **`SPECTER2` vs `Voyage` as the load-bearing comparison.** The semantic lens is one lens among multiple; embedding-model selection within the semantic lens is a per-lens design decision, not the v0.2 architectural call.
- **The `Stella`-as-fallback structure.** With no tournament, no fallback slot; deferred branches re-enter via the lens-design process if and when relevant.
- **Bounded-task evaluation as the function-in-use definition.** The longitudinal pilot evaluates lens utility over weeks of practice, not over individual bounded tasks.

## Where it goes forward

[v0.2 Phase 17](../../milestones/v0.2-MILESTONE.md) — Longitudinal Pilot Harness. Captures lens usage, selections, dismissals, returns over weeks of Logan's research practice. The question shifts from "which configuration helps a task" to "which lenses get selected for which research-practice operations, and where do they disagree productively?"

## What this supersession is not

- Not a claim that the original `008/DESIGN.md` was wrong on its own terms. As a tournament-frame spike design, it was internally rigorous (priors stated, disputed-instance rules clear, pilot-only fallback well-pre-registered). The supersession is about the frame being wrong for the project's architectural question, not about the spike being poorly designed.
- Not an erasure. `008/DESIGN.md` and `008/TASK-MATRIX.md` are preserved unchanged below the status header. Future readers can see what was originally drafted and why.
- Not a precedent for shelving spikes silently. Methodology binds: when a spike is superseded, the rationale is captured in a SUPERSESSION artifact alongside the original design. The 2026-04-25 methodology audit cycle is the precedent for this discipline.

## Lesson preserved for the spike program

The drift from ADR-0001's coexistence commitment to winner-picking via sequential narrowing was invisible from inside the spike program because every individual step (005's framework robustness, 006's retrieval geometry, 007's mechanism narrowing, 008's task-based evaluation) was locally defensible. The cumulative drift was visible only from outside — a paired adversarial review and an explicit ADR-against-current-work audit. The lesson, encoded in [`spikes/METHODOLOGY.md`](../METHODOLOGY.md) practice discipline F (pattern-watch with self-application), is that discipline at the layer below does not automatically transfer to the layer above; periodic ADR-against-current-work audits are the counter-posture.
