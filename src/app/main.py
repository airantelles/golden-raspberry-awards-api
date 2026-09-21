"""FastAPI application factory and ASGI entry point."""

import logging
import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.api import register_interval_routes
from app.database import Database
from app.importer import import_movies

DEFAULT_CSV_PATH = Path(__file__).resolve().parents[2] / "docs" / "Movielist.csv"
SUPPORTED_LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Create and release the database owned by an application instance."""
    database: Database = application.state.database
    try:
        logger.info("Application startup started")
        logger.info("Dataset selected for import: %s", application.state.csv_path)
        try:
            database.create_schema()
        except Exception:
            logger.exception(
                "Application startup failed while creating database schema"
            )
            raise
        try:
            import_movies(database, application.state.csv_path)
        except Exception:
            logger.exception(
                "CSV import failed during application startup: dataset=%s",
                application.state.csv_path,
            )
            raise
        logger.info("Application initialization completed")
        yield
    finally:
        database.dispose()
        logger.info("Application shutdown completed")


def create_app(csv_path: Path | None = None) -> FastAPI:
    """Create an isolated application instance configured with one CSV dataset."""
    _configure_logging()
    application = FastAPI(
        title="Golden Raspberry Awards API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.database = Database()
    application.state.csv_path = _resolve_csv_path(csv_path)
    register_interval_routes(application)

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


def _configure_logging() -> None:
    """Configure application logging without replacing Uvicorn's loggers."""
    configured_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
    level = SUPPORTED_LOG_LEVELS.get(configured_level)
    if level is None:
        supported_levels = ", ".join(SUPPORTED_LOG_LEVELS)
        raise ValueError(
            f"Unsupported LOG_LEVEL {configured_level!r}; "
            f"expected one of: {supported_levels}"
        )

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    logging.getLogger("app").setLevel(level)


app = create_app()
