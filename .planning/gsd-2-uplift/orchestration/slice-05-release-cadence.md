# Slice 5 — Concrete observable patterns: release cadence + breaking-change posture + features

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first.

**Provisional spec, pre-pilot.** Pilot disposition may revise this spec — including whether the slice 5 split (concrete observation here; abstract interpretation deferred) holds.

**This slice is intentionally concrete.** Abstract interpretation against any specific time-horizon or evaluative axis is downstream synthesis work, not your output. If you find yourself reaching for "this means gsd-2 supports X horizon..." kind of conclusions, **stop** — those are synthesis-level claims, not slice-level observations. Stay observational.

## Slice scope

**This slice covers:** observable patterns about gsd-2's release cadence, breaking-change posture, and feature inventory bearing on multi-milestone work, requirement-drift handling, and integration with release workflows — all *concrete*, all *observational*, none interpretive.

**This slice does NOT cover:**
- Mental model / mission / target user (slice 1)
- Architecture / runtime layering (slice 2)
- User-facing commands / automation / testing (slice 3)
- Artifacts / extension surfaces / migration / install-version-release-mechanics implementation (slice 4 — if a question feels like slice 4 territory rather than slice 5, prefer slice 4 framing). **Note:** breaking-change *communication* (deprecation policy, release-note conventions, in-code deprecation markers) is slice 5 Q2 — slice 4 limits itself to install/update/version implementation surfaces.
- **Abstract interpretation against any specific time-horizon or evaluative axis** — explicitly out of scope; synthesis stage handles this.

If a question reads to you as inviting interpretation rather than observation, surface in your open-questions section as "open question — interpretive; defer to synthesis." Resist closure verdicts like "gsd-2 supports / doesn't-support X."

## Diagnostic questions

Answer concretely with source / git citations and (for Q1) raw command output.

**Preflight (run before Q1) — diagnostic only; do not write to the gsd-2 clone:**

```bash
cd ~/workspace/projects/gsd-2-explore/
git rev-parse --is-shallow-repository
git log --oneline | wc -l                              # commits visible
git log --since="6 months ago" --pretty=format:"%h" | wc -l   # commits in 6-mo window
```

If the repository is shallow (`true`) and the 6-month window appears truncated (commits-in-6mo equals total-commits-visible, suggesting the shallow boundary cuts inside the window):

- **Do not run `git fetch` / `--unshallow` / `--deepen` yourself.** Per the preamble, gsd-2 is a read-only target for the slice agent. Modifying the clone is the dispatcher's responsibility (OVERVIEW §2.1 reserves deepening for cases like this).
- **Report the truncation in section (i) of your output** with: shallow-status, total-commits-visible, commits-in-6mo-window, and the caveat "history truncated at shallow boundary; cadence numbers are lower bound; dispatcher should deepen the clone and re-dispatch slice 5 if precise cadence is needed."
- **Proceed with Q1** using available history; surface the caveat per-claim (e.g., "commits/week ≥ X over visible window; true value may be higher if pre-shallow commits exist").

If the repository is not shallow, or the shallow boundary falls before the 6-month window, proceed normally.

1. **Release cadence** — run these and include raw output:

   ```bash
   cd ~/workspace/projects/gsd-2-explore/
   git log --since="6 months ago" --pretty=format:"%h %ai %s" | head -100
   git tag --sort=-creatordate | head -30
   git log --tags --pretty=format:"%h %ai %d %s" | head -30
   ```

   Then characterize concretely (not qualitatively): commits-per-week-on-average over the last 6 months; number of tags in last 6 months; gaps between tags (weeks). Do not call it "fast" or "slow" — give the numbers, let synthesis interpret.

2. **Breaking-change posture (stated and observed).** This question owns deprecation/breaking-change communication for the entire slice partition (slice 4 limits itself to install/update/version *implementation* surfaces).

   - **Stated policy.** Search for `CHANGELOG.md`, release notes (GitHub releases, `RELEASES.md`, `NEWS.md`), and any documented deprecation policy (in `CONTRIBUTING.md`, in `docs/`). What does gsd-2 *say* about how it handles breaking changes?
   - **In-code markers.** Grep for `DeprecationWarning`, `@deprecated`, `// DEPRECATED`, equivalent markers in the language of gsd-2's source. How many; where; with what removal-target metadata?
   - **Observed practice.** Cross-check stated policy against recent commits/releases: do recent breaking changes follow the stated cycle (deprecated-in-vN, removed-in-vN+M), or do they ship without warning? Are breaking changes signposted in commit messages / release titles, or only discoverable from diff?
   - Cite specific files and examples for each.

3. **Multi-milestone / release-related artifacts.** Does gsd-2 have artifact classes that bear on multi-milestone work? E.g., `MILESTONE.md`, `ROADMAP.md`, `RELEASE.md`, multi-version configuration files, version-aware migration scripts. List each; cite its schema briefly.

4. **Prod / dev distinctions.** Does gsd-2 distinguish between prod and dev environments, or between production releases and experimental work? How is the distinction surfaced in artifacts / tooling / configuration? Cite specifics.

5. **Multi-milestone / release-workflow / drift-handling feature inventory (concrete observation only).** What features does gsd-2 have that bear on multi-milestone work, codebase-complexity scaling, requirement-drift handling, or integration with release workflows? **Cite features concretely.** Do **not** characterize whether features "support" any particular development style or time horizon — that's synthesis-level interpretation. Produce an inventory, not an evaluation.

   Example of concrete observation (good): "gsd-2 has a `MILESTONE.md` file format defined at `<file:line>`; it carries fields `objectives`, `phases`, `success_criteria` per `<file:line>`."
   
   Example of interpretive characterization (avoid): "gsd-2's `MILESTONE.md` supports planning at scale" or "this feature enables long-horizon development."

## Slice-specific forbidden reading

In addition to the standard forbidden-reading list in the preamble:

- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/01-mental-model-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/02-architecture-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/03-workflow-surface-output.md`
- `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/04-artifact-lifecycle-output.md`

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/05-release-cadence-output.md` via `apply_patch`.

Raw `git log` / `git tag` output goes in section (i). Numerical summaries (commits/week, tags/6-mo, gaps in weeks) go in section (ii) Q1. Concrete features go in section (ii) Q5 with citations only.

## What "good slice 5 output" looks like

- A reader should be able to answer "what is gsd-2's release pattern" with numbers (commits/week; tags/6-month-period; gap-between-tags) — not adjectives.
- Q2 (breaking-change posture) should distinguish "stated policy" (CHANGELOG.md / docs) from "observed practice" (do recent commits actually follow deprecation cycles, or do breaking changes ship without warning?). In-code deprecation markers belong here too.
- Q5 should be a feature inventory, not a feature evaluation. If you can list 5 concrete features that *bear on* multi-milestone / drift / release-workflow work without claiming they *support* any particular development style, that's the right register.
- If gsd-2's release cadence is wildly volatile (e.g., 5 breaking releases in 2 months) or wildly stable (e.g., no commits in 6 months), surface as direction-shifting evidence — extreme cases matter for downstream decisions; let synthesis interpret.
- If you find that the slice-5 split (concrete vs interpretive) feels artificial — e.g., "release cadence" itself requires comparison-frame to be meaningful — flag in open-questions. The split is provisional pending pilot output, so feedback from this slice may revise it.

---

*Slice 5 spec. Pre-pilot. Subject to revision (including possible reversal of the slice-5 split per B4) based on pilot output. Single-author cross-vendor read; subject to W2 audit per the dispatching project's orchestration.*
