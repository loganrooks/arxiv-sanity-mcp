# Cross-Vendor Audit Prompt — v0.2 Plan + VISION + LONG-ARC + METHODOLOGY

## Your role

You are an independent reviewer auditing the v0.2 plan of an MCP-native research-discovery substrate ("arxiv-sanity-mcp"). The plan was authored in a single session by a single Anthropic Claude Opus 4.7 reader. The audit's purpose is to test whether an independent vendor reads the same coherence (or finds the same gaps) in the integrated artifact set, before Phase 12 execution begins.

**Working directory:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp`

You are running on GPT-5.5 with reasoning effort `high`. Take your time with the artifacts; the cost of a careful audit is acceptable.

## Project context (minimal, for vocabulary)

- The project shipped v0.1 (31 plans, 403 tests, MCP server with 13 tools / 4 resources / 3 prompts) on 2026-03-14.
- An accepted ADR (ADR-0001) commits the project to "exploration-first architecture: multiple retrieval and ranking strategies must coexist."
- Post-v0.1, a four-spike research suite (005-008) drifted toward tournament-narrowing — picking a winning embedding model — quietly violating ADR-0001's coexistence commitment. The drift was caught only by a 2026-04-25 paired methodology audit.
- The 2026-04-25 redirection deliberation committed v0.2 to a multi-lens substrate honoring ADR-0001 in implementation, not only in design. ADR-0005 is the architectural commit; the v0.2 plan operationalizes it into 6 phases (12-17), 15 plans, ~2 months.
- Audience is AI / CS / ML researchers (primary); AI-ethics, AI-philosophy researchers (adjacent).

## What to audit

Audit these documents as a single integrated artifact set, not separately:

1. `.planning/milestones/v0.2-MILESTONE.md` — scope spec
2. `.planning/ROADMAP.md` — Phases 12-17 details (other phases are completed v0.1 history; you can ignore)
3. `.planning/REQUIREMENTS.md` — the v0.2 Requirements section (17 codes: LENS-01..05, CITE-01..04, LDIS-01..03, LPILOT-01..03, MCP-08, MCP-09)
4. `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` — architectural commit
5. `.planning/VISION.md` — product identity
6. `.planning/LONG-ARC.md` — planning doctrine
7. `.planning/spikes/METHODOLOGY.md` — six interpretive lenses + six practice disciplines (the practice disciplines were extended this session)

Optional reference (consult, don't audit):
- `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` — gating audit for Option B
- `docs/adrs/ADR-0001-exploration-first.md` — the load-bearing ADR

Do not audit `.planning/spikes/005-*` through `008-*` — these are completed-or-superseded historical artifacts under the displaced tournament frame.

## Audit dimensions (apply in order)

For each dimension, give: (a) your finding(s) with file:line citations, (b) confidence level (low / medium / high), (c) recommended action if any.

1. **LONG-ARC anti-pattern check.** LONG-ARC.md names anti-patterns: tournament narrowing, accidental single-lens interface, silent defaults, ADR-violation-by-drift, closure pressure, embedding-model-as-load-bearing, single-reader framing claims as authoritative. Does the v0.2 plan re-introduce any of these despite the doctrine? Look especially at Phase 13 (MCP surface lens-awareness — what's the default behavior when `lens=` is omitted? when multiple lenses are registered?), Phase 16 (lens-disagreement / intersection ops — does any default silently default to fusion?), Phase 17 (longitudinal pilot — is the opt-in specified or silent?).

2. **VISION coherence check.** VISION.md commits to a multi-lens substrate, research-practice operations beyond retrieval, longitudinal-memory across years, provenance/inspectability, lens trajectory (committed/open/speculative), and an explicit anti-vision. Does the v0.2 plan honor these? Does it foreclose any operations VISION names? Conversely, does it commit to anything that VISION's anti-vision rejects?

3. **LONG-ARC protected-seams check.** LONG-ARC.md names protected seams: lens extensibility; bundle-of-signals primitive; per-lens provenance; MCP surface lens-awareness; citation/community as first-class data (not enrichment); longitudinal state; inspectability of every signal; MCP-native operations. Does the plan preserve all of these? Where is each seam concretely instantiated in the phases? Are any seams underspecified or silently violated?

4. **METHODOLOGY practice-discipline check.** METHODOLOGY.md (practice-disciplines section, added 2026-04-25) names: paired review for framing claims; model verification before delegating gating audits; single-reader factual-claim verification; calibrated language as default register; pressure-test artifacts before remedies; pattern-watch with self-application. Does the plan apply these disciplines, especially calibrated language and pre-registration of empirical thresholds? Phase 14 plan 1 is a coverage spike — is the empirical threshold for "OpenAlex coverage too thin" pre-registered, or is it left to spike-time judgment?

5. **Critical-path realism check.** The plan claims `12 → 13 → 16 → 17` as the critical path, with 14 parallelizable against 12 and 15 dependent on `{12, 14}`. Is this realistic? Does any plan within a phase have undisclosed cross-phase dependencies? Is "~2 months" plausible given the dependency graph and ADR-0005's enumerated work items?

6. **Coverage check.** Walk through ADR-0005's enumerated commitments (Lens interface, lens= parameter, ProfileRankingService dispatcher, bundle-of-signals primitive, citations storage retrieval-shaped, SearchResult shape generalization with backward compat, lens-disagreement and intersection as MCP operations) and verify each maps to a phase + plan. Any commitment unmapped? Any unaccounted scope?

7. **Risk completeness.** v0.2-MILESTONE.md names 6 risks with mitigations. Are these the actual risks? What's missing? Specifically check for: backward-compat ripple (existing MCP consumers, CLI, tests); Phase 14 schema decision (edges table vs JSONB projection — what governs the choice?); semantic-lens embedding-model selection (does v0.2 ship the semantic lens unchanged from v0.1, or is this an open decision?); Phase 17 capture-schema-stability strategy (what if mid-pilot review reveals capture-schema gaps?); pilot signal isolation (multi-lens pilot may capture lens *usage* without isolating lens *value*).

## Output format

Write your audit to standard output (will be captured to `.planning/audits/2026-04-25-v0.2-plan-audit-cross-vendor.md`). Use this structure:

```
---
type: cross-vendor-audit
status: complete
date: 2026-04-25
target: v0.2 plan + VISION + LONG-ARC + METHODOLOGY (integrated artifact set)
auditor: GPT-5.5 via codex CLI, reasoning_effort=high
---

# Cross-Vendor Audit — v0.2 Plan + VISION + LONG-ARC + METHODOLOGY

## Summary

[2-4 sentences on overall finding: integrated coherence, named gaps, recommended actions]

## Findings by dimension

### Dimension 1 — LONG-ARC anti-pattern check
[findings with file:line + confidence + recommended action]

### Dimension 2 — VISION coherence check
[same]

### Dimension 3 — LONG-ARC protected-seams check
[same]

### Dimension 4 — METHODOLOGY practice-discipline check
[same]

### Dimension 5 — Critical-path realism check
[same]

### Dimension 6 — Coverage check
[same]

### Dimension 7 — Risk completeness
[same]

## Cross-cutting observations

[anything that crossed dimensions or didn't fit cleanly]

## Confidence calibration

[which findings are load-bearing on single readings vs cross-confirmed across multiple artifacts; which framing claims warrant same-vendor adversarial confirmation]

## What I am not telling you

[bounded scope; what the audit didn't cover, e.g., source-code coupling, test infrastructure, ingestion paths]
```

## Constraints

- Write file:line citations for every load-bearing claim. No claims from memory of common patterns.
- Calibrated language is the default register, not a closing-section concession. State confidence where claims are made.
- "Recommended action" is the operative phrase; "must" appears only where binding is explicit (e.g., ADR-0001 or ADR-0003 violations).
- Don't pull punches; don't false-balance. If the plan is sound, say so. If it has gaps, name them with evidence.
- Don't audit the spikes (005-008) — those are out of scope.
- Don't audit source code; this is plan-level.
- Aim for ~1500-2500 words total.

Begin reading the artifacts.
