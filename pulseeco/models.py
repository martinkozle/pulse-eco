import warnings

warnings.warn(
    "Importing from `pulseeco.models` is deprecated"
    ", use `pulseeco` or `pulseeco.client.models` instead",
    category=DeprecationWarning,
    stacklevel=2,
)

from .client.models import *  # noqa: F403
