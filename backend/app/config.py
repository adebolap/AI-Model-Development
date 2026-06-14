from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://logiflow:logiflow@localhost:5432/logiflow"
    environment: str = "development"
    google_client_id: str = ""
    google_client_secret: str = ""
    openai_api_key: str = ""
    stripe_secret_key: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
