from __future__ import annotations

from typing import TYPE_CHECKING

from pulseeco.api import PulseEcoAPI
from pulseeco.constants import PULSE_ECO_BASE_URL_FORMAT

from .models import DataValue, DataValues, Overall, Sensor, Sensors

if TYPE_CHECKING:
    import datetime

    from pulseeco.api.base import PulseEcoAPIBase
    from pulseeco.api.http_clients import ASYNC_CLIENT, CLIENT

    from .enums import AveragePeriod, DataValueType


class PulseEcoClient:
    """High level pulse.eco client."""

    def __init__(
        self,
        city_name: str,
        auth: tuple[str, str] | None = None,
        base_url: str = PULSE_ECO_BASE_URL_FORMAT,
        session: None = None,
        client: CLIENT | None = None,
        async_client: ASYNC_CLIENT | None = None,
        pulse_eco_api: PulseEcoAPIBase | None = None,
    ) -> None:
        """Initialize the pulse.eco client.

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
        :param pulse_eco_api: a pulse.eco API wrapper, defaults to None,
            if set, the other parameters are ignored
        """
        self._pulse_eco_api: PulseEcoAPIBase
        if pulse_eco_api is None:
            self._pulse_eco_api = PulseEcoAPI(
                city_name=city_name,
                auth=auth,
                base_url=base_url,
                session=session,
                client=client,
                async_client=async_client,
            )
        else:
            self._pulse_eco_api = pulse_eco_api

    def sensors(self) -> list[Sensor]:
        """Get all sensors for a city.

        :return: a list of sensors
        """
        return Sensors.validate_python(self._pulse_eco_api.sensors())

    async def asensors(self) -> list[Sensor]:
        """Get all sensors for a city.

        :return: a list of sensors
        """
        return Sensors.validate_python(await self._pulse_eco_api.asensors())

    def sensor(self, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID.

        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return Sensor.model_validate(self._pulse_eco_api.sensor(sensor_id=sensor_id))

    async def asensor(self, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID.

        :param sensor_id: the unique ID of the sensor
        :return: a sensor
        """
        return Sensor.model_validate(
            await self._pulse_eco_api.asensor(sensor_id=sensor_id)
        )

    def data_raw(
        self,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get raw data for a city.

        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type, defaults to None
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of data values
        """
        return DataValues.validate_python(
            self._pulse_eco_api.data_raw(
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        )

    async def adata_raw(
        self,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get raw data for a city.

        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type, defaults to None
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of data values
        """
        return DataValues.validate_python(
            await self._pulse_eco_api.adata_raw(
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        )

    def avg_data(
        self,
        period: AveragePeriod,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get average data for a city.

        :param period: the period of the average data
        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of average data values
        """
        return DataValues.validate_python(
            self._pulse_eco_api.avg_data(
                period=period,
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        )

    async def aavg_data(
        self,
        period: AveragePeriod,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: DataValueType,
        sensor_id: str | None = None,
    ) -> list[DataValue]:
        """Get average data for a city.

        :param period: the period of the average data
        :param from_: the start datetime of the data
            as a datetime object or an isoformat string
        :param to: the end datetime of the data
            as a datetime object or an isoformat string
        :param type: the data value type
        :param sensor_id: the unique ID of the sensor, defaults to None
        :return: a list of average data values
        """
        return DataValues.validate_python(
            await self._pulse_eco_api.aavg_data(
                period=period,
                from_=from_,
                to=to,
                type=type,
                sensor_id=sensor_id,
            )
        )

    def data24h(self) -> list[DataValue]:
        """Get 24h data for a city.

        The data values are sorted ascending by their timestamp.

        :return: a list of data values for the past 24 hours
        """
        return DataValues.validate_python(self._pulse_eco_api.data24h())

    async def adata24h(self) -> list[DataValue]:
        """Get 24h data for a city.

        The data values are sorted ascending by their timestamp.

        :return: a list of data values for the past 24 hours
        """
        return DataValues.validate_python(await self._pulse_eco_api.adata24h())

    def current(self) -> list[DataValue]:
        """Get the last received valid data for each sensor in a city.

        Will not return sensor data older than 2 hours.

        :return: a list of current data values
        """
        return DataValues.validate_python(self._pulse_eco_api.current())

    async def acurrent(self) -> list[DataValue]:
        """Get the last received valid data for each sensor in a city.

        Will not return sensor data older than 2 hours.

        :return: a list of current data values
        """
        return DataValues.validate_python(await self._pulse_eco_api.acurrent())

    def overall(self) -> Overall:
        """Get the current average data for all sensors per value for a city.

        :return: the overall data for the city
        """
        return Overall.model_validate(self._pulse_eco_api.overall())

    async def aoverall(self) -> Overall:
        """Get the current average data for all sensors per value for a city.

        :return: the overall data for the city
        """
        return Overall.model_validate(await self._pulse_eco_api.aoverall())
