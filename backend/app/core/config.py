"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "2ZTech Downloader"
    app_env: str = "development"
    app_debug: bool = True
    app_secret_key: str = Field(..., min_length=32)
    app_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:5173"
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://ztech:ztech_secure_password_change_me@localhost:5432/ztech_downloader"
    )

    # Redis
    redis_url: str = "redis://localhost:6379/0"
    redis_password: Optional[str] = None

    # JWT
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Workers & Downloads
    max_workers: int = 5
    max_retries: int = 3
    retry_base_delay_seconds: int = 5
    retry_max_delay_seconds: int = 300
    download_timeout_seconds: int = 3600
    max_concurrent_downloads_per_user: int = 10
    default_download_path: str = "/app/downloads"
    max_file_size_mb: int = 10240

    # Storage
    storage_backend: str = "local"
    storage_local_root: str = "/app/downloads"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window_seconds: int = 60

    # Security
    ssrf_block_private_ips: bool = True
    allowed_url_schemes: str = "http,https"

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def allowed_schemes(self) -> List[str]:
        return [s.strip().lower() for s in self.allowed_url_schemes.split(",") if s.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        if v < 1 or v > 50:
            raise ValueError("max_workers must be between 1 and 50")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
