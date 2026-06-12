import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    url = os.environ.get("DATABASE_URL", "postgresql://pitchmind:pitchmind_dev@localhost:5433/pitchmind")
    return create_engine(url, pool_pre_ping=True)


@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False)
