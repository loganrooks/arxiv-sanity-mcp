# Phase 10: Agent Integration Test - Research

**Researched:** 2026-03-14
**Domain:** MCP server integration, Claude Code MCP configuration, agent workflow validation
**Confidence:** HIGH

## Summary

Phase 10 is an integration testing and documentation phase, not a code-building phase. The primary technical challenges are: (1) correctly configuring the arxiv-discovery MCP server in Claude Code so it connects to the production database, (2) executing a genuine research session through the agent's natural tool discovery rather than manual tool-call construction, and (3) documenting friction points and setup issues discovered through actual experience.

The MCP server implementation is complete (13 tools, 4 resources, 3 prompts) and validated by 493 tests. The database has realistic research data (126 papers, 1 interest profile with 13 signals, 98 triage states, 1 collection). The core risk is configuration -- Claude Code's MCP server configuration has specific requirements for stdio servers (Python path, working directory, environment variables) that the README's generic instructions may not adequately capture for this project's setup.

**Primary recommendation:** Use `claude mcp add-json` with scope `local` under the arxiv-sanity-mcp project path to configure the server, with explicit venv Python path and DATABASE_URL in the env block. Test server connection before attempting the research session. Document the exact configuration that works, then validate that the README instructions match.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **MCP Client:** Claude Code on dionysus (the only available MCP client)
- **Server name:** `arxiv-discovery` (matches README convention)
- **Python:** Must use project venv Python 3.13 (`/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python`)
- **Args:** `["-m", "arxiv_mcp.mcp"]`
- **Transport:** stdio
- **Environment:** `DATABASE_URL` passed in MCP config env block, pointing to production database (`arxiv_mcp`, not `arxiv_mcp_test`)
- **Working directory:** Project root (`/home/rookslog/workspace/projects/arxiv-sanity-mcp`)
- **Database state:** Use existing `arxiv_mcp` database with Phase 5 data (126 papers). Do NOT start fresh.
- **Migrations:** Verify at `008` (head) via `alembic upgrade head`
- **Research session:** Complete all 5 E2E flows from milestone audit (Literature Review, Interest-Driven Discovery, Watch/Delta Monitoring, Content Access, Prompt-Guided)
- **Topics:** Use existing arxiv-scan corpus topics (philosophy-adjacent: consciousness, phenomenology, cognitive science, philosophy of mind)
- **Minimum tools exercised:** search_papers, triage_paper, add_to_collection, find_related_papers, enrich_paper, create_profile or existing profile for ranked search
- **"Without manual tool-call construction":** Pose natural research questions to Claude Code with the MCP server active and observe whether the agent discovers and uses the tools correctly
- **Setup validation:** Follow README from scratch (clean mental model), test each step, fix any wrong/ambiguous/missing instructions
- **Friction doc:** `10-FRICTION.md` in phase directory with categories: Blockers, Friction, Ergonomic
- **Fix policy:** Critical fixes now with `fix(10):` prefix commits; non-critical tracked for v0.2.0 in friction doc
- **Ergonomic fix threshold:** Tool doesn't work / misleading description / unhelpful errors / server crashes = fix now. Everything else = v0.2.0.

### Claude's Discretion
- Exact research questions posed during agent session
- Order of flow validation
- Level of detail in friction documentation
- Whether to test edge cases beyond the 5 core flows
- README wording for any corrections found

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope. This is the final milestone phase.
</user_constraints>

## Standard Stack

### Core (Already Installed -- No New Dependencies)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastMCP (mcp SDK) | Current | MCP server framework | Already powers the server (Phase 04.1) |
| Claude Code | 2.x | MCP client / agent | Only available MCP client on dionysus |
| PostgreSQL | 16+ | Database backend | Already running with Phase 5 data |
| asyncpg | Current | Async PostgreSQL driver | Already installed in venv |

### Supporting (Configuration Tools)

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `claude mcp add-json` | Register MCP server in Claude Code | Server configuration step |
| `claude mcp list` | Verify server connection | After configuration |
| `claude mcp get` | Debug server details | If connection fails |
| `claude mcp remove` | Remove misconfigured server | If reconfiguration needed |
| `/mcp` (in-session) | Check server status during session | During research session |

### No Alternatives Needed
This phase uses only existing infrastructure. No library selection decisions.

## Architecture Patterns

### Pattern 1: MCP Server Configuration for stdio Python Server

**What:** Configure a local Python FastMCP server to run via stdio transport in Claude Code
**When to use:** When the server is a Python project with its own venv, not globally installed

There are two approaches for configuring the server. Both are valid.

**Approach A: `claude mcp add-json` (recommended for precise control)**

```bash
claude mcp add-json arxiv-discovery '{
  "type": "stdio",
  "command": "/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python",
  "args": ["-m", "arxiv_mcp.mcp"],
  "cwd": "/home/rookslog/workspace/projects/arxiv-sanity-mcp",
  "env": {
    "DATABASE_URL": "postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp"
  }
}' --scope local
```

**Approach B: `claude mcp add` with flags**

```bash
claude mcp add \
  --transport stdio \
  --env DATABASE_URL=postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp \
  arxiv-discovery \
  -- /home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python -m arxiv_mcp.mcp
```

Note: Approach B does not support `cwd` directly via the CLI. The `add-json` approach is preferred because it supports the `cwd` field, which ensures pydantic-settings can discover the `.env` file as a fallback.

**Approach C: Project-scoped `.mcp.json` (for README/team sharing)**

Create `.mcp.json` in the project root:
```json
{
  "mcpServers": {
    "arxiv-discovery": {
      "type": "stdio",
      "command": "${ARXIV_MCP_PYTHON:-python}",
      "args": ["-m", "arxiv_mcp.mcp"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL:-postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp}"
      }
    }
  }
}
```

This uses environment variable expansion (`${VAR:-default}`) so each developer can customize paths. Claude Code prompts for approval before using project-scoped servers from `.mcp.json`.

**Source:** Official Claude Code MCP documentation at https://code.claude.com/docs/en/mcp

### Pattern 2: Server Verification Protocol

**What:** Step-by-step verification that the MCP server is running correctly
**When to use:** After initial configuration, before attempting research session

1. `claude mcp list` -- verify `arxiv-discovery` appears and shows "Connected"
2. Start a new Claude Code session in the project directory
3. `/mcp` -- verify server appears in the in-session server list
4. Ask Claude to "list the available MCP tools from arxiv-discovery" -- verify it sees all 13 tools
5. Ask Claude to "search for papers about consciousness" -- verify search_papers returns results from the database

If step 1 fails: Check Python path, check venv exists, check `python -m arxiv_mcp.mcp` runs without errors.
If step 4 fails: Server starts but tools aren't registered -- check import errors.
If step 5 fails: Server connects but database is unreachable -- check DATABASE_URL and PostgreSQL.

### Pattern 3: Agent Research Session Design

**What:** Structure for the 5 E2E flow validation
**When to use:** During the actual research session

The session should progress naturally through research questions that exercise all 5 flows. The key constraint is "without manual tool-call construction" -- the agent must discover and select tools based on natural language prompts, not explicit tool name instructions.

**Example natural language prompts (not tool instructions):**

- Flow 1 (Literature Review): "I'm interested in recent work on consciousness and phenomenology. Can you find relevant papers, help me identify the most important ones, and organize them?"
- Flow 2 (Interest-Driven Discovery): "I have an interest profile called 'arxiv-scan-tensions'. Can you use it to find papers that match my research interests and explain why each paper scored well?"
- Flow 3 (Watch/Delta Monitoring): "Set up monitoring for new papers about 'philosophy of mind' so I can check for updates later."
- Flow 4 (Content Access): "For paper [arxiv_id], can you get me the full content, not just the abstract?"
- Flow 5 (Prompt-Guided): Use the `/mcp__arxiv-discovery__literature_review_session` prompt directly

### Anti-Patterns to Avoid
- **Telling the agent which tool to use:** This defeats the purpose. Say "find related papers" not "use the find_related_papers tool"
- **Testing in the same session as configuration:** Start a fresh Claude Code session after configuring the server
- **Ignoring friction silently:** Every hiccup, confusion, or wrong tool selection is signal. Document it.
- **Fixing code during the research session:** Complete the session first, document all friction, then fix in separate commits

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| MCP config editing | Manual JSON editing of ~/.claude.json | `claude mcp add-json` command | Handles escaping, scope management, and config file merging |
| Server health check | Custom healthcheck script | `claude mcp list` and `/mcp` | Built-in to Claude Code, shows connection status |
| Database verification | Custom DB check script | Quick SQL via CLI or Python | One-off verification, not production tooling |

## Common Pitfalls

### Pitfall 1: Wrong Python Path

**What goes wrong:** Using `"command": "python"` in MCP config picks up system Python (which may lack arxiv_mcp package or be wrong version)
**Why it happens:** System Python is in PATH, venv Python is not
**How to avoid:** Always use absolute path: `/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python`
**Warning signs:** `ModuleNotFoundError: No module named 'arxiv_mcp'` in server startup logs
**Confidence:** HIGH -- verified: system Python is conda 3.13.5, venv Python is also 3.13.5. On this machine both would work, but absolute path is still correct practice.

### Pitfall 2: Missing cwd Causes .env Discovery Failure

**What goes wrong:** pydantic-settings looks for `.env` relative to the process cwd. If Claude Code starts the server process in a different directory, the `.env` file isn't found.
**Why it happens:** Claude Code's stdio server launch may not set cwd to the project directory by default.
**How to avoid:** Pass `DATABASE_URL` explicitly in the MCP config env block. Also set `cwd` in the config if using `add-json`.
**Warning signs:** Server connects but returns empty results (using hardcoded default DATABASE_URL which happens to match on this machine -- so this pitfall is invisible here but breaks portability).
**Confidence:** HIGH -- verified: Settings has a hardcoded default that matches this machine's setup. But relying on the default is fragile.

### Pitfall 3: triage_paper "unseen" State Confusion

**What goes wrong:** Agent tries to set triage state to "unseen" because the tool docstring lists it. The DB uses absence-means-unseen pattern, so setting "unseen" deletes the triage record rather than creating one with "unseen" state.
**Why it happens:** Docstring lists "unseen" as valid state, which is technically correct (the service handles it by deleting the record), but an agent might expect it to create a visible record.
**How to avoid:** Document this behavior in friction findings. Not necessarily a bug -- the service correctly handles it.
**Warning signs:** Agent calls triage_paper with state="unseen" and gets a success response, but the paper's triage state appears as absent/None rather than "unseen" in subsequent queries.
**Confidence:** HIGH -- from milestone audit observations.

### Pitfall 4: total_estimate Always None

**What goes wrong:** Agent asks "how many total results are there?" and cannot answer because total_estimate is always None in search results and collection views.
**Why it happens:** Known tech debt from Phase 5 -- count queries not implemented.
**How to avoid:** Document as friction, not a bug to fix in this phase. Track as v0.2.0 item.
**Warning signs:** Agent makes incorrect assumptions about result set size.
**Confidence:** HIGH -- from milestone audit and validation log.

### Pitfall 5: find_related_papers Lacks Workflow Enrichment

**What goes wrong:** Results from find_related_papers don't include triage_state or collection_slugs, unlike results from search_papers.
**Why it happens:** find_related_papers bypasses WorkflowSearchService (design choice documented in milestone audit).
**How to avoid:** Document as friction. Agent must call get_paper or read paper://ID to check triage state of related results.
**Warning signs:** Agent assumes a related paper hasn't been seen before, but it was actually already triaged.
**Confidence:** HIGH -- from milestone audit.

### Pitfall 6: MCP Server Restart Required After Config Changes

**What goes wrong:** Modifying tool descriptions or server code doesn't take effect until Claude Code session is restarted.
**Why it happens:** Claude Code caches MCP server tool definitions at session start.
**How to avoid:** After any `fix(10):` commit that changes tool descriptions or server code, restart the Claude Code session before retesting.
**Warning signs:** Changes to tool descriptions don't appear; old behavior persists.
**Confidence:** HIGH -- standard MCP client behavior.

### Pitfall 7: OpenAlex Enrichment May Fail Without Email

**What goes wrong:** enrich_paper hits OpenAlex rate limit (1 req/s anonymous vs 10 req/s with email)
**Why it happens:** OPENALEX_EMAIL not set in .env or MCP config env block
**How to avoid:** Add OPENALEX_EMAIL to the MCP config env block for the research session. Not critical -- enrichment will work at lower rate -- but may slow down the session.
**Warning signs:** Enrichment calls take longer than expected, or intermittent 429 errors.
**Confidence:** MEDIUM -- may not hit rate limits with small corpus.

## Code Examples

### MCP Server Configuration (Exact Config for This Machine)

```json
{
  "type": "stdio",
  "command": "/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python",
  "args": ["-m", "arxiv_mcp.mcp"],
  "cwd": "/home/rookslog/workspace/projects/arxiv-sanity-mcp",
  "env": {
    "DATABASE_URL": "postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp"
  }
}
```

Source: Verified against project .env file, config.py defaults, and Claude Code MCP documentation.

### Server Registration Command

```bash
claude mcp add-json arxiv-discovery '{"type":"stdio","command":"/home/rookslog/workspace/projects/arxiv-sanity-mcp/.venv/bin/python","args":["-m","arxiv_mcp.mcp"],"cwd":"/home/rookslog/workspace/projects/arxiv-sanity-mcp","env":{"DATABASE_URL":"postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp"}}' --scope local
```

### Database State Verification

```bash
# Check migration state
cd /home/rookslog/workspace/projects/arxiv-sanity-mcp && .venv/bin/alembic current
# Expected: 008 (head)

# Check data exists
.venv/bin/python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
async def check():
    engine = create_async_engine('postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp')
    async with engine.connect() as conn:
        for table in ['papers', 'interest_profiles', 'triage_states', 'collections', 'interest_signals']:
            r = await conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
            print(f'{table}: {r.scalar()}')
    await engine.dispose()
asyncio.run(check())
"
# Expected: papers: 126, interest_profiles: 1, triage_states: 98, collections: 1, interest_signals: 13
```

### Friction Document Template (10-FRICTION.md)

```markdown
# Phase 10: Agent Integration Test - Friction Report

**Session date:** YYYY-MM-DD
**MCP client:** Claude Code vX.X on dionysus
**Database:** arxiv_mcp (126 papers, Phase 5 corpus)

## Blockers (prevented workflow completion)

### B-01: [Title]
- **Description:** ...
- **Expected:** ...
- **Actual:** ...
- **Resolution:** Fixed in commit [hash] / Tracked for v0.2.0

## Friction (slowed down but workaround exists)

### F-01: [Title]
- **Description:** ...
- **Expected:** ...
- **Actual:** ...
- **Workaround:** ...
- **Resolution:** Fixed in commit [hash] / Tracked for v0.2.0

## Ergonomic (nice-to-have improvements)

### E-01: [Title]
- **Description:** ...
- **Improvement:** ...
- **Resolution:** Tracked for v0.2.0
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `claude_desktop_config.json` | `~/.claude.json` (local scope) or `.mcp.json` (project scope) | Claude Code 2.x | Server config is now per-project or user-scoped, not desktop-only |
| Manual JSON editing | `claude mcp add-json` CLI | Claude Code 2.x | Safer config management with scope control |
| No `cwd` support | `cwd` field in stdio config | MCP SDK recent | Servers can run in correct working directory |
| `--scope project` was default | `--scope local` is default | Claude Code 2.1.x | Local scope is default; project scope requires explicit flag |

**Deprecated/outdated:**
- The README currently shows `"command": "python"` -- should use absolute venv path for reliability
- The README shows config in `claude_desktop_config.json` format -- should also document `.mcp.json` for Claude Code project-scoped config

## Open Questions

1. **Does Claude Code pass `cwd` to the stdio server process?**
   - What we know: The `cwd` field is supported in `.mcp.json` and `add-json` configurations. Official docs show it in examples.
   - What's unclear: Whether `cwd` is honored when using the `add-json` CLI vs directly in `.mcp.json`. Testing will confirm.
   - Recommendation: Include `cwd` in config AND pass `DATABASE_URL` explicitly (belt and suspenders).

2. **Will Tool Search defer arxiv-discovery tools?**
   - What we know: Claude Code auto-enables Tool Search when MCP tools exceed 10% of context. 13 tools from arxiv-discovery alone may or may not trigger this.
   - What's unclear: Whether the threshold is hit with only one additional MCP server (sequential-thinking has 1 tool).
   - Recommendation: If tools aren't discovered, check `ENABLE_TOOL_SEARCH` setting. 13 tools is unlikely to trigger the 10% threshold with modern context windows.

3. **How will the agent handle the MCP resource @ mention syntax?**
   - What we know: Resources can be referenced as `@arxiv-discovery:paper://arxiv_id` in Claude Code prompts.
   - What's unclear: Whether the agent will naturally use this syntax or prefer tool calls.
   - Recommendation: Observe during session; this is a key friction signal.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio 0.24+ |
| Config file | `pyproject.toml` [tool.pytest.ini_options] |
| Quick run command | `pytest tests/test_mcp/ -x -q` |
| Full suite command | `pytest tests/ -x -q` |

### Phase Requirements -> Test Map

This phase has no formal requirement IDs. Its success criteria are primarily manual validation:

| Criterion | Behavior | Test Type | Automated Command | File Exists? |
|-----------|----------|-----------|-------------------|-------------|
| SC-1 | MCP server connects successfully | manual + smoke | `claude mcp list` | N/A |
| SC-2 | Agent completes full research workflow | manual | Human-observed session | N/A |
| SC-3 | Friction points documented | manual | Review 10-FRICTION.md | N/A |
| SC-4 | Setup guide validated from scratch | manual | Follow README steps | N/A |
| SC-5 | Critical fixes resolved or tracked | manual + unit | `pytest tests/test_mcp/ -x -q` | Existing |

### Sampling Rate

- **Per task commit:** `pytest tests/test_mcp/ -x -q` (for any fix(10): commits)
- **Per wave merge:** `pytest tests/ -x -q`
- **Phase gate:** Full suite green + all 5 E2E flows completed

### Wave 0 Gaps

None -- existing test infrastructure covers all phase requirements. This phase tests integration, not unit behavior. Any new tests created for `fix(10):` commits will use the existing test patterns in `tests/test_mcp/`.

## Sources

### Primary (HIGH confidence)
- Claude Code MCP documentation: https://code.claude.com/docs/en/mcp -- Full configuration syntax, scopes, env var expansion
- Project codebase: `src/arxiv_mcp/mcp/server.py`, `config.py`, tool modules -- Direct code inspection
- Project validation log: `.planning/phases/05-mcp-validation-iteration/validation-log.md` -- Known friction points from Phase 5
- Project milestone audit: `.planning/v1-MILESTONE-AUDIT.md` -- All 5 E2E flows verified at service level

### Secondary (MEDIUM confidence)
- FastMCP + Claude Code integration docs: https://gofastmcp.com/integrations/claude-code -- FastMCP-specific patterns
- Builder.io Claude Code MCP guide: https://www.builder.io/blog/claude-code-mcp-servers -- Third-party tutorial with examples

### Tertiary (LOW confidence)
- GitHub issue on cwd behavior: https://github.com/modelcontextprotocol/python-sdk/issues/1520 -- Community discussion on working directory handling

## Metadata

**Confidence breakdown:**
- MCP Configuration: HIGH -- verified against official docs and existing server on this machine (sequential-thinking pattern)
- Database State: HIGH -- verified via direct SQL queries (126 papers, 008 migration head)
- Known Friction Points: HIGH -- documented in Phase 5 validation log and milestone audit
- Tool Descriptions: HIGH -- read all 13 tool implementations directly
- cwd Handling: MEDIUM -- documented in official docs but not tested on this specific setup

**Research date:** 2026-03-14
**Valid until:** 2026-04-14 (stable -- Claude Code MCP API unlikely to change significantly)
