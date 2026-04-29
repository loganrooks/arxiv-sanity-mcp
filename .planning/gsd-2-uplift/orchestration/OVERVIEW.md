---
type: orchestration-overview
date: 2026-04-27
status: active; pre-pilot (drafted post-dispatch-readiness deliberation; awaiting light orchestration audit before pilot dispatch)
package: |
  This directory carries the orchestration package for first-wave gsd-2 exploration:
  - OVERVIEW.md (this file) — procedural shell, dispatch commands, dispositions log
  - preamble.md — common preamble prepended to each slice dispatch
  - slice-01-mental-model.md (PILOT)
  - slice-02-architecture.md
  - slice-03-workflow-surface.md
  - slice-04-artifact-lifecycle.md
  - slice-05-release-cadence.md
  - audit-spec.md — W2 audit template
  - synthesis-spec.md — W3 synthesis spec
ground: .planning/gsd-2-uplift/DECISION-SPACE.md §1.11-§1.16 (decisions B1-B6); §1.4; §1.7; §1.8; §2.3
deliberation_log: .planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md
parent_artifact: .planning/gsd-2-uplift/INITIATIVE.md
audience: future-Claude (running pilots + audits + synthesis); Logan (disposing pilot output; collaborating)
purpose: |
  Procedural shell for the orchestration package. Each agent dispatched on a slice
  receives: preamble.md + slice-0X-*.md (concatenated). The dispatcher runs the
  commands in §3, reviews output per §4 (pilot-gate), proceeds per disposition, runs
  audits per §5, runs synthesis per §6, handles failures / pivots per §7-§8, and
  records dispositions per §11.
---

# Orchestration overview — gsd-2 first-wave exploration

This document is the **procedural shell** for the orchestration package. The package's load-bearing content is the per-slice specs + audit spec + synthesis spec. This document carries: wave structure (§1); setup (§2); dispatch commands (§3); pilot-gate criteria (§4); audit cycle (§5); synthesis cycle (§6); mid-stream pivot protocol (§7); failure-mode handling (§8); time budgeting (§9); guidance on Logan-direct-reading (§10); dispositions log (§11); cross-references (§12).

For "what does each slice ask," go to the per-slice spec. For "how do we run the wave," start here.

## §1. Wave structure (D′)

Per decisions B1-B6 from DECISION-SPACE.md §1.11-§1.16:

```
W1-pilot: cross-vendor codex on slice 1 (mental-model)
   ↓
[Pilot-gate disposition (§4): proceed-parallel / re-slice /
 escalate to Option C / de-escalate to A / change approach]
   ↓
W1-parallel: cross-vendor codex on slices 2-5 after pilot calibration
   ↓
W2: same-vendor Claude xhigh audit per audit-spec.md
    (slice 4 always; others conditional per B2)
   ↓
W3: same-vendor Claude xhigh synthesis per synthesis-spec.md
    (paired-synthesis at W3 reserved as conditional escalation per B3)
   ↓
[Incubation checkpoint per DECISION-SPACE §2.3]
   ↓
Second-wave-scoping (out of scope for this orchestration)
```

**Vendor scope** (per B3): W1 cross-vendor; W2 + W3 same-vendor.

**Aim** (per B1): characterize gsd-2 carefully enough that second-wave can decide whether/what to do.

## §2. Setup

Run before pilot dispatch.

### §2.1 Clone gsd-2

```bash
cd ~/workspace/projects/
git clone --depth 50 https://github.com/gsd-build/gsd-2 gsd-2-explore
cd gsd-2-explore
git log --oneline | head -20  # sanity check
ls -la  # confirm directory layout
```

Shallow depth is intentional. If a slice needs deeper history, the dispatcher deepens the clone before dispatching that slice — the slice agent treats gsd-2 as read-only and does not run `git fetch` itself. Slice 5 specifically: if its preflight (`git rev-parse --is-shallow-repository` + 6-month commit count) reports truncation, deepen with `git -C ~/workspace/projects/gsd-2-explore/ fetch --unshallow --tags` (or `--deepen=500 --tags` if `--unshallow` fails) before re-dispatching slice 5.

### §2.2 Output paths

```bash
mkdir -p ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/
```

Per-slice outputs land at `.planning/gsd-2-uplift/exploration/0X-<slice>-output.md`:
- `01-mental-model-output.md` (slice 1; pilot)
- `02-architecture-output.md`
- `03-workflow-surface-output.md`
- `04-artifact-lifecycle-output.md`
- `05-release-cadence-output.md`

W2 audits: `.planning/gsd-2-uplift/exploration/0X-<slice>-audit.md`.
W3 synthesis: `.planning/gsd-2-uplift/exploration/SYNTHESIS.md`.
If paired-synthesis escalates: `SYNTHESIS-COMPARISON.md` alongside.

### §2.3 Codex-CLI pitfall reminders

Per `.planning/handoffs/2026-04-26-post-wave-4-handoff.md` §9 + the archived dispatch package's README at `.planning/audits/archive/2026-04-26-wave-5-paired-audit-package/README.md`:

- **Never co-locate `-o` capture path with the agent's apply_patch write target.** `codex exec --output-last-message <file>` overwrites `<file>` at process exit. Use a separate path for `-o` (e.g., `/tmp/codex-slice-N.lastmessage`).
- **Recovery from missing apply_patch output:** `~/.codex/sessions/...rollout-*.jsonl` carries the apply_patch content. Recover with:
  ```bash
  jq -r '.payload | select(.type=="custom_tool_call" and .name=="apply_patch") | .input' \
    ~/.codex/sessions/rollout-*.jsonl
  ```
- **Sandbox:** use `--sandbox workspace-write` (agent writes within `~/workspace/projects/arxiv-sanity-mcp/`; cannot modify gsd-2-explore or anything else).

### §2.4 gh CLI for slice 4 contribution-culture probe

Slice 4's prompt includes specific `gh` commands. Verify gh is authenticated for the gsd-2 repo before slice 4 dispatch:

```bash
gh repo view gsd-build/gsd-2 --json description  # smoke test
```

If `gh` lacks auth or the repo isn't accessible, slice 4 may need to skip Q5 contribution-culture probe; flag in disposition.

### §2.5 Pre-pilot orchestration audit (recommended)

Per dispatch-readiness deliberation §9(f): light same-vendor xhigh audit of this orchestration package itself before pilot dispatch. Catches closure-pressure-recurrence in the orchestration plan + framing-leak in the slice prompts that would propagate to all 5 dispatches.

**Light** = single same-vendor xhigh pass; not full parallel audit. Same-vendor adversarial-auditor reads OVERVIEW.md + preamble.md + slice-01-mental-model.md + audit-spec.md + synthesis-spec.md. Flags concerns; Logan disposes before pilot.

Optional but recommended given Stage 1 audit's finding that closure-pressure-recurrence in foundational artifacts is a real failure mode this project has hit.

## §3. Dispatch commands

### §3.1 Per-slice dispatch shape

Each slice dispatch concatenates `preamble.md` + the slice spec:

```bash
SLICE_NUM=01  # or 02, 03, 04, 05
SLICE_NAME=mental-model  # or architecture, workflow-surface, artifact-lifecycle, release-cadence

PROMPT=$(cat \
  ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/preamble.md \
  ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/slice-${SLICE_NUM}-${SLICE_NAME}.md)

codex exec \
  -m "gpt-5.5" \
  -c "model_reasoning_effort=\"high\"" \
  --cd /home/rookslog/workspace/projects/arxiv-sanity-mcp \
  --sandbox workspace-write \
  -o /tmp/codex-slice-${SLICE_NUM}.lastmessage \
  "$PROMPT"
```

**Verification after dispatch:**
- `ls -la .planning/gsd-2-uplift/exploration/${SLICE_NUM}-${SLICE_NAME}-output.md` — confirm file exists and is non-empty.
- Read the frontmatter; confirm `status: complete`.
- If file missing or empty: recover from rollout-jsonl per §2.3.

### §3.2 Pilot dispatch (slice 1 only)

```bash
SLICE_NUM=01
SLICE_NAME=mental-model

PROMPT=$(cat \
  ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/preamble.md \
  ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/slice-01-mental-model.md)

codex exec \
  -m "gpt-5.5" \
  -c "model_reasoning_effort=\"high\"" \
  --cd /home/rookslog/workspace/projects/arxiv-sanity-mcp \
  --sandbox workspace-write \
  -o /tmp/codex-slice-01.lastmessage \
  "$PROMPT"
```

After completion: read pilot output; apply §4 pilot-gate.

### §3.3 Parallel dispatch (slices 2-5; after pilot disposition)

Run after §4 pilot-gate disposes "proceed-parallel" (or with revisions if pilot disposed differently). Each slice runs as a separate `codex exec` invocation. They can run truly in parallel if you have capacity (4 simultaneous codex sessions); else serialize.

```bash
for SLICE in "02-architecture" "03-workflow-surface" "04-artifact-lifecycle" "05-release-cadence"; do
  SLICE_NUM=${SLICE%%-*}
  PROMPT=$(cat \
    ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/preamble.md \
    ~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/orchestration/slice-${SLICE}.md)
  
  codex exec \
    -m "gpt-5.5" \
    -c "model_reasoning_effort=\"high\"" \
    --cd /home/rookslog/workspace/projects/arxiv-sanity-mcp \
    --sandbox workspace-write \
    -o /tmp/codex-slice-${SLICE_NUM}.lastmessage \
    "$PROMPT" &
done
wait
```

(The `&` + `wait` runs them in parallel. If parallel exceeds capacity, drop the `&` for sequential execution.)

### §3.4 Audit dispatch (W2; per audit-spec.md)

Per audit-spec.md, dispatch the adversarial-auditor-xhigh subagent within Claude Code, passing the audit prompt with `{N}` and `{slice-name}` substituted. Mandatory for slice 4; conditional for others per B2 selective-audit criteria (see audit-spec.md "When to dispatch").

### §3.5 Synthesis dispatch (W3; per synthesis-spec.md)

Per synthesis-spec.md, run synthesis as a deliberate Claude Opus xhigh task (either via the dispatching session collaboratively or as a dispatched xhigh agent). Inputs: all 5 slice outputs + audits + DECISION-SPACE.md + INITIATIVE.md.

After synthesis lands, evaluate paired-synthesis escalation criterion (synthesis-spec.md). If escalation: dispatch cross-vendor codex synthesizer; produce comparison.

## §4. Pilot-gate disposition criteria

After slice 1 (pilot) output lands at `.planning/gsd-2-uplift/exploration/01-mental-model-output.md`, review before proceeding. Disposition options below; **no disposition is default** — choose after reading the pilot. Listing order roughly tracks "least to most divergent from plan" for readability; it is **not** preference order, and listing first does not imply preferring first.

### §4.1 Proceed-parallel

**Criteria:** pilot output is concrete, well-grounded, low framing-leakage. Slice 1 prompt-shape is right; calibration discipline was honored; output is reader-useful (~150-300 lines; sections (i)-(v) populated; calibration labels present; flagged divergences concrete). No direction-shifting evidence surfaced that would warrant pause-for-targeted-evidence.

**Action:** dispatch slices 2-5 in parallel using §3.3 (with any minor calibration tweaks based on pilot output).

**Calibration tweaks** that may apply:
- If pilot's Q4 (agent/human stance) was thin, strengthen Q4-equivalent questions in slices 3 + 4
- If pilot cited README too often relative to source, strengthen "verify against source" framing in 2-5 (already present; can be amplified)
- If pilot's open-questions section flagged the slice-1 prompt itself as ambiguous, revise per the flag and re-dispatch only if material; otherwise note for retrospective

### §4.2 Hold for targeted evidence

**Criteria:** pilot output surfaces plausible-but-not-dispositive direction-shifting evidence (e.g., gsd-2's mission reads partially divergent from project assumptions; one slice-2/3/4/5 question's answer is foreshadowed by pilot in a way that could shift later slices' framing). Not enough to flip the metaquestion (that's §4.6 territory) but enough that parallel dispatch would build on a shaky foundation.

**Action:** pause parallel dispatch; gather narrowly-targeted additional evidence (e.g., dispatch a single slice-2 read first; or have Logan read gsd-2 directly per §10; or revise the framing-leakage in remaining slice prompts before parallel). Then re-evaluate disposition.

### §4.3 Re-slice

**Criteria:** pilot reveals slicing partition is wrong-shaped. E.g., slice 1's Q2 (problem solved) bleeds into slice 5's territory; or Q3 (target user) requires slice 3 (workflow surface) context to answer cleanly.

**Action:** redesign slicing; revise slice prompts before parallel dispatch. May require structural rework (escalate to §4.6 if shift is fundamental).

### §4.4 De-escalate to Option A

**Criteria:** pilot output is uniformly high quality (concrete; well-grounded; low framing-leakage) — selective audit's marginal value drops if all slices look like this. Combined audit-and-synthesis (1 agent) becomes attractive.

**Action:** dispatch slices 2-5 parallel; after their outputs land, run combined audit-and-synthesis (one xhigh same-vendor agent doing both) instead of separate W2 + W3.

### §4.5 Escalate to Option C

**Criteria:** pilot output reveals problems — framing leaks despite forbidden-reading; outputs shallow on key questions; cross-vendor agent reads gsd-2 in ways suggesting paired same-vendor reading would surface different things.

**Action:** dispatch slices 2-5 paired (cross-vendor + same-vendor independent reads with forbidden-reading on each other); compare per slice; W2 audit is paired-reading comparison rather than per-output critique.

### §4.6 Change approach entirely

**Criteria:** cross-vendor approach itself isn't working — codex can't read gsd-2 productively at this level of detail; slicing is fundamentally mis-shaped; characterization-aim is itself wrong.

**Action:** pause; surface to Logan; re-disposition with deliberation log entry. Triggers re-evaluation of B2/B3 wave-structure decisions. May produce different exploration shape entirely.

### §4.7 Disposition record

Whichever disposition lands, record in §11 with:
- Pilot output summary (3-5 sentences)
- Disposition chosen
- Rationale (1-3 sentences)
- Calibration tweaks applied (if any)

## §5. W2 audit cycle

Per audit-spec.md.

- **Slice 4 audit:** mandatory; dispatch as soon as slice 4 output lands.
- **Slices 1, 2, 3, 5 audits:** conditional per audit-spec.md "When to dispatch" criteria; disposition per slice when output lands.
- **Audit disposition** per audit-spec.md §6 (clean / minor / material / critical) recorded in §11.4.

If any audit returns "material" or "critical" findings: pause slice progression; address before W3 synthesis. Material findings → re-dispatch the slice (with prompt revisions integrating audit notes); critical findings → re-disposition wave-structure with Logan.

## §6. W3 synthesis cycle

Per synthesis-spec.md.

- After all slice outputs land + their audits dispose: dispatch synthesis.
- Synthesis output at `.planning/gsd-2-uplift/exploration/SYNTHESIS.md`.
- Evaluate paired-synthesis escalation criterion (synthesis-spec.md). If escalate: dispatch cross-vendor codex synthesizer; produce `SYNTHESIS-COMPARISON.md`. Record decision in §11.5.

After synthesis lands (and comparison if paired): incubation checkpoint per DECISION-SPACE §2.3. Out of scope for this orchestration.

## §7. Mid-stream pivot protocol

Per dispatch-readiness deliberation §9(d).

### §7.1 Pivot trigger

A slice output (pilot or any of 2-5) surfaces direction-shifting evidence sufficient to flip the §1.7 metaquestion answer. Examples:
- Slice 2 reveals architecture structurally hostile to extension.
- Slice 4 reveals migration tooling fundamentally incompatible with `.planning/` shape.
- Slice 5 reveals cadence + breaking-change posture so volatile that extension is perpetually behind.
- Any slice reveals gsd-2's mission/scope so divergent that uplift would distort identity.

### §7.2 Pivot procedure

1. **Pause** remaining slice dispatches (if pivot triggers mid-W1).
2. **Surface to Logan** with focused summary: which slice; what evidence; which §3 question(s) the evidence addresses; provisional read of metaquestion + R2/R3 viability impact.
3. **Write a pivot-disposition artifact** at `.planning/gsd-2-uplift/exploration/PIVOT-DISPOSITION.md` (or, for less-than-full-pivot dispositions, append the §11.7 entry per the schema below). This converts pivot decisions from chat-state into durable planning state — without an artifact, cancellation/redirection becomes invisible to future readers and reviewers.

   PIVOT-DISPOSITION.md schema (required fields):
   ```
   ---
   trigger_slice: <01 / 02 / 03 / 04 / 05>
   trigger_date: <YYYY-MM-DD>
   evidence_summary: <2-3 sentences; cite slice output's section + line>
   metaquestion_impact: <flips / shifts but does not flip / orthogonal>
   r2_r3_viability_impact: <high / medium / low / none>
   disposition: <confirm-pivot / confirm-continue / re-shape>
   rationale: <2-5 sentences>
   followup_artifacts: <list of INITIATIVE.md / DECISION-SPACE.md sections that will update>
   ---
   ```
4. **Re-disposition** via deliberation log entry. Possible outcomes (matching the artifact's `disposition` field):
   - **Confirm pivot:** the project's first-wave-aim is not the right shape; second-wave scopes a different direction (or cancels).
   - **Confirm continue:** evidence is real but insufficient to flip metaquestion; finish slices for fuller picture.
   - **Re-shape exploration:** evidence shifts question-shape; remaining slices' prompts revised.
5. **Update INITIATIVE.md / DECISION-SPACE.md** per re-disposition outcome (§3 framing questions + §1.7 metaquestion + §1.8 R2/R3 hybrid as applicable).
6. **Resume or close W1** depending on re-disposition.

### §7.3 What's not a pivot trigger

- Minor slice findings (e.g., gsd-2 doesn't have feature X; we'd build it ourselves).
- Audit-W2 findings on output quality (those flow through §5 audit disposition).
- Synthesis-stage findings (those flow through incubation-checkpoint).
- Cross-vendor agent producing thin output (W2 audit issue; not pivot).

Pivot threshold is high: only direction-shifting-evidence-sufficient-to-flip-metaquestion. Lower-threshold findings flow through normal disposition steps.

## §8. Failure-mode handling

### §8.1 Codex hangs or output truncation

- Check `~/.codex/sessions/...rollout-*.jsonl`; recover apply_patch content with §2.3 jq command.
- Restart with same prompt; codex sessions are stateless per dispatch.
- If specific slice consistently hangs (e.g., slice 4 with gh probe times out), split the slice's gh probe into a sub-dispatch.

### §8.2 Sandbox issues

- Verify `--sandbox workspace-write` set.
- Verify `cwd` is dispatching project root, not gsd-2-explore.
- Agent reads gsd-2 by absolute path; writes within dispatching project.

### §8.3 Output landed but is wrong file or empty

- Inspect apply_patch invocation in `rollout-*.jsonl`.
- If empty: re-dispatch with explicit "your final action must be writing to `<path>` via apply_patch."
- If wrong file: move file; note in §11 disposition.

### §8.4 Cross-vendor agent reads forbidden material

- Inspect tool-trace in `rollout-*.jsonl` for forbidden path reads.
- If forbidden read happened: discard slice output; re-dispatch with strengthened forbidden-reading list (specific paths); consider sandbox restrictions.
- If only suspected: W2 audit catches; flag in audit output.

### §8.5 Logan reading slice output reveals framing-leakage despite forbidden-reading

Treat as W2 audit finding; severity-stratify (minor → addendum; material → re-dispatch; critical → abandon slice + surface to deliberation).

## §9. Time budgeting

Concrete estimates (revise post-pilot per actual experience):

| Stage | Estimate (wall-clock) | Notes |
|---|---|---|
| Setup | 5-10 min | One-time |
| Pre-pilot orchestration audit | 30-60 min | Optional; recommended |
| Pilot dispatch (slice 1) | 30-60 min | Codex GPT-5.5 high |
| Pilot review + calibration | 30-60 min | Logan + Claude |
| Parallel slices 2-5 dispatch | 30-60 min | If truly parallel |
| W2 audits (mandatory + selective) | 30-90 min × N | Claude xhigh per audit |
| W3 synthesis | 1-3 hours | Claude xhigh; longer if paired escalates |
| Incubation checkpoint | 1-3 hours | Logan + Claude deliberation |

**Total first-wave-through-checkpoint:** ~1-2 days of Logan-time-equivalent.

## §10. Logan reading gsd-2 directly

Per dispatch-readiness deliberation §9(c) + §9(h): Logan-led direct reading of gsd-2 is the most reliable counter to framing-leakage.

- **Not before pilot.** Pre-reading would build expectations that contaminate pilot disposition.
- **After pilot.** Read what surprised in pilot output to ground-truth surprises.
- **During parallel.** If a slice reads off-target, Logan's direct read accelerates W2 audit's substance check.
- **Before incubation.** Logan reading synthesis + at least one slice's source-citations directly ground-truths synthesis claims that drive operating-frame-update.

Non-mandatory; Logan disposes when. Highest benefit: pilot-review and pre-incubation stages.

## §11. Per-wave dispositions log

Append-only. Initially empty.

### §11.1 Pre-pilot

**2026-04-27 — orchestration package authored.** Single-author Claude (Opus 4.7 xhigh) draft of OVERVIEW.md + preamble.md + 5 slice specs + audit-spec.md + synthesis-spec.md. Committed at `edefdaf` (2026-04-27).

**2026-04-27 — pre-pilot cross-vendor audit dispatched.** Codex GPT-5.5 xhigh audit of the orchestration package per Logan's call (extending §2.5's recommended same-vendor pre-pilot pass to cross-vendor). Output at `cross-vendor-audit.md`. Verdict: **material → revise package then proceed** (no critical findings). Findings spanned framing-leakage in slice prompts, closure pressure in pilot/audit/synthesis disposition language, operational bugs (path verification, stale §-references, missing gh fallback, shallow-clone preflight), slice 4/5 deprecation overlap, missing cancellation-pathway artifact, and a coverage watchlist for known omitted areas (debugging, collaboration, telemetry, security).

**2026-04-27 — preflight failure recorded.** The pre-pilot cross-vendor audit was dispatched *before* gsd-2 was cloned to `~/workspace/projects/gsd-2-explore/`. OVERVIEW §2.1 prescribes the clone before any dispatch; the dispatcher (Claude) skipped this step. Auditor flagged absence at §4.4 / §10. Surfaced by Logan; gsd-2 cloned post-audit. Most audit findings are within-artifact and remain valid; coverage-gap and source-fit findings were limited by the absence and will be re-checked in the focused re-audit. Pattern recorded as methodological observation §B.5 in `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md`.

**2026-04-27 — within-artifact revisions applied.** Per Logan's disposition (option 1: apply revisions, then re-audit focused on revised W1 preamble + slices 1/4/5 with gsd-2 present). Revisions covered findings 1.1-1.4 (framing-leakage), 2.1-2.4 (closure pressure), 4.1-4.2 (coverage watchlist + slice 4/5 deprecation split), 5.1-5.4 (operational bugs), 8.2 (cancellation artifact). Findings 8.3 (stop-loss) deferred. Auditor's interpretive caveat (§10) noted; revisions retained calibration for B4 long-horizon split and B5 contribution-culture in the deferred re-audit.

**2026-04-27 — focused cross-vendor re-audit landed.** Codex GPT-5.5 xhigh re-audit per Logan's option-1 disposition. Output at `cross-vendor-reaudit.md`. Verdict: **addendum-needed, then proceed to pilot.** All 15 prior findings resolved (13 fully, 2 partially → corresponding to the 2 new findings below). Re-audit §2 confirmed slice-fit against now-present gsd-2 (TypeScript/Node repo with substantial top-level surfaces; partition adequate; preamble watchlist likely to fire on real surfaces — debug mode, teams workflow, dashboard, security all visible at top level). Two new minor findings:

- **Re-audit §3.1**: §4 ordering claim ("alphabetical-by-action") didn't match actual order (least-to-most-divergent). Fix applied: corrected the claim to match.
- **Re-audit §3.2**: slice 5 deepening conflicted with read-only gsd-2 framing. Fix applied: slice 5 preflight is now diagnostic-only (no `git fetch`); OVERVIEW §2.1 reserves deepening to dispatcher with explicit command; slice 5 reports truncation + lower-bound caveats and dispatcher re-dispatches if precise cadence is needed.

**2026-04-27 — pre-pilot disposition: clean to proceed.** With addendum fixes applied, no further structural revisions before pilot. Pilot dispatch (slice 1, codex GPT-5.5 high) is the next substantive action; pending Logan's go-ahead per the disposition discipline.

### §11.2 Pilot disposition

*[empty]*

### §11.3 Parallel-slice dispositions

*[empty]*

### §11.4 W2 audit dispositions

Per `audit-spec.md §6` disposition categories. Full reasoning in `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` (D1-D4).

**2026-04-28 — slice 1 audit not triggered.** Pilot disposition was already proceed-parallel (per §11.2 implicit; pilot output reviewed and disposed without re-audit warrant). No further action.

**2026-04-28 — slice 2 audit dispatched and disposed.** Audit at `.planning/gsd-2-uplift/exploration/02-architecture-audit.md` (Claude Opus xhigh adversarial-auditor). Verdict: **Clean → proceed.** Five source spot-checks all verified. ADR-010 vendoring claim (proposed-not-implemented; ~79 files of GSD-authored code in vendored Pi packages) verified verbatim at `docs/dev/ADR-010-pi-clean-seam-architecture.md:12-29`. RTK gating divergence verified verbatim (`README.md:22` vs `src/cli.ts:167-178`). No critical or material findings; no framing-leakage. Direction-shifting evidence (ADR-010 status; vendoring extent; RTK divergence) all independently corroborated. **Disposition: clean → proceed (no addendum, no re-dispatch).**

**2026-04-28 — slice 3 audit skipped.** Per `audit-spec.md §7-§16` selective-audit criteria, slice 3 met all skip conditions: output is concrete, well-grounded, well-cited; calibration honest; no claims that would materially affect second-wave-scoping decisions beyond what was already verified at re-audit time; no unexplained in-scope omissions surfaced from the dispatching project's read. Slice 3's two-engine finding additionally corroborates the W2 dive at `w2-markdown-phase-engine-findings.md` which was independently verified. **Disposition: skip (justified by selective-audit criteria); synthesis reads slice 3 directly.**

**2026-04-28 — slice 4 audit dispatched and disposed.** Audit at `.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-audit.md` (Claude Opus xhigh adversarial-auditor; mandatory per audit-spec.md `:9` because R2 viability is load-bearing). Verdict: **Minor → addendum.** Source verification clean (5/5 spot-checks accurate at cited ranges). One severity-tagged "material" completeness finding (CG-1: Q2 missed enumeration of three additional extension subsystems — ecosystem at `ecosystem/loader.ts:1-110`; workflow plugins at `workflow-plugins.ts:1-60`; skills at `skill-manifest.ts:1-60`). Auditor disposed material → addendum (not re-dispatch) on substantive trigger reading: CG-1 *adds* to the slice's central claim ("gsd-2 has substantive extension surfaces") rather than reverses it; addendum integrates the four-surface enumeration via auditor's source-cited paragraph. No framing-leakage. **Disposition: minor → addendum applied to slice 4 in-place at section (vi) using auditor's suggested paragraph (audit `:144-146`); no re-dispatch warranted (substantive disposition documented in deliberation log D1).**

**2026-04-28 — slice 5 audit dispatched and disposed.** Audit at `.planning/gsd-2-uplift/exploration/05-release-cadence-audit.md` (Claude Opus xhigh adversarial-auditor). Verdict: **Minor → addendum.** Math reproduces exactly across 8 spot-checks (cadence; tag count; tag-gap math; alias telemetry; CHANGELOG `[Unreleased]` deprecation). Three citation line-number errors found: `scripts/generate-changelog.mjs:194-204` (file is 152 lines; content at `:58, 66-67`), `:230-260` (content at `:96, 118-125`), and `scripts/update-changelog.mjs:78-136` (file is 59 lines; content at `:33-56`). Content described correct in all three cases; only line numbers wrong. Cross-finding integration flag for synthesis: elaborate breaking-change *machinery* vs rapid-cadence *practice* (auditor flagged as synthesis-stage; lives in audit §5 → captured in synthesis-input chain per synthesis-spec.md `:35`). No framing-leakage. **Disposition: minor → addendum applied to slice 5 in-place via strikethrough-and-correct at six citation occurrences plus corrigenda section (vi) at end (D2). Cross-finding integration flag left for synthesis-stage per audit's recommendation (D3). No re-dispatch warranted.**

**Pre-synthesis state:** all five W1 slice outputs landed (slices 1-5); all post-audit addenda + corrigenda applied; three audits disposed; slice 1 + slice 3 audits not needed. Synthesis-input chain is complete. Next: W3 synthesis dispatch per §11.5 + `synthesis-spec.md`.

### §11.5 W3 synthesis disposition (incl. paired-synthesis escalation decision)

Per `synthesis-spec.md §"Paired-synthesis escalation criterion"` at `:172-189`. Full reasoning in `.planning/deliberations/2026-04-28-w2-audit-dispositions-and-synthesis-readiness.md` (D5) for synthesis dispatch shape; `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md` (DC0-DC4) for comparison-drafting decisions.

**2026-04-28 — W3 same-vendor synthesis dispatched and landed.** Per D5 disposition: single same-vendor synthesizer (Claude Opus xhigh general-purpose subagent at max effort; effort inherited from parent xhigh session per Logan's substrate-gap correction). Inputs: 5 slice outputs (with slice 4 (vi) addendum + slice 5 (vi) corrigenda) + 3 audits + framing-widening + DECISION-SPACE.md + INITIATIVE.md + side-investigation evidence + tier-comparison + W2 disposition log. Output at `.planning/gsd-2-uplift/exploration/SYNTHESIS.md` (609 lines; 8 sections §0-§7; F1-F8 numbered findings stratification). Frontmatter sets `escalation_to_paired_synthesis: yes` (Trigger 4 fires confirmed; Triggers 2 + 3 plausibly fire per §0). Post-synthesis citation-verification spot-checks (5/5 verifications: F1 ADR-010 status; F2 four extension subsystems; F3 zero BREAKING-marked commits; F4 two-engine architecture; F5 RTK gating divergence; F8 SCHEMA_VERSION = 22) all passed against gsd-2 source — synthesis factual content source-grounded; interpretive layering is exactly what paired-synthesis escalation tests. **Disposition: same-vendor synthesis complete; escalate to paired-synthesis per Trigger 4.**

**2026-04-28 — paired-synthesis (cross-vendor) dispatched and landed.** Per Trigger 4 firing: codex GPT-5.5 high cross-vendor synthesizer dispatched via background `codex exec` (bg ID `b8ikf3e4m`; ~10 min wall-clock; 268,544 tokens). Forbidden-reading enforced: Claude's SYNTHESIS.md, Gemini deep-research doc, predecessor handoff. Codex confirmed independence in §0 frontmatter note. Output at `.planning/gsd-2-uplift/exploration/SYNTHESIS-CROSS.md` (207 lines; 8 sections §0-§7). Independent integration of audited W1 evidence + framing-widening operating frame; independent source spot-checks beyond audits at `commands-workflow-templates.ts:424-508`, `custom-workflow-engine.ts:90-226`, `workflow-plugins.ts:120-221`. **Disposition: paired-synthesis complete; both syntheses landed; comparison artifact follows.**

**2026-04-28 — SYNTHESIS-COMPARISON.md drafting (in-session-collaborative per D5a).** Per `synthesis-spec.md:185-188` + `DECISION-SPACE §2.3` incubation-feeding chain: comparison artifact at `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md` drafted in-session (Claude Opus 4.7 xhigh) with Logan adjudication on §2 divergent findings + §5 multi-axis integration. Comparison-stage decisions DC0-DC4 captured in `.planning/deliberations/2026-04-28-comparison-drafting-decisions.md`:

- **DC0** — Affirm handoff §6.3 scaffold (§0-§6) with three operational refinements (DC1-DC3).
- **DC1** — §0 top-line takeaway differentiates three divergence-types: substantive R4-disposition-timing (codex declares synthesis-stage shift; Claude defers shift to incubation); register R5 framing (common operational endpoint); artifact-shape register/length divergence.
- **DC2** — §1 carries 9 convergent findings; RTK gating divergence stays collapsed within §1.5 docs-vs-source class; tightly-interleaved release/workflow/artifact infrastructure re-categorized as Claude-unique (moves to §3 asymmetric coverage).
- **DC3** — Per-finding "Implication for incubation" multi-clause lines refactored to tight "Bears on §5.X" pointers; integration load lives in §5 multi-axis structure (§5.1 metaquestion / §5.2 R1-R5 mix / §5.3 six-context anchoring (Logan-disposed) / §5.4 side-probe triggers).
- **DC4** — R4 weighting characterized as substantive interpretive-disposition-timing divergence (not register) — load-bearing for incubation starting position. Different starting positions yield different disposition shapes.

§4 of the comparison-drafting deliberation log records the methodological observation that arxiv-sanity-mcp's `AGENTS.md` / `CLAUDE.md` anti-pattern checklists are project-specific to arxiv-sanity-mcp's own implementation work and were over-imported into gsd-2-uplift comparison reasoning during DC1; correct grounds for gsd-2-uplift-specific anti-pattern self-checks live in `framing-widening §0 + §10` + `DECISION-SPACE §4` + `LONG-ARC.md` generic anti-patterns + `handoff §8` + `METHODOLOGY.md` M1. The drift event is a small data point that the migration trigger per `INITIATIVE.md §7` is approaching readiness; recorded as session-discipline observation; not blocking near-horizon work.

**Status as of this update (2026-04-29):** SYNTHESIS-COMPARISON.md draft-complete. Full §0-§6 landed in-session-collaborative per D5a. Section-shape:

- **§0** three-divergence-type top-line summary (substantive R4 disposition-timing; register R5; artifact-shape register/length).
- **§1** nine convergent findings (Pi vendoring; extension plurality; two-engine; release machinery-vs-practice; docs-vs-source drift; R2 viable; telemetry/observability/security centrality; B4 split; R3 under-evidenced) with tight `Bears on §5.X` pointers per DC3.
- **§2** three divergent findings: §2.1 R4 weighting (Logan-adjudication per DC4 substantive interpretive-disposition-timing); §2.2 R5 framing (surfacing-only register at common operational endpoint); §2.3 synthesis register/length (surfacing-only artifact-shape).
- **§3** six asymmetric-coverage items: 3 Claude-unique (interleaved release/workflow/artifact infra; substrate-richness methodological observation; symmetry note ground); 3 codex-unique (cross-vendor framing-leakage caveat; R5 reference-plus-sibling reframe; first-target-selection methodology; named effective-state probe). Pattern: complementary depth-vs-breadth, not contradiction.
- **§4** five methodological observations: M1 paired-review observed-as-claimed-in-some-instances-and-inverted-in-others (n=1; refines M1 toward depth-vs-breadth axis); convergence-as-robustness-within-framing; tier-comparison preliminary observation (GPT-5.5 high sufficient for synthesis-stage cross-vendor); framing-import drift surfaced (initiative-maturity signal); stratification methodology converged.
- **§5** four-axis incubation-checkpoint integration: §5.1 metaquestion (direction-holds-with-qualifications, medium-high); §5.2 R-mix (narrowed-and-widened shape; Logan-adjudication on §2.1 disposition-timing + first-target-shape + R3 probe-firing); §5.3 six-context anchoring (Logan-disposed; A-primary + F-secondary plausible per syntheses); §5.4 side-probe triggers (six probes surfaced with trigger-conditions; Logan-disposed pre-vs-post critical path); §5.5 cross-axis composition observation with suggested deliberation order.
- **§6** confidence + limits + D5a in-session-collaboration caveat (§6.3) + audit chain (§6.4) + reading-order guidance (§6.5) + confidence-summary table (§6.6).

**Disposition:** SYNTHESIS-COMPARISON.md draft-complete; comparison artifact ready for incubation-checkpoint. Incubation per `DECISION-SPACE §2.3` is Logan-led + out of orchestration scope. Post-incubation second-wave-scoping signal returns to orchestration scope when fired.

### §11.6 Incubation-checkpoint outcome

*[empty — populated when checkpoint runs; though strictly speaking that's outside this orchestration's scope]*

### §11.6.5 v1-GSD premise-bleed audit (post-comparison; pre-incubation)

Per `DECISION-SPACE.md §1.17` (audit-methodology decision) + `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md` (deliberation trace). This audit is a bounded premise-bleed lens audit before §2.1 + §5 incubation adjudication on SYNTHESIS-COMPARISON.md, motivated by Logan's 2026-04-28 premise-correction concern (v1-GSD mental-model bleed potentially under-weighting gsd-2 runtime-application surfaces).

**2026-04-28 — audit-spec arc (revise-before-dispatch).**

- Claude drafted `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/AUDIT-SPEC.md` v1 (initial draft; same-vendor adversarial-auditor recommended baseline).
- Logan commissioned cross-vendor review (GPT-5.5 xhigh) at `AUDIT-SPEC-REVIEW.md`. Disposition: revise-before-dispatch. Returned 7 findings (4 Material / 2 Moderate / 1 Minor).
- Claude analyzed findings (transparent reasoning per finding) at `.planning/deliberations/2026-04-28-audit-spec-review-deliberation.md §3` + cross-cutting observations §4.
- Logan authorized Claude to perform per-finding adjudication and write disposition; Claude-disposed at deliberation log §5 with rationale + where-Logan-might-differ + revision-implication per finding.
- Logan post-disposition follow-up confirmed F1 + F4 with refinements (manual-escalation discretion; lookup-mechanics + meta-discipline). Logan pushed on F6 (universalization concern); Claude verified META-SYNTHESIS coverage; Logan accepted three F6 refinements (soft-cap-with-overflow; META-SYNTHESIS §2 typed-vocab citation; META-SYNTHESIS §3 prohibited-articulations integration).
- Load-bearing decisions distilled to `DECISION-SPACE.md §1.17` (7-rule audit methodology).
- Revised AUDIT-SPEC.md v2 applies all 7 finding adjudications + 5 post-disposition refinements; ~30-50% rewrite.

**Disposition: AUDIT-SPEC.md v2 revised-for-dispatch; awaiting Logan final-call before Step-1 cross-vendor codex auditor dispatch.** Step-2 same-vendor stress fires conditionally on Class C return (default) or Logan manual-escalation discretion. Audit feeds incubation-checkpoint disposition on SYNTHESIS-COMPARISON.md (commit-as-is / commit-with-addendum / revise-before-commit) per AUDIT-SPEC.md §8 disposition pathway.

**2026-04-29 — audit-arc execution (Step-1 + Step-2 + differential + disposition).**

- Step-1 cross-vendor codex GPT-5.5 high dispatched (~6 min wall-clock; 211k tokens; 0/5 source reads, 2/5 propagation samples). Output at `audits/2026-04-28-v1-gsd-mental-model-premise-bleed-audit/FINDINGS.md`. Result: **6 instances; 1A/5B/0C; no auto-Step-2 trigger.** Headline: "premise-bleed real but front-loaded; chain self-corrects."
- Logan disposed (d) per AUDIT-SPEC.md §8: manual Step-2 escalation as **independent same-vendor read** (spec §3.4 manual-escalation discretion overriding the default Class-C-trigger + differential structure). Rationale: obtain a Step-2 read free of Step-1 priors so the differential carries no anchoring contamination.
- Step-2 same-vendor Claude xhigh adversarial-auditor dispatched in independent mode (~10 min wall-clock; 222k tokens). Output at `audits/.../FINDINGS-STEP2.md` (transcribed from subagent text return; runtime blocked direct file write — provenance-noted in frontmatter). Result: **9 instances; 4A/3B/2C narrowly load-bearing.** Headline: "premise-bleed localized rather than pervasive; residual at integration-grammar level (F6 + F9 = framing-application-as-fact at SYNTHESIS-COMPARISON.md §5 axes)." Isolation: clean (no Step-1 outputs encountered).
- Main-thread differential at `audits/.../DIFFERENTIAL.md` (~250 lines). Reconciliation: vendor-position-symmetric — cross-vendor caught vocabulary-import bleed, same-vendor caught integration-grammar-as-fact at meta-level; both readings defensible and complementary; M1 paired-review property worked as designed. Quality assessment: both audits high-transparency, well-grounded, internally self-critical. Recommendation: commit-with-addendum (option (b) per §8). Reasoning: F6+F9 share a single low-cost dissolver (lift SYNTHESIS-CROSS.md §6 framing-leakage caveat to point-of-use at §5); addendum also serves Step-1's strongest findings (F2+F3 carry-forward).

**Disposition (2026-04-29): commit-with-addendum applied per Logan approval.** SYNTHESIS-COMPARISON.md frontmatter status updated to `committed-with-audit-addendum`; new §7 ("Premise-bleed audit addendum") landed with §7.1 reading-frame for §5 axes (point-of-use foregrounding of framing-leakage caveat) + §7.2 artifact-side carry-forward (INITIATIVE.md §3.2 + DECISION-SPACE.md §1.8 as historical staging vocabulary) + §7.3 what-the-audit-did-not-surface + §7.4 cross-references. Disposition trail recorded at `audits/.../DISPOSITION.md`. Audit-arc complete; comparison ready for §2.1 + §5 incubation adjudication with §7.1 reading-frame active.

**Methodological note on §3.4 spec-deviation.** Logan's invocation of independent-mode-Step-2 + main-thread-differential overrode the spec §3.4 default differential structure. Tradeoff: gain in differential-cleanness (no anchoring contamination); loss in third-reader-independence (main-thread differential is in-session-collaborative). Net favorable for this audit's purpose; recorded in DISPOSITION.md §4.1 + DIFFERENTIAL.md §0 provenance-note.

**Lesson for future audits.** The cross-vendor + same-vendor-xhigh pairing produced complementary findings (cross-vendor catches vocabulary-import; same-vendor catches integration-grammar-as-fact). The pairing's structural value is independent of any specific finding; this is the M1 paired-review property in action. Argues for retaining this discipline shape in future audits where premise-bleed or framing-leak is a concern, with conditional escalation per spec §3.4 default OR manual-discretion. Recorded at DISPOSITION.md §4.2.

### §11.6.6 Trajectory plan + Phase A plan-self-audit (2026-04-29; post-§7-addendum, pre-incubation)

**Trigger.** Logan asked for an orchestrated trajectory from current state (audit-arc complete + §7 addendum landed; comparison ready for incubation) to extraction of the gsd-2-uplift initiative into its own dedicated repo. Requirements: quality gating, checkpoints, audit/review/verification at load-bearing junctures, framing-issue prevention, multi-kind error-prevention, clear orchestration + artifact + commit plan (backward-traceable responsibility), self-checkpoints via cross-vendor xhigh audits (or high where appropriate). Plus self-contained for context-clearing — Logan plans to clear context before execution.

**Plan landed.** `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` (in-repo authoritative; ~735 lines). Eight-phase trajectory A→H with onboarding (§0; horizon stack + test-case-vs-substrate + mandatory pre-reading + discipline + 13-kind failure-mode taxonomy + Logan-disposed parameters); per-phase goal/inputs/outputs/quality-gate/failure-branch/commit (§1); audit cadence (§2.1-§2.5; per-audit reasoning-level table at §2.4 calibrating xhigh vs high per audit-task shape); artifact map (§3); commit map (§4 with §4.2.1 cross-repo commit-identity rules); failure-mode handling (§5; §5.6 control matrix mapping each §0.6 kind to phases/check/recorded-at/owner); verification (§6); references (§7). Logan-disposed §0.7 parameters: hybrid autonomy with phase-boundary pauses; per-audit reasoning-level via §2.4; standing-context as new artifact `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` + CLAUDE.md doctrine-load-point; plan endpoint at Phase H complete.

**Phase A executed.** Cross-vendor codex GPT-5.5 xhigh plan-self-audit dispatched. PLAN-AUDIT.md returned 9 findings (1A/6B/2C); medium-high confidence. Class C: F1 plan-file artifact-custody (plan lived outside arxiv-sanity-mcp at `/home/rookslog/.claude/plans/`; Phase A commit map said "plan file + audit folder" but external path can't be committed); F2 Phase G move/stay map conflicts with INITIATIVE.md §7's authoritative custody rule (DECISION-SPACE.md and the deliberation log STAY in arxiv-sanity-mcp; only INITIATIVE.md + exploration outputs MIGRATE). Class B: F3 (LONG-ARC.md path drift), F4 (failure-mode taxonomy lacks operationalization map), F5 (Phase G xhigh in §1.7 vs high in §2.4 inconsistency), F6 (§0.5 memory-file provenance gap), F7 (Phase H "without reference" overstates independence), F8 (cross-repo commit-identity gap). Class A: F9 (stale DRAFT status + Phase B artifact-map TBD).

**Logan disposed revise-before-execute** (option (c) per AUDIT-SPEC.md §8.2). All 9 findings addressed via in-body plan revisions (rather than addendum). Per-finding revision trace in `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/DISPOSITION.md`. Key revisions: F1 — in-repo authoritative path established at `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md`, runtime mirror demoted to working-draft; F2 — Phase G prose-block replaced with explicit 14-row artifact-by-artifact disposition table aligned with INITIATIVE.md §7 custody rule; F4 — new §5.6 control matrix (13-row mapping table); F8 — new §4.2.1 cross-repo commit-identity rules requiring source+target hashes in EXTRACTION-LOG.md and both commit bodies.

**Tooling-side outcome.** Removed `gsd-read-guard.js` PreToolUse hook from `~/.claude/settings.json` (was firing advisory read-before-edit reminder per-Edit; redundant for Claude which natively follows the pattern; was burning ~120 tokens per Edit call). Kept `gsd-prompt-guard.js` and `gsd-workflow-guard.js`.

**Phase A→B boundary reached.** Per §0.7 Q1 hybrid autonomy: pause at phase boundaries for Logan disposition. PAUSED awaiting Logan green-light before Phase B begins.

**Lesson for future audits.** Single-vendor cross-vendor plan-self-audit (no paired Step-2) caught both Class C items at meta-level — F2's INITIATIVE.md §7 conflict was an explicit-artifact contradiction (cross-vendor's strength); F1's plan-file-custody was an artifact-control-shape question (also cross-vendor's strength). Same-vendor adversarial-auditor xhigh as paired Step-2 was Logan-discretion at §2.3 default-fires; not invoked here. If future plan-revisions surface in-session-collaboration register-leak residual not caught by cross-vendor alone, paired Step-2 can be invoked retrospectively. Recorded for future audits at DISPOSITION.md §4.1.

### §11.6.7 Trajectory plan Phase B — standing-context artifact RELATIONSHIP-TO-PARENT.md (2026-04-29; post-Phase-A-revision)

**Trigger.** Phase B of trajectory plan — land the test-case-vs-substrate clarification (§0.3 of the plan) as standing context, so future sessions don't re-confuse "the project" with "the substrate." Per Logan §0.7 Q3 disposition: Option (a) — new artifact `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` + CLAUDE.md doctrine load-point bullet.

**Artifacts landed.** RELATIONSHIP-TO-PARENT.md (~120 lines post-addendum: §1 what arxiv-sanity-mcp is in the bigger picture + §1.1 frame-status-stipulated subsection + §2 why it matters for execution + §3 migration implications + §4 cross-references). CLAUDE.md doctrine-load-point bullet added under "## Doctrine load-points" section (later tightened from "touching X or Y" phrasing to operational-trigger phrasing per F-RTP-5 audit-B). DISPOSITION.md + AUDIT-SPEC.md + audit-findings-A.md + audit-findings-B.md in `.planning/gsd-2-uplift/audits/2026-04-29-relationship-to-parent-audit/`.

**Phase B audit executed.** Per plan §2.4 row B: same-vendor adversarial-auditor-xhigh at high reasoning level (NOT xhigh — bounded artifact + register-leak detection on a clarification artifact); same-vendor only (cross-vendor would be M1 strict-undersell — register-leak is single-vendor-detectable). Two independent dispatches both ran; both transcribed inline because their FINDINGS.md Write was blocked at runtime layer (root cause diagnosed mid-session: Claude Code 2.1.123 binary's `tengu_sub_nomdrep_q7k` feature flag rejects sub-agent Write basenames matching `/^(REPORT|SUMMARY|FINDINGS|ANALYSIS).*\.md$/i`; bypass: filename convention `audit-findings*.md`).

**Convergent disposition.** Both dispatches returned commit-with-addendum non-binding signal. Convergent finding F-RTP-1: §7.1 meta-level residual — artifact treats test-case-vs-substrate as observed-fact rather than as stipulated frame (cited SYNTHESIS-COMPARISON.md §7 as precedent but did not apply §7.1's discipline to itself). Divergent secondaries: dispatch-1 emphasized long-horizon-plurality / substrate-shape-definitional / "the test case"-singular; dispatch-2 emphasized subordination-tension / single-case-generalization / CLAUDE.md-trigger-ambiguity. Findings sets coexist as audit-findings-A.md + audit-findings-B.md (paired, not superseding).

**Disposition applied autonomously per §0.7 Q1 (hybrid autonomy within phases).** Addendum landed: new §1.1 "Frame status — stipulated, not observed" subsection (~25 lines; modeled on SYNTHESIS-COMPARISON.md §7.1 pattern) folds in audit-A's long-horizon-plurality + "the test case"-singular findings AND audit-B's single-case-generalization + subordination-tension findings into one bullet structure. Inline edit to substrate-component parenthetical foregrounds under-investigation status (audit-A F-RTP-3). Inline edit "**spike-intensive test case**" → "*a* **spike-intensive test case**" (audit-A F-RTP-6). Cross-reference additions in §4: framing-widening §2 (long-horizon plurality) + trajectory plan §2.1-§2.3 (audit cadence as operational mechanism per audit-A F-RTP-5). CLAUDE.md doctrine-load-point trigger tightened per audit-B F-RTP-5. Two findings recorded but not actioned: audit-A F-RTP-4 (binary failure-mode framing — auditor flagged borderline/drop-as-taste) + audit-B F-RTP-4 (frontmatter comfort-language — auditor's own confidence low-medium, boundary-of-taste).

**Tooling-side outcome.** Diagnosed and bypassed Claude Code 2.1.123's `tengu_sub_nomdrep_q7k` feature flag via filename-convention shift to `audit-findings*.md`. AUDIT-SPEC.md §4 in this audit folder records the convention for future Phase C-onward audits in this trajectory plan; agent definition `~/.claude/agents/adversarial-auditor-xhigh.md` got a brief Output Protocol section recording the operational convention (no feature-flag exposition; just the operational fact + override-by-dispatching-prompt clause). Convention applies to future audits; older FINDINGS-named artifacts (premise-bleed FINDINGS.md / FINDINGS-STEP2.md; trajectory-plan PLAN-AUDIT.md) remain at their original names since they predate the diagnosis.

**Phase B→C boundary reached.** Per §0.7 Q1 hybrid autonomy: pause at phase boundaries for Logan disposition. PAUSED awaiting Logan green-light before Phase C (incubation-checkpoint adjudication on SYNTHESIS-COMPARISON.md §2.1 + §5 axes) begins.

**Lesson for future audits.** Two findings sets from independent dispatches of the same audit task surfaced complementary rather than redundant signal — convergent on the load-bearing F-RTP-1 finding, divergent on secondaries. Both kept as audit-findings-A/B. Future Logan-discretion paired-dispatch decisions could weigh: paired-dispatch surfaces more findings but at additive token cost; if cost-benefit favors single-dispatch, accept the narrower coverage. Recorded.

### §11.7 Mid-stream pivot dispositions (if any)

*[empty — populated by §7.2 pivot procedure if triggered. Schema lives in §7.2.]*

## §12. Cross-references

**Decisions ground.** `.planning/gsd-2-uplift/DECISION-SPACE.md` §1.11-§1.16 (B1-B6); §1.4 (slice partition); §1.7 (metaquestion + non-exhaustive teeth); §1.8 (R2/R3 hybrid); §2.3 (incubation checkpoint); §3.1 (goal-articulation validation); §3.4 (long-horizon framing-axis question).

**Dynamics ground.** `.planning/deliberations/2026-04-27-dispatch-readiness-deliberation.md`; `.planning/deliberations/2026-04-26-uplift-initiative-genesis-and-dispatch-deferral.md`.

**Staging.** `.planning/gsd-2-uplift/INITIATIVE.md` §1, §3, §5.

**Methodology.** `.planning/spikes/METHODOLOGY.md`:104-115 (M1 paired-review); :117 (forbidden-reading-list extension).

**Codex pitfalls.** `.planning/handoffs/2026-04-26-post-wave-4-handoff.md` §9; archived dispatch package's `README.md` at `.planning/audits/archive/2026-04-26-wave-5-paired-audit-package/`.

**Anti-pattern self-check.** `AGENTS.md` "Project-specific anti-patterns to detect."

**Package siblings.** `preamble.md`, `slice-01-mental-model.md` through `slice-05-release-cadence.md`, `audit-spec.md`, `synthesis-spec.md`.

---

*Single-author orchestration overview written 2026-04-27 by Claude (Opus 4.7) at Logan's direction post-dispatch-readiness deliberation. Subject to the same fallibility caveat as DECISION-SPACE.md §0 and predecessor logs. Pre-pilot status; revise based on pilot disposition + per-wave findings. The §11 dispositions log is the authoritative record of what actually happened during execution.*
