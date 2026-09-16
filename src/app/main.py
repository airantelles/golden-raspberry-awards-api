"""FastAPI application factory and ASGI entry point."""

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.database import Database
from app.importer import import_movies

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "docs" / "Movielist.csv"


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Create and release the database owned by an application instance."""
    database: Database = application.state.database
    try:
        database.create_schema()
        import_movies(database, application.state.csv_path)
        yield
    finally:
        database.dispose()


def create_app(csv_path: Path | None = None) -> FastAPI:
    """Create an isolated application instance configured with one CSV dataset."""
    application = FastAPI(
        title="Golden Raspberry Awards API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.database = Database()
    application.state.csv_path = _resolve_csv_path(csv_path)

    @application.get("/health")
    def health() -> dict[str, str]:
        """Report that the API process is available."""
        return {"status": "ok"}

    return application


def _resolve_csv_path(csv_path: Path | None) -> Path:
    if csv_path is not None:
        return csv_path.expanduser().resolve()
    configured_path = os.getenv("MOVIELIST_CSV_PATH")
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return DEFAULT_CSV_PATH


app = create_app()
