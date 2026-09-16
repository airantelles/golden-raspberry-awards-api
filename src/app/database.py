"""Database infrastructure owned by each application instance."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    """Base class for the application's ORM models."""


class Database:
    """Create and manage an isolated in-memory SQLite database."""

    def __init__(self) -> None:
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False)

    def create_schema(self) -> None:
        """Create every mapped table for this database instance."""
        from app import models

        _ = models
        Base.metadata.create_all(self.engine)

    def dispose(self) -> None:
        """Release the single in-memory SQLite connection."""
        self.engine.dispose()
