import logging
import os
from pathlib import Path
from typing import Optional, Any

# from fastapi.security import OAuth2PasswordBearer
# from passlib.context import CryptContext
from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Any = Path(__file__).resolve().parent
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY") or ''
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 60 * 24

    LOG_LEVEL: int = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
    JSON_LOGS: bool = True if os.environ.get("JSON_LOGS", "0") == "1" else False

    POSTGRES_USER: str = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT: str = os.environ.get("POSTGRES_PORT")
    POSTGRES_NAME: str = os.environ.get("POSTGRES_NAME")
    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            print("Loading SQLALCHEMY_DATABASE_URI from .docker.env file ...")
            return v
        print("Creating SQLALCHEMY_DATABASE_URI from .env file ...")
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_HOST"),
            path=f"{values.data.get('POSTGRES_NAME') or ''}",
        )

    # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")

    class Config:
        env_file = ".env"


settings = Settings()
