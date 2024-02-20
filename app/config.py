import logging
import os
from pathlib import Path
from typing import Optional, Any

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR = Path(__file__).resolve().parent
    API_V1_STR: str = "/api/v1"
    SECRET_KEY = os.environ.get("SECRET_KEY") or ''
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24

    LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
    JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False

    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_DB: str = os.environ.get("POSTGRES_DB")
    DATABASE_URI: Optional[PostgresDsn] = None

    @classmethod
    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        build = PostgresDsn.build(
            scheme="postgresdb",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )
        return build

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")

    class Config:
        env_file = ".env"


settings = Settings()
