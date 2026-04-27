# W2 audit spec — same-vendor adversarial audit of cross-vendor slice outputs

This is the W2 audit specification per decision B2 (selective audit; slice 4 mandatory; others conditional). Same-vendor (Claude xhigh adversarial-auditor) reader; per-slice instance. Reusable template — adapt the slice-N references for each audit dispatch.

## When to dispatch

Per decision B2 selective audit:

- **Slice 4 audit is mandatory.** R2 viability is load-bearing; the cross-vendor read of extension surfaces must be verified.
- **Slices 1, 2, 3, 5 audits are conditional.** Audit if:
  - Output reads thin (< 100 lines or surface-level only)
  - Output reads off-target (didn't address the diagnostic questions)
  - Output makes claims load-bearing on second-wave-scoping decisions
  - Framing-leakage suspected (output uses dispatching-project vocabulary)
- **Skip if:** output is concrete, well-grounded, well-cited, calibration is honest, no direction-shifting evidence surfaced (low downstream stakes).

Disposition decision goes in OVERVIEW §12 dispositions log.

## Auditor role

Same-vendor (Claude Opus xhigh) adversarial-auditor. Dispatch via the `adversarial-auditor-xhigh` subagent type or by direct Opus invocation with explicit `model: "opus"`. Effort: xhigh.

## Audit prompt template

Substitute `{N}` and `{slice-name}` for the specific slice being audited.

```markdown
# Audit of slice {N} output — {slice-name}

## Your role

Adversarial auditor (same-vendor; Claude Opus xhigh). Your job is to verify slice {N}'s cross-vendor output against gsd-2 source and against framing-leakage risks.

## Forbidden reading

- Other slices' outputs and prompts (they would anchor your reading)
- The dispatching project's INITIATIVE.md, DECISION-SPACE.md, deliberation logs (would re-import the framings the cross-vendor read was meant to escape)
- The Gemini deep-research doc (framing-misaligned per project)
- The W3 synthesis (which doesn't exist yet at audit time, but listed for completeness)

You **may** read:
- The slice {N} output you're auditing (`.planning/gsd-2-uplift/exploration/0{N}-{slice-name}-output.md`)
- The slice {N} prompt (the slice-{N} spec at `.planning/gsd-2-uplift/orchestration/slice-0{N}-{slice-name}.md` plus the common preamble at `preamble.md`)
- gsd-2 source at `~/workspace/projects/gsd-2-explore/`
- This audit prompt
- Other audit outputs at `.planning/gsd-2-uplift/exploration/0X-*-audit.md` if they exist (cross-audit-pattern recognition)

## Audit dimensions

For each dimension below, produce a bullet-list of findings with severity (clean / minor / material / critical).

### 1. Source verification

Spot-check 3-5 specific claims in the slice output against gsd-2 source.

- Are the claims accurate?
- Are line citations correct (file exists; line says what slice claims)?
- Are there over-confident claims where source-evidence is thin?

For each spot-check: cite slice's claim → gsd-2 source → verdict (verifiable / not-verifiable / wrong).

### 2. Completeness

Are there mechanisms / artifacts / patterns the slice missed within its own scope?

- Run targeted scans of gsd-2 source relevant to the slice (e.g., `find ~/workspace/projects/gsd-2-explore/ -type f -name "*.py" | head -50` or equivalent for the slice's domain).
- Spot-check for missed patterns. The slice's diagnostic questions define scope; check whether *all* scope is covered.

Out-of-scope misses are not audit findings; only in-scope misses count.

### 3. Framing-leakage detection

Did the cross-vendor output adopt vocabulary or framings that match the dispatching project's prior thinking?

Specific patterns to flag if observed:
- Use of "α / β / γ / δ" shapes or "doctrine load-points" or "anti-pattern self-check" phrasings (these are from the project's harvest §5)
- "Artifact-mapping" framing (from the deferred dispatch package)
- "Long-horizon agential development" or "harness-uplift" goal articulation (from the project's INITIATIVE.md)
- "Calibrated language" register matching project's in-house patterns (subtler — flag if you see it)

If found: quote verbatim; cite where in slice output; verdict on whether leakage is via the slice's prompt (which we control and could revise) or via cross-vendor reaching beyond forbidden-reading-list (more concerning).

### 4. Calibration discipline

Are confidence labels appropriate?

- Over-confident claims (high confidence on thinly-evidenced claims): flag.
- Over-hedged claims (medium-low when source-evidence is concrete): flag.
- Missing confidence labels on substantive claims: flag.
- Inconsistent calibration (Q1 over-confident; Q3 over-hedged): flag the pattern.

### 5. Direction-shifting evidence — surfaced and missed

Did the slice surface direction-shifting evidence (per the dispatching project's §3.1 metaquestion + §3.4 long-horizon framing-axis question + cancellation-possibility per §1.11 aim)?

- Was there evidence in source the slice might have flagged but didn't?
- Was there evidence the slice flagged that, on your independent reading, doesn't actually shift direction (false positive)?
- Are there patterns across the slice's findings that, integrated, would shift direction even though no individual finding would? (This is the synthesis stage's job, but if you see it strongly, flag.)

## Output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/0{N}-{slice-name}-audit.md` via apply_patch.

Output structure:

```markdown
---
audit_target: .planning/gsd-2-uplift/exploration/0{N}-{slice-name}-output.md
date: <date>
auditor: Claude Opus xhigh adversarial-auditor
status: complete
---

# Audit of slice {N} output — {slice-name}

## §0. Audit summary
<top-line findings, severity-stratified: critical / material / minor / clean>

## §1. Source verification
<spot-checks with verdicts>

## §2. Completeness
<in-scope misses, if any>

## §3. Framing-leakage
<specific instances with verbatim quotes, if any>

## §4. Calibration discipline
<over-confident / appropriate / over-hedged claims>

## §5. Direction-shifting evidence
<what was surfaced; what was missed; integration-flags if any>

## §6. Recommendation

One of:
- **Clean → proceed.** No material findings; output stands as-is for synthesis.
- **Minor findings → addendum.** Findings exist but don't change synthesis-relevant claims; addendum to slice output captures them; synthesis proceeds.
- **Material findings → re-dispatch.** Findings change synthesis-relevant claims; re-dispatch slice with strengthened prompt; integrate audit notes into the re-dispatch's prompt.
- **Critical findings → pause.** Findings call into question the wave-structure or the cross-vendor approach itself; pause; surface to Logan; re-disposition.

## §7. Same-vendor framing-leakage caveat

I am same-vendor relative to the cross-vendor reader I'm auditing. My critique is grounded in within-artifact verifiable contradictions where possible. Where my findings are interpretive (especially §3 framing-leakage and §5 direction-shifting evidence), I have flagged them at lower severity unless the case is dispositive. Cross-vendor audit of my audit would catch different things; this audit does not substitute.
```

## Calibration discipline (for auditor)

- Calibrated language: "appears to" rather than "is"; confidence labels per finding.
- Verifiable contradictions get high confidence; interpretive claims get medium or lower.
- Same-vendor framing-leakage is real for the auditor too — flag where you might be reading sympathetically.
- Resist closure-pressure: don't reach for "clean → proceed" verdict if findings genuinely warrant addendum or re-dispatch.
- Surface uncertainty rather than papering it over.
```

## Audit dispatch command (Claude Code subagent)

For dispatching via Claude Code's adversarial-auditor-xhigh subagent:

```
# Within Claude Code, dispatch via Agent tool with subagent_type="adversarial-auditor-xhigh"
# Pass the audit prompt above (with {N} and {slice-name} substituted) as the prompt parameter
# Effort defaults to xhigh for the adversarial-auditor-xhigh subagent type
```

For direct Opus invocation outside Claude Code: pass the audit prompt as the user message; ensure `model: "opus"` and effort `xhigh`.

---

*Audit spec for W2 of first-wave exploration. Reusable template — adapt {N} and {slice-name} per audit. Single-author template; subject to revision based on actual audit outputs (e.g., if audit-prompt itself proves to underwrite-or-overwrite scope).*
