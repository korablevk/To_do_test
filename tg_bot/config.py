import os
from typing import Literal, Type

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def DATABASE_URL(self):
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    DJANGO_SECRET_KEY: str
    DJANGO_SUPERUSER_PASSWORD: str
    DJANGO_DEBUG: bool
    DJANGO_TIME_ZONE: str

    HOSTNAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    API_V1_STR: str
    WSGI_APP_URL: str

    BOT_LANGUAGE: str

    TG_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
