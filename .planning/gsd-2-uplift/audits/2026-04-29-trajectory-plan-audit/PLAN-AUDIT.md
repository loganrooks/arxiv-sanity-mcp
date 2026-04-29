---
type: trajectory-plan-audit-findings
date: 2026-04-29
auditor: codex GPT-5.5 xhigh (cross-vendor; plan-self-audit)
plan_file: /home/rookslog/.claude/plans/cheerful-forging-galaxy.md
target: trajectory plan + standing context per §0.4 mandatory pre-reading
status: complete
---

# §0. Summary + Classification Breakdown

- Total findings surfaced: 9
- Classification breakdown:
  - Class A (cosmetic / wording-addendum): 1
  - Class B (substantive but non-trajectory-changing): 6
  - Class C (load-bearing trajectory shape): 2
- Top-line read: the plan largely lives up to its declared framing-as-load-bearing principle. The horizon stack is explicit; incubation remains Logan-disposed; the audit cadence is mostly calibrated rather than blanket-maximal; and the plan has real negative-space and failure-loop machinery.
- The most concerning items are not the central deliberation arc. They are artifact-control and extraction-shape issues: the plan is outside the repo but the Phase A commit map treats it as committable, and Phase G's move/stay map conflicts with the initiative's own migration-trigger text for `DECISION-SPACE.md` and deliberation records.
- Highest-risk lens questions: Lens 5 (backward-traceable responsibility), Lens 6 (fresh-session onboarding), and Lens 7 (negative space). Lens 2 returns one internal inconsistency around Phase G reasoning level, but the underlying high-vs-xhigh principle is strong.
- Non-binding disposition signal: commit-as-is is defensible only if Logan reads the Class C items as execution housekeeping rather than trajectory-shaping. Commit-with-addendum is plausible if the two Class C items are resolved by a pre-execution addendum that changes artifact custody and Phase G migration rules. Revise-before-execute is plausible if Logan wants the committed plan itself, not an addendum, to be the execution authority.

Read notes:
- I read the plan in full.
- I read the requested standing context targeted to the audit lens, including `CLAUDE.md`, `AGENTS.md`, `.planning/LONG-ARC.md`, `INITIATIVE.md`, `DECISION-SPACE.md`, `framing-widening.md`, `SYNTHESIS-COMPARISON.md`, the premise-bleed audit spec/differential/disposition with sampled findings, `META-SYNTHESIS.md`, `.planning/STATE.md`, and the two methodology files named in the plan's §0.4.
- I did not read this conversation transcript, `/tmp/phase-a-plan-audit-dispatch.md`, or any `.logs/` subdirectory.
- I also did not read the memory files named in the plan's §7, because they are not in §0.4's mandatory pre-reading list and the audit input boundary is plan + §0.4 standing context + audit folder.

# §1. Per-Instance Findings

### Finding 1 — Phase A commit map treats an external runtime plan file as if it can be committed with the repo audit

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §1.1, §3.1, §7; lines 151, 166, 457, 631
- **Quote:** "Outputs: `.planning/gsd-2-uplift/audits/2026-04-29-trajectory-plan-audit/PLAN-AUDIT.md`" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:151`)
- **Quote:** "Commit: `docs(gsd-2-uplift): trajectory plan + plan-self-audit (pre-execution)` — plan file + audit folder + DISPOSITION.md if needed." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:166`)
- **Quote:** "Plan file: `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md` (this file)." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:631`)
- **Lens-question:** 5 (commit-map traceability), 6 (fresh-session execution), 7 (negative-space artifact custody)
- **Type:** artifact-map / commit-map / negative-space
- **Classification:** **Class C**
- **Justification:** The plan is itself the load-bearing framing artifact, but its authoritative location is outside the arxiv-sanity-mcp git worktree. The Phase A commit shape says the "plan file" commits with the audit folder, yet the plan path is under `/home/rookslog/.claude/plans/`, not under `.planning/`. That means the repo commit cannot actually preserve the plan artifact unless execution first creates a committed copy or a committed immutable reference. This directly affects backward-traceable responsibility: future readers can have `PLAN-AUDIT.md` without the exact plan it audited.
- **Why this is trajectory-shape, not housekeeping:** Phase A is the root gate for all later execution. If the plan is not committed or content-addressed in the repo, later Phase C-H artifacts cannot trace the execution trajectory back to the audited plan text. This undercuts the plan's own stated requirement that responsibility be traceable backward.
- **What dissolves:** before Phase A is disposed, either copy the plan into the audit folder or `.planning/gsd-2-uplift/trajectory/` and commit that copy, or record a content hash plus durable archived copy path in `PLAN-AUDIT.md` / `DISPOSITION.md`. The commit map should say exactly which committed artifact is the authority.

### Finding 2 — Phase G's move/stay map conflicts with INITIATIVE.md §7 on `DECISION-SPACE.md` and deliberation records

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §1.7; lines 291-295
- **Quote:** "What moves to new repo (per INITIATIVE.md §7 + this plan's analysis): `.planning/gsd-2-uplift/` (entire tree: INITIATIVE.md + DECISION-SPACE.md + audits/ + exploration/ + orchestration/)." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:291-293`)
- **Grounding artifact:** `.planning/gsd-2-uplift/INITIATIVE.md`
- **Grounding quote:** "The decision-space and the deliberation log stay in arxiv-sanity-mcp's `.planning/` (they record arxiv-sanity-mcp's session that genesised the initiative); INITIATIVE.md and exploration outputs migrate to the new repo as initiative-scoping artifacts." (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/INITIATIVE.md:181`)
- **Lens-question:** 4 (deliberation discipline), 5 (backward traceability), 7 (negative-space move/stay exclusions)
- **Type:** cross-artifact inconsistency / migration-shape
- **Classification:** **Class C**
- **Justification:** The plan says it is following `INITIATIVE.md §7`, but then changes the migration semantics by moving the entire `.planning/gsd-2-uplift/` tree including `DECISION-SPACE.md`. The initiative text explicitly says `DECISION-SPACE.md` and the deliberation log stay in arxiv-sanity-mcp because they record the genesis session. This is not a local wording issue: Phase G's extraction map determines which repo owns the decision record, which repo owns the initiative artifacts, and how future responsibility traces backward.
- **Why this is trajectory-shape:** the extraction trajectory's endpoint changes depending on whether `DECISION-SPACE.md` migrates, is duplicated, or stays with bidirectional references. The plan also says uplift-scoped deliberations "likely 2026-04-26 onward" move subject to per-deliberation Logan disposition (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:293`), which is compatible with deliberation discipline, but the `DECISION-SPACE.md` move is not similarly Logan-disposed against the prior artifact.
- **What dissolves:** Phase G needs an explicit artifact-by-artifact move/stay/duplicate/reference table that reconciles with `INITIATIVE.md §7`. At minimum, `DECISION-SPACE.md` needs a Logan-disposed treatment: stay, move, copy, or split into genesis-vs-current-decision records. Deliberations need the same table, not only "likely 2026-04-26 onward."

### Finding 3 — Mandatory pre-reading points to a non-existent root `LONG-ARC.md` path

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §0.4 and §7; lines 70 and 636
- **Quote:** "`/home/rookslog/workspace/projects/arxiv-sanity-mcp/LONG-ARC.md` — anti-patterns + protected seams + doctrine-interaction-with-spike-program." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:70`)
- **Quote:** "- arxiv-sanity-mcp/LONG-ARC.md" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:636`)
- **Grounding artifact:** `.planning/LONG-ARC.md`
- **Grounding quote:** "document: LONG-ARC" and "scope: Durable doctrine that disciplines current planning to preserve VISION.md without overscoping into it." (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/LONG-ARC.md:2-5`)
- **Lens-question:** 1 (standing context load-bearing), 6 (fresh-session onboarding), 7 (negative-space path drift)
- **Type:** onboarding / authority path
- **Classification:** **Class B**
- **Justification:** The file that exists and was readable is `.planning/LONG-ARC.md`, while the plan's exact mandatory path points to a root-level `LONG-ARC.md`. A fresh executor following §0.4 literally will fail one of the "Do not skip" pre-reading steps. The error is substantive because `LONG-ARC.md` is repeatedly treated as doctrine ground for closure pressure, single-reader framing claims, and protected seams.
- **Why not Class C:** this does not change the trajectory shape if corrected; it is an authority-path defect, not a reason to reroute phases.
- **What dissolves:** update §0.4 and §7 to `.planning/LONG-ARC.md`, or explicitly state that `LONG-ARC.md` is shorthand for `.planning/LONG-ARC.md` in this repo.

### Finding 4 — Failure-mode taxonomy is richer than the operational handling map

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §0.6 and §5; lines 105-123, 537-589
- **Quote:** "Different kinds of erring need different checks. The plan's quality gates target each:" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:105-107`)
- **Quote:** "If new framing-bleed surfaces mid-execution" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:551`)
- **Quote:** "If scope creep emerges" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:560`)
- **Lens-question:** 3 (active vs nominal failure-mode handling), 7 (which kinds of erring are absent)
- **Type:** negative-space / failure-mode operationalization
- **Classification:** **Class B**
- **Justification:** §0.6 names thirteen kinds of erring, including comparative-claims-without-comparative-data, false-confidence calibration, comfort-language, performative-vs-operational openness, integration-grammar-as-fact, skill-heuristic shallow-match, execution error, and in-session-collaboration risk. §5 operationalizes gate failure, framing bleed, scope creep, productive curiosity, and Logan discretion. Several named failure modes therefore rely on generic audits or the executor's memory of §0.6 rather than on concrete per-phase procedures.
- **Why this matters:** the plan says its quality gates target each kind, but a fresh executor would not have a checklist showing where each taxonomy item is applied after Phase A. That makes the taxonomy partly active and partly nominal.
- **Why not Class C:** the plan still has real gates, audit cadence, §0.6 checks, and per-phase verification. This can be fixed by adding a compact mapping table without changing the eight-phase trajectory.
- **What dissolves:** add a §5.6 or appendix mapping each §0.6 failure mode to (i) phases where it applies, (ii) concrete check, (iii) artifact where disposition is recorded, and (iv) whether Logan, auditor, or executor owns the call.

### Finding 5 — Phase G audit level is internally inconsistent: xhigh in the phase, high in the reasoning table

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §1.7 and §2.4; lines 324 and 431-432
- **Quote:** "Quality gate: Cross-vendor xhigh audit of EXTRACTION-LOG.md + sample-check that new repo's load-bearing artifacts reference internal-only" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:324`)
- **Quote:** "G | Extraction execution audit | Cross-vendor codex GPT-5.5 | **high** | Mechanical-coherence: orphan-reference check + missed-migration check + cross-reference integrity. Bounded scope. Deep reasoning not required. high suffices. xhigh would be over-engineered." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:432`)
- **Lens-question:** 2 (quality-gating discipline and reasoning-level calibration)
- **Type:** audit-cadence inconsistency
- **Classification:** **Class B**
- **Justification:** The reasoning-level principle is well-articulated: framing-load + cross-cutting + decision-stake + negative-space depth push toward xhigh; mechanical coherence and bounded register checks can use high (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:405-417`). The Phase G table applies that principle elegantly: high is enough because extraction execution checks orphan references, missed migrations, and cross-reference integrity. But Phase G's own quality gate says xhigh.
- **Why this matters:** the plan can dispatch the wrong audit level depending on which section the executor treats as authoritative. It also weakens the plan's claim that reasoning effort is judged per audit rather than blanket-maxed.
- **Why not Class C:** the correct resolution is already present in §2.4. Aligning §1.7 with §2.4 does not change the trajectory, only the audit dispatch.
- **What dissolves:** change Phase G's quality gate to cross-vendor high, or add a specific reason why Phase G's actual sample-check includes enough framing-load to override the table.

### Finding 6 — §0.5 depends on `feedback_*` / `reference_*` memory artifacts without making them mandatory, citable, or self-contained

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §0.5 and §7; lines 95-103 and 655-661
- **Quote:** "Epistemic rigor (per `feedback_epistemic_rigor`). No premature conclusions. Comparative claims need comparative data. No 'fast enough' framing." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:95`)
- **Quote:** "No-explore-for-audits (per `feedback_no_explore_for_audits`). Default Explore agent is for code-search, not audit-grade analysis." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:101`)
- **Quote:** "**Memory references (per-Logan-personalization, may apply to future sessions):**" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:655`)
- **Lens-question:** 6 (fresh-session onboarding), 7 (excluded context)
- **Type:** onboarding / provenance
- **Classification:** **Class B**
- **Justification:** The §0.5 bullets do carry usable discipline summaries, so a fresh executor is not helpless. But the plan cites memory-derived authorities as if they ground execution norms while listing those memory files only later as "may apply," not as mandatory pre-reading. That leaves a provenance gap: future execution can invoke "per feedback_epistemic_rigor" without a project-committed, audit-visible source.
- **Why this matters:** Logan intends to clear context. Any load-bearing discipline that is only in runtime memory or personal feedback files can be unavailable, stale, or forbidden by a narrower dispatch boundary. The plan's strongest fresh-session claim should not depend on optional memory references.
- **Why not Class C:** §0.5 paraphrases enough of the discipline for execution; the missing piece is citation/authority hygiene, not trajectory shape.
- **What dissolves:** either make the discipline fully self-contained in §0.5 with no external memory dependence, or move exact memory paths into §0.4 as optional provenance with a rule that execution does not depend on reading them.

### Finding 7 — Phase H's "without reference to arxiv-sanity-mcp" test overstates internal coherence and risks erasing the diagnostic-loop dependency

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §1.8, with cross-check to §0.3 and §1.7; lines 60-62, 303-310, 339
- **Quote:** "arxiv-sanity-mcp's spike-program outputs are *evidence about substrate behavior*, not just project-specific decisions." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:62`)
- **Quote:** "What gets cited-by-reference from new repo to arxiv-sanity-mcp: Spike-program outputs (as evidence about substrate behavior under arxiv-sanity-mcp-spike conditions)." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:303-304`)
- **Quote:** "can it reconstruct the medium-horizon and short-horizon work without reference to arxiv-sanity-mcp?" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:339`)
- **Lens-question:** 1 (test-case-vs-substrate preservation), 6 (fresh-session test), 7 (excluded dependency)
- **Type:** verification criterion / negative-space
- **Classification:** **Class B** with Class C boundary if read literally
- **Justification:** The plan correctly insists that arxiv-sanity-mcp is diagnostic for substrate-shape, and Phase G explicitly says the new repo cites spike-program and foundation-audit outputs by reference. Phase H then asks whether the new repo can reconstruct medium/short-horizon work "without reference to arxiv-sanity-mcp." That is too absolute. The intended test should be "without requiring arxiv-sanity-mcp as the primary home for uplift state," not "without reference" to the diagnostic test case.
- **Why this matters:** an executor trying to satisfy the literal Phase H test might over-purify the new repo by removing or minimizing references that §0.3 says are diagnostic and that §1.7 says should remain cited-by-reference.
- **Why not Class C by default:** nearby Phase G text preserves the cross-reference design, so the literal overstatement is correctable without changing the endpoint.
- **What dissolves:** revise Phase H test to: "can it reconstruct the uplift initiative's medium/short-horizon state from new-repo-local artifacts, while following explicit references back to arxiv-sanity-mcp for diagnostic evidence?"

### Finding 8 — Commit-map traceability lacks cross-repo commit identity requirements for extraction

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** §4.2 and Phase G/H commit patterns; lines 511-523, 328-331, 351
- **Quote:** "body — what changed, why this matters, references to upstream/downstream" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:515`)
- **Quote:** "New repo side: `chore(repo): initial population from arxiv-sanity-mcp gsd-2-uplift initiative`" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:330`)
- **Quote:** "final commit messages reference EXTRACTION-LOG.md." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:351`)
- **Lens-question:** 5 (backward-traceable responsibility)
- **Type:** commit-map negative-space
- **Classification:** **Class B**
- **Justification:** The commit map is directionally good: atomic per phase, audit folders travel with findings, DECISION-SPACE updates commit with decisions, and commit bodies reference upstream/downstream. But extraction creates two git histories. The plan does not require the arxiv-side extraction commit to record the new-repo initial commit hash, nor require the new-repo initial commit to record the source commit hash/path map. `EXTRACTION-LOG.md` is the natural home, but the commit rules do not make cross-repo identity mandatory.
- **Why this matters:** Logan's stated requirement is backward responsibility tracing. Cross-repo extraction is exactly where traceability often fails: after artifacts move, a future reader needs source commit, target commit, old path, new path, and disposition reason.
- **Why not Class C:** this strengthens the commit protocol but does not alter phase ordering or extraction eligibility.
- **What dissolves:** require `EXTRACTION-LOG.md` to include source repo commit, target repo initial commit, path-by-path move/copy/stay/reference disposition, and both commits' hashes after creation. Require both commit bodies to name the paired commit hash once available, or a follow-up commit that records it.

### Finding 9 — Stale status / artifact-map markers contradict the resolved §0.7 parameters

- **Artifact:** `/home/rookslog/.claude/plans/cheerful-forging-galaxy.md`
- **Location:** frontmatter-like header, §0.7, §3.1, §6.1; lines 3-5, 125-135, 457-459, 601
- **Quote:** "Plan status: DRAFT — awaiting Logan-disposition on §0.7 open-questions before finalization" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:4`)
- **Quote:** "§0.7 Logan-disposed plan parameters (resolved 2026-04-29)" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:125`)
- **Quote:** "Standing-context artifact | TBD per Logan §0.7 Q3 disposition" (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:458`)
- **Quote:** "§0.7 open questions Logan-disposed (plan finalized)." (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:601`)
- **Lens-question:** 6 (fresh-session onboarding), 5 (artifact-map traceability)
- **Type:** stale-status / artifact-map
- **Classification:** **Class A**
- **Justification:** The plan body says §0.7 is resolved and even gives the standing-context location option in §0.7 Q3, while the header still says draft awaiting those dispositions and the artifact map still says TBD. This can confuse a fresh executor about whether execution may start after Phase A disposition.
- **Why not Class B:** the resolved content is present in the same artifact; this is consistency cleanup, not substantive plan change.
- **What dissolves:** update the status line and Phase B artifact-map location to match §0.7 Q3, or explicitly state that the plan remains draft pending Phase A audit despite §0.7 being resolved.

# §2. Cross-Artifact Propagation Patterns

- **Pattern 1 — Good framing discipline, weaker artifact custody.** The plan is careful about deliberation custody: audits surface non-binding signals, Logan disposes, incubation remains Logan-led. But artifact custody is weaker where the plan leaves the repo (`/home/rookslog/.claude/plans/...`) and where extraction crosses repos. Findings 1, 2, and 8 are the same class of traceability risk at different layers.
- **Pattern 2 — The trajectory preserves the big framing but occasionally over-compresses the operational test.** §0.2 and §0.3 carry the horizon stack well. Phase H's "without reference to arxiv-sanity-mcp" phrasing over-compresses "internal coherence" into "independence," which conflicts with the diagnostic-loop relationship.
- **Pattern 3 — Reasoning-level calibration is substantively good but locally inconsistent.** §2.4 is one of the strongest parts of the plan: it discriminates xhigh vs high by artifact load. The Phase G line that says xhigh appears to be a local drift from that principle, not a failed principle.
- **Pattern 4 — Path shorthand has become unsafe for fresh-session execution.** Many repo docs use `LONG-ARC.md` as shorthand, but the plan's §0.4 uses an absolute path. Shorthand is tolerable in local prose; it is not tolerable in a mandatory pre-reading list with "Do not skip."
- **Pattern 5 — Failure-mode taxonomy needs a control matrix.** The taxonomy is unusually explicit and useful, but the operations are distributed across §0.5, §0.6, §2, §5, and §6. A compact matrix would turn it from a doctrine list into an execution control surface.

# §3. Notable Absences / Inverse Signals

- **The plan does not collapse incubation into execution.** It explicitly says the plan does not pre-decide incubation dispositions, first-second-wave target shape, R-mix narrowing direction, context anchoring, or dedicated-repo internal structure (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:35-40`). This is a strong inverse signal against closure pressure.
- **Phase A xhigh is justified, not ceremonial.** The plan says Phase A has highest trajectory framing-load, spans all major plan sections, and requires deep negative-space reasoning (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:421-424`). That matches the audit lens and is not overkill.
- **Phase G high is justified in §2.4.** Despite the local xhigh conflict in §1.7, the table's rationale for high is correct: orphan-reference, missed-migration, and cross-reference-integrity checks are mechanical-coherence work (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:431-432`).
- **The plan preserves Logan disposition at load-bearing boundaries.** §0.7 sets hybrid autonomy with pauses at phase boundaries (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:127-129`), and Phase C records Logan as the disposer of per-axis incubation decisions (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:199-203`).
- **The predecessor audit arc is properly absorbed.** The standing context records that the premise-bleed audit addendum is active at point-of-use for §5 axes (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/gsd-2-uplift/exploration/SYNTHESIS-COMPARISON.md:426-437`), and the plan carries that reading-frame into Phase C inputs (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:190-212`).
- **The extraction-readiness gate asks a real readiness question.** Phase F requires stable disposition, first-target evidence, internal coherence, extraction triggers, and no outstanding load-bearing blockers (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:265-270`). That prevents "create repo because repo is the plan endpoint" from becoming automatic.
- **The plan does not treat all audits as paired by default.** The M1 strict-undersell note correctly warns against applying the heaviest discipline everywhere (`/home/rookslog/.claude/plans/cheerful-forging-galaxy.md:435`). This is a mature cost/rigor calibration.

# §4. Confidence + Limits + Self-Flagged Concerns

- **Confidence on classification:** medium-high overall.
- **Class C confidence:** medium-high on Finding 1; high on the contradiction in Finding 2, medium-high on Class C rather than Class B because Logan could dispose copy-vs-move in an addendum without revising the whole trajectory.
- **Class B confidence:** medium-high on Findings 3, 5, 6, 8; medium on Findings 4 and 7 because they depend on how much burden an executor places on nearby corrective text.
- **Class A confidence:** high.
- **Source-reading limit:** I did not inspect runtime memory files named in §7. That is intentional under this dispatch boundary. If Logan intended those memory files to be part of Phase A's evidence base, Finding 6 should be recalibrated after reading them; my present finding is about the plan's self-containedness, not the memory contents.
- **Cross-vendor framing-leakage caveat:** as codex, I may be less sensitive to in-house Claude+Logan register and more sensitive to explicit artifact/commit contradictions. I may under-detect comfort-language or subtle same-vendor framing inheritance that a same-vendor adversarial audit would catch.
- **No alternative plan drafted:** I did not propose a replacement trajectory. Findings name what dissolves the issue, but do not rewrite the plan.
- **Forbidden-reading compliance:** I did not read the conversation transcript, `/tmp/phase-a-plan-audit-dispatch.md`, or any `.logs/` folder.
- **Line-citation caveat:** for the missing root `LONG-ARC.md`, the absence is an artifact-observation from the checkout; the positive citation is to the existing `.planning/LONG-ARC.md` file.
- **Classification caveat:** I used Class C only where execution would likely need to change the artifact custody or extraction endpoint before proceeding. I held process-quality gaps at Class B when the eight-phase trajectory could remain intact.
- **Audit-shape caveat:** this is a plan-self-audit, not a replacement plan. Some "what dissolves" notes name the minimum control that would make the existing plan executable; they are not intended as final wording.

# §5. Non-Binding Disposition Signal

- **Why Logan might choose commit-as-is:** if Logan reads the two Class C findings as implementation details that the executor can handle during Phase A/B without changing the plan authority, the overall trajectory is coherent. The plan preserves incubation discipline, has a strong Phase F extraction-readiness gate, and already contains enough checks to avoid the prior premise-bleed failure mode. Commit-as-is is most defensible if Logan separately instructs the executor how to preserve the external plan file and how to resolve `DECISION-SPACE.md` custody at Phase G.
- **Why Logan might choose commit-with-addendum:** the two Class C findings are tractable as a plan addendum. An addendum can declare the committed plan-copy/hash authority, correct the `LONG-ARC.md` path, align Phase G audit level to high, add a failure-mode control matrix, and replace the Phase G move/stay list with an artifact-by-artifact disposition table. This preserves the eight-phase trajectory while fixing the load-bearing traceability defects before execution.
- **Why Logan might choose revise-before-execute:** if Logan wants the plan file itself to be the execution authority rather than "plan plus addendum," revise before execution. This is especially warranted if the extraction move/stay map is read as a trajectory-shaping decision rather than a local correction, because `DECISION-SPACE.md` custody affects the future dedicated repo's identity and arxiv-sanity-mcp's retained genesis trail.

Logan disposes per AUDIT-SPEC.md §8. This audit does not pick the disposition.
