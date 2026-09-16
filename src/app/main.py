"""FastAPI application factory and ASGI entry point."""

from pathlib import Path

from fastapi import FastAPI


def create_app(csv_path: Path | None = None) -> FastAPI:
    """Create an isolated application instance.

    The CSV path is accepted now to keep the factory contract stable. It will be
    used by the import lifecycle when CSV loading is introduced.
    """
    _ = csv_path
    application = FastAPI(title="Golden Raspberry Awards API", version="0.1.0")

    @application.get("/health")
    def health() -> dict[str, str]:
        """Report that the API process is available."""
        return {"status": "ok"}

    return application


app = create_app()
