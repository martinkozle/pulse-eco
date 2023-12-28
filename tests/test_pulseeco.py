from __future__ import annotations

import datetime

import dotenv
import pytest

from pulseeco import AveragePeriod, PulseEcoClient
from pulseeco.constants import DATA_RAW_MAX_SPAN
from pulseeco.enums import DataValueType
from pulseeco.models import Sensor
from pulseeco.utils import split_datetime_span


@pytest.fixture(scope="session")
def pulse_eco() -> PulseEcoClient:
    dotenv.load_dotenv(override=True)
    return PulseEcoClient(city_name="skopje")


@pytest.fixture(scope="session")
def sensors(pulse_eco: PulseEcoClient) -> list[Sensor]:
    return pulse_eco.sensors()


@pytest.fixture(scope="session")
def now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


@pytest.fixture(scope="session")
def data_raw_max_span_ago(now: datetime.datetime) -> datetime.datetime:
    return now - DATA_RAW_MAX_SPAN


def test_sensors(pulse_eco: PulseEcoClient) -> None:
    pulse_eco.sensors()


def test_sensor(pulse_eco: PulseEcoClient, sensors: list[Sensor]) -> None:
    assert len(sensors) > 0, "there should be at least one sensor"
    sensor_id = sensors[0].sensor_id
    sensor = pulse_eco.sensor(sensor_id)
    assert sensor == sensors[0], "sensor should be the same as the one from sensors"


def test_split_datetime_span() -> None:
    fr = "2019-03-17T12:00:00"
    to = "2019-04-03T14:57:03"
    td = datetime.timedelta(days=7)
    datetimes = list(split_datetime_span(fr, to, td))
    expected_datetimes = [
        (
            datetime.datetime(2019, 3, 17, 12, 0),  # noqa: DTZ001
            datetime.datetime(2019, 3, 24, 12, 0),  # noqa: DTZ001
        ),
        (
            datetime.datetime(2019, 3, 24, 12, 0, 1),  # noqa: DTZ001
            datetime.datetime(2019, 3, 31, 12, 0),  # noqa: DTZ001
        ),
        (
            datetime.datetime(2019, 3, 31, 12, 0, 1),  # noqa: DTZ001
            datetime.datetime(2019, 4, 3, 14, 57, 3),  # noqa: DTZ001
        ),
    ]
    assert datetimes == expected_datetimes, "datetime split should be consistent"


def test_data_raw(pulse_eco: PulseEcoClient) -> None:
    from_ = "2017-03-15T02:00:00+01:00"
    to = "2017-04-19T12:00:00+01:00"
    data_raw = pulse_eco.data_raw(
        from_=from_,
        to=to,
        type=DataValueType.PM10,
        sensor_id="1001",
    )
    assert len(data_raw) > 0, "there should be at least one data value"


def test_data_raw_past_span(
    pulse_eco: PulseEcoClient,
    sensors: list[Sensor],
    data_raw_max_span_ago: datetime.datetime,
    now: datetime.datetime,
) -> None:
    for sensor in sensors:
        pulse_eco.data_raw(
            from_=data_raw_max_span_ago,
            to=now,
            sensor_id=sensor.sensor_id,
        )


def test_avg_data(pulse_eco: PulseEcoClient) -> None:
    from_ = "2019-03-01T12:00:00+00:00"
    to = "2020-05-01T12:00:00+00:00"
    for period in (AveragePeriod.DAY, AveragePeriod.WEEK, AveragePeriod.MONTH):
        avg_data = pulse_eco.avg_data(
            period=period,
            from_=from_,
            to=to,
            type=DataValueType.PM10,
            sensor_id="-1",
        )
        assert len(avg_data) > 0, "there should be at least one data value"


def test_data24h(pulse_eco: PulseEcoClient) -> None:
    data24h = pulse_eco.data24h()
    assert len(data24h) > 0, "there should be at least one data value"


def test_current(pulse_eco: PulseEcoClient) -> None:
    current = pulse_eco.current()
    assert len(current) > 0, "there should be at least one data value"


def test_overall(pulse_eco: PulseEcoClient) -> None:
    pulse_eco.overall()
