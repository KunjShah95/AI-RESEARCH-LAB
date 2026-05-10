"""Database configuration"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./gateway.db")


class DatabaseSession:
    def __init__(self):
        self.engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def __iter__(self):
        yield self.SessionLocal()


_db_instance = None


def get_db():
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseSession()
    return iter([_db_instance])
