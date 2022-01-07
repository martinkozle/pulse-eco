import warnings
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union

import requests

from .data_types import DataValue, Overall, Sensor
from .utils import convert_datetime_to_str, split_datetime_span

PULSE_ECO_BASE_URL = 'https://{city_name}.pulse.eco/rest/{end_point}'
DATA_RAW_MAX_SPAN = timedelta(days=7)
AVG_DATA_MAX_SPAN = timedelta(days=365)


class PulseEco:
    """pulse.eco API wrapper
    """

    def __init__(self, auth: Tuple[str, str],
                 base_url: str = PULSE_ECO_BASE_URL):
        """Initialize the PulseEco API wrapper

        :param auth: a tuple of (email, password)
        :param base_url: the base URL of the API, defaults to
            'https://{city_name}.pulse.eco/rest/{end_point}'
        """
        self._session = requests.Session()
        self._session.auth = auth
        self._base_url = base_url

    def _base_request(self, city_name: str, end_point: str,
                      params: Optional[dict] = None):
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

    def sensors(self, city_name: str) -> List[Sensor]:
        """Get all sensors for a city

        :param city_name: the city name
        :return: list of sensors
        """
        return self._base_request(city_name, 'sensor')

    def sensor(self, city_name: str, sensor_id: str) -> Sensor:
        """Get a sensor by it's ID

        :param city_name: the city name
        :param sensor_id: the unique ID of the sensor
        :return: sensor
        """
        return self._base_request(city_name, f'sensor/{sensor_id}')

    def data_raw(
        self,
        city_name: str,
        from_: Union[str, datetime],
        to: Union[str, datetime],
        sensor_id: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[DataValue]:
        """Get raw data for a given query

        :param city_name: the city name
        :param from_: the start datetime of the data
        :param to: the end datetime of the data
        :param sensor_id: the unique ID of the sensor
        :param type: the type ID of the sensor
        :return: raw data
        """
        if sensor_id is None and type is None:
            warnings.warn(
                'Warning! If you encounter an error, '
                'you should probably specify either sensor_id or type.')
        data = []
        datetime_spans = split_datetime_span(from_, to, DATA_RAW_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                'sensorId': sensor_id,
                'type': type,
                'from': convert_datetime_to_str(from_temp),
                'to': convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            data += self._base_request(city_name, 'dataRaw', params=params)
        return data

    def avg_data(
        self,
        city_name: str,
        period: str,
        from_: Union[str, datetime],
        to: Union[str, datetime],
        type: str,
        sensor_id: Optional[str] = None
    ) -> List[DataValue]:
        """Get average data for a query in given time periods

        :param city_name: the city name
        :param period: the period of the data (day, week, month)
        :param from_: the start datetime of the data
        :param to: the end datetime of the data
        :param type: the type ID of the sensor
        :param sensor_id: the unique ID of the sensor
        :return: average data
        """
        if period not in ('day', 'week', 'month'):
            warnings.warn(
                'Warning! Invalid value for period. '
                'Should be one of: day, week, month')
        data = []
        datetime_spans = split_datetime_span(from_, to, AVG_DATA_MAX_SPAN)
        for from_temp, to_temp in datetime_spans:
            params = {
                'sensorId': sensor_id,
                'type': type,
                'from': convert_datetime_to_str(from_temp),
                'to': convert_datetime_to_str(to_temp),
            }
            params = {k: v for k, v in params.items() if v is not None}
            data += self._base_request(city_name, f'avgData/{period}',
                                       params=params)
        return data

    def data24h(self, city_name: str) -> List[DataValue]:
        """Get all of the data in the past 24h

        The data values are sorted ascending by their timestamp.

        :param city_name: the city name
        :return: senssor data of the past 24h
        """
        return self._base_request(city_name, 'data24h')

    def current(self, city_name: str) -> List[DataValue]:
        """Get the last received valid data for each sensor

        Will not return sensor data older than 2h.

        :param city_name: the city name
        :return: sensor data of the past 2h
        """
        return self._base_request(city_name, 'current')

    def overall(self, city_name: str) -> Overall:
        """Get the current average data for all sensors per value

        Example:

        .. code-block:: python

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

        :param city_name: the city name
        :return: overall data for the city
        """
        return self._base_request(city_name, 'overall')
