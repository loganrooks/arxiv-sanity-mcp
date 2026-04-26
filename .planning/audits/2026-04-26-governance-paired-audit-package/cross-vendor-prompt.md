# Cross-Vendor Governance Audit Prompt — ADRs 0001-0004 + AGENTS + CLAUDE + REQUIREMENTS-outside-v0.2 + ROADMAP-outside-12-17 + STATE + foundation-audit + ECOSYSTEM-COMMENTARY

## Your role

You are an independent reviewer auditing the **governance-doc set** of an MCP-native research-discovery substrate ("arxiv-sanity-mcp"). The governance docs sit underneath the project's planning canon (ROADMAP / phase plans) — they are the doctrine layer that current planning is supposed to honor. The audit's purpose is to test whether the governance substrate is itself coherent, honored elsewhere, and free of the closure-pressure / scope-creep / drift patterns the recent paired methodology audit surfaced in the v0.2 plan layer.

**Working directory:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp`

You are running on GPT-5.5 with reasoning effort `high`. Take your time with the artifacts; the cost of a careful audit is acceptable.

## Forbidden reading (M1 discipline)

You **must not read** any of these files. They are audits of a different artifact set (the v0.2 plan), not the governance-doc set you are auditing. Reading them would prime your reading of the governance docs through the v0.2 audit's frame and produce delta-on-prior reasoning instead of independent reading. This forbidden-reading list is per METHODOLOGY discipline A's independent-dispatch sub-discipline (Hypothesis status, codified 2026-04-26 from the v0.2 audit cycle's documented contamination effects).

- Anything matching `.planning/audits/2026-04-25-*` (cross-vendor, same-vendor, contaminated, independent, comparison, synthesis — all of the v0.2 plan audit cycle)
- Anything under `.planning/audits/2026-04-25-v0.2-paired-audit-package/`
- Anything under `.planning/audits/2026-04-26-governance-paired-audit-package/` *except this prompt file*

If you find yourself wanting to read one of these to "calibrate" or "compare," do not. The point of independence is that you produce a reading uncontaminated by other readings. The synthesis step (separate from this audit) will combine your reading with others; that is not your job here.

You may freely read everything else in the repository, including the v0.2 plan documents themselves (`v0.2-MILESTONE.md`, `ADR-0005`, `ROADMAP.md` Phases 12-17, etc.) — those are derivative artifacts of the governance docs you're auditing, and seeing how the doctrine is invoked in the derivative set is part of the audit. Only the v0.2 *audit* artifacts are forbidden, not the v0.2 plan artifacts.

## Project context (minimal, for vocabulary)

- arxiv-sanity-mcp: an MCP-native research-discovery substrate for AI / CS / ML researchers (primary audience); AI-ethics, AI-philosophy researchers (adjacent).
- v0.1 shipped 2026-03-14 (31 plans, 403 tests, MCP server with 10 tools / 4 resources / 3 prompts).
- v0.2 is in planning (Phases 12-17, ~2 months); the v0.2 plan layer was paired-audited 2026-04-25 (results not visible to you per the forbidden-reading list).
- The governance-doc set you're auditing pre-dates the v0.2 plan and provides the doctrinal substrate that v0.2 invokes.

## What to audit

Read these as the integrated governance-doc set:

1. **ADRs 0001-0004** at `docs/adrs/ADR-000{1,2,3,4}-*.md`. The four foundational ADRs:
   - ADR-0001 — exploration-first architecture (the multi-retrieval/coexistence commitment)
   - ADR-0002 — metadata-first, lazy enrichment
   - ADR-0003 — license and provenance first
   - ADR-0004 — MCP as workflow substrate
2. **`AGENTS.md`** (project root) — agent behavior rules and working posture
3. **`CLAUDE.md`** (project root, not the user's `~/.claude/CLAUDE.md`) — instructions for Claude Code working on this repo
4. **`.planning/REQUIREMENTS.md`** *outside the v0.2 section*. The v0.1 / shipped section and the v2-deferred section. The v0.2 section (LENS-01..05, CITE-01..04, LDIS-01..03, LPILOT-01..03, MCP-08, MCP-09) was already audited separately; do not re-audit it.
5. **`.planning/ROADMAP.md`** *outside Phases 12-17*. Phases 1-11 (v0.1 history) and any v2-and-beyond backlog. Phases 12-17 (v0.2) were already audited separately.
6. **`.planning/STATE.md`** — the project's live state record
7. **`.planning/foundation-audit/`** — directory of foundation-audit notes
8. **`.planning/ECOSYSTEM-COMMENTARY.md`** — cross-project analysis (arxiv-scan ↔ MCP)

You may also read (without auditing them as targets) any other planning artifacts you need to evaluate the doctrine-vs-derivative-claim relationships: the v0.2 plan, deliberation documents under `.planning/deliberations/`, the v0.1 phase plans under `.planning/phases/`, the spike artifacts under `.planning/spikes/` (especially METHODOLOGY.md). These are reading-as-context, not audit targets.

## Audit dimensions (apply in order)

For each dimension, give: (a) your finding(s) with file:line citations, (b) confidence level (low / medium / high), (c) recommended action if any.

### Dimension 1 — ADR coherence and binding clarity

ADRs 0001-0004 are the foundational durable decisions. Are they doing binding work?

- Is each ADR's stated decision precise enough that a future drift could be caught against it (the way the 005-008 spike chain's drift was caught against ADR-0001 only after months)? Or are the decisions vague enough to be invoked rhetorically without binding?
- ADR-0001's "exploration-first / multiple strategies coexist" — is this a precise commitment, an aspirational principle, or a rhetorical anchor? Compare to how ADR-0005 invokes it.
- ADR-0002 (metadata-first, lazy enrichment), ADR-0003 (license and provenance first), ADR-0004 (MCP as workflow substrate) — same questions for each. Are they invoked elsewhere in the governance set? Where they are invoked, is the invocation honoring the ADR or stretching it?

### Dimension 2 — AGENTS.md / CLAUDE.md operational discipline

These files contain instructions for the agents (human and AI) working on the project.

- Do the instructions match how the project actually works? Where they prescribe practices, are those practices observable in the codebase / planning artifacts / commit history?
- Is there scope creep — instructions that have accreted but no one follows, or that duplicate content across files (AGENTS.md and CLAUDE.md often have overlap)?
- The project uses status markers (Settled / Chosen for now / Hypothesis / Open) per CLAUDE.md. Are these markers used consistently in the documents that should use them, or only sporadically?

### Dimension 3 — REQUIREMENTS / ROADMAP outside v0.2: historical accuracy + forward coherence

- The v0.1 section of REQUIREMENTS.md and Phases 1-11 of ROADMAP describe completed work. Spot-check: does what's claimed-shipped match what shipped (test counts, MCP tool/resource/prompt counts, file presence)? Any phantom requirements (claimed but never delivered)?
- The v2-deferred section of REQUIREMENTS.md and any v2 backlog in ROADMAP commit to future work. Does the deferred set make sense given v0.2's direction? Are any v2-deferred items now foreclosed or made harder by v0.2's architectural commitments? Are any v2-deferred items now redundant given v0.2 absorbs them?
- Is the requirement-to-phase mapping audit-able? Can a reader trace a requirement to its delivering phase and back?

### Dimension 4 — STATE.md reliability

STATE.md is the project's live state record per GSD discipline.

- Does STATE.md reflect actual current state, or has it drifted from reality?
- Are its claims load-bearing (i.e., would a reader rely on STATE.md for go/no-go decisions)? If so, are the load-bearing claims verifiable?
- Is the timestamping discipline observed?
- Where it cites artifacts (test count, plan count, etc.), do the cites match git/file reality?

### Dimension 5 — Foundation-audit notes: ratified vs orphaned

The `.planning/foundation-audit/` directory contains the project's epistemic-audit findings (predates the methodology audit cycle).

- What's in there? Inventory.
- Were the actionable items resolved? Trace any "fix X" / "decide Y" findings to either resolution or current open status.
- Are unresolved items still tracked somewhere live (e.g., ROADMAP, deliberations, ADRs), or have they orphaned (the audit's findings exist in the directory but nothing else references them)?
- If orphaned: is that because they were resolved-by-other-means, or genuinely lost?

### Dimension 6 — ECOSYSTEM-COMMENTARY scope and currency

`.planning/ECOSYSTEM-COMMENTARY.md` is cross-project analysis (arxiv-scan ↔ MCP per the doc's stated purpose).

- Is the document's scope still relevant given v0.2's direction?
- Are its claims (e.g., about external projects, ecosystem positioning, gaps) still true?
- If stale: is it labeled as historical / dated, or presented as current?

### Dimension 7 — Closure-pressure / register-inflation patterns at the doctrine layer

The recent v0.2 plan audit cycle surfaced patterns the audit's own author wrote: closure pressure (calibrated language confined to closing sections), rhetorical inflation ("load-bearing" / "first-class" / "binding" labels doing argument-shaping work without supporting argument), prescriptive consequences overrunning diagnostic grounds.

- Do any of the governance docs exhibit these patterns?
- ADRs are particularly prone to "binding" rhetoric — is the binding language in ADRs 0001-0004 calibrated, or inflated?
- AGENTS.md / CLAUDE.md often use prescriptive language ("must", "always", "never") — is the prescription matched by mechanism that enforces it, or is it instruction-as-aspiration?

### Dimension 8 — Doctrine-vs-derivative integrity

The governance docs are doctrine. STATE.md, foundation-audit notes, ECOSYSTEM-COMMENTARY, and the v0.2 plan are derivative artifacts that invoke or extend the doctrine.

- Do the derivative artifacts inherit doctrine claims correctly?
- Where derivatives extend doctrine (e.g., LONG-ARC extending VISION, METHODOLOGY extending ADR-0001 in spirit), are the extensions consistent or do they drift?
- Specific check: ADR-0001's coexistence commitment is operationalized in the v0.2 plan via ADR-0005. Is the operationalization faithful to ADR-0001, or does it under-cover or over-extend?

## Output format

Write your audit to standard output (will be captured to `.planning/audits/2026-04-26-governance-audit-cross-vendor.md`). Use this structure:

```
---
type: cross-vendor-governance-audit
status: complete
date: 2026-04-26
target: governance-doc set (ADRs 0001-0004 + AGENTS + CLAUDE + REQUIREMENTS-outside-v0.2 + ROADMAP-outside-12-17 + STATE + foundation-audit + ECOSYSTEM-COMMENTARY)
auditor: GPT-5.5 via codex CLI, reasoning_effort=high
independence: This audit was dispatched without reference to any audit of the v0.2 plan layer. The dispatching prompt forbade reading prior v0.2-plan-audit artifacts per METHODOLOGY discipline A's independent-dispatch sub-discipline.
---

# Cross-Vendor Governance Audit

## Summary
[2-4 sentences on overall finding: doctrine coherence, named gaps, recommended actions]

## Findings by dimension
### Dimension 1 — ADR coherence and binding clarity
[findings with file:line + confidence + recommended action]
### Dimension 2 — AGENTS.md / CLAUDE.md operational discipline
[same]
### Dimension 3 — REQUIREMENTS / ROADMAP outside v0.2 — historical accuracy + forward coherence
[same]
### Dimension 4 — STATE.md reliability
[same]
### Dimension 5 — Foundation-audit notes: ratified vs orphaned
[same]
### Dimension 6 — ECOSYSTEM-COMMENTARY scope and currency
[same]
### Dimension 7 — Closure-pressure / register-inflation at the doctrine layer
[same]
### Dimension 8 — Doctrine-vs-derivative integrity
[same]

## Cross-cutting observations
[anything that crossed dimensions or didn't fit cleanly]

## Confidence calibration
[which findings are load-bearing on single readings vs cross-confirmed across multiple artifacts; which framing claims warrant same-vendor adversarial confirmation]

## What I am not telling you
[bounded scope: what the audit didn't cover]
```

## Constraints

- Write file:line citations for every load-bearing claim. No claims from memory of common patterns.
- Calibrated language is the default register, not a closing-section concession. State confidence where claims are made.
- "Recommended action" is the operative phrase; "must" appears only where binding is explicit (ADR violation, etc.).
- Don't pull punches; don't false-balance. If the doctrine is sound, say so. If it has gaps, name them with evidence.
- Don't audit source code; this is doctrine-and-planning level.
- Aim for ~2000-3000 words total.

## Dispatch instructions for Logan

To run this audit via codex CLI:

```bash
cd /home/rookslog/workspace/projects/arxiv-sanity-mcp
codex --model gpt-5.5 --reasoning-effort high --file .planning/audits/2026-04-26-governance-paired-audit-package/cross-vendor-prompt.md > .planning/audits/2026-04-26-governance-audit-cross-vendor.md
```

(Adjust the codex CLI invocation to whatever local convention is in use.)

Begin reading the artifacts.
