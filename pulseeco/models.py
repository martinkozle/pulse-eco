from __future__ import annotations

import datetime  # noqa: TCH003
from typing import Any, Optional

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field
from typing_extensions import Annotated

from .enums import DataValueType, SensorStatus, SensorType  # noqa: TCH001


class Sensor(BaseModel):
    sensor_id: str = Field(alias="sensorId", description="The unique ID of the sensor")
    position: str = Field(
        description="Latitude and longitude GPS coordinates of the sensor"
    )
    comments: str = Field(description="Any other comments about the sensor")
    type: SensorType = Field(description="The type of the sensor")
    description: str = Field(description="Short description / nome")
    status: SensorStatus = Field(description="The current status of the sensor")


class DataValue(BaseModel):
    sensor_id: str = Field(alias="sensorId", description="The unique ID of the sensor")
    stamp: datetime.datetime = Field(
        description="Timestamp of when the measurement was taken"
    )
    type: DataValueType = Field(description="The type of the data value taken")
    position: Optional[str] = Field(  # noqa: UP007
        description="Latitude and longitude GPS coordinates of the sensor"
    )
    value: int = Field(description="The actual value of the measurement taken")
    year: Optional[int] = Field(  # noqa: UP007
        default=None,
        description="Year when the measurement was taken"
        ", not included with newer data, prefer stamp",
    )


def validate_na(v: Any) -> Any | None:  # noqa: ANN401
    """Validate `N/A` value."""
    if v == "N/A":
        return None
    return v


OverallValue = Annotated[Optional[int], BeforeValidator(validate_na)]


class OverallValues(BaseModel):
    model_config = ConfigDict(extra="allow")

    no2: OverallValue = None
    no2_ppb: OverallValue = None
    o3: OverallValue = None
    so2: OverallValue = None
    co: OverallValue = None
    co_ppb: OverallValue = None
    nh3: OverallValue = None
    nh3_ppm: OverallValue = None
    nh3_ppb: OverallValue = None
    pm25: OverallValue = None
    pm10: OverallValue = None
    pm1: OverallValue = None
    temperature: OverallValue = None
    humidity: OverallValue = None
    pressure: OverallValue = None
    noise: OverallValue = None
    noise_dba: OverallValue = None
    gas_resistance: OverallValue = Field(None, alias="gasResistance")


class Overall(BaseModel):
    city_name: str = Field(alias="cityName", description="The city name")
    values: OverallValues = Field(description="The overall values for the city")
