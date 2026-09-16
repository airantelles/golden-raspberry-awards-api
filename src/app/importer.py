"""CSV validation and persistence for the movie awards dataset."""

import csv
import re
from collections.abc import Iterable
from pathlib import Path

from sqlalchemy.orm import Session

from app.database import Database
from app.models import Movie, Producer

EXPECTED_COLUMNS = ("year", "title", "studios", "producers", "winner")
_PRODUCER_SEPARATOR = re.compile(r"\s*,\s*(?:and\s+)?|\s+and\s+")


class CsvImportError(ValueError):
    """Raised when a dataset cannot be imported safely."""


def import_movies(database: Database, csv_path: Path) -> None:
    """Validate and import one CSV dataset in a single database transaction."""
    resolved_path = csv_path.expanduser().resolve()
    if not resolved_path.is_file():
        raise CsvImportError(f"CSV file does not exist: {resolved_path}")

    try:
        with resolved_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            _validate_header(reader, resolved_path)

            with database.session_factory.begin() as session:
                producers_by_name: dict[str, Producer] = {}
                for row in reader:
                    _import_row(
                        session,
                        row,
                        csv_path=resolved_path,
                        line_number=reader.line_num,
                        producers_by_name=producers_by_name,
                    )
    except OSError as error:
        message = f"Could not read CSV file {resolved_path}: {error}"
        raise CsvImportError(message) from error


def _validate_header(reader: csv.DictReader[str], csv_path: Path) -> None:
    fieldnames = reader.fieldnames
    if fieldnames is None:
        raise CsvImportError(f"CSV file is empty: {csv_path}")

    normalized_fieldnames = [
        field.strip() if field is not None else "" for field in fieldnames
    ]
    missing_columns = set(EXPECTED_COLUMNS).difference(normalized_fieldnames)
    duplicated_columns = {
        column
        for column in normalized_fieldnames
        if normalized_fieldnames.count(column) > 1
    }
    if missing_columns or duplicated_columns:
        details: list[str] = []
        if missing_columns:
            details.append(f"missing columns: {', '.join(sorted(missing_columns))}")
        if duplicated_columns:
            details.append(
                f"duplicated columns: {', '.join(sorted(duplicated_columns))}"
            )
        raise CsvImportError(f"Invalid CSV header in {csv_path}: {'; '.join(details)}")

    reader.fieldnames = normalized_fieldnames


def _import_row(
    session: Session,
    row: dict[str | None, str | list[str] | None],
    *,
    csv_path: Path,
    line_number: int,
    producers_by_name: dict[str, Producer],
) -> None:
    if None in row:
        raise CsvImportError(
            f"Invalid CSV row {line_number} in {csv_path}: too many columns"
        )

    values = _required_values(row, csv_path=csv_path, line_number=line_number)
    movie = Movie(
        year=_parse_year(values["year"], csv_path=csv_path, line_number=line_number),
        title=values["title"],
        studios=values["studios"],
        winner=_parse_winner(
            values["winner"], csv_path=csv_path, line_number=line_number
        ),
    )
    for producer_name in _parse_producers(
        values["producers"], csv_path=csv_path, line_number=line_number
    ):
        producer = producers_by_name.get(producer_name)
        if producer is None:
            producer = Producer(name=producer_name)
            producers_by_name[producer_name] = producer
        movie.producers.append(producer)
    session.add(movie)


def _required_values(
    row: dict[str | None, str | list[str] | None], *, csv_path: Path, line_number: int
) -> dict[str, str]:
    values: dict[str, str] = {}
    for column in EXPECTED_COLUMNS:
        value = row.get(column)
        if not isinstance(value, str):
            raise CsvImportError(
                f"Invalid CSV row {line_number} in {csv_path}: "
                f"missing value for {column}"
            )
        normalized_value = value.strip()
        if column != "winner" and not normalized_value:
            raise CsvImportError(
                f"Invalid CSV row {line_number} in {csv_path}: empty value for {column}"
            )
        values[column] = normalized_value
    return values


def _parse_year(value: str, *, csv_path: Path, line_number: int) -> int:
    try:
        return int(value)
    except ValueError as error:
        raise CsvImportError(
            f"Invalid CSV row {line_number} in {csv_path}: year must be an integer"
        ) from error


def _parse_winner(value: str, *, csv_path: Path, line_number: int) -> bool:
    normalized_value = value.casefold()
    if normalized_value in ("", "yes"):
        return normalized_value == "yes"
    raise CsvImportError(
        f"Invalid CSV row {line_number} in {csv_path}: winner must be 'yes' or empty"
    )


def _parse_producers(value: str, *, csv_path: Path, line_number: int) -> Iterable[str]:
    names = [" ".join(name.split()) for name in _PRODUCER_SEPARATOR.split(value)]
    if not all(names):
        raise CsvImportError(
            f"Invalid CSV row {line_number} in {csv_path}: invalid producers list"
        )
    return dict.fromkeys(names)
