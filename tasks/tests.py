from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task


class TaskCRUDTestCase(TestCase):
    fixtures = ("users.json", "statuses.json", "tasks.json")

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user1.set_password("password123")
        self.user1.save()

        self.user2 = User.objects.get(pk=2)
        self.user2.set_password("password456")
        self.user2.save()

        self.status = Status.objects.get(pk=1)
        self.task = Task.objects.get(pk=1)

    def test_task_list_unauthenticated(self):
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_task_list_authenticated(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_detail_view(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("task_detail", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)
        self.assertContains(response, self.task.description)

    def test_task_creation(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "Nueva Tarea Creada",
                "description": "Detalles de la nueva tarea",
                "status": self.status.pk,
                "executor": self.user2.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        new_task = Task.objects.get(name="Nueva Tarea Creada")
        self.assertEqual(new_task.author, self.user1)

    def test_task_update(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("task_update", kwargs={"pk": self.task.pk}),
            {
                "name": "Tarea Modificada",
                "description": "Nueva descripcion",
                "status": self.status.pk,
                "executor": self.user1.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Tarea Modificada")

    def test_task_delete_by_non_author_forbidden(self):
        self.client.login(username="jane_doe", password="password456")
        response = self.client.post(reverse("task_delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_author(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(reverse("task_delete", kwargs={"pk": self.task.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_user_with_tasks_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.user1.delete()
