from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Leafline Revamped"
    API_V1_PREFIX: str = "/api/v1"

    # DB – will use SQLite for now, can swap to Postgres later
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./leafline.db"

    # Auth / JWT
    SECRET_KEY: str = "super-secret-key-change-me"  # in production, override via env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
