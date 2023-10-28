from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime

    from pulseeco.api.data_types import DataValueAvg, DataValueRaw, Overall, Sensor

from abc import ABC, abstractmethod


class PulseEcoAPIBase(ABC):
    """Low level unsafe pulse.eco API wrapper base class"""

    @abstractmethod
    def sensors(self, city_name: str) -> list[Sensor]:
        ...

    @abstractmethod
    def sensor(self, city_name: str, sensor_id: str) -> Sensor:
        ...

    @abstractmethod
    def data_raw(
        self,
        city_name: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValueRaw]:
        ...

    @abstractmethod
    def avg_data(
        self,
        city_name: str,
        period: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str,
        sensor_id: str | None = None,
    ) -> list[DataValueAvg]:
        ...

    @abstractmethod
    def data24h(self, city_name: str) -> list[DataValueRaw]:
        ...

    @abstractmethod
    def current(self, city_name: str) -> list[DataValueRaw]:
        ...

    @abstractmethod
    def overall(self, city_name: str) -> Overall:
        ...
