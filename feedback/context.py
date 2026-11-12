from django.conf import settings

from .models import Appeal, Employee, Notification
from .services import clock


def shell(request):
    """Data every page needs: who is "logged in", navigation, the bell and the demo clock."""
    if request.path.startswith("/admin/"):
        return {}
    employee = getattr(request, "employee", None)
    context = {
        "me": employee,
        "demo_mode": settings.DEMO_MODE,
        "system_now": clock.localnow(),
        "clock_shifted": clock.offset_minutes() != 0,
        "personas": Employee.objects.filter(is_active=True).select_related("department").order_by("sort"),
    }
    if employee is None:
        return context
    manages = employee.is_head or employee.sees_everything
    inbox_count = Appeal.objects.filter(assignee=employee, status__in=Appeal.CLOCK_STATUSES).count()
    context.update({
        "unread_count": Notification.objects.filter(recipient=employee, read_at__isnull=True).count(),
        "inbox_count": inbox_count,
        "show_inbox": manages or inbox_count or Appeal.objects.filter(assignee=employee).exists(),
        "show_registry": manages,
        "show_dashboard": manages,
        "can_register_for_others": manages,
        "nav": request.resolver_match.url_name if request.resolver_match else "",
    })
    return context
