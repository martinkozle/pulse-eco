from __future__ import annotations

from typing import TypedDict


class Sensor(TypedDict):
    sensorId: str
    position: str
    comments: str
    type: str
    description: str
    status: str


class DataValueBase(TypedDict):
    sensorId: str
    stamp: str
    type: str
    value: str


class DataValueRaw(DataValueBase):
    position: str


class DataValueAvg(DataValueBase):
    position: None


class OverallValues(TypedDict):
    no2: str
    o3: str
    pm25: str
    pm10: str
    temperature: str
    humidity: str
    pressure: str
    noise_dba: str
    noise: int
    gasResistance: int


class Overall(TypedDict):
    cityName: str
    values: OverallValues
