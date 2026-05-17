from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    UPI_ID: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()