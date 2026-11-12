"""Builds the demo database from the seed files in `data/`.

Nothing is stored with fixed dates. Each request has a script ("created 4
working days ago, taken into review a day later, ...") in
`data/seed_timeline.json`, and this loader replays the scripts through the same
workflow functions the interface uses. So the history, deadlines, escalations
and dashboard numbers are real, and they are up to date whenever the data is
loaded — on the day of the pitch as well as today.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, time as dtime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.db import transaction
from django.utils import timezone

from ..integrations import bitrix24, ensure_catalog, telegram
from ..models import (
    Appeal, Attachment, Category, CategoryGroup, Delivery, Department, Employee, Event, FunctionalRole, Holiday,
    Integration, Notification, OutboxEvent, RoutingRule, SystemSettings,
)
from . import clock, escalation, workcal, workflow

TYPES = {label: value for value, label in Appeal.Type.choices}
PRIORITIES = {label: value for value, label in Appeal.Priority.choices}
DEMO_ADMIN_USERNAME = "demo-admin"


def load_json(name: str):
    return json.loads((settings.SEED_DIR / name).read_text(encoding="utf-8"))


def _person(external_id) -> Employee:
    return Employee.objects.get(external_id=str(external_id))


def wipe() -> None:
    for model in (Delivery, OutboxEvent, Notification, Attachment, Event):
        model.objects.all().delete()
    Appeal.objects.update(duplicate_of=None)
    for model in (Appeal, RoutingRule, Category, CategoryGroup, FunctionalRole):
        model.objects.all().delete()
    Department.objects.update(head=None, parent=None)
    Employee.objects.all().delete()
    Department.objects.all().delete()
    Holiday.objects.all().delete()
    Integration.objects.all().delete()
    shutil.rmtree(settings.MEDIA_ROOT / "attachments", ignore_errors=True)


def seed_calendar() -> None:
    data = load_json("calendar_kz.json")
    system = SystemSettings.load()
    system.weekend_days = ",".join(str(day) for day in data["weekend_days"])
    system.work_start_hour = data["work_start_hour"]
    system.work_end_hour = data["work_end_hour"]
    system.clock_offset_minutes = 0
    system.save()
    Holiday.objects.bulk_create(
        Holiday(date=row["date"], name=row["name"], is_working=row.get("is_working", False)) for row in data["holidays"]
    )
    workcal.invalidate()
    clock.invalidate()


def seed_directory() -> dict:
    data = load_json("seed_directory.json")
    return bitrix24.import_directory(data["department.get"]["result"], data["user.get"]["result"])


def seed_reference() -> None:
    data = load_json("seed_reference.json")
    for external_id, access in data["access"].items():
        Employee.objects.filter(external_id=external_id).update(access=access)
    for external_id, deputy_id in data["deputies"].items():
        Employee.objects.filter(external_id=external_id).update(deputy=_person(deputy_id))

    roles = {}
    for row in data["roles"]:
        roles[row["code"]] = FunctionalRole.objects.create(code=row["code"], name=row["name"], holder=_person(row["holder"]))

    categories = {}
    for group_index, group_row in enumerate(data["groups"]):
        group = CategoryGroup.objects.create(
            name=group_row["name"], sort=(group_index + 1) * 10, default_role=roles.get(group_row.get("default_role"))
        )
        for index, row in enumerate(group_row["categories"]):
            categories[row["name"]] = Category.objects.create(
                name=row["name"], group=group, sort=(index + 1) * 10, keywords=row.get("keywords", ""),
                first_response_days=row.get("first_response_days", 2),
                problem_decision_days=row.get("problem_decision_days", 5),
                idea_decision_days=row.get("idea_decision_days", 10),
            )

    for row in data["rules"]:
        rule = RoutingRule.objects.create(
            order=row["order"], name=row["name"], sensitive_only=row.get("sensitive_only", False),
            request_type=row.get("type", ""), priority=row.get("priority", ""),
            target_kind=row["target"], target_role=roles.get(row.get("role")),
        )
        rule.categories.set([categories[name] for name in row.get("categories", [])])


def ensure_demo_admin() -> None:
    """A Django admin user for the reference-data pages. It has no password: the app signs it in for the admin persona."""
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(
        username=DEMO_ADMIN_USERNAME, defaults={"is_staff": True, "is_superuser": True}
    )
    if created:
        user.set_unusable_password()
        user.save()


class _Timeline:
    """Turns "N working days ago at H o'clock" into moments, relative to the day the data is loaded."""

    def __init__(self) -> None:
        self.calendar = workcal.get_calendar()
        self.now = timezone.now()
        self.today = timezone.localtime(self.now).date()

    def day(self, working_days_ago: int):
        day = self.today
        step = -1 if working_days_ago > 0 else 1
        for _ in range(abs(working_days_ago)):
            day += timedelta(days=step)
            while not self.calendar.is_working_day(day):
                day += timedelta(days=step)
        return day

    def moment(self, spec: dict):
        moment = timezone.make_aware(datetime.combine(self.day(spec["d"]), dtime(spec["h"], spec.get("m", 0))))
        return min(moment, self.now - timedelta(minutes=5))


def _run_step(appeal: Appeal, step: dict, timeline: _Timeline, default_next: str) -> None:
    action = step["do"]
    by = _person(step["by"]) if step.get("by") else None
    handler = by or appeal.assignee
    text = step.get("text", "")
    if action == "take":
        workflow.take(appeal, handler)
    elif action == "ask":
        workflow.ask(appeal, handler, text)
    elif action == "answer":
        workflow.answer(appeal, by or appeal.author, text)
    elif action == "message":
        workflow.message(appeal, by or appeal.author, text)
    elif action == "note":
        workflow.note(appeal, handler, text)
    elif action == "decide":
        planned = timeline.day(step["planned"]) if "planned" in step else None
        accepted = step["decision"] == Appeal.Decision.ACCEPTED  # the dataset's "next action" fits accepted requests only
        workflow.decide(
            appeal, handler, step["decision"], step["reason"],
            next_actions=step.get("next", default_next if accepted else ""),
            planned_date=planned, alternative=step.get("alternative", ""),
        )
    elif action == "start":
        workflow.start(appeal, handler)
    elif action == "progress":
        workflow.progress(appeal, handler, text)
    elif action == "implement":
        workflow.implement(appeal, handler, text)
    elif action == "confirm":
        workflow.confirm(appeal, by or appeal.author)
    elif action == "reopen":
        workflow.reopen(appeal, by or appeal.author, text)
    elif action == "close_praise":
        workflow.close_praise(appeal, handler, text)
    elif action == "duplicate":
        workflow.mark_duplicate(appeal, handler, Appeal.objects.get(number=step["main"]), text)
    elif action == "support":
        workflow.support(appeal, by)
    elif action == "reassign":
        workflow.reassign(appeal, handler, _person(step["to"]), text)
    else:
        raise ValueError(f"Unknown seed step: {action}")


def seed_requests() -> int:
    reference = load_json("seed_reference.json")
    plan = load_json("seed_timeline.json")
    timeline = _Timeline()
    categories = {c.name: c for c in Category.objects.all()}

    rows = {}
    for row in load_json("seed_requests.json"):
        rows[row["id"]] = {**row, "author": reference["dataset_authors"][row["author_role"]]}
    for row in load_json("seed_extra_requests.json"):
        if "id" in row:
            rows[row["id"]] = row

    # One global, chronological list: absences, registrations and every later step.
    actions = []
    for absence in plan.get("absences", []):
        actions.append((timeline.moment(absence["from"]), 0, "absence", absence))
    for number, script in plan["appeals"].items():
        actions.append((timeline.moment(script["created"]), 1, "create", number))
        for step in script.get("steps", []):
            actions.append((timeline.moment(step), 2, "step", (number, step)))
    actions.sort(key=lambda item: (item[0], item[1]))

    for moment, _, kind, payload in actions:
        with clock.freeze(moment):
            if kind == "absence":
                Employee.objects.filter(external_id=payload["employee"]).update(absent=True, absence_note=payload["note"])
            elif kind == "create":
                row = rows[payload]
                appeal = workflow.create_appeal(
                    number=row["id"], author=_person(row["author"]), type=TYPES[row["type"]],
                    category=categories[row["category"]], text=row["text"],
                    proposed_solution=row.get("proposed_solution", ""), priority=PRIORITIES[row["priority"]],
                    confidential=row.get("confidential", False),
                    about_person=_person(row["about_person"]) if row.get("about_person") else None,
                    registered_by=_person(row["registered_by"]) if row.get("registered_by") else None,
                    source=row.get("source", Appeal.Source.WEB),
                )
                sample = plan.get("attachments", {}).get(row["id"])
                if sample:
                    path = settings.SEED_DIR / "attachments" / sample
                    with path.open("rb") as handle:
                        Attachment.objects.create(
                            appeal=appeal, file=File(handle, name=sample), name=sample, size=path.stat().st_size,
                            uploaded_by=appeal.author, created_at=moment,
                        )
            else:
                number, step = payload
                appeal = Appeal.objects.select_related("assignee", "author", "category").get(number=number)
                escalation.tick_one(appeal, moment)  # what the system had already done by this moment
                appeal.refresh_from_db()
                _run_step(appeal, step, timeline, rows[number].get("next_action", ""))
    return len(plan["appeals"])


@transaction.atomic
def reset_and_seed() -> dict:
    """Throw away all demo data and rebuild it. Telegram links survive, so nobody has to re-link."""
    telegram_links = dict(
        Employee.objects.exclude(telegram_chat_id="").exclude(external_id="").values_list("external_id", "telegram_chat_id")
    )
    wipe()
    seed_calendar()
    directory = seed_directory()
    seed_reference()
    ensure_catalog()
    if telegram.configured():
        Integration.objects.filter(code="telegram").update(enabled=True)
    ensure_demo_admin()
    for external_id, chat_id in telegram_links.items():
        Employee.objects.filter(external_id=external_id).update(telegram_chat_id=chat_id)
    appeals = seed_requests()
    ticked = escalation.tick()
    # The demo starts with a clean bell: history is in the requests, not in unread notifications.
    Notification.objects.filter(created_at__lt=timezone.now() - timedelta(days=2)).update(read_at=timezone.now())
    settle_outbox()
    return {**directory, "appeals": appeals, **ticked}


def settle_outbox() -> None:
    """Close the outgoing events produced by replaying history.

    Loading demo data must never message real people, so nothing here goes to
    Telegram. Events of the last three days are passed through the Bitrix24
    simulator only, so the integration log is not empty when the demo starts.
    """
    now = timezone.now()
    simulator = bitrix24.Bitrix24NotifySimulator()
    integration = Integration.objects.get(code=simulator.code)
    recent = OutboxEvent.objects.filter(created_at__gte=now - timedelta(days=3)).select_related("recipient")
    if integration.enabled:
        Delivery.objects.bulk_create(
            Delivery(
                event=event, integration=integration, status=Delivery.Status.SIMULATED, attempts=1,
                request=simulator.build_request(event), created_at=event.created_at, updated_at=event.created_at,
            )
            for event in recent if simulator.applicable(event.recipient)
        )
        integration.last_ok_at = now
        integration.save(update_fields=["last_ok_at"])
    OutboxEvent.objects.filter(processed_at__isnull=True).update(processed_at=now)


def is_seeded() -> bool:
    return Employee.objects.exists()
