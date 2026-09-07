from datetime import date, datetime, timedelta


def days_between(start: date, end: date) -> int:
    return (end - start).days


def add_days(d: date, days: int) -> date:
    return d + timedelta(days=days)


def now_utc() -> datetime:
    return datetime.utcnow()


def iso(d) -> str:
    return d.isoformat() if d else None
