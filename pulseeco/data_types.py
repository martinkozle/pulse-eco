from typing import Optional, TypedDict


class Sensor(TypedDict):
    sensorId: str
    position: str
    comments: str
    type: str
    description: str
    status: str


class DataValue(TypedDict):
    sensorId: str
    stamp: str
    year: Optional[int]
    type: str
    position: str
    value: str


class OverallValues(TypedDict):
    no2: str
    o3: str
    pm25: str
    pm10: str
    temperature: str
    humidity: str
    pressure: str
    noise_dba: str


class Overall(TypedDict):
    cityName: str
    values: OverallValues
