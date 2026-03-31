from __future__ import annotations

from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    """MCP Server configuration — loaded from environment variables or .env file."""

    # Database
    database_url: str = "sqlite:///./data/pm_team_hub.db"

    # ChromaDB
    chroma_persist_dir: str = "./data/chroma"

    # Skills directory (relative to project root)
    skills_dir: str = os.getenv(
        "SKILLS_DIR",
        str(Path(__file__).resolve().parent.parent / "skills"),
    )

    # Agents directory
    agents_dir: str = os.getenv(
        "AGENTS_DIR",
        str(Path(__file__).resolve().parent.parent / "agents"),
    )

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: str = "*"

    # Auth (simple JWT for small team)
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
