from datetime import datetime, timedelta, timezone
from typing import List, Tuple, Union


def convert_datetime_to_str(datetime: datetime) -> str:
    """Convert a datetime object to a string

    :param datetime: a datetime object
    :return: an isoformat string
    """
    if datetime.tzinfo is None:
        datetime = datetime.replace(tzinfo=timezone.utc)
    return datetime.isoformat()


def split_datetime_span(
        fr: Union[str, datetime],
        to: Union[str, datetime],
        td: timedelta) -> List[Tuple[datetime, datetime]]:
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
    output = []
    current = fr
    prev = current
    while current + td < to:
        current += td
        output.append((prev, current))
        prev = current + timedelta(seconds=1)
    output.append((prev, to))
    return output
