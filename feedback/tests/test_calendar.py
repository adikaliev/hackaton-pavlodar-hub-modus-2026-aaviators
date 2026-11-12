from datetime import date

from feedback.models import Holiday, SystemSettings
from feedback.services import clock, workcal

from .base import CoreTestCase, local


class WorkingCalendarTests(CoreTestCase):
    def setUp(self):
        super().setUp()
        self.calendar = workcal.get_calendar()

    def test_weekends_and_public_holidays_are_days_off(self):
        self.assertFalse(self.calendar.is_working_day(date(2026, 11, 14)))  # Saturday
        self.assertFalse(self.calendar.is_working_day(date(2026, 12, 16)))  # Independence Day
        self.assertFalse(self.calendar.is_working_day(date(2026, 10, 26)))  # Republic Day fell on Sunday
        self.assertTrue(self.calendar.is_working_day(date(2026, 11, 12)))

    def test_deadline_is_the_end_of_the_nth_working_day(self):
        due = self.calendar.due_after(local(2026, 11, 12, 13), 2)  # Thursday + 2 working days
        self.assertEqual(due, local(2026, 11, 16, 18))  # Monday, end of day

    def test_deadline_skips_a_holiday(self):
        due = self.calendar.due_after(local(2026, 10, 23, 11), 1)  # Friday; Monday 26 Oct is a day off
        self.assertEqual(due, local(2026, 10, 27, 18))

    def test_request_registered_on_a_day_off_starts_on_the_next_working_day(self):
        due = self.calendar.due_after(local(2026, 11, 14, 12), 2)  # Saturday -> counts from Monday
        self.assertEqual(due, local(2026, 11, 18, 18))

    def test_overdue_is_counted_in_working_days(self):
        due = local(2026, 11, 13, 18)  # Friday evening
        self.assertEqual(self.calendar.working_days_after(due, local(2026, 11, 13, 19)), 0)
        self.assertEqual(self.calendar.working_days_after(due, local(2026, 11, 15, 12)), 0)  # weekend does not count
        self.assertEqual(self.calendar.working_days_after(due, local(2026, 11, 16, 9)), 1)
        self.assertEqual(self.calendar.working_days_after(due, local(2026, 11, 18, 9)), 3)

    def test_working_hours_between_ignore_nights_and_weekends(self):
        hours = self.calendar.working_hours_between(local(2026, 11, 13, 16), local(2026, 11, 16, 11))
        self.assertEqual(hours, 4)  # Friday 16-18 and Monday 9-11

    def test_calendar_is_a_setting_not_code(self):
        Holiday.objects.create(date=date(2026, 11, 12), name="Корпоративный выходной")
        settings = SystemSettings.load()
        settings.weekend_days = "4,5"  # Friday and Saturday
        settings.save()
        calendar = workcal.get_calendar()
        self.assertFalse(calendar.is_working_day(date(2026, 11, 12)))
        self.assertFalse(calendar.is_working_day(date(2026, 11, 13)))
        self.assertTrue(calendar.is_working_day(date(2026, 11, 15)))  # Sunday now works

    def test_demo_clock_moves_forward_by_working_days(self):
        clock.unfreeze()  # use the real clock with an offset
        before = clock.now()
        clock.advance_working_days(3)
        after = clock.now()
        self.assertEqual(self.calendar.count_working_days(clock.timezone.localtime(before).date(),
                                                          clock.timezone.localtime(after).date()), 3)
        clock.reset()
