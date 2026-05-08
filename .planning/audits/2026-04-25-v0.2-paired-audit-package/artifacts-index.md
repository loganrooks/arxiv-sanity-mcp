---
type: artifacts-index
status: reference
date: 2026-04-25
purpose: Paths and brief descriptions for every artifact in the v0.2 paired audit scope
---

# v0.2 Paired Audit — Artifacts Index

## In scope (audit these as an integrated set)

| Path | What it is | Why it's in scope |
|---|---|---|
| `.planning/milestones/v0.2-MILESTONE.md` | v0.2 scope spec: goals, architectural commits, scope boundaries, open scoping resolutions, risks, methodology bindings | Defines what v0.2 is and isn't |
| `.planning/ROADMAP.md` (Phases 12-17 only) | Phase-level details: goals, dependencies, requirements, success criteria, plan titles | The execution-level plan |
| `.planning/REQUIREMENTS.md` (v0.2 section only) | 17 new requirement codes (LENS-01..05, CITE-01..04, LDIS-01..03, LPILOT-01..03, MCP-08, MCP-09) with traceability | What gets verified |
| `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` | Architectural commit that the plan operationalizes | The decision being executed |
| `.planning/VISION.md` | Product identity at maturity: platform identity, anti-vision, lens trajectory, audience grounding, reopen conditions | The destination v0.2 is staging toward |
| `.planning/LONG-ARC.md` | Planning doctrine: protected seams, anti-patterns to detect, methodology brief, explicit non-decisions | The discipline current planning must respect |
| `.planning/spikes/METHODOLOGY.md` | Six interpretive lenses + six practice disciplines (extended this session) | The methodology binding all spike-level and audit-level work |

## Reference (consult, don't audit)

| Path | What it is | Why consult |
|---|---|---|
| `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` | Phase 3 property audit (Opus rerun, verified) gating Option B selection | Establishes the empirical baseline for the v0.2 plan |
| `.planning/deliberations/2026-04-25-long-arc-and-multi-lens-redirection.md` | The substantive direction-shift deliberation | Journey context for why v0.2 looks the way it does |
| `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md` | Cross-session handoff at v0.2 plan commit | Orientation for the audit's purpose and scope |
| `docs/adrs/ADR-0001-exploration-first.md` | Multi-lens coexistence commitment, binding for v0.2 | The constraint v0.2 must honor in implementation, not only design |

## Out of scope (don't audit, don't read first)

| Path | Why out of scope |
|---|---|
| `.planning/spikes/005-*` through `008-*` | Spike program is in transitional state; 008 superseded; 005-007 are completed historical artifacts under the now-displaced tournament frame. Don't audit. Reference the override annotation in 007/HANDOFF.md and 008/SUPERSESSION.md only if needed. |
| `.planning/spikes/reviews/2026-04-25-*` | Methodology audit cycle outputs (cross-vendor, Opus adversarial, pressure pass). Reference for methodology pattern; don't audit. |
| `.planning/audits/2026-04-25-phase-3-property-audit-provisional.md` | Superseded provisional audit. Preserved as evidence of methodology failure (default Explore agent on a gating audit). Don't audit. |
| `.planning/deliberations/2026-04-25-*` (other than long-arc) | Other 2026-04-25 deliberations (audience reframe, load-bearing assumptions audit, etc.). Reference if needed; don't audit. |
| Source code under `src/` | Code audit not in scope; this is plan-level audit. |
| Test code under `tests/` | Test audit not in scope; backward-compat strategy is plan-level claim. |

## Artifact relationships (for orientation)

- **VISION.md** ← describes-the-destination ← **LONG-ARC.md** ← **MILESTONE / ROADMAP / REQUIREMENTS / ADR**
- **METHODOLOGY.md** ← discipline-source ← **LONG-ARC.md** (which summarizes a brief subset and cross-references)
- **ADR-0001 (exploration-first)** ← architectural-binding ← **ADR-0005 (multi-lens substrate)** ← operationalizes ← **MILESTONE / ROADMAP**
- **Property audit (Opus)** ← empirical-input ← **ADR-0005's Option B selection**
- **Redirection deliberation** ← journey-source ← **VISION + LONG-ARC + ADR-0005**
