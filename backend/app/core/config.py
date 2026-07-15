from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project Root/
ROOT_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    # Application
    Rag_APP_NAME: str = "AI Agent Security RAG"
    APP_VERSION: str = "1.0.0"

    # APIs
    GROQ_API_KEY: str
    VOYAGE_API_KEY: str

    # Qdrant
    QDRANT_API_KEY: str
    QDRANT_URL: str

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()