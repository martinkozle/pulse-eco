from __future__ import annotations

import datetime  # noqa: TCH003
from typing import Optional

from pydantic import BaseModel, Field

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


class OverallValues(BaseModel):
    no2: int
    o3: int
    pm25: int
    pm10: int
    temperature: int
    humidity: int
    pressure: int
    noise_dba: int


class Overall(BaseModel):
    city_name: str = Field(alias="cityName", description="The city name")
    values: OverallValues = Field(description="The overall values for the city")
