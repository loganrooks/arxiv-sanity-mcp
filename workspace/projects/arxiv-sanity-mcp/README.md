# arXiv Discovery MCP

MCP server for arXiv paper discovery, triage, and monitoring with inspectable ranking.

## What This Is

arXiv Discovery MCP is a research discovery substrate inspired by [arxiv-sanity](https://arxiv-sanity-lite.com/). It helps researchers and AI agents discover, triage, and monitor arXiv papers through the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) -- exposing tools, resources, and prompts that integrate directly into Claude Desktop, Claude Code, or any MCP-compatible client.

Unlike "chat with papers" wrappers, this system provides explicit interest modeling, inspectable ranking explanations, and structured workflow state. You build an interest profile from seed papers, followed authors, and saved queries. The system uses that profile to rank search results, surface new papers, and explain why each result scored the way it did.

The project tracks content provenance and respects reuse constraints per content type. All ranking signals are transparent: you can see exactly which interest signals contributed to each paper's score.

## Features

### MCP Tools (13)

**Discovery**
- `search_papers` -- Full-text search with optional profile-ranked results
- `browse_recent` -- Browse recent papers by arXiv category
- `find_related_papers` -- Find papers related to one or more seed papers
- `get_paper` -- Retrieve full metadata for a single paper

**Workflow**
- `triage_paper` -- Mark papers as shortlisted, seen, or dismissed
- `add_to_collection` -- Add papers to named collections (auto-creates)
- `create_watch` -- Create a saved query that monitors for new papers

**Interest & Enrichment**
- `add_signal` -- Add an interest signal (seed paper, followed author, etc.)
- `batch_add_signals` -- Add multiple interest signals at once
- `create_profile` -- Create a named interest profile
- `suggest_signals` -- Get profile expansion suggestions based on usage patterns
- `enrich_paper` -- Fetch citation counts, FWCI, and topics from OpenAlex

**Content**
- `get_content_variant` -- Retrieve paper content (abstract, HTML, or PDF-to-markdown) with rights gating

### MCP Resources (4)

- `paper://{arxiv_id}` -- Paper metadata, triage state, enrichment, and content variants
- `collection://{slug}` -- Collection contents with pagination
- `profile://{slug}` -- Interest profile with all signals
- `watch://{slug}/deltas` -- New papers since last check

### MCP Prompts (3)

- `daily-digest` -- Workflow guidance for reviewing new papers across watches
- `literature-map-from-seeds` -- Workflow for building a literature map from seed papers
- `triage-shortlist` -- Workflow for reviewing and triaging a collection

### CLI

All MCP capabilities are mirrored in a full CLI (`arxiv-mcp`) for terminal workflows, scripting, and debugging.

### Test Coverage

493 tests passing across ingestion, search, workflow, interest modeling, enrichment, content normalization, and MCP integration.

## Prerequisites

- **Python 3.13+** (uses 3.13 language features)
- **PostgreSQL 16+** (must be running and accessible)
- **Git** (for cloning the repository)

## Installation

```bash
git clone https://github.com/loganrooks/arxiv-sanity-mcp.git
cd arxiv-sanity-mcp
pip install -e .
```

For development (tests, linting):

```bash
pip install -e .
pip install pytest pytest-asyncio pytest-cov pytest-timeout respx ruff
```

## Database Setup

1. Create the database user and databases:

```bash
sudo -u postgres psql -c "CREATE USER arxiv_mcp WITH PASSWORD 'arxiv_mcp_dev';"
sudo -u postgres psql -c "CREATE DATABASE arxiv_mcp OWNER arxiv_mcp;"
sudo -u postgres psql -c "CREATE DATABASE arxiv_mcp_test OWNER arxiv_mcp;"
```

2. Create a `.env` file in the project root (or set environment variables):

```
DATABASE_URL=postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp
```

3. Run database migrations:

```bash
alembic upgrade head
```

## Quick Start

Once installed and the database is set up, try these commands:

```bash
# Harvest a paper by arXiv ID
arxiv-mcp harvest fetch 2301.00001

# Search for papers
arxiv-mcp search query "attention mechanism"

# Browse recent papers in a category
arxiv-mcp search browse --category cs.AI

# Create a collection
arxiv-mcp collection create "reading-list"

# Triage a paper
arxiv-mcp triage mark 2301.00001 shortlisted
```

## MCP Server Configuration

Add this to your Claude Desktop config (`claude_desktop_config.json`) or Claude Code MCP settings:

```json
{
  "mcpServers": {
    "arxiv-discovery": {
      "command": "python",
      "args": ["-m", "arxiv_mcp.mcp"],
      "cwd": "/path/to/arxiv-sanity-mcp",
      "env": {
        "DATABASE_URL": "postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp"
      }
    }
  }
}
```

Replace `/path/to/arxiv-sanity-mcp` with the actual path to your cloned repository.

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp` | PostgreSQL connection string |
| `OPENALEX_EMAIL` | No | (empty) | Email for OpenAlex polite pool (recommended; increases rate limit from 1 to 10 req/s) |
| `OPENALEX_API_KEY` | No | (empty) | OpenAlex API key for enrichment |
| `DEPLOYMENT_MODE` | No | `local` | `local` or `hosted` -- controls content license enforcement |

## Design Documents

Architectural documentation is in the [`docs/`](docs/) directory:

| Document | Description |
|----------|-------------|
| [01 - Project Vision](docs/01-project-vision.md) | Goals and product values |
| [02 - Product Principles](docs/02-product-principles.md) | Design principles and constraints |
| [03 - Design Space](docs/03-design-space.md) | Retrieval and ranking options explored |
| [04 - Reference Designs](docs/04-reference-designs.md) | Systems studied for design inspiration |
| [05 - Architecture Hypotheses](docs/05-architecture-hypotheses.md) | Architectural bets and rationale |
| [06 - MCP Surface Options](docs/06-mcp-surface-options.md) | MCP interface design decisions |
| [07 - Data Sources & Content Rights](docs/07-data-sources-content-rights.md) | arXiv data access and licensing |
| [08 - Evaluation & Experiments](docs/08-evaluation-and-experiments.md) | Testing methodology |
| [09 - Roadmap](docs/09-roadmap.md) | Development phases |
| [10 - Open Questions](docs/10-open-questions.md) | Unresolved design questions |
| [11 - Sources](docs/11-sources.md) | External references |

### Architecture Decision Records

- **ADR-0001** -- Exploration-first architecture
- **ADR-0002** -- Metadata-first, lazy enrichment
- **ADR-0003** -- License and provenance first
- **ADR-0004** -- MCP as workflow substrate

See [`docs/adrs/`](docs/adrs/) for full details.

## License

[MIT](LICENSE)
