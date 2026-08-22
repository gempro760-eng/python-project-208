from django.contrib.auth.models import User
from django.db.models import ProtectedError
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskCRUDTestCase(TestCase):
    fixtures = ("users.json", "statuses.json", "tasks.json", "labels.json")

    def setUp(self):
        self.user1 = User.objects.get(pk=1)
        self.user1.set_password("password123")
        self.user1.save()

        self.user2 = User.objects.get(pk=2)
        self.user2.set_password("password456")
        self.user2.save()

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.label1 = Label.objects.get(pk=1)

        self.task1 = Task.objects.get(pk=1)
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name="Segunda Tarea",
            description="Otra tarea de prueba",
            status=self.status2,
            author=self.user2,
            executor=self.user1,
        )

    def test_task_list_unauthenticated(self):
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    def test_task_list_authenticated(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_task_filter_by_status(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"), {"status": self.status1.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_task_filter_by_executor(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"), {"executor": self.user1.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task1.name)

    def test_task_filter_by_label(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"), {"label": self.label1.pk})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_task_filter_self_tasks(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("tasks_list"), {"self_tasks": "on"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)

    def test_task_detail_view(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.get(reverse("task_detail", kwargs={"pk": self.task1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task1.description)

    def test_task_creation(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("task_create"),
            {
                "name": "Nueva Tarea Creada",
                "description": "Detalles de la nueva tarea",
                "status": self.status1.pk,
                "executor": self.user2.pk,
                "labels": [self.label1.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        new_task = Task.objects.get(name="Nueva Tarea Creada")
        self.assertEqual(new_task.author, self.user1)

    def test_task_update(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("task_update", kwargs={"pk": self.task1.pk}),
            {
                "name": "Tarea Modificada",
                "description": "Nueva descripcion",
                "status": self.status1.pk,
                "executor": self.user1.pk,
                "labels": [self.label1.pk],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.name, "Tarea Modificada")

    def test_task_delete_by_non_author_forbidden(self):
        self.client.login(username="jane_doe", password="password456")
        response = self.client.post(
            reverse("task_delete", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertTrue(Task.objects.filter(pk=self.task1.pk).exists())

    def test_task_delete_by_author(self):
        self.client.login(username="john_doe", password="password123")
        response = self.client.post(
            reverse("task_delete", kwargs={"pk": self.task1.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks_list"))
        self.assertFalse(Task.objects.filter(pk=self.task1.pk).exists())

    def test_user_with_tasks_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.user1.delete()
