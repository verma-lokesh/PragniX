from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Navora"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "mysql+pymysql://root:root@localhost:3306/navora"

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_DATABASE: str = "navora"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root"

    LLM_PROVIDER: str = "none"
    LLM_API_KEY: str | None = None
    LLM_MODEL: str = "claude-sonnet-4-6"
    TAVILY_API_KEY: str | None = None

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str | None = None
    LANGCHAIN_PROJECT: str = "navora"

    OTEL_ENDPOINT: str | None = None

    MODEL_ARTIFACT_PATH: str = "backend/ml/artifacts"


@lru_cache
def get_settings() -> Settings:
    return Settings()
