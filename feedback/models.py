"""Data model of the feedback system.

Naming: an employee's request ("обращение") is called `Appeal` in code, to keep
it apart from Django's HTTP request objects.

Core tables: directory (Department, Employee, FunctionalRole), reference data
(CategoryGroup, Category, RoutingRule, Holiday, SystemSettings), requests
(Appeal, Event, Attachment), in-app notifications (Notification).
Integration tables: Integration, OutboxEvent, Delivery. The core only ever
writes OutboxEvent rows; it never calls an external system.
"""
from __future__ import annotations

from django.db import models


# --------------------------------------------------------------------------- directory


class Department(models.Model):
    name = models.CharField("Название", max_length=200)
    parent = models.ForeignKey(
        "self", verbose_name="Входит в", null=True, blank=True, on_delete=models.SET_NULL, related_name="children"
    )
    head = models.ForeignKey(
        "Employee", verbose_name="Руководитель", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="headed_departments",
    )
    sort = models.IntegerField("Порядок", default=500)
    external_id = models.CharField("ID в Битрикс24", max_length=50, blank=True)

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ["sort", "name"]

    def __str__(self) -> str:
        return self.name

    def chain_up(self) -> list["Department"]:
        """This department and its ancestors, nearest first."""
        chain, node, seen = [], self, set()
        while node is not None and node.pk not in seen:
            chain.append(node)
            seen.add(node.pk)
            node = node.parent
        return chain

    def business_area(self) -> "Department":
        """The top-level branch ("направление") this department belongs to."""
        chain = self.chain_up()
        # chain[-1] is the company root; the branch is the node just below it.
        return chain[-2] if len(chain) >= 2 else chain[-1]

    def subtree_ids(self) -> list[int]:
        ids, queue = [], [self.pk]
        children: dict[int | None, list[int]] = {}
        for pk, parent_id in Department.objects.values_list("pk", "parent_id"):
            children.setdefault(parent_id, []).append(pk)
        while queue:
            pk = queue.pop()
            if pk in ids:
                continue
            ids.append(pk)
            queue.extend(children.get(pk, []))
        return ids


class Employee(models.Model):
    class Access(models.TextChoices):
        EMPLOYEE = "employee", "Сотрудник"
        COORDINATOR = "coordinator", "Координатор"
        LEADERSHIP = "leadership", "Руководство"
        ADMIN = "admin", "Администратор"

    class Channel(models.TextChoices):
        AUTO = "auto", "Автоматически (Telegram → Битрикс24)"
        TELEGRAM = "telegram", "Telegram"
        BITRIX24 = "bitrix24", "Битрикс24"
        INAPP = "inapp", "Только в системе"

    full_name = models.CharField("ФИО", max_length=200)
    position = models.CharField("Должность", max_length=200, blank=True)
    department = models.ForeignKey(
        Department, verbose_name="Подразделение", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="employees",
    )
    access = models.CharField("Уровень доступа", max_length=20, choices=Access.choices, default=Access.EMPLOYEE)
    deputy = models.ForeignKey(
        "self", verbose_name="Заместитель", null=True, blank=True, on_delete=models.SET_NULL, related_name="deputy_for"
    )
    absent = models.BooleanField("Отсутствует", default=False)
    absence_note = models.CharField("Причина отсутствия", max_length=200, blank=True, help_text="Например: в отпуске")
    is_active = models.BooleanField("Работает", default=True)
    email = models.EmailField("Рабочая почта", blank=True)
    external_id = models.CharField("ID в Битрикс24", max_length=50, blank=True)
    notify_channel = models.CharField("Канал уведомлений", max_length=20, choices=Channel.choices, default=Channel.AUTO)
    telegram_chat_id = models.CharField("Telegram chat id", max_length=50, blank=True)
    telegram_link_code = models.CharField("Код привязки Telegram", max_length=40, blank=True)
    sort = models.IntegerField("Порядок", default=500)

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["sort", "full_name"]

    def __str__(self) -> str:
        return self.full_name

    @property
    def short_name(self) -> str:
        """"Фамилия И." from "Имя Фамилия"."""
        parts = self.full_name.split()
        if len(parts) >= 2:
            return f"{parts[-1]} {parts[0][0]}."
        return self.full_name

    @property
    def available(self) -> bool:
        return self.is_active and not self.absent

    @property
    def is_head(self) -> bool:
        return self.headed_departments.exists()

    @property
    def is_coordinator(self) -> bool:
        return self.access == self.Access.COORDINATOR

    @property
    def is_leadership(self) -> bool:
        return self.access == self.Access.LEADERSHIP

    @property
    def is_admin(self) -> bool:
        return self.access == self.Access.ADMIN

    @property
    def sees_everything(self) -> bool:
        return self.access in {self.Access.COORDINATOR, self.Access.LEADERSHIP}

    def manager(self) -> "Employee | None":
        """The nearest department head above this person (never the person themself)."""
        if self.department is None:
            return None
        for dept in self.department.chain_up():
            if dept.head_id and dept.head_id != self.pk:
                return dept.head
        return None

    def area_head(self) -> "Employee | None":
        """Head of the employee's business area ("руководитель направления")."""
        if self.department is None:
            return None
        return self.department.business_area().head

    def managed_department_ids(self) -> list[int]:
        ids: list[int] = []
        for dept in self.headed_departments.all():
            ids.extend(dept.subtree_ids())
        return sorted(set(ids))

    @property
    def role_label(self) -> str:
        if self.access != self.Access.EMPLOYEE:
            return self.get_access_display()
        return "Руководитель подразделения" if self.is_head else "Сотрудник"


class FunctionalRole(models.Model):
    """A responsibility a routing rule points to. The holder can change without touching rules."""

    code = models.SlugField("Код", max_length=60, unique=True)
    name = models.CharField("Роль", max_length=200)
    holder = models.ForeignKey(
        Employee, verbose_name="Кто исполняет", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="functional_roles",
    )

    class Meta:
        verbose_name = "Роль ответственного"
        verbose_name_plural = "Роли ответственных"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


# --------------------------------------------------------------------------- reference data


class CategoryGroup(models.Model):
    name = models.CharField("Направление", max_length=200)
    sort = models.IntegerField("Порядок", default=500)
    default_role = models.ForeignKey(
        FunctionalRole, verbose_name="Ответственный за направление", null=True, blank=True, on_delete=models.SET_NULL,
        help_text="Получает обращения категорий, у которых нет собственного правила.",
    )

    class Meta:
        verbose_name = "Направление обращений"
        verbose_name_plural = "Направления обращений"
        ordering = ["sort", "name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField("Категория", max_length=200)
    group = models.ForeignKey(
        CategoryGroup, verbose_name="Направление", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="categories",
    )
    first_response_days = models.PositiveIntegerField("Первый ответ, раб. дней", default=2)
    problem_decision_days = models.PositiveIntegerField("Решение по проблеме, раб. дней", default=5)
    idea_decision_days = models.PositiveIntegerField("Решение по предложению, раб. дней", default=10)
    keywords = models.TextField(
        "Ключевые слова", blank=True, help_text="Через запятую. По ним система подсказывает категорию по тексту."
    )
    is_active = models.BooleanField("Используется", default=True)
    sort = models.IntegerField("Порядок", default=500)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["group__sort", "sort", "name"]

    def __str__(self) -> str:
        return self.name


class RoutingRule(models.Model):
    class Target(models.TextChoices):
        ROLE = "role", "Роль ответственного"
        AUTHOR_DEPT_HEAD = "author_dept_head", "Руководитель подразделения автора"
        AUTHOR_AREA_HEAD = "author_area_head", "Руководитель направления автора"
        GROUP_ROLE = "group_role", "Ответственный за направление категории"
        COORDINATOR = "coordinator", "Координатор"

    order = models.PositiveIntegerField("Порядок проверки", default=100)
    name = models.CharField("Правило", max_length=200)
    is_active = models.BooleanField("Включено", default=True)
    # Conditions. An empty condition means "any".
    sensitive_only = models.BooleanField("Только обращения о действиях конкретного человека", default=False)
    request_type = models.CharField("Тип обращения", max_length=20, blank=True)
    categories = models.ManyToManyField(Category, verbose_name="Категории", blank=True)
    author_department = models.ForeignKey(
        Department, verbose_name="Подразделение автора", null=True, blank=True, on_delete=models.SET_NULL
    )
    priority = models.CharField("Приоритет", max_length=20, blank=True)
    # Target.
    target_kind = models.CharField("Кому", max_length=30, choices=Target.choices, default=Target.ROLE)
    target_role = models.ForeignKey(
        FunctionalRole, verbose_name="Роль", null=True, blank=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Правило маршрутизации"
        verbose_name_plural = "Правила маршрутизации"
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return f"№{self.order}. {self.name}"

    @property
    def target_label(self) -> str:
        if self.target_kind == self.Target.ROLE and self.target_role:
            return self.target_role.name
        return self.get_target_kind_display()


class Holiday(models.Model):
    """An exception to the Mon–Fri working week: a public holiday or a working weekend day."""

    date = models.DateField("Дата", unique=True)
    name = models.CharField("Название", max_length=200, blank=True)
    is_working = models.BooleanField(
        "Рабочий день", default=False, help_text="Отметьте для перенесённых рабочих суббот; иначе день считается выходным."
    )

    class Meta:
        verbose_name = "День календаря"
        verbose_name_plural = "Календарь: праздники и переносы"
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.date:%d.%m.%Y} — {self.name}"


class SystemSettings(models.Model):
    """Single-row table with the settings an administrator can change without a developer."""

    weekend_days = models.CharField(
        "Выходные дни недели", max_length=20, default="5,6", help_text="Номера дней, 0 — понедельник. По умолчанию суббота и воскресенье."
    )
    work_start_hour = models.PositiveIntegerField("Начало рабочего дня, час", default=9)
    work_end_hour = models.PositiveIntegerField("Конец рабочего дня, час", default=18)
    escalate_head_after = models.PositiveIntegerField("Эскалация руководителю: просрочка, раб. дней", default=1)
    escalate_leadership_after = models.PositiveIntegerField("Эскалация руководству: просрочка, раб. дней", default=3)
    high_priority_factor = models.FloatField("Множитель сроков для высокого приоритета", default=0.5)
    confirm_days = models.PositiveIntegerField("Дней автору на подтверждение результата", default=7)
    clock_offset_minutes = models.IntegerField(
        "Сдвиг демо-часов, минут", default=0, help_text="Только для демонстрации: «перемотка» времени вперёд."
    )

    class Meta:
        verbose_name = "Настройки системы"
        verbose_name_plural = "Настройки системы"

    def __str__(self) -> str:
        return "Настройки системы"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        from .services import clock, workcal

        clock.invalidate()
        workcal.invalidate()

    @classmethod
    def load(cls) -> "SystemSettings":
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# --------------------------------------------------------------------------- requests


class Appeal(models.Model):
    class Type(models.TextChoices):
        PROBLEM = "problem", "Проблема"
        IDEA = "idea", "Предложение"
        PRAISE = "praise", "Положительный отзыв"

    class Status(models.TextChoices):
        NEW = "new", "Новое"
        REVIEW = "review", "На рассмотрении"
        WAITING = "waiting", "Ожидает уточнения"
        DECIDED = "decided", "Решение принято"
        IN_PROGRESS = "in_progress", "В работе"
        IMPLEMENTED = "implemented", "Реализовано"
        REJECTED = "rejected", "Отклонено"
        DUPLICATE = "duplicate", "Дубликат"
        CLOSED = "closed", "Закрыто"

    class Priority(models.TextChoices):
        HIGH = "high", "Высокий"
        MEDIUM = "medium", "Средний"
        LOW = "low", "Низкий"

    class Source(models.TextChoices):
        WEB = "web", "Форма в системе"
        MEETING = "meeting", "Совещание"
        CALL = "call", "Звонок"
        EMAIL = "email", "Письмо"
        TALK = "talk", "Устный разговор"
        CHAT = "chat", "Переписка в чате"

    class Decision(models.TextChoices):
        ACCEPTED = "accepted", "Принято"
        REJECTED = "rejected", "Отклонено"
        ALREADY_DONE = "already_done", "Уже сделано"

    OPEN_STATUSES = (Status.NEW, Status.REVIEW, Status.WAITING, Status.DECIDED, Status.IN_PROGRESS, Status.IMPLEMENTED)
    FINAL_STATUSES = (Status.REJECTED, Status.DUPLICATE, Status.CLOSED)
    # Statuses where a deadline is running and someone on our side has to act.
    CLOCK_STATUSES = (Status.NEW, Status.REVIEW, Status.DECIDED, Status.IN_PROGRESS)

    number = models.CharField("Номер", max_length=20, unique=True)
    type = models.CharField("Тип", max_length=20, choices=Type.choices)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT, related_name="appeals")
    text = models.TextField("Описание")
    proposed_solution = models.TextField("Предлагаемое решение", blank=True)
    priority = models.CharField("Приоритет", max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)

    author = models.ForeignKey(Employee, verbose_name="Автор", on_delete=models.PROTECT, related_name="appeals")
    registered_by = models.ForeignKey(
        Employee, verbose_name="Зарегистрировал", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="registered_appeals",
    )
    source = models.CharField("Источник", max_length=20, choices=Source.choices, default=Source.WEB)
    is_confidential = models.BooleanField("Конфиденциально", default=False)
    about_person = models.ForeignKey(
        Employee, verbose_name="Касается действий сотрудника", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="appeals_about",
    )
    is_sensitive = models.BooleanField("О действиях конкретного человека", default=False)
    is_published = models.BooleanField("Видно коллегам", default=True)

    assignee = models.ForeignKey(
        Employee, verbose_name="Ответственный", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="assigned_appeals",
    )
    routing_rule = models.ForeignKey(
        RoutingRule, verbose_name="Сработавшее правило", null=True, blank=True, on_delete=models.SET_NULL
    )
    routing_note = models.CharField("Как назначен ответственный", max_length=500, blank=True)
    auto_assigned = models.BooleanField("Назначено правилами без ручного шага", default=True)
    via_default_rule = models.BooleanField("Дошло до правила по умолчанию", default=False)

    created_at = models.DateTimeField("Создано")
    first_response_due = models.DateTimeField("Срок первого ответа", null=True, blank=True)
    first_response_at = models.DateTimeField("Первый ответ", null=True, blank=True)
    decision_due = models.DateTimeField("Срок решения", null=True, blank=True)
    decided_at = models.DateTimeField("Решение принято", null=True, blank=True)
    planned_date = models.DateField("Плановая дата реализации", null=True, blank=True)
    implemented_at = models.DateTimeField("Реализовано", null=True, blank=True)
    closed_at = models.DateTimeField("Закрыто", null=True, blank=True)
    paused_at = models.DateTimeField("Срок приостановлен с", null=True, blank=True)
    deadline_extended = models.BooleanField("Срок продлевался", default=False)

    decision = models.CharField("Решение", max_length=20, choices=Decision.choices, blank=True)
    decision_reason = models.TextField("Обоснование решения", blank=True)
    next_actions = models.TextField("Дальнейшие действия", blank=True)
    alternative = models.TextField("Что сделаем вместо этого", blank=True)
    result = models.TextField("Что сделано", blank=True)
    author_confirmed = models.BooleanField("Автор подтвердил результат", null=True, blank=True)
    reopened_count = models.PositiveIntegerField("Возвратов в работу", default=0)

    escalation_level = models.PositiveSmallIntegerField("Уровень эскалации", default=0)
    escalated_to = models.ForeignKey(
        Employee, verbose_name="Эскалировано руководителю", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="escalated_appeals",
    )
    reminded_on = models.DateField("Напоминание отправлено", null=True, blank=True)

    duplicate_of = models.ForeignKey(
        "self", verbose_name="Дубликат обращения", null=True, blank=True, on_delete=models.SET_NULL,
        related_name="duplicates",
    )
    supporters = models.ManyToManyField(Employee, verbose_name="Поддержали («у меня тоже»)", blank=True, related_name="supported_appeals")

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.number} · {self.get_type_display()}"

    # -- presentation helpers -------------------------------------------------

    @property
    def title(self) -> str:
        text = " ".join(self.text.split())
        first = text.split(". ")[0].rstrip(".")
        if len(first) > 110:
            first = first[:107].rsplit(" ", 1)[0] + "…"
        return first

    @property
    def is_open(self) -> bool:
        return self.status in self.OPEN_STATUSES

    @property
    def author_status_text(self) -> str:
        """Plain-language wording the author sees (solution design, section 3.2)."""
        s = self.Status
        if self.type == self.Type.PRAISE and self.status == s.CLOSED:
            return "Спасибо! Отзыв передан адресату"
        return {
            s.NEW: "Получено, ждёт первого ответа",
            s.REVIEW: "Рассматривается",
            s.WAITING: "Нужен ваш ответ",
            s.DECIDED: "Принято, готовится реализация",
            s.IN_PROGRESS: "Реализуется",
            s.IMPLEMENTED: "Сделано — подтвердите, что проблема решена",
            s.REJECTED: "Отклонено — см. обоснование",
            s.DUPLICATE: "Объединено с другим обращением",
            s.CLOSED: "Закрыто",
        }[self.status]

    @property
    def stage(self) -> int:
        """The owner's three stages: 1 consideration, 2 decision, 3 implementation, 4 finished."""
        s = self.Status
        return {
            s.NEW: 1, s.REVIEW: 1, s.WAITING: 1, s.DECIDED: 2, s.IN_PROGRESS: 3, s.IMPLEMENTED: 3,
            s.REJECTED: 4, s.DUPLICATE: 4, s.CLOSED: 4,
        }[self.status]

    @property
    def support_count(self) -> int:
        return self.supporters.count()

    @property
    def repeat_count(self) -> int:
        """How many times the problem was raised: duplicates merged in plus "me too" votes."""
        return self.duplicates.count() + self.supporters.count()

    # -- deadlines ------------------------------------------------------------

    @property
    def deadline_kind(self) -> str:
        s = self.Status
        if self.status == s.NEW:
            return "Первый ответ"
        if self.status == s.REVIEW:
            return "Решение"
        if self.status in (s.DECIDED, s.IN_PROGRESS):
            return "Реализация"
        return ""

    @property
    def current_due(self):
        """The deadline that is running now, or None when nobody on our side is on the clock."""
        from .services import workcal

        s = self.Status
        if self.status == s.NEW:
            return self.first_response_due
        if self.status == s.REVIEW:
            return self.decision_due
        if self.status in (s.DECIDED, s.IN_PROGRESS) and self.planned_date:
            return workcal.get_calendar().end_of_day(self.planned_date)
        return None

    def overdue_days(self, now=None) -> int | None:
        """None when not overdue; otherwise working days past the deadline (0 = overdue today)."""
        from .services import clock, workcal

        due = self.current_due
        if due is None:
            return None
        now = now or clock.now()
        if now <= due:
            return None
        return workcal.get_calendar().working_days_after(due, now)

    def days_left(self, now=None) -> int | None:
        from .services import clock, workcal

        due = self.current_due
        if due is None:
            return None
        now = now or clock.now()
        if now > due:
            return None
        return workcal.get_calendar().working_days_until(now, due)


class Event(models.Model):
    """History of a request. It is the timeline, the thread with the author and the audit log."""

    class Kind(models.TextChoices):
        CREATED = "created", "Зарегистрировано"
        ASSIGNED = "assigned", "Назначен ответственный"
        STATUS = "status", "Изменён статус"
        MESSAGE = "message", "Сообщение"
        QUESTION = "question", "Вопрос автору"
        ANSWER = "answer", "Ответ автора"
        NOTE = "note", "Внутренний комментарий"
        DECISION = "decision", "Решение"
        PROGRESS = "progress", "Ход реализации"
        RESULT = "result", "Результат"
        CONFIRMED = "confirmed", "Автор подтвердил"
        REOPENED = "reopened", "Возвращено в работу"
        ESCALATED = "escalated", "Эскалация"
        REMINDER = "reminder", "Напоминание"
        EXTENDED = "extended", "Срок продлён"
        DUPLICATE = "duplicate", "Объединение"
        SUPPORT = "support", "У меня тоже"
        ACCESS = "access", "Просмотр"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Видно автору"
        INTERNAL = "internal", "Только участникам рассмотрения"

    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField("Когда")
    actor = models.ForeignKey(Employee, verbose_name="Кто", null=True, blank=True, on_delete=models.SET_NULL)
    kind = models.CharField("Событие", max_length=20, choices=Kind.choices)
    visibility = models.CharField("Видимость", max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    text = models.TextField("Текст", blank=True)
    from_status = models.CharField(max_length=20, blank=True)
    to_status = models.CharField(max_length=20, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "Журнал действий"
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return f"{self.appeal.number}: {self.get_kind_display()}"

    @property
    def to_status_label(self) -> str:
        return dict(Appeal.Status.choices).get(self.to_status, "")

    @property
    def is_system(self) -> bool:
        return self.actor_id is None


class Attachment(models.Model):
    appeal = models.ForeignKey(Appeal, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField("Файл", upload_to="attachments/%Y/%m/")
    name = models.CharField("Имя файла", max_length=255)
    size = models.PositiveIntegerField("Размер, байт", default=0)
    uploaded_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField("Загружен")

    class Meta:
        verbose_name = "Вложение"
        verbose_name_plural = "Вложения"
        ordering = ["created_at", "id"]

    def __str__(self) -> str:
        return self.name


class Notification(models.Model):
    """In-app notification. Part of the core: it works with every integration switched off."""

    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="notifications")
    appeal = models.ForeignKey(Appeal, null=True, blank=True, on_delete=models.CASCADE, related_name="notifications")
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления в системе"
        ordering = ["-created_at", "-id"]

    def __str__(self) -> str:
        return self.text


# --------------------------------------------------------------------------- integrations


class Integration(models.Model):
    class Mode(models.TextChoices):
        REAL = "real", "Реализовано"
        SIMULATOR = "simulator", "Имитация"
        PLANNED = "planned", "В планах"

    code = models.SlugField("Код", max_length=40, unique=True)
    name = models.CharField("Интеграция", max_length=200)
    kind = models.CharField("Вид", max_length=100)
    mode = models.CharField("Режим", max_length=20, choices=Mode.choices, default=Mode.PLANNED)
    enabled = models.BooleanField("Включена", default=False)
    description = models.TextField("Описание", blank=True)
    when_off = models.CharField("Что происходит, когда выключена", max_length=300, blank=True)
    config = models.JSONField("Настройки", default=dict, blank=True)
    last_ok_at = models.DateTimeField("Последняя успешная операция", null=True, blank=True)
    last_error = models.CharField("Последняя ошибка", max_length=500, blank=True)
    sort = models.IntegerField(default=500)

    class Meta:
        verbose_name = "Интеграция"
        verbose_name_plural = "Интеграции"
        ordering = ["sort", "name"]

    def __str__(self) -> str:
        return self.name


class OutboxEvent(models.Model):
    """Outgoing event log. The core writes here; switched-on integrations read from here."""

    created_at = models.DateTimeField()
    kind = models.CharField(max_length=40)
    appeal = models.ForeignKey(Appeal, null=True, blank=True, on_delete=models.CASCADE, related_name="outbox")
    recipient = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.CASCADE)
    payload = models.JSONField(default=dict)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Исходящее событие"
        verbose_name_plural = "Журнал исходящих событий"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.kind} #{self.pk}"


class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Ждёт отправки"
        SENT = "sent", "Отправлено"
        SIMULATED = "simulated", "Имитация: запрос записан"
        FAILED = "failed", "Не доставлено"

    event = models.ForeignKey(OutboxEvent, on_delete=models.CASCADE, related_name="deliveries")
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE, related_name="deliveries")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    attempts = models.PositiveIntegerField(default=0)
    next_attempt_at = models.DateTimeField(null=True, blank=True)
    request = models.JSONField("Запрос во внешнюю систему", default=dict, blank=True)
    error = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        verbose_name = "Доставка"
        verbose_name_plural = "Журнал интеграций"
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.integration.code}: {self.get_status_display()}"
