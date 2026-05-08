---
type: pressure-pass
status: complete
date: 2026-04-25
author: Claude (Opus 4.7)
scope:
  - .planning/spikes/005-evaluation-framework-robustness/HANDOFF.md
  - .planning/spikes/006-model-retrieval-interactions/HANDOFF.md
  - .planning/spikes/007-training-data-mechanism-probes/HANDOFF.md
  - .planning/spikes/NEXT-ROUND-SUITE.md
  - .planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md
related:
  - ../../deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md
  - ../../deliberations/reviews/2026-04-16-sequential-narrowing-deliberation-review.md
---

# Handoff Pressure Pass — 2026-04-25

## Purpose

Read-and-annotate pass over the active suite's handoff and design artifacts before a remedy is selected from the deliberation's dimensional response space. This artifact records findings without overwriting the source artifacts. The handoffs remain the primary evidence; this pass is a structured second reading.

## Method

For each artifact, the diagnostic questions from the addendum to [sequential-narrowing-anti-regret-and-spike-inference-limits.md](../../deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md):

1. Which exclusions are evidence-weakened, cost-deferred, or both? Note where classification resists clean assignment.
2. What would actually reopen each excluded branch? Is the trigger concrete or gestural?
3. Which auxiliary bundle was held fixed? Named or implicit, short or sprawling?
4. Where does prose drift from "posterior shift under conditions" toward "family that matters"?
5. What does this handoff not legitimately tell us?
6. Redesign signal: which excluded branches, if reclassified, would force which artifacts to be redrawn?

For each finding, name which cells in the dimensional response space (Subject × Nature × Trigger × Scope) are actuated.

---

## 005 / HANDOFF.md

### Q1 — exclusions classified

- **"Drop the assumption that Qwen3 is a presumptive complementary second-view candidate"** — `[both]`. There is *some* evidence (family-induced shifts under `category + lexical`), but the handoff explicitly preserves the full challenger set in `006` (Carry Forward item 3). So 005 did not actually exclude Qwen3 — it only weakened the *presumption*. The true exclusion happens at 006. Tag this *prior shift*, not *exclusion*.
- **"Drop any expectation that alternative profile construction is likely to produce a new positive challenger without retrieval evidence"** — this is a *predictive generalization*, not an exclusion of a specific branch. It does not fit the evidence/cost classification cleanly. Flag as **interpretive prior shift presented as decision**.
- **SPECTER2-refined family** (Deferred) — `[cost-deferred]`. Held back "as a tertiary cross-check if 006 produces ambiguous results." Pure sequencing.
- **Voyage non-API analogue** (Deferred) — `[cost-deferred]`. No timeline, no budget owner.

### Q2 — reopening triggers

- Qwen3 presumption: trigger is gestural — "006 must test whether retrieval geometry changes restore any challenger that 005 weakened, especially Qwen3," with no threshold for what counts as "restore."
- SPECTER2-refined: "if 006 produces ambiguous results" — what counts as ambiguous is undefined.
- Voyage non-API analogue: conditional on availability of a non-API analogue, with no time horizon.

**All three triggers are gestural.** None is concrete enough to fire without retrospective relitigation.

### Q3 — auxiliary bundle

The Trace-Attunement note partially names this: "leaves citation-native and graph-native profile construction outside the present test." But the *full* bundle is not pre-stated as a freeze. Held fixed but not enumerated:
- Profile granularity (8 profiles, P1-P8)
- Sample size and seed-anchoring conditions
- The set of model families being compared
- Three-family choice for profile construction (MiniLM-saved, category+lexical, SPECTER2-refined as fallback)

**Bundle is sprawling and only partially named.**

### Q4 — drift

Low. The Counter-Reading section explicitly hedges. "Treat the Qwen3 candidate-second-view story as weakened rather than live by default" preserves contestability. The closest thing to drift is the predictive generalization in Drop For Now item 2, which extrapolates beyond the test's scope.

### Q5 — what 005 does not legitimately tell us

- How Qwen3 would behave under richer profile families (citation-native, graph-native, user-corrected).
- That the family-induced shifts observed are *the* deepest framework dependence — only that *those* shifts exist within *those* three families.
- Anything about the relative magnitude of family-bias vs. retrieval-bias vs. mechanism-bias.
- That the SPECTER2-refined family would have failed; it was held back by sequencing, not weakened.

### Q6 — redesign signals

- If the SPECTER2-refined family is reclassified to "evidence-warranted-but-deferred," it forces a `005.5` or `006`-extension to actually run that family. Cell: **Subject: pre-`008` chain · Nature: insert · Trigger: cost reassessment · Scope: local to wave.**
- Auxiliary-bundle gap (citation-native, graph-native profiles outside the test) touches **ADR-0001** (exploration-first architecture). If alternative profile constructions are excluded by sequencing rather than evidence, the ADR's "multiple retrieval/ranking strategies must coexist" intent is at risk of soft erosion. Cell: **Subject: interpretation layer / ADR · Nature: amend · Trigger: methodological discovery · Scope: cross-program.**

---

## 006 / HANDOFF.md

### Q1 — exclusions classified

- **Qwen3 dropped** — `[evidence-weakened-via-chain]`. The phrasing "did not produce a clean retrieval-based rescue" is *absence of rescue*, not evidence of unsuitability. For a rescue to be needed, 005's prior weakening must already be load-bearing — and 005's weakening was itself partially cost-deferred (see 005 Q1). The exclusion is therefore thinner than the chain implies.
- **Model-specific kNN configuration re-entering 008** (Deferred) — `[cost-deferred]`. The Counter-Reading is explicit: "kNN's near-universal union gains mean the spike should have carried method-specific configurations rather than model families. I am not choosing that reading here because it would explode the downstream space too early." This is a textbook cost-deferred exclusion that the handoff itself names.
- **MMR alternative** (Deferred) — `[cost-deferred]`. Untested by sequencing.

### Q2 — reopening triggers

- Qwen3: **none.** Once dropped at 006, no spike has obligation to revisit.
- kNN configuration / MMR: "should later re-enter 008 as a concrete challenger" — no condition, no owner.

The 006 handoff is more closed than 005.

### Q3 — auxiliary bundle

- Family-level analysis (not configuration-level)
- Centroid vs. Spike 003 kNN-per-seed (not MMR or other operators)
- The two profile families chosen by 005
- Seeds, sample, profile set held constant

The Trace-Attunement note flags the operator contrast as partial. **The family-level vs. configuration-level distinction is the most consequential held-fixed auxiliary, and it is flagged in Counter-Reading rather than as a freeze statement at the front.**

### Q4 — drift

Medium. Stella is carried as "explicitly ambiguous" — careful. But:
- "007 should treat Qwen3 as dropped unless a concrete later reason emerges to reopen it" — operational closure with no pre-registered concrete reason.
- "007 must narrow the live challenger set to at most two for 008, following the suite rule" — sequencing rule mentioned in the same register as evidence claims, allowing downstream readers to interpret the resulting two as evidence-warranted rather than budget-warranted.

### Q5 — what 006 does not legitimately tell us

- That Qwen3 is non-complementary in general; only that under MiniLM-saved + category+lexical profiles with centroid + Spike-003 kNN-per-seed, it didn't show a rescue.
- That the family is the right unit of analysis. 006 explicitly deferred this question.
- That MMR would behave like centroid; untested.
- That Stella's instability is intrinsic; could be an artifact of the specific kNN procedure used.

### Q6 — redesign signals

- **HIGHEST-IMPACT FINDING IN THE PASS:** If the family-vs-configuration distinction is reclassified from "deferred" to "the actual primary failure mode," `008`'s narrowing premise — *that families are the right unit* — collapses. `008/DESIGN.md` says compare three configurations: `MiniLM + TF-IDF`, `SPECTER2`, `Voyage`. But the latter two are family designators, not specific configurations. If the live question is configuration-level, **`008` is asking the wrong question.** Cell: **Subject: `008` + NEXT-ROUND-SUITE · Nature: reframe · Trigger: methodological discovery · Scope: cross-wave.**
- If Qwen3's drop is reclassified to `[cost-deferred-via-chain]`, then either a lightweight rescue probe is warranted or `007.5`/`008` should pre-register a Qwen3 fallback slot. Cell: **Subject: pre-`008` chain · Nature: insert · Trigger: evidence reversal · Scope: local to wave.**
- MMR untested → potential `006.5` or methodology-level note. Cell: **Subject: methodology + pre-`008` chain · Nature: augment + insert · Trigger: cost reassessment · Scope: program-level.**

---

## 007 / HANDOFF.md

### Q1 — exclusions classified

- **Stella deferred** — `[cost-deferred + stance-deferred]`. The Counter-Reading is explicit: "Stella should have claimed an 008 slot because it had the strongest 006 complementarity score. I am not choosing that reading because 007 was supposed to narrow on mechanism-backed reasons." The judgment that *mechanism-support trumps complementarity* is **the load-bearing stance choice in the entire chain.** It is not pre-registered in `NEXT-ROUND-SUITE.md`. It is not argued from evidence in 007. It excludes Stella from `008` on its own.
- **GTE deferred** — `[cost-deferred]`. Inherits the "at most two challengers" capacity rule. No specific evidence basis given.
- **Voyage→Stella substitution** (open) — `[cost-deferred]`. Fallback only.
- **Qwen3 kept dropped** — `[chain-derived]`. "Nothing in 007 created a new reason to reopen it" — absence of evidence, not evidence. Inherits 006's chain weakness.

### Q2 — reopening triggers

- Stella: "If Voyage proves too operationally unstable during 008 execution prep, Stella is the first fallback candidate." **This is the only operational trigger in the entire chain — but it fires on Voyage's failure, not on Stella's strength.** No trigger fires Stella in if Stella's case strengthens; the asymmetry is load-bearing.
- GTE: none.
- Qwen3: none.

### Q3 — auxiliary bundle

- **Mechanism-backed-narrative as the gate criterion** (vs. complementarity, or other criteria)
- Substitute mechanism probes used because the citation/community route was *unavailable* — partial proxy
- Profile set, sample, seeds held constant
- Four-family shortlist from 006

The Trace-Attunement note acknowledges the substitution. **The substitution itself is a major auxiliary** — the citation/community probe being unavailable is not a mild caveat; it removes the strongest evidential leg.

### Q4 — drift

Medium-high. The Counter-Reading does honest work, but the carried claim ("SPECTER2 + Voyage win on mechanism-backed reasons") sits in a frame where:
- The "mechanism > complementarity" weighting is asserted, not argued.
- The substitute probes (lexical/category proxies) are weaker than the originally-intended citation/community probes, but the carried conclusion does not weight this absence.
- "SPECTER2 retained the strongest specialized-domain pattern" — stated without margin or magnitude.

### Q5 — what 007 does not legitimately tell us

- That Stella is functionally inferior to SPECTER2 / Voyage. Only that Stella has weaker *mechanism-backed support under the substitute probes used*.
- That mechanism-support is the right gate.
- That the citation/community route, if available, would have agreed with the proxy probes.
- That the four families on the shortlist are meaningfully comparable along a single mechanism dimension.

### Q6 — redesign signals — highest-stakes set in the pass

- **CRITICAL:** If "mechanism-support > complementarity" is reclassified from a stance to a contested choice, Stella's exclusion is barely justified. **Forces:** `008` should run with three challengers (SPECTER2, Voyage, Stella) plus the control — exceeding the suite rule. Or split: `008a` runs SPECTER2+Voyage as designed; `008b` runs Stella under matched conditions. Cell: **Subject: `008` + NEXT-ROUND-SUITE · Nature: split or widen · Trigger: methodological discovery · Scope: cross-wave.**
- **CRITICAL:** If the citation/community probe being unavailable is reclassified as "the *primary* mechanism evidence is missing," 007's mechanism-backed narrowing is built on substitute probes, and a `007.5` running citation/community probes (now or in the future) becomes urgent. Cell: **Subject: pre-`008` chain · Nature: insert · Trigger: methodological discovery · Scope: local to wave.**
- The Voyage→Stella fallback is operational only, not evidential. **Methodology-level finding:** fallback mechanisms should also fire on positive evidence for the deferred branch, not just on operational failure of the carried branch. Cell: **Subject: methodology + artifact discipline · Nature: augment · Trigger: methodological discovery · Scope: program-level.**

---

## NEXT-ROUND-SUITE.md (suite-level contract)

### Q1 — structural exclusions

- "Spikes 005 and 006 run on the full current comparison set. Spikes 007 and 008 run on a shortlisted set of model families, not every challenger" — `[suite-level cost-deferred]` framed as evidence-driven narrowing.
- The shortlisting rule is justified on pre-spike pairwise distance. **Pairwise distance is a representational measure, not a functional one.** This proxy is taken as a stand-in for "structural distinctness" and not validated.

### Q2 — suite-level reopening triggers

- "Unless 005/006 show that collapsing to representatives would erase meaningful differences" — gestural. "Meaningful" undefined.
- "If 005's findings invert under alternative profiles, every later spike must be read as framework-dependent" — more concrete but binary. Partial inversion (which is what 005 actually showed) has no defined response.

### Q3 — suite-level auxiliary bundle

- The four-spike sequence itself: 005 → 006 → 007 → 008. *Narrowing is the right structure* is a meta-auxiliary.
- The "shortlisted set of model families" frame assumes families are the right unit (the same slippage 006 deferred).
- The `[chosen for now]` 4-stage program is a strong commitment to a specific epistemic posture (eliminative) without explicit alternative-posture comparison.

### Q4 — drift

Structural. The suite contract is internally consistent, but its biases toward narrowing are not flagged as biases:
- "008 must compare the incumbent control plus at most two shortlisted challengers in one pass" — hard rule, no test of whether the rule fits the question.
- "007 -> 008: 007 must either narrow the live candidate set to at most two challengers or explicitly state that mechanism probes failed to discriminate." **Asymmetry: narrowing is the default; non-narrowing requires explicit declaration.** Biases toward closure.

### Q5 — what NEXT-ROUND-SUITE.md does not legitimately tell us

- That the "narrow as you go" structure is the right structure for this question.
- That family-level analysis is sufficient.
- That four spikes exhaust the relevant probes.
- That pairwise representational distance reliably proxies structural distinctness.

### Q6 — redesign signals

- If pressure findings show family-level analysis is wrong, NEXT-ROUND-SUITE.md needs amending. Cell: **Subject: post-`008` plan + meta-suite · Nature: amend + reframe · Trigger: methodological discovery · Scope: program-level.**
- If "narrow at each step" is reframed as "rank and deprioritize," the program's structural premise needs revision — touches the whole program, not just `008`. Cell: **Subject: methodology + suite contract · Nature: reframe · Trigger: methodological discovery · Scope: program-level.**

---

## 008 / DESIGN.md

### Q1 — pre-committed decisions

- "Run at most three configurations in one pass: incumbent + up to two challengers" — locked, inheriting 007's narrowing.
- "current 007 handoff selects SPECTER2 and Voyage for the first pass, with Stella retained only as an explicit fallback if Voyage proves impractical" — cost-deferred with operational-only reopening trigger.
- "Use a representative profile set, not all 8 by default" — `[cost-deferred]`. Three of eight (P2 + P3/P8 + P5/P7).

### Q2 — reopening triggers within 008

- The Voyage→Stella fallback — operational only.
- "If human review is unavailable, stop at `pilot only / incomplete`" — well-pre-registered. ✓
- "If two or more sampled task instances are `disputed`, 008 may not close H1 or H5" — well-pre-registered. ✓

**`008/DESIGN.md` has the strongest pre-registered triggers in the chain — but they are *internal* triggers (will-this-spike-close-the-question), not *external* triggers (should-deferred-branches-reopen).**

### Q3 — auxiliary bundle

- Three "configurations" — but the design uses configuration language for `MiniLM + TF-IDF` and family language for `SPECTER2` / `Voyage`. **Slippage.**
- Three of eight profiles. Five profiles absent.
- Three task templates per profile. Task generation methodology held fixed.
- Tool budget, turn budget, context budget — held constant across configurations.

### Q4 — drift

Low for the spike's own claims. Hypothesis priors explicit (P(H1) = 0.70, P(H5) = 0.45). Bounded language preserved. **Structural slippage moderate** in the configuration-vs-family register: "the unit of interest is whether a configuration helps an agent" — but the design measures family proxies as configurations.

### Q5 — what 008 does not legitimately tell us regardless of outcome

- Whether the family-as-configuration assumption holds.
- Anything about challengers excluded at 007.
- Anything about profiles outside P2/P3/P8/P5/P7.
- Anything about alternative retrieval geometries (centroid vs kNN vs MMR).
- Anything about alternative mechanism narratives.
- Its "function-in-use" verdict is bounded to the specific task templates chosen.

### Q6 — redesign signals

- If pressure findings shift Stella from `[stance-deferred]` to `[evidence-comparable]`, the "two challengers + incumbent" rule becomes the bottleneck. Options: split `008` (Stella runs in `008b`), widen to three challengers, or convert Stella's exclusion into a *pre-registered post-`008` trigger* ("if SPECTER2 wins by < X on metric Y, run Stella in `008b`"). Cell: **Subject: `008` · Nature: split, widen, or pre-register external trigger · Trigger: evidence reversal · Scope: local to wave.**
- If the configuration-vs-family slippage is reclassified as material, `008` should be reframed: instead of testing "SPECTER2 vs Voyage vs incumbent" as families, it should specify exact configurations (model + retrieval geometry + profile-aware operator). Cell: **Subject: `008` · Nature: reframe · Trigger: methodological discovery · Scope: local to wave.**
- If "the citation/community probe was unavailable" is load-bearing, `008` should pre-register what happens if a `007.5` is later run. Cell: **Subject: `008` + artifact discipline · Nature: augment · Trigger: methodological discovery · Scope: cross-wave.**

---

## Cross-artifact synthesis

Seven findings, in order of impact:

1. **Mechanism-support > complementarity is a load-bearing stance choice that is not labeled as a stance.** It is the single decision excluding Stella from `008`. Not pre-registered in `NEXT-ROUND-SUITE.md`, not argued from evidence in 007. Reclassifying it as a *contested choice* changes the program substantively. **Highest impact.**

2. **The configuration-vs-family slippage runs through the whole chain.** 005 evaluates families; 006 honestly defers configuration-level questions; 007 narrows on family; 008 evaluates "configurations" but uses family names. The configuration question is never directly answered yet `008` is being asked to answer it. **Second-highest impact.**

3. **Auxiliary bundles are partially named in Trace-Attunement notes but never pre-stated as freezes.** Each handoff acknowledges what was held fixed only ex post. A pre-registered freeze would change retrospective auditability.

4. **Reopening triggers are gestural, not operational, except for `008`'s internal closure conditions.** Branches dropped at 005/006/007 do not have triggers that could fire from outside the executing spike. The single operational trigger (Voyage→Stella) fires on operational failure of the carried branch, not on positive evidence for the deferred branch — load-bearing asymmetry.

5. **The 005 → 006 chain on Qwen3 is thinner than the 007 narrative implies.** 005 weakened the *presumption*; 006 didn't *rescue* (absence of evidence). 007 inherits "Qwen3 dropped" without flagging chain dependency.

6. **`008/DESIGN.md` has the strongest pre-registration discipline in the chain (P(H1)=0.70, P(H5)=0.45, disputed-instance rules, pilot-only fallback).** Its inheritance from upstream is uncritical, however. This is asymmetric: rigour at the leaf, looseness at the chain.

7. **The "narrow at each step" structure is itself an unflagged auxiliary.** NEXT-ROUND-SUITE treats narrowing as default and non-narrowing as exception. The reverse framing (rank-and-deprioritize) is never considered at program level.

## Cells in the dimensional response space actuated

| Finding | Subject | Nature | Trigger | Scope |
|---|---|---|---|---|
| 1. Mechanism-vs-complementarity stance | `008` + methodology | split or widen (008) + augment (methodology) | methodological discovery | cross-wave |
| 2. Configuration-vs-family slippage | `008` + NEXT-ROUND-SUITE + methodology | reframe (008) + amend (suite) + augment (methodology) | methodological discovery | program-level |
| 3. Auxiliary bundle freeze missing | artifact discipline | augment | methodological discovery | program-level |
| 4. Reopening triggers gestural | artifact discipline + `008` + 005/006/007 retroactively | augment + retroactively patch | methodological discovery | cross-wave |
| 5. Qwen3 chain dependency | pre-`008` chain + 005/006 retroactively | insert (007.5 or 005.5) + retroactively patch | evidence reversal | local to wave |
| 6. 008's pre-registration discipline strong; inheritance weak | `008` | augment (pre-register external triggers) | methodological discovery | local |
| 7. Narrow-at-each-step as auxiliary | NEXT-ROUND-SUITE + methodology | reframe + augment | methodological discovery | program-level |

## Composition

The findings cluster:

- **Tactical (008-redesign):** 1, 2, 6 — directly affect whether/how `008` should run.
- **Methodological (artifact discipline):** 3, 4, 7 — affect templates, suite contract, methodology.
- **Retroactive (handoff patch):** 4, 5 — affect 005/006/007 handoffs.

A coherent composed response, drawn from the dimensional space:

1. **Tactical** — `008` reframed (configuration-vs-family) and either split or widened to include Stella. Stella's re-entry pre-registered with a concrete metric/margin trigger, not just operational fallback. The mechanism-vs-complementarity gate criterion either argued explicitly or treated as one of two contested gates.
2. **Methodological** — Auxiliary bundle freeze + `[evidence-weakened] / [cost-deferred] / [both]` decision tag + concrete reopening trigger added to handoff template. NEXT-ROUND-SUITE amended to consider rank-and-deprioritize as alternative posture, even if narrowing is retained.
3. **Retroactive** — 005 / 006 / 007 handoffs retroactively annotated (in a separate companion artifact, not by overwriting) with decision tags and the reopening triggers that were missing.
4. **Cross-program** — One paragraph noting that the auxiliary-bundle gap (citation-native, graph-native profiles outside the test) touches ADR-0001's "multiple retrieval/ranking strategies must coexist" intent. Not an ADR amendment yet — a flag for the next ADR review.

## What the response should NOT do

- Run `008` as designed without addressing Stella, configuration-vs-family, or external reopening triggers. The tactical findings are load-bearing on `008`'s validity.
- Rewrite the upstream handoffs in place. The handoffs are evidence; retroactive annotation goes in a separate artifact.
- Adopt the full review remedy set as a one-shot template fix without doing the configuration-vs-family work. That fix is template-level; the configuration-vs-family question is substantive.

## Confidence calibration

These findings are derived from a single read pass by one reader. They are **not** the final word.

- Findings 1 (mechanism-vs-complementarity) and 2 (configuration-vs-family) are the most contestable because they are framing claims, not evidence claims. A second reader, or the original spike author, may judge that mechanism-support was always implicitly the gate criterion and that family-level analysis was always the agreed unit. If so, the load-bearing stance label is mine, not theirs — but the *unflagged* nature of the choice still warrants the methodological remedy.
- Findings 3, 4, 7 are template/contract observations, less contestable.
- Findings 5, 6 are direct readings of the artifacts, least contestable.

## Recommendation

Return to [sequential-narrowing-anti-regret-and-spike-inference-limits.md](../../deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md) and compose a response from the dimensional space that includes — at minimum — Findings 1, 2, and 4 as tactical / methodological work. Findings 3, 5, 6, 7 are productive but secondary. The composition decision (which cells to actuate, in what order) is for the next deliberation step, not for this pass.

The pass is complete. The handoffs are unchanged.

---

## After the paired review — 2026-04-25

> The original prose above is preserved as written on 2026-04-25 morning, before the paired review was dispatched. Nothing above this line has been edited. This section is layered on top — a third reading, alongside the two reviews now on disk.

### Dispatch record

Two reviewers, dispatched in parallel from a shared package at [`2026-04-25-paired-review-package/`](./2026-04-25-paired-review-package/).

| Reviewer | Model | Effort | Output |
|---|---|---|---|
| Cross-vendor primary | GPT-5.5 (codex CLI) | xhigh | [`2026-04-25-pressure-pass-cross-vendor-review.md`](./2026-04-25-pressure-pass-cross-vendor-review.md) |
| Opus adversarial | Claude Opus 4.7 (fresh session) | xhigh | [`2026-04-25-pressure-pass-opus-adversarial.md`](./2026-04-25-pressure-pass-opus-adversarial.md) |

Cross-vendor ran in two phases (Phase 1 independent reading without access to the pressure pass; Phase 2 comparison after Phase 1 was written). Opus adversarial ran in one phase with full access to both the pressure pass and the underlying artifacts. Both reviews speak for themselves at the linked paths and are not summarised here.

### What the differences demand

The point of pairing two readers was not to produce a verdict on the pressure pass. It was to surface whatever the differences between two readings, working at different distances from the pass, would expose. What follows is what those differences indicate, treated as readings layered on top of the original prose rather than as judgements about it.

#### One convergent fact

Both readers, working independently from non-overlapping prompts, identified the same textual point: `NEXT-ROUND-SUITE.md:65-69` pre-registers a `007 → 008` ranking rule that puts complementarity #1 and mechanism support #2. The pressure pass's Finding 1 sentence "Not pre-registered in `NEXT-ROUND-SUITE.md`" is wrong on this rule. The convergent identification of a single textual fact across model families is the most reliable signal in the pair, and it indicts a specific clause above (Cross-artifact synthesis Finding 1, the second sentence) — not the whole framing, but a clause within it.

#### Multiple defensible readings of the same residue

Where the pressure pass committed to one reading of Finding 1, both reviews together carry at least three:

1. **Methodological-vocabulary reading.** The criterion choice was insufficiently labelled as a stance. The remedy is template discipline: when a methodological commitment is made, label it.
2. **Document-discipline reading.** The suite contract's tiebreaker was reversed at 007 without an override registration. The remedy is reconciliation between suite contract and methodology, plus retroactive annotation at 007 to register the reversal.
3. **Cost-rationality reading.** The "at most two" cap forced a criterion choice; the criterion choice in turn excluded `Stella` alongside other concurrent grounds (`007/FINDINGS.md`'s "proxy-heavy," 004's "thinnest evidence case," 006's "ambiguous" tag). The remedy is enumerative discipline: when a decision is load-bearing, list the concurrent grounds, not the highlighted one.

These are not the same finding. Each implies different downstream actions. The next deliberation composition step should let all three readings shape the response rather than collapse them into one.

#### A retraction the chain itself contains

Finding 2 above claims the configuration-vs-family slippage "runs through the whole chain." The pressure pass's own 006 analysis classifies 006's treatment as honest deferral. 006 is therefore a counter-example to its own chain-wide claim, not an instance of it. This is not something the reviews need to demonstrate; the pressure pass demonstrates it against itself. What survives is local: `008/DESIGN.md` uses "configuration" and family-name interchangeably, and the comparison surface is asymmetric (incumbent specified at model+retrieval; challengers as families only). That asymmetry has reproducibility implications. The remedy is a `008/DESIGN.md` preamble paragraph, not a structural reframe.

#### Reading distance, register, and visibility

Cross-vendor flagged a few overstatements briefly. Opus adversarial enumerated thirteen specific sentences. The same-vendor reader caught Anthropic-internal rhetorical patterns — all-caps emphasis, "load-bearing" as label, `Forces:` prescriptive consequences — more readily than the cross-vendor reader did. Cross-vendor saw substance more readily than register; Opus adversarial saw register more readily than substance. The pair caught more together than either would have alone. This is itself worth recording as a methodology observation: paired reviews of different vendor stances appear to catch different categories of failure.

#### Self-application

The pressure pass exhibits the same closure pressure the parent deliberation diagnosed in the spike suite. Persuasive framing in lieu of argument; prescriptive remedies overrunning their diagnostic grounds; calibrated language reserved for a closing footnote rather than running through the prose. The deliberation's addendum already warned about this in advance: *"if a future addition to this addendum collapses [the dimensional frame], that collapse should itself be flagged."* The pressure pass collapsed it; the paired review surfaced the collapse; this section flags it.

### What this implies for the next step

Composition in [`sequential-narrowing-anti-regret-and-spike-inference-limits.md`](../../deliberations/sequential-narrowing-anti-regret-and-spike-inference-limits.md) should:

- Hold the three Finding 1 readings rather than picking one. Each implies remedy-cells in different parts of the dimensional space (template vs document-discipline vs enumerative-discipline). Letting them coexist is the methodology's stance.
- Localise Finding 2's remedy to `008/DESIGN.md`'s preamble plus an asymmetric-comparison-surface fix. The chain-wide framing does not survive its own internal logic and should not propagate.
- Re-examine the pressure pass's Findings 5 and 7 with the overstep audit's lens. Finding 5 (Qwen3 chain dependency) treats absence of *new* pre-registration as absence of pre-registration; Finding 7 (narrow-at-each-step pathologization) treats methodologically required asymmetry as evidential bias. Both are out of formal scope for the paired review but visible in the same pattern.
- Adopt calibrated language as standard, not exceptional. The pressure pass's confidence-calibration section conceded its framings might be wrong but did not retire the rhetorically loaded vocabulary. Calibration that does not propagate to register is not calibration.

The original Recommendation above (compose Findings 1, 2, and 4 as tactical / methodological work) stands as a record of what was concluded before the paired review. It is not the operative direction now; this section is.

The pressure pass remains as written. The reviews remain at their linked paths. This section is a third reading, layered on top.
