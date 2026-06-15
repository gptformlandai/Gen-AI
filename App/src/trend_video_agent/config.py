from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Trend-Aware Video Agent"
    app_env: str = "local"
    local_storage_dir: str = "./data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
