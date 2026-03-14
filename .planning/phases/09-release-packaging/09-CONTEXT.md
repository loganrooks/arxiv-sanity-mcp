# Phase 9: Release Packaging - Context

**Gathered:** 2026-03-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Make the project distributable: legally licensed, documented for users (not designers), hosted on GitHub with CI, and tagged as v0.1.0. A new user can find, install, configure, and run the MCP server from the README alone. No new features, no code changes beyond metadata and CI configuration.

</domain>

<decisions>
## Implementation Decisions

### License
- MIT License at repo root
- Project license (distinct from per-paper content licenses governed by ADR-0003)
- MIT chosen for maximum adoption — standard for Python tools, no copyleft, compatible with all downstream use

### GitHub Repository
- Name: `arxiv-sanity-mcp` (honors arxiv-sanity heritage, matches directory name)
- Account: `loganrooks` (gh CLI authenticated, has `repo` + `workflow` scopes)
- URL: `https://github.com/loganrooks/arxiv-sanity-mcp`
- Visibility: Public (consistent with ADR-0004, all dependencies are open-source)
- No existing remote configured — repo must be created fresh and history pushed

### README
- Complete rewrite of existing design-phase bootstrapping README
- Primary audience: researchers who want to use this as an MCP server for arXiv paper discovery
- Secondary audience: MCP tool shoppers evaluating whether to add this server
- Required sections (from SC-2): project description, feature overview, installation instructions, quick-start guide, MCP server configuration example, link to design docs
- Must be honest about prerequisites (PostgreSQL, Python 3.13+, migration setup)
- Feature overview should highlight: 10 MCP tools, 4 resources, 3 prompts, 493 tests passing, content normalization with rights gating

### pyproject.toml Metadata
- Author: Logan Rooks
- License: MIT (field + classifier)
- Repository URL: `https://github.com/loganrooks/arxiv-sanity-mcp`
- Keywords: arxiv, mcp, research, discovery, papers, academic, model-context-protocol
- Classifiers: Python 3.13, Development Status 3-Alpha, Topic Scientific/Engineering, License MIT
- Package name stays `arxiv-mcp` (already established in imports and CLI entry point)

### CHANGELOG
- Keep a Changelog format (https://keepachangelog.com)
- v0.1.0 entry summarizing capabilities from Phases 1-8
- Categories: Added (all features are new for first release)
- Group by functional domain: Ingestion, Search & Discovery, Workflow, Interest Modeling, Enrichment, Content Normalization, MCP Interface

### CI Pipeline
- GitHub Actions (`.github/workflows/ci.yml`)
- Python 3.13 only (matches `requires-python = ">=3.13"`)
- PostgreSQL 16 service container with test database
- Steps: checkout → setup Python → install deps → create DB user + extensions → alembic upgrade → pytest → ruff check
- Triggers: push to `main`, pull requests to `main`
- No deployment step (local-first tool, not a hosted service)

### v0.1.0 Tag
- Git tag `v0.1.0` on the final release commit (after CI is green)
- Tag only after all other SC items are satisfied

### Claude's Discretion
- README exact prose, section ordering beyond the required elements
- CHANGELOG entry granularity (per-phase vs per-capability)
- CI job naming and caching strategy
- pyproject.toml classifier completeness
- Whether to add a `.github/CONTRIBUTING.md` or `SECURITY.md` (not required by SC but nice to have — bias toward minimal)

</decisions>

<specifics>
## Specific Ideas

- The existing README.md is a design-phase bootstrapping document ("This repository is being initialized as an exploration-first project..."). It should be preserved in `docs/` or replaced entirely — the new README is for USERS, not designers.
- The `docs/` directory (01-11 numbered design documents + ADRs) should remain as-is. README links to it for those who want architectural depth.
- Package name `arxiv-mcp` vs repo name `arxiv-sanity-mcp`: this mismatch is intentional. The package name is what users `pip install`; the repo name honors heritage and is more discoverable.
- CI must replicate the test database setup from `conftest.py` — specifically the `arxiv_mcp` database user, tsvector extension, and alembic migrations through 008.

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `pyproject.toml`: Already has basic project metadata, build system (hatchling), dependencies, dev dependencies, pytest/ruff config. Needs metadata additions, not rewrite.
- `src/arxiv_mcp/config.py`: Settings class with database URL, API keys — documents what env vars the user needs to configure.
- `src/arxiv_mcp/cli.py`: CLI entry point — README quick-start should reference CLI commands.
- `src/arxiv_mcp/mcp/server.py`: MCP server entry point — README needs `mcp run` or equivalent invocation.
- `alembic/`: Migration chain 001-008. CI and quick-start both need `alembic upgrade head`.

### Established Patterns
- Hatchling build system with `src/` layout — standard Python packaging
- `dependency-groups` for dev dependencies (PEP 735)
- `[project.scripts]` entry point: `arxiv-mcp = "arxiv_mcp.cli:cli"`
- Ruff for linting (target py313, line-length 100)
- pytest-asyncio with `asyncio_mode = "auto"`

### Integration Points
- No git remote exists — `git remote add origin` + initial push needed
- `.github/workflows/` directory doesn't exist — must be created
- `data/categories.toml` — static data file, needs to be included in wheel (already handled by hatchling src layout)
- `.env` file pattern for configuration — README must document required env vars

### Critical CI Setup Requirements
- PostgreSQL service container needs: user `arxiv_mcp`, password matching test config, database creation
- tsvector/full-text-search extension (built-in to PostgreSQL, but `CREATE EXTENSION` may be needed)
- `alembic upgrade head` must run before tests
- Tests use function-scoped async engine fixtures (no shared state issues in CI)

</code_context>

<failure_modes>
## Anticipated Failure Modes

### CI + PostgreSQL
- Test database setup is non-trivial: user creation, database creation, alembic migrations. If any step fails silently, tests will fail with connection errors, not helpful messages.
- Mitigation: CI should explicitly create user + DB before running alembic, with clear error output.

### README Quick-Start Complexity
- Installation requires: Python 3.13+, PostgreSQL running, database user created, `.env` configured, `alembic upgrade head`, then CLI/MCP server. Five steps before anything works.
- Mitigation: Be explicit about each prerequisite. Consider a "Prerequisites" section before "Installation."

### Package Name vs Repo Name Mismatch
- `pip install arxiv-mcp` from repo `arxiv-sanity-mcp`. Users might search PyPI for `arxiv-sanity-mcp`.
- Mitigation: README states both names clearly. Not publishing to PyPI in v0.1.0 (install from source/git), so this is a future concern.

### Python 3.13 Constraint
- Many users may not have Python 3.13. This limits early adoption.
- Mitigation: README states requirement prominently. This is intentional (codebase uses 3.13 features).

</failure_modes>

<deferred>
## Deferred Ideas

- PyPI publication — future release (v0.2.0+), not v0.1.0
- Docker image / docker-compose for one-command setup — would simplify quick-start dramatically but is a separate phase
- GitHub Release with pre-built artifacts — could be added after CI is working
- CONTRIBUTING.md, SECURITY.md — nice-to-have but not required for v0.1.0
- Homebrew/pipx installation method — depends on PyPI publication

</deferred>

---

*Phase: 09-release-packaging*
*Context gathered: 2026-03-13*
