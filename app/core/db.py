import os

from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URI.unicode_string(), echo=True, future=True)


def get_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> AsyncSession:
    session = sessionmaker(
        engine, class_=Session, expire_on_commit=False
    )
    with session() as session:
        yield session
