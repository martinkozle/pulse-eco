import datetime
import os

import dotenv
import pytest

from pulseeco import AveragePeriod, PulseEcoClient
from pulseeco.enums import DataValueType
from pulseeco.utils import split_datetime_span


@pytest.fixture(scope="session")
def pulse_eco() -> PulseEcoClient:
    dotenv.load_dotenv(override=True)
    email = os.environ["USERNAME"]
    password = os.environ["PASSWORD"]
    assert email, "USERNAME environment variable not set"
    assert password, "PASSWORD environment variable not set"
    return PulseEcoClient(auth=(email, password))


def test_sensors(pulse_eco: PulseEcoClient) -> None:
    """Test sensors endpoint"""
    pulse_eco.sensors("skopje")


def test_sensor(pulse_eco: PulseEcoClient) -> None:
    """Test sensor endpont"""
    sensors = pulse_eco.sensors("skopje")
    assert len(sensors) > 0, "there should be at least one sensor"
    sensor_id = sensors[0].sensor_id
    sensor = pulse_eco.sensor("skopje", sensor_id)
    assert sensor == sensors[0], "sensor should be the same as the one from sensors"


def test_split_datetime_span() -> None:
    fr = "2019-03-17T12:00:00"
    to = "2019-04-03T14:57:03"
    td = datetime.timedelta(days=7)
    datetimes = split_datetime_span(fr, to, td)
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
    """Test dataRaw endpoint"""
    from_ = "2017-03-15T02:00:00+01:00"
    to = "2017-04-19T12:00:00+01:00"
    data_raw = pulse_eco.data_raw(
        city_name="skopje",
        from_=from_,
        to=to,
        sensor_id="1001",
        type=DataValueType.PM10,
    )
    assert len(data_raw) > 0, "there should be at least one data value"


def test_avg_data(pulse_eco: PulseEcoClient) -> None:
    """Test average endpoint"""
    from_ = "2019-03-01T12:00:00+00:00"
    to = "2020-05-01T12:00:00+00:00"
    for period in (AveragePeriod.DAY, AveragePeriod.WEEK, AveragePeriod.MONTH):
        avg_data = pulse_eco.avg_data(
            city_name="skopje",
            period=period,
            from_=from_,
            to=to,
            type=DataValueType.PM10,
            sensor_id="-1",
        )
        assert len(avg_data) > 0, "there should be at least one data value"


def test_data24h(pulse_eco: PulseEcoClient) -> None:
    """Test data24h endpoint"""
    data24h = pulse_eco.data24h(city_name="skopje")
    assert len(data24h) > 0, "there should be at least one data value"


def test_current(pulse_eco: PulseEcoClient) -> None:
    """Test current endpoint"""
    current = pulse_eco.current(city_name="skopje")
    assert len(current) > 0, "there should be at least one data value"


def test_overall(pulse_eco: PulseEcoClient) -> None:
    """Test overall endpoint"""
    pulse_eco.overall(city_name="skopje")
