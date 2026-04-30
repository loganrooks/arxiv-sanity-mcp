---
type: phase-D-step-2-practical-decisions
date: 2026-04-30
gsd_2_commit: 42ef05fbe
phase: trajectory plan §1.4 Phase D — first-second-wave-target dispatch + execution
sub-step: §7.10.4 Step 2 — practical decisions (post-Step-1-disposition; pre-Step-3 mini-spec)
status: |
  Drafted by Claude (Opus 4.7, /effort xhigh, in-session-collaboration with Logan)
  per trajectory plan §7.10.4 Step 2 + §0.7 hybrid autonomy (autonomous-within-phase).
  Logan green-lit Step 2 dispatch at /effort xhigh turn 2026-04-30 immediately
  following STEP1-DISPOSITION.md accept-as-stated. Step 2 operationalizes the
  E-primary + A-comparator disposition into work-location / output-staging /
  time-budget+abort / auditor / spike-sizing decisions for Step 3 mini-spec
  drafting and Phase D execution.

authoring_discipline: |
  Step 2 is autonomous-within-phase per plan §0.7 hybrid autonomy: Claude drafts
  practical decisions; Logan-disposition pause-point is the natural Step 4/Step 5
  boundary (gates dispositions + audit dispatch), NOT each Step 2 sub-decision.
  Within Step 2, each sub-decision carries its own auditable reasoning so Phase D
  entry audit (Step 5) can third-reader-stress-test the practical-decision shape
  alongside Step 1 design-framing and Step 3 mini-spec.

  D5a in-session-collaboration risk applies recursively: Step 2 inherits Logan-
  framing inheritance from Step 1 disposition. Phase D entry audit per plan §2.4
  row D paired (same-vendor xhigh adversarial-auditor of design framing +
  cross-vendor xhigh audit of evidence-load) is the structural correction.

ground:
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md (axis 1-4 dispositions; load-bearing for Step 2 scope)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md (5-candidate surfacing)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md (sub-option (ii) caveat as standing constraint)
  - .planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md (skill subsystem snapshot; primitives inventory)
  - .planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md §7.10.4 Step 2 + §7.10.5 executor checklist
  - .planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md §1.4 + §2.4 row D + §3.1 + §0.7
  - .planning/spikes/METHODOLOGY.md (six lenses; paired-review practices; M4 spike-sizing)
  - ~/workspace/projects/gsd-2-explore/ at commit 42ef05fbe (verified branch=main, clean tree, fresh-pulled 2026-04-30)
  - reference_spike_design.md provenance pointer (per §0.5 self-containment caveat: optional; bullet content here governs)

read_order: |
  - For "what was disposed and how": §1 dispositions table.
  - For "per-decision reasoning + defenses": §2.H6 / §2.H7 / §2.M1 / §2.M3 / §2.M4.
  - For "audit-priority risks Step 2 acknowledges": §3.
  - For "what Phase D entry audit (Step 5) reads from Step 2": §4 cross-references.
---

# Phase D Step 2 — Practical decisions

This artifact operationalizes the Step 1 dispositions (E primary + A comparator + gap-mapping at Step 1 + F/G OOS per STEP1-DISPOSITION.md) into the five practical decisions specified at INCUBATION-CHECKPOINT.md §7.10.4 Step 2 + §7.10.5 executor checklist.

## §1. Dispositions

| Decision | Disposition | Confidence |
|---|---|---|
| **H6 — Work-location** | (a) existing clone at `~/workspace/projects/gsd-2-explore/` + new working-branch `phase-d-decision-trace-spike` (off `main` at 42ef05fbe); Shape A artifacts at `~/.agents/skills/decision-trace/` (user-side; no clone interaction) | high |
| **H7 — Output staging** | `.planning/gsd-2-uplift/wave-2/decision-trace/` for Phase D execution outputs (MINI-SPEC + EXECUTION-LOG + FINDINGS); pointer artifacts cite Shape E location in gsd-2 clone + Shape A location at user-side; audit folder `.planning/gsd-2-uplift/audits/2026-MM-DD-phase-d-entry-audit/` per plan §3.2 | high |
| **M1 — Time-budget + abort triggers** | 8 working-day hard limit; 5 explicit abort triggers (day-4 runnable checkpoint / branch-lifetime / coordination-cascade / description-keyword-rewrite-overrun / P5-caveat-blocks-core-behavior) | medium-high |
| **M3 — Auditor selection** | Paired per plan §2.4 row D: same-vendor `adversarial-auditor-xhigh` Claude agent (design framing; xhigh effort; independent mode) + cross-vendor codex GPT-5.5 xhigh (evidence-load); both fire on same corpus | high |
| **M4 — Spike-sizing envelope** | Skill-only at Phase D (workflow template + schema enrichment + hooks + YAML workflow all OOS); ≤500 lines per skill per create-skill doctrine; ≤2 coordination touchpoints (new skill + per-unit-type allowlist update if needed); falsifiable observation on ≥1 real decision-trace task | medium-high |

## §2. Per-decision reasoning

### §2.H6 — Work-location

**Disposition:** (a) Existing clone at `~/workspace/projects/gsd-2-explore/` + new working-branch `phase-d-decision-trace-spike` off `main` at commit 42ef05fbe (verified 2026-04-30: branch=main, clean tree, fresh-pulled). Shape A artifacts at `~/.agents/skills/decision-trace/` (user-side discovery; no gsd-2 clone interaction).

**Options considered:**

| Option | Verdict | Reasoning |
|---|---|---|
| (a) Existing clone + new working-branch | **chosen** | Reversible (revert branch); existing clone is fresh-pulled at commit 42ef05fbe matching M2 + P5 evidence base; no isolation overhead |
| (b) Fresh clone for Phase D | rejected | Adds clone overhead without isolation benefit; existing clone is clean |
| (c) Fork on GitHub then clone fork | rejected | Commits to R5-prep posture before evidence licenses (per axis 1 disposition: R5 deferred); premature |
| (d) Sandbox via worktree | rejected | Adds complexity for spike-scale work; branch isolation suffices for reversibility |
| (e) Design-only (no code) | rejected | Phase D is "execute first-target" per plan §1.4; design-only is Phase C-shaped |

**Defense against challenges:**

- **"Why not fork? We have direct intervention authority."** Direct intervention authority means we CAN modify gsd-2 source on a working-branch; it does NOT mean we must commit to upstream-PR posture pre-evidence. Fork-first conflates "modify source" with "prepare PR" — the latter is Phase E-conditional per axis 1 disposition. A working-branch on the existing clone preserves R2-with-PR-deferral correctly.
- **"Won't M2's exploration state contaminate the working-branch?"** No: M2 was read-only (per its scope frontmatter). Working-tree was clean post-M2; branch is fresh off `main` at 42ef05fbe.
- **"What if we need to reset?"** Branch-revert is a single command. If the branch overruns the M1 abort triggers, `git checkout main && git branch -D phase-d-decision-trace-spike` resets cleanly.

**Operational specifics:**

- Branch creation command (run at Phase D dispatch): `cd ~/workspace/projects/gsd-2-explore && git checkout -b phase-d-decision-trace-spike main`
- Commit pattern within branch: small atomic commits per spike-program METHODOLOGY (each commit reverts cleanly; squash-merge eligible if Phase E licenses upstream PR).
- Shape A artifact location: `~/.agents/skills/decision-trace/SKILL.md` (single file initially; router subdirectories per `create-skill/SKILL.md:23-34` only if Step 3 mini-spec licenses).

### §2.H7 — Output staging

**Disposition:** `.planning/gsd-2-uplift/wave-2/decision-trace/` for Phase D execution outputs in arxiv-sanity-mcp planning tree. Audit folder per plan §3.2 at `.planning/gsd-2-uplift/audits/2026-MM-DD-phase-d-entry-audit/` (date stamped at Step 5 dispatch).

**Sub-structure:**

```
.planning/gsd-2-uplift/wave-2/decision-trace/
  MINI-SPEC.md              # Step 3 output: Phase D dispatch contract (gate 3 amended)
  EXECUTION-LOG.md          # Records build + observation + per-task notes during Phase D execution
  FINDINGS.md               # Phase D evidence corpus (post-execution); reads against §7 dispositions for Phase E
  shape-e-pointer.md        # ~10 lines: Shape E artifact lives at gsd-2-explore branch:src/resources/skills/decision-trace/SKILL.md (commit hash recorded)
  shape-a-pointer.md        # ~10 lines: Shape A artifact lives at ~/.agents/skills/decision-trace/SKILL.md (snapshot hash recorded)
```

**Reasoning:**

- Per plan §3.1 Phase D row: "`.planning/gsd-2-uplift/wave-2/${target-name}/`" — pattern fixed; `target-name = decision-trace`.
- Skill artifacts themselves DO NOT live in arxiv-sanity-mcp planning tree (they live at gsd-2 clone + user-side). Pointer artifacts capture identity + location + commit/snapshot hash so Phase E + extraction phases can resolve them.
- Audit folder follows plan §3.2 naming convention (date-stamped at dispatch, not pre-created).

**Defense:**

- **"Why pointer artifacts vs full snapshot?"** Snapshotting skill files into arxiv-sanity-mcp tree creates a third copy of the artifact (gsd-2 clone + user-side + arxiv-sanity-mcp pointer) that drifts. Pointer with commit/snapshot hash gives traceability without copy-management overhead. Phase H extraction can resolve via the recorded hash.
- **"What about post-extraction custody?"** Per plan §1.7 artifact-by-artifact table: `wave-2/` MOVES to new repo on extraction. Pointer artifacts move with it; their referenced gsd-2 clone state remains accessible via commit hash even after extraction.

### §2.M1 — Time-budget + abort triggers

**Disposition:** 8 working-day hard limit (within plan §1.4 implicit "1-2 weeks" range). 5 explicit abort triggers below.

**Time-budget reasoning:**

- Plan §1.4 implies 1-2 week range per M1 default; 8 working days = 1.6 calendar weeks at 5-day work-week, conservative within range.
- Spike-program METHODOLOGY emphasizes "earliest possible test"; 8 days allows 4 days build + 4 days observation + iteration.
- 8 days is a **hard limit**, not a soft target: if Phase D requires more, the abort triggers fire before the limit is reached.

**Abort triggers (each falsifiable + observable):**

1. **Day 4 runnable-checkpoint failure.** If by end of working-day 4 neither Shape E (in-tree skill) nor Shape A (user-side skill) is *runnable* — runnable defined as: gsd-2 discovers + lists in `<available_skills>` block per `auto-prompts.ts:707-797`; description-keyword match fires for at least one decision-trace-shaped activation context — abort and revisit Step 1 design-space. Reasoning: spike-program METHODOLOGY argues the earliest possible test should fire by mid-spike; runnable-by-day-4 is conservative.

2. **Branch-lifetime overrun (8-day hard limit).** If working-branch `phase-d-decision-trace-spike` exceeds 8 working days without convergent observation evidence (i.e., we can't write FINDINGS.md against the dispositions yet), abort: revert branch and re-design-space at Step 1. Per axis 1 risk #6 (working-branch R2 may drift toward commitment): "the longer the branch lives, the harder reversal becomes."

3. **Coordination cascade beyond bounded scope.** If Shape E execution requires modifying >2 surfaces beyond the new SKILL.md (e.g., per-unit-type allowlist update + auto-prompts integration + extension-validator update + manifest test update), abort: re-evaluate at Step 1 as "test was actually D-shaped or F-shaped, not E-shaped." The 2-surface cap matches M4 spike-sizing envelope (new skill + optional allowlist update).

4. **Description-keyword rewrite overrun.** Per `create-skill/SKILL.md:58`: "Rewrite at least twice before settling." If E's or A's description requires >3 rewrites to achieve discrimination from `forensics`/`handoff`/existing skills, surface as Phase D evidence (yellow flag, not hard abort): the description-keyword discriminability is itself substrate-shape evidence — gsd-2's keyword-driven activation may be brittle for reconstruction-shaped semantics.

5. **P5 effective-state caveat blocks core skill behavior.** If reading PREFERENCES.md directly turns out insufficient for layer attribution (project / global / profile / mode distinction is not reconstructible from on-disk files alone), surface as Phase D evidence + flag for Phase E re-disposition of P5 sub-option (might trigger sub-option (i) re-scope retroactively).

**Defense against challenges:**

- **"8 days is too tight for E + A + observation + iteration."** If 8 days is genuinely too tight, that itself is Phase D evidence — Shape E may be more invasive than the spike-shape framing acknowledged. Day-4 checkpoint catches this pattern before the hard limit fires.
- **"Why hard limit instead of soft target?"** Soft targets drift. Hard limit + day-4 checkpoint together create a calibration loop: if day-4 fails, abort; if day-4 passes, the remaining 4 days are spent on observation + iteration with confidence the build is functional.
- **"What if abort triggers fire and we lose Phase D?"** Aborting Phase D back to Step 1 design-space is *productive curiosity* per plan §5.4 — the spike generated evidence that the chosen shape is wrong-shaped. Re-design-space with that evidence; this is the spike-program working as intended.

### §2.M3 — Auditor selection

**Disposition:** Paired per plan §2.4 row D design-shape:
- **Same-vendor:** `adversarial-auditor-xhigh` Claude agent at xhigh reasoning-effort, **independent mode** (does not read cross-vendor output before producing its own; per AUDIT-SPEC.md §3.4 manual-discretion override pattern from premise-bleed audit).
- **Cross-vendor:** codex GPT-5.5 at xhigh reasoning-effort.

Both auditors fire on the same corpus (§4 cross-references). Differential analysis (DIFFERENTIAL.md) follows premise-bleed audit precedent.

**Reasoning:**

- Plan §2.4 row D explicitly specifies design-shape audits at xhigh both vendors. Phase D first-target IS design-shape (E primary; not probe-shape).
- Independent same-vendor mode catches integration-grammar-as-fact at meta-level (the §7.1 residual the premise-bleed audit caught); cross-vendor catches vocabulary/substance (the Step-1 cross-vendor canonical strength).
- Per §0.6 failure-mode taxonomy + plan §2.4 reasoning-level rationale: Phase D first-target carries framing-load (decision-trace shape selection) + cross-cutting reasoning (Step 1 + Step 2 + Step 3 read together) + decision-stake (Phase E reads Phase D evidence). All three signals point to xhigh.

**Defense:**

- **"Why paired? Single-vendor would be cheaper."** Single-vendor at design-shape work is M1 strict-undersell per plan §0.6: the failure-modes (framing-error + premise-bleed + integration-grammar-as-fact) require BOTH vendor positions. Premise-bleed audit precedent (Phase A → Phase A-audit) established this.
- **"Why independent mode for same-vendor?"** Differential mode would let same-vendor read cross-vendor first; that creates anchoring effects. Independent mode preserves the M1 paired-review property's same-vendor strength (register/integration-grammar detection) without cross-vendor priming.

### §2.M4 — Spike-sizing envelope

**Disposition:** Skill-only at Phase D. ≤500 lines per skill per `create-skill/SKILL.md:42-54` doctrine. ≤2 coordination touchpoints. Falsifiable observation on ≥1 real decision-trace task.

**In scope:**

| Item | Specification |
|---|---|
| Build Shape E | In-tree gsd-2 skill at `src/resources/skills/decision-trace/SKILL.md` (single SKILL.md ≤500 lines; YAML frontmatter per `skills.ts:81-95` validation; pure-prompt body) |
| Build Shape A | User-side gsd-2 skill at `~/.agents/skills/decision-trace/SKILL.md` (single SKILL.md ≤500 lines; same frontmatter shape) |
| Per-unit-type allowlist update (conditional) | If Step 3 mini-spec disposes "decision-trace activates at `complete-milestone` / etc.": update `skill-manifest.ts:33-123` `UNIT_TYPE_SKILL_MANIFEST`. This is the second of ≤2 coordination touchpoints. **Per Phase D entry audit F-PD-A4 disposition:** activation surface is 5-dimensional (D1-D5 per MINI-SPEC §1.E activation matrix); P3 + B3 test-step routing must use unit-types with `preferences:"active-only"` (e.g., `complete-milestone` per `unit-context-manifest.ts:402-421`) NOT `reassess-roadmap` (`preferences:"none"` per `:508-523`). |
| Test on ≥1 real decision-trace task | Reconstruct rationale chain from arxiv-sanity-mcp's `.planning/deliberations/` per MINI-SPEC §2.3 test-task disposition. **Per Phase D entry audit F-PD-A5 + F-PD-B2 disposition:** primary task must be non-co-produced (pre-current-arc deliberation; e.g., 2026-04-26 uplift initiative genesis) to reduce D5a inheritance; framing-widening (2026-04-28) is co-produced and reads as backup-with-D5a-caveat. Capture observation in EXECUTION-LOG.md with H5 channel-(a)/(b)/(a→b) inline tags per MINI-SPEC §7.3 + §8.4 inline-tagging discipline. |
| Description-keyword discrimination | Up to 3 rewrites per `create-skill/SKILL.md:58` "rewrite at least twice"; surface as Phase D evidence if >3 rewrites needed |
| Capture P5 caveat handling | Skill prompt instructs reading `~/.gsd/PREFERENCES.md` + `.gsd/PREFERENCES.md` directly; layer attribution preserved in trace artifact format |

**Out of scope:**

| Item | Disposition reference |
|---|---|
| Workflow template (markdown-phase or YAML) | Deferred to Phase E if E's evidence licenses; per axis 1 disposition |
| Schema enrichment of `.gsd/DECISIONS.md` | Shape D — out-of-scope-this-arc per axis 1 |
| Hook primitive | Shape F — OOS-this-arc per axis 4 |
| YAML deterministic workflow | Shape G — OOS-this-arc per axis 4 |
| Upstream PR | Phase E-conditional; gated by §7.3.b R3 contribution-culture probe re-disposition |
| Cross-project decision-trace | Per-project scope only at Phase D; cross-project surface is a different question |
| Heal-skill / skill-health subsystem integration | M2 §8 open question 3; flagged for Phase E |
| `gsd_progress` vs `headless query` state-coherence drift | P5 §7 open question 2; flagged for Phase E |
| Validation-layer silent-drop hypothesis | P5 §7 open question 1; flagged for Phase E |
| Router-pattern subdirectories (`workflows/`, `references/`, `templates/`, `scripts/`) | Default skill-only single SKILL.md; router pattern only if Step 3 mini-spec licenses based on description-keyword discrimination work |

**Defense:**

- **"Why ≤2 coordination touchpoints? E may genuinely need more."** If E genuinely needs >2 surfaces, that's a coordination-cascade abort trigger (M1 #3) — the chosen shape is wrong-shaped, not under-scoped. The 2-surface cap forces the question.
- **"Why a real task instead of synthetic?"** Synthetic tasks let the skill author shape the task to fit the skill; real tasks (arxiv-sanity-mcp deliberations) test whether the skill's shape fits work shapes the skill didn't anticipate. Higher evidence value.
- **"Which deliberation as test task?"** Step 3 mini-spec disposes specific test-task; candidates include framing-widening (2026-04-28), premise-bleed audit-arc (2026-04-28), incubation-checkpoint dispositions (2026-04-29). Each has different complexity; mini-spec picks based on falsifiability + scope.

## §3. Audit-priority risks Step 2 acknowledges

1. **Branch-lifetime drift toward commitment.** Working-branch R2 reversibility erodes with branch age. Day-4 checkpoint + 8-day hard limit + branch-revert procedure are explicit mitigations; if these fail to fire when warranted, Phase D entry audit (Step 5) catches.

2. **8-day budget calibration is medium-confidence.** No prior gsd-2-side spike provides a base rate for "build + observe + iterate on a new in-tree skill." If 8 days is wrong-calibration, day-4 checkpoint surfaces it; abort to re-design-space rather than extending.

3. **Per-unit-type allowlist update may force wider Step 3 scope question prematurely.** The allowlist entry depends on which lifecycle steps decision-trace activates at — itself a Step 3 mini-spec disposition. Step 2 marks it conditional; Step 3 forces the choice.

4. **Test-task selection (which deliberation) carries framing inheritance.** All candidate test-tasks are Claude+Logan co-produced under in-session collaboration. Choosing one over another carries D5a inheritance. Step 3 mini-spec's test-task selection should explicitly name this inheritance + carry falsifiable predictions per H4.

5. **Pointer-artifact-with-hash as custody pattern is convention-asserting.** Step 2 H7 disposition asserts pointer artifacts at `wave-2/decision-trace/` with commit/snapshot hashes are the right custody pattern for Phase E + extraction. Phase D entry audit catches if this convention is over-fit (e.g., should we snapshot a copy after all? does extraction really resolve via hash cleanly?).

6. **Independent-mode same-vendor + cross-vendor pairing inherits premise-bleed audit precedent.** That precedent fired on a single audit-arc; treating it as universal pattern for Phase D-shape audits is a generalization. If the precedent doesn't hold here (e.g., differential mode would catch what independent misses), Step 5 surfaces.

7. **D5a recursion at Step 2.** Step 2 inherits Logan-framing inheritance from STEP1-DISPOSITION.md (which co-produced under /effort max + /effort xhigh accept). Phase D entry audit per plan §2.4 row D paired is the structural correction — reads §7.10 + STEP1-design-space + STEP1-DISPOSITION + this Step 2 + Step 3 mini-spec together.

## §4. Cross-references

### Step 0 + Step 1 outputs (load-bearing for Step 2)

- `.planning/gsd-2-uplift/wave-2/pre-D-probes/P5-effective-state-emission-findings.md` — sub-option (ii) caveat as standing constraint; M1 abort trigger #5 references it.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/M2-codebase-snapshot-findings.md` — primitives inventory; H7 pointer-artifact custody references its R-strategy table.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-design-space.md` — 5-candidate surfacing.
- `.planning/gsd-2-uplift/wave-2/pre-D-probes/STEP1-DISPOSITION.md` — axis 1-4 dispositions; load-bearing for Step 2 scope.

### Standing context

- `.planning/gsd-2-uplift/exploration/INCUBATION-CHECKPOINT.md` §7.10.4 Step 2 + §7.10.5 executor checklist (H6/H7/M1/M3/M4 enumeration).
- `.planning/gsd-2-uplift/RELATIONSHIP-TO-PARENT.md` §1 (test-case-vs-substrate; H5 anchor referenced by mini-spec).
- `.planning/gsd-2-uplift/audits/2026-04-29-incubation-checkpoint-audit/DISPOSITION.md` §8 (Phase D entry pre-mini-spec amendment).

### Trajectory plan governance

- `.planning/gsd-2-uplift/trajectory/cheerful-forging-galaxy.md` §1.4 Phase D goal + §2.4 row D audit shape (paired) + §3.1 artifact location + §3.2 audit-folder naming + §0.7 hybrid autonomy.

### Methodology grounding

- `.planning/spikes/METHODOLOGY.md` six interpretive lenses + paired-review practices A-F (load-bearing for M3 auditor selection + M4 spike-sizing).
- `.planning/foundation-audit/METHODOLOGY.md` decision-review epistemic discipline (carries through to Step 3 mini-spec gate-3 amendments).

### What Phase D entry audit (Step 5) reads from Step 2

Per plan §2.4 row D paired (same-vendor xhigh adversarial-auditor of design framing + cross-vendor xhigh audit of evidence-load):

- This Step 2 artifact (work-location / staging / budget / auditor / sizing decisions + reasoning + acknowledged risks)
- Day-4 checkpoint result (if reached pre-audit; auditor reads the runnable-state evidence)
- Branch state at audit time (branch hasn't drifted past Step 5 dispatch)
- Test-task selection rationale (carried in Step 3 mini-spec but referenced here)

The audit reads Step 2 alongside §7.10 + STEP1-design-space + STEP1-DISPOSITION + Step 3 mini-spec — structural correction for Step 2's D5a inheritance + practical-decision quality + spike-sizing envelope calibration.

### Logan-disposition turn

- 2026-04-30 /effort xhigh "green light" — autonomous-within-phase Step 2 dispatch authorized per plan §0.7 hybrid autonomy. Step 2 sub-decisions are Claude-disposed within scope; pause-point is Step 4/Step 5 (gates dispositions + audit dispatch).

---

*Step 2 practical decisions artifact authored by Claude (Opus 4.7, /effort xhigh) 2026-04-30 in-session-collaboration with Logan per trajectory plan §7.10.4 Step 2 + §0.7 hybrid autonomy. Sub-decisions are Claude-disposed within scope; reasoning is auditable. The in-session-collaboration risk applies recursively; Phase D entry audit per plan §2.4 row D paired is the structural correction. Subject to same fallibility caveat as STEP1-DISPOSITION.md and DECISION-SPACE.md §0.*
