# Slice 2 — Architecture + runtime + Pi SDK relationship

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first.

**Provisional spec, pre-pilot.** Pilot disposition (slice 1) may revise this spec's questions, scope, or forbidden-reading. The dispatching project will append a "Revision N" note here if pilot output warrants pre-dispatch changes.

## Slice scope

**This slice covers:** how gsd-2 is *built* — runtime architecture, substrate-vs-gsd-2-specific layering, module/file structure, packaging, and the agent-runtime contract (the API surface agents see when interacting with gsd-2).

**This slice does NOT cover:**
- What gsd-2 does or who it's for (slice 1)
- User-facing commands / automation / testing primitives (slice 3)
- Artifacts the system produces / extension surfaces / migration / distribution (slice 4)
- Release cadence / breaking-change posture (slice 5)

If you find that slice-2 questions cannot be cleanly separated from slice-1 (mental model) — for example, "what is gsd-2 vs Pi SDK" requires knowing what gsd-2 *does* — note this in open-questions; do not re-do slice 1.

## Diagnostic questions

Answer concretely with source citations.

1. **What is the runtime architecture?** What does gsd-2 require at runtime — Pi SDK, RTK CLI, specific Python/Node/etc. version, sandbox semantics? How are these composed? What's the dependency graph at the language-runtime level?

2. **What is gsd-2 vs Pi SDK vs RTK?** Where does the gsd-2-specific code start; where does substrate (Pi SDK / RTK) stop? Are there clean boundaries (gsd-2 imports Pi as library) or are the layers entangled (gsd-2 monkey-patches Pi; Pi knows about gsd-2)? Cite specific imports / module structure / file boundaries.

3. **What is the module / file structure?** Top-level directories; what each contains; entry points; configuration files. Produce a brief tree-view (depth 2-3) with one-line descriptions per directory.

4. **How does gsd-2 ship?** Package manager (pip / npm / cargo / other); install path (`pip install gsd-2` / git clone / something else); runtime dependencies (requirements.txt / package.json / equivalent); lock-files; whether it's installable as a library, an executable, or both.

5. **What's the agent-runtime contract?** When agents (Claude Code, Pi-mono agents, etc.) interact with gsd-2, what's the API surface — auto-loaded files (AGENTS.md / CLAUDE.md / equivalent), slash commands, hooks, MCP tools, library calls, something else? Cite where in source the contract is defined.

## Slice-specific forbidden reading

In addition to the standard forbidden-reading list in the preamble:

- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md` (slice 1's output — would anchor your reading to slice 1's framing of "what gsd-2 is")

You may consult RTK and Pi SDK external docs if gsd-2's README references them.

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/02-architecture-output.md` via `apply_patch`.

## What "good slice 2 output" looks like

- A reader should be able to draw a one-page architecture diagram (substrate / gsd-2 / agent-runtime / artifacts) from your output without re-reading gsd-2.
- Q2 (gsd-2 vs Pi SDK boundary) is load-bearing for the dispatching project's downstream decisions; if the boundary is unclear from source, flag concretely.
- Q5 (agent-runtime contract) is also load-bearing; if the contract is implicit (no explicit API definition), describe what behavior agents would observe rather than what's "documented."
- If gsd-2 substantially overlaps in identity with Pi SDK such that "gsd-2 vs Pi SDK" isn't a meaningful distinction, surface that — it would shift the dispatching project's understanding of what it would be relating to.

---

*Slice 2 spec. Pre-pilot. Subject to revision based on pilot output. Single-author cross-vendor read; subject to W2 audit per the dispatching project's orchestration.*
