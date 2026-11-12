"""Bitrix24 on our side of the wire: a simulator and the directory import.

We have no access to the client's portal, so nothing here opens a network
connection. The notification channel records the exact REST call it would make;
the directory import reads JSON in the response format of `department.get` and
`user.get`, so the same code can later be fed from the real API.
"""
from __future__ import annotations

from django.conf import settings

from ..models import Delivery, Department, Employee

NOTIFY_METHOD = "im.notify.system.add"


class Bitrix24NotifySimulator:
    code = "bitrix24_notify"

    def applicable(self, recipient) -> bool:
        return bool(recipient and recipient.external_id)

    def build_request(self, event) -> dict:
        payload = event.payload
        url = f"{settings.PUBLIC_BASE_URL}{payload['path']}"
        return {
            "method": NOTIFY_METHOD,
            "params": {
                "USER_ID": event.recipient.external_id,
                "MESSAGE": f"Обращение {payload['number']}: статус «{payload['status']}». [URL={url}]Открыть[/URL]",
                "TAG": f"FEEDBACK|{payload['number']}",
            },
        }

    def send(self, request: dict) -> str:
        return Delivery.Status.SIMULATED  # nothing is sent: the request stays in the integration log


def import_directory(departments: list[dict], users: list[dict]) -> dict:
    """Upsert departments and employees from `department.get` / `user.get` results."""
    # Departments already known count as parents too, so a partial import keeps the tree intact.
    by_id: dict[str, Department] = {d.external_id: d for d in Department.objects.exclude(external_id="")}
    for row in departments:
        dept, _ = Department.objects.update_or_create(
            external_id=str(row["ID"]),
            defaults={"name": row["NAME"], "sort": int(row.get("SORT") or 500)},
        )
        by_id[str(row["ID"])] = dept
    for row in departments:
        parent = by_id.get(str(row.get("PARENT") or ""))
        dept = by_id[str(row["ID"])]
        if dept.parent_id != (parent.pk if parent else None):
            dept.parent = parent
            dept.save(update_fields=["parent"])

    people: dict[str, Employee] = {}
    for index, row in enumerate(users):
        dept_ids = row.get("UF_DEPARTMENT") or []
        department = by_id.get(str(dept_ids[0])) if dept_ids else None
        full_name = " ".join(part for part in (row.get("NAME"), row.get("LAST_NAME")) if part)
        person, _ = Employee.objects.update_or_create(
            external_id=str(row["ID"]),
            defaults={
                "full_name": full_name, "position": row.get("WORK_POSITION") or "", "department": department,
                "email": row.get("EMAIL") or "", "is_active": bool(row.get("ACTIVE", True)), "sort": index,
            },
        )
        people[str(row["ID"])] = person

    for row in departments:
        head_id = str(row.get("UF_HEAD") or "")
        head = people.get(head_id) or (Employee.objects.filter(external_id=head_id).first() if head_id else None)
        dept = by_id[str(row["ID"])]
        if dept.head_id != (head.pk if head else None):
            dept.head = head
            dept.save(update_fields=["head"])

    if users:
        Employee.objects.exclude(external_id="").exclude(external_id__in=list(people)).update(is_active=False)
    return {"departments": len(departments), "employees": len(people)}
