# Slice 5 — Concrete observable patterns: release cadence + breaking-change posture + features

> Read the common preamble at `.planning/gsd-2-uplift/orchestration/preamble.md` first.

**Provisional spec, pre-pilot.** Pilot disposition may revise this spec — including whether the slice 5 split holds (per dispatching project's decision B4: pilot may reveal the split is unnecessary if cross-vendor handles abstract framing fine).

**This slice is intentionally concrete.** Abstract interpretation of long-horizon-relevance is downstream synthesis work, not your output. If you find yourself reaching for "this means gsd-2 supports X horizon..." kind of conclusions, **stop** — those are synthesis-level claims, not slice-level observations. Stay observational.

## Slice scope

**This slice covers:** observable patterns about gsd-2's release cadence, breaking-change posture, and feature inventory bearing on long-horizon work — all *concrete*, all *observational*, none interpretive.

**This slice does NOT cover:**
- Mental model / mission / target user (slice 1)
- Architecture / runtime layering (slice 2)
- User-facing commands / automation / testing (slice 3)
- Artifacts / extension surfaces / migration / distribution (slice 4 — install/version/release-mechanics overlap; if a question feels like slice 4 territory rather than slice 5, prefer slice 4 framing)
- **Abstract long-horizon-relevance interpretation** — explicitly out of scope; synthesis stage handles this

If a question reads to you as inviting interpretation rather than observation, surface in your open-questions section as "open question — interpretive; defer to synthesis." Resist closure verdicts like "gsd-2 supports / doesn't-support X horizon."

## Diagnostic questions

Answer concretely with source / git citations and (for Q1) raw command output.

1. **Release cadence** — run these and include raw output:

   ```bash
   cd ~/workspace/projects/gsd-2-explore/
   git log --since="6 months ago" --pretty=format:"%h %ai %s" | head -100
   git tag --sort=-creatordate | head -30
   git log --tags --pretty=format:"%h %ai %d %s" | head -30
   ```

   Then characterize concretely (not qualitatively): commits-per-week-on-average over the last 6 months; number of tags in last 6 months; gaps between tags (weeks). Do not call it "fast" or "slow" — give the numbers, let synthesis interpret.

2. **Breaking-change posture.** Search for `CHANGELOG.md`, release notes (in GitHub releases, in `RELEASES.md`, in `NEWS.md`), deprecation markers in code (e.g., `DeprecationWarning`, `@deprecated`). How does gsd-2 communicate breaking changes? Is there a deprecation cycle (deprecated-in-vN, removed-in-vN+M)? Are breaking changes signposted in commit messages, release titles, or only discoverable from diff? Cite specific files and examples.

3. **Multi-milestone / release-related artifacts.** Does gsd-2 have artifact classes that bear on multi-milestone work? E.g., `MILESTONE.md`, `ROADMAP.md`, `RELEASE.md`, multi-version configuration files, version-aware migration scripts. List each; cite its schema briefly.

4. **Prod / dev distinctions.** Does gsd-2 distinguish between prod and dev environments, or between production releases and experimental work? How is the distinction surfaced in artifacts / tooling / configuration? Cite specifics.

5. **Long-horizon-relevant features (concrete observation only).** What features does gsd-2 have that bear on multi-milestone work, codebase-complexity scaling, requirement-drift handling, integration-with-release-workflows? **Cite features concretely.** Do **not** characterize whether they "support long-horizon development" — that's synthesis-level interpretation.

   Example of concrete observation (good): "gsd-2 has a `MILESTONE.md` file format defined at `<file:line>`; it carries fields `objectives`, `phases`, `success_criteria` per `<file:line>`."
   
   Example of interpretive characterization (avoid): "gsd-2's `MILESTONE.md` supports long-horizon planning."

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
- Q2 (breaking-change posture) should distinguish "stated policy" (CHANGELOG.md / docs) from "observed practice" (do recent commits actually follow deprecation cycles, or do breaking changes ship without warning?).
- Q5 should be a feature inventory, not a feature evaluation. If you can list 5 concrete features that *bear on* long-horizon work without claiming they *support* long-horizon work, that's the right register.
- If gsd-2's release cadence is wildly volatile (e.g., 5 breaking releases in 2 months) or wildly stable (e.g., no commits in 6 months), surface as direction-shifting evidence — extreme cases matter for the dispatching project's downstream decisions about R2 viability.
- If you find that the slice-5 split (concrete vs interpretive) feels artificial — e.g., "release cadence" itself requires comparison-frame to be meaningful — flag in open-questions. The dispatching project's decision B4 is provisional pending pilot output, so feedback from this slice may revise it.

---

*Slice 5 spec. Pre-pilot. Subject to revision (including possible reversal of the slice-5 split per B4) based on pilot output. Single-author cross-vendor read; subject to W2 audit per the dispatching project's orchestration.*
