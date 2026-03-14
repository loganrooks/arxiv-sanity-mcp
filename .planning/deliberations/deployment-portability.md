# Deliberation: Deployment and Portability

<!--
Deliberation template grounded in:
- Dewey's inquiry cycle (situation → problematization → hypothesis → test → warranted assertion)
- Toulmin's argument structure (claim, grounds, warrant, rebuttal)
- Lakatos's progressive vs degenerating programme shifts
- Peirce's fallibilism (no conclusion is permanently settled)

Lifecycle: open → concluded → adopted → evaluated → superseded
-->

**Date:** 2026-03-14
**Status:** Concluded
**Trigger:** After Phase 10 (agent integration test) completion, user asked: "are we sure everything is working? how might one install this locally on another computer?" Investigation revealed the project is feature-complete but not deployment-ready. Subsequent deliberation expanded scope to include: backend flexibility (SQLite vs PostgreSQL), deployment tiers (personal vs hosted), arxiv-sanity-lite architecture comparison, and PyPI distribution.
**Affects:** v0.1.x release, v0.2 milestone planning, new users, installation on apollo (MacBook), potential contributors
**Related:**
- Phase 10 friction report (`.planning/phases/10-agent-integration-test/10-FRICTION.md`)
- Phase 9 (release packaging — README, pyproject.toml, CI, GitHub)
- `CHANGELOG.md` (v0.1.0 released 2026-03-14)
- `.planning/deliberations/v2-literature-review-features.md` (open, v2 scope)
- arxiv-sanity-lite by Karpathy (https://github.com/karpathy/arxiv-sanity-lite) — architectural reference

## Situation

v0.1.0 is feature-complete: 13 MCP tools, 4 resources, 3 prompts, 493 tests, full CLI, CI pipeline. But installation requires 8 manual steps including PostgreSQL server setup, and the database starts empty.

**Comparison with arxiv-sanity-lite** (the project that inspired this one):
- arxiv-sanity-lite uses SQLite via `sqlitedict`, brute-force search (Python for-loop), per-request SVM over TF-IDF. Total deps: 5. Runs on a $5 VPS.
- Our project uses PostgreSQL with tsvector full-text search, async SQLAlchemy ORM, 8 migrations, 14+ dependencies. Feature-rich but heavy to install.
- arxiv-sanity-lite's architecture proves that SQLite + simple Python is sufficient for ~30K papers at the personal research tool scale.

**PostgreSQL coupling analysis:**
- Full-text search (`tsvector`, `ts_rank_cd`, `websearch_to_tsquery`): 4 files, ~250 lines in `db/queries.py`
- JSONB columns: 7 uses across models (storage, not queried)
- `pg_insert` ON CONFLICT: 4 files (upsert pattern)
- `asyncpg` driver: referenced in 7 files via connection strings
- `ARRAY(String)`: 1 use (`category_list`)
- All have SQLite equivalents (FTS5, JSON text, INSERT OR REPLACE, aiosqlite, JSON arrays)

**FastMCP transport support (corroborated):**
- `FastMCP.run()` accepts `transport: Literal['stdio', 'sse', 'streamable-http']`
- Hosted mode requires zero code changes — just `mcp.run(transport='streamable-http')`

**MCP distribution ecosystem:**
- Standard for Python: publish to PyPI, users install via `pip install` or `uvx` (zero-install runner)
- Standard for Node.js: publish to npm, users install via `npx`
- Our project is Python → PyPI is the distribution channel
- `uvx arxiv-mcp serve` would be the zero-install experience (requires SQLite default)

### Evidence Base

| Source | What it shows | Corroborated? | Signal ID |
|--------|--------------|---------------|-----------|
| `ls Makefile Dockerfile docker-compose.yml` | All absent | Yes (ls) | informal |
| `arxiv-mcp --help` | No `init`/`doctor`/`serve` commands | Yes (CLI output) | informal |
| `pytest -x -q` full suite | 1 failure: `test_get_or_create_html_variant` (live HTTP) | Yes (test run) | informal |
| PostgreSQL-specific grep | tsvector in 4 files, JSONB in 7, pg_insert in 4 | Yes (grep) | informal |
| SQLite FTS5 capabilities | Supports stemming (porter), BM25 ranking, boolean queries | Yes (web research) | informal |
| `FastMCP.run()` signature | Supports stdio, sse, streamable-http transports | Yes (help() output) | informal |
| arxiv-sanity-lite repo | SQLite + pickle + for-loop search, 5 deps, $5 VPS | Yes (web research) | informal |
| MCP distribution research | uvx/pip for Python, npx for Node.js, registries emerging | Yes (web research) | informal |

## Framing

**Core question:** How should we architect deployment tiers so that novices get a zero-friction experience while experienced users get the full power of PostgreSQL and self-hosting — without maintaining two completely separate products?

**Adjacent questions:**
- Where do we draw the abstraction boundary so that adding backends is cheap?
- What features define our uniqueness over arxiv-sanity-lite and must work on ALL tiers?
- Should continuous arXiv indexing (like arxiv-sanity-lite's daemon) be part of this?

## Analysis

### The Deployment Tiers

Three tiers emerged from deliberation, each serving a different user:

**Tier 1: Personal (SQLite, zero-config)**
```bash
pip install arxiv-mcp       # or: uvx arxiv-mcp serve
arxiv-mcp init              # auto-creates ~/.arxiv-mcp/data.db, seeds papers
```
- Target: Researchers, first-time users, anyone who wants to try it
- Backend: SQLite with FTS5
- Transport: stdio (launched by Claude Code/Desktop)
- Features: All core features work (search, triage, collections, profiles, ranking, enrichment)
- Limitations: Single user, no vector search, moderate scale (~10K papers)

**Tier 2: Power User (PostgreSQL, local)**
```bash
pip install arxiv-mcp
arxiv-mcp init --db postgres    # guided PostgreSQL setup or docker-compose
```
- Target: Developers, power users, users who outgrow SQLite
- Backend: PostgreSQL (local or docker-compose)
- Transport: stdio
- Features: Everything in Tier 1 + concurrent access + future pgvector for semantic search
- Migration path from Tier 1: `arxiv-mcp migrate --to postgres` (export SQLite → import PostgreSQL)

**Tier 3: Hosted (PostgreSQL, HTTP transport)**
```bash
# On the server:
arxiv-mcp init --db postgres
arxiv-mcp serve --transport http --port 8080

# On any client:
claude mcp add --transport http arxiv-discovery https://your-server:8080/mcp
```
- Target: Research groups, labs, shared instances
- Backend: PostgreSQL (required for concurrent access)
- Transport: streamable-http (FastMCP already supports this)
- Features: Everything in Tier 2 + multi-user + remote access
- No code changes needed for HTTP transport — it's a FastMCP flag

### The Architecture: Strategy Pattern with Storage Interface

```
┌──────────────────────────────────────────────────┐
│              MCP Tools / CLI / Prompts            │ ← Unchanged across all tiers
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────┴───────────────────────────┐
│           Service Layer (search, triage,          │ ← Unchanged across all tiers
│           collections, profiles, ranking,         │
│           enrichment, content)                    │
└──────────────────────┬───────────────────────────┘
                       │
┌──────────────────────┴───────────────────────────┐
│            Storage Interface (Protocol)           │ ← The abstraction boundary
│  - search_papers(query, filters) → results        │
│  - upsert_paper(data) → paper                    │
│  - get_triage_state(id) → state                  │
│  - (etc. — one method per operation)             │
└──────────┬───────────────────────┬───────────────┘
           │                       │
┌──────────┴──────────┐  ┌────────┴────────────────┐
│   SQLite Backend     │  │   PostgreSQL Backend     │
│   - FTS5 search      │  │   - tsvector search      │
│   - aiosqlite        │  │   - asyncpg               │
│   - JSON columns     │  │   - JSONB columns         │
│   - Single file      │  │   - pgvector (v2)         │
└─────────────────────┘  └─────────────────────────┘
```

### What's Unique About Our Project (Must Work on ALL Tiers)

These features differentiate us from arxiv-sanity-lite and must be preserved regardless of backend:

1. **Explainable interest-profile ranking** — 5-signal composite ranker with per-result explanations
2. **MCP-native** — agents discover and use tools naturally (not a web UI)
3. **Structured triage workflow** — 7 states with reasons (not just tags)
4. **Watch/delta monitoring** — saved searches that track new papers
5. **Lazy enrichment from OpenAlex** — citation counts, topics, related works
6. **Content normalization with rights tracking** — abstract/HTML/PDF with license gating

All of these work through the service layer, which sits above the storage interface. The backend choice affects only *how* data is stored and searched, not *what* features are available.

### Option A: Phase 11 only (distribution + setup tooling, PostgreSQL stays only backend)

- **Claim:** Publish to PyPI, add `arxiv-mcp init`/`doctor`/`serve`, docker-compose, Makefile. Keep PostgreSQL as the only backend. Defer SQLite to later.
- **Grounds:** Gets the project installable via `pip install` immediately. The init command handles PostgreSQL setup. Docker Compose removes the biggest friction point.
- **Warrant:** Solves 80% of the installation problem with 20% of the work. SQLite backend is more code to write and test. Most Claude Code users are technical enough for guided PostgreSQL setup.
- **Rebuttal:** Still requires PostgreSQL. The `uvx arxiv-mcp serve` dream (zero-config) isn't achievable without a serverless backend. Users who just want to try it face a real barrier.
- **Qualifier:** Probably sufficient for v0.1.1. Defers the zero-friction experience.

### Option B: Phase 11 + Phase 12 (distribution + storage abstraction + SQLite)

- **Claim:** Phase 11 for distribution/tooling (PyPI, init, doctor, serve, Makefile). Phase 12 for storage abstraction and SQLite backend. This enables the full tier system.
- **Grounds:** The storage interface is the key architectural decision. Once it exists, adding backends is incremental. SQLite as default means `uvx arxiv-mcp serve` works with zero prerequisites. The abstraction also prepares for v2's vector search (which may want a third backend option).
- **Warrant:** The difference between "install and configure a database" and "install and it works" is the difference between a project only the author uses and one that others actually adopt. arxiv-sanity-lite proved that SQLite is sufficient for this problem at personal scale.
- **Rebuttal:** Two phases of infrastructure work before any new features. The storage abstraction needs its own test suite. Risk of over-engineering if nobody else actually installs the project.
- **Qualifier:** Presumably the right call if the goal is genuine adoption beyond the author.

## Tensions

1. **Simplicity vs flexibility:** One backend is simpler to maintain. Two backends serve more users but double the storage-layer test surface.

2. **v0.1.x vs v0.2 boundary:** Distribution/tooling feels like a v0.1 gap. Storage abstraction feels like a v0.2 architectural change. But they're both prerequisites for genuine portability.

3. **Build for adoption vs build features:** Every phase spent on deployment infrastructure is a phase not spent on v2 features (semantic search, literature review enhancements). But features nobody can install have zero impact.

4. **Continuous indexing gap:** arxiv-sanity-lite has a daemon that continuously fetches new papers. Our project has `harvest` and `import` commands but no background indexing. This is a product gap separate from deployment, but affects the "ongoing value" story. (Deferred — not in scope for this deliberation.)

## Recommendation

**Conclusion: Option B — Phase 11 (Distribution) + Phase 12 (Storage Abstraction)**

**Phase 11: Distribution & Developer Experience** (v0.1.1)

| Plan | Deliverables |
|------|-------------|
| 11-01 | Fix failing test + `docker-compose.yml` for PostgreSQL + `Makefile` |
| 11-02 | `arxiv-mcp init` (guided setup) + `arxiv-mcp doctor` (health check) + seed data fixture |
| 11-03 | `arxiv-mcp serve` entry point + publish to PyPI + update README for `pip install` |

**Phase 12: Storage Abstraction** (v0.2.0 — first phase of v0.2 milestone)

| Plan | Deliverables |
|------|-------------|
| 12-01 | Define storage interface protocol + refactor PostgreSQL behind it |
| 12-02 | SQLite backend with FTS5 + `arxiv-mcp init` defaults to SQLite |
| 12-03 | `arxiv-mcp serve --transport http` documentation + migration command (`sqlite → postgres`) |

**Rationale:**
- Phase 11 makes v0.1 installable by others (3-step process instead of 8)
- Phase 12 makes it zero-config installable (`pip install arxiv-mcp && arxiv-mcp init` — done)
- The storage interface prepares for v2's semantic search (pgvector as a PostgreSQL-only feature is a natural tier differentiator)
- Hosted mode (Tier 3) requires zero code — FastMCP already supports `streamable-http` transport
- Separating into two phases lets us ship v0.1.1 quickly, then tackle the abstraction as the first v0.2 work

**Tier feature matrix (what works where):**

| Feature | Tier 1 (SQLite) | Tier 2 (PostgreSQL) | Tier 3 (Hosted) |
|---------|----------------|--------------------|-----------------|
| Full-text search | FTS5 | tsvector | tsvector |
| Interest profiles + ranking | Yes | Yes | Yes |
| Triage / collections / watches | Yes | Yes | Yes |
| OpenAlex enrichment | Yes | Yes | Yes |
| Content normalization | Yes | Yes | Yes |
| MCP prompts | Yes | Yes | Yes |
| Concurrent users | No | Limited | Yes |
| Vector/semantic search (v2) | No | pgvector | pgvector |
| Scale | ~10K papers | Unlimited | Unlimited |

## Predictions

**If adopted, we predict:**

| ID | Prediction | Observable by | Falsified if |
|----|-----------|---------------|-------------|
| P1 | `arxiv-mcp init` will reduce setup from ~15 min to <3 min | Time a fresh install on apollo after Phase 11 | Setup still takes >10 min |
| P2 | >70% of new users will choose SQLite (Tier 1) over PostgreSQL | Track backend selection in init command (after Phase 12) | Most users choose PostgreSQL |
| P3 | The storage interface will require <5 methods to cover all backend operations | Count methods in the protocol after Phase 12-01 | Interface has >15 methods (too granular = wrong abstraction) |
| P4 | SQLite FTS5 search quality will be indistinguishable from PostgreSQL tsvector for corpora <10K papers | Compare search results for same queries on both backends | Users report noticeably worse search on SQLite |
| P5 | Zero users will need Tier 3 (hosted) in the first 6 months | Track `--transport http` usage | Someone requests hosted mode within 3 months |

## Decision Record

**Decision:** Tiered deployment architecture. Phase 11 (distribution/tooling) as v0.1.1. Phase 12 (storage abstraction/SQLite) as first phase of v0.2. Three tiers: Personal (SQLite), Power (PostgreSQL), Hosted (HTTP transport). Storage interface as the abstraction boundary.
**Decided:** 2026-03-14
**Implemented via:** not yet implemented — Phase 11 and Phase 12 to be created
**Signals addressed:** None (triggered by post-Phase-10 conversation)

## Evaluation

<!--
Filled when status moves to `evaluated`.
Compare predictions against actual outcomes. Explain deviations.
-->

## Supersession

<!--
Filled when status moves to `superseded`.
-->
