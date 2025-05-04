from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


def convert_datetime_to_str(datetime: datetime) -> str:
    """Convert a datetime object to a string

    :param datetime: a datetime object
    :return: an isoformat string
    """
    if datetime.tzinfo is None:
        datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()


def split_datetime_span(
    fr: str | datetime, to: str | datetime, td: timedelta
) -> Iterator[tuple[datetime, datetime]]:
    """Split a datetime span into a list of (fr, to) datetime pairs
        with a given maximum timedelta

    :param fr: the start datetime of the span
    :param to: the end datetime of the span
    :param td: the timedelta between the datetimes
    :return: a list of datetimes
    """
    if isinstance(fr, str):
        fr = datetime.fromisoformat(fr)
    if isinstance(to, str):
        to = datetime.fromisoformat(to)
    current = fr
    prev = current
    while current + td < to:
        current += td
        yield prev, current
        prev = current = current + timedelta(seconds=1)
    if prev < to:
        yield prev, to
