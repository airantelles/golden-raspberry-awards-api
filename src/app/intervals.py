"""Queries for consecutive winning intervals of movie producers."""

import logging
from collections.abc import Iterable
from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Movie, Producer, movie_producers

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProducerInterval:
    """One consecutive pair of wins attributed to a producer."""

    producer: str
    interval: int
    previous_win: int
    following_win: int


@dataclass(frozen=True)
class ProducerIntervalExtremes:
    """All producer intervals tied at the global minimum and maximum."""

    min: tuple[ProducerInterval, ...]
    max: tuple[ProducerInterval, ...]


def find_producer_interval_extremes(session: Session) -> ProducerIntervalExtremes:
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
        .subquery()
    )
    interval_rows = select(
        winning_rows.c.producer,
        (winning_rows.c.following_win - winning_rows.c.previous_win).label("interval"),
        winning_rows.c.previous_win,
        winning_rows.c.following_win,
    ).where(winning_rows.c.previous_win.is_not(None))

    intervals = {
        ProducerInterval(
            producer=row.producer,
            interval=row.interval,
            previous_win=row.previous_win,
            following_win=row.following_win,
        )
        for row in session.execute(interval_rows)
    }
    if not intervals:
        logger.debug(
            "Producer interval extremes calculated: minimum_results=0 maximum_results=0"
        )
        return ProducerIntervalExtremes(min=(), max=())

    minimum = min(interval.interval for interval in intervals)
    maximum = max(interval.interval for interval in intervals)
    minimum_results = _sort_intervals(
        interval for interval in intervals if interval.interval == minimum
    )
    maximum_results = _sort_intervals(
        interval for interval in intervals if interval.interval == maximum
    )
    logger.debug(
        "Producer interval extremes calculated: minimum_results=%d maximum_results=%d",
        len(minimum_results),
        len(maximum_results),
    )
    return ProducerIntervalExtremes(
        min=minimum_results,
        max=maximum_results,
    )


def _sort_intervals(
    intervals: Iterable[ProducerInterval],
) -> tuple[ProducerInterval, ...]:
    return tuple(
        sorted(
            intervals,
            key=lambda interval: (
                interval.producer.casefold(),
                interval.producer,
                interval.previous_win,
                interval.following_win,
            ),
        )
    )
