---
type: session-handoff
date: 2026-04-26
status: post-Wave-5-disposition (pre-Wave-5-execution)
predecessor: .planning/handoffs/2026-04-26-post-wave-4-handoff.md
purpose: |
  Hand off Wave 5 execution to a fresh session. The Wave 5 dispositioning
  step is complete and committed (harvest §10 disposition record + synthesis
  §4.5 pointer + cross-vendor dispatch package). The execution work — running
  the cross-vendor codex dispatch, integrating any findings, then landing
  Wave 5 substantive commits 1-3 (AGENTS.md / CLAUDE.md / STATE.md) — is the
  fresh session's job per Logan's "wait for fresh session" instruction.

  This handoff is written so a fresh session can execute Wave 5 cold. Prior
  context restoration via the post-Wave-4 handoff is *not* required — that
  handoff is referenced here for cross-references but its content is summarized
  where load-bearing.
onboarding_read_order: |
  Read in this order if starting fresh:
  1. CLAUDE.md (project root) — auto-loaded; establishes project identity
  2. This handoff — full state of play and Wave 5 step-by-step
  3. .planning/audits/2026-04-26-wave-5-exemplar-harvest.md §10 — dispositions
     with full reasoning, assumptions, "where my reasoning may be wrong"
  4. AGENTS.md (project root) — current state of the file Wave 5 will modify
  5. .planning/STATE.md — current project state
  6. .planning/audits/2026-04-26-wave-5-paired-audit-package/cross-vendor-vocabulary-prompt.md
     — the dispatch you'll run as Wave 5 step 1

  Optional (read selectively when relevant to the Wave 5 commit you're about to land):
  - .planning/LONG-ARC.md — anti-patterns at lines 42-54 (load-bearing for AGENTS.md commit)
  - .planning/VISION.md — anti-vision at lines 76-84 (load-bearing for CLAUDE.md commit)
  - docs/adrs/ADR-0001-exploration-first.md — verbatim quote at line 22 (load-bearing for G-D2 fix)
  - docs/05-architecture-hypotheses.md:118-140 — Stack D definition (load-bearing for G-D4 fix)
  - docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md — verify Stack-D foreclosure status hasn't shifted

  Forbidden / not-to-be-treated-as-authority (per harvest §10.11 trust hierarchy):
  - .planning/research/gemini-deep-research/automating-long-term-planning-with-gsd-2.md
    (framing-misaligned per the reading-notes in the same directory)
  - handoff §6 in the post-Wave-4 handoff (CR1-CR5 inventory; per Logan, sourced
    from current GSD audit experience, not gsd-2; not authoritative)
---

# Handoff — Post Wave 5 Disposition (pre-Wave-5-execution)

This document is the durable record of: (a) what's been dispositioned in Wave 5; (b) what's pending and why; (c) the four pre-Wave-5 commits that landed in this session; (d) the step-by-step Wave 5 execution sequence the fresh session will run; (e) what NOT to do; (f) cross-references.

If you are reading this cold (fresh session), read in the order at the top of this file's frontmatter. Sections build on each other.

## 1. Where we are right now

**Date:** 2026-04-26 (post-Wave-5-disposition; pre-Wave-5-execution).

**Branch:** `spike/001-volume-filtering` (~25 commits ahead of origin; not pushed).

**Active work:** Wave 5 of the v0.2 governance-doc audit-cycle sequencing. Wave 5 = exemplar AGENTS.md / CLAUDE.md harvest + deferred-pending-exemplar dispositions (G-D1..G-D4) + the new LONG-ARC.md / VISION.md runtime-integration question Logan raised.

**Wave 5 disposition step is COMPLETE.** All ten substantive items dispositioned (harvest §10). Logan accepted dispositions as Claude recommended; no divergences. Three pre-Wave-5 commits landed in this session:

- `8dc2491` — `docs(audits): record G-D dispositions in Wave 5 exemplar harvest` (the harvest with §10 comprehensive disposition record + §11 candidate-uplift-primitives soft note).
- `985df34` — `docs(audits): point governance synthesis at Wave 5 harvest dispositions` (synthesis §4.5 pointer addendum).
- `076be7e` — `docs(audits): Wave 5 cross-vendor vocabulary-mapping dispatch package` (paired-audit-package directory with prompt + README).

**Wave 5 EXECUTION step is PENDING for fresh session.** The cross-vendor codex dispatch (pre-Wave-5 step 4) and Wave 5 substantive commits 1-3 (AGENTS.md, CLAUDE.md, STATE.md) have not run. Per Logan's "wait for fresh session" instruction, they happen in a clean context window.

**Wave 5 commit 4** (Gemini reading-notes) was committed by Logan during this session at `c7d1346` — already done; not in the fresh session's work.

## 2. Artifact inventory (Wave 5 + relevant prior cumulative)

### 2.1 Wave 5 disposition artifacts (committed in this session)

| Artifact | Path | Commit |
|---|---|---|
| Wave 5 exemplar harvest with §10 disposition record + §11 soft note | `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` | `8dc2491` |
| Governance synthesis §4.5 pointer addendum | `.planning/audits/2026-04-26-governance-audit-synthesis.md` (modified) | `985df34` |
| Cross-vendor dispatch package (prompt + README) | `.planning/audits/2026-04-26-wave-5-paired-audit-package/` | `076be7e` |
| Gemini doc reading-notes | `.planning/research/gemini-deep-research/READING-NOTES.md` | `c7d1346` (Logan-committed earlier in this session) |

### 2.2 Wave 5 execution artifacts (pending — fresh session creates)

| Artifact | Path | Will be created by |
|---|---|---|
| Cross-vendor vocabulary-mapping check output | `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md` | Codex dispatch (Wave 5 step 1) |
| AGENTS.md substantive expansion | `AGENTS.md` (modified) | Wave 5 commit 1 |
| CLAUDE.md targeted additions | `CLAUDE.md` (modified) | Wave 5 commit 2 |
| STATE.md frontmatter currency + post-Wave-5 update | `.planning/STATE.md` (modified) | Wave 5 commit 3 |
| Possibly: harvest §10.9 addendum integrating cross-vendor findings | `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md` (modified) | If dispatch surfaces material findings |

### 2.3 Cumulative prior artifacts (referenced; full inventory in post-Wave-4 handoff §2)

- v0.2 plan synthesis with Wave 1+3 dispositions: `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md` (revised at `931bca1`)
- Governance synthesis with Wave 4 §2.5 G-B dispositions and now §4.5 G-D pointer: `.planning/audits/2026-04-26-governance-audit-synthesis.md`
- Post-Wave-4 handoff (predecessor): `.planning/handoffs/2026-04-26-post-wave-4-handoff.md`
- METHODOLOGY (M1 codified at line 112; reinforced not confirmed by Wave 2 cycle): `.planning/spikes/METHODOLOGY.md`

## 3. Wave 5 dispositions (and why)

All ten dispositions accepted as Claude recommended. Full reasoning lives in harvest §10; this section is a summary.

### 3.1 G-D1 — `AGENTS.md` "Project-specific anti-patterns to detect" section

**Disposition:** shape (a) **with refinement** — verbatim cite-back to `LONG-ARC.md:46-54` per pattern.

**Why:** AGENTS.md is auto-loaded by gsd-2 post-migration (with CLAUDE.md as fallback) per the gsd-2 README. Under current Claude Code, AGENTS.md is convention-loaded. Either way, putting anti-patterns in AGENTS.md is the right placement. Verbatim cite-back makes duplication-drift between AGENTS.md and LONG-ARC.md detectable on next-pass review.

**Patterns to include** (drawn from `LONG-ARC.md:42-54` + the audit-cycle deliberations + the 005-008 lesson):

- Tournament narrowing under "disciplined" framing → rank-and-deprioritize, not eliminate; multi-lens framing replaces winner-pick
- Single-lens "interface" by accident → validate abstractions by shipping a second implementation, per ADR-0005
- Silent defaults → name the reference frame explicitly; require challengers measured against multiple frames or task outcomes
- ADR violation by gradual local-reasonable steps → run an ADR-against-current-work check at deliberation boundaries; ADRs are read at planning time, not just at writing time
- Closure pressure at every layer → calibrated language as default register; flag confident remedies for paired review before adoption
- Embedding-model choice as load-bearing decision → treat embedding-model selection as one lens-design decision among many; most leverage lives upstream
- Single-reader framing claims as authoritative → paired review for framing claims (cross-vendor + same-vendor); consult METHODOLOGY.md

Format: `pattern → counter-posture` (positive declarative). Target ~30 lines, ~7 patterns. If the section grows past ~30 lines it crosses BLOATED_SKILL territory; write tight.

### 3.2 G-D2 — `AGENTS.md` ADR-citation example fix

**Disposition:** shape (a) — verbatim quote + misquote-vs-correct contrast as teaching example.

**Replacement text** (proposed; verify ADR-0001 verbatim before pinning):

> Example (verbatim quote, with deliberate fidelity to the ADR text):
> ADR-0001 states "multiple retrieval and ranking strategies can coexist" — this is a capability commitment about the architecture (the design must support coexistence), not a directive that every project decision *must* engage multiple strategies. Compare to the inflated paraphrase "multiple retrieval/ranking strategies must coexist" — that paraphrase converts a permission into a directive and is therefore inaccurate, even though it sounds more authoritative.

**Verification before commit:** re-read `docs/adrs/ADR-0001-exploration-first.md:22` to confirm verbatim. Currently confirmed in this session as: "multiple retrieval and ranking strategies can coexist" (decision body, line 22).

### 3.3 G-D3 — `CLAUDE.md` restructuring

**Disposition:** shape (a) **full split, lean keep nice-to-have**.

**Mandatory** (do these regardless):

1. Add "Doctrine load-points" section (~8 lines, contingent on α adoption — which is dispositioned). Content per harvest §5.1:

   > **Doctrine load-points** (read the listed document before editing or proposing changes that match the trigger):
   > - Touching ranking, retrieval, or lens-architecture code → `LONG-ARC.md` (anti-patterns), `docs/adrs/ADR-0001`, `docs/adrs/ADR-0005`.
   > - Adding a new abstraction or signal type → `LONG-ARC.md` (protected seams), `VISION.md` (anti-vision section).
   > - Touching MCP tool, resource, or prompt surfaces → `docs/adrs/ADR-0004`, `LONG-ARC.md` (MCP-native operations).
   > - Proposing rights-affecting changes (license, redistribution, content storage) → `docs/adrs/ADR-0003`.
   > - Proposing changes to enrichment cost or scheduling → `docs/adrs/ADR-0002`.
   > - Proposing changes to the spike program structure or methodology → `.planning/spikes/METHODOLOGY.md`, `LONG-ARC.md` (doctrine-interaction-with-spike-program).

2. Fix G-D4 Stack-D line (see §3.4).

**Nice-to-have** (kept per disposition; drop if migration is imminent in days):

3. Replace bare opening line with calibrated-tradeoff preamble (Karpathy-pattern):

   > This file is auto-loaded as runtime context for agents working in this repository. It defines project identity, accepted decisions, and routing pointers — not behavioral discipline (see `AGENTS.md`). The bias is toward stability of decisions already made and explicit pointers for decisions that need to be re-checked. For genuinely trivial tasks, use judgment.

4. Reframe "Key Architectural Constraints" negatives to positive declaratives where feasible. Specifically:
   - "Do not assume tags are canonical / dense retrieval is winner / paper chat is product" → "Treat tags as one signal among several, not the canonical taste primitive; treat dense retrieval as one lens among several, not the default; the product is discovery and triage, not paper-chat"
   - Keep "Do not prematurely commit to a retrieval family" as-is (the negation is the point).

Total CLAUDE.md size target after edits: ~110 lines (from ~80). Net addition: ~30 lines.

### 3.4 G-D4 — `CLAUDE.md` Stack-trajectory line

**Disposition:** shape (a) **with verification step** — re-check Stack-D foreclosure status against ADR-0005 before pinning the gloss.

**Replacement text** (proposed; verify ADR-0005 first):

> **Stack trajectory:** Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). The maximalist Stack D (full local hybrid research platform — see `docs/05-architecture-hypotheses.md:118`) is foreclosed because it commits compute and complexity that v0.x has no evidence to justify; the trajectory remains open if v0.3+ evidence warrants reopening.

**Verification before commit:** read `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` and confirm whether Stack-D's foreclosure rationale has shifted post-redirection. If ADR-0005's compute/complexity ambition has shifted, update the gloss to reflect post-redirection thinking. If not, gloss as proposed.

### 3.5 LONG-ARC.md / VISION.md runtime integration

**Disposition:** **α + β + γ + δ-as-pointer-note**.

- **α — doctrine load-points map** → CLAUDE.md (already covered in G-D3 above).
- **β — anti-pattern self-check** → AGENTS.md (this is G-D1's section, dual-purpose).
- **γ — deliberation-boundary protocol** → AGENTS.md, ~15 lines, with **conditional language ("when X, do Y")** not absolute. Boundaries to enumerate:
  - Reshaping a spike, milestone, or phase plan structurally (not minor edits)
  - Modifying any accepted ADR's text, status, or scope
  - Introducing or removing a top-level abstraction (lens type, signal type, workflow primitive)
  - Changing the MCP tool/resource/prompt surface in ways visible to existing callers
  - Editing LONG-ARC.md, VISION.md, or the project root CLAUDE.md / AGENTS.md
  - Closing an Open Question without a new ADR or explicit Logan confirmation

  For each: state observed problem, proposed change, why now, alternatives considered, expected write set, verification plan (gsd-modifier-style checklist).

- **δ-as-pointer-note** → AGENTS.md γ section, **2 sentences only**:

  > Once v0.2 introduces the Lens interface, signal_type registry, and MCP-tool lens-awareness surfaces, those should be added to a protected-seams change-control list per the discipline above. The list does not yet exist because the surfaces do not yet exist.

**Aggregate-absolute-count concern:** α+β+γ together add ~50 lines across two files. Watch for OVER_CONSTRAINED — if absolutes accumulate past ~15 across both files, the model's reasoning paralyzes. Mitigation: write each item as conditional ("when X, do Y") rather than absolute ("ALWAYS do Y") wherever possible.

## 4. Pending Logan decisions

Wave 5 disposition step is complete. What remains for Logan's input:

1. **Q1 / Q4 / Q16 validation** — orthogonal to Wave 5; tracked in STATE.md Pending Validations table from Wave 4 commit `ee06cc1`. Logan reads `docs/10-open-questions.md` lines 9, 31, 104 and confirms or reopens. No agent work needed.

2. **Whether to bundle handoff commits if cross-vendor dispatch surfaces minor refinements** — if dispatch findings are minor, integrate into the harvest as an addendum and continue. If material, pause and re-disposition with Logan.

3. **Mid-horizon decisions deferred to gsd-2 uplift work** — see post-Wave-4 handoff §6 (Logan's reframe to "tentatively, not binding") and harvest §11 soft note (gsd-2 vocabulary-mapping is open).

## 5. Wave 5 execution sequence (fresh session — start here)

This is the step-by-step. Each step has verification before proceeding.

### Step 1: Cross-vendor vocabulary-mapping dispatch

**Goal:** answer one diagnostic question — "do Claude's α/β/γ/δ shapes for LONG-ARC/VISION integration map onto gsd-2's `.gsd/` artifact vocabulary, or do they require new artifact classes?"

**Command:**

```bash
codex exec \
  -m "gpt-5.5" \
  -c "model_reasoning_effort=\"high\"" \
  --cd /home/rookslog/workspace/projects/arxiv-sanity-mcp \
  --sandbox workspace-write \
  "$(cat /home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/audits/2026-04-26-wave-5-paired-audit-package/cross-vendor-vocabulary-prompt.md)"
```

**Codex-CLI pitfall (per post-Wave-4 handoff §9 + paired-audit-package README):** do **NOT** add `-o` flag co-located with the agent's apply_patch write target (`.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`). The prompt instructs the agent to write via apply_patch. If you want last-message capture, use a different path like `/tmp/codex-vocab-check.lastmessage`.

**Verification:** the agent's last action should be `ls -la .planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`. Confirm the file exists and has `status: complete` in its frontmatter. If the file is missing or empty, recover from `~/.codex/sessions/...rollout-*.jsonl` per the post-Wave-4 handoff §9 recipe (`jq -r '.payload | select(.type=="custom_tool_call" and .name=="apply_patch") | .input'`).

**After dispatch returns:**

1. Read the output file `.planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md`.
2. Commit the output: `git add .planning/audits/2026-04-26-wave-5-paired-vocabulary-check.md && git commit -m "docs(audits): record Wave 5 cross-vendor vocabulary-mapping check output"`.
3. Decide based on findings:
   - **If findings are minor** (no fifth shape; minor mapping clarifications): add a brief addendum to harvest §10.9 noting the diagnostic's conclusions. Commit. Proceed to Step 2.
   - **If findings are material** (fifth shape proposed; significant vocabulary mismatch): pause. Surface to Logan with a focused summary. Do NOT proceed to Wave 5 substantive commits without Logan's re-disposition.

### Step 2: Wave 5 commit 1 — AGENTS.md substantive expansion

**Pre-flight verification:**

- Re-read `docs/adrs/ADR-0001-exploration-first.md:22` to confirm verbatim quote: should be "multiple retrieval and ranking strategies can coexist" (currently confirmed; ADR could change between now and execution).
- Re-read `LONG-ARC.md:42-54` to confirm anti-pattern fidelity. The patterns listed in §3.1 of this handoff are drawn directly from there.
- Re-read `.planning/spikes/METHODOLOGY.md:112` to confirm M1 description (used in the "single-reader framing claims as authoritative" anti-pattern).

**Edits to make** (in one commit):

1. Add new section "Project-specific anti-patterns to detect" with the 7 patterns from §3.1, each with verbatim cite-back like `(LONG-ARC.md:46, "silent defaults")`.
2. Fix the ADR-citation example per §3.2.
3. Add "Deliberation boundaries" section per §3.5 γ (with conditional language; ~15 lines).
4. Add the δ-pointer-note 2-sentence forward-looking note within the γ section per §3.5 δ.
5. Reframe the "Do not do these things" section to positive declarative where feasible (operational items only; the philosophical ones like "do not assume tags are canonical" remain useful negations).

**Post-flight verification:**

- `wc -l AGENTS.md` — confirm not bloated past ~250 lines.
- Count absolutes (MUST/ALWAYS/NEVER) across α+β+γ — if >~15, rewrite to conditionals.
- `git diff` — review for clarity and adherence to dispositions.

**Commit message:**

```
docs(governance): expand AGENTS.md with anti-patterns, deliberation boundaries, and corrected ADR-citation example

Wave 5 commit 1 of 3 per harvest §7. Implements:
- G-D1: new "Project-specific anti-patterns to detect" section (7 patterns
  with verbatim cite-back to LONG-ARC.md:42-54)
- G-D2: ADR-citation example fixed to use ADR-0001 verbatim "can coexist"
  with misquote-vs-correct contrast as teaching demonstration
- γ: new "Deliberation boundaries" section listing change-types that
  pause-and-surface (conditional language to avoid OVER_CONSTRAINED)
- δ-as-pointer-note: 2-sentence forward-looking note within γ signaling
  protected-seams change-control intent for v0.2-surfaces-not-yet-shipped
- Positive-declarative reframing of operational "Do not" items

See .planning/audits/2026-04-26-wave-5-exemplar-harvest.md §10.2, §10.3,
§10.6 for full reasoning, assumptions, and "where my reasoning may be
wrong" per disposition.
```

### Step 3: Wave 5 commit 2 — CLAUDE.md targeted additions

**Pre-flight verification:**

- Re-read `docs/05-architecture-hypotheses.md:118-140` to confirm Stack-D gloss is faithful (currently confirmed: "Stack D — Full local hybrid research platform" defined at line 118, recommendation in line 140).
- Re-read `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md` and **verify Stack-D foreclosure status hasn't shifted post-redirection**. ADR-0005 is the v0.2 commitment; if its compute/complexity ambition has expanded in ways that re-open Stack-D, the gloss must reflect that.

**Edits to make** (in one commit):

1. Add doctrine load-points section per §3.3 mandatory item 1 (~8 lines).
2. Fix G-D4 Stack-D line per §3.4 (gloss with definition + pointer; ~2 lines).
3. **Nice-to-have** (drop only if you're told migration is imminent in days): replace bare opening line with calibrated-tradeoff preamble per §3.3 nice-to-have item 3. Reframe "Key Architectural Constraints" negatives to positive declaratives where feasible per §3.3 nice-to-have item 4.

**Post-flight verification:**

- `wc -l CLAUDE.md` — confirm not bloated past ~120 lines.
- `git diff` — review.

**Commit message:**

```
docs(governance): add doctrine load-points, fix Stack-D silent default, calibrated preamble

Wave 5 commit 2 of 3 per harvest §7. Implements:
- α: new "Doctrine load-points" section listing trigger conditions and the
  doctrine document to read for each (LONG-ARC, VISION, ADRs 0001-0005)
- G-D4: Stack-D line glossed with definition + pointer to docs/05:118
  (verified against ADR-0005 status; foreclosure rationale unchanged
  post-redirection [or: updated to reflect ...])
- G-D3 nice-to-have: calibrated-tradeoff preamble (Karpathy-pattern) +
  positive-declarative reframing of "Key Architectural Constraints"
  operational items

See .planning/audits/2026-04-26-wave-5-exemplar-harvest.md §10.4, §10.5,
§10.6 for full reasoning per disposition.
```

### Step 4: Wave 5 commit 3 — STATE.md update

**Edits to make** (in one commit):

1. Update frontmatter `last_updated` to current ISO timestamp.
2. Update `last_activity` to summarize Wave 5 completion.
3. Update `stopped_at` to indicate Wave 5 substantive commits landed.
4. Update Pending Todos to remove Wave 5 items now complete; add any new pending items surfaced.
5. Update Session Continuity to point to a future post-Wave-5-execution handoff (or leave pointing to this handoff if no further session is queued).

**Verification:** test count (~493) and tool count (13) unchanged (v0.2 implementation hasn't started; nothing in Wave 5 modifies code).

**Commit message:**

```
docs(state): post-Wave-5 STATE.md update — frontmatter currency + Wave 5 closeout

Wave 5 commit 3 of 3 per harvest §7. Records Wave 5 completion in STATE.md:
frontmatter currency, pending-todos collapse for Wave 5 items, session
continuity points forward.
```

### Step 5: Optional — write a post-Wave-5-execution handoff

If Logan doesn't immediately queue follow-on work and a clean break is warranted, write a brief post-Wave-5-execution handoff at `.planning/handoffs/2026-04-26-post-wave-5-execution-handoff.md` (or `2026-04-27-` if it slips a day). The handoff inventories the Wave 5 commits + cross-vendor output, notes the next horizon (gsd-2 uplift work or Q1/Q4/Q16 validation or other), and points future sessions at the right starting place.

If Logan immediately queues the next work, skip this step and just update STATE.md per Step 4.

## 6. What the next session should NOT do

- **Do not re-litigate Wave 5 dispositions.** They are accepted per harvest §10. New evidence (e.g., the cross-vendor diagnostic surfacing a fifth shape) can prompt re-disposition; absent that, dispositions stand.
- **Do not skip the cross-vendor dispatch.** Logan considered skipping and reversed ("alright then lets still do it"). The dispatch is part of Wave 5 execution.
- **Do not co-locate the codex agent's apply_patch write target with `-o` capture path.** Per post-Wave-4 handoff §9 documented pitfall.
- **Do not start gsd-2 uplift work as part of Wave 5.** That's mid-horizon, separate initiative. Wave 5 is governance edits to arxiv-sanity-mcp specifically.
- **Do not treat the Gemini deep-research doc as authority.** Per `.planning/research/gemini-deep-research/READING-NOTES.md`: factually largely accurate on gsd-2 mechanisms, framing-misaligned on the actual question, LLM-eval specifics unverified.
- **Do not treat handoff §6 of the post-Wave-4 handoff as authority** for gsd-2 intervention surfaces. Per Logan's flag, sourced from current GSD audit experience, not gsd-2; not a complete or accurate inventory.
- **Do not bundle Wave 5 commits.** Logan said "separate" for the disposition commits and the same discipline applies to execution: AGENTS.md is one commit, CLAUDE.md is another, STATE.md is a third. If the cross-vendor dispatch surfaces an addendum to the harvest, that's its own commit.
- **Do not let aggregate absolute-count exceed ~15 across α+β+γ in AGENTS.md and CLAUDE.md combined.** Use conditional language ("when X, do Y") wherever possible.
- **Do not exceed target line counts** without explicit reason (~250 for AGENTS.md, ~120 for CLAUDE.md). If your draft is over, tighten before commit.
- **Do not commit `.planning/config.json`** unless Logan asks. It's been modified by some other process; not in Wave 5 scope.
- **Do not skip pre-flight verification.** Each commit's pre-flight is mandatory: re-read the source files cited in the edits to confirm verbatim fidelity. The G-D2 fix turned on this exact discipline.

## 7. Tensions surfaced (preserve as choice-points)

These are not commitments; they are choice-points the fresh session should preserve.

### 7.1 G-D3 nice-to-have keep-vs-drop

Disposition is "lean keep nice-to-have." Tension: under post-migration gsd-2, CLAUDE.md becomes fallback (not primary auto-load). Nice-to-have additions are durable Karpathy-pattern but their primary-runtime value diminishes. **If migration is imminent in days, drop nice-to-have.** If weeks-to-months, keep. The fresh session should ask Logan if migration timing has clarified before committing the nice-to-have additions.

### 7.2 Cross-vendor diagnostic — what counts as "material findings" warranting pause

If the diagnostic surfaces a fifth shape that Claude didn't construct, that's clearly material — pause, surface to Logan, re-disposition. If the diagnostic notes minor mapping clarifications (e.g., "α fits KNOWLEDGE.md cleanly post-migration; current placement in CLAUDE.md is fine for current Claude Code runtime"), that's minor — integrate as addendum to harvest §10.9 and proceed.

The boundary: **does the finding change a disposition, or does it confirm/refine one?** Changes warrant pause; refinements proceed.

### 7.3 Cross-vendor codex availability

Codex CLI is at `/home/rookslog/.npm-global/bin/codex` version 0.125.0 (verified in this session). The dispatch in Step 1 assumes `gpt-5.5` is the model identifier and `model_reasoning_effort=high` is the config key. If those fail, check `codex exec --help` and adjust. Logan has run prior codex dispatches (Wave 2 cross-vendor); auth is presumed working.

## 8. Methodology notes (this cycle)

These are operational lessons from doing the Wave 5 disposition cycle. Worth preserving for the next paired-audit cycle and for the gsd-2 uplift work.

### 8.1 Recommendation churn as a signal

Across this session Claude moved on the cross-vendor-audit recommendation **four times** (skip → do-it → skip → do-it). Recorded in harvest §10.9 as the "recommendation-churn observation." The lesson: when Claude moves on an item each turn, that's a confidence signal — not a sign of careful re-evaluation. Logan's intermittent overrides resolved the churn by selecting a baseline. **Future practice:** if Claude flips on an item more than twice in a session, surface the flip-flop explicitly to the user as a confidence-instability flag rather than continuing to re-recommend.

### 8.2 Calibration errors recorded

Two specific errors in this cycle, recorded in harvest calibration_note and §10.12:

1. **Date-arithmetic error:** Claude called arXiv IDs `2604.03447` and `2602.07609` "future-dated" when today is 2026-04-26 (April 26, 2026); YYMM.NNNNN format makes 2604.xxxxx current-month. Logan caught this.
2. **Pi SDK / RTK called invented:** Claude called these "confabulated" before Logan provided the gsd-2 README which verified both as real (Pi SDK at github.com/badlogic/pi-mono; RTK at github.com/rtk-ai/rtk).

**Pattern:** Claude over-discounted real items by lumping them with correctly-flagged invented claims (like the "PluginEval" framework from a different research doc). Mitigation going forward: use "unverified" rather than "confabulated" when web access is unavailable for verification.

### 8.3 The "include everything" instruction shaped harvest §10's length

Logan instructed: "include everything, even the assumptions, cross-cutting concerns and the 'where I might be wrong' etc." Harvest §10 grew to ~370 lines as a result. Future readers should treat §10 as a comprehensive disposition record, **not as a template suggesting all dispositions need to be this long**. For routine dispositions, the Wave 4 §2.5 pattern (~15-30 lines per item) is the default.

### 8.4 Closure-pressure-at-meta-layer recurred

Producing a tidy harvest with shape (a)/(b)/(c) per item and a single recommended combination was itself the closure-pressure pattern the audit cycle keeps surfacing. Recorded in harvest §6.5 and §10.12. **No mitigation succeeded fully.** The honest acknowledgment is that closure pressure recurs at the meta-layer regardless of how often we name it; the only counter is staying alert to "if a recommended shape feels obviously right on first read, slow down."

## 9. Cross-references

### 9.1 Wave 5 (this cycle)

- Harvest with §10 disposition record + §11 soft note: `.planning/audits/2026-04-26-wave-5-exemplar-harvest.md`
- Synthesis §4.5 disposition pointer: `.planning/audits/2026-04-26-governance-audit-synthesis.md`
- Cross-vendor dispatch package: `.planning/audits/2026-04-26-wave-5-paired-audit-package/`
- Gemini doc reading-notes: `.planning/research/gemini-deep-research/READING-NOTES.md`
- This handoff: `.planning/handoffs/2026-04-26-post-wave-5-disposition-handoff.md`

### 9.2 Source documents (read-targets per onboarding)

- LONG-ARC anti-patterns: `.planning/LONG-ARC.md:42-54`
- VISION anti-vision: `.planning/VISION.md:76-84`
- METHODOLOGY (M1 at line 112): `.planning/spikes/METHODOLOGY.md`
- Stack A/B/C/D definitions: `docs/05-architecture-hypotheses.md:59-140`
- ADR-0001 verbatim text: `docs/adrs/ADR-0001-exploration-first.md:22`
- ADR-0005 multi-lens substrate: `docs/adrs/ADR-0005-multi-lens-v0.2-substrate.md`
- Current CLAUDE.md (project root): `CLAUDE.md`
- Current AGENTS.md (project root): `AGENTS.md`
- Current STATE.md: `.planning/STATE.md`

### 9.3 Predecessor handoffs and synthesis

- Post-Wave-4 handoff (predecessor): `.planning/handoffs/2026-04-26-post-wave-4-handoff.md`
- Post-Wave-2 handoff (further predecessor): `.planning/handoffs/2026-04-26-post-wave-2-handoff.md`
- Governance synthesis: `.planning/audits/2026-04-26-governance-audit-synthesis.md`
- v0.2 plan synthesis: `.planning/audits/2026-04-25-v0.2-plan-audit-synthesis.md`

### 9.4 Tools

- Codex CLI: `/home/rookslog/.npm-global/bin/codex` (v0.125.0)
- Custom subagent definition (used in Wave 2, available for future paired audits): `~/.claude/agents/adversarial-auditor-xhigh.md`

## 10. Quick-reference: commit SHAs (Wave 5 only)

In chronological order on `spike/001-volume-filtering`:

| SHA | Description |
|---|---|
| `c7d1346` | docs(reading-notes): add comprehensive reading notes for automating long-term planning with gsd-2 (Logan-committed; includes the Gemini doc itself + reading-notes) |
| `8dc2491` | docs(audits): record G-D dispositions in Wave 5 exemplar harvest |
| `985df34` | docs(audits): point governance synthesis at Wave 5 harvest dispositions |
| `076be7e` | docs(audits): Wave 5 cross-vendor vocabulary-mapping dispatch package |
| (pending) | docs(handoff): post-Wave-5-disposition handoff (this commit) |

Plus all prior commits per post-Wave-4 handoff §12 (Wave 1 + Wave 3 + Wave 4 + post-Wave-4 currency commits).

## 11. The single highest-priority action for the next session

**Run the cross-vendor codex dispatch per §5 Step 1 above.** Its output informs whether Wave 5 substantive commits proceed directly or pause for re-disposition.

If the dispatch's findings are minor: integrate as harvest §10.9 addendum, then proceed through Wave 5 commits 1-3 (AGENTS.md, CLAUDE.md, STATE.md) per §5 Steps 2-4. Each commit has pre-flight and post-flight verification; do not skip.

If the dispatch's findings are material: pause, surface to Logan, re-disposition. Do not commit Wave 5 substantive edits without Logan's re-disposition.

After Wave 5 commits 1-3 land, write a brief post-Wave-5-execution handoff or update STATE.md only — Logan's call on whether next horizon (gsd-2 uplift / Q1-Q4-Q16 validation / other) is queued immediately.

---

*Single-author handoff written 2026-04-26 by Claude (Opus 4.7) at Logan's direction. Subject to the same fallibility caveat as the Wave 4 governance synthesis revision (synthesis §2.5 footer). If any disposition becomes contested in execution, harvest §10 records full reasoning for re-evaluation.*
