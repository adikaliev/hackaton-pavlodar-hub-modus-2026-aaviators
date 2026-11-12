"""The request lifecycle: every state change goes through a function in this module.

Each function checks permissions, validates input, updates the request, writes
one history event and queues notifications. Notifications are written to the
in-app list (core) and to the outgoing event log; this module never talks to an
external system.
"""
from __future__ import annotations

import math
import re
from datetime import date

from django.conf import settings
from django.db import transaction

from ..models import Appeal, Attachment, Employee, Event, Notification, OutboxEvent, SystemSettings
from . import clock, permissions, routing, workcal

S = Appeal.Status
K = Event.Kind
PUBLIC = Event.Visibility.PUBLIC
INTERNAL = Event.Visibility.INTERNAL

MIN_REASON_LENGTH = 10


class WorkflowError(Exception):
    """A rule of the process was broken. The message is shown to the user."""


# --------------------------------------------------------------------------- helpers


def add_event(appeal, kind, *, actor=None, text="", visibility=PUBLIC, from_status="", to_status="", meta=None, at=None):
    return Event.objects.create(
        appeal=appeal, kind=kind, actor=actor, text=text.strip(), visibility=visibility,
        from_status=from_status, to_status=to_status, meta=meta or {}, created_at=at or clock.now(),
    )


def notify(recipient, appeal, text, *, kind="status", actor=None, at=None) -> None:
    """In-app notification plus a row in the outgoing event log."""
    if recipient is None or (actor is not None and recipient.pk == actor.pk):
        return
    moment = at or clock.now()
    Notification.objects.create(recipient=recipient, appeal=appeal, text=text[:500], created_at=moment)
    # Only the number, the status and a link leave the system (solution design, section 7.1).
    OutboxEvent.objects.create(
        created_at=moment, kind=kind, appeal=appeal, recipient=recipient,
        payload={
            "number": appeal.number,
            "status": appeal.get_status_display(),
            "event": kind,
            "path": f"/a/{appeal.number}/",
        },
    )


def _notify_author(appeal, text, *, kind="status", actor=None) -> None:
    notify(appeal.author, appeal, text, kind=kind, actor=actor)


def _notify_followers(appeal, text, *, actor=None) -> None:
    """People who backed the request ("me too") or whose duplicate was merged into it."""
    for person in appeal.supporters.all():
        if person.pk != appeal.author_id:
            notify(person, appeal, text, kind="followed", actor=actor)


def _first_response(appeal, moment) -> None:
    if appeal.first_response_at is None:
        appeal.first_response_at = moment


def _move(appeal, status) -> str:
    """Change status. A new stage starts a new deadline, so escalation starts over."""
    previous = appeal.status
    appeal.status = status
    appeal.escalation_level = 0
    appeal.escalated_to = None
    appeal.reminded_on = None
    return previous


def _require(emp, appeal, action) -> None:
    if action not in permissions.actions(emp, appeal):
        raise WorkflowError("Это действие сейчас недоступно: проверьте статус обращения и свою роль.")


def _require_text(text, what="комментарий", minimum=1) -> str:
    text = (text or "").strip()
    if len(text) < minimum:
        if minimum > 1:
            raise WorkflowError(f"Напишите {what} — не короче {minimum} символов.")
        raise WorkflowError(f"Напишите {what}.")
    return text


def _leadership_meta(actor, appeal) -> dict:
    return {"leadership": True} if actor.is_leadership and appeal.assignee_id != actor.pk else {}


def next_number() -> str:
    last = 0
    for number in Appeal.objects.values_list("number", flat=True):
        match = re.fullmatch(r"A-(\d+)", number)
        if match:
            last = max(last, int(match.group(1)))
    return f"A-{last + 1:03d}"


def deadline_days(category, type, priority) -> tuple[int, int]:
    """(first response, decision) in working days for a category, type and priority."""
    first = category.first_response_days
    if type == Appeal.Type.PROBLEM:
        decision = category.problem_decision_days
    elif type == Appeal.Type.IDEA:
        decision = category.idea_decision_days
    else:
        decision = category.first_response_days
    if priority == Appeal.Priority.HIGH:
        factor = SystemSettings.load().high_priority_factor
        first = max(1, math.ceil(first * factor))
        decision = max(1, math.ceil(decision * factor))
    return first, max(decision, first)


def validate_upload(upload) -> None:
    extension = upload.name.rsplit(".", 1)[-1].lower() if "." in upload.name else ""
    if extension not in settings.ATTACHMENT_ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(settings.ATTACHMENT_ALLOWED_EXTENSIONS))
        raise WorkflowError(f"Файл «{upload.name}» не принят. Разрешены: {allowed}.")
    if upload.size > settings.ATTACHMENT_MAX_BYTES:
        raise WorkflowError(f"Файл «{upload.name}» больше {settings.ATTACHMENT_MAX_BYTES // 1024 // 1024} МБ.")


def attach(appeal, uploads, actor) -> None:
    for upload in uploads:
        validate_upload(upload)
    for upload in uploads:
        Attachment.objects.create(
            appeal=appeal, file=upload, name=upload.name[:255], size=upload.size, uploaded_by=actor,
            created_at=clock.now(),
        )


# --------------------------------------------------------------------------- registration


@transaction.atomic
def create_appeal(
    *, author, type, category, text, proposed_solution="", priority=Appeal.Priority.MEDIUM, confidential=False,
    about_person=None, sensitive=False, published=True, registered_by=None, source=Appeal.Source.WEB, files=(),
    number=None,
) -> Appeal:
    text = _require_text(text, "описание", MIN_REASON_LENGTH)
    if category is None or not category.is_active:
        raise WorkflowError("Выберите категорию.")
    if about_person is not None and about_person.pk == author.pk:
        raise WorkflowError("Обращение не может касаться действий самого автора.")
    if registered_by is not None and registered_by.pk == author.pk:
        registered_by = None
    sensitive = bool(sensitive or about_person)
    confidential = bool(confidential or sensitive)  # sensitive requests are confidential automatically
    now = clock.now()
    calendar = workcal.get_calendar()

    routed = routing.route(
        type=type, category=category, author=author, priority=priority, sensitive=sensitive, about_person=about_person
    )
    first_days, decision_days = deadline_days(category, type, priority)
    appeal = Appeal.objects.create(
        number=number or next_number(), type=type, category=category, text=text,
        proposed_solution=(proposed_solution or "").strip(), priority=priority, status=S.NEW,
        author=author, registered_by=registered_by, source=source,
        is_confidential=confidential, is_sensitive=sensitive, about_person=about_person,
        is_published=bool(published) and not confidential,
        assignee=routed.assignee, routing_rule=routed.rule, routing_note=routed.note[:500],
        auto_assigned=True, via_default_rule=routed.via_default,
        created_at=now,
        first_response_due=calendar.due_after(now, first_days),
        decision_due=calendar.due_after(now, decision_days),
    )
    created_text = ""
    if registered_by is not None:
        created_text = f"Зарегистрировано со слов сотрудника. Источник: {appeal.get_source_display().lower()}."
    add_event(appeal, K.CREATED, actor=registered_by or author, text=created_text, to_status=S.NEW)
    add_event(appeal, K.ASSIGNED, text=routed.note, meta={"rule": routed.rule.order if routed.rule else None})
    attach(appeal, files, registered_by or author)

    due = calendar_date(appeal.first_response_due)
    notify(appeal.assignee, appeal, f"Новое обращение {appeal.number}. Первый ответ — до {due}.", kind="assigned")
    notify(
        author, appeal,
        f"Обращение {appeal.number} зарегистрировано. Ответственный: "
        f"{appeal.assignee.short_name if appeal.assignee else 'назначается'}, первый ответ — до {due}.",
        kind="registered",  # the receipt: sent to the author even when they filed the request themselves
    )
    return appeal


def calendar_date(moment) -> str:
    from django.utils import timezone

    return timezone.localtime(moment).strftime("%d.%m.%Y")


# --------------------------------------------------------------------------- review


@transaction.atomic
def take(appeal, actor) -> None:
    _require(actor, appeal, "take")
    now = clock.now()
    _first_response(appeal, now)
    previous = _move(appeal, S.REVIEW)
    appeal.save()
    add_event(
        appeal, K.STATUS, actor=actor, text="Взято на рассмотрение.", from_status=previous, to_status=S.REVIEW,
        meta=_leadership_meta(actor, appeal),
    )
    due = calendar_date(appeal.decision_due)
    _notify_author(appeal, f"Обращение {appeal.number} рассматривается. Решение — до {due}.", actor=actor)


@transaction.atomic
def ask(appeal, actor, text) -> None:
    """Ask the author a question. The deadline is paused until the author answers."""
    _require(actor, appeal, "ask")
    text = _require_text(text, "вопрос автору")
    now = clock.now()
    _first_response(appeal, now)
    appeal.paused_at = now
    previous = _move(appeal, S.WAITING)
    appeal.save()
    add_event(appeal, K.QUESTION, actor=actor, text=text, from_status=previous, to_status=S.WAITING,
              meta=_leadership_meta(actor, appeal))
    _notify_author(appeal, f"По обращению {appeal.number} нужен ваш ответ.", kind="question", actor=actor)


@transaction.atomic
def answer(appeal, actor, text) -> None:
    """The author answers; the request returns to review and the deadline resumes."""
    _require(actor, appeal, "answer")
    text = _require_text(text, "ответ")
    now = clock.now()
    calendar = workcal.get_calendar()
    if appeal.paused_at and appeal.decision_due:
        from django.utils import timezone

        paused_days = calendar.count_working_days(
            timezone.localtime(appeal.paused_at).date(), timezone.localtime(now).date()
        )
        if paused_days:
            appeal.decision_due = calendar.extend(appeal.decision_due, paused_days)
    appeal.paused_at = None
    previous = _move(appeal, S.REVIEW)
    appeal.save()
    add_event(appeal, K.ANSWER, actor=actor, text=text, from_status=previous, to_status=S.REVIEW)
    notify(appeal.assignee, appeal, f"Автор ответил на вопрос по обращению {appeal.number}.", kind="answer", actor=actor)


@transaction.atomic
def message(appeal, actor, text, files=()) -> None:
    """A message in the thread between the author and the people handling the request."""
    _require(actor, appeal, "message")
    text = _require_text(text, "сообщение")
    now = clock.now()
    if permissions.is_author(actor, appeal):
        add_event(appeal, K.MESSAGE, actor=actor, text=text)
        attach(appeal, files, actor)
        notify(appeal.assignee, appeal, f"Новое сообщение автора по обращению {appeal.number}.", kind="message", actor=actor)
        return
    previous = ""
    if appeal.status == S.NEW:
        _first_response(appeal, now)
        previous = _move(appeal, S.REVIEW)
        appeal.save()
    add_event(appeal, K.MESSAGE, actor=actor, text=text, from_status=previous, to_status=S.REVIEW if previous else "",
              meta=_leadership_meta(actor, appeal))
    attach(appeal, files, actor)
    _notify_author(appeal, f"Новое сообщение по обращению {appeal.number}.", kind="message", actor=actor)


@transaction.atomic
def note(appeal, actor, text) -> None:
    """Internal comment: visible to the people handling the request, never to the author."""
    _require(actor, appeal, "note")
    text = _require_text(text, "комментарий")
    add_event(appeal, K.NOTE, actor=actor, text=text, visibility=INTERNAL)
    notify(appeal.assignee, appeal, f"Внутренний комментарий по обращению {appeal.number}.", kind="note", actor=actor)


@transaction.atomic
def decide(appeal, actor, decision, reason, *, next_actions="", planned_date: date | None = None, alternative="") -> None:
    """Record a decision. A decision without written reasons is not accepted."""
    _require(actor, appeal, "decide")
    reason = _require_text(reason, "обоснование решения", MIN_REASON_LENGTH)
    if decision not in Appeal.Decision.values:
        raise WorkflowError("Выберите решение: принять, отклонить или «уже сделано».")
    now = clock.now()
    _first_response(appeal, now)
    appeal.decision = decision
    appeal.decision_reason = reason
    appeal.next_actions = (next_actions or "").strip()
    appeal.alternative = (alternative or "").strip()
    appeal.decided_at = now
    appeal.paused_at = None
    meta = _leadership_meta(actor, appeal)

    if decision == Appeal.Decision.ACCEPTED:
        if planned_date is None:
            raise WorkflowError("Укажите плановую дату реализации: без неё решение нельзя проконтролировать.")
        if planned_date < clock.today():
            raise WorkflowError("Плановая дата не может быть в прошлом.")
        appeal.planned_date = planned_date
        previous = _move(appeal, S.DECIDED)
        appeal.save()
        add_event(appeal, K.DECISION, actor=actor, text=reason, from_status=previous, to_status=S.DECIDED, meta=meta)
        text = f"По обращению {appeal.number} принято решение: принято. Срок реализации — {planned_date:%d.%m.%Y}."
    elif decision == Appeal.Decision.REJECTED:
        appeal.closed_at = now
        previous = _move(appeal, S.REJECTED)
        appeal.save()
        add_event(appeal, K.DECISION, actor=actor, text=reason, from_status=previous, to_status=S.REJECTED, meta=meta)
        text = f"По обращению {appeal.number} принято решение: отклонено. Обоснование — в карточке обращения."
    else:  # already done: the author still confirms that the problem is gone
        appeal.result = reason
        appeal.implemented_at = now
        previous = _move(appeal, S.IMPLEMENTED)
        appeal.save()
        add_event(appeal, K.DECISION, actor=actor, text=reason, from_status=previous, to_status=S.IMPLEMENTED, meta=meta)
        text = f"По обращению {appeal.number}: уже сделано. Подтвердите, что вопрос решён."
    _notify_author(appeal, text, kind="decision", actor=actor)
    _notify_followers(appeal, f"По обращению {appeal.number}, которое вы поддержали, принято решение.", actor=actor)


@transaction.atomic
def close_praise(appeal, actor, text) -> None:
    """Positive feedback takes a short path: passed on to the person, then closed."""
    _require(actor, appeal, "close_praise")
    text = _require_text(text, "кому и как передан отзыв", MIN_REASON_LENGTH)
    now = clock.now()
    _first_response(appeal, now)
    appeal.decision = Appeal.Decision.ACCEPTED
    appeal.decision_reason = text
    appeal.result = text
    appeal.decided_at = now
    appeal.closed_at = now
    previous = _move(appeal, S.CLOSED)
    appeal.save()
    add_event(appeal, K.RESULT, actor=actor, text=text, from_status=previous, to_status=S.CLOSED)
    _notify_author(appeal, f"Спасибо за отзыв {appeal.number}: он передан адресату.", kind="decision", actor=actor)


# --------------------------------------------------------------------------- implementation


@transaction.atomic
def start(appeal, actor) -> None:
    _require(actor, appeal, "start")
    previous = _move(appeal, S.IN_PROGRESS)
    appeal.save()
    add_event(appeal, K.STATUS, actor=actor, text="Начата реализация.", from_status=previous, to_status=S.IN_PROGRESS)
    _notify_author(appeal, f"Обращение {appeal.number}: начата реализация.", actor=actor)


@transaction.atomic
def progress(appeal, actor, text, planned_date: date | None = None) -> None:
    """Report progress; optionally move the planned date (the change stays in the history)."""
    _require(actor, appeal, "progress")
    text = _require_text(text, "что сделано и что дальше")
    meta, previous, to_status = {}, "", ""
    if planned_date and planned_date != appeal.planned_date:
        if planned_date < clock.today():
            raise WorkflowError("Плановая дата не может быть в прошлом.")
        meta = {"planned_from": f"{appeal.planned_date:%d.%m.%Y}" if appeal.planned_date else "",
                "planned_to": f"{planned_date:%d.%m.%Y}"}
        appeal.planned_date = planned_date
        appeal.escalation_level, appeal.escalated_to, appeal.reminded_on = 0, None, None
    if appeal.status == S.DECIDED:
        previous, to_status = _move(appeal, S.IN_PROGRESS), S.IN_PROGRESS
    appeal.save()
    add_event(appeal, K.PROGRESS, actor=actor, text=text, from_status=previous, to_status=to_status, meta=meta)
    _notify_author(appeal, f"Обращение {appeal.number}: есть новости о ходе реализации.", kind="progress", actor=actor)


@transaction.atomic
def implement(appeal, actor, result) -> None:
    _require(actor, appeal, "implement")
    result = _require_text(result, "что именно сделано", MIN_REASON_LENGTH)
    now = clock.now()
    appeal.result = result
    appeal.implemented_at = now
    appeal.author_confirmed = None
    previous = _move(appeal, S.IMPLEMENTED)
    appeal.save()
    add_event(appeal, K.RESULT, actor=actor, text=result, from_status=previous, to_status=S.IMPLEMENTED)
    _notify_author(appeal, f"Обращение {appeal.number} реализовано. Подтвердите, что вопрос решён.", kind="implemented", actor=actor)
    _notify_followers(appeal, f"Обращение {appeal.number}, которое вы поддержали, реализовано.", actor=actor)


@transaction.atomic
def confirm(appeal, actor) -> None:
    _require(actor, appeal, "confirm")
    appeal.author_confirmed = True
    appeal.closed_at = clock.now()
    previous = _move(appeal, S.CLOSED)
    appeal.save()
    add_event(appeal, K.CONFIRMED, actor=actor, text="Автор подтвердил: вопрос решён.", from_status=previous, to_status=S.CLOSED)
    notify(appeal.assignee, appeal, f"Автор подтвердил результат по обращению {appeal.number}.", kind="confirmed", actor=actor)


@transaction.atomic
def reopen(appeal, actor, text) -> None:
    """The author says the problem is not solved; the request goes back to work with a fresh date."""
    _require(actor, appeal, "reopen")
    text = _require_text(text, "что осталось нерешённым", MIN_REASON_LENGTH)
    calendar = workcal.get_calendar()
    appeal.author_confirmed = False
    appeal.reopened_count += 1
    appeal.implemented_at = None
    appeal.planned_date = calendar.add_working_days(calendar.effective_day(clock.now()), 5)
    previous = _move(appeal, S.IN_PROGRESS)
    appeal.save()
    add_event(appeal, K.REOPENED, actor=actor, text=text, from_status=previous, to_status=S.IN_PROGRESS)
    notify(appeal.assignee, appeal, f"Автор не подтвердил результат по обращению {appeal.number}: возвращено в работу.",
           kind="reopened", actor=actor)


# --------------------------------------------------------------------------- owner changes


def _restart_first_response(appeal) -> None:
    """A new owner gets a fresh first-response deadline; the decision deadline does not move."""
    if appeal.status == S.NEW:
        first_days, _ = deadline_days(appeal.category, appeal.type, appeal.priority)
        appeal.first_response_due = workcal.get_calendar().due_after(clock.now(), first_days)
    appeal.escalation_level, appeal.escalated_to, appeal.reminded_on = 0, None, None


@transaction.atomic
def not_mine(appeal, actor, text) -> None:
    """"Not mine": the rules run again without this person. Nothing is closed on the author."""
    _require(actor, appeal, "not_mine")
    text = _require_text(text, "почему обращение не ваше и кому его лучше передать", MIN_REASON_LENGTH)
    refused = {actor.pk}
    for event in appeal.events.filter(kind=K.ASSIGNED):
        refused.update(event.meta.get("refused", []))
    routed = routing.route(
        type=appeal.type, category=appeal.category, author=appeal.author, priority=appeal.priority,
        sensitive=appeal.is_sensitive, about_person=appeal.about_person, excluded=refused,
    )
    if routed.assignee is None:
        raise WorkflowError("Не удалось найти другого ответственного. Обратитесь к координатору.")
    appeal.assignee = routed.assignee
    appeal.routing_rule = routed.rule
    appeal.routing_note = routed.note[:500]
    appeal.auto_assigned = False
    appeal.via_default_rule = routed.via_default
    _restart_first_response(appeal)
    appeal.save()
    add_event(appeal, K.NOTE, actor=actor, text=f"Не моё: {text}", visibility=INTERNAL)
    add_event(appeal, K.ASSIGNED, text=f"Ответственный изменён. {routed.note}",
              meta={"refused": sorted(refused), "rule": routed.rule.order if routed.rule else None})
    notify(routed.assignee, appeal, f"Вам передано обращение {appeal.number}.", kind="assigned", actor=actor)


@transaction.atomic
def reassign(appeal, actor, target: Employee, reason) -> None:
    """Manual assignment by a manager or the coordinator, overriding the rule. Always with a reason."""
    _require(actor, appeal, "reassign")
    reason = _require_text(reason, "причину переназначения", MIN_REASON_LENGTH)
    if target.pk == appeal.assignee_id:
        raise WorkflowError("Этот сотрудник уже ответственный.")
    if not permissions.can_reassign_to(actor, appeal, target):
        raise WorkflowError("Этому сотруднику нельзя передать обращение: руководитель назначает только в своём подразделении.")
    previous_owner = appeal.assignee
    appeal.assignee = target
    appeal.auto_assigned = False  # via_default_rule stays: it records that the rules did not cover the request
    appeal.routing_note = f"Назначил вручную {actor.short_name}: {reason}"[:500]
    _restart_first_response(appeal)
    appeal.save()
    was = previous_owner.short_name if previous_owner else "—"
    add_event(appeal, K.ASSIGNED, actor=actor, text=f"Ответственный: {target.short_name} (был {was}). Причина: {reason}",
              meta={"manual": True})
    notify(target, appeal, f"Вам передано обращение {appeal.number}.", kind="assigned", actor=actor)
    notify(previous_owner, appeal, f"Обращение {appeal.number} передано другому ответственному.", kind="assigned", actor=actor)


@transaction.atomic
def extend(appeal, actor, days, reason) -> None:
    """Extend the decision deadline once, with a reason; the author is told."""
    _require(actor, appeal, "extend")
    reason = _require_text(reason, "причину продления", MIN_REASON_LENGTH)
    try:
        days = int(days)
    except (TypeError, ValueError):
        raise WorkflowError("Укажите, на сколько рабочих дней продлить срок.") from None
    if not 1 <= days <= 10:
        raise WorkflowError("Срок можно продлить на 1–10 рабочих дней.")
    appeal.decision_due = workcal.get_calendar().extend(max(appeal.decision_due, clock.now()), days)
    appeal.deadline_extended = True
    appeal.escalation_level, appeal.escalated_to, appeal.reminded_on = 0, None, None
    appeal.save()
    due = calendar_date(appeal.decision_due)
    add_event(appeal, K.EXTENDED, actor=actor, text=f"Срок решения продлён до {due}. Причина: {reason}")
    _notify_author(appeal, f"Срок решения по обращению {appeal.number} продлён до {due}.", kind="extended", actor=actor)


@transaction.atomic
def mark_duplicate(appeal, actor, main: Appeal, text="") -> None:
    """Merge a request into the main one. The duplicate's author follows the main request."""
    _require(actor, appeal, "duplicate")
    if main.pk == appeal.pk:
        raise WorkflowError("Нельзя объединить обращение с самим собой.")
    if main.status == S.DUPLICATE:
        raise WorkflowError(f"{main.number} само является дубликатом. Выберите основное обращение.")
    now = clock.now()
    _first_response(appeal, now)
    appeal.duplicate_of = main
    appeal.decision_reason = (text or "").strip() or f"Та же тема, что в обращении {main.number}."
    appeal.decided_at = now
    appeal.closed_at = now
    appeal.paused_at = None
    previous = _move(appeal, S.DUPLICATE)
    appeal.save()
    if appeal.author_id != main.author_id:
        main.supporters.add(appeal.author)
    add_event(appeal, K.DUPLICATE, actor=actor, text=f"Объединено с обращением {main.number}. {appeal.decision_reason}",
              from_status=previous, to_status=S.DUPLICATE)
    add_event(main, K.DUPLICATE, actor=actor, text=f"Присоединено обращение {appeal.number} на ту же тему.",
              visibility=INTERNAL)
    _notify_author(appeal, f"Обращение {appeal.number} объединено с {main.number}: новости придут по основному.",
                   kind="duplicate", actor=actor)


@transaction.atomic
def support(appeal, actor) -> None:
    """"Me too": a colleague backs an open request instead of filing a duplicate."""
    _require(actor, appeal, "support")
    appeal.supporters.add(actor)
    add_event(appeal, K.SUPPORT, actor=actor, text="+1 «У меня тоже».")


def log_confidential_view(appeal, viewer) -> None:
    """Views of sensitive requests are logged (solution design, section 4.8)."""
    if appeal.is_sensitive and not permissions.is_author(viewer, appeal):
        add_event(appeal, K.ACCESS, actor=viewer, text="Просмотр обращения.", visibility=INTERNAL)
