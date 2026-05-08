# Phase 05: Deferred Items

## Pre-existing DB Fixture Issues

Multiple integration tests fail with `UniqueViolationError: duplicate key value violates unique constraint "pg_type_typname_nsp_index"` when trying to CREATE TABLE papers. This is a pre-existing test infrastructure issue where multiple test files try to create the same table types in the PostgreSQL test database within a single pytest session.

Affected test files:
- `tests/test_enrichment/test_models.py`
- `tests/test_search/test_pagination.py`
- `tests/test_search/test_service.py`
- `tests/test_workflow/test_collections.py`

Root cause: Session-scoped vs function-scoped async engine fixtures conflicting on table creation.

Not caused by Phase 05 changes. Not blocking any Phase 05 work.
