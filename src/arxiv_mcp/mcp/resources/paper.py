"""Paper resource: paper://{arxiv_id}.

Provides a composite view of a paper including metadata, triage state,
enrichment data, and collection memberships.
"""

from __future__ import annotations

from mcp.server.fastmcp import Context
from sqlalchemy import select

from arxiv_mcp.db.models import Paper
from arxiv_mcp.mcp.server import AppContext, mcp


def _get_app(ctx: Context) -> AppContext:
    """Extract AppContext from MCP request context."""
    return ctx.request_context.lifespan_context


@mcp.resource("paper://{arxiv_id}")
async def paper_resource(arxiv_id: str, ctx: Context) -> dict:
    """Paper metadata including triage state, enrichment data, and collection memberships."""
    app = _get_app(ctx)

    # Get paper from DB
    async with app.session_factory() as session:
        result = await session.execute(
            select(Paper).where(Paper.arxiv_id == arxiv_id)
        )
        paper = result.scalar_one_or_none()

    if paper is None:
        return {"error": f"Paper not found: {arxiv_id}"}

    # Get triage state
    triage_state = await app.triage.get_triage_state(arxiv_id)

    # Get enrichment status
    enrichment_record = await app.enrichment.get_enrichment_status(arxiv_id)
    enrichment_data = None
    if enrichment_record is not None:
        enrichment_data = {
            "openalex_id": enrichment_record.openalex_id,
            "doi": enrichment_record.doi,
            "cited_by_count": enrichment_record.cited_by_count,
            "fwci": enrichment_record.fwci,
            "status": enrichment_record.status,
            "source_api": enrichment_record.source_api,
            "enriched_at": str(enrichment_record.enriched_at) if enrichment_record.enriched_at else None,
        }

    # Get collection memberships
    collections = await app.collections.get_paper_collections(arxiv_id)
    collections_data = [c.model_dump(mode="json") for c in collections]

    # Get available content variants (type + converted_at, without full content)
    content_variants = await app.content.list_variants(arxiv_id)

    return {
        "arxiv_id": paper.arxiv_id,
        "title": paper.title,
        "authors_text": paper.authors_text,
        "abstract": paper.abstract,
        "categories": paper.categories,
        "primary_category": paper.primary_category,
        "submitted_date": str(paper.submitted_date) if paper.submitted_date else None,
        "updated_date": str(paper.updated_date) if paper.updated_date else None,
        "announced_date": str(paper.announced_date) if paper.announced_date else None,
        "doi": paper.doi,
        "license_uri": paper.license_uri,
        "triage_state": triage_state,
        "enrichment": enrichment_data,
        "collections": collections_data,
        "content_variants": content_variants,
    }
