from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, cast

import requests

from .constants import AVG_DATA_MAX_SPAN, DATA_RAW_MAX_SPAN, PULSE_ECO_BASE_URL
from .data_types import DataValueAvg, DataValueRaw, Overall, Sensor
from .utils import convert_datetime_to_str, split_datetime_span

if TYPE_CHECKING:
    import datetime


class PulseEcoAPI:
    """Low level unsafe pulse.eco API wrapper"""

    def __init__(
        self,
        auth: tuple[str, str] | None = None,
        base_url: str = PULSE_ECO_BASE_URL,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the pulse.eco API wrapper

        :param auth: a tuple of (email, password), defaults to None
        :param base_url: the base URL of the API, defaults to
            'https://{city_name}.pulse.eco/rest/{end_point}'
        :param session: a requests session
            , use this to customize the session and add retries, defaults to None
        """
        if session is not None:
            self._session = session
        else:
            self._session = requests.Session()
        if auth is not None:
            self._session.auth = auth
        self._base_url = base_url

    def __del__(self) -> None:
        """Close the session"""
        self._session.close()

    def _base_request(
        self, city_name: str, end_point: str, params: dict[str, Any] | None = None
    ) -> Any:  # noqa: ANN401
        """Make a request to the PulseEco API

        :param city_name: the city name
        :param end_point: an end point of the API
        :param params: get parameters, defaults to None
        :return: the response json
        """
        if params is None:
            params = {}
        url = self._base_url.format(city_name=city_name, end_point=end_point)
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def sensors(self, city_name: str) -> list[Sensor]:
        """Get all sensors for a city

        :param city_name: the city name
        :return: a list of sensors
        """
        return cast("list[Sensor]", self._base_request(city_name, "sensor"))

    def sensor(self, city_name: str, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID

        :param city_name: the city name
        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return cast(Sensor, self._base_request(city_name, f"sensor/{sensor_id}"))

    def data_raw(
        self,
        city_name: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValueRaw]:
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
        if sensor_id is None and type is None:
            warnings.warn(
                "Warning! If you encounter an error, "
                "you should probably specify either sensor_id or type.",
                stacklevel=2,
            )
        data: list[DataValueRaw] = []
        datetime_spans = split_datetime_span(from_, to, DATA_RAW_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                "sensorId": sensor_id,
                "type": type,
                "from": convert_datetime_to_str(from_temp),
                "to": convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            data_value = cast(
                "list[DataValueRaw]",
                self._base_request(city_name, "dataRaw", params=params),
            )
            data += data_value
        return data

    def avg_data(
        self,
        city_name: str,
        period: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str,
        sensor_id: str | None = None,
    ) -> list[DataValueAvg]:
        """Get average data for a city

        :param city_name: the city name
        :param period: the period of the average data (day, week, month)
        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of average data values
        """
        if period not in {"day", "week", "month"}:
            warnings.warn(
                "Warning! Invalid value for period. "
                "Should be one of: day, week, month",
                stacklevel=2,
            )
        data: list[DataValueAvg] = []
        datetime_spans = split_datetime_span(from_, to, AVG_DATA_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                "sensorId": sensor_id,
                "type": type,
                "from": convert_datetime_to_str(from_temp),
                "to": convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            data_value = cast(
                "list[DataValueAvg]",
                self._base_request(city_name, f"avgData/{period}", params=params),
            )
            data += data_value
        return data

    def data24h(self, city_name: str) -> list[DataValueRaw]:
        """Get 24h data for a city

        The data values are sorted ascending by their timestamp.

        :param city_name: the city name
        :return: a list of data values for the past 24 hours
        """
        return cast("list[DataValueRaw]", self._base_request(city_name, "data24h"))

    def current(self, city_name: str) -> list[DataValueRaw]:
        """Get the last received valid data for each sensor in a city

        Will not return sensor data older than 2 hours.

        :param city_name: the city name
        :return: a list of current data values
        """
        return cast("list[DataValueRaw]", self._base_request(city_name, "current"))

    def overall(self, city_name: str) -> Overall:
        """Get the current average data for all sensors per value for a city

        ## Example:

        ```python
        {
            'cityName': 'skopje',
            'values': {
                'no2': '22',
                'o3': '4',
                'pm25': '53',
                'pm10': '73',
                'temperature': '7',
                'humidity': '71',
                'pressure': '992',
                'noise_dba': '43'
            }
        }
        ```

        :param city_name: the city name
        :return: the overall data for the city
        """
        return cast(Overall, self._base_request(city_name, "overall"))
