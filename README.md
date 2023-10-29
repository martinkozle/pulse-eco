# pulse-eco

![GitHub Workflow Test](https://github.com/martinkozle/pulse-eco/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/martinkozle/pulse-eco/branch/main/graph/badge.svg)](https://codecov.io/gh/martinkozle/pulse-eco)
![GitHub Workflow Build](https://github.com/martinkozle/pulse-eco/actions/workflows/build.yml/badge.svg)

[![PyPI](https://img.shields.io/pypi/v/pulse-eco?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/pulse-eco)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pulse-eco)

[![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black)
[![GitHub license](https://img.shields.io/github/license/martinkozle/pulse-eco)](https://github.com/martinkozle/pulse-eco/blob/main/LICENSE)

[![pulse.eco logo](https://pulse.eco/img/pulse-logo-horizontal.svg)](https://pulse.eco)

pulse.eco client for Python.

## Installation

pulse-eco is avialiable on [PyPI](https://pypi.org/project/pulse-eco):

```console
python -m pip install pulse-eco
```

Requires Python version 3.8+.

## Documentation

Official pulse.eco REST API documentation can be found on  [pulse.eco/restapi](https://pulse.eco/restapi).

API Reference and User Guide for this package is available on [GitHub Pages](https://martinkozle.github.io/pulse-eco/).

## Requesting data with a larger time range

The pulse.eco API limits the maximum time span of data you can get from one request.
For `/dataRaw` it is one week, while for `/avgData` it is one year.

If the time range is larger than the maximum, the pulse.eco client creates multiple requests to the API and then joins the data together. Be aware of this.

## Development

### Install Hatch

<https://hatch.pypa.io/latest/install/>

### Create dev environment

Activate a Python 3.8 environment and run:

```console
hatch env create dev
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

## Contributing

Contributions, especially to the documentation, are welcome.
