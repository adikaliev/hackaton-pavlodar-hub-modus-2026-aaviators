from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile

from feedback.models import Appeal, Event, Notification
from feedback.services import workflow
from feedback.services.workflow import WorkflowError

from .base import CoreTestCase, local

S = Appeal.Status


class RegistrationTests(CoreTestCase):
    def test_new_request_gets_number_owner_and_two_deadlines(self):
        appeal = self.submit()  # Monday 9 Nov, problem, medium priority
        self.assertRegex(appeal.number, r"^A-\d{3}$")
        self.assertEqual(appeal.assignee, self.person(24))
        self.assertEqual(appeal.first_response_due, local(2026, 11, 11, 18))  # 2 working days
        self.assertEqual(appeal.decision_due, local(2026, 11, 16, 18))  # 5 working days
        self.assertTrue(appeal.auto_assigned)
        kinds = list(appeal.events.values_list("kind", flat=True))
        self.assertEqual(kinds, [Event.Kind.CREATED, Event.Kind.ASSIGNED])

    def test_idea_has_a_longer_decision_deadline_and_high_priority_halves_both(self):
        idea = self.submit(type=Appeal.Type.IDEA)
        self.assertEqual(idea.decision_due, local(2026, 11, 23, 18))  # 10 working days
        urgent = self.submit(priority=Appeal.Priority.HIGH)
        self.assertEqual(urgent.first_response_due, local(2026, 11, 10, 18))  # 1 working day
        self.assertEqual(urgent.decision_due, local(2026, 11, 12, 18))  # 3 working days

    def test_author_and_owner_are_notified_in_the_app(self):
        appeal = self.submit()
        self.assertTrue(Notification.objects.filter(recipient=appeal.assignee, appeal=appeal).exists())
        self.assertTrue(Notification.objects.filter(recipient=appeal.author, appeal=appeal).exists())

    def test_manager_registers_a_request_on_behalf_of_an_employee(self):
        appeal = self.submit(author="7", registered_by=self.person(6), source=Appeal.Source.MEETING,
                             category="Документооборот")
        self.assertEqual(appeal.author, self.person(7))
        self.assertEqual(appeal.registered_by, self.person(6))
        self.assertIn("совещание", appeal.events.first().text)

    def test_attachments_are_limited_by_type(self):
        good = SimpleUploadedFile("photo.png", b"x" * 10, content_type="image/png")
        appeal = self.submit(files=[good])
        self.assertEqual(appeal.attachments.count(), 1)
        with self.assertRaises(WorkflowError):
            self.submit(files=[SimpleUploadedFile("run.exe", b"x")])

    def test_empty_description_is_rejected(self):
        with self.assertRaises(WorkflowError):
            self.submit(text="  ")


class ReviewTests(CoreTestCase):
    def setUp(self):
        super().setUp()
        self.appeal = self.submit()
        self.owner = self.appeal.assignee
        self.author = self.appeal.author

    def test_question_pauses_the_deadline_and_answer_resumes_it(self):
        self.at(2026, 11, 10)
        workflow.ask(self.appeal, self.owner, "Какие именно операции дублируются?")
        self.assertEqual(self.appeal.status, S.WAITING)
        self.assertIsNone(self.appeal.current_due)  # nobody on our side is on the clock
        self.assertIsNotNone(self.appeal.first_response_at)

        self.at(2026, 11, 13)  # the author took three working days to answer
        workflow.answer(self.appeal, self.author, "Ввод поставщика в заявке и в учётной системе.")
        self.assertEqual(self.appeal.status, S.REVIEW)
        self.assertEqual(self.appeal.decision_due, local(2026, 11, 19, 18))  # moved by the three paused days

    def test_decision_needs_written_reasons(self):
        workflow.take(self.appeal, self.owner)
        with self.assertRaises(WorkflowError):
            workflow.decide(self.appeal, self.owner, Appeal.Decision.REJECTED, "нет")
        self.appeal.refresh_from_db()
        self.assertEqual(self.appeal.status, S.REVIEW)

    def test_accepted_decision_needs_a_planned_date(self):
        with self.assertRaises(WorkflowError):
            workflow.decide(self.appeal, self.owner, Appeal.Decision.ACCEPTED, "Проблема подтверждена, берём в работу.")
        workflow.decide(self.appeal, self.owner, Appeal.Decision.ACCEPTED, "Проблема подтверждена, берём в работу.",
                        next_actions="Настроить обмен между системами.", planned_date=date(2026, 11, 20))
        self.assertEqual(self.appeal.status, S.DECIDED)
        self.assertEqual(self.appeal.current_due, local(2026, 11, 20, 18))

    def test_rejection_keeps_the_reason_and_the_alternative(self):
        workflow.decide(self.appeal, self.owner, Appeal.Decision.REJECTED, "Системы несовместимы без доработки поставщика.",
                        alternative="Сделаем шаблон для ручного переноса.")
        self.assertEqual(self.appeal.status, S.REJECTED)
        self.assertTrue(self.appeal.alternative)
        self.assertIsNotNone(self.appeal.closed_at)

    def test_author_cannot_process_their_own_request(self):
        for action in (workflow.take, ):
            with self.assertRaises(WorkflowError):
                action(self.appeal, self.author)
        with self.assertRaises(WorkflowError):
            workflow.decide(self.appeal, self.author, Appeal.Decision.ACCEPTED, "Сам себе одобряю это обращение.",
                            planned_date=date(2026, 11, 20))

    def test_author_confirms_the_result_or_sends_it_back(self):
        workflow.decide(self.appeal, self.owner, Appeal.Decision.ACCEPTED, "Проблема подтверждена, берём в работу.",
                        planned_date=date(2026, 11, 12))
        workflow.implement(self.appeal, self.owner, "Настроена выгрузка поставщиков из заявки в учётную систему.")
        self.assertEqual(self.appeal.status, S.IMPLEMENTED)

        workflow.reopen(self.appeal, self.author, "Выгрузка не переносит реквизиты банка.")
        self.assertEqual(self.appeal.status, S.IN_PROGRESS)
        self.assertEqual(self.appeal.reopened_count, 1)
        self.assertIsNotNone(self.appeal.current_due)  # a fresh date, so it cannot hang

        workflow.implement(self.appeal, self.owner, "Реквизиты банка добавлены в выгрузку.")
        workflow.confirm(self.appeal, self.author)
        self.assertEqual(self.appeal.status, S.CLOSED)
        self.assertTrue(self.appeal.author_confirmed)

    def test_deadline_can_be_extended_only_once_and_the_author_is_told(self):
        workflow.take(self.appeal, self.owner)
        workflow.extend(self.appeal, self.owner, 2, "Ждём ответ поставщика учётной системы.")
        self.assertEqual(self.appeal.decision_due, local(2026, 11, 18, 18))
        self.assertTrue(Notification.objects.filter(recipient=self.author, text__contains="продлён").exists())
        with self.assertRaises(WorkflowError):
            workflow.extend(self.appeal, self.owner, 2, "Ещё раз продлеваем без причины.")

    def test_internal_note_is_not_public(self):
        workflow.note(self.appeal, self.owner, "Нужно уточнить у бухгалтерии.")
        note = self.appeal.events.get(kind=Event.Kind.NOTE)
        self.assertEqual(note.visibility, Event.Visibility.INTERNAL)

    def test_positive_feedback_takes_the_short_path(self):
        praise = self.submit(author="19", category="Корпоративная среда", type=Appeal.Type.PRAISE,
                             text="Спасибо коллегам за учебные встречи, очень помогает в работе.")
        workflow.close_praise(praise, praise.assignee, "Отзыв передан организаторам встреч.")
        self.assertEqual(praise.status, S.CLOSED)


class RecurringProblemTests(CoreTestCase):
    def test_duplicate_is_merged_and_its_author_follows_the_main_request(self):
        main = self.submit(author="17")
        second = self.submit(author="7")
        workflow.mark_duplicate(second, second.assignee, main, "Та же тема.")
        self.assertEqual(second.status, S.DUPLICATE)
        self.assertEqual(second.duplicate_of, main)
        self.assertIn(self.person(7), main.supporters.all())
        self.assertEqual(main.repeat_count, 2)  # one merged duplicate plus its author's vote

    def test_me_too_counts_once_per_colleague(self):
        appeal = self.submit(author="17")
        colleague = self.person(7)
        workflow.support(appeal, colleague)
        self.assertEqual(appeal.support_count, 1)
        with self.assertRaises(WorkflowError):
            workflow.support(appeal, colleague)
        with self.assertRaises(WorkflowError):
            workflow.support(appeal, appeal.author)
