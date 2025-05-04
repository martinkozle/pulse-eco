# pulse-eco

![GitHub Workflow Test](https://github.com/martinkozle/pulse-eco/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/martinkozle/pulse-eco/branch/main/graph/badge.svg)](https://codecov.io/gh/martinkozle/pulse-eco)
![GitHub Workflow Build](https://github.com/martinkozle/pulse-eco/actions/workflows/build.yml/badge.svg)

[![PyPI](https://img.shields.io/pypi/v/pulse-eco?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pulse-eco)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pulse-eco)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black)
[![GitHub license](https://img.shields.io/github/license/martinkozle/pulse-eco)](https://github.com/martinkozle/pulse-eco/blob/main/LICENSE)

[![pulse.eco logo](https://pulse.eco/img/pulse-logo-horizontal.svg)](https://pulse.eco)

pulse.eco client for Python.

## Installation

Requires Python version 3.9+.

The `pulse-eco` package comes with no base dependencies, everything is an extra. A sensible default is:

```console
python -m pip install pulse-eco[client,httpx]
```

### List of extras

- `client` - includes Pydantic, used for the higher level validated client (`pulseeco.client`).
- `requests` - includes [requests](https://requests.readthedocs.io/en/latest/) HTTP client with sync support.
- `aiohttp` - includes [aiohttp](https://docs.aiohttp.org/en/stable/) HTTP client with async support.
- `httpx` - includes [HTTPX](https://www.python-httpx.org/) HTTP client with both sync and async support.

## Documentation

API Reference and User Guide for this package is available on [GitHub Pages](https://martinkozle.github.io/pulse-eco/).

Official pulse.eco REST API documentation can be found on [pulse.eco/restapi](https://pulse.eco/restapi).

## Requesting data with a larger time range

The pulse.eco API limits the maximum time span of data you can get from one request.
For `/dataRaw` it is one week, while for `/avgData` it is one year.

If the time range is larger than the maximum, the pulse-eco Python client performs multiple requests to the API and then joins the data together. Be aware of this.

## Development

### Install Hatch

<https://hatch.pypa.io/latest/install/>

### Create dev environment

Activate a Python 3.9 environment and run:

```console
hatch env create dev
```

To delete the environment, run:

```console
hatch env remove dev
```

### Install pre-commit hooks

```console
hatch run dev:setup
```

### Create .env file

Set auth credentials in `.env` file:

```console
cp .env.example .env
```

### Before committing

This command must pass without errors before committing:

```console
hatch run dev:check
```

### Docs

To preview the docs locally, run:

```console
hatch run dev:docs-serve
```
