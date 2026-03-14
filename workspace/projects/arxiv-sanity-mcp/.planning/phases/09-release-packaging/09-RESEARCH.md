# Phase 9: Release Packaging - Research

**Researched:** 2026-03-13
**Domain:** Python packaging, GitHub Actions CI, open-source release preparation
**Confidence:** HIGH

## Summary

Phase 9 is a non-code phase: no new features, no source changes beyond metadata additions. The deliverables are LICENSE, README, pyproject.toml metadata, CHANGELOG, GitHub repo creation, CI workflow, and a v0.1.0 tag. All decisions are locked in CONTEXT.md -- the research task is to verify technical details for each deliverable.

The project already has a working pyproject.toml with hatchling build system, `src/` layout, and correct entry points. The primary technical challenge is the CI workflow: GitHub Actions must provision PostgreSQL 16, create the `arxiv_mcp` database user, run Alembic migrations (which use asyncpg via online mode), and execute 493 tests. A secondary challenge is that `ruff check` currently reports 98 errors (82 F401 unused imports, 8 F541, 7 F841, 3 E402, 2 F811) -- these must be resolved before CI can include lint checks.

**Primary recommendation:** Execute as three sequential tasks: (1) license + pyproject metadata + changelog, (2) README rewrite, (3) GitHub repo + CI + tag. Task 1 is pure file creation. Task 2 requires careful prose for installation instructions. Task 3 requires the ruff errors to be fixed first, then CI configuration.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- MIT License at repo root (project license, distinct from per-paper content licenses)
- GitHub repository: `arxiv-sanity-mcp` under `loganrooks` account, public, fresh creation
- README: Complete rewrite for users (not designers). Required sections: description, features, install, quick-start, MCP config, docs link
- pyproject.toml: author Logan Rooks, MIT license, repo URL, keywords [arxiv, mcp, research, discovery, papers, academic, model-context-protocol], classifiers [Python 3.13, Dev Status 3-Alpha, Topic Scientific/Engineering, License MIT]
- CHANGELOG: Keep a Changelog format, v0.1.0 entry grouped by functional domain
- CI: GitHub Actions, Python 3.13 only, PostgreSQL 16 service container, steps: checkout -> setup Python -> install deps -> create DB user + extensions -> alembic upgrade -> pytest -> ruff check
- v0.1.0 tag after all other SC items satisfied

### Claude's Discretion
- README exact prose, section ordering beyond required elements
- CHANGELOG entry granularity (per-phase vs per-capability)
- CI job naming and caching strategy
- pyproject.toml classifier completeness
- Whether to add CONTRIBUTING.md or SECURITY.md (bias toward minimal)

### Deferred Ideas (OUT OF SCOPE)
- PyPI publication (v0.2.0+)
- Docker image / docker-compose
- GitHub Release with pre-built artifacts
- CONTRIBUTING.md, SECURITY.md
- Homebrew/pipx installation method
</user_constraints>

## Standard Stack

### Core (all locked by CONTEXT.md)

| Tool | Version | Purpose | Why Standard |
|------|---------|---------|--------------|
| Hatchling | latest | Build backend | Already in pyproject.toml, `src/` layout support |
| GitHub Actions | v2 | CI/CD | Standard for GitHub-hosted projects |
| actions/checkout | v5 | Repo checkout | Current stable |
| actions/setup-python | v6 | Python 3.13 provisioning | Built-in pip caching support |
| PostgreSQL 16 | service container | Test database | Matches production PostgreSQL version |

### Supporting

| Tool | Version | Purpose | When to Use |
|------|---------|---------|-------------|
| ruff | >=0.9 | Linting in CI | Already in dev dependencies |
| pytest | >=8.0 | Test runner | Already in dev dependencies |
| alembic | >=1.14 | DB migrations in CI | Already in project dependencies |
| gh CLI | installed | GitHub repo creation | Authenticated on this machine (loganrooks, repo+workflow scopes) |

### Alternatives Considered

None -- all tools are locked decisions. No alternatives to evaluate.

**Installation:** No new dependencies. All tools are either already in pyproject.toml or are GitHub Actions marketplace actions.

## Architecture Patterns

### Deliverable Structure

```
arxiv-sanity-mcp/
  LICENSE                          # NEW - MIT license text
  CHANGELOG.md                     # NEW - Keep a Changelog format
  README.md                        # REWRITE - user-facing documentation
  pyproject.toml                   # MODIFY - add metadata fields
  .github/
    workflows/
      ci.yml                      # NEW - GitHub Actions CI workflow
```

### Pattern 1: pyproject.toml Metadata (PEP 621)

**What:** Complete project metadata in `[project]` table per PEP 621 spec.
**When to use:** All fields that are currently missing from the existing pyproject.toml.

The existing pyproject.toml already has: name, version, description, readme, requires-python, dependencies, scripts, build-system, dev dependency-groups, pytest config, ruff config.

**Fields to ADD:**
```toml
# Source: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
[project]
# ... existing fields ...
authors = [{name = "Logan Rooks"}]
license = "MIT"
keywords = ["arxiv", "mcp", "research", "discovery", "papers", "academic", "model-context-protocol"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.13",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Information Analysis",
]

[project.urls]
Homepage = "https://github.com/loganrooks/arxiv-sanity-mcp"
Repository = "https://github.com/loganrooks/arxiv-sanity-mcp"
Issues = "https://github.com/loganrooks/arxiv-sanity-mcp/issues"
Changelog = "https://github.com/loganrooks/arxiv-sanity-mcp/blob/main/CHANGELOG.md"
```

**PEP 639 note:** The `license` field should use SPDX identifier format (`"MIT"`) not the old `{text = "..."}` format. Hatchling supports PEP 639.

### Pattern 2: GitHub Actions CI with PostgreSQL Service Container

**What:** CI workflow with PostgreSQL 16 as a service container, health checks, and test database setup.
**When to use:** The `ci.yml` workflow file.

```yaml
# Source: https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: '3.13'
          cache: 'pip'
      - name: Install dependencies
        run: pip install -e ".[dev]"  # or equivalent
      - name: Create test database and user
        run: |
          PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE USER arxiv_mcp WITH PASSWORD 'arxiv_mcp_dev';"
          PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE arxiv_mcp OWNER arxiv_mcp;"
          PGPASSWORD=postgres psql -h localhost -U postgres -c "CREATE DATABASE arxiv_mcp_test OWNER arxiv_mcp;"
      - name: Run migrations
        run: alembic upgrade head
        env:
          DATABASE_URL: postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp
      - name: Run tests
        run: pytest
        env:
          DATABASE_URL: postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp
          TEST_DATABASE_URL: postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_test
      - name: Lint
        run: ruff check .
```

### Pattern 3: Keep a Changelog Format

**What:** Structured changelog per https://keepachangelog.com/en/1.1.0/
**When to use:** CHANGELOG.md file.

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - YYYY-MM-DD

### Added

- **Ingestion**: OAI-PMH bulk harvesting with resumption tokens ...
- **Search & Discovery**: Full-text search, browse recent, find related ...
...
```

### Anti-Patterns to Avoid

- **Over-engineering CI:** Do not add matrix builds, multiple Python versions, or deployment steps. Python 3.13 only, no deployment (local-first tool).
- **README as design doc:** The existing README is a design-phase document. The new README must be for USERS, not designers. Do not blend architectural discussion into installation instructions.
- **Committing .env to CI:** Use `env:` blocks in the workflow YAML, not `.env` file creation.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| License text | Write from memory | Copy MIT License template verbatim from OSI/SPDX | Exact wording matters legally |
| CI PostgreSQL | Docker compose in CI | GitHub Actions `services:` block | Native integration, health checks, port mapping |
| Python setup | Manual python install | `actions/setup-python@v6` | Handles version resolution, caching |
| Changelog format | Custom format | Keep a Changelog 1.1.0 | Established convention, parseable by tools |
| GitHub repo | Manual web UI | `gh repo create` | Scriptable, respects auth |

**Key insight:** Every deliverable in this phase has an established template or tool. Zero custom solutions needed.

## Common Pitfalls

### Pitfall 1: Ruff Lint Failures in CI

**What goes wrong:** CI fails on `ruff check .` because the codebase currently has 98 ruff errors (82 F401 unused imports, 8 F541, 7 F841, 3 E402, 2 F811).
**Why it happens:** Ruff was in dev dependencies but was not enforced as a pre-commit or CI gate until now. Errors accumulated across 8 phases.
**How to avoid:** Run `ruff check --fix .` to auto-fix the 88 fixable errors, then manually address the remaining ~10. The E402 errors in `cli.py` are intentional (Click group registration pattern) and should be suppressed with per-file-ignores in pyproject.toml.
**Warning signs:** CI passes tests but fails on lint step.

**Specific ruff configuration needed:**
```toml
[tool.ruff.lint.per-file-ignores]
"alembic/versions/*.py" = ["F401"]  # Alembic autogenerated imports
"src/arxiv_mcp/cli.py" = ["E402"]  # Click group registration after @cli definition
```

### Pitfall 2: Alembic Migrations Failing in CI

**What goes wrong:** `alembic upgrade head` fails because it cannot connect to the database or the user/database doesn't exist yet.
**Why it happens:** Alembic env.py loads `database_url` from `Settings` (pydantic-settings). In CI, the `DATABASE_URL` environment variable must be set BEFORE running alembic. The user `arxiv_mcp` must be created on the PostgreSQL service container BEFORE running migrations.
**How to avoid:** CI step ordering: (1) create user, (2) create databases, (3) set env vars, (4) run alembic. The alembic env.py uses asyncpg for online migrations, so psycopg2 is NOT needed in CI.
**Warning signs:** `connection refused` or `role "arxiv_mcp" does not exist` errors.

### Pitfall 3: Pydantic Settings Loading .env in CI

**What goes wrong:** `Settings` model tries to load `.env` file, which doesn't exist in CI. If there's no `DATABASE_URL` env var either, it falls back to the default `localhost:5432/arxiv_mcp` URL which may or may not work.
**Why it happens:** The default `database_url` in Settings is `postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp`. This happens to match what the CI service container will provide (if we create the user correctly).
**How to avoid:** The defaults in Settings actually work for CI IF the PostgreSQL service container is set up with the same user/password/db. Verify that CI creates: user `arxiv_mcp` with password `arxiv_mcp_dev`, databases `arxiv_mcp` and `arxiv_mcp_test`.

### Pitfall 4: Test Database vs Application Database

**What goes wrong:** Tests use `test_database_url` (pointing to `arxiv_mcp_test`), but alembic runs against `database_url` (pointing to `arxiv_mcp`). If only one database is created, either migrations or tests fail.
**Why it happens:** The test fixtures use `create_all` + manual tsvector trigger (not alembic), so the test database doesn't need alembic migrations. But the application database does.
**How to avoid:** Create BOTH databases in CI. Alembic only needs to run against the application database. Tests use `test_database_url` and create tables via `Base.metadata.create_all`.

### Pitfall 5: Dependency Installation Method

**What goes wrong:** `pip install -e .` installs the package but not dev dependencies. Tests and ruff are in `[dependency-groups] dev`.
**Why it happens:** PEP 735 dependency groups are not yet universally supported by `pip install`. The `--group` flag may not be available in the pip version shipped with Python 3.13.
**How to avoid:** Use `pip install -e . && pip install pytest pytest-asyncio pytest-cov pytest-timeout respx ruff mypy` or check if `pip install --group dev` works in the CI Python version. Alternative: add a `requirements-dev.txt` or use `pip install -e ".[dev]"` by converting dependency-groups to optional-dependencies.

**CRITICAL NOTE:** The current pyproject.toml uses `[dependency-groups]` (PEP 735), NOT `[project.optional-dependencies]`. Standard `pip install -e ".[dev]"` will NOT work. The CI step must either:
1. Install groups explicitly: `pip install -e . && pip install pytest pytest-asyncio pytest-cov pytest-timeout respx ruff`
2. Or use a tool that supports dependency groups (e.g., `pip install --group dev` if available in pip >= 25.0)

### Pitfall 6: Git Remote and Push Auth

**What goes wrong:** `git push` fails because SSH keys aren't configured or HTTPS auth isn't set up.
**Why it happens:** The project has no remote configured. `gh` CLI is authenticated with HTTPS token, but git operations protocol is set to SSH in `gh auth status`.
**How to avoid:** Use `gh repo create` which handles remote setup. Then verify `git push` works. If SSH-based, ensure SSH key is available. The `gh auth status` shows "Git operations protocol: ssh" -- so the push should use SSH transport.

### Pitfall 7: hatchling Package Data

**What goes wrong:** `data/categories.toml` is not included in the installed package because it's outside the `src/arxiv_mcp/` package directory.
**Why it happens:** The `[tool.hatch.build.targets.wheel] packages = ["src/arxiv_mcp"]` only includes files under `src/arxiv_mcp/`. The `data/` directory is at project root.
**How to avoid:** This is NOT a CI concern for v0.1.0 since users install from source (git clone, not pip install from wheel). The `config.py` resolves `categories_file` relative to `PROJECT_ROOT` which works for source installs. If PyPI publishing happens later, this needs fixing.

## Code Examples

### MIT License File

```text
MIT License

Copyright (c) 2026 Logan Rooks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### GitHub Repo Creation via gh CLI

```bash
# Create repo (public, no wiki/projects -- minimal)
gh repo create loganrooks/arxiv-sanity-mcp --public --source=. --remote=origin --push

# OR if you want to create first, then push:
gh repo create loganrooks/arxiv-sanity-mcp --public
git remote add origin https://github.com/loganrooks/arxiv-sanity-mcp.git
git push -u origin main
```

### Dependency Installation in CI

```bash
# Option A: Explicit dev deps (most reliable)
pip install -e .
pip install pytest pytest-asyncio pytest-cov pytest-timeout respx ruff

# Option B: If pip supports --group (pip >= 25.0)
pip install -e . --group dev
```

### PostgreSQL User/DB Setup in CI

```bash
# Run as postgres superuser via psql on the service container
PGPASSWORD=postgres psql -h localhost -U postgres <<SQL
CREATE USER arxiv_mcp WITH PASSWORD 'arxiv_mcp_dev';
CREATE DATABASE arxiv_mcp OWNER arxiv_mcp;
CREATE DATABASE arxiv_mcp_test OWNER arxiv_mcp;
GRANT ALL PRIVILEGES ON DATABASE arxiv_mcp TO arxiv_mcp;
GRANT ALL PRIVILEGES ON DATABASE arxiv_mcp_test TO arxiv_mcp;
SQL
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `license = {text = "..."}` | `license = "MIT"` (SPDX) | PEP 639, 2024 | Use SPDX identifier, not text blob |
| `setup.py` / `setup.cfg` | `pyproject.toml` (PEP 621) | 2022+ | Already using pyproject.toml |
| `extras_require` | `[dependency-groups]` (PEP 735) | 2024 | Already using dependency-groups |
| Travis CI | GitHub Actions | 2020+ | Standard for GitHub repos |
| `actions/setup-python@v4` | `@v6` | 2025 | Current stable with caching |
| `actions/checkout@v3` | `@v5` | 2024 | Current stable |

**Deprecated/outdated:**
- `setup.py`: Replaced by pyproject.toml; this project already uses hatchling
- `license = {file = "LICENSE"}` table format: Replaced by SPDX string per PEP 639

## Existing Codebase State (Critical for Planning)

### What Already Exists (DO NOT recreate)
- `pyproject.toml` with name, version, description, dependencies, build-system, scripts, ruff config, pytest config
- `.gitignore` with Python, IDE, testing, env exclusions
- `.env.example` (cannot read due to permissions, but exists at 655 bytes)
- `data/categories.toml` static data file
- Test suite: 493 tests across 54 files in 9 test directories
- CLI entry point: `arxiv-mcp` via `arxiv_mcp.cli:cli`
- MCP server: `python -m arxiv_mcp.mcp` (FastMCP with lifespan DI)

### What Must Be Created
- `LICENSE` file (does not exist)
- `CHANGELOG.md` (does not exist)
- `.github/workflows/ci.yml` (`.github/` directory does not exist)
- Git remote (no remote configured)
- Git tag `v0.1.0` (no tags exist)

### What Must Be Modified
- `pyproject.toml`: Add authors, license, keywords, classifiers, [project.urls]
- `README.md`: Complete rewrite (existing is design-phase bootstrapping doc)
- Ruff configuration: Add per-file-ignores for intentional patterns
- Source files: `ruff check --fix .` to resolve 88 auto-fixable lint errors, manual fixes for remaining ~10

### MCP Surface (for README feature list)
- **13 tools:** search_papers, browse_recent, find_related_papers, get_paper, triage_paper, add_to_collection, create_watch, add_signal, batch_add_signals, create_profile, suggest_signals, enrich_paper, get_content_variant
- **4 resources:** paper://{arxiv_id}, collection://{slug}, profile://{slug}, watch://{slug}/deltas
- **3 prompts:** daily-digest, literature-map-from-seeds, triage-shortlist
- **493 tests passing**

### Environment Variables for README Documentation
From `config.py` Settings class:
- `DATABASE_URL` (default: `postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp`)
- `TEST_DATABASE_URL` (default: same pattern with `_test` suffix)
- `OPENALEX_API_KEY` (optional, for enrichment)
- `OPENALEX_EMAIL` (optional, for polite pool)
- `DEPLOYMENT_MODE` (default: `local`, controls license enforcement)

## Open Questions

1. **pip and dependency-groups compatibility**
   - What we know: pyproject.toml uses `[dependency-groups]` (PEP 735). Standard pip may not support `--group` flag.
   - What's unclear: Which pip version first supports `--group`. The Python 3.13 setup-python action ships pip 24.x or 25.x.
   - Recommendation: Use explicit `pip install` of dev packages in CI as fallback. This is reliable regardless of pip version. If `--group` support is confirmed, switch to it.

2. **Git operations protocol (SSH vs HTTPS)**
   - What we know: `gh auth status` shows "Git operations protocol: ssh". The `gh` CLI is authenticated via HTTPS keyring token.
   - What's unclear: Whether SSH keys are configured for github.com on this machine.
   - Recommendation: Use `gh repo create --source=. --remote=origin --push` which handles auth automatically. If that fails, fall back to HTTPS remote URL.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0+ with pytest-asyncio (asyncio_mode = "auto") |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `pytest -x --timeout=30` |
| Full suite command | `pytest` |

### Phase Requirements -> Test Map

Phase 9 has no mapped requirement IDs. Success criteria ARE the requirements. Validation is file-existence and CI-green checks, not behavioral tests.

| SC | Behavior | Test Type | Automated Command | File Exists? |
|----|----------|-----------|-------------------|-------------|
| SC-1 | LICENSE file exists with MIT text | smoke | `test -f LICENSE && grep -q "MIT License" LICENSE` | n/a (file check) |
| SC-2 | README has required sections | smoke | `grep -q "Installation" README.md && grep -q "Quick Start" README.md` | n/a (file check) |
| SC-3 | pyproject.toml has metadata | smoke | `python -c "import tomllib; d=tomllib.load(open('pyproject.toml','rb')); assert 'authors' in d['project']"` | n/a (file check) |
| SC-4 | CHANGELOG exists with v0.1.0 | smoke | `grep -q "0.1.0" CHANGELOG.md` | n/a (file check) |
| SC-5 | GitHub repo exists | smoke | `gh repo view loganrooks/arxiv-sanity-mcp` | n/a (API check) |
| SC-6 | CI passes on push/PR | integration | `gh run list --workflow=ci.yml --limit=1` | n/a (CI check) |
| SC-7 | v0.1.0 tag exists | smoke | `git tag -l v0.1.0` | n/a (git check) |

### Sampling Rate
- **Per task commit:** Shell-based existence checks (file present, content verified)
- **Per wave merge:** Full `pytest` + `ruff check .` locally before pushing
- **Phase gate:** CI green on GitHub (SC-6), all other SC items verified

### Wave 0 Gaps
None -- this phase does not add behavioral code. No new test files needed. Existing 493 tests must continue passing after ruff --fix changes.

## Sources

### Primary (HIGH confidence)
- [GitHub Actions PostgreSQL service containers](https://docs.github.com/en/actions/use-cases-and-examples/using-containerized-services/creating-postgresql-service-containers) - Service container config, health checks, port mapping
- [PEP 621 pyproject.toml specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/) - Metadata field syntax
- [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) - Authors, license (PEP 639 SPDX format), classifiers, URLs
- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) - Changelog format spec
- [actions/setup-python](https://github.com/actions/setup-python) - Python 3.13 setup, pip caching
- [SPDX MIT License](https://spdx.org/licenses/MIT.html) - License identifier and text

### Secondary (MEDIUM confidence)
- [GitHub Actions Python CI 2025](https://ber2.github.io/posts/2025_github_actions_python/) - Modern CI patterns
- Local codebase inspection of pyproject.toml, config.py, conftest.py, alembic/env.py - Direct verification of project state

### Tertiary (LOW confidence)
- pip `--group` flag availability for PEP 735 dependency-groups - Not verified against specific pip version

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all tools are already in use or are GitHub/Python ecosystem standards
- Architecture: HIGH - file creation tasks with established templates
- Pitfalls: HIGH - verified by direct codebase inspection (ruff errors counted, alembic env.py read, conftest.py analyzed)
- CI configuration: HIGH for service container pattern (official docs), MEDIUM for dependency installation (PEP 735 tool support unclear)

**Research date:** 2026-03-13
**Valid until:** 2026-04-13 (stable domain, no fast-moving dependencies)
