# W3 synthesis spec — same-vendor cross-slice integration

This is the W3 synthesis specification per decisions B2 (same-vendor synthesis as default) and B3 (paired-synthesis at W3 reserved as conditional escalation if synthesis drives operating-frame-update decisions).

## When to dispatch

After all 5 slice outputs land + W2 audits land (mandatory slice 4 audit + any selective audits dispatched per B2). Synthesis runs after audit-disposition for each slice is recorded in OVERVIEW §11.

## Synthesizer role

Same-vendor (Claude Opus xhigh) synthesizer. Either via the dispatching project's Claude Code session (you, working under Logan's collaboration) or as a dispatched xhigh agent. The synthesis is a deliberate, careful artifact-production task; not appropriate for default Explore agents (per `feedback_no_explore_for_audits.md` discipline applied broadly to gating evidence).

## Synthesis aim

**Pull cross-slice patterns; integrate audit findings; produce SYNTHESIS.md that incubation-checkpoint reads from.**

The synthesis is **not**:
- A roadmap or design proposal (second-wave work)
- A re-evaluation of the goal articulation (incubation-checkpoint work)
- A characterization of gsd-2 (slices already did that)
- A defense of the operating frame (synthesis is honest about what surfaced, not advocacy)

The synthesis **is**:
- Pattern-integration across slices
- Direction-shifting-evidence integration
- Operating-frame-update flagging (where first-wave evidence shifts §1.7 metaquestion answer; §1.8 R2/R3 viability; §3.4 long-horizon framing-axis)
- Surfacing of contradictions between slices
- Resolution of B4's provisional split: did slice 5's split hold; does abstract long-horizon-relevance interpretation belong here at synthesis or did slice 5 absorb it after pilot disposition

## Inputs

The synthesizer reads:

1. **All 5 slice outputs** at `.planning/gsd-2-uplift/exploration/0X-*-output.md`.
2. **All W2 audit outputs** at `.planning/gsd-2-uplift/exploration/0X-*-audit.md` (slice 4 mandatory; others if dispatched).
3. **DECISION-SPACE.md** at `.planning/gsd-2-uplift/DECISION-SPACE.md`, specifically:
   - §1.7 (metaquestion C-with-non-exhaustive-teeth)
   - §1.8 (R2/R3 hybrid)
   - §1.11 (first-wave aim — characterize-for-decision)
   - §1.12 (wave structure D′)
   - §3.4 (long-horizon framing-axis question)
4. **INITIATIVE.md** at `.planning/gsd-2-uplift/INITIATIVE.md`, specifically:
   - §1 (goal articulation)
   - §3 (open framing questions)
5. **OVERVIEW §11 dispositions log** for the wave's per-slice disposition history.

## Synthesis output

Write to `~/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/SYNTHESIS.md` via apply_patch.

Output structure:

```markdown
---
type: first-wave-synthesis
date: <date>
agent: Claude Opus xhigh synthesizer
inputs: [list slice output paths + audit output paths]
status: complete
escalation_to_paired_synthesis: <yes/no, with rationale>
---

# First-wave synthesis — gsd-2 characterization

## §0. Synthesis summary

Top-line findings, severity-stratified by their bearing on operating-frame-update decisions:

- **Operating-frame-shift findings:** <findings that, if accepted, would change a decision in DECISION-SPACE.md — e.g., flip R2 verdict, flip metaquestion answer, narrow design-shape decisively>
- **Operating-frame-confirm findings:** <findings consistent with the operating frame; refinements rather than shifts>
- **Open at synthesis stage:** <findings the synthesis surfaced but couldn't resolve — incubation-checkpoint or second-wave work>

If escalation_to_paired_synthesis is yes (per B3): note here, with rationale, before §1 begins.

## §1. Cross-slice pattern integration

Patterns that emerge across multiple slices. Cite which slices contribute which findings to each pattern.

### §1.1 <pattern name>
- Contributing slice(s): <list>
- Pattern: <description>
- Confidence: <high/medium/medium-low>

[More patterns as warranted]

## §2. Operating-frame test results

### §2.1 R2 (extension) viability per DECISION-SPACE §1.8

Slice 4 evidence (with audit confirmation): <summary>
Slice 2 architecture support: <summary>
Verdict: <viable / questionable / not-viable> with confidence label.
Implications for §1.8 R1/R2/R3 hybrid: <what changes>

### §2.2 R3 (upstream PR) viability per DECISION-SPACE §1.8

Slice 4 contribution-culture light probe: <raw counts; observations>
What this suggests for R3: <viability assessment with confidence>
What this *doesn't* tell us (deferred deep probe): <list>

### §2.3 §1.7 metaquestion — direction-shifting evidence summary

Per §3.1 starter list and beyond:
- Evidence supporting "uplift-of-gsd-2 is the right shape": <list>
- Evidence challenging "uplift-of-gsd-2 is the right shape": <list>
- Evidence orthogonal to the metaquestion: <list>

Synthesis read: <metaquestion answer surface — direction holds / direction shifts / direction needs incubation-checkpoint deliberation>

### §2.4 §3.4 long-horizon framing-axis

Did the long-horizon framing concretize, or did evidence suggest a different axis (complexity-scale; team-scale; risk-management; value-coherence)?

Slice 5 + slice 4 evidence: <summary>
Cross-slice patterns relevant: <list>
Synthesis read: <axis confirmed / axis questioned / different axis surfaced>

### §2.5 §3.2 design-shape candidates (concrete intervention shapes)

Per §3.2 (patcher / skills / hybrid / something-else): what concrete intervention shapes does the first-wave evidence surface as candidates? Cite which slices' findings each candidate rests on.

This is **surfacing**, not pre-deciding. Second-wave-scoping makes the call.

### §2.6 B4 resolution — slice 5 split

Did the provisional split (concrete in slice 5; abstract in synthesis) hold per pilot disposition? If yes: synthesis carries the abstract long-horizon-relevance interpretation here. If no (slice 5 stayed whole): synthesis integrates without doubling.

Long-horizon-relevance interpretation (if the split held): <interpretation grounded in slice 5's concrete observations + cross-slice features>

## §3. Slice contradictions

Where slice X says something slice Y says differently. Flag concretely; do not paper over.

### §3.1 <contradiction>
- Slice X says: <claim with citation>
- Slice Y says: <claim with citation>
- Audit findings on either: <if audits caught the contradiction>
- Resolution: <if synthesis can resolve> / <flag for incubation-checkpoint>

## §4. Open questions surfaced

Beyond the existing §3 framing questions in INITIATIVE.md. Each: question; why open at synthesis stage; what would resolve.

## §5. Recommendations for incubation-checkpoint

Not "what should we do" but "what should the checkpoint specifically re-evaluate based on these findings." Per DECISION-SPACE §2.3 the checkpoint:
- Re-reads goal articulation
- Checks direction-shifting evidence per §3.1 starter list and beyond
- Checks whether R1/R2/R3 hybrid has narrowed
- Decides whether second-wave proceeds or re-disposition needed

For each above: synthesis-level recommendation about what to look at and why, given first-wave evidence.

## §6. Confidence and limits

- What synthesis couldn't resolve.
- What would need a second wave or different exploration shape.
- Flag if first-wave evidence is insufficient for incubation-checkpoint to operate cleanly (would warrant additional exploration before checkpoint).

## §7. Single-author + same-vendor caveat

This synthesis is a same-vendor (Claude Opus xhigh) reading of the slices and audits. Same-vendor framing-leakage caveat applies. If the paired-synthesis escalation criterion (per "Paired-synthesis escalation criterion" section below) was met, a cross-vendor synthesis was also dispatched; comparison goes in <output path of comparison>. If not escalated, this synthesis is the single-author synthesis input to incubation-checkpoint.
```

## Paired-synthesis escalation criterion

Per decision B3 + dispatch-readiness deliberation §B.2:

After the first synthesis lands, evaluate against the following triggers. **Any one** trigger warrants escalation; the bar is calibrated low because synthesis is the last evidence-stage before incubation-checkpoint.

Escalation triggers:

1. **Decision-shifting claims.** Synthesis claims, if accepted at face value, would change a decision in DECISION-SPACE.md (R2 verdict flips; metaquestion answer flips; design-shape narrows decisively; long-horizon framing-axis shifts).
2. **Load-bearing no-change claims.** Synthesis does not flip a decision but supplies the *primary rationale* for keeping the operating frame intact — i.e., the incubation-checkpoint's confidence in not-pivoting depends substantially on this synthesis's reading.
3. **Major contradiction resolution.** Synthesis resolves a contradiction between two or more slices in a way that materially shapes downstream interpretation.
4. **High-uncertainty interpretive claims at load-bearing positions.** Synthesis carries claims marked medium-low confidence that the incubation-checkpoint would rely on (e.g., "extension surfaces appear to support R2 with caveats X, Y" — caveats whose interpretation a second reader might calibrate differently).

If any trigger fires: **escalate to paired-synthesis.** Dispatch a cross-vendor codex synthesizer independently with same inputs (slices + audits + DECISION-SPACE.md framing + INITIATIVE.md framing). Compare outputs. Write comparison artifact at `.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md`. Both syntheses + comparison feed incubation-checkpoint.

If none fires (synthesis is genuinely refinement-only with no load-bearing positions): **single synthesis suffices.**

The escalation decision is itself a disposition step (record in OVERVIEW §11.5). Cost of escalation: ~2x synthesis dispatch + comparison drafting. Cost of not-escalating-when-warranted: incubation-checkpoint operating on a same-vendor-blinded synthesis at a load-bearing moment.

## Synthesis discipline

- Calibrated language; confidence labels per claim.
- Mark contradictions between slices explicitly; do not paper over.
- Do not pre-decide design shape (second-wave work).
- Do not validate the goal articulation (incubation-checkpoint work).
- Cite slices and audits per finding; reader should be able to trace synthesis claims back to slice observations.
- Surface direction-shifting evidence even where it would be uncomfortable.
- Apply the dispatching project's anti-pattern self-check (`AGENTS.md` "Project-specific anti-patterns to detect"): tournament narrowing; single-lens "interface" by accident; silent defaults; ADR violation by gradual local-reasonable steps; closure pressure at every layer; embedding-model choice as load-bearing decision; single-reader framing claims as authoritative.

---

*W3 synthesis spec for first-wave exploration. Single synthesis is default; paired-synthesis is conditional escalation per B3. Subject to revision based on actual slice + audit outputs (the synthesis prompt may need additions if the inputs reveal coverage gaps).*
