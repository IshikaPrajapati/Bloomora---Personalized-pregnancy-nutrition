from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bloomora API"
    environment: str = "development"
    allow_origins: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
