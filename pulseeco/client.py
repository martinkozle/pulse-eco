from __future__ import annotations

from typing import TYPE_CHECKING

from .api import PulseEcoAPI
from .constants import PULSE_ECO_BASE_URL
from .models import DataValue, Overall, Sensor

if TYPE_CHECKING:
    import datetime

    import requests

    from .api.base import PulseEcoAPIBase
    from .enums import AveragePeriod, DataValueType


class PulseEcoClient:
    """High level pulse.eco client"""

    def __init__(
        self,
        auth: tuple[str, str] | None = None,
        base_url: str = PULSE_ECO_BASE_URL,
        session: requests.Session | None = None,
        pulse_eco_api: PulseEcoAPIBase | None = None,
    ) -> None:
        """Initialize the pulse.eco client

        :param auth: a tuple of (email, password), defaults to None
        :param base_url: the base URL of the API, defaults to
            'https://{city_name}.pulse.eco/rest/{end_point}'
        :param session: a requests session
            , use this to customize the session and add retries, defaults to None
        :param pulse_eco_api: a pulse.eco API wrapper, defaults to None
            , if set, the other parameters are ignored
        """
        self._pulse_eco_api: PulseEcoAPIBase
        if pulse_eco_api is None:
            self._pulse_eco_api = PulseEcoAPI(
                auth=auth, base_url=base_url, session=session
            )
        else:
            self._pulse_eco_api = pulse_eco_api

    def sensors(self, city_name: str) -> list[Sensor]:
        """Get all sensors for a city

        :param city_name: the city name
        :return: a list of sensors
        """
        return [
            Sensor.model_validate(sensor)
            for sensor in self._pulse_eco_api.sensors(city_name=city_name)
        ]

    def sensor(self, city_name: str, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID

        :param city_name: the city name
        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return Sensor.model_validate(
            self._pulse_eco_api.sensor(city_name=city_name, sensor_id=sensor_id)
        )

    def data_raw(
        self,
        city_name: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get raw data for a city

        :param city_name: the city name
        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type, defaults to None
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of data values
        """
        return [
            DataValue.model_validate(data_value)
            for data_value in self._pulse_eco_api.data_raw(
                city_name=city_name,
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        ]

    def avg_data(
        self,
        city_name: str,
        period: AveragePeriod,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get average data for a city

        :param city_name: the city name
        :param period: the period of the average data
        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of average data values
        """
        return [
            DataValue.model_validate(data_value)
            for data_value in self._pulse_eco_api.avg_data(
                city_name=city_name,
                period=period,
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        ]

    def data24h(self, city_name: str) -> list[DataValue]:
        """Get 24h data for a city

        The data values are sorted ascending by their timestamp.

        :param city_name: the city name
        :return: a list of data values for the past 24 hours
        """
        return [
            DataValue.model_validate(data_value)
            for data_value in self._pulse_eco_api.data24h(city_name=city_name)
        ]

    def current(self, city_name: str) -> list[DataValue]:
        """Get the last received valid data for each sensor in a city

        Will not return sensor data older than 2 hours.

        :param city_name: the city name
        :return: a list of current data values
        """
        return [
            DataValue.model_validate(data_value)
            for data_value in self._pulse_eco_api.current(city_name=city_name)
        ]

    def overall(self, city_name: str) -> Overall:
        """Get the current average data for all sensors per value for a city

        :param city_name: the city name
        :return: the overall data for the city
        """
        return Overall.model_validate(self._pulse_eco_api.overall(city_name=city_name))
