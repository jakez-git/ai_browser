from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PathsSettings(BaseModel):
    knowledge_root: Path = Field(
        Path("z:/rag/knowledge_base"),
        description="Root directory to watch for knowledge base updates.",
    )
    models_dir: Path = Field(
        Path("z:/rag/models"),
        description="Directory containing local model artifacts (LLM/embeddings).",
    )


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="AI_BROWSER_", env_file=".env", env_file_encoding="utf-8")

    environment: str = Field("development", description="Runtime environment name")
    enable_watchdog: bool = Field(True, description="Enable filesystem watcher service")
    max_context_chunks: int = Field(5, ge=1, le=50, description="Maximum chunks to include in context")
    paths: PathsSettings = Field(default_factory=PathsSettings)


@lru_cache
def get_settings() -> AppSettings:
    """Return cached application settings instance."""

    return AppSettings()
