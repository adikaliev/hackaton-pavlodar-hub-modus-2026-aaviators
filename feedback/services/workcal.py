"""Working-day calendar.

Deadlines are counted in working days. The working week, working hours and the
list of holidays are data (SystemSettings and Holiday), so another country or
another year needs no code change.

Rule for a deadline of N working days: the day a request is registered is day
zero (if it is a day off, day zero is the next working day); the deadline is the
end of the working day N working days later.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from datetime import date, datetime, time as dtime, timedelta

from django.utils import timezone


@dataclass(frozen=True)
class WorkCalendar:
    weekend: frozenset = frozenset({5, 6})
    exceptions: dict = field(default_factory=dict)  # date -> True if working, False if day off
    work_start: int = 9
    work_end: int = 18

    # -- days -----------------------------------------------------------------

    def is_working_day(self, day: date) -> bool:
        if day in self.exceptions:
            return self.exceptions[day]
        return day.weekday() not in self.weekend

    def next_working_day(self, day: date) -> date:
        """The first working day strictly after `day`."""
        day += timedelta(days=1)
        while not self.is_working_day(day):
            day += timedelta(days=1)
        return day

    def effective_day(self, moment: datetime) -> date:
        """The working day a moment belongs to: the same day, or the next working day."""
        day = timezone.localtime(moment).date()
        while not self.is_working_day(day):
            day += timedelta(days=1)
        return day

    def add_working_days(self, day: date, count: int) -> date:
        for _ in range(max(count, 0)):
            day = self.next_working_day(day)
        return day

    def count_working_days(self, after: date, until: date) -> int:
        """Working days d with after < d <= until."""
        count, day = 0, after
        while day < until:
            day += timedelta(days=1)
            if self.is_working_day(day):
                count += 1
        return count

    # -- moments --------------------------------------------------------------

    def _at(self, day: date, hour: int) -> datetime:
        return timezone.make_aware(datetime.combine(day, dtime(hour % 24, 0)))

    def start_of_day(self, day: date) -> datetime:
        return self._at(day, self.work_start)

    def end_of_day(self, day: date) -> datetime:
        return self._at(day, self.work_end)

    def due_after(self, start: datetime, working_days: int) -> datetime:
        return self.end_of_day(self.add_working_days(self.effective_day(start), working_days))

    def extend(self, due: datetime, working_days: int) -> datetime:
        return self.end_of_day(self.add_working_days(timezone.localtime(due).date(), working_days))

    def working_days_after(self, due: datetime, now: datetime) -> int:
        """Whole working days past a deadline: 0 on the deadline day, 1 on the next working day."""
        return self.count_working_days(timezone.localtime(due).date(), timezone.localtime(now).date())

    def working_days_until(self, now: datetime, due: datetime) -> int:
        return self.count_working_days(timezone.localtime(now).date(), timezone.localtime(due).date())

    def moment_overdue_by(self, due: datetime, working_days: int) -> datetime:
        """The moment a deadline becomes `working_days` overdue (start of that working day)."""
        day = self.add_working_days(timezone.localtime(due).date(), working_days)
        return self.start_of_day(day)

    def shift(self, moment: datetime, working_days: int) -> datetime:
        """Same local time of day, N working days later."""
        local = timezone.localtime(moment)
        day = self.add_working_days(local.date(), working_days)
        return timezone.make_aware(datetime.combine(day, local.time().replace(tzinfo=None)))

    def working_hours_between(self, start: datetime, end: datetime) -> float:
        """Working time between two moments, in hours."""
        if end <= start:
            return 0.0
        start, end = timezone.localtime(start), timezone.localtime(end)
        total, day = 0.0, start.date()
        while day <= end.date():
            if self.is_working_day(day):
                lo = max(start, self.start_of_day(day))
                hi = min(end, self.end_of_day(day))
                if hi > lo:
                    total += (hi - lo).total_seconds() / 3600
            day += timedelta(days=1)
        return total

    @property
    def hours_per_day(self) -> int:
        return max(self.work_end - self.work_start, 1)


_cache: dict = {"read_at": 0.0, "calendar": None}
_TTL_SECONDS = 2.0


def invalidate() -> None:
    _cache["read_at"] = 0.0


def get_calendar() -> WorkCalendar:
    if _cache["calendar"] is None or time.monotonic() - _cache["read_at"] > _TTL_SECONDS:
        from ..models import Holiday, SystemSettings

        settings = SystemSettings.load()
        weekend = frozenset(int(x) for x in settings.weekend_days.replace(" ", "").split(",") if x.isdigit())
        exceptions = {h.date: h.is_working for h in Holiday.objects.all()}
        _cache["calendar"] = WorkCalendar(
            weekend=weekend, exceptions=exceptions, work_start=settings.work_start_hour, work_end=settings.work_end_hour
        )
        _cache["read_at"] = time.monotonic()
    return _cache["calendar"]
