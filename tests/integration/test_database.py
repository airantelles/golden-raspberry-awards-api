"""Integration tests for the SQLAlchemy persistence infrastructure."""

from sqlalchemy import inspect, select

from app.database import Database
from app.models import Movie, Producer


def test_schema_is_created_and_shared_by_independent_sessions() -> None:
    """The in-memory database persists mapped relations across sessions."""
    database = Database()
    try:
        database.create_schema()

        inspector = inspect(database.engine)
        assert set(inspector.get_table_names()) == {
            "movie_producers",
            "movies",
            "producers",
        }

        with database.session_factory() as session:
            movie = Movie(
                year=1990,
                title="A Film",
                studios="A Studio",
                winner=True,
            )
            movie.producers.append(Producer(name="A Producer"))
            session.add(movie)
            session.commit()

        with database.session_factory() as session:
            stored_movie = session.scalar(select(Movie))
            assert stored_movie is not None
            assert stored_movie.producers[0].name == "A Producer"

    finally:
        database.dispose()
