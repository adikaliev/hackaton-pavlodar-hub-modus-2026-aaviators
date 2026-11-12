"""The system clock.

All domain code asks this module for the time instead of `timezone.now()`.
That gives two things:

* the demo clock: a "+1 working day" button moves the whole system forward, so
  a juror can watch a fresh request get overdue and escalate without waiting;
* the seed loader replays each request's history at the moment it "happened".
"""
from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from datetime import timedelta

from django.utils import timezone

_local = threading.local()
_cache = {"read_at": 0.0, "offset": 0}
_TTL_SECONDS = 1.0


def invalidate() -> None:
    _cache["read_at"] = 0.0


def offset_minutes() -> int:
    if time.monotonic() - _cache["read_at"] > _TTL_SECONDS:
        from ..models import SystemSettings

        value = SystemSettings.objects.filter(pk=1).values_list("clock_offset_minutes", flat=True).first()
        _cache["offset"] = value or 0
        _cache["read_at"] = time.monotonic()
    return _cache["offset"]


def now():
    frozen = getattr(_local, "frozen", None)
    if frozen is not None:
        return frozen
    return timezone.now() + timedelta(minutes=offset_minutes())


def localnow():
    return timezone.localtime(now())


def today():
    return localnow().date()


@contextmanager
def freeze(moment):
    """Pin the clock for the current thread (seed loader and tests)."""
    previous = getattr(_local, "frozen", None)
    _local.frozen = moment
    try:
        yield
    finally:
        _local.frozen = previous


def unfreeze() -> None:
    """Drop any pinned moment for the current thread."""
    _local.frozen = None


def advance_working_days(days: int) -> None:
    """Demo control: jump forward by N working days, keeping the time of day."""
    from ..models import SystemSettings
    from . import workcal

    current = now()
    target = workcal.get_calendar().shift(current, days)
    settings = SystemSettings.load()
    settings.clock_offset_minutes += int((target - current).total_seconds() // 60)
    settings.save()


def reset() -> None:
    from ..models import SystemSettings

    settings = SystemSettings.load()
    settings.clock_offset_minutes = 0
    settings.save()
