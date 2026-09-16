"""Integration tests for producer winning-interval queries."""

from pathlib import Path

from app.database import Database
from app.importer import import_movies
from app.intervals import ProducerInterval, find_producer_interval_extremes


def test_consecutive_wins_define_all_tied_interval_extremes(tmp_path: Path) -> None:
    """Only adjacent wins count, including distinct wins from the same year."""
    database = _import_dataset(
        tmp_path,
        "year;title;studios;producers;winner\n"
        "2000;Ada First;Studio;Ada;yes\n"
        "2000;Ada Second;Studio;Ada;yes\n"
        "2001;Ada Losing Film;Studio;Ada;\n"
        "2003;Ada Third;Studio;Ada;yes\n"
        "2001;Bia First;Studio;Bia;yes\n"
        "2001;Bia Second;Studio;Bia;yes\n"
        "2004;Bia Third;Studio;Bia;yes\n"
        "2000;Cid First;Studio;Cid;yes\n"
        "2003;Cid Second;Studio;Cid;yes\n"
        "2005;Cid Third;Studio;Cid;yes\n"
        "1999;Solo Film;Studio;Solo;yes\n"
        "2010;Shared Winner;Studio;Dora and Evan;yes\n"
        "2013;Dora Winner;Studio;Dora;yes\n"
        "2013;Evan Another Winner;Studio;Evan;yes\n"
        "2013;Evan Winner;Studio;Evan;yes\n",
    )
    try:
        with database.session_factory() as session:
            extremes = find_producer_interval_extremes(session)

        assert extremes.min == (
            ProducerInterval("Ada", 0, 2000, 2000),
            ProducerInterval("Bia", 0, 2001, 2001),
            ProducerInterval("Evan", 0, 2013, 2013),
        )
        assert extremes.max == (
            ProducerInterval("Ada", 3, 2000, 2003),
            ProducerInterval("Bia", 3, 2001, 2004),
            ProducerInterval("Cid", 3, 2000, 2003),
            ProducerInterval("Dora", 3, 2010, 2013),
            ProducerInterval("Evan", 3, 2010, 2013),
        )
    finally:
        database.dispose()


def test_no_producer_with_two_wins_returns_empty_extremes(tmp_path: Path) -> None:
    """A producer's sole win and non-winning films create no interval."""
    database = _import_dataset(
        tmp_path,
        "year;title;studios;producers;winner\n"
        "2000;Alice Winner;Studio;Alice;yes\n"
        "2001;Alice Loser;Studio;Alice;\n"
        "2002;Bob Loser;Studio;Bob;\n"
        "2003;Carol Winner;Studio;Carol;yes\n",
    )
    try:
        with database.session_factory() as session:
            extremes = find_producer_interval_extremes(session)

        assert extremes.min == ()
        assert extremes.max == ()
    finally:
        database.dispose()


def _import_dataset(tmp_path: Path, contents: str) -> Database:
    csv_path = tmp_path / "movies.csv"
    csv_path.write_text(contents, encoding="utf-8")
    database = Database()
    database.create_schema()
    import_movies(database, csv_path)
    return database
