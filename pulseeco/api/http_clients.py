from __future__ import annotations

from importlib.util import find_spec
from typing import TYPE_CHECKING, Union

has_requests = find_spec("requests") is not None
has_aiohttp = find_spec("aiohttp") is not None
has_httpx = find_spec("httpx") is not None

if has_requests:
    import requests  # type: ignore[import-not-found, unused-ignore]

if has_httpx:
    import httpx  # type: ignore[import-not-found, unused-ignore]

if TYPE_CHECKING:
    import aiohttp  # type: ignore[import-not-found, unused-ignore]


class _SingleUseRequestsClient:
    def __init__(self) -> None:
        self.get = requests.get


class _SingleUseHttpxClient:
    def __init__(self) -> None:
        self.get = httpx.get


_SingleUseClient = Union[_SingleUseRequestsClient, _SingleUseHttpxClient]


def _get_fallback_sync_client() -> _SingleUseClient:
    if has_requests:
        return _SingleUseRequestsClient()
    if has_httpx:
        return _SingleUseHttpxClient()
    raise ImportError(
        "No supported sync http client is installed"
        ", install one of the extras `requests` or `httpx`"
        ", you can install either with `pip install pulse-eco[requests]`"
        " or `pip install pulse-eco[httpx]`"
    )


if TYPE_CHECKING:
    CLIENT = Union[requests.Session, httpx.Client, _SingleUseClient]
    ASYNC_CLIENT = Union[aiohttp.ClientSession, httpx.AsyncClient]
