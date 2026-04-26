---
type: research-reading-notes
date: 2026-04-26
target_artifact: automating-long-term-planning-with-gsd-2.md
status: as-of 2026-04-26 — supersede with a re-run reading-note if research is re-run with sharper prompt
provenance: produced by Claude (Opus 4.7) under Logan's direction during the Wave 5 exemplar harvest 2026-04-26; recorded as part of the harvest's dispositioned package per `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` §10.10
---

# Reading notes — Gemini deep-research doc on gsd-2 long-term planning

This file accompanies `automating-long-term-planning-with-gsd-2.md` so a future session picking up that doc cold has explicit framing context. Without these notes, a careless reader risks treating the doc's framing as authoritative.

## Verifiable facts the doc gets right (per gsd-2 README)

The Gemini doc accurately describes several real gsd-2 mechanisms. These are confirmed by the gsd-2 README at github.com/gsd-build/gsd-2 (provided by Logan 2026-04-26):

- **Pi SDK** is real (https://github.com/badlogic/pi-mono) — gsd-2 is built on it.
- **RTK** is real (https://github.com/rtk-ai/rtk) — gsd-2 provisions a managed RTK binary for shell-output semantic compression.
- **Worktree isolation, TOCTOU ancestry guard, atomic sync-lock with PID-verified stale override, GIT_DIR / GIT_INDEX_FILE / GIT_WORK_TREE stripping** — all real per v2.78 changelog "Major git-safety pass."
- **The auto-loop dispatch pipeline / fresh-session-per-unit / context pre-loading / complexity-based routing with token profiles** — real per README "How It Works" section.
- **AGENTS.md auto-loaded by Pi core (with CLAUDE.md as fallback) at user and project levels** — real per README "Agent Instructions" section. Directly relevant to the Wave 5 governance work.

## Where the doc's framing is misaligned

Per Logan's read 2026-04-26: the Gemini doc answers "how to architect a code-patcher built on gsd-2" rather than "how to extend gsd-2 with VISION.md / LONG-ARC.md support." The title — "Architecting a Mid-Horizon Automated Patcher: Extending the GSD-2 Framework for Long-Term Planning and Calibration Drift Mitigation" — reveals the misframing: it treats "patcher" as a code-modification tool that uses gsd-2's framework, not as the act of patching gsd-2 itself to add long-horizon-planning workflows.

Practical consequence: most of the doc's §6 (Plandex AST mapping, Ralph Loop, Gas Town orchestration, the 13-step auto-loop pipeline as architecture for a patcher) is about a code-patching tool, not about extending gsd-2's workflow surfaces. Treating those sections as gsd-2 design specifications would propagate the misframing.

## What is unverified (not "confabulated" — distinct claims to flag)

The doc cites specific LLM-evaluation mechanisms with specific quantified claims that I cannot verify without web access:

- **TRACE framework** (cited as `arxiv.org/html/2604.03447v1`) with detection-rate claims (67-94% on explicit doc bugs; drops 7-42 points on silent implementation drift). The arXiv ID 2604.03447 is current-month (today is 2026-04-26; YYMM.NNNNN format makes 2604.xxxxx April 2026), not future-dated; the paper may exist. I cannot verify either way.
- **SAFi framework** with specific Exponential Moving Average decay 0.9 and cosine-distance drift detection. Cited via Reddit thread; specific mechanism unverified.
- **LLM ADR-violation paper** at `arxiv.org/html/2602.07609v1`. Same calibration as TRACE — current-month arXiv ID, may exist, unverified.

Honest stance: these are **unverified**, not "confabulated." Earlier in the harvest deliberation I called them confabulated based on a date-arithmetic error (treating 2604.xxxxx as future-dated when it is current-month) and a calibration-pattern overreach (lumping unverified specifics with my correctly-flagged invented claims like the "PluginEval" framework from a different research doc). Logan caught the calibration error; this note records the correction.

## What carries genuine value despite the misframing

- **Schema validation by independent convergence.** The doc's proposed VISION.md schema (Platform Identity / Divergence / Anti-Vision) and LONG-ARC.md schema (Protected Seams / Anti-Patterns / Explicit Non-Decisions) match what the project independently constructed. Weak external validation; mildly increases confidence that the schemas are durable rather than arxiv-sanity-mcp idiosyncrasies.
- **Two-stage compliance-audit pattern** (cheap LLM screens, high-tier validates). Workflow-primitive idea relevant to gsd-2 uplift later, not to Wave 5 content. The M1 paired-review discipline (METHODOLOGY.md:112) gestures toward similar shape.
- **Artifact-level trust reasoning** (TRACE framing, regardless of whether the specific paper exists). Distinguishing "doc says X" from "code shows X" and weighting code higher in conflicts is what the project's CONTEXT.md epistemic discipline already does (source-traceable vs artifact-reported vs derived). Re-articulation; nothing structurally new.

## Disposition for use

Treat the doc as **input, not authority**, for any future gsd-2 design conversation. Specifically:

- The factual descriptions of gsd-2 mechanisms are largely accurate; cross-check against README before relying on a specific claim.
- The framing ("architect a code-patcher") is misaligned with the actual gsd-2-extension question; do not import the framing.
- The LLM-evaluation specifics (TRACE, SAFi) are unverified; do not treat their specific numbers as ground truth without independent verification.
- The doc's CR1-CR5 references reproduce the same mappings as handoff §6 (which Logan flagged as not authoritative and possibly mis-sourced from current-GSD audit experience). Treat with corresponding caution.

## When to re-run

Consider re-running the deep research with a sharper prompt that distinguishes "patch gsd-2 to add long-horizon planning workflows" from "build a code-patcher tool." The current doc's title and §6 indicate the prompt didn't make this distinction sharply. A sharper prompt with explicit examples ("we want to know how to extend gsd-2's `.gsd/` artifact set to natively support VISION.md and LONG-ARC.md as first-class artifact classes; we are *not* asking how to build a tool that modifies code") may produce a more directly useful output. If re-run, supersede this reading-note with a fresh one dated to the re-run.

## Cross-references

- Source doc: `.planning/research/gemini-deep-research/automating-long-term-planning-with-gsd-2.md`
- gsd-2 README (verification source): github.com/gsd-build/gsd-2 (provided by Logan in conversation 2026-04-26; not committed to repo)
- Wave 5 exemplar harvest: `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` §10.10 (where this reading-notes file's creation was dispositioned)
- Handoff §6 (also misaligned per Logan): `.planning/handoffs/2026-04-26-post-wave-4-handoff.md`
- Other deep-research docs in this directory: `agent-configuration-best-practices-research.md`, `claude-code-and-agent-configuration-guide.md` (calibration patterns may apply similarly; not separately reviewed)
