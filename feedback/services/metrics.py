"""Numbers for the dashboard (solution design, section 4.5; spec §2.7; dataset scenario 6).

Everything is computed from the requests the viewer is allowed to see, so the
same page serves leadership (the whole company) and a department head (their queue).
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import timedelta

from django.utils import timezone

from ..models import Appeal
from . import workcal

S = Appeal.Status


def _share(part: int, whole: int) -> int:
    return round(100 * part / whole) if whole else 0


def format_hours(hours: float | None, hours_per_day: int) -> str:
    if hours is None:
        return "—"
    if hours < hours_per_day:
        return f"{hours:.1f} ч".replace(".", ",")
    return f"{hours / hours_per_day:.1f} раб. дн.".replace(".", ",")


def _bars(counter: Counter, labels: dict | None = None, limit: int | None = None) -> list[dict]:
    items = counter.most_common(limit)
    top = max((count for _, count in items), default=0)
    return [
        {"label": labels.get(key, key) if labels else key, "count": count, "width": _share(count, top)}
        for key, count in items
    ]


def summary(appeals: list[Appeal], now) -> dict:
    calendar = workcal.get_calendar()
    total = len(appeals)
    type_labels, status_labels = dict(Appeal.Type.choices), dict(Appeal.Status.choices)

    by_type = Counter(a.type for a in appeals)
    by_status = Counter(a.status for a in appeals)
    by_group = Counter(a.category.group.name if a.category.group else "Без направления" for a in appeals)
    by_category = Counter(a.category.name for a in appeals)

    reviewed = [a for a in appeals if a.decided_at]
    with_outcome = [
        a for a in appeals
        if a.status in (S.IMPLEMENTED, S.REJECTED, S.CLOSED, S.DUPLICATE) and (a.result or a.decision_reason)
    ]
    implemented = [
        a for a in appeals
        if a.status in (S.IMPLEMENTED, S.CLOSED) and a.type != Appeal.Type.PRAISE
        and a.decision in (Appeal.Decision.ACCEPTED, Appeal.Decision.ALREADY_DONE)
    ]
    closed = [a for a in appeals if a.status in Appeal.FINAL_STATUSES]

    response_hours = [
        calendar.working_hours_between(a.created_at, a.first_response_at) for a in appeals if a.first_response_at
    ]
    avg_response = sum(response_hours) / len(response_hours) if response_hours else None

    answered_on_time = sum(1 for a in appeals if a.first_response_at and a.first_response_at <= a.first_response_due)
    answered_late = sum(1 for a in appeals if a.first_response_at and a.first_response_at > a.first_response_due)
    unanswered_late = sum(1 for a in appeals if not a.first_response_at and a.first_response_due and now > a.first_response_due)
    judged = answered_on_time + answered_late + unanswered_late

    # "Who is holding what": overdue requests by person and by department.
    overdue = []
    for a in appeals:
        days = a.overdue_days(now)
        if days is not None:
            overdue.append((a, days))
    overdue.sort(key=lambda item: (-item[0].escalation_level, -item[1]))

    open_by_person: Counter = Counter()
    for a in appeals:
        if a.status in Appeal.CLOCK_STATUSES and a.assignee_id:
            open_by_person[a.assignee_id] += 1

    holders: dict = {}
    for a, days in overdue:
        if a.assignee is None:
            continue
        row = holders.setdefault(a.assignee_id, {
            "person": a.assignee, "department": a.assignee.department, "overdue": 0, "max_days": 0,
            "escalated": 0, "open": open_by_person[a.assignee_id], "appeals": [],
        })
        row["overdue"] += 1
        row["max_days"] = max(row["max_days"], days)
        row["escalated"] += 1 if a.escalation_level >= 2 else 0
        row["appeals"].append(a)
    holder_rows = sorted(holders.values(), key=lambda r: (-r["overdue"], -r["max_days"]))
    for row in holder_rows:
        row["width"] = _share(row["overdue"], row["open"])

    open_by_dept: Counter = Counter()
    overdue_by_dept: Counter = Counter()
    for a in appeals:
        if a.status in Appeal.CLOCK_STATUSES and a.assignee and a.assignee.department:
            open_by_dept[a.assignee.department.name] += 1
    for a, _ in overdue:
        if a.assignee and a.assignee.department:
            overdue_by_dept[a.assignee.department.name] += 1
    dept_rows = [
        {"label": name, "overdue": count, "open": open_by_dept[name], "width": _share(count, open_by_dept[name])}
        for name, count in overdue_by_dept.most_common()
    ]

    # Recurring themes: requests that were raised again ("me too" votes and merged duplicates).
    recurring = sorted(
        ({"appeal": a, "repeats": a.repeat_count} for a in appeals if a.status != S.DUPLICATE),
        key=lambda item: -item["repeats"],
    )
    recurring = [item for item in recurring if item["repeats"] > 0][:6]

    # Themes by category group, this period against the previous one (14 days each).
    period = timedelta(days=14)
    recent: Counter = Counter()
    earlier: Counter = Counter()
    for a in appeals:
        name = a.category.group.name if a.category.group else "Без направления"
        if a.created_at >= now - period:
            recent[name] += 1
        elif a.created_at >= now - 2 * period:
            earlier[name] += 1
    top_recent = max(recent.values(), default=0)
    themes = [
        {"label": name, "count": by_group[name], "recent": recent[name], "earlier": earlier[name],
         "width": _share(recent[name], top_recent), "delta": recent[name] - earlier[name]}
        for name, _ in by_group.most_common()
    ]

    # Requests registered per week, for the last eight weeks.
    weeks = []
    week_start = timezone.localtime(now).date() - timedelta(days=timezone.localtime(now).weekday())
    counts = defaultdict(int)
    for a in appeals:
        day = timezone.localtime(a.created_at).date()
        counts[day - timedelta(days=day.weekday())] += 1
    for index in range(7, -1, -1):
        start = week_start - timedelta(weeks=index)
        weeks.append({"label": f"{start:%d.%m}", "count": counts[start], "start": start})
    top_week = max((w["count"] for w in weeks), default=0)
    for week in weeks:
        week["height"] = _share(week["count"], top_week)

    auto = sum(1 for a in appeals if a.auto_assigned)
    to_coordinator = sum(1 for a in appeals if a.via_default_rule)

    return {
        "total": total,
        "open": sum(1 for a in appeals if a.is_open),
        "closed": len(closed),
        "closed_share": _share(len(closed), total),
        # The four measures from spec §2.7.
        "reviewed_share": _share(len(reviewed), total),
        "reviewed": len(reviewed),
        "avg_response": format_hours(avg_response, calendar.hours_per_day),
        "responded": len(response_hours),
        "outcome_share": _share(len(with_outcome), total),
        "with_outcome": len(with_outcome),
        "implemented": len(implemented),
        # Guaranteed answer.
        "on_time_share": _share(answered_on_time, judged),
        "on_time": answered_on_time,
        "judged": judged,
        "overdue_count": len(overdue),
        "overdue": overdue,
        "escalated": [a for a, _ in overdue if a.escalation_level >= 2],
        "holders": holder_rows,
        "departments": dept_rows,
        # Structure.
        "by_type": _bars(by_type, type_labels),
        "by_status": [
            {"label": status_labels[key], "count": by_status[key], "width": _share(by_status[key], max(by_status.values(), default=0))}
            for key in Appeal.Status.values if by_status[key]
        ],
        "by_category": _bars(by_category, limit=8),
        "themes": themes,
        "recurring": recurring,
        "weeks": weeks,
        # Routing quality.
        "auto_share": _share(auto, total),
        "coordinator_share": _share(to_coordinator, total),
        "to_coordinator": to_coordinator,
    }
