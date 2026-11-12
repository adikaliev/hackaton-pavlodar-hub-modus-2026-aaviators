"""Shared fixtures for tests.

The core is tested the way the architecture promises: with every integration
switched off (`CoreTestCase`). Tests that are about integrations switch on only
what they need.
"""
from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from feedback.integrations import ensure_catalog
from feedback.models import Appeal, Category, Employee, Integration
from feedback.services import clock, seed, workcal, workflow

# Monday 9 November 2026, 10:00 local time. No public holidays that week.
MONDAY = (2026, 11, 9, 10, 0)


def local(year, month, day, hour=10, minute=0):
    return timezone.make_aware(datetime(year, month, day, hour, minute))


class CoreTestCase(TestCase):
    """Directory, categories, rules and calendar loaded; no requests; all integrations off."""

    @classmethod
    def setUpTestData(cls):
        seed.seed_calendar()
        seed.seed_directory()
        seed.seed_reference()
        ensure_catalog()
        Integration.objects.update(enabled=False)

    def setUp(self):
        clock.invalidate()
        workcal.invalidate()
        self.at(*MONDAY)
        self.addCleanup(clock.unfreeze)

    def at(self, year, month, day, hour=10, minute=0):
        """Pin the clock to a moment (local time)."""
        clock._local.frozen = local(year, month, day, hour, minute)

    @staticmethod
    def person(external_id) -> Employee:
        return Employee.objects.get(external_id=str(external_id))

    @staticmethod
    def category(name) -> Category:
        return Category.objects.get(name=name)

    def submit(self, author="7", category="Интеграции и IT", type=Appeal.Type.PROBLEM, **extra) -> Appeal:
        text = extra.pop("text", "Сведения приходится вводить дважды в разных системах, это отнимает время.")
        return workflow.create_appeal(
            author=self.person(author), type=type, category=self.category(category), text=text, **extra
        )

    def login(self, external_id):
        self.client.get(f"/as/{external_id}/")
