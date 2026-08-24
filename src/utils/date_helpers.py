from datetime import datetime


def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    return dt.strftime(fmt)


def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    return datetime.strptime(date_str, fmt)


def date_diff_days(start: datetime, end: datetime) -> int:
    return (end - start).days
