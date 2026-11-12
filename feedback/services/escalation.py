"""Escalation on silence (solution design, section 3.4).

`tick()` is idempotent and cheap. It runs from the background worker, after the
demo clock is moved and after the demo data is loaded. Each step of the ladder
is written to the request history once, stamped with the moment it happened:

1. on the last day of a deadline — a reminder to the assignee;
2. N working days overdue (default 1) — the request goes to the assignee's manager;
3. M working days overdue (default 3) — the request goes to leadership.

It also closes implemented requests the author did not confirm in time.
"""
from __future__ import annotations

from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from ..models import Appeal, Event, SystemSettings
from . import clock, routing, workcal
from .workflow import add_event, notify

S = Appeal.Status
K = Event.Kind

DEADLINE_WORDING = {
    S.NEW: "Срок первого ответа истёк",
    S.REVIEW: "Срок решения истёк",
    S.DECIDED: "Плановая дата реализации прошла",
    S.IN_PROGRESS: "Плановая дата реализации прошла",
}


def _days_word(count: int) -> str:
    return f"{count} раб. дн."


def _escalate(appeal, level: int, due, now, calendar, settings) -> None:
    threshold = settings.escalate_head_after if level == 1 else settings.escalate_leadership_after
    moment = min(calendar.moment_overdue_by(due, threshold), now)
    wording = DEADLINE_WORDING.get(appeal.status, "Срок истёк")
    owner = appeal.assignee.short_name.rstrip(".") if appeal.assignee else "не назначен"
    blocked = {appeal.author_id, appeal.about_person_id}

    if level == 1:
        head = appeal.assignee.manager() if appeal.assignee else None
        if head is not None and head.pk in blocked:
            head = None
        if head is None:  # nobody between the assignee and leadership: go straight to the top
            head = next((leader for leader in routing.leadership() if leader.pk not in blocked), None)
        appeal.escalation_level = 1
        appeal.escalated_to = head
        appeal.save(update_fields=["escalation_level", "escalated_to"])
        to = head.short_name.rstrip(".") if head else "руководство"
        add_event(
            appeal, K.ESCALATED, at=moment, meta={"level": 1},
            text=f"{wording}: просрочка {_days_word(threshold)} Ответственный — {owner}. "
                 f"Обращение на контроле у руководителя: {to}.",
        )
        notify(head, appeal, f"Просрочено обращение {appeal.number} (ответственный — {owner}). Оно на вашем контроле.",
               kind="escalated", at=moment)
        notify(appeal.assignee, appeal, f"Обращение {appeal.number} просрочено и передано на контроль руководителю.",
               kind="escalated", at=moment)
    else:
        appeal.escalation_level = 2
        appeal.save(update_fields=["escalation_level"])
        add_event(
            appeal, K.ESCALATED, at=moment, meta={"level": 2},
            text=f"{wording}: просрочка {_days_word(threshold)} Ответственный — {owner}. "
                 f"Обращение на контроле у руководства компании.",
        )
        for leader in routing.leadership():
            if leader.pk not in blocked:
                notify(leader, appeal, f"Просрочка {_days_word(threshold)}: обращение {appeal.number}, ответственный — {owner}.",
                       kind="escalated", at=moment)


def tick_one(appeal, now=None, calendar=None, settings=None) -> dict:
    """Reminder and escalation for one request. Safe to call any number of times."""
    now = now or clock.now()
    calendar = calendar or workcal.get_calendar()
    settings = settings or SystemSettings.load()
    stats = {"reminders": 0, "escalations": 0}
    if appeal.status not in Appeal.CLOCK_STATUSES:
        return stats
    due = appeal.current_due
    if due is None:
        return stats
    today = timezone.localtime(now).date()
    with transaction.atomic():
        if now <= due:
            if timezone.localtime(due).date() == today and appeal.reminded_on != today:
                appeal.reminded_on = today
                appeal.save(update_fields=["reminded_on"])
                add_event(appeal, K.REMINDER, at=now, visibility=Event.Visibility.INTERNAL,
                          text=f"Срок истекает сегодня. Напоминание ответственному ({appeal.deadline_kind.lower()}).")
                notify(appeal.assignee, appeal, f"Сегодня истекает срок по обращению {appeal.number}.",
                       kind="reminder", at=now)
                stats["reminders"] += 1
            return stats
        overdue = calendar.working_days_after(due, now)
        if overdue >= settings.escalate_leadership_after:
            target = 2
        elif overdue >= settings.escalate_head_after:
            target = 1
        else:
            target = 0
        while appeal.escalation_level < target:
            _escalate(appeal, appeal.escalation_level + 1, due, now, calendar, settings)
            stats["escalations"] += 1
    return stats


def tick(now=None) -> dict:
    now = now or clock.now()
    calendar = workcal.get_calendar()
    settings = SystemSettings.load()
    stats = {"reminders": 0, "escalations": 0, "auto_closed": 0}

    running = Appeal.objects.filter(status__in=Appeal.CLOCK_STATUSES).select_related("assignee__department", "author")
    for appeal in running:
        for key, value in tick_one(appeal, now, calendar, settings).items():
            stats[key] += value

    waiting = Appeal.objects.filter(status=S.IMPLEMENTED, implemented_at__isnull=False)
    for appeal in waiting:
        closes_at = appeal.implemented_at + timedelta(days=settings.confirm_days)
        if now >= closes_at:
            with transaction.atomic():
                appeal.status = S.CLOSED
                appeal.closed_at = closes_at
                appeal.save(update_fields=["status", "closed_at"])
                add_event(appeal, K.STATUS, at=closes_at, from_status=S.IMPLEMENTED, to_status=S.CLOSED,
                          text=f"Закрыто автоматически: автор не ответил за {settings.confirm_days} дн.")
                stats["auto_closed"] += 1
    return stats
