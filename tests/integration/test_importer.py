"""Integration tests for CSV loading during the application lifespan."""

import csv
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import inspect, select

from app.database import Database
from app.importer import CsvImportError, import_movies
from app.main import DEFAULT_CSV_PATH, create_app
from app.models import Movie, Producer


def test_default_dataset_is_imported_when_no_path_is_configured(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The packaged dataset is located independently of the working directory."""
    monkeypatch.delenv("MOVIELIST_CSV_PATH", raising=False)
    monkeypatch.chdir(tmp_path)
    expected_movie_count = _csv_row_count(DEFAULT_CSV_PATH)
    application = create_app()

    assert application.state.csv_path == DEFAULT_CSV_PATH

    with TestClient(application):
        database = application.state.database
        assert set(inspect(database.engine).get_table_names()) == {
            "movie_producers",
            "movies",
            "producers",
        }
        with database.session_factory() as session:
            assert len(session.scalars(select(Movie)).all()) == expected_movie_count


def test_explicit_csv_paths_import_isolated_datasets(tmp_path: Path) -> None:
    """Each factory call keeps its CSV configuration and database independent."""
    first_csv = _write_csv(
        tmp_path / "first.csv",
        "year;title;studios;producers;winner\n"
        "2001; First Film ; Studio One ; Alice and Bob ; yes \n",
    )
    second_csv = _write_csv(
        tmp_path / "second.csv",
        "year;title;studios;producers;winner\n"
        "2002;Second Film;Studio Two;Carol;\n"
        "2003;Third Film;Studio Three;Carol;YES\n",
    )
    first_application = create_app(first_csv)
    second_application = create_app(second_csv)

    assert first_application.state.csv_path == first_csv
    assert second_application.state.csv_path == second_csv

    with TestClient(first_application):
        first_database = first_application.state.database
        with first_database.session_factory() as session:
            first_movies = session.scalars(select(Movie)).all()
            stored_movies = [
                (movie.year, movie.title, movie.winner) for movie in first_movies
            ]
            assert stored_movies == [(2001, "First Film", True)]
            assert sorted(producer.name for producer in first_movies[0].producers) == [
                "Alice",
                "Bob",
            ]

        with TestClient(second_application):
            second_database = second_application.state.database
            with second_database.session_factory() as session:
                stored_titles = [
                    movie.title for movie in session.scalars(select(Movie)).all()
                ]
                assert stored_titles == [
                    "Second Film",
                    "Third Film",
                ]
                assert session.scalars(select(Producer.name)).all() == ["Carol"]


def test_producer_lists_create_clean_shared_associations(tmp_path: Path) -> None:
    """Producer separators and incidental spacing are handled during app startup."""
    csv_path = _write_csv(
        tmp_path / "producers.csv",
        "year;title;studios;producers;winner\n"
        "2001;First Film;Studio; Alice  Example, Alice Example and Bob Example ;yes\n"
        "2002;Second Film;Studio;Alice Example, Carol Example and Dave Example;\n"
        "2003;Third Film;Studio;Alice Example, Bob Example, and Eve Example;yes\n"
        "2004;Fourth Film;Studio;Alice Example;\n",
    )
    application = create_app(csv_path)

    with TestClient(application):
        database = application.state.database
        with database.session_factory() as session:
            movies = session.scalars(select(Movie).order_by(Movie.year)).all()
            producers = session.scalars(select(Producer).order_by(Producer.name)).all()

            producer_names_by_movie = [
                sorted(producer.name for producer in movie.producers)
                for movie in movies
            ]
            assert producer_names_by_movie == [
                ["Alice Example", "Bob Example"],
                ["Alice Example", "Carol Example", "Dave Example"],
                ["Alice Example", "Bob Example", "Eve Example"],
                ["Alice Example"],
            ]
            assert [producer.name for producer in producers] == [
                "Alice Example",
                "Bob Example",
                "Carol Example",
                "Dave Example",
                "Eve Example",
            ]
            alice = next(
                producer for producer in producers if producer.name == "Alice Example"
            )
            assert sorted(movie.title for movie in alice.movies) == [
                "First Film",
                "Fourth Film",
                "Second Film",
                "Third Film",
            ]


def test_invalid_csv_rolls_back_every_row_in_the_transaction(tmp_path: Path) -> None:
    """A malformed later row cannot leave earlier rows persisted."""
    invalid_csv = _write_csv(
        tmp_path / "invalid.csv",
        "year;title;studios;producers;winner\n"
        "2001;Valid Film;Studio;Alice;yes\n"
        "2002;Invalid Film;Studio;Bob;maybe\n",
    )
    database = Database()
    try:
        database.create_schema()

        with pytest.raises(CsvImportError, match="winner must be 'yes' or empty"):
            import_movies(database, invalid_csv)

        with database.session_factory() as session:
            assert session.scalars(select(Movie)).all() == []
            assert session.scalars(select(Producer)).all() == []
    finally:
        database.dispose()


def _csv_row_count(csv_path: Path) -> int:
    with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
        return sum(1 for _ in csv.DictReader(csv_file, delimiter=";"))


def _write_csv(path: Path, contents: str) -> Path:
    path.write_text(contents, encoding="utf-8")
    return path
