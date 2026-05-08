# Same-Vendor Adversarial Audit Prompt — v0.2 Plan + VISION + LONG-ARC + METHODOLOGY

## Your role

You are a same-vendor adversarial reviewer (Claude Opus 4.7, fresh session) auditing the v0.2 plan of an MCP-native research-discovery substrate ("arxiv-sanity-mcp"). The plan, VISION, LONG-ARC, and the practice-disciplines extension to METHODOLOGY were all authored in a single session by another Claude Opus 4.7 reader. You share the same vendor and the same model — your value is *register* awareness: you can recognize Anthropic-internal rhetorical patterns (closure pressure, prescriptive language overrunning diagnostic grounds, "load-bearing" / all-caps emphasis as argument-substitutes, calibrated language confined to closing footnotes) that a cross-vendor reader may not flag.

**Your role is hostile.** Argue *against* the plan's framing claims. Find the rhetorical inflation. Find the closure pressure. Find the moves where prescriptive language outruns its diagnostic grounds. The plan's author is your adversary; assume they are intelligent, well-intentioned, and wrong about specific things.

**Working directory:** `/home/rookslog/workspace/projects/arxiv-sanity-mcp`

You are running at reasoning effort `high`.

## What this is, what it isn't

This is *not* a code audit. The v0.2 plan has not been executed; there is no v0.2 code. This is an audit of the *plan documents themselves* — their coherence, their architectural commitments, their language, their mapping to the underlying ADR-0005 and VISION.

This is *not* a sanity check. The cross-vendor reviewer is doing the substance check. Your job is the register check that the cross-vendor reviewer cannot do (because they're not Claude and don't share the in-house rhetorical patterns).

## Project context (minimal, for vocabulary)

- The project shipped v0.1 (31 plans, 403 tests, MCP server) on 2026-03-14.
- ADR-0001 commits the project to "exploration-first architecture: multiple retrieval and ranking strategies must coexist." This was binding all along but quietly violated by the post-v0.1 spike program (005-008), which drifted toward tournament narrowing.
- The drift was caught by a 2026-04-25 paired methodology audit. The redirection deliberation committed v0.2 to a multi-lens substrate honoring ADR-0001 in implementation, not only design. ADR-0005 is the architectural commit; v0.2 plan operationalizes it.
- The same author who drove the redirection wrote VISION, LONG-ARC, the METHODOLOGY practice-disciplines extension, and the v0.2 plan. The author is aware of closure-pressure recurrence and explicitly self-applied the discipline (`spikes/METHODOLOGY.md` practice discipline F: pattern-watch with self-application).
- The author's stated lessons from the methodology audit cycle: tournament narrowing recurs at every layer; calibrated language must be default register; rhetorical labels ("load-bearing", "highest-impact", "CRITICAL", "Forces:") need argument under them.
- **Your hostile question: did the author succeed at applying these disciplines, or did the closure-pressure pattern recur in this very work?**

## What to audit

Audit these documents as a single integrated set:

1. `.planning/milestones/v0.2-MILESTONE.md`
2. `.planning/ROADMAP.md` (Phases 12-17 only)
3. `.planning/REQUIREMENTS.md` (v0.2 section only — 17 codes)
4. `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
5. `.planning/VISION.md`
6. `.planning/LONG-ARC.md`
7. `.planning/spikes/METHODOLOGY.md` (the practice-disciplines extension specifically — six new disciplines added 2026-04-25)

Optional reference:
- `.planning/audits/2026-04-25-phase-3-property-audit-opus.md` — the gating audit
- `.planning/handoffs/2026-04-25-v0.2-plan-handoff.md` — orientation
- The 2026-04-25 spike paired review outputs at `.planning/spikes/reviews/` — these are the precedent for *how* paired review is supposed to work; review them to calibrate what hostile reading looks like in this project.

## Adversarial dimensions (apply in order)

### Dimension A — Closure pressure recurrence

Did closure pressure recur in the v0.2 plan / VISION / LONG-ARC / METHODOLOGY? Specifically:

- Where is calibrated language confined to closing sections rather than running through prose? (METHODOLOGY discipline D, applied to its own author.)
- Where do rhetorical labels (e.g., "load-bearing", "binding", "first-class", "the load-bearing claim") do argument-shaping work without supporting argument under them?
- Where do prescriptive consequences ("therefore X", "must Y", "the plan commits to Z") overrun the diagnostic grounds the document gives?
- Where does the author confidently list a multi-item claim (e.g., "the plan commits to: lens interface; lens= parameter; dispatcher; bundle of signals; citations storage; generalized SearchResult; lens-disagreement") without acknowledging which items are speculative vs grounded vs binding?

### Dimension B — Reverse-engineered necessity

Did the author construct option spaces or framings that make the chosen answer the only sensible one? The 2026-04-16 deliberation review identified this pattern in the original deliberation ("the option space was constructed to make Option C the only sensible answer"). Does it recur?

- Are the three Options (A, B, C) for the roadmap commit a real option space, or were they constructed to make B inevitable?
- Are the six audit dimensions in the METHODOLOGY practice-disciplines extension a closed taxonomy, or do they leak / overlap / hide a seventh discipline that wasn't named?
- Is "Option B is the load-bearing choice" (ADR-0005 Context section) argued from evidence, or asserted from a framing that pre-empted A and C?
- Is "validate the abstraction by shipping at least two lenses" (ADR-0005 Decision) an empirical claim, a methodological commitment, or a rhetorical move?

### Dimension C — Tournament-narrowing / fusion-by-default recurrence

The plan explicitly proscribes tournament narrowing and fusion-by-default. Did the author actually exclude these, or did they sneak back in?

- What is the default behavior when a user requests `lens=["semantic", "citation_community"]` with no explicit operation? If undefined, the implementation will pick a default at integration time — which is exactly the pattern of silent defaults the LONG-ARC anti-patterns name.
- Is the semantic-lens embedding model a per-lens design decision, or is the v0.2 plan silently shipping the v0.1 baseline because no one explicitly addressed it?
- Phase 17 (longitudinal pilot) replaces tournament `008` — but does the pilot harness silently re-introduce winner-pick framing through what it captures (e.g., "which lens led to selection most often")? What capture choices implicitly tournament-frame the pilot?

### Dimension D — Self-application gaps

The author explicitly invokes "self-application" as a discipline (METHODOLOGY discipline F). Did the author actually apply the disciplines to their own writing in the same way they applied them to the spike program?

- Did the author paired-review the v0.2 plan before committing it? (No — this audit IS the paired review. The author committed first, audited after. Is that the right order?)
- Did the author pre-register empirical thresholds for the OpenAlex coverage spike (Phase 14 plan 1)? (Audit Phase 14's spike design for pre-registration discipline.)
- Did the author verify load-bearing factual claims against the codebase, or rest on memory? (The Property audit is the reference; check whether the plan's other claims about the codebase have similar verification.)
- Did the author produce calibrated language throughout, or is calibration in closing sections / "Risks" sections only?

### Dimension E — VISION's anti-vision under hostile read

VISION's anti-vision section says the platform is *not* a paper chatbot, RAG wrapper, ranked-list-but-fancier, arxiv-sanity-but-better, leaderboard, generic discovery, or implicit-profile-learning-without-confirmation.

- Does the v0.2 plan covertly slip toward any of these despite the explicit anti-vision? (E.g., is "ranked-list-but-fancier" actually different from "multi-lens with optional fusion" once implemented?)
- Are the differentiations from arxiv-sanity load-bearing, or are they post-hoc rationalizations that won't survive a researcher actually using the tool? (The argument that v0.1 + v0.2 is "not arxiv-sanity-but-better" is asserted in VISION, not argued. Hostile read: it *is* arxiv-sanity-but-better and the differentiation claims are aspirational.)

### Dimension F — Methodology extension scope-creep

The METHODOLOGY.md practice-disciplines extension (committed 2026-04-25) adds six disciplines to a previously-stable six-lens document. Did this extension creep in scope or substance?

- Were these disciplines really lessons from the audit cycle, or were they pre-existing methodological commitments retrofitted as "lessons"?
- Is "pattern-watch with self-application" (discipline F) actually applicable, or is it a meta-discipline that adds no operational guidance and exists only to make the document feel philosophically complete?
- Did adding six practice disciplines change the document's center of gravity from interpretive lenses to operational protocols, possibly making future use of the document more burdensome?

## Output format

Write your audit to `.planning/audits/2026-04-25-v0.2-plan-audit-opus-adversarial.md`. You have Write tool access. Use this structure:

```
---
type: same-vendor-adversarial-audit
status: complete
date: 2026-04-25
target: v0.2 plan + VISION + LONG-ARC + METHODOLOGY (integrated artifact set)
auditor: Claude Opus 4.7 (fresh session, hostile reader)
effort: high
---

# Same-Vendor Adversarial Audit — v0.2 Plan + VISION + LONG-ARC + METHODOLOGY

## Hostile summary

[2-4 sentences naming the strongest adversarial findings]

## Findings by dimension

### Dimension A — Closure pressure recurrence
[hostile findings with file:line citations + confidence + what would have to be true for the finding to dissolve]

### Dimension B — Reverse-engineered necessity
[same]

### Dimension C — Tournament-narrowing / fusion-by-default recurrence
[same]

### Dimension D — Self-application gaps
[same]

### Dimension E — VISION's anti-vision under hostile read
[same]

### Dimension F — Methodology extension scope-creep
[same]

## Steelman residue

[which adversarial frames did less work than they look like they did on first writing — be honest about which attacks weakened on examination, in the spirit of the prior session's Opus adversarial review]

## What survives

[the strongest hostile findings that survived the steelman pass — what should the v0.2 plan author actually do about these]

## What this audit cannot tell you

[bounded scope; same-vendor adversarial reading misses substance the cross-vendor reader catches]
```

## Constraints

- File:line citations for every load-bearing claim. No claims from memory.
- Calibrated language is the default register; rhetorical inflation in *your* writing is also a target. Audit yourself as you go.
- The 2026-04-25 spike paired review's Opus adversarial output is the precedent for what good hostile reading looks like (`.planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md`). Reference its register: numbered sentence-level overstep audit; steelman residue section honest about which frames were weaker than they looked.
- Don't audit code; this is plan-level.
- Don't audit the spike program (005-008); those are out of scope and partially superseded.
- Aim for ~2000-3000 words. The Opus adversarial review on the spike paired review was ~3000 words and is a good benchmark.

Begin.
