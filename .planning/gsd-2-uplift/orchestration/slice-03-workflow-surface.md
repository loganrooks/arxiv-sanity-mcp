# Slice 3 — Workflow surface + automation + testing

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first.

**Provisional spec, pre-pilot.** Pilot disposition may revise this spec's questions, scope, or forbidden-reading.

## Slice scope

**This slice covers:** what gsd-2 lets *users* (humans + agents) *do* — the user-facing workflow surface, automation gsd-2 provides, hooks gsd-2 exposes, and testing primitives gsd-2 supports.

**This slice does NOT cover:**
- Mental model / mission / target user (slice 1)
- Architecture / runtime / substrate-vs-gsd-2-specific layering (slice 2)
- Artifacts the system produces / extension surfaces / migration / distribution (slice 4)
- Release cadence / breaking-change posture (slice 5)

If a question reads as "what does gsd-2 *do* internally" rather than "what does gsd-2 expose to users / agents," that's slice 2 territory.

## Diagnostic questions

Answer concretely with source citations.

1. **What slash commands or CLI commands does gsd-2 expose?** List them. Group by purpose if the grouping is clear from gsd-2's own structure. Per command: name; what it does; what artifacts it produces or consumes.

2. **What automation does gsd-2 provide?** Auto-loops? Auto-execution of plans? Auto-verification? Auto-loading of context? What gets automated and what is left to manual user invocation? Where is the human-vs-machine line drawn?

3. **What hooks does gsd-2 expose?** Pre-tool, post-tool, lifecycle hooks (session-start / session-stop / etc.). How are they configured (config file / decorator / runtime registration)? What can users do at hook-time? Cite specific hook points in source.

4. **What testing primitives exist?** Test discovery; test execution; test verification gsd-2 supports for users' projects. Also: how is gsd-2 itself tested (test directory; CI configuration; test pattern)?

5. **Where does the user touch gsd-2 vs where does the agent touch gsd-2?** Is there a clean human / agent split (humans run command X; agents read file Y), or are they mixed (humans and agents both invoke the same surface)? Are there parts of gsd-2 designed for human-only use? Agent-only use?

## Slice-specific forbidden reading

In addition to the standard forbidden-reading list in the preamble:

- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/02-architecture-output.md`

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md` via `apply_patch`.

## What "good slice 3 output" looks like

- A reader should be able to anticipate "if I (as user) want to do X, gsd-2 expects me to do Y" for the major X's gsd-2 supports.
- Q1 (commands list) is foundational for downstream slices; be exhaustive within reason. If gsd-2 has 20+ commands, list them in a table; if 5-10, list them prosaically.
- Q5 (human vs agent surface split) is load-bearing for the dispatching project's downstream decisions; flag any ambiguity concretely.
- If gsd-2's automation surface is so thin that "agentic-development framework" feels like an overclaim, surface that — it would shift the dispatching project's characterization-aim.
- If gsd-2's automation is much richer than expected (heavy auto-loops; deep hook system; built-in agent orchestration), surface that too — it would shift downstream design decisions about what to build vs what gsd-2 already provides.

---

*Slice 3 spec. Pre-pilot. Subject to revision based on pilot output. Single-author cross-vendor read; subject to W2 audit per the dispatching project's orchestration.*
