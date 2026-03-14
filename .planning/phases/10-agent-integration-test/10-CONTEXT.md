# Phase 10: Agent Integration Test - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

Validate the MCP server in a real MCP client (Claude Code), complete a genuine research session through MCP tools without manual tool-call construction, and produce setup documentation validated by actual experience. No new features — this phase tests what Phases 1-9 built and documents the real-world integration experience.

</domain>

<decisions>
## Implementation Decisions

### MCP Client
- Claude Code on this machine (dionysus) — the only available MCP client (Claude Desktop is Mac-only; no other MCP clients installed)
- Configure in `~/.claude.json` under `mcpServers` key (same location as existing `sequential-thinking` server)
- Server name: `arxiv-discovery` (matches README convention)

### MCP Server Configuration
- Command: must use the project venv's Python 3.13, not system Python (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python`)
- Args: `["-m", "arxiv_mcp.mcp"]`
- Transport: stdio (per Phase 04.1 decision)
- Environment: `DATABASE_URL` passed in MCP config's `env` block pointing to the production database (`arxiv_mcp`, not `arxiv_mcp_test`)
- Working directory: project root (`/home/rookslog/workspace/projects/arxiv-sanity-mcp`) — needed for `.env` file discovery by pydantic-settings

### Database State
- Use existing `arxiv_mcp` database with Phase 5 imported data (126 papers from arxiv-scan, triage states, interest profile with tension vocabulary signals)
- Do NOT start fresh — the Phase 5 corpus provides a realistic research environment
- Verify migrations are current (`alembic upgrade head` through migration 008) before starting

### Research Session Design
- Complete all 5 end-to-end flows validated in milestone audit: Literature Review, Interest-Driven Discovery, Watch/Delta Monitoring, Content Access, Prompt-Guided
- Use existing arxiv-scan corpus topics (philosophy-adjacent: consciousness, phenomenology, cognitive science, philosophy of mind) — these are real research interests, not synthetic test data
- Session must exercise at minimum: search_papers, triage_paper, add_to_collection, find_related_papers, enrich_paper, create_profile or use existing profile for ranked search
- "Without manual tool-call construction" means: pose natural research questions to Claude Code with the MCP server active and observe whether the agent discovers and uses the tools correctly

### Setup Validation Method
- Follow README instructions from scratch in a clean mental model (pretend the database and venv don't exist)
- Test each step: clone (skip — already have repo), install, database setup (already done — verify), migration, CLI commands, MCP server config
- If any instruction is wrong, ambiguous, or missing a prerequisite: fix the README as part of this phase
- Validate MCP config block from README works when pasted into `.claude.json`

### Friction Documentation
- Structured findings document in phase directory: `10-FRICTION.md`
- Categories: (1) Blockers — prevented workflow completion, (2) Friction — slowed down but workaround exists, (3) Ergonomic — nice-to-have improvements
- Each item: description, expected behavior, actual behavior, severity, resolution (fixed now / tracked for v0.2.0)

### Ergonomic Fix Policy
- **Critical (fix now):** Tool doesn't work, misleading description causes wrong tool selection, error messages are unhelpful, server crashes
- **Non-critical (track for v0.2.0):** Tool works but could be more convenient, description could be clearer, missing batch operations, cosmetic issues
- Fixes applied during this phase get their own commits with `fix(10):` prefix
- v0.2.0 items go in `10-FRICTION.md` with the `v0.2.0` tag

### Claude's Discretion
- Exact research questions posed during the agent session
- Order of flow validation (whichever feels natural)
- Level of detail in friction documentation
- Whether to test edge cases beyond the 5 core flows
- README wording for any corrections found

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/arxiv_mcp/mcp/server.py`: FastMCP server with `app_lifespan` managing all 12 services in `AppContext` — this is what the MCP client will connect to
- `src/arxiv_mcp/mcp/__main__.py`: Entry point (`python -m arxiv_mcp.mcp` calls `mcp.run()`)
- `src/arxiv_mcp/config.py`: Settings class with all env vars documented — `DATABASE_URL`, `OPENALEX_EMAIL`, `DEPLOYMENT_MODE`
- `README.md`: MCP Server Configuration section already has the JSON config block (Phase 9)
- `scripts/import_arxiv_scan.py` (Phase 5): Import script that populated the test corpus

### Established Patterns
- MCP server registration in `~/.claude.json` under `mcpServers` key — existing `sequential-thinking` server shows the pattern
- stdio transport — all existing MCP servers on this machine use stdio
- `.env` file in project root for database credentials — pydantic-settings loads it automatically
- `PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent` — categories.toml resolution is independent of cwd

### Integration Points
- `~/.claude.json` → `mcpServers.arxiv-discovery` — new entry needed
- Project `.venv/bin/python` — must be explicitly referenced (system Python is not 3.13)
- PostgreSQL `arxiv_mcp` database on localhost:5432 — already running, already migrated
- `.env` file at project root — already exists with `DATABASE_URL`

### Known Risks (from milestone audit)
- `total_estimate` always returns `None` in search results — cosmetic, agent won't know total count
- `find_related_papers` bypasses WorkflowSearchService — related results lack triage_state/collection_slugs
- PDF adapter (Marker) optional — `get_content_variant(variant="best")` may only return abstract
- `triage_paper` docstring lists "unseen" but DB uses absence-means-unseen pattern — agent might try to set "unseen" state

</code_context>

<failure_modes>
## Anticipated Failure Modes

### Python Path Resolution
- **Risk:** MCP config uses `"command": "python"` but system python may not be 3.13 or lack arxiv_mcp package
- **Mitigation:** Use absolute path to venv python: `.venv/bin/python` with correct `cwd`
- **Verification:** Server starts and lists tools without ImportError

### .env File Discovery
- **Risk:** pydantic-settings looks for `.env` relative to cwd. If MCP client doesn't set cwd correctly, database URL defaults to the hardcoded default (which happens to be correct on this machine, but fragile)
- **Mitigation:** Pass `DATABASE_URL` explicitly in MCP config `env` block AND keep `.env` as fallback
- **Verification:** Server connects to database and tools return data

### Tool Description Quality
- **Risk:** Tool descriptions aren't clear enough for Claude to select the right tool or provide correct parameters
- **Mitigation:** This is exactly what the research session tests. Document any misuse patterns.
- **Verification:** Agent completes workflow without being corrected about which tool to use

### Categories.toml Path
- **Risk:** `Settings.load_categories()` resolves `categories_file` relative to `PROJECT_ROOT` which is computed from `Path(__file__).resolve()` — this is safe regardless of cwd
- **Verification:** `browse_recent` with category filter works

### MCP Server Lifecycle
- **Risk:** Server process killed without clean shutdown → engine not disposed
- **Mitigation:** Not critical — connections are pooled and timeout naturally. PostgreSQL handles orphaned connections.
- **Verification:** No connection leaks after multiple start/stop cycles

### Existing Data Integrity
- **Risk:** Phase 5 import data might have drifted if anyone modified the database since
- **Mitigation:** Quick verification query at session start (count papers, check profile exists)
- **Verification:** `search_papers` returns results; existing profile is loadable

</failure_modes>

<specifics>
## Specific Ideas

- The arxiv-scan corpus includes papers on consciousness, phenomenology, and philosophy of mind — these are Logan's actual research interests, making this a genuine validation not a synthetic test
- Phase 5's validation session was done via CLI tool calls. Phase 10 tests the same flows but through MCP — the experience should be qualitatively different (agent discovers tools vs human constructs calls)
- The milestone audit (v1-MILESTONE-AUDIT.md) verified all 5 E2E flows work at the service level. Phase 10 verifies they work at the MCP client level — the last mile.
- If the agent struggles to use a tool, that's signal about tool description quality, not about the tool's functionality (which is already tested by 493 tests)

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope. This is the final milestone phase.

</deferred>

---

*Phase: 10-agent-integration-test*
*Context gathered: 2026-03-14*
