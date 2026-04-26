# Governance-Doc Paired Audit Package — 2026-04-26

Wave 2 of the v0.2 plan-revision sequencing (per audit synthesis 2026-04-25-v0.2-plan-audit-synthesis.md §9). Paired audit of the not-yet-audited governance-doc set.

## Scope

Audit target (integrated artifact set):

- `docs/adrs/ADR-000{1,2,3,4}-*.md` (ADR-0005 audited separately in v0.2 cycle)
- `AGENTS.md` (project root)
- `CLAUDE.md` (project root)
- `.planning/REQUIREMENTS.md` outside v0.2 codes
- `.planning/ROADMAP.md` outside Phases 12-17
- `.planning/STATE.md`
- `.planning/foundation-audit/`
- `.planning/ECOSYSTEM-COMMENTARY.md`

## Pair structure

| Reviewer | Model / effort | Prompt | Output target |
|---|---|---|---|
| Cross-vendor | GPT-5.5 high (codex CLI) | `cross-vendor-prompt.md` | `.planning/audits/2026-04-26-governance-audit-cross-vendor.md` |
| Same-vendor adversarial | Claude Opus 4.7 xhigh (`adversarial-auditor-xhigh` subagent) | `same-vendor-xhigh-prompt.md` | `.planning/audits/2026-04-26-governance-audit-opus-adversarial-xhigh.md` |

## M1 discipline applied

This is the first paired audit dispatch under METHODOLOGY discipline A's independent-dispatch sub-discipline (Hypothesis status, codified 2026-04-26 from the v0.2 audit cycle's documented contamination effects — see `METHODOLOGY.md:112`).

Both prompts include explicit forbidden-reading lists naming all v0.2-plan-audit artifacts and the parallel governance-audit artifact. Compliance is verifiable in each agent's tool-use trace.

The forthcoming synthesis (separate session) will compare the cross-vendor and same-vendor outputs and either confirm or weaken the discipline's Hypothesis status based on whether the independent-dispatch protocol again produces measurable separation between paired audits.

## Dispatch sequence

1. Dispatching session writes both prompt files (this commit).
2. Same-vendor xhigh dispatched in background via the `adversarial-auditor-xhigh` subagent.
3. Logan dispatches cross-vendor side via codex CLI (instructions in `cross-vendor-prompt.md`).
4. Both audits write to disk.
5. Comparison + synthesis in a separate session.

## Out of scope for this audit

- ADR-0005 (audited in v0.2 cycle)
- v0.2 plan documents (audited in v0.2 cycle): `v0.2-MILESTONE.md`, ROADMAP Phases 12-17, REQUIREMENTS v0.2 codes, VISION.md, LONG-ARC.md, METHODOLOGY.md practice-disciplines extension
- Source code (this is a doctrine-and-planning level audit)
- Test infrastructure
- The v0.2 audit artifacts themselves (forbidden per M1)
