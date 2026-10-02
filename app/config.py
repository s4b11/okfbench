"""App configuration from environment."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "OKFBench Chat"
    database_url: str = f"sqlite:///{(BASE_DIR / 'okfbench.db').as_posix()}"
    groq_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "openai/gpt-oss-20b"
    llm_stub: bool = False
    top_k: int = 5
    okf_hop_depth: int = 2
    cors_origins: str = "*"

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
