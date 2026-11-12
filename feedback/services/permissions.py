"""Who sees what and who may do what (solution design, section 5)."""
from __future__ import annotations

from django.db.models import Q

from ..models import Appeal, Employee

S = Appeal.Status


def public_q() -> Q:
    """Requests colleagues may see: the author allowed it, and it is not confidential."""
    return Q(is_published=True, is_confidential=False, is_sensitive=False)


def visible_q(emp: Employee) -> Q:
    """Requests an employee works with: as author, assignee, department head, coordinator or leadership."""
    not_about_me = ~Q(about_person=emp)
    if emp.sees_everything:
        return not_about_me
    q = Q(author=emp) | Q(registered_by=emp) | Q(assignee=emp) | Q(escalated_to=emp)
    managed = emp.managed_department_ids()
    if managed:
        q |= Q(assignee__department_id__in=managed, is_sensitive=False)
    return q & not_about_me


def is_author(emp: Employee, appeal: Appeal) -> bool:
    return appeal.author_id == emp.pk


def is_handler(emp: Employee, appeal: Appeal) -> bool:
    """May process the request: the assignee, the heads above them, leadership."""
    if appeal.about_person_id == emp.pk or appeal.author_id == emp.pk:
        return False
    if appeal.assignee_id == emp.pk or appeal.escalated_to_id == emp.pk or emp.is_leadership:
        return True
    if appeal.is_sensitive or appeal.assignee is None:
        return False
    return appeal.assignee.department_id in emp.managed_department_ids()


def can_view(emp: Employee, appeal: Appeal) -> bool:
    if appeal.about_person_id == emp.pk:
        return False
    if is_author(emp, appeal) or appeal.registered_by_id == emp.pk or emp.sees_everything:
        return True
    if is_handler(emp, appeal):
        return True
    return appeal.is_published and not appeal.is_confidential and not appeal.is_sensitive


def view_mode(emp: Employee, appeal: Appeal) -> str:
    """'author', 'handler', 'observer' (sees everything, does not process) or 'colleague'."""
    if is_author(emp, appeal):
        return "author"
    if is_handler(emp, appeal):
        return "handler"
    if emp.sees_everything or appeal.registered_by_id == emp.pk:
        return "observer"
    return "colleague"


def sees_author(emp: Employee, appeal: Appeal) -> bool:
    """In confidential mode the author's name is hidden from the assignee and the department head."""
    if not appeal.is_confidential:
        return True
    return is_author(emp, appeal) or appeal.registered_by_id == emp.pk or emp.sees_everything


def sees_internal(emp: Employee, appeal: Appeal) -> bool:
    """Internal comments: the people handling the request, the coordinator and leadership. Never the author."""
    if is_author(emp, appeal):
        return False
    return is_handler(emp, appeal) or emp.sees_everything


def can_reassign_to(emp: Employee, appeal: Appeal, target: Employee) -> bool:
    if target.pk in {appeal.author_id, appeal.about_person_id} or not target.is_active:
        return False
    if emp.is_leadership or emp.is_coordinator:
        return True
    return target.department_id in emp.managed_department_ids()


def can_support(emp: Employee, appeal: Appeal) -> bool:
    """"Me too": anyone but the author and the assignee may back an open request the author made visible."""
    if not (appeal.is_open and appeal.is_published) or appeal.is_confidential or appeal.is_sensitive:
        return False
    if emp.pk in {appeal.author_id, appeal.assignee_id}:
        return False
    return not appeal.supporters.filter(pk=emp.pk).exists()


def actions(emp: Employee, appeal: Appeal) -> set[str]:
    """Names of the actions the employee may take on the request right now."""
    allowed = _role_actions(emp, appeal)
    if can_support(emp, appeal):
        allowed.add("support")
    return allowed


def _role_actions(emp: Employee, appeal: Appeal) -> set[str]:
    allowed: set[str] = set()
    status, mode = appeal.status, view_mode(emp, appeal)
    is_praise = appeal.type == Appeal.Type.PRAISE

    if mode == "author":
        if status in Appeal.OPEN_STATUSES:
            allowed.add("message")
        if status == S.WAITING:
            allowed.add("answer")
        if status == S.IMPLEMENTED:
            allowed |= {"confirm", "reopen"}
        return allowed

    if mode == "handler":
        allowed.add("note")
        if status in Appeal.OPEN_STATUSES:
            allowed.add("message")
        if status == S.NEW:
            allowed.add("take")
        if status in (S.NEW, S.REVIEW):
            allowed.add("ask")
            if is_praise:
                allowed.add("close_praise")
        if status in (S.NEW, S.REVIEW, S.WAITING):
            allowed.add("duplicate")
            if not is_praise:
                allowed.add("decide")
        if status == S.REVIEW and not appeal.deadline_extended:
            allowed.add("extend")
        if status == S.DECIDED:
            allowed.add("start")
        if status in (S.DECIDED, S.IN_PROGRESS):
            allowed |= {"progress", "implement"}
        if status in (S.NEW, S.REVIEW, S.WAITING, S.DECIDED, S.IN_PROGRESS):
            if appeal.assignee_id == emp.pk:
                allowed.add("not_mine")
            if emp.is_leadership or emp.is_coordinator or emp.is_head:
                allowed.add("reassign")
        return allowed

    if mode == "observer" and emp.is_coordinator:
        allowed.add("note")
        if status in (S.NEW, S.REVIEW, S.WAITING, S.DECIDED, S.IN_PROGRESS):
            allowed.add("reassign")
        if status in (S.NEW, S.REVIEW, S.WAITING):
            allowed.add("duplicate")
        return allowed

    return allowed
