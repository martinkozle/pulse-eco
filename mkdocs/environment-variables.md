# Environment variables

## Base URL format

Environment variable: `PULSE_ECO_BASE_URL_FORMAT`

The default base URL format is `https://{city_name}.pulse.eco/rest/{end_point}`.

## Authentication

Authentication is not required for fetching data. But if provided, it has to be valid for the city.

Credentials can also be provided as environment variables. To provide credentials for a city, use the following format:

```txt
PULSE_ECO_{city_name}_USERNAME
PULSE_ECO_{city_name}_PASSWORD
```

Example environmtent variables in priority order:

```txt
PULSE_ECO_SKOPJE_USERNAME
PULSE_ECO_SKOPJE_PASSWORD

PULSE_ECO_skopje_USERNAME
PULSE_ECO_skopje_PASSWORD

PULSE_ECO_USERNAME
PULSE_ECO_PASSWORD
```

Only use the generic `PULSE_ECO_USERNAME` and `PULSE_ECO_PASSWORD` environment variables
if your application requests data from a single city.
