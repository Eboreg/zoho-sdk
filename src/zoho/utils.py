import datetime
from zoneinfo import ZoneInfo

from zoho.settings import settings


def get_timezone():
    return ZoneInfo(settings.timezone)


def now() -> datetime.datetime:
    return datetime.datetime.now(get_timezone())
