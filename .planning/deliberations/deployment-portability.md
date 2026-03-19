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
**Status:** Open — Spike 002 Round 1 done but has methodological gaps (Round 2 in progress). Spike 001 is 3/8 complete. Deliberation blocked on spike completion — see `.planning/spikes/ROADMAP.md` for full dependency chain and execution plan.
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

## Status Update (2026-03-15)

The recommendation above was drafted prematurely — several key assumptions require empirical testing before architectural decisions can be made. A spike program has been created to investigate:

1. **Volume and filtering landscape** (Spike 001): What are the real-world paper volumes under different configurations? What scoring signals predict paper importance at ingestion time? What are the coverage/regret tradeoffs of different filtering strategies?

2. **Backend performance benchmarking** (Spike 002): At the volumes identified in Spike 001, how do SQLite and PostgreSQL perform across the full paper lifecycle?

The phasing (11 + 12) and tier feature matrix above remain the *working hypothesis*, but they should not be adopted until spike findings either confirm or revise them. In particular:
- The "~10K papers" SQLite limit in the tier matrix is an unverified guess
- The storage interface design depends on understanding the promotion pipeline
- The scoring/filtering system design emerged as a prerequisite question not addressed in this deliberation

**Spike program roadmap:** `.planning/spikes/ROADMAP.md`
**Deliberation status:** Open — re-evaluate after Spike 001 findings

## Status Update (2026-03-17) — Spike 001 Capability Envelope Complete

The A1c capability benchmarks are complete. They tested three key operations at 6 scale points (5K–215K papers) using 19,252 real arXiv papers. The results invalidate several assumptions in the analysis above and require revising the tier model.

### Evidence from Spike 001 A1c

| Experiment | Key Finding | Deliberation Impact |
|-----------|-------------|---------------------|
| A1c.1: TF-IDF matrix | 157 MB at 215K. Cosine search 516ms (crosses 100ms at ~50-75K) | Memory is not the constraint — compute is. Pre-filtering or embedding switch mitigates. |
| A1c.2: Concurrent SQLite | WAL mode: p50 stays 1.3-1.6ms at 0-100 writes/s. Zero lock errors. | Concurrent single-writer access is a non-issue. "No concurrent users" in tier matrix was wrong for single-writer. |
| A1c.3: Embeddings | Brute-force search 16ms at 215K (30x faster than TF-IDF). GPU 20x faster for computing embeddings (1.7 vs 35ms/paper). 315 MB float32 at 215K. | pgvector is unnecessary at personal scale. Tier differentiator is GPU for compute, not database for search. |

Full results: `.planning/spikes/001-volume-filtering-scoring-landscape/FINDINGS.md`

### Assumptions Falsified

**1. "~10K papers" SQLite scale limit (Tier matrix, line 224)**
- **Claim:** SQLite can handle ~10K papers
- **Evidence:** FTS5 search under 100ms to 500K papers. Embedding search under 100ms to ~1.3M papers. WAL concurrent access zero degradation. TF-IDF similarity under 100ms to ~50-75K (mitigable via pre-filtering or embedding switch).
- **Revised:** SQLite's operational limit is **~500K papers for keyword search**, with higher limits for embedding similarity. The TF-IDF path has a 50-75K limit that's addressable through design (see mitigations below).

**2. "Vector/semantic search: No (SQLite) / pgvector (PostgreSQL)" (Tier matrix, line 223)**
- **Claim:** Semantic search requires pgvector on PostgreSQL
- **Evidence:** Brute-force dot product over 384-dim pre-normalized embeddings: 16ms at 215K papers. Faster than FTS5 keyword search (30ms) at the same scale. pgvector's ANN indexing only becomes valuable above ~1M papers where brute-force O(n) starts to matter.
- **Revised:** Semantic search works on **any backend** via brute-force numpy. pgvector is a scaling optimization for >1M papers, not a capability gate.

**3. "Concurrent users: No (SQLite)" (Tier matrix, line 222)**
- **Claim:** SQLite cannot handle concurrent access
- **Evidence:** WAL mode with single writer (harvest daemon) + single reader (MCP server): zero latency degradation, zero lock errors at 100 writes/second. Daily harvest rate is 0.007 papers/second — orders of magnitude below contention threshold.
- **Revised:** SQLite handles the **single-writer** scenario (one harvest daemon + one MCP server) perfectly. "No concurrent users" only applies to **multi-writer** scenarios (multiple users triaging simultaneously).

### Revised Tier Model

The original tiers were organized around **database choice** (SQLite → PostgreSQL → Hosted). The spike data shows the meaningful axes are:

| Axis | What it determines | Measured evidence |
|------|-------------------|-------------------|
| **Corpus size** | Which search methods stay interactive | FTS5: 500K. Embeddings: 1.3M. TF-IDF: 50-75K (mitigable). |
| **GPU availability** | Whether embedding computation is seconds or hours | 20x speedup (1.7ms vs 35ms per paper). But incremental daily is only 21s even on CPU. |
| **User count** | Whether SQLite suffices or PostgreSQL is needed | Single-writer: SQLite is fine. Multi-writer: PostgreSQL required. |

**Revised feature matrix:**

| Feature | SQLite (default) | PostgreSQL (opt-in) |
|---------|-----------------|---------------------|
| Full-text search | FTS5 (30ms at 215K) | tsvector |
| Interest profiles + ranking | Yes | Yes |
| TF-IDF recommendations | Yes (pre-filter at >50K) | Yes |
| Embedding/semantic search | Yes, brute-force (16ms at 215K) | Yes + pgvector ANN at >1M |
| Triage / collections / watches | Yes | Yes |
| OpenAlex enrichment | Yes | Yes |
| Content normalization | Yes | Yes |
| Concurrent single-writer | Yes (WAL mode) | Yes |
| Concurrent multi-writer | **No** | Yes |
| Scale ceiling | ~500K papers | Unlimited |

Only one "No" remains: multi-writer concurrency. Everything else works on SQLite.

### Performance Mitigations (Design-Level)

The raw benchmarks identify three bottlenecks. Each has design-level mitigations that don't require hardware changes:

**TF-IDF cosine similarity (516ms at 215K, crosses 100ms at ~50K-75K):**
1. **Category pre-filtering** — Search within primary category. cs.AI primary ≈ 16K/year → 20ms.
2. **SVM pre-selection** — arxiv-sanity-lite's approach: SVM trained on user library selects candidates, cosine only over candidates.
3. **Switch to embedding similarity** — 30x faster. Use TF-IDF for keyword search only, embeddings for similarity.
4. **Rolling window** — Only compute similarity over recent N months, not full corpus.

**CPU embedding computation (35ms/paper, 2 hours for full 215K corpus):**
1. **Incremental embedding** — 600 new papers/day × 35ms = **21 seconds/day on CPU**. The 2-hour figure is cold-start only.
2. **Lazy embedding** — Only embed papers the user interacts with (triaged, collected). Most papers never need embeddings.
3. **Pre-computed from OpenAlex** — OpenAlex is adding embeddings to their API. Fetch instead of compute.
4. **Cold-start mitigation** — First `arxiv-mcp init` could batch-embed the seed corpus (a one-time setup step).

**Feature matrix loading on MCP server startup (~472 MB total: 315 MB embeddings + 157 MB TF-IDF):**
1. **Memory-mapped files** — `numpy.memmap` for both matrices. Load time → ~0ms (OS pages on demand).
2. **Background loading** — Start MCP server immediately for metadata/triage. Load features in background thread.
3. **Lazy initialization** — Don't load until first recommendation/similarity query. First query ~2s, all subsequent instant.

With these mitigations, the practical user experience is:
- **Server start:** Instant (mmap or lazy load)
- **Daily operation:** 21 seconds/day for embedding new papers (CPU), instant on GPU
- **Similarity search:** 16ms (embeddings) or <100ms (TF-IDF with pre-filtering)
- **Cold start (first install):** 6 minutes (GPU) or batch overnight (CPU) — one-time cost

### Impact on Recommendation

**Option B (Phase 11 + Phase 12) remains correct** but the motivation shifts:

**Original motivation:** SQLite needed because PostgreSQL is too hard to install. Storage abstraction needed because SQLite can't do semantic search.

**Revised motivation:** SQLite is the **sufficient default** for the full feature set at personal scale. PostgreSQL is an opt-in upgrade for multi-writer access or extreme scale (>500K). The storage abstraction is good architecture for testability and portability, not a capability bridge.

**Revised Phase 12 scope:**
- Storage abstraction still needed for clean backend switching
- SQLite backend can now support **all features** including semantic search (was previously marked "No")
- pgvector integration moves from "required for semantic search" to "optional optimization at >1M papers"
- **New: Feature lifecycle layer** — memory-mapped embedding/TF-IDF storage, incremental update, lazy loading. This is above the storage layer but below the service layer.

### Revised Predictions

| ID | Original Prediction | Revised | Status |
|----|-------------------|---------|--------|
| P1 | `arxiv-mcp init` reduces setup to <3 min | Unchanged | Still testable |
| P2 | >70% choose SQLite | Strengthened — SQLite has full feature parity | Still testable |
| P3 | Storage interface <5 methods | Unknown — needs implementation | Still testable |
| P4 | FTS5 quality ≈ tsvector for <10K papers | Revised to <500K papers (scale limit much higher) | Needs testing |
| P5 | Zero users need Tier 3 in 6 months | Unchanged | Still testable |
| P6 | *(new)* Brute-force embedding search stays under 100ms to 500K papers | Extrapolated ~37ms at 500K | Testable with real data |
| P7 | *(new)* Incremental daily embedding on CPU takes <60 seconds | 600 papers × 35ms = 21s projected | Testable operationally |

### What Spike 001 A1c Does NOT Answer

1. **FTS5 vs tsvector result quality** — Are they functionally equivalent? Search *latency* is established; search *quality* is not.
2. **Feature lifecycle implementation** — Memory-mapped files, incremental updates, lazy loading are proposed but not prototyped.
3. **MCP server startup time** — Projected as near-instant with mmap but not measured.
4. **Cold start UX** — What does "embedding 19K papers for 11 minutes on CPU" feel like as a first-run experience?
5. **Embedding quality for this domain** — all-MiniLM-L6-v2 may not be optimal for academic abstracts. SPECTER2 or domain-specific models might be better.

These are smaller, more targeted questions. Some are testable experiments (add to Spike 001 A2+ or new spikes); others are design decisions that can be made with current evidence.

### Spike 002 Status — COMPLETE

~~**Original plan:** Benchmark PostgreSQL at the same scales for fair comparison.~~
~~**Revised assessment:** Less urgent. The spike data shows SQLite handles the full workload. Spike 002 would confirm the delta is small, but the decision no longer depends on it. PostgreSQL's remaining advantage (multi-writer) is architectural, not performance-based.~~
~~**Recommendation:** Defer Spike 002. Proceed to Phase 11 (distribution) with current evidence. If multi-user demand emerges, run Spike 002 then.~~

**The above was premature.** Spike 002 was executed (2026-03-18) and produced findings that significantly revise the analysis. See Status Update below.

## Status Update (2026-03-18) — Spike 002 Complete

Spike 002 measured PostgreSQL across 6 dimensions at the same scale points as Spike 001, using the same 19,252 real arXiv papers. The results invalidate additional assumptions and require a second tier model revision.

Full findings: `.planning/spikes/002-backend-comparison/FINDINGS.md`

### Evidence from Spike 002

| Dimension | Key Finding | Deliberation Impact |
|-----------|-------------|---------------------|
| D1: Search quality | FTS5 and tsvector return materially different papers (avg Jaccard 0.39). FTS5 fails on hyphenated terms. 13/20 queries show low agreement. | **Major.** Backend choice is a retrieval quality decision, not just performance. P4 falsified. |
| D2: Search latency | FTS5 is 3.5–4.8x faster at all scale points. tsvector ~100ms at 215K. | Moderate. Both under 500ms. FTS5 speed advantage is real but both are interactive. |
| D3: Vector search | pgvector HNSW is 5–23x faster than numpy brute-force, near-constant ~0.8ms. Recall ≥0.91. | **Major.** HNSW provides genuine value even at 19K. "pgvector unnecessary" falsified. |
| D4: Writes | SQLite 5–6x faster for bulk import. Both handle concurrent R+W without degradation. | Minor. Cold start difference (1.5s vs 8.6s at 19K) is not user-visible. |
| D5: Operations | SQLite: 87x faster connections, instant backup, 2x smaller on disk. | Moderate for deployment simplicity. Negated by connection pooling in practice. |
| D6: Workflow | 6-tool MCP workflow: SQLite 15ms, PG 21ms (1.4x). | Minor. Both well under 100ms for complete workflows. |

### Assumptions Falsified (Second Round)

**4. P4: "FTS5 quality ≈ tsvector for <500K papers" (Revised prediction from first update)**
- **Claim:** Search quality is equivalent between backends
- **Evidence:** Average Jaccard 0.39 at 19K. "language model" returns Jaccard 0.03 (near-complete disagreement). FTS5 fails entirely on 2/20 queries with hyphenated terms.
- **Revised:** FTS5 and tsvector are **not interchangeable**. They use different stemming, different ranking functions, and handle multi-word queries differently. The quality gap is independent of scale.

**5. "pgvector unnecessary at personal scale" (Spike 001 claim, reinforced in A1c update)**
- **Claim:** Brute-force numpy is sufficient; pgvector only needed at >1M papers
- **Evidence:** pgvector HNSW: 0.6ms at 215K. Numpy brute-force: 14ms at 215K. HNSW is 23x faster and near-constant regardless of scale. Recall 91% at 215K with default params.
- **Revised:** pgvector provides genuine value **at every scale tested** (5K–215K). The O(1) vs O(n) scaling means the advantage grows with corpus size. The Spike 001 claim was one-sided inference.

**6. "Only one 'No' remains: multi-writer" (Revised tier matrix from first update)**
- **Claim:** SQLite has full feature parity except multi-writer
- **Evidence:** Search quality divergence means SQLite and PostgreSQL offer different user experiences even for single users. The difference isn't a missing feature — it's a different quality of results for the same queries.
- **Revised:** The tier model has **two meaningful differentiators**: (1) search quality (stemming, ranking, hyphen handling), (2) vector search speed. Multi-writer is third.

### Second Tier Model Revision

The first revision (after Spike 001) organized tiers around corpus size/GPU/user count. Spike 002 shows **search quality** is a new axis:

| Axis | What it determines | Evidence |
|------|-------------------|----------|
| **Search quality** | Whether results are optimal for multi-word/hyphenated queries | Jaccard 0.39 between FTS5 and tsvector. FTS5 fails on hyphens. |
| **Vector search speed** | Whether semantic search is sub-millisecond or tens of ms | HNSW 0.8ms vs numpy 3–14ms depending on scale |
| **Deployment simplicity** | Whether user needs PostgreSQL server | SQLite is zero-config; PostgreSQL needs install/config |
| **User count** | Whether multi-writer is needed | Single-writer: either. Multi-writer: PostgreSQL. |

**Second revised feature matrix:**

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Full-text search speed | **Faster** (3.5–4.8x) | Slower but interactive |
| Full-text search quality | Different stemming, fails on hyphens | Better stemming, handles all query types |
| Interest profiles + ranking | Yes | Yes |
| Embedding/semantic search | Brute-force (3–14ms, scales linearly) | **HNSW (0.6–1ms, near-constant)** |
| TF-IDF recommendations | Yes (pre-filter at >50K) | Yes |
| Triage / collections / watches | Yes | Yes |
| OpenAlex enrichment | Yes | Yes |
| Content normalization | Yes | Yes |
| Concurrent single-writer | Yes (WAL mode) | Yes |
| Concurrent multi-writer | **No** | Yes |
| Deployment | Zero-config, single file | Requires server |
| Disk space | 2x smaller | 2x larger |
| Backup | File copy (instant) | pg_dump (seconds) |
| Scale ceiling | ~500K for keyword | Unlimited |

The story is no longer "SQLite does everything, PostgreSQL adds multi-writer." It's: **SQLite is simpler to deploy but has worse search quality and slower vector search. PostgreSQL is harder to deploy but provides better results.** This is a genuine tradeoff, not a simple tier ordering.

### Impact on Recommendation

**Option B (Phase 11 + Phase 12) still holds** but the storage abstraction design must account for quality differences:

1. **Default backend question reopened.** The first revision concluded "SQLite as default" because it had "full feature parity." Spike 002 shows it doesn't — search quality differs materially. The default should be the backend that gives users the best experience, not the easiest to install.

2. **Storage interface cannot hide quality differences.** A `search_papers()` method will return different results depending on backend. This isn't a bug — it's a property of the backends. The abstraction must be honest about this (documentation, not code).

3. **pgvector integration moves earlier.** The first revision pushed pgvector to "optional optimization at >1M papers." Spike 002 shows HNSW has value at 19K. If PostgreSQL is in the picture at all, pgvector should be available from day one.

4. **The "try it easily → upgrade for power" story is complicated.** If SQLite search quality is worse, users who start on SQLite may have a worse first impression. On the other hand, SQLite's zero-config story is what gets them in the door at all.

### Remaining Questions for Deliberation (Not Spikes)

The data is now sufficient for the deployment deliberation to reach a conclusion. The remaining questions are judgment calls, not empirical ones:

1. **Default backend choice:** SQLite (easier to start, worse search) vs PostgreSQL (harder to start, better results). Or: docker-compose as the PostgreSQL "easy path."
2. **Whether to ship both backends or PostgreSQL-only with docker-compose for simplicity.** Two backends means 2x storage test surface. Docker-compose could make PostgreSQL nearly as easy as SQLite.
3. **Whether the FTS5 quality gap matters in practice for this user base.** The Jaccard was measured against tsvector as ground truth, but neither has been measured against human relevance judgments. FTS5 might return equally useful (just different) papers.

### Second Revised Predictions

| ID | Original | After Spike 001 | After Spike 002 | Status |
|----|----------|-----------------|-----------------|--------|
| P1 | init reduces setup to <3 min | Unchanged | Unchanged | Testable |
| P2 | >70% choose SQLite | Strengthened | **Weakened** — quality gap may push users to PG | Testable |
| P3 | Storage interface <5 methods | Unchanged | Unchanged | Testable |
| P4 | FTS5 quality ≈ tsvector | Extended to <500K | **Falsified** (Jaccard 0.39 at 19K) | Done |
| P5 | Zero Tier 3 users in 6mo | Unchanged | Unchanged | Testable |
| P6 | Embedding search <100ms to 500K | Extrapolated ~37ms | Confirmed trajectory, but HNSW is 0.6ms | Partially confirmed |
| P7 | Daily CPU embedding <60s | 21s projected | Unchanged | Testable |
| P8 | *(new)* pgvector HNSW recall stays >0.9 at 500K | — | Extrapolated from 0.91 at 215K | Testable |

## Decision Record

**Decision:** Pending — Spike 002 Round 1 data available but has methodological gaps (D1 confound, missing reference comparison, missing result inspection). Spike 001 is 3/8 complete (A2/A3/B/C pending). Deliberation cannot conclude until both spikes are done — the empirical foundation is incomplete.
**Decided:** —
**Implemented via:** not yet implemented
**Signals addressed:** Spike 001 A1 (volume mapping), A1b (FTS5 benchmark), A1c.1 (TF-IDF), A1c.2 (concurrent SQLite), A1c.3 (embeddings), Spike 002 D1–D6 Round 1 (provisional — see caveats in FINDINGS.md)
**Signals pending:** Spike 002 Round 2 (D1 remediation, reference designs, quick validations), Spike 001 A2/A3/B/C

## Evaluation

<!--
Filled when status moves to `evaluated`.
Compare predictions against actual outcomes. Explain deviations.
-->

## Supersession

<!--
Filled when status moves to `superseded`.
-->
