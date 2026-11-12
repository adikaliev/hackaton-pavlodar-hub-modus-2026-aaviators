from datetime import date

from feedback.models import Appeal, Event, Notification
from feedback.services import escalation, workflow

from .base import CoreTestCase, local

S = Appeal.Status


class EscalationTests(CoreTestCase):
    """Created Monday 9 Nov; first response is due Wednesday 11 Nov, 18:00."""

    def setUp(self):
        super().setUp()
        self.appeal = self.submit()
        self.owner = self.person(24)
        self.it_head = self.person(23)
        self.ceo = self.person(1)

    def reload(self):
        self.appeal.refresh_from_db()
        return self.appeal

    def test_nothing_happens_before_the_deadline(self):
        self.at(2026, 11, 10)
        self.assertEqual(escalation.tick()["escalations"], 0)
        self.assertEqual(self.reload().escalation_level, 0)

    def test_reminder_on_the_last_day_is_sent_once(self):
        self.at(2026, 11, 11, 9)
        self.assertEqual(escalation.tick()["reminders"], 1)
        self.assertEqual(escalation.tick()["reminders"], 0)
        self.assertTrue(Notification.objects.filter(recipient=self.owner, text__contains="истекает срок").exists())

    def test_one_working_day_overdue_goes_to_the_manager(self):
        self.at(2026, 11, 12, 9, 30)
        escalation.tick()
        appeal = self.reload()
        self.assertEqual(appeal.escalation_level, 1)
        self.assertEqual(appeal.escalated_to, self.it_head)
        event = appeal.events.get(kind=Event.Kind.ESCALATED)
        self.assertEqual(event.created_at, local(2026, 11, 12, 9))  # stamped with the moment it became overdue
        self.assertIn("Бекмуханов", event.text)
        self.assertTrue(Notification.objects.filter(recipient=self.it_head, appeal=appeal).exists())

    def test_three_working_days_overdue_goes_to_leadership(self):
        self.at(2026, 11, 16, 10)  # Monday: Thu, Fri, Mon = 3 working days after the deadline
        escalation.tick()
        appeal = self.reload()
        self.assertEqual(appeal.escalation_level, 2)
        self.assertEqual(appeal.events.filter(kind=Event.Kind.ESCALATED).count(), 2)  # both steps are in the history
        self.assertTrue(Notification.objects.filter(recipient=self.ceo, appeal=appeal).exists())

    def test_weekend_does_not_count_towards_escalation(self):
        self.at(2026, 11, 15, 12)  # Sunday: only Thursday and Friday have passed
        escalation.tick()
        self.assertEqual(self.reload().escalation_level, 1)

    def test_tick_is_idempotent(self):
        self.at(2026, 11, 16, 10)
        escalation.tick()
        events = Event.objects.count()
        notifications = Notification.objects.count()
        self.assertEqual(escalation.tick()["escalations"], 0)
        self.assertEqual(Event.objects.count(), events)
        self.assertEqual(Notification.objects.count(), notifications)

    def test_escalated_manager_can_act_and_a_new_stage_starts_clean(self):
        self.at(2026, 11, 12, 10)
        escalation.tick()
        appeal = self.reload()
        workflow.take(appeal, self.it_head)  # the manager steps in
        self.assertEqual(appeal.status, S.REVIEW)
        self.assertEqual(appeal.escalation_level, 0)
        self.assertEqual(escalation.tick()["escalations"], 0)  # the decision deadline is still ahead

    def test_paused_request_is_not_escalated(self):
        workflow.ask(self.appeal, self.owner, "Какие операции дублируются?")
        self.at(2026, 11, 20)
        escalation.tick()
        self.assertEqual(self.reload().escalation_level, 0)

    def test_missed_planned_date_is_escalated_too(self):
        workflow.decide(self.appeal, self.owner, Appeal.Decision.ACCEPTED, "Проблема подтверждена, берём в работу.",
                        planned_date=date(2026, 11, 10))
        self.at(2026, 11, 11, 10)
        escalation.tick()
        appeal = self.reload()
        self.assertEqual(appeal.escalation_level, 1)
        self.assertIn("Плановая дата", appeal.events.get(kind=Event.Kind.ESCALATED).text)

    def test_request_without_a_manager_in_between_goes_straight_to_leadership(self):
        # A request owned by a direct report of the CEO.
        appeal = self.submit(author="17", category="Регламенты", type=Appeal.Type.IDEA)
        self.assertEqual(appeal.assignee, self.person(30))
        self.at(2026, 11, 12, 10)
        escalation.tick()
        appeal.refresh_from_db()
        self.assertEqual(appeal.escalated_to, self.ceo)

    def test_unconfirmed_result_closes_after_the_confirmation_window(self):
        workflow.decide(self.appeal, self.owner, Appeal.Decision.ALREADY_DONE, "Обмен между системами уже настроен в октябре.")
        self.assertEqual(self.appeal.status, S.IMPLEMENTED)
        self.at(2026, 11, 13)
        self.assertEqual(escalation.tick()["auto_closed"], 0)
        self.at(2026, 11, 17)
        self.assertEqual(escalation.tick()["auto_closed"], 1)
        self.assertEqual(self.reload().status, S.CLOSED)
