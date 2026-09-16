"""Pydantic response schemas for the public API."""

from pydantic import BaseModel, ConfigDict, Field


class ProducerIntervalResponse(BaseModel):
    """A consecutive pair of award wins for one producer."""

    model_config = ConfigDict(serialize_by_alias=True)

    producer: str
    interval: int
    previous_win: int = Field(serialization_alias="previousWin")
    following_win: int = Field(serialization_alias="followingWin")


class ProducerIntervalExtremesResponse(BaseModel):
    """The producer intervals tied at the global minimum and maximum."""

    min: list[ProducerIntervalResponse]
    max: list[ProducerIntervalResponse]
