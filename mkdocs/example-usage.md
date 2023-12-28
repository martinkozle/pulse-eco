# Example usage

## Initialize client

```python
from pulseeco import PulseEcoClient

pulse_eco = PulseEcoClient(city_name="skopje", auth=("user", "pass"))
```

## Get all sensors

```pycon
>>> pulse_eco.sensors()
[
  Sensor(
    sensor_id='sensor_dev_60237_141',
    position='42.03900255426,21.40771061182',
    comments='Imported Sensor.community #60237',
    type='20004',
    description='Sensor.community 60237',
    status='NOT_CLAIMED'
  ),
  Sensor(
    sensor_id='sensor_dev_10699_244',
    position='41.986,21.452',
    comments='Imported Sensor.community #10699',
    type='20004',
    description='Sensor.community 10699',
    status='NOT_CLAIMED_UNCONFIRMED'
  ),
  Sensor(
    sensor_id='66710fdc-cdfc-4bbe-93a8-7e796fb8a88d',
    position='41.995238146587674,21.402708292007443',
    comments='V1 WiFi sensor in Kozle',
    type='1',
    description='Kozle',
    status='ACTIVE'
  ),
  ...
]
```

## Get a sensor by id

```pycon
>>> pulse_eco.sensor(sensor_id="1000")
Sensor(
  sensor_id='1000',
  position='41.99249998,21.4236110',
  comments='MOEPP sensor at Centar',
  type='0',
  description='MOEPP Centar',
  status='ACTIVE'
)
```

## Get raw data

`from_` and `to` can be either `datetime.datetime` objects or `str` in ISO 8601 format.

```pycon
>>> import datetime
>>> from pulseeco import DataValueType
>>> pulse_eco.data_raw(
...   from_=datetime.datetime(year=2017, month=3, day=15, hour=2),
...   to=datetime.datetime(year=2017, month=4, day=19, hour=12),
...   type=DataValueType.PM10,
...   sensor_id="1001",
... )
[
  DataValue(sensor_id='1001', stamp=datetime.datetime(2017, 3, 15, 3, 0, 8, tzinfo=TzInfo(+01:00)), type='pm10', position='41.9783,21.47', value=28, year=None),
  DataValue(sensor_id='1001', stamp=datetime.datetime(2017, 3, 15, 4, 0, 8, tzinfo=TzInfo(+01:00)), type='pm10', position='41.9783,21.47', value=55, year=None),
  ...
  DataValue(sensor_id='1001', stamp=datetime.datetime(2017, 4, 19, 12, 0, 9, tzinfo=TzInfo(+02:00)), type='pm10', position='41.9783,21.47', value=6, year=None),
  DataValue(sensor_id='1001', stamp=datetime.datetime(2017, 4, 19, 13, 0, 9, tzinfo=TzInfo(+02:00)), type='pm10', position='41.9783,21.47', value=31, year=None)
]
```

## Get average data

sensor_id `"-1"` is a magic value that gives average values for the whole city.

```pycon
>>> import datetime
>>> from pulseeco import AveragePeriod, DataValueType
>>> pulse_eco.avg_data(
...   period=AveragePeriod.MONTH,
...   from_=datetime.datetime(year=2019, month=3, day=1, hour=12),
...   to=datetime.datetime(year=2020, month=5, day=1, hour=12),
...   type=DataValueType.PM10,
...   sensor_id="-1",
... )
[
  DataValue(sensor_id='-1', stamp=datetime.datetime(2019, 3, 1, 13, 0, tzinfo=TzInfo(+01:00)), type='pm10', position='', value=29, year=None),
  DataValue(sensor_id='-1', stamp=datetime.datetime(2019, 4, 1, 14, 0, tzinfo=TzInfo(+02:00)), type='pm10', position='', value=19, year=None),
  ...
  DataValue(sensor_id='-1', stamp=datetime.datetime(2020, 4, 1, 14, 0, tzinfo=TzInfo(+02:00)), type='pm10', position='', value=17, year=None),
  DataValue(sensor_id='-1', stamp=datetime.datetime(2020, 5, 1, 14, 0, tzinfo=TzInfo(+02:00)), type='pm10', position='', value=12, year=None)
]
```

## Get 24h data

```pycon
>>> pulse_eco.data24h()
[ ... ]
```

## Get current data

Get the last received valid data for each sensor in a city.

```pycon
>>> pulse_eco.current()
[ ... ]
```

## Get overall data

Get the current average data for all sensors per value for a city.

```pycon
>>> pulse_eco.overall()
Overall(
  city_name='skopje',
  values=OverallValues(
    no2=6,
    o3=10,
    so2=None,
    co=None,
    pm25=56,
    pm10=95,
    temperature=6,
    humidity=73,
    pressure=995,
    noise=None,
    noise_dba=42,
    gas_resistance=None
  )
)
```
