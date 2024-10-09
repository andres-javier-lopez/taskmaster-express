import datetime
from zoneinfo import ZoneInfo

from taskmasterexp.settings import TIMEZONE

TZ = ZoneInfo(TIMEZONE)


def get_weekday() -> str:
    """Return the current weekday."""
    return datetime.datetime.now(tz=TZ).strftime("%A")


def get_current_time() -> str:
    """Return the current time in ISO format."""
    return datetime.datetime.now(tz=TZ).isoformat()
