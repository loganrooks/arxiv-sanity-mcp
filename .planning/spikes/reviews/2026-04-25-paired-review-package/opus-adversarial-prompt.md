---
type: review-prompt
audience: Claude Opus 4.7 (fresh session, separate from the pressure-pass author's session)
phase: adversarial steelman
output_target: .planning/spikes/reviews/2026-04-25-pressure-pass-opus-adversarial.md
---

# Opus Adversarial Prompt — Steelman the Opposite Framing

## Your role

A previous Claude Opus session wrote a "pressure pass" on a research project's spike handoffs. The pressure pass identified seven findings. Findings 3 through 7 are template / contract / direct-reading observations and are not in scope here. **Findings 1 and 2 are framing claims** — about whether certain choices were load-bearing-but-unflagged or merely implicitly understood — and the previous session itself flagged these as the most contestable findings in the pass.

Your job is **adversarial**. You are not asked to confirm or deny. You are asked to write the strongest possible argument that Findings 1 and 2 are *wrong* or *substantially overstated*, and to identify any rhetorical or evidential moves in the pressure pass that overstep.

This is a paired review. A cross-vendor reviewer is doing an independent reading of the underlying artifacts in parallel. Your role is the *attack on the argument structure*, not an independent reading. **You should read the pressure pass and engage with it directly.**

## Read

In this order:

1. The pressure pass: `.planning/spikes/reviews/2026-04-25-handoff-pressure-pass.md`
2. The underlying handoffs and design (so your attack is grounded, not just rhetorical):
   - `.planning/spikes/005-evaluation-framework-robustness/HANDOFF.md`
   - `.planning/spikes/006-model-retrieval-interactions/HANDOFF.md`
   - `.planning/spikes/007-training-data-mechanism-probes/HANDOFF.md`
   - `.planning/spikes/NEXT-ROUND-SUITE.md`
   - `.planning/spikes/008-function-in-use-and-blind-spots/DESIGN.md`
3. Working vocabulary (light skim if needed):
   - `.planning/spikes/METHODOLOGY.md`
   - `.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md`

You may also skim `FINDINGS.md` / `POSTERIOR.md` / `DECISION.md` from any 005/006/007 directory if needed.

## Your task

For each of Findings 1 and 2 in the pressure pass, write the strongest case that the finding is wrong, overstated, or based on a misreading. Genuine adversarial work, not a steelman wrapped around a confirmation.

### Finding 1 — pressure pass claim

> "Mechanism-support > complementarity is a load-bearing stance choice that is not labeled as one. It is the single decision excluding `Stella` from `008`. Not pre-registered in `NEXT-ROUND-SUITE.md`, not argued from evidence in 007. Reclassifying it as a *contested choice* changes the program substantively."

**Adversarial frames you should explore:**

- *The implicit-norm read.* `METHODOLOGY.md` and `SPIKE-DESIGN-PRINCIPLES.md` may already commit the program to mechanism-backed reasoning as the canonical narrowing posture. If so, 007's choice is not a "stance choice" — it is the methodology's default applied. The pressure pass's "load-bearing-but-unflagged" framing would then be a category error.
- *The Counter-Reading-is-the-flag read.* 007's Counter-Reading section *explicitly* names the alternative criterion (complementarity) and *explicitly* says why it is not chosen. That is structurally identical to flagging the stance choice. The pressure pass treats the Counter-Reading as evidence that the stance was unflagged; an opposite read is that the Counter-Reading is exactly the flagging that the methodology requires.
- *The chain-coherence read.* `005`, `006`, `007` each defer or weaken candidates on different evidence types. Mechanism-support is not introduced *de novo* at 007; it is the kind of evidence that 007 was specifically designed to test. Choosing the gate that matches the spike's purpose is not a stance choice. It is the spike doing its job.
- *The cost-rationality read.* The "evaluation cost" mentioned in 007's Counter-Reading is a real constraint. If the program-level cost budget makes "no more than two challengers in 008" non-negotiable, the question is not *whether* to narrow but *on what criterion*. Mechanism-support is at minimum defensible. The pressure pass treats the criterion choice as central; from this angle, the criterion choice is downstream of the budget.

Pick whichever frame(s) you find genuinely defensible and argue them. You may also propose adversarial frames the prompt has not anticipated.

### Finding 2 — pressure pass claim

> "Configuration-vs-family slippage runs through the whole chain. 005 evaluates families; 006 honestly defers configuration-level questions; 007 narrows on family; `008` evaluates 'configurations' but uses family names. The configuration question is never directly answered yet `008` is asking for that answer."

**Adversarial frames you should explore:**

- *The register-not-substance read.* "Configuration" and "family" may be different registers of the same object in this program's vocabulary. `MiniLM + TF-IDF` is shorthand for the incumbent default configuration; `SPECTER2` is shorthand for the family's canonical configuration tested in the prior round. The pressure pass's "slippage" reading depends on treating these terms as substantively different — but if the program treats canonical-family-configuration as the unit, there is no slippage, only register variation that careful reading absorbs without error.
- *The deferred-not-elided read.* 006 *explicitly defers* model-specific `kNN` configuration to a possible future re-entry into 008. The pressure pass treats this deferral as part of the slippage evidence; an opposite read is that the deferral is exactly the methodology's auxiliary-aware discipline working as intended. You cannot test everything; you defer cleanly. Naming the deferred question is not slippage — it is principled bracketing.
- *The wrong-question read.* The configuration-level question is not what `008` is asking. `008` is asking which families help research tasks at the function-in-use layer. Whether the family is best operationalised by one configuration or by ten is a Round-2 question, not a Round-1 question. The pressure pass conflates "the program does not currently answer the configuration question" with "`008` is asking the wrong question."
- *The substitutability read.* If, within a family, the configuration choice is locally consequential but globally substitutable (i.e., any reasonable `SPECTER2` configuration would behave similarly at the function-in-use layer), then the family-as-configuration shorthand is empirically warranted, not slippage.

### Pressure-pass overstep audit

Independent of Findings 1 and 2 *as a whole*, scan the pressure pass for specific moves that overstep:

- Sentences where the pass draws a stronger conclusion than the textual evidence supports.
- Places where the pass treats absence of evidence as evidence of absence.
- Places where the pass labels a choice "load-bearing" without showing the load it bears.
- Places where the pass uses persuasive framing ("CRITICAL," "load-bearing," "highest-impact") in lieu of argument.
- Places where the pass's confidence-calibration section underplays its own contestable framing.

Quote the specific sentences. Be unsparing.

## Output format

```
# Opus Adversarial Pass — Findings 1 and 2

## Adversarial argument against Finding 1

[Your strongest case. Multiple paragraphs. Use the frames above or invent new ones. Cite artifacts. Be willing to land on "Finding 1 is roughly half right; here is what survives and what does not."]

## Adversarial argument against Finding 2

[Same shape.]

## Pressure-pass overstep audit

[Numbered list of specific sentences that overstep, with the overstep named for each.]

## Net effect

[One paragraph: even after your adversarial work, what survives of Findings 1 and 2? You may conclude the original framing fully survives, partly survives, or does not survive. Honesty over performance.]

## Steelman residue

[If the adversarial frames are weaker than they look on first writing — say so explicitly. The point is to *test* Findings 1 and 2, not to defeat them rhetorically.]
```

## Norms for this review

- **Adversarial, not contrarian.** The goal is to find the strongest objections, not to disagree for its own sake. If the strongest adversarial argument is still weak, name it as weak.
- **Cite the artifacts.** Specific quotes from the handoffs / designs / methodology documents are more useful than abstract claims about how spike methodology "should" work.
- **Acknowledge what you cannot defeat.** If part of Finding 1 or Finding 2 survives every frame you can construct, name what survives — that is the most useful possible output.
- **Match Anthropic-internal-and-external register.** The previous Opus session may have produced rhetoric that reads compellingly to a same-vendor reader. Be alert to this and discount it where appropriate.
- **No new findings.** Stay focused on Findings 1 and 2 and the overstep audit. Do not generate new findings; if you notice something else, mention it briefly under "Net effect" and stop.
