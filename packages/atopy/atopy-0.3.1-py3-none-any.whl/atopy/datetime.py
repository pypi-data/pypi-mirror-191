from datetime import date, datetime, timedelta
from time import time_ns

from pytz import BaseTzInfo, timezone, utc


def pytz_timezone(s: str) -> BaseTzInfo:
    return timezone(s)


def utc_localize(utc_naive: datetime) -> datetime:
    """
    naive: datetime with no timezone information
    """
    return utc.localize(utc_naive)


def utc_astimezone(utc_aware: datetime, tz: BaseTzInfo) -> datetime:
    """
    aware: datetime with timezone information
    """
    assert utc_aware.tzinfo is utc
    return utc_aware.astimezone(tz)


def utc_now() -> datetime:
    return utc_localize(datetime.utcnow())


def nstime() -> int:
    return time_ns()


def nstime_datetime(ns: int) -> datetime:
    return utc_localize(datetime.utcfromtimestamp(ns / 1000000000))


def ustime() -> int:
    return nstime() // 1000


def ustime_datetime(us: int) -> datetime:
    return utc_localize(datetime.utcfromtimestamp(us / 1000000))


def mstime() -> int:
    return nstime() // 1000000


def mstime_datetime(ms: int) -> datetime:
    return utc_localize(datetime.utcfromtimestamp(ms / 1000))


def date_add(d: date, days: int) -> date:
    """
    days range: -999999999 <= days <= 999999999
    """
    return d + timedelta(days=days)


def date_weekday(d: date) -> int:
    """
    Return the day of the week as an integer, Monday is 0 and Sunday is 6.
    """
    return d.weekday()


def date_is_weekend(d: date) -> bool:
    return date_weekday(d) > 4


def date_to(d: date, fmt: str = "%Y-%m-%d") -> str:
    return d.strftime(fmt)


def date_from(datestr: str, fmt: str = "%Y-%m-%d") -> date:
    return datetime.strptime(datestr, fmt).date()
