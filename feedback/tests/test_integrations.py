import json
from unittest import mock

from django.test import override_settings

from feedback.integrations import bitrix24, dispatcher, telegram
from feedback.models import Delivery, Department, Employee, Integration, Notification, OutboxEvent
from feedback.services import seed, workflow

from .base import CoreTestCase


def switch(code, on=True):
    Integration.objects.filter(code=code).update(enabled=on)


class CoreWithoutIntegrationsTests(CoreTestCase):
    """The architecture rule: the core works with every integration switched off."""

    def test_full_cycle_works_and_nothing_leaves_the_system(self):
        self.assertFalse(Integration.objects.filter(enabled=True).exists())
        appeal = self.submit()
        workflow.take(appeal, appeal.assignee)
        stats = dispatcher.dispatch_pending()
        self.assertEqual(Delivery.objects.count(), 0)
        self.assertEqual(stats["sent"] + stats["simulated"], 0)
        self.assertTrue(Notification.objects.filter(recipient=appeal.author).exists())  # in-app is the core
        self.assertFalse(OutboxEvent.objects.filter(processed_at__isnull=True).exists())  # the log does not pile up

    def test_core_never_calls_the_network(self):
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("network call from the core")):
            appeal = self.submit()
            workflow.ask(appeal, appeal.assignee, "Какие операции дублируются?")
            workflow.answer(appeal, appeal.author, "Ввод поставщика.")


class Bitrix24SimulatorTests(CoreTestCase):
    def test_simulator_records_the_exact_rest_call_and_sends_nothing(self):
        switch("bitrix24_notify")
        appeal = self.submit()
        with mock.patch("urllib.request.urlopen", side_effect=AssertionError("the simulator must not send")):
            stats = dispatcher.dispatch_pending()
        self.assertEqual(stats["simulated"], 2)  # the owner and the author
        delivery = Delivery.objects.get(event__recipient=appeal.assignee)
        self.assertEqual(delivery.status, Delivery.Status.SIMULATED)
        self.assertEqual(delivery.request["method"], "im.notify.system.add")
        self.assertEqual(delivery.request["params"]["USER_ID"], "24")
        self.assertIn(appeal.number, delivery.request["params"]["MESSAGE"])

    def test_no_request_text_or_names_leave_the_system(self):
        switch("bitrix24_notify")
        appeal = self.submit(text="Секретная формулировка проблемы с учётной системой.")
        dispatcher.dispatch_pending()
        for delivery in Delivery.objects.all():
            sent = json.dumps(delivery.request, ensure_ascii=False)
            self.assertNotIn("Секретная", sent)
            self.assertNotIn(appeal.author.full_name.split()[-1], sent)

    def test_directory_import_reads_the_bitrix24_response_format(self):
        departments = [
            {"ID": "900", "NAME": "Новый отдел", "SORT": 900, "PARENT": "1", "UF_HEAD": "901"},
        ]
        users = seed.load_json("seed_directory.json")["user.get"]["result"] + [
            {"ID": "901", "ACTIVE": True, "NAME": "Тест", "LAST_NAME": "Тестов", "WORK_POSITION": "Руководитель",
             "UF_DEPARTMENT": [900], "EMAIL": "t@modus.example"},
        ]
        stats = bitrix24.import_directory(departments, users)
        self.assertEqual(stats["employees"], 31)
        department = Department.objects.get(external_id="900")
        self.assertEqual(department.head.full_name, "Тест Тестов")
        self.assertEqual(department.parent.external_id, "1")

    def test_employee_missing_from_the_directory_is_deactivated_not_deleted(self):
        users = [u for u in seed.load_json("seed_directory.json")["user.get"]["result"] if u["ID"] != "5"]
        bitrix24.import_directory([], users)
        self.assertFalse(Employee.objects.get(external_id="5").is_active)


@override_settings(TELEGRAM_BOT_TOKEN="test-token", TELEGRAM_BOT_USERNAME="feedback_bot", PUBLIC_BASE_URL="https://feedback.example.kz")
class TelegramTests(CoreTestCase):
    def setUp(self):
        super().setUp()
        switch("telegram")
        Employee.objects.filter(external_id="7").update(telegram_chat_id="555")

    def test_linked_employee_gets_number_status_and_link_only(self):
        with mock.patch.object(telegram, "call", return_value={"ok": True}) as call:
            appeal = self.submit(text="Секретная формулировка проблемы с учётной системой.")
            stats = dispatcher.dispatch_pending()
        self.assertEqual(stats["sent"], 1)  # only the linked author; the owner has no Telegram
        method, params = call.call_args.args
        self.assertEqual(method, "sendMessage")
        self.assertEqual(params["chat_id"], "555")
        self.assertIn(appeal.number, params["text"])
        self.assertNotIn("Секретная", json.dumps(params, ensure_ascii=False))
        self.assertEqual(params["reply_markup"]["inline_keyboard"][0][0]["url"],
                         f"https://feedback.example.kz/a/{appeal.number}/")

    def test_failed_delivery_is_retried_then_falls_back_to_the_next_channel(self):
        switch("bitrix24_notify")
        with mock.patch.object(telegram, "call", side_effect=telegram.DeliveryError("Telegram недоступен")):
            self.submit()
            dispatcher.dispatch_pending()
            delivery = Delivery.objects.get(integration__code="telegram")
            self.assertEqual((delivery.status, delivery.attempts), (Delivery.Status.PENDING, 1))
            for _ in range(dispatcher.MAX_ATTEMPTS):
                Delivery.objects.filter(pk=delivery.pk).update(next_attempt_at=None)
                dispatcher.dispatch_pending()
        delivery.refresh_from_db()
        self.assertEqual(delivery.status, Delivery.Status.FAILED)
        fallback = Delivery.objects.get(event=delivery.event, integration__code="bitrix24_notify")
        self.assertEqual(fallback.status, Delivery.Status.SIMULATED)
        self.assertIn("недоступен", Integration.objects.get(code="telegram").last_error)

    def test_user_action_does_not_wait_for_telegram(self):
        with mock.patch.object(telegram, "call", side_effect=AssertionError("called during a user action")):
            appeal = self.submit()
            workflow.take(appeal, appeal.assignee)
        self.assertEqual(appeal.status, "review")

    def test_account_is_linked_by_a_one_time_code(self):
        employee = self.person(17)
        url = telegram.link_url(employee)
        code = url.rsplit("=", 1)[1]
        self.assertTrue(url.startswith("https://t.me/feedback_bot?start="))
        reply = telegram.handle_update({"update_id": 1, "message": {"chat": {"id": 777}, "text": f"/start {code}"}})
        employee.refresh_from_db()
        self.assertEqual(employee.telegram_chat_id, "777")
        self.assertEqual(employee.telegram_link_code, "")
        self.assertIn("привязан", reply)
        # The code works once; an unknown chat gets nothing.
        again = telegram.handle_update({"update_id": 2, "message": {"chat": {"id": 888}, "text": f"/start {code}"}})
        self.assertIn("не найден", again)

    def test_bot_does_not_accept_request_text_in_chat(self):
        reply = telegram.handle_update({"update_id": 3, "message": {"chat": {"id": 999}, "text": "У нас проблема с 1С"}})
        self.assertIn("только присылает уведомления", reply)
        self.assertEqual(OutboxEvent.objects.count(), 0)

    def test_employee_can_choose_in_app_only(self):
        Employee.objects.filter(external_id="7").update(notify_channel=Employee.Channel.INAPP)
        with mock.patch.object(telegram, "call", return_value={"ok": True}) as call:
            self.submit()
            dispatcher.dispatch_pending()
        call.assert_not_called()
