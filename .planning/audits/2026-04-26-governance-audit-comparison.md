---
type: audit-comparison
status: complete
date: 2026-04-26
target: governance-doc set (ADRs 0001-0004 + AGENTS + CLAUDE + REQUIREMENTS-outside-v0.2 + ROADMAP-outside-12-17 + STATE + foundation-audit + ECOSYSTEM-COMMENTARY)
inputs:
  - 2026-04-26-governance-audit-cross-vendor.md (GPT-5.5 high via codex CLI)
  - 2026-04-26-governance-audit-opus-adversarial-xhigh.md (Claude Opus 4.7 xhigh via adversarial-auditor-xhigh subagent)
methodology_test: |
  This is the first paired audit dispatch under METHODOLOGY discipline A's
  independent-dispatch sub-discipline (M1, Hypothesis status, codified
  2026-04-26 from the v0.2 audit cycle's documented contamination effects).
  Both prompts included explicit forbidden-reading lists naming all
  v0.2-plan-audit artifacts and the parallel governance-audit artifact.
  This comparison serves as the second test of M1: if the two audits
  converge on substance while differing in framing/atomicity (which is
  what paired review is supposed to produce), M1's Hypothesis status
  is reinforced. If they substantially overlap or substantially diverge
  in unprincipled ways, M1's status is weakened.
purpose: |
  Map findings between cross-vendor and same-vendor xhigh audits to
  identify convergent risks (treat as one issue) and divergences (need
  adjudication). Feeds the synthesis step which produces actionable
  dispositions.
---

# Governance-Doc Audit Comparison — 2026-04-26

## 0. Topline

Both audits independently identify the same dominant pattern: **the four foundational ADRs (0001-0004) are calibrated and restrained; derivative artifacts (LONG-ARC, VISION, ADR-0005, milestones, AGENTS.md's own example) inflate the ADRs' rhetorical pitch when citing them**. Cross-vendor (CV) frames this in terms of register drift and "binding posture" attribution; same-vendor xhigh (SV) frames it in terms of calibration discipline (METHODOLOGY discipline D applied to the doctrine layer) and produces a more pointed instance: AGENTS.md's example of how to cite an ADR misquotes ADR-0001 in the very example teaching the discipline.

Beyond this central convergence, both audits find: STATE.md / CLAUDE.md staleness and counts drift; foundation-audit findings not fully propagated into prescriptive docs; AGENTS.md / CLAUDE.md overlap without canonical authority rule; ECOSYSTEM-COMMENTARY needs status annotations; ADR-0005's reading of ADR-0001 strains the original.

One substantive **divergence**: v2-deferred requirements name specific technologies (SPECTER2, pgvector, Semantic Scholar). CV reads this as coherent with v0.2's deferral framing; SV reads it as the LONG-ARC anti-pattern "embedding-model choice as load-bearing decision" recurring at the requirements layer. SV's read is more rigorous on this; the synthesis should adopt it.

## 1. Convergence matrix

Each row is a substantive issue identified by at least one audit, mapped to where each audit names it. Rows are ordered by signal strength (multi-audit convergence first; single-audit findings second).

| # | Issue | Cross-vendor finding(s) | Same-vendor xhigh finding(s) | Convergence |
|---:|---|---|---|---|
| 1 | ADR-0001 (and 0002-0004) use hedged modal verbs ("can," "will"); derivative docs cite as "binding"/"must" | D1.1, D1.3, D7.2, D8.1 | A1, A3, D1, E3 + "What works well" | **Strong** — both audits converge; the central finding |
| 2 | CLAUDE.md is stale (claims "Phase 6 next"; says "10 tools" while shipped is 13) | D2.1, D3.1, D7.3 (instr-as-aspiration partial) | D3 | **Strong** — both audits cite same drift |
| 3 | STATE.md is internally inconsistent (23 vs 31 plans; "Pending Todos: None" with pending items adjacent; date mismatch frontmatter vs body) | D4.1, D4.2, D4.3 | E2 | **Strong** — CV breaks this into 3 findings; SV consolidates into 1 with all the same instances |
| 4 | Foundation-audit findings filed but not propagated into prescriptive layer (FINDINGS.md lacks resolution annotations; AGENTS.md not updated despite documented violations of its prescriptions) | D5.2, D5.3, D7.3 | A2, C3, D3 | **Strong** — both audits hit this from multiple angles |
| 5 | ECOSYSTEM-COMMENTARY makes recommendations dated 2026-03-11 without status annotations on what's been implemented | D6.1, D6.2 | E1 | **Strong** — both call for status annotations on its §3-§7 recommendations |
| 6 | AGENTS.md / CLAUDE.md / PROJECT.md overlap on architectural constraints; no canonical authority rule for which document is the source of truth | D2.3 | F1, F2, F3 | **Strong** — CV is concise on this; SV develops it (governance set is large; no read-order; two METHODOLOGY docs not in dialog; deliberation directory unindexed) |
| 7 | ADR-0005 reads ADR-0001 stronger than the original text licenses (capability claim "can coexist" → delivery claim "must ship two implementations") | D1.3, D8.1 | E3, A1 | **Strong** — same finding from both; SV is more pointed on the structural fix (ADR-0005 should own the upgrade rather than attribute to ADR-0001) |
| 8 | AGENTS.md "must"/"do not" prescriptions lack enforcement mechanism, exit conditions, or revision-on-violation cadence | D7.3 | A2, D1 | **Convergent** — CV calls it "instruction-as-aspiration"; SV develops it with the AGENTS.md own example misquoting ADR-0001 |
| 9 | Tool counts drift across surfaces (CHANGELOG/tests say 13; CLAUDE.md says 10; LONG-ARC says 403 tests vs current ~493) | D3.1 | (D3 mentions same staleness pattern but doesn't enumerate counts) | **Strong** on CV; SV partial — CV's quantitative grounding is sharper here |
| 10 | MCP-07 became internally inconsistent: REQUIREMENTS says "[chosen for now] 5-10 tool heuristic, not a firm requirement"; tests assert exactly 13 | D3.2 | (mentioned indirectly in C2 as similar pattern) | **CV-only sharp finding**; SV's framing in C2 (v2 tech-naming) is parallel but not identical |
| 11 | v2-deferred requirements name specific technologies (SPECTER2, pgvector, Semantic Scholar) — DIVERGENT | D3.4 (says coherent with v0.2 deferral) | C2 (says LONG-ARC anti-pattern recurrence at requirements layer) | **DIVERGENT** — see §3 below |
| 12 | Pending user-validation items (docs/10 Q1, Q4, Q16 closures) under-tracked | D5.3 | C3 (subset; AGENTS.md prescription not honored) | **Convergent** — both call for explicit live tracker |
| 13 | Per-phase ADR-against-plan audit not operationalized as a checkpoint (LONG-ARC names the discipline but no operational hook) | (D5.2 closeout-matrix is related but not the same) | D2 | **SV-only sharp finding** — operational hook proposal is concrete; CV's closeout-matrix is the audit-finding equivalent but doesn't propose the per-phase mechanism |
| 14 | CLAUDE.md "Stack trajectory: Not Stack D" is a silent default (no definition of Stack D in CLAUDE.md) | (not addressed) | C1 | **SV-only** — SV self-labels as "trivial but real" |
| 15 | AGENTS.md's example for "ADR citation must be specific" misquotes ADR-0001 ("must coexist" vs ADR's "can coexist") | (not caught) | D1 | **SV-only** — concrete instance of the convergence-1 pattern; SV is sharper |
| 16 | ADR-0001's Context section excludes the inherited-frame-rejection alternative (arxiv-sanity defaults the ADR was implicitly pushing back against) | (not addressed) | B2 | **SV-only** — SV self-labels Quality, Medium confidence |
| 17 | CV finds ADRs 0002-0004 bind more concretely than 0001; recommends "common misuses" sections | D1.2 | (not addressed; B1 says ADRs are appropriate to their genre) | **CV-only** |
| 18 | Status-marker discipline inconsistently used (REQUIREMENTS uses `[chosen for now]`; ROADMAP / CONTEXT files don't) | D2.2 | (not addressed; SV's "What works well" praises the REQUIREMENTS use) | **CV-only** |
| 19 | Phase 2 success criteria omit "seen" while WKFL-03 in REQUIREMENTS includes it | D3.3 | (not addressed) | **CV-only** |
| 20 | External ecosystem claims (arxiv-scan, Hugging Face, OpenAlex, MCP servers) not verified | D6.3 | (not addressed; SV explicitly says external claims are out of scope) | **CV-only** — SV explicitly bounded scope |
| 21 | VISION / LONG-ARC extend ADR-0003 provenance commitment coherently (positive finding) | D8.2 | (not addressed; SV's "What works well" partially overlaps) | **CV-only positive finding** |
| 22 | ROADMAP cites forbidden audit artifact (Property audit) as evidence for Option B | D8.3 | (not addressed) | **CV-only** — meta-observation about audit-citation structure |
| 23 | Two `METHODOLOGY.md` files (foundation-audit + spikes) are not in explicit dialog | (not addressed) | F2 | **SV-only** — SV self-labels Medium confidence |
| 24 | `.planning/deliberations/` directory of 14 files has no INDEX.md or status map | (not addressed) | F3 | **SV-only** |
| 25 | ADRs 0001-0004 do not enumerate alternatives — but the genre is appropriate to that | (not addressed) | B1 (self-labeled taste) | **SV-only, self-discounted** |

**Total:** 25 substantive issues. 12 strong-convergent (rows 1-9, 12), 9 single-audit findings of differing weight, 1 substantive divergence, 3 single-audit findings the originating audit self-discounts.

## 2. Convergent risks (issues that multiple findings point at; treat as one)

These mirror the SV audit's own "Convergent risks" section but extended with CV's contributions:

### CR1. Calibration drift between source and citation (rows 1, 7, 8, 15)

The four foundational ADRs use hedged modal verbs. Derivative artifacts re-cite them with stronger modals. The pattern recurs across LONG-ARC.md, VISION.md, ADR-0005, milestone docs, AGENTS.md (in its own ADR-citation example, which misquotes ADR-0001). Both audits converge; SV's D1 is the sharpest concrete instance (misquote in the AGENTS.md example) and SV's E3 is the sharpest structural finding (ADR-0005 should own the stronger commitment rather than attribute to ADR-0001).

A single doctrine-pass that re-verifies ADR citations against ADR text would address most of CR1.

### CR2. Audit findings don't propagate into the audited prescriptive layer (rows 2, 4, 12)

Foundation-audit identified violations of AGENTS.md prescriptions; AGENTS.md was not updated. ECOSYSTEM-COMMENTARY identified CLAUDE.md staleness; specific staleness was fixed but new staleness accreted. STATE.md inconsistencies (row 3) are likely a similar pattern at smaller scale. Pending user-validation items (row 12) live in `docs/10` without a live tracker.

A "post-audit follow-through" convention would address most of CR2: each prescriptive doc gets a "Known difficulty patterns" or resolution-annotation section linking documented violations to revised guidance.

### CR3. No canonical read-order or document map for the governance set (rows 6, 18, 23, 24)

The governance set has grown organically. Two `METHODOLOGY.md` files not in dialog. 14-file deliberation directory unindexed. PROJECT.md / CLAUDE.md / AGENTS.md overlap on architectural constraints. Status-marker discipline inconsistently used. A new contributor or returning agent has no canonical entry path.

A single map (5-7 lines in CLAUDE.md or a separate READING-ORDER.md) would address several findings at once.

### CR4. STATE.md is unreliable as the live-state record (rows 3, 9)

CLAUDE.md:40-41 says STATE.md is the live-state record. STATE.md has internally inconsistent metrics (23 vs 31 plans), mixed historical-vs-current framing, body-frontmatter date mismatch, and stale "Pending Todos: None" framing. Tool counts drift across STATE / CLAUDE / LONG-ARC / actual code.

CV breaks STATE.md issues into three findings; SV consolidates into one (E2). Both call for structural attention: split historical metrics from current activity into separately-legible sections.

### CR5. ADR-0005 strains ADR-0001's reading; the chain should be named accurately (rows 1, 7)

ADR-0001 says strategies "can coexist" (capability claim about architecture). ADR-0005 reads this as requiring v0.2 to ship at least two lenses (delivery claim). SV E3 proposes the cleanest fix: ADR-0005's Context section reframes one sentence to own the stronger commitment as ADR-0005's contribution rather than as ADR-0001's requirement. CV D8.1 makes the same point in less developed form ("describe v0.2 as 'chosen to operationalize ADR-0001,' not 'required by ADR-0001' unless citing ADR-0005").

## 3. Substantive divergence: v2-deferred technology naming (row 11)

This is the only substantive divergence between the two audits.

**CV finding D3.4:** v2 semantic search and selective embeddings remain deferred (REQUIREMENTS:141-147); v0.2 keeps pgvector and Semantic Scholar out of scope; advanced citation sources remain complementary because v0.2 uses OpenAlex first but preserves fallback. **Conclusion: coherent with v0.2.** Recommended action: annotate ADVN-02 as "broader citation coverage after OpenAlex-first v0.2," not a duplicate.

**SV finding C2:** v2-deferred requirements (SEMA-01: SPECTER2 embeddings; SEMA-02: pgvector; ADVN-01: Semantic Scholar adapter) name specific technologies. The deferred-status tag is honest about timing, but the *which-technology* decision is implicit: "by writing 'SPECTER2' rather than 'embedding model TBD,' the requirement pre-commits the v2 work to that choice." **Conclusion: LONG-ARC anti-pattern "embedding-model choice as load-bearing decision" recurring at the requirements layer.** Recommended action: reframe SEMA-01 through SEMA-04 and ADVN-01 as capability requirements with named technologies as illustrative-only ("e.g., SPECTER2 or equivalent embedding model selected via lens-design analysis").

**Adjudication:** SV's read is more rigorous. CV is reading the deferred-status tag as honest framing of timing (true); SV is reading the technology naming as silent pre-commitment of the choice (also true, and a documented LONG-ARC anti-pattern). They are right about different things. CV's "coherent" framing doesn't address whether the technology pre-commitment is OK; SV's framing does, and aligns with the team's own anti-pattern doctrine.

**Synthesis disposition:** adopt SV's reframe.

## 4. Methodology delta — paired-audit performance under M1 (forbidden-reading discipline applied)

This is the second test of M1 (the first being the v0.2 cycle's contaminated-vs-independent xhigh comparison).

**Independence verified by structure.** The two audits used different dimension structures (CV: D1-D8; SV: A-F). They produced different finding granularities (CV: 24 atomic findings, ~96 words/finding average; SV: 17 multi-paragraph findings, ~447 words/finding average). They cite different file:line targets in many cases. They use different finding tiers (CV: confidence high/medium/low + recommended action; SV: severity tier + confidence + what would dissolve + suggested improvement direction). This is the kind of structural divergence that suggests the readings are independent rather than anchored on a shared template.

**Convergence on substance, divergence on framing.** 12 of 25 issues are strongly convergent; the convergent issues largely concern surface-verifiable facts (counts, drift, missing annotations) and shared-doctrine concerns (calibration discipline, anti-pattern recurrence). Divergence concentrates in: depth-of-development per finding (SV deeper), atomic-finding-yield per dimension (CV more atomic), and one substantive read (row 11 v2 tech naming). This matches the v0.2 cycle's pattern: cross-vendor catches surface, same-vendor catches register/pattern, both converge on the strongest doctrinal issues.

**Single-audit findings.** CV-only findings concentrate in atomic-fact territory (Phase 2 success criteria misalignment, ADR 0002-0004 binding-concreteness, MCP-07 inconsistency, status-marker inconsistency, external-ecosystem-currency, ROADMAP audit-citation structure). SV-only findings concentrate in pattern/structural territory (governance scope-creep, methodology-doc dialog gap, deliberation index, ADR-0001 inheritance-rejection framing, "Stack D" silent default, AGENTS.md own-example misquote, per-phase ADR audit operationalization).

This is what M1 was supposed to produce: independently dispatched paired reviewers find substance overlap on the strongest issues while differing on framing depth and atomic-finding yield. **M1's Hypothesis status is reinforced** by this comparison. (Not "confirmed" — single comparison cycle is still single-comparison evidence; the discipline should remain Hypothesis until further cycles either reinforce or weaken the pattern.)

**Cost of independence.** Both audits complete in ~7 minutes wallclock from dispatch to file-on-disk; comparable to the v0.2 same-vendor xhigh duration. No measurable delay cost from the forbidden-reading discipline. The forbidden-reading list adds ~10-20 lines to the prompt; trivially cheap.

**One implementation lesson noted for future codex dispatches:** the codex `--output-last-message` flag overwrites the file with the agent's final chat message, clobbering anything the agent wrote there itself via `apply_patch`. This was caught in the Wave 2 dispatch (cross-vendor audit content recovered from session JSONL). Future dispatch convention: do not co-locate the agent's write target with `-o` capture path, or skip `-o` entirely and recover audit content from the codex output stream.

## 5. Joint blind spots (issues neither audit addressed within scope)

Both audits explicitly acknowledged scope bounds in their "What I am not telling you" / closing sections. Joint blind spots that fall outside both audits' scope:

1. **Source-code behavior.** Both audits did spot-checks (CV verified MCP tool counts via test files; SV verified `signal_type` open at DB level via migration 005); neither audited code-vs-doctrine alignment systematically. Open question: does the implementation actually honor what the governance docs claim?

2. **`docs/05-08`, `docs/10`, `docs/templates`.** Neither audit treated the numbered design docs as audit targets. They are referenced as context but not audited. Particularly notable: `docs/templates/` is the project's ADR template authority; if it has issues (e.g., doesn't require Alternatives-Considered for posture ADRs), that's an upstream gap neither audit caught.

3. **`PROJECT.md`.** Mentioned by both audits as "primary active reference" or context but not audited as a target. PROJECT.md may overlap with VISION.md / LONG-ARC.md in ways neither audit characterized.

4. **`.planning/spikes/` artifacts beyond METHODOLOGY.md.** The spike chain (001-008) is referenced but not audited. Spike artifacts may carry their own register / scope-creep issues.

5. **`.planning/quick/` tasks.** Referenced (via Quick Task 1's role in resolving foundation-audit findings) but not audited as a class. The quick-task substrate is a governance-adjacent surface neither audit characterized.

6. **`docs/06-mcp-surface-options.md` and `docs/07-data-sources-content-rights.md`.** CV read both for verification of specific claims; neither audit treated them as audit targets in their own right.

7. **The user's auto-memory / global CLAUDE.md.** SV explicitly noted the dual-role limitation of project-CLAUDE.md being loaded as runtime instruction; neither audit looked at the user's `~/.claude/CLAUDE.md` or `/home/rookslog/CLAUDE.md` (which are out of scope; mentioned for completeness).

8. **`.planning/measurement/`.** Untracked directory present in git status but not audited; status unknown.

These blind spots are not findings — they are bounded-scope acknowledgments. The synthesis may flag some of them as candidates for a future audit cycle if they become load-bearing.

## 6. What this comparison does not commit

- **Does not synthesize the findings into actionable dispositions.** That is the synthesis step (next deliverable: `2026-04-26-governance-audit-synthesis.md`).
- **Does not adjudicate each single-audit finding on its merits.** Adjudication happens in synthesis. The comparison just maps findings to each other.
- **Does not revise the M1 status from Hypothesis.** Single-comparison evidence reinforces but does not confirm. The discipline should remain `Hypothesis` until further paired-audit cycles either reinforce or weaken the pattern.
- **Does not weight the audits unequally.** This comparison treats both as primary inputs (different weighting from the v0.2 cycle's comparison, which weighted the contaminated xhigh lower; here, both audits were independently dispatched per M1, so both are primary).
- **Does not address the joint blind spots as audit findings.** They are scope-acknowledgments for synthesis to either accept or escalate to a follow-up audit.

## 7. Inputs to synthesis

The synthesis should:
- Treat CR1-CR5 as the load-bearing convergent findings; they are commit-ready in the sense that any one of them maps to concrete edits with broad multi-audit support.
- Adopt SV's reframe for row 11 (v2 technology naming) — the only substantive divergence.
- Treat single-audit findings (rows 13-25) per their original audit's confidence and severity tiers; some will be adopt-now, some will be defer, some will be drop.
- **Defer dispositions on AGENTS.md and CLAUDE.md substantive content edits pending exemplar review.** Logan has noted exemplar AGENTS.md / CLAUDE.md from other projects to harvest principles from; substantive AGENTS/CLAUDE edits should wait for that harvest. Dispositions in this synthesis on those documents should be flagged "deferred pending exemplar review."
- **Note the mid-horizon framing change.** Logan clarified 2026-04-26 that the gsd-2-related mid-horizon work is not just migration but **uplift**: integrating LONG-ARC.md / VISION.md into gsd-2 workflows as a project-agnostic capability, possibly producing an automated patcher repo that uplifts arbitrary projects with long-horizon planning capacity. This is a substantial standalone initiative and the synthesis should not pre-empt it (e.g., proposing changes to current GSD workflows that would conflict with the uplift design).
