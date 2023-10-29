from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import datetime

    from pulseeco.api.data_types import DataValueAvg, DataValueRaw, Overall, Sensor

from abc import ABC, abstractmethod


class PulseEcoAPIBase(ABC):  # pragma: no cover
    """Low level unsafe pulse.eco API wrapper base class"""

    @abstractmethod
    def sensors(self) -> list[Sensor]: ...

    @abstractmethod
    def sensor(self, sensor_id: str) -> Sensor: ...

    @abstractmethod
    def data_raw(
        self,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str | None = None,
        sensor_id: str | None = None,
    ) -> list[DataValueRaw]: ...

    @abstractmethod
    def avg_data(
        self,
        period: str,
        from_: str | datetime.datetime,
        to: str | datetime.datetime,
        type: str,
        sensor_id: str | None = None,
    ) -> list[DataValueAvg]: ...

    @abstractmethod
    def data24h(self) -> list[DataValueRaw]: ...

    @abstractmethod
    def current(self) -> list[DataValueRaw]: ...

    @abstractmethod
    def overall(self) -> Overall: ...
