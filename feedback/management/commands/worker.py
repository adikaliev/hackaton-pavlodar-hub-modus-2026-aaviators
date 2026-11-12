import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import close_old_connections

from feedback.services import worker


class Command(BaseCommand):
    help = "Run escalation and the integration dispatcher in a loop (or once with --once)."

    def add_arguments(self, parser):
        parser.add_argument("--once", action="store_true")

    def handle(self, *args, **options):
        while True:
            stats = worker.run_once()
            if any(stats.values()):
                self.stdout.write(str(stats))
            if options["once"]:
                return
            close_old_connections()
            time.sleep(settings.WORKER_INTERVAL_SECONDS)
