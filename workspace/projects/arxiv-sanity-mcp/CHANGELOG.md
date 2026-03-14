# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-14

### Added

- **Ingestion**: OAI-PMH bulk harvesting with resumption tokens, arXiv API client for targeted queries, four time semantics (submission, update, announcement, OAI datestamp), incremental harvesting with checkpoints
- **Search and Discovery**: Full-text search by title/author/abstract/category/date with AND/OR composition, browse recent announcements by category, find related papers via lexical similarity, cursor-based pagination
- **Workflow State**: Named collections with add/remove, triage states (unseen/seen/shortlisted/dismissed/read/cite-later/archived) with batch operations, saved queries with on-demand re-run, watches with delta tracking ("what's new")
- **Interest Modeling**: Interest profiles with seed papers, saved queries, followed authors, and negative examples, signal provenance tracking (manual/suggestion/agent), suggestion engine from workflow activity
- **Ranking and Explanation**: Composable ranking pipeline with 5 signal scorers, per-result structured ranking explanations, ranker input inspection
- **Enrichment**: Lazy OpenAlex enrichment (topics, citations, FWCI, related works), bidirectional ID resolution (arXiv/DOI/OpenAlex), provenance tracking per enrichment record
- **Content Normalization**: Content variants (abstract/HTML/source-derived/PDF-derived markdown), rights-gated content serving per ADR-0003, Marker PDF parsing backend behind extensible adapter interface
- **MCP Interface**: 13 tools (search_papers, browse_recent, find_related_papers, get_paper, triage_paper, add_to_collection, create_watch, add_signal, batch_add_signals, create_profile, suggest_signals, enrich_paper, get_content_variant), 4 resource templates (paper, collection, profile, watch deltas), 3 prompts (daily-digest, literature-map-from-seeds, triage-shortlist)
- **CLI**: Full command-line interface mirroring all service capabilities with Rich output and JSON mode

[0.1.0]: https://github.com/loganrooks/arxiv-sanity-mcp/releases/tag/v0.1.0
