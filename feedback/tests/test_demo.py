"""The demo database and the six demo scenarios from the organizers' dataset (docs/dataset.md, section 4)."""
from collections import Counter

from django.test import TestCase
from django.utils import timezone

from feedback.models import Appeal, Event, Integration, Notification
from feedback.services import clock, metrics, seed, workcal, workflow

S = Appeal.Status


class DemoDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        seed.reset_and_seed()

    def setUp(self):
        clock.unfreeze()
        clock.invalidate()
        workcal.invalidate()

    def login(self, external_id):
        self.client.get(f"/as/{external_id}/")

    # -- the seed itself --------------------------------------------------------

    def test_dataset_requests_keep_their_statuses(self):
        expected = {row["id"]: row["status"] for row in seed.load_json("seed_requests.json")}
        actual = {a.number: a.get_status_display() for a in Appeal.objects.filter(number__in=expected)}
        self.assertEqual(actual, expected)

    def test_history_is_in_chronological_order_and_never_in_the_future(self):
        now = timezone.now()
        for appeal in Appeal.objects.prefetch_related("events"):
            moments = [event.created_at for event in appeal.events.all()]
            self.assertEqual(moments, sorted(moments), appeal.number)
            self.assertLessEqual(moments[-1], now, appeal.number)

    def test_demo_has_requests_at_every_escalation_level(self):
        levels = Counter(Appeal.objects.filter(status__in=Appeal.CLOCK_STATUSES).values_list("escalation_level", flat=True))
        self.assertGreaterEqual(levels[1], 2)
        self.assertGreaterEqual(levels[2], 2)

    def test_loading_demo_data_never_messages_real_people(self):
        from feedback.models import Delivery, OutboxEvent

        self.assertFalse(OutboxEvent.objects.filter(processed_at__isnull=True).exists())
        self.assertFalse(Delivery.objects.exclude(integration__code="bitrix24_notify").exists())
        self.assertFalse(Delivery.objects.exclude(status=Delivery.Status.SIMULATED).exists())
        self.assertTrue(Delivery.objects.exists())  # the integration log is not empty on first open

    def test_reset_is_repeatable(self):
        before = Appeal.objects.count()
        seed.reset_and_seed()
        self.assertEqual(Appeal.objects.count(), before)
        self.assertEqual(Integration.objects.count(), 9)

    # -- scenario 1: create a request ---------------------------------------------

    def test_scenario_1_create_a_request_with_an_attachment(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        self.login("7")
        category = seed.Category.objects.get(name="Каталог и данные")
        response = self.client.post("/new/", {
            "type": "problem", "category": category.pk, "priority": "medium", "published": "on",
            "text": "В спецификации встречаются два обозначения одной и той же позиции каталога.",
            "files": SimpleUploadedFile("spec.pdf", b"%PDF-1.4 test"),
        })
        appeal = Appeal.objects.order_by("-id").first()
        self.assertRedirects(response, f"/a/{appeal.number}/?receipt=1")
        receipt = self.client.get(f"/a/{appeal.number}/?receipt=1")
        self.assertContains(receipt, "Обращение зарегистрировано")
        self.assertContains(receipt, appeal.assignee.full_name)
        self.assertEqual(appeal.attachments.count(), 1)

    # -- scenario 2: owner by category, alternative when absent ------------------------

    def test_scenario_2_owner_by_rule_and_backup_when_absent(self):
        a016 = Appeal.objects.get(number="A-016")  # training owner is on holiday
        self.assertEqual(a016.assignee.external_id, "21")
        self.assertIn("в отпуске", a016.routing_note)
        a024 = Appeal.objects.get(number="A-024")  # no rule for the category -> coordinator -> manual reassignment
        self.assertTrue(a024.via_default_rule)
        self.assertFalse(a024.auto_assigned)
        self.login("23")
        self.assertContains(self.client.get("/rules/"), "Ничего не подошло")

    # -- scenario 3: status, clarification, comment history --------------------------

    def test_scenario_3_clarification_and_history(self):
        a005 = Appeal.objects.get(number="A-005")
        self.assertEqual(a005.status, S.WAITING)
        self.login("17")  # the author
        page = self.client.get("/a/A-005/")
        self.assertContains(page, "Нужен ваш ответ")
        self.client.post("/a/A-005/do/answer/", {"text": "Речь о счетах и актах; важен этап согласования оплаты."})
        a005.refresh_from_db()
        self.assertEqual(a005.status, S.REVIEW)
        kinds = list(a005.events.values_list("kind", flat=True))
        self.assertIn(Event.Kind.QUESTION, kinds)
        self.assertEqual(kinds[-1], Event.Kind.ANSWER)
        self.assertTrue(Notification.objects.filter(recipient=a005.assignee, text__contains="ответил").exists())

    # -- scenario 4: the author sees the state and the outcome, including a rejection ----

    def test_scenario_4_author_sees_reasoned_rejection_and_confirms_a_result(self):
        self.login("19")
        page = self.client.get("/a/A-017/")
        self.assertContains(page, "Отклонено")
        self.assertContains(page, "нет подходящей свободной площади")
        self.assertContains(page, "Что сделаем вместо этого")
        self.login("7")
        self.assertContains(self.client.get("/my/"), "Нужно ваше действие")
        self.client.post("/a/A-004/do/confirm/")
        self.assertEqual(Appeal.objects.get(number="A-004").status, S.CLOSED)

    # -- scenario 5: filters and overdue -----------------------------------------------

    def test_scenario_5_filters_find_overdue_requests(self):
        self.login("1")
        overdue = self.client.get("/all/?deadline=overdue")
        for number in ("A-007", "A-012", "A-034"):
            self.assertContains(overdue, number)
        self.assertNotContains(overdue, "A-001")
        by_status = self.client.get("/all/?status=rejected")
        self.assertContains(by_status, "A-017")
        self.assertNotContains(by_status, "A-007")
        category = seed.Category.objects.get(name="Обучение")
        by_category = self.client.get(f"/all/?category={category.pk}")
        self.assertContains(by_category, "A-004")
        self.assertNotContains(by_category, "A-005")
        department = Appeal.objects.get(number="A-007").assignee.department
        by_department = self.client.get(f"/all/?dept={department.pk}")
        self.assertContains(by_department, "A-012")
        self.assertNotContains(by_department, "A-017")
        self.assertContains(self.client.get("/all/?q=батареек"), "A-033")

    # -- scenario 6: summary -----------------------------------------------------------

    def test_scenario_6_summary_numbers(self):
        appeals = list(Appeal.objects.select_related("category__group", "assignee__department", "author")
                       .prefetch_related("supporters", "duplicates"))
        data = metrics.summary(appeals, clock.now())
        self.assertEqual(data["total"], 34)
        self.assertEqual({row["label"]: row["count"] for row in data["by_type"]},
                         {"Проблема": 17, "Предложение": 15, "Положительный отзыв": 2})
        self.assertGreater(data["closed_share"], 0)
        self.assertNotEqual(data["avg_response"], "—")
        self.assertGreaterEqual(data["implemented"], 4)
        self.assertEqual(data["holders"][0]["person"].external_id, "24")  # who is holding the most overdue requests
        self.login("1")
        page = self.client.get("/dashboard/")
        for text in ("Доля рассмотренных", "Время до первого ответа", "С зафиксированным результатом",
                     "Реализовано улучшений", "Кто что держит", "Повторяющиеся проблемы"):
            self.assertContains(page, text)

    # -- the demo clock ----------------------------------------------------------------

    def test_fresh_request_escalates_when_the_demo_clock_is_moved(self):
        self.login("7")
        category = seed.Category.objects.get(name="Каталог и данные")
        appeal = workflow.create_appeal(
            author=seed.Employee.objects.get(external_id="7"), type="problem", category=category,
            text="Проверка эскалации: в каталоге две карточки одной позиции.",
        )
        self.client.post("/demo/clock/", {"action": "3"})
        appeal.refresh_from_db()
        self.assertEqual(appeal.escalation_level, 1)  # first response was due in 2 working days
        self.client.post("/demo/clock/", {"action": "3"})
        appeal.refresh_from_db()
        self.assertEqual(appeal.escalation_level, 2)
        self.assertEqual(appeal.events.filter(kind=Event.Kind.ESCALATED).count(), 2)
        self.client.post("/demo/clock/", {"action": "reset"})

    def test_every_page_opens_for_every_key_role(self):
        pages = ["/", "/new/", "/my/", "/inbox/", "/all/", "/dashboard/", "/done/", "/notifications/", "/rules/",
                 "/integrations/", "/profile/"]
        for role in ("1", "7", "24", "21", "23", "15", "3"):
            self.login(role)
            for path in pages:
                self.assertIn(self.client.get(path).status_code, (200, 302), f"{role} {path}")
            for number in Appeal.objects.values_list("number", flat=True):
                self.assertIn(self.client.get(f"/a/{number}/").status_code, (200, 404), f"{role} {number}")
