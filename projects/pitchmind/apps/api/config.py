from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://pitchmind:pitchmind_dev@localhost:5433/pitchmind"
    redis_url: str = "redis://localhost:6380/0"
    supabase_url: str = ""
    supabase_jwt_secret: str = ""
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    stripe_price_id_pro: str = ""
    stripe_price_id_team: str = ""

    web_url: str = "http://localhost:3000"
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"


settings = Settings()

