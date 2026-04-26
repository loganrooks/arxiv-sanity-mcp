# Wave 5 Cross-Vendor Vocabulary-Mapping Check — 2026-04-26

Pre-Wave-5 step 2 in the dispositioned commit sequence at `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` §7. This is a **focused diagnostic**, not a full re-audit.

## What this is

A narrow cross-vendor read scoped to one diagnostic question: do Claude's α/β/γ/δ shapes for LONG-ARC.md / VISION.md integration (harvest §5.1-5.5) map onto gsd-2's existing `.gsd/` artifact vocabulary (PROJECT.md / DECISIONS.md / KNOWLEDGE.md / RUNTIME.md / STATE.md / ROADMAP.md), or do they require new artifact classes that gsd-2 doesn't currently have?

## What this is not

- Not a re-audit of the harvest. Dispositions accepted in harvest §10 stand unless this check surfaces something materially different.
- Not a critique of Claude's framing-quality.
- Not a full paired audit (single dispatch, not paired with a same-vendor independent reading).

## Pair structure

| Reviewer | Model / effort | Prompt | Output target |
|---|---|---|---|
| Cross-vendor | GPT-5.5 high (codex CLI) | `cross-vendor-vocabulary-prompt.md` | `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md` |

Single dispatch only. Same-vendor independent reading not run because: (i) Claude's harvest already represents Opus's reading; a same-vendor independent read would be a third Opus-shaped voice, not a different perspective. (ii) The diagnostic question is concrete (artifact-vocabulary mapping) and benefits more from a different-vendor concrete-mapping reading than from another same-vendor framing read.

## M1 discipline applied

Forbidden-reading list in the prompt covers the Gemini deep-research doc (framing-misaligned per project's reading-notes), the prior governance synthesis (would prime reader on Claude's framing), and v0.2 plan-audit artifacts (different artifact set).

## Dispatch sequence

1. Dispatching session writes the prompt and this README (this commit).
2. **Fresh session executes `codex exec` with the prompt** per the post-Wave-5-disposition handoff at `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md`.
3. Output lands at `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`.
4. Fresh session reads the output and integrates findings into harvest §10.9 (a brief addendum noting the diagnostic's conclusions) before proceeding to Wave 5 substantive commits.

## Codex-CLI pitfall reminder

Per post-Wave-4 handoff §9: `codex exec --output-last-message <file>` overwrites `<file>` at process exit. **Do NOT co-locate** the agent's apply_patch write target (`.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`) with `-o` capture path. The prompt instructs the agent to write via apply_patch only. If `-o` is used, capture to a different path (e.g., `/tmp/codex-vocab-check.lastmessage`).

## Out of scope for this dispatch

- Anything outside harvest §5 + §11 (the harvest itself is not being re-audited)
- gsd-2 source code (the README is the public artifact; whether it matches actual runtime behavior is unverified)
- Wave 5 substantive AGENTS.md / CLAUDE.md / STATE.md edits (those are Wave 5 commits 1-3, downstream of this diagnostic)
