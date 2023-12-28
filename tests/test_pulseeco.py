from __future__ import annotations

import datetime

import pytest
import requests

from pulseeco import AveragePeriod, PulseEcoClient
from pulseeco.api.pulse_eco_api import PulseEcoAPI
from pulseeco.constants import (
    DATA_RAW_MAX_SPAN,
    PULSE_ECO_BASE_URL_FORMAT_ENV_KEY,
    PULSE_ECO_PASSWORD_ENV_KEY,
    PULSE_ECO_USERNAME_ENV_KEY,
)
from pulseeco.enums import DataValueType
from pulseeco.models import OverallValues, Sensor
from pulseeco.utils import split_datetime_span


@pytest.fixture(scope="session")
def cities() -> list[str]:
    return [
        "tirana",
        "sofia",
        "yambol",
        "zagreb",
        "nicosia",
        "copenhagen",
        "berlin",
        "berlin",
        "syros",
        "thessaloniki",
        "cork",
        "novoselo",
        "struga",
        "bitola",
        "shtip",
        "skopje",
        "tetovo",
        "gostivar",
        "ohrid",
        "resen",
        "kumanovo",
        "strumica",
        "bogdanci",
        "kichevo",
        "delft",
        "amsterdam",
        "bucharest",
        "targumures",
        "sacele",
        "codlea",
        "cluj-napoca",
        "oradea",
        "iasi",
        "brasov",
        "nis",
        "lausanne",
        "zuchwil",
        "bern",
        "luzern",
        "grenchen",
        "zurich",
        "grand-rapids",
        "portland",
    ]


@pytest.fixture(scope="session")
def pulse_eco_skopje() -> PulseEcoClient:
    return PulseEcoClient(city_name="skopje")


@pytest.fixture(scope="session")
def sensors_skopje(pulse_eco_skopje: PulseEcoClient) -> list[Sensor]:
    return pulse_eco_skopje.sensors()


@pytest.fixture(scope="session")
def now() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


@pytest.fixture(scope="session")
def data_raw_max_span_ago(now: datetime.datetime) -> datetime.datetime:
    return now - DATA_RAW_MAX_SPAN


def test_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    custom_pulse_eco_base_url_format = "custom_{city_name}_{end_point}"
    monkeypatch.setenv(
        PULSE_ECO_BASE_URL_FORMAT_ENV_KEY, custom_pulse_eco_base_url_format
    )
    custom_pulse_eco_username = "username"
    monkeypatch.setenv(PULSE_ECO_USERNAME_ENV_KEY, custom_pulse_eco_username)
    custom_pulse_eco_password = "password"  # noqa: S105
    monkeypatch.setenv(PULSE_ECO_PASSWORD_ENV_KEY, custom_pulse_eco_password)
    pulse_eco_api = PulseEcoAPI(city_name="skopje")
    assert (
        pulse_eco_api._base_url == custom_pulse_eco_base_url_format  # noqa: SLF001
    ), "`_base_url` should be the same as the one from env vars"
    assert pulse_eco_api._session.auth == (  # noqa: SLF001
        custom_pulse_eco_username,
        custom_pulse_eco_password,
    ), "`_session.auth` should be the same as the credentials from env vars"


def test_auth() -> None:
    pulse_eco_api = PulseEcoAPI(city_name="skopje", auth=("username", "password"))
    assert pulse_eco_api._session.auth == (  # noqa: SLF001
        "username",
        "password",
    ), "`_session.auth` should be the same as the passed credentials"


def test_custom_session() -> None:
    with requests.Session() as session:
        session.proxies["protocol"] = "proxy"
        pulse_eco_api = PulseEcoAPI(city_name="skopje", session=session)
        assert (
            pulse_eco_api._session.proxies["protocol"] == "proxy"  # noqa: SLF001
        ), "`_session` should be the same as the one from the session parameter"


def test_custom_pulse_eco_api() -> None:
    class CustomPulseEcoAPI(PulseEcoAPI):
        pass

    custom_pulse_eco_api = CustomPulseEcoAPI("skopje")
    pulse_eco = PulseEcoClient("skopje", pulse_eco_api=custom_pulse_eco_api)
    assert (
        pulse_eco._pulse_eco_api == custom_pulse_eco_api  # noqa: SLF001
    ), "`_pulse_eco_api` should be the same as the passed object"


def test_sensor_skopje(
    pulse_eco_skopje: PulseEcoClient, sensors_skopje: list[Sensor]
) -> None:
    assert len(sensors_skopje) > 0, "there should be at least one sensor"
    sensor_id = sensors_skopje[0].sensor_id
    sensor = pulse_eco_skopje.sensor(sensor_id)
    assert (
        sensor == sensors_skopje[0]
    ), "sensor should be the same as the one from sensors"


def test_sensors_all_cities(cities: list[str]) -> None:
    for city_name in cities:
        pulse_eco = PulseEcoClient(city_name=city_name)
        pulse_eco.sensors()


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


def test_data_raw_skopje(pulse_eco_skopje: PulseEcoClient) -> None:
    from_ = "2017-03-15T02:00:00+01:00"
    to = "2017-04-19T12:00:00+01:00"
    data_raw = pulse_eco_skopje.data_raw(
        from_=from_,
        to=to,
        type=DataValueType.PM10,
        sensor_id="1001",
    )
    assert len(data_raw) > 0, "there should be at least one data value"


def test_data_raw_past_span(
    pulse_eco_skopje: PulseEcoClient,
    cities: list[str],
    data_raw_max_span_ago: datetime.datetime,
    now: datetime.datetime,
) -> None:
    for city in cities:
        pulse_eco = PulseEcoClient(city_name=city)
        sensors = pulse_eco.sensors()
        for sensor in sensors:
            pulse_eco.data_raw(
                from_=data_raw_max_span_ago,
                to=now,
                sensor_id=sensor.sensor_id,
            )


def test_avg_data(pulse_eco_skopje: PulseEcoClient) -> None:
    from_ = "2019-03-01T12:00:00+00:00"
    to = "2020-05-01T12:00:00+00:00"
    for period in (AveragePeriod.DAY, AveragePeriod.WEEK, AveragePeriod.MONTH):
        avg_data = pulse_eco_skopje.avg_data(
            period=period,
            from_=from_,
            to=to,
            type=DataValueType.PM10,
            sensor_id="-1",
        )
        assert len(avg_data) > 0, "there should be at least one data value"


def test_data24h(pulse_eco_skopje: PulseEcoClient) -> None:
    data24h = pulse_eco_skopje.data24h()
    assert len(data24h) > 0, "there should be at least one data value"


def test_current(pulse_eco_skopje: PulseEcoClient) -> None:
    current = pulse_eco_skopje.current()
    assert len(current) > 0, "there should be at least one data value"


def test_overall_values_type() -> None:
    assert OverallValues(pm10="N/A").pm10 is None, "`N/A` should validate to None"


def test_overall(cities: list[str]) -> None:
    for city in cities:
        pulse_eco = PulseEcoClient(city_name=city)
        overall = pulse_eco.overall()
        model_extra = overall.values.model_extra
        assert (
            model_extra is None or len(model_extra) == 0
        ), "there shouldn't be any extra values"
