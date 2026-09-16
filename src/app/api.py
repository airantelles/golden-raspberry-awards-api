"""REST endpoint registration for producer award intervals."""

from fastapi import FastAPI

from app.database import Database
from app.intervals import ProducerInterval, find_producer_interval_extremes
from app.schemas import ProducerIntervalExtremesResponse, ProducerIntervalResponse


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
            extremes = find_producer_interval_extremes(session)
        return ProducerIntervalExtremesResponse(
            min=[_to_response(interval) for interval in extremes.min],
            max=[_to_response(interval) for interval in extremes.max],
        )


def _to_response(interval: ProducerInterval) -> ProducerIntervalResponse:
    """Map a query result to its public representation."""
    return ProducerIntervalResponse(
        producer=interval.producer,
        interval=interval.interval,
        previous_win=interval.previous_win,
        following_win=interval.following_win,
    )
