"""Application configuration via Pydantic Settings.

Loads from environment variables and .env file. All settings have
sensible defaults for local development.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root: two levels up from this file (src/arxiv_mcp/config.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = (
        "postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp"
    )
    test_database_url: str = (
        "postgresql+asyncpg://arxiv_mcp:arxiv_mcp_dev@localhost:5432/arxiv_mcp_test"
    )

    # arXiv endpoints
    arxiv_oai_url: str = "https://oaipmh.arxiv.org/oai"
    arxiv_api_url: str = "https://export.arxiv.org/api/query"

    # Category configuration
    categories_file: str = "data/categories.toml"

    # Rate limiting
    harvest_rate_limit: float = 3.0  # seconds between arXiv API requests

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    # Workflow soft limits (warning thresholds)
    soft_limit_collections: int = 100
    soft_limit_saved_queries: int = 50
    soft_limit_watches: int = 20
    default_watch_cadence: str = "daily"
    export_default_path: str = "data/workflow_export.json"

    # Interest profile settings
    soft_limit_profiles: int = 50
    default_negative_weight: float = 0.3

    # Enrichment settings
    openalex_api_key: str = ""
    openalex_api_url: str = "https://api.openalex.org"
    openalex_email: str = ""  # Set for OpenAlex polite pool (10 req/s vs 1 req/s anonymous)
    enrichment_cooldown_days: int = 7
    enrichment_batch_size: int = 50
    enrichment_rate_limit: float = 5.0

    def load_categories(self) -> dict:
        """Load category configuration from TOML file.

        Returns a dict with 'defaults' and 'categories' keys.
        The categories_file path is resolved relative to the project root.
        """
        import tomllib

        categories_path = PROJECT_ROOT / self.categories_file
        with open(categories_path, "rb") as f:
            return tomllib.load(f)

    @property
    def configured_categories(self) -> list[str]:
        """Return flat list of all configured arXiv categories."""
        data = self.load_categories()
        categories = []
        for archive_cats in data.get("categories", {}).values():
            categories.extend(archive_cats)
        return categories

    @property
    def default_archives(self) -> list[str]:
        """Return list of archives to harvest by default."""
        data = self.load_categories()
        return data.get("defaults", {}).get("archives", [])


@lru_cache
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
