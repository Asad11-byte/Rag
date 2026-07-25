from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Look for a local .env two levels up from this file (backend/.env),
# but don't error if it's not found — on Vercel, config comes from
# real environment variables set in the dashboard, not this file.
_LOCAL_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    Rag_APP_NAME: str = "AI Agent Security RAG"
    APP_VERSION: str = "1.0.0"

    GROQ_API_KEY: str
    JINA_API_KEY: str

    QDRANT_API_KEY: str
    QDRANT_URL: str

    model_config = SettingsConfigDict(
        env_file=_LOCAL_ENV_FILE if _LOCAL_ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()