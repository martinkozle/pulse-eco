from pulseeco._version import VERSION  # noqa: PLC2701
from pulseeco.api import PulseEcoAPI

print("_version.py VERSION:", VERSION)
PulseEcoAPI(city_name="skopje", client=...)  # type: ignore[arg-type]
