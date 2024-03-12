from __future__ import annotations

import asyncio
import inspect
import os
import warnings
from typing import TYPE_CHECKING, Any, List, cast

from pulseeco.constants import (
    AVG_DATA_MAX_SPAN,
    DATA_RAW_MAX_SPAN,
    PULSE_ECO_BASE_URL_FORMAT,
    PULSE_ECO_BASE_URL_FORMAT_ENV_KEY,
    PULSE_ECO_CITY_PASSWORD_ENV_KEY_FORMAT,
    PULSE_ECO_CITY_USERNAME_ENV_KEY_FORMAT,
    PULSE_ECO_PASSWORD_ENV_KEY,
    PULSE_ECO_USERNAME_ENV_KEY,
)
from pulseeco.utils import convert_datetime_to_str, split_datetime_span

from .base import PulseEcoAPIBase
from .data_types import DataValueAvg, DataValueRaw, Overall, Sensor
from .http_clients import _get_fallback_sync_client

if TYPE_CHECKING:
    import datetime

    from .http_clients import (
        ASYNC_CLIENT,
        CLIENT,
    )


def get_auth_from_env(city_name: str) -> tuple[str, str] | None:
    """Get the auth tuple from the environment variables.

    :param city_name: the city name
    :return: a tuple of (email, password) or None
    """
    city_upper_username_env_key = PULSE_ECO_CITY_USERNAME_ENV_KEY_FORMAT.format(
        city_name=city_name.upper()
    )
    city_upper_password_env_key = PULSE_ECO_CITY_PASSWORD_ENV_KEY_FORMAT.format(
        city_name=city_name.upper()
    )

    city_username_env_key = PULSE_ECO_CITY_USERNAME_ENV_KEY_FORMAT.format(
        city_name=city_name
    )
    city_password_env_key = PULSE_ECO_CITY_PASSWORD_ENV_KEY_FORMAT.format(
        city_name=city_name
    )

    for username_env_key in (
        city_upper_username_env_key,
        city_username_env_key,
        PULSE_ECO_USERNAME_ENV_KEY,
    ):
        if username_env_key in os.environ:
            username = os.environ[username_env_key]
            break
    else:
        return None

    for password_env_key in (
        city_upper_password_env_key,
        city_password_env_key,
        PULSE_ECO_PASSWORD_ENV_KEY,
    ):
        if password_env_key in os.environ:
            return username, os.environ[password_env_key]
    return None


class PulseEcoAPI(PulseEcoAPIBase):
    """Low level unsafe pulse.eco API wrapper."""

    def __init__(
        self,
        city_name: str,
        auth: tuple[str, str] | None = None,
        base_url: str = PULSE_ECO_BASE_URL_FORMAT,
        session: None = None,
        client: CLIENT | None = None,
        async_client: ASYNC_CLIENT | None = None,
    ) -> None:
        """Initialize the pulse.eco API wrapper.

        :param city_name: the city name
        :param auth: a tuple of (email, password), defaults to None
        :param base_url: the base URL of the API, defaults to
            'https://{city_name}.pulse.eco/rest/{end_point}'
        :param session: deprecated, use client and async_client instead
        :param client: a sync http client, supported types are:
            requests.Session, httpx.Client,
            defaults to None which uses a new requests.Session for each request,
            use a context managed session for better performance and resource management
        :param async_client: an async http client, supported types are:
            aiohttp.ClientSession, httpx.AsyncClient,
            defaults to None which will use the sync client
        """
        self.city_name = city_name

        if base_url is not None and PULSE_ECO_BASE_URL_FORMAT_ENV_KEY in os.environ:
            base_url = os.environ[PULSE_ECO_BASE_URL_FORMAT_ENV_KEY]

        if session is not None:
            warnings.warn(
                "The `session` parameter is deprecated. "
                "Use `client` and `async_client` instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        client = client if client is not None else session

        self._client: CLIENT

        if client is not None:
            self._client = client
        else:
            self._client = _get_fallback_sync_client()

        self._async_client = async_client

        if auth is None:
            auth = get_auth_from_env(city_name=city_name)

        self._auth = auth

        self._base_url = base_url

    def _base_request(
        self, end_point: str, params: dict[str, Any] | None = None
    ) -> Any:  # noqa: ANN401
        """Make a request to the PulseEco API.

        :param end_point: an end point of the API
        :param params: get parameters, defaults to None
        :return: the response json
        """
        if params is None:
            params = {}
        url = self._base_url.format(city_name=self.city_name, end_point=end_point)

        # httpx does not support auth None
        if self._auth is not None:
            response = self._client.get(url, params=params, auth=self._auth)
        else:
            response = self._client.get(url, params=params)
        response.raise_for_status()

        return response.json()

    async def _abase_request(
        self, end_point: str, params: dict[str, Any] | None = None
    ) -> Any:  # noqa: ANN401
        """Make an async request to the PulseEco API.

        :param end_point: an end point of the API
        :param params: get parameters, defaults to None
        :return: the response json
        """
        if self._async_client is None:
            return self._base_request(end_point, params)

        if params is None:
            params = {}

        url = self._base_url.format(city_name=self.city_name, end_point=end_point)

        response = await self._async_client.get(url, params=params)
        response.raise_for_status()

        # In case of aiohttp, the response.json() is a coroutine function
        if inspect.iscoroutinefunction(response.json):
            return await response.json()
        return response.json()

    def sensors(self) -> list[Sensor]:
        """Get all sensors for a city.

        :return: a list of sensors
        """
        return cast(List[Sensor], self._base_request("sensor"))

    async def asensors(self) -> list[Sensor]:
        """Get all sensors for a city.

        :return: a list of sensors
        """
        return cast(List[Sensor], await self._abase_request("sensor"))

    def sensor(self, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID

        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return cast(Sensor, self._base_request(f"sensor/{sensor_id}"))

    async def asensor(self, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID

        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return cast(Sensor, await self._abase_request(f"sensor/{sensor_id}"))

    def data_raw(
        self,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValueRaw]:
        """Get raw data for a city.

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
                List[DataValueRaw],
                self._base_request("dataRaw", params=params),
            )
            data += data_value
        return data

    async def adata_raw(
        self,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValueRaw]:
        """Get raw data for a city.

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
        coroutines: list[asyncio.Future[list[DataValueRaw]]] = []
        datetime_spans = split_datetime_span(from_, to, DATA_RAW_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                "sensorId": sensor_id,
                "type": type,
                "from": convert_datetime_to_str(from_temp),
                "to": convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            coroutines.append(
                cast(
                    "asyncio.Future[list[DataValueRaw]]",
                    self._abase_request("dataRaw", params=params),
                )
            )
        return [
            data
            for data_value in await asyncio.gather(*coroutines)
            for data in data_value
        ]

    def avg_data(
        self,
        period: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str,
        sensor_id: str | None = None,
    ) -> list[DataValueAvg]:
        """Get average data for a city.

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
                List[DataValueAvg],
                self._base_request(f"avgData/{period}", params=params),
            )
            data += data_value
        return data

    async def aavg_data(
        self,
        period: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str,
        sensor_id: str | None = None,
    ) -> list[DataValueAvg]:
        """Get average data for a city.

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
        coroutines: list[asyncio.Future[list[DataValueAvg]]] = []
        datetime_spans = split_datetime_span(from_, to, AVG_DATA_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                "sensorId": sensor_id,
                "type": type,
                "from": convert_datetime_to_str(from_temp),
                "to": convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            coroutines.append(
                cast(
                    "asyncio.Future[list[DataValueAvg]]",
                    self._abase_request(f"avgData/{period}", params=params),
                )
            )
        return [
            data
            for data_value in await asyncio.gather(*coroutines)
            for data in data_value
        ]

    def data24h(self) -> list[DataValueRaw]:
        """Get 24h data for a city.

        The data values are sorted ascending by their timestamp.

        :return: a list of data values for the past 24 hours
        """
        return cast(List[DataValueRaw], self._base_request("data24h"))

    async def adata24h(self) -> list[DataValueRaw]:
        """Get 24h data for a city.

        The data values are sorted ascending by their timestamp.

        :return: a list of data values for the past 24 hours
        """
        return cast(List[DataValueRaw], await self._abase_request("data24h"))

    def current(self) -> list[DataValueRaw]:
        """Get the last received valid data for each sensor in a city

        Will not return sensor data older than 2 hours.

        :return: a list of current data values
        """
        return cast(List[DataValueRaw], self._base_request("current"))

    async def acurrent(self) -> list[DataValueRaw]:
        """Get the last received valid data for each sensor in a city

        Will not return sensor data older than 2 hours.

        :return: a list of current data values
        """
        return cast(List[DataValueRaw], await self._abase_request("current"))

    def overall(
        self,
    ) -> Overall:
        """Get the current average data for all sensors per value for a city.

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

        :return: the overall data for the city
        """
        return cast(Overall, self._base_request("overall"))

    async def aoverall(
        self,
    ) -> Overall:
        """Get the current average data for all sensors per value for a city.

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

        :return: the overall data for the city
        """
        return cast(Overall, await self._abase_request("overall"))
