import json

from django import template
from django.utils import timezone

from ..models import Appeal

register = template.Library()

STATUS_TONE = {
    Appeal.Status.NEW: "new", Appeal.Status.REVIEW: "work", Appeal.Status.WAITING: "wait",
    Appeal.Status.DECIDED: "work", Appeal.Status.IN_PROGRESS: "work", Appeal.Status.IMPLEMENTED: "good",
    Appeal.Status.REJECTED: "muted", Appeal.Status.DUPLICATE: "muted", Appeal.Status.CLOSED: "good",
}


@register.filter
def dt(value):
    """Local date and time: 12.11.2026 14:05."""
    if not value:
        return "—"
    return timezone.localtime(value).strftime("%d.%m.%Y %H:%M")


@register.filter
def day(value):
    """Local date: 12.11.2026. Accepts a date or a datetime."""
    if not value:
        return "—"
    if hasattr(value, "hour"):
        value = timezone.localtime(value)
    return value.strftime("%d.%m.%Y")


@register.filter
def status_tone(status):
    return STATUS_TONE.get(status, "muted")


@register.filter
def pretty_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


@register.filter
def filesize(size):
    if size < 1024:
        return f"{size} Б"
    if size < 1024 * 1024:
        return f"{size / 1024:.0f} КБ"
    return f"{size / 1024 / 1024:.1f} МБ".replace(".", ",")


@register.simple_tag
def query(request, **changes):
    """The current query string with some parameters replaced (for filter links)."""
    params = request.GET.copy()
    for key, value in changes.items():
        if value in (None, ""):
            params.pop(key, None)
        else:
            params[key] = value
    encoded = params.urlencode()
    return f"?{encoded}" if encoded else "?"
