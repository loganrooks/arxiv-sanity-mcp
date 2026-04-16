# Spike Design Review Spec

Reusable task specification for independent review of a spike design or spike suite before execution.

## Purpose

Use this spec when asking an external reviewer or another agent to review spike planning artifacts for structural weaknesses before execution.

The reviewer should test whether the design:

- asks a clear question,
- operationalizes its own evidence contract,
- preserves the project's product values,
- keeps open questions visible,
- avoids premature closure,
- and is likely to produce findings that are interpretable rather than merely busy.

The goal is not to rewrite the spike. The goal is to identify the highest-severity problems that would make execution misleading, inconclusive, or falsely decisive.

## Required Inputs

Provide the reviewer with:

- the target spike or suite design files
- [SPIKE-DESIGN-PRINCIPLES.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/SPIKE-DESIGN-PRINCIPLES.md)
- [METHODOLOGY.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/.planning/spikes/METHODOLOGY.md)
- relevant prior spike findings, decisions, open questions, and pre-spike analyses
- the core project docs that define values and evaluation posture:
  - [docs/01-project-vision.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/01-project-vision.md)
  - [docs/02-product-principles.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/02-product-principles.md)
  - [docs/05-architecture-hypotheses.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/05-architecture-hypotheses.md)
  - [docs/08-evaluation-and-experiments.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/08-evaluation-and-experiments.md)
  - [docs/10-open-questions.md](/home/rookslog/workspace/projects/arxiv-sanity-mcp/docs/10-open-questions.md)
- any explicit user instructions that constrain the review

## Reviewer Role

Review as an independent critic, not as the author.

Assume the design may be articulate about its own risks while still failing to operationalize them. Prefer checking executable commitments over praising self-awareness.

## Review Standards

Evaluate the target against these standards:

1. **Scope clarity**
   - Is the spike question precise?
   - Is it clear what the spike does not answer?

2. **Evidence-contract coherence**
   - Does the executable protocol actually support the kinds of claims the design says it will make?
   - Are the required metrics, reviews, gates, and comparisons actually present?

3. **Framework-awareness**
   - Are entanglements in the evaluation frame named and operationalized rather than merely acknowledged?
   - Are auxiliary assumptions varied where the claims depend on them?

4. **Project-value alignment**
   - Does the design preserve discovery over overload, explicit steerability, explainability, provenance, and cost-awareness?
   - Does it avoid hidden architectural foreclosure?

5. **Interpretation discipline**
   - Does the design separate representational difference, mechanistic explanation, and function-in-use?
   - Does it preserve room for inconclusive outcomes?

6. **Execution-readiness**
   - Are failure modes, branch conditions, and blocking gates concrete enough to be enforceable?
   - Would two different executors likely run materially similar protocols from this design?

## Epistemic Language

When characterizing findings or support, use the repo's current epistemic schema:

- `source-traceable`
- `artifact-reported`
- `derived`
- `interpretive`
- `chosen for now`
- `open`

Do not use bare `grounded` as the main epistemic label.

## Output Format

Return findings first, ordered by severity.

Include:

1. **Verdict**
   - `ready`
   - `revise-before-execution`
   - `blocked`

2. **Findings**
   - each finding should include:
     - short title
     - severity: `blocker`, `major`, `notable`, or `minor`
     - why it matters
     - concrete file references
     - minimal corrective direction

3. **Open assumptions**
   - only if needed for interpreting the findings

4. **Brief strengths**
   - optional and short
   - only after findings

If there are no findings, say so explicitly and then name the residual risks.

## What To Look For Specifically

Pay particular attention to these failure modes:

- the design says one thing but the protocol tests another
- metrics are present but not matched to the claim type
- qualitative review is mentioned but not structurally required
- prior credences or probability-shift targets are absent
- handoff terms like `survive`, `shortlist`, or `live` are used without operational outputs
- a baseline or incumbent is rhetorically displaced without direct comparison
- framework dependence is named but not varied
- mechanism stories are asserted before the design has isolated them
- task-based claims are made from list-based evidence
- a task harness is deferred to execution time instead of pre-registered
- human absence is acknowledged but no concrete evaluator-plurality gate follows
- human absence is acknowledged but the design still talks as if researcher value is settled
- open questions are silently closed by design wording

## What Not To Do

- Do not rewrite the design wholesale.
- Do not turn the review into an execution plan.
- Do not reward sophistication of language over protocol quality.
- Do not treat a citation or file reference as equivalent to validation.
- Do not close unresolved product questions without explicit authority.

## Copyable Prompt Frame

Use this when handing the spec to another system:

> Review the provided spike design artifacts using `SPIKE-DESIGN-REVIEW-SPEC.md`.
> Findings first, ordered by severity.
> Focus on structural weaknesses, epistemic slippage, hidden assumptions, sequencing errors, and missing gates.
> Use the repo's epistemic schema (`source-traceable`, `artifact-reported`, `derived`, `interpretive`, `chosen for now`, `open`).
> Prefer concrete file references and minimal corrective direction over long summaries.
