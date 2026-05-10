"""Configuration management using pydantic-settings"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(
        default="postgresql://localhost:5432/paper_analyzer",
        description="PostgreSQL connection URL",
    )

    crypto_secret_key: str = Field(
        default="default-secret-key-change-in-production",
        description="Encryption key for API keys",
    )

    # LLM Provider API Keys
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    anthropic_api_key: str | None = Field(default=None, alias="ANTHROPIC_API_KEY")
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    openrouter_api_key: str | None = Field(default=None, alias="OPENROUTER_API_KEY")
    mistral_api_key: str | None = Field(default=None, alias="MISTRAL_API_KEY")
    google_api_key: str | None = Field(default=None, alias="GOOGLE_API_KEY")
    nvidia_api_key: str | None = Field(default=None, alias="NVIDIA_API_KEY")
    semantic_scholar_key: str | None = Field(default=None, alias="S2_API_KEY")

    app_name: str = "Autonomous Paper Analyzer"
    debug: bool = False

    llm_temperature: float = 0.3
    llm_max_tokens: int = 2000

    # Gateway Settings
    # Encryption
    encryption_key: str | None = Field(default=None, alias="ENCRYPTION_KEY")

    # OAuth
    github_client_id: str | None = Field(default=None, alias="GITHUB_CLIENT_ID")
    github_client_secret: str | None = Field(default=None, alias="GITHUB_CLIENT_SECRET")
    google_client_id: str | None = Field(default=None, alias="GOOGLE_CLIENT_ID")
    google_client_secret: str | None = Field(default=None, alias="GOOGLE_CLIENT_SECRET")

    # Rate Limits
    default_rate_limit: int = Field(default=60, alias="DEFAULT_RATE_LIMIT")
    max_rate_limit: int = Field(default=1000, alias="MAX_RATE_LIMIT")

    # Cache
    cache_enabled: bool = Field(default=True, alias="CACHE_ENABLED")
    cache_ttl: int = Field(default=3600, alias="CACHE_TTL")

    # Redis (optional)
    redis_url: str | None = Field(default=None, alias="REDIS_URL")


settings = Settings()
