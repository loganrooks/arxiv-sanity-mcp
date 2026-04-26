# Same-Vendor Critical Audit Prompt (xhigh rerun) — v0.2 Plan + VISION + LONG-ARC + METHODOLOGY

## Why this rerun exists

The first run of this audit (2026-04-25, effort `high`) produced findings preserved at `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md`. METHODOLOGY discipline A (`spikes/METHODOLOGY.md:107-108`) prescribes **xhigh** for paired-review members. The first run executed at `high`, a discipline-A self-application gap. This rerun closes it.

The base posture for this audit lives in your subagent definition (`adversarial-auditor-xhigh`) — read it as your standing role. This prompt provides the project-specific scope, context, and dimensions.

## Project context

- arxiv-sanity-mcp: an MCP-native research-discovery substrate for AI/CS/ML researchers.
- v0.1 shipped 2026-03-14 (31 plans, 403 tests, MCP server with 10 tools / 4 resources / 3 prompts).
- ADR-0001 commits the project to "exploration-first architecture: multiple retrieval and ranking strategies must coexist." The post-v0.1 spike program (005-008) drifted toward tournament narrowing, quietly violating it. The drift was caught by a 2026-04-25 paired methodology audit.
- The redirection committed v0.2 to a multi-lens substrate honoring ADR-0001 in implementation, not only design. ADR-0005 is the architectural commit. The v0.2 plan operationalizes it.
- The same author wrote VISION, LONG-ARC, the METHODOLOGY practice-disciplines extension, and the v0.2 plan in a single session. They are aware of closure-pressure recurrence (METHODOLOGY discipline F: pattern-watch with self-application).
- The team's stated lessons from the methodology audit cycle: tournament narrowing recurs at every layer; calibrated language must be default register, not closing-section exception; rhetorical labels need argument under them.

The audit's central question, grounded in the team's stated goals: **did the author succeed at applying these disciplines to their own writing, and where the work falls short, what specifically needs to change for v0.2 to deliver against VISION + ADR-0005 + LONG-ARC seams without the patterns the team has committed to avoiding?**

## What to audit (integrated artifact set)

1. `.planning/milestones/v0.2-MILESTONE.md`
2. `.planning/ROADMAP.md` (Phases 12-17 only)
3. `.planning/REQUIREMENTS.md` (v0.2 section only — 17 codes)
4. `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
5. `.planning/VISION.md`
6. `.planning/LONG-ARC.md`
7. `.planning/spikes/METHODOLOGY.md` (the practice-disciplines extension specifically — six new disciplines added 2026-04-25, lines 97-164)

Reference (consult, do not audit):

- `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` — gating audit
- `.planning/audits/2026-04-25-v0.2-plan-audit-cross-vendor.md` — the cross-vendor pair-member's output (you may read it for convergence/divergence awareness, but do not anchor your findings to theirs)
- `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md` — the prior `high` run of this audit; useful as a baseline (where do you go deeper at xhigh, where do your findings differ, where do they converge)
- `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md` — orientation
- `.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md` — register precedent for this project's paired-review work

## Dimensions (apply in order)

For every finding, follow the output structure specified in your subagent definition: **what / why it matters (grounded in 1–5) / severity tier / confidence / what would dissolve / suggested improvement direction.**

### Dimension A — Closure pressure recurrence

Did closure pressure recur in the v0.2 artifact set? Specifically:

- Where is calibrated language confined to closing sections (Risks, Open questions, Reopen conditions) rather than running through prose? (METHODOLOGY discipline D, applied to its own author.)
- Where do rhetorical labels ("load-bearing", "binding", "first-class", "canonical") do argument-shaping work without supporting argument under them?
- Where do prescriptive consequences ("the plan commits to X", "must Y", "therefore Z") overrun the diagnostic grounds the document gives?
- Where does a multi-item commitment list bury per-item credence (e.g., conflating verified, inferred, and speculative items in one indexed bullet list)?

### Dimension B — Reverse-engineered necessity

Did the author construct option spaces or framings that make the chosen answer the only sensible one? The 2026-04-16 deliberation review identified this pattern in the original deliberation. Does it recur here?

- Are the three Options (A, B, C) for the roadmap commit a real option space, or were they constructed to make B inevitable?
- Is "validate the abstraction by shipping at least two lenses" (ADR-0005) an empirical claim, a methodological commitment, or a rhetorical move? If methodological, is it labeled as such?
- Are the six audit dimensions in the METHODOLOGY practice-disciplines extension a closed taxonomy, or do they leak / overlap / hide a seventh discipline that wasn't named?

### Dimension C — Tournament-narrowing / fusion-by-default recurrence

The plan explicitly proscribes tournament narrowing and fusion-by-default. Did the author actually exclude these, or did they sneak back in by structure even when ejected by name?

- What is the default behavior when a user requests `lens=` omitted, or `lens=["semantic", "citation_community"]` with no explicit operation? If unspecified, integration-time defaults will fill the gap — exactly the silent-defaults anti-pattern.
- Is the semantic-lens embedding model a per-lens design decision, or is the v0.2 plan silently shipping the v0.1 baseline because no one explicitly addressed it?
- Phase 17 (longitudinal pilot) replaces tournament `008`. Does the pilot's capture schema implicitly tournament-frame the analysis (e.g., "lens-of-record per event" assumes one lens-of-record per event, which structurally re-introduces winner-pick at analysis time)?

### Dimension D — Self-application gaps

The author explicitly invokes self-application as a discipline (METHODOLOGY discipline F). Did they apply the disciplines to their own writing the way they applied them to the spike program?

- Did the author paired-review the v0.2 plan before committing it? (No — this audit is the paired review. The author committed first, audited after. Is that the right order, and what's the remediation?)
- Did the author pre-register empirical thresholds for the OpenAlex coverage spike (Phase 14 plan 1), as METHODOLOGY discipline B and the Bayesian lens require?
- Did the author verify load-bearing factual claims against the codebase, or rest on memory? The Property audit is the reference; do other plan claims have similar verification?
- Did the author produce calibrated language throughout, or only in Risks / Reopen-conditions sections?

### Dimension E — VISION's anti-vision under critical read

VISION's anti-vision section says the platform is *not* a paper chatbot, RAG wrapper, ranked-list-but-fancier, arxiv-sanity-but-better, leaderboard, generic discovery, or implicit-profile-learning-without-confirmation.

- Does the v0.2 plan covertly slip toward any of these despite the explicit anti-vision? (E.g., is "ranked-list-but-fancier" actually different from "multi-lens with optional fusion" once implemented?)
- Are the differentiations from arxiv-sanity load-bearing for v0.2 delivery, or are they aspirational claims that won't survive a researcher actually using the tool?
- Is "not implicit-profile-learning without confirmation" preserved by mechanism in v0.2, or only preserved by deferral (the relevant feature ships post-v0.2)?

### Dimension F — Methodology extension scope-creep

The METHODOLOGY.md practice-disciplines extension (lines 97-164) adds six disciplines to a previously stable six-lens document. Did this extension creep in scope or substance?

- Are these disciplines genuinely lessons from the audit cycle, or pre-existing methodological commitments retrofitted as "lessons"?
- Is "pattern-watch with self-application" (discipline F) operationally distinct from disciplines A–E, or is it a meta-discipline that adds no separate guidance?
- Did adding six practice disciplines shift the document's center of gravity from interpretive lenses to operational protocols? If so, what's the cost to future use?

## Output

Write to `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial-xhigh.md`. The prior `high` run remains at `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md` for comparison — do not overwrite it.

Frontmatter:

```yaml
---
type: same-vendor-critical-audit
status: complete
date: 2026-04-26
target: v0.2 plan + VISION + LONG-ARC + METHODOLOGY (integrated artifact set)
auditor: Claude Opus 4.7 (fresh session, critical reviewer per adversarial-auditor-xhigh)
effort: xhigh
supersedes: 2026-04-25-v0.2-plan-audit-opus-adversarial.md (high run; preserved for comparison)
parallel_to: 2026-04-25-v0.2-plan-audit-cross-vendor.md
---
```

Document structure (per the subagent definition):

1. **Summary** — 3-5 sentences naming the strongest survived findings and the most consequential strength.
2. **Findings by dimension** — A through F. For each finding: what / why it matters (ground 1–5) / severity tier / confidence / what would dissolve / suggested improvement direction.
3. **What works well** — strengths grounded in the same 1–5; what the team should preserve.
4. **Convergent risks** — where multiple findings point at the same underlying weakness.
5. **Steelman residue** — honest pass over which findings did less work than they looked like.
6. **What this audit cannot tell you** — bounded scope.

## Length and density

The prior `high` run was ~5500 words. xhigh has more reasoning budget; use it for *depth per finding* (more thorough grounding, more careful steelman), not for finding-count inflation. Aim for ~4000–6000 words. A tighter audit with stronger grounding outperforms a longer one with thinner grounding.

Begin.
