"""FastAPI application factory and ASGI entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from app.database import Database


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Create and release the database owned by an application instance."""
    database: Database = application.state.database
    database.create_schema()
    try:
        yield
    finally:
        database.dispose()


def create_app(csv_path: Path | None = None) -> FastAPI:
    """Create an isolated application instance.

    The CSV path is accepted now to keep the factory contract stable. It will be
    used by the import lifecycle when CSV loading is introduced.
    """
    _ = csv_path
    application = FastAPI(
        title="Golden Raspberry Awards API",
        version="0.1.0",
        lifespan=lifespan,
    )
    application.state.database = Database()

    @application.get("/health")
    def health() -> dict[str, str]:
        """Report that the API process is available."""
        return {"status": "ok"}

    return application


app = create_app()
