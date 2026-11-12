"""Rule-based routing (solution design, section 3.1).

Rules are checked in order and the first match wins. A rule names a role, not a
person; the person is found from the directory. If that person is unavailable
or must not handle the request, the backup chain is used:

    person -> their deputy -> the heads above them -> coordinator -> leadership.

Nobody is ever asked to handle their own request or a request about themselves.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from ..models import Employee, FunctionalRole, RoutingRule

COORDINATOR_ROLE = "coordinator"


@dataclass
class RoutingResult:
    assignee: Employee | None
    rule: RoutingRule | None
    note: str
    via_default: bool = False
    trail: list[str] = field(default_factory=list)


def coordinator() -> Employee | None:
    role = FunctionalRole.objects.filter(code=COORDINATOR_ROLE).select_related("holder").first()
    if role and role.holder:
        return role.holder
    return Employee.objects.filter(access=Employee.Access.COORDINATOR, is_active=True).first()


def leadership() -> list[Employee]:
    return list(Employee.objects.filter(access=Employee.Access.LEADERSHIP, is_active=True))


def _matches(rule: RoutingRule, *, type, category, author, priority, sensitive) -> bool:
    if rule.sensitive_only and not sensitive:
        return False
    if rule.request_type and rule.request_type != type:
        return False
    if rule.priority and rule.priority != priority:
        return False
    rule_categories = {c.pk for c in rule.categories.all()}
    if rule_categories and (category is None or category.pk not in rule_categories):
        return False
    if rule.author_department_id:
        if author is None or author.department_id is None:
            return False
        if author.department_id not in rule.author_department.subtree_ids():
            return False
    if rule.target_kind == RoutingRule.Target.GROUP_ROLE:
        if category is None or category.group is None or category.group.default_role is None:
            return False
    return True


def _target(rule: RoutingRule, *, category, author) -> Employee | None:
    kind = rule.target_kind
    if kind == RoutingRule.Target.ROLE:
        return rule.target_role.holder if rule.target_role else None
    if kind == RoutingRule.Target.AUTHOR_DEPT_HEAD:
        return author.manager() if author else None
    if kind == RoutingRule.Target.AUTHOR_AREA_HEAD:
        if author is None:
            return None
        head = author.area_head()
        return head if head and head.pk != author.pk else author.manager()
    if kind == RoutingRule.Target.GROUP_ROLE:
        return category.group.default_role.holder
    if kind == RoutingRule.Target.COORDINATOR:
        return coordinator()
    return None


def _why_not(person: Employee, *, author, about_person, excluded: set[int]) -> str | None:
    """Reason a person cannot take the request, or None if they can."""
    if about_person is not None and person.pk == about_person.pk:
        return "обращение касается его действий"
    if author is not None and person.pk == author.pk:
        return "это автор обращения"
    if person.pk in excluded:
        return "вернул обращение как не своё"
    if not person.is_active:
        return "больше не работает"
    if person.absent:
        return person.absence_note or "отсутствует"
    return None


def _backup_chain(person: Employee):
    """People to try after `person`, in order."""
    seen = {person.pk}

    def unseen(candidate):
        if candidate is not None and candidate.pk not in seen:
            seen.add(candidate.pk)
            return True
        return False

    if unseen(person.deputy):
        yield person.deputy
    boss, levels = person.manager(), 0
    while boss is not None and levels < 12:  # climb the whole chain, even past people already tried
        if unseen(boss):
            yield boss
        if unseen(boss.deputy):
            yield boss.deputy
        boss, levels = boss.manager(), levels + 1
    coord = coordinator()
    if unseen(coord):
        yield coord
        if unseen(coord.deputy):
            yield coord.deputy
    for leader in leadership():
        if unseen(leader):
            yield leader


def resolve_person(candidate: Employee, *, author=None, about_person=None, excluded=()) -> tuple[Employee | None, str]:
    """Apply the backup chain. Returns the person and a note for the history."""
    excluded = set(excluded)
    reason = _why_not(candidate, author=author, about_person=about_person, excluded=excluded)
    if reason is None:
        return candidate, ""
    for backup in _backup_chain(candidate):
        if _why_not(backup, author=author, about_person=about_person, excluded=excluded) is None:
            return backup, f"вместо {candidate.short_name}: {reason}"
    return None, ""


def route(*, type, category, author, priority="", sensitive=False, about_person=None, excluded=()) -> RoutingResult:
    trail: list[str] = []
    rules = RoutingRule.objects.filter(is_active=True).select_related("target_role__holder", "author_department")
    rules = rules.prefetch_related("categories")
    for rule in rules:
        if not _matches(rule, type=type, category=category, author=author, priority=priority, sensitive=sensitive):
            continue
        candidate = _target(rule, category=category, author=author)
        if candidate is None:
            trail.append(f"Правило №{rule.order} «{rule.name}» подошло, но роль никем не занята — идём дальше.")
            continue
        person, backup_note = resolve_person(candidate, author=author, about_person=about_person, excluded=excluded)
        if person is None:
            trail.append(f"Правило №{rule.order} «{rule.name}»: {candidate.short_name} и замещающие недоступны — идём дальше.")
            continue
        via_default = rule.target_kind == RoutingRule.Target.COORDINATOR and not rule.sensitive_only
        note = f"Правило №{rule.order} «{rule.name}» → {rule.target_label}: {person.short_name}"
        if backup_note:
            note += f" ({backup_note})"
        trail.append(note)
        return RoutingResult(person, rule, note, via_default, trail)

    # Nothing matched and no rule pointed to an available person: leadership is the last resort,
    # so a request is never left without an owner.
    for leader in leadership():
        if _why_not(leader, author=author, about_person=about_person, excluded=set(excluded)) is None:
            note = f"Ни одно правило не дало доступного ответственного → руководство: {leader.short_name}"
            trail.append(note)
            return RoutingResult(leader, None, note, True, trail)
    trail.append("Не найден ни один доступный ответственный.")
    return RoutingResult(None, None, "Ответственный не найден — проверьте справочник и правила", True, trail)
