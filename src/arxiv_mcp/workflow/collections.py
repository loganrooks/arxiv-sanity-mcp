"""Collection service for organizing papers into named groups.

Provides full CRUD, membership management (add/remove/bulk), merge,
archive/unarchive, reverse lookup, and show with triage state display.
Follows the SearchService pattern: session_factory + settings DI.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import case, delete, func, literal, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from pydantic import BaseModel

from arxiv_mcp.config import Settings
from arxiv_mcp.db.models import Collection, CollectionPaper, Paper, TriageState
from arxiv_mcp.models.pagination import PageInfo, PaginatedResponse
from arxiv_mcp.models.workflow import CollectionSummary
from arxiv_mcp.workflow.util import slugify


class CollectionPaperView(BaseModel):
    """Pydantic view of a paper in a collection, including triage state."""

    arxiv_id: str
    title: str | None = None
    source: str
    added_at: datetime
    triage_state: str


class CollectionService:
    """Manages paper collections with membership tracking and triage display.

    All mutations update collection.updated_at. Paper counts are computed
    via subquery (no N+1 queries). Slug collisions raise ValueError.
    """

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        settings: Settings,
    ) -> None:
        self.session_factory = session_factory
        self.settings = settings

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    async def create_collection(
        self, name: str, source: str = "manual"
    ) -> CollectionSummary:
        """Create a new named collection. Raises ValueError on slug collision."""
        slug = slugify(name)
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            # Check for slug collision
            existing = await session.execute(
                select(Collection).where(Collection.slug == slug)
            )
            if existing.scalar_one_or_none() is not None:
                raise ValueError(f"Collection with slug '{slug}' already exists")

            coll = Collection(
                slug=slug,
                name=name,
                is_archived=False,
                created_at=now,
                updated_at=now,
            )
            session.add(coll)
            await session.commit()
            await session.refresh(coll)

            return CollectionSummary(
                slug=coll.slug,
                name=coll.name,
                paper_count=0,
                is_archived=coll.is_archived,
                created_at=coll.created_at,
                updated_at=coll.updated_at,
            )

    async def list_collections(
        self, include_archived: bool = False
    ) -> list[CollectionSummary]:
        """List all collections with paper counts.

        Excludes archived collections by default.
        Uses subquery for paper_count to avoid N+1.
        """
        paper_count_sq = (
            select(
                CollectionPaper.collection_id,
                func.count(CollectionPaper.paper_id).label("paper_count"),
            )
            .group_by(CollectionPaper.collection_id)
            .subquery()
        )

        stmt = (
            select(
                Collection,
                func.coalesce(paper_count_sq.c.paper_count, 0).label("paper_count"),
            )
            .outerjoin(
                paper_count_sq,
                Collection.id == paper_count_sq.c.collection_id,
            )
        )

        if not include_archived:
            stmt = stmt.where(Collection.is_archived.is_(False))

        stmt = stmt.order_by(Collection.created_at.desc())

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.all()

        return [
            CollectionSummary(
                slug=coll.slug,
                name=coll.name,
                paper_count=pc,
                is_archived=coll.is_archived,
                created_at=coll.created_at,
                updated_at=coll.updated_at,
            )
            for coll, pc in rows
        ]

    async def delete_collection(
        self, slug: str, purge_orphans: bool = False
    ) -> None:
        """Delete a collection. CASCADE removes memberships.

        With purge_orphans=True, also deletes papers that are no longer
        in any collection AND have no triage state (unseen).
        """
        async with self.session_factory() as session:
            coll = await self._get_collection_or_raise(session, slug)

            if purge_orphans:
                # Get paper IDs in this collection before deleting
                paper_ids_result = await session.execute(
                    select(CollectionPaper.paper_id).where(
                        CollectionPaper.collection_id == coll.id
                    )
                )
                paper_ids = [r[0] for r in paper_ids_result.all()]

            await session.delete(coll)
            await session.commit()

            if purge_orphans and paper_ids:
                # Delete papers not in any other collection and with no triage state
                for pid in paper_ids:
                    other_membership = await session.execute(
                        select(CollectionPaper.paper_id).where(
                            CollectionPaper.paper_id == pid
                        )
                    )
                    if other_membership.scalar_one_or_none() is None:
                        triage = await session.execute(
                            select(TriageState.paper_id).where(
                                TriageState.paper_id == pid
                            )
                        )
                        if triage.scalar_one_or_none() is None:
                            await session.execute(
                                delete(Paper).where(Paper.arxiv_id == pid)
                            )
                await session.commit()

    async def rename_collection(
        self, slug: str, new_name: str
    ) -> CollectionSummary:
        """Rename a collection. Updates slug and updated_at.

        Raises ValueError if the new slug already exists.
        """
        new_slug = slugify(new_name)

        async with self.session_factory() as session:
            coll = await self._get_collection_or_raise(session, slug)

            # Check for slug collision (unless renaming to same slug)
            if new_slug != slug:
                existing = await session.execute(
                    select(Collection).where(Collection.slug == new_slug)
                )
                if existing.scalar_one_or_none() is not None:
                    raise ValueError(
                        f"Collection with slug '{new_slug}' already exists"
                    )

            coll.name = new_name
            coll.slug = new_slug
            coll.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(coll)

            # Get paper count
            pc_result = await session.execute(
                select(func.count(CollectionPaper.paper_id)).where(
                    CollectionPaper.collection_id == coll.id
                )
            )
            paper_count = pc_result.scalar() or 0

            return CollectionSummary(
                slug=coll.slug,
                name=coll.name,
                paper_count=paper_count,
                is_archived=coll.is_archived,
                created_at=coll.created_at,
                updated_at=coll.updated_at,
            )

    # ------------------------------------------------------------------
    # Membership
    # ------------------------------------------------------------------

    async def add_papers(
        self, slug: str, arxiv_ids: list[str], source: str = "manual"
    ) -> int:
        """Add papers to a collection. Skips already-present papers (idempotent).

        Returns the number of papers actually added.
        """
        now = datetime.now(timezone.utc)
        added = 0

        async with self.session_factory() as session:
            coll = await self._get_collection_or_raise(session, slug)

            # Get existing memberships
            existing_result = await session.execute(
                select(CollectionPaper.paper_id).where(
                    CollectionPaper.collection_id == coll.id,
                    CollectionPaper.paper_id.in_(arxiv_ids),
                )
            )
            existing_ids = {r[0] for r in existing_result.all()}

            for arxiv_id in arxiv_ids:
                if arxiv_id not in existing_ids:
                    session.add(
                        CollectionPaper(
                            collection_id=coll.id,
                            paper_id=arxiv_id,
                            source=source,
                            added_at=now,
                        )
                    )
                    added += 1

            if added > 0:
                coll.updated_at = now
                await session.commit()

            return added

    async def remove_papers(self, slug: str, arxiv_ids: list[str]) -> int:
        """Remove papers from a collection. Returns count of papers removed."""
        async with self.session_factory() as session:
            coll = await self._get_collection_or_raise(session, slug)

            result = await session.execute(
                delete(CollectionPaper).where(
                    CollectionPaper.collection_id == coll.id,
                    CollectionPaper.paper_id.in_(arxiv_ids),
                ).returning(CollectionPaper.paper_id)
            )
            removed = len(result.all())

            if removed > 0:
                coll.updated_at = datetime.now(timezone.utc)
                await session.commit()

            return removed

    # ------------------------------------------------------------------
    # Show collection with triage state
    # ------------------------------------------------------------------

    async def show_collection(
        self,
        slug: str,
        sort_by: str = "added",
        page_size: int = 20,
        cursor_token: str | None = None,
    ) -> PaginatedResponse[CollectionPaperView]:
        """Show papers in a collection with triage state via LEFT JOIN.

        Supports sort_by: 'added' (default), 'paper_date', 'title'.
        Returns PaginatedResponse of CollectionPaperView items.
        """
        page_size = min(max(1, page_size), self.settings.max_page_size)

        triage_state_expr = case(
            (TriageState.state.is_(None), literal("unseen")),
            else_=TriageState.state,
        ).label("triage_state")

        stmt = (
            select(
                Paper.arxiv_id,
                Paper.title,
                CollectionPaper.source,
                CollectionPaper.added_at,
                triage_state_expr,
            )
            .join(CollectionPaper, Paper.arxiv_id == CollectionPaper.paper_id)
            .join(Collection, Collection.id == CollectionPaper.collection_id)
            .outerjoin(TriageState, TriageState.paper_id == Paper.arxiv_id)
            .where(Collection.slug == slug)
        )

        # Sorting
        if sort_by == "paper_date":
            stmt = stmt.order_by(Paper.submitted_date.desc(), Paper.arxiv_id.desc())
        elif sort_by == "title":
            stmt = stmt.order_by(Paper.title.asc(), Paper.arxiv_id.asc())
        else:
            # Default: sort by added_at desc
            stmt = stmt.order_by(
                CollectionPaper.added_at.desc(), Paper.arxiv_id.desc()
            )

        stmt = stmt.limit(page_size + 1)

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.all()

        has_next = len(rows) > page_size
        items_rows = rows[:page_size]

        items = [
            CollectionPaperView(
                arxiv_id=row.arxiv_id,
                title=row.title,
                source=row.source,
                added_at=row.added_at,
                triage_state=row.triage_state,
            )
            for row in items_rows
        ]

        page_info = PageInfo(has_next=has_next, next_cursor=None)
        return PaginatedResponse[CollectionPaperView](items=items, page_info=page_info)

    # ------------------------------------------------------------------
    # Merge
    # ------------------------------------------------------------------

    async def merge_collections(
        self, source_slug: str, target_slug: str
    ) -> CollectionSummary:
        """Merge source collection into target. Moves papers, deletes source.

        Skips papers already in the target (avoids PK violation).
        Returns updated target CollectionSummary.
        """
        now = datetime.now(timezone.utc)

        async with self.session_factory() as session:
            source = await self._get_collection_or_raise(session, source_slug)
            target = await self._get_collection_or_raise(session, target_slug)

            # Get papers in source
            source_papers_result = await session.execute(
                select(CollectionPaper).where(
                    CollectionPaper.collection_id == source.id
                )
            )
            source_papers = source_papers_result.scalars().all()

            # Get existing target paper IDs
            target_ids_result = await session.execute(
                select(CollectionPaper.paper_id).where(
                    CollectionPaper.collection_id == target.id
                )
            )
            target_ids = {r[0] for r in target_ids_result.all()}

            # Move non-duplicate papers
            for sp in source_papers:
                if sp.paper_id not in target_ids:
                    session.add(
                        CollectionPaper(
                            collection_id=target.id,
                            paper_id=sp.paper_id,
                            source=sp.source,
                            added_at=sp.added_at,
                        )
                    )

            # Delete source (CASCADE removes its memberships)
            await session.delete(source)
            target.updated_at = now
            await session.commit()

            # Get final paper count
            pc_result = await session.execute(
                select(func.count(CollectionPaper.paper_id)).where(
                    CollectionPaper.collection_id == target.id
                )
            )
            paper_count = pc_result.scalar() or 0

            return CollectionSummary(
                slug=target.slug,
                name=target.name,
                paper_count=paper_count,
                is_archived=target.is_archived,
                created_at=target.created_at,
                updated_at=target.updated_at,
            )

    # ------------------------------------------------------------------
    # Archive
    # ------------------------------------------------------------------

    async def archive_collection(self, slug: str) -> CollectionSummary:
        """Archive a collection (hidden from default listing)."""
        return await self._set_archived(slug, True)

    async def unarchive_collection(self, slug: str) -> CollectionSummary:
        """Unarchive a collection (visible in default listing)."""
        return await self._set_archived(slug, False)

    # ------------------------------------------------------------------
    # Reverse lookup
    # ------------------------------------------------------------------

    async def get_paper_collections(
        self, arxiv_id: str
    ) -> list[CollectionSummary]:
        """Return all collections a paper belongs to."""
        paper_count_sq = (
            select(
                CollectionPaper.collection_id,
                func.count(CollectionPaper.paper_id).label("paper_count"),
            )
            .group_by(CollectionPaper.collection_id)
            .subquery()
        )

        stmt = (
            select(
                Collection,
                func.coalesce(paper_count_sq.c.paper_count, 0).label("paper_count"),
            )
            .join(
                CollectionPaper,
                Collection.id == CollectionPaper.collection_id,
            )
            .outerjoin(
                paper_count_sq,
                Collection.id == paper_count_sq.c.collection_id,
            )
            .where(CollectionPaper.paper_id == arxiv_id)
        )

        async with self.session_factory() as session:
            result = await session.execute(stmt)
            rows = result.all()

        return [
            CollectionSummary(
                slug=coll.slug,
                name=coll.name,
                paper_count=pc,
                is_archived=coll.is_archived,
                created_at=coll.created_at,
                updated_at=coll.updated_at,
            )
            for coll, pc in rows
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    async def _get_collection_or_raise(
        self, session: AsyncSession, slug: str
    ) -> Collection:
        """Fetch collection by slug or raise ValueError."""
        result = await session.execute(
            select(Collection).where(Collection.slug == slug)
        )
        coll = result.scalar_one_or_none()
        if coll is None:
            raise ValueError(f"Collection not found: '{slug}'")
        return coll

    async def _set_archived(
        self, slug: str, archived: bool
    ) -> CollectionSummary:
        """Set the archived flag on a collection."""
        async with self.session_factory() as session:
            coll = await self._get_collection_or_raise(session, slug)
            coll.is_archived = archived
            coll.updated_at = datetime.now(timezone.utc)
            await session.commit()
            await session.refresh(coll)

            pc_result = await session.execute(
                select(func.count(CollectionPaper.paper_id)).where(
                    CollectionPaper.collection_id == coll.id
                )
            )
            paper_count = pc_result.scalar() or 0

            return CollectionSummary(
                slug=coll.slug,
                name=coll.name,
                paper_count=paper_count,
                is_archived=coll.is_archived,
                created_at=coll.created_at,
                updated_at=coll.updated_at,
            )
