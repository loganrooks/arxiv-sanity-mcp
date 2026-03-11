---
phase: foundation-fixes
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - alembic/versions/005_drop_signal_type_check.py
  - alembic/versions/006_enrichment_composite_pk.py
  - src/arxiv_mcp/db/models.py
  - src/arxiv_mcp/enrichment/service.py
  - src/arxiv_mcp/enrichment/cli.py
  - src/arxiv_mcp/interest/ranking.py
  - src/arxiv_mcp/config.py
  - src/arxiv_mcp/enrichment/openalex.py
  - tests/test_interest/test_ranking.py
  - docs/10-open-questions.md
  - .planning/REQUIREMENTS.md
  - AGENTS.md
autonomous: true
must_haves:
  truths:
    - "New signal types can be added without a DB migration"
    - "Multiple enrichment sources can store data for the same paper"
    - "Marking one paper as negative does NOT demote all papers sharing its categories"
    - "OpenAlex polite pool access is configurable via openalex_email setting"
    - "Open Questions Q1, Q4, Q16 annotated as provisionally resolved"
    - "Provisional requirements annotated with [chosen for now] markers"
  artifacts:
    - path: "alembic/versions/005_drop_signal_type_check.py"
      provides: "Migration to drop ck_signal_type_valid CHECK constraint"
    - path: "alembic/versions/006_enrichment_composite_pk.py"
      provides: "Migration to change paper_enrichments PK to (arxiv_id, source_api)"
    - path: "src/arxiv_mcp/interest/ranking.py"
      provides: "apply_negative_demotion with direct ID matching only"
    - path: "src/arxiv_mcp/config.py"
      provides: "openalex_email setting"
  key_links:
    - from: "src/arxiv_mcp/enrichment/service.py"
      to: "src/arxiv_mcp/db/models.py"
      via: "composite PK lookups and upserts"
      pattern: "session\\.get\\(PaperEnrichment.*\\(arxiv_id.*source_api\\)"
    - from: "src/arxiv_mcp/enrichment/openalex.py"
      to: "src/arxiv_mcp/config.py"
      via: "mailto parameter from settings.openalex_email"
      pattern: "mailto.*openalex_email"
---

<objective>
Fix six foundation issues identified by the epistemic audit (FINDINGS.md items I1, I3, I4, I6 plus documentation I5-related annotations).

Purpose: Remove hardcoded constraints that block extensibility (signal types, enrichment sources), fix an ADR-0001-violating implicit inference (category-based negative demotion), add missing config (openalex_email), and annotate provisional decisions in documentation.

Output: Two Alembic migrations, updated service/ranking code, updated config, and annotated documentation.
</objective>

<execution_context>
@./.claude/get-shit-done/workflows/execute-plan.md
@./.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@.planning/foundation-audit/FINDINGS.md
@CLAUDE.md
@AGENTS.md

<interfaces>
<!-- Key types and contracts the executor needs. -->

From src/arxiv_mcp/db/models.py:
```python
class PaperEnrichment(Base):
    __tablename__ = "paper_enrichments"
    arxiv_id: Mapped[str] = mapped_column(String(20), ForeignKey("papers.arxiv_id", ondelete="CASCADE"), primary_key=True)
    source_api: Mapped[str] = mapped_column(String(32), default="openalex")
    # ... other columns
    __table_args__ = (
        CheckConstraint("status IN ('success', 'not_found', 'partial', 'error')", name="ck_enrichment_status_valid"),
        Index("idx_enrichments_status", "status"),
        Index("idx_enrichments_enriched_at", "enriched_at"),
    )

class InterestSignal(Base):
    __tablename__ = "interest_signals"
    signal_type: Mapped[str] = mapped_column(String(32), nullable=False)
    __table_args__ = (
        CheckConstraint("signal_type IN ('seed_paper', 'saved_query', 'followed_author', 'negative_example')", name="ck_signal_type_valid"),
        # ...
    )
```

From src/arxiv_mcp/interest/signals.py:
```python
VALID_SIGNAL_TYPES = {"seed_paper", "saved_query", "followed_author", "negative_example"}
```

From src/arxiv_mcp/enrichment/service.py:
```python
async def _upsert_enrichment(self, session, arxiv_id, result, now):
    # Uses pg_insert ON CONFLICT on index_elements=["arxiv_id"]

async def get_enrichment_status(self, arxiv_id: str) -> PaperEnrichment | None:
    return await session.get(PaperEnrichment, arxiv_id)

async def _filter_cooldown(self, session, arxiv_ids, refresh):
    # Queries PaperEnrichment.arxiv_id.in_(arxiv_ids)
```

From src/arxiv_mcp/interest/ranking.py:
```python
def apply_negative_demotion(scores, paper, profile_context):
    # Currently checks: paper.arxiv_id in negative_ids OR bool(paper_cats & negative_categories)
    # Should ONLY check: paper.arxiv_id in negative_ids

class ProfileContext:
    negative_papers: list[PaperSummary]
    negative_categories: set[str]  # This field will become unused
```

From src/arxiv_mcp/config.py:
```python
class Settings(BaseSettings):
    openalex_api_key: str = ""
    openalex_api_url: str = "https://api.openalex.org"
    enrichment_rate_limit: float = 5.0
    # Missing: openalex_email
```

From src/arxiv_mcp/enrichment/openalex.py:
```python
class OpenAlexAdapter:
    def __init__(self, settings: Settings):
        # Currently uses hardcoded User-Agent: "arxiv-mcp/0.1.0"
        # Should add mailto param when openalex_email is set
```
</interfaces>
</context>

<tasks>

<task type="auto">
  <name>Task 1: Schema migrations (drop signal_type CHECK, composite enrichment PK)</name>
  <files>
    alembic/versions/005_drop_signal_type_check.py
    alembic/versions/006_enrichment_composite_pk.py
    src/arxiv_mcp/db/models.py
    src/arxiv_mcp/enrichment/service.py
    src/arxiv_mcp/enrichment/cli.py
  </files>
  <action>
**Migration 005 — Drop signal_type CHECK constraint (I1):**

Create `alembic/versions/005_drop_signal_type_check.py` (hand-written, revision="005", down_revision="004"). Follow the established migration conventions (see 001-004).

- `upgrade()`: `op.drop_constraint("ck_signal_type_valid", "interest_signals", type_="check")`
- `downgrade()`: Re-create the CHECK constraint with the original 4 types.

Update `src/arxiv_mcp/db/models.py` InterestSignal `__table_args__`: Remove the `CheckConstraint("signal_type IN (...)", name="ck_signal_type_valid")` entry. Leave the status CHECK constraint, UniqueConstraint, and Index intact. Add a comment: `# signal_type validated at application level (signals.py VALID_SIGNAL_TYPES)`. Do NOT change VALID_SIGNAL_TYPES in signals.py -- that stays as the application-level validation.

**Migration 006 — Composite enrichment PK (I4):**

Create `alembic/versions/006_enrichment_composite_pk.py` (revision="006", down_revision="005").

- `upgrade()`:
  1. Drop the two existing indexes first: `op.drop_index("idx_enrichments_status")`, `op.drop_index("idx_enrichments_enriched_at")`
  2. Drop old PK: `op.drop_constraint("paper_enrichments_pkey", "paper_enrichments", type_="primary")`
  3. Create new composite PK: `op.create_primary_key("paper_enrichments_pkey", "paper_enrichments", ["arxiv_id", "source_api"])`
  4. Re-create the two indexes: `op.create_index("idx_enrichments_status", "paper_enrichments", ["status"])`, `op.create_index("idx_enrichments_enriched_at", "paper_enrichments", ["enriched_at"])`
- `downgrade()`: Reverse — drop indexes, drop composite PK, create single-column PK on arxiv_id, re-create indexes. Note: downgrade may fail if multiple source_api records exist per arxiv_id. Add a comment noting this.

Update `src/arxiv_mcp/db/models.py` PaperEnrichment:
- Change `arxiv_id` mapped_column: keep `ForeignKey("papers.arxiv_id", ondelete="CASCADE")` but remove `primary_key=True`
- Change `source_api` mapped_column: keep `String(32)`, keep `default="openalex"`, remove `nullable=False` (no longer needed — PK columns are implicitly NOT NULL)
- Add `__table_args__` with `PrimaryKeyConstraint("arxiv_id", "source_api", name="paper_enrichments_pkey")` in addition to existing CheckConstraint and Indexes. Import `PrimaryKeyConstraint` from sqlalchemy.

Update `src/arxiv_mcp/enrichment/service.py`:
- `enrich_paper()` line 74: Change `await session.get(PaperEnrichment, arxiv_id)` to `await session.get(PaperEnrichment, (arxiv_id, self.adapter.adapter_name))` (composite PK lookup).
- `get_enrichment_status()` line 193: Change `await session.get(PaperEnrichment, arxiv_id)` to use a select query: `select(PaperEnrichment).where(PaperEnrichment.arxiv_id == arxiv_id, PaperEnrichment.source_api == "openalex")` — or better, add an optional `source_api` parameter defaulting to `"openalex"` and use `session.get(PaperEnrichment, (arxiv_id, source_api))`.
- `_upsert_enrichment()` line 283: Change `on_conflict_do_update(index_elements=["arxiv_id"], ...)` to `on_conflict_do_update(index_elements=["arxiv_id", "source_api"], ...)`. Update the `update_cols` exclusion to filter out both "arxiv_id" and "source_api".
- `_filter_cooldown()`: The existing query `PaperEnrichment.arxiv_id.in_(arxiv_ids)` is still correct for cooldown — if ANY source enriched recently, skip. No change needed here.

Update `src/arxiv_mcp/enrichment/cli.py`:
- Find the `get_enrichment_status` call (line 292) and update if its signature changed (add source_api param).
  </action>
  <verify>
    <automated>cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && conda run -n arxiv-mcp python -m pytest tests/test_enrichment/ tests/test_interest/test_profiles.py -x -q 2>&1 | tail -20</automated>
  </verify>
  <done>
    - Migration 005 drops ck_signal_type_valid CHECK constraint; downgrade restores it
    - Migration 006 changes paper_enrichments PK to (arxiv_id, source_api); downgrade reverses
    - ORM model matches new schema (no signal_type CHECK in InterestSignal, composite PK in PaperEnrichment)
    - All enrichment service queries use composite PK for lookups
    - All upserts use both columns in ON CONFLICT
    - Existing tests pass (or are updated to match new composite PK)
  </done>
</task>

<task type="auto">
  <name>Task 2: Remove category-based negative demotion, add openalex_email config</name>
  <files>
    src/arxiv_mcp/interest/ranking.py
    tests/test_interest/test_ranking.py
    src/arxiv_mcp/config.py
    src/arxiv_mcp/enrichment/openalex.py
  </files>
  <action>
**Fix I3 — Remove category-based negative demotion:**

In `src/arxiv_mcp/interest/ranking.py`, function `apply_negative_demotion` (line 371):

Change the `is_negative` check from:
```python
is_negative = (
    paper.arxiv_id in negative_ids
    or bool(paper_cats & profile_context.negative_categories)
)
```
to:
```python
is_negative = paper.arxiv_id in negative_ids
```

Remove the `paper_cats` variable (no longer needed). Remove the early return check for `profile_context.negative_categories` — only check `profile_context.negative_papers`. The function should now be:
```python
def apply_negative_demotion(scores, paper, profile_context):
    if not profile_context.negative_papers:
        return
    negative_ids = {p.arxiv_id for p in profile_context.negative_papers}
    if paper.arxiv_id not in negative_ids:
        return
    demotion_factor = 1.0 - profile_context.negative_weight
    for score in scores:
        score.weighted_score *= demotion_factor
```

Add a comment: `# Direct ID matching only — category-based demotion removed per ADR-0001 (exploration-first)`

Do NOT remove `negative_categories` from `ProfileContext` dataclass — it may be used elsewhere and removal is a separate concern. Just stop using it in `apply_negative_demotion`.

Update `tests/test_interest/test_ranking.py` TestNegativeDemotion:

- `test_demotion_applied` (line 266): This test uses `arxiv_id="neg-paper"` which matches a negative paper ID directly. It should still pass. But remove `negative_categories={"cs.CL"}` from the context to be clear the test exercises direct ID matching. (Keep it if you want to prove categories are ignored.)
- Add a new test `test_category_overlap_does_not_trigger_demotion`: Create a paper with categories overlapping negative_categories but whose arxiv_id is NOT in negative_papers. Assert scores are NOT demoted. This is the key regression test for I3.
  ```python
  def test_category_overlap_does_not_trigger_demotion(self):
      """Category overlap with negative papers should NOT trigger demotion (ADR-0001)."""
      paper = _make_paper(arxiv_id="innocent-paper", category_list=["cs.CL"])
      ctx = _make_profile_context(
          negative_papers=[_make_paper(arxiv_id="neg-paper", category_list=["cs.CL"])],
          negative_categories={"cs.CL"},
          negative_weight=0.5,
      )
      scores = [
          SignalScore(
              signal_type=SignalType.QUERY_MATCH,
              raw_score=0.8, normalized_score=0.8,
              weight=0.35, weighted_score=0.28,
              explanation="test",
          ),
      ]
      apply_negative_demotion(scores, paper, ctx)
      # Score should be unchanged — category overlap alone does not trigger demotion
      assert scores[0].weighted_score == pytest.approx(0.28)
  ```

**Fix I6 — Add openalex_email config:**

In `src/arxiv_mcp/config.py`, add to the Settings class in the "Enrichment settings" section:
```python
openalex_email: str = ""  # Set for OpenAlex polite pool (10 req/s vs 1 req/s anonymous)
```

In `src/arxiv_mcp/enrichment/openalex.py`, update `OpenAlexAdapter`:
- In the `_build_params` method (line 101): After the existing api_key check, add:
  ```python
  if self._settings.openalex_email:
      params["mailto"] = self._settings.openalex_email
  ```
- In the `resolve_ids` and `enrich` methods: Update the `headers` dict in `httpx.AsyncClient` to include the email in the User-Agent if set:
  ```python
  user_agent = "arxiv-mcp/0.1.0"
  if self._settings.openalex_email:
      user_agent += f" (mailto:{self._settings.openalex_email})"
  ```
  Use this `user_agent` in the `headers={"User-Agent": user_agent}` parameter. This follows OpenAlex polite pool conventions.
  </action>
  <verify>
    <automated>cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && conda run -n arxiv-mcp python -m pytest tests/test_interest/test_ranking.py tests/test_enrichment/test_models.py -x -q 2>&1 | tail -20</automated>
  </verify>
  <done>
    - apply_negative_demotion only matches exact arxiv_id, never category overlap
    - New test proves category-only overlap does NOT trigger demotion
    - Settings.openalex_email exists with empty string default
    - OpenAlexAdapter sends mailto param and updated User-Agent when email is configured
    - All ranking and enrichment model tests pass
  </done>
</task>

<task type="auto">
  <name>Task 3: Documentation annotations (open questions, requirements provenance, CONTEXT.md discipline)</name>
  <files>
    docs/10-open-questions.md
    .planning/REQUIREMENTS.md
    AGENTS.md
  </files>
  <action>
**Annotate Open Questions Q1, Q4, Q16:**

In `docs/10-open-questions.md`, add a status annotation after the heading of each resolved question:

For Q1 (line 8, "## 1. What is the right default notion of interest state?"):
Add immediately after the heading line:
```
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: four signal types (seed_paper, saved_query, followed_author, negative_example). Signal type set is now application-validated, not DB-constrained, allowing future extension without migration. See FINDINGS.md I1, I5.
```

For Q4 (line 27, "## 4. Which external enrichments are worth the dependency cost?"):
Add immediately after the heading line:
```
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: OpenAlex as sole enrichment source (demand-driven, not bulk). Schema now supports composite PK (arxiv_id, source_api) for multi-source extensibility. See FINDINGS.md I4, I5.
```

For Q16 (line 97, "## 16. What is the right processing intensity promotion strategy?"):
Add immediately after the heading line:
```
> **Status: Resolved during implementation (pending user validation)**
> Implementation chose: demand-driven promotion only (enrich when user/agent touches the paper). Budget-constrained and cohort-based strategies remain viable future options. See FINDINGS.md I5.
```

**Annotate provisional requirements in REQUIREMENTS.md:**

For each of these requirements, add a `[chosen for now]` marker after the requirement ID:

- CONT-05 (line 73): Change from `- [ ] **CONT-05**:` to `- [ ] **CONT-05** [chosen for now]:` and append to the end of the line: ` (source says "working hypothesis" -- one backend behind extensible interface may suffice for v1)`
- INTR-04 (line 50): Change from `- [x] **INTR-04**:` to `- [x] **INTR-04** [chosen for now]:` and append: ` (source says "possible" signal type)`
- INTR-05 (line 51): Change from `- [x] **INTR-05**:` to `- [x] **INTR-05** [chosen for now]:` and append: ` (source says "possible" signal type)`
- MCP-05 (line 82): Change from `- [ ] **MCP-05**:` to `- [ ] **MCP-05** [chosen for now]:` and append: ` (source lists as examples, not deliverables; open question whether prompts are reusable)`
- MCP-07 (line 84): Change from `- [ ] **MCP-07**:` to `- [ ] **MCP-07** [chosen for now]:` and append: ` (no traceable source; sensible heuristic but not a firm requirement)`

**Add CONTEXT.md epistemic discipline section to AGENTS.md:**

At the end of AGENTS.md (after the "Definition of success for early agents" section), add:

```markdown

## CONTEXT.md epistemic discipline

When creating or updating CONTEXT.md files for phase planning:

### Separate grounded decisions from inferences
- **Grounded**: Decision traceable to a specific passage in user-authored docs (01-11), an accepted ADR, or explicit user instruction. Cite the source.
- **Inferred**: Decision made by AI based on patterns, analogies, or judgment. Mark explicitly as `[inferred]` or `[chosen for now]` with reasoning.
- **Never** present an inference as if it were grounded.

### Do not close Open Questions without authority
- Items in `docs/10-open-questions.md` are **intentionally unresolved** by the user.
- An AI agent may **propose** an answer (mark as `[chosen for now]`) but must not silently adopt it as settled.
- Closing an Open Question requires: user confirmation, or a new ADR with explicit rationale.
- If implementation requires choosing an answer, document it as provisional and flag for user review.

### ADR citations must be specific
- When citing an ADR to justify a decision, quote the specific clause or principle that applies.
- Do not cite an ADR number alone as blanket authority for decisions the ADR does not address.
- Example: "ADR-0001 states 'multiple retrieval/ranking strategies must coexist' -- this means..." not just "per ADR-0001."

### No speculative product strategy
- CONTEXT.md files describe implementation decisions, not business models or monetization.
- Product strategy (pricing, donation models, growth) is out of scope unless the user introduces it.
```
  </action>
  <verify>
    <automated>cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && grep -c "pending user validation" docs/10-open-questions.md && grep -c "chosen for now" .planning/REQUIREMENTS.md && grep -c "epistemic discipline" AGENTS.md</automated>
  </verify>
  <done>
    - Q1, Q4, Q16 in docs/10-open-questions.md each have "Resolved during implementation (pending user validation)" annotations with what was chosen
    - CONT-05, INTR-04, INTR-05, MCP-05, MCP-07 in REQUIREMENTS.md annotated with [chosen for now] and provenance notes
    - AGENTS.md has new "CONTEXT.md epistemic discipline" section with rules for grounded vs inferred decisions, Open Question closure, ADR citation specificity, and no speculative product strategy
  </done>
</task>

</tasks>

<verification>
After all three tasks, run the full test suite to confirm no regressions:

```bash
cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && conda run -n arxiv-mcp python -m pytest -x -q 2>&1 | tail -20
```

Then verify migrations are syntactically valid:

```bash
cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && conda run -n arxiv-mcp python -c "import alembic.versions" 2>&1 || echo "OK if import fails -- just check files parse"
conda run -n arxiv-mcp python -c "
import ast
for f in ['alembic/versions/005_drop_signal_type_check.py', 'alembic/versions/006_enrichment_composite_pk.py']:
    ast.parse(open(f).read())
    print(f'{f}: valid Python')
"
```
</verification>

<success_criteria>
1. Migrations 005 and 006 exist, are syntactically valid, and follow project conventions
2. InterestSignal ORM model has no signal_type CHECK constraint; VALID_SIGNAL_TYPES in signals.py unchanged
3. PaperEnrichment has composite PK (arxiv_id, source_api) in both ORM and migration
4. All session.get(PaperEnrichment, ...) calls use composite key tuples
5. apply_negative_demotion uses direct ID matching only -- new test proves category overlap alone is insufficient
6. Settings.openalex_email exists; OpenAlexAdapter sends mailto when configured
7. Three Open Questions annotated as provisionally resolved
8. Five requirements annotated with [chosen for now] provenance markers
9. AGENTS.md has epistemic discipline section
10. Full test suite passes
</success_criteria>

<output>
After completion, create `.planning/quick/1-foundation-fixes-extensible-schemas-remo/1-SUMMARY.md`
</output>
