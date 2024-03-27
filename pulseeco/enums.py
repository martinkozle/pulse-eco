import warnings

warnings.warn(
    "Importing from `pulseeco.enums` is deprecated"
    ", use `pulseeco` or `pulseeco.client.enums` instead",
    category=DeprecationWarning,
    stacklevel=2,
)

from .client.enums import *  # noqa: F403
