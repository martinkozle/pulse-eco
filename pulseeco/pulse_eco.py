from datetime import datetime, timezone
from typing import List, Optional, Tuple, Union

import requests

from .types import DataValue, Overall, Sensor

PULSE_ECO_REST_API_DOCS = 'https://pulse.eco/restapi'
PULSE_ECO_BASE_URL = 'https://{city_name}.pulse.eco/rest/{end_point}'


class PulseEco:
    """PulseEco API wrapper

    Documentation: https://pulse.eco/restapi
    """

    def __init__(self, auth: Tuple[str, str],
                 base_url: str = PULSE_ECO_BASE_URL):
        """Initialize the PulseEco API wrapper

        :param auth: a tuple of (email, password)
        :param base_url: the base URL of the API, defaults to
            'https://{city_name}.pulse.eco/rest/{end_point}'
        """
        self.session = requests.Session()
        self.session.auth = auth
        self.base_url = base_url

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
        url = self.base_url.format(city_name=city_name, end_point=end_point)
        response = self.session.get(url, params=params)
        print(response.url)
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

    @staticmethod
    def _convert_datetime_to_str(datetime: datetime) -> str:
        """Convert a datetime object to a string

        :param datetime: a datetime object
        :return: an isoformat string
        """
        if datetime.tzinfo is None:
            datetime = datetime.replace(tzinfo=timezone.utc)
        return datetime.isoformat()

    def data_raw(
        self,
        city_name: str,
        *,
        sensor_id: Optional[str] = None,
        position: Optional[str] = None,
        type: Optional[str] = None,
        description: Optional[str] = None,
        comments: Optional[str] = None,
        status: Optional[str] = None,
        from_: Optional[Union[str, datetime]] = None,
        to: Optional[Union[str, datetime]] = None
    ) -> List[DataValue]:
        """Get raw data for a given query

        :param city_name: the city name
        :param sensor_id: the unique ID of the sensor
        :param position: latitude and longitude GPS coordinates of the sensor
        :param type: the type ID of the sensor
        :param description: short description / name of the sensor
        :param comments: any other comments about the sensor
        :param status: the current status of the sensor
        :param from_: the start datetime of the data
        :param to: the end datetime of the data
        :return: raw data
        """
        if isinstance(from_, datetime):
            from_ = self._convert_datetime_to_str(from_)
        if isinstance(to, datetime):
            to = self._convert_datetime_to_str(to)
        params = {
            'sensorId': sensor_id,
            'position': position,
            'type': type,
            'description': description,
            'comments': comments,
            'status': status,
            'from': from_,
            'to': to,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._base_request(city_name, 'dataRaw', params=params)

    def avg_data(
        self,
        city_name: str,
        period: str,
        type: str = None,
        *,
        sensor_id: Optional[str] = None,
        position: Optional[str] = None,
        description: Optional[str] = None,
        comments: Optional[str] = None,
        status: Optional[str] = None,
        from_: Optional[Union[str, datetime]] = None,
        to: Optional[Union[str, datetime]] = None
    ) -> List[DataValue]:
        """Get average data for a query in given time periods

        :param city_name: the city name
        :param period: the period of the data (day, week, month)
        :param sensor_id: the unique ID of the sensor
        :param position: latitude and longitude GPS coordinates of the sensor
        :param type: the type ID of the sensor
        :param description: short description / name of the sensor
        :param comments: any other comments about the sensor
        :param status: the current status of the sensor
        :param from_: the start datetime of the data
        :param to: the end datetime of the data
        :return: average data
        """
        if isinstance(from_, datetime):
            from_ = self._convert_datetime_to_str(from_)
        if isinstance(to, datetime):
            to = self._convert_datetime_to_str(to)
        if period not in ('day', 'week', 'month'):
            raise ValueError(
                'Invalid value for period. Expected one of: day, week, month')
        params = {
            'sensorId': sensor_id,
            'position': position,
            'type': type,
            'description': description,
            'comments': comments,
            'status': status,
            'from': from_,
            'to': to,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return self._base_request(city_name, f'avgData/{period}',
                                  params=params)

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
