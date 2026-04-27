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

Shallow depth is intentional. If a slice needs deeper history, deepen the clone for that slice.

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

After slice 1 (pilot) output lands at `.planning/gsd-2-uplift/exploration/01-mental-model-output.md`, review before proceeding. Disposition options below; **no disposition is default** — choose after reading the pilot. Naming order is alphabetical-by-action, not preference order.

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

**2026-04-27 — focused cross-vendor re-audit dispatch.** *[populated when re-audit completes — track outcome here.]*

### §11.2 Pilot disposition

*[empty]*

### §11.3 Parallel-slice dispositions

*[empty]*

### §11.4 W2 audit dispositions

*[empty]*

### §11.5 W3 synthesis disposition (incl. paired-synthesis escalation decision)

*[empty]*

### §11.6 Incubation-checkpoint outcome

*[empty — populated when checkpoint runs; though strictly speaking that's outside this orchestration's scope]*

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
