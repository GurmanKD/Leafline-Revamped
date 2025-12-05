from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Leafline Revamped"
    API_V1_PREFIX: str = "/api/v1"

    # DB – will use SQLite for now, can swap to Postgres later
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./leafline.db"

    class Config:
        env_file = ".env"


settings = Settings()
