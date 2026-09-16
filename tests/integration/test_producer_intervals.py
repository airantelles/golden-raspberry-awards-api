"""End-to-end HTTP tests for the producer award-interval resource."""

from collections.abc import Callable
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def write_csv(tmp_path: Path) -> Callable[[str], Path]:
    """Create the one replacement dataset used by an isolated application."""

    def _write_csv(contents: str) -> Path:
        csv_path = tmp_path / "movies.csv"
        csv_path.write_text(contents, encoding="utf-8")
        return csv_path

    return _write_csv


def test_intervals_endpoint_uses_the_versioned_default_dataset() -> None:
    """The default CSV is imported through startup and exposes its contract."""
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
