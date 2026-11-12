from feedback.models import Appeal, Event
from feedback.services import permissions, workflow

from .base import CoreTestCase


class ConfidentialityTests(CoreTestCase):
    def test_confidential_author_is_hidden_from_owner_and_department_head(self):
        appeal = self.submit(author="17", category="Интеграции и IT", confidential=True)
        owner, head = self.person(24), self.person(23)
        self.assertFalse(permissions.sees_author(owner, appeal))
        self.assertFalse(permissions.sees_author(head, appeal))
        self.assertTrue(permissions.sees_author(self.person(21), appeal))  # coordinator
        self.assertTrue(permissions.sees_author(self.person(1), appeal))  # leadership
        self.assertTrue(permissions.sees_author(appeal.author, appeal))
        self.assertFalse(appeal.is_published)  # confidential requests are never shown to colleagues

        self.login("24")
        page = self.client.get(f"/a/{appeal.number}/").content.decode()
        page = page.split("<main", 1)[1]  # the role switcher in the header lists every employee
        self.assertNotIn("Соколова", page)
        self.assertIn("конфиденциальное", page)
        # The owner can still ask the author a question.
        workflow.ask(appeal, owner, "Какие системы вы имеете в виду?")
        self.assertEqual(appeal.status, Appeal.Status.WAITING)

    def test_request_about_a_person_is_invisible_to_that_person(self):
        manager = self.person(3)
        appeal = self.submit(author="5", category="Постановка задач", about_person=manager)
        self.assertTrue(appeal.is_sensitive and appeal.is_confidential)
        self.assertFalse(permissions.can_view(manager, appeal))
        self.assertFalse(Appeal.objects.filter(permissions.visible_q(manager), pk=appeal.pk).exists())
        self.login("3")
        self.assertEqual(self.client.get(f"/a/{appeal.number}/").status_code, 404)
        self.assertNotContains(self.client.get("/all/"), appeal.number)

    def test_views_of_a_sensitive_request_are_logged(self):
        appeal = self.submit(author="5", category="Постановка задач", about_person=self.person(3))
        self.login("21")
        self.client.get(f"/a/{appeal.number}/")
        self.client.get(f"/a/{appeal.number}/")
        self.assertEqual(appeal.events.filter(kind=Event.Kind.ACCESS).count(), 1)  # once per session

    def test_internal_comments_never_reach_the_author(self):
        appeal = self.submit(author="17")
        workflow.note(appeal, appeal.assignee, "Внутренняя заметка для коллег по отделу.")
        self.login("17")
        self.assertNotContains(self.client.get(f"/a/{appeal.number}/"), "Внутренняя заметка")
        self.login("24")
        self.assertContains(self.client.get(f"/a/{appeal.number}/"), "Внутренняя заметка")

    def test_colleague_sees_a_published_request_without_the_thread(self):
        appeal = self.submit(author="17")
        workflow.ask(appeal, appeal.assignee, "Уточните, какие операции дублируются?")
        colleague = self.person(14)
        self.assertEqual(permissions.view_mode(colleague, appeal), "colleague")
        self.login("14")
        response = self.client.get(f"/a/{appeal.number}/")
        self.assertContains(response, "У меня тоже")
        self.assertNotContains(response, "какие операции дублируются")

    def test_unpublished_request_is_closed_to_colleagues(self):
        appeal = self.submit(author="17", published=False)
        self.login("14")
        self.assertEqual(self.client.get(f"/a/{appeal.number}/").status_code, 404)

    def test_department_head_sees_the_queue_of_the_department_only(self):
        it_request = self.submit(author="17", category="Интеграции и IT")
        other = self.submit(author="17", category="Регламенты", type=Appeal.Type.IDEA, published=False)
        it_head = self.person(23)
        visible = Appeal.objects.filter(permissions.visible_q(it_head))
        self.assertIn(it_request, visible)
        self.assertNotIn(other, visible)

    def test_pages_require_a_role(self):
        self.assertEqual(self.client.get("/my/").status_code, 302)
        self.assertEqual(self.client.get("/dashboard/").status_code, 302)
        self.login("7")  # an ordinary employee has no company dashboard
        self.assertEqual(self.client.get("/dashboard/").status_code, 302)
        self.assertEqual(self.client.get("/my/").status_code, 200)
