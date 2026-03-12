# Phase 5 Context: MCP Validation & Iteration

**Date:** 2026-03-12
**Source:** Ecosystem commentary analysis (`.planning/ECOSYSTEM-COMMENTARY.md`), Phase 04.1 verification results, doc 06 open questions

---

## User Decisions

### 1. Phase 5 Is Qualitatively Different From Prior Phases

Phases 1-4 + 04.1 built features. Phase 5 validates them with real workflows and iterates. This means:
- The primary activity is **using the MCP**, not building new code
- Evidence from real usage drives design decisions — not speculation
- The MCP surface will change based on what works and what doesn't
- Prompts are designed through practice, not theorized in advance

### 2. First Validation Dataset: arxiv-scan Import

The arxiv-scan pipeline (`/scratch/arxiv-scan/`) produced data that should bootstrap the first real MCP usage:

| Data | Source File | MCP Target | Import Action |
|------|------------|------------|---------------|
| 154 analyzed papers | `pipeline/reading/paper-analyses/*.json` | Paper metadata + triage states | Ingest via arXiv API, set triage states from value scores (shortlisted ≥7, seen ≤6) |
| 10 tension definitions | `pipeline/evaluation-guidelines.md` | Interest profile signals | Create profile with tension vocabulary as seed signals |
| 1,211 triage decisions | `pipeline/triage/final-selection.json` | Bulk triage import | Validate MCP ranking against known human decisions |
| 4 known false negatives | `pipeline/excluded-paper-audit.md` | Ranking validation | Test whether MCP ranking surfaces them without being told |
| Thematic synthesis | `pipeline/synthesis/thematic-*.md` | Profile description | Natural language scope statement for interest profiles |
| Citation/influence data | `pipeline/full-citation-data.json` | OpenAlex enrichment | Compare MCP enrichment against known citation counts |

**Import strategy:** Write a one-time import script that:
1. Ingests the 154 papers via arXiv API (metadata substrate)
2. Sets triage states from paper-index value scores
3. Creates an interest profile from arxiv-scan's tension vocabulary
4. Enriches top papers via OpenAlex for citation data
5. Runs ranking against imported papers to compare MCP ranking vs arxiv-scan human ranking
6. Tests whether `find_related_papers` with known seeds surfaces the 4 false negatives

### 3. Doc 06 Open Questions to Resolve

From `docs/06-mcp-surface-options.md` §10, these questions need evidence-based answers:

| Question | Current Status | How Phase 5 Resolves It |
|----------|---------------|------------------------|
| How much workflow state belongs in v1? | **Answered in code** — full workflow tools shipped in Phase 04.1 (triage, collections, watches, signals) | Validate that agents actually use all workflow tools. If some are never called, simplify. |
| Should interest profiles exist before collections, or vice versa? | **Answered in code** — both exist independently (profiles Phase 3, collections Phase 2) | Observe which agents create first in practice. Does it matter? |
| Should result sets be explicit persisted objects or ephemeral? | **Not answered** — result sets are currently ephemeral (not persisted) | Does the validation session reveal a need for result set persistence? E.g., "show me what I searched yesterday" |
| Which operations benefit from resources vs tools? | **Partially answered** — 9 tools + 4 resources implemented per Option D (hybrid) | Does the agent read resources effectively? Are there tools that should be resources or vice versa? |
| Which prompts are genuinely reusable? | **Not answered** — prompts deferred to Phase 5 | Design prompts based on observed workflows, not speculation. |

### 4. Prompt Design Candidates

From doc 06 §5 and ecosystem commentary §7, three prompt candidates. Design through practice:

**`literature-review-session`** — Guided multi-step workflow:
1. Start with seed papers or keywords
2. search_papers → browse results → triage_paper (shortlist/dismiss)
3. find_related_papers from shortlisted → expand discovery
4. add_to_collection for keepers → enrich_paper for metadata
5. Repeat until diminishing returns

**`daily-digest`** — Automated monitoring:
1. Check all active watches → get deltas
2. For each new paper: get_paper → quick triage assessment
3. Auto-shortlist high-confidence matches, flag borderline for human review
4. Summary of new papers by collection/profile

**`triage-shortlist`** — Batch evaluation:
1. Given a collection of unseen papers
2. For each: read paper resource → assess against profile
3. Recommend triage states with reasoning
4. Human confirms or overrides

These are hypotheses. Real workflows may diverge. The point is to try them and see what sticks.

### 5. MCP Surface Iteration Expectations

Based on the current 9-tool + 4-resource surface, likely iteration points:

**Probably fine as-is:**
- Core discovery tools (search_papers, browse_recent, find_related_papers, get_paper)
- Core workflow tools (triage_paper, add_to_collection)
- Paper and collection resources

**Likely needs iteration:**
- `create_watch` — currently requires saving a query first (two-step). May need a combined operation.
- `add_signal` — single signal at a time. Batch add may be needed.
- `find_related_papers` — already supports multi-seed (str|list[str]). May need provenance tracking (which seed → which result).
- Watch resource — `watch://{slug}/deltas` may need richer filtering.

**Possibly missing:**
- `run_saved_query` — currently no tool to re-run a saved query through MCP (exists in CLI)
- `get_delta_since_checkpoint` — not a separate tool (embedded in watch resource)
- Bulk triage — currently one paper at a time via MCP (batch exists in CLI)
- BibTeX export — low cost, may surface as needed
- Profile description / snapshot — not exposed yet

### 6. What NOT to Build in Phase 5

- No content normalization (Phase 6)
- No semantic search (v2)
- No evaluation lenses (feedback loop design — after Phase 5 validation proves the base system works)
- No new ranking scorers or signal types (until validation reveals specific needs)
- Don't optimize before validating — the point is to discover what's wrong, not to prematurely perfect

### 7. Success Criteria Interpretation

From ROADMAP.md:

1. **"At least one real literature review session through MCP"** — This means: connect Claude Code (or another MCP client) to the server with a real PostgreSQL database containing real arXiv papers, and perform a genuine research workflow. The arxiv-scan import provides the dataset.

2. **"Doc 06 open questions resolved with evidence"** — Each of the 5 questions in §3 above gets a written answer citing specific observations from the validation session. Not opinion — evidence.

3. **"MCP prompts available and producing useful agent workflows"** — At least 2 of the 3 prompt candidates implemented and tested. "Useful" means the agent can complete a meaningful task (e.g., triage 20 papers) using the prompt without human intervention beyond confirmation.

4. **"Tool set iterated at least once"** — The 9-tool + 4-resource surface has been modified based on validation feedback. This could be: adding a missing tool, combining two tools, changing parameters, adding a resource, etc. The change must be motivated by a real usage observation, not speculation.
