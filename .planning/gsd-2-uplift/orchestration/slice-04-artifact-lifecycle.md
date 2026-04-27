# Slice 4 — Artifact lifecycle + extension surfaces + migration tooling + distribution + light contribution-culture probe

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first.

**Provisional spec, pre-pilot.** Pilot disposition may revise this spec.

**This slice is load-bearing for the dispatching project's downstream decisions about how (or whether) to relate to gsd-2 as an extension target.** Take this slice carefully; if extension surfaces are unclear from your reading, flag the unclarity concretely rather than papering over.

## Slice scope

**This slice covers:** how gsd-2 *meets the world* — what artifacts gsd-2 produces, where it allows external code to plug in (extension surfaces), how it migrates other tooling's artifacts into its frame, how it ships, plus a *light* contribution-culture probe (PR / issue activity at-a-glance via `gh` CLI).

**This slice does NOT cover:**
- Mental model / mission / target user (slice 1)
- Architecture / runtime layering (slice 2)
- User-facing commands / automation / testing (slice 3)
- Release cadence / breaking-change posture (slice 5 — though install/version/release-mechanics are slice 4 territory)

The contribution-culture probe is **light** — raw counts and cited timestamps from `gh` CLI. Do **not** characterize qualitatively (e.g., "gsd-2's maintainers are responsive / unresponsive" requires interpretation that is downstream synthesis work). Report what the data shows; let synthesis interpret.

## Diagnostic questions

Answer concretely with source citations and (for Q5) raw `gh` output.

1. **What artifacts does gsd-2 produce?** Files, directories, structured outputs in users' projects. What's the schema of each (key fields; required vs optional; format)? What's the lifecycle (created when; updated when; deleted when; long-lived vs ephemeral)? Cite where in source the artifacts are defined / written.

2. **Are there extension surfaces?** First establish whether gsd-2 exposes any mechanism for external code to plug in. If yes: plugin system? Module override / monkey-patch points? Configuration that changes behavior substantively (not just turning features on/off)? Commands or hooks that third-party code can register? Subclassing / interface-implementation patterns? Be concrete — cite where in source extension surfaces appear, and what shape extensions must take. If no extension surfaces exist (gsd-2 expects monolithic forking rather than extending), say so directly with citations.

3. **What migration tooling exists?** Does gsd-2 have a `migrate` command or equivalent for converting other tooling's artifacts (e.g., another framework's planning directories, or earlier gsd versions) into gsd-2's artifact format? What does it convert; what doesn't it convert; what fails-loudly vs silently-drops? Cite where the migrator is implemented.

4. **How does gsd-2 install / update / version?** Package manager + install path (covered briefly in slice 2 Q4; here go deeper); release artifacts (PyPI / npm / GitHub releases / something); version-bumping mechanism; lock-file conventions; install-time vs run-time dependencies.

   Note: deprecation policy and breaking-change communication are slice 5's territory (Q2). Limit Q4 to installation/update/version *implementation surfaces* — leave the *communication of breaking changes* to slice 5.

5. **Light contribution-culture probe** — run these `gh` CLI commands and include raw output in your "What I read" section, then summarize in section (ii) Q5 with **counts and cited timestamps only** (do not characterize qualitatively):

   ```bash
   gh repo view gsd-build/gsd-2 --json description,homepageUrl,createdAt,pushedAt,stargazerCount,forkCount,openIssuesCount
   gh pr list --repo gsd-build/gsd-2 --state all --limit 20 --json number,title,state,createdAt,closedAt,mergedAt,author
   gh issue list --repo gsd-build/gsd-2 --state all --limit 20 --json number,title,state,createdAt,closedAt,author
   ```

   Plus: read `CONTRIBUTING.md` if it exists in gsd-2's repo; quote relevant sections.
   
   Report:
   - PR counts: total in last 20; merged / closed / open breakdown.
   - Approximate close-time for the most recent 5 closed/merged PRs (cite exact timestamps, let reader compute interval).
   - Issue counts: total in last 20; closed / open breakdown.
   - Whether `CONTRIBUTING.md` exists; if yes, list the section headers and any structural requirements (e.g., "PRs require accompanying ADR" or "all PRs must be linked to an issue").
   - Stargazer + fork counts (one-line each).

   **Fallback if `gh` is unavailable.** If any of the `gh` invocations fail (auth missing; network restricted; repo not accessible at this name), include the exact error output verbatim in section (i), then proceed with whatever local evidence is available — `CONTRIBUTING.md` if present in the clone; `README.md` references to issues/PRs; commit messages mentioning PRs. Mark Q5 as **incomplete (gh probe failed)** in section (ii). Do not skip the question silently.

## Slice-specific forbidden reading

In addition to the standard forbidden-reading list in the preamble:

- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/02-architecture-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md`

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md` via `apply_patch`.

The contribution-culture probe raw `gh` output goes in section (i) ("What I read"). The summarized counts go in section (ii) Q5. **Do not interpolate qualitative judgments about contribution culture in section (ii)** — that's synthesis-stage work. Cite the data; let synthesis interpret.

## What "good slice 4 output" looks like

- A reader should be able to answer "if I want to extend gsd-2 with feature X, where would the extension code go and what shape would it need to take?" — at least at the level of "here are the surfaces; the specific design depends on what X is."
- Q2 (extension surfaces) is the most load-bearing diagnostic in this slice. **If extension surfaces are unclear, flag concretely.** Do not over-claim ("gsd-2 has an extension system") if the evidence is "there's a `plugins/` directory with one example." Calibrate.
- Q3 (migration tooling) bears on whether the dispatching project could migrate its existing artifacts to gsd-2's frame — but the slice's job is to characterize what migration *exists*, not to evaluate whether dispatching-project-specific migration is feasible (that's downstream).
- Q5 contribution-culture probe: this slice produces raw observations only. If the project's PR/issue history is wildly active or completely dormant, that surfaces direction-shifting evidence (extreme posture matters); flag in open-questions if so, but do not interpret intermediate cases.
- If extension surfaces are *absent* (gsd-2 expects monolithic forking rather than extending), surface this concretely as direction-shifting evidence in your open-questions section. Downstream synthesis will integrate this with the project's own framing.

---

*Slice 4 spec. Pre-pilot. Subject to revision based on pilot output. Single-author cross-vendor read; subject to W2 audit (mandatory per the dispatching project's orchestration; this slice's audit is not optional).*
