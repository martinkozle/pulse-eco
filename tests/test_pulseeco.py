import os
from datetime import datetime, timedelta

import pulseeco as pe
import pytest
from dotenv import load_dotenv
from pytest import fixture


def assert_is_list(data):
    assert isinstance(data, list), 'data is not a list'


def assert_is_not_empty(data: list):
    assert data, 'data is empty'


def assert_is_non_empty_list(data):
    assert_is_list(data)
    assert_is_not_empty(data)


@fixture
def pulse_eco() -> pe.PulseEco:
    load_dotenv()
    email = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    assert email, 'USERNAME environment variable not set'
    assert password, 'PASSWORD environment variable not set'
    return pe.PulseEco(auth=(email, password))


def _test_sensor(sensor):
    keys = ['sensorId', 'position', 'comments',
            'type', 'description', 'status']
    for key in keys:
        assert key in sensor, f'{key} not in sensor'


def test_sensors(pulse_eco: pe.PulseEco):
    """Test sensors endpoint"""
    sensors = pulse_eco.sensors('skopje')
    assert_is_non_empty_list(sensors)


@pytest.mark.dependency(depends=['test_sensors'])
def test_sensor(pulse_eco: pe.PulseEco):
    """Test sensor endpont"""
    sensors = pulse_eco.sensors('skopje')
    assert_is_non_empty_list(sensors)
    sensor_id = sensors[0]['sensorId']
    sensor = pulse_eco.sensor('skopje', sensor_id)
    _test_sensor(sensor)
    assert sensor == sensors[0], \
        'sensor is not the same as the one from sensors'


def _test_data_value(data_value):
    keys = ['sensorId', 'stamp', 'type', 'position', 'value']
    for key in keys:
        assert key in data_value, f'{key} not in data_value'


def test_split_datetime_span():
    fr = '2019-03-17T12:00:00'
    to = '2019-04-03T14:57:03'
    td = timedelta(days=7)
    datetimes = pe.split_datetime_span(fr, to, td)
    expected_datetimes = [
        (datetime(2019, 3, 17, 12, 0), datetime(2019, 3, 24, 12, 0)),
        (datetime(2019, 3, 24, 12, 0, 1), datetime(2019, 3, 31, 12, 0)),
        (datetime(2019, 3, 31, 12, 0, 1), datetime(2019, 4, 3, 14, 57, 3))
    ]
    assert datetimes == expected_datetimes, 'incorrect datetime split'


def test_data_raw(pulse_eco: pe.PulseEco):
    """Test dataRaw endpoint"""
    from_ = '2017-03-15T02:00:00+01:00'
    to = '2017-04-19T12:00:00+01:00'
    data_raw = pulse_eco.data_raw(
        city_name='skopje',
        from_=from_,
        to=to,
        sensor_id='1001',
        type='pm10'
    )
    assert_is_non_empty_list(data_raw)
    data_value = data_raw[0]
    _test_data_value(data_value)


def test_avg_data(pulse_eco: pe.PulseEco):
    """Test average endpoint"""
    from_ = '2019-03-01T12:00:00+00:00'
    to = '2020-05-01T12:00:00+00:00'
    for period in ('day', 'week', 'month'):
        avg_data = pulse_eco.avg_data(
            city_name='skopje',
            period=period,
            from_=from_,
            to=to,
            type='pm10',
            sensor_id='-1'
        )
        assert_is_non_empty_list(avg_data)
        data_value = avg_data[0]
        _test_data_value(data_value)


def test_data24h(pulse_eco: pe.PulseEco):
    """Test data24h endpoint"""
    data24h = pulse_eco.data24h(
        city_name='skopje'
    )
    assert_is_list(data24h)
    if len(data24h) > 0:
        data_value = data24h[0]
        _test_data_value(data_value)
    else:
        print('No data24h data')


def test_current(pulse_eco: pe.PulseEco):
    """Test current endpoint"""
    current = pulse_eco.current(
        city_name='skopje'
    )
    assert_is_list(current)
    if len(current) > 0:
        data_value = current[0]
        _test_data_value(data_value)
    else:
        print('No current data')


def test_overall(pulse_eco: pe.PulseEco):
    """Test overall endpoint"""
    overall = pulse_eco.overall(
        city_name='skopje'
    )
    assert 'cityName' in overall, 'cityName not in overall'
    assert overall['cityName'] == 'skopje', 'cityName is not input city'
    assert 'values' in overall, 'values not in overall'
    value_types = ('no2', 'o3', 'pm25', 'pm10', 'temperature',
                   'humidity', 'pressure', 'noise_dba')
    for value_type in value_types:
        assert value_type in overall['values'], f'{value_type} not in values'
