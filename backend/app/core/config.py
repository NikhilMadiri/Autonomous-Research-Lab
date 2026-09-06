from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Autonomous Research Lab API"
    app_version: str = "0.1.0"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://research:research@localhost:5432/research_lab"
    redis_url: str = "redis://localhost:6379/0"
    backend_cors_origins: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")
    @property
    def cors_origins(self) -> list[str]:
        return [x.strip() for x in self.backend_cors_origins.split(",") if x.strip()]

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

