"""Pages of the feedback system. Business rules live in `services/`; views only read input and render."""
from __future__ import annotations

from datetime import date, timedelta
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.db.models import Count, Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_POST

from .integrations import bitrix24, telegram
from .middleware import SESSION_KEY
from .models import (
    Appeal, Attachment, Category, CategoryGroup, Delivery, Department, Employee, Event, Integration, Notification,
    OutboxEvent, RoutingRule,
)
from .services import clock, escalation, metrics, permissions, routing, seed, similar, workcal, workflow
from .services.workflow import WorkflowError

S = Appeal.Status
LIST_RELATED = ("category__group", "author__department", "assignee__department", "escalated_to")


# --------------------------------------------------------------------------- helpers


def persona_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.employee is None:
            return redirect(f"{reverse('landing')}?next={request.get_full_path()}")
        return view(request, *args, **kwargs)

    return wrapper


def _safe_next(request, fallback: str) -> str:
    target = request.POST.get("next") or request.GET.get("next") or ""
    if target and url_has_allowed_host_and_scheme(target, allowed_hosts={request.get_host()}):
        return target
    return fallback


def deadline_state(appeal: Appeal, now) -> dict:
    """How the deadline looks in lists and on the request page: a tone, an icon and a label."""
    if appeal.status == S.WAITING:
        return {"tone": "wait", "icon": "⏸", "label": "Срок на паузе: ждём ответа автора", "rank": 5}
    if appeal.status == S.IMPLEMENTED:
        return {"tone": "wait", "icon": "⏸", "label": "Ждём подтверждения автора", "rank": 6}
    due = appeal.current_due
    if due is None:
        return {"tone": "none", "icon": "", "label": "", "rank": 9}
    kind = appeal.deadline_kind
    overdue = appeal.overdue_days(now)
    local_due = timezone.localtime(due)
    if overdue is not None:
        label = f"Просрочено на {overdue} раб. дн." if overdue else "Просрочено сегодня"
        where = {1: "на контроле у руководителя", 2: "на контроле у руководства"}.get(appeal.escalation_level, "")
        return {"tone": "critical", "icon": "▲", "label": label, "where": where, "kind": kind, "due": due,
                "rank": 0 - appeal.escalation_level - overdue / 100, "overdue": overdue}
    left = appeal.days_left(now)
    if left == 0:
        return {"tone": "warning", "icon": "●", "label": f"Срок сегодня до {local_due:%H:%M}", "kind": kind, "due": due, "rank": 2}
    if left == 1:
        return {"tone": "warning", "icon": "●", "label": f"Остался 1 раб. день · до {local_due:%d.%m}", "kind": kind, "due": due, "rank": 3}
    return {"tone": "ok", "icon": "", "label": f"до {local_due:%d.%m} · {left} раб. дн.", "kind": kind, "due": due,
            "rank": 4 + left / 1000}


def _rows(appeals, viewer, now) -> list[dict]:
    return [
        {"appeal": a, "deadline": deadline_state(a, now), "sees_author": permissions.sees_author(viewer, a)}
        for a in appeals
    ]


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


# --------------------------------------------------------------------------- landing and demo controls


SCENARIOS = [
    {
        "n": 1, "title": "Создать обращение",
        "what": "Тип, категория, описание, файл. После отправки — квитанция: номер, ответственный, срок ответа.",
        "steps": [("7", "new", "Подать обращение как специалист по закупкам")],
    },
    {
        "n": 2, "title": "Ответственный по правилам и замещение",
        "what": "Правила назначают роль, а не человека. Ответственная за обучение в отпуске — обращение получает заместитель. "
                "Категория без правила уходит координатору.",
        "steps": [
            ("12", "appeal:A-016", "A-016: назначен заместитель"),
            ("23", "rules", "Правила и проверка «кто получит»"),
            ("21", "appeal:A-024", "A-024: правило по умолчанию → координатор"),
        ],
    },
    {
        "n": 3, "title": "Статус, уточнение, история",
        "what": "Ответственный задаёт вопрос — срок ставится на паузу. Автор отвечает — обращение возвращается на рассмотрение.",
        "steps": [
            ("17", "appeal:A-005", "A-005 глазами автора: ответить на вопрос"),
            ("16", "appeal:A-005", "A-005 глазами ответственного"),
            ("24", "inbox", "Входящие IT-специалиста"),
        ],
    },
    {
        "n": 4, "title": "Автор видит состояние и итог",
        "what": "Статус простыми словами, история, мотивированный отказ с тем, что будет сделано вместо. "
                "После «Реализовано» автор подтверждает результат или возвращает в работу.",
        "steps": [
            ("19", "appeal:A-017", "A-017: мотивированный отказ"),
            ("7", "appeal:A-004", "A-004: подтвердить результат"),
            ("7", "my", "Мои обращения"),
        ],
    },
    {
        "n": 5, "title": "Фильтры и просроченные",
        "what": "Поиск и фильтры по подразделению, категории, статусу и сроку. Просроченные — одним нажатием.",
        "steps": [
            ("1", "registry:?deadline=overdue", "Все просроченные"),
            ("15", "inbox", "Очередь финансового директора"),
        ],
    },
    {
        "n": 6, "title": "Сводка для руководства",
        "what": "Четыре показателя из ТЗ, обращения по типам и статусам, доля закрытых, среднее время первого ответа, "
                "«кто что держит», повторяющиеся темы.",
        "steps": [("1", "dashboard", "Экран собственника")],
    },
]

EXTRAS = [
    ("1", "appeal:A-007", "Эскалация: A-007 дошло до руководства"),
    ("24", "appeal:A-026", "Дубликаты: объединить A-026 с A-007"),
    ("14", "done", "Лента «Сделано по вашим предложениям»"),
    ("30", "appeal:A-028", "Конфиденциально: автор скрыт от ответственного"),
    ("6", "new", "Руководитель регистрирует замечание с совещания"),
    ("23", "integrations", "Интеграции: реализовано, имитация, планы"),
]


def _target_url(target: str) -> str:
    name, _, arg = target.partition(":")
    if name == "appeal":
        return reverse("appeal", args=[arg])
    return reverse(name) + arg


def _login_link(external_id: str, target: str) -> str:
    return f"{reverse('login_as', args=[external_id])}?next={_target_url(target)}"


def landing(request):
    people = {p.external_id: p for p in Employee.objects.select_related("department")}
    scenarios = []
    for scenario in SCENARIOS:
        steps = [
            {"url": _login_link(who, target), "label": label, "who": people.get(who)}
            for who, target, label in scenario["steps"]
        ]
        scenarios.append({**scenario, "steps": steps})
    extras = [{"url": _login_link(who, target), "label": label, "who": people.get(who)} for who, target, label in EXTRAS]
    return render(request, "feedback/landing.html", {
        "scenarios": scenarios, "extras": extras, "next": request.GET.get("next", ""),
        "has_data": bool(people),
    })


def login_as(request, external_id: str):
    employee = get_object_or_404(Employee, external_id=external_id, is_active=True)
    request.session[SESSION_KEY] = employee.external_id
    request.session.pop("seen_sensitive", None)
    if employee.is_head or employee.sees_everything:
        home = reverse("dashboard")
    elif Appeal.objects.filter(assignee=employee, status__in=Appeal.CLOCK_STATUSES).exists():
        home = reverse("inbox")
    else:
        home = reverse("my")
    return redirect(_safe_next(request, home))


def switch_persona(request):
    external_id = request.GET.get("id", "")
    if not external_id:
        request.session.pop(SESSION_KEY, None)
        return redirect("landing")
    return login_as(request, external_id)


@require_POST
def demo_clock(request):
    if not settings.DEMO_MODE:
        raise Http404
    action = request.POST.get("action")
    if action == "reset":
        clock.reset()
        messages.success(request, "Демо-часы возвращены к настоящему времени.")
    else:
        days = 3 if action == "3" else 1
        clock.advance_working_days(days)
        stats = escalation.tick()
        note = f"Время в системе сдвинуто на {days} раб. дн. вперёд."
        if stats["escalations"] or stats["reminders"]:
            note += f" Система сама отправила напоминаний: {stats['reminders']}, эскалаций: {stats['escalations']}."
        messages.success(request, note)
    return redirect(_safe_next(request, reverse("landing")))


@require_POST
def demo_reset(request):
    if not settings.DEMO_MODE:
        raise Http404
    seed.reset_and_seed()
    messages.success(request, "Демо-данные загружены заново, часы возвращены к настоящему времени.")
    return redirect(_safe_next(request, reverse("landing")))


# --------------------------------------------------------------------------- submit


def _form_context(request, values=None) -> dict:
    employee = request.employee
    groups = CategoryGroup.objects.prefetch_related("categories").order_by("sort")
    return {
        "groups": groups,
        "types": Appeal.Type.choices,
        "sources": [choice for choice in Appeal.Source.choices if choice[0] != Appeal.Source.WEB],
        "people": Employee.objects.filter(is_active=True).exclude(pk=employee.pk).select_related("department"),
        "values": values or {"type": Appeal.Type.PROBLEM, "priority": Appeal.Priority.MEDIUM, "published": "on"},
        "calendar": workcal.get_calendar(),
        "max_mb": settings.ATTACHMENT_MAX_BYTES // 1024 // 1024,
    }


@persona_required
def appeal_new(request):
    employee = request.employee
    if request.method != "POST":
        return render(request, "feedback/form.html", _form_context(request))

    data = request.POST
    try:
        category = Category.objects.filter(pk=data.get("category") or 0, is_active=True).first()
        author, registered_by, source = employee, None, Appeal.Source.WEB
        if data.get("on_behalf") and (employee.is_head or employee.sees_everything):
            author = Employee.objects.filter(pk=data.get("author") or 0, is_active=True).first()
            if author is None:
                raise WorkflowError("Выберите сотрудника, со слов которого регистрируете обращение.")
            registered_by = employee
            source = data.get("source") if data.get("source") in Appeal.Source.values else Appeal.Source.MEETING
        about = None
        if data.get("sensitive"):
            about = Employee.objects.filter(pk=data.get("about_person") or 0).first()
        if data.get("type") not in Appeal.Type.values:
            raise WorkflowError("Выберите тип обращения.")
        appeal = workflow.create_appeal(
            author=author, type=data["type"], category=category, text=data.get("text", ""),
            proposed_solution=data.get("proposed_solution", ""),
            priority=data.get("priority") if data.get("priority") in Appeal.Priority.values else Appeal.Priority.MEDIUM,
            confidential=bool(data.get("confidential")), sensitive=bool(data.get("sensitive")), about_person=about,
            published=bool(data.get("published")), registered_by=registered_by, source=source,
            files=request.FILES.getlist("files"),
        )
    except WorkflowError as error:
        messages.error(request, str(error))
        return render(request, "feedback/form.html", _form_context(request, data), status=400)
    return redirect(f"{reverse('appeal', args=[appeal.number])}?receipt=1")


@persona_required
def api_hints(request):
    """While the author types: suggest a category and show similar open requests."""
    text = request.GET.get("q", "")
    category = similar.suggest_category(text)
    candidates = Appeal.objects.filter(permissions.public_q(), status__in=Appeal.OPEN_STATUSES).select_related("category")
    found = similar.find_similar(text, candidates)
    html = render_to_string("feedback/_similar.html", {"similar": found, "me": request.employee}, request=request)
    return JsonResponse({
        "category_id": category.pk if category else None,
        "category_name": category.name if category else "",
        "html": html if found else "",
    })


# --------------------------------------------------------------------------- lists


def _filtered(request, queryset, viewer, now) -> tuple[list[dict], dict]:
    """Apply the search and filters from the query string. Deadline filters are computed in Python."""
    params = request.GET
    search = params.get("q", "").strip()
    if search:
        queryset = queryset.filter(
            Q(text__icontains=search) | Q(number__icontains=search) | Q(decision_reason__icontains=search)
            | Q(result__icontains=search) | Q(next_actions__icontains=search) | Q(proposed_solution__icontains=search)
        )
    if params.get("type") in Appeal.Type.values:
        queryset = queryset.filter(type=params["type"])
    if params.get("status") in Appeal.Status.values:
        queryset = queryset.filter(status=params["status"])
    elif params.get("status") == "open":
        queryset = queryset.filter(status__in=Appeal.OPEN_STATUSES)
    if params.get("priority") in Appeal.Priority.values:
        queryset = queryset.filter(priority=params["priority"])
    if params.get("category", "").isdigit():
        queryset = queryset.filter(category_id=params["category"])
    if params.get("group", "").isdigit():
        queryset = queryset.filter(category__group_id=params["group"])
    if params.get("dept", "").isdigit():
        department = Department.objects.filter(pk=params["dept"]).first()
        if department:
            queryset = queryset.filter(assignee__department_id__in=department.subtree_ids())
    if params.get("author_dept", "").isdigit():
        department = Department.objects.filter(pk=params["author_dept"]).first()
        if department:
            queryset = queryset.filter(author__department_id__in=department.subtree_ids(), is_confidential=False)
    if params.get("assignee", "").isdigit():
        queryset = queryset.filter(assignee_id=params["assignee"])

    rows = _rows(queryset.select_related(*LIST_RELATED).prefetch_related("supporters", "duplicates"), viewer, now)
    deadline = params.get("deadline", "")
    if deadline == "overdue":
        rows = [r for r in rows if r["deadline"]["tone"] == "critical"]
    elif deadline == "today":
        rows = [r for r in rows if r["deadline"]["tone"] == "warning"]
    elif deadline == "escalated":
        rows = [r for r in rows if r["appeal"].escalation_level >= 1 and r["deadline"]["tone"] == "critical"]
    elif deadline == "paused":
        rows = [r for r in rows if r["deadline"]["tone"] == "wait"]

    if params.get("sort") == "new":
        rows.sort(key=lambda r: r["appeal"].created_at, reverse=True)
    else:
        rows.sort(key=lambda r: (r["deadline"]["rank"], -r["appeal"].created_at.timestamp()))
    active = {key: value for key, value in params.items() if value and key != "sort"}
    return rows, active


def _filter_options() -> dict:
    return {
        "types": Appeal.Type.choices,
        "statuses": Appeal.Status.choices,
        "priorities": Appeal.Priority.choices,
        "groups": CategoryGroup.objects.prefetch_related("categories").order_by("sort"),
        "departments": Department.objects.order_by("sort"),
    }


@persona_required
def my(request):
    employee, now = request.employee, clock.now()
    queryset = Appeal.objects.filter(Q(author=employee) | Q(registered_by=employee)).distinct()
    rows, active = _filtered(request, queryset, employee, now)
    rows.sort(key=lambda r: r["appeal"].created_at, reverse=True)
    needs_me = [r for r in rows if r["appeal"].author_id == employee.pk and r["appeal"].status in (S.WAITING, S.IMPLEMENTED)]
    return render(request, "feedback/list.html", {
        "scope": "my", "title": "Мои обращения", "rows": rows, "active": active, "needs_me": needs_me,
        "lead": "Здесь видно, на каком этапе каждое ваше обращение, кто отвечает и к какому сроку.",
    })


@persona_required
def inbox(request):
    employee, now = request.employee, clock.now()
    tab = request.GET.get("tab", "mine")
    base = Appeal.objects.filter(permissions.visible_q(employee)).exclude(author=employee)
    mine = base.filter(assignee=employee, status__in=Appeal.OPEN_STATUSES)
    managed = employee.managed_department_ids()
    department = base.filter(assignee__department_id__in=managed, status__in=Appeal.OPEN_STATUSES)
    if employee.is_leadership:
        escalated = base.filter(escalation_level__gte=2, status__in=Appeal.CLOCK_STATUSES)
    else:
        escalated = base.filter(escalated_to=employee, escalation_level__gte=1, status__in=Appeal.CLOCK_STATUSES)
    exceptions = base.filter(via_default_rule=True, status__in=Appeal.OPEN_STATUSES)

    tabs = [("mine", "Назначено мне", mine.count())]
    if managed:
        tabs.append(("department", "Очередь подразделения", department.count()))
    if managed or employee.is_leadership:
        tabs.append(("escalated", "Эскалировано мне", escalated.count()))
    if employee.is_coordinator:
        tabs.append(("exceptions", "Исключения: не нашлось правила", exceptions.count()))
    chosen = {"department": department, "escalated": escalated, "exceptions": exceptions}.get(tab, mine)
    if tab not in {code for code, _, _ in tabs}:
        tab, chosen = "mine", mine
    rows, active = _filtered(request, chosen, employee, now)
    return render(request, "feedback/list.html", {
        "scope": "inbox", "title": "Входящие", "rows": rows, "active": active, "tabs": tabs, "tab": tab,
        "lead": "Сначала просроченные, затем те, у кого срок ближе.", "options": _filter_options(),
    })


@persona_required
def registry(request):
    employee, now = request.employee, clock.now()
    if not (employee.is_head or employee.sees_everything):
        return redirect("my")
    rows, active = _filtered(request, Appeal.objects.filter(permissions.visible_q(employee)).distinct(), employee, now)
    scope_note = "Все обращения компании." if employee.sees_everything else "Обращения вашего подразделения и ваши собственные."
    return render(request, "feedback/list.html", {
        "scope": "registry", "title": "Все обращения", "rows": rows, "active": active,
        "lead": f"{scope_note} Поиск идёт по тексту, решениям и результатам.", "options": _filter_options(),
        "show_quick": True,
    })


# --------------------------------------------------------------------------- request page


def _get_appeal(request, number: str) -> Appeal:
    appeal = get_object_or_404(
        Appeal.objects.select_related(
            "category__group", "author__department", "assignee__department", "registered_by", "about_person",
            "duplicate_of", "escalated_to", "routing_rule",
        ),
        number=number,
    )
    if not permissions.can_view(request.employee, appeal):
        raise Http404
    return appeal


@persona_required
def appeal_detail(request, number: str):
    employee, now = request.employee, clock.now()
    appeal = _get_appeal(request, number)
    mode = permissions.view_mode(employee, appeal)
    internal = permissions.sees_internal(employee, appeal)

    if appeal.is_sensitive and mode != "author":
        seen = request.session.get("seen_sensitive", [])
        if appeal.number not in seen:
            workflow.log_confidential_view(appeal, employee)
            request.session["seen_sensitive"] = seen + [appeal.number]

    events = appeal.events.select_related("actor")
    if mode == "colleague":
        events = events.none()
    elif not internal:
        events = events.filter(visibility=Event.Visibility.PUBLIC)
    allowed = permissions.actions(employee, appeal)

    candidates = []
    if "reassign" in allowed:
        candidates = [
            person for person in Employee.objects.filter(is_active=True).select_related("department")
            if permissions.can_reassign_to(employee, appeal, person) and person.pk != appeal.assignee_id
        ]
    related = []
    if mode in {"handler", "observer"} and appeal.status in (S.NEW, S.REVIEW, S.WAITING):
        pool = Appeal.objects.filter(permissions.visible_q(employee)).exclude(status=S.DUPLICATE).select_related("category")
        related = similar.find_similar(appeal.text, pool, limit=3, exclude_pk=appeal.pk)

    sees_author = permissions.sees_author(employee, appeal)
    timeline = []
    for event in events:
        if event.actor is None:
            who, role = "Система", ""
        elif event.kind == Event.Kind.SUPPORT:
            who, role = "Коллега", ""
        elif event.actor_id == appeal.author_id:
            who, role = (event.actor.short_name if sees_author else "Автор"), "автор"
        else:
            who, role = event.actor.short_name, event.actor.position
        if event.kind == Event.Kind.STATUS:
            label = f"Статус: {event.to_status_label}"
        elif event.to_status and event.kind != Event.Kind.CREATED:
            label = f"{event.get_kind_display()} → {event.to_status_label}"
        else:
            label = event.get_kind_display()
        timeline.append({"e": event, "who": who, "role": role, "label": label})

    calendar = workcal.get_calendar()
    return render(request, "feedback/detail.html", {
        "appeal": appeal, "mode": mode, "events": timeline, "actions": allowed, "internal": internal,
        "sees_author": sees_author,
        "deadline": deadline_state(appeal, now),
        "attachments": appeal.attachments.all() if mode != "colleague" else [],
        "candidates": candidates, "related": related,
        "duplicates": appeal.duplicates.all(),
        "support_count": appeal.supporters.count(),
        "receipt": request.GET.get("receipt") == "1" and mode in {"author", "observer", "handler"},
        "default_planned": calendar.add_working_days(calendar.effective_day(now), 10).isoformat(),
        "today_iso": timezone.localtime(now).date().isoformat(),
    })


@require_POST
@persona_required
def appeal_action(request, number: str, action: str):
    employee, data = request.employee, request.POST
    appeal = _get_appeal(request, number)
    text = data.get("text", "")
    done = ""
    try:
        if action == "take":
            workflow.take(appeal, employee)
            done = "Обращение взято на рассмотрение. Автор уведомлён."
        elif action == "ask":
            workflow.ask(appeal, employee, text)
            done = "Вопрос отправлен автору. Срок поставлен на паузу до ответа."
        elif action == "answer":
            workflow.answer(appeal, employee, text)
            done = "Ответ отправлен. Обращение вернулось на рассмотрение."
        elif action == "message":
            workflow.message(appeal, employee, text, files=request.FILES.getlist("files"))
            done = "Сообщение добавлено."
        elif action == "note":
            workflow.note(appeal, employee, text)
            done = "Внутренний комментарий добавлен. Автор его не видит."
        elif action == "decide":
            workflow.decide(
                appeal, employee, data.get("decision", ""), data.get("reason", ""),
                next_actions=data.get("next_actions", ""), planned_date=_parse_date(data.get("planned_date", "")),
                alternative=data.get("alternative", ""),
            )
            done = "Решение зафиксировано. Автор уведомлён."
        elif action == "close_praise":
            workflow.close_praise(appeal, employee, text)
            done = "Отзыв передан адресату, обращение закрыто."
        elif action == "start":
            workflow.start(appeal, employee)
            done = "Статус: в работе."
        elif action == "progress":
            workflow.progress(appeal, employee, text, _parse_date(data.get("planned_date", "")))
            done = "Автор увидит новость о ходе реализации."
        elif action == "implement":
            workflow.implement(appeal, employee, text)
            done = "Отмечено как реализованное. Ждём подтверждения автора."
        elif action == "confirm":
            workflow.confirm(appeal, employee)
            done = "Спасибо! Обращение закрыто."
        elif action == "reopen":
            workflow.reopen(appeal, employee, text)
            done = "Обращение возвращено в работу."
        elif action == "not_mine":
            workflow.not_mine(appeal, employee, text)
            messages.success(request, f"Правила применены заново. Новый ответственный: {appeal.assignee.short_name}")
            return redirect("inbox")
        elif action == "reassign":
            target = Employee.objects.filter(pk=data.get("target") or 0).first()
            if target is None:
                raise WorkflowError("Выберите нового ответственного.")
            workflow.reassign(appeal, employee, target, text)
            done = f"Ответственный изменён: {target.short_name}"
        elif action == "extend":
            workflow.extend(appeal, employee, data.get("days"), text)
            done = "Срок продлён. Автор уведомлён о новой дате."
        elif action == "duplicate":
            main = Appeal.objects.filter(number=data.get("main", "").strip().upper()).first()
            if main is None or not permissions.can_view(employee, main):
                raise WorkflowError("Основное обращение с таким номером не найдено.")
            workflow.mark_duplicate(appeal, employee, main, text)
            done = f"Объединено с {main.number}. Автор будет получать новости по основному обращению."
        elif action == "support":
            workflow.support(appeal, employee)
            done = "Ваш голос учтён: тема отмечена как повторяющаяся."
        else:
            raise Http404
    except WorkflowError as error:
        messages.error(request, str(error))
    else:
        messages.success(request, done)
    if not permissions.can_view(employee, appeal):
        return redirect("inbox")
    return redirect(_safe_next(request, reverse("appeal", args=[appeal.number])))


@persona_required
def attachment(request, pk: int):
    item = get_object_or_404(Attachment.objects.select_related("appeal"), pk=pk)
    employee = request.employee
    if not permissions.can_view(employee, item.appeal) or permissions.view_mode(employee, item.appeal) == "colleague":
        raise Http404
    return FileResponse(item.file.open("rb"), as_attachment=True, filename=item.name)


# --------------------------------------------------------------------------- dashboard and feed


@persona_required
def dashboard(request):
    employee, now = request.employee, clock.now()
    if not (employee.is_head or employee.sees_everything):
        return redirect("my")
    appeals = list(
        Appeal.objects.filter(permissions.visible_q(employee)).distinct()
        .select_related(*LIST_RELATED).prefetch_related("supporters", "duplicates")
    )
    data = metrics.summary(appeals, now)
    data["overdue_rows"] = [
        {"appeal": a, "deadline": deadline_state(a, now), "sees_author": permissions.sees_author(employee, a)}
        for a, _ in data["overdue"]
    ]
    done = Appeal.objects.filter(_done_q()).select_related("author", "category").order_by("-implemented_at")[:4]
    return render(request, "feedback/dashboard.html", {
        "m": data, "company_wide": employee.sees_everything, "done": done,
        "scope_note": "Вся компания" if employee.sees_everything else "Ваше подразделение и ваши обращения",
    })


def _done_q() -> Q:
    return (
        permissions.public_q() & Q(status__in=(S.IMPLEMENTED, S.CLOSED))
        & Q(decision__in=(Appeal.Decision.ACCEPTED, Appeal.Decision.ALREADY_DONE)) & ~Q(type=Appeal.Type.PRAISE)
    )


@persona_required
def done_feed(request):
    done = (
        Appeal.objects.filter(_done_q()).select_related("author__department", "category", "assignee")
        .annotate(votes=Count("supporters")).order_by("-implemented_at")
    )
    open_public = (
        Appeal.objects.filter(permissions.public_q(), status__in=(S.NEW, S.REVIEW, S.WAITING, S.DECIDED, S.IN_PROGRESS))
        .exclude(type=Appeal.Type.PRAISE).select_related("category").annotate(votes=Count("supporters"))
        .order_by("-votes", "-created_at")[:12]
    )
    mine = set(request.employee.supported_appeals.values_list("pk", flat=True))
    return render(request, "feedback/done.html", {"done": done, "open_public": open_public, "supported": mine})


@persona_required
def notifications(request):
    employee = request.employee
    items = list(Notification.objects.filter(recipient=employee).select_related("appeal")[:60])
    unread = {n.pk for n in items if n.read_at is None}
    Notification.objects.filter(recipient=employee, read_at__isnull=True).update(read_at=clock.now())
    return render(request, "feedback/notifications.html", {"items": items, "unread": unread})


# --------------------------------------------------------------------------- settings pages


@persona_required
def rules(request):
    rule_list = list(
        RoutingRule.objects.select_related("target_role__holder__deputy", "author_department").prefetch_related("categories")
    )
    counts = dict(Appeal.objects.values_list("routing_rule").annotate(n=Count("pk")))
    type_labels = dict(Appeal.Type.choices)
    coordinator_now = routing.coordinator()
    for rule in rule_list:
        rule.fired = counts.get(rule.pk, 0)
        if rule.target_kind == RoutingRule.Target.ROLE:
            rule.holder_now = rule.target_role.holder if rule.target_role else None
        elif rule.target_kind == RoutingRule.Target.COORDINATOR:
            rule.holder_now = coordinator_now
        else:
            rule.holder_now = None
        conditions = []
        if rule.sensitive_only:
            conditions.append("отмечено «о действиях конкретного человека»")
        if rule.request_type:
            conditions.append(f"тип «{type_labels.get(rule.request_type, rule.request_type)}»")
        names = [c.name for c in rule.categories.all()]
        if names:
            conditions.append("категория: " + ", ".join(f"«{name}»" for name in names))
        if rule.author_department:
            conditions.append(f"автор из «{rule.author_department.name}»")
        if rule.target_kind == RoutingRule.Target.GROUP_ROLE:
            conditions.append("у направления категории есть ответственный")
        rule.conditions_text = "; ".join(conditions) or "любое обращение"

    result, values = None, request.GET
    if values.get("check"):
        category = Category.objects.select_related("group__default_role__holder").filter(pk=values.get("category") or 0).first()
        author = Employee.objects.select_related("department").filter(pk=values.get("author") or 0).first()
        about = Employee.objects.filter(pk=values.get("about") or 0).first()
        if category and author:
            result = routing.route(
                type=values.get("type", Appeal.Type.PROBLEM), category=category, author=author,
                priority=values.get("priority", ""), sensitive=bool(about), about_person=about,
            )
    return render(request, "feedback/rules.html", {
        "rules": rule_list, "result": result, "values": values,
        "groups": CategoryGroup.objects.prefetch_related("categories").order_by("sort"),
        "people": Employee.objects.filter(is_active=True).select_related("department"),
        "types": Appeal.Type.choices,
        "absent": Employee.objects.filter(absent=True, is_active=True).select_related("deputy"),
        "calendar_note": workcal.get_calendar(),
    })


@persona_required
def integrations(request):
    employee = request.employee
    if request.method == "POST":
        if not employee.is_admin:
            messages.error(request, "Переключать интеграции может только администратор.")
            return redirect("integrations")
        code, action = request.POST.get("code", ""), request.POST.get("action", "")
        integration = get_object_or_404(Integration, code=code)
        if action == "toggle" and integration.mode != Integration.Mode.PLANNED:
            integration.enabled = not integration.enabled
            integration.save(update_fields=["enabled"])
            messages.success(request, f"{integration.name}: {'включена' if integration.enabled else 'выключена'}. Ядро продолжает работать.")
        elif action == "import" and code == "bitrix24_directory":
            data = seed.load_json("seed_directory.json")
            stats = bitrix24.import_directory(data["department.get"]["result"], data["user.get"]["result"])
            integration.last_ok_at = clock.now()
            integration.save(update_fields=["last_ok_at"])
            messages.success(request, f"Справочник загружен из файла: подразделений {stats['departments']}, сотрудников {stats['employees']}.")
        return redirect("integrations")

    items = list(Integration.objects.all())
    deliveries = (
        Delivery.objects.select_related("event__appeal", "event__recipient", "integration")
        .order_by("-updated_at", "-id")[:25]
    )
    return render(request, "feedback/integrations.html", {
        "integrations": items,
        "deliveries": deliveries,
        "outbox_total": OutboxEvent.objects.count(),
        "outbox_pending": OutboxEvent.objects.filter(processed_at__isnull=True).count(),
        "delivery_counts": dict(Delivery.objects.values_list("status").annotate(n=Count("pk"))),
        "inapp_total": Notification.objects.count(),
        "telegram_configured": telegram.configured(),
        "telegram_linked": Employee.objects.exclude(telegram_chat_id="").count(),
    })


@persona_required
def profile(request):
    employee = request.employee
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "channel" and request.POST.get("channel") in Employee.Channel.values:
            employee.notify_channel = request.POST["channel"]
            employee.save(update_fields=["notify_channel"])
            messages.success(request, "Канал уведомлений сохранён.")
        elif action == "unlink":
            employee.telegram_chat_id = ""
            employee.save(update_fields=["telegram_chat_id"])
            messages.success(request, "Telegram отвязан.")
        return redirect("profile")
    telegram_on = Integration.objects.filter(code="telegram", enabled=True).exists()
    telegram_url = telegram.link_url(employee) if telegram.configured() and not employee.telegram_chat_id else ""
    return render(request, "feedback/profile.html", {
        "channels": Employee.Channel.choices,
        "telegram_on": telegram_on,
        "telegram_configured": telegram.configured(),
        "telegram_url": telegram_url,
        # segno builds the SVG itself from the link; no user input reaches it unescaped.
        "telegram_qr": mark_safe(telegram.link_qr_svg(telegram_url)) if telegram_url and telegram_on else "",
        "roles": employee.functional_roles.all(),
        "manager": employee.manager(),
    })


@persona_required
def telegram_status(request):
    """Polled by the profile page while it shows the link, so a computer screen notices when the phone links."""
    return JsonResponse({"linked": bool(request.employee.telegram_chat_id)})


@persona_required
def open_admin(request):
    """Reference data is edited in the Django admin. In the demo the admin persona is signed in automatically."""
    if not (settings.DEMO_MODE and request.employee.is_admin):
        messages.error(request, "Справочники и правила меняет администратор системы.")
        return redirect("rules")
    seed.ensure_demo_admin()
    user = get_user_model().objects.get(username=seed.DEMO_ADMIN_USERNAME)
    persona = request.session.get(SESSION_KEY)
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    request.session[SESSION_KEY] = persona
    return redirect(_safe_next(request, "/admin/"))
