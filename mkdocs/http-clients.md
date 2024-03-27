# HTTP Clients

The `pulse-eco` package is designed to be modular and compatible with different HTTP clients.

## Supported clients

The following HTTP clients are currently supported:

### Sync

- `requests`
- `httpx`

### Async

- `aiohttp`
- `httpx`

## Context management

It is recommended to always use context managers when working with HTTP clients.

Examples:

```python
import requests

from pulseeco.client import PulseEcoClient

with requests.Session() as client:
    pulse_eco = PulseEcoClient(city_name="skopje", client=client)
    pulse_eco.sensors()
```

```python
import aiohttp

from pulseeco.client import PulseEcoClient

async with aiohttp.ClientSession() as client:
    pulse_eco = PulseEcoClient(city_name="skopje", async_client=client)
    await pulse_eco.asensors()
```

```python
import httpx

from pulseeco.client import PulseEcoClient

async with httpx.AsyncClient() as client:
    pulse_eco = PulseEcoClient(city_name="skopje", async_client=client)
    await pulse_eco.asensors()
```
