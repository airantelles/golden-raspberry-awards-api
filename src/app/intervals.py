"""Queries for consecutive winning intervals of movie producers."""

import logging

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import Movie, Producer, movie_producers
from app.schemas import ProducerIntervalExtremesResponse, ProducerIntervalResponse

logger = logging.getLogger(__name__)


def find_producer_interval_extremes(
    session: Session,
) -> ProducerIntervalExtremesResponse:
    """Return tied extrema from consecutive wins of every producer.

    The window is partitioned per producer and ordered by the stable movie order
    defined for the dataset. Rows without a previous win are excluded after the
    window expression is evaluated.
    """
    logger.debug("Producer interval extremes calculation started")
    previous_win = (
        func.lag(Movie.year)
        .over(
            partition_by=Producer.id,
            order_by=(Movie.year, Movie.title, Movie.id),
        )
        .label("previous_win")
    )
    winning_rows = (
        select(
            Producer.name.label("producer"),
            Movie.year.label("following_win"),
            previous_win,
        )
        .select_from(movie_producers)
        .join(Producer, Producer.id == movie_producers.c.producer_id)
        .join(Movie, Movie.id == movie_producers.c.movie_id)
        .where(Movie.winner.is_(True))
        .cte("winning_rows")
    )
    interval_rows = (
        select(
            winning_rows.c.producer,
            (winning_rows.c.following_win - winning_rows.c.previous_win).label(
                "interval"
            ),
            winning_rows.c.previous_win,
            winning_rows.c.following_win,
        )
        .where(winning_rows.c.previous_win.is_not(None))
        .cte("interval_rows")
    )
    bounds = select(
        func.min(interval_rows.c.interval).label("minimum"),
        func.max(interval_rows.c.interval).label("maximum"),
    ).cte("bounds")
    is_min = interval_rows.c.interval == bounds.c.minimum
    is_max = interval_rows.c.interval == bounds.c.maximum
    extremes = (
        select(interval_rows, is_min.label("is_min"), is_max.label("is_max"))
        .join(bounds, or_(is_min, is_max))
        .distinct()
        .order_by(
            func.casefold(interval_rows.c.producer),
            interval_rows.c.producer,
            interval_rows.c.previous_win,
            interval_rows.c.following_win,
        )
    )

    result = ProducerIntervalExtremesResponse(min=[], max=[])
    for row in session.execute(extremes):
        interval = ProducerIntervalResponse(
            producer=row.producer,
            interval=row.interval,
            previous_win=row.previous_win,
            following_win=row.following_win,
        )
        if row.is_min:
            result.min.append(interval)
        # Independent flags preserve both lists when minimum equals maximum.
        if row.is_max:
            result.max.append(interval)
    logger.debug(
        "Producer interval extremes calculated: minimum_results=%d maximum_results=%d",
        len(result.min),
        len(result.max),
    )
    return result
