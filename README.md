# pulse-eco

[![PyPI](https://img.shields.io/pypi/v/pulse-eco)](https://pypi.org/project/pulse-eco)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pulse-eco)
[![GitHub license](https://img.shields.io/github/license/martinkozle/pulse-eco)](https://github.com/martinkozle/pulse-eco/blob/main/LICENSE)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/martinkozle/pulse-eco/python-package.yml?branch=main)

[![pulse.eco logo](https://pulse.eco/img/pulse-logo-horizontal.svg)](https://pulse.eco)

pulse.eco API wrapper for Python.

```python
>>> import pulseeco as pe
>>> pulse_eco = pe.PulseEco(auth=('user', 'pass'))
>>> pulse_eco.overall('skopje')
{'cityName': 'skopje',
 'values': {'no2': '36',
  'o3': '6',
  'pm25': '63',
  'pm10': '88',
  'temperature': '11',
  'humidity': '75',
  'pressure': '980',
  'noise_dba': '45'}}
>>> pulse_eco.current('skopje')
[{'sensorId': '1005',
  'stamp': '2022-01-06T16:00:00Z',
  'type': 'no2',
  'position': '41.9992,21.4408',
  'value': '62'},
 {'sensorId': '1004',
  'stamp': '2022-01-06T16:00:00Z',
  'type': 'no2',
  'position': '42.0036,21.4636',
  'value': '6'}, ...]
```

## Installation

pulse-eco is avialiable on [PyPI](https://pypi.org/project/pulse-eco):

```console
python -m pip install pulse-eco
```

Requires Python version 3.8+.

## Documentation

Official pulse.eco REST API documentation can be found on  [pulse.eco/restapi](https://pulse.eco/restapi).  
API Reference and User Guide for this package is available on [Read the Docs](https://pulse-eco.readthedocs.io/en/latest/).

## Requesting data with a larger time range

The pulse.eco API limits the maximum time span of data you can get from one request.
For /dataRaw it is one week, while for /avgData it is one year.

If the time range is larger than the maximum, the pulseeco module creates multiple requests to the API and then joins the data together. Be aware of this.

## Warnings instead of errors

This package does not raise errors for invalid input. Instead it prints warning messages for known bad inputs and makes the API call anyway. So expect an HTTPError.  
This is because the REST API documentation doesn't cover all possible errors for bad arguments. Another reason is because this package is trying to be future proof.

To disable these warnings:

```python
import warnings

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    ...
```

or (disables warnings for other packages that use warnings module as well):

```python
import warnings

warnings.filterwarnings('ignore')
```

## pulseeco command line tool

This package also provides a command line tool.

```console
$ pulseeco --help
usage: pulseeco [-h] [-B BASE_URL] -U USER -P PASSWORD -C CITY {sensors,sensor,dataRaw,avgData,data24h,current,overall} ...

PulseEco API client

positional arguments:
  {sensors,sensor,dataRaw,avgData,data24h,current,overall}
    sensors             List sensors
    sensor              Get sensor info by ID
    dataRaw             Get raw data
    avgData             Get average data
    data24h             Get 24h data
    current             Get current data
    overall             Get overall data

optional arguments:
  -h, --help            show this help message and exit
  -B BASE_URL, --base-url BASE_URL
                        PulseEco API base URL
  -U USER, --user USER  PulseEco API user
  -P PASSWORD, --password PASSWORD
                        PulseEco API password
  -C CITY, --city CITY  the city name
```

In order to use table print with the command, you need to either install pandas separately or install pulse-eco with the extra [pandas]:

```console
python -m pip install pulse-eco[pandas]
```
