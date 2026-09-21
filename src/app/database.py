"""Database infrastructure owned by each application instance."""

from sqlite3 import Connection

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import ConnectionPoolEntry, StaticPool


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
        event.listen(self.engine, "connect", _register_casefold)

    def create_schema(self) -> None:
        """Create every mapped table for this database instance."""
        from app import models

        _ = models
        Base.metadata.create_all(self.engine)

    def dispose(self) -> None:
        """Release the single in-memory SQLite connection."""
        self.engine.dispose()


def _register_casefold(connection: Connection, record: ConnectionPoolEntry) -> None:
    """Preserve Unicode name ordering when SQLite sorts the interval response."""
    connection.create_function("casefold", 1, str.casefold, deterministic=True)
