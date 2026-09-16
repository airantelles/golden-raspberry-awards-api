"""SQLAlchemy ORM models for the movie awards dataset."""

from __future__ import annotations

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

movie_producers = Table(
    "movie_producers",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("producer_id", ForeignKey("producers.id"), primary_key=True),
)


class Movie(Base):
    """A film in the awards dataset."""

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    studios: Mapped[str] = mapped_column(nullable=False)
    winner: Mapped[bool] = mapped_column(nullable=False)
    producers: Mapped[list[Producer]] = relationship(
        secondary=movie_producers,
        back_populates="movies",
    )


class Producer(Base):
    """A producer associated with one or more films."""

    __tablename__ = "producers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    movies: Mapped[list[Movie]] = relationship(
        secondary=movie_producers,
        back_populates="producers",
    )
