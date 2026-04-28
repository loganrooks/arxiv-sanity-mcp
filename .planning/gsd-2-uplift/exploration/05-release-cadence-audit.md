---
audit_target: .planning/gsd-2-uplift/exploration/05-release-cadence-output.md
date: 2026-04-28
auditor: Claude Opus xhigh adversarial-auditor
status: complete
---

# Audit of slice 5 output — release-cadence

## §0. Audit summary

- **Critical:** none.
- **Material:** none. (One systematic citation issue is on the line-number axis only; content is correct and the substantive claims survive.)
- **Minor:** (1) Several script-file line citations are out-of-range against the actual file lengths — `scripts/generate-changelog.mjs:194-204` / `:230-260` (file is 152 lines) and `scripts/update-changelog.mjs:78-136` (file is 59 lines). The content described at those citations is otherwise accurate; this is a citation-discipline issue, not a content issue. (2) The "lower bound 84.765 commits/week" framing is mathematically valid but the visible-window 401/wk figure carries more cadence-characterization signal; the slice does present both, hedging is adequate. (3) Completeness: the slice did not surface `cleanup-dev-versions.yml` (Monday 06:00 UTC, `MAX_AGE_DAYS=30`) which corroborates the 30-day retention claim it cites from docs, nor did it cite `SCHEMA_VERSION = 22` at `gsd-db.ts:183` which would concretize Finding 3.5 (version-aware migration).
- **Clean:** Math reproduces exactly (38.642-day visible span, 401.430 commits/week, 0.160 average tag-gap weeks, all 33 individual gaps spot-checked). Shallow-clone hedging is properly per-claim. Q2 (breaking-change posture) cleanly distinguishes stated policy from observed practice. Zero framing-leakage from the dispatching project's vocabulary — including the specifically-flagged "long-horizon" pattern. Confidence labels are appropriately calibrated, including correct medium-confidence on the OAuth-pre-deprecation negative finding.

**Verdict:** Minor findings → addendum. The line-number-citation issue should be noted for synthesis (don't trust line numbers in three script files; the content is verified) but does not change any synthesis-relevant claim. Confidence: high on this verdict.

## §1. Source verification

### Spot-check 1: shallow-clone preflight numbers

- **Slice claim** (line 32): "total visible commits are `2217`, and commits in the six-month window are `2216`."
- **Source check:** `git rev-parse --is-shallow-repository` → `true`; `git log --oneline | wc -l` → `2217`; `git log --since="6 months ago" --pretty=format:"%h" | wc -l` → `2216`.
- **Verdict:** verifiable, exact match. The shallow-truncation framing is accurate (commits-in-6mo equals total-1, confirming the shallow boundary cuts inside the window). Confidence: high.

### Spot-check 2: tag count and date range

- **Slice claim** (line 254, 294): "34 tags dated `2026-03-20` through `2026-04-25`"; "first visible tag `2026-03-20 01:26:46 +0000`; last visible tag `2026-04-25 23:25:44 +0000`."
- **Source check:** `git tag | wc -l` → `34`. `git for-each-ref --sort=creatordate refs/tags` first entry: `v2.36.0 2026-03-20 01:26:46 +0000`; last: `v2.78.1 2026-04-25 23:25:44 +0000`.
- **Verdict:** verifiable, exact match. Confidence: high.

### Spot-check 3: cadence math

- **Slice claim** (line 252): "visible 38.642-day span... visible-history density is `401.430 commits/week`. Spread across a nominal 183-day six-month window, `2216` commits gives a lower bound of `84.765 commits/week`."
- **Source check:** independently computed `(2026-04-27 09:50:47 -0500) - (2026-03-19 17:26:31 -0600)` = 38.642 days = 5.5203 weeks. 2216/5.5203 = 401.430. 2216/(183/7) = 84.765.
- **Verdict:** verifiable, exact match. Confidence: high.

### Spot-check 4: tag-gap math

- **Slice claim** (lines 261, 291, 294): individual gaps (e.g., v2.36.0→v2.39.0 = 0.109 weeks; v2.78.0→v2.78.1 = 0.020 weeks) and average across 33 consecutive-pair gaps = 0.160 weeks.
- **Source check:** v2.36.0 (2026-03-20 01:26:46 +0000) → v2.39.0 (2026-03-20 19:41:22 +0000) = 0.760 days = 0.1086 weeks. v2.78.0 (2026-04-25 20:04:28 +0000) → v2.78.1 (2026-04-25 23:25:44 +0000) = 0.140 days = 0.0200 weeks. Mean of all 33 listed gaps = 0.160. All match.
- **Verdict:** verifiable, exact match. Confidence: high.

### Spot-check 5: script line citations (the one issue)

- **Slice claim** (line 304): `scripts/generate-changelog.mjs:194-204` for hasBreaking detection; `scripts/generate-changelog.mjs:230-260` for major-bump mapping.
- **Source check:** `wc -l scripts/generate-changelog.mjs` → 152 lines total. Actual locations: line 58 (`let hasBreaking = false`), line 66-67 (`if (subject.includes("BREAKING CHANGE") || subject.includes("!:"))` ... `hasBreaking = true`), line 96 (`const bumpType = hasBreaking ? "major" : ...`), lines 118-125 (semver bump arithmetic).
- **Verdict:** content-correct, line-citation wrong (overshoots file length). Same pattern for `scripts/update-changelog.mjs:78-136` (file is 59 lines; the cited content — insert after `[Unreleased]`, update comparison links — appears at lines 33-56). The slice's overall finding (these scripts implement breaking-detection and changelog automation) is verified; the line numbers are not. Severity: minor (citation discipline). Confidence: high that the discrepancy is real; medium that it represents a systematic agent-side fabrication of plausible line ranges rather than e.g. a misread of a different file.

### Spot-check 6: alias telemetry and CHANGELOG `[Unreleased]` deprecation

- **Slice claim** (lines 300, 308): `CHANGELOG.md:1-5` for Keep-a-Changelog header; `CHANGELOG.md:7-10` for `[Unreleased]` `### Deprecated` MCP-alias entry; `packages/mcp-server/src/alias-telemetry.ts:1-9` for "Step 1 of a two-step deprecation" comment.
- **Source check:** CHANGELOG line 1-5 = title + Keep-a-Changelog reference; line 7 = `## [Unreleased]`; line 9-10 = `### Deprecated` + 11-alias entry. `alias-telemetry.ts:1-9` includes "Step 1 of a two-step deprecation (#5031)... single JSON line per invocation to stderr."
- **Verdict:** verifiable, exact match. Confidence: high.

### Spot-check 7: `BREAKING CHANGE` absence in CHANGELOG and recent commits

- **Slice claim** (Finding 2.7, line 318): "I did not find a `BREAKING CHANGE` commit in the visible search results."
- **Source check:** `grep -iE "^### Breaking|BREAKING" CHANGELOG.md` → 2 incidental matches only (line 2175 "imports breaking CI build"; line 2868 "destroys unique milestone ID case... breaking dependency resolution"). No `### Breaking Changes` section heading anywhere in 3846-line CHANGELOG. `git log --since="6 months ago" --pretty=format:"%s" | grep -iE "^feat\(.*\)!:|^fix\(.*\)!:|BREAKING CHANGE"` → zero matches.
- **Verdict:** verifiable; corroborates slice's medium-confidence hedge. The factual gap (release tooling can detect BREAKING; observed practice doesn't use it) is real. Confidence: high.

### Spot-check 8: OAuth removal pre-deprecation hedge

- **Slice claim** (Finding 2.6, line 316): OAuth removal in v2.70.0 / v2.74.0 lacks visible pre-deprecation, but flagged medium-confidence "because the clone is shallow and I did not inspect GitHub releases outside the local clone."
- **Source check:** OAuth references in CHANGELOG before line 777 (the v2.70.0 removal) include line 425 `**auth**: self-heal stale Anthropic OAuth credential (#4399)` (post-removal cleanup, not pre-deprecation), line 472 `hide unsupported ChatGPT codex oauth models` (different OAuth context). No deprecation entry for Anthropic OAuth visible in the changelog before its removal.
- **Verdict:** verifiable; the medium-confidence hedge is appropriate given shallow truncation could have hidden earlier deprecation. Confidence: high on the hedge being calibrated.

## §2. Completeness

In-scope misses, all minor:

- **`cleanup-dev-versions.yml` not cited (Q4).** The slice cites `docs/dev/ci-cd-pipeline.md:188-196` for the "Old `-dev.` versions are cleaned up weekly (30-day retention)" claim but does not verify it against `.github/workflows/cleanup-dev-versions.yml` (which has `cron: "0 6 * * 1"` — Monday 06:00 UTC — and `MAX_AGE_DAYS=30`). This is a missed opportunity to corroborate a docs claim from source, especially given Finding (iv).4 already flags doc/source divergence elsewhere in CI/CD. Severity: minor.
- **`SCHEMA_VERSION = 22` at `gsd-db.ts:183` not cited (Q3 / Finding 3.5).** Slice describes "version-aware migration" with conditional migration blocks but does not cite the explicit SCHEMA_VERSION constant or note that gsd-2 is currently on schema version 22 (suggesting 22 prior schema migrations have been applied). This is concrete observable information that bears on Q5's "drift-handling feature inventory" — schema-migration depth is a feature. Severity: minor.
- **`forensics-check.yml`, `pr-risk.yml`, `ai-triage.yml`, `version-check.yml` not cited (Q4 / Q5).** Several CI workflows beyond the dev/next/prod-publish trio went uncited. `version-check.yml` is particularly relevant to Q4 (it auto-comments on stale-version issues). Severity: minor; the slice covered the main publication channels but the inventory is incomplete on the CI-automation surface.
- **No reference to schema/migration count as `BREAKING CHANGE` proxy.** Q2 sought breaking-change *observability*. The schema-version migration history at `gsd-db.ts:670-930` is a strong observable signal of breaking-change practice (schema migrations *are* breaking changes for any stored DB). Slice notes the migration mechanism but does not connect it back to Q2. Severity: minor; would have strengthened Finding 2.7.

No critical or material in-scope misses identified.

## §3. Framing-leakage

**No framing-leakage detected.** Specific patterns scanned for:

- "α / β / γ / δ" / Greek-letter shapes: not present.
- "doctrine load-points" / "anti-pattern self-check": not present.
- "artifact-mapping" framing (as a project-level term): not present. The slice does describe gsd-2's own artifact taxonomy in Q3, which is gsd-2's vocabulary, not the dispatching project's.
- **"long-horizon" / "long-horizon agential development":** absent. The slice prompt at lines 64-69 specifically directs the agent away from time-horizon characterization ("Do **not** characterize whether features 'support' any particular development style or time horizon"). The slice complies — Finding 5 inventory is purely observational, and the open-questions section explicitly defers interpretation ("Open question — interpretive; defer to synthesis").
- "harness-uplift" goal articulation: not present.
- "R2 / R1" / "R2/R3 hybrid": not present.
- "first-class" / "binding" / "load-bearing" / "smuggle" / "closure pressure" / "protected seam": one match for "first-class" (line 87, 90) but it is the slice quoting raw `git log` output where gsd-2's own commit subjects use "first-class" — i.e., gsd-2's vocabulary, not framing leakage. The other rhetorical patterns absent.
- Calibrated language in the project's specific in-house register (e.g., "appears to" used as hedge-suffix; per-claim confidence labels): present and appropriate. This is the *prompted* discipline (preamble lines 36-37), not unprompted leakage.

The slice maintains gsd-2's own terms throughout (e.g., "milestone/slice/task hierarchy", "auto-mode", "headless mode", "experimental preferences", "dist-tags", "workflow templates"). Confidence: high that no framing-leakage is occurring.

## §4. Calibration discipline

Calibration is generally well-handled:

- **High-confidence claims with concrete source evidence:** appropriate. Findings 1.1-1.3 (cadence math), 2.1-2.5 (breaking-change tooling and markers), 3.1-3.7 (artifact hierarchy), 4.1-4.6 (release channels) are all correctly labeled high-confidence with source citations.
- **Medium-confidence on the right claims:** Finding 2.6 (OAuth pre-deprecation) and Finding 2.7 (commit-message conventions for breaking) are correctly labeled medium given (a) shallow truncation and (b) reliance on local artifacts only. The hedge "because the clone is shallow and I did not inspect GitHub releases outside the local clone" is exactly the right hedge.
- **Per-claim confidence labels rather than a single closing footnote:** the slice puts confidence labels in-line with each finding, matching the prompted discipline. No "calibrated language confined to closing footnote" pattern.
- **Shallow-clone caveat surfaced per-claim:** Finding 1.1 explicitly hedges "true six-month count may be higher because the clone is shallow"; Finding 1.2 notes "tag count before `2026-03-20` in the six-month window cannot be ruled out from this clone alone"; Finding 1.3 caveats "high for visible tags only"; Finding 2.6 invokes the shallow caveat; section (iv).1 surfaces the precision limitation as an open question. This is exactly the discipline the prompt requested at preamble lines 35-39.
- **No over-confident claims spotted.** The line-number citations in the three script files are wrong, but the content claims are right; this is a citation-discipline issue, not a confidence-calibration issue.
- **One mild reach:** Finding 2.7 says recent removals "appear signposted primarily as `fix`, `refactor`, or `Changed/Fixed` entries." This is medium-confidence in the slice and survives audit, but the word "primarily" overstates the reach of the visible-history search; "are signposted as" without "primarily" would be cleaner. Severity: borderline taste.

Overall calibration confidence: high.

## §5. Direction-shifting evidence

### What the slice surfaced that could shift direction (preserved as-flagged):

- Section (iv).8: "release mechanics and product workflow are tightly interleaved." Release templates, CI workflows, changelog tooling, GSD-managed milestone artifacts, worktree merge behavior, in-session update checks all present. The slice correctly does *not* draw an interpretive conclusion; it flags the observation and defers to synthesis.
- Finding 2.7: stated policy supports `BREAKING CHANGE:` detection; observed practice has zero `BREAKING CHANGE`-marked commits in visible history. Tooling exists; convention isn't enforced. Direction-relevant: if the dispatching project assumed gsd-2's tooling-pattern includes commit-message discipline, that assumption is weakly supported by source.
- Finding 4.5: experimental preferences explicitly waive the deprecation cycle. Direction-relevant for any "what does gsd-2 commit to keeping stable" question.
- Section (iv).5: telemetry/observability "appears central, not incidental." Worktree telemetry, forensics, doctor, logs, HTML reports, event logs, DB gate runs, audit events. Cross-slice watchlist hit.
- Section (iv).7: security/trust boundaries appear central enough for cross-slice integration (auto-mode tool policy hard errors, secret/prompt-injection scanning).

### What the slice might have flagged but didn't (audit-side surfaces):

- **Schema version 22 as a drift signal.** gsd-2 has gone through 22 DB-schema migrations. This is observable, in-scope for Q3/Q5 (drift-handling features), and not surfaced. Whether 22 schema migrations is a lot or a little is interpretive (synthesis), but the *number* is concrete observation that would inform synthesis. Severity: minor; the slice didn't claim drift-handling depth is shallow, so this isn't a wrong claim — it's an absent one.
- **Tag/release cadence ratio.** 34 tags over 38.642 visible-window days = ~6.2 tags/week visible cadence. The slice computes 0.160-week average gaps but doesn't flip the framing to tags-per-week, which is a more legible cadence number. This is largely framing taste, but the prompt at line 88 specifically asks for "tags/6-month-period" format. Slice provides "34 tags since 2025-10-28" which technically answers the question, but the format requested was tags/6-mo and this is tags/visible-window. Severity: minor.
- **The pattern across Findings 2.6, 2.7, 4.5, and 4.6 integrates to a single observation:** gsd-2 has elaborate breaking-change *machinery* (workflow templates, generator scripts, PR template, CONTRIBUTING policy) but the *observed practice* is rapid release cadence (~6.2 tags/week visible) with breaking-change communication relying on changelog narrative rather than convention enforcement, and experimental preferences explicitly waive the cycle. This is a cross-finding pattern the synthesis stage should recognize. The slice does flag it implicitly via Finding 2.7 and section (iv).3 ("Breaking-change practice needs release-note and diff sampling beyond this slice") but does not name the integration. Severity: minor; this is properly synthesis-stage work, but worth flagging here so synthesis doesn't miss it.

### False positives (none found):

None of the slice's flagged direction-shifting items are spurious on independent reading. Section (iv).8's "tightly interleaved" claim is supported by the cited features.

Confidence on this section: medium. §5 is interpretive by nature; same-vendor risk applies.

## §6. Recommendation

**Minor findings → addendum.** The output stands for synthesis with two notes:

1. **Citation-discipline addendum (high-confidence):** Three script-file line citations are out of range against actual file lengths — `scripts/generate-changelog.mjs:194-204` and `:230-260` (file is 152 lines; actual content at lines 58, 66-67, 96, 118-125), and `scripts/update-changelog.mjs:78-136` (file is 59 lines; actual content at lines 33-56). The content described is verified correct; only the line numbers are wrong. Synthesis should not rely on the specific line numbers in these three files for re-verification; following the file paths and content descriptions will land in the right place.

2. **Completeness addendum (medium-confidence):** Synthesis should be aware that the slice did not cite `cleanup-dev-versions.yml` (corroborates the 30-day retention claim), `SCHEMA_VERSION = 22` at `gsd-db.ts:183` (concretizes drift-handling depth), or four secondary CI workflows (`forensics-check.yml`, `pr-risk.yml`, `ai-triage.yml`, `version-check.yml`). None of these absences invalidate the slice's findings; they are augmentations.

No re-dispatch needed. The cross-finding integration noted in §5 is properly synthesis-stage work.

## §7. Same-vendor framing-leakage caveat

I am same-vendor relative to the cross-vendor reader I am auditing. My critique is grounded in within-artifact verifiable contradictions where possible — the line-number out-of-range issue (§1, spot-check 5) and the math-reproduction checks (§1, spot-checks 3 and 4) are dispositive. Where my findings are interpretive (§3 framing-leakage absence, §5 direction-shifting evidence), I have flagged them at lower severity unless the case is dispositive — for example, my §3 verdict of "no leakage" rests on a finite scan of named patterns and could miss subtler register-matching that a different reader would catch. Cross-vendor audit of my audit would catch different things; this audit does not substitute.

One specific same-vendor risk to name: I might be reading sympathetically on calibration discipline because the slice's hedging style matches the *prompted* discipline that I would also have produced under the same prompt. The slice's calibration is genuinely good, but I cannot rule out that I am giving it more credit than a cross-vendor reader would. The §1 verifiable findings (math, citations, content cross-checks) are not subject to this risk; the §4 calibration assessment is.
