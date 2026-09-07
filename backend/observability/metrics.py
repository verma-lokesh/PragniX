"""In-memory metrics counters as an MVP stand-in for a full metrics backend."""
from collections import defaultdict

_counters = defaultdict(int)
_timers = defaultdict(list)


def increment(name: str, value: int = 1):
    _counters[name] += value


def record_duration(name: str, duration_ms: float):
    _timers[name].append(duration_ms)


def snapshot() -> dict:
    return {"counters": dict(_counters), "timers": {k: v[-20:] for k, v in _timers.items()}}
