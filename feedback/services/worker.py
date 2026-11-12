"""Background work: escalation and delivery of outgoing events.

Two ways to run it:

* `python manage.py worker` — a separate process (the production way);
* a daemon thread inside the web process (`INLINE_WORKER=1`, the default for the
  demo), so one command is enough to see everything work.

Either way a user action never waits for this code.
"""
from __future__ import annotations

import logging
import threading
import time

from django.conf import settings
from django.db import close_old_connections

log = logging.getLogger("feedback.worker")

_started = False
_lock = threading.Lock()


def run_once() -> dict:
    from ..integrations import dispatcher, telegram
    from . import escalation

    stats = dict(escalation.tick())
    try:
        stats["telegram_updates"] = telegram.poll_updates()
    except telegram.DeliveryError as error:
        log.warning("Telegram polling failed: %s", error)
    stats.update(dispatcher.dispatch_pending())
    return stats


def _loop() -> None:
    while True:
        try:
            run_once()
        except Exception:  # the loop must survive anything: it is what keeps requests from being lost
            log.exception("Worker iteration failed")
        finally:
            close_old_connections()
        time.sleep(settings.WORKER_INTERVAL_SECONDS)


def ensure_started() -> None:
    global _started
    if _started or not settings.INLINE_WORKER:
        return
    with _lock:
        if _started:
            return
        _started = True
        threading.Thread(target=_loop, name="feedback-worker", daemon=True).start()
        log.info("Inline worker started (every %s s)", settings.WORKER_INTERVAL_SECONDS)
