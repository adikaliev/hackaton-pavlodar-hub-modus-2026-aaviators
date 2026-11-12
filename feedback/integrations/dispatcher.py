"""Delivers outgoing events to the notification channels that are switched on.

Order of channels for a recipient: Telegram, then Bitrix24. If a channel fails
after retries, the next one is tried. If no channel is on (or none fits the
recipient), nothing is lost: the in-app notification was already written by the
core before this code ran.
"""
from __future__ import annotations

import logging
from datetime import timedelta

from django.utils import timezone

from ..models import Delivery, Employee, Integration, OutboxEvent
from ..services import clock
from .bitrix24 import Bitrix24NotifySimulator
from .telegram import DeliveryError, TelegramChannel

log = logging.getLogger("feedback.integrations")

CHANNELS = {"telegram": TelegramChannel(), "bitrix24_notify": Bitrix24NotifySimulator()}
ORDER = ["telegram", "bitrix24_notify"]
MAX_ATTEMPTS = 3
RETRY_SECONDS = (15, 60)


def _wanted(recipient: Employee) -> list[str]:
    choice = recipient.notify_channel
    if choice == Employee.Channel.INAPP:
        return []
    if choice == Employee.Channel.BITRIX24:
        return ["bitrix24_notify"]
    return ORDER  # "auto" and "telegram": Telegram first, Bitrix24 as the fallback


def _next_channel(event: OutboxEvent, integrations: dict, tried: set[str]) -> str | None:
    if event.recipient is None:
        return None
    for code in _wanted(event.recipient):
        integration = integrations.get(code)
        if code in tried or integration is None or not integration.enabled:
            continue
        if CHANNELS[code].applicable(event.recipient):
            return code
    return None


def _plan(event: OutboxEvent, integrations: dict, tried: set[str]) -> Delivery | None:
    code = _next_channel(event, integrations, tried)
    if code is None:
        return None
    moment = clock.now()
    return Delivery.objects.create(
        event=event, integration=integrations[code], request=CHANNELS[code].build_request(event),
        created_at=moment, updated_at=moment,
    )


def dispatch_pending(limit: int = 200) -> dict:
    stats = {"planned": 0, "sent": 0, "simulated": 0, "failed": 0, "retry": 0}
    integrations = {i.code: i for i in Integration.objects.filter(code__in=ORDER)}

    # 1. New events: choose the first channel that is on and fits the recipient.
    new_events = OutboxEvent.objects.filter(processed_at__isnull=True).select_related("recipient").order_by("id")[:limit]
    for event in new_events:
        if _plan(event, integrations, set()):
            stats["planned"] += 1
        event.processed_at = clock.now()
        event.save(update_fields=["processed_at"])

    # 2. Deliveries that are due: send, retry later, or fall back to the next channel.
    real_now = timezone.now()
    due = Delivery.objects.filter(status=Delivery.Status.PENDING).select_related("event__recipient", "integration")
    for delivery in due.order_by("id")[:limit]:
        if delivery.next_attempt_at and delivery.next_attempt_at > real_now:
            continue
        integration = delivery.integration
        channel = CHANNELS[integration.code]
        delivery.attempts += 1
        delivery.updated_at = clock.now()
        try:
            if not integration.enabled:
                raise DeliveryError("Интеграция выключена")
            delivery.status = channel.send(delivery.request)
            delivery.error = ""
            integration.last_ok_at = clock.now()
            integration.last_error = ""
            integration.save(update_fields=["last_ok_at", "last_error"])
            stats["simulated" if delivery.status == Delivery.Status.SIMULATED else "sent"] += 1
        except DeliveryError as error:
            delivery.error = str(error)[:500]
            integration.last_error = delivery.error
            integration.save(update_fields=["last_error"])
            if delivery.attempts >= MAX_ATTEMPTS or not integration.enabled:
                delivery.status = Delivery.Status.FAILED
                stats["failed"] += 1
                tried = set(delivery.event.deliveries.values_list("integration__code", flat=True))
                if _plan(delivery.event, integrations, tried):
                    stats["planned"] += 1
            else:
                wait = RETRY_SECONDS[min(delivery.attempts - 1, len(RETRY_SECONDS) - 1)]
                delivery.next_attempt_at = real_now + timedelta(seconds=wait)
                stats["retry"] += 1
            log.warning("Delivery %s via %s failed: %s", delivery.pk, integration.code, delivery.error)
        delivery.save()
    return stats
