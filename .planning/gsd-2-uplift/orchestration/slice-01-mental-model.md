# Slice 1 — Mental model + mission + target user (PILOT)

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first. This document is the slice-specific spec; the preamble carries common context (working directories, calibration discipline, standard forbidden reading, output structure).

**This slice is the pilot.** Pilot output disposes whether the dispatching project proceeds with parallel dispatch of slices 2-5, re-slices, escalates, or de-escalates. See OVERVIEW §4 for pilot-gate criteria. **Your output sets calibration for the remaining slices** — the project reviews this output before drafting prompts for the others.

## Slice scope

**This slice covers:** what gsd-2 *is* — its mental model, mission, target user, agentic-development stance, and current development status. Read source + README to build a careful first-pass characterization.

**This slice does NOT cover:**
- Architecture / runtime / Pi SDK relationship (slice 2)
- Workflow surface / commands / automation / testing (slice 3)
- Artifact lifecycle / extension surfaces / migration / distribution (slice 4)
- Release cadence / breaking-change posture / observable patterns (slice 5)

If material in your reading bleeds into another slice's scope, note it in your open-questions section and let it be — do not expand into another slice.

## Diagnostic questions

Answer concretely with source citations. Use a sub-heading per question in section (ii) of your output.

1. **What does gsd-2 do?** What is the user-visible behavior? What is the entry point (command, library import, file-based interaction)? What sequences of operations does the system support? Be concrete: cite specific files / commands / artifacts you observed.

2. **What problem does gsd-2 solve?** What pain point does the README claim to address? Is the framing self-consistent — does the artifact set you observe match the claimed pain? Are there mismatches between framing and implementation?

3. **Who is the target user?** Solo developers? Teams? Organizations? What does the user know coming in? What does gsd-2 expect the user to bring? Is the audience claim grounded in the implementation, or aspirational?

4. **What is gsd-2's stance toward agentic development?** Is gsd-2 an agent-orchestration framework, an agent-assisted planning framework, a workflow-templating tool, something else? How does it expect agents to interact with its artifacts? What does it leave to humans vs delegate to agents?

5. **What is the current development status?** Active, mature, experimental? Last commit; release cadence at-a-glance (a quick look — detailed cadence analysis is slice 5's scope, so don't dive deep).

## Slice-specific forbidden reading

In addition to the standard forbidden-reading list in the preamble:

- (None additional — slice 1 is pilot; no prior slice outputs exist yet.)

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md` via `apply_patch`. Use the standard output structure from the preamble.

## What "good slice 1 output" looks like (slice-specific calibration)

- A reader who has never seen gsd-2 should come away knowing what it is and who it's for, with concrete enough understanding to formulate substantive questions for slices 2-5.
- Q1 answer should distinguish "what gsd-2 advertises" from "what gsd-2 actually does in source" — those may differ.
- Q4 answer is load-bearing for the dispatching project's downstream decisions; if you can't answer it cleanly from source, flag in open-questions specifically.
- If gsd-2's mission feels divergent from agentic-development-tooling (e.g., it's actually a generic project-management tool with agent integrations bolted on), surface that as direction-shifting evidence — the dispatching project's characterization-aim assumes gsd-2 is in the agential-development framework space.

## Pilot-specific note

Because you are slice 1 (pilot), your output also informs the dispatching project's calibration of slices 2-5 prompts. If you found the slice-1 prompt itself unclear, ambiguous, or framing-leaky — flag in open-questions. The project will revise other slices' prompts based on your feedback before parallel dispatch.

---

*Slice 1 spec. Pre-pilot. Subject to revision based on pilot output. Single-author cross-vendor read; subject to W2 audit per the dispatching project's orchestration.*
