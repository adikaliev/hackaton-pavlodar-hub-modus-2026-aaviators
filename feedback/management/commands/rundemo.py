from django.core.management import call_command
from django.core.management.base import BaseCommand

from feedback.services import seed


class Command(BaseCommand):
    help = "One command for the jury: create the database, load demo data if it is empty, start the server."

    def add_arguments(self, parser):
        parser.add_argument("addrport", nargs="?", default="127.0.0.1:8000")
        parser.add_argument("--noreload", action="store_true")

    def handle(self, *args, **options):
        call_command("migrate", interactive=False, verbosity=0)
        if not seed.is_seeded():
            self.stdout.write("Loading demo data...")
            seed.reset_and_seed()
        call_command("runserver", options["addrport"], use_reloader=not options["noreload"])
