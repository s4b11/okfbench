"""App configuration from environment."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "OKFBench Chat"
    database_url: str = f"sqlite:///{(BASE_DIR / 'okfbench.db').as_posix()}"
    groq_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = ""
    llm_stub: bool = False
    top_k: int = Field(5, ge=1, le=20)
    okf_hop_depth: int = Field(2, ge=0, le=3)
    cors_origins: str = "*"

    @field_validator("database_url")
    @classmethod
    def postgres_driver(cls, value: str) -> str:
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return value.replace(prefix, "postgresql+psycopg://", 1)
        return value

    @property
    def use_stub_llm(self) -> bool:
        if self.llm_stub:
            return True
        return not (self.groq_api_key or self.openai_api_key)

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()
