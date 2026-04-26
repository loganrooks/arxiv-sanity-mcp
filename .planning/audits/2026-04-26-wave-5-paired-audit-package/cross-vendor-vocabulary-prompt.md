# Cross-Vendor Vocabulary-Mapping Check — harvest §5 + §11

## Your role

You are a focused second reader for a governance harvest produced by Claude (Opus 4.7) at `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`. Your job is to answer **one diagnostic question** about §5 (LONG-ARC.md / VISION.md integration) and §11 (candidate uplift primitives soft note).

Working directory: `/home/rookslog/workspace/projects/arxiv-sanity-mcp`

You are running on GPT-5.5 with reasoning effort `high`. Take your time with the artifacts; the cost of a careful diagnostic is acceptable.

## What this is, and what it is not

This is **not** a re-audit of the harvest. The harvest's dispositions have already been accepted by the user; not your concern.

This is **not** a critique of Claude's framing-quality. The harvest's α/β/γ/δ shapes for LONG-ARC/VISION integration are Claude's construction; the question is whether they *map* well onto a different artifact vocabulary, not whether they're well-framed in their own terms.

This **is** a focused diagnostic on a single concrete question (below) before Wave 5 substantive commits land.

## The diagnostic question

The arxiv-sanity-mcp project will mid-horizon migrate from current GSD (`.planning/` directory) to gsd-2 (a coding-agent harness with its own filesystem-driven artifact set, `.gsd/` directory). The migration is "tentative not binding" — Wave 5 governance work is for arxiv-sanity-mcp specifically, but patterns may be referenced when gsd-2 work begins.

**The gsd-2 native `.gsd/` artifact set is** (per gsd-2 README at github.com/gsd-build/gsd-2):

- `PROJECT.md` — what the project is right now
- `DECISIONS.md` — append-only architectural-decision register
- `KNOWLEDGE.md` — cross-session rules and patterns
- `RUNTIME.md` — runtime context (API endpoints, env vars, services)
- `STATE.md` — quick-glance dashboard
- `M001-ROADMAP.md` — milestone plan with slice checkboxes
- `M001-CONTEXT.md` — discuss-phase decisions captured from human dialog
- `M001-RESEARCH.md` — codebase and ecosystem research
- `S01-PLAN.md` — slice task decomposition with must-haves
- `T01-PLAN.md` / `T01-SUMMARY.md` — individual task plan / what-happened
- `S01-UAT.md` — human test script

gsd-2 has **no native artifact class for VISION.md or LONG-ARC.md**.

gsd-2 also auto-loads `AGENTS.md` (with `CLAUDE.md` as a fallback) at user and project levels via the Pi SDK.

**The question:** do Claude's α / β / γ / δ-as-pointer-note shapes (defined in harvest §5.1-5.5; dispositioned in §10.6) map cleanly onto the gsd-2 artifact vocabulary above, or do they require new artifact classes that gsd-2 doesn't currently have?

Specifically:

1. **Shape α — "Doctrine load-points map" in CLAUDE.md.** A short section listing trigger conditions (e.g., "touching ranking code → read LONG-ARC.md anti-patterns + ADR-0001 + ADR-0005"). Where would this content live in the gsd-2 artifact set? Does any existing gsd-2 artifact accommodate routing-by-trigger? Or does this require a new artifact class?

2. **Shape β — "Project-specific anti-patterns to detect" section in AGENTS.md.** ~7 patterns harvested from `LONG-ARC.md:42-54`, each in `pattern → counter-posture` format. Where does this live in gsd-2? AGENTS.md is the natural runtime home (gsd-2 auto-loads it), but does the *content* (anti-patterns) fit any existing gsd-2 artifact's purpose? `KNOWLEDGE.md` ("cross-session rules and patterns") seems closest — is it close enough?

3. **Shape γ — "Deliberation boundaries" section in AGENTS.md.** Listing change-types that should pause-and-surface (modifying ADRs; introducing/removing top-level abstractions; editing LONG-ARC.md / VISION.md; etc.). Is there a gsd-2 artifact for boundary-protocol content? Or is this AGENTS.md-only with no gsd-2 mirror?

4. **Shape δ-as-pointer-note — protected-seams change-control.** A 2-sentence forward-looking pointer in AGENTS.md γ section (deferred placeholder content until v0.2 surfaces ship). Same mapping question — and once v0.2 surfaces ship, where does the populated change-control list belong in gsd-2 vocabulary?

5. **Open: is there a fifth shape Claude didn't construct that maps better onto gsd-2 vocabulary?** For example, if `KNOWLEDGE.md` is the natural home for anti-patterns and `DECISIONS.md` is the append-only ADR register, perhaps the integration is "make LONG-ARC.md content into KNOWLEDGE.md entries and VISION.md content into PROJECT.md augmentations" — losing the standalone documents but gaining native gsd-2-vocabulary fit. Or some other shape entirely.

## What to read

Required:

1. `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` — focus on §5 (Shape α-δ definitions) and §11 (uplift soft note). §10.6 captures Claude's dispositioned reasoning. You may read other harvest sections for context but don't re-audit them.
2. `.planning/LONG-ARC.md` — the file being integrated. Anti-patterns at lines 42-54 are the primary content β surfaces.
3. `.planning/VISION.md` — the file being integrated. Anti-vision section at lines 76-84 is referenced by α.
4. `CLAUDE.md` (project root) and `AGENTS.md` (project root) — current state of the runtime files.

Helpful context (read selectively):

- `.planning/PROJECT.md` — current project identity
- `.planning/spikes/METHODOLOGY.md` — methodology disciplines including M1 at line 112
- `docs/adrs/ADR-0001-exploration-first.md` and `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` — load-bearing ADRs invoked by α load-points

## Forbidden reading (M1 discipline)

You **must not read**:

- The Gemini deep-research doc at `.planning/research/gemini-deep-research/automating-long-term-planning-with-gsd-2.md`. Per the user's read and Claude's reading-notes at `.planning/research/gemini-deep-research/READING-NOTES.md`, the Gemini doc contains a fundamental framing misalignment (it answers "code-patcher built on gsd-2" rather than "extend gsd-2 with VISION/LONG-ARC support"). Reading it would prime your reading.
- `.planning/audits/2026-04-26-governance-audit-synthesis.md` — Claude's prior synthesis. The harvest's dispositions reference it; you should focus on the harvest's content, not the synthesis's framing.
- Any other audit cycle artifacts at `.planning/audits/2026-04-25-*` (v0.2 plan audit cycle) — different artifact set, different framing.

If you find yourself wanting to read one of these to "calibrate," do not. The point of the focused diagnostic is that you produce a reading uncontaminated by Claude's prior framing.

## Output protocol — write-first / verify-last

**First action (before reading anything):** create the output file with a header. Use `apply_patch` to write to:

`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`

Header content:

```markdown
---
type: vocabulary-mapping-check
date: 2026-04-26
vendor: codex (gpt-5.5, reasoning effort high)
prompt: .planning/audits/2026-04-26-wave-5-paired-audit-package/cross-vendor-vocabulary-prompt.md
target_harvest: .planning/audits/2026-04-26-wave-5-exemplar-harvest.md
diagnostic_question: do Claude's α/β/γ/δ shapes map onto gsd-2's `.gsd/` artifact vocabulary, or require new artifact classes?
status: in-progress
---

# Cross-Vendor Vocabulary-Mapping Check (output)

[populating during the run]
```

**Subsequent actions:** update the file via `apply_patch` as you reason through each shape.

**Last action:** `ls -la .planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md` to confirm the file landed on disk.

(This write-first / verify-last protocol is per the project's METHODOLOGY M1 sub-discipline at `.planning/spikes/METHODOLOGY.md:112`. It ensures the file appears on disk independent of the chat-message capture, which is important because of a documented `codex exec --output-last-message` overwrite pitfall — see post-Wave-4 handoff §9. **Do NOT use the `-o` flag co-located with this output path** if the dispatcher set one.)

## Output structure

Write your analysis to the output file with the following sections:

1. **§1 — Per-shape mapping analysis.** For each of α, β, γ, δ-pointer-note (four subsections):
   - Best-fit gsd-2 artifact (if any). Cite the specific artifact name.
   - Quality of fit: `clean` / `partial` / `poor` / `no-fit`.
   - Mismatch nature (if `partial`/`poor`/`no-fit`): what the shape carries that the gsd-2 artifact doesn't accommodate, or vice versa.
   - Concrete recommendation: `keep shape as-designed` / `refactor onto gsd-2 vocabulary` / `create new gsd-2 artifact class` / `hybrid (specify)`.
2. **§2 — Fifth-shape candidates.** Any integration shape Claude didn't construct that you think maps better onto gsd-2 vocabulary. Or `none — Claude's α/β/γ/δ are the right framework for the question as posed`. If you propose a fifth shape, give it a name and a one-paragraph description.
3. **§3 — Where I might be wrong.** Honest acknowledgment. The gsd-2 vocabulary is summarized in this prompt; you have not read the gsd-2 source code or its actual workflow definitions. Recommendations are based on artifact-set descriptions plus what the gsd-2 README publicly documents — not on how the artifacts function in execution.
4. **§4 — Confidence summary.** Per-shape confidence (`low` / `medium` / `high`) and one-line rationale per.
5. **§5 — Update frontmatter.** Change `status: in-progress` to `status: complete` as the final apply_patch step.

Target length: 200-400 lines total. Don't pad; don't truncate. Calibrated language preferred — avoid framing your findings as more confident than they are.

## Reasoning effort

Use reasoning effort `high`. The diagnostic is concrete (artifact-vocabulary mapping) but the implications for both Wave 5 phrasing and any later gsd-2 design are non-trivial.

## Calibrated-language register

The host project uses calibrated language as a default register (per LONG-ARC.md anti-pattern "Closure pressure at every layer"). When stating findings, prefer:

- "fits cleanly" rather than "obviously the right home"
- "appears to require" rather than "requires"
- "the gsd-2 README describes X; whether the runtime actually behaves that way is unverified" rather than "gsd-2 does X"
- "I see no fifth shape; another reader might" rather than "no fifth shape exists"

Confident language is reserved for facts you can directly verify (e.g., from reading current files in the repo).

## Final notes

- This dispatch is part of the Wave 5 pre-commit pipeline. The post-Wave-5-disposition handoff at `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md` (created at the same time as this dispatch package) describes the full pipeline. You don't need to read that handoff for this diagnostic, but it documents the dispatch's place in the larger sequence.
- After your output file is written and your last action is the `ls` verification, the dispatching session integrates findings into the harvest (a brief addendum to §10.9 noting your conclusions) and then proceeds with Wave 5 commits.
- If your diagnostic surfaces a fifth shape or vocabulary mismatch that materially changes the harvest's dispositions, the dispatching session pauses Wave 5 commits and re-dispositions before proceeding. If your diagnostic confirms Claude's α/β/γ/δ are the right framework (or surfaces only minor refinements), the dispatching session proceeds directly to Wave 5 commits.

That's the question, the protocol, and the stakes. Begin.
