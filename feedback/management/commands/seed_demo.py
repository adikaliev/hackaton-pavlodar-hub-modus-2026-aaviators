from django.core.management.base import BaseCommand

from feedback.services import seed


class Command(BaseCommand):
    help = "Rebuild the demo database from the seed files in data/."

    def add_arguments(self, parser):
        parser.add_argument("--if-empty", action="store_true", help="Do nothing if the database already has data.")

    def handle(self, *args, **options):
        if options["if_empty"] and seed.is_seeded():
            self.stdout.write("Demo data is already loaded.")
            return
        stats = seed.reset_and_seed()
        self.stdout.write(self.style.SUCCESS(f"Demo data loaded: {stats}"))
