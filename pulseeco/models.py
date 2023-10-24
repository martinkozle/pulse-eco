from __future__ import annotations

import datetime  # noqa: TCH003
from typing import Optional

from pydantic import BaseModel, Field

from .enums import DataValueType, SensorStatus, SensorType  # noqa: TCH001


class Sensor(BaseModel):
    sensor_id: str = Field(alias="sensorId")
    position: str
    comments: str
    type: SensorType
    description: str
    status: SensorStatus


class DataValue(BaseModel):
    sensor_id: str = Field(alias="sensorId")
    stamp: datetime.datetime
    type: DataValueType
    position: Optional[str]  # noqa: UP007
    value: int
    year: Optional[int] = None  # noqa: UP007


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
    city_name: str = Field(alias="cityName")
    values: OverallValues
