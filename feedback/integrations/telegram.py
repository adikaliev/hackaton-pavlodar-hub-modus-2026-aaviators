"""Telegram: the only real external integration.

* Notifications carry the request number, the status and a link. No request
  text and no names (Telegram's servers are outside Kazakhstan).
* An employee links their account with a one-time code: the profile page shows
  `t.me/<bot>?start=<code>` as a button and as a QR code, and the bot ties the
  chat to the employee record.
  An unlinked chat gets nothing and can do nothing.

The bot token comes from the environment (`TELEGRAM_BOT_TOKEN`) and is never
stored in the database or written to the integration log.
"""
from __future__ import annotations

import json
import secrets
import urllib.error
import urllib.request
from urllib.parse import urlparse

import segno
from django.conf import settings

from ..models import Delivery, Employee, Integration

API = "https://api.telegram.org/bot{token}/{method}"
TIMEOUT_SECONDS = 10


class DeliveryError(Exception):
    pass


def configured() -> bool:
    return bool(settings.TELEGRAM_BOT_TOKEN)


def call(method: str, params: dict) -> dict:
    """One Bot API call. Raises DeliveryError with a message that is safe to show and log."""
    if not configured():
        raise DeliveryError("Не задан TELEGRAM_BOT_TOKEN в .env")
    request = urllib.request.Request(
        API.format(token=settings.TELEGRAM_BOT_TOKEN, method=method),
        data=json.dumps(params).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        try:
            description = json.loads(error.read().decode("utf-8")).get("description", "")
        except (ValueError, OSError):
            description = ""
        raise DeliveryError(f"Telegram ответил {error.code}: {description}".strip()) from None
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise DeliveryError(f"Telegram недоступен: {getattr(error, 'reason', error)}") from None
    if not body.get("ok"):
        raise DeliveryError(f"Telegram отклонил запрос: {body.get('description', '')}")
    return body


def _link_is_public(url: str) -> bool:
    host = urlparse(url).hostname or ""
    return host not in {"localhost", "127.0.0.1", "0.0.0.0", ""} and "." in host


class TelegramChannel:
    code = "telegram"

    def applicable(self, recipient) -> bool:
        return bool(recipient and recipient.telegram_chat_id and configured())

    def build_request(self, event) -> dict:
        payload = event.payload
        url = f"{settings.PUBLIC_BASE_URL}{payload['path']}"
        text = f"Обращение {payload['number']}: статус «{payload['status']}»."
        params: dict = {"chat_id": event.recipient.telegram_chat_id, "text": text}
        if _link_is_public(url):
            params["reply_markup"] = {"inline_keyboard": [[{"text": "Открыть", "url": url}]]}
        else:  # Telegram rejects buttons that point to a local address
            params["text"] = f"{text}\n{url}"
        return {"method": "sendMessage", "params": params}

    def send(self, request: dict) -> str:
        call(request["method"], request["params"])
        return Delivery.Status.SENT


def link_code(employee: Employee) -> str:
    """One-time code for the `t.me/<bot>?start=<code>` link."""
    if not employee.telegram_link_code:
        employee.telegram_link_code = secrets.token_urlsafe(12)
        employee.save(update_fields=["telegram_link_code"])
    return employee.telegram_link_code


def link_url(employee: Employee) -> str:
    if not settings.TELEGRAM_BOT_USERNAME:
        return ""
    return f"https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={link_code(employee)}"


def link_qr_svg(url: str) -> str:
    """The same one-time link as a QR code, for linking from a computer: scan it with the phone's camera.

    Drawn on our server as inline SVG, so the code never goes to an online QR service.
    """
    if not url:
        return ""
    qr = segno.make(url, error="m")
    return qr.svg_inline(scale=5, border=3, dark="#1f1f1c", light="#ffffff", svgclass="qr",
                         title="QR-код для привязки Telegram")


def handle_update(update: dict) -> str | None:
    """Process one update. Only `/start <code>` does anything; request text is never accepted in chat."""
    message = update.get("message") or {}
    chat_id = str((message.get("chat") or {}).get("id") or "")
    text = (message.get("text") or "").strip()
    if not chat_id:
        return None
    if text.startswith("/start") and len(text.split()) == 2:
        code = text.split()[1]
        employee = Employee.objects.filter(telegram_link_code=code, is_active=True).first() if code else None
        if employee is None:
            return "Код не найден или уже использован. Откройте ссылку из своего профиля в системе ещё раз."
        Employee.objects.filter(telegram_chat_id=chat_id).exclude(pk=employee.pk).update(telegram_chat_id="")
        employee.telegram_chat_id = chat_id
        employee.telegram_link_code = ""
        employee.save(update_fields=["telegram_chat_id", "telegram_link_code"])
        return "Аккаунт привязан. Сюда будут приходить номер обращения, статус и ссылка — без текста обращений."
    return ("Этот бот только присылает уведомления. Обращения подаются в системе: "
            "так их текст не остаётся в переписке.")


def poll_updates() -> int:
    """Fetch new updates (long polling without waiting) and process them. Returns how many were handled."""
    integration = Integration.objects.filter(code="telegram").first()
    if integration is None or not integration.enabled or not configured():
        return 0
    offset = int(integration.config.get("offset", 0))
    body = call("getUpdates", {"offset": offset, "timeout": 0, "allowed_updates": ["message"]})
    handled = 0
    for update in body.get("result", []):
        offset = max(offset, int(update["update_id"]) + 1)
        reply = handle_update(update)
        chat_id = ((update.get("message") or {}).get("chat") or {}).get("id")
        if reply and chat_id:
            try:
                call("sendMessage", {"chat_id": chat_id, "text": reply})
            except DeliveryError:
                pass
        handled += 1
    if handled:
        integration.config = {**integration.config, "offset": offset}
        integration.save(update_fields=["config"])
    return handled
