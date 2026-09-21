"""End-to-end HTTP tests for the producer award-interval resource."""

import logging
from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.importer import CsvImportError
from app.main import create_app


@pytest.fixture
def write_csv(tmp_path: Path) -> Callable[[str], Path]:
    """Create the one replacement dataset used by an isolated application."""

    def _write_csv(contents: str) -> Path:
        csv_path = tmp_path / "movies.csv"
        csv_path.write_text(contents, encoding="utf-8")
        return csv_path

    return _write_csv


def test_intervals_endpoint_uses_the_versioned_default_dataset(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The default CSV is imported through startup and exposes its contract."""
    monkeypatch.delenv("MOVIELIST_CSV_PATH", raising=False)
    with TestClient(create_app()) as client:
        response = client.get("/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {
        "min": [
            {
                "producer": "Joel Silver",
                "interval": 1,
                "previousWin": 1990,
                "followingWin": 1991,
            }
        ],
        "max": [
            {
                "producer": "Matthew Vaughn",
                "interval": 13,
                "previousWin": 2002,
                "followingWin": 2015,
            }
        ],
    }


def test_intervals_endpoint_handles_ties_consecutive_wins_and_producer_lists(
    write_csv: Callable[[str], Path],
) -> None:
    """Use a replacement CSV with every relevant multi-win relationship.

    Mila's wins make intervals 1 and 3: using her first and last win would
    incorrectly produce 4. Ada's losing film between wins must be ignored.
    """
    csv_path = write_csv(
        "year;title;studios;producers;winner\n"
        "2000;Ada and Bea First;Studio;Ada and Bea;yes\n"
        "2000;Ada Second;Studio;Ada;yes\n"
        "2001;Carlos and Diana First;Studio;Carlos, Diana;yes\n"
        "2001;Combined First;Studio;Elena, Farah and Gina;yes\n"
        "2001;Combined Second;Studio;Elena, Farah and Gina;yes\n"
        "2001;Mila First;Studio;Mila;yes\n"
        "2001;Nora First;Studio;Nora;yes\n"
        "2002;Ada Losing Film;Studio;Ada;\n"
        "2002;Mila Second;Studio;Mila;yes\n"
        "2003;Unrelated Loser;Studio;Solo;\n"
        "2003;Ada Third;Studio;Ada;yes\n"
        "2004;Carlos Repeat;Studio;Carlos;yes\n"
        "2004;Diana Repeat;Studio;Diana;yes\n"
        "2004;Nora Second;Studio;Nora;yes\n"
        "2005;Mila Third;Studio;Mila;yes\n"
    )

    with TestClient(create_app(csv_path)) as client:
        response = client.get("/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {
        "min": [
            {
                "producer": "Ada",
                "interval": 0,
                "previousWin": 2000,
                "followingWin": 2000,
            },
            {
                "producer": "Elena",
                "interval": 0,
                "previousWin": 2001,
                "followingWin": 2001,
            },
            {
                "producer": "Farah",
                "interval": 0,
                "previousWin": 2001,
                "followingWin": 2001,
            },
            {
                "producer": "Gina",
                "interval": 0,
                "previousWin": 2001,
                "followingWin": 2001,
            },
        ],
        "max": [
            {
                "producer": "Ada",
                "interval": 3,
                "previousWin": 2000,
                "followingWin": 2003,
            },
            {
                "producer": "Carlos",
                "interval": 3,
                "previousWin": 2001,
                "followingWin": 2004,
            },
            {
                "producer": "Diana",
                "interval": 3,
                "previousWin": 2001,
                "followingWin": 2004,
            },
            {
                "producer": "Mila",
                "interval": 3,
                "previousWin": 2002,
                "followingWin": 2005,
            },
            {
                "producer": "Nora",
                "interval": 3,
                "previousWin": 2001,
                "followingWin": 2004,
            },
        ],
    }


def test_intervals_endpoint_returns_empty_lists_when_no_producer_repeats(
    write_csv: Callable[[str], Path],
) -> None:
    """Single winners and losing films create no interval records."""
    csv_path = write_csv(
        "year;title;studios;producers;winner\n"
        "2000;Alice Winner;Studio;Alice;yes\n"
        "2001;Alice Loser;Studio;Alice;\n"
        "2001;Bob Winner;Studio;Bob;yes\n"
        "2002;Carol Loser;Studio;Carol;\n"
        "2003;Diana Winner;Studio;Diana;yes\n"
    )

    with TestClient(create_app(csv_path)) as client:
        response = client.get("/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {"min": [], "max": []}


def test_normalized_producers_and_repeated_zero_intervals(
    write_csv: Callable[[str], Path],
) -> None:
    """Preserve literal names, deduplicate producers and sort tied zero pairs."""
    producers = (
        "zeta, Alpha, alpha, R & B, Brian Robbinsand Sharla Sumpter Bridgett, "
        "  Mary   Jane, and Alpha"
    )
    csv_path = write_csv(
        "\ufeffyear;title;studios;producers;winner\n"
        f"2000;Third;Studio;{producers}; YES \n"
        f"2000;First;Studio;{producers};yes\n"
        f"2000;Second;Studio;{producers};yes\n"
        "1999;Loser;Studio;Alpha;\n"
    )
    expected = [
        {
            "producer": producer,
            "interval": 0,
            "previousWin": 2000,
            "followingWin": 2000,
        }
        for producer in (
            "Alpha",
            "alpha",
            "Brian Robbinsand Sharla Sumpter Bridgett",
            "Mary Jane",
            "R & B",
            "zeta",
        )
    ]
    with TestClient(create_app(csv_path)) as client:
        response = client.get("/producers/intervals")

    assert response.status_code == 200
    assert response.json() == {"min": expected, "max": expected}


def test_configured_csv_explicit_precedence_and_application_isolation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Two live applications keep different datasets and configuration paths."""
    configured = tmp_path / "configured.csv"
    configured.write_text(
        "year;title;studios;producers;winner\n"
        "2003;Later;Studio;Ada;yes\n"
        "2000;Earlier;Studio;Ada;yes\n",
        encoding="utf-8",
    )
    explicit = tmp_path / "empty.csv"
    explicit.write_text("year;title;studios;producers;winner\n", encoding="utf-8")
    monkeypatch.setenv("MOVIELIST_CSV_PATH", str(configured))
    expected = {
        "producer": "Ada",
        "interval": 3,
        "previousWin": 2000,
        "followingWin": 2003,
    }

    with TestClient(create_app()) as configured_client:
        with TestClient(create_app(explicit)) as explicit_client:
            response = explicit_client.get("/producers/intervals")
            assert response.status_code == 200
            assert response.json() == {"min": [], "max": []}
            response = configured_client.get("/producers/intervals")
            assert response.status_code == 200
            assert response.json() == {"min": [expected], "max": [expected]}
        assert configured_client.get("/producers/intervals").json() == {
            "min": [expected],
            "max": [expected],
        }


def test_lifespan_logs_startup_import_statistics_and_shutdown(
    caplog: pytest.LogCaptureFixture, write_csv: Callable[[str], Path]
) -> None:
    """Expose operational lifecycle events through the real application startup."""
    csv_path = write_csv(
        "year;title;studios;producers;winner\n"
        "2000;First;Studio;Ada and Bea;yes\n"
        "2001;Second;Studio;Ada;\n"
    )
    caplog.set_level(logging.INFO, logger="app")

    with TestClient(create_app(csv_path)):
        pass

    records = caplog.records
    assert any(
        record.name == "app.main"
        and record.levelno == logging.INFO
        and record.getMessage() == "Application startup started"
        for record in records
    )
    assert any(
        record.name == "app.main"
        and record.levelno == logging.INFO
        and str(csv_path) in record.getMessage()
        for record in records
    )
    assert any(
        record.name == "app.importer"
        and record.levelno == logging.INFO
        and "CSV import started" in record.getMessage()
        for record in records
    )
    assert any(
        record.name == "app.importer"
        and record.levelno == logging.INFO
        and "CSV import completed" in record.getMessage()
        and "movies_imported=2" in record.getMessage()
        and "producers_loaded=2" in record.getMessage()
        for record in records
    )
    assert any(
        record.name == "app.main"
        and record.levelno == logging.INFO
        and record.getMessage() == "Application initialization completed"
        for record in records
    )
    assert any(
        record.name == "app.main"
        and record.levelno == logging.INFO
        and record.getMessage() == "Application shutdown completed"
        for record in records
    )


def test_invalid_csv_logs_import_failure_during_startup(
    caplog: pytest.LogCaptureFixture, tmp_path: Path
) -> None:
    """Keep CSV failures observable while preserving their original exception."""
    csv_path = tmp_path / "invalid.csv"
    csv_path.write_text("year;title;studios;producers\n", encoding="utf-8")
    caplog.set_level(logging.ERROR, logger="app")

    with pytest.raises(CsvImportError):
        with TestClient(create_app(csv_path)):
            pytest.fail("Invalid CSV must prevent startup")

    assert any(
        record.name == "app.main"
        and record.levelno == logging.ERROR
        and "CSV import failed during application startup" in record.getMessage()
        and str(csv_path) in record.getMessage()
        and record.exc_info is not None
        for record in caplog.records
    )


@pytest.mark.parametrize(
    ("invalid_contents", "message"),
    [
        (b"", "CSV file is empty"),
        (b"year;title;studios;producers\n", "missing columns: winner"),
        (
            b"year;title;studios;producers;winner;winner\n",
            "duplicated columns: winner",
        ),
        (
            b"year;title;studios;producers;winner\n2000;Film;Studio;Ada;\xff\n",
            "not valid UTF-8",
        ),
        *[
            (
                b"year;title;studios;producers;winner\n"
                b"2000;Valid;Studio;Ada;yes\n" + invalid_row,
                error,
            )
            for invalid_row, error in (
                (b'2001;Film;Studio;Ada;"yes', "Invalid CSV syntax"),
                (b'2001;Film;Studio;Ada;"yes"x\n', "Invalid CSV syntax"),
                (b"2001;Film;Studio;Ada;yes;extra\n", "too many columns"),
                (b"2001;Film;Studio;Ada\n", "missing value for winner"),
                (b"year;Film;Studio;Ada;yes\n", "year must be an integer"),
                (b"2001;Film;Studio;Ada;no\n", "winner must be 'yes' or empty"),
                (b"2001;Film;Studio;Ada,;yes\n", "invalid producers list"),
            )
        ],
    ],
)
def test_invalid_csv_aborts_startup_and_allows_clean_restart(
    tmp_path: Path, invalid_contents: bytes, message: str
) -> None:
    """Fail through real startup, then reuse the app with a repaired dataset."""
    csv_path = tmp_path / "movies.csv"
    csv_path.write_bytes(invalid_contents)
    application = create_app(csv_path)

    with pytest.raises(CsvImportError, match=message) as caught:
        with TestClient(application):
            pytest.fail("Invalid CSV must prevent startup")
    assert str(csv_path) in str(caught.value)

    csv_path.write_text(
        "year;title;studios;producers;winner\n2002;Replacement;Studio;Ada;yes\n",
        encoding="utf-8",
    )
    with TestClient(application) as client:
        response = client.get("/producers/intervals")
        assert response.status_code == 200
        assert response.json() == {"min": [], "max": []}
