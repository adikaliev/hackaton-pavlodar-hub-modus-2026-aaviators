from feedback.models import Appeal, Employee, FunctionalRole
from feedback.services import routing, seed, workflow

from .base import CoreTestCase


class DatasetRoutingTests(CoreTestCase):
    """The demo rules must reproduce the organizers' "conditional owner" for all 20 requests."""

    def test_rules_reproduce_all_twenty_dataset_assignments(self):
        reference = seed.load_json("seed_reference.json")
        rows = seed.load_json("seed_requests.json")
        self.assertEqual(len(rows), 20)
        for row in rows:
            author = self.person(reference["dataset_authors"][row["author_role"]])
            expected = reference["dataset_assignees"][row["assignee_role"]]
            if expected == "head":
                expected_person = author.manager()
            elif expected == "area":
                expected_person = author.area_head()
            else:
                expected_person = self.person(expected)
            result = routing.route(
                type=seed.TYPES[row["type"]], category=self.category(row["category"]), author=author,
                priority=seed.PRIORITIES[row["priority"]],
            )
            self.assertEqual(result.assignee, expected_person, f"{row['id']}: {result.note}")
            self.assertFalse(result.via_default, row["id"])


class RoutingRuleTests(CoreTestCase):
    def route(self, category, author="7", type=Appeal.Type.PROBLEM, **extra):
        return routing.route(type=type, category=self.category(category), author=self.person(author), **extra)

    def test_rule_order_decides_between_two_matching_rules(self):
        # Same category: positive feedback goes to HR (rule 2), an idea to the head of administration (rule 12).
        praise = self.route("Корпоративная среда", "19", Appeal.Type.PRAISE)
        idea = self.route("Корпоративная среда", "19", Appeal.Type.IDEA)
        self.assertEqual(praise.assignee, self.person(21))
        self.assertEqual(idea.assignee, self.person(18))

    def test_absent_owner_is_replaced_by_the_deputy(self):
        Employee.objects.filter(external_id="29").update(absent=True, absence_note="в отпуске")
        result = self.route("Обучение", "12", Appeal.Type.IDEA)
        self.assertEqual(result.assignee, self.person(21))
        self.assertIn("в отпуске", result.note)

    def test_chain_goes_to_the_manager_when_the_deputy_is_also_absent(self):
        Employee.objects.filter(external_id__in=["24", "23"]).update(absent=True)
        result = self.route("Интеграции и IT")
        self.assertEqual(result.assignee, self.person(22))  # technical director, head of the area

    def test_category_without_a_rule_goes_to_the_owner_of_its_group(self):
        result = self.route("Рабочее место и оборудование", "26", Appeal.Type.IDEA)
        self.assertEqual(result.assignee, self.person(18))
        self.assertEqual(result.rule.order, 15)

    def test_nothing_matched_goes_to_the_coordinator(self):
        result = self.route("Объекты и выезды", "27")
        self.assertEqual(result.assignee, self.person(21))
        self.assertTrue(result.via_default)

    def test_request_about_a_person_never_reaches_that_person(self):
        about = self.person(3)  # the author's own manager
        result = self.route("Постановка задач", "5", sensitive=True, about_person=about)
        self.assertEqual(result.assignee, self.person(21))  # HR
        # Even when the request is about the HR manager herself, she is skipped.
        result = self.route("Постановка задач", "5", sensitive=True, about_person=self.person(21))
        self.assertNotEqual(result.assignee, self.person(21))
        self.assertIsNotNone(result.assignee)

    def test_nobody_handles_their_own_request(self):
        # The head of purchasing files a request that rule 13 would send to "the author's department head".
        result = self.route("Межотдельное взаимодействие", "6")
        self.assertEqual(result.assignee, self.person(2))  # commercial director, one level up
        # The IT specialist files an IT request: it goes to the deputy, not to the author.
        self.assertEqual(self.route("Интеграции и IT", "24").assignee, self.person(23))

    def test_unfilled_role_falls_through_to_the_next_rule(self):
        FunctionalRole.objects.filter(code="it").update(holder=None)
        result = self.route("Интеграции и IT")
        self.assertIsNotNone(result.assignee)
        self.assertTrue(any("роль никем не занята" in line for line in result.trail))

    def test_not_mine_reruns_the_rules_without_that_person(self):
        appeal = self.submit(category="Интеграции и IT")
        specialist = self.person(24)
        self.assertEqual(appeal.assignee, specialist)
        workflow.not_mine(appeal, specialist, "Это вопрос учётной политики, а не IT.")
        appeal.refresh_from_db()
        self.assertEqual(appeal.assignee, self.person(23))  # the deputy named in the backup chain
        self.assertFalse(appeal.auto_assigned)
        self.assertNotIn(appeal.status, Appeal.FINAL_STATUSES)  # nothing is closed on the author

    def test_manager_reassigns_only_within_own_department(self):
        appeal = self.submit(category="Интеграции и IT")
        it_head = self.person(23)
        with self.assertRaises(workflow.WorkflowError):
            workflow.reassign(appeal, it_head, self.person(17), "Передаю в бухгалтерию для оценки.")
        appeal.escalated_to = None
        workflow.reassign(appeal, it_head, it_head, "Беру на себя: нужен доступ к настройкам.")
        appeal.refresh_from_db()
        self.assertEqual(appeal.assignee, it_head)
        self.assertIn("вручную", appeal.routing_note)
