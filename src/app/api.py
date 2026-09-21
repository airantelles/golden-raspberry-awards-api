"""REST endpoint registration for producer award intervals."""

from fastapi import FastAPI

from app.database import Database
from app.intervals import find_producer_interval_extremes
from app.schemas import ProducerIntervalExtremesResponse


def register_interval_routes(application: FastAPI) -> None:
    """Register the resource-oriented producer intervals endpoint."""

    @application.get(
        "/producers/intervals",
        response_model=ProducerIntervalExtremesResponse,
        response_model_by_alias=True,
    )
    def get_producer_interval_extremes() -> ProducerIntervalExtremesResponse:
        """Return all producer intervals tied at each global extreme."""
        database: Database = application.state.database
        with database.session_factory() as session:
            return find_producer_interval_extremes(session)
