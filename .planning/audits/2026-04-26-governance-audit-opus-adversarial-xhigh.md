---
type: same-vendor-critical-governance-audit
status: complete
date: 2026-04-26
target: governance-doc set (ADRs 0001-0004 + AGENTS + CLAUDE + REQUIREMENTS-outside-v0.2 + ROADMAP-outside-12-17 + STATE + foundation-audit + ECOSYSTEM-COMMENTARY)
auditor: Claude Opus 4.7 (fresh session, critical reviewer per adversarial-auditor-xhigh)
effort: xhigh
independence: This audit was dispatched without reference to any audit of the v0.2 plan layer or the parallel cross-vendor governance audit being dispatched alongside it. The dispatching prompt forbade reading prior v0.2-plan-audit artifacts and the parallel cross-vendor governance audit per METHODOLOGY discipline A's independent-dispatch sub-discipline.
---

## Summary

The governance-doc layer is in unusual shape relative to the v0.1 ADRs it grew out of: those ADRs (0001-0004) are notably restrained — short, modest, hedged — and the team's later doctrine (LONG-ARC, VISION, STATE, ROADMAP) has accreted around them at much higher rhetorical pitch. The strongest survived findings are (1) the ADRs themselves are *under*-committed relative to how downstream artifacts treat them ("ADR-0001 binds" appears as a derivative-layer claim; the ADR text itself never uses "binding" or even "must"); (2) AGENTS.md and CLAUDE.md prescribe an extensive epistemic discipline that the foundation-audit explicitly documents the project violating, and that violation has not driven any update to the prescriptive docs themselves; (3) STATE.md carries internally inconsistent metrics blocks and stale `Pending Todos: None` framing that make it unreliable as the live-state record CLAUDE.md says it is; (4) the foundation-audit findings include implementation issues marked MEDIUM-HIGH that have not been folded back into REQUIREMENTS or ADRs even after they were resolved in code, leaving the requirements layer disconnected from what the audit actually surfaced. The most consequential strength: the ADRs are honestly conservative — they say less than the team often attributes to them, which is the right epistemic posture for foundation documents. The drift problem is in the surrounding doctrine, not in the ADRs themselves.

## Findings by dimension

### Dimension A — Closure pressure recurrence at the doctrine layer

#### A1. The ADRs themselves are calibrated; the doctrine that cites them is not

**What.** ADR-0001 (`docs/adrs/ADR-0001-exploration-first.md:18-26`) says "We will structure the early system so that: multiple retrieval and ranking strategies *can* coexist" — modal "can," scope-qualified to "the early system." The Decision section uses one "will," and the Notes section explicitly de-escalates: "This ADR is about process and architecture posture, not about avoiding implementation." There is no "binding," no "load-bearing," no "must," no all-caps emphasis. The same pattern holds for ADRs 0002-0004 — each is one page, with hedged modal verbs and a Notes section that softens.

Compare LONG-ARC.md:46 ("Tournament narrowing... violates ADR-0001's coexistence intent"), LONG-ARC.md:25 ("v0.2 has been architecturally committed via ADR-0005"), `milestones/v0.2-MILESTONE.md:103` ("ADR-0001 — exploration-first architecture (binding for v0.2 implementation)"), ADR-0005 line 9 ("multiple retrieval and ranking strategies can coexist as a binding posture"). The word "binding" never appears in ADR-0001. It is an attribution.

**Why it matters.** Ground 4 (methodology discipline D, calibrated language as default register, `METHODOLOGY.md:142-150`). The team's own discipline says "Rhetorical labels ('load-bearing,' 'critical,' all-caps emphasis) require argument under them, not in lieu of argument." The label "binding" is doing argument-shaping work in derivative artifacts (it is what makes the v0.2 multi-lens commitment feel forced rather than chosen) but the underlying ADR text doesn't carry that weight. This is also ground 3 (accepted ADR honored at implementation layer): the derivative attribution is *stronger* than the source, which inverts the usual drift direction but is just as much a calibration failure.

**Severity.** Quality, edging toward blocking on one axis: if v0.2 work is partially justified by "ADR-0001 binds" framing that the ADR itself doesn't support, then disagreement about v0.2 scope cannot be cleanly adjudicated by reading the ADR. The team would have to either rewrite ADR-0001 to actually bind or stop describing it as binding.

**Confidence.** High. Verifiable by direct text comparison.

**What would dissolve.** Either: (a) an ADR-0001 amendment that explicitly upgrades "can coexist" to "must coexist" with exit conditions and consequences, making the binding language honest; or (b) a doctrine-layer pass that replaces "binding" with "the principle we have chosen to honor in implementation" — accurate, lower-pitch, doesn't require ADR amendment.

**Suggested improvement direction.** The cheaper move is (b) — go through LONG-ARC, VISION, ADR-0005, milestone docs and replace "binding" with calibrated phrasing that matches what ADR-0001 actually says ("the architectural posture ADR-0001 commits us to," "the coexistence principle ADR-0001 sets out"). Reserve "binds" for an explicit ADR amendment if the team decides the stronger commitment is what they want.

#### A2. AGENTS.md uses prescriptive "must"/"do not" lists without enforcement mechanism or exit condition

**What.** AGENTS.md:17-25 ("Do not do these things") is a seven-item negative list. AGENTS.md:115-121 ("Separate traceable claims...") includes "Never present a derived or interpretive claim as if it were source-traceable" and "Avoid bare `grounded` as an epistemic label in new planning artifacts." AGENTS.md:124-126 ("Do not close Open Questions without authority"). None of these have an enforcement mechanism (who checks?), an exit condition (when does this discipline relax or get amended?), or a record of violations.

The foundation-audit (`FINDINGS.md:262-273`) documents that several of these were violated in practice (Open Questions Q1, Q4, Q16 were silently closed in CONTEXT files; ADR scope was stretched repeatedly). The violations are recorded; the prescriptive document is not amended in response.

**Why it matters.** Ground 4 (methodology discipline F, pattern-watch with self-application, `METHODOLOGY.md:160-166`). The team has codified that disciplines should self-apply. AGENTS.md is the team's prescriptive document for how AI agents should work; if its rules are violated and the violations don't propagate back into the document (e.g., as "this discipline was hard to apply because X; here's the revised guidance"), the document is closure-pressure shaped: it states the rule and assumes the rule does the work.

**Severity.** Quality. The discipline content is good; the document's relationship to its own observed violation rate is what's missing.

**Confidence.** Medium-high. The foundation-audit explicitly catalogs violations; the AGENTS.md text doesn't reflect those violations in its current form. I cannot tell from outside whether there's an informal practice of revising AGENTS.md after violations and just hasn't happened yet, or whether the document is treated as static.

**What would dissolve.** Either evidence that AGENTS.md is on a revision cadence and version-2 incorporates the foundation-audit's findings, or an explicit "known violation patterns" section that links the prescriptions to where they have been hard to honor.

**Suggested improvement direction.** Append a "Known difficulty patterns" section that lists the specific violation patterns the foundation-audit documented (Open Questions silently closed, ADR scope stretched in CONTEXT files, "grounded" used as overloaded label). One-paragraph each, with the file:line of the documented violation. This turns the prescriptions from rules-asserted into rules-with-empirical-grounding.

#### A3. CLAUDE.md uses the strongest prescriptive register of the governance set and sits at "currently loaded into agent context"

**What.** CLAUDE.md:20-24 uses bolded "Do not prematurely commit," "Do not assume tags are the canonical taste representation, dense retrieval is the winner, or 'paper chat' is the product." Line 24: "Stack trajectory: Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). Not Stack D." That "Not Stack D" is a flat negative without context for what Stack D is or why it's foreclosed.

The dispatching prompt notes that CLAUDE.md is automatically loaded into agent context and explicitly asked me to flag if anything is "doing instruction-of-the-auditor work that biases the audit." CLAUDE.md:13 attributes to ADR-0001 the claim "Multiple retrieval/ranking strategies must coexist" — using "must" where ADR-0001 uses "can." This is the same A1 pattern, but now embedded in the document an agent reads as runtime instruction.

**Why it matters.** Ground 1 (stated end goal: governance-doc set should be a faithful interpretive substrate for agents working on the project) and ground 4 (calibrated language). When a runtime-loaded document mis-attributes "must" to an ADR that uses "can," every agent session is being conditioned to treat the stronger reading as canonical.

**Severity.** Quality. The bias is real but small; the agent has access to the actual ADR text and can verify.

**Confidence.** High on the textual mismatch; medium on whether the runtime-context exposure actually shifts agent behavior in any consequential way. I can observe the issue in myself: I noticed the mismatch only when I read both documents back-to-back. That's a weak signal that the prescriptive register is doing some shaping.

**What would dissolve.** Bring CLAUDE.md:13 into faithful paraphrase ("multiple retrieval/ranking strategies *can* coexist" or "the ADR commits us to designing so they can coexist"), and add one-sentence rationale for the "Not Stack D" line so agents know what they're avoiding and why.

**Suggested improvement direction.** A small CLAUDE.md pass that aligns ADR paraphrases with ADR text, adds a one-sentence "what is Stack D" gloss (or links to where it's defined), and softens "Do not assume" to "Do not assume without evidence" — preserves the discipline, drops the inflation.

### Dimension B — Reverse-engineered necessity in ADRs

#### B1. ADRs 0001-0004 do not enumerate alternatives — but the genre is appropriate to that

**What.** None of ADRs 0001-0004 has an "Alternatives Considered" section. Each has Context → Decision → Consequences → Notes. This contrasts with the project's own ADR template (per AGENTS.md:51 referencing `docs/templates/`, and per ADR-0005 which does discuss alternatives in its Context).

For ADR-0001, the Context (lines 6-16) lists five areas of uncertainty and concludes "A premature hard commitment would likely make later experiments expensive or biased." This reads as setup for "therefore exploration-first," but no alternative posture is named. For ADR-0002, the Context (lines 7-11) names cost-and-complexity concerns, then jumps to lazy enrichment. For ADR-0003, the Context names varying rights regimes, then jumps to first-class provenance. ADR-0004 names "naïve design would expose web concepts as a search API" then jumps to workflow substrate.

**Why it matters.** Ground 5 (delivery risk) only weakly. These four ADRs are early-architectural-posture documents written before the project had any code; the alternatives in each case are essentially "the opposite of what we chose" (commit early; eager enrichment; ignore provenance; mega-search API). Naming those would be a formality. The methodology document (`METHODOLOGY.md:18-19`) names "Alternative Evaluation" as a justification axis, but it also notes (line 1-page) that this is "for evaluating whether project decisions rest on adequate epistemic grounds" — meant for adversarial review, not necessarily for ADR composition.

**Severity.** Taste, mostly. The ADRs are short and honest about being posture documents (each Notes section says some version of "this is about posture, not implementation").

**Confidence.** High on the textual observation; low on whether this is an actionable finding.

**What would dissolve.** Either an explicit project decision that posture-ADRs don't need alternative-enumeration (worth recording somewhere — maybe in `docs/templates/`), or a small backfill that adds "Alternatives considered" sections to ADRs 0001-0004 retroactively.

**Suggested improvement direction.** I'd lean toward leaving ADRs 0001-0004 alone. They are short, honest, hedged, and their Notes sections already de-escalate the prescriptive register. If anything, the lesson is to make sure newer ADRs (like ADR-0005) honor the same restraint — and ADR-0005 is much longer (67 lines vs ADR-0001's 41) and uses "binding" once. The drift is downstream, not at the foundational ADR layer.

#### B2. ADR-0001's "Context" reads as honest description but excludes the alternative the team had been pursuing

**What.** ADR-0001's Context (lines 6-16) lists five major uncertainties at project start. What it doesn't say: the project's *prior frame* — the arxiv-sanity-as-reference frame that the team was inheriting — already had a settled position on each (TF-IDF for retrieval, library/tags for interest, web UI for surface). The Context describes the uncertainties as if they were freshly perceived, when in fact the project began with a strong inherited frame that ADR-0001 was implicitly pushing back against.

This is a small thing: the ADR isn't dishonest, but its Context section presents the option space as "we face uncertainty" rather than "we've decided not to inherit the arxiv-sanity defaults wholesale." The latter framing would make the decision more explicitly a *positioning* decision and less a *response-to-uncertainty* decision.

**Why it matters.** Ground 2 (long-term vision). VISION.md:24-32 ("What we inherit from arxiv-sanity, what we diverge from") is the document that does the explicit positioning work. If ADR-0001 had named "we are choosing not to inherit arxiv-sanity's settled frame" in its Context, the divergence trajectory would be traceable to a foundation-layer decision rather than to a vision-layer claim that came years later.

**Severity.** Quality. The vision document does the work eventually; the foundational ADR could have done it earlier.

**Confidence.** Medium. I'm reading some narrative coherence into the foundation that the team may not have perceived at the time of writing.

**What would dissolve.** Evidence that the team understood ADR-0001 at write-time as primarily a divergence-from-inheritance decision and chose not to frame it that way for principled reasons. Or, alternatively, an ADR-0001 amendment now that adds a Notes line connecting it to the VISION.md positioning.

**Suggested improvement direction.** Add one sentence to ADR-0001's Notes: "This posture is also a deliberate non-inheritance of arxiv-sanity's settled choices on retrieval, interest model, and surface — see VISION.md for the long-arc positioning." Cheap, makes the trajectory visible.

### Dimension C — Anti-pattern recurrence at doctrine layer

#### C1. CLAUDE.md's "Stack trajectory: Not Stack D" is a silent default at the doctrine layer

**What.** CLAUDE.md:24 reads "Stack trajectory: Stack A (metadata + lexical + graph) moving toward Stack B (+ selective local semantic). Not Stack D." There is no reference to where Stacks A/B/C/D are defined in CLAUDE.md itself. Searching reveals these are presumably defined in `docs/05` or one of the architecture-hypotheses docs. An agent reading CLAUDE.md as runtime context sees a definite negation ("Not Stack D") without context, definition, or argument.

This is the LONG-ARC.md:48 anti-pattern ("Silent defaults") at the doctrine layer: a reference frame becomes the implicit foreclosure without explicit naming of what's being foreclosed.

**Why it matters.** Ground 3 (LONG-ARC anti-pattern explicitly named) and ground 4 (calibrated language). The team has named this exact pattern as something to avoid; CLAUDE.md instances it.

**Severity.** Quality. Easy to fix; not delivery-blocking.

**Confidence.** High on the text; medium-high on the framing as anti-pattern recurrence (it is genuinely a silent default in the LONG-ARC sense, but at low stakes).

**What would dissolve.** A glossary expansion in CLAUDE.md that names what Stack D is and why it's foreclosed, or a removal of the "Not Stack D" line if the foreclosure isn't load-bearing in current planning.

**Suggested improvement direction.** One sentence: "Stack D = (something) — foreclosed because (reason)." Or remove the line; the positive trajectory ("A → B") is the actionable content.

#### C2. v2-deferred requirements name specific technologies that pre-commit by naming

**What.** REQUIREMENTS.md:142-153 ("v2 Requirements" → "Semantic Search" and "Advanced Enrichment") lists deferred items including:
- SEMA-01: "System computes SPECTER2 embeddings selectively for user-touched/saved papers"
- SEMA-02: "Semantic search via pgvector for embedded paper cohorts"
- ADVN-01: "Semantic Scholar adapter for recommendations and SPECTER2 embeddings"

These name specific technologies (SPECTER2, pgvector, Semantic Scholar) as if they were the chosen solutions. The deferred-status tag is honest about timing, but the *which-technology* decision is implicit: by writing "SPECTER2" rather than "embedding model TBD," the requirement pre-commits the v2 work to that choice.

LONG-ARC.md:48 names "embedding-model choice as load-bearing decision" as an anti-pattern: "Treating 'which model wins' as the architectural commitment when most actual tool-quality leverage lives upstream." The v2 requirements as currently written pre-commit to SPECTER2 specifically.

**Why it matters.** Ground 3 (LONG-ARC anti-pattern). The team's own doctrine warns against this exact pattern. Ground 5 (delivery risk): when the team gets to v2 work and the question "should we use SPECTER2 or X?" comes up, the v2 requirements list answers it implicitly. That's exactly the silent-default mechanism LONG-ARC names.

**Severity.** Quality, with one caveat: this is precisely the failure mode that LONG-ARC.md says recurs ("we have already drifted into this once"). If the team is running its own discipline against itself, finding this pattern in the v2 requirements should prompt revision.

**Confidence.** High on the text. Medium on the framing — it's possible "SPECTER2" is being used as shorthand for "an embedding model in the SPECTER family" and the team understands it that way internally; if so, the document doesn't say so.

**What would dissolve.** Either an explicit note in the v2 section that the named technologies are placeholders pending lens-design work, or a pass that replaces the names with capability descriptions ("an embedding model selected per-lens-design," "a vector search index").

**Suggested improvement direction.** Reframe SEMA-01 through SEMA-04 and ADVN-01 as capability requirements with named technologies as illustrative-only ("e.g., SPECTER2 or equivalent embedding model selected via lens-design analysis"). Cost: small. Benefit: keeps v2 work open in the way LONG-ARC says to.

#### C3. Foundation-audit's "audit-as-product" risk: findings filed, not propagated into living docs

**What.** `FINDINGS.md:218-273` (the Synthesis section) lists 12 issues with severity tiers and remedies, plus 6 implementation issues (I1-I6) marked MEDIUM-HIGH to LOW. STATE.md and REQUIREMENTS.md show that several of these (I1, I3, I4, I6) were resolved via Quick Task 1 (`STATE.md:217-220`). However:

- The foundation-audit FINDINGS.md document itself has no "Resolution status" annotations on the listed issues. A reader of FINDINGS.md cannot tell from FINDINGS.md alone which issues are open vs closed.
- The remedies listed in the Synthesis section ("Process fix: ADR citations in CONTEXT files should quote the specific clause") have not been folded into AGENTS.md's prescriptive lists in any traceable way (AGENTS.md:129-132 *does* have a similar discipline, but I cannot verify whether that section was added in response to the audit or pre-existed it — there's no provenance trail).
- Findings about Open Question closures (Q1, Q4, Q16, finding I5) — no record in `docs/10-open-questions.md` (which I haven't read but is referenced) acknowledging that those closures happened and are being treated as provisional vs settled.

**Why it matters.** Ground 4 (methodology discipline F, self-application). The foundation-audit was the team's most ambitious epistemic-hygiene exercise. If its findings live only in FINDINGS.md and don't propagate into the documents they were findings *about*, the audit becomes audit-as-product — the deliverable was the audit document, not the changes to the audited substrate. Ground 5 (delivery risk): future contributors reading AGENTS.md or REQUIREMENTS.md will not know which prescriptions were stress-tested by the audit and which weren't.

**Severity.** Quality, edging toward blocking on the Open Questions point. If Q1/Q4/Q16 were closed without user authority and that's still not surfaced as provisional in the requirements that depend on those closures, the requirements layer is carrying invisible debt.

**Confidence.** Medium-high. Some propagation may have happened informally (Quick Task 1 closed I1/I3/I4/I6 in code, and a "Quick Tasks Completed" entry exists at `STATE.md:217-220`); what I can't see is propagation into the prescriptive governance docs themselves.

**What would dissolve.** A "Foundation-audit follow-through" section in the audit directory or in STATE.md that maps each FINDINGS.md issue to where it was addressed (or "not addressed; reason"). Plus: a one-paragraph annotation in REQUIREMENTS.md noting that several v0.1 requirements (INTR-04, INTR-05, MCP-05, MCP-07, CONT-05) were flagged in the foundation-audit as exploratory→firm category errors, so the `[chosen for now]` annotations now present in those requirements (lines 53-54, 82, 91, 93) trace to that audit.

**Suggested improvement direction.** A 30-minute pass: add resolution annotations to FINDINGS.md (RESOLVED/OPEN/SUPERSEDED for each numbered issue), with file:line references where the resolution lives. This turns the audit from a snapshot into a live document.

### Dimension D — Self-application gaps

#### D1. AGENTS.md's "ADR citations must be specific" discipline is not satisfied by the doctrine layer that cites ADRs

**What.** AGENTS.md:129-132 reads: "When citing an ADR to justify a decision, quote the specific clause or principle that applies. Do not cite an ADR number alone as blanket authority for decisions the ADR does not address. Example: 'ADR-0001 states "multiple retrieval/ranking strategies must coexist" — this means...' not just 'per ADR-0001.'"

Now compare:
- LONG-ARC.md:46: "Tournament narrowing... violates ADR-0001's coexistence intent" — no quote, "intent" inferred.
- LONG-ARC.md:25: "v0.2 has been architecturally committed via ADR-0005" — no quote.
- ADR-0005 line 9: "ADR-0001 commits the project to exploration-first architecture: 'multiple retrieval and ranking strategies can coexist' as a binding posture." This *does* quote — but adds "as a binding posture," which is not in the ADR.
- v0.2-MILESTONE.md:103: "ADR-0001 — exploration-first architecture (binding for v0.2 implementation)" — no quote.

Note also: AGENTS.md's *example* in line 131 quotes "multiple retrieval/ranking strategies *must* coexist" — the example itself misquotes ADR-0001, which uses "can." This is a small textual finding but a concentrated demonstration: the document that prescribes "quote the specific clause" misquotes its own example.

**Why it matters.** Ground 4 (methodology discipline F, self-application; and discipline A on the codified misquote-as-evidence pattern). The discipline is sound; the doctrine layer that grew up after AGENTS.md doesn't honor it consistently, and the prescriptive document itself contains a misquote in its example.

**Severity.** Quality. The misquote in AGENTS.md is the most concrete instance — easy fix, important because it's the document teaching the discipline.

**Confidence.** High on the textual mismatch.

**What would dissolve.** Fix the AGENTS.md example to match the actual ADR text: "ADR-0001 states 'multiple retrieval and ranking strategies *can* coexist' — this means designing so that they remain coexistable; it does not by itself prohibit shipping a single lens." The expanded example is honest about the ADR's actual scope.

**Suggested improvement direction.** Two changes: (1) fix AGENTS.md:131's example to match ADR-0001 text exactly; (2) a short pass on LONG-ARC and milestone docs to replace bare "ADR-0001 commits..." with quoted clauses.

#### D2. ADR-0001's coexistence claim was not preserved in the Phase 3-4 implementation; that violation surfaced via foundation-audit (ground 4)

**What.** Foundation-audit FINDINGS.md:246-256 documents that I1 (four signal types hardcoded), I2 (flat scorer not multi-stage), I3 (negative demotion as implicit category inference), and I4 (single enrichment record per paper) are all *implementation patterns that violate ADR-0001's coexistence commitment*. They were not caught by ADR-against-implementation review at the time of Phase 3-4 work; they were caught later by the foundation-audit.

LONG-ARC.md:101 ("Run an ADR-against-current-work audit at each deliberation boundary") is the doctrinal response to this exact pattern. But the LONG-ARC doctrine post-dates the violations it's responding to — it's a 2026-04-25 document responding to drift identified by the 2026-04-25 deliberation cycle.

What the governance docs *don't* show: a process for when ADR-0001 should have been read against Phase 3 work *at* Phase 3 time. AGENTS.md:53-60 ("Respect the core constraints") names some general principles but no per-phase ADR review step. The discipline now exists in LONG-ARC; it didn't exist when it would have caught the violations.

**Why it matters.** Ground 4 (self-application of discipline) and ground 3 (ADR honored at implementation layer). The team has the diagnosis, has named the anti-pattern, and has a counter-posture — but the foundation-audit's findings about the Phase 3-4 violations are a documented case of the discipline arriving after the violation. The honest read: the team has learned this lesson and applied it going forward (ADR-0005, multi-lens redirection); the question for the audit is whether the *governance docs themselves* now contain a per-phase ADR-review checkpoint.

**Severity.** Quality. The doctrinal counter-posture exists in LONG-ARC; its operationalization (when does an ADR audit happen, who runs it, what artifact?) is implicit.

**Confidence.** Medium-high. I can verify the gap; what I can't see is whether informal practice (e.g., spike methodology audits) is covering the gap operationally.

**What would dissolve.** A named operational hook: "Each phase-plan checkpoint runs an ADR-against-plan audit before phase exit; the audit artifact is filed at `.planning/audits/<phase>-adr-audit.md`." If this exists informally and just isn't documented, document it. If it doesn't exist, create the operational hook.

**Suggested improvement direction.** Add to LONG-ARC.md:96-103 ("What current planning must do") an operational sub-bullet: "Run an ADR-against-phase-plan audit at each phase-plan checkpoint, filing the artifact under `.planning/audits/`." This makes the doctrine's "ADR-against-current-work audit at each deliberation boundary" line specific enough to be checkable.

#### D3. The foundation-audit findings about CLAUDE.md staleness are partially addressed but the pattern that caused them is not

**What.** ECOSYSTEM-COMMENTARY.md:30 (in §2 "What It Missed") notes "CLAUDE.md stale" — "Still says 'Pre-implementation design phase. No source code exists.' Four phases are complete with working code, tests, and CLI." Current CLAUDE.md no longer says that — it says "Phases 1-5 + 04.1 complete. 403 tests passing" (line 9). So the specific staleness was fixed.

But: the date on the "Current status" line is now stale in the other direction. CLAUDE.md:9 says "Phase 6 (Content Normalization) is next." Per ROADMAP.md:25 and STATE.md:7, Phase 6 (and 7, 8, 9, 10) is complete; v0.1 is shipped; v0.2 is the active milestone. The "next" claim in CLAUDE.md is wrong by months and several major milestones.

The pattern: the team fixed the specific staleness ECOSYSTEM-COMMENTARY identified, but didn't institutionalize a CLAUDE.md update cadence. So a new staleness has accreted in the interim.

**Why it matters.** Ground 4 (self-application: the team identified the pattern but didn't address its recurrence mechanism) and ground 5 (delivery risk: CLAUDE.md is loaded into agent context as runtime instruction; agents are conditioned with stale milestone framing).

**Severity.** Quality. CLAUDE.md is short; an update is cheap. The structural finding (lack of cadence) is the more durable issue.

**Confidence.** High. Direct verification.

**What would dissolve.** Either a CLAUDE.md update that aligns with current STATE.md, or a STATE.md → CLAUDE.md sync convention (e.g., "CLAUDE.md is updated when STATE.md milestone changes").

**Suggested improvement direction.** Update CLAUDE.md:9 to reflect current state. Add to AGENTS.md or a new section in CLAUDE.md itself a "this file is updated on milestone change" note, naming the trigger condition.

### Dimension E — Doctrine-derivative drift

#### E1. ECOSYSTEM-COMMENTARY makes claims about positioning that are partially aspirational and partially descriptive without distinguishing

**What.** ECOSYSTEM-COMMENTARY.md is dated 2026-03-11 (line 3) and explicitly notes its number-staleness in the same line: "Numbers in this document reflect pre-04.1 state (307 tests → now 357, 150 papers → now 154, 5 proposed tools → 9 shipped)." This is good honest framing for the numeric staleness.

But the document also makes claims like (§3) "This resequencing treats MCP as the product surface (per ADR-0004), not as a wrapper applied after-the-fact" and (§5) "Multi-seed expansion with provenance | Snowball sampling: ... currently `find_related_papers` takes a single seed; should support multiple..." Some of these claims are descriptive of actual project decisions; some are recommendations the document was making at write-time. The document doesn't distinguish which is which from its current vantage point.

For example: "Multi-seed expansion" was eventually implemented (STATE.md:137 records "find_related_papers accepts str|list[str]"). But ECOSYSTEM-COMMENTARY still presents it as a recommendation. A reader cannot tell from ECOSYSTEM-COMMENTARY alone which of its 2026-03-11 recommendations have been implemented, which were rejected, and which are still pending.

**Why it matters.** Ground 5 (delivery risk: contributors reading ECOSYSTEM-COMMENTARY for guidance might re-do work that's already done, or treat already-implemented features as still-aspirational). Ground 4 (calibrated language: a doc dated 2026-03-11 making 2026-03-11 recommendations is honest only if the reader knows the temporal frame; the document partially provides this and partially doesn't).

**Severity.** Quality.

**Confidence.** Medium-high. Some of the "should support" framings have clearly been overtaken by implementation; others are harder to triangulate without reading the source code.

**What would dissolve.** A short "Status as of 2026-04-26" section appended to ECOSYSTEM-COMMENTARY that walks each recommendation and marks IMPLEMENTED / REJECTED / DEFERRED with file:line evidence. Or: explicit deprecation of the doc with a redirect to current planning artifacts.

**Suggested improvement direction.** Append a status table to ECOSYSTEM-COMMENTARY listing each substantive recommendation (§3 resequencing, §4A-D pre-MCP fixes, §5 priorities, §6 import strategy, §7 MCP surface) with current status. 30-minute pass.

#### E2. STATE.md is internally inconsistent and partially stale

**What.** STATE.md frontmatter lines 4-5: "milestone: v0.1, milestone_name: milestone, status: complete." Line 7: "stopped_at: v0.2 architectural shape committed via ADR-0005...detailed v0.2 plan still to be written." Line 9: "last_activity: 2026-04-25 -- multi-lens redirection committed."

But also:
- STATE.md:43 ("Velocity:") reports "Total plans completed: 23" — yet frontmatter line 13 says "completed_plans: 31" and line 25 says "Progress: [██████████] 100% (31/31 plans)."
- STATE.md:65-75 ("By Phase" extension after the markdown table) lists Phase 06 P01 through Phase 10 P03 with durations and task counts, but the formatting is inconsistent with the table above (no header row, mid-document).
- STATE.md:198 reads "Pending Todos: None yet." — but the very next sections ("Roadmap Evolution," "Blockers/Concerns") name several open items including "Phase 6: Docling vs Marker quality comparison... needs Phase 6 experimentation" (line 211, written as if Phase 6 were still future) and "OpenAlex credit-based pricing tiers need research" (line 212).
- STATE.md:225-226 ("Last session: 2026-04-16T18:50:00Z, Stopped at: v0.1 treated as complete historical milestone...") — but line 8 says "last_updated: 2026-04-25T20:00:00Z." So either the last_updated reflects only frontmatter changes (and the body wasn't updated on 2026-04-25), or one of the dates is wrong.

**Why it matters.** Ground 1 (CLAUDE.md states STATE.md is the live state record at line 40-41). If the live-state record is internally inconsistent and partially stale, agents using it as ground-truth substrate are working from unreliable data. Ground 4 (calibrated language as default register: a state document should be one of the highest-fidelity artifacts).

**Severity.** Quality, edging toward blocking on the "23 vs 31 plans" inconsistency. Either number is wrong, or the labels need clarification (maybe "23" is a stale figure and "31" is current; the document doesn't say).

**Confidence.** High. Direct textual inconsistencies.

**What would dissolve.** A STATE.md pass that reconciles the metrics, removes the stale "Phase 6 next" framings, updates the session-log section to current, and either removes or annotates the "Pending Todos: None yet" line with the actual pending items.

**Suggested improvement direction.** STATE.md needs structural attention more than content addition. Suggest splitting it into a tight header (current milestone, current activity, last update) and a clearly-archived "v0.1 historical metrics" section, so the live-state-record function and the historical-metrics function are separately legible.

#### E3. ADR-0001's coexistence commitment is operationalized in ADR-0005 in a way that strains the original

**What.** ADR-0001 says "multiple retrieval and ranking strategies can coexist" (line 22). ADR-0005 reads this as requiring v0.2 to ship at least two lenses, citing as justification that "Only a second lens forces the tool surface (Property 2) and storage layer (Property 3) to actually serve two lens shapes" (ADR-0005:19).

The strain: ADR-0001 says strategies *can* coexist (capability claim about the architecture); ADR-0005 reads this as requiring that they *do* coexist (a delivery claim). Those are different. ADR-0005's reading is defensible — "an architecture that admits N implementations but only ever instantiates one is shaped by that one in ways the abstraction-by-design can't catch." But ADR-0001 doesn't say that; it just says the architecture should admit coexistence.

This is a substantive reading-into. ADR-0005's reasoning is sound on its own terms; what's at issue is whether ADR-0001 actually demands the second-lens commitment, or whether ADR-0005 is making a stronger commitment that *uses ADR-0001 as warrant* without ADR-0001 actually licensing it.

**Why it matters.** Ground 3 (faithful operationalization of accepted ADRs at implementation layer). If ADR-0005's reading of ADR-0001 is the strong reading, ADR-0005 should either (a) cite ADR-0001 as an interpretive starting point and own the stronger commitment, or (b) propose an ADR-0001 amendment that updates "can coexist" to "must coexist via shipped second implementation."

**Severity.** Quality. The substantive v0.2 commitment is defensible on its own merits; the framing as "ADR-0001 requires this" is what's at issue.

**Confidence.** Medium-high. The textual mismatch is clear; whether the team experiences the mismatch as straining is something I can't tell from outside.

**What would dissolve.** Either an ADR-0001 amendment that explicitly upgrades the coexistence claim (which would let ADR-0005's reading stand cleanly), or an ADR-0005 reframing that owns the stronger commitment as ADR-0005's own contribution rather than as ADR-0001's requirement.

**Suggested improvement direction.** Cleanest: ADR-0005's Context section reframes one sentence: "ADR-0001's 'can coexist' is in this ADR upgraded to 'must coexist via at least two shipped implementations' on the basis of the property audit's evidence that single-lens 'interfaces' shape themselves around the lens that ships." This makes ADR-0005 the locus of the stronger commitment, with ADR-0001 as warrant rather than as source.

### Dimension F — Governance scope-creep / orphan content

#### F1. The governance set has grown without clear read-order or pruning, and overlaps significantly

**What.** The governance/doctrine set as I encountered it:
- Project-level: AGENTS.md (136 lines), CLAUDE.md (50 lines), `~/.claude/CLAUDE.md` (global), `~/CLAUDE.md` (project home)
- ADRs: ADR-0001 through ADR-0005 (~50-70 lines each)
- `.planning/`: PROJECT.md, VISION.md (118 lines), LONG-ARC.md (117 lines), ROADMAP.md (370 lines), REQUIREMENTS.md (260 lines), STATE.md (226 lines), ECOSYSTEM-COMMENTARY.md (148 lines), v1-MILESTONE-AUDIT.md
- `.planning/foundation-audit/`: METHODOLOGY.md, FINDINGS.md
- `.planning/spikes/METHODOLOGY.md` (separate from foundation-audit METHODOLOGY)
- `.planning/milestones/v0.1-MILESTONE.md`, `v0.2-MILESTONE.md`
- 14+ deliberation files in `.planning/deliberations/`

CLAUDE.md:34-44 lists a partial document structure but doesn't include VISION, LONG-ARC, milestones, or deliberations. PROJECT.md (line 22-25) lists "Primary active references" but the list is selective. There is no canonical "read this in order" path for a new contributor.

Overlaps: AGENTS.md and CLAUDE.md repeat several constraints (preferred abstractions; "do not assume" lists). PROJECT.md "Constraints" (lines 87-96) repeats most of CLAUDE.md "Key Architectural Constraints" (lines 18-24). LONG-ARC.md "Protected seams" (lines 30-40) overlaps with VISION.md "Load-bearing surface" (lines 34-38) and with the four ADRs.

Two `METHODOLOGY.md` files exist (`foundation-audit/METHODOLOGY.md` and `spikes/METHODOLOGY.md`) with non-trivial scope overlap (both about epistemic discipline applied to project work). Foundation-audit/METHODOLOGY is dated indirectly (referenced as Phase 5 audit material); spikes/METHODOLOGY is dated 2026-03-30 with extension on 2026-04-25. They're not in obvious dialog with each other.

**Why it matters.** Ground 5 (delivery risk: a new contributor — or a future agent session — has no canonical entry path). Ground 1 (governance docs are supposed to be a coherent substrate; coherence requires either a single canonical read-order or explicit map).

**Severity.** Quality. The overlap is mostly redundant rather than contradictory; the read-order gap is the more durable issue.

**Confidence.** High on the text counts and overlaps; medium on the impact (informal practice may be carrying the gap).

**What would dissolve.** Either a "READING-ORDER.md" or an expansion of CLAUDE.md's Document Structure section that names every governance document, what it does, and the recommended read-order for different roles (new contributor, agent starting a session, contributor returning after months away).

**Suggested improvement direction.** A small map: 5-7 lines in CLAUDE.md mapping roles to read-paths. ("New contributor: PROJECT.md → VISION.md → LONG-ARC.md → ADRs → AGENTS.md → ROADMAP.md. Agent starting a session: this file + STATE.md + relevant phase plan.") Cheap; high yield.

#### F2. Two methodology documents (foundation-audit and spikes) are not in explicit dialog

**What.** `.planning/foundation-audit/METHODOLOGY.md` (~67 lines) presents a 5-axis methodology (evidence tracing, alternative evaluation, sensitivity analysis, inference chain integrity, category discipline). `.planning/spikes/METHODOLOGY.md` (~187 lines as of last extension) presents 6 critical lenses (Bayesian, standpoint, paradigm, mechanistic, values-in-science, Duhem-Quine) plus 6 practice disciplines (A-F).

Neither document references the other. Foundation-audit/METHODOLOGY says (line 5) "Used during the Phase 5 foundation audit and available for future decision review." Spikes/METHODOLOGY says (line 21) "This document captures reusable critical lenses for spike design and interpretation."

The two are clearly meant for different scopes (foundation-audit for decision review; spikes for spike design and interpretation), but the scopes overlap (both apply to "epistemic justification for project decisions"). The 5 axes of foundation-audit could be re-derived from the 6+6 spike-methodology lenses and disciplines; the 6+6 could be re-derived from the 5 axes by adding spike-specific extensions. They're not in dialog about whether they're the same framework, complementary frameworks, or competing frameworks.

**Why it matters.** Ground 5 (delivery risk: new contributors learning the methodology don't know which document is canonical for what). Ground 4 (self-application of discipline: if the team's discipline is calibrated language and pattern-watch, two un-dialogued methodology documents is a form of methodology drift).

**Severity.** Quality.

**Confidence.** Medium. Both documents are clearly thoughtful; the lack of dialog might be intentional separation rather than orphan content.

**What would dissolve.** Either a one-line reference at the top of each pointing to the other and explaining the scope split, or a consolidation pass.

**Suggested improvement direction.** Add to spikes/METHODOLOGY.md a one-paragraph "Relationship to foundation-audit/METHODOLOGY" note; same in reverse. Consolidation isn't necessary if the scope split is real.

#### F3. The deliberation directory is large and not indexed

**What.** `.planning/deliberations/` contains 14 markdown files. Several have dates in their filenames (2026-04-25-*); several don't (e.g., `local-gap-propagation-and-signal-interpretation.md`, `comparative-characterization-and-nonadditive-evaluation-praxis.md`). PROJECT.md:25 lists `local-gap-propagation-and-signal-interpretation.md` as a primary active reference, but no other deliberation is named.

There is no `deliberations/INDEX.md` or `README.md`. A new contributor entering this directory has no map: which deliberations are still active, which were superseded, which produced ADRs vs which are exploratory.

**Why it matters.** Ground 5 (delivery risk + future-team usability). Ground 1 (the deliberations are clearly meant to be part of the project's epistemic substrate; without an index they're a corpus, not a substrate).

**Severity.** Quality.

**Confidence.** Medium-high.

**What would dissolve.** A deliberation index — date, title, status (active/produced-ADR/superseded/exploratory), one-line summary.

**Suggested improvement direction.** A short `deliberations/INDEX.md` that lists each file with status and one-line summary. 30-minute pass.

## What works well

These are the strengths grounded in the same (1)–(5) the team should preserve:

- **The four foundational ADRs are honestly conservative.** ADRs 0001-0004 are short, hedged, posture-explicit, and their Notes sections actively de-escalate (ADR-0001:40-41 "This ADR is about process and architecture posture, not about avoiding implementation"; ADR-0002:38 "This does not prohibit broader enrichment later. It only sets the early default posture"; ADR-0004:34-35 "This ADR does not say all workflow objects ship in v1. It says the MCP design should anticipate them."). This restraint is exactly the right register for foundational documents. The drift problem is in derivative artifacts attributing more to these ADRs than they say; the ADRs themselves are not the problem.
- **VISION.md and LONG-ARC.md are well-separated by function.** VISION.md is product identity (audience, lens trajectory, anti-vision); LONG-ARC.md is planning doctrine (protected seams, anti-patterns, what current planning must do, reopen conditions). The split is honest about what each document is for. Both have explicit "Reopen conditions" sections that give the documents lifecycle hygiene most governance docs lack.
- **The foundation-audit's category-discipline analysis is genuinely strong.** FINDINGS.md §2 ("Requirements Extraction") with its identification of "category errors" (hedging language → firm specification) is a transferable methodology, well-illustrated with concrete examples (CONT-05, MCP-05, INTR-04). The five categories ("Settled / Chosen for now / Hypothesis / Open" in AGENTS.md and CLAUDE.md) are then operationalized from this analysis. The discipline is real and the prescription matches the diagnosis.
- **REQUIREMENTS.md uses `[chosen for now]` annotations.** Lines 53-54 (INTR-04, INTR-05), 82 (CONT-05), 91 (MCP-05), 93 (MCP-07) carry explicit "[chosen for now]" tags with parenthetical justification ("source says 'possible' signal type"). This is calibration that propagates to the prose of the requirement, not just the closing footnote — exactly the discipline METHODOLOGY discipline D requires.
- **Anti-patterns named in LONG-ARC.md are concrete and grounded.** Lines 42-52 list six anti-patterns with diagnoses *and* counter-postures *and* (in several cases) specific prior incidents the project has experienced. "ADR violation by gradual local-reasonable steps. Each step locally defensible; cumulative drift away from an accepted ADR. The 005-008 spike chain did this to ADR-0001 over weeks." This is doctrine grounded in experience, not abstract principles.
- **The spike-methodology document shows genuine self-application.** METHODOLOGY discipline F (`spikes/METHODOLOGY.md:160-166`) explicitly diagnoses that the team's own audit cycle exhibited the closure-pressure pattern at multiple layers. The codification of paired review (discipline A) is a real institutional response to a real failure. This is what the AGENTS.md prescriptions could become if they were similarly grounded in observed difficulty.

## Convergent risks

Where multiple findings within this audit point at the same underlying weakness:

**Convergence 1: Calibration drift between source and citation (A1, A2, D1, E3).** The four foundational ADRs use hedged modal verbs ("can," "will," not "must"). Derivative artifacts (LONG-ARC, ADR-0005, milestone docs, AGENTS.md's own example) re-cite them with stronger modals ("binding," "must," "binds"). The pattern recurs at multiple layers. Treat as one issue: the team's prose drifts from source-text to interpretive-paraphrase, and the interpretive paraphrases inflate the rhetorical pitch. A single doctrine-pass that re-verifies ADR citations against ADR text would address most of these findings.

**Convergence 2: Audit findings don't propagate into the audited prescriptive layer (A2, C3, D3).** The foundation-audit identified violations of AGENTS.md prescriptions; AGENTS.md was not updated in response. ECOSYSTEM-COMMENTARY identified CLAUDE.md staleness; the specific staleness was fixed but the underlying cadence problem produced new staleness. STATE.md inconsistencies identified in this audit (E2) are likely a similar pattern at smaller scale. Treat as one issue: prescriptive governance documents in this project do not have a documented update mechanism that triggers when audits surface violations or staleness. A "post-audit follow-through" convention would address most of these.

**Convergence 3: No canonical read-order or document map for the governance set (F1, F2, F3, also bears on D3).** The governance set has grown organically. There is no single document that says "these are all the governance documents; here is what each does; here is the order to read them in." This produces orphaning (deliberations not indexed), redundancy (PROJECT.md / CLAUDE.md / AGENTS.md overlap), and reading-order ambiguity (two methodology files; multiple roadmap-shaped artifacts). A single map would address several findings at once.

## Steelman residue

Honest pass over my own findings:

- **A1 ("ADRs are calibrated; doctrine is not").** This is the strongest survived finding, but the steelman is real: derivative documents *should* read ADRs interpretively, not just paraphrase them. ADR-0001's "can coexist" is shorthand for an architectural posture; "binding" is one valid characterization of "we have committed to this posture." The finding stands because the gap between the modal verbs is large enough to do real work in framing decisions, but I should not pretend that derivative-attribution drift is automatically a calibration failure. It can be a valid intensification grounded in lived experience (e.g., the team learned via 005-008 drift that "can" needed to become "must" to be honored).

- **B1 ("ADRs don't enumerate alternatives").** I labeled this taste in my own writing, and I think that's right. The finding does less work than the heading suggests. Posture-ADRs in their genre don't typically enumerate alternatives; the methodology document's "Alternative Evaluation" axis is for adversarial review, not ADR composition. I included this finding mainly to demonstrate I had read the dimension B prompt; the actual signal is weak.

- **C1 ("Stack D silent default").** This is genuinely the LONG-ARC anti-pattern, but the stakes are tiny. CLAUDE.md is brief and "Not Stack D" is one line; even a perfectly calibrated CLAUDE.md would have similar shorthand. The finding is correct but trivial. I kept it because the dimension-C prompt specifically asked for this pattern; if the dimension hadn't asked, I might have folded this into a one-line note rather than a numbered finding.

- **C3 ("audit-as-product").** I framed this strongly ("findings filed, not propagated"). The steelman: the team did propagate the audit findings into Quick Task 1 (resolving I1/I3/I4/I6), and the calibrated-language `[chosen for now]` annotations now visible in REQUIREMENTS.md trace plausibly to the foundation-audit's category-error analysis. So the propagation is partial, not absent. My finding overstates the gap. The accurate version is "propagation happened in code and in some annotations but didn't update FINDINGS.md itself, so the audit document is a snapshot rather than a live tracker."

- **D2 ("ADR-0001 violations weren't caught at Phase 3-4 time").** This is a fact about project history, but the steelman is that catching ADR-0001 violations in Phase 3-4 required the kind of property-audit discipline that the team has *now* developed and didn't have *then*. Faulting the governance docs for not having a then-nonexistent discipline encoded is anachronistic. The stronger version of the finding is: now that the discipline exists, is it operationalized in a way that will catch the next ADR-violation drift before it accumulates? That's the question worth asking, and my finding partially asks it but mixes it with the historical observation in a way that's not as sharp as it could be.

- **E3 ("ADR-0005 strains ADR-0001's reading").** I labeled this Quality. On reflection, it might be lower-stakes than I framed. ADR-0005 is the team's own ADR; it can absorb the stronger commitment as its own without amending ADR-0001, and "ADR-0001 commits us to architecture that admits coexistence; we now interpret that as requiring shipped second implementation per the property-audit evidence" is a defensible reading-into. The finding stands but mostly as encouragement to make the reading-into explicit rather than as a critique.

- **F2 ("two METHODOLOGY documents not in dialog").** The steelman: they may simply have different scopes, and the lack of dialog reflects appropriate separation. My finding partly assumes that all methodology documents in a project should be in mutual dialog; that's not obviously true. Foundation-audit/METHODOLOGY is for decision-review epistemic discipline; spikes/METHODOLOGY is for spike design and interpretation. They genuinely could be parallel without redundancy. The cross-reference recommendation is still useful but the finding is weaker than the heading suggested.

## What this audit cannot tell you

Bounded scope. Same-vendor critical reading reads register and structure. I cannot tell you:

- Whether the v0.2 plan is technically sound (substance question).
- Whether the foundation-audit's I1-I6 findings were correctly resolved in code (code question).
- Whether the lens abstraction will hold up under a citation/community lens implementation (empirical question).
- Whether the calibrated-language discipline is actually changing project outcomes vs being a frame the project happens to like (would require longitudinal observation across audits).
- Whether the doctrinal drift I'm identifying is unusual in scope or mild compared to peer projects (would require comparison set).
- Whether the team's informal practice covers gaps I've identified in formal documentation (would require participant observation).
- Whether AGENTS.md / CLAUDE.md instructions actually shift agent behavior in measurable ways (empirical question that requires controlled comparison).
- Whether the parallel cross-vendor governance audit identifies the same convergent risks I've identified, or different ones (by design, I haven't read it).

The substance check is the cross-vendor reviewer's role and the codebase's job. This audit has read the governance documents as documents — what they say, what they cite, what register they use, where they cohere and where they don't. That's a meaningful slice of the question but it's a slice.
